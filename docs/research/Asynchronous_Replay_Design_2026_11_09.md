# Asynchronous adaptive replay study fixed design

Frozen paper: outputs/frozen_paper_2026_11_09/MANIFEST.json. The current paper and all accepted comparisons remain unchanged. This new study is exploratory and must not replace the paper based on a favorable score alone.

## Question

Does local calibration-driven rare-memory allocation improve Slowloris retention when stations encounter the same rare-first task sequence at different times?

## Fixed setup

Use the existing 36,172-row sampled corpus and five original allocation profiles, with a new persistent role split seed 62. This is a new prospective partition of reused data, not independently collected or genuinely unseen external validation. Fit preprocessing only on first-cohort fitting rows and freeze it. The original current-paper evaluation has already informed the broad research direction.

Task order: low-rate/rare, vulnerability scan, flooding, reconnaissance. Each client encounters each cohort once, with benign fitting references recurring. Synchronized starts use offsets [0,0,0,0,0]. Delayed starts use [0,1,0,2,1] in the original client order. Evaluate six global phases in either condition. Inactive clients do not train or contribute aggregation weights. Synchronization has two idle terminal phases. Delayed exposure creates six active server stages; total current-task local exposures are matched, but global update count, replay exposures and Adam resets can differ and must be reported. This design isolates a compound timing/participation stressor, not a pure single-factor causal intervention.

MLP 64/32 ReLU, Adam learning rate 0.003, five local epochs, five rounds per phase, batch128, weight decay0.0001, no clipping. Memory60 per federated client and300 pooled. All current training, preprocessing and memory use fitting roles only. Head classes become available when first exposed anywhere. The preprocessing schema is initialized from the first cohort across clients before the delayed training schedule.

## Methods and calibration

Class-balanced, published CBRS population, fixed RBR and adaptive RBR. Fixed population and loss mechanics are reused. Replay fractions0.25/0.50. Fixed RBR q0.10/0.20. Adaptive RBR base q0.10 and maximum0.20/0.30. It computes pressure from the greater of current rare-class error and twice the drop from its best previous calibration recall, clipped to[0,1], and linearly interpolates between base and maximum. Each client monitors only its own supported rare calibration classes with at least five rows. With existing fragmentation support, this will predominantly monitor Slowloris; it is not a claim of general rare-group validation. No evaluation rows or other clients' calibration examples influence its controller. Pooled controls monitor their own pooled calibration data. No additional allocation communication is introduced; labeled local monitoring and computation are required. Memory is updated after each client's active task, using retained memory plus current fitting candidates; discarded history is not recovered.

Calibrate all methods separately per environment/schedule using training seed100 and mean checkpoint original-type calibration macro recall, over six phases. Ties favor first listed grid item. All48 calibration fits must precede every evaluation. Evaluation uses training seeds100-109, four methods, two schedules, two environments:160 runs. Save all settings, selected scores, models, checkpoint probabilities, local monitoring rows, memory traces and training counts.

## Reporting and stopping

Primary merged-Scan scores: old-cohort accuracy, forgetting, Slowloris recall, worst-client macro recall. Old cohorts remain the first three original cohorts. Report exact-type sensitivity, each client, compute/update counts, and all losses. Paired t9 intervals over10 seed differences are unadjusted. Primary prespecified success screen: delayed federated adaptive minus fixed RBR has a positive lower95% bound for Slowloris and lower bounds above-1 percentage point for old accuracy and worst-client score. This is an exploratory screen, not multiplicity-adjusted confirmation. Report schedule and federation interactions; do not claim one exists from a nonsignificant result.

No candidate or controller may be changed after viewing evaluation. If it fails, retain the outcome and use calibration-only development or genuinely fresh data for a new design; do not keep reopening this evaluation until a winner appears. Generic adaptive replay and dynamic memory allocation already have prior art (Adaptive Memory Replay, CVPR Workshops2024; FeDMRA, arXiv2603.28455). Novelty and superiority remain unestablished.
