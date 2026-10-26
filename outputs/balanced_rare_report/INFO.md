# Complete final experiment results

Merged-Scan scores are primary; Slowloris is the reported rare-attack metric. The combined 605-example metric is not used in this report. All evaluation results are preserved, including losses.

## Main summary and memory results

- Used merged-Scan scores as primary, Slowloris recall alone, and paired comparisons against both existing baselines; retained exact-type sensitivity results.

## 2. Main results table

Merged-Scan primary scores, federated, memory 60/client. Mean ± SD over ten seed averages across three orders. Worst client: supported-class macro recall. Joint forgetting: not applicable.

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| No replay | 22.22 ± 0.00 | 77.60 ± 0.02 | 33.33 ± 0.00 | 14.81 ± 0.00 |
| Uniform | 65.29 ± 2.92 | 34.53 ± 2.93 | 66.98 ± 7.02 | 45.50 ± 2.86 |
| Class-balanced | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.56 ± 4.19 | 77.97 ± 1.05 |
| Protected | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.73 ± 2.36 | 47.15 ± 3.82 |
| Balanced + rare | 85.52 ± 1.27 | 14.24 ± 1.27 | 76.62 ± 4.16 | 79.03 ± 1.00 |
| EWC | 24.89 ± 1.30 | 74.95 ± 1.30 | 33.33 ± 0.00 | 17.15 ± 3.56 |
| A-GEM | 46.03 ± 4.58 | 53.80 ± 4.58 | 50.29 ± 4.68 | 37.12 ± 3.29 |
| Joint | 94.20 ± 0.07 | N/A | 76.82 ± 0.17 | 77.89 ± 1.48 |

Memory sweep: old accuracy / Slowloris / worst client (%).

| Method | Memory 60 | Memory 300 |
| --- | --- | --- |
| Class-balanced | 83.99 / 71.56 / 77.97 | 88.26 / 83.43 / 81.48 |
| Protected | 72.84 / 82.73 / 47.15 | 91.24 / 94.45 / 75.72 |
| Balanced + rare | 85.52 / 76.62 / 79.03 | 89.94 / 89.37 / 81.91 |

## 3. Key comparisons

Paired 95% intervals; better/worse denotes statistically significant direction.
- New − class-balanced, memory 60: old accuracy +1.53 [+0.23, +2.84]; better; Slowloris +5.06 [+1.27, +8.84]; better; worst client +1.06 [-0.07, +2.19]; not significant.
- New − protected, memory 60: old accuracy +12.68 [+10.97, +14.40]; better; Slowloris -6.11 [-9.82, -2.40]; worse; worst client +31.87 [+29.33, +34.42]; better.
- Federated − centralized difference in new-over-balanced gains, memory 60: old accuracy -0.14 [-1.54, +1.26]; Slowloris +0.06 [-4.26, +4.38]; both not significant.

## 4. What this means

- At memory 60, the new method improves federated old accuracy and Slowloris recall over class-balanced replay. Worst-client improvement is not significant. The requested significance pattern is met on order-averaged results in both settings; this does not establish non-inferiority.
- The method does not dominate protected replay: federated Slowloris recall is lower at both capacities, and old accuracy is lower at memory 300, while worst-client score is higher. All order-specific losses are retained.
- At memory 60, the gain over class-balanced is not significantly different between federated and centralized training. Exact-type sensitivity supports the broad trade-off, but some significance conclusions differ; see INFO.md.

Memory-300 federated comparisons (new minus baseline):

| Comparison | Old accuracy | Slowloris | Worst client |
| --- | --- | --- | --- |
| vs balanced | +1.68 [+0.95, +2.40]; better | +5.94 [+3.46, +8.43]; better | +0.42 [+0.12, +0.73]; better |
| vs protected | -1.30 [-2.22, -0.39]; worse | -5.08 [-7.71, -2.44]; worse | +6.19 [+5.24, +7.14]; better |

## 5. Problems or surprises

- Only 600 Slowloris, five fragmentation and 16 benign evaluation examples exist. No fragmentation conclusions are drawn; benign-starved false alarms remain undefined.
- Merged scoring retains original task cohorts, 15-type training and type-level balancing. Scan spans two tasks. Exact-type comparisons are sensitivity results; differences between views must be disclosed.
- Intervals reflect ten training seeds on one fixed split, with three orders averaged per seed; multiple comparisons are unadjusted. The earlier Slowloris federation interaction at memory 300 remains exploratory.

## 6. Questions for review

- Review the paired outcomes and agree on the final trade-off/contribution before manuscript writing. Results and method are now frozen; no further method adjustment or experiment is proposed.

## merged_scans: complete mean ± SD tables


### federated

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| agem | 46.03 ± 4.58 | 53.80 ± 4.58 | 50.29 ± 4.68 | 37.12 ± 3.29 |
| balanced_rare_300 | 89.94 ± 0.98 | 9.50 ± 1.08 | 89.37 ± 2.87 | 81.91 ± 1.34 |
| balanced_rare_60 | 85.52 ± 1.27 | 14.24 ± 1.27 | 76.62 ± 4.16 | 79.03 ± 1.00 |
| class_balanced_120 | 88.24 ± 1.26 | 11.49 ± 1.28 | 78.13 ± 3.67 | 80.29 ± 1.62 |
| class_balanced_300 | 88.26 ± 0.76 | 11.43 ± 0.77 | 83.43 ± 1.02 | 81.48 ± 1.29 |
| class_balanced_60 | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.56 ± 4.19 | 77.97 ± 1.05 |
| ewc | 24.89 ± 1.30 | 74.95 ± 1.30 | 33.33 ± 0.00 | 17.15 ± 3.56 |
| fedprox_no_replay | 22.24 ± 0.05 | 77.59 ± 0.05 | 33.33 ± 0.00 | 14.80 ± 0.16 |
| joint | 94.20 ± 0.07 | N/A | 76.82 ± 0.17 | 77.89 ± 1.48 |
| no_replay | 22.22 ± 0.00 | 77.60 ± 0.02 | 33.33 ± 0.00 | 14.81 ± 0.00 |
| protected_120 | 80.09 ± 2.93 | 19.55 ± 2.98 | 84.73 ± 2.50 | 58.15 ± 4.34 |
| protected_300 | 91.24 ± 0.52 | 8.15 ± 0.64 | 94.45 ± 1.97 | 75.72 ± 1.43 |
| protected_60 | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.73 ± 2.36 | 47.15 ± 3.82 |
| uniform_120 | 78.08 ± 2.05 | 21.72 ± 2.06 | 77.16 ± 7.41 | 58.27 ± 3.25 |
| uniform_300 | 90.85 ± 0.77 | 8.91 ± 0.77 | 83.12 ± 3.94 | 75.20 ± 1.08 |
| uniform_60 | 65.29 ± 2.92 | 34.53 ± 2.93 | 66.98 ± 7.02 | 45.50 ± 2.86 |

### centralized

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| agem | 57.87 ± 3.96 | 41.98 ± 3.97 | 50.03 ± 2.17 | 49.19 ± 2.98 |
| balanced_rare_300 | 91.90 ± 0.56 | 7.47 ± 0.57 | 91.32 ± 0.54 | 86.86 ± 0.32 |
| balanced_rare_60 | 91.70 ± 0.89 | 7.71 ± 1.05 | 88.36 ± 2.22 | 85.52 ± 1.03 |
| class_balanced_120 | 89.50 ± 1.39 | 10.17 ± 1.44 | 83.79 ± 4.09 | 86.23 ± 0.44 |
| class_balanced_300 | 88.75 ± 1.38 | 11.01 ± 1.38 | 80.40 ± 3.50 | 85.91 ± 0.51 |
| class_balanced_60 | 90.03 ± 0.87 | 9.43 ± 1.02 | 83.36 ± 2.93 | 84.88 ± 0.97 |
| ewc | 22.32 ± 0.19 | 77.51 ± 0.19 | 33.33 ± 0.00 | 14.59 ± 1.25 |
| fedprox_no_replay | 22.35 ± 0.27 | 77.44 ± 0.28 | 33.33 ± 0.00 | 14.98 ± 0.34 |
| joint | 97.96 ± 0.69 | N/A | 95.33 ± 3.88 | 88.00 ± 0.31 |
| no_replay | 22.22 ± 0.01 | 77.64 ± 0.02 | 33.33 ± 0.00 | 14.81 ± 0.00 |
| protected_120 | 87.39 ± 1.50 | 12.05 ± 1.50 | 92.66 ± 2.27 | 71.58 ± 2.42 |
| protected_300 | 95.06 ± 0.69 | 4.28 ± 0.67 | 95.74 ± 3.57 | 83.51 ± 1.28 |
| protected_60 | 80.48 ± 1.62 | 19.28 ± 1.64 | 90.37 ± 1.81 | 60.27 ± 3.91 |
| uniform_120 | 85.02 ± 2.40 | 14.79 ± 2.41 | 85.21 ± 2.73 | 71.20 ± 2.91 |
| uniform_300 | 92.77 ± 1.17 | 7.03 ± 1.21 | 87.51 ± 3.22 | 81.82 ± 1.65 |
| uniform_60 | 74.42 ± 2.04 | 25.40 ± 2.04 | 69.35 ± 6.10 | 59.65 ± 1.64 |

