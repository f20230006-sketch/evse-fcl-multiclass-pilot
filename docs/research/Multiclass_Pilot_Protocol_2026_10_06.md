# Multiclass no-replay pilot protocol

This is the first-check experiment requested in the supervisor email. It does not authorize the full comparison or support manuscript claims by itself.

## Fixed design

- Predictor: input -> 64 -> 32 -> 15 output classes; ReLU after each hidden layer.
- Training: Adam; 5 complete shuffled local epochs per communication round, 5 rounds per task, batch size 128, weight decay 0.0001, unweighted multiclass cross-entropy. No gradient clipping. Optimizer state resets after each broadcast. Clients start from identical copies of the global model.
- Federated optimizer: sample-count FedAvg, using current fitting rows only; replay is absent.
- Class policy: a predeclared vocabulary of benign plus 14 attack types. Globally unseen output classes are masked. At evaluation, all seen classes compete and the model receives no task identity. No future-task samples fit the preprocessor.
- Pilot replication: seeds 42, 43, 44; one fixed order: reconnaissance, flooding, low-rate/rare, vulnerability scan. Ten seeds and three orders belong to the later full comparison.
- Sampling: a cap of 3,000 per attack, or all available rows for smaller classes; all benign rows retained. Source-file/source-row provenance identifies each sample. This remains a flow-level split, not a held-out-capture generalization study.
- Roles: original client-label-stratified persistent fitting/calibration/evaluation protocol, fractions 0.65/0.15/0.20 with small-block safeguards. No calibration or evaluation rows enter fitting.
- Preprocessor: fitted only on the first task's fitting rows pooled across clients, then frozen. Original identifier exclusions, z-score scaling, one-hot encoding, and numeric z-score clip of 5 are retained. This shared fit is an offline simulation assumption, not a demonstrated privacy protocol.

## Calibration selection

Only learning rate is selected. Candidates are 0.0003, 0.001, and 0.003. Each is trained through the task sequence on seed 42, with selection based on the mean across checkpoints of macro recall on the unique union of seen-task calibration rows. Ties favor the smaller learning rate. This screens no-replay learning rate, not settings for future replay methods. Evaluation predictions are not produced during screening.

All other settings above are fixed engineering choices rather than tuned values. The protocol is serialized before calibration screening and evaluation. Exact trials are recorded in `hyperparameter_trials.json`.

## Forgetting decision

For each old task, measure exact attack-type accuracy immediately after learning that task, then after the final task. Benign rows are excluded from this accuracy. A seed shows a clear drop if at least one old task initially reached 50% attack accuracy and subsequently dropped by at least 10 percentage points. Clear forgetting requires this in at least two of the three seeds. These thresholds operationalize the email's unspecified 'clear' requirement; they are pilot criteria, not thresholds supplied by the supervisor or a formal significance test.

Also save the full checkpoint-by-task matrix and best-earlier-to-current nonnegative forgetting. Poor initial learning alone does not pass the gate. Always show rare-class support.

## Data limitation and publication gate

The local network CSVs contain 82 benign flows: 14 charging and 68 idle. Under the retained protocol, each pilot seed has 16 unique benign evaluation flows. The benign-starved profile has zero benign rows in every role, so its false alarm rate is undefined. The user confirmed no additional real benign data are available.

The default runner stops if fewer than 200 genuine benign evaluation rows are available. The explicit `--allow-limited-benign-diagnostic` flag permits only a documented attack-forgetting diagnostic. It does not satisfy the requested false-alarm evidence. Synthetic, bootstrapped, or duplicated benign rows are not added to evaluation.

Do not launch the full replay/EWC/DER++/joint or centralized comparison until the first-check result has been presented to the supervisor and the benign-support limitation has been resolved or an alternative evaluation protocol has been agreed. If no clear forgetting occurs, stop and discuss framing as requested.

## Client allocations retained from v3

Within each original label, seeded shuffling is followed by flooring the following allocation counts and assigning remaining records by largest fractional remainder:

| Label group | Recon-heavy | Flood-heavy | Rare-heavy | Mixed | Benign-starved |
|---|---:|---:|---:|---:|---:|
| Benign | 55% | 15% | 10% | 20% | 0% |
| Reconnaissance | 55% | 10% | 5% | 20% | 10% |
| Flooding | 10% | 55% | 5% | 20% | 10% |
| Rare allocation group | 5% | 5% | 55% | 25% | 10% |
| Other labels | 10% | 10% | 10% | 55% | 15% |

The rare allocation group contains Slowloris, ICMP fragmentation, and vulnerability scanning. Rare-attack recall reports exact identification of Slowloris and ICMP fragmentation. Every source row belongs to one client only. These are simulated profiles, not five separately observed stations.

## Metrics and files

Per checkpoint: pooled metrics, metrics for each client, metrics for each old/current task and client, exact per-class recall/support, attack-type accuracy, forgetting, rare-attack recall, false alarm rate, worst-client macro recall, multiclass one-vs-rest AUROC and average precision, and binary attack-ranking AUROC/AP using 1-p(benign).

Average precision is used as the step-integral PR-area convention and is explicitly labelled; it is not trapezoidal PR AUC. Macro ranking averages include only classes with both positive and negative evaluation support. Recall macro averages include classes present in the evaluated block. Undefined metrics are null, never zero-filled. Pooled evaluation unions deduplicate recurring benign rows. Client differences must be interpreted with their different class supports.

Artifacts: frozen preprocessor metadata, class mappings, split manifests/audits, input inventory, per-epoch local losses, checkpoint metrics, final probabilities, final state dictionaries, calibration trials, and the decision file. Final model evaluation does not claim operational intrusion detection or unseen-attack robustness.

## Reproduce

Install the separate pilot dependencies listed in `requirements-multiclass.txt` into an appropriate environment. From the project root:

```powershell
python scripts/run_multiclass_no_replay_pilot.py --prepare-only
python scripts/run_multiclass_no_replay_pilot.py
```

The second command deliberately stops on current benign support. To reproduce the explicitly limited diagnostic:

```powershell
python scripts/run_multiclass_no_replay_pilot.py --allow-limited-benign-diagnostic
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -p test_multiclass_pilot.py -v
```

Cached sampled records are invalidated by data path, seed, cap, label column, file sizes/mtime, and loader hash. For a pristine resample, use a new output directory in a copied configuration. Source hashes and runtime versions are saved with each run. Cached raw features are local-only and are excluded from the publication package.
