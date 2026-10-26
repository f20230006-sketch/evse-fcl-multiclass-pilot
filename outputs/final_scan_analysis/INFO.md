# Final analysis information

Read SUMMARY.pdf first (two pages). This file and the CSVs provide the detailed reference. No email drafts or implementation files are included in the results archives.

## Scan-only Random Forest check

Pooled fitting rows from the six scan types only. The original fitting/calibration/evaluation roles and three frozen first-task representations were retained. Two prespecified forest settings were screened on calibration data at seed 42, then the selected setting was run with seeds 42–51 for each representation: 6 calibration fits and 30 evaluation fits. These are diagnostic classifiers, not new continual-learning runs. No calibration rows were added to fitting.

Accuracy / balanced accuracy: 34.25% ± 0.14%; six-class chance 16.67%; fitting accuracy 100%. Above-chance difference: +17.59 [17.49, 17.69]; significant points. The six classes each have 600 evaluation examples. These fixed-split seed intervals do not establish cross-capture generalization. This result does not support the condition that all six types are near chance, so merging is not justified as proven intrinsic indistinguishability. The original MLP loss plateau alone does not establish an irreducible error floor.

| Scan type | RF recall (%) |
|---|---|
| Aggressive_Scan | 43.61 |
| OS_Fingerprinting | 36.14 |
| SYN_Stealth_Scan | 33.39 |
| Service_Version_Detection | 32.92 |
| TCP_Port_Scan | 24.67 |
| Vulnerability_Scan | 34.79 |

## Exact merged scoring definition

Only Aggressive_Scan, OS_Fingerprinting, SYN_Stealth_Scan, Service_Version_Detection, TCP_Port_Scan and Vulnerability_Scan map to Scan. Slowloris_Scan stays separate. Six probabilities are summed before argmax; the resulting output space has 10 labels. No training labels, weights or stored replay examples changed. The class-balanced memories were originally balanced over 15 types, not the 10 merged labels. Scan spans the original reconnaissance and vulnerability cohorts; retention/forgetting use those original cohorts rather than pretending a new independent merged task sequence was trained.

Raw re-scores are in merged_predictions/. Every checkpoint stores indices, merged truth and predicted labels. The final checkpoint also stores full merged probabilities. Original source probability arrays are referenced and hashed in saved_prediction_input_hashes.json; they remain in the earlier evidence archive rather than being duplicated here.

## All merged main results

| Environment | Method | Old accuracy | Forgetting | Rare recall | Worst-client score |
|---|---|---|---|---|---|
| centralized | agem | 57.87 ± 3.96 | 41.98 ± 3.97 | 49.83 ± 2.15 | 49.19 ± 2.98 |
| centralized | class_balanced_120 | 89.50 ± 1.39 | 10.17 ± 1.44 | 83.65 ± 4.01 | 86.23 ± 0.44 |
| centralized | class_balanced_300 | 88.75 ± 1.38 | 11.01 ± 1.38 | 80.30 ± 3.42 | 85.91 ± 0.51 |
| centralized | class_balanced_60 | 90.03 ± 0.87 | 9.43 ± 1.02 | 83.21 ± 2.86 | 84.88 ± 0.97 |
| centralized | ewc | 22.32 ± 0.19 | 77.51 ± 0.19 | 33.27 ± 0.02 | 14.59 ± 1.25 |
| centralized | fedprox_no_replay | 22.35 ± 0.27 | 77.44 ± 0.28 | 33.29 ± 0.02 | 14.98 ± 0.34 |
| centralized | joint | 97.96 ± 0.69 | N/A | 95.10 ± 3.80 | 88.00 ± 0.31 |
| centralized | no_replay | 22.22 ± 0.01 | 77.64 ± 0.02 | 33.28 ± 0.00 | 14.81 ± 0.00 |
| centralized | protected_120 | 87.39 ± 1.50 | 12.05 ± 1.50 | 92.24 ± 2.26 | 71.58 ± 2.42 |
| centralized | protected_300 | 95.06 ± 0.69 | 4.28 ± 0.67 | 95.39 ± 3.53 | 83.51 ± 1.28 |
| centralized | protected_60 | 80.48 ± 1.62 | 19.28 ± 1.64 | 89.92 ± 1.78 | 60.27 ± 3.91 |
| centralized | uniform_120 | 85.02 ± 2.40 | 14.79 ± 2.41 | 84.83 ± 2.72 | 71.20 ± 2.91 |
| centralized | uniform_300 | 92.77 ± 1.17 | 7.03 ± 1.21 | 87.19 ± 3.20 | 81.82 ± 1.65 |
| centralized | uniform_60 | 74.42 ± 2.04 | 25.40 ± 2.04 | 69.07 ± 6.03 | 59.65 ± 1.64 |
| federated | agem | 46.03 ± 4.58 | 53.80 ± 4.58 | 50.12 ± 4.65 | 37.12 ± 3.29 |
| federated | class_balanced_120 | 88.24 ± 1.26 | 11.49 ± 1.28 | 77.92 ± 3.68 | 80.29 ± 1.62 |
| federated | class_balanced_300 | 88.26 ± 0.76 | 11.43 ± 0.77 | 83.20 ± 1.03 | 81.48 ± 1.29 |
| federated | class_balanced_60 | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.41 ± 4.15 | 77.97 ± 1.05 |
| federated | ewc | 24.89 ± 1.30 | 74.95 ± 1.30 | 33.31 ± 0.03 | 17.15 ± 3.56 |
| federated | fedprox_no_replay | 22.24 ± 0.05 | 77.59 ± 0.05 | 33.32 ± 0.03 | 14.80 ± 0.16 |
| federated | joint | 94.20 ± 0.07 | N/A | 76.25 ± 0.21 | 77.89 ± 1.48 |
| federated | no_replay | 22.22 ± 0.00 | 77.60 ± 0.02 | 33.33 ± 0.00 | 14.81 ± 0.00 |
| federated | protected_120 | 80.09 ± 2.93 | 19.55 ± 2.98 | 84.30 ± 2.47 | 58.15 ± 4.34 |
| federated | protected_300 | 91.24 ± 0.52 | 8.15 ± 0.64 | 93.95 ± 1.97 | 75.72 ± 1.43 |
| federated | protected_60 | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.28 ± 2.36 | 47.15 ± 3.82 |
| federated | uniform_120 | 78.08 ± 2.05 | 21.72 ± 2.06 | 76.80 ± 7.37 | 58.27 ± 3.25 |
| federated | uniform_300 | 90.85 ± 0.77 | 8.91 ± 0.77 | 82.72 ± 3.89 | 75.20 ± 1.08 |
| federated | uniform_60 | 65.29 ± 2.92 | 34.53 ± 2.93 | 66.70 ± 6.94 | 45.50 ± 2.86 |

## Key comparisons at every memory and order

