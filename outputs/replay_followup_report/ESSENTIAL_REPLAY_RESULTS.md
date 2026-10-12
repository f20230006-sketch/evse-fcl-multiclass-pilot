# Follow-up replay results

All values are percentages; paired differences are percentage points. Three orders are averaged within each of ten training seeds before pooled intervals. Per-order intervals use ten matched seeds. Intervals describe training randomness on one fixed split, are unadjusted for multiple comparisons, and do not represent independent capture uncertainty.

Memory sizes 60/120/300 mean slots per federated client. Centralized totals are 300/600/1500, matching the five-client system budget. Original 60-slot uniform/protected and other-method evidence is reused exactly, not retrained.

## Type-level summary

| Environment | Method | Old accuracy | Forgetting | Rare recall | Worst-client macro recall |
|---|---|---:|---:|---:|---:|
| centralized | agem | 29.89 | 53.02 | 50.20 | 31.53 |
| centralized | class_balanced_60 | 54.36 | 27.77 | 85.90 | 55.35 |
| centralized | ewc | 0.26 | 82.67 | 33.27 | 9.61 |
| centralized | fedprox_no_replay | 0.21 | 82.53 | 33.29 | 9.82 |
| centralized | joint | 63.51 | N/A | 98.94 | 57.65 |
| centralized | no_replay | 0.00 | 82.82 | 33.28 | 9.67 |
| centralized | protected_60 | 51.61 | 31.16 | 95.28 | 39.57 |
| centralized | uniform_60 | 43.75 | 38.94 | 69.52 | 38.68 |
| federated | agem | 21.43 | 61.34 | 51.43 | 24.37 |
| federated | class_balanced_60 | 47.68 | 34.97 | 72.09 | 51.71 |
| federated | ewc | 3.33 | 79.48 | 33.31 | 11.95 |
| federated | fedprox_no_replay | 0.02 | 82.77 | 33.32 | 9.66 |
| federated | joint | 55.39 | N/A | 76.90 | 52.58 |
| federated | no_replay | 0.00 | 82.76 | 33.33 | 9.70 |
| federated | protected_60 | 42.78 | 38.80 | 86.48 | 30.85 |
| federated | uniform_60 | 35.31 | 47.21 | 67.18 | 29.43 |

## Paired comparisons, including each attack order

Difference = protected minus comparison. Higher old accuracy/recall is favorable; lower forgetting is favorable.

