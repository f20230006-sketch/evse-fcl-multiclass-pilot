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