| Environment | Order | Protected method | Comparison | Metric | Difference [95% interval]; result |
|---|---|---|---|---|---|
| federated | averaged | protected_60 | uniform_60 | old_task_accuracy | +7.55 [4.88, 10.22]; significant |
| federated | averaged | protected_60 | uniform_60 | forgetting | -7.69 [-10.39, -4.99]; significant |
| federated | averaged | protected_60 | uniform_60 | rare_attack_recall | +15.58 [10.34, 20.81]; significant |
| federated | averaged | protected_60 | uniform_60 | worst_client_macro_recall | +1.65 [-1.19, 4.49]; not significant |
| federated | order_1 | protected_60 | uniform_60 | old_task_accuracy | -0.16 [-5.75, 5.44]; not significant |
| federated | order_1 | protected_60 | uniform_60 | forgetting | +0.16 [-5.46, 5.77]; not significant |
| federated | order_1 | protected_60 | uniform_60 | rare_attack_recall | -13.72 [-16.58, -10.86]; significant |
| federated | order_1 | protected_60 | uniform_60 | worst_client_macro_recall | +2.03 [-6.76, 10.81]; not significant |
| federated | order_2 | protected_60 | uniform_60 | old_task_accuracy | +3.09 [1.70, 4.48]; significant |
| federated | order_2 | protected_60 | uniform_60 | forgetting | -3.09 [-4.48, -1.70]; significant |
| federated | order_2 | protected_60 | uniform_60 | rare_attack_recall | -3.17 [-6.35, 0.01]; not significant |
| federated | order_2 | protected_60 | uniform_60 | worst_client_macro_recall | -2.04 [-7.08, 3.01]; not significant |
| federated | order_3 | protected_60 | uniform_60 | old_task_accuracy | +19.72 [14.74, 24.71]; significant |
| federated | order_3 | protected_60 | uniform_60 | forgetting | -20.14 [-25.25, -15.03]; significant |
| federated | order_3 | protected_60 | uniform_60 | rare_attack_recall | +63.62 [47.60, 79.64]; significant |
| federated | order_3 | protected_60 | uniform_60 | worst_client_macro_recall | +4.96 [3.47, 6.45]; significant |
| federated | averaged | protected_60 | class_balanced_60 | old_task_accuracy | -11.15 [-13.31, -8.99]; significant |
| federated | averaged | protected_60 | class_balanced_60 | forgetting | +11.06 [8.88, 13.24]; significant |
| federated | averaged | protected_60 | class_balanced_60 | rare_attack_recall | +10.87 [8.78, 12.95]; significant |
| federated | averaged | protected_60 | class_balanced_60 | worst_client_macro_recall | -30.81 [-33.37, -28.26]; significant |
| federated | order_1 | protected_60 | class_balanced_60 | old_task_accuracy | -9.90 [-14.76, -5.04]; significant |
| federated | order_1 | protected_60 | class_balanced_60 | forgetting | +9.96 [5.10, 14.82]; significant |
| federated | order_1 | protected_60 | class_balanced_60 | rare_attack_recall | +25.64 [19.89, 31.38]; significant |
| federated | order_1 | protected_60 | class_balanced_60 | worst_client_macro_recall | -31.96 [-39.46, -24.47]; significant |
| federated | order_2 | protected_60 | class_balanced_60 | old_task_accuracy | -26.27 [-27.85, -24.69]; significant |
| federated | order_2 | protected_60 | class_balanced_60 | forgetting | +26.27 [24.69, 27.85]; significant |
| federated | order_2 | protected_60 | class_balanced_60 | rare_attack_recall | -2.99 [-6.18, 0.20]; not significant |
| federated | order_2 | protected_60 | class_balanced_60 | worst_client_macro_recall | -58.66 [-61.86, -55.46]; significant |
| federated | order_3 | protected_60 | class_balanced_60 | old_task_accuracy | +2.72 [0.77, 4.67]; significant |
| federated | order_3 | protected_60 | class_balanced_60 | forgetting | -3.04 [-5.11, -0.97]; significant |
| federated | order_3 | protected_60 | class_balanced_60 | rare_attack_recall | +9.95 [3.89, 16.01]; significant |
| federated | order_3 | protected_60 | class_balanced_60 | worst_client_macro_recall | -1.81 [-3.61, -0.02]; significant |
| federated | averaged | protected_120 | uniform_120 | old_task_accuracy | +2.01 [0.33, 3.68]; significant |
| federated | averaged | protected_120 | uniform_120 | forgetting | -2.16 [-3.83, -0.49]; significant |
| federated | averaged | protected_120 | uniform_120 | rare_attack_recall | +7.50 [2.50, 12.51]; significant |
| federated | averaged | protected_120 | uniform_120 | worst_client_macro_recall | -0.12 [-3.86, 3.63]; not significant |
| federated | order_1 | protected_120 | uniform_120 | old_task_accuracy | -5.48 [-10.02, -0.93]; significant |
| federated | order_1 | protected_120 | uniform_120 | forgetting | +5.49 [0.93, 10.06]; significant |
| federated | order_1 | protected_120 | uniform_120 | rare_attack_recall | -14.61 [-16.09, -13.13]; significant |
| federated | order_1 | protected_120 | uniform_120 | worst_client_macro_recall | -3.69 [-11.22, 3.84]; not significant |
| federated | order_2 | protected_120 | uniform_120 | old_task_accuracy | -0.78 [-6.32, 4.76]; not significant |
| federated | order_2 | protected_120 | uniform_120 | forgetting | +0.78 [-4.76, 6.32]; not significant |
| federated | order_2 | protected_120 | uniform_120 | rare_attack_recall | -0.96 [-5.86, 3.94]; not significant |
| federated | order_2 | protected_120 | uniform_120 | worst_client_macro_recall | -0.90 [-11.47, 9.66]; not significant |
| federated | order_3 | protected_120 | uniform_120 | old_task_accuracy | +12.27 [7.35, 17.18]; significant |
| federated | order_3 | protected_120 | uniform_120 | forgetting | -12.76 [-17.63, -7.88]; significant |
| federated | order_3 | protected_120 | uniform_120 | rare_attack_recall | +38.08 [23.27, 52.89]; significant |
| federated | order_3 | protected_120 | uniform_120 | worst_client_macro_recall | +4.24 [2.30, 6.19]; significant |
| federated | averaged | protected_120 | class_balanced_120 | old_task_accuracy | -8.15 [-10.73, -5.57]; significant |
| federated | averaged | protected_120 | class_balanced_120 | forgetting | +8.07 [5.44, 10.70]; significant |
| federated | averaged | protected_120 | class_balanced_120 | rare_attack_recall | +6.39 [3.08, 9.69]; significant |
| federated | averaged | protected_120 | class_balanced_120 | worst_client_macro_recall | -22.14 [-25.98, -18.31]; significant |
| federated | order_1 | protected_120 | class_balanced_120 | old_task_accuracy | -5.61 [-12.01, 0.79]; not significant |
| federated | order_1 | protected_120 | class_balanced_120 | forgetting | +5.82 [-0.62, 12.26]; not significant |
| federated | order_1 | protected_120 | class_balanced_120 | rare_attack_recall | +10.60 [3.08, 18.11]; significant |
| federated | order_1 | protected_120 | class_balanced_120 | worst_client_macro_recall | -19.03 [-28.15, -9.90]; significant |
| federated | order_2 | protected_120 | class_balanced_120 | old_task_accuracy | -21.84 [-24.61, -19.07]; significant |
| federated | order_2 | protected_120 | class_balanced_120 | forgetting | +21.84 [19.07, 24.61]; significant |
| federated | order_2 | protected_120 | class_balanced_120 | rare_attack_recall | -2.35 [-5.62, 0.92]; not significant |
| federated | order_2 | protected_120 | class_balanced_120 | worst_client_macro_recall | -46.72 [-53.16, -40.29]; significant |
| federated | order_3 | protected_120 | class_balanced_120 | old_task_accuracy | +3.00 [1.08, 4.93]; significant |
| federated | order_3 | protected_120 | class_balanced_120 | forgetting | -3.46 [-5.61, -1.32]; significant |
| federated | order_3 | protected_120 | class_balanced_120 | rare_attack_recall | +10.91 [4.37, 17.44]; significant |
| federated | order_3 | protected_120 | class_balanced_120 | worst_client_macro_recall | -0.68 [-1.57, 0.21]; not significant |
| federated | averaged | protected_300 | uniform_300 | old_task_accuracy | +0.39 [-0.03, 0.80]; not significant |
| federated | averaged | protected_300 | uniform_300 | forgetting | -0.76 [-1.19, -0.34]; significant |
| federated | averaged | protected_300 | uniform_300 | rare_attack_recall | +11.23 [8.16, 14.31]; significant |
| federated | averaged | protected_300 | uniform_300 | worst_client_macro_recall | +0.52 [-0.13, 1.17]; not significant |
| federated | order_1 | protected_300 | uniform_300 | old_task_accuracy | +1.13 [-0.03, 2.29]; not significant |
| federated | order_1 | protected_300 | uniform_300 | forgetting | -1.15 [-2.31, 0.01]; not significant |
| federated | order_1 | protected_300 | uniform_300 | rare_attack_recall | +3.90 [-0.29, 8.09]; not significant |
| federated | order_1 | protected_300 | uniform_300 | worst_client_macro_recall | -0.95 [-2.51, 0.61]; not significant |
| federated | order_2 | protected_300 | uniform_300 | old_task_accuracy | -6.22 [-7.39, -5.04]; significant |
| federated | order_2 | protected_300 | uniform_300 | forgetting | +6.22 [5.04, 7.39]; significant |
| federated | order_2 | protected_300 | uniform_300 | rare_attack_recall | +7.72 [0.42, 15.02]; significant |
| federated | order_2 | protected_300 | uniform_300 | worst_client_macro_recall | +0.21 [-2.29, 2.70]; not significant |
| federated | order_3 | protected_300 | uniform_300 | old_task_accuracy | +6.26 [5.04, 7.47]; significant |
| federated | order_3 | protected_300 | uniform_300 | forgetting | -7.36 [-8.83, -5.90]; significant |
| federated | order_3 | protected_300 | uniform_300 | rare_attack_recall | +22.08 [17.74, 26.43]; significant |
| federated | order_3 | protected_300 | uniform_300 | worst_client_macro_recall | +2.30 [1.11, 3.49]; significant |
| federated | averaged | protected_300 | class_balanced_300 | old_task_accuracy | +2.98 [2.30, 3.66]; significant |
| federated | averaged | protected_300 | class_balanced_300 | forgetting | -3.28 [-4.04, -2.53]; significant |
| federated | averaged | protected_300 | class_balanced_300 | rare_attack_recall | +10.75 [9.08, 12.43]; significant |
| federated | averaged | protected_300 | class_balanced_300 | worst_client_macro_recall | -5.77 [-6.64, -4.89]; significant |
| federated | order_1 | protected_300 | class_balanced_300 | old_task_accuracy | +2.03 [1.37, 2.69]; significant |
| federated | order_1 | protected_300 | class_balanced_300 | forgetting | -1.90 [-2.56, -1.24]; significant |
| federated | order_1 | protected_300 | class_balanced_300 | rare_attack_recall | +13.02 [10.80, 15.25]; significant |
| federated | order_1 | protected_300 | class_balanced_300 | worst_client_macro_recall | -8.87 [-10.94, -6.79]; significant |
| federated | order_2 | protected_300 | class_balanced_300 | old_task_accuracy | +1.63 [0.21, 3.05]; significant |
| federated | order_2 | protected_300 | class_balanced_300 | forgetting | -1.63 [-3.05, -0.21]; significant |
| federated | order_2 | protected_300 | class_balanced_300 | rare_attack_recall | -0.00 [-0.08, 0.08]; not significant |
| federated | order_2 | protected_300 | class_balanced_300 | worst_client_macro_recall | -7.90 [-9.90, -5.91]; significant |
| federated | order_3 | protected_300 | class_balanced_300 | old_task_accuracy | +5.28 [3.90, 6.66]; significant |
| federated | order_3 | protected_300 | class_balanced_300 | forgetting | -6.33 [-8.01, -4.65]; significant |
| federated | order_3 | protected_300 | class_balanced_300 | rare_attack_recall | +19.24 [14.22, 24.26]; significant |
| federated | order_3 | protected_300 | class_balanced_300 | worst_client_macro_recall | -0.53 [-2.12, 1.07]; not significant |
| centralized | averaged | protected_60 | uniform_60 | old_task_accuracy | +6.07 [4.18, 7.95]; significant |
| centralized | averaged | protected_60 | uniform_60 | forgetting | -6.12 [-8.01, -4.24]; significant |
| centralized | averaged | protected_60 | uniform_60 | rare_attack_recall | +20.85 [16.85, 24.86]; significant |
| centralized | averaged | protected_60 | uniform_60 | worst_client_macro_recall | +0.62 [-2.13, 3.38]; not significant |
| centralized | order_1 | protected_60 | uniform_60 | old_task_accuracy | -1.96 [-4.17, 0.26]; not significant |
| centralized | order_1 | protected_60 | uniform_60 | forgetting | +1.94 [-0.31, 4.19]; not significant |
| centralized | order_1 | protected_60 | uniform_60 | rare_attack_recall | -0.56 [-2.21, 1.08]; not significant |
| centralized | order_1 | protected_60 | uniform_60 | worst_client_macro_recall | -2.93 [-6.33, 0.47]; not significant |
| centralized | order_2 | protected_60 | uniform_60 | old_task_accuracy | -0.54 [-3.48, 2.40]; not significant |
| centralized | order_2 | protected_60 | uniform_60 | forgetting | +0.54 [-2.40, 3.48]; not significant |
| centralized | order_2 | protected_60 | uniform_60 | rare_attack_recall | +0.10 [-0.06, 0.26]; not significant |
| centralized | order_2 | protected_60 | uniform_60 | worst_client_macro_recall | -2.08 [-9.42, 5.26]; not significant |
| centralized | order_3 | protected_60 | uniform_60 | old_task_accuracy | +20.69 [16.66, 24.73]; significant |
| centralized | order_3 | protected_60 | uniform_60 | forgetting | -20.86 [-24.84, -16.87]; significant |
| centralized | order_3 | protected_60 | uniform_60 | rare_attack_recall | +63.02 [51.33, 74.72]; significant |
| centralized | order_3 | protected_60 | uniform_60 | worst_client_macro_recall | +6.88 [4.92, 8.84]; significant |
| centralized | averaged | protected_60 | class_balanced_60 | old_task_accuracy | -9.54 [-11.13, -7.95]; significant |
| centralized | averaged | protected_60 | class_balanced_60 | forgetting | +9.85 [8.15, 11.55]; significant |
| centralized | averaged | protected_60 | class_balanced_60 | rare_attack_recall | +6.72 [3.84, 9.59]; significant |
| centralized | averaged | protected_60 | class_balanced_60 | worst_client_macro_recall | -24.61 [-27.24, -21.98]; significant |
| centralized | order_1 | protected_60 | class_balanced_60 | old_task_accuracy | +3.77 [1.78, 5.77]; significant |
| centralized | order_1 | protected_60 | class_balanced_60 | forgetting | -3.43 [-5.58, -1.28]; significant |
| centralized | order_1 | protected_60 | class_balanced_60 | rare_attack_recall | +24.51 [20.84, 28.19]; significant |
| centralized | order_1 | protected_60 | class_balanced_60 | worst_client_macro_recall | -10.85 [-14.71, -6.99]; significant |
| centralized | order_2 | protected_60 | class_balanced_60 | old_task_accuracy | -31.54 [-34.66, -28.43]; significant |
| centralized | order_2 | protected_60 | class_balanced_60 | forgetting | +31.54 [28.43, 34.66]; significant |
| centralized | order_2 | protected_60 | class_balanced_60 | rare_attack_recall | +0.60 [0.10, 1.09]; significant |
| centralized | order_2 | protected_60 | class_balanced_60 | worst_client_macro_recall | -53.22 [-60.13, -46.32]; significant |
| centralized | order_3 | protected_60 | class_balanced_60 | old_task_accuracy | -0.86 [-2.84, 1.12]; not significant |
| centralized | order_3 | protected_60 | class_balanced_60 | forgetting | +1.44 [-0.90, 3.78]; not significant |
| centralized | order_3 | protected_60 | class_balanced_60 | rare_attack_recall | -4.96 [-12.34, 2.42]; not significant |
| centralized | order_3 | protected_60 | class_balanced_60 | worst_client_macro_recall | -9.75 [-11.14, -8.36]; significant |
| centralized | averaged | protected_120 | uniform_120 | old_task_accuracy | +2.37 [0.51, 4.24]; significant |
| centralized | averaged | protected_120 | uniform_120 | forgetting | -2.74 [-4.56, -0.92]; significant |
| centralized | averaged | protected_120 | uniform_120 | rare_attack_recall | +7.42 [5.13, 9.71]; significant |
| centralized | averaged | protected_120 | uniform_120 | worst_client_macro_recall | +0.38 [-2.58, 3.33]; not significant |
| centralized | order_1 | protected_120 | uniform_120 | old_task_accuracy | -2.90 [-4.21, -1.60]; significant |
| centralized | order_1 | protected_120 | uniform_120 | forgetting | +2.89 [1.56, 4.23]; significant |
| centralized | order_1 | protected_120 | uniform_120 | rare_attack_recall | -10.18 [-14.66, -5.70]; significant |
| centralized | order_1 | protected_120 | uniform_120 | worst_client_macro_recall | +0.31 [-1.24, 1.86]; not significant |
| centralized | order_2 | protected_120 | uniform_120 | old_task_accuracy | -0.38 [-5.22, 4.47]; not significant |
| centralized | order_2 | protected_120 | uniform_120 | forgetting | +0.38 [-4.47, 5.22]; not significant |
| centralized | order_2 | protected_120 | uniform_120 | rare_attack_recall | -2.40 [-4.88, 0.09]; not significant |
| centralized | order_2 | protected_120 | uniform_120 | worst_client_macro_recall | -2.50 [-10.37, 5.37]; not significant |
| centralized | order_3 | protected_120 | uniform_120 | old_task_accuracy | +10.40 [8.67, 12.14]; significant |
| centralized | order_3 | protected_120 | uniform_120 | forgetting | -11.49 [-13.11, -9.87]; significant |
| centralized | order_3 | protected_120 | uniform_120 | rare_attack_recall | +34.83 [30.05, 39.60]; significant |
| centralized | order_3 | protected_120 | uniform_120 | worst_client_macro_recall | +3.32 [1.07, 5.58]; significant |
| centralized | averaged | protected_120 | class_balanced_120 | old_task_accuracy | -2.11 [-3.43, -0.79]; significant |
| centralized | averaged | protected_120 | class_balanced_120 | forgetting | +1.88 [0.58, 3.18]; significant |
| centralized | averaged | protected_120 | class_balanced_120 | rare_attack_recall | +8.60 [6.35, 10.84]; significant |
| centralized | averaged | protected_120 | class_balanced_120 | worst_client_macro_recall | -14.65 [-16.45, -12.85]; significant |
| centralized | order_1 | protected_120 | class_balanced_120 | old_task_accuracy | +4.87 [3.28, 6.45]; significant |
| centralized | order_1 | protected_120 | class_balanced_120 | forgetting | -4.85 [-6.46, -3.24]; significant |
| centralized | order_1 | protected_120 | class_balanced_120 | rare_attack_recall | +18.51 [13.75, 23.28]; significant |
| centralized | order_1 | protected_120 | class_balanced_120 | worst_client_macro_recall | -6.38 [-8.91, -3.86]; significant |
| centralized | order_2 | protected_120 | class_balanced_120 | old_task_accuracy | -13.60 [-16.65, -10.56]; significant |
| centralized | order_2 | protected_120 | class_balanced_120 | forgetting | +13.60 [10.55, 16.64]; significant |
| centralized | order_2 | protected_120 | class_balanced_120 | rare_attack_recall | -2.31 [-4.81, 0.19]; not significant |
| centralized | order_2 | protected_120 | class_balanced_120 | worst_client_macro_recall | -29.75 [-34.31, -25.19]; significant |
| centralized | order_3 | protected_120 | class_balanced_120 | old_task_accuracy | +2.40 [0.90, 3.91]; significant |
| centralized | order_3 | protected_120 | class_balanced_120 | forgetting | -3.10 [-4.71, -1.49]; significant |
| centralized | order_3 | protected_120 | class_balanced_120 | rare_attack_recall | +9.59 [4.80, 14.37]; significant |
| centralized | order_3 | protected_120 | class_balanced_120 | worst_client_macro_recall | -7.82 [-9.94, -5.70]; significant |
| centralized | averaged | protected_300 | uniform_300 | old_task_accuracy | +2.29 [1.62, 2.96]; significant |
| centralized | averaged | protected_300 | uniform_300 | forgetting | -2.75 [-3.43, -2.07]; significant |
| centralized | averaged | protected_300 | uniform_300 | rare_attack_recall | +8.20 [5.07, 11.33]; significant |
| centralized | averaged | protected_300 | uniform_300 | worst_client_macro_recall | +1.69 [0.47, 2.91]; significant |
| centralized | order_1 | protected_300 | uniform_300 | old_task_accuracy | +0.46 [-0.46, 1.37]; not significant |
| centralized | order_1 | protected_300 | uniform_300 | forgetting | -0.47 [-1.40, 0.47]; not significant |
| centralized | order_1 | protected_300 | uniform_300 | rare_attack_recall | +2.20 [-0.64, 5.03]; not significant |
| centralized | order_1 | protected_300 | uniform_300 | worst_client_macro_recall | +0.82 [-2.55, 4.18]; not significant |
| centralized | order_2 | protected_300 | uniform_300 | old_task_accuracy | +0.28 [-0.74, 1.30]; not significant |
| centralized | order_2 | protected_300 | uniform_300 | forgetting | -0.28 [-1.30, 0.74]; not significant |
| centralized | order_2 | protected_300 | uniform_300 | rare_attack_recall | -0.17 [-8.96, 8.63]; not significant |
| centralized | order_2 | protected_300 | uniform_300 | worst_client_macro_recall | +1.67 [-1.77, 5.11]; not significant |
| centralized | order_3 | protected_300 | uniform_300 | old_task_accuracy | +6.14 [4.65, 7.62]; significant |
| centralized | order_3 | protected_300 | uniform_300 | forgetting | -7.51 [-9.05, -5.96]; significant |
| centralized | order_3 | protected_300 | uniform_300 | rare_attack_recall | +22.56 [17.97, 27.15]; significant |
| centralized | order_3 | protected_300 | uniform_300 | worst_client_macro_recall | +2.58 [-0.63, 5.79]; not significant |
| centralized | averaged | protected_300 | class_balanced_300 | old_task_accuracy | +6.31 [5.01, 7.61]; significant |
| centralized | averaged | protected_300 | class_balanced_300 | forgetting | -6.72 [-8.02, -5.42]; significant |
| centralized | averaged | protected_300 | class_balanced_300 | rare_attack_recall | +15.09 [12.34, 17.84]; significant |
| centralized | averaged | protected_300 | class_balanced_300 | worst_client_macro_recall | -2.40 [-3.58, -1.22]; significant |
| centralized | order_1 | protected_300 | class_balanced_300 | old_task_accuracy | +8.32 [5.59, 11.05]; significant |
| centralized | order_1 | protected_300 | class_balanced_300 | forgetting | -8.23 [-10.96, -5.51]; significant |
| centralized | order_1 | protected_300 | class_balanced_300 | rare_attack_recall | +29.24 [21.55, 36.93]; significant |
| centralized | order_1 | protected_300 | class_balanced_300 | worst_client_macro_recall | -0.59 [-4.55, 3.37]; not significant |
| centralized | order_2 | protected_300 | class_balanced_300 | old_task_accuracy | +4.20 [2.48, 5.93]; significant |
| centralized | order_2 | protected_300 | class_balanced_300 | forgetting | -4.22 [-5.95, -2.49]; significant |
| centralized | order_2 | protected_300 | class_balanced_300 | rare_attack_recall | -7.16 [-14.36, 0.04]; not significant |
| centralized | order_2 | protected_300 | class_balanced_300 | worst_client_macro_recall | -2.48 [-3.40, -1.56]; significant |
| centralized | order_3 | protected_300 | class_balanced_300 | old_task_accuracy | +6.40 [5.49, 7.31]; significant |
| centralized | order_3 | protected_300 | class_balanced_300 | forgetting | -7.72 [-8.61, -6.82]; significant |
| centralized | order_3 | protected_300 | class_balanced_300 | rare_attack_recall | +23.19 [20.71, 25.67]; significant |
| centralized | order_3 | protected_300 | class_balanced_300 | worst_client_macro_recall | -4.13 [-6.38, -1.87]; significant |

