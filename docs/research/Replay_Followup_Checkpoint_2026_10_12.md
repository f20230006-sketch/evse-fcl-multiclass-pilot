# Completed follow-up checkpoint — 12 October 2026

The 7 October supervisor requests have been implemented and evaluated. No experiments remain running or require retraining.

- Essential class-balanced-60 stage: 12 calibration trials, 60 evaluations.
- Supplementary uniform/balanced/protected-120/300 sweep: 72 calibration trials, 360 evaluations.
- Existing 420 evaluations reused unchanged; combined report covers 840.
- All 420 new final models and 8,280,160 checkpoint prediction rows verified against original frozen prepared inputs. Seventeen relevant unit tests passed; all 208 paired interval rows and 60 joint confusion runs independently checked.
- New output roots: replay_followup_essential, replay_followup_sweep, replay_followup_report, joint_diagnostics.
- Main handoff: outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md and SUPERVISOR_REPLY_DRAFT.txt. Email is draft only.
- Archive: outputs/FCL_Oct07_Followup_All_Deliverables_2026_10_12.zip; all raw checkpoint NPZs included. Input caches/prepared features/raw datasets excluded. Git contains lighter metadata/models/code/configs rather than the large checkpoint NPZs.
- Memory 60: balanced beats protected old-type retention (47.68% vs 42.78% federated); protected beats balanced rare recall (86.48% vs 72.09%). Supported paired differences; contribution is a trade-off, not dominance.
- Memory 300: protected old accuracy 61.75% vs uniform 60.08%, gain +1.67 points [1.19, 2.14]. Benefits differ by attack order and metric.
- Joint all-type evaluation accuracy 57.21% federated / 59.56% centralized; fitting accuracy 57.61% / 60.11%. Scan confusion is recurrent; intrinsic indistinguishability is not established. Joint family micro accuracy (sum-probability convention) 89.34% / 90.87%. Joint is an empirical offline reference and not a demonstrated upper bound.
- No training-label merges, added datasets, manuscript submission, PR merge, or email sending performed. Family reports use pre-existing task groups only.
- OCPP supplied source contains 163,570 nominal benign rows but incompatible features and unverified independent grouping; both ZIPs duplicate one another. CICEVSE CSVs duplicate original 14/68 rows. Original benign evaluation support remains 16.
- Private publication checkout: work/evse-fcl-multiclass-pilot; branch full-multiclass-comparison; GitHub PR #1. Original source/config hashes remain unchanged.

Scientific next step: supervisor reviews the updated class-balanced trade-off, order dependence and joint matrices before manuscript claims or a newly specified merged-label/optimized-joint study.
