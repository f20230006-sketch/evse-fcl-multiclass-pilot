# Multiclass full-comparison protocol

The user explicitly authorized proceeding with the original CICEVSE data despite class imbalance and excluded the subsequently supplied archives/CSV copies. The prior three-seed no-replay pilot demonstrated forgetting. This run retains the data-support limitation rather than treating it as a blocker; it does not claim the email's request for hundreds of benign test records has been satisfied.

## Design and reproducibility

- Fixed original network-flow sample: seed 42, cap 3,000 per attack; all 82 benign rows retained. The selected sample has 36,172 records; rare classes with fewer available records remain below the cap.
- Client assignment and persistent fitting/calibration/evaluation roles use split seed 42, fixed across all methods, training seeds, environments and orders. Training seeds 42-51 vary model initialization, local batch order and memory sampling; they do not represent ten independent datasets or splits. This prevents cross-seed reuse of calibration rows as evaluation rows.
- Three prespecified task permutations are in the configuration. For each permutation, fit preprocessing on that order's first-task fitting rows only, then freeze it. Federated and centralized methods share the resulting feature representation and exact source rows. The shared preprocessing fit remains an offline simulation assumption.
- Predictor: input -> 64 -> 32 -> 15, ReLU, Adam, batch size 128, weight decay 0.0001, 5 complete current-data epochs per round, 5 rounds per task. No gradient clipping. Numeric standardized inputs retain the v3 clip of 5. Adam state resets at every broadcast. No automated class balancing or synthetic benign supplementation is applied.
- Fixed framework defaults: Adam beta values (0.9, 0.999), epsilon 1e-8, no learning-rate scheduler, coupled L2 weight decay (not AdamW), and PyTorch `nn.Linear` default weight/bias initialization. Inputs and model parameters are float32; targets are int64.
- CPU execution, deterministic PyTorch operations, one Torch thread per worker, a main pool of three processes. A supplementary three-process pool computed the final centralized/order-3 block ahead of the main queue using identical job fingerprints; its runtime note is saved in supplementary_execution.json. Scientific settings and outputs are unchanged; the main executor resumes these completed jobs. Library versions, source hashes, input inventory, sample checksum and job fingerprints are saved. Completed jobs can resume only with matching source/config/sample fingerprints.
- Globally unseen class logits are masked; all seen classes compete at inference, without task identity. Class vocabulary is prespecified, but future examples never fit preprocessing.

## Comparators

1. No replay: current-task fitting rows only; benign reference fitting rows recur.
2. Uniform replay 60: random bounded selection from previous memory plus current fitting rows at task boundaries. This is the project's original refresh policy, not uniform reservoir sampling from all historical rows.
3. Protected replay 60: same refresh pool, reserving up to 20% of available memory for benign and 20% for the two protected rare attack labels, then randomly filling remaining positions. Missing groups cannot satisfy quotas.
4. EWC: summed previous-task quadratic penalties around consolidated global parameter anchors. Importance is the mean squared **per-example** observed-label cross-entropy gradient on at most 128 uniformly sampled fitting examples per client/task. No Fisher normalization; coefficient selected on calibration. No sample replay.
5. A-GEM (Adam adaptation): current gradient projected against a sampled memory reference gradient if their dot product is negative. Uses the same task-boundary uniform memory policy. Adam applies the projected raw gradients; its preconditioning means the classic SGD first-order constraint on the actual parameter step is not guaranteed. This adaptation is disclosed and is not a claim of exact replication of the original single-pass/SGD evaluation protocol.
6. Joint/offline reference: all task fitting records are available from the start, with the same Task-1-only preprocessor. Five rounds x five epochs cover the whole pooled/client fitting set. This gives each attack example approximately the same number of local passes as the continual schedule, while benign exposure and round structure differ. All classes are active. Forgetting is N/A because this is not a continual model. It is an empirical upper-reference candidate, not a mathematically guaranteed upper bound.
7. FedProx/no replay: same no-replay sequence with a squared-distance penalty to the broadcast parameters. The centralized version is a pooled proximal-training control.

