"""Compute the final queued case block ahead of the main pool; identical job fingerprints."""
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from run_full_multiclass_comparison import execute_job
from evse_ids.multiclass_pilot import save_json

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT/"outputs/multiclass_full_comparison"
    protocol = json.loads((output/"protocol_before_evaluation.json").read_text())
    config = protocol["config"]
    progress = json.loads((output/"progress.json").read_text())
    # The main ordered pool must still be far from the final centralized block.
    if progress["phase"]!="evaluation" or progress["completed"]>=280:
        raise SystemExit("Too late to safely schedule the supplementary block")
    selections = json.loads((output/"hyperparameter_trials.json").read_text())["selected"]
    sample_hash = json.loads((output/"sample_provenance.json").read_text())["sha256"]
    order,environment = "order_3","centralized"
    jobs = []
    for method in config["methods"]:
        settings = selections[order][environment][method]
        for seed in config["seeds"]:
            directory = output/"runs"/order/environment/method/f"seed_{seed}"
            key = {"protocol":protocol["fingerprint"],"sample":sample_hash,"order":order,"environment":environment,
                   "method":method,"settings":settings,"seed":seed,"calibration_only":False}
            jobs.append({"order":order,"environment":environment,"method":method,"settings":settings,"seed":seed,
                         "calibration_only":False,"prepared_path":str(output/"splits"/order/"prepared_local_only.pt"),
                         "config":config,"directory":str(directory),
                         "fingerprint":hashlib.sha256(json.dumps(key,sort_keys=True).encode()).hexdigest()})
    save_json(output/"supplementary_execution.json", {"main_workers":3,"supplementary_workers":3,
        "block":"order_3 centralized","cases":len(jobs),"scientific_settings_changed":False,
        "purpose":"Compute a disjoint late block in advance; main executor subsequently resumes completed matching jobs"})
    with ProcessPoolExecutor(max_workers=3) as pool:
        pending = [pool.submit(execute_job,job) for job in jobs]
        for count,future in enumerate(as_completed(pending),1):
            result = future.result()
            save_json(output/"supplementary_progress.json", {"completed":count,"total":len(jobs)})
            print(f"supplementary {count}/{len(jobs)} {result['method']} seed={result['seed']}",flush=True)


if __name__=="__main__": main()
