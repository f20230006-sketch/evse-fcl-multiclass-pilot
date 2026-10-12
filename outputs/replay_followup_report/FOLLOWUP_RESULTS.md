# Follow-up replay results

All values are percentages; paired differences are percentage points. Three orders are averaged within each of ten training seeds before pooled intervals. Per-order intervals use ten matched seeds. Intervals describe training randomness on one fixed split, are unadjusted for multiple comparisons, and do not represent independent capture uncertainty.

Memory sizes 60/120/300 mean slots per federated client. Centralized totals are 300/600/1500, matching the five-client system budget. Original 60-slot uniform/protected and other-method evidence is reused exactly, not retrained.

## Type-level summary

| Environment | Method | Old accuracy | Forgetting | Rare recall | Worst-client macro recall |
|---|---|---:|---:|---:|---:|
| centralized | agem | 29.89 | 53.02 | 50.20 | 31.53 |
| centralized | class_balanced_120 | 54.41 | 27.74 | 86.75 | 55.56 |
| centralized | class_balanced_300 | 52.88 | 29.85 | 84.08 | 55.59 |
| centralized | class_balanced_60 | 54.36 | 27.77 | 85.90 | 55.35 |
| centralized | ewc | 0.26 | 82.67 | 33.27 | 9.61 |
| centralized | fedprox_no_replay | 0.21 | 82.53 | 33.29 | 9.82 |
| centralized | joint | 63.51 | N/A | 98.94 | 57.65 |
| centralized | no_replay | 0.00 | 82.82 | 33.28 | 9.67 |
| centralized | protected_120 | 56.54 | 25.75 | 93.54 | 46.80 |
| centralized | protected_300 | 63.87 | 18.42 | 97.90 | 54.92 |
| centralized | protected_60 | 51.61 | 31.16 | 95.28 | 39.57 |
| centralized | uniform_120 | 54.92 | 27.51 | 86.24 | 46.74 |
| centralized | uniform_300 | 62.81 | 19.45 | 94.48 | 54.02 |
| centralized | uniform_60 | 43.75 | 38.94 | 69.52 | 38.68 |
| federated | agem | 21.43 | 61.34 | 51.43 | 24.37 |
| federated | class_balanced_120 | 50.53 | 32.06 | 78.61 | 52.87 |
| federated | class_balanced_300 | 53.23 | 28.40 | 88.53 | 53.87 |
| federated | class_balanced_60 | 47.68 | 34.97 | 72.09 | 51.71 |
| federated | ewc | 3.33 | 79.48 | 33.31 | 11.95 |
| federated | fedprox_no_replay | 0.02 | 82.77 | 33.32 | 9.66 |
| federated | joint | 55.39 | N/A | 76.90 | 52.58 |
| federated | no_replay | 0.00 | 82.76 | 33.33 | 9.70 |
| federated | protected_120 | 49.94 | 31.53 | 88.34 | 37.83 |
| federated | protected_300 | 61.75 | 19.84 | 95.37 | 49.17 |
| federated | protected_60 | 42.78 | 38.80 | 86.48 | 30.85 |
| federated | uniform_120 | 48.09 | 34.43 | 80.05 | 37.96 |
| federated | uniform_300 | 60.08 | 21.53 | 86.87 | 49.06 |
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
| federated protected_120_minus_uniform_120 | averaged | old_task_accuracy | 1.86 | [-0.08, 3.80] |
| federated protected_120_minus_uniform_120 | averaged | forgetting | -2.90 | [-4.94, -0.85] |
| federated protected_120_minus_uniform_120 | averaged | rare_attack_recall | 8.29 | [2.01, 14.56] |
| federated protected_120_minus_uniform_120 | averaged | worst_client_macro_recall | -0.13 | [-2.22, 1.97] |
| federated protected_120_minus_uniform_120 | order_1 | old_task_accuracy | -7.36 | [-11.95, -2.78] |
| federated protected_120_minus_uniform_120 | order_1 | forgetting | 7.38 | [2.77, 11.99] |
| federated protected_120_minus_uniform_120 | order_1 | rare_attack_recall | -14.61 | [-16.09, -13.13] |
| federated protected_120_minus_uniform_120 | order_1 | worst_client_macro_recall | -2.36 | [-7.08, 2.35] |
| federated protected_120_minus_uniform_120 | order_2 | old_task_accuracy | -0.96 | [-6.73, 4.81] |
| federated protected_120_minus_uniform_120 | order_2 | forgetting | 1.07 | [-4.73, 6.87] |
| federated protected_120_minus_uniform_120 | order_2 | rare_attack_recall | -0.76 | [-2.13, 0.61] |
| federated protected_120_minus_uniform_120 | order_2 | worst_client_macro_recall | -0.55 | [-7.18, 6.09] |
| federated protected_120_minus_uniform_120 | order_3 | old_task_accuracy | 13.89 | [7.47, 20.31] |
| federated protected_120_minus_uniform_120 | order_3 | forgetting | -17.13 | [-23.65, -10.62] |
| federated protected_120_minus_uniform_120 | order_3 | rare_attack_recall | 40.23 | [21.33, 59.13] |
| federated protected_120_minus_uniform_120 | order_3 | worst_client_macro_recall | 2.53 | [0.30, 4.77] |
| federated protected_120_minus_class_balanced_120 | averaged | old_task_accuracy | -0.58 | [-2.85, 1.69] |
| federated protected_120_minus_class_balanced_120 | averaged | forgetting | -0.53 | [-2.81, 1.75] |
| federated protected_120_minus_class_balanced_120 | averaged | rare_attack_recall | 9.72 | [7.28, 12.17] |
| federated protected_120_minus_class_balanced_120 | averaged | worst_client_macro_recall | -15.04 | [-17.39, -12.69] |
| federated protected_120_minus_class_balanced_120 | order_1 | old_task_accuracy | -4.89 | [-11.31, 1.54] |
| federated protected_120_minus_class_balanced_120 | order_1 | forgetting | 5.00 | [-1.42, 11.42] |
| federated protected_120_minus_class_balanced_120 | order_1 | rare_attack_recall | 10.48 | [2.93, 18.03] |
| federated protected_120_minus_class_balanced_120 | order_1 | worst_client_macro_recall | -13.02 | [-18.49, -7.55] |
| federated protected_120_minus_class_balanced_120 | order_2 | old_task_accuracy | -3.61 | [-6.92, -0.30] |
| federated protected_120_minus_class_balanced_120 | order_2 | forgetting | 3.66 | [0.38, 6.94] |
| federated protected_120_minus_class_balanced_120 | order_2 | rare_attack_recall | -1.06 | [-2.38, 0.26] |
| federated protected_120_minus_class_balanced_120 | order_2 | worst_client_macro_recall | -30.53 | [-34.29, -26.76] |
| federated protected_120_minus_class_balanced_120 | order_3 | old_task_accuracy | 6.76 | [5.28, 8.23] |
| federated protected_120_minus_class_balanced_120 | order_3 | forgetting | -10.25 | [-11.69, -8.82] |
| federated protected_120_minus_class_balanced_120 | order_3 | rare_attack_recall | 19.75 | [14.79, 24.71] |
| federated protected_120_minus_class_balanced_120 | order_3 | worst_client_macro_recall | -1.57 | [-2.58, -0.57] |
| federated protected_300_minus_uniform_300 | averaged | old_task_accuracy | 1.67 | [1.19, 2.14] |
| federated protected_300_minus_uniform_300 | averaged | forgetting | -1.69 | [-2.04, -1.35] |
| federated protected_300_minus_uniform_300 | averaged | rare_attack_recall | 8.50 | [7.20, 9.80] |
| federated protected_300_minus_uniform_300 | averaged | worst_client_macro_recall | 0.11 | [-0.47, 0.69] |
| federated protected_300_minus_uniform_300 | order_1 | old_task_accuracy | 0.88 | [-0.47, 2.24] |
| federated protected_300_minus_uniform_300 | order_1 | forgetting | -0.90 | [-2.26, 0.45] |
| federated protected_300_minus_uniform_300 | order_1 | rare_attack_recall | 2.61 | [-1.50, 6.72] |
| federated protected_300_minus_uniform_300 | order_1 | worst_client_macro_recall | -0.50 | [-1.78, 0.79] |
| federated protected_300_minus_uniform_300 | order_2 | old_task_accuracy | -3.03 | [-3.60, -2.47] |
| federated protected_300_minus_uniform_300 | order_2 | forgetting | 3.13 | [2.60, 3.65] |
| federated protected_300_minus_uniform_300 | order_2 | rare_attack_recall | 0.53 | [0.05, 1.00] |
| federated protected_300_minus_uniform_300 | order_2 | worst_client_macro_recall | -0.25 | [-1.75, 1.24] |
| federated protected_300_minus_uniform_300 | order_3 | old_task_accuracy | 7.15 | [6.06, 8.24] |
| federated protected_300_minus_uniform_300 | order_3 | forgetting | -7.30 | [-8.17, -6.42] |
| federated protected_300_minus_uniform_300 | order_3 | rare_attack_recall | 22.36 | [19.25, 25.48] |
| federated protected_300_minus_uniform_300 | order_3 | worst_client_macro_recall | 1.08 | [-0.31, 2.47] |
| federated protected_300_minus_class_balanced_300 | averaged | old_task_accuracy | 8.52 | [7.83, 9.21] |
| federated protected_300_minus_class_balanced_300 | averaged | forgetting | -8.56 | [-9.22, -7.90] |
| federated protected_300_minus_class_balanced_300 | averaged | rare_attack_recall | 6.84 | [4.93, 8.74] |
| federated protected_300_minus_class_balanced_300 | averaged | worst_client_macro_recall | -4.70 | [-5.34, -4.06] |
| federated protected_300_minus_class_balanced_300 | order_1 | old_task_accuracy | 4.30 | [3.55, 5.05] |
| federated protected_300_minus_class_balanced_300 | order_1 | forgetting | -4.27 | [-5.05, -3.49] |
| federated protected_300_minus_class_balanced_300 | order_1 | rare_attack_recall | 13.44 | [11.17, 15.70] |
| federated protected_300_minus_class_balanced_300 | order_1 | worst_client_macro_recall | -6.27 | [-7.02, -5.53] |
| federated protected_300_minus_class_balanced_300 | order_2 | old_task_accuracy | 19.85 | [19.28, 20.41] |
| federated protected_300_minus_class_balanced_300 | order_2 | forgetting | -19.86 | [-20.55, -19.17] |
| federated protected_300_minus_class_balanced_300 | order_2 | rare_attack_recall | -0.00 | [-0.08, 0.08] |
| federated protected_300_minus_class_balanced_300 | order_2 | worst_client_macro_recall | -5.50 | [-6.80, -4.20] |
| federated protected_300_minus_class_balanced_300 | order_3 | old_task_accuracy | 1.41 | [-0.82, 3.65] |
| federated protected_300_minus_class_balanced_300 | order_3 | forgetting | -1.55 | [-3.81, 0.72] |
| federated protected_300_minus_class_balanced_300 | order_3 | rare_attack_recall | 7.07 | [1.19, 12.96] |
| federated protected_300_minus_class_balanced_300 | order_3 | worst_client_macro_recall | -2.33 | [-4.09, -0.57] |
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
| centralized protected_120_minus_uniform_120 | averaged | old_task_accuracy | 1.62 | [0.07, 3.17] |
| centralized protected_120_minus_uniform_120 | averaged | forgetting | -1.76 | [-3.29, -0.23] |
| centralized protected_120_minus_uniform_120 | averaged | rare_attack_recall | 7.30 | [5.11, 9.49] |
| centralized protected_120_minus_uniform_120 | averaged | worst_client_macro_recall | 0.06 | [-1.85, 1.96] |
| centralized protected_120_minus_uniform_120 | order_1 | old_task_accuracy | -3.43 | [-4.95, -1.91] |
| centralized protected_120_minus_uniform_120 | order_1 | forgetting | 3.43 | [1.90, 4.96] |
| centralized protected_120_minus_uniform_120 | order_1 | rare_attack_recall | -10.08 | [-14.64, -5.52] |
| centralized protected_120_minus_uniform_120 | order_1 | worst_client_macro_recall | 0.07 | [-1.53, 1.67] |
| centralized protected_120_minus_uniform_120 | order_2 | old_task_accuracy | -2.02 | [-6.69, 2.65] |
| centralized protected_120_minus_uniform_120 | order_2 | forgetting | 1.84 | [-2.92, 6.60] |
| centralized protected_120_minus_uniform_120 | order_2 | rare_attack_recall | -0.33 | [-0.76, 0.09] |
| centralized protected_120_minus_uniform_120 | order_2 | worst_client_macro_recall | -2.06 | [-7.05, 2.92] |
| centralized protected_120_minus_uniform_120 | order_3 | old_task_accuracy | 10.31 | [8.98, 11.65] |
| centralized protected_120_minus_uniform_120 | order_3 | forgetting | -10.56 | [-12.05, -9.06] |
| centralized protected_120_minus_uniform_120 | order_3 | rare_attack_recall | 32.31 | [28.13, 36.50] |
| centralized protected_120_minus_uniform_120 | order_3 | worst_client_macro_recall | 2.16 | [0.52, 3.80] |
| centralized protected_120_minus_class_balanced_120 | averaged | old_task_accuracy | 2.14 | [0.53, 3.74] |
| centralized protected_120_minus_class_balanced_120 | averaged | forgetting | -1.99 | [-3.64, -0.34] |
| centralized protected_120_minus_class_balanced_120 | averaged | rare_attack_recall | 6.79 | [5.12, 8.46] |
| centralized protected_120_minus_class_balanced_120 | averaged | worst_client_macro_recall | -8.76 | [-10.07, -7.45] |
| centralized protected_120_minus_class_balanced_120 | order_1 | old_task_accuracy | 5.66 | [3.81, 7.50] |
| centralized protected_120_minus_class_balanced_120 | order_1 | forgetting | -5.64 | [-7.49, -3.78] |
| centralized protected_120_minus_class_balanced_120 | order_1 | rare_attack_recall | 17.70 | [12.09, 23.32] |
| centralized protected_120_minus_class_balanced_120 | order_1 | worst_client_macro_recall | -2.92 | [-5.02, -0.82] |
| centralized protected_120_minus_class_balanced_120 | order_2 | old_task_accuracy | 2.04 | [-1.47, 5.54] |
| centralized protected_120_minus_class_balanced_120 | order_2 | forgetting | -2.14 | [-5.81, 1.53] |
| centralized protected_120_minus_class_balanced_120 | order_2 | rare_attack_recall | -0.25 | [-0.68, 0.18] |
| centralized protected_120_minus_class_balanced_120 | order_2 | worst_client_macro_recall | -19.51 | [-22.56, -16.47] |
| centralized protected_120_minus_class_balanced_120 | order_3 | old_task_accuracy | -1.29 | [-4.08, 1.51] |
| centralized protected_120_minus_class_balanced_120 | order_3 | forgetting | 1.80 | [-1.46, 5.06] |
| centralized protected_120_minus_class_balanced_120 | order_3 | rare_attack_recall | 2.91 | [-1.52, 7.34] |
| centralized protected_120_minus_class_balanced_120 | order_3 | worst_client_macro_recall | -3.86 | [-5.53, -2.19] |
| centralized protected_300_minus_uniform_300 | averaged | old_task_accuracy | 1.06 | [0.14, 1.97] |
| centralized protected_300_minus_uniform_300 | averaged | forgetting | -1.02 | [-2.03, -0.02] |
| centralized protected_300_minus_uniform_300 | averaged | rare_attack_recall | 3.41 | [1.09, 5.73] |
| centralized protected_300_minus_uniform_300 | averaged | worst_client_macro_recall | 0.90 | [-0.10, 1.89] |
| centralized protected_300_minus_uniform_300 | order_1 | old_task_accuracy | 0.57 | [-0.37, 1.52] |
| centralized protected_300_minus_uniform_300 | order_1 | forgetting | -0.56 | [-1.46, 0.34] |
| centralized protected_300_minus_uniform_300 | order_1 | rare_attack_recall | 1.80 | [-0.90, 4.50] |
| centralized protected_300_minus_uniform_300 | order_1 | worst_client_macro_recall | 0.56 | [-1.51, 2.63] |
| centralized protected_300_minus_uniform_300 | order_2 | old_task_accuracy | 0.01 | [-0.55, 0.57] |
| centralized protected_300_minus_uniform_300 | order_2 | forgetting | -0.01 | [-0.56, 0.54] |
| centralized protected_300_minus_uniform_300 | order_2 | rare_attack_recall | 0.18 | [-0.22, 0.58] |
| centralized protected_300_minus_uniform_300 | order_2 | worst_client_macro_recall | 1.15 | [-1.14, 3.45] |
| centralized protected_300_minus_uniform_300 | order_3 | old_task_accuracy | 2.59 | [0.47, 4.71] |
| centralized protected_300_minus_uniform_300 | order_3 | forgetting | -2.50 | [-4.93, -0.08] |
| centralized protected_300_minus_uniform_300 | order_3 | rare_attack_recall | 8.25 | [2.35, 14.14] |
| centralized protected_300_minus_uniform_300 | order_3 | worst_client_macro_recall | 0.97 | [-1.09, 3.04] |
| centralized protected_300_minus_class_balanced_300 | averaged | old_task_accuracy | 10.99 | [9.84, 12.13] |
| centralized protected_300_minus_class_balanced_300 | averaged | forgetting | -11.42 | [-12.52, -10.32] |
| centralized protected_300_minus_class_balanced_300 | averaged | rare_attack_recall | 13.82 | [11.29, 16.35] |
| centralized protected_300_minus_class_balanced_300 | averaged | worst_client_macro_recall | -0.68 | [-1.53, 0.17] |
| centralized protected_300_minus_class_balanced_300 | order_1 | old_task_accuracy | 9.46 | [6.78, 12.13] |
| centralized protected_300_minus_class_balanced_300 | order_1 | forgetting | -9.33 | [-12.02, -6.65] |
| centralized protected_300_minus_class_balanced_300 | order_1 | rare_attack_recall | 28.88 | [20.94, 36.81] |
| centralized protected_300_minus_class_balanced_300 | order_1 | worst_client_macro_recall | 0.46 | [-1.93, 2.85] |
| centralized protected_300_minus_class_balanced_300 | order_2 | old_task_accuracy | 19.16 | [15.12, 23.21] |
| centralized protected_300_minus_class_balanced_300 | order_2 | forgetting | -19.25 | [-23.20, -15.30] |
| centralized protected_300_minus_class_balanced_300 | order_2 | rare_attack_recall | -0.08 | [-0.26, 0.10] |
| centralized protected_300_minus_class_balanced_300 | order_2 | worst_client_macro_recall | -0.65 | [-1.02, -0.28] |
| centralized protected_300_minus_class_balanced_300 | order_3 | old_task_accuracy | 4.33 | [1.87, 6.80] |
| centralized protected_300_minus_class_balanced_300 | order_3 | forgetting | -5.69 | [-8.12, -3.26] |
| centralized protected_300_minus_class_balanced_300 | order_3 | rare_attack_recall | 12.66 | [5.15, 20.17] |
| centralized protected_300_minus_class_balanced_300 | order_3 | worst_client_macro_recall | -1.84 | [-3.60, -0.09] |
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
| centralized | class_balanced_120 | 59.43 | 85.01 | 69.28 |
| centralized | class_balanced_300 | 58.13 | 80.78 | 69.27 |
| centralized | class_balanced_60 | 60.40 | 84.40 | 68.26 |
| centralized | ewc | 1.00 | 33.28 | 25.78 |
| centralized | fedprox_no_replay | 0.11 | 33.29 | 25.09 |
| centralized | joint | 76.81 | 96.61 | 72.55 |
| centralized | no_replay | 2.96 | 33.28 | 27.13 |
| centralized | protected_120 | 58.99 | 93.31 | 69.44 |
| centralized | protected_300 | 64.15 | 97.85 | 72.60 |
| centralized | protected_60 | 50.66 | 90.10 | 62.75 |
| centralized | uniform_120 | 55.96 | 84.93 | 66.48 |
| centralized | uniform_300 | 61.46 | 89.81 | 71.13 |
| centralized | uniform_60 | 44.68 | 69.22 | 58.00 |
| federated | agem | 22.53 | 50.67 | 42.74 |
| federated | class_balanced_120 | 57.55 | 78.59 | 66.43 |
| federated | class_balanced_300 | 58.21 | 83.90 | 67.20 |
| federated | class_balanced_60 | 54.67 | 72.14 | 64.15 |
| federated | ewc | 3.19 | 33.33 | 27.28 |
| federated | fedprox_no_replay | 0.01 | 33.32 | 25.01 |
| federated | joint | 72.43 | 76.60 | 67.23 |
| federated | no_replay | 1.53 | 33.33 | 26.22 |
| federated | protected_120 | 50.65 | 85.18 | 63.49 |
| federated | protected_300 | 61.80 | 94.78 | 69.93 |
| federated | protected_60 | 43.29 | 83.25 | 58.24 |
| federated | uniform_120 | 49.51 | 77.64 | 61.65 |
| federated | uniform_300 | 59.86 | 85.88 | 68.84 |
| federated | uniform_60 | 37.77 | 66.88 | 53.33 |