## merged_scans: all paired comparisons, including losses


### centralized, memory 60, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.67 | [+1.12, +2.22] | better |
| class_balanced_60 | forgetting | -1.72 | [-2.39, -1.05] | better |
| class_balanced_60 | slowloris_recall | +5.00 | [+3.04, +6.96] | better |
| class_balanced_60 | worst_client_macro_recall | +0.64 | [+0.14, +1.14] | better |
| protected_60 | old_task_accuracy | +11.21 | [+9.53, +12.90] | better |
| protected_60 | forgetting | -11.57 | [-13.37, -9.77] | better |
| protected_60 | slowloris_recall | -2.01 | [-4.53, +0.50] | not significant |
| protected_60 | worst_client_macro_recall | +25.25 | [+22.39, +28.10] | better |

### centralized, memory 60, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.50 | [+0.32, +2.69] | better |
| class_balanced_60 | forgetting | -1.50 | [-2.69, -0.32] | better |
| class_balanced_60 | slowloris_recall | +4.53 | [+0.91, +8.16] | better |
| class_balanced_60 | worst_client_macro_recall | +0.51 | [-0.23, +1.26] | not significant |
| protected_60 | old_task_accuracy | -2.27 | [-4.07, -0.47] | worse |
| protected_60 | forgetting | +1.93 | [-0.04, +3.90] | not significant |
| protected_60 | slowloris_recall | -20.47 | [-22.05, -18.88] | worse |
| protected_60 | worst_client_macro_recall | +11.36 | [+6.87, +15.85] | better |

### centralized, memory 60, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_60 | old_task_accuracy | +31.54 | [+28.43, +34.66] | better |
| protected_60 | forgetting | -31.54 | [-34.66, -28.43] | better |
| protected_60 | slowloris_recall | -0.52 | [-1.03, -0.00] | worse |
| protected_60 | worst_client_macro_recall | +53.22 | [+46.32, +60.13] | better |

### centralized, memory 60, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +3.51 | [+1.59, +5.42] | better |
| class_balanced_60 | forgetting | -3.66 | [-5.96, -1.37] | better |
| class_balanced_60 | slowloris_recall | +10.47 | [+3.89, +17.05] | better |
| class_balanced_60 | worst_client_macro_recall | +1.41 | [+0.12, +2.70] | better |
| protected_60 | old_task_accuracy | +4.37 | [+2.38, +6.35] | better |
| protected_60 | forgetting | -5.11 | [-7.42, -2.80] | better |
| protected_60 | slowloris_recall | +14.95 | [+7.97, +21.93] | better |
| protected_60 | worst_client_macro_recall | +11.16 | [+10.11, +12.22] | better |

### centralized, memory 300, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +3.15 | [+2.32, +3.98] | better |
| class_balanced_300 | forgetting | -3.54 | [-4.35, -2.73] | better |
| class_balanced_300 | slowloris_recall | +10.92 | [+8.52, +13.32] | better |
| class_balanced_300 | worst_client_macro_recall | +0.96 | [+0.52, +1.39] | better |
| protected_300 | old_task_accuracy | -3.16 | [-3.75, -2.56] | worse |
| protected_300 | forgetting | +3.18 | [+2.56, +3.81] | worse |
| protected_300 | slowloris_recall | -4.42 | [-7.04, -1.80] | worse |
| protected_300 | worst_client_macro_recall | +3.36 | [+2.37, +4.34] | better |

### centralized, memory 300, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +2.98 | [+0.43, +5.52] | better |
| class_balanced_300 | forgetting | -2.98 | [-5.52, -0.43] | better |
| class_balanced_300 | slowloris_recall | +9.58 | [+1.91, +17.26] | better |
| class_balanced_300 | worst_client_macro_recall | +1.00 | [-0.05, +2.06] | not significant |
| protected_300 | old_task_accuracy | -5.34 | [-5.81, -4.87] | worse |
| protected_300 | forgetting | +5.26 | [+4.79, +5.73] | worse |
| protected_300 | slowloris_recall | -19.93 | [-21.49, -18.37] | worse |
| protected_300 | worst_client_macro_recall | +1.59 | [-1.62, +4.81] | not significant |

### centralized, memory 300, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | old_task_accuracy | -4.20 | [-5.93, -2.48] | worse |
| protected_300 | forgetting | +4.22 | [+2.49, +5.95] | worse |
| protected_300 | slowloris_recall | +7.33 | [+0.10, +14.57] | better |
| protected_300 | worst_client_macro_recall | +2.48 | [+1.56, +3.40] | better |

### centralized, memory 300, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +6.48 | [+5.57, +7.38] | better |
| class_balanced_300 | forgetting | -7.64 | [-8.56, -6.72] | better |
| class_balanced_300 | slowloris_recall | +23.17 | [+20.60, +25.74] | better |
| class_balanced_300 | worst_client_macro_recall | +1.87 | [+0.96, +2.78] | better |
| protected_300 | old_task_accuracy | +0.08 | [-0.19, +0.35] | not significant |
| protected_300 | forgetting | +0.08 | [-0.26, +0.42] | not significant |
| protected_300 | slowloris_recall | -0.67 | [-1.69, +0.36] | not significant |
| protected_300 | worst_client_macro_recall | +5.99 | [+4.14, +7.84] | better |

### federated, memory 60, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.53 | [+0.23, +2.84] | better |
| class_balanced_60 | forgetting | -1.54 | [-2.85, -0.22] | better |
| class_balanced_60 | slowloris_recall | +5.06 | [+1.27, +8.84] | better |
| class_balanced_60 | worst_client_macro_recall | +1.06 | [-0.07, +2.19] | not significant |
| protected_60 | old_task_accuracy | +12.68 | [+10.97, +14.40] | better |
| protected_60 | forgetting | -12.60 | [-14.34, -10.85] | better |
| protected_60 | slowloris_recall | -6.11 | [-9.82, -2.40] | worse |
| protected_60 | worst_client_macro_recall | +31.87 | [+29.33, +34.42] | better |

### federated, memory 60, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +3.58 | [+0.93, +6.23] | better |
| class_balanced_60 | forgetting | -3.58 | [-6.23, -0.93] | better |
| class_balanced_60 | slowloris_recall | +11.60 | [+2.99, +20.21] | better |
| class_balanced_60 | worst_client_macro_recall | +2.94 | [+0.54, +5.34] | better |
| protected_60 | old_task_accuracy | +13.48 | [+8.64, +18.33] | better |
| protected_60 | forgetting | -13.54 | [-18.39, -8.70] | better |
| protected_60 | slowloris_recall | -14.85 | [-24.15, -5.55] | worse |
| protected_60 | worst_client_macro_recall | +34.90 | [+27.68, +42.13] | better |

### federated, memory 60, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_60 | old_task_accuracy | +26.27 | [+24.69, +27.85] | better |
| protected_60 | forgetting | -26.27 | [-27.85, -24.69] | better |
| protected_60 | slowloris_recall | +3.02 | [-0.23, +6.26] | not significant |
| protected_60 | worst_client_macro_recall | +58.66 | [+55.46, +61.86] | better |

### federated, memory 60, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.02 | [-1.24, +3.28] | not significant |
| class_balanced_60 | forgetting | -1.02 | [-3.31, +1.26] | not significant |
| class_balanced_60 | slowloris_recall | +3.57 | [-2.12, +9.25] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.24 | [-2.17, +2.66] | not significant |
| protected_60 | old_task_accuracy | -1.70 | [-4.04, +0.63] | not significant |
| protected_60 | forgetting | +2.02 | [-0.55, +4.59] | not significant |
| protected_60 | slowloris_recall | -6.50 | [-11.95, -1.05] | worse |
| protected_60 | worst_client_macro_recall | +2.06 | [-0.38, +4.49] | not significant |

### federated, memory 300, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +1.68 | [+0.95, +2.40] | better |
| class_balanced_300 | forgetting | -1.93 | [-2.75, -1.12] | better |
| class_balanced_300 | slowloris_recall | +5.94 | [+3.46, +8.43] | better |
| class_balanced_300 | worst_client_macro_recall | +0.42 | [+0.12, +0.73] | better |
| protected_300 | old_task_accuracy | -1.30 | [-2.22, -0.39] | worse |
| protected_300 | forgetting | +1.35 | [+0.33, +2.37] | worse |
| protected_300 | slowloris_recall | -5.08 | [-7.71, -2.44] | worse |
| protected_300 | worst_client_macro_recall | +6.19 | [+5.24, +7.14] | better |

### federated, memory 300, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.19 | [-0.01, +0.40] | not significant |
| class_balanced_300 | forgetting | -0.19 | [-0.39, +0.01] | not significant |
| class_balanced_300 | slowloris_recall | +0.78 | [+0.11, +1.45] | better |
| class_balanced_300 | worst_client_macro_recall | -0.25 | [-1.10, +0.59] | not significant |
| protected_300 | old_task_accuracy | -1.84 | [-2.43, -1.25] | worse |
| protected_300 | forgetting | +1.71 | [+1.12, +2.30] | worse |
| protected_300 | slowloris_recall | -12.87 | [-14.78, -10.95] | worse |
| protected_300 | worst_client_macro_recall | +8.61 | [+6.36, +10.87] | better |

