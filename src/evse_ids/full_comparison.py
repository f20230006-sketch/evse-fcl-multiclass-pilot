"""MLP continual comparison with local rehearsal, EWC, A-GEM and pooled controls."""
from __future__ import annotations

import copy
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.func import functional_call, grad, vmap

from .continual_ablation import update_replay_buffer
from .continual_stable import ROLE_FIT, ROLE_CAL, ROLE_EVAL
from .multiclass_pilot import (
    TrafficMLP, TASKS, BENIGN, RARE, fedavg, masked_logits, metrics,
    predict, save_json, seed_everything, union_rows,
)


def projected_gradient(current, reference):
    dot = torch.dot(current, reference)
    norm = torch.dot(reference, reference)
    if dot < 0 and norm > 1e-12:
        return current - dot / norm * reference, True
    return current, False


def quadratic_penalty(model, anchor, importance=None):
    terms = [(p-anchor[name]).square() * (importance[name] if importance is not None else 1)
             for name, p in model.named_parameters()]
    return sum(term.sum() for term in terms) / 2


def empirical_fisher(model, x, y, rows, seen, rng, maximum):
    rows = np.asarray(rows, dtype=int)
    if len(rows) > maximum:
        rows = rng.choice(rows, maximum, replace=False)
    params = {name: p.detach() for name, p in model.named_parameters()}
    fisher = {name: torch.zeros_like(p) for name, p in params.items()}
    if not len(rows):
        return fisher, rows
    def example_loss(parameters, example, target):
        output = functional_call(model, parameters, (example.unsqueeze(0),))
        return nn.functional.cross_entropy(masked_logits(output, seen), target.unsqueeze(0))
    gradients = vmap(grad(example_loss), in_dims=(None, 0, 0))
    for start in range(0, len(rows), 32):
        batch = rows[start:start+32]
        values = gradients(params, x[batch], y[batch])
        for name in fisher:
            fisher[name] += values[name].detach().square().sum(dim=0) / len(rows)
    return fisher, rows


def train_client(global_model, data, current, memory, seen, config, method, settings, terms, rng):
    local = copy.deepcopy(global_model)
    if not len(current):
        return local, {"epoch_losses": [], "projections": 0, "steps": 0}
    if not np.all(data["roles"][current] == ROLE_FIT) or not np.all(data["roles"][memory] == ROLE_FIT):
        raise AssertionError("Calibration/evaluation row entered fitting or replay")
    optimizer = torch.optim.Adam(local.parameters(), lr=settings["learning_rate"], weight_decay=config["weight_decay"])
    reference_parameters = {name:p.detach().clone() for name,p in global_model.named_parameters()}
    params = list(local.parameters())
    fraction = settings.get("replay_fraction", 0.0) if len(memory) else 0.0
    replay_batch = max(1, int(config["batch_size"] * fraction)) if fraction else 0
    current_batch = config["batch_size"] - replay_batch
    steps, projections, losses = 0, 0, []
    for _ in range(config["local_epochs"]):
        shuffled = rng.permutation(current)
        total, observations = 0.0, 0
        for start in range(0, len(shuffled), current_batch):
            rows = shuffled[start:start+current_batch]
            optimizer.zero_grad(set_to_none=True)
            loss = nn.functional.cross_entropy(masked_logits(local(data["x"][rows]), seen), data["y"][rows])
            if replay_batch:
                old = rng.choice(memory, replay_batch, replace=True)
                old_loss = nn.functional.cross_entropy(masked_logits(local(data["x"][old]), seen), data["y"][old])
                loss = (1-fraction)*loss + fraction*old_loss
            if method == "ewc":
                loss = loss + settings["ewc_lambda"] * sum(quadratic_penalty(local, anchor, fisher) for anchor,fisher in terms)
            if method == "fedprox_no_replay":
                loss = loss + settings["proximal_mu"] * quadratic_penalty(local, reference_parameters)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite local objective")
            if method == "agem" and len(memory):
                current_grads = torch.autograd.grad(loss, params)
                old = rng.choice(memory, settings["reference_batch_size"], replace=True)
                reference_loss = nn.functional.cross_entropy(masked_logits(local(data["x"][old]), seen), data["y"][old])
                reference_grads = torch.autograd.grad(reference_loss, params)
                g = torch.cat([p.reshape(-1) for p in current_grads])
                gref = torch.cat([p.reshape(-1) for p in reference_grads])
                g, changed = projected_gradient(g, gref)
                projections += int(changed)
                position = 0
                for p in params:
                    p.grad = g[position:position+p.numel()].reshape_as(p).clone()
                    position += p.numel()
            else:
                loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in params):
                raise FloatingPointError("Non-finite local gradient")
            optimizer.step()
            total += float(loss.detach()) * len(rows)
            observations += len(rows)
            steps += 1
        losses.append(total/observations)
    if any(not torch.isfinite(p).all() for p in params):
        raise FloatingPointError("Non-finite model")
    return local, {"epoch_losses": losses, "projections": projections, "steps": steps}


