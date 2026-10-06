"""Gate-first MLP experiment. No full-comparison methods are launched here."""
from __future__ import annotations

import copy
import hashlib
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn

from .continual_stable import (
    ROLE_CAL, ROLE_EVAL, ROLE_FIT, assign_persistent_roles,
    build_persistent_tasks, client_for_each_row, fit_frozen_preprocessor, split_audit,
)
from .data import load_sampled_csv_dataset_with_provenance, is_benign_label
from .validation import reproducible_non_iid_client_partitions

TASKS = {
    "reconnaissance": {"Aggressive_Scan", "SYN_Stealth_Scan", "TCP_Port_Scan", "Service_Version_Detection", "OS_Fingerprinting"},
    "flooding": {"SYN_Flood", "TCP_Flood", "UDP_Flood", "ICMP_Flood", "PSHACK_Flood", "SynonymousIP_Flood"},
    "low_rate_rare": {"Slowloris_Scan", "ICMP_Fragmentation"},
    "post_rare_vulnerability": {"Vulnerability_Scan"},
}
BENIGN = {"Benign", "benign", "Normal", "normal", "B", "0"}
RARE = TASKS["low_rate_rare"]


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)


class TrafficMLP(nn.Module):
    def __init__(self, inputs, classes):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(inputs, 64), nn.ReLU(),
                                    nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, classes))

    def forward(self, x):
        return self.layers(x)


def masked_logits(logits, seen):
    mask = torch.ones(logits.shape[1], dtype=torch.bool, device=logits.device)
    mask[list(seen)] = False
    return logits.masked_fill(mask.unsqueeze(0), -1e9)


def train_local(global_model, x, y, rows, seen, config, lr, rng):
    local = copy.deepcopy(global_model)
    rows = np.asarray(rows, dtype=int)
    if not len(rows):
        return local, []
    local.train()
    optimizer = torch.optim.Adam(local.parameters(), lr=lr, weight_decay=config["weight_decay"])
    losses = []
    for _ in range(config["local_epochs"]):
        shuffled = rng.permutation(rows)
        total = 0.0
        for start in range(0, len(shuffled), config["batch_size"]):
            batch = shuffled[start:start + config["batch_size"]]
            optimizer.zero_grad(set_to_none=True)
            logits = masked_logits(local(x[batch]), seen)
            loss = nn.functional.cross_entropy(logits, y[batch])
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite local loss")
            loss.backward()
            for p in local.parameters():
                if p.grad is not None and not torch.isfinite(p.grad).all():
                    raise FloatingPointError("Non-finite local gradient")
            if config["gradient_clip_norm"] is not None:
                nn.utils.clip_grad_norm_(local.parameters(), config["gradient_clip_norm"])
            optimizer.step()
            total += float(loss.detach()) * len(batch)
        losses.append(total / len(rows))
    for p in local.parameters():
        if not torch.isfinite(p).all():
            raise FloatingPointError("Non-finite local parameter")
    return local, losses


def fedavg(global_model, locals_and_counts):
    total = sum(n for _, n in locals_and_counts)
    if not total:
        raise ValueError("No fitting rows in round")
    state = global_model.state_dict()
    for key in state:
        state[key] = sum(model.state_dict()[key] * (n / total)
                         for model, n in locals_and_counts if n)
    global_model.load_state_dict(state)


def predict(model, x, rows, seen):
    model.eval()
    with torch.no_grad():
        blocks = [torch.softmax(masked_logits(model(x[rows[s:s+4096]]), seen), dim=1).cpu().numpy()
                  for s in range(0, len(rows), 4096)]
    return np.concatenate(blocks) if blocks else np.empty((0, model.layers[-1].out_features))


def rank_metrics(binary, scores):
    """Tie-aware ROC AUC and average precision (step-integral PR AUC)."""
    binary = np.asarray(binary, dtype=int)
    scores = np.asarray(scores, dtype=float)
    positives = int(binary.sum())
    negatives = len(binary) - positives
    if not positives or not negatives:
        return None, None
    order = np.argsort(-scores, kind="stable")
    target, sorted_scores = binary[order], scores[order]
    ends = np.r_[np.flatnonzero(np.diff(sorted_scores)), len(binary) - 1]
    tp = np.cumsum(target)[ends]
    fp = ends + 1 - tp
    tpr = np.r_[0.0, tp / positives]
    fpr = np.r_[0.0, fp / negatives]
    auc = float(np.trapezoid(tpr, fpr))
    ap = float(np.sum(np.diff(np.r_[0.0, tp / positives]) * tp / (tp + fp)))
    return auc, ap


