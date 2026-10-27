# Exploratory model tuning: results update

27 October 2026 | Percentages; paired differences in percentage points.

## 1. Work completed

- Completed 108 common-configuration calibration fits, 72 replay calibration fits, then 180 evaluations: three methods × three orders × two settings × ten seeds.
- Shared selected MLP: 128/64, learning rate 0.001, dropout 0.0, weight decay 0.0001, 5 local epochs, five rounds/task.
- Storage remains 60 examples/client and 300 centrally. Original labels, splits, client allocations and Task-1 preprocessing remain unchanged.
- Model parameter counts by order: 27,023, 20,367, 25,999; model_profile.json records the frozen-model comparison.

## 2. Federated results

Mean ± SD over ten seed averages of three orders; merged-Scan primary scoring.

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| Frozen balanced | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.56 ± 4.19 | 77.97 ± 1.05 |
| Frozen protected | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.73 ± 2.36 | 47.15 ± 3.82 |
| Frozen balanced+rare | 85.52 ± 1.27 | 14.24 ± 1.27 | 76.62 ± 4.16 | 79.03 ± 1.00 |
| Tuned balanced | 84.95 ± 1.77 | 14.64 ± 1.84 | 71.83 ± 4.87 | 76.12 ± 1.73 |
| Tuned protected | 77.00 ± 2.57 | 22.46 ± 2.64 | 83.93 ± 3.21 | 46.98 ± 4.14 |
| Tuned balanced+rare | 87.53 ± 1.74 | 11.69 ± 1.77 | 81.77 ± 5.79 | 77.26 ± 1.00 |

## 3. Frozen-to-tuned comparison

Paired 95% intervals; better/worse denotes significant direction.
- Tuned balanced+rare − frozen balanced+rare: old accuracy +2.00 [+1.06, +2.95]; better; forgetting -2.54 [-3.56, -1.52]; better; Slowloris +5.16 [+1.87, +8.44]; better; worst client -1.77 [-2.92, -0.62]; worse.

## 4. Centralized results

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| Frozen balanced | 90.03 ± 0.87 | 9.43 ± 1.02 | 83.36 ± 2.93 | 84.88 ± 0.97 |
| Frozen protected | 80.48 ± 1.62 | 19.28 ± 1.64 | 90.37 ± 1.81 | 60.27 ± 3.91 |
| Frozen balanced+rare | 91.70 ± 0.89 | 7.71 ± 1.05 | 88.36 ± 2.22 | 85.52 ± 1.03 |
| Tuned balanced | 90.78 ± 0.72 | 8.37 ± 0.92 | 86.27 ± 2.05 | 85.17 ± 1.55 |
| Tuned protected | 83.18 ± 1.89 | 16.25 ± 1.95 | 95.49 ± 1.29 | 61.61 ± 3.57 |
| Tuned balanced+rare | 92.46 ± 0.48 | 6.71 ± 0.56 | 92.02 ± 1.61 | 86.03 ± 1.03 |

## 5. Matched-backbone federated comparisons

Tuned balanced+rare minus the other tuned method.

| Comparison | Old accuracy | Slowloris | Worst client |
| --- | --- | --- | --- |
| vs tuned balanced | +2.58 [+0.47, +4.69]; better | +9.94 [+3.78, +16.09]; better | +1.14 [-0.55, +2.82]; not significant |
| vs tuned protected | +10.52 [+8.52, +12.52]; better | -2.16 [-7.01, +2.70]; not significant | +30.28 [+27.08, +33.49]; better |

## Interpretation

- The tuned policy improves federated retention, forgetting and Slowloris versus its frozen version, but worst-client score falls by 1.77 points significantly. This is not an across-the-board improvement. A larger model and changed selection/training pipeline contribute; gains cannot automatically be credited to the quota.
- Against newly tuned class-balanced, old accuracy and Slowloris improve significantly; worst-client difference is not significant. Against tuned protected, old accuracy and worst-client score improve significantly, while the Slowloris difference is not significant. Non-significance does not establish equivalence.
- Selection used the new final-calibration retention/Slowloris/worst-client objective. Earlier evaluation outcomes were already known: this is exploratory, not untouched-test confirmation. All orders and losses are included; ten-seed intervals describe one fixed split and are unadjusted for multiplicity.

Only 16 benign and five fragmentation evaluation examples exist. No fragmentation or false-alarm improvement is inferred. Larger models, if selected, increase parameter storage; replay budgets count examples, not all memory bytes. The previously sent manuscript and results remain unchanged.

## Common model calibration scores

| Candidate | Settings | Mean calibration objective |
| --- | --- | --- |
| 0 | {"hidden_sizes": [64, 32], "dropout": 0.0, "weight_decay": 0.0001, "local_epochs": 5, "learning_rate": 0.003} | 0.817453 |
| 1 | {"hidden_sizes": [64, 32], "dropout": 0.0, "weight_decay": 0.0001, "local_epochs": 5, "learning_rate": 0.001} | 0.815055 |
| 2 | {"hidden_sizes": [64, 32], "dropout": 0.0, "weight_decay": 0.0001, "local_epochs": 5, "learning_rate": 0.0005} | 0.797635 |
| 3 | {"hidden_sizes": [128, 64], "dropout": 0.0, "weight_decay": 0.0001, "local_epochs": 5, "learning_rate": 0.001} | 0.823440 |
| 4 | {"hidden_sizes": [64, 32], "dropout": 0.1, "weight_decay": 0.001, "local_epochs": 5, "learning_rate": 0.001} | 0.792399 |
| 5 | {"hidden_sizes": [128, 64], "dropout": 0.1, "weight_decay": 0.001, "local_epochs": 3, "learning_rate": 0.001} | 0.799547 |

## Replay selections

