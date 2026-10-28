# CBRS baseline comparison - 28 October 2026

## What was done

- Implemented published CBRS population, including persistent full-class flags and within-class reservoir replacement.
- Original split 42, memory 60/client (300 pooled), same 64/32 MLP, three orders, ten training seeds, federated and centralized.
- Calibrated only replay fraction 0.25/0.50 using the unchanged calibration criterion; all 12 calibration fits preceded all 60 evaluations.
- Added CBRS to the main table and shortened the manuscript to four pages with consistent RBR naming.

## Main results

Federated merged-Scan final scores, original split; percentages, mean +/- SD over ten seed averages of three orders.

| Method | Old accuracy | Forgetting | Slowloris | Worst-client |
|---|---|---|---|---|
| No replay | 22.22 +/- 0.00 | 77.60 +/- 0.02 | 33.33 +/- 0.00 | 14.81 +/- 0.00 |
| Uniform | 65.29 +/- 2.92 | 34.53 +/- 2.93 | 66.98 +/- 7.02 | 45.50 +/- 2.86 |
| Class-balanced | 83.99 +/- 1.44 | 15.77 +/- 1.42 | 71.56 +/- 4.19 | 77.97 +/- 1.05 |
| CBRS | 83.88 +/- 1.12 | 15.89 +/- 1.12 | 72.57 +/- 2.04 | 77.87 +/- 1.50 |
| Protected | 72.84 +/- 2.25 | 26.84 +/- 2.29 | 82.73 +/- 2.36 | 47.15 +/- 3.82 |
| RBR | 85.52 +/- 1.27 | 14.24 +/- 1.27 | 76.62 +/- 4.16 | 79.03 +/- 1.00 |
| EWC | 24.89 +/- 1.30 | 74.95 +/- 1.30 | 33.33 +/- 0.00 | 17.15 +/- 3.56 |
| A-GEM | 46.03 +/- 4.58 | 53.80 +/- 4.58 | 50.29 +/- 4.68 | 37.12 +/- 3.29 |
| Joint | 94.20 +/- 0.07 | -- | 76.82 +/- 0.17 | 77.89 +/- 1.48 |

## RBR minus CBRS

Percentage points [95% paired interval]. An interval excluding zero is significant. Higher is better for the three metrics below.

| Setting | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|
| Federated | +1.64 [+0.40, +2.88] | +4.04 [+0.41, +7.68] | +1.16 [+0.02, +2.30] |
| Centralized | +3.25 [+2.21, +4.30] | +7.93 [+4.09, +11.77] | +0.49 [-0.68, +1.66] |

## Interpretation

Federated old-attack accuracy: +1.64 [+0.40, +2.88] points; better for RBR.

Federated Slowloris recall: +4.04 [+0.41, +7.68] points; better for RBR.

Federated worst-client score: +1.16 [+0.02, +2.30] points; better for RBR.

Centralized old-attack accuracy: +3.25 [+2.21, +4.30] points; better for RBR.

Centralized Slowloris recall: +7.93 [+4.09, +11.77] points; better for RBR.

Centralized worst-client score: +0.49 [-0.68, +1.66] points; difference not significant.

Order-specific loss: centralized, order 2, Slowloris recall -0.58 [-1.07, -0.10] points.

## Each order

| Setting | Order | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| Fed. | 1 | +3.52 [-0.31, +7.36] | +9.72 [-1.66, +21.09] | +3.02 [-0.79, +6.82] |
| Fed. | 2 | +0.72 [-1.22, +2.67] | -0.08 [-0.28, +0.11] | +0.02 [-1.25, +1.29] |
| Fed. | 3 | +0.69 [-1.20, +2.57] | +2.50 [-0.58, +5.58] | +0.44 [-2.07, +2.95] |
| Central | 1 | +3.94 [+1.08, +6.79] | +12.52 [+3.74, +21.29] | +0.01 [-3.19, +3.21] |
| Central | 2 | +2.49 [+1.47, +3.52] | -0.58 [-1.07, -0.10] | +0.47 [-0.67, +1.62] |
| Central | 3 | +3.33 [+1.70, +4.97] | +11.85 [+6.00, +17.70] | +0.99 [-0.31, +2.28] |

## Scoring sensitivity

| Setting | View | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| Fed. | Merged | +1.64 [+0.40, +2.88] | +4.04 [+0.41, +7.68] | +1.16 [+0.02, +2.30] |
| Fed. | Exact | +0.23 [-1.75, +2.21] | +3.57 [-0.92, +8.06] | +0.94 [+0.13, +1.76] |
| Central | Merged | +3.25 [+2.21, +4.30] | +7.93 [+4.09, +11.77] | +0.49 [-0.68, +1.66] |
| Central | Exact | +2.43 [+0.46, +4.40] | +7.34 [+3.72, +10.96] | +0.58 [-0.11, +1.28] |

## Scope and verification

This compares population policies under the accepted task-based training schedule and fixed replay loss. CBRS ingestion is sequential at task boundaries; each fitting flow enters once, while benign reference flows still recur in training. The original paper's separate weighted-retrieval recipe is not substituted. All losses and non-significant comparisons are retained. Intervals describe training randomness on the same fixed split and are unadjusted for multiple comparisons.

Only 16 benign and five fragmentation evaluation flows are available. There are no false-alarm or fragmentation conclusions. Previous cross-split RBR/class-balanced evidence is preserved; CBRS was not run on extra splits or at memory 300/client.

Verification passed for 60 models, 240 checkpoints, 1,182,880 prediction rows and 64 paired intervals. Population state, counts, stream arrivals, role boundaries and calibration selection were checked.
