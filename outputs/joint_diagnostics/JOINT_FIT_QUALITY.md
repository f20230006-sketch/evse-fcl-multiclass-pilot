# Joint model fit quality

Frozen final models are diagnosed after the study; no hyperparameters or training labels were changed. These all-type micro accuracies differ from the old-task macro accuracy in the original summary.

| Environment | Role | All-type accuracy | Macro type recall | Cross entropy |
|---|---|---:|---:|---:|
| centralized | calibration | 59.64% | 64.93% | 0.923 |
| centralized | evaluation | 59.56% | 63.10% | 0.924 |
| centralized | fitting | 60.11% | 66.46% | 0.905 |
| federated | calibration | 57.41% | 59.27% | 0.974 |
| federated | evaluation | 57.21% | 56.71% | 0.982 |
| federated | fitting | 57.61% | 60.90% | 0.967 |

Compare fitting and evaluation performance before attributing the result to generalization. Low fitting accuracy shows that the existing small-MLP/training protocol also struggles on its training examples; it does not prove irreducible type ambiguity. Confusion matrices locate the affected types. The separate exact-feature audit finds virtually no cross-type byte-identical features, so it does not establish an intrinsic 55% ceiling. More optimization/capacity or alternate-feature studies would require a new calibration-only protocol rather than retroactively changing this published reference.