### federated, memory 300, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | old_task_accuracy | -1.63 | [-3.05, -0.21] | worse |
| protected_300 | forgetting | +1.63 | [+0.21, +3.05] | worse |
| protected_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | worst_client_macro_recall | +7.90 | [+5.91, +9.90] | better |

### federated, memory 300, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +4.83 | [+2.73, +6.94] | better |
| class_balanced_300 | forgetting | -5.62 | [-7.99, -3.24] | better |
| class_balanced_300 | slowloris_recall | +17.05 | [+9.86, +24.24] | better |
| class_balanced_300 | worst_client_macro_recall | +1.53 | [+0.83, +2.22] | better |
| protected_300 | old_task_accuracy | -0.45 | [-2.36, +1.47] | not significant |
| protected_300 | forgetting | +0.71 | [-1.59, +3.01] | not significant |
| protected_300 | slowloris_recall | -2.37 | [-9.33, +4.60] | not significant |
| protected_300 | worst_client_macro_recall | +2.05 | [+0.51, +3.60] | better |

## merged_scans: every order, mean ± SD

| Environment | Method | Order | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- | --- | --- |
| centralized | agem | order_1 | 71.43 ± 5.13 | 28.40 ± 5.13 | 48.13 ± 1.12 | 53.91 ± 8.71 |
| centralized | agem | order_2 | 35.47 ± 10.73 | 64.43 ± 10.72 | 100.00 ± 0.00 | 26.93 ± 2.92 |
| centralized | agem | order_3 | 66.69 ± 2.17 | 33.12 ± 2.15 | 1.97 ± 6.22 | 66.72 ± 1.68 |
| centralized | balanced_rare_300 | order_1 | 91.69 ± 0.57 | 8.02 ± 0.65 | 76.62 ± 1.62 | 86.31 ± 0.51 |
| centralized | balanced_rare_300 | order_2 | 86.51 ± 1.44 | 13.40 ± 1.44 | 100.00 ± 0.00 | 86.43 ± 0.53 |
| centralized | balanced_rare_300 | order_3 | 97.50 ± 0.32 | 0.99 ± 0.43 | 97.33 ± 1.20 | 87.85 ± 0.76 |
| centralized | balanced_rare_60 | order_1 | 91.18 ± 0.83 | 8.27 ± 0.94 | 75.68 ± 2.24 | 83.83 ± 3.48 |
| centralized | balanced_rare_60 | order_2 | 88.66 ± 0.96 | 11.24 ± 0.95 | 99.42 ± 0.68 | 85.93 ± 1.04 |
| centralized | balanced_rare_60 | order_3 | 95.24 ± 1.76 | 3.62 ± 2.08 | 89.98 ± 5.90 | 86.80 ± 1.38 |
| centralized | class_balanced_120 | order_1 | 88.65 ± 3.08 | 11.11 ± 3.11 | 67.07 ± 9.45 | 85.40 ± 1.16 |
| centralized | class_balanced_120 | order_2 | 85.81 ± 0.99 | 14.09 ± 0.98 | 99.97 ± 0.11 | 86.31 ± 0.17 |
| centralized | class_balanced_120 | order_3 | 94.04 ± 2.46 | 5.31 ± 2.65 | 84.33 ± 8.20 | 86.98 ± 0.75 |
| centralized | class_balanced_300 | order_1 | 88.71 ± 3.56 | 10.99 ± 3.56 | 67.03 ± 10.92 | 85.31 ± 1.34 |
| centralized | class_balanced_300 | order_2 | 86.51 ± 1.44 | 13.40 ± 1.44 | 100.00 ± 0.00 | 86.43 ± 0.53 |
| centralized | class_balanced_300 | order_3 | 91.03 ± 1.18 | 8.62 ± 1.22 | 74.17 ± 3.52 | 85.98 ± 0.88 |
| centralized | class_balanced_60 | order_1 | 89.68 ± 1.35 | 9.77 ± 1.43 | 71.15 ± 4.13 | 83.32 ± 3.26 |
| centralized | class_balanced_60 | order_2 | 88.66 ± 0.96 | 11.24 ± 0.95 | 99.42 ± 0.68 | 85.93 ± 1.04 |
| centralized | class_balanced_60 | order_3 | 91.73 ± 2.15 | 7.28 ± 2.66 | 79.52 ± 8.13 | 85.39 ± 1.51 |
| centralized | ewc | order_1 | 33.31 ± 0.02 | 66.47 ± 0.22 | 0.00 ± 0.00 | 11.10 ± 0.02 |
| centralized | ewc | order_2 | 0.06 ± 0.19 | 99.84 ± 0.19 | 100.00 ± 0.00 | 21.19 ± 3.55 |
| centralized | ewc | order_3 | 33.60 ± 0.56 | 66.23 ± 0.57 | 0.00 ± 0.00 | 11.50 ± 0.83 |
| centralized | fedprox_no_replay | order_1 | 33.33 ± 0.00 | 66.50 ± 0.03 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| centralized | fedprox_no_replay | order_2 | 0.39 ± 0.81 | 99.51 ± 0.82 | 100.00 ± 0.00 | 22.70 ± 1.02 |
| centralized | fedprox_no_replay | order_3 | 33.33 ± 0.00 | 66.30 ± 0.35 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| centralized | joint | order_1 | 97.78 ± 1.84 | N/A | 95.05 ± 5.67 | 88.24 ± 0.53 |
| centralized | joint | order_2 | 98.52 ± 0.63 | N/A | 93.95 ± 9.37 | 87.82 ± 0.94 |
| centralized | joint | order_3 | 97.59 ± 1.64 | N/A | 97.00 ± 5.92 | 87.95 ± 0.65 |
| centralized | no_replay | order_1 | 33.32 ± 0.02 | 66.54 ± 0.03 | 0.00 ± 0.00 | 11.10 ± 0.01 |
| centralized | no_replay | order_2 | 0.00 ± 0.00 | 99.90 ± 0.02 | 100.00 ± 0.00 | 22.22 ± 0.00 |
| centralized | no_replay | order_3 | 33.33 ± 0.00 | 66.48 ± 0.06 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| centralized | protected_120 | order_1 | 93.52 ± 1.52 | 6.26 ± 1.54 | 85.95 ± 6.42 | 79.02 ± 3.19 |
| centralized | protected_120 | order_2 | 72.21 ± 3.78 | 27.69 ± 3.77 | 97.52 ± 3.48 | 56.56 ± 6.30 |
| centralized | protected_120 | order_3 | 96.45 ± 0.73 | 2.21 ± 0.93 | 94.52 ± 2.58 | 79.16 ± 2.63 |
| centralized | protected_300 | order_1 | 97.03 ± 0.70 | 2.76 ± 0.70 | 96.55 ± 2.19 | 84.72 ± 4.44 |
| centralized | protected_300 | order_2 | 90.72 ± 1.72 | 9.19 ± 1.72 | 92.67 ± 10.12 | 83.95 ± 1.16 |
| centralized | protected_300 | order_3 | 97.43 ± 0.33 | 0.91 ± 0.20 | 98.00 ± 0.53 | 81.86 ± 2.75 |
| centralized | protected_60 | order_1 | 93.45 ± 2.21 | 6.34 ± 2.24 | 96.15 ± 1.59 | 72.47 ± 5.40 |
| centralized | protected_60 | order_2 | 57.12 ± 3.68 | 42.78 ± 3.68 | 99.93 ± 0.14 | 32.70 ± 8.97 |
| centralized | protected_60 | order_3 | 90.87 ± 1.43 | 8.72 ± 1.53 | 75.03 ± 5.01 | 75.64 ± 1.03 |
| centralized | uniform_120 | order_1 | 96.42 ± 1.12 | 3.37 ± 1.15 | 96.18 ± 1.53 | 78.71 ± 2.13 |
| centralized | uniform_120 | order_2 | 72.59 ± 6.44 | 27.31 ± 6.43 | 99.97 ± 0.11 | 59.06 ± 9.53 |
| centralized | uniform_120 | order_3 | 86.04 ± 2.39 | 13.70 ± 2.41 | 59.48 ± 7.25 | 75.84 ± 2.08 |
| centralized | uniform_300 | order_1 | 96.58 ± 1.30 | 3.22 ± 1.33 | 94.30 ± 4.72 | 83.90 ± 4.28 |
| centralized | uniform_300 | order_2 | 90.44 ± 1.86 | 9.46 ± 1.86 | 92.85 ± 10.25 | 82.28 ± 4.27 |
| centralized | uniform_300 | order_3 | 91.29 ± 2.05 | 8.41 ± 2.19 | 75.38 ± 6.57 | 79.28 ± 3.52 |
| centralized | uniform_60 | order_1 | 95.41 ± 1.15 | 4.39 ± 1.18 | 96.68 ± 1.11 | 75.39 ± 2.42 |
| centralized | uniform_60 | order_2 | 57.66 ± 3.29 | 42.24 ± 3.29 | 99.83 ± 0.33 | 34.79 ± 5.33 |
| centralized | uniform_60 | order_3 | 70.18 ± 6.18 | 29.58 ± 6.16 | 11.53 ± 18.66 | 68.76 ± 2.55 |
| federated | agem | order_1 | 52.63 ± 3.28 | 47.17 ± 3.25 | 46.03 ± 1.14 | 23.51 ± 5.69 |
| federated | agem | order_2 | 17.70 ± 11.73 | 82.23 ± 11.74 | 100.00 ± 0.00 | 21.19 ± 6.93 |
| federated | agem | order_3 | 67.75 ± 4.54 | 32.01 ± 4.54 | 4.83 ± 13.83 | 66.67 ± 1.73 |
| federated | balanced_rare_300 | order_1 | 91.76 ± 0.33 | 7.84 ± 0.35 | 76.72 ± 1.06 | 83.61 ± 2.83 |
| federated | balanced_rare_300 | order_2 | 82.36 ± 2.04 | 17.57 ± 2.04 | 100.00 ± 0.00 | 82.87 ± 1.46 |
| federated | balanced_rare_300 | order_3 | 95.69 ± 2.35 | 3.09 ± 2.67 | 91.40 ± 8.11 | 79.24 ± 2.47 |
| federated | balanced_rare_60 | order_1 | 86.83 ± 3.83 | 12.87 ± 3.84 | 62.57 ± 11.99 | 80.56 ± 2.70 |
| federated | balanced_rare_60 | order_2 | 82.21 ± 1.25 | 17.72 ± 1.25 | 99.87 ± 0.22 | 81.69 ± 1.35 |
| federated | balanced_rare_60 | order_3 | 87.53 ± 1.90 | 12.12 ± 1.93 | 67.42 ± 2.11 | 74.84 ± 2.81 |
| federated | class_balanced_120 | order_1 | 88.43 ± 3.49 | 11.15 ± 3.52 | 66.50 ± 10.73 | 81.38 ± 3.62 |
| federated | class_balanced_120 | order_2 | 87.25 ± 1.09 | 12.67 ± 1.09 | 99.15 ± 1.17 | 83.65 ± 3.47 |
| federated | class_balanced_120 | order_3 | 89.03 ± 0.59 | 10.63 ± 0.61 | 68.75 ± 1.88 | 75.85 ± 1.59 |
| federated | class_balanced_300 | order_1 | 91.56 ± 0.23 | 8.03 ± 0.22 | 75.93 ± 0.68 | 83.86 ± 2.62 |
| federated | class_balanced_300 | order_2 | 82.36 ± 2.04 | 17.57 ± 2.04 | 100.00 ± 0.00 | 82.87 ± 1.46 |
| federated | class_balanced_300 | order_3 | 90.86 ± 1.05 | 8.71 ± 1.13 | 74.35 ± 3.39 | 77.71 ± 2.46 |
| federated | class_balanced_60 | order_1 | 83.24 ± 2.79 | 16.45 ± 2.74 | 50.97 ± 8.68 | 77.62 ± 2.79 |
| federated | class_balanced_60 | order_2 | 82.21 ± 1.25 | 17.72 ± 1.25 | 99.87 ± 0.22 | 81.69 ± 1.35 |
| federated | class_balanced_60 | order_3 | 86.52 ± 2.86 | 13.14 ± 2.87 | 63.85 ± 7.66 | 74.59 ± 1.89 |
| federated | ewc | order_1 | 33.33 ± 0.00 | 66.51 ± 0.06 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| federated | ewc | order_2 | 0.37 ± 0.79 | 99.55 ± 0.79 | 100.00 ± 0.00 | 17.31 ± 5.92 |
| federated | ewc | order_3 | 40.96 ± 3.70 | 58.79 ± 3.70 | 0.00 ± 0.00 | 23.02 ± 6.58 |
| federated | fedprox_no_replay | order_1 | 33.33 ± 0.00 | 66.52 ± 0.04 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| federated | fedprox_no_replay | order_2 | 0.05 ± 0.14 | 99.85 ± 0.14 | 100.00 ± 0.00 | 22.17 ± 0.48 |
| federated | fedprox_no_replay | order_3 | 33.33 ± 0.00 | 66.41 ± 0.04 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| federated | joint | order_1 | 91.72 ± 0.14 | N/A | 77.07 ± 0.50 | 81.03 ± 2.80 |
| federated | joint | order_2 | 99.32 ± 0.14 | N/A | 76.65 ± 0.05 | 79.10 ± 2.64 |
| federated | joint | order_3 | 91.57 ± 0.09 | N/A | 76.73 ± 0.09 | 73.54 ± 2.20 |
| federated | no_replay | order_1 | 33.33 ± 0.00 | 66.49 ± 0.06 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| federated | no_replay | order_2 | 0.00 ± 0.00 | 99.93 ± 0.01 | 100.00 ± 0.00 | 22.22 ± 0.00 |
| federated | no_replay | order_3 | 33.33 ± 0.00 | 66.38 ± 0.03 | 0.00 ± 0.00 | 11.11 ± 0.00 |
| federated | protected_120 | order_1 | 82.82 ± 7.12 | 16.98 ± 7.11 | 77.72 ± 1.05 | 62.35 ± 10.63 |
| federated | protected_120 | order_2 | 65.41 ± 4.04 | 34.52 ± 4.04 | 96.73 ± 4.14 | 36.93 ± 7.16 |
| federated | protected_120 | order_3 | 92.03 ± 2.61 | 7.17 ± 2.94 | 79.75 ± 8.92 | 75.17 ± 1.07 |
| federated | protected_300 | order_1 | 93.60 ± 0.87 | 6.13 ± 0.90 | 89.58 ± 2.86 | 75.00 ± 0.94 |
| federated | protected_300 | order_2 | 83.99 ± 0.62 | 15.94 ± 0.62 | 100.00 ± 0.00 | 74.97 ± 3.25 |
| federated | protected_300 | order_3 | 96.14 ± 1.36 | 2.38 ± 1.70 | 93.77 ± 5.16 | 77.19 ± 1.21 |
| federated | protected_60 | order_1 | 73.34 ± 6.09 | 26.42 ± 6.10 | 77.42 ± 2.19 | 45.65 ± 10.49 |
| federated | protected_60 | order_2 | 55.94 ± 1.45 | 43.99 ± 1.45 | 96.85 ± 4.47 | 23.03 ± 4.47 |
| federated | protected_60 | order_3 | 89.24 ± 1.93 | 10.10 ± 2.24 | 73.92 ± 6.13 | 72.78 ± 2.14 |
| federated | uniform_120 | order_1 | 88.29 ± 5.49 | 11.48 ± 5.51 | 92.43 ± 2.38 | 66.04 ± 8.84 |
| federated | uniform_120 | order_2 | 66.19 ± 6.28 | 33.74 ± 6.28 | 97.68 ± 4.85 | 37.83 ± 12.02 |
| federated | uniform_120 | order_3 | 79.76 ± 7.60 | 19.93 ± 7.63 | 41.35 ± 23.11 | 70.93 ± 2.84 |
| federated | uniform_300 | order_1 | 92.47 ± 1.42 | 7.27 ± 1.43 | 85.60 ± 5.27 | 75.95 ± 2.18 |
| federated | uniform_300 | order_2 | 90.21 ± 1.82 | 9.72 ± 1.82 | 92.27 ± 10.31 | 74.76 ± 1.48 |
| federated | uniform_300 | order_3 | 89.89 ± 0.51 | 9.74 ± 0.54 | 71.50 ± 1.60 | 74.88 ± 1.60 |
| federated | uniform_60 | order_1 | 73.50 ± 5.68 | 26.26 ± 5.69 | 91.17 ± 2.19 | 43.63 ± 9.80 |
| federated | uniform_60 | order_2 | 52.84 ± 1.41 | 47.08 ± 1.41 | 100.00 ± 0.00 | 25.07 ± 5.40 |
| federated | uniform_60 | order_3 | 69.51 ± 6.84 | 30.24 ± 6.85 | 9.77 ± 20.72 | 67.82 ± 2.75 |

