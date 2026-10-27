# What changed in the exploratory tuning

This follow-up preserves the original result package and manuscript. It tunes model/training settings and reruns the same continual stream from initialization for each seed; it does not update weights using evaluation rows or silently replace the earlier experiment.

## Selected common model

Calibration selected hidden layers 128 and 64, compared with the earlier 64 and 32, and learning rate 0.001 instead of the earlier replay-method rate 0.003. ReLU, Adam, five local epochs, five rounds/task, weight decay 0.0001, and the original 15 output types remain. Dropout and stronger weight decay were tested but were not selected. A larger network has more representational capacity; a smaller learning rate makes each optimizer update more gradual. Whether these help evaluation must be measured, not assumed.

The larger model has 27,023, 20,367 and 25,999 parameters across the three order-specific feature representations. The earlier model has 11,471, 8,143 and 10,959. Matching replay-example counts therefore does not match total memory bytes or computation.

## Replay mixing

Each allocator is separately calibrated over replay fractions 0.25, 0.50 and 0.75. With batch size 128, 0.75 uses 96 replay examples and up to 32 current examples per step, versus 64/64 for 0.50. Replay samples are drawn with replacement from the bounded stored memory. The same few stored examples can occur multiple times in minibatches, but there are still at most 60 unique stored rows per client. Smaller current minibatches also increase optimizer steps for a fixed number of current-data epochs; this is a training-work change.

Class-balanced and protected replay receive the same selected model configuration and their own replay-fraction selection. Balanced+rare additionally selects a 10% or 20% minimum rare reservation. At capacity 60, those reserve up to 6 or 12 rare examples when available, then fill remaining slots by the existing balanced allocator. There is no new benign quota. The protected comparator retains its original 20% benign/20% rare policy.

## What stays fixed

Original sampled rows, five client profiles, three attack orders, persistent roles, Task-1 preprocessing, memory 60 per client, centralized total 300, ten evaluation seeds and original-type training stay fixed. Primary scores still sum the six scan probabilities. Slowloris recall remains the reported rare metric. No new data, synthetic benign examples, altered splits or favorable seed selection is introduced.

## Selection and scope

The calibration objective now averages final-checkpoint merged old accuracy, Slowloris recall and worst-client macro recall equally. This differs from the original criterion and is disclosed. One common backbone is selected by averaging equally across the three allocators, both environments and all orders. All 180 calibration fits finish before 180 evaluations. Both successful and unsuccessful tested settings are retained.

Frozen-versus-tuned differences measure the changed overall pipeline. Tuned-versus-tuned comparisons describe allocator differences conditional on the common selected model and the recorded tuning grids. A gain in accuracy does not alone establish novelty or a gain specific to federation. Earlier evaluation results had already been observed, so this is exploratory evidence, not new untouched-test confirmation. The earlier manuscript is not automatically rewritten around these results.
