"""Generate a supervisor-readable result without sending any email."""
import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="outputs/multiclass_no_replay_pilot")
    parser.add_argument("--repository-url", default=None)
    args = parser.parse_args()
    output = ROOT / args.output_dir
    gate = json.loads((output/"forgetting_gate.json").read_text())
    trials = json.loads((output/"hyperparameter_trials.json").read_text())
    protocol = json.loads((output/"protocol_before_evaluation.json").read_text())
    config = protocol["config"]
    lines = ["# Multiclass no-replay first check", "", "6 October 2026. Diagnostic pilot; no full comparison was run.", "",
             f"Clear forgetting observed: **{gate['clear_forgetting_observed']}**. Benign-data requirements satisfied: **{gate['data_requirements_satisfied']}**.", "",
             "MLP 64/32, ReLU, Adam, 5 local epochs per round, 5 rounds per task; no gradient clipping; attack cap 3,000; persistent roles and Task-1-only preprocessing retained.", "",
             f"Learning rate **{trials['selected_learning_rate']}**, selected on calibration data only. All tried values and scores are saved in hyperparameter_trials.json. Other settings are fixed.", "",
             "## Direct old-attack accuracy drops", "", "Accuracy excludes benign examples and requires the exact attack type.", "",
             "| Seed | Old task | Accuracy after learning | Accuracy after final task | Drop (percentage points) | Initially learned >=50% |",
             "|---|---|---:|---:|---:|---|"]
    for seed in gate["seed_results"]:
        for row in seed["tasks"]:
            lines.append(f"| {seed['seed']} | {row['task']} | {100*row['initial_attack_accuracy']:.2f}% | {100*row['final_attack_accuracy']:.2f}% | {row['drop_percentage_points']:.2f} | {row['adequately_learned']} |")
    lines += ["", "Criterion recorded before evaluation: >=10 percentage-point drop on an old task initially learned to >=50% accuracy, in >=2/3 seeds. This is a practical pilot criterion, not a statistical significance test.", "", "## Final per-client metrics", "",
              "Macro recall averages supported classes. Null false alarm rates mean no benign evaluation support.", "",
              "| Seed | Client | Evaluation rows | Benign support | Exact attack accuracy | Macro recall | Rare recall | FPR |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
    metric_rows = []
    results = []
    fmt = lambda value: "N/A" if value is None else f"{100*value:.2f}%"
    for seed in config["seeds"]:
        result = json.loads((output/f"seed_{seed}"/"results.json").read_text())
        results.append(result)
        for checkpoint in result["history"]:
            for client, metric in checkpoint["per_client"].items():
                scalar = {k:v for k,v in metric.items() if k != "per_class"}
                metric_rows.append({"seed": seed, "checkpoint": checkpoint["checkpoint"], "client": client, **scalar})
        for client, m in result["history"][-1]["per_client"].items():
            lines.append(f"| {seed} | {client} | {m['rows']} | {m['benign_support']} | {fmt(m['attack_accuracy'])} | {fmt(m['macro_recall'])} | {fmt(m['rare_attack_recall'])} | {fmt(m['false_alarm_rate'])} |")
    pd.DataFrame(metric_rows).to_csv(output/"per_client_checkpoint_metrics.csv", index=False)
    lines += ["", "## Accuracy matrix", "", "See checkpoint_task_accuracy.csv for every checkpoint and old/current task; seed results JSON files include task-by-client metrics, per-class supports, AUROC and average precision.", "",
              "## Limitations and required next decision", "",
              "Only 82 genuine benign flows exist locally; only 16 unique benign evaluation rows per seed remain under the corrected protocol. The benign-starved client has no benign evaluation rows. ICMP fragmentation and ICMP flood remain data-limited; a sampling cap cannot create observations. No duplicated/synthetic test examples were introduced.", "",
              "Do not claim protected-replay effectiveness from this no-replay pilot. No replay-method comparison, EWC, DER++, joint-training, centralized comparison, ten-seed/three-order study, or manuscript claim updates have been run. Reconnaissance initially reaches only about 25-27% attack-type accuracy and does not meet the initial-learning gate. Rare-task accuracy is weighted by support and is dominated by Slowloris; inspect per-class ICMP-fragmentation support/recall before interpreting it.", "",
              "Present this first-check result to the supervisor before full experiments. Agree on additional benign collection or a revised evaluation/framing. If no clear forgetting was found, stop as instructed.", "",
              f"Research repository: {args.repository_url}." if args.repository_url else "GitHub publication is pending account access. A local repository-ready package is supplied."]
    (output/"SUPERVISOR_FIRST_CHECK.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    seed_summary = []
    for r in results:
        old = [r["history"][-1]["tasks"][name] for name in config["attack_order"][:-1]]
        seed_summary.append({"seed": r["seed"], "mean_final_old_task_attack_accuracy": sum(m["attack_accuracy"] for m in old)/len(old),
            "mean_final_old_task_forgetting": sum(m["forgetting"] for m in old)/len(old),
            "final_pooled": r["history"][-1]["pooled"], "worst_client_macro_recall": r["history"][-1]["worst_client_macro_recall"]})
    (output/"pilot_summary.json").write_text(json.dumps(seed_summary, indent=2, allow_nan=False), encoding="utf-8")
    mean_drop = sum(row["mean_final_old_task_forgetting"] for row in seed_summary)/len(seed_summary)
    email = ["Subject: Multiclass no-replay first check and benign-data limitation", "", "Dear Dr. Kaur,", "",
        "I implemented the 64/32 ReLU MLP with Adam and five local epochs per round, raised the attack cap to 3,000, and retained persistent fitting/calibration/evaluation roles and Task-1-only preprocessing.", "",
        f"The three-seed, one-order diagnostic pilot found clear forgetting = {gate['clear_forgetting_observed']} under a preregistered practical criterion. Mean final old-task forgetting was {100*mean_drop:.2f} percentage points. The attached report includes initial-to-final attack-type accuracy for every old task and seed, as well as client-level metrics.", "",
        "The local network CSVs contain only 82 real benign flows, giving 16 unique benign evaluation rows per seed. The benign-starved client has none. I have no additional real benign data, so this does not yet meet your requested false-alarm evaluation support.", "",
        "I stopped before the full comparison. Please review the first-check report and advise on obtaining additional benign data or revising the evaluation protocol/framing before proceeding.", "", "Best regards,", "Yuvaraj"]
    (output/"SUPERVISOR_EMAIL_DRAFT.txt").write_text("\n".join(email)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
