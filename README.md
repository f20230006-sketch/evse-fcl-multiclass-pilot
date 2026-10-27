# EVSE multiclass federated continual learning

## Targeted validation and revised letter - 27 October 2026

Read [two-page summary](outputs/targeted_validation_report_2026_10_27/SUMMARY.pdf), [complete numerical notes](outputs/targeted_validation_report_2026_10_27/INFO.md), and the [revised letter](manuscripts/ieee_networking_letters_2026_10_27/main.pdf). This round preserves the accepted 64/32 MLP and excludes the separate exploratory tuning from the manuscript results.

Three additional persistent-role splits retain the sampled rows and seed-42 client allocation. The key memory-60 class-balanced versus balanced+rare comparison uses ten training seeds, three orders and both environments; an original-split rare+random/no-benign ablation is also included. All 132 calibration fits precede 420 evaluations. Every split/order and both score spaces, including losses, are reported. These overlapping splits do not establish independent capture generalization.

Source-file groups exist; no explicit session/capture column was found. The limited two-file coverage for benign and Slowloris prevents all three roles from being supported under whole-file assignment. Public FedCBDR source was checked at its recorded commit: missing direct imports, an unsupported README method, and image/CUDA dependencies preclude a faithful quick tabular baseline. Its global coordination and objective changes are distinguished from our purely local allocator.

Code, configs, split manifests, calibration records, all final weights, per-run/per-client tables and verification are included. Compressed checkpoint probabilities are in the separate raw archive. Clean review/raw archives omit email drafts. The original sent letter remains preserved; the revised draft retains author placeholders and has not been submitted.

Reproduce in a separate output workspace with the original input sample and hashes. Run `scripts/run_targeted_validation.py`, `scripts/inspect_targeted_sources.py`, `scripts/analyze_targeted_validation.py`, and `scripts/verify_targeted_validation.py`. The public FedCBDR checkout is needed only for its read-only feasibility check. Core numerical runs do not depend on that checkout.


## Exploratory model tuning — 27 October 2026

A separately authorized follow-up tests six common model configurations, then replay fractions 0.25/0.50/0.75 and rare shares 0.10/0.20. Class-balanced, protected and balanced+rare share the calibration-selected backbone; 180 calibration fits finish before 180 evaluations across both environments, all orders and ten seeds, memory 60/client. Read [SUMMARY.pdf](outputs/exploratory_tuning_report_2026_10_27/SUMMARY.pdf), [complete results](outputs/exploratory_tuning_report_2026_10_27/INFO.md) and the [design](docs/research/Exploratory_Tuning_Design_2026_10_27.md).

This is exploratory: the earlier evaluation outcomes were already known. The calibration objective changes to the equal-weight final-checkpoint mean of merged old accuracy, Slowloris recall and worst-client macro recall. Frozen-to-tuned gains are overall pipeline differences; matched-backbone controls address conditional allocator differences. All losses and calibration candidates remain visible. Original data roles, task cohorts, 15-type training, memory capacity, earlier numerical evidence and the previously sent manuscript are preserved. No untouched-test confirmation, universal superiority or novelty claim follows from this follow-up alone.

Verification covers all new models, predictions, buffer policies, frozen digests and selection timing. An initial Windows output-directory permission failure occurred before fitting one calibration job; identical-config recovery reused 179 finished calibration fits. See execution_incidents.json. Clean review/raw archives and a separate email draft are provided locally; no email was sent. Reproduction should use a separate output workspace and matching recorded input hashes.


## Frozen final replay experiment — 26 October 2026

The final balanced-plus-rare-quota method is complete at memory 60 and 300 per client: 48 calibration fits followed by 120 evaluations, ten seeds, three orders, federated and centralized. Read [SUMMARY.pdf](outputs/balanced_rare_report/SUMMARY.pdf) (two pages), [SUMMARY.md](outputs/balanced_rare_report/SUMMARY.md) and [INFO.md](outputs/balanced_rare_report/INFO.md) before older reports. Merged-Scan scoring is primary and the rare metric is now Slowloris recall alone. Exact-type results are sensitivity checks, including any differences in conclusions. No inference is made from five fragmentation examples.

The [frozen design](docs/research/Balanced_Rare_Frozen_Design_2026_10_26.md) reserves a feasible 10% or 20% rare share, then fills remaining slots using the existing class-balanced allocator, including benign as an ordinary class. Replay fractions are 0.25/0.50. Choices use the unchanged original-type calibration criterion, not evaluation outcomes. No post-evaluation adjustment or extra experiment was performed. Statistical non-significance does not establish non-inferiority. Both environments and every memory/order result, including losses, are retained.

Code, configs, all calibration records, memory partitions and final weights are here; checkpoint probabilities are provided in the separate raw-results bundle. Clean review/raw bundles contain no email drafts or implementation files. Verification checks every new model, checkpoint, role, quota, merged decision and paired comparison. Results are frozen for review before writing; no manuscript is included.