## What federation adds

The experimental question is how local fitting and per-client bounded memories under heterogeneous client profiles affect retention and rare-type recall compared with pooled training at the same system memory budget. A replay benefit that appears equally in both settings is not a federation-specific contribution. The clear observed joint-model rare-type deficits locate a federated robustness problem, but do not by themselves show that protection uniquely solves it. These comparisons include the separately calibrated procedures; they do not isolate a pure causal effect of averaging alone.

Signed deficit is centralized recall minus federated recall. A positive interaction means protection reduces that signed deficit more than its comparison method.

| Score space | Class | Method | Centralized−federated recall [95% interval] |
|---|---|---|---|
| original_type | Slowloris_Scan | joint | +21.73 [21.45, 22.00]; significant |
| original_type | Slowloris_Scan | uniform_60 | +2.34 [-3.38, 8.06]; not significant |
| original_type | Slowloris_Scan | class_balanced_60 | +13.83 [11.31, 16.35]; significant |
| original_type | Slowloris_Scan | protected_60 | +8.81 [6.84, 10.77]; significant |
| original_type | Slowloris_Scan | uniform_120 | +6.20 [-0.65, 13.05]; not significant |
| original_type | Slowloris_Scan | class_balanced_120 | +8.08 [4.10, 12.07]; significant |
| original_type | Slowloris_Scan | protected_120 | +5.17 [2.40, 7.93]; significant |
| original_type | Slowloris_Scan | uniform_300 | +7.56 [5.29, 9.83]; significant |
| original_type | Slowloris_Scan | class_balanced_300 | -4.59 [-7.22, -1.96]; significant |
| original_type | Slowloris_Scan | protected_300 | +2.39 [1.44, 3.34]; significant |
| original_type | ICMP_Fragmentation | joint | +58.67 [49.18, 68.15]; significant |
| original_type | ICMP_Fragmentation | uniform_60 | +2.00 [-7.01, 11.01]; not significant |
| original_type | ICMP_Fragmentation | class_balanced_60 | +11.33 [2.61, 20.05]; significant |
| original_type | ICMP_Fragmentation | protected_60 | +8.00 [-0.65, 16.65]; not significant |
| original_type | ICMP_Fragmentation | uniform_120 | +4.67 [-2.10, 11.43]; not significant |
| original_type | ICMP_Fragmentation | class_balanced_120 | +14.67 [10.28, 19.05]; significant |
| original_type | ICMP_Fragmentation | protected_120 | +9.33 [1.48, 17.19]; significant |
| original_type | ICMP_Fragmentation | uniform_300 | +14.67 [7.28, 22.05]; significant |
| original_type | ICMP_Fragmentation | class_balanced_300 | +12.67 [6.53, 18.80]; significant |
| original_type | ICMP_Fragmentation | protected_300 | +19.33 [13.20, 25.47]; significant |
| merged_scans | Slowloris_Scan | joint | +18.52 [15.73, 21.30]; significant |
| merged_scans | Slowloris_Scan | uniform_60 | +2.37 [-3.04, 7.78]; not significant |
| merged_scans | Slowloris_Scan | class_balanced_60 | +11.80 [8.44, 15.16]; significant |
| merged_scans | Slowloris_Scan | protected_60 | +7.64 [6.06, 9.23]; significant |
| merged_scans | Slowloris_Scan | uniform_120 | +8.06 [2.66, 13.45]; significant |
| merged_scans | Slowloris_Scan | class_balanced_120 | +5.66 [1.09, 10.22]; significant |
| merged_scans | Slowloris_Scan | protected_120 | +7.93 [5.50, 10.36]; significant |
| merged_scans | Slowloris_Scan | uniform_300 | +4.39 [0.60, 8.18]; significant |
| merged_scans | Slowloris_Scan | class_balanced_300 | -3.03 [-5.59, -0.46]; significant |
| merged_scans | Slowloris_Scan | protected_300 | +1.29 [-1.89, 4.47]; not significant |
| merged_scans | ICMP_Fragmentation | joint | +58.00 [48.99, 67.01]; significant |
| merged_scans | ICMP_Fragmentation | uniform_60 | +2.00 [-7.01, 11.01]; not significant |
| merged_scans | ICMP_Fragmentation | class_balanced_60 | +11.33 [2.61, 20.05]; significant |
| merged_scans | ICMP_Fragmentation | protected_60 | +8.00 [-0.65, 16.65]; not significant |
| merged_scans | ICMP_Fragmentation | uniform_120 | +4.67 [-2.10, 11.43]; not significant |
| merged_scans | ICMP_Fragmentation | class_balanced_120 | +14.67 [10.28, 19.05]; significant |
| merged_scans | ICMP_Fragmentation | protected_120 | +9.33 [1.48, 17.19]; significant |
| merged_scans | ICMP_Fragmentation | uniform_300 | +14.67 [7.28, 22.05]; significant |
| merged_scans | ICMP_Fragmentation | class_balanced_300 | +12.67 [6.53, 18.80]; significant |
| merged_scans | ICMP_Fragmentation | protected_300 | +19.33 [13.20, 25.47]; significant |

