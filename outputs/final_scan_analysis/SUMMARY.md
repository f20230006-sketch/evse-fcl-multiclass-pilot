# Final checks: short supervisor summary

17 October 2026 | All table values are percentages; comparisons are percentage points.

## 1. What was done

- Trained a scan-only Random Forest to test whether six scan types can be distinguished.
- Re-scored all 840 saved runs with the six scan probabilities summed into one Scan class; no MLP retraining.
- Compared Slowloris and ICMP fragmentation separately, federated versus centralized, and examined the rare-heavy and benign-starved clients.
- Reconstructed the 33.33% rare-recall result from class counts and attack orders.

## 2. Main results table

Merged-Scan scores, federated setting, final checkpoint. Mean ± SD over ten seed averages across three orders; replay capacity 60 per client. Old accuracy refers to original old-task cohorts. Worst-client score is supported-class macro recall.

| Method | Old accuracy | Forgetting | Rare recall | Worst-client score |
|---|---|---|---|---|
| No replay | 22.22 ± 0.00 | 77.60 ± 0.02 | 33.33 ± 0.00 | 14.81 ± 0.00 |
| Uniform | 65.29 ± 2.92 | 34.53 ± 2.93 | 66.70 ± 6.94 | 45.50 ± 2.86 |
| Class-balanced | 83.99 ± 1.44 | 15.77 ± 1.42 | 71.41 ± 4.15 | 77.97 ± 1.05 |
| Protected | 72.84 ± 2.25 | 26.84 ± 2.29 | 82.28 ± 2.36 | 47.15 ± 3.82 |
| EWC | 24.89 ± 1.30 | 74.95 ± 1.30 | 33.31 ± 0.03 | 17.15 ± 3.56 |
| A-GEM | 46.03 ± 4.58 | 53.80 ± 4.58 | 50.12 ± 4.65 | 37.12 ± 3.29 |
| Joint | 94.20 ± 0.07 | N/A | 76.25 ± 0.21 | 77.89 ± 1.48 |

Memory sweep: old accuracy / rare recall. Size is per client; centralized totals are five times larger.

| Memory | Uniform | Class-balanced | Protected |
|---|---|---|---|
| 60 | 65.29 / 66.70 | 83.99 / 71.41 | 72.84 / 82.28 |
| 120 | 78.08 / 76.80 | 88.24 / 77.92 | 80.09 / 84.30 |
| 300 | 90.85 / 82.72 | 88.26 / 83.20 | 91.24 / 93.95 |

## 3. Key comparisons

- Protected − uniform: old accuracy +7.55 [4.88, 10.22]; significant. At memory 300: +0.39 [-0.03, 0.80]; not significant.
- Protected − class-balanced: old accuracy -11.15 [-13.31, -8.99]; significant; rare recall +10.87 [8.78, 12.95]; significant.
- Federated − centralized difference in protected-over-uniform old-accuracy improvement: +1.49 [-1.68, 4.66]; not significant.

## 4. What this means

- Random Forest accuracy is 34.25% ± 0.14% versus 16.67% chance (100% fitting accuracy). The six scans are not shown to be indistinguishable; merged results are an alternative view.
- At memory 60, protected replay improves merged rare recall over class-balanced replay but gives lower old accuracy and worst-client score. There is no supported extra overall retention benefit from federation.
- Federated training shows large rare-type deficits under joint training (table below). Protection does not narrow the gap more than uniform at memory 60. For Slowloris at memory 300, extra gap reduction: +5.17 [2.66, 7.68]; significant (percentage points; exploratory, unadjusted for multiple comparisons).

Original type-level rare recall (federated / centralized), memory 60 for replay:

| Method | Slowloris | ICMP fragmentation |
|---|---|---|
| Joint | 77.46 / 99.19 | 10.00 / 68.67 |
| Uniform | 67.46 / 69.80 | 33.33 / 35.33 |
| Class-balanced | 72.25 / 86.08 | 53.33 / 64.67 |
| Protected | 86.97 / 95.78 | 28.00 / 36.00 |

## 5. Problems or surprises

- ICMP fragmentation has only 5 test examples, versus 600 Slowloris examples. Benign test support remains 16; benign-starved false alarm rate is undefined.
- The original rare metric is (correct Slowloris + correct ICMP fragmentation) / 605. Federated no replay is 0%, 100%, 0% across orders, averaging 33.33%. Both types are correct only when rare attacks come last; neither is always correct across orders. EWC is 33.31% ± 0.03%, not exactly 33.33% ± 0.00%.
- Merged scores retain original old-task cohorts and type-level replay policies. Coarsening changes task overlap; it is not evidence that forgetting was fixed. Intervals describe training randomness on one split, not new independent captures.

## 6. Questions for the supervisor

- Given the above-chance Random Forest result, should exact attack types remain primary and merged-Scan scores be a sensitivity analysis?
- Should the letter emphasize the retention/rare-recall trade-off, with the Slowloris federation interaction labeled exploratory? No further experiments are proposed.
