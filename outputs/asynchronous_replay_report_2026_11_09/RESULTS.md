# Asynchronous adaptive replay results

The current paper and baseline evidence remain frozen. This is a separate exploratory study: one rare-first order, a prospective row partition of the reused corpus (seed62), ten training seeds, two timing schedules and matched-capacity federated/centralized controls. No independent external dataset was available.

## Main delayed federated results

| Method | Old accuracy | Forgetting | Slowloris recall | Worst client |
|---|---:|---:|---:|---:|
| class_balanced | 84.73 ± 2.67 | 14.75 ± 2.57 | 64.25 ± 6.61 | 78.17 ± 3.36 |
| cbrs | 85.32 ± 3.42 | 14.28 ± 3.50 | 61.12 ± 10.42 | 80.29 ± 2.13 |
| fixed_rbr | 87.23 ± 0.80 | 12.34 ± 0.81 | 67.98 ± 2.52 | 79.86 ± 1.95 |
| adaptive_rbr | 86.87 ± 0.84 | 12.69 ± 0.86 | 67.38 ± 2.94 | 79.66 ± 2.51 |

Values are percentages, mean ± sample SD across ten training seeds.

## Adaptive minus fixed RBR

- synchronized, federated, old_task_accuracy: -0.38 points [-1.86, 1.11]; not significant.
- synchronized, federated, forgetting: +0.55 points [-1.08, 2.18]; not significant.
- synchronized, federated, slowloris_recall: -3.02 points [-7.70, 1.67]; not significant.
- synchronized, federated, worst_client_macro_recall: -0.30 points [-2.75, 2.14]; not significant.
- synchronized, centralized, old_task_accuracy: +2.87 points [0.76, 4.98]; better.
- synchronized, centralized, forgetting: -3.23 points [-5.55, -0.91]; better.
- synchronized, centralized, slowloris_recall: +9.23 points [2.52, 15.94]; better.
- synchronized, centralized, worst_client_macro_recall: +1.66 points [0.67, 2.65]; better.
- delayed, federated, old_task_accuracy: -0.35 points [-1.25, 0.55]; not significant.
- delayed, federated, forgetting: +0.35 points [-0.55, 1.26]; not significant.
- delayed, federated, slowloris_recall: -0.60 points [-2.75, 1.55]; not significant.
- delayed, federated, worst_client_macro_recall: -0.21 points [-1.20, 0.78]; not significant.
- delayed, centralized, old_task_accuracy: +1.54 points [0.07, 3.01]; better.
- delayed, centralized, forgetting: -1.68 points [-3.27, -0.09]; better.
- delayed, centralized, slowloris_recall: +5.30 points [0.46, 10.14]; better.
- delayed, centralized, worst_client_macro_recall: +0.53 points [-2.11, 3.18]; not significant.

## Prespecified outcome

{
  "slowloris_positive_lower_bound": false,
  "old_accuracy_lower_above_minus_one_point": false,
  "worst_client_lower_above_minus_one_point": false,
  "all_prespecified_conditions_met": false,
  "scope": "Exploratory screen on reused-corpus split62, one rare-first order; unadjusted intervals. Not external validation."
}

## Interpretation boundaries

The controller uses local labeled calibration monitoring; it is not label-free adaptation. The rare-monitor support threshold means it predominantly monitors Slowloris. Local current-task exposures are matched, while delayed aggregation stages, replay exposures and optimizer resets differ; see training_costs.csv. All baselines, exact-type sensitivity, per-client metrics and interaction intervals are retained. A nonsignificant interaction does not establish a federation-specific advantage.

Evaluation results must not be used to redesign this controller. A favorable screen alone does not justify replacing the frozen paper; external or genuinely independent confirmation and a novelty review would be needed. An unfavorable screen remains a valid finding.