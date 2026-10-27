# Targeted validation design - 27 October 2026

Frozen before new fitting. Preserve the accepted 64/32 ReLU MLP, Adam learning rate 0.003, five local epochs, five rounds, batch 128, weight decay 0.0001, original task cohorts, three orders and ten training seeds 42-51. Do not incorporate the separate exploratory 128/64 model.

Use additional persistent-role split seeds 43, 44 and 45 on the same sampled rows and seed-42 client allocation. Roles remain stratified by client and original label. Fit preprocessing exclusively on Task-1 fitting rows for each split/order, freeze afterwards, and share it across compared methods/environments. Thus split-specific feature vocabularies can change, while allocation and sampling cannot. These overlapping random splits are sensitivity checks, not independent captures.

Compare class-balanced and balanced+rare at 60 rows/client, centralized total 300. Select settings separately for each split/order/environment with calibration seed 42, unchanged mean checkpoint original-type calibration macro recall, first-candidate tie break. Grids: replay fraction 0.25/0.50; balanced+rare quota 0.10/0.20. Complete all calibration fits before evaluating any new run. No evaluation-based redesign or second search.

Optional targeted ablation: original split only, rare reservation with uniformly random remainder and no benign reservation. Quota 0.10/0.20 and replay 0.25/0.50, same calibration criterion. This uses the original protected allocator with just the rare group. It is a component comparison rather than a fully crossed causal factorial experiment.

Report merged-Scan primary and exact-type sensitivity, all four metrics, each split/environment/order and ten-seed paired t intervals. Average orders within each seed for split summaries; do not treat all split-seed pairs as independent observations. Include all losses. Use original accepted results as split 42 reference. No new pipeline for capture grouping; inspect identifiers and source-file class coverage only.