| Environment/method contrast | Order | Metric | Difference | 95% interval |
|---|---|---|---:|---|
| federated protected_60_minus_uniform_60 | averaged | old_task_accuracy | 7.47 | [4.37, 10.57] |
| federated protected_60_minus_uniform_60 | averaged | forgetting | -8.41 | [-11.57, -5.25] |
| federated protected_60_minus_uniform_60 | averaged | rare_attack_recall | 19.31 | [12.50, 26.11] |
| federated protected_60_minus_uniform_60 | averaged | worst_client_macro_recall | 1.42 | [-0.68, 3.52] |
| federated protected_60_minus_uniform_60 | order_1 | old_task_accuracy | -2.02 | [-7.37, 3.33] |
| federated protected_60_minus_uniform_60 | order_1 | forgetting | 2.01 | [-3.35, 7.38] |
| federated protected_60_minus_uniform_60 | order_1 | rare_attack_recall | -13.72 | [-16.58, -10.86] |
| federated protected_60_minus_uniform_60 | order_1 | worst_client_macro_recall | 0.98 | [-4.59, 6.55] |
| federated protected_60_minus_uniform_60 | order_2 | old_task_accuracy | 1.22 | [-0.05, 2.49] |
| federated protected_60_minus_uniform_60 | order_2 | forgetting | -1.28 | [-2.47, -0.10] |
| federated protected_60_minus_uniform_60 | order_2 | rare_attack_recall | -1.04 | [-1.51, -0.57] |
| federated protected_60_minus_uniform_60 | order_2 | worst_client_macro_recall | -0.89 | [-3.55, 1.76] |
| federated protected_60_minus_uniform_60 | order_3 | old_task_accuracy | 23.19 | [16.81, 29.58] |
| federated protected_60_minus_uniform_60 | order_3 | forgetting | -25.96 | [-32.70, -19.23] |
| federated protected_60_minus_uniform_60 | order_3 | rare_attack_recall | 72.68 | [52.85, 92.50] |
| federated protected_60_minus_uniform_60 | order_3 | worst_client_macro_recall | 4.17 | [2.31, 6.03] |
| federated protected_60_minus_class_balanced_60 | averaged | old_task_accuracy | -4.90 | [-7.42, -2.38] |
| federated protected_60_minus_class_balanced_60 | averaged | forgetting | 3.82 | [1.22, 6.43] |
| federated protected_60_minus_class_balanced_60 | averaged | rare_attack_recall | 14.39 | [11.86, 16.92] |
| federated protected_60_minus_class_balanced_60 | averaged | worst_client_macro_recall | -20.86 | [-22.54, -19.19] |
| federated protected_60_minus_class_balanced_60 | order_1 | old_task_accuracy | -9.37 | [-14.20, -4.55] |
| federated protected_60_minus_class_balanced_60 | order_1 | forgetting | 9.41 | [4.59, 14.23] |
| federated protected_60_minus_class_balanced_60 | order_1 | rare_attack_recall | 25.62 | [19.89, 31.35] |
| federated protected_60_minus_class_balanced_60 | order_1 | worst_client_macro_recall | -22.30 | [-27.21, -17.39] |
| federated protected_60_minus_class_balanced_60 | order_2 | old_task_accuracy | -11.15 | [-13.45, -8.85] |
| federated protected_60_minus_class_balanced_60 | order_2 | forgetting | 10.97 | [8.71, 13.22] |
| federated protected_60_minus_class_balanced_60 | order_2 | rare_attack_recall | -0.99 | [-1.47, -0.51] |
| federated protected_60_minus_class_balanced_60 | order_2 | worst_client_macro_recall | -38.74 | [-40.36, -37.12] |
| federated protected_60_minus_class_balanced_60 | order_3 | old_task_accuracy | 5.84 | [4.26, 7.42] |
| federated protected_60_minus_class_balanced_60 | order_3 | forgetting | -8.91 | [-11.27, -6.55] |
| federated protected_60_minus_class_balanced_60 | order_3 | rare_attack_recall | 18.55 | [12.74, 24.35] |
| federated protected_60_minus_class_balanced_60 | order_3 | worst_client_macro_recall | -1.55 | [-3.41, 0.31] |
| federated protected_60_minus_ewc | averaged | old_task_accuracy | 39.45 | [37.42, 41.48] |
| federated protected_60_minus_ewc | averaged | forgetting | -40.68 | [-42.89, -38.46] |
| federated protected_60_minus_ewc | averaged | rare_attack_recall | 53.18 | [51.36, 54.99] |
| federated protected_60_minus_ewc | averaged | worst_client_macro_recall | 18.90 | [16.59, 21.21] |
| federated protected_60_minus_agem | averaged | old_task_accuracy | 21.35 | [18.19, 24.50] |
| federated protected_60_minus_agem | averaged | forgetting | -22.55 | [-25.73, -19.36] |
| federated protected_60_minus_agem | averaged | rare_attack_recall | 35.05 | [29.92, 40.18] |
| federated protected_60_minus_agem | averaged | worst_client_macro_recall | 6.47 | [3.91, 9.04] |
| centralized protected_60_minus_uniform_60 | averaged | old_task_accuracy | 7.86 | [5.85, 9.87] |
| centralized protected_60_minus_uniform_60 | averaged | forgetting | -7.78 | [-9.78, -5.78] |
| centralized protected_60_minus_uniform_60 | averaged | rare_attack_recall | 25.77 | [21.17, 30.37] |
| centralized protected_60_minus_uniform_60 | averaged | worst_client_macro_recall | 0.89 | [-0.68, 2.45] |
| centralized protected_60_minus_uniform_60 | order_1 | old_task_accuracy | -1.81 | [-3.93, 0.31] |
| centralized protected_60_minus_uniform_60 | order_1 | forgetting | 1.79 | [-0.37, 3.95] |
| centralized protected_60_minus_uniform_60 | order_1 | rare_attack_recall | -0.56 | [-2.21, 1.08] |
| centralized protected_60_minus_uniform_60 | order_1 | worst_client_macro_recall | -1.87 | [-3.94, 0.20] |
| centralized protected_60_minus_uniform_60 | order_2 | old_task_accuracy | -0.17 | [-3.28, 2.95] |
| centralized protected_60_minus_uniform_60 | order_2 | forgetting | 0.23 | [-2.94, 3.40] |
| centralized protected_60_minus_uniform_60 | order_2 | rare_attack_recall | 0.07 | [-0.08, 0.22] |
| centralized protected_60_minus_uniform_60 | order_2 | worst_client_macro_recall | -0.91 | [-5.40, 3.58] |
| centralized protected_60_minus_uniform_60 | order_3 | old_task_accuracy | 25.55 | [20.88, 30.23] |
| centralized protected_60_minus_uniform_60 | order_3 | forgetting | -25.36 | [-30.02, -20.71] |
| centralized protected_60_minus_uniform_60 | order_3 | rare_attack_recall | 77.80 | [64.12, 91.48] |
| centralized protected_60_minus_uniform_60 | order_3 | worst_client_macro_recall | 5.44 | [4.14, 6.73] |
| centralized protected_60_minus_class_balanced_60 | averaged | old_task_accuracy | -2.75 | [-4.80, -0.71] |
| centralized protected_60_minus_class_balanced_60 | averaged | forgetting | 3.39 | [1.27, 5.51] |
| centralized protected_60_minus_class_balanced_60 | averaged | rare_attack_recall | 9.38 | [7.49, 11.27] |
| centralized protected_60_minus_class_balanced_60 | averaged | worst_client_macro_recall | -15.79 | [-17.53, -14.04] |
| centralized protected_60_minus_class_balanced_60 | order_1 | old_task_accuracy | 4.52 | [2.32, 6.72] |
| centralized protected_60_minus_class_balanced_60 | order_1 | forgetting | -4.26 | [-6.62, -1.89] |
| centralized protected_60_minus_class_balanced_60 | order_1 | rare_attack_recall | 23.57 | [19.79, 27.35] |
| centralized protected_60_minus_class_balanced_60 | order_1 | worst_client_macro_recall | -6.87 | [-9.72, -4.02] |
| centralized protected_60_minus_class_balanced_60 | order_2 | old_task_accuracy | -11.36 | [-14.70, -8.01] |
| centralized protected_60_minus_class_balanced_60 | order_2 | forgetting | 11.59 | [8.12, 15.06] |
| centralized protected_60_minus_class_balanced_60 | order_2 | rare_attack_recall | 0.50 | [0.04, 0.95] |
| centralized protected_60_minus_class_balanced_60 | order_2 | worst_client_macro_recall | -35.20 | [-39.57, -30.84] |
| centralized protected_60_minus_class_balanced_60 | order_3 | old_task_accuracy | -1.42 | [-4.49, 1.65] |
| centralized protected_60_minus_class_balanced_60 | order_3 | forgetting | 2.84 | [-0.24, 5.93] |
| centralized protected_60_minus_class_balanced_60 | order_3 | rare_attack_recall | 4.08 | [-1.94, 10.10] |
| centralized protected_60_minus_class_balanced_60 | order_3 | worst_client_macro_recall | -5.29 | [-6.44, -4.13] |
| centralized protected_60_minus_ewc | averaged | old_task_accuracy | 51.35 | [50.19, 52.50] |
| centralized protected_60_minus_ewc | averaged | forgetting | -51.51 | [-52.66, -50.36] |
| centralized protected_60_minus_ewc | averaged | rare_attack_recall | 62.01 | [60.55, 63.48] |
| centralized protected_60_minus_ewc | averaged | worst_client_macro_recall | 29.96 | [28.02, 31.89] |
| centralized protected_60_minus_agem | averaged | old_task_accuracy | 21.73 | [19.30, 24.15] |
| centralized protected_60_minus_agem | averaged | forgetting | -21.86 | [-24.28, -19.44] |
| centralized protected_60_minus_agem | averaged | rare_attack_recall | 45.09 | [42.36, 47.82] |
| centralized protected_60_minus_agem | averaged | worst_client_macro_recall | 8.03 | [5.78, 10.29] |