def metrics(y, prob, class_names, seen):
    y = np.asarray(y, dtype=int)
    pred = prob.argmax(axis=1) if len(y) else np.array([], dtype=int)
    benign = y == 0
    attacks = ~benign
    rare_ids = [i for i, name in enumerate(class_names) if name in RARE]
    rare = np.isin(y, rare_ids)
    recalls, aucs, aps = [], [], []
    per_class = []
    for c in seen:
        mask = y == c
        recall = float(np.mean(pred[mask] == c)) if mask.any() else None
        auc, ap = rank_metrics(mask, prob[:, c])
        per_class.append({"class": class_names[c], "support": int(mask.sum()), "recall": recall,
                          "auroc": auc, "auprc_average_precision": ap})
        if recall is not None:
            recalls.append(recall)
        if auc is not None:
            aucs.append(auc)
            aps.append(ap)
    binary_auc, binary_ap = rank_metrics(attacks, 1 - prob[:, 0])
    return {
        "rows": len(y), "benign_support": int(benign.sum()), "attack_support": int(attacks.sum()),
        "accuracy": float(np.mean(pred == y)) if len(y) else None,
        "attack_accuracy": float(np.mean(pred[attacks] == y[attacks])) if attacks.any() else None,
        "macro_recall": float(np.mean(recalls)) if recalls else None,
        "rare_attack_support": int(rare.sum()),
        "rare_attack_recall": float(np.mean(pred[rare] == y[rare])) if rare.any() else None,
        "false_alarm_rate": float(np.mean(pred[benign] != 0)) if benign.any() else None,
        "auroc_macro_ovr": float(np.mean(aucs)) if aucs else None,
        "auprc_macro_ovr_average_precision": float(np.mean(aps)) if aps else None,
        "ranking_classes_with_both_positive_and_negative_support": len(aucs),
        "binary_attack_auroc": binary_auc, "binary_attack_auprc_average_precision": binary_ap,
        "per_class": per_class,
    }


def prepare(frame, config, seed, directory):
    frame = frame.copy()
    label_column = config["label_column"]
    labels = frame[label_column].astype(str).to_numpy()
    labels = np.array(["Benign" if is_benign_label(v) else v for v in labels])
    frame[label_column] = labels
    classes = ["Benign"] + sorted(set.union(*TASKS.values()))
    unexpected = set(labels) - set(classes)
    if unexpected:
        raise ValueError(f"Labels outside predeclared task vocabulary: {sorted(unexpected)}")
    y = np.array([classes.index(v) for v in labels])
    assigned = reproducible_non_iid_client_partitions(labels, seed=seed)
    fit, cal, evaluation = config["role_fractions"]
    roles, role_report = assign_persistent_roles(labels, assigned, seed=seed,
        fitting_fraction=fit, calibration_fraction=cal, evaluation_fraction=evaluation)
    tasks = build_persistent_tasks(labels, assigned, roles,
        [(name, TASKS[name]) for name in config["attack_order"]], benign_names=BENIGN)
    preprocessing_rows = np.unique(np.concatenate(list(tasks[0]["train"].values())))
    x, state, preprocessing = fit_frozen_preprocessor(frame, label_column, preprocessing_rows,
                                                     z_clip=config["numeric_z_clip"])
    # The reused v3 helper reports a logistic parameter count; replace it for this MLP.
    preprocessing.pop("parameter_count_including_bias", None)
    preprocessing["mlp_parameter_count"] = x.shape[1]*64 + 64 + 64*32 + 32 + 32*len(classes) + len(classes)
    audit = split_audit(frame, label_column, assigned, roles, tasks, preprocessing_rows, benign_names=BENIGN)
    audit["persistent_role_assignment"] = role_report
    clients = client_for_each_row(assigned, len(frame))
    manifest = frame[["__source_file__", "__source_row__", "__evse__", "__operating_state__"]].copy()
    manifest["sample_index"] = np.arange(len(frame))
    manifest["label"] = labels
    manifest["class_id"] = y
    manifest["client"] = clients
    manifest["persistent_role"] = roles
    manifest["preprocessing_fit"] = np.isin(np.arange(len(frame)), preprocessing_rows)
    manifest["task"] = ["benign_reference_all_tasks" if v == "Benign" else
                        next(name for name, group in TASKS.items() if v in group) for v in labels]
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(directory / "split_manifest.csv", index=False)
    save_json(directory / "split_audit.json", audit)
    save_json(directory / "preprocessing.json", preprocessing)
    save_json(directory / "class_mapping.json", {name: i for i, name in enumerate(classes)})
    return {"x": torch.tensor(x, dtype=torch.float32), "y": torch.tensor(y, dtype=torch.long),
            "labels": labels, "classes": classes, "roles": roles, "clients": clients,
            "tasks": tasks, "assigned": assigned, "manifest": manifest, "audit": audit}


