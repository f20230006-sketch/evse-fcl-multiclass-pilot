# Current model diagnosis

## Confirmed design gaps

The saved phase/client logs show that three clients receive no distillation on their delayed first task despite prior globally learned classes: flooding-heavy and benign-starved at phase2 (three prior classes), and mixed at phase3 (four prior classes). The legacy policy initializes teacher protection only after a client has completed a local task. This does not invalidate the earlier gains; it leaves some earlier global knowledge unprotected during late first participation. New tests demonstrate the gap and corrected global coverage.

Calibration selections rank the original15 attack/benign labels while the primary score merges six scans. This is an objective mismatch, not test leakage. The next design isolates selection-only effects by scoring exactly the same calibration fits under both views. Three calibration initialization seeds replace reliance on a single seed for new comparisons.

Old runner/config descriptive text contains stale counts and seed descriptions. The executed configuration fields, saved seeds and completion records show40 calibration fits,100 evaluated runs and calibration seed200. Frozen records will not be rewritten; new configuration descriptions match execution.

## Error structure from calibration data

The current distilled RBR model's pooled calibration mean recall is77.26% for Slowloris,99.35% for merged Scan, and84.71% for SynonymousIP flood. Slowloris-to-Scan confusion is prominent. Some lower-support classes have weaker recall, but the tiny ICMP-fragmentation sample cannot support a broad conclusion. Per-client calibration macro recall also trails distilled class-balanced replay at several profiles, consistent with an allocation/retention trade-off rather than uniform superiority. See the complete CSVs for support counts and dispersion.

## Targeted hypotheses

Global-aligned teacher coverage may preserve knowledge when late clients first join. Family-consistent distillation may avoid imposing distinctions among six scan types that primary scoring intentionally merges, while leaving supervised labels unchanged. Neither hypothesis is assumed to improve evaluation. Existing same-corpus evaluation partitions will not choose another winner; the bounded next design uses calibration-first screening, a prospective repartition, and explicit exploratory scope.

## Preserved evidence

PRIOR_RESULTS_LOCK.json records hashes of both completed study reports, the manuscript extension and their archives. The original accepted paper remains in the separate verified freeze. No prior result has been overwritten.

## Calibration-only aggregation probe

A representative seed200 probe reproduced the original six-phase calibration trajectory exactly while observing30 aggregation rounds on449 Slowloris calibration rows. FedAvg recall was never below the weighted mean of local recalls in that probe. This does not support a claim that immediate weight averaging is the dominant failure mechanism. Recall still drops after later-task updates, so local optimization and sequential drift remain relevant. These are descriptive observations on one calibration trajectory, not a causal or external validation result. Full before/local/ensemble/after values are retained in aggregation_calibration_probe.csv.