| Order | Environment | Method | Rare share | Replay fraction |
| --- | --- | --- | --- | --- |
| order_1 | federated | tuned_class_balanced_60 | 0.0 | 0.5 |
| order_1 | federated | tuned_protected_60 | 0.2 | 0.5 |
| order_1 | federated | tuned_balanced_rare_60 | 0.1 | 0.75 |
| order_1 | centralized | tuned_class_balanced_60 | 0.0 | 0.75 |
| order_1 | centralized | tuned_protected_60 | 0.2 | 0.5 |
| order_1 | centralized | tuned_balanced_rare_60 | 0.2 | 0.75 |
| order_2 | federated | tuned_class_balanced_60 | 0.0 | 0.5 |
| order_2 | federated | tuned_protected_60 | 0.2 | 0.75 |
| order_2 | federated | tuned_balanced_rare_60 | 0.1 | 0.5 |
| order_2 | centralized | tuned_class_balanced_60 | 0.0 | 0.5 |
| order_2 | centralized | tuned_protected_60 | 0.2 | 0.5 |
| order_2 | centralized | tuned_balanced_rare_60 | 0.1 | 0.5 |
| order_3 | federated | tuned_class_balanced_60 | 0.0 | 0.75 |
| order_3 | federated | tuned_protected_60 | 0.2 | 0.75 |
| order_3 | federated | tuned_balanced_rare_60 | 0.1 | 0.75 |
| order_3 | centralized | tuned_class_balanced_60 | 0.0 | 0.75 |
| order_3 | centralized | tuned_protected_60 | 0.2 | 0.75 |
| order_3 | centralized | tuned_balanced_rare_60 | 0.2 | 0.5 |

The protected allocator always reserves 20% benign and 20% rare; class-balanced has no reservation. The new policy uses its selected rare share. All share the selected model configuration. The new criterion is an equal-weight final-calibration average of old accuracy, Slowloris recall and worst-client macro recall, replacing the earlier mean-checkpoint original-type criterion. This change is part of the pipeline comparison.

## Training work and model size

The actual per-run settings and selected backbone are authoritative. Some top-level configuration fields are inherited frozen defaults and are overridden by these settings. A larger replay fraction reduces current examples per minibatch and increases optimizer steps for the same number of current-data epochs; compute is not matched. Elapsed times below are concurrent desktop execution observations, not controlled latency benchmarks or deployment measurements.

| Environment | Method | Mean optimizer steps | Mean elapsed seconds |
| --- | --- | --- | --- |
| centralized | tuned_balanced_rare_60 | 9691.7 | 16.74 |
| centralized | tuned_class_balanced_60 | 12508.3 | 45.80 |
| centralized | tuned_protected_60 | 10700.0 | 45.79 |
| federated | tuned_balanced_rare_60 | 12675.0 | 15.92 |
| federated | tuned_class_balanced_60 | 10858.3 | 13.57 |
| federated | tuned_protected_60 | 12666.7 | 15.68 |

{"order_1": 27023, "order_2": 20367, "order_3": 25999}

Replay example counts remain matched; total model-memory bytes and optimizer work can differ from the frozen study.

## Offline proof-of-concept demonstration

Run scripts/demo_exploratory_model.py to load a saved tuned model and classify one deterministically selected evaluation example per merged class. Examples are selected before inspecting predictions; errors are retained. This is offline inference on prepared flow features, not a live packet IDS, a fresh test, calibrated probabilities or an accuracy estimate from ten examples. The 60-row replay budget is a logical access constraint in the offline simulator; full feature tensors remain resident for auditing, so it is not a measured physical-RAM limit.

## merged_scans / federated

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| balanced_rare_60 | 85.52 ± 1.27 | 14.24 ± 1.27 | 76.62 ± 4.16 | 79.03 ± 1.00 |
| class_balanced_60 | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.56 ± 4.19 | 77.97 ± 1.05 |
| protected_60 | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.73 ± 2.36 | 47.15 ± 3.82 |
| tuned_balanced_rare_60 | 87.53 ± 1.74 | 11.69 ± 1.77 | 81.77 ± 5.79 | 77.26 ± 1.00 |
| tuned_class_balanced_60 | 84.95 ± 1.77 | 14.64 ± 1.84 | 71.83 ± 4.87 | 76.12 ± 1.73 |
| tuned_protected_60 | 77.00 ± 2.57 | 22.46 ± 2.64 | 83.93 ± 3.21 | 46.98 ± 4.14 |

## merged_scans / centralized

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| balanced_rare_60 | 91.70 ± 0.89 | 7.71 ± 1.05 | 88.36 ± 2.22 | 85.52 ± 1.03 |
| class_balanced_60 | 90.03 ± 0.87 | 9.43 ± 1.02 | 83.36 ± 2.93 | 84.88 ± 0.97 |
| protected_60 | 80.48 ± 1.62 | 19.28 ± 1.64 | 90.37 ± 1.81 | 60.27 ± 3.91 |
| tuned_balanced_rare_60 | 92.46 ± 0.48 | 6.71 ± 0.56 | 92.02 ± 1.61 | 86.03 ± 1.03 |
| tuned_class_balanced_60 | 90.78 ± 0.72 | 8.37 ± 0.92 | 86.27 ± 2.05 | 85.17 ± 1.55 |
| tuned_protected_60 | 83.18 ± 1.89 | 16.25 ± 1.95 | 95.49 ± 1.29 | 61.61 ± 3.57 |

## merged_scans / centralized / averaged: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.76 | [+0.27, +1.25] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -1.06 | [-1.65, -0.46] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +2.91 | [+1.03, +4.79] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +0.30 | [-0.57, +1.17] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +2.69 | [+2.00, +3.38] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -3.03 | [-3.78, -2.29] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +5.12 | [+3.66, +6.57] | better | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +1.34 | [-0.91, +3.60] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +0.76 | [+0.35, +1.17] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -0.99 | [-1.38, -0.60] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +3.66 | [+2.50, +4.82] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | +0.52 | [-0.32, +1.35] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +1.67 | [+1.04, +2.31] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -1.66 | [-2.39, -0.92] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +5.75 | [+3.52, +7.98] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.86 | [-0.23, +1.95] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +9.28 | [+7.68, +10.89] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -9.53 | [-11.22, -7.84] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -3.47 | [-4.91, -2.02] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +24.42 | [+21.88, +26.96] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +2.43 | [+1.81, +3.06] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -2.72 | [-3.39, -2.04] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +8.66 | [+6.26, +11.06] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +1.16 | [+0.42, +1.89] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +11.98 | [+10.59, +13.37] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -12.57 | [-14.05, -11.08] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +1.65 | [-0.19, +3.49] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +25.76 | [+23.02, +28.51] | better | overall pipeline |

