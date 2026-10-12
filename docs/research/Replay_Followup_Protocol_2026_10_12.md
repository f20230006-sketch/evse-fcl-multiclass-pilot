# Supervisor follow-up protocol — 12 October 2026

This extension addresses the six requests in the 7 October email without changing the completed original study or importing the previously excluded datasets.

## Frozen experiment and matched budgets

The original 36,172-row sample, seed-42 allocation and persistent fitting/calibration/evaluation roles are reused byte-for-byte. Prepared input tensors and split manifests are fingerprinted. Preprocessing remains fitted on first-task fitting rows and frozen separately for each of the original three task orders. The existing 10 training seeds, model, optimizer, five local epochs, five rounds/task and evaluation conventions are unchanged.

Memory is **60, 120 or 300 unique examples per federated client**, hence 300, 600 or 1,500 slots system-wide. Centralized controls use those same system-wide totals. Do not describe centralized memory as 60/120/300 total. Budgets count examples, not bytes. The 60-slot uniform/protected results and all previously evaluated EWC/A-GEM/joint models are reused exactly.

## Class-balanced baseline

The existing `balanced` allocator in `continual_ablation.py` is now connected to the MLP continual runner. After each task, the candidate pool is the unique union of that client's retained memory and current fitting rows. Rows within each label bucket are shuffled with the separate memory RNG. One slot is taken per class in sorted label order repeatedly until capacity is filled or the pool is exhausted. Thus plentiful classes differ by at most one slot; the final remainder follows sorted label order. Classes with fewer examples retain all available candidates, and unfilled slots are redistributed across remaining classes. Classes unavailable at a client receive no synthetic examples; specifically, the benign-starved client cannot retain benign samples.

This implements equal feasible quotas across seen classes under the same task-boundary memory protocol as uniform and protected replay. It does not retrieve discarded historical examples, oversample memory records, change within-class selection by importance, or balance current-task minibatches. Pool-only allocation is explicitly distinguished from an oracle that can refill memory from the full historical dataset. Per-stage class counts, seen class IDs and capacity are recorded in `memory_audit.json`.

Uniform/protected methods retain their original allocator mechanics at the increased capacities. Protected replay still reserves 20% for benign and 20% for the predeclared rare group, when candidates exist, and fills remaining capacity uniformly. Rehearsal sampling remains replacement sampling from the retained memory during optimization.

## Calibration and sequencing

Two prespecified replay fractions, 0.25 and 0.50, are screened per method/environment/order. Learning rate 0.003 and all other training settings remain fixed from the original protocol. The criterion is mean checkpoint seen-task calibration macro recall; ties choose the first grid entry. Evaluation rows never select settings.

The essential stage has 12 calibration-only trials followed by 60 class-balanced-60 evaluations. These completed before the supplementary sweep began. The sweep has 72 calibration-only trials followed by 360 evaluations: three allocators × two new capacities × three orders × two environments × ten seeds. Each stage completes all its calibration trials before its evaluation jobs. Combined with the 420 existing evaluations, the final comparison contains 840 evaluated cases; only 420 are new training runs.

## Joint diagnosis and family-level reporting

Final predictions from all 60 original joint models produce both count and row-normalized confusion matrices for each environment/order and pooled across orders. Per-class support, recall, confused-pair rates and frequency across all 30 seed/order runs are exported. Matrix counts repeat the same evaluation observations across training seeds/orders; they do not increase independent data support.

Additional post-hoc diagnostics compare fitting, calibration and evaluation accuracy/loss of the frozen joint models, show local training-loss traces, and audit byte-identical transformed vectors with different labels. No optimizer setting, sample role, feature pipeline or training label is changed by these diagnostics. The exact-vector majority oracle is an in-sample diagnostic, not a learned model or a generalization estimate. A lack of exact conflicts does not prove that all types are separable by the small MLP.

The original near-99% single-task pilot figures apply to selected easier tasks, not all attack types. Joint old-task macro accuracy (~55% federated) is also a different metric from all-type micro accuracy (~57%). Confusion alone does not prove intrinsic indistinguishability; low fitting performance points to limitations of the current representation/model/optimization combination too.

Family reporting uses the **already-defined four task groups**, plus benign. It sums type probabilities within each group before argmax and reports old-family accuracy, family forgetting, rare-group recall, worst-client macro recall, macro AUROC and average precision. Accuracy obtained by simply mapping the winning type to its group is also exported as a separate convention. These are re-scores of type-trained models, not merged-label retraining. The grouping was defined before evaluation; it is not chosen from observed confusion pairs. No new label merging is performed before the supervisor reviews the matrices.

## Paired comparisons and orders

Old-task accuracy, forgetting, rare-attack recall and worst-client macro recall are compared using protected minus uniform and protected minus class-balanced at all three capacities, separately per order and after averaging orders within each seed. Protected-60 minus EWC and A-GEM comparisons use the same four metrics. Intervals use ten paired seed differences, sample SD and the two-sided t critical value for nine degrees of freedom. Raw differences and per-run metrics are included. Intervals are unadjusted for multiple comparisons and describe training randomness on the fixed split.

Evidence that a mean benefit occurs does not imply it holds in every order. Exact type recall and family recall are distinct outcomes. EWC/A-GEM conclusions apply to the recorded calibration grid and Adam adaptation, not every possible implementation of those methods.

## Excluded data and remaining limitations

The two supplied OCPP benign ZIPs are byte-identical: one dataset containing 163,570 rows in three CSVs, with 69 columns. Only source/destination port names overlap the 86-field CICEVSE schema. Their hybrid physical/simulated source and contiguous sequences do not establish compatible features or independent capture units. They contain substantially more nominally benign traffic but cannot defensibly be appended to the existing experiment without matched extraction and grouping provenance. The supplied CICEVSE charging/idle CSVs duplicate the existing 14/68 rows exactly and provide no new benign observations.

The original 16 independent benign evaluation flows remain the available support; benign-starved false alarm rate is undefined. No additional training datasets were imported. The original-data limitation and exclusion rationale remain disclosed. The current deliverables support supervisor review of the contribution before manuscript writing; they are not a manuscript submission.

## Commands

```powershell
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -p test_replay_followup.py -v
python scripts/run_replay_followup.py --config configs/replay_followup_essential.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_essential
python scripts/report_joint_diagnostics.py
python scripts/audit_joint_fit_quality.py
python scripts/audit_joint_feature_aliases.py
python scripts/run_replay_followup.py --config configs/replay_followup_sweep.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_sweep
python scripts/report_replay_followup.py --family
```

Original source/input hashes and completed-case fingerprints guard resume. For an intentionally changed protocol, choose a new output directory rather than overwrite published evidence. Plotting additionally requires matplotlib; the local workspace installation is used only by report scripts and never added to training workers' import paths.