def union_rows(tasks, role, client=None):
    blocks = [task[role][client] for task in tasks] if client else [r for task in tasks for r in task[role].values()]
    return np.unique(np.concatenate(blocks)) if blocks else np.array([], dtype=int)


def run(data, config, seed, lr, directory, *, calibration_only=False):
    seed_everything(seed)
    global_model = TrafficMLP(data["x"].shape[1], len(data["classes"]))
    clients = list(data["assigned"])
    rngs = {client: np.random.default_rng(seed * 100 + i) for i, client in enumerate(clients)}
    seen = {0}
    history, training_log = [], []
    best = {}
    for t, task in enumerate(data["tasks"]):
        seen.update(data["classes"].index(label) for label in TASKS[task["name"]])
        seen_list = sorted(seen)
        for round_index in range(config["rounds_per_task"]):
            updates = []
            for client in clients:
                rows = task["train"][client]
                if not np.all(data["roles"][rows] == ROLE_FIT):
                    raise AssertionError("Non-fitting row in local training")
                local, losses = train_local(global_model, data["x"], data["y"], rows, seen_list,
                                             config, lr, rngs[client])
                updates.append((local, len(rows)))
                training_log.append({"task": task["name"], "round": round_index + 1, "client": client,
                    "fitting_rows": len(rows), "replay_rows": 0, "epoch_losses": losses})
            fedavg(global_model, updates)
        permitted = data["tasks"][:t+1]
        # Calibration-only screening never invokes predictions on evaluation rows.
        cal_rows = union_rows(permitted, "calibration")
        assert np.all(data["roles"][cal_rows] == ROLE_CAL)
        cal_prob = predict(global_model, data["x"], cal_rows, seen_list)
        calibration = metrics(data["y"][cal_rows].numpy(), cal_prob, data["classes"], seen_list)
        checkpoint = {"checkpoint": t+1, "learned_task": task["name"], "seen_classes": seen_list,
                      "calibration": calibration}
        if not calibration_only:
            checkpoint["tasks"] = {}
            for prior in permitted:
                rows = union_rows([prior], "test")
                assert np.all(data["roles"][rows] == ROLE_EVAL)
                prob = predict(global_model, data["x"], rows, seen_list)
                m = metrics(data["y"][rows].numpy(), prob, data["classes"], seen_list)
                initial_best = best.get(prior["name"], m["attack_accuracy"])
                m["forgetting"] = max(0.0, initial_best - m["attack_accuracy"]) if m["attack_accuracy"] is not None else None
                if m["attack_accuracy"] is not None:
                    best[prior["name"]] = max(initial_best, m["attack_accuracy"])
                checkpoint["tasks"][prior["name"]] = m
                m["per_client"] = {}
                for client in clients:
                    mask = data["clients"][rows] == client
                    local_metric = metrics(data["y"][rows[mask]].numpy(), prob[mask], data["classes"], seen_list)
                    key = (prior["name"], client)
                    value = local_metric["attack_accuracy"]
                    prior_best = best.get(key, value)
                    local_metric["forgetting"] = max(0.0, prior_best - value) if value is not None else None
                    if value is not None:
                        best[key] = max(prior_best, value)
                    m["per_client"][client] = local_metric
            eval_rows = union_rows(permitted, "test")
            assert np.all(data["roles"][eval_rows] == ROLE_EVAL)
            prob = predict(global_model, data["x"], eval_rows, seen_list)
            checkpoint["pooled"] = metrics(data["y"][eval_rows].numpy(), prob, data["classes"], seen_list)
            checkpoint["per_client"] = {}
            for client in clients:
                mask = data["clients"][eval_rows] == client
                checkpoint["per_client"][client] = metrics(data["y"][eval_rows[mask]].numpy(), prob[mask], data["classes"], seen_list)
            values = [m["macro_recall"] for m in checkpoint["per_client"].values() if m["macro_recall"] is not None]
            checkpoint["worst_client_macro_recall"] = min(values) if values else None
            pred = prob.argmax(axis=1)
            manifest = data["manifest"].iloc[eval_rows].copy()
            manifest["y_pred"] = pred
            for c, label in enumerate(data["classes"]):
                manifest[f"p_{label}"] = prob[:, c]
            manifest.to_csv(Path(directory) / f"checkpoint_{t+1}_predictions.csv", index=False)
            if t == len(data["tasks"])-1:
                manifest.to_csv(Path(directory) / "final_predictions.csv", index=False)
        history.append(checkpoint)
        print(f"seed={seed} lr={lr:g} task={task['name']} cal_macro_recall={calibration['macro_recall']:.4f}", flush=True)
    result = {"seed": seed, "learning_rate": lr, "method": "fedavg_no_replay",
              "calibration_only": calibration_only, "history": history,
              "selection_score": float(np.mean([h["calibration"]["macro_recall"] for h in history]))}
    save_json(Path(directory) / "training_log.json", training_log)
    save_json(Path(directory) / "results.json", result)
    if not calibration_only:
        torch.save(global_model.state_dict(), Path(directory) / "final_model.pt")
    return result


