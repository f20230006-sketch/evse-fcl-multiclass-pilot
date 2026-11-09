# Teacher alignment corrective study fixed design

## Diagnosed limitations

Saved logs show that the legacy teacher is disabled for each client's first local task. Under delayed participation, flooding-heavy and benign-starved clients start at global phase2 and mixed at phase3, after globally learned classes already exist. These three first tasks therefore have no prior-model constraint. This is a design limitation, not a numerical leak or invalidation of the earlier measured gains. Later tasks in this fixed schedule cover all prior global classes; the main observed gap is delayed first participation.

Calibration labels also show Slowloris-to-Scan confusion and weaker supported flood classes. Fragmentation has too few examples for a general conclusion. Calibration settings were ranked using15 exact types although primary evaluation merges six scans. This creates an objective mismatch, not evaluation leakage. Old config prose and the cloned runner header contain stale seed/count descriptions; executable fields, actual seed200, and completed40/100 records are authoritative. Corrections will be described without rewriting frozen records.

## Bounded fixes and ablations

Keep the same MLP64/32, capacity60 per client/300 pooled, Adam0.003, five local epochs/rounds, weight decay0.0001, batch128, no clipping. Use one rare-first delayed sequence, six phases and offsets[0,1,0,2,1]. Use prospective row partition64 of the same already examined corpus; it is not independent external validation. Fit preprocessing on Task-1 fitting data and freeze it. Active local exposures match earlier stress protocols. Extra teacher state and different global update/reset counts remain explicit.

Compare six evaluation aliases:

- Legacy teacher with original-type calibration criterion.
- Identical legacy teacher with merged-Scan criterion; reuse the same calibration fits to isolate selection.
- Global-aligned teacher with prior global class coverage, including late first participation, and merged criterion.
- Global-aligned family teacher: aggregate temperature-scaled probabilities of the six scan labels for distillation. Student includes currently seen members of an already known family; teacher includes only previously seen members. New families are excluded from the old-family penalty. Supervised labels remain original types. Merged criterion.
- Class-balanced memory with legacy teacher and merged criterion.
- Class-balanced memory with global-aligned family teacher and merged criterion.

Family-aware distillation is a targeted consistency experiment, not an established novelty claim. Generic distillation and hierarchical/family methods have prior art. RBR memory population itself is unchanged.

## Calibration and gate

Replay fractions0.25/0.50, distillation weights0.1/1.0, temperature fixed2, and RBR rare fractions0.10/0.20. Match grids and learning settings across applicable methods. Average each candidate's mean-phase calibration macro recall over training seeds300/301/302; this reduces dependence on one calibration initialization. Ties favor first grid item. There are192 actual calibration fits:32 candidates across2 environments and3 seeds; the legacy criterion aliases share fits.

Before any evaluation, save all trials, selections and a gate. Proceed only if the selected global or family variant's three-seed federated merged calibration score exceeds selected legacy-merged by at least0.002. If neither passes, retain calibration-only evidence and stop without reading a new evaluation partition. If either passes, evaluate all six aliases in both environments with10 new training seeds310-319,120 runs, once. No candidate changes after evaluation.

## Outcomes and stopping

Primary candidate is family versus legacy-merged in delayed federation: Slowloris lower95% interval above0, old accuracy and worst-client lower bounds above-1 percentage point. Also report family versus global, both class-balanced controls, criterion-only effects, original-type sensitivity, clients and costs. All paired t9 intervals are exploratory/unadjusted. Calibration gate passage is not a test-performance claim. A failure to improve remains a result. Preserve the original paper and both completed exploratory studies. No automatic promotion to manuscript main claims or continued holdout tuning.