def block_metrics(y, probability, classes, seen):
    m = metrics(y, probability, classes, seen)
    supported_rare = [p["recall"] for p in m["per_class"] if p["class"] in RARE and p["recall"] is not None]
    m["rare_attack_macro_recall"] = float(np.mean(supported_rare)) if supported_rare else None
    return m


def evaluate(model, data, tasks, seen, best, *, joint=False):
    rows = union_rows(tasks, "test")
    if not np.all(data["roles"][rows] == ROLE_EVAL):
        raise AssertionError("Non-evaluation row in evaluation")
    probability = predict(model, data["x"], rows, seen)
    y = data["y"][rows].numpy()
    pooled = block_metrics(y, probability, data["classes"], seen)
    task_results = {}
    for task in tasks:
        attack_ids = [data["classes"].index(name) for name in TASKS[task["name"]]]
        mask = (y == 0) | np.isin(y, attack_ids)
        m = block_metrics(y[mask], probability[mask], data["classes"], seen)
        value = m["attack_accuracy"]
        prior_best = best.get(task["name"], value)
        m["forgetting"] = None if joint or value is None else max(0.0, prior_best-value)
        if value is not None:
            best[task["name"]] = max(prior_best, value)
        m["per_client"] = {}
        for client in data["assigned"]:
            local = mask & (data["clients"][rows] == client)
            cm = block_metrics(y[local], probability[local], data["classes"], seen)
            value = cm["attack_accuracy"]
            key = (task["name"], client)
            prior_best = best.get(key, value)
            cm["forgetting"] = None if joint or value is None else max(0.0, prior_best-value)
            if value is not None:
                best[key] = max(prior_best, value)
            m["per_client"][client] = cm
        task_results[task["name"]] = m
    per_client = {}
    for client in data["assigned"]:
        mask = data["clients"][rows] == client
        per_client[client] = block_metrics(y[mask], probability[mask], data["classes"], seen)
    return {"pooled": pooled, "tasks": task_results, "per_client": per_client}, rows, probability


def final_summary(history, data, method):
    final = history[-1]
    old_names = [task["name"] for task in data["tasks"][:-1]]
    old_accuracy = [final["tasks"][name]["attack_accuracy"] for name in old_names]
    forgetting = [final["tasks"][name]["forgetting"] for name in old_names]
    summary = {**{k:v for k,v in final["pooled"].items() if k != "per_class"},
               "old_task_accuracy": float(np.mean(old_accuracy)),
               "forgetting": None if method == "joint" else float(np.mean(forgetting))}
    client_summaries = {}
    for client, metrics_ in final["per_client"].items():
        old = [final["tasks"][name]["per_client"][client] for name in old_names]
        values = [m["attack_accuracy"] for m in old if m["attack_accuracy"] is not None]
        drops = [m["forgetting"] for m in old if m["forgetting"] is not None]
        client_summaries[client] = {**{k:v for k,v in metrics_.items() if k != "per_class"},
            "old_task_accuracy": float(np.mean(values)) if values else None,
            "forgetting": float(np.mean(drops)) if drops else None}
    summary["worst_client_macro_recall"] = min(m["macro_recall"] for m in client_summaries.values() if m["macro_recall"] is not None)
    return summary, client_summaries


