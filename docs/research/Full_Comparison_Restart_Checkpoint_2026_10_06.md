# Restart checkpoint — 2026-10-06

All requested multiclass experiments are complete. No retraining remains.

- 84 calibration trials and 420 evaluation runs: 10 training seeds, three orders, seven methods, two environments.
- Verification passed for all final models and 7,531,320 checkpoint prediction rows; 13 unit tests passed.
- Original fixed split and Task-1-only preprocessing retained. Additional supplied datasets excluded as instructed. Only 16 benign evaluation records; benign-starved client FPR is undefined.
- Federated old-attack type accuracy: protected replay 42.78%, uniform replay 35.31%, no replay 0%. Centralized protected 51.61%, uniform 43.75%. No demonstrated additional retention benefit specific to federation; worst-client improvement remains uncertain.
- Results: outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md and SUPERVISOR_UPDATE.md.
- Publication checkout: work/evse-fcl-multiclass-pilot; branch full-multiclass-comparison; private GitHub repository f20230006-sketch/evse-fcl-multiclass-pilot.
- Git includes source/configs/split manifests/metrics/final models. Raw data and prepared features excluded. Full checkpoint probabilities are in outputs/full_multiclass_comparison_repository.zip.
- Remaining handoff: publish branch/draft PR, review scientific framing with supervisor before writing manuscript. Do not revive earlier binary-model improvement claims.
