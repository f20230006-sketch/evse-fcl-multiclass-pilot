# Exploratory model tuning — 27 October 2026

Authorized separately after sending the frozen results and manuscript. Preserve all previous results and manuscript bytes. This follow-up does not supersede the previous freeze or retrospectively change its claims. Existing evaluation outcomes have already been examined; this is exploratory follow-up, not untouched-test confirmation. No better result is guaranteed, no failed configuration is hidden, and novelty is not inferred from higher accuracy alone.

## Scope fixed before new runs

Keep original 15-type training, six-scan probability-sum primary scoring, original task cohorts, source rows, allocation, persistent roles and Task-1-only preprocessing. No new data, augmentation, synthetic benign, resplitting or merged-label retraining. Memory stays 60 per client, centralized total 300. Run all three orders, both environments and seeds 42–51. Report all losses against frozen results and newly matched baselines. No selection of a favorable seed/order or repeated tuning after evaluation.

## Stage A: common model configuration

Six explicitly enumerated backbones in the JSON cover original 64/32 and larger 128/64 hidden layers; learning rates 0.003/0.001/0.0005; dropout 0/0.1; weight decay 0.0001/0.001; local epochs 5/3. Five rounds/task, ReLU, Adam, batch 128, no gradient clipping. Adam state resets each local update, as before. Dropout is active only while fitting; predictions always use eval mode.

For every backbone, evaluate calibration-only runs for class-balanced, protected and balanced+rare, at all three orders and both environments, seed 42. Fix replay fraction 0.5; balanced+rare rare fraction 0.1, protected's original benign/rare shares remain 0.2. Total 108 fits. Select one common backbone by averaging the calibration objective equally over all 18 allocator/order/environment cases; ties first candidate. This equal-budget screen is shared by all allocators, not chosen for the new policy alone.

## Stage B: replay settings

Hold that shared backbone fixed. Class-balanced/protected each try replay fractions 0.25, 0.50, 0.75. Balanced+rare tries those three fractions × rare reservations 0.10/0.20. Select per allocator/order/environment using seed 42. Total 72 calibration fits. All 180 calibration fits and all choices finish before 180 evaluation runs (three allocators × three orders × two environments × ten seeds). No subsequent search round.

## Objective and interpretation

The predeclared calibration objective is the equal-weight mean of final-checkpoint merged old-cohort accuracy, Slowloris recall and worst-client supported-class macro recall. This differs from the original mean-checkpoint type-level criterion and must be disclosed. At intermediate checkpoints Slowloris may be absent, but only the final checkpoint chooses settings. None of these values comes from evaluation rows. Changed model/training/selection settings make frozen-vs-tuned differences overall pipeline improvements, not isolated evidence for the allocator. Newly matched baselines provide the conditional allocation comparison. Three methods have the same backbone search; the rare policy has its additional quota parameter grid.

Report primary metrics, paired t9 intervals after averaging orders per seed, every order and both environments. Near-zero differences below 1e-12 are numerical ties. Unadjusted intervals cover training randomness on one fixed split; calibration reuse/adaptive research history limits interpretation. No non-inferiority, privacy, real deployment, independent-station or false-alarm claim is added. Keep fragmentation unsupported (five rows) and benign limits (16 rows) explicit. Evaluation is reported once after the search is complete, including regressions.

## Audit

Protocol fingerprints new and inherited sources/config/design plus prepared data and split manifests before fitting. Save every setting, calibration score, checkpoint probability, final model, memory partition and training log. Check persistent roles, candidate pools, capacities, inference-mode dropout, source hashes and model reproduction. Test the reference backbone against the old identical calibration case to detect unintended implementation drift. Keep logs/configs and clean review/raw evidence separate from email drafts. No automatically rewritten manuscript or email sending is authorized by this tuning run.
