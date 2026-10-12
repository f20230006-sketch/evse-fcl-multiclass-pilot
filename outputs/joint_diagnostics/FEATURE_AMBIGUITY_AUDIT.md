# Exact feature-vector ambiguity audit

This diagnostic groups byte-identical float32 feature vectors after the original frozen preprocessing. For each persistent role separately, the oracle assigns the most common label to each exact vector. Its accuracy is a same-role, in-sample maximum for deterministic classification using these features, not a trained model, held-out estimate, tuning signal or attainable generalization target. It uses labels only for diagnosis; no model or label grouping is changed. Conflicts may be inherent in the supplied flows or induced by clipping/unknown-category handling; this audit does not distinguish those causes.

| Order | Role | Rows | Distinct vectors | Rows sharing a vector with another type | Oracle type ceiling | Oracle family ceiling |
|---|---|---:|---:|---:|---:|---:|
| order_1 | fitting | 23513 | 23486 | 3 | 100.00% | 100.00% |
| order_1 | calibration | 5425 | 5420 | 0 | 100.00% | 100.00% |
| order_1 | evaluation | 7234 | 7227 | 0 | 100.00% | 100.00% |
| order_2 | fitting | 23513 | 23487 | 3 | 100.00% | 100.00% |
| order_2 | calibration | 5425 | 5420 | 0 | 100.00% | 100.00% |
| order_2 | evaluation | 7234 | 7227 | 0 | 100.00% | 100.00% |
| order_3 | fitting | 23513 | 23485 | 3 | 100.00% | 100.00% |
| order_3 | calibration | 5425 | 5420 | 0 | 100.00% | 100.00% |
| order_3 | evaluation | 7234 | 7227 | 0 | 100.00% | 100.00% |

This ceiling is micro accuracy over all samples, so compare it with joint all-type accuracy, not old-task macro accuracy. It does not establish a ceiling for a different feature extractor or merged-label retraining. Inspect the paired CSV to locate specific overlapping types.
