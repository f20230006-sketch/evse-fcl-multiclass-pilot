# Targeted validation results - 27 October 2026

## What was done

- Repeated the key memory-60 comparison on three additional persistent-role splits, using the accepted model and calibration-only selection.
- Added rare reservation with random remainder and no benign quota on the original split.
- Re-scored merged-Scan and exact-type views, checked grouping metadata and inspected public FedCBDR code.
- Revised the letter with the validation results, allocation ablation and 17 references.

## Main results

Federated, original split; percentages, mean +/- SD of ten seed averages across three orders.

| Method | Old accuracy | Forgetting | Slowloris | Worst-client |
|---|---|---|---|---|
| Class-balanced | 83.99 +/- 1.44 | 15.77 +/- 1.42 | 71.56 +/- 4.19 | 77.97 +/- 1.05 |
| Protected | 72.84 +/- 2.25 | 26.84 +/- 2.29 | 82.73 +/- 2.36 | 47.15 +/- 3.82 |
| Balanced+rare | 85.52 +/- 1.27 | 14.24 +/- 1.27 | 76.62 +/- 4.16 | 79.03 +/- 1.00 |
| Rare+random | 72.07 +/- 2.87 | 27.60 +/- 2.90 | 84.78 +/- 2.04 | 48.62 +/- 5.37 |

## Cross-split comparisons

Balanced+rare minus class-balanced, percentage points [95% paired interval]. Each split uses ten paired training seeds averaged across the three orders. An interval excluding zero is significant; negative forgetting is better.

| Split | Setting | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| 42 | Fed. | +1.53 [+0.23, +2.84] | +5.06 [+1.27, +8.84] | +1.06 [-0.07, +2.19] |
| 42 | Central | +1.67 [+1.12, +2.22] | +5.00 [+3.04, +6.96] | +0.64 [+0.14, +1.14] |
| 43 | Fed. | +2.23 [+0.95, +3.51] | +7.93 [+4.03, +11.83] | +0.64 [-0.62, +1.91] |
| 43 | Central | +1.11 [+0.47, +1.74] | +3.48 [+1.31, +5.65] | +1.39 [-0.91, +3.69] |
| 44 | Fed. | +3.37 [+2.11, +4.63] | +11.28 [+7.59, +14.97] | +1.39 [+0.29, +2.49] |
| 44 | Central | +1.13 [-0.19, +2.46] | +3.80 [-0.79, +8.39] | -0.06 [-0.68, +0.55] |
| 45 | Fed. | +2.06 [+0.40, +3.72] | +6.09 [+1.30, +10.88] | +0.93 [-0.40, +2.25] |
| 45 | Central | +0.82 [+0.01, +1.63] | +2.61 [-0.01, +5.22] | -0.17 [-0.94, +0.60] |

## What this means

Federated: old-accuracy differences are positive on 4/4 splits, significantly better on 4/4; Slowloris differences are positive on 4/4, significantly better on 4/4. Worst-client score is significantly worse on 0/4.

Centralized: old-accuracy differences are positive on 4/4 splits, significantly better on 3/4; Slowloris differences are positive on 4/4, significantly better on 2/4. Worst-client score is significantly worse on 0/4.

## Allocation ablation

Original split, federated differences [95% interval].

| Comparison | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|
| Rare+random - Protected | -0.76 [-3.06, +1.54] | +2.05 [+0.69, +3.41] | +1.47 [-2.19, +5.12] |
| Balanced+rare - Rare+random | +13.45 [+10.83, +16.06] | -8.16 [-11.62, -4.71] | +30.41 [+26.61, +34.21] |

## Exact-type sensitivity

Original split, balanced+rare minus class-balanced [95% interval].

| Setting | View | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| Fed. | Merged | +1.53 [+0.23, +2.84] | +5.06 [+1.27, +8.84] | +1.06 [-0.07, +2.19] |
| Fed. | Exact | +1.90 [+0.37, +3.43] | +6.02 [+1.51, +10.54] | +0.70 [-0.04, +1.45] |
| Central | Merged | +1.67 [+1.12, +2.22] | +5.00 [+3.04, +6.96] | +0.64 [+0.14, +1.14] |
| Central | Exact | +0.83 [+0.05, +1.61] | +3.72 [+2.04, +5.39] | +0.34 [+0.10, +0.58] |

## Evidence scope

The extra splits reuse overlapping flows from the same dataset, not new captures. Source filenames are available provenance groups, but no explicit session/capture column was found. Flow IDs and timestamps are not established session groups. File-level coverage is documented; no new splitting pipeline was built. Benign evaluation remains 16 flows and fragmentation five, so neither false-alarm nor fragmentation gains are claimed. The class-balanced and rare reservations operate on original types even for merged reporting.

Public FedCBDR code exists but the inspected checkout has missing imported modules, an unsupported README method name, and an image/CUDA pipeline. It was not reconstructed or presented as a baseline. Our allocation is local, with no additional coordination messages, whereas FedCBDR uses global memory coordination and objective/logit balancing.

All 132 calibration fits precede all 420 new evaluation runs. Saved models, roles, replay boundaries, 8280160 checkpoint prediction rows and 448 intervals passed verification. No exploratory tuned-model results replace the accepted protocol.
