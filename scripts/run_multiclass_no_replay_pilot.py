"""Run the supervisor's FIRST CHECK only; never launch replay comparisons."""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np
import pandas as pd
import torch
from evse_ids.data import load_sampled_csv_dataset_with_provenance
from evse_ids.multiclass_pilot import prepare, run, forgetting_gate, save_json, source_hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/multiclass_no_replay_pilot.json")
    parser.add_argument("--allow-limited-benign-diagnostic", action="store_true",
                        help="Explicitly run a non-publication diagnostic with deficient benign support")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text())
    if sorted(config["attack_order"]) != sorted(["reconnaissance", "flooding", "low_rate_rare", "post_rare_vulnerability"]):
        raise ValueError("attack_order must contain each task exactly once")
    if config["hidden_sizes"] != [64, 32] or config["optimizer"] != "Adam":
        raise ValueError("This runner implements only the specified 64/32 Adam architecture")
    if config["calibration_seed"] not in config["seeds"]:
        raise ValueError("calibration_seed must belong to seeds")
    output = ROOT / config["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    save_json(output / "protocol_before_evaluation.json", {"config": config, "source_hashes": source_hashes(ROOT),
        "allow_limited_benign_diagnostic": args.allow_limited_benign_diagnostic,
        "versions": {"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "pandas": pd.__version__},
        "all_settings_fixed_except": "learning rate selected from recorded grid on calibration data only",
        "pilot_scope": "three seeds, one attack order, FedAvg no replay only"})
    prepared = {}
    source_files = [{"path": str(p.relative_to(ROOT/config["data"])), "bytes": p.stat().st_size,
                     "modified_ns": p.stat().st_mtime_ns}
                    for p in sorted((ROOT/config["data"]).rglob("*.csv"))]
    save_json(output / "input_file_inventory.json", source_files)
    for seed in config["seeds"]:
        cache = output / f"sampled_seed_{seed}.pkl"
        cache_stamp = cache.with_suffix(".cache_key")
        key = hashlib.sha256(json.dumps({"files": source_files, "seed": seed,
            "data": str((ROOT/config["data"]).resolve()), "label": config["label_column"],
            "cap": config["max_rows_per_attack"], "loader_hash": source_hashes(ROOT)["src/evse_ids/data.py"]}, sort_keys=True).encode()).hexdigest()
        if cache.exists() and cache_stamp.exists() and cache_stamp.read_text() == key:
            frame = pd.read_pickle(cache)
        else:
            print(f"Sampling data for seed {seed}...", flush=True)
            frame = load_sampled_csv_dataset_with_provenance(ROOT/config["data"], config["label_column"], config["max_rows_per_attack"], seed)
            frame.to_pickle(cache)
            cache_stamp.write_text(key)
        prepared[seed] = prepare(frame, config, seed, output/f"seed_{seed}")
    readiness = {str(seed): {"unique_benign_evaluation_rows": data["audit"]["unique_benign_evaluation_source_keys"],
        "meets_minimum": data["audit"]["unique_benign_evaluation_source_keys"] >= config["minimum_benign_evaluation_rows"]}
        for seed, data in prepared.items()}
    data_ready = all(v["meets_minimum"] for v in readiness.values())
    save_json(output / "data_readiness.json", {"required_benign_evaluation_rows": config["minimum_benign_evaluation_rows"],
        "seeds": readiness, "ready": data_ready, "benign_starved_false_alarm_rate": "undefined: zero benign evaluation support"})
    if args.prepare_only:
        return
    if not data_ready and not args.allow_limited_benign_diagnostic:
        raise SystemExit("STOP: insufficient benign evaluation support. See data_readiness.json; diagnostic override is explicit.")
    screen = []
    for lr in config["learning_rates_tried"]:
        directory = output/"calibration_screen"/f"lr_{lr:g}"
        directory.mkdir(parents=True, exist_ok=True)
        result = run(prepared[config["calibration_seed"]], config, config["calibration_seed"], lr, directory, calibration_only=True)
        screen.append({"learning_rate": lr, "calibration_score": result["selection_score"]})
    chosen = max(screen, key=lambda row: (row["calibration_score"], -row["learning_rate"]))["learning_rate"]
    save_json(output / "hyperparameter_trials.json", {"tried": screen, "selected_learning_rate": chosen,
        "selection_basis": "mean across checkpoints of pooled seen-class calibration macro recall; ties favor smaller learning rate",
        "evaluation_rows_used_for_selection": False})
    results = []
    for seed, data in prepared.items():
        results.append(run(data, config, seed, chosen, output/f"seed_{seed}"))
    gate = forgetting_gate(results, config, data_ready)
    save_json(output / "forgetting_gate.json", gate)
    rows = [{"seed": result["seed"], "checkpoint": h["checkpoint"], "task": task,
             "attack_accuracy": metric["attack_accuracy"], "forgetting": metric["forgetting"], "attack_support": metric["attack_support"]}
            for result in results for h in result["history"] for task, metric in h["tasks"].items()]
    pd.DataFrame(rows).to_csv(output/"checkpoint_task_accuracy.csv", index=False)
    print(json.dumps(gate, indent=2), flush=True)


if __name__ == "__main__":
    main()