## original_type: complete mean ± SD tables


### federated

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| agem | 21.43 ± 3.03 | 61.34 ± 3.00 | 51.62 ± 6.26 | 24.37 ± 2.14 |
| balanced_rare_300 | 53.80 ± 0.18 | 27.61 ± 0.29 | 91.23 ± 0.53 | 53.78 ± 0.62 |
| balanced_rare_60 | 49.58 ± 1.97 | 33.08 ± 1.99 | 78.27 ± 5.01 | 52.41 ± 0.69 |
| class_balanced_120 | 50.53 ± 1.21 | 32.06 ± 1.22 | 78.83 ± 3.68 | 52.87 ± 1.06 |
| class_balanced_300 | 53.23 ± 1.04 | 28.40 ± 1.01 | 88.81 ± 2.69 | 53.87 ± 0.64 |
| class_balanced_60 | 47.68 ± 1.68 | 34.97 ± 1.67 | 72.25 ± 4.12 | 51.71 ± 0.72 |
| ewc | 3.33 ± 0.81 | 79.48 ± 0.81 | 33.33 ± 0.00 | 11.95 ± 1.63 |
| fedprox_no_replay | 0.02 ± 0.05 | 82.77 ± 0.12 | 33.33 ± 0.00 | 9.66 ± 0.15 |
| joint | 55.39 ± 0.11 | N/A | 77.46 ± 0.05 | 52.58 ± 1.06 |
| no_replay | 0.00 ± 0.00 | 82.76 ± 0.06 | 33.33 ± 0.00 | 9.70 ± 0.21 |
| protected_120 | 49.94 ± 2.71 | 31.53 ± 2.82 | 88.80 ± 2.28 | 37.83 ± 2.68 |
| protected_300 | 61.75 ± 0.44 | 19.84 ± 0.63 | 95.88 ± 0.97 | 49.17 ± 0.95 |
| protected_60 | 42.78 ± 2.52 | 38.80 ± 2.76 | 86.97 ± 2.57 | 30.85 ± 2.56 |
| uniform_120 | 48.09 ± 2.27 | 34.43 ± 2.19 | 80.43 ± 8.94 | 37.96 ± 2.00 |
| uniform_300 | 60.08 ± 0.62 | 21.53 ± 0.55 | 87.31 ± 1.66 | 49.06 ± 0.87 |
| uniform_60 | 35.31 ± 3.11 | 47.21 ± 3.09 | 67.46 ± 8.26 | 29.43 ± 1.91 |