## Prespecified family-level scoring

The four original task groups plus benign are the reporting families. Class probabilities are summed within each family before argmax. This re-scores the existing type-trained models, does not retrain merged labels, and does not use confusion matrices to choose group membership. The additional mapped-type-prediction accuracy uses the family of the highest-probability type instead; both conventions are supplied. These task-defined groups should not be confused with a newly validated semantic taxonomy. Family correctness is an easier outcome than exact attack-type correctness.

| Environment | Method | Family old accuracy | Family rare recall | Family worst-client macro recall |
|---|---|---:|---:|---:|
| centralized | agem | 33.73 | 49.34 | 51.30 |
| centralized | class_balanced_60 | 60.40 | 84.40 | 68.26 |
| centralized | ewc | 1.00 | 33.28 | 25.78 |
| centralized | fedprox_no_replay | 0.11 | 33.29 | 25.09 |
| centralized | joint | 76.81 | 96.61 | 72.55 |
| centralized | no_replay | 2.96 | 33.28 | 27.13 |
| centralized | protected_60 | 50.66 | 90.10 | 62.75 |
| centralized | uniform_60 | 44.68 | 69.22 | 58.00 |
| federated | agem | 22.53 | 50.67 | 42.74 |
| federated | class_balanced_60 | 54.67 | 72.14 | 64.15 |
| federated | ewc | 3.19 | 33.33 | 27.28 |
| federated | fedprox_no_replay | 0.01 | 33.32 | 25.01 |
| federated | joint | 72.43 | 76.60 | 67.23 |
| federated | no_replay | 1.53 | 33.33 | 26.22 |
| federated | protected_60 | 43.29 | 83.25 | 58.24 |
| federated | uniform_60 | 37.77 | 66.88 | 53.33 |

## Qualification
Use the signed intervals and per-order tables to assess whether protected replay exceeds class-balanced replay and whether its advantage persists with memory. Neither positive point estimates alone nor pooled results establish a benefit in every order. The original benign evaluation support remains 16; benign-starved FPR is undefined. Joint confusion and excluded-dataset reports are separate deliverables.
