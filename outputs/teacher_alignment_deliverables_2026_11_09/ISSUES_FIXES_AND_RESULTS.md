# Current model issues and measured fixes

All earlier paper results, both prior studies and the manuscript extension remain unchanged. The recommended experimental pipeline retains the original MLP and replay memory, aligns calibration with merged-Scan scoring, and protects prior global classes when a client joins late.

## Confirmed issues

1. Three clients received no distillation on their first delayed task even though earlier classes had already been learned globally. Corrected teacher coverage now includes the prior global head classes.
2. Original calibration ranked15 exact labels while primary reporting merges six scan types. The new selection-only ablation ranks the same calibration fits under merged scoring.
3. One calibration initialization can make choices unstable. New selections average training seeds300/301/302.

A calibration-only probe reproduced the prior six-phase trajectory exactly. The largest observed drops came with late updates, including a single-client final phase. FedAvg did not underperform the weighted mean of local recalls in that representative probe; a generic claim that aggregation alone is the dominant fault is unsupported.

## Matched delayed federated results

| Pipeline | Old accuracy | Forgetting | Slowloris recall | Worst client |
|---|---:|---:|---:|---:|
| Original teacher and exact-type selection | 90.86 ± 2.04 | 8.36 ± 2.47 | 76.42 ± 7.26 | 82.67 ± 2.96 |
| Original teacher with merged selection | 92.26 ± 1.71 | 5.29 ± 2.72 | 85.00 ± 7.37 | 83.84 ± 2.30 |
| Corrected RBR with global teacher | 93.80 ± 1.39 | 3.67 ± 2.38 | 89.97 ± 6.44 | 83.85 ± 2.88 |
| Family-distillation hypothesis | 88.99 ± 1.58 | 10.79 ± 1.60 | 68.93 ± 4.73 | 83.62 ± 1.17 |
| Class-balanced with original teacher | 92.01 ± 1.19 | 6.45 ± 1.99 | 81.15 ± 6.12 | 83.29 ± 2.21 |
| Class-balanced with family teacher | 89.15 ± 1.78 | 10.61 ± 1.79 | 68.67 ± 5.57 | 83.62 ± 0.82 |
| Class-balanced with global teacher, independently calibrated | 90.77 ± 0.79 | 8.91 ± 0.83 | 73.87 ± 1.73 | 82.92 ± 2.30 |
| Class-balanced with global teacher, RBR-matched parameters | 91.55 ± 0.76 | 7.76 ± 1.15 | 77.08 ± 3.13 | 82.88 ± 2.40 |

Values are percentages, mean ± sample SD over ten evaluation seeds310-319 on split64. These figures must not be compared directly with older split63 or paper-wide averages.

## Effect sizes and uncertainty

Combined correction versus the original teacher/selection approach: old accuracy+2.95 points [1.25,4.65]; Slowloris+13.55 [8.18,18.92]; worst-client+1.17 [-1.98,4.33]. This is a secondary combined comparison, not the prespecified family hypothesis.

Selection alignment alone: Slowloris+8.58 [1.38,15.78]; old accuracy+1.41 [-0.04,2.85]. Adding global coverage to merged selection: old accuracy+1.54 [0.15,2.94]; Slowloris+4.97 [-0.72,10.66]. Thus the additional coverage correction has a significant retention effect, while its incremental Slowloris effect is uncertain. Variants are calibrated separately, so performance differences include selected hyperparameters.

Against class-balanced replay with the identical corrected teacher, replay fraction0.50 and distillation weight1.0: old accuracy+2.26 [1.43,3.09], Slowloris+12.88 [8.38,17.38], worst-client+0.97 [-1.87,3.81]. This parameter-matched control was added transparently after the primary evaluation, using only the previously locked RBR calibration settings, without new tuning.

The independently calibrated corrected class-balanced control selected a different replay fraction. The strongest observed legacy class-balanced control still trails corrected RBR on old accuracy+1.80 [0.45,3.14] and Slowloris+8.82 [1.47,16.16], while worst-client+0.56 [-2.08,3.19] is uncertain. All controls are retained.

## Rejected hypothesis and scope

The prespecified family-distillation primary hypothesis failed. It reached68.93% Slowloris recall versus89.97% for the type-level global teacher; it will not replace the recommended pipeline. The corrected global variant had higher calibration score than the family variant before evaluation. Its secondary results are exploratory, not a rescued primary success.

All intervals are nominal, unadjusted paired t9 intervals over ten training seeds. Split64 is a prospective repartition of an already studied corpus, not independent external validation. Three calibration seeds reduce initialization dependence but do not solve dataset uncertainty. Teacher coverage is a design correction, not a claim that it improves every memory policy; class-balanced controls do not show uniform benefit. The teacher adds state and computation. Sparse benign and fragmentation evaluation still preclude broad corresponding claims.

## Work completed and verification

The primary corrective design completed192 calibration fits before120 evaluations. A separately declared post-evaluation matched baseline added24 calibration fits before20 evaluations. A fixed-parameter baseline added10 evaluations without new tuning. Total216 calibration fits and150 evaluated models, plus two calibration-only diagnostic reproduction/probe fits. Five new unit tests passed. Verification covers900 checkpoints and4,166,700 prediction rows, fitting-only replay, calibration-only selection, saved-weight reproduction and preserved prior locks.

The centralized no-gap global/legacy models are identical in all10 pairs, supporting the targeted coverage interpretation. The original six-phase calibration trajectory was reproduced with maximum absolute difference0.0.

## Recommended next step

Use the global prior-class teacher and merged calibration criterion as the next research candidate. Keep type-level supervised training and type-level distillation. Confirm the candidate across additional orders or genuinely independent/capture-separated data before promoting broad main-paper claims. Do not continue tuning against this evaluation partition. No original paper result has been replaced.

## Contents

diagnostics/ contains the teacher-coverage, confusion and aggregation probes. results/ contains all main metrics, controls, client results, costs and intervals. protocols/ contains fixed designs, selected settings and completion records. The raw archive contains full new models, checkpoint predictions, split tensors, audits, logs and source. No email reply is included.