### centralized

| Method | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- |
| agem | 29.89 ± 2.74 | 53.02 ± 2.73 | 50.40 ± 3.30 | 31.53 ± 1.88 |
| balanced_rare_300 | 55.36 ± 2.15 | 26.84 ± 2.18 | 91.48 ± 0.61 | 55.97 ± 0.30 |
| balanced_rare_60 | 55.19 ± 1.07 | 26.84 ± 1.11 | 89.79 ± 1.26 | 55.69 ± 0.56 |
| class_balanced_120 | 54.41 ± 2.22 | 27.74 ± 2.23 | 86.92 ± 3.29 | 55.56 ± 0.41 |
| class_balanced_300 | 52.88 ± 1.77 | 29.85 ± 1.70 | 84.21 ± 3.60 | 55.59 ± 0.34 |
| class_balanced_60 | 54.36 ± 1.79 | 27.77 ± 1.83 | 86.08 ± 1.67 | 55.35 ± 0.50 |
| ewc | 0.26 ± 0.43 | 82.67 ± 0.47 | 33.33 ± 0.00 | 9.61 ± 0.95 |
| fedprox_no_replay | 0.21 ± 0.32 | 82.53 ± 0.31 | 33.33 ± 0.00 | 9.82 ± 0.27 |
| joint | 63.51 ± 2.88 | N/A | 99.19 ± 0.40 | 57.65 ± 0.26 |
| no_replay | 0.00 ± 0.00 | 82.82 ± 0.11 | 33.33 ± 0.00 | 9.67 ± 0.25 |
| protected_120 | 56.54 ± 1.68 | 25.75 ± 1.66 | 93.97 ± 1.92 | 46.80 ± 1.84 |
| protected_300 | 63.87 ± 0.32 | 18.42 ± 0.33 | 98.27 ± 0.57 | 54.92 ± 0.90 |
| protected_60 | 51.61 ± 1.58 | 31.16 ± 1.63 | 95.78 ± 2.06 | 39.57 ± 2.50 |
| uniform_120 | 54.92 ± 1.95 | 27.51 ± 1.97 | 86.63 ± 2.22 | 46.74 ± 1.57 |
| uniform_300 | 62.81 ± 1.26 | 19.45 ± 1.43 | 94.87 ± 3.29 | 54.02 ± 1.43 |
| uniform_60 | 43.75 ± 2.18 | 38.94 ± 2.09 | 69.80 ± 6.21 | 38.68 ± 1.35 |

## original_type: all paired comparisons, including losses


### centralized, memory 60, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.83 | [+0.05, +1.61] | better |
| class_balanced_60 | forgetting | -0.93 | [-1.67, -0.19] | better |
| class_balanced_60 | slowloris_recall | +3.72 | [+2.04, +5.39] | better |
| class_balanced_60 | worst_client_macro_recall | +0.34 | [+0.10, +0.58] | better |
| protected_60 | old_task_accuracy | +3.58 | [+1.95, +5.21] | better |
| protected_60 | forgetting | -4.32 | [-6.00, -2.64] | better |
| protected_60 | slowloris_recall | -5.98 | [-7.15, -4.81] | worse |
| protected_60 | worst_client_macro_recall | +16.12 | [+14.38, +17.87] | better |

### centralized, memory 60, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.73 | [+0.49, +2.98] | better |
| class_balanced_60 | forgetting | -1.73 | [-2.98, -0.49] | better |
| class_balanced_60 | slowloris_recall | +5.02 | [+1.36, +8.67] | better |
| class_balanced_60 | worst_client_macro_recall | +0.28 | [-0.25, +0.80] | not significant |
| protected_60 | old_task_accuracy | -2.79 | [-4.72, -0.86] | worse |
| protected_60 | forgetting | +2.53 | [+0.44, +4.61] | worse |
| protected_60 | slowloris_recall | -19.03 | [-21.27, -16.80] | worse |
| protected_60 | worst_client_macro_recall | +7.15 | [+4.42, +9.88] | better |

### centralized, memory 60, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_60 | old_task_accuracy | +11.36 | [+8.01, +14.70] | better |
| protected_60 | forgetting | -11.59 | [-15.06, -8.12] | better |
| protected_60 | slowloris_recall | -0.42 | [-0.89, +0.05] | not significant |
| protected_60 | worst_client_macro_recall | +35.20 | [+30.84, +39.57] | better |

### centralized, memory 60, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.75 | [-1.54, +3.05] | not significant |
| class_balanced_60 | forgetting | -1.06 | [-3.13, +1.01] | not significant |
| class_balanced_60 | slowloris_recall | +6.13 | [+1.55, +10.71] | better |
| class_balanced_60 | worst_client_macro_recall | +0.74 | [-0.01, +1.48] | not significant |
| protected_60 | old_task_accuracy | +2.17 | [+0.31, +4.03] | better |
| protected_60 | forgetting | -3.90 | [-5.67, -2.14] | better |
| protected_60 | slowloris_recall | +1.50 | [-2.57, +5.57] | not significant |
| protected_60 | worst_client_macro_recall | +6.02 | [+4.94, +7.11] | better |

### centralized, memory 300, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +2.48 | [+1.57, +3.38] | better |
| class_balanced_300 | forgetting | -3.01 | [-3.94, -2.08] | better |
| class_balanced_300 | slowloris_recall | +7.27 | [+4.76, +9.79] | better |
| class_balanced_300 | worst_client_macro_recall | +0.37 | [+0.13, +0.61] | better |
| protected_300 | old_task_accuracy | -8.51 | [-9.95, -7.07] | worse |
| protected_300 | forgetting | +8.41 | [+6.94, +9.88] | worse |
| protected_300 | slowloris_recall | -6.78 | [-7.29, -6.28] | worse |
| protected_300 | worst_client_macro_recall | +1.05 | [+0.27, +1.83] | better |

### centralized, memory 300, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +2.87 | [+0.23, +5.51] | better |
| class_balanced_300 | forgetting | -2.87 | [-5.51, -0.23] | better |
| class_balanced_300 | slowloris_recall | +9.03 | [+1.13, +16.94] | better |
| class_balanced_300 | worst_client_macro_recall | +0.55 | [-0.11, +1.21] | not significant |
| protected_300 | old_task_accuracy | -6.59 | [-7.11, -6.07] | worse |
| protected_300 | forgetting | +6.47 | [+5.92, +7.01] | worse |
| protected_300 | slowloris_recall | -20.12 | [-21.69, -18.54] | worse |
| protected_300 | worst_client_macro_recall | +0.08 | [-1.91, +2.08] | not significant |

### centralized, memory 300, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | old_task_accuracy | -19.16 | [-23.21, -15.12] | worse |
| protected_300 | forgetting | +19.25 | [+15.30, +23.20] | worse |
| protected_300 | slowloris_recall | +0.20 | [+0.01, +0.39] | better |
| protected_300 | worst_client_macro_recall | +0.65 | [+0.28, +1.02] | better |

### centralized, memory 300, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +4.56 | [+2.06, +7.06] | better |
| class_balanced_300 | forgetting | -6.17 | [-8.78, -3.56] | better |
| class_balanced_300 | slowloris_recall | +12.78 | [+5.42, +20.14] | better |
| class_balanced_300 | worst_client_macro_recall | +0.57 | [-0.02, +1.17] | not significant |
| protected_300 | old_task_accuracy | +0.23 | [-0.13, +0.58] | not significant |
| protected_300 | forgetting | -0.48 | [-0.99, +0.02] | not significant |
| protected_300 | slowloris_recall | -0.43 | [-0.95, +0.09] | not significant |
| protected_300 | worst_client_macro_recall | +2.42 | [+0.94, +3.89] | better |