## merged_scans / centralized / order_1: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.85 | [-0.01, +1.71] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -1.41 | [-2.31, -0.51] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +2.77 | [-0.36, +5.90] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +0.32 | [-2.43, +3.07] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +0.14 | [-0.83, +1.11] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -0.12 | [-1.10, +0.85] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -0.88 | [-1.74, -0.03] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +1.14 | [-1.77, +4.05] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +2.86 | [+2.00, +3.72] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -3.41 | [-4.20, -2.62] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +10.75 | [+7.59, +13.91] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | +1.85 | [+0.08, +3.62] | better | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +3.51 | [+2.60, +4.41] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -3.50 | [-4.41, -2.59] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +12.52 | [+9.19, +15.85] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +2.04 | [-1.12, +5.21] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +0.45 | [-0.83, +1.73] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -1.36 | [-2.75, +0.04] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -8.83 | [-11.17, -6.50] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +12.07 | [+9.88, +14.26] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +4.36 | [+3.21, +5.51] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -4.91 | [-5.95, -3.88] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +15.28 | [+11.44, +19.12] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +2.36 | [+0.71, +4.01] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +0.59 | [-1.08, +2.26] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -1.48 | [-3.35, +0.39] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -9.72 | [-12.14, -7.29] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +13.21 | [+9.19, +17.23] | better | overall pipeline |

## merged_scans / centralized / order_2: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | -0.52 | [-1.02, -0.02] | worse | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | +0.52 | [+0.02, +1.01] | worse | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +0.25 | [-0.18, +0.68] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -0.64 | [-1.93, +0.65] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +3.26 | [+2.07, +4.46] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -3.26 | [-4.47, -2.06] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -1.05 | [-2.06, -0.04] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.75 | [-4.71, +6.21] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | -0.52 | [-1.02, -0.02] | worse | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | +0.52 | [+0.02, +1.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +0.25 | [-0.18, +0.68] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.64 | [-1.93, +0.65] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +27.76 | [+24.16, +31.36] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -27.76 | [-31.36, -24.16] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | +0.78 | [-0.30, +1.87] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +51.83 | [+45.74, +57.93] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | -0.52 | [-1.02, -0.02] | worse | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | +0.52 | [+0.02, +1.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +0.25 | [-0.18, +0.68] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -0.64 | [-1.93, +0.65] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +31.02 | [+28.18, +33.87] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -31.03 | [-33.86, -28.19] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -0.27 | [-0.52, -0.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +52.58 | [+45.91, +59.26] | better | overall pipeline |

## merged_scans / centralized / order_3: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +1.94 | [+0.63, +3.26] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -2.28 | [-3.82, -0.74] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +5.72 | [+0.98, +10.46] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +1.21 | [+0.38, +2.04] | better | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +4.68 | [+3.33, +6.03] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -5.71 | [-7.24, -4.19] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +17.28 | [+12.67, +21.90] | better | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +2.14 | [+0.11, +4.18] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | -0.05 | [-1.00, +0.91] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -0.09 | [-1.17, +0.99] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | -0.02 | [-3.59, +3.56] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | +0.34 | [-0.43, +1.10] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +1.51 | [-0.48, +3.51] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -1.47 | [-3.79, +0.85] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +4.73 | [-2.31, +11.78] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.54 | [-0.34, +1.41] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | -0.36 | [-1.65, +0.92] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | +0.52 | [-1.04, +2.08] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -2.35 | [-6.90, +2.20] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +9.36 | [+7.40, +11.31] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +3.46 | [+1.33, +5.59] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -3.75 | [-6.31, -1.19] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +10.45 | [+2.62, +18.28] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +1.75 | [+0.47, +3.03] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +4.32 | [+2.79, +5.85] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -5.19 | [-6.97, -3.42] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +14.93 | [+9.37, +20.49] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +11.50 | [+10.83, +12.17] | better | overall pipeline |

## merged_scans / federated / averaged: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.96 | [+0.28, +1.63] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -1.14 | [-1.84, -0.43] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +0.27 | [-1.56, +2.10] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -1.84 | [-3.34, -0.35] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +4.17 | [+3.37, +4.96] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -4.37 | [-5.21, -3.54] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +1.20 | [-0.42, +2.82] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | -0.18 | [-1.82, +1.47] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +2.00 | [+1.06, +2.95] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -2.54 | [-3.56, -1.52] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +5.16 | [+1.87, +8.44] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -1.77 | [-2.92, -0.62] | worse | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +2.58 | [+0.47, +4.69] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -2.94 | [-5.10, -0.78] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +9.94 | [+3.78, +16.09] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +1.14 | [-0.55, +2.82] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +10.52 | [+8.52, +12.52] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -10.77 | [-12.82, -8.71] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -2.16 | [-7.01, +2.70] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +30.28 | [+27.08, +33.49] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +3.54 | [+1.66, +5.41] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -4.08 | [-5.96, -2.20] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +10.21 | [+4.26, +16.16] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -0.71 | [-1.78, +0.37] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +14.69 | [+12.95, +16.42] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -15.14 | [-16.86, -13.42] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -0.96 | [-5.93, +4.02] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +30.11 | [+27.05, +33.16] | better | overall pipeline |

