# Final balanced + rare experiment: results summary

26 October 2026 | Values: percentages; differences: percentage points.

## 1. What was done

- Added balanced + rare replay at memories 60 and 300 per client, with no separate benign quota.
- Selected one of four fixed quota/replay configurations on calibration data, then ran ten seeds, three orders and both training settings (48 calibration fits; 120 evaluations).
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