## Per-class protection interactions

| Score space | Class | Memory/client | Baseline | Extra gap reduction [95% interval] |
|---|---|---|---|---|
| original_type | Slowloris_Scan | 60 | uniform | -6.47 [-13.42, 0.49]; not significant |
| original_type | Slowloris_Scan | 60 | class_balanced | +5.02 [2.25, 7.79]; significant |
| original_type | Slowloris_Scan | 120 | uniform | +1.03 [-6.42, 8.48]; not significant |
| original_type | Slowloris_Scan | 120 | class_balanced | +2.92 [-0.28, 6.12]; not significant |
| original_type | Slowloris_Scan | 300 | uniform | +5.17 [2.66, 7.68]; significant |
| original_type | Slowloris_Scan | 300 | class_balanced | -6.98 [-9.56, -4.41]; significant |
| original_type | ICMP_Fragmentation | 60 | uniform | -6.00 [-20.82, 8.82]; not significant |
| original_type | ICMP_Fragmentation | 60 | class_balanced | +3.33 [-3.86, 10.53]; not significant |
| original_type | ICMP_Fragmentation | 120 | uniform | -4.67 [-12.79, 3.45]; not significant |
| original_type | ICMP_Fragmentation | 120 | class_balanced | +5.33 [-3.32, 13.98]; not significant |
| original_type | ICMP_Fragmentation | 300 | uniform | -4.67 [-11.05, 1.71]; not significant |
| original_type | ICMP_Fragmentation | 300 | class_balanced | -6.67 [-17.68, 4.35]; not significant |
| merged_scans | Slowloris_Scan | 60 | uniform | -5.27 [-10.95, 0.40]; not significant |
| merged_scans | Slowloris_Scan | 60 | class_balanced | +4.16 [0.74, 7.57]; significant |
| merged_scans | Slowloris_Scan | 120 | uniform | +0.13 [-5.76, 6.02]; not significant |
| merged_scans | Slowloris_Scan | 120 | class_balanced | -2.27 [-6.27, 1.73]; not significant |
| merged_scans | Slowloris_Scan | 300 | uniform | +3.10 [-2.32, 8.52]; not significant |
| merged_scans | Slowloris_Scan | 300 | class_balanced | -4.32 [-7.43, -1.20]; significant |
| merged_scans | ICMP_Fragmentation | 60 | uniform | -6.00 [-20.82, 8.82]; not significant |
| merged_scans | ICMP_Fragmentation | 60 | class_balanced | +3.33 [-3.86, 10.53]; not significant |
| merged_scans | ICMP_Fragmentation | 120 | uniform | -4.67 [-12.79, 3.45]; not significant |
| merged_scans | ICMP_Fragmentation | 120 | class_balanced | +5.33 [-3.32, 13.98]; not significant |
| merged_scans | ICMP_Fragmentation | 300 | uniform | -4.67 [-11.05, 1.71]; not significant |
| merged_scans | ICMP_Fragmentation | 300 | class_balanced | -6.67 [-17.68, 4.35]; not significant |