def run_case(data, config, environment, method, settings, seed, directory, *, calibration_only=False):
    start_time = time.monotonic()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    seed_everything(seed)
    torch.set_num_threads(config["torch_threads_per_worker"])
    model = TrafficMLP(data["x"].shape[1], len(data["classes"]))
    clients = list(data["assigned"]) if environment == "federated" else ["pooled"]
    capacity = config["federated_memory_per_client"] if environment == "federated" else config["centralized_memory_total"]
    memories = {client: np.array([], dtype=int) for client in clients}
    terms = {client: [] for client in clients}
    train_rng = {client:np.random.default_rng(seed*100+i) for i,client in enumerate(clients)}
    memory_rng = {client:np.random.default_rng(seed*100+i+10000) for i,client in enumerate(clients)}
    history, log, buffer_log, scores, best = [], [], [], [], {}
    seen = {0}
    stages = [data["tasks"]] if method == "joint" else [[task] for task in data["tasks"]]
    for stage_index, stage in enumerate(stages):
        for task in stage:
            seen.update(data["classes"].index(name) for name in TASKS[task["name"]])
        seen_list = sorted(seen)
        current = {client:union_rows(stage, "train", client if environment == "federated" else None) for client in clients}
        for round_index in range(config["rounds_per_task"]):
            updates = []
            for client in clients:
                local, info = train_client(model, data, current[client], memories[client], seen_list,
                                          config, method, settings, terms[client], train_rng[client])
                count = len(np.unique(np.concatenate([current[client], memories[client]])))
                updates.append((local, count))
                log.append({"stage": stage_index+1, "round": round_index+1, "client": client,
                            "current_fitting_rows": len(current[client]), "replay_rows": len(memories[client]),
                            "aggregation_unique_rows": count, **info})
            fedavg(model, updates)
        allowed_tasks = data["tasks"] if method == "joint" else data["tasks"][:stage_index+1]
        calibration_rows = union_rows(allowed_tasks, "calibration")
        if not np.all(data["roles"][calibration_rows] == ROLE_CAL):
            raise AssertionError("Calibration role violation")
        calibration_probability = predict(model, data["x"], calibration_rows, seen_list)
        calibration_metrics = block_metrics(data["y"][calibration_rows].numpy(), calibration_probability, data["classes"], seen_list)
        scores.append(calibration_metrics["macro_recall"])
        checkpoint = {"checkpoint": len(data["tasks"]) if method == "joint" else stage_index+1,
                      "learned_task": "joint_all_tasks" if method == "joint" else stage[0]["name"],
                      "seen_classes": seen_list, "calibration": calibration_metrics}
        if not calibration_only:
            evaluation, rows, probability = evaluate(model, data, allowed_tasks, seen_list, best, joint=method == "joint")
            checkpoint.update(evaluation)
            np.savez_compressed(directory/f"checkpoint_{checkpoint['checkpoint']}_predictions.npz",
                                sample_index=rows, y_true=data["y"][rows].numpy(),
                                y_pred=probability.argmax(1), probability=probability)
        history.append(checkpoint)
        if method == "ewc" and stage_index < len(stages)-1:
            for client in clients:
                fisher, fisher_rows = empirical_fisher(model, data["x"], data["y"], current[client], seen_list,
                    memory_rng[client], config["fisher_max_examples_per_client_task"])
                assert np.all(data["roles"][fisher_rows] == ROLE_FIT)
                anchor = {name:p.detach().clone() for name,p in model.named_parameters()}
                terms[client].append((anchor, fisher))
                buffer_log.append({"stage": stage_index+1, "client": client, "fisher_rows": fisher_rows.tolist()})
        if method in {"uniform_60", "protected_60", "agem"}:
            for client in clients:
                memories[client] = update_replay_buffer(memories[client], current[client], data["labels"],
                    capacity=capacity, strategy="protected" if method == "protected_60" else "uniform",
                    rng=memory_rng[client], protected_groups=[BENIGN, RARE], minimum_fraction=config["protected_minimum_fraction"])
                assert len(memories[client]) <= capacity and np.all(data["roles"][memories[client]] == ROLE_FIT)
                buffer_log.append({"stage": stage_index+1, "client": client, "memory_rows": memories[client].tolist()})
    result = {"environment": environment, "method": method, "seed": seed, "settings": settings,
              "calibration_only": calibration_only, "history": history,
              "selection_score": float(np.mean(scores)), "elapsed_seconds": time.monotonic()-start_time}
    if not calibration_only:
        summary, per_client = final_summary(history, data, method)
        result["summary"] = summary
        result["per_client_summary"] = per_client
        torch.save(model.state_dict(), directory/"final_model.pt")
    save_json(directory/"training_log.json", log)
    save_json(directory/"memory_audit.json", buffer_log)
    save_json(directory/"results.json", result)
    return {"selection_score": result["selection_score"], "elapsed_seconds": result["elapsed_seconds"]}
