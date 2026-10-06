"""Calibration first, then 10 seeds x 3 orders x 2 environments x 7 methods."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
import pandas as pd
import torch
from evse_ids.multiclass_pilot import prepare, save_json
from evse_ids.data import load_sampled_csv_dataset_with_provenance
from evse_ids.full_comparison import run_case


def execute_job(job):
    directory = Path(job["directory"])
    stamp = directory/"complete.json"
    if stamp.exists():
        old = json.loads(stamp.read_text())
        if old["fingerprint"] == job["fingerprint"]:
            return {**job, **old["result"], "resumed": True}
        raise ValueError(f"Job source/config changed: {directory}; use a new output directory")
    data = torch.load(job["prepared_path"], weights_only=False, map_location="cpu")
    result = run_case(data, job["config"], job["environment"], job["method"], job["settings"],
                      job["seed"], directory, calibration_only=job["calibration_only"])
    save_json(stamp, {"fingerprint":job["fingerprint"], "result":result})
    return {**job, **result, "resumed":False}


def run_jobs(jobs, workers, label, output):
    done = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(execute_job, job):job for job in jobs}
        for future in as_completed(pending):
            result = future.result()
            done.append(result)
            progress = {"phase":label, "completed":len(done), "total":len(jobs),
                        "last":{k:result[k] for k in ["order","environment","method","seed"]}}
            save_json(output/"progress.json", progress)
            print(json.dumps(progress), flush=True)
    return done


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/multiclass_full_comparison.json")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT/args.config).read_text())
    output = ROOT/config["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    sources = ["src/evse_ids/full_comparison.py", "src/evse_ids/multiclass_pilot.py", "src/evse_ids/continual_ablation.py",
               "src/evse_ids/continual_stable.py", "src/evse_ids/data.py", "src/evse_ids/validation.py",
               "scripts/run_full_multiclass_comparison.py", args.config]
    hashes = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
    fingerprint = hashlib.sha256(json.dumps({"config":config,"source":hashes},sort_keys=True).encode()).hexdigest()
    protocol_file = output/"protocol_before_evaluation.json"
    if protocol_file.exists() and json.loads(protocol_file.read_text())["fingerprint"] != fingerprint:
        raise ValueError("Protocol/source changed; preserve old results and choose a new output directory")
    source_files = [{"path":str(p.relative_to(ROOT/config["data"])),"bytes":p.stat().st_size,"modified_ns":p.stat().st_mtime_ns}
                    for p in sorted((ROOT/config["data"]).rglob("*.csv"))]
    if protocol_file.exists() and json.loads(protocol_file.read_text())["input_inventory"] != source_files:
        raise ValueError("Input files changed; use a new output directory")
    save_json(protocol_file, {"config":config,"source_hashes":hashes,"fingerprint":fingerprint,
        "input_inventory":source_files,"versions":{"python":platform.python_version(),"torch":torch.__version__,"pandas":pd.__version__},
        "sampling_and_roles":"Fixed seed-42 sample, client allocation and persistent roles across all training seeds and attack orders",
        "full_comparison_authorization":"User explicitly instructed to proceed despite class imbalance; supplied additional data excluded"})
    cache = output/"sampled_fixed.pkl"
    if cache.exists():
        frame = pd.read_pickle(cache)
    else:
        pilot = ROOT/"outputs/multiclass_no_replay_pilot"
        original_inventory = json.loads((pilot/"input_file_inventory.json").read_text()) if (pilot/"input_file_inventory.json").exists() else None
        pilot_protocol = json.loads((pilot/"protocol_before_evaluation.json").read_text()) if (pilot/"protocol_before_evaluation.json").exists() else None
        compatible = (original_inventory == source_files and pilot_protocol is not None and
                      pilot_protocol["config"]["max_rows_per_attack"] == config["max_rows_per_attack"] and
                      config["sampling_seed"] == 42 and pilot_protocol["source_hashes"]["src/evse_ids/data.py"] == hashes["src/evse_ids/data.py"])
        if compatible and (pilot/"sampled_seed_42.pkl").exists():
            frame = pd.read_pickle(pilot/"sampled_seed_42.pkl")
        else:
            frame = load_sampled_csv_dataset_with_provenance(ROOT/config["data"],config["label_column"],config["max_rows_per_attack"],config["sampling_seed"])
        frame.to_pickle(cache)
    sample_hash = hashlib.sha256(cache.read_bytes()).hexdigest()
    save_json(output/"sample_provenance.json", {"sha256":sample_hash,"rows":len(frame),"label_counts":{str(k):int(v) for k,v in frame[config["label_column"]].value_counts().items()}})
    prepared = {}
    for order, sequence in config["orders"].items():
        directory = output/"splits"/order
        pc = {**config,"attack_order":sequence}
        data = prepare(frame,pc,config["split_seed"],directory)
        path = directory/"prepared_local_only.pt"
        torch.save(data,path)
        prepared[order] = str(path)
    if args.prepare_only:
        return
    def make_job(order,environment,method,settings,seed,calibration_only,trial=None):
        root = output/"calibration" if calibration_only else output/"runs"
        directory = root/order/environment/method/(f"trial_{trial}" if calibration_only else f"seed_{seed}")
        job = {"order":order,"environment":environment,"method":method,"settings":settings,"seed":seed,
               "calibration_only":calibration_only,"prepared_path":prepared[order],"config":config,"directory":str(directory)}
        job["fingerprint"] = hashlib.sha256(json.dumps({"protocol":fingerprint,"sample":sample_hash,
            "order":order,"environment":environment,"method":method,"settings":settings,"seed":seed,"calibration_only":calibration_only},sort_keys=True).encode()).hexdigest()
        return job
    screen = [make_job(order,env,method,settings,config["calibration_seed"],True,trial)
              for order in config["orders"] for env in config["environments"] for method in config["methods"]
              for trial,settings in enumerate(config["grids"][method])]
    results = run_jobs(screen,config["workers"],"calibration",output)
    selected, trials = {}, []
    for order in config["orders"]:
        selected[order] = {}
        for env in config["environments"]:
            selected[order][env] = {}
            for method in config["methods"]:
                candidates = [r for r in results if r["order"]==order and r["environment"]==env and r["method"]==method]
                chosen = max(candidates,key=lambda r:(r["selection_score"],-config["grids"][method].index(r["settings"])))
                selected[order][env][method] = chosen["settings"]
                for r in candidates:
                    trials.append({"order":order,"environment":env,"method":method,"settings":r["settings"],
                                   "calibration_score":r["selection_score"],"selected":r is chosen})
    save_json(output/"hyperparameter_trials.json", {"trials":trials,"selected":selected,
        "selection_basis":"Mean seen-task calibration macro recall across checkpoints; joint uses its one offline calibration checkpoint; ties choose first prespecified candidate",
        "test_data_used":False,"fixed_setting_explanation":"All non-grid settings fixed; replay/EWC/A-GEM/FedProx learning rate 0.003 fixed from prior no-replay calibration pilot"})
    pd.DataFrame([{**r,"settings":json.dumps(r["settings"],sort_keys=True)} for r in trials]).to_csv(output/"hyperparameter_trials.csv",index=False)
    evaluations = [make_job(order,env,method,selected[order][env][method],seed,False)
                   for order in config["orders"] for env in config["environments"] for method in config["methods"] for seed in config["seeds"]]
    completed = run_jobs(evaluations,config["workers"],"evaluation",output)
    save_json(output/"completion.json", {"status":"complete","calibration_runs":len(results),"evaluation_runs":len(completed),
        "seeds":len(config["seeds"]),"orders":len(config["orders"]),"environments":len(config["environments"]),"methods":len(config["methods"]),"fingerprint":fingerprint})


if __name__ == "__main__":
    main()
