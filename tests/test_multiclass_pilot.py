import copy
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from evse_ids.multiclass_pilot import (
    TrafficMLP, fedavg, forgetting_gate, masked_logits, metrics, prepare,
    rank_metrics, seed_everything, train_local,
)


class MulticlassPilotTests(unittest.TestCase):
    def test_rank_metrics_ties_and_degenerate_support(self):
        self.assertEqual(rank_metrics([0, 1], [0.5, 0.5]), (0.5, 0.5))
        self.assertEqual(rank_metrics([0, 1], [0.1, 0.9]), (1.0, 1.0))
        self.assertEqual(rank_metrics([0, 0], [0.1, 0.9]), (None, None))

    def test_future_classes_have_zero_probability(self):
        logits = torch.tensor([[0.0, 1.0, 100.0]])
        probability = torch.softmax(masked_logits(logits, [0, 1]), dim=1)
        self.assertEqual(float(probability[0, 2]), 0.0)
        self.assertEqual(int(probability.argmax(1)), 1)

    def test_fedavg_uses_example_counts_and_does_not_mutate_locals(self):
        model = TrafficMLP(2, 3)
        a, b = copy.deepcopy(model), copy.deepcopy(model)
        with torch.no_grad():
            for p in a.parameters(): p.fill_(2)
            for p in b.parameters(): p.fill_(6)
        fedavg(model, [(a, 1), (b, 3)])
        self.assertTrue(all(torch.allclose(p, torch.full_like(p, 5)) for p in model.parameters()))
        self.assertTrue(all(torch.allclose(p, torch.full_like(p, 2)) for p in a.parameters()))

    def test_local_training_learns_types_without_mutating_global(self):
        seed_everything(42)
        x = torch.tensor([[-2.0, 0], [2.0, 0], [0, 2.0]] * 20)
        y = torch.tensor([0, 1, 2] * 20)
        model = TrafficMLP(2, 3)
        before = copy.deepcopy(model.state_dict())
        local, losses = train_local(model, x, y, np.arange(len(y)), [0, 1, 2],
            {"weight_decay": 0.0, "local_epochs": 15, "batch_size": 12, "gradient_clip_norm": None},
            0.01, np.random.default_rng(42))
        self.assertGreater(float((local(x).argmax(1) == y).float().mean()), 0.95)
        self.assertLess(losses[-1], losses[0])
        self.assertTrue(all(torch.equal(before[k], model.state_dict()[k]) for k in before))

    def test_preprocessor_excludes_future_and_evaluation_rows(self):
        labels = np.array(["Benign"] * 60 + ["Aggressive_Scan"] * 60 + ["UDP_Flood"] * 60)
        values = np.r_[np.zeros(120), np.full(60, 10000.0)]
        frame = pd.DataFrame({"Label": labels, "feature": values, "__source_file__": "capture.csv",
                              "__source_row__": np.arange(180), "__evse__": "EVSE-A", "__operating_state__": "charging"})
        config = {"label_column": "Label", "role_fractions": [0.65, 0.15, 0.20],
                  "attack_order": ["reconnaissance", "flooding", "low_rate_rare", "post_rare_vulnerability"], "numeric_z_clip": 5}
        temp_root = Path(__file__).resolve().parents[1] / "tmp" / "multiclass_tests"
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            data = prepare(frame, config, 42, Path(temp))
            import json
            metadata = json.loads((Path(temp)/"preprocessing.json").read_text())
            self.assertEqual(metadata["means"]["feature"], 0)
            manifest = data["manifest"]
            fitted = manifest[manifest.preprocessing_fit]
            self.assertTrue((fitted.persistent_role == "fitting").all())
            self.assertFalse((fitted.label == "UDP_Flood").any())
            starved = manifest[manifest.client == "benign_starved"]
            self.assertFalse((starved.label == "Benign").any())

    def test_false_alarm_rate_is_undefined_without_benign(self):
        m = metrics(np.array([1, 2]), np.array([[0, 1, 0], [0, 0, 1]]),
                    ["Benign", "Slowloris_Scan", "UDP_Flood"], [0, 1, 2])
        self.assertIsNone(m["false_alarm_rate"])
        self.assertEqual(m["rare_attack_recall"], 1)

    def test_forgetting_gate_requires_initial_learning(self):
        config = {"attack_order": ["a", "b"], "minimum_initial_old_task_accuracy": 0.5,
                  "clear_drop_percentage_points": 10, "minimum_seed_fraction_with_clear_drop": 2/3}
        def result(seed, initial, final):
            return {"seed": seed, "history": [{"tasks": {"a": {"attack_accuracy": initial}}},
                    {"tasks": {"a": {"attack_accuracy": final}}}]}
        gate = forgetting_gate([result(42, .9, .2), result(43, .8, .3), result(44, .2, .0)], config, False)
        self.assertTrue(gate["clear_forgetting_observed"])
        self.assertFalse(gate["seed_results"][2]["clear_drop"])
        self.assertFalse(gate["full_comparison_authorized_by_runner"])
        self.assertFalse(gate["data_requirements_satisfied"])


if __name__ == "__main__":
    unittest.main()
