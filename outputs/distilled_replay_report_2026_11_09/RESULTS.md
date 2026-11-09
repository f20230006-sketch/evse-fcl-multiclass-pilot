# Teacher-distilled replay results

Second exploratory mechanism, split63 of reused corpus, one rare-first delayed order; unadjusted intervals and extra teacher RAM. Not external validation or novel distillation.

## Delayed federated merged-Scan results

| Method | Old accuracy | Forgetting | Slowloris recall | Worst client |
|---|---:|---:|---:|---:|
| class_balanced | 86.31 ± 3.38 | 13.10 ± 3.47 | 65.03 ± 9.48 | 82.23 ± 1.87 |
| cbrs | 87.04 ± 2.70 | 12.52 ± 2.76 | 66.77 ± 7.61 | 82.43 ± 2.63 |
| fixed_rbr | 84.74 ± 5.58 | 14.63 ± 5.80 | 64.62 ± 12.26 | 80.17 ± 4.67 |
| class_balanced_kd | 88.15 ± 3.59 | 11.42 ± 3.68 | 66.43 ± 11.12 | 84.42 ± 1.12 |
| fixed_rbr_kd | 89.73 ± 2.07 | 9.70 ± 2.19 | 76.03 ± 4.57 | 83.42 ± 2.38 |

Percentages, mean ± sample SD over ten training seeds.

## Distilled RBR minus fixed RBR

- federated, old_task_accuracy: +4.99 points [1.05, 8.93]; better.
- federated, forgetting: -4.92 points [-9.05, -0.80]; better.
- federated, slowloris_recall: +11.42 points [1.63, 21.20]; better.
- federated, worst_client_macro_recall: +3.25 points [0.29, 6.21]; better.
- centralized, old_task_accuracy: +0.21 points [-1.52, 1.93]; not significant.
- centralized, forgetting: -0.21 points [-1.90, 1.47]; not significant.
- centralized, slowloris_recall: +0.33 points [-4.69, 5.36]; not significant.
- centralized, worst_client_macro_recall: +0.60 points [0.17, 1.04]; better.

## Prespecified screen

{
  "slowloris_positive_lower_bound": true,
  "old_accuracy_lower_above_minus_one_point": true,
  "worst_client_lower_above_minus_one_point": true,
  "all_prespecified_conditions_met": true,
  "scope": "Second exploratory mechanism, split63 of reused corpus, one rare-first delayed order; unadjusted intervals and extra teacher RAM. Not external validation or novel distillation."
}

## Interpretation

The teacher mechanism changes the training objective and adds model state; gains cannot be credited solely to memory allocation. Distilled class-balanced replay is included to assess that distinction. The current paper stays frozen. Complete original-type, centralized, per-client and interaction results are included. Favorable exploration requires independent confirmation before replacing accepted claims; unfavorable results are retained without further evaluation-driven tuning.