## merged_scans / federated / order_1: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.49 | [-0.14, +1.13] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -0.72 | [-1.46, +0.03] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +1.43 | [-0.35, +3.21] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -1.05 | [-4.35, +2.26] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +2.68 | [+1.51, +3.85] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -2.73 | [-3.89, -1.57] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +12.95 | [+11.46, +14.44] | better | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +1.04 | [-0.54, +2.61] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +1.13 | [-0.27, +2.54] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -1.77 | [-3.16, -0.39] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +5.47 | [+0.50, +10.44] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -2.54 | [-6.14, +1.06] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +4.22 | [+1.03, +7.41] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -4.64 | [-7.75, -1.53] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +15.63 | [+5.15, +26.12] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +1.45 | [-3.24, +6.14] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +11.94 | [+6.96, +16.91] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -12.59 | [-17.54, -7.64] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -22.33 | [-31.61, -13.06] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +31.33 | [+23.15, +39.51] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +4.72 | [+1.78, +7.65] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -5.35 | [-8.15, -2.56] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +17.07 | [+7.45, +26.69] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +0.40 | [-2.62, +3.42] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +14.62 | [+9.73, +19.51] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -15.32 | [-20.17, -10.46] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -9.38 | [-18.84, +0.08] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +32.37 | [+24.36, +40.37] | better | overall pipeline |

## merged_scans / federated / order_2: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +3.17 | [+2.17, +4.18] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -3.17 | [-4.17, -2.17] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | -0.62 | [-1.26, +0.02] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -1.88 | [-3.47, -0.28] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +7.93 | [+5.87, +9.99] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -7.93 | [-9.98, -5.87] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -17.47 | [-21.11, -13.82] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | -1.99 | [-5.45, +1.48] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +3.17 | [+2.17, +4.18] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -3.17 | [-4.17, -2.17] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | -0.62 | [-1.26, +0.02] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -1.88 | [-3.47, -0.28] | worse | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +21.52 | [+18.95, +24.08] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -21.51 | [-24.08, -18.95] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | +19.87 | [+16.96, +22.77] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +58.77 | [+56.53, +61.01] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +3.17 | [+2.17, +4.18] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -3.17 | [-4.17, -2.17] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | -0.62 | [-1.26, +0.02] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -1.88 | [-3.47, -0.28] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +29.44 | [+27.57, +31.32] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -29.44 | [-31.32, -27.56] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +2.40 | [-1.02, +5.82] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +56.78 | [+53.50, +60.07] | better | overall pipeline |

## merged_scans / federated / order_3: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | -0.80 | [-2.32, +0.72] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | +0.47 | [-1.21, +2.16] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +0.00 | [-5.57, +5.57] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -2.61 | [-5.65, +0.44] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +1.89 | [+0.44, +3.33] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -2.47 | [-4.06, -0.88] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +8.12 | [+3.22, +13.01] | better | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.41 | [-1.23, +2.05] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +1.71 | [-0.41, +3.82] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -2.69 | [-5.02, -0.36] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +10.62 | [+4.28, +16.95] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.89 | [-3.50, +1.72] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +3.52 | [-0.32, +7.37] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -4.19 | [-8.31, -0.06] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +14.18 | [+3.87, +24.50] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +1.96 | [-2.66, +6.58] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | -1.88 | [-4.61, +0.84] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | +1.80 | [-1.27, +4.87] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -4.00 | [-11.21, +3.21] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +0.75 | [-3.01, +4.51] | not significant | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +2.72 | [-0.59, +6.03] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -3.71 | [-7.20, -0.22] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +14.18 | [+5.23, +23.14] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -0.65 | [-4.07, +2.78] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +0.00 | [-2.27, +2.28] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -0.67 | [-3.09, +1.75] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +4.12 | [-1.37, +9.60] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +1.17 | [-1.81, +4.14] | not significant | overall pipeline |

## merged_scans: every order

