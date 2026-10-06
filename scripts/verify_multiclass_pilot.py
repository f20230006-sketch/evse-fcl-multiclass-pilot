"""Independently verify split boundaries and accuracy drops from saved predictions."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from evse_ids.multiclass_pilot import TrafficMLP
from evse_ids.continual_stable import make_model_frame
from evse_ids.data import PreprocessState, transform_features


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="outputs/multiclass_no_replay_pilot")
    args = parser.parse_args()
    output = ROOT/args.output_dir
    protocol = json.loads((output/"protocol_before_evaluation.json").read_text())
    config = protocol["config"]
    for relative, digest in protocol["source_hashes"].items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest, f"Source changed: {relative}"
    trials = json.loads((output/"hyperparameter_trials.json").read_text())
    assert not trials["evaluation_rows_used_for_selection"]
    assert len(trials["tried"]) == len(config["learning_rates_tried"])
    for directory in (output/"calibration_screen").iterdir():
        assert not list(directory.glob("*predictions.csv")), "Evaluation prediction in calibration-only screen"
        assert json.loads((directory/"results.json").read_text())["calibration_only"]
    checked_rows = 0
    checked_task_accuracies = 0
    for seed in config["seeds"]:
        directory = output/f"seed_{seed}"
        manifest = pd.read_csv(directory/"split_manifest.csv")
        assert not manifest.duplicated(["__source_file__", "__source_row__"]).any()
        assert (manifest.loc[manifest.preprocessing_fit, "persistent_role"] == "fitting").all()
        assert (manifest.loc[manifest.preprocessing_fit, "task"].isin([config["attack_order"][0], "benign_reference_all_tasks"])).all()
        result = json.loads((directory/"results.json").read_text())
        mapping = json.loads((directory/"class_mapping.json").read_text())
        labels = [name for name, _ in sorted(mapping.items(), key=lambda item:item[1])]
        for checkpoint in result["history"]:
            frame = pd.read_csv(directory/f"checkpoint_{checkpoint['checkpoint']}_predictions.csv")
            assert not frame.duplicated("sample_index").any(), "Repeated benign row in pooled evaluation"
            assert (frame.persistent_role == "evaluation").all()
            aligned = manifest.set_index("sample_index").loc[frame.sample_index]
            assert np.array_equal(aligned.class_id.to_numpy(), frame.class_id.to_numpy())
            assert np.array_equal(aligned.__source_row__.to_numpy(), frame.__source_row__.to_numpy())
            assert np.array_equal(aligned.__source_file__.to_numpy(), frame.__source_file__.to_numpy())
            probability = frame[[f"p_{name}" for name in labels]].to_numpy()
            assert np.isfinite(probability).all()
            assert (probability >= 0).all() and (probability <= 1).all()
            assert np.allclose(probability.sum(1), 1, atol=1e-6)
            assert np.array_equal(probability.argmax(1), frame.y_pred.to_numpy())
            for task, metric in checkpoint["tasks"].items():
                attacks = frame[frame.task == task]
                independent_accuracy = float((attacks.y_pred == attacks.class_id).mean())
                assert np.isclose(independent_accuracy, metric["attack_accuracy"])
                assert len(attacks) == metric["attack_support"]
                checked_task_accuracies += 1
            for client, metric in checkpoint["per_client"].items():
                local = frame[frame.client == client]
                assert len(local) == metric["rows"]
                benign = local[local.class_id == 0]
                if len(benign):
                    assert np.isclose(float((benign.y_pred != 0).mean()), metric["false_alarm_rate"])
                else:
                    assert metric["false_alarm_rate"] is None
            checked_rows += len(frame)
        # Recreate frozen inputs and predict from final saved model independently.
        sampled = pd.read_pickle(output/f"sampled_seed_{seed}.pkl")
        prep = json.loads((directory/"preprocessing.json").read_text())
        state = PreprocessState(**{key: prep[key] for key in ["numeric_columns", "categorical_columns", "feature_names", "means", "stds", "categories"]})
        model_frame, _ = make_model_frame(sampled, config["label_column"])
        x = transform_features(model_frame, config["label_column"], state)
        x[:, :len(state.numeric_columns)] = np.clip(x[:, :len(state.numeric_columns)], -config["numeric_z_clip"], config["numeric_z_clip"])
        model = TrafficMLP(x.shape[1], len(mapping))
        model.load_state_dict(torch.load(directory/"final_model.pt", weights_only=True))
        assert sum(p.numel() for p in model.parameters()) == prep["mlp_parameter_count"]
        final = pd.read_csv(directory/"final_predictions.csv")
        with torch.no_grad():
            prediction = model(torch.tensor(x[final.sample_index.to_numpy()], dtype=torch.float32)).argmax(1).numpy()
        assert np.array_equal(prediction, final.y_pred.to_numpy())
        training = json.loads((directory/"training_log.json").read_text())
        assert len(training) == len(config["attack_order"])*config["rounds_per_task"]*5
        for entry in training:
            expected = manifest[(manifest.client == entry["client"]) & (manifest.persistent_role == "fitting") &
                                manifest.task.isin([entry["task"], "benign_reference_all_tasks"])]
            assert len(expected) == entry["fitting_rows"]
            assert entry["replay_rows"] == 0
            assert len(entry["epoch_losses"]) == config["local_epochs"] if len(expected) else not entry["epoch_losses"]
    summary = {"status": "passed", "checked_checkpoint_prediction_rows": checked_rows,
               "checked_task_accuracy_cells": checked_task_accuracies, "source_hashes_match": True,
               "final_saved_models_reproduce_predictions": True, "calibration_screen_excludes_evaluation": True,
               "persistent_role_and_task1_preprocessing_checks": True,
               "scientific_limitation": "Passing verification does not resolve insufficient benign data or low initial reconnaissance accuracy"}
    (output/"verification.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
