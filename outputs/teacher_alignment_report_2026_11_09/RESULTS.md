# Current model corrective study

The prior paper, comparison studies and manuscript extension are unchanged. Diagnostics identified unprotected late first participation, a calibration/primary-score mismatch, and substantial Slowloris-to-Scan confusion. The old configuration prose also had stale descriptions; executed values and records remain authoritative.

The new design compares teacher coverage, score-aligned selection and family-consistent distillation, with matched class-balanced controls. Calibration averages three initialization seeds. Role split64 reuses the existing corpus and is not independent external validation.

## Calibration gate

{
  "baseline_legacy_merged": 0.9093141506996373,
  "global_gain": 0.006385939253563677,
  "family_gain": 0.003233952201942669,
  "required_margin": 0.002,
  "proceed_to_evaluation": true
}

192 actual calibration fits were completed before this gate. The two legacy selection criteria share the same calibration fits.

## Matched delayed federated results

| Alias | Old accuracy | Forgetting | Slowloris | Worst client |
|---|---:|---:|---:|---:|
| legacy_exact | 90.86 ± 2.04 | 8.36 ± 2.47 | 76.42 ± 7.26 | 82.67 ± 2.96 |
| legacy_merged | 92.26 ± 1.71 | 5.29 ± 2.72 | 85.00 ± 7.37 | 83.84 ± 2.30 |
| global | 93.80 ± 1.39 | 3.67 ± 2.38 | 89.97 ± 6.44 | 83.85 ± 2.88 |
| family | 88.99 ± 1.58 | 10.79 ± 1.60 | 68.93 ± 4.73 | 83.62 ± 1.17 |
| cb_legacy | 92.01 ± 1.19 | 6.45 ± 1.99 | 81.15 ± 6.12 | 83.29 ± 2.21 |
| cb_family | 89.15 ± 1.78 | 10.61 ± 1.79 | 68.67 ± 5.57 | 83.62 ± 0.82 |

Percentages, mean ± sample SD over ten evaluation seeds. These scores must not be compared directly with earlier partitions.

## Primary family correction versus legacy merged selection

- old_task_accuracy: -3.28 points [-4.90,-1.65]; worse.
- forgetting: +5.49 points [3.03,7.95]; worse.
- slowloris_recall: -16.07 points [-23.52,-8.62]; worse.
- worst_client_macro_recall: -0.22 points [-1.44,1.01]; not significant.

## Prespecified exploratory screen

{
  "slowloris_positive_lower_bound": false,
  "old_accuracy_lower_above_minus_one_point": false,
  "worst_client_lower_above_minus_one_point": false,
  "all_prespecified_conditions_met": false
}

All controls, both score views and all unfavorable outcomes are retained. Correct teacher coverage is a software/design correction; it does not by itself establish improved generalization. Criterion changes and model changes have distinct ablations. All intervals are unadjusted. The teacher adds RAM/computation, and no new external or capture-separated validation was obtained. The current paper and prior positive extension remain frozen.