The memory-60 protected-versus-uniform interactions are not significant for either rare type. Original-type Slowloris at memory 300 has an interaction of +5.17 [2.66, 7.68]; significant points. This is a secondary comparison among many unadjusted contrasts; it should be described as exploratory, not selected after viewing results as a new confirmatory primary endpoint. ICMP fragmentation does not show a supported protection-over-uniform gap reduction.

## Rare-heavy and benign-starved clients

Both original-type and merged scores are reported below for every replay capacity and joint reference, in both environments. Full seed/order rows and paired client intervals are supplied as CSVs. N/A means no supported evaluation examples, not zero recall. FPR at the benign-starved client is undefined. These are synthetic allocation profiles evaluated with the global model, not personalized local models or five independently captured physical stations.

### merged_scans / centralized / benign_starved

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 91.01 ± 1.11 | 8.44 ± 1.10 | 88.22 ± 2.45 | 86.01 ± 2.97 | 87.17 ± 3.22 | 16.67 ± 23.57 | N/A |
| class_balanced_300 | 90.69 ± 1.27 | 8.84 ± 1.33 | 87.65 ± 1.80 | 84.32 ± 2.97 | 85.50 ± 3.10 | 13.33 ± 17.21 | N/A |
| class_balanced_60 | 90.72 ± 0.63 | 8.59 ± 0.75 | 87.35 ± 1.83 | 83.61 ± 2.01 | 84.78 ± 2.16 | 13.33 ± 17.21 | N/A |
| joint | 98.20 ± 0.48 | N/A | 90.72 ± 2.91 | 95.08 ± 2.70 | 96.22 ± 2.96 | 26.67 ± 30.63 | N/A |
| protected_120 | 88.15 ± 1.29 | 11.25 ± 1.23 | 75.43 ± 3.82 | 93.39 ± 2.05 | 94.06 ± 2.00 | 53.33 ± 17.21 | N/A |
| protected_300 | 95.42 ± 0.73 | 3.96 ± 0.73 | 89.53 ± 3.33 | 95.79 ± 2.81 | 96.50 ± 2.77 | 53.33 ± 17.21 | N/A |
| protected_60 | 81.36 ± 1.61 | 18.25 ± 1.61 | 63.39 ± 3.80 | 91.37 ± 1.94 | 92.17 ± 1.84 | 43.33 ± 22.50 | N/A |
| uniform_120 | 85.82 ± 2.14 | 13.81 ± 2.15 | 76.03 ± 2.81 | 86.28 ± 2.58 | 86.83 ± 2.44 | 53.33 ± 23.31 | N/A |
| uniform_300 | 93.77 ± 1.13 | 5.84 ± 1.15 | 88.92 ± 4.53 | 89.89 ± 2.81 | 90.44 ± 2.76 | 56.67 ± 22.50 | N/A |
| uniform_60 | 75.02 ± 2.32 | 24.61 ± 2.37 | 62.39 ± 3.81 | 69.67 ± 7.03 | 70.06 ± 7.29 | 46.67 ± 17.21 | N/A |

