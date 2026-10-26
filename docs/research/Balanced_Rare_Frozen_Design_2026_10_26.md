# Balanced plus rare quota: frozen final design

Fixed on 26 October 2026 before any new calibration or evaluation run. This is the final additional experiment; no redesign or extra grid follows evaluation.

## Allocator

At a task boundary, candidates are unique previous-buffer rows plus current-task fitting rows. Previously discarded examples cannot return. Reserve floor(capacity × rare share) rows from the predeclared group {Slowloris_Scan, ICMP_Fragmentation}, limited by available candidates. Use the existing class-balanced allocator within this group (equal feasible quotas, sorted-label remainder priority, shortage redistribution). This within-group choice is fixed here to avoid selecting after results.

Remove reserved rows, then use the unchanged class-balanced allocator to fill all remaining slots over every remaining candidate class, including benign and rare types. Thus the rare share is a minimum reservation, not an upper bound; rare examples can also enter the balanced part. No separate benign reservation, random common-class fill, duplicates, or future-task candidates. If rare candidates are absent or scarce, all unused slots go to the balanced part. Capacities are 60 and 300 per federated client, versus 300 and 1500 for the pooled centralized model, preserving total storage.

## Fixed training and selection

Reuse original frozen prepared inputs, persistent fitting/calibration/evaluation roles and Task-1-only preprocessing. MLP input→64→32→15 original-type outputs, ReLU, Adam, learning rate 0.003, five local epochs and five rounds/task, batch 128, weight decay 0.0001, no clipping. Original task streams and labels remain unchanged. Merged Scan probabilities are summed for primary scoring; no merged-label retraining.

For each capacity × order × environment, try exactly four configurations in this order: (rare share 0.10, replay fraction 0.25), (0.10, 0.50), (0.20, 0.25), (0.20, 0.50). Calibration seed 42. Preserve the other methods' selection criterion: mean original-type calibration macro recall over checkpoints, ties first grid entry. This criterion is intentionally unchanged even though merged scores are now primary. Finish all 48 calibration fits and record choices before starting any evaluation fit.

Run seeds 42–51, all three original orders and both environments: 120 evaluation fits, 480 checkpoints. Both capacities are included before starting; no optional capacity decision after seeing results. Replay fraction is the training minibatch mixture weight, independent of storage quota. Changes are restricted to buffer allocation.

## Reporting fixed in advance

Primary columns: merged old-attack cohort accuracy, cohort forgetting, Slowloris recall and worst-client supported-class macro recall. Keep original old-task cohorts because Scan spans two tasks. Report means and SD across ten seed means over three orders; paired two-sided t intervals across ten seed differences (df=9), for each capacity/environment and each order. Comparators are existing class-balanced and protected runs at matching capacity/order/seed, retaining their calibration choices. Include all losses, and exact-type sensitivity tables. Slowloris can change under merged scoring because Scan becomes a competing summed probability. No conclusions from five-example fragmentation; benign support remains 16.

Separate improved/worse/not significant labels per metric. Intervals crossing zero do not demonstrate non-inferiority or equivalence. No predeclared non-inferiority margin exists. Multiple comparisons are unadjusted, disclosed; seed intervals describe training randomness on one fixed split. Preserve prior exploratory Slowloris memory-300 federation interaction labeling. No claim of intrinsically indistinguishable scans, and no unsupported claim that every conclusion matches between scoring views.

## Evidence and freeze

Record hashes of this design, all new training/allocator/runner/config sources and inherited source/input files in protocol_before_evaluation.json. Matching stamps allow interruption recovery only, not altered reruns. Save every calibration score, setting, final model, checkpoint probability, memory partition and training log. Independently verify role boundaries, candidate availability, feasible counts, source hashes, final-model predictions and paired arithmetic. Freeze results once complete. Documentation must use neutral results/review language; email drafts remain outside archives. No manuscript is drafted during this experiment.