Reproduce only intentionally in a separate output workspace, retaining original prepared inputs. Run `scripts/run_balanced_rare_final.py`, `scripts/verify_balanced_rare_final.py`, `scripts/analyze_balanced_rare_final.py`, then `scripts/verify_balanced_rare_report.py`. Read the recorded protocols and existing evidence first. The frozen source/input hashes prevent silently resuming changed experiments.


## Final checks — 17 October 2026

Read the [two-page summary](outputs/final_scan_analysis/SUMMARY.pdf) or [Markdown summary](outputs/final_scan_analysis/SUMMARY.md), then [INFO.md](outputs/final_scan_analysis/INFO.md) for all merged/rare/client tables. The scan-only Random Forest achieves 34.25% versus 16.67% chance, so intrinsic indistinguishability of all six scans is not established. All 840 saved MLP runs were re-scored without retraining. Separate Slowloris/fragmentation recalls and paired federation interactions are included; the memory-60 protection-over-uniform interaction is not significant. The supported Slowloris interaction at memory 300 is exploratory and unadjusted for multiplicity.

The six merged scan probabilities produce ten output classes; Slowloris stays separate. Original task cohorts and original type-level replay memories are retained for this alternative scoring view. The 33.33% rare metric is explained by last-task order effects over 600 Slowloris and five fragmentation examples, not an always-correct class. All source predictions and splits remain unchanged.

Scripts and compact evidence are in Git. Two clean ZIPs are provided separately: a 2.2 MB review bundle and a 329 MB raw-result bundle. Neither contains email drafts or code. Original MLP probabilities are referenced by digest rather than duplicated; final merged probabilities and RF predictions are in the raw bundle. [Final verification](outputs/final_scan_analysis/verification.json) covers 840 runs, 3,180 checkpoints, 15,811,480 re-scored rows, 592 interval rows and 30 RF evaluations. No manuscript or new MLP training was introduced.

Install `requirements-final-scan.txt` in an isolated environment. The scan diagnostic needs the matching local prepared inputs from the original study; they are excluded from publication. The RF protocol records its source/input hashes, six calibration trials and selected settings before evaluation. Read existing completed evidence first. Any intentional fresh rerun should use a separate output directory/workspace so the frozen evidence remains intact.


The 7 October follow-up is complete: class-balanced replay, joint confusion diagnostics, a 60/120/300 memory sweep, paired EWC/A-GEM comparisons, every attack order, and an excluded-dataset reply. **84 new calibration trials and 420 new evaluations**, alongside the original 420 evaluations. Original evidence is preserved.

Read the [follow-up results summary](outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md), [full tables](outputs/replay_followup_report/FOLLOWUP_RESULTS.md), [joint confusion report](outputs/joint_diagnostics/JOINT_CONFUSION_REPORT.md), [follow-up protocol](docs/research/Replay_Followup_Protocol_2026_10_12.md), [dataset reply](docs/research/Excluded_Datasets_Reply_2026_10_12.md), and [deliverables index](DELIVERABLES_INDEX_2026_10_12.md). The [original results](outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md) remain available.

At memory 60, class-balanced replay exceeds protected replay on old-type retention; protected replay has higher rare-type recall. Benefits depend on metric, capacity and attack order. Do not claim uniform dominance or intrinsic type indistinguishability. Only 16 benign evaluation flows are available, and benign-starved FPR is undefined. Seeds vary training randomness on one fixed split. Joint is an empirical offline reference.

## Evidence and reproduction

Code/configs, split manifests, all calibration trials, per-run/station metrics, diagnostics, final weights and verification are in Git. All raw compressed checkpoint predictions are distributed in the accompanying deliverables ZIP. Raw datasets, prepared feature tensors and input caches are excluded. [TESTING.md](TESTING.md) records checks; [TODOS.md](TODOS.md) records scientific work remaining.

Install `requirements-followup.txt` in an isolated environment. Obtain the matching original CICEVSE flow CSVs. The full comparison `--prepare-only` path recreates the original prepared features, subject to protocol/input checks. Follow-up protocols fingerprint exact original source and prepared-input bytes; platform/library changes can affect serialization and numeric results.

```powershell
$env:PYTHONPATH = "$PWD/src"
python scripts/run_replay_followup.py --config configs/replay_followup_essential.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_essential
python scripts/run_replay_followup.py --config configs/replay_followup_sweep.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_sweep
python scripts/report_replay_followup.py --family
python scripts/verify_followup_reports.py
python scripts/summarize_replay_followup.py
```

Published completed-case stamps are original evidence. To retrain intentionally, use fresh original-study and follow-up output directories, updating `reference_output` to the fresh original study; keep published results untouched. Library versions/source/input fingerprints are recorded in the experiment protocols. No new merged-label model or manuscript is claimed.
