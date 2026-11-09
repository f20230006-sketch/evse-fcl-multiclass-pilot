# Reproducing the corrective study

This is incremental evidence for the existing EV-charging project. Restore into the original project checkout with the previous frozen-paper and exploratory-study inputs intact; source hashes and PRIOR_RESULTS_LOCK intentionally protect those inputs. Overlay source/ contents into the project root and restore the archived outputs/ beneath the same root. The earlier frozen and raw archives remain separately available.

The raw archive contains the full new prepared tensors, models, checkpoint probabilities, fitting-memory audits, logs and fixed protocols. These can be independently inspected without rerunning training. Each protocol preserves its actual settings and hashes. The 192-fit core study, separately declared 24-fit matched baseline, and parameter-matched baseline have distinct timelines. The two added baselines are transparently post-evaluation controls and do not retune the corrected RBR model.

Recommended settings are pre-evaluation calibration selections, not the highest-scoring evaluation seed. Do not use the held-out partitions for further tuning. The family-distillation hypothesis failed and is retained as a negative finding; the type-level global teacher is the recommended experimental candidate.
