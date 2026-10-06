# Full multiclass comparison results

Completed evaluation runs: **420/420**. Original CICEVSE data only; supplied additional datasets excluded.

Results are percentages except where stated. Means average the three orders within each training seed, then average ten seeds. Seeds vary training randomness on one fixed split.

| Environment | Method | Old-task accuracy | Forgetting | Rare recall | FPR | Worst-client macro recall | Macro AUROC | Macro AP |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| centralized | agem | 29.89 | 53.02 | 50.20 | 0.00 | 31.53 | 70.83 | 38.35 |
| centralized | ewc | 0.26 | 82.67 | 33.27 | 0.00 | 9.61 | 61.41 | 22.14 |
| centralized | fedprox_no_replay | 0.21 | 82.53 | 33.29 | 0.00 | 9.82 | 65.26 | 32.15 |
| centralized | joint | 63.51 | N/A | 98.94 | 1.46 | 57.65 | 91.44 | 63.38 |
| centralized | no_replay | 0.00 | 82.82 | 33.28 | 0.00 | 9.67 | 58.70 | 20.24 |
| centralized | protected_60 | 51.61 | 31.16 | 95.28 | 0.42 | 39.57 | 78.04 | 44.18 |
| centralized | uniform_60 | 43.75 | 38.94 | 69.52 | 0.62 | 38.68 | 78.50 | 43.68 |
| federated | agem | 21.43 | 61.34 | 51.43 | 3.33 | 24.37 | 70.72 | 35.54 |
| federated | ewc | 3.33 | 79.48 | 33.31 | 6.46 | 11.95 | 66.48 | 28.03 |
| federated | fedprox_no_replay | 0.02 | 82.77 | 33.32 | 1.25 | 9.66 | 62.41 | 25.58 |
| federated | joint | 55.39 | N/A | 76.90 | 4.17 | 52.58 | 90.36 | 60.22 |
| federated | no_replay | 0.00 | 82.76 | 33.33 | 5.83 | 9.70 | 57.28 | 19.63 |
| federated | protected_60 | 42.78 | 38.80 | 86.48 | 1.67 | 30.85 | 76.00 | 40.20 |
| federated | uniform_60 | 35.31 | 47.21 | 67.18 | 4.58 | 29.43 | 76.49 | 38.74 |

## Does protected replay beat uniform replay?

Paired differences below are percentage points. Negative forgetting/FPR differences favor protection; positive accuracy/recall differences favor protection.

| Contrast | Metric | Mean difference | 95% paired-seed interval |
|---|---|---:|---|
| federated protected_minus_uniform | old_task_accuracy | 7.47 | [4.37, 10.57] |
| centralized protected_minus_uniform | old_task_accuracy | 7.86 | [5.85, 9.87] |
| federated_minus_centralized_replay_improvement | old_task_accuracy | -0.39 | [-4.28, 3.50] |
| federated protected_minus_uniform | forgetting | -8.41 | [-11.57, -5.25] |
| centralized protected_minus_uniform | forgetting | -7.78 | [-9.78, -5.78] |
| federated_minus_centralized_replay_improvement | forgetting | -0.63 | [-4.53, 3.27] |
| federated protected_minus_uniform | rare_attack_recall | 19.31 | [12.50, 26.11] |
| centralized protected_minus_uniform | rare_attack_recall | 25.77 | [21.17, 30.37] |
| federated_minus_centralized_replay_improvement | rare_attack_recall | -6.46 | [-13.31, 0.39] |
| federated protected_minus_uniform | false_alarm_rate | -2.92 | [-5.16, -0.67] |
| centralized protected_minus_uniform | false_alarm_rate | -0.21 | [-0.68, 0.26] |
| federated_minus_centralized_replay_improvement | false_alarm_rate | -2.71 | [-4.94, -0.48] |
| federated protected_minus_uniform | worst_client_macro_recall | 1.42 | [-0.68, 3.52] |
| centralized protected_minus_uniform | worst_client_macro_recall | 0.89 | [-0.68, 2.45] |
| federated_minus_centralized_replay_improvement | worst_client_macro_recall | 0.53 | [-1.48, 2.55] |

## Every station

Full metrics and uncertainty for each profile are in per_client_summary_metrics.csv; each seed/order result is in per_client_per_run_metrics.csv. Per-class recall, support, AUROC and AP are in per_class_metrics.csv. These include the benign-starved client even when its FPR is undefined.

## Training and tuning

MLP 64/32, ReLU, Adam, five local epochs per round, five rounds per task, no gradient clipping. Calibration-only grids and exact selection scores are in hyperparameter_trials.csv/JSON. Replay/EWC/A-GEM/FedProx learning rate was not independently tuned; 0.003 was fixed from the prior calibration pilot. Joint and no-replay learning rates were screened. See the full protocol for Fisher sampling, projection, rehearsal mixing, and memory accounting.

## Interpretation limits

Proceeding despite imbalance was explicitly authorized. The test set still contains 16 genuine benign examples, so FPR is coarse and undefined at the benign-starved profile. Reported results do not satisfy the request for hundreds of benign test examples. Three orders are paired repeated conditions, not 30 independent datasets. A-GEM uses Adam and task-boundary uniform memory, an explicitly disclosed adaptation. Joint is an empirical offline reference and is not guaranteed to outperform every continual method. Macro AP uses average precision rather than trapezoidal PR AUC.

Compare protected and uniform under the same budget, and inspect the federated-centralized difference in their improvements before claiming a federation-specific effect. Hyperparameters were selected separately per environment/order, so that difference also reflects separately calibrated procedures. The expected benign-starved/rare-station story must be supported by actual station metrics, not assumed.

The code, configs, split manifests, calibration evidence, and selected final/checkpoint predictions are intended for the existing private GitHub repository. Historical pilot results are preserved.