Mapping the winning type preserves the original prediction decision, whereas summing probabilities can change it; the two conventions need not have the same old-task accuracy. The `mapped_*` CSV columns provide the alternative explicitly.

| Environment | Method | Mapped family old accuracy | Mapped family rare recall | Mapped family worst-client macro recall |
|---|---|---:|---:|---:|
| centralized | agem | 32.65 | 50.35 | 50.52 |
| centralized | class_balanced_120 | 60.27 | 87.23 | 69.35 |
| centralized | class_balanced_300 | 58.58 | 84.26 | 69.38 |
| centralized | class_balanced_60 | 61.25 | 86.46 | 68.29 |
| centralized | ewc | 0.41 | 33.28 | 25.30 |
| centralized | fedprox_no_replay | 0.21 | 33.29 | 25.16 |
| centralized | joint | 77.81 | 99.11 | 73.73 |
| centralized | no_replay | 0.00 | 33.28 | 25.00 |
| centralized | protected_120 | 58.90 | 93.67 | 69.31 |
| centralized | protected_300 | 64.17 | 97.94 | 72.53 |
| centralized | protected_60 | 52.39 | 95.42 | 63.56 |
| centralized | uniform_120 | 56.44 | 86.32 | 66.75 |
| centralized | uniform_300 | 63.08 | 94.53 | 71.88 |
| centralized | uniform_60 | 44.87 | 69.64 | 58.04 |
| federated | agem | 22.14 | 51.56 | 42.43 |
| federated | class_balanced_120 | 56.85 | 79.12 | 66.25 |
| federated | class_balanced_300 | 58.68 | 88.75 | 67.17 |
| federated | class_balanced_60 | 53.75 | 72.80 | 63.88 |
| federated | ewc | 3.74 | 33.33 | 27.71 |
| federated | fedprox_no_replay | 0.02 | 33.32 | 25.01 |
| federated | joint | 72.42 | 77.17 | 67.74 |
| federated | no_replay | 0.00 | 33.33 | 25.00 |
| federated | protected_120 | 51.58 | 88.53 | 63.81 |
| federated | protected_300 | 62.08 | 95.57 | 69.94 |
| federated | protected_60 | 44.42 | 86.74 | 58.79 |
| federated | uniform_120 | 50.10 | 80.28 | 61.96 |
| federated | uniform_300 | 60.38 | 87.06 | 69.13 |
| federated | uniform_60 | 37.86 | 67.36 | 53.35 |

## Qualification
Use the signed intervals and per-order tables to assess whether protected replay exceeds class-balanced replay and whether its advantage persists with memory. Neither positive point estimates alone nor pooled results establish a benefit in every order. The original benign evaluation support remains 16; benign-starved FPR is undefined. Joint confusion and excluded-dataset reports are separate deliverables.