| Environment | Method | Order | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- | --- | --- |
| centralized | balanced_rare_60 | order_1 | 91.18 ± 0.83 | 8.27 ± 0.94 | 75.68 ± 2.24 | 83.83 ± 3.48 |
| centralized | balanced_rare_60 | order_2 | 88.66 ± 0.96 | 11.24 ± 0.95 | 99.42 ± 0.68 | 85.93 ± 1.04 |
| centralized | balanced_rare_60 | order_3 | 95.24 ± 1.76 | 3.62 ± 2.08 | 89.98 ± 5.90 | 86.80 ± 1.38 |
| centralized | class_balanced_60 | order_1 | 89.68 ± 1.35 | 9.77 ± 1.43 | 71.15 ± 4.13 | 83.32 ± 3.26 |
| centralized | class_balanced_60 | order_2 | 88.66 ± 0.96 | 11.24 ± 0.95 | 99.42 ± 0.68 | 85.93 ± 1.04 |
| centralized | class_balanced_60 | order_3 | 91.73 ± 2.15 | 7.28 ± 2.66 | 79.52 ± 8.13 | 85.39 ± 1.51 |
| centralized | protected_60 | order_1 | 93.45 ± 2.21 | 6.34 ± 2.24 | 96.15 ± 1.59 | 72.47 ± 5.40 |
| centralized | protected_60 | order_2 | 57.12 ± 3.68 | 42.78 ± 3.68 | 99.93 ± 0.14 | 32.70 ± 8.97 |
| centralized | protected_60 | order_3 | 90.87 ± 1.43 | 8.72 ± 1.53 | 75.03 ± 5.01 | 75.64 ± 1.03 |
| centralized | tuned_balanced_rare_60 | order_1 | 94.04 ± 0.67 | 4.86 ± 0.64 | 86.43 ± 3.13 | 85.68 ± 2.61 |
| centralized | tuned_balanced_rare_60 | order_2 | 88.14 ± 1.01 | 11.76 ± 1.01 | 99.67 ± 0.28 | 85.29 ± 2.09 |
| centralized | tuned_balanced_rare_60 | order_3 | 95.19 ± 1.43 | 3.53 ± 1.76 | 89.97 ± 5.37 | 87.14 ± 0.59 |
| centralized | tuned_class_balanced_60 | order_1 | 90.53 ± 1.06 | 8.36 ± 1.40 | 73.92 ± 3.34 | 83.63 ± 3.70 |
| centralized | tuned_class_balanced_60 | order_2 | 88.14 ± 1.01 | 11.76 ± 1.01 | 99.67 ± 0.28 | 85.29 ± 2.09 |
| centralized | tuned_class_balanced_60 | order_3 | 93.68 ± 1.67 | 5.00 ± 1.88 | 85.23 ± 5.64 | 86.60 ± 0.72 |
| centralized | tuned_protected_60 | order_1 | 93.59 ± 1.57 | 6.21 ± 1.58 | 95.27 ± 1.96 | 73.61 ± 2.82 |
| centralized | tuned_protected_60 | order_2 | 60.38 ± 4.68 | 39.52 ± 4.69 | 98.88 ± 1.44 | 33.45 ± 9.05 |
| centralized | tuned_protected_60 | order_3 | 95.56 ± 0.76 | 3.01 ± 0.94 | 92.32 ± 2.84 | 77.78 ± 2.69 |
| federated | balanced_rare_60 | order_1 | 86.83 ± 3.83 | 12.87 ± 3.84 | 62.57 ± 11.99 | 80.56 ± 2.70 |
| federated | balanced_rare_60 | order_2 | 82.21 ± 1.25 | 17.72 ± 1.25 | 99.87 ± 0.22 | 81.69 ± 1.35 |
| federated | balanced_rare_60 | order_3 | 87.53 ± 1.90 | 12.12 ± 1.93 | 67.42 ± 2.11 | 74.84 ± 2.81 |
| federated | class_balanced_60 | order_1 | 83.24 ± 2.79 | 16.45 ± 2.74 | 50.97 ± 8.68 | 77.62 ± 2.79 |
| federated | class_balanced_60 | order_2 | 82.21 ± 1.25 | 17.72 ± 1.25 | 99.87 ± 0.22 | 81.69 ± 1.35 |
| federated | class_balanced_60 | order_3 | 86.52 ± 2.86 | 13.14 ± 2.87 | 63.85 ± 7.66 | 74.59 ± 1.89 |
| federated | protected_60 | order_1 | 73.34 ± 6.09 | 26.42 ± 6.10 | 77.42 ± 2.19 | 45.65 ± 10.49 |
| federated | protected_60 | order_2 | 55.94 ± 1.45 | 43.99 ± 1.45 | 96.85 ± 4.47 | 23.03 ± 4.47 |
| federated | protected_60 | order_3 | 89.24 ± 1.93 | 10.10 ± 2.24 | 73.92 ± 6.13 | 72.78 ± 2.14 |
| federated | tuned_balanced_rare_60 | order_1 | 87.96 ± 3.98 | 11.10 ± 3.95 | 68.03 ± 12.03 | 78.02 ± 4.15 |
| federated | tuned_balanced_rare_60 | order_2 | 85.38 ± 1.74 | 14.55 ± 1.74 | 99.25 ± 0.94 | 79.82 ± 2.21 |
| federated | tuned_balanced_rare_60 | order_3 | 89.24 ± 2.62 | 9.43 ± 2.81 | 78.03 ± 7.76 | 73.95 ± 3.67 |
| federated | tuned_class_balanced_60 | order_1 | 83.74 ± 3.50 | 15.74 ± 3.61 | 52.40 ± 10.68 | 76.57 ± 3.05 |
| federated | tuned_class_balanced_60 | order_2 | 85.38 ± 1.74 | 14.55 ± 1.74 | 99.25 ± 0.94 | 79.82 ± 2.21 |
| federated | tuned_class_balanced_60 | order_3 | 85.72 ± 3.73 | 13.62 ± 3.99 | 63.85 ± 10.30 | 71.98 ± 4.52 |
| federated | tuned_protected_60 | order_1 | 76.02 ± 6.23 | 23.69 ± 6.22 | 90.37 ± 2.27 | 46.69 ± 10.85 |
| federated | tuned_protected_60 | order_2 | 63.86 ± 2.77 | 36.07 ± 2.76 | 79.38 ± 3.20 | 21.05 ± 2.46 |
| federated | tuned_protected_60 | order_3 | 91.12 ± 3.01 | 7.63 ± 3.41 | 82.03 ± 8.22 | 73.19 ± 3.02 |

## original_type / federated

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| balanced_rare_60 | 49.58 ± 1.97 | 33.08 ± 1.99 | 78.27 ± 5.01 | 52.41 ± 0.69 |
| class_balanced_60 | 47.68 ± 1.68 | 34.97 ± 1.67 | 72.25 ± 4.12 | 51.71 ± 0.72 |
| protected_60 | 42.78 ± 2.52 | 38.80 ± 2.76 | 86.97 ± 2.57 | 30.85 ± 2.56 |
| tuned_balanced_rare_60 | 54.65 ± 1.66 | 26.44 ± 1.66 | 83.89 ± 4.83 | 51.56 ± 0.64 |
| tuned_class_balanced_60 | 50.99 ± 2.18 | 30.38 ± 2.17 | 74.22 ± 4.34 | 50.84 ± 1.11 |
| tuned_protected_60 | 45.87 ± 2.65 | 34.88 ± 2.86 | 85.27 ± 2.69 | 30.79 ± 2.73 |

## original_type / centralized

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| balanced_rare_60 | 55.19 ± 1.07 | 26.84 ± 1.11 | 89.79 ± 1.26 | 55.69 ± 0.56 |
| class_balanced_60 | 54.36 ± 1.79 | 27.77 ± 1.83 | 86.08 ± 1.67 | 55.35 ± 0.50 |
| protected_60 | 51.61 ± 1.58 | 31.16 ± 1.63 | 95.78 ± 2.06 | 39.57 ± 2.50 |
| tuned_balanced_rare_60 | 56.56 ± 0.89 | 25.17 ± 0.93 | 93.69 ± 0.70 | 55.66 ± 0.61 |
| tuned_class_balanced_60 | 58.88 ± 1.69 | 23.08 ± 1.72 | 88.17 ± 1.72 | 55.36 ± 0.79 |
| tuned_protected_60 | 53.13 ± 1.75 | 29.14 ± 1.86 | 96.11 ± 0.97 | 39.98 ± 2.46 |