### merged_scans / centralized / low_rate_rare_heavy

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 89.52 ± 1.54 | 10.23 ± 1.59 | 93.99 ± 1.06 | 83.32 ± 4.15 | 83.41 ± 4.23 | 73.33 ± 5.74 | 6.67 ± 8.61 |
| class_balanced_300 | 88.76 ± 1.36 | 11.05 ± 1.36 | 94.25 ± 1.33 | 79.98 ± 3.33 | 80.02 ± 3.42 | 75.56 ± 11.48 | 3.33 ± 7.03 |
| class_balanced_60 | 90.11 ± 0.76 | 9.35 ± 0.95 | 90.09 ± 2.11 | 82.82 ± 2.66 | 82.93 ± 2.71 | 71.11 ± 5.74 | 15.00 ± 9.46 |
| joint | 98.01 ± 0.73 | N/A | 95.48 ± 2.61 | 94.87 ± 3.90 | 95.07 ± 3.95 | 73.33 ± 16.73 | 10.00 ± 11.65 |
| protected_120 | 87.48 ± 1.58 | 11.96 ± 1.59 | 73.36 ± 2.27 | 91.72 ± 2.38 | 92.21 ± 2.41 | 37.78 ± 7.77 | 0.00 ± 0.00 |
| protected_300 | 95.02 ± 0.70 | 4.28 ± 0.62 | 84.37 ± 1.41 | 95.22 ± 3.64 | 95.62 ± 3.68 | 51.11 ± 5.74 | 1.67 ± 5.27 |
| protected_60 | 80.55 ± 1.69 | 19.27 ± 1.71 | 64.31 ± 3.91 | 89.51 ± 1.66 | 90.03 ± 1.69 | 32.22 ± 11.05 | 3.33 ± 7.03 |
| uniform_120 | 85.17 ± 2.52 | 14.72 ± 2.54 | 73.60 ± 3.54 | 84.45 ± 2.83 | 84.91 ± 2.88 | 34.44 ± 8.20 | 5.00 ± 8.05 |
| uniform_300 | 92.86 ± 1.17 | 6.99 ± 1.23 | 83.62 ± 1.10 | 86.78 ± 3.32 | 87.16 ± 3.31 | 44.44 ± 9.07 | 3.33 ± 7.03 |
| uniform_60 | 74.55 ± 2.00 | 25.33 ± 2.01 | 62.50 ± 1.91 | 68.89 ± 5.81 | 69.24 ± 5.87 | 30.00 ± 7.50 | 5.00 ± 8.05 |

