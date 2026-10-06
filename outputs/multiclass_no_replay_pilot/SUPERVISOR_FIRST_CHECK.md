# Multiclass no-replay first check

6 October 2026. Diagnostic pilot; no full comparison was run.

Clear forgetting observed: **True**. Benign-data requirements satisfied: **False**.

MLP 64/32, ReLU, Adam, 5 local epochs per round, 5 rounds per task; no gradient clipping; attack cap 3,000; persistent roles and Task-1-only preprocessing retained.

Learning rate **0.003**, selected on calibration data only. All tried values and scores are saved in hyperparameter_trials.json. Other settings are fixed.

## Direct old-attack accuracy drops

Accuracy excludes benign examples and requires the exact attack type.

| Seed | Old task | Accuracy after learning | Accuracy after final task | Drop (percentage points) | Initially learned >=50% |
|---|---|---:|---:|---:|---|
| 42 | reconnaissance | 25.83% | 0.00% | 25.83 | False |
| 42 | flooding | 99.60% | 0.00% | 99.60 | True |
| 42 | low_rate_rare | 99.83% | 0.00% | 99.83 | True |
| 43 | reconnaissance | 24.47% | 0.00% | 24.47 | False |
| 43 | flooding | 99.67% | 0.00% | 99.67 | True |
| 43 | low_rate_rare | 100.00% | 0.00% | 100.00 | True |
| 44 | reconnaissance | 26.73% | 0.00% | 26.73 | False |
| 44 | flooding | 99.80% | 0.00% | 99.80 | True |
| 44 | low_rate_rare | 99.83% | 0.00% | 99.83 | True |

Criterion recorded before evaluation: >=10 percentage-point drop on an old task initially learned to >=50% accuracy, in >=2/3 seeds. This is a practical pilot criterion, not a statistical significance test.

## Final per-client metrics

Macro recall averages supported classes. Null false alarm rates mean no benign evaluation support.

| Seed | Client | Evaluation rows | Benign support | Exact attack accuracy | Macro recall | Rare recall | FPR |
|---|---|---:|---:|---:|---:|---:|---:|
| 42 | reconnaissance_heavy | 2020 | 9 | 1.49% | 14.29% | 0.00% | 0.00% |
| 42 | flooding_heavy | 2019 | 2 | 1.49% | 14.29% | 0.00% | 0.00% |
| 42 | low_rate_rare_heavy | 966 | 2 | 34.23% | 13.33% | 0.00% | 0.00% |
| 42 | mixed_open_set | 1507 | 3 | 9.97% | 13.33% | 0.00% | 0.00% |
| 42 | benign_starved | 722 | 0 | 8.31% | 7.14% | 0.00% | N/A |
| 43 | reconnaissance_heavy | 2020 | 9 | 1.49% | 14.29% | 0.00% | 0.00% |
| 43 | flooding_heavy | 2019 | 2 | 1.49% | 14.29% | 0.00% | 0.00% |
| 43 | low_rate_rare_heavy | 966 | 2 | 34.23% | 13.33% | 0.00% | 0.00% |
| 43 | mixed_open_set | 1507 | 3 | 9.97% | 13.33% | 0.00% | 0.00% |
| 43 | benign_starved | 722 | 0 | 8.31% | 7.14% | 0.00% | N/A |
| 44 | reconnaissance_heavy | 2020 | 9 | 1.49% | 13.49% | 0.00% | 11.11% |
| 44 | flooding_heavy | 2019 | 2 | 1.49% | 14.29% | 0.00% | 0.00% |
| 44 | low_rate_rare_heavy | 966 | 2 | 34.23% | 13.33% | 0.00% | 0.00% |
| 44 | mixed_open_set | 1507 | 3 | 9.97% | 13.33% | 0.00% | 0.00% |
| 44 | benign_starved | 722 | 0 | 8.31% | 7.14% | 0.00% | N/A |

## Accuracy matrix

See checkpoint_task_accuracy.csv for every checkpoint and old/current task; seed results JSON files include task-by-client metrics, per-class supports, AUROC and average precision.

## Limitations and required next decision

Only 82 genuine benign flows exist locally; only 16 unique benign evaluation rows per seed remain under the corrected protocol. The benign-starved client has no benign evaluation rows. ICMP fragmentation and ICMP flood remain data-limited; a sampling cap cannot create observations. No duplicated/synthetic test examples were introduced.

Do not claim protected-replay effectiveness from this no-replay pilot. No replay-method comparison, EWC, DER++, joint-training, centralized comparison, ten-seed/three-order study, or manuscript claim updates have been run. Reconnaissance initially reaches only about 25-27% attack-type accuracy and does not meet the initial-learning gate. Rare-task accuracy is weighted by support and is dominated by Slowloris; inspect per-class ICMP-fragmentation support/recall before interpreting it.

Present this first-check result to the supervisor before full experiments. Agree on additional benign collection or a revised evaluation/framing. If no clear forgetting was found, stop as instructed.

Research repository: https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot.
