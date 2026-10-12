# Supervisor follow-up: completed deliverables

The 7 October requests are complete. New training: **84 calibration-only trials + 420 evaluation runs**. The combined evidence contains **840 evaluated cases**, including the unchanged original 420. No training labels were merged.

## 1. Class-balanced replay at memory 60

| Environment | Method | Old-type accuracy | Forgetting | Rare-type recall | Worst-client macro recall |
|---|---|---:|---:|---:|---:|
| federated | uniform_60 | 35.31 | 47.21 | 67.18 | 29.43 |
| federated | class_balanced_60 | 47.68 | 34.97 | 72.09 | 51.71 |
| federated | protected_60 | 42.78 | 38.80 | 86.48 | 30.85 |
| centralized | uniform_60 | 43.75 | 38.94 | 69.52 | 38.68 |
| centralized | class_balanced_60 | 54.36 | 27.77 | 85.90 | 55.35 |
| centralized | protected_60 | 51.61 | 31.16 | 95.28 | 39.57 |

Protected minus class-balanced, percentage points with paired-seed 95% intervals:
- federated: old accuracy -4.90 [-7.42, -2.38]; rare recall +14.39 [11.86, 16.92].
- centralized: old accuracy -2.75 [-4.80, -0.71]; rare recall +9.38 [7.49, 11.27].

The baseline changes the contribution: protected replay is not the strongest tested method for overall old-type retention at memory 60. It trades some retention and station-wide macro recall for greater rare-type recall relative to class-balanced replay. Do not claim that protected replay dominates all equal-budget alternatives.

## 2. Joint confusion and fit quality

See `outputs/joint_diagnostics/JOINT_CONFUSION_REPORT.md` and both PNG/PDF matrices. Several scan types are repeatedly confused; tiny ICMP classes also have notable errors. Final-model all-type accuracy is 57.21% federated / 59.56% centralized, compared with fitting accuracy 57.61% / 60.11%. Low fitting accuracy demonstrates difficulty under the current model/training setup too; confusion does not prove irreducible label ambiguity. The exact transformed-vector audit finds virtually no cross-type identical vectors.

The near-99% pilot figures apply to selected easier tasks, not all-type joint accuracy. Prespecified task-family reporting is included alongside type results without selecting new merges from evaluation confusion. Family all-sample accuracy from summed probabilities is:
- federated: 89.34% (mapped winning-type family accuracy 88.89%).
- centralized: 90.87% (mapped winning-type family accuracy 85.89%).

## 3. Memory-size sweep

The size is per federated client; centralized budgets are five times this size. These are separate calibration-selected procedures.

| Environment | Memory/client | Uniform old accuracy / rare recall | Balanced old accuracy / rare recall | Protected old accuracy / rare recall |
|---|---:|---|---|---|
| federated | 60 | 35.31 / 67.18 | 47.68 / 72.09 | 42.78 / 86.48 |
| federated | 120 | 48.09 / 80.05 | 50.53 / 78.61 | 49.94 / 88.34 |
| federated | 300 | 60.08 / 86.87 | 53.23 / 88.53 | 61.75 / 95.37 |
| centralized | 60 | 43.75 / 69.52 | 54.36 / 85.90 | 51.61 / 95.28 |
| centralized | 120 | 54.92 / 86.24 | 54.41 / 86.75 | 56.54 / 93.54 |
| centralized | 300 | 62.81 / 94.48 | 52.88 / 84.08 | 63.87 / 97.90 |

| Environment | Capacity | Protected−uniform old accuracy | Protected−balanced old accuracy | Protected−balanced rare recall |
|---|---:|---|---|---|
| federated | 60 | +7.47 [4.37, 10.57] | -4.90 [-7.42, -2.38] | +14.39 [11.86, 16.92] |
| federated | 120 | +1.86 [-0.08, 3.80] | -0.58 [-2.85, 1.69] | +9.72 [7.28, 12.17] |
| federated | 300 | +1.67 [1.19, 2.14] | +8.52 [7.83, 9.21] | +6.84 [4.93, 8.74] |
| centralized | 60 | +7.86 [5.85, 9.87] | -2.75 [-4.80, -0.71] | +9.38 [7.49, 11.27] |
| centralized | 120 | +1.62 [0.07, 3.17] | +2.14 [0.53, 3.74] | +6.79 [5.12, 8.46] |
| centralized | 300 | +1.06 [0.14, 1.97] | +10.99 [9.84, 12.13] | +13.82 [11.29, 16.35] |

Intervals, not only point estimates, determine whether a difference persists at larger memory. Effects can differ across capacities and metrics; memory growth does not automatically establish disappearance or monotonic improvement.

Protected-300 federated old-type accuracy (61.75%) exceeds the original joint reference (55.39%). Joint therefore is an empirical offline reference, not a demonstrated upper bound. Its five all-data rounds and continual training/rehearsal have different optimization and repeated-benign exposures, as recorded in the original protocol. A strictly optimized upper-bound claim would require a separately specified calibration-only training-budget study.