## original_type / centralized / averaged: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +4.52 | [+2.92, +6.11] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -4.69 | [-6.31, -3.06] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +2.09 | [+0.93, +3.26] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +0.01 | [-0.63, +0.65] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +1.52 | [+0.69, +2.35] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -2.02 | [-2.89, -1.14] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +0.33 | [-1.30, +1.96] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.42 | [-1.05, +1.88] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +1.37 | [+1.06, +1.68] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -1.67 | [-2.15, -1.19] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +3.89 | [+3.05, +4.74] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.04 | [-0.47, +0.40] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | -2.32 | [-3.38, -1.26] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +2.09 | [+1.02, +3.15] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +5.52 | [+4.11, +6.92] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.29 | [-0.20, +0.78] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +3.43 | [+1.73, +5.13] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -3.97 | [-5.76, -2.18] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -2.42 | [-3.28, -1.55] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +15.67 | [+14.05, +17.29] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +2.20 | [+1.22, +3.17] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -2.60 | [-3.65, -1.55] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +7.61 | [+6.17, +9.05] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +0.30 | [-0.13, +0.74] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +4.95 | [+3.34, +6.56] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -5.99 | [-7.62, -4.36] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -2.09 | [-3.78, -0.40] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +16.09 | [+14.32, +17.86] | better | overall pipeline |

## original_type / centralized / order_1: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +2.97 | [+1.76, +4.17] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -3.33 | [-4.57, -2.08] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +4.35 | [+0.61, +8.09] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +0.54 | [-0.91, +2.00] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +0.86 | [+0.04, +1.68] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -0.92 | [-1.76, -0.09] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -0.88 | [-1.74, -0.03] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.47 | [-1.61, +2.55] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +4.78 | [+3.75, +5.82] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -5.14 | [-6.28, -3.99] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +11.53 | [+8.85, +14.22] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | +1.13 | [-0.01, +2.26] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +3.55 | [+2.58, +4.52] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -3.54 | [-4.52, -2.57] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +12.20 | [+9.08, +15.32] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.86 | [-0.43, +2.16] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +1.13 | [-0.11, +2.38] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -1.69 | [-2.99, -0.39] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -6.62 | [-8.14, -5.09] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +7.81 | [+6.39, +9.22] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +6.52 | [+5.23, +7.80] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -6.87 | [-8.25, -5.49] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +16.55 | [+12.89, +20.21] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +1.41 | [+0.29, +2.52] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +1.99 | [+0.17, +3.82] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -2.61 | [-4.54, -0.68] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -7.50 | [-8.99, -6.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +8.27 | [+5.61, +10.93] | better | overall pipeline |

## original_type / centralized / order_2: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | -0.58 | [-2.22, +1.06] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | +0.73 | [-0.86, +2.32] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +0.17 | [-0.25, +0.58] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -0.92 | [-1.72, -0.12] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +1.68 | [+0.91, +2.45] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -1.95 | [-2.71, -1.19] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -0.73 | [-1.50, +0.03] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.29 | [-2.57, +3.14] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | -0.58 | [-2.22, +1.06] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | +0.73 | [-0.86, +2.32] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +0.17 | [-0.25, +0.58] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.92 | [-1.72, -0.12] | worse | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +9.09 | [+4.86, +13.33] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -8.91 | [-13.29, -4.53] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | +0.48 | [-0.39, +1.36] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +34.00 | [+29.96, +38.03] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | -0.58 | [-2.22, +1.06] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | +0.73 | [-0.86, +2.32] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +0.17 | [-0.25, +0.58] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -0.92 | [-1.72, -0.12] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +10.78 | [+7.02, +14.54] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -10.86 | [-14.81, -6.91] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -0.25 | [-0.50, -0.00] | worse | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +34.28 | [+30.13, +38.44] | better | overall pipeline |

## original_type / centralized / order_3: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +11.16 | [+7.42, +14.90] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -11.47 | [-15.24, -7.69] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +1.77 | [-0.78, +4.31] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | +0.41 | [+0.05, +0.76] | better | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +2.02 | [+0.15, +3.89] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -3.19 | [-5.18, -1.20] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +2.60 | [-2.14, +7.34] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.50 | [-1.41, +2.40] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | -0.10 | [-0.45, +0.26] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -0.60 | [-1.34, +0.14] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | -0.02 | [-0.77, +0.74] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.31 | [-0.89, +0.26] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | -10.51 | [-13.50, -7.51] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +9.81 | [+6.82, +12.79] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +4.35 | [-0.13, +8.83] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.02 | [-0.55, +0.58] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +0.05 | [-1.08, +1.18] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -1.32 | [-2.75, +0.12] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -1.12 | [-3.16, +0.92] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +5.21 | [+3.55, +6.88] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +0.66 | [-1.65, +2.97] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -1.66 | [-3.95, +0.62] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +6.12 | [+1.41, +10.82] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +0.42 | [-0.20, +1.04] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +2.07 | [+0.29, +3.86] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -4.50 | [-6.18, -2.83] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +1.48 | [-2.67, +5.64] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +5.71 | [+4.70, +6.72] | better | overall pipeline |

## original_type / federated / averaged: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +3.32 | [+2.44, +4.19] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -4.60 | [-5.52, -3.67] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +1.97 | [+0.51, +3.42] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -0.87 | [-1.75, +0.01] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +3.09 | [+2.49, +3.69] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -3.92 | [-4.31, -3.52] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -1.71 | [-2.92, -0.49] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | -0.05 | [-1.07, +0.96] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +5.07 | [+3.88, +6.26] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -6.64 | [-7.91, -5.37] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +5.62 | [+3.16, +8.08] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.85 | [-1.60, -0.10] | worse | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +3.65 | [+1.82, +5.49] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -3.94 | [-5.78, -2.10] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +9.68 | [+4.82, +14.54] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.72 | [-0.22, +1.66] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +8.78 | [+6.36, +11.19] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -8.44 | [-10.91, -5.97] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -1.37 | [-5.45, +2.71] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +20.77 | [+18.67, +22.86] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +6.97 | [+5.50, +8.44] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -8.54 | [-10.01, -7.07] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +11.64 | [+6.49, +16.80] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -0.15 | [-0.86, +0.56] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +11.87 | [+9.53, +14.20] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -12.36 | [-14.77, -9.95] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -3.08 | [-7.36, +1.21] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +20.71 | [+18.75, +22.68] | better | overall pipeline |

