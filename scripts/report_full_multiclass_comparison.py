"""Aggregate matched runs without treating three orders as independent seeds."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
METRICS = ["old_task_accuracy","forgetting","rare_attack_recall","rare_attack_macro_recall",
           "false_alarm_rate","worst_client_macro_recall","accuracy","attack_accuracy","macro_recall",
           "auroc_macro_ovr","auprc_macro_ovr_average_precision","binary_attack_auroc","binary_attack_auprc_average_precision"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="outputs/multiclass_full_comparison")
    parser.add_argument("--allow-partial",action="store_true")
    args = parser.parse_args()
    output = ROOT/args.output_dir
    config = json.loads((output/"protocol_before_evaluation.json").read_text())["config"]
    expected = len(config["seeds"])*len(config["orders"])*len(config["environments"])*len(config["methods"])
    paths = sorted((output/"runs").glob("*/*/*/seed_*/results.json"))
    if len(paths) != expected and not args.allow_partial:
        raise SystemExit(f"Incomplete comparison: {len(paths)}/{expected} results")
    rows, client_rows, class_rows, task_rows, checkpoint_rows = [], [], [], [], []
    for path in paths:
        r = json.loads(path.read_text())
        order = path.parents[3].name
        key = {"order":order,"environment":r["environment"],"method":r["method"],"seed":r["seed"]}
        rows.append({**key,**r["summary"],"elapsed_seconds":r["elapsed_seconds"],"settings":json.dumps(r["settings"],sort_keys=True)})
        for client,m in r["per_client_summary"].items():
            client_rows.append({**key,"client":client,**m})
        for h in r["history"]:
            checkpoint_rows.append({**key,"checkpoint":h["checkpoint"],**{k:v for k,v in h["pooled"].items() if k!="per_class"}})
            for task,m in h["tasks"].items():
                task_rows.append({**key,"checkpoint":h["checkpoint"],"task":task,"client":"pooled",
                                  **{k:v for k,v in m.items() if k not in {"per_class","per_client"}}})
                for client,cm in m["per_client"].items():
                    task_rows.append({**key,"checkpoint":h["checkpoint"],"task":task,"client":client,
                                      **{k:v for k,v in cm.items() if k!="per_class"}})
            if h is r["history"][-1]:
                for pc in h["pooled"]["per_class"]:
                    class_rows.append({**key,"client":"pooled",**pc})
                for client,m in h["per_client"].items():
                    for pc in m["per_class"]:
                        class_rows.append({**key,"client":client,**pc})
    frame, clients = pd.DataFrame(rows),pd.DataFrame(client_rows)
    frame.to_csv(output/"per_run_metrics.csv",index=False)
    clients.to_csv(output/"per_client_per_run_metrics.csv",index=False)
    pd.DataFrame(class_rows).to_csv(output/"per_class_metrics.csv",index=False)
    pd.DataFrame(task_rows).to_csv(output/"checkpoint_task_client_metrics.csv",index=False)
    pd.DataFrame(checkpoint_rows).to_csv(output/"checkpoint_pooled_metrics.csv",index=False)
    summaries = []
    # First average the three orders within each seed; then quantify ten-seed variation.
    seed_mean = frame.groupby(["environment","method","seed"])[METRICS].mean().reset_index()
    seed_mean.to_csv(output/"per_seed_order_averaged_metrics.csv",index=False)
    for (environment,method),group in seed_mean.groupby(["environment","method"]):
        record = {"environment":environment,"method":method,"n_seeds":len(group)}
        for metric in METRICS:
            values = group[metric].dropna()
            record[metric+"_mean"] = float(values.mean()) if len(values) else None
            record[metric+"_std"] = float(values.std(ddof=1)) if len(values)>1 else None
        summaries.append(record)
    summary = pd.DataFrame(summaries)
    summary.to_csv(output/"summary_metrics.csv",index=False)
    order_summary = frame.groupby(["order","environment","method"])[METRICS].agg(["mean","std"])
    order_summary.columns = ["_".join(column) for column in order_summary.columns]
    order_summary.reset_index().to_csv(output/"per_order_summary_metrics.csv",index=False)
    client_metrics = [m for m in METRICS if m in clients.columns]
    client_seed_mean = clients.groupby(["environment","method","client","seed"])[client_metrics].mean()
    client_summary = client_seed_mean.groupby(["environment","method","client"])[client_metrics].agg(["mean","std"])
    client_summary.columns = ["_".join(column) for column in client_summary.columns]
    client_summary.reset_index().to_csv(output/"per_client_summary_metrics.csv",index=False)
    contrasts = []
    for metric in METRICS:
        pivot = seed_mean.pivot(index="seed",columns=["environment","method"],values=metric)
        deltas = {}
        for environment in config["environments"]:
            left,right = (environment,"protected_60"),(environment,"uniform_60")
            if left not in pivot or right not in pivot:
                continue
            difference = (pivot[left]-pivot[right]).dropna()
            deltas[environment] = difference
            if len(difference):
                mean,std = float(difference.mean()),float(difference.std(ddof=1))
                half = 2.262*std/np.sqrt(len(difference)) if len(difference)==10 else None
                contrasts.append({"contrast":environment+" protected_minus_uniform","metric":metric,"n_seeds":len(difference),
                                  "mean_difference":mean,"std_difference":std,"ci95_low":mean-half if half is not None else None,"ci95_high":mean+half if half is not None else None})
        if set(deltas)=={"federated","centralized"}:
            difference = (deltas["federated"]-deltas["centralized"]).dropna()
            if len(difference):
                mean,std = float(difference.mean()),float(difference.std(ddof=1))
                half = 2.262*std/np.sqrt(len(difference)) if len(difference)==10 else None
                contrasts.append({"contrast":"federated_minus_centralized_replay_improvement","metric":metric,"n_seeds":len(difference),
                                  "mean_difference":mean,"std_difference":std,"ci95_low":mean-half if half is not None else None,"ci95_high":mean+half if half is not None else None})
    pd.DataFrame(contrasts).to_csv(output/"paired_contrasts.csv",index=False)
    def display(value):
        return "N/A" if pd.isna(value) else f"{100*value:.2f}"
    lines = ["# Full multiclass comparison results", "", f"Completed evaluation runs: **{len(paths)}/{expected}**. Original CICEVSE data only; supplied additional datasets excluded.", "",
             "Results are percentages except where stated. Means average the three orders within each training seed, then average ten seeds. Seeds vary training randomness on one fixed split.", "",
             "| Environment | Method | Old-task accuracy | Forgetting | Rare recall | FPR | Worst-client macro recall | Macro AUROC | Macro AP |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in summaries:
        values = [r[m+"_mean"] for m in ["old_task_accuracy","forgetting","rare_attack_recall","false_alarm_rate","worst_client_macro_recall","auroc_macro_ovr","auprc_macro_ovr_average_precision"]]
        lines.append("| "+" | ".join([r["environment"],r["method"]]+[display(v) for v in values])+" |")
    lines += ["", "## Does protected replay beat uniform replay?", "",
              "Paired differences below are percentage points. Negative forgetting/FPR differences favor protection; positive accuracy/recall differences favor protection.", "",
              "| Contrast | Metric | Mean difference | 95% paired-seed interval |", "|---|---|---:|---|"]
    for c in contrasts:
        if c["metric"] not in {"old_task_accuracy","forgetting","rare_attack_recall","false_alarm_rate","worst_client_macro_recall"}:
            continue
        interval = "N/A" if c["ci95_low"] is None else f"[{100*c['ci95_low']:.2f}, {100*c['ci95_high']:.2f}]"
        lines.append(f"| {c['contrast']} | {c['metric']} | {100*c['mean_difference']:.2f} | {interval} |")
    lines += ["", "## Every station", "", "Full metrics and uncertainty for each profile are in per_client_summary_metrics.csv; each seed/order result is in per_client_per_run_metrics.csv. Per-class recall, support, AUROC and AP are in per_class_metrics.csv. These include the benign-starved client even when its FPR is undefined.", "",
              "## Training and tuning", "", "MLP 64/32, ReLU, Adam, five local epochs per round, five rounds per task, no gradient clipping. Calibration-only grids and exact selection scores are in hyperparameter_trials.csv/JSON. Replay/EWC/A-GEM/FedProx learning rate was not independently tuned; 0.003 was fixed from the prior calibration pilot. Joint and no-replay learning rates were screened. See the full protocol for Fisher sampling, projection, rehearsal mixing, and memory accounting.", "",
              "## Interpretation limits", "", "Proceeding despite imbalance was explicitly authorized. The test set still contains 16 genuine benign examples, so FPR is coarse and undefined at the benign-starved profile. Reported results do not satisfy the request for hundreds of benign test examples. Three orders are paired repeated conditions, not 30 independent datasets. A-GEM uses Adam and task-boundary uniform memory, an explicitly disclosed adaptation. Joint is an empirical offline reference and is not guaranteed to outperform every continual method. Macro AP uses average precision rather than trapezoidal PR AUC.", "",
              "Compare protected and uniform under the same budget, and inspect the federated-centralized difference in their improvements before claiming a federation-specific effect. Hyperparameters were selected separately per environment/order, so that difference also reflects separately calibrated procedures. The expected benign-starved/rare-station story must be supported by actual station metrics, not assumed.", "",
              "The code, configs, split manifests, calibration evidence, and selected final/checkpoint predictions are intended for the existing private GitHub repository. Historical pilot results are preserved."]
    (output/"FULL_COMPARISON_RESULTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    if len(paths)==expected:
        interpretation = ["# Supervisor update: completed multiclass comparison", "",
            "The requested experiment has been executed on the original CICEVSE data: 10 training seeds, three attack orders, both federated and pooled centralized learning, and seven methods. The additional supplied datasets were excluded. Persistent roles and Task-1-only preprocessing were retained.", "",
            "## Protected versus uniform replay", ""]
        for environment in config["environments"]:
            p = summary[(summary.environment==environment)&(summary.method=="protected_60")].iloc[0]
            u = summary[(summary.environment==environment)&(summary.method=="uniform_60")].iloc[0]
            interpretation.append(f"**{environment.capitalize()}:** protected replay old-task accuracy = {100*p.old_task_accuracy_mean:.2f}%, uniform = {100*u.old_task_accuracy_mean:.2f}%; rare-attack recall = {100*p.rare_attack_recall_mean:.2f}% versus {100*u.rare_attack_recall_mean:.2f}%; worst-client macro recall = {100*p.worst_client_macro_recall_mean:.2f}% versus {100*u.worst_client_macro_recall_mean:.2f}%.")
            interpretation.append("")
        for c in contrasts:
            if c["contrast"]=="federated_minus_centralized_replay_improvement" and c["metric"]=="old_task_accuracy":
                interval = f"[{100*c['ci95_low']:.2f}, {100*c['ci95_high']:.2f}]" if c["ci95_low"] is not None else "N/A"
                interpretation += [f"The federated-minus-centralized difference in the protected-over-uniform old-task improvement is **{100*c['mean_difference']:.2f} percentage points**, with paired-seed 95% interval {interval}. This compares separately calibrated procedures on a fixed split, not a general causal claim that federation improves retention.", ""]
        interpretation += ["## What is included", "", "The full result table includes no replay, EWC, A-GEM (Adam adaptation), joint/offline reference and FedProx. Every client, attack type and task checkpoint is reported in the CSV evidence, alongside all tried calibration settings and recorded fixed choices.", "",
            "## What remains limited", "", "The original test set still has 16 genuine benign flows and the benign-starved client has no benign evaluation examples. Proceeding despite this was explicitly authorized; this unmet data requirement is not described as solved. The study has ten training seeds on one fixed sample/split, not ten independent datasets. Source/session-level generalization and manuscript readiness require separate assessment.", "",
            "Please assess the actual protected-versus-uniform and federated-versus-centralized results before finalizing the four-page Networking Letters claims. No old logistic-result improvement claims were reused."]
        (output/"SUPERVISOR_UPDATE.md").write_text("\n".join(interpretation)+"\n",encoding="utf-8")
    print(summary[["environment","method","old_task_accuracy_mean","forgetting_mean","rare_attack_recall_mean","false_alarm_rate_mean","worst_client_macro_recall_mean"]].to_string(index=False))


if __name__ == "__main__": main()