Rehearsal uses a separately sampled memory minibatch mixed with current data, with a calibration-selected memory weight/fraction of 0.25 or 0.50. Every current fitting record is still visited per local epoch; memory rows may recur with replacement. This minibatch rehearsal policy differs from the historical logistic runner's simple unique concatenation and is documented rather than described as identical. FedAvg weights use the unique current-plus-memory count; changing memory composition may change aggregation weights.

Federated sample memory is 60 per client, at most 300 system-wide; centralized sample memory is 300 total. Memory equality refers to raw-example slots, not total bytes: EWC and A-GEM have different parameter/gradient overheads. Replay never contains calibration or evaluation rows. The benign-starved profile retains zero benign data, so it cannot locally protect benign examples or support a local false-alarm estimate.

## Calibration-only settings

Two prespecified candidates per method/environment/order, screened on calibration seed 42 before any evaluation job is launched:

| Method | Tried settings |
|---|---|
| No replay | learning rate 0.001, 0.003 |
| Uniform 60 | replay fraction 0.25, 0.50; learning rate fixed 0.003 |
| Protected 60 | replay fraction 0.25, 0.50; learning rate fixed 0.003 |
| EWC | coefficient 1, 100; learning rate fixed 0.003 |
| A-GEM | reference batch size 32, 64; learning rate fixed 0.003 |
| Joint | learning rate 0.001, 0.003 |
| FedProx | coefficient 0.001, 0.01; learning rate fixed 0.003 |

The fixed learning rate 0.003 for the retention/proximal methods comes from the prior no-replay calibration pilot; it was not independently optimized for those methods. Selection maximizes mean seen-task calibration macro recall across task checkpoints; joint uses its one offline checkpoint. Ties choose the first prespecified candidate. Selected settings can differ by environment/order, so the main federated-centralized interaction measures the behavior of separately calibrated procedures, not an isolated optimizer effect with identical hyperparameters. All candidates, scores, selected flags and fixed settings are recorded.

## Evaluation and inference limits

There are 84 calibration runs and 420 evaluation runs: 10 seeds x 3 orders x 2 environments x 7 methods. Evaluate fixed held-out rows at every task checkpoint and save compressed row-level probabilities. Deduplicate recurring benign rows in pooled evaluation.

Report exact old attack-type accuracy, prior-best-to-final nonnegative forgetting, pooled and macro rare-attack recall, false alarm rate, worst-client macro recall, multiclass one-vs-rest AUROC and average precision, and binary attack-ranking AUROC/AP using 1-p(benign). Report every metric by client, task, seed, order and environment where defined. Macro recall averages classes present in the evaluated block; one-vs-rest ranking averages only classes with positive and negative support. Average precision is a step-integral PR-area convention, explicitly labelled, not trapezoidal PR AUC. Unsupported metrics are null/N/A.

Summaries average orders within each training seed, then report mean/sample standard deviation across ten seeds. Protected-minus-uniform contrasts use paired seeds and orders. The federated-centralized interaction is the difference between those two within-environment improvements. Confidence intervals describe training randomness under a fixed split; they do not establish generalization to unseen captures or stations. The larger archive row count is not treated as independent experimental replication.

The test set still has 16 genuine benign flows, so one false alarm changes pooled FPR by 6.25 percentage points. A reported zero is zero observed alarms, not proof of a low population FPR. The five profiles are simulated and their exact original allocation fractions remain those documented in the pilot protocol. Per-station false alarm rate is undefined at the benign-starved profile.

## Method references

- [EWC](https://arxiv.org/abs/1612.00796): importance-weighted parameter retention.
- [A-GEM](https://arxiv.org/abs/1812.00420): gradient projection against an episodic-memory reference; adaptation details above.
- [FedProx](https://arxiv.org/abs/1812.06127): proximal local optimization under heterogeneity.

## Commands

```powershell
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -p test_full_comparison.py -v
python scripts/run_full_multiclass_comparison.py
python scripts/report_full_multiclass_comparison.py
python scripts/verify_full_multiclass_comparison.py
```

The original pilot artifacts are preserved. Raw data and prepared feature caches remain local-only. The manuscript target is IEEE Networking Letters, four pages; the result report and evidence must determine the claims rather than the expected protected-replay story.