def forgetting_gate(results, config, data_ready):
    seed_rows = []
    for result in results:
        history = result["history"]
        task_rows = []
        for j, name in enumerate(config["attack_order"][:-1]):
            initial = history[j]["tasks"][name]["attack_accuracy"]
            final = history[-1]["tasks"][name]["attack_accuracy"]
            eligible = initial is not None and initial >= config["minimum_initial_old_task_accuracy"]
            drop = 100 * (initial-final) if initial is not None and final is not None else None
            task_rows.append({"task": name, "initial_attack_accuracy": initial, "final_attack_accuracy": final,
                              "drop_percentage_points": drop, "adequately_learned": eligible})
        clear = any(row["adequately_learned"] and row["drop_percentage_points"] >= config["clear_drop_percentage_points"] for row in task_rows)
        seed_rows.append({"seed": result["seed"], "clear_drop": clear, "tasks": task_rows})
    fraction = sum(row["clear_drop"] for row in seed_rows) / len(seed_rows)
    clear = fraction >= config["minimum_seed_fraction_with_clear_drop"]
    return {"criteria": {k: config[k] for k in ["minimum_initial_old_task_accuracy", "clear_drop_percentage_points", "minimum_seed_fraction_with_clear_drop"]},
            "seed_results": seed_rows, "fraction_seeds_with_clear_drop": fraction,
            "clear_forgetting_observed": clear, "data_requirements_satisfied": data_ready,
            "full_comparison_authorized_by_runner": False,
            "next_action": "supervisor_review_required_before_full_comparison" if clear else "stop_and_discuss_different_framing",
            "limitations": [] if data_ready else ["Insufficient real benign evaluation support; diagnostic pilot only"]}


def source_hashes(root):
    paths = ["src/evse_ids/multiclass_pilot.py", "src/evse_ids/continual_stable.py", "src/evse_ids/data.py",
             "src/evse_ids/validation.py", "scripts/run_multiclass_no_replay_pilot.py", "configs/multiclass_no_replay_pilot.json"]
    return {p: hashlib.sha256((Path(root)/p).read_bytes()).hexdigest() for p in paths}