## original_type / federated / order_1: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.43 | [-0.23, +1.10] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -0.88 | [-1.66, -0.10] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +1.42 | [-0.36, +3.19] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -0.57 | [-2.64, +1.51] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +4.73 | [+3.68, +5.77] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -5.11 | [-6.10, -4.12] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +12.95 | [+11.46, +14.44] | better | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.75 | [-0.26, +1.76] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +2.39 | [+1.15, +3.64] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -3.17 | [-4.39, -1.95] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +5.20 | [+1.12, +9.28] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -1.47 | [-3.38, +0.44] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +5.92 | [+2.56, +9.29] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -6.25 | [-9.58, -2.92] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +15.90 | [+5.45, +26.35] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.87 | [-1.95, +3.68] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +11.00 | [+6.20, +15.80] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -11.43 | [-16.15, -6.72] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -22.07 | [-31.20, -12.93] | worse | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +21.85 | [+16.92, +26.77] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +6.36 | [+3.28, +9.44] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -7.13 | [-10.09, -4.18] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +17.32 | [+7.74, +26.89] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +0.30 | [-1.46, +2.06] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +15.73 | [+11.04, +20.42] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -16.54 | [-21.11, -11.98] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -9.12 | [-18.44, +0.21] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +22.60 | [+17.77, +27.42] | better | overall pipeline |

## original_type / federated / order_2: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +0.48 | [-0.55, +1.51] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -0.61 | [-1.70, +0.48] | not significant | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | -0.22 | [-0.42, -0.01] | worse | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -1.03 | [-2.23, +0.17] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +4.17 | [+2.87, +5.46] | better | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -6.23 | [-6.79, -5.67] | better | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | -19.25 | [-21.48, -17.02] | worse | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | -1.01 | [-2.84, +0.81] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +0.48 | [-0.55, +1.51] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -0.61 | [-1.70, +0.48] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | -0.22 | [-0.42, -0.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -1.03 | [-2.23, +0.17] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +7.46 | [+4.70, +10.23] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -5.35 | [-7.85, -2.85] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | +20.03 | [+17.61, +22.46] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +38.72 | [+36.95, +40.50] | better | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +0.48 | [-0.55, +1.51] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -0.61 | [-1.70, +0.48] | not significant | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | -0.22 | [-0.42, -0.01] | worse | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | -1.03 | [-2.23, +0.17] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +11.63 | [+9.35, +13.91] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -11.58 | [-13.85, -9.31] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | +0.78 | [+0.22, +1.35] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +37.71 | [+35.75, +39.67] | better | overall pipeline |

## original_type / federated / order_3: all comparisons

| Left | Right | Metric | Difference | 95% interval | Outcome | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| tuned_class_balanced_60 | class_balanced_60 | old_task_accuracy | +9.04 | [+7.11, +10.96] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | forgetting | -12.29 | [-14.33, -10.25] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | slowloris_recall | +4.70 | [+0.19, +9.21] | better | overall pipeline |
| tuned_class_balanced_60 | class_balanced_60 | worst_client_macro_recall | -1.02 | [-2.70, +0.66] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | old_task_accuracy | +0.38 | [-0.77, +1.52] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | forgetting | -0.42 | [-1.20, +0.36] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | slowloris_recall | +1.18 | [-2.74, +5.11] | not significant | overall pipeline |
| tuned_protected_60 | protected_60 | worst_client_macro_recall | +0.10 | [-1.28, +1.48] | not significant | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | old_task_accuracy | +12.34 | [+9.92, +14.76] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | forgetting | -16.14 | [-18.54, -13.73] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | slowloris_recall | +11.88 | [+7.68, +16.09] | better | overall pipeline |
| tuned_balanced_rare_60 | balanced_rare_60 | worst_client_macro_recall | -0.06 | [-2.04, +1.92] | not significant | overall pipeline |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | old_task_accuracy | +5.04 | [+1.02, +9.05] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | forgetting | -5.58 | [-9.47, -1.68] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | slowloris_recall | +13.13 | [+5.25, +21.02] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_class_balanced_60 | worst_client_macro_recall | +1.30 | [-1.66, +4.26] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | old_task_accuracy | +7.86 | [+5.44, +10.28] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | forgetting | -8.54 | [-11.20, -5.87] | better | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | slowloris_recall | -2.08 | [-7.61, +3.44] | not significant | matched backbone |
| tuned_balanced_rare_60 | tuned_protected_60 | worst_client_macro_recall | +1.73 | [-0.80, +4.26] | not significant | matched backbone |
| tuned_balanced_rare_60 | class_balanced_60 | old_task_accuracy | +14.07 | [+11.24, +16.91] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | forgetting | -17.87 | [-20.64, -15.09] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | slowloris_recall | +17.83 | [+10.49, +25.17] | better | overall pipeline |
| tuned_balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | +0.28 | [-1.71, +2.27] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | old_task_accuracy | +8.24 | [+5.86, +10.61] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | forgetting | -8.96 | [-11.70, -6.21] | better | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | slowloris_recall | -0.90 | [-7.34, +5.54] | not significant | overall pipeline |
| tuned_balanced_rare_60 | protected_60 | worst_client_macro_recall | +1.83 | [-0.15, +3.81] | not significant | overall pipeline |

## original_type: every order