### merged_scans / federated / benign_starved

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 89.76 ± 1.42 | 9.86 ± 1.44 | 90.19 ± 1.79 | 80.55 ± 3.86 | 81.22 ± 3.79 | 40.00 ± 14.05 | N/A |
| class_balanced_300 | 90.38 ± 0.78 | 9.18 ± 0.85 | 89.24 ± 1.49 | 86.67 ± 1.34 | 87.67 ± 1.38 | 26.67 ± 14.05 | N/A |
| class_balanced_60 | 86.00 ± 1.34 | 13.63 ± 1.33 | 88.58 ± 1.56 | 74.92 ± 3.90 | 75.50 ± 3.91 | 40.00 ± 14.05 | N/A |
| joint | 95.63 ± 0.07 | N/A | 86.69 ± 0.04 | 82.02 ± 0.17 | 83.39 ± 0.18 | 0.00 ± 0.00 | N/A |
| protected_120 | 81.61 ± 2.81 | 17.94 ± 2.82 | 59.17 ± 3.67 | 87.21 ± 1.93 | 88.44 ± 1.96 | 13.33 ± 17.21 | N/A |
| protected_300 | 91.92 ± 0.47 | 7.43 ± 0.49 | 77.62 ± 3.97 | 93.83 ± 1.53 | 95.28 ± 1.44 | 6.67 ± 14.05 | N/A |
| protected_60 | 74.09 ± 2.49 | 25.48 ± 2.51 | 47.56 ± 3.89 | 84.59 ± 1.89 | 85.89 ± 1.87 | 6.67 ± 14.05 | N/A |
| uniform_120 | 79.08 ± 1.99 | 20.55 ± 1.93 | 58.70 ± 3.56 | 78.31 ± 8.03 | 79.50 ± 8.09 | 6.67 ± 14.05 | N/A |
| uniform_300 | 91.95 ± 0.80 | 7.70 ± 0.81 | 76.79 ± 2.10 | 85.30 ± 3.22 | 86.67 ± 3.23 | 3.33 ± 10.54 | N/A |
| uniform_60 | 66.33 ± 3.24 | 33.28 ± 3.24 | 46.40 ± 3.26 | 67.54 ± 7.81 | 68.28 ± 8.03 | 23.33 ± 22.50 | N/A |

### merged_scans / federated / low_rate_rare_heavy

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 88.06 ± 1.28 | 11.55 ± 1.30 | 80.63 ± 1.84 | 77.22 ± 3.65 | 77.45 ± 3.62 | 51.11 ± 14.05 | 21.67 ± 11.25 |
| class_balanced_300 | 87.87 ± 0.89 | 11.77 ± 0.90 | 82.30 ± 1.94 | 82.54 ± 0.94 | 82.74 ± 0.93 | 61.11 ± 5.86 | 21.67 ± 11.25 |
| class_balanced_60 | 83.55 ± 1.50 | 16.13 ± 1.47 | 78.30 ± 1.65 | 70.76 ± 4.22 | 70.90 ± 4.26 | 55.56 ± 12.83 | 28.33 ± 8.05 |
| joint | 93.98 ± 0.08 | N/A | 78.14 ± 1.71 | 75.29 ± 0.22 | 75.88 ± 0.18 | 10.00 ± 8.20 | 25.00 ± 14.16 |
| protected_120 | 79.99 ± 2.90 | 19.53 ± 2.98 | 63.93 ± 5.18 | 83.45 ± 2.52 | 83.89 ± 2.55 | 35.56 ± 7.03 | 8.33 ± 8.78 |
| protected_300 | 91.10 ± 0.60 | 8.14 ± 0.78 | 80.90 ± 1.65 | 93.81 ± 2.13 | 94.28 ± 2.12 | 42.22 ± 11.48 | 11.67 ± 11.25 |
| protected_60 | 72.58 ± 2.27 | 26.97 ± 2.34 | 53.99 ± 2.92 | 81.42 ± 2.30 | 81.87 ± 2.29 | 32.22 ± 8.20 | 5.00 ± 8.05 |
| uniform_120 | 78.21 ± 2.02 | 21.52 ± 2.05 | 64.97 ± 3.29 | 76.45 ± 7.37 | 76.77 ± 7.43 | 41.11 ± 7.50 | 15.00 ± 12.30 |
| uniform_300 | 90.69 ± 0.92 | 9.00 ± 0.94 | 80.05 ± 1.76 | 81.89 ± 3.95 | 82.25 ± 4.01 | 42.22 ± 10.21 | 13.33 ± 13.15 |
| uniform_60 | 65.31 ± 2.84 | 34.43 ± 2.89 | 50.69 ± 3.69 | 66.62 ± 6.77 | 66.89 ± 6.85 | 36.67 ± 9.15 | 18.33 ± 12.30 |

### original_type / centralized / benign_starved

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 55.06 ± 2.32 | 26.93 ± 2.35 | 56.84 ± 1.53 | 88.36 ± 2.91 | 89.56 ± 3.23 | 16.67 ± 23.57 | N/A |
| class_balanced_300 | 54.11 ± 2.07 | 28.53 ± 1.98 | 56.85 ± 1.27 | 87.05 ± 2.69 | 88.28 ± 2.85 | 13.33 ± 17.21 | N/A |
| class_balanced_60 | 54.09 ± 1.79 | 27.92 ± 1.78 | 56.47 ± 1.22 | 85.52 ± 1.57 | 86.72 ± 1.49 | 13.33 ± 17.21 | N/A |
| joint | 63.09 ± 3.09 | N/A | 59.38 ± 2.16 | 97.65 ± 0.63 | 98.83 ± 0.49 | 26.67 ± 30.63 | N/A |
| protected_120 | 57.10 ± 1.37 | 25.19 ± 1.29 | 48.82 ± 2.49 | 94.59 ± 1.58 | 95.28 ± 1.49 | 53.33 ± 17.21 | N/A |
| protected_300 | 64.07 ± 0.39 | 18.34 ± 0.45 | 57.92 ± 2.05 | 97.70 ± 0.85 | 98.44 ± 0.68 | 53.33 ± 17.21 | N/A |
| protected_60 | 51.79 ± 1.58 | 30.80 ± 1.65 | 41.27 ± 2.52 | 95.14 ± 1.37 | 96.00 ± 1.17 | 43.33 ± 22.50 | N/A |
| uniform_120 | 55.50 ± 1.66 | 26.91 ± 1.66 | 49.25 ± 1.83 | 87.54 ± 2.49 | 88.11 ± 2.33 | 53.33 ± 23.31 | N/A |
| uniform_300 | 63.22 ± 1.33 | 18.93 ± 1.40 | 57.75 ± 3.03 | 95.25 ± 3.24 | 95.89 ± 3.05 | 56.67 ± 22.50 | N/A |
| uniform_60 | 44.20 ± 2.29 | 38.32 ± 2.27 | 40.43 ± 2.40 | 70.00 ± 6.99 | 70.39 ± 7.25 | 46.67 ± 17.21 | N/A |

