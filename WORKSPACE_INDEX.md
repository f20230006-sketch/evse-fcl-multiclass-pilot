# EV Charging Research Workspace Index

Latest follow-up: [7 October supervisor requests, completed 12 October](outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md). Includes class-balanced replay, 60/120/300 memory sweeps, joint confusion and fit diagnostics, family-level scores, paired method/order intervals, and the excluded-dataset reply. All 420 new evaluations and 84 new calibration trials are complete and verified. [Protocol](docs/research/Replay_Followup_Protocol_2026_10_12.md), [draft email](outputs/replay_followup_report/SUPERVISOR_REPLY_DRAFT.txt), and [all-deliverables ZIP](outputs/FCL_Oct07_Followup_All_Deliverables_2026_10_12.zip).

Latest experiment: [full multiclass comparison](outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md), completed 6 October 2026 with 10 training seeds, three attack orders, two environments and seven methods. See [protocol](docs/research/Full_Comparison_Protocol_2026_10_06.md) and [supervisor update](outputs/multiclass_full_comparison/SUPERVISOR_UPDATE.md). Supplied additional datasets were excluded; the user authorized proceeding despite the original benign-support limitation.

- `src/evse_ids/`: reusable data, model, metrics, federation, and continual-learning code.
- `scripts/`: executable experiment runners.
- `configs/`: experiment configurations.
- `data/`: official dataset and source artifacts.
- `outputs/continual/`: continual-learning JSON outputs.
- `outputs/`: other experiment outputs.
- `docs/reports/`: dated research reports.
- `docs/experiments/`: experiment designs and novel-method proposals.
- `docs/meetings/`: dated meeting notes and historical decks.
- `presentations/updated/`: current presentation deliverables.
- `presentations/archive/`: older presentation copies when superseded.
- `Research_Log.md`: chronological project log.

Current next-stage report: `docs/reports/CICEVSE2024_3_Round_Continual_FL_Report_2026_08_08.md`.
`ieti/`: IET Intelligent Transport Systems manuscript, requirements, frozen evidence and verified result tables (started 2026-09-06).