### federated, memory 60, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.90 | [+0.37, +3.43] | better |
| class_balanced_60 | forgetting | -1.90 | [-3.41, -0.38] | better |
| class_balanced_60 | slowloris_recall | +6.02 | [+1.51, +10.54] | better |
| class_balanced_60 | worst_client_macro_recall | +0.70 | [-0.04, +1.45] | not significant |
| protected_60 | old_task_accuracy | +6.80 | [+4.58, +9.02] | better |
| protected_60 | forgetting | -5.72 | [-8.00, -3.44] | better |
| protected_60 | slowloris_recall | -8.70 | [-12.62, -4.78] | worse |
| protected_60 | worst_client_macro_recall | +21.57 | [+19.89, +23.24] | better |

### federated, memory 60, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +3.96 | [+1.18, +6.75] | better |
| class_balanced_60 | forgetting | -3.96 | [-6.75, -1.18] | better |
| class_balanced_60 | slowloris_recall | +12.12 | [+3.28, +20.95] | better |
| class_balanced_60 | worst_client_macro_recall | +1.77 | [+0.28, +3.26] | better |
| protected_60 | old_task_accuracy | +13.34 | [+8.64, +18.04] | better |
| protected_60 | forgetting | -13.38 | [-18.07, -8.68] | better |
| protected_60 | slowloris_recall | -14.32 | [-23.64, -4.99] | worse |
| protected_60 | worst_client_macro_recall | +24.07 | [+19.47, +28.66] | better |

### federated, memory 60, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_60 | old_task_accuracy | +11.15 | [+8.85, +13.45] | better |
| protected_60 | forgetting | -10.97 | [-13.22, -8.71] | better |
| protected_60 | slowloris_recall | +1.00 | [+0.49, +1.51] | better |
| protected_60 | worst_client_macro_recall | +38.74 | [+37.12, +40.36] | better |

### federated, memory 60, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_60 | old_task_accuracy | +1.74 | [-0.63, +4.10] | not significant |
| class_balanced_60 | forgetting | -1.73 | [-4.05, +0.59] | not significant |
| class_balanced_60 | slowloris_recall | +5.95 | [-0.49, +12.39] | not significant |
| class_balanced_60 | worst_client_macro_recall | +0.34 | [-1.38, +2.07] | not significant |
| protected_60 | old_task_accuracy | -4.10 | [-6.13, -2.07] | worse |
| protected_60 | forgetting | +7.18 | [+4.52, +9.84] | worse |
| protected_60 | slowloris_recall | -12.78 | [-18.23, -7.34] | worse |
| protected_60 | worst_client_macro_recall | +1.89 | [+0.13, +3.66] | better |

### federated, memory 300, averaged

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.57 | [-0.11, +1.26] | not significant |
| class_balanced_300 | forgetting | -0.79 | [-1.54, -0.04] | better |
| class_balanced_300 | slowloris_recall | +2.42 | [+0.56, +4.28] | better |
| class_balanced_300 | worst_client_macro_recall | -0.09 | [-0.31, +0.13] | not significant |
| protected_300 | old_task_accuracy | -7.95 | [-8.24, -7.65] | worse |
| protected_300 | forgetting | +7.77 | [+7.34, +8.21] | worse |
| protected_300 | slowloris_recall | -4.65 | [-5.50, -3.80] | worse |
| protected_300 | worst_client_macro_recall | +4.61 | [+4.00, +5.21] | better |

### federated, memory 300, order_1

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.25 | [+0.01, +0.49] | better |
| class_balanced_300 | forgetting | -0.25 | [-0.49, -0.01] | better |
| class_balanced_300 | slowloris_recall | +0.82 | [+0.13, +1.50] | better |
| class_balanced_300 | worst_client_macro_recall | -0.14 | [-0.63, +0.36] | not significant |
| protected_300 | old_task_accuracy | -4.05 | [-4.69, -3.41] | worse |
| protected_300 | forgetting | +4.03 | [+3.36, +4.69] | worse |
| protected_300 | slowloris_recall | -13.25 | [-15.18, -11.32] | worse |
| protected_300 | worst_client_macro_recall | +6.14 | [+5.37, +6.90] | better |

### federated, memory 300, order_2

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | forgetting | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| class_balanced_300 | worst_client_macro_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | old_task_accuracy | -19.85 | [-20.41, -19.28] | worse |
| protected_300 | forgetting | +19.86 | [+19.17, +20.55] | worse |
| protected_300 | slowloris_recall | +0.00 | [+0.00, +0.00] | not significant |
| protected_300 | worst_client_macro_recall | +5.50 | [+4.20, +6.80] | better |

### federated, memory 300, order_3

| Baseline | Metric | Difference | 95% interval | Outcome |
| --- | --- | --- | --- | --- |
| class_balanced_300 | old_task_accuracy | +1.47 | [-0.68, +3.62] | not significant |
| class_balanced_300 | forgetting | -2.12 | [-4.44, +0.20] | not significant |
| class_balanced_300 | slowloris_recall | +6.45 | [+0.74, +12.16] | better |
| class_balanced_300 | worst_client_macro_recall | -0.14 | [-1.07, +0.78] | not significant |
| protected_300 | old_task_accuracy | +0.05 | [-0.20, +0.31] | not significant |
| protected_300 | forgetting | -0.57 | [-1.40, +0.25] | not significant |
| protected_300 | slowloris_recall | -0.70 | [-1.66, +0.26] | not significant |
| protected_300 | worst_client_macro_recall | +2.19 | [+0.88, +3.49] | better |

## original_type: every order, mean ± SD

