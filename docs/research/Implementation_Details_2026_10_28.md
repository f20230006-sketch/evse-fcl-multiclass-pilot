# Implementation and reproduction details

This supplements the four-page letter. RBR is the short name for the previously recorded `balanced_rare` method; historical output identifiers and values remain unchanged.

## Shared model and optimization

The original MLP has 64 and 32 hidden ReLU units and 15 outputs. It uses Adam, five local epochs per round, five rounds per task, batch size 128, weight decay 0.0001 and no gradient clipping. Adam state restarts at each local update, as in all accepted comparisons. Each client trains on the full current fitting cohort per epoch; replay mini-batches sample stored indices with replacement, but stored memory entries are unique. Current batch size is 128 minus the replay batch size, so different calibrated replay fractions can change optimizer-step counts. No equal-compute or byte-level memory claim is made.

All clients participate. FedAvg counts unique current-plus-memory fitting rows, including overlap from recurring benign reference flows. Centralized capacity is five times the per-client row capacity. Unseen output classes are masked until learned. Calibration/evaluation flows never enter fitting or replay.

## Data roles and preprocessing

The fixed seed-42 sample and allocation produce 36,172 rows, with 23,513 fitting, 5,425 calibration and 7,234 evaluation. Split manifests retain source filename and source-row provenance; these fields are excluded from features. For each order, preprocessing is fit only on Task-1 fitting rows and then frozen. Original-split input widths for orders 1/2/3 are 138/86/130; categorical vocabularies therefore mix representation and order effects. Additional persistent-role seeds 43-45 reuse the same sample and client allocations and refit Task-1 preprocessing. These overlapping splits are not independent captured traffic.

## Calibration and saved evidence

Calibration seed is 42 and evaluation training seeds are 42-51. The criterion is mean-checkpoint original-type calibration macro recall; ties use the first enumerated candidate. Replay fractions are 0.25/0.50. RBR also calibrates rare reservation 0.10/0.20 at learning rate 0.003. All calibration completes before evaluation for each experiment family. The original RBR final comparison used 48 calibration fits then 120 evaluations at capacities 60 and 300. The additional-split/rare-random round used 132 calibration fits then 420 evaluations. The sole added CBRS comparison uses 12 calibration fits then 60 evaluations, original split 42, memory 60/client or 300 centrally.

Two-sided paired t9 intervals use ten differences after averaging three orders within each training seed. Per-order comparisons retain ten paired seeds. Absolute differences below 10^-12 are treated as numerical zero; this prevents binary-roundoff ties from becoming spuriously significant. Intervals are unadjusted for multiplicity and non-significance is not equivalence or non-inferiority.

## Published CBRS population integration

The frozen design is in `CBRS_Frozen_Design_2026_10_28.md`. The implementation follows Algorithm 1 and the supplementary proof of Chrysakis and Moens (ICML 2020). Full-class flags begin only when memory is filled and persist after a class has been largest. Every tied largest class is marked full. Non-full incoming classes replace a uniformly chosen member of any largest class; full incoming classes use within-class replacement probability m_c/n_c with inclusive encounter counts. Class counters and flags persist across tasks.

To isolate allocation under the accepted training protocol, new fitting rows are shuffled and streamed into the reservoir after each task. Distinct benign fitting flows enter the population stream only in Task 1, while recurring as current training references as before. The backbone, task schedule, uniform replay retrieval and convex cross-entropy replay loss are shared with the allocation controls. The paper's separate weighted-retrieval and changing-loss-weight recipes are not substituted. This evaluates the published population algorithm under this project's task-based training setting rather than reproducing the paper's complete online-learning benchmark.

Training RNG uses seed*100+client-index; reservoir decisions use +10000 and input-stream permutation uses +20000. Independent RNGs make population choices invariant to replay fraction. Internal reservoir slot order persists; exported replay indices are sorted. The only extra online population state is per-class counters/flags; no all-history flow cache or unbounded seen-ID set is needed by the algorithm. Prepared full tensors exist for this offline audit and are not claimed as physical bounded RAM.

## Reproduction and scope

Run `scripts/run_cbrs_comparison.py`, then `scripts/analyze_cbrs_comparison.py`, `scripts/verify_cbrs_comparison.py` and the report/letter builders. Source/config and prepared-input fingerprints are frozen before fitting. Independent algorithm tests compare every update against a separate reference, including persistent full status, rare-class preservation and chunk-invariant state. Saved models, predictions, stream permutations, population states, role boundaries and all paired intervals are verified.

No CBRS capacity-300-per-client sweep, additional split test, weighted CBRS variant or new model search is run. The existing larger-model exploratory study remains separate from letter evidence. GitHub repository: https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot (private; access required). Original raw data are supplied separately by the dataset provider.
