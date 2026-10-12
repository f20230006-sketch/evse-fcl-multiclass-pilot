# EVSE multiclass federated continual learning

The 7 October follow-up is complete: class-balanced replay, joint confusion diagnostics, a 60/120/300 memory sweep, paired EWC/A-GEM comparisons, every attack order, and an excluded-dataset reply. **84 new calibration trials and 420 new evaluations**, alongside the original 420 evaluations. Original evidence is preserved.

Read the [follow-up supervisor summary](outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md), [full tables](outputs/replay_followup_report/FOLLOWUP_RESULTS.md), [joint confusion report](outputs/joint_diagnostics/JOINT_CONFUSION_REPORT.md), [follow-up protocol](docs/research/Replay_Followup_Protocol_2026_10_12.md), [dataset reply](docs/research/Excluded_Datasets_Reply_2026_10_12.md), and [deliverables index](DELIVERABLES_INDEX_2026_10_12.md). The [original results](outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md) remain available.

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