| Environment | Method | Order | Old accuracy | Forgetting | Slowloris | Worst client |
| --- | --- | --- | --- | --- | --- | --- |
| centralized | agem | order_1 | 38.27 ± 5.18 | 37.07 ± 5.21 | 48.15 ± 1.09 | 34.87 ± 5.66 |
| centralized | agem | order_2 | 17.67 ± 5.60 | 55.91 ± 5.54 | 100.00 ± 0.00 | 16.44 ± 1.53 |
| centralized | agem | order_3 | 33.72 ± 3.28 | 66.08 ± 3.28 | 3.05 ± 9.64 | 43.29 ± 1.50 |
| centralized | balanced_rare_300 | order_1 | 58.67 ± 0.60 | 16.56 ± 0.76 | 76.63 ± 1.63 | 55.58 ± 0.30 |
| centralized | balanced_rare_300 | order_2 | 41.33 ± 6.06 | 32.25 ± 5.98 | 100.00 ± 0.00 | 55.09 ± 0.55 |
| centralized | balanced_rare_300 | order_3 | 66.07 ± 0.42 | 31.69 ± 0.86 | 97.82 ± 0.68 | 57.23 ± 0.47 |
| centralized | balanced_rare_60 | order_1 | 58.96 ± 1.18 | 16.07 ± 1.18 | 77.12 ± 3.03 | 54.60 ± 1.58 |
| centralized | balanced_rare_60 | order_2 | 41.31 ± 2.46 | 32.06 ± 2.37 | 99.55 ± 0.62 | 55.69 ± 0.75 |
| centralized | balanced_rare_60 | order_3 | 65.31 ± 0.92 | 32.38 ± 1.41 | 92.72 ± 1.99 | 56.78 ± 0.67 |
| centralized | class_balanced_120 | order_1 | 55.85 ± 3.18 | 19.41 ± 3.20 | 67.98 ± 9.62 | 55.10 ± 0.76 |
| centralized | class_balanced_120 | order_2 | 41.20 ± 3.63 | 32.29 ± 3.62 | 100.00 ± 0.00 | 55.00 ± 0.55 |
| centralized | class_balanced_120 | order_3 | 66.17 ± 3.94 | 31.51 ± 4.28 | 92.77 ± 5.93 | 56.58 ± 0.64 |
| centralized | class_balanced_300 | order_1 | 55.80 ± 3.71 | 19.43 ± 3.71 | 67.60 ± 11.21 | 55.03 ± 0.87 |
| centralized | class_balanced_300 | order_2 | 41.33 ± 6.06 | 32.25 ± 5.98 | 100.00 ± 0.00 | 55.09 ± 0.55 |
| centralized | class_balanced_300 | order_3 | 61.51 ± 3.55 | 37.86 ± 3.50 | 85.03 ± 10.65 | 56.66 ± 0.93 |
| centralized | class_balanced_60 | order_1 | 57.22 ± 1.45 | 17.80 ± 1.61 | 72.10 ± 4.24 | 54.33 ± 1.64 |
| centralized | class_balanced_60 | order_2 | 41.31 ± 2.46 | 32.06 ± 2.37 | 99.55 ± 0.62 | 55.69 ± 0.75 |
| centralized | class_balanced_60 | order_3 | 64.55 ± 3.67 | 33.44 ± 3.66 | 86.58 ± 5.19 | 56.05 ± 0.65 |
| centralized | ewc | order_1 | 0.00 ± 0.00 | 75.28 ± 0.27 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| centralized | ewc | order_2 | 0.06 ± 0.19 | 73.65 ± 0.36 | 100.00 ± 0.00 | 13.62 ± 2.28 |
| centralized | ewc | order_3 | 0.73 ± 1.31 | 99.09 ± 1.31 | 0.00 ± 0.00 | 8.06 ± 1.42 |
| centralized | fedprox_no_replay | order_1 | 0.00 ± 0.00 | 75.24 ± 0.21 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| centralized | fedprox_no_replay | order_2 | 0.39 ± 0.81 | 72.97 ± 0.80 | 100.00 ± 0.00 | 14.60 ± 0.65 |
| centralized | fedprox_no_replay | order_3 | 0.25 ± 0.71 | 99.38 ± 0.77 | 0.00 ± 0.00 | 7.71 ± 0.72 |
| centralized | joint | order_1 | 73.47 ± 0.41 | N/A | 98.38 ± 1.14 | 58.74 ± 0.68 |
| centralized | joint | order_2 | 44.33 ± 3.44 | N/A | 99.90 ± 0.26 | 56.97 ± 0.66 |
| centralized | joint | order_3 | 72.73 ± 5.81 | N/A | 99.28 ± 0.24 | 57.25 ± 0.49 |
| centralized | no_replay | order_1 | 0.00 ± 0.00 | 75.10 ± 0.20 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| centralized | no_replay | order_2 | 0.00 ± 0.00 | 73.55 ± 0.26 | 100.00 ± 0.00 | 14.29 ± 0.00 |
| centralized | no_replay | order_3 | 0.00 ± 0.00 | 99.82 ± 0.06 | 0.00 ± 0.00 | 7.58 ± 0.75 |
| centralized | protected_120 | order_1 | 61.51 ± 2.27 | 13.78 ± 2.34 | 86.05 ± 6.53 | 52.18 ± 2.83 |
| centralized | protected_120 | order_2 | 43.24 ± 3.83 | 30.15 ± 4.00 | 99.63 ± 0.60 | 35.49 ± 4.02 |
| centralized | protected_120 | order_3 | 64.88 ± 0.46 | 33.31 ± 1.07 | 96.22 ± 1.31 | 52.72 ± 2.38 |
| centralized | protected_300 | order_1 | 65.26 ± 0.67 | 10.09 ± 0.71 | 96.75 ± 2.14 | 55.49 ± 2.75 |
| centralized | protected_300 | order_2 | 60.49 ± 0.73 | 13.00 ± 0.76 | 99.80 ± 0.27 | 54.44 ± 0.45 |
| centralized | protected_300 | order_3 | 65.85 ± 0.29 | 32.17 ± 0.41 | 98.25 ± 0.46 | 54.82 ± 1.96 |
| centralized | protected_60 | order_1 | 61.75 ± 2.28 | 13.54 ± 2.35 | 96.15 ± 1.59 | 47.46 ± 3.62 |
| centralized | protected_60 | order_2 | 29.95 ± 3.82 | 43.65 ± 4.02 | 99.97 ± 0.11 | 20.48 ± 5.67 |
| centralized | protected_60 | order_3 | 63.14 ± 2.03 | 36.29 ± 2.08 | 91.22 ± 6.25 | 50.76 ± 1.30 |
| centralized | uniform_120 | order_1 | 64.94 ± 0.48 | 10.35 ± 0.49 | 96.18 ± 1.53 | 52.11 ± 1.98 |
| centralized | uniform_120 | order_2 | 45.26 ± 6.32 | 28.31 ± 6.33 | 100.00 ± 0.00 | 37.55 ± 6.17 |
| centralized | uniform_120 | order_3 | 54.57 ± 1.94 | 43.87 ± 2.14 | 63.72 ± 6.29 | 50.56 ± 1.79 |
| centralized | uniform_300 | order_1 | 64.69 ± 1.47 | 10.65 ± 1.52 | 94.90 ± 4.45 | 54.93 ± 2.73 |
| centralized | uniform_300 | order_2 | 60.48 ± 0.73 | 13.01 ± 0.73 | 99.63 ± 0.69 | 53.29 ± 2.95 |
| centralized | uniform_300 | order_3 | 63.26 ± 2.98 | 34.68 ± 3.38 | 90.07 ± 8.47 | 53.85 ± 2.33 |
| centralized | uniform_60 | order_1 | 63.55 ± 0.98 | 11.75 ± 0.97 | 96.68 ± 1.11 | 49.33 ± 1.59 |
| centralized | uniform_60 | order_2 | 30.12 ± 3.06 | 43.43 ± 3.13 | 99.90 ± 0.32 | 21.39 ± 3.58 |
| centralized | uniform_60 | order_3 | 37.59 ± 6.34 | 61.65 ± 6.29 | 12.82 ± 18.96 | 45.32 ± 1.67 |
| federated | agem | order_1 | 19.69 ± 3.01 | 55.47 ± 2.87 | 46.05 ± 1.15 | 15.52 ± 3.38 |
| federated | agem | order_2 | 8.88 ± 5.96 | 64.54 ± 5.95 | 100.00 ± 0.00 | 13.36 ± 4.19 |
| federated | agem | order_3 | 35.73 ± 6.14 | 64.02 ± 6.15 | 8.80 ± 18.55 | 44.23 ± 2.02 |
| federated | balanced_rare_300 | order_1 | 58.79 ± 0.38 | 16.27 ± 0.34 | 76.75 ± 1.09 | 54.94 ± 1.12 |
| federated | balanced_rare_300 | order_2 | 37.17 ± 0.44 | 36.29 ± 0.53 | 100.00 ± 0.00 | 53.53 ± 0.24 |
| federated | balanced_rare_300 | order_3 | 65.44 ± 0.33 | 30.27 ± 0.70 | 96.93 ± 1.11 | 52.87 ± 1.54 |
| federated | balanced_rare_60 | order_1 | 54.18 ± 3.78 | 20.90 ± 3.78 | 63.10 ± 11.96 | 53.56 ± 1.47 |
| federated | balanced_rare_60 | order_2 | 38.80 ± 2.90 | 34.66 ± 2.85 | 100.00 ± 0.00 | 53.49 ± 1.09 |
| federated | balanced_rare_60 | order_3 | 55.75 ± 2.58 | 43.67 ± 2.64 | 71.72 ± 5.90 | 50.19 ± 2.12 |
| federated | class_balanced_120 | order_1 | 55.37 ± 3.59 | 19.67 ± 3.59 | 66.62 ± 10.77 | 53.47 ± 1.71 |
| federated | class_balanced_120 | order_2 | 39.96 ± 1.45 | 33.46 ± 1.50 | 99.90 ± 0.16 | 54.21 ± 1.57 |
| federated | class_balanced_120 | order_3 | 56.24 ± 0.44 | 43.06 ± 0.57 | 69.98 ± 1.39 | 50.93 ± 1.21 |
| federated | class_balanced_300 | order_1 | 58.54 ± 0.25 | 16.52 ± 0.33 | 75.93 ± 0.68 | 55.07 ± 1.04 |
| federated | class_balanced_300 | order_2 | 37.17 ± 0.44 | 36.29 ± 0.53 | 100.00 ± 0.00 | 53.53 ± 0.24 |
| federated | class_balanced_300 | order_3 | 63.97 ± 3.04 | 32.39 ± 3.05 | 90.48 ± 8.09 | 53.01 ± 1.86 |
| federated | class_balanced_60 | order_1 | 50.21 ± 2.76 | 24.87 ± 2.70 | 50.98 ± 8.66 | 51.79 ± 1.81 |
| federated | class_balanced_60 | order_2 | 38.80 ± 2.90 | 34.66 ± 2.85 | 100.00 ± 0.00 | 53.49 ± 1.09 |
| federated | class_balanced_60 | order_3 | 54.01 ± 2.74 | 45.39 ± 2.71 | 65.77 ± 7.40 | 49.85 ± 1.41 |
| federated | ewc | order_1 | 0.00 ± 0.00 | 75.20 ± 0.15 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| federated | ewc | order_2 | 0.61 ± 1.00 | 72.86 ± 0.98 | 100.00 ± 0.00 | 11.39 ± 3.59 |
| federated | ewc | order_3 | 9.38 ± 2.22 | 90.37 ± 2.22 | 0.00 ± 0.00 | 17.31 ± 2.60 |
| federated | fedprox_no_replay | order_1 | 0.00 ± 0.00 | 75.14 ± 0.22 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| federated | fedprox_no_replay | order_2 | 0.05 ± 0.14 | 73.44 ± 0.23 | 100.00 ± 0.00 | 14.25 ± 0.31 |
| federated | fedprox_no_replay | order_3 | 0.00 ± 0.00 | 99.74 ± 0.04 | 0.00 ± 0.00 | 7.58 ± 0.33 |
| federated | joint | order_1 | 67.37 ± 0.38 | N/A | 78.97 ± 0.13 | 55.92 ± 1.63 |
| federated | joint | order_2 | 40.17 ± 0.19 | N/A | 76.65 ± 0.05 | 53.12 ± 2.12 |
| federated | joint | order_3 | 58.63 ± 0.05 | N/A | 76.77 ± 0.09 | 48.70 ± 1.76 |
| federated | no_replay | order_1 | 0.00 ± 0.00 | 75.19 ± 0.14 | 0.00 ± 0.00 | 7.14 ± 0.00 |
| federated | no_replay | order_2 | 0.00 ± 0.00 | 73.37 ± 0.13 | 100.00 ± 0.00 | 14.29 ± 0.00 |
| federated | no_replay | order_3 | 0.00 ± 0.00 | 99.71 ± 0.03 | 0.00 ± 0.00 | 7.68 ± 0.62 |
| federated | protected_120 | order_1 | 50.48 ± 7.15 | 24.67 ± 7.22 | 77.72 ± 1.05 | 40.46 ± 6.58 |
| federated | protected_120 | order_2 | 36.35 ± 4.45 | 37.12 ± 4.46 | 98.78 ± 1.84 | 23.68 ± 4.56 |
| federated | protected_120 | order_3 | 63.00 ± 1.85 | 32.80 ± 1.74 | 89.90 ± 6.46 | 49.36 ± 1.02 |
| federated | protected_300 | order_1 | 62.84 ± 0.99 | 12.24 ± 0.96 | 90.00 ± 2.95 | 48.80 ± 0.13 |
| federated | protected_300 | order_2 | 57.02 ± 0.60 | 16.43 ± 0.65 | 100.00 ± 0.00 | 48.03 ± 1.85 |
| federated | protected_300 | order_3 | 65.38 ± 0.18 | 30.85 ± 0.93 | 97.63 ± 0.59 | 50.68 ± 1.66 |
| federated | protected_60 | order_1 | 40.84 ± 6.03 | 34.28 ± 6.00 | 77.42 ± 2.19 | 29.49 ± 6.72 |
| federated | protected_60 | order_2 | 27.65 ± 1.03 | 45.63 ± 0.96 | 99.00 ± 0.71 | 14.75 ± 2.30 |
| federated | protected_60 | order_3 | 59.85 ± 2.45 | 36.48 ± 3.56 | 84.50 ± 6.66 | 48.30 ± 2.20 |
| federated | uniform_120 | order_1 | 57.85 ± 5.43 | 17.29 ± 5.51 | 92.43 ± 2.38 | 42.82 ± 5.67 |
| federated | uniform_120 | order_2 | 37.31 ± 6.81 | 36.05 ± 6.86 | 99.53 ± 0.92 | 24.22 ± 7.45 |
| federated | uniform_120 | order_3 | 49.11 ± 9.13 | 49.94 ± 8.86 | 49.33 ± 27.48 | 46.82 ± 2.84 |
| federated | uniform_300 | order_1 | 61.95 ± 1.60 | 13.15 ± 1.59 | 87.32 ± 4.94 | 49.30 ± 1.84 |
| federated | uniform_300 | order_2 | 60.05 ± 0.86 | 13.30 ± 0.78 | 99.52 ± 0.61 | 48.29 ± 0.93 |
| federated | uniform_300 | order_3 | 58.23 ± 1.55 | 38.14 ± 1.80 | 75.08 ± 4.57 | 49.60 ± 1.43 |
| federated | uniform_60 | order_1 | 42.85 ± 5.63 | 32.26 ± 5.58 | 91.17 ± 2.19 | 28.51 ± 6.52 |
| federated | uniform_60 | order_2 | 26.43 ± 1.34 | 46.91 ± 1.30 | 100.00 ± 0.00 | 15.64 ± 2.82 |
| federated | uniform_60 | order_3 | 36.66 ± 8.03 | 62.45 ± 8.25 | 11.22 ± 24.32 | 44.13 ± 2.34 |