### original_type / centralized / low_rate_rare_heavy

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 54.21 ± 2.30 | 27.93 ± 2.49 | 62.71 ± 0.71 | 86.31 ± 3.26 | 86.42 ± 3.32 | 73.33 ± 5.74 | 6.67 ± 8.61 |
| class_balanced_300 | 52.74 ± 1.80 | 30.14 ± 1.79 | 62.70 ± 0.74 | 83.85 ± 3.46 | 83.93 ± 3.50 | 75.56 ± 11.48 | 3.33 ± 7.03 |
| class_balanced_60 | 54.28 ± 1.60 | 27.92 ± 1.91 | 60.28 ± 1.36 | 85.63 ± 1.58 | 85.76 ± 1.60 | 71.11 ± 5.74 | 15.00 ± 9.46 |
| joint | 63.15 ± 3.05 | N/A | 64.51 ± 2.19 | 98.94 ± 0.38 | 99.17 ± 0.41 | 73.33 ± 16.73 | 10.00 ± 11.65 |
| protected_120 | 56.42 ± 1.72 | 25.85 ± 1.87 | 49.12 ± 1.50 | 93.15 ± 2.07 | 93.66 ± 2.08 | 37.78 ± 7.77 | 0.00 ± 0.00 |
| protected_300 | 63.67 ± 0.32 | 18.74 ± 0.50 | 56.43 ± 1.16 | 97.83 ± 0.60 | 98.25 ± 0.62 | 51.11 ± 5.74 | 1.67 ± 5.27 |
| protected_60 | 51.44 ± 1.70 | 31.49 ± 1.67 | 43.04 ± 2.53 | 94.91 ± 2.13 | 95.48 ± 2.16 | 32.22 ± 11.05 | 3.33 ± 7.03 |
| uniform_120 | 54.80 ± 2.02 | 27.64 ± 2.08 | 49.18 ± 2.19 | 85.87 ± 2.09 | 86.33 ± 2.11 | 34.44 ± 8.20 | 5.00 ± 8.05 |
| uniform_300 | 62.53 ± 1.22 | 19.71 ± 1.48 | 56.16 ± 0.84 | 94.02 ± 3.31 | 94.47 ± 3.37 | 44.44 ± 9.07 | 3.33 ± 7.03 |
| uniform_60 | 43.53 ± 2.12 | 39.22 ± 1.96 | 41.64 ± 1.28 | 69.27 ± 5.92 | 69.63 ± 5.98 | 30.00 ± 7.50 | 5.00 ± 8.05 |

### original_type / federated / benign_starved

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 51.65 ± 1.33 | 30.90 ± 1.40 | 58.06 ± 1.24 | 81.37 ± 4.14 | 82.06 ± 4.09 | 40.00 ± 14.05 | N/A |
| class_balanced_300 | 53.98 ± 0.94 | 27.59 ± 0.95 | 57.38 ± 1.16 | 90.22 ± 2.10 | 91.28 ± 2.08 | 26.67 ± 14.05 | N/A |
| class_balanced_60 | 49.01 ± 1.62 | 33.40 ± 1.71 | 56.87 ± 0.83 | 75.68 ± 3.75 | 76.28 ± 3.78 | 40.00 ± 14.05 | N/A |
| joint | 56.33 ± 0.16 | N/A | 56.10 ± 0.31 | 82.51 ± 0.00 | 83.89 ± 0.00 | 0.00 ± 0.00 | N/A |
| protected_120 | 51.00 ± 2.66 | 30.48 ± 2.72 | 38.33 ± 2.32 | 90.16 ± 2.00 | 91.44 ± 1.91 | 13.33 ± 17.21 | N/A |
| protected_300 | 62.08 ± 0.28 | 19.61 ± 0.27 | 50.02 ± 2.38 | 94.81 ± 0.64 | 96.28 ± 0.53 | 6.67 ± 14.05 | N/A |
| protected_60 | 43.88 ± 2.55 | 37.83 ± 2.71 | 31.25 ± 2.84 | 88.31 ± 1.84 | 89.67 ± 1.87 | 6.67 ± 14.05 | N/A |
| uniform_120 | 48.68 ± 2.20 | 33.79 ± 2.06 | 38.27 ± 2.11 | 80.93 ± 9.33 | 82.17 ± 9.44 | 6.67 ± 14.05 | N/A |
| uniform_300 | 61.01 ± 0.59 | 20.68 ± 0.61 | 49.83 ± 1.42 | 88.63 ± 1.33 | 90.06 ± 1.27 | 3.33 ± 10.54 | N/A |
| uniform_60 | 36.05 ± 3.37 | 46.32 ± 3.22 | 30.04 ± 2.11 | 67.87 ± 8.59 | 68.61 ± 8.83 | 23.33 ± 22.50 | N/A |

### original_type / federated / low_rate_rare_heavy

| Method | Old accuracy | Forgetting | Macro recall | Combined rare | Slowloris | Fragmentation | FPR |
|---|---|---|---|---|---|---|---|
| class_balanced_120 | 49.83 ± 1.31 | 32.52 ± 1.39 | 53.58 ± 1.30 | 77.80 ± 3.65 | 78.04 ± 3.61 | 51.11 ± 14.05 | 21.67 ± 11.25 |
| class_balanced_300 | 52.95 ± 1.12 | 28.61 ± 1.24 | 55.03 ± 1.27 | 88.01 ± 2.77 | 88.25 ± 2.77 | 61.11 ± 5.86 | 21.67 ± 11.25 |
| class_balanced_60 | 47.21 ± 1.68 | 35.42 ± 1.82 | 52.01 ± 1.00 | 71.41 ± 4.16 | 71.56 ± 4.19 | 55.56 ± 12.83 | 28.33 ± 8.05 |
| joint | 55.07 ± 0.47 | N/A | 52.83 ± 1.22 | 75.74 ± 0.11 | 76.31 ± 0.09 | 12.22 ± 6.31 | 25.00 ± 14.16 |
| protected_120 | 49.68 ± 2.65 | 31.64 ± 2.85 | 42.83 ± 3.33 | 87.54 ± 2.36 | 88.01 ± 2.40 | 35.56 ± 7.03 | 8.33 ± 8.78 |
| protected_300 | 61.54 ± 0.60 | 19.88 ± 0.76 | 53.95 ± 1.08 | 95.33 ± 1.27 | 95.81 ± 1.23 | 42.22 ± 11.48 | 11.67 ± 11.25 |
| protected_60 | 42.39 ± 2.64 | 39.06 ± 3.09 | 36.12 ± 1.94 | 85.69 ± 2.68 | 86.17 ± 2.71 | 32.22 ± 8.20 | 5.00 ± 8.05 |
| uniform_120 | 48.07 ± 2.21 | 34.23 ± 2.07 | 43.74 ± 1.91 | 79.85 ± 8.83 | 80.20 ± 8.93 | 41.11 ± 7.50 | 15.00 ± 12.30 |
| uniform_300 | 59.79 ± 0.66 | 21.62 ± 0.76 | 53.55 ± 1.13 | 86.26 ± 1.77 | 86.66 ± 1.80 | 42.22 ± 10.21 | 13.33 ± 13.15 |
| uniform_60 | 35.16 ± 3.06 | 47.16 ± 3.10 | 33.99 ± 2.38 | 67.11 ± 8.04 | 67.38 ± 8.13 | 36.67 ± 9.15 | 18.33 ± 12.30 |

## Clarification of 33.33%

The original combined rare recall weights 600 Slowloris examples and 5 ICMP-fragmentation examples by their supports; it is not the unweighted mean of two recalls or a mean over three classes. The separate macro-rare metric is distinct. For federated no replay, both types have 100% recall only in order 2, where rare attacks are last, and both have 0% in orders 1/3. Each seed therefore averages (0 + 1 + 0)/3 = 1/3, giving zero seed SD. Neither class is always correct across attack orders. EWC has some fragmentation misses in order 2, giving 33.31% ± 0.03% federated. Centralized no replay and EWC also have misses and differ slightly from 33.33%. See rare_metric_reconstruction.csv and rare_baseline_class_breakdown.csv.

## Evidence and limitations

All 840 original runs were re-scored; no MLP was retrained. The independent verification JSON checks every merged checkpoint against original probabilities, input hash preservation, paired calculations, RF role boundaries, and rare-metric reconstruction. Three new unit tests cover the mapping, probability-sum decision rule and ten-pair interval requirement. Original results and the earlier 17-test evidence remain preserved. Five fragmentation test examples and sixteen benign examples limit claims. Results are frozen for review; manuscript writing and additional experiments remain on hold.