## 4. EWC and A-GEM

| Environment | Method | Old accuracy | Forgetting | Rare recall | Worst-client macro recall |
|---|---|---:|---:|---:|---:|
| federated | ewc | 3.33 | 79.48 | 33.31 | 11.95 |
| federated | agem | 21.43 | 61.34 | 51.43 | 24.37 |
| centralized | ewc | 0.26 | 82.67 | 33.27 | 9.61 |
| centralized | agem | 29.89 | 53.02 | 50.20 | 31.53 |

| Environment | Protected−method | Metric | Paired difference [95% interval] |
|---|---|---|---|
| federated | ewc | old_task_accuracy | +39.45 [37.42, 41.48] |
| federated | ewc | forgetting | -40.68 [-42.89, -38.46] |
| federated | ewc | rare_attack_recall | +53.18 [51.36, 54.99] |
| federated | ewc | worst_client_macro_recall | +18.90 [16.59, 21.21] |
| federated | agem | old_task_accuracy | +21.35 [18.19, 24.50] |
| federated | agem | forgetting | -22.55 [-25.73, -19.36] |
| federated | agem | rare_attack_recall | +35.05 [29.92, 40.18] |
| federated | agem | worst_client_macro_recall | +6.47 [3.91, 9.04] |
| centralized | ewc | old_task_accuracy | +51.35 [50.19, 52.50] |
| centralized | ewc | forgetting | -51.51 [-52.66, -50.36] |
| centralized | ewc | rare_attack_recall | +62.01 [60.55, 63.48] |
| centralized | ewc | worst_client_macro_recall | +29.96 [28.02, 31.89] |
| centralized | agem | old_task_accuracy | +21.73 [19.30, 24.15] |
| centralized | agem | forgetting | -21.86 [-24.28, -19.44] |
| centralized | agem | rare_attack_recall | +45.09 [42.36, 47.82] |
| centralized | agem | worst_client_macro_recall | +8.03 [5.78, 10.29] |

## 5. Attack-order consistency

Every order-specific comparison at every memory is in `paired_intervals.csv` and `FOLLOWUP_RESULTS.md`. The following focuses on the original capacity. Positive old accuracy/recall is favorable; negative forgetting is favorable.

| Environment | Order | Protected−uniform old accuracy | Protected−balanced old accuracy | Protected−uniform rare recall | Protected−balanced rare recall |
|---|---|---|---|---|---|
| federated | order_1 | -2.02 [-7.37, 3.33] | -9.37 [-14.20, -4.55] | -13.72 [-16.58, -10.86] | +25.62 [19.89, 31.35] |
| federated | order_2 | +1.22 [-0.05, 2.49] | -11.15 [-13.45, -8.85] | -1.04 [-1.51, -0.57] | -0.99 [-1.47, -0.51] |
| federated | order_3 | +23.19 [16.81, 29.58] | +5.84 [4.26, 7.42] | +72.68 [52.85, 92.50] | +18.55 [12.74, 24.35] |
| centralized | order_1 | -1.81 [-3.93, 0.31] | +4.52 [2.32, 6.72] | -0.56 [-2.21, 1.08] | +23.57 [19.79, 27.35] |
| centralized | order_2 | -0.17 [-3.28, 2.95] | -11.36 [-14.70, -8.01] | +0.07 [-0.08, 0.22] | +0.50 [0.04, 0.95] |
| centralized | order_3 | +25.55 [20.88, 30.23] | -1.42 [-4.49, 1.65] | +77.80 [64.12, 91.48] | +4.08 [-1.94, 10.10] |

The benefit does not hold uniformly in every order. In particular, federated order 1 rare recall favors uniform over protected at memory 60; order 2 rare recall slightly favors balanced over protected. Report the pooled benefit together with these exceptions.

## 6. Excluded datasets

The OCPP source has 163,570 nominal benign rows, but the two ZIPs are identical and its 69-column message/session schema is not compatible with the 86-field CICEVSE inputs. Independent capture grouping is unverified. The supplied CICEVSE charging/idle files duplicate the existing 14/68 rows exactly. More compatible benign traffic remains unavailable for this experiment. See `docs/research/Excluded_Datasets_Reply_2026_10_12.md` and the audit evidence.

## Checks and limitations

Four new allocator tests plus the original thirteen tests passed. New final models, every checkpoint prediction, source/input fingerprints, persistent roles, feasible quotas, candidate-pool limits, calibration isolation and metric arithmetic are independently checked. Consult the verification JSONs for exact counts. Sixteen benign evaluation flows remain the support; FPR at the benign-starved profile is undefined. Ten seeds quantify training randomness on one fixed split. Paired intervals are unadjusted for multiplicity. No additional datasets, new training-label merges, manuscript or submission were introduced.