## Calibration selections

Selection criterion remained mean original-type calibration macro recall over checkpoints, as in prior methods. Evaluation scores did not select settings.

| Order | Environment | Memory | Rare quota | Replay fraction |
| --- | --- | --- | --- | --- |
| order_1 | federated | 60 | 0.1 | 0.5 |
| order_1 | federated | 300 | 0.1 | 0.5 |
| order_1 | centralized | 60 | 0.1 | 0.5 |
| order_1 | centralized | 300 | 0.2 | 0.25 |
| order_2 | federated | 60 | 0.1 | 0.25 |
| order_2 | federated | 300 | 0.1 | 0.25 |
| order_2 | centralized | 60 | 0.1 | 0.5 |
| order_2 | centralized | 300 | 0.1 | 0.25 |
| order_3 | federated | 60 | 0.1 | 0.25 |
| order_3 | federated | 300 | 0.1 | 0.5 |
| order_3 | centralized | 60 | 0.2 | 0.5 |
| order_3 | centralized | 300 | 0.2 | 0.5 |

## Requested significance pattern

This screen requires significantly higher Slowloris recall than class-balanced, and no significantly lower old accuracy or worst-client score. It does not establish equivalence/non-inferiority. Averaging all three orders is distinct from meeting it within each order.

| Score space | Environment | Memory | Order | Screen met |
| --- | --- | --- | --- | --- |
| merged_scans | centralized | 60 | averaged | True |
| merged_scans | centralized | 60 | order_1 | True |
| merged_scans | centralized | 60 | order_2 | False |
| merged_scans | centralized | 60 | order_3 | True |
| merged_scans | centralized | 300 | averaged | True |
| merged_scans | centralized | 300 | order_1 | True |
| merged_scans | centralized | 300 | order_2 | False |
| merged_scans | centralized | 300 | order_3 | True |
| merged_scans | federated | 60 | averaged | True |
| merged_scans | federated | 60 | order_1 | True |
| merged_scans | federated | 60 | order_2 | False |
| merged_scans | federated | 60 | order_3 | False |
| merged_scans | federated | 300 | averaged | True |
| merged_scans | federated | 300 | order_1 | True |
| merged_scans | federated | 300 | order_2 | False |
| merged_scans | federated | 300 | order_3 | True |
| original_type | centralized | 60 | averaged | True |
| original_type | centralized | 60 | order_1 | True |
| original_type | centralized | 60 | order_2 | False |
| original_type | centralized | 60 | order_3 | True |
| original_type | centralized | 300 | averaged | True |
| original_type | centralized | 300 | order_1 | True |
| original_type | centralized | 300 | order_2 | False |
| original_type | centralized | 300 | order_3 | True |
| original_type | federated | 60 | averaged | True |
| original_type | federated | 60 | order_1 | True |
| original_type | federated | 60 | order_2 | False |
| original_type | federated | 60 | order_3 | False |
| original_type | federated | 300 | averaged | True |
| original_type | federated | 300 | order_1 | True |
| original_type | federated | 300 | order_2 | False |
| original_type | federated | 300 | order_3 | True |

## Sensitivity: significance conclusions that differ

Broad trade-off agreement does not mean every statistical conclusion matches.

| Environment | Memory | Order | Baseline | Metric | Merged | Exact type |
| --- | --- | --- | --- | --- | --- | --- |
| federated | 60 | order_2 | protected_60 | slowloris_recall | not significant | better |
| federated | 60 | order_3 | protected_60 | old_task_accuracy | not significant | worse |
| federated | 60 | order_3 | protected_60 | forgetting | not significant | worse |
| federated | 60 | order_3 | protected_60 | worst_client_macro_recall | not significant | better |
| federated | 300 | averaged | class_balanced_300 | old_task_accuracy | better | not significant |
| federated | 300 | averaged | class_balanced_300 | worst_client_macro_recall | better | not significant |
| federated | 300 | order_1 | class_balanced_300 | old_task_accuracy | not significant | better |
| federated | 300 | order_1 | class_balanced_300 | forgetting | not significant | better |
| federated | 300 | order_3 | class_balanced_300 | old_task_accuracy | better | not significant |
| federated | 300 | order_3 | class_balanced_300 | forgetting | better | not significant |
| federated | 300 | order_3 | class_balanced_300 | worst_client_macro_recall | better | not significant |
| centralized | 60 | order_3 | class_balanced_60 | old_task_accuracy | better | not significant |
| centralized | 60 | order_3 | class_balanced_60 | forgetting | better | not significant |
| centralized | 60 | order_3 | class_balanced_60 | worst_client_macro_recall | better | not significant |
| centralized | 60 | averaged | protected_60 | slowloris_recall | not significant | worse |
| centralized | 60 | order_1 | protected_60 | forgetting | not significant | worse |
| centralized | 60 | order_2 | protected_60 | slowloris_recall | worse | not significant |
| centralized | 60 | order_3 | protected_60 | slowloris_recall | better | not significant |
| centralized | 300 | order_3 | class_balanced_300 | worst_client_macro_recall | better | not significant |

## Audit and interpretation

The design and training-source hashes were recorded before calibration. All 48 calibrations completed and selected settings were recorded before any new evaluation. No tuning followed evaluation. Raw predictions, final models, memory partitions and training logs are retained separately. Previous baselines and their selected settings were reused without retraining. Paired differences below 1e-12 in absolute value are treated as numerical zero, preventing floating-point ties in near-zero forgetting from being labeled significant. No training result or selected setting was changed.

Memory is examples, not model parameters: 60 or 300 per client; centralized total 300 or 1500. Rare reservation is a minimum share, not a ceiling; the balanced remainder includes rare types and benign. Within the rare group, the unchanged feasible class-balanced allocator is used.

See paired_intervals.csv, federation_interactions.csv, per_order_summary.csv and new_per_client_metrics.csv for machine-readable evidence. No fragmentation interpretation or non-inferiority claim is warranted. No manuscript was generated.
