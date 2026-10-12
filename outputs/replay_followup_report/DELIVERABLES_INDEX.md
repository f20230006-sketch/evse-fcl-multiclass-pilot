# Deliverables responding to the 7 October supervisor email

Prepared 12 October 2026. Start with **outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md** and the draft email in the same directory.

| Request | Deliverables | Status |
|---|---|---|
| 1. Class-balanced replay 60 | replay_followup_essential/; type_summary.csv and paired_intervals.csv | 12 calibration trials, 60 evaluation runs; verified |
| 2. Joint-training diagnosis | joint_diagnostics/ PNG/PDF and count/normalized CSV matrices, per-type confusion consistency, fit-quality and exact-feature audits | All 60 joint models analyzed; no training-label merges |
| 2. Family-level results | replay_followup_report/family_per_run_metrics.csv, family_summary.csv, family_checkpoint_metrics.json | Existing task groups; summed probabilities and mapped winning-type conventions both reported |
| 3. Memory sweep | replay_followup_sweep/; memory_sweep_*.png/.pdf; summary/paired CSVs | 72 calibration trials, 360 evaluation runs |
| 4. EWC/A-GEM | supervisor summary section 4; paired_intervals.csv | Four requested metrics and matched-seed intervals against protected replay |
| 5. Every attack order | type_per_order_summary.csv; paired_intervals.csv; FOLLOWUP_RESULTS.md | All three orders, both environments and every tested replay capacity |
| 6. Excluded datasets | docs/research/Excluded_Datasets_Reply_2026_10_12.md; additional_benign_audit/ | Source, counts, duplicate evidence, compatibility and independence limits |
| Implementation/protocol | src/, scripts/, configs/, tests/, requirements-followup.txt; Replay_Followup_Protocol_2026_10_12.md | Reproducible runner with calibration/source/input guards |
| Raw evidence | original/full and both follow-up runs/calibration directories | Models, every saved NPZ prediction, logs, metrics, memory audits, completion stamps |
| Checks | verification.json in each follow-up directory; report_verification.json | Models/predictions, roles, budgets, feasible quotas, paired arithmetic and confusion counts |
| Correspondence | SUPERVISOR_REPLY_DRAFT.txt | Draft only; not sent |

Short output paths above are relative to `outputs/` in this archive. The original 6 October study is preserved in `outputs/multiclass_full_comparison/`. There are 840 combined evaluations; 420 are new. The original forgetting pilot and earlier audit evidence are preserved. Historical binary/logistic claims are not used to interpret this follow-up.

## Read raw results

Each evaluated `runs/order/environment/method/seed_*/` directory contains `results.json`, `final_model.pt`, `training_log.json`, `memory_audit.json`, `complete.json` and task checkpoint NPZ files. NPZ keys are `sample_index`, `y_true`, `y_pred`, `probability`. Indices and output columns use the original order's `splits/order_*/split_manifest.csv` and `class_mapping.json`. The follow-up reuses these original split files rather than allocating new rows. Every attempted calibration trial is in `calibration/`; calibration never emits evaluation prediction files.

Confusion counts repeat the fixed test observations across seeds/orders. All confidence intervals describe paired training randomness on one split. Family correctness differs from exact attack-type correctness; summed-family probabilities may change the winning prediction whereas mapped-type scoring retains it.

## Exclusions and integrity

Original input CSV/PCAP data, pickle sample caches, prepared feature tensors, Git metadata/credentials, dependency installation folders and Python caches are excluded. These are not raw experiment results. All saved row-level prediction NPZs are included in this ZIP; Git retains the lighter code/metadata/model evidence. The full archive does not need nested copies of earlier ZIPs.

`deliverables_manifest.json` hashes every payload member; `archive_validation.json` verifies member count, CRC and every digest. Verify after extraction with `python verify_deliverables_manifest.py`. Original full-model verification additionally needs the matching prepared feature tensors, recreated locally from the original data with the documented frozen protocol. Integrity verification alone does not reproduce training.

The private repository draft PR remains https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot/pull/1 . Repository access and transfer permission for this large ZIP must be granted separately. No email, dataset import, new training-label merge, manuscript submission or PR merge is performed by packaging.