| Environment | Method | Order | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- | --- | --- |
| centralized | balanced_rare_60 | order_1 | 58.96 ± 1.18 | 16.07 ± 1.18 | 77.12 ± 3.03 | 54.60 ± 1.58 |
| centralized | balanced_rare_60 | order_2 | 41.31 ± 2.46 | 32.06 ± 2.37 | 99.55 ± 0.62 | 55.69 ± 0.75 |
| centralized | balanced_rare_60 | order_3 | 65.31 ± 0.92 | 32.38 ± 1.41 | 92.72 ± 1.99 | 56.78 ± 0.67 |
| centralized | class_balanced_60 | order_1 | 57.22 ± 1.45 | 17.80 ± 1.61 | 72.10 ± 4.24 | 54.33 ± 1.64 |
| centralized | class_balanced_60 | order_2 | 41.31 ± 2.46 | 32.06 ± 2.37 | 99.55 ± 0.62 | 55.69 ± 0.75 |
| centralized | class_balanced_60 | order_3 | 64.55 ± 3.67 | 33.44 ± 3.66 | 86.58 ± 5.19 | 56.05 ± 0.65 |
| centralized | protected_60 | order_1 | 61.75 ± 2.28 | 13.54 ± 2.35 | 96.15 ± 1.59 | 47.46 ± 3.62 |
| centralized | protected_60 | order_2 | 29.95 ± 3.82 | 43.65 ± 4.02 | 99.97 ± 0.11 | 20.48 ± 5.67 |
| centralized | protected_60 | order_3 | 63.14 ± 2.03 | 36.29 ± 2.08 | 91.22 ± 6.25 | 50.76 ± 1.30 |
| centralized | tuned_balanced_rare_60 | order_1 | 63.74 ± 0.79 | 10.93 ± 0.91 | 88.65 ± 1.95 | 55.73 ± 0.99 |
| centralized | tuned_balanced_rare_60 | order_2 | 40.73 ± 2.30 | 32.80 ± 2.41 | 99.72 ± 0.29 | 54.76 ± 1.00 |
| centralized | tuned_balanced_rare_60 | order_3 | 65.21 ± 0.92 | 31.78 ± 1.28 | 92.70 ± 1.68 | 56.47 ± 0.36 |
| centralized | tuned_class_balanced_60 | order_1 | 60.19 ± 1.47 | 14.47 ± 1.48 | 76.45 ± 4.26 | 54.87 ± 1.38 |
| centralized | tuned_class_balanced_60 | order_2 | 40.73 ± 2.30 | 32.80 ± 2.41 | 99.72 ± 0.29 | 54.76 ± 1.00 |
| centralized | tuned_class_balanced_60 | order_3 | 75.72 ± 3.63 | 21.98 ± 3.63 | 88.35 ± 5.11 | 56.46 ± 0.63 |
| centralized | tuned_protected_60 | order_1 | 62.61 ± 1.55 | 12.62 ± 1.60 | 95.27 ± 1.96 | 47.93 ± 2.37 |
| centralized | tuned_protected_60 | order_2 | 31.64 ± 4.59 | 41.71 ± 4.67 | 99.23 ± 1.13 | 20.77 ± 5.67 |
| centralized | tuned_protected_60 | order_3 | 65.16 ± 1.35 | 33.10 ± 1.50 | 93.82 ± 1.43 | 51.26 ± 2.22 |
| federated | balanced_rare_60 | order_1 | 54.18 ± 3.78 | 20.90 ± 3.78 | 63.10 ± 11.96 | 53.56 ± 1.47 |
| federated | balanced_rare_60 | order_2 | 38.80 ± 2.90 | 34.66 ± 2.85 | 100.00 ± 0.00 | 53.49 ± 1.09 |
| federated | balanced_rare_60 | order_3 | 55.75 ± 2.58 | 43.67 ± 2.64 | 71.72 ± 5.90 | 50.19 ± 2.12 |
| federated | class_balanced_60 | order_1 | 50.21 ± 2.76 | 24.87 ± 2.70 | 50.98 ± 8.66 | 51.79 ± 1.81 |
| federated | class_balanced_60 | order_2 | 38.80 ± 2.90 | 34.66 ± 2.85 | 100.00 ± 0.00 | 53.49 ± 1.09 |
| federated | class_balanced_60 | order_3 | 54.01 ± 2.74 | 45.39 ± 2.71 | 65.77 ± 7.40 | 49.85 ± 1.41 |
| federated | protected_60 | order_1 | 40.84 ± 6.03 | 34.28 ± 6.00 | 77.42 ± 2.19 | 29.49 ± 6.72 |
| federated | protected_60 | order_2 | 27.65 ± 1.03 | 45.63 ± 0.96 | 99.00 ± 0.71 | 14.75 ± 2.30 |
| federated | protected_60 | order_3 | 59.85 ± 2.45 | 36.48 ± 3.56 | 84.50 ± 6.66 | 48.30 ± 2.20 |
| federated | tuned_balanced_rare_60 | order_1 | 56.57 ± 3.74 | 17.74 ± 3.63 | 68.30 ± 11.84 | 52.08 ± 2.35 |
| federated | tuned_balanced_rare_60 | order_2 | 39.28 ± 2.90 | 34.05 ± 2.88 | 99.78 ± 0.28 | 52.46 ± 1.93 |
| federated | tuned_balanced_rare_60 | order_3 | 68.09 ± 2.83 | 27.53 ± 2.47 | 83.60 ± 5.20 | 50.13 ± 2.56 |
| federated | tuned_class_balanced_60 | order_1 | 50.65 ± 3.53 | 23.99 ± 3.61 | 52.40 ± 10.68 | 51.22 ± 1.98 |
| federated | tuned_class_balanced_60 | order_2 | 39.28 ± 2.90 | 34.05 ± 2.88 | 99.78 ± 0.28 | 52.46 ± 1.93 |
| federated | tuned_class_balanced_60 | order_3 | 63.05 ± 3.31 | 33.10 ± 3.51 | 70.47 ± 8.61 | 48.83 ± 2.90 |
| federated | tuned_protected_60 | order_1 | 45.57 ± 6.31 | 29.17 ± 6.28 | 90.37 ± 2.27 | 30.24 ± 6.97 |
| federated | tuned_protected_60 | order_2 | 31.82 ± 2.40 | 39.40 ± 1.61 | 79.75 ± 3.31 | 13.74 ± 1.57 |
| federated | tuned_protected_60 | order_3 | 60.23 ± 2.95 | 36.06 ± 3.64 | 85.68 ± 7.25 | 48.40 ± 2.38 |
