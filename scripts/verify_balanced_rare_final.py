"""Independent checks of follow-up predictions, frozen reference splits, and class quotas."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from evse_ids.multiclass_pilot import TrafficMLP


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="outputs/balanced_rare_final")
    parser.add_argument("--allow-partial",action="store_true",help="Check finished cases during a run without claiming completion")
    args = parser.parse_args()
    output = ROOT/args.output_dir
    protocol = json.loads((output/"protocol_before_evaluation.json").read_text())
    config = protocol["config"]
    if not args.allow_partial:
        completion = json.loads((output/"completion.json").read_text())
        assert completion["evaluation_runs"]==len(config["seeds"])*len(config["orders"])*len(config["environments"])*len(config["methods"])
        assert completion["calibration_runs"]==sum(len(config["grids"][m]) for m in config["methods"])*len(config["orders"])*len(config["environments"])
    assert not json.loads((output/"hyperparameter_trials.json").read_text())["test_data_used"]
    for relative,digest in protocol["source_hashes"].items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest,relative
    for relative,digest in protocol["reference_inputs"].items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest,relative
    torch.set_num_threads(1)
    checked_rows,checked_runs,checked_models = 0,0,0
    for order,sequence in config["orders"].items():
        directory = ROOT/config["reference_output"]/"splits"/order
        manifest = pd.read_csv(directory/"split_manifest.csv")
        assert not manifest.duplicated(["__source_file__","__source_row__"]).any()
        fitted = manifest[manifest.preprocessing_fit]
        assert (fitted.persistent_role=="fitting").all()
        assert fitted.task.isin([sequence[0],"benign_reference_all_tasks"]).all()
        data = torch.load(directory/"prepared_local_only.pt",weights_only=False,map_location="cpu")
        source_roles = manifest.persistent_role.to_numpy()
        source_classes = manifest.class_id.to_numpy()
        source_tasks = manifest.task.to_numpy()
        source_clients = manifest.client.to_numpy()
        for result_path in sorted((output/"runs"/order).glob("*/*/seed_*/results.json")):
            if not (result_path.parent/"complete.json").exists():
                continue
            r = json.loads(result_path.read_text())
            checked_runs += 1
            best = {}
            final_prediction = None
            for checkpoint in r["history"]:
                p = np.load(result_path.parent/f"checkpoint_{checkpoint['checkpoint']}_predictions.npz")
                indices,y,pred,prob = p["sample_index"],p["y_true"],p["y_pred"],p["probability"]
                assert len(indices)==len(np.unique(indices))
                assert (source_roles[indices]=="evaluation").all()
                assert np.array_equal(y,source_classes[indices])
                row_tasks,row_clients = source_tasks[indices],source_clients[indices]
                assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=1e-6)
                assert (prob>=0).all() and (prob<=1).all()
                assert np.array_equal(pred,prob.argmax(1))
                for task,m in checkpoint["tasks"].items():
                    mask = row_tasks==task
                    value = float((pred[mask]==y[mask]).mean())
                    assert np.isclose(value,m["attack_accuracy"])
                    assert mask.sum()==m["attack_support"]
                    drop = max(0,best.get(task,value)-value)
                    assert m["forgetting"] is None if r["method"]=="joint" else np.isclose(drop,m["forgetting"])
                    best[task] = max(best.get(task,value),value)
                    for client,cm in m["per_client"].items():
                        local_mask = mask & (row_clients==client)
                        if local_mask.any():
                            assert np.isclose(float((pred[local_mask]==y[local_mask]).mean()),cm["attack_accuracy"])
                for client,m in checkpoint["per_client"].items():
                    mask = row_clients==client
                    benign = mask & (y==0)
                    if benign.any():
                        assert np.isclose(float((pred[benign]!=0).mean()),m["false_alarm_rate"])
                    else:
                        assert m["false_alarm_rate"] is None
                    labels = np.unique(y[mask])
                    macro = float(np.mean([np.mean(pred[mask & (y==c)]==c) for c in labels]))
                    assert np.isclose(macro,m["macro_recall"])
                checked_rows += len(indices)
                final_prediction = (indices,pred,prob)
            # Saved final weights reproduce all final class predictions.
            model = TrafficMLP(data["x"].shape[1],len(data["classes"]))
            model.load_state_dict(torch.load(result_path.parent/"final_model.pt",weights_only=True))
            indices,pred,prob = final_prediction
            with torch.no_grad():
                batches = [torch.softmax(model(data["x"][indices[s:s+4096]]),1).numpy() for s in range(0,len(indices),4096)]
            independently_predicted = np.concatenate(batches)
            assert np.array_equal(independently_predicted.argmax(1),pred)
            assert np.allclose(independently_predicted,prob,atol=1e-6)
            checked_models += 1
            memory = json.loads((result_path.parent/"memory_audit.json").read_text())
            previous = {}
            capacity = int(r["method"].rsplit("_",1)[1]) * (1 if r["environment"]=="federated" else 5)
            for entry in memory:
                rows = entry.get("memory_rows",entry.get("fisher_rows",[]))
                assert (source_roles[rows]=="fitting").all()
                if "memory_rows" in entry:
                    assert len(rows)<=capacity and len(rows)==len(set(rows))
                else:
                    assert len(rows)<=config["fisher_max_examples_per_client_task"]
                allowed = sequence[:entry["stage"]]+["benign_reference_all_tasks"]
                assert np.isin(source_tasks[rows],allowed).all()
                assert (source_clients[rows] == entry["client"]).all() if r["environment"]=="federated" else True
                if "memory_rows" in entry:
                    client=entry["client"]
                    current=np.flatnonzero((source_roles=="fitting") & np.isin(source_tasks,[sequence[entry["stage"]-1],"benign_reference_all_tasks"]) & ((source_clients==client) if r["environment"]=="federated" else True))
                    pool=np.unique(np.concatenate([previous.get(client,np.array([],dtype=int)),current]))
                    assert np.isin(rows,pool).all(), "Discarded history accessed"
                    if r["method"].startswith("class_balanced_"):
                        labels=source_classes[pool];available={c:int((labels==c).sum()) for c in np.unique(labels)}
                        used={c:int((source_classes[rows]==c).sum()) for c in available}
                        unsaturated=[used[c] for c in available if used[c]<available[c]]
                        assert not unsaturated or max(unsaturated)-min(unsaturated)<=1, "Unequal feasible quotas"
                        assert len(rows)==min(capacity,len(pool))
                    if r['method'].startswith('balanced_rare_'):
                        reserved=np.asarray(entry['reserved_rows'],dtype=int)
                        balanced=np.asarray(entry['balanced_rows'],dtype=int)
                        label_names=np.asarray(data['labels']).astype(str)
                        rare=pool[np.isin(label_names[pool],['Slowloris_Scan','ICMP_Fragmentation'])]
                        quota=int(np.floor(capacity*r['settings']['rare_quota_fraction']))
                        assert entry['rare_quota_slots']==quota
                        assert entry['rare_candidates']==len(rare)
                        assert len(reserved)==min(quota,len(rare))
                        assert np.isin(reserved,rare).all()
                        assert not set(reserved)&set(balanced)
                        assert set(rows)==set(reserved)|set(balanced)
                        assert len(rows)==min(capacity,len(pool))
                        def feasible_counts(candidates, selected):
                            buckets={label:int((label_names[candidates]==label).sum()) for label in sorted(set(label_names[candidates]))}
                            target={label:0 for label in buckets}
                            remaining=len(selected)
                            while remaining:
                                for label in buckets:
                                    if target[label]<buckets[label] and remaining:
                                        target[label]+=1;remaining-=1
                            assert target=={label:int((label_names[selected]==label).sum()) for label in buckets}
                        feasible_counts(rare,reserved)
                        feasible_counts(np.setdiff1d(pool,reserved),balanced)
                    assert entry["capacity"]==capacity
                    for c in entry["seen_classes"]:
                        assert entry["class_counts"][data["classes"][c]]==int((source_classes[rows]==c).sum())
                    previous[client]=np.asarray(rows,dtype=int)
            summary = r["summary"]
            old = [r["history"][-1]["tasks"][name]["attack_accuracy"] for name in sequence[:-1]]
            assert np.isclose(np.mean(old),summary["old_task_accuracy"])
    for directory in (output/"calibration").glob("*/*/*/trial_*"):
        assert not list(directory.glob("*predictions.npz"))
        assert json.loads((directory/"results.json").read_text())["calibration_only"]
    trials=json.loads((output/'hyperparameter_trials.json').read_text())
    selection_time=(output/'hyperparameter_trials.json').stat().st_mtime_ns
    calibration_cases=list((output/'calibration').glob('*/*/*/trial_*/results.json'))
    for path in calibration_cases:
        record=json.loads(path.read_text())
        assert np.isclose(record['selection_score'],np.mean([h['calibration']['macro_recall'] for h in record['history']]))
        assert (path.parent/'complete.json').stat().st_mtime_ns<=selection_time
    evaluation_predictions=list((output/'runs').glob('*/*/*/seed_*/*predictions.npz'))
    if not args.allow_partial:assert len(evaluation_predictions)==480
    for path in evaluation_predictions:
        assert path.stat().st_mtime_ns>=selection_time, 'Evaluation preceded calibration selection'
    for order in config['orders']:
        for environment in config['environments']:
            for method in config['methods']:
                settings=config['grids'][method]
                values=[json.loads((output/'calibration'/order/environment/method/f'trial_{i}'/'results.json').read_text())['selection_score'] for i in range(len(settings))]
                chosen=settings[max(range(len(values)),key=lambda i:(values[i],-i))]
                assert trials['selected'][order][environment][method]==chosen
                for result in (output/'runs'/order/environment/method).glob('seed_*/results.json'):
                    assert json.loads(result.read_text())['settings']==chosen
    assert checked_runs==checked_models
    if not args.allow_partial:
        assert checked_runs==completion["evaluation_runs"]
    report = {"status":"partial_checks_passed" if args.allow_partial else "passed","evaluation_runs":checked_runs,"saved_models_checked":checked_models,
              "checkpoint_prediction_rows_checked":checked_rows,"source_hashes_match":True,
              "calibration_evaluation_isolation":True,"persistent_roles_and_task1_preprocessing":True,
              "memory_capacity_and_fitting_roles":True,"benign_support_exception_disclosed":True,
              "rare_reservation_and_balanced_feasible_quotas":True,"fixed_reference_input_hashes":True,
              "all_calibration_completed_before_evaluation":True,"calibration_trials_checked":len(calibration_cases)}
    (output/("verification_partial.json" if args.allow_partial else "verification.json")).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__": main()
