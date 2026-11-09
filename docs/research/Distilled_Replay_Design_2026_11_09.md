# Teacher-distilled replay exploratory design

This second direction follows a negative adaptive-quota screen. All first-study outputs remain unchanged. No changes are allowed after this design's evaluation begins, and no current-paper result will be overwritten.

## Mechanism

Keep the existing population allocators and MLP. At the start of a client's active task, copy the broadcast model as a fixed teacher. The first task has no teacher penalty. During subsequent local updates, add temperature2 KL divergence between teacher and student probabilities over the previously available class outputs. Apply it to current and uniformly sampled replay fitting examples, with the same current/replay convex weights as supervised cross-entropy. The teacher stays fixed across the five rounds of that task. Its outputs over newly available classes are excluded. This preserves prior behavior without storing more raw replay examples, but adds one teacher model per active client, computation and RAM. Teacher state is not part of the60-row replay budget. This is an established distillation mechanism, not an asserted novel method or a faithful named DER++ implementation.

## Controlled comparison

One rare-first order and delayed offsets[0,1,0,2,1], six phases, the original five allocation profiles, MLP64/32, five epochs and rounds, Adam0.003, batch128, weight decay0.0001, no clipping. Use a prospective role partition seed63 of the reused corpus, initialize preprocessing on Task-1 fitting data and freeze it. It is not unseen external validation. Learning outcomes from split62 influenced the choice to investigate a different mechanism; no split63 evaluation is used for settings.

Methods: class-balanced, CBRS, fixed RBR, class-balanced plus distillation, RBR plus distillation. Budgets60/client and300 pooled. Calibrate replay fraction0.25/0.50; RBR quota0.10/0.20; distillation weight0.1/1.0; temperature fixed2.0. Same original-type mean calibration macro-recall criterion, calibration training seed200. Fixed tie order. All40 calibration fits finish before100 evaluation runs (10 seeds200-209, five methods, two environments). Every candidate and selection is recorded.

## Analysis

Primary: merged-Scan delayed-federated distilled RBR minus fixed RBR has Slowloris lower95% bound above0 and old accuracy/worst-client lower bounds above-1 percentage point. Report all four metrics, original-type sensitivity, both environments, all five methods and each client. Compare distilled RBR with distilled class-balanced to isolate allocation from the teacher mechanism. Intervals are unadjusted exploratory t9 intervals over10 seeds. Saved teacher/class metadata, models, fitting-only replay traces, checkpoint predictions and costs support verification. No further evaluation-driven iteration is authorized by this design; a third direction needs calibration-only development or independent data, not repeated attempts to make this holdout win.
