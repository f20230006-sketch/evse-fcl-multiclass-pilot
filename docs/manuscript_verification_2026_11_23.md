# Manuscript verification — 23 November 2026

Overleaf is the manuscript source of truth. This check used the six-page PDF exported on 23 November 2026, SHA-256 fbc66d818331b4302df42073885b90344aa8973e31bf9f4f00dfb26a7bd8efcd. The companion source export was used only to cross-check reference assets. This repository hosts the research implementation, evidence and reproduction instructions; its historical manuscript copies do not supersede Overleaf.

| Check | Status | Evidence and scope |
|---|---|---|
| Table I | PASS | All 32 printed numbers matched aggregation of exact-type per-run metrics. |
| Table II | PASS | All 70 printed numbers matched merged-Scan per-run aggregation; joint forgetting is not applicable. |
| Table III | PASS | All 24 printed values matched seed-wise paired intervals on constructed splits 42–45. |
| Figure 2 | PASS | All 12 means and 24 endpoints recomputed from per-run evidence; match archived coordinates to 1e-7 percentage points. The companion figure is byte-identical to the November 17 asset, and its drawing stream is embedded in the November 23 PDF. |
| Dataset, splits and training | PASS | The saved role manifests and configurations confirm 36,172 sampled rows, 23,513/5,425/7,234 persistent roles, splits 42–45, three orders, and 60/300 focal local capacities. The five constructed profiles, 64–32 MLP, five rounds and five local epochs, weighted FedAvg, and Task 1 fitting-only preprocessing agree with code. |
| Replay and scoring | PASS | RBR's two-stage allocation, fixed replay loss for allocation methods, protected quotas and CBRS population-only comparison agree with the implementation. DER++ was not evaluated. Merged-Scan probabilities are summed before argmax; original cohorts remain. The three orders are R/F/L/V, F/R/V/L, and L/V/F/R. |
| Statistics and headline results | PASS | Ten training seeds, averaging orders within seed before paired Student t intervals, agree with archived analysis. Main gains of 1.53 and 5.06 points over class-balanced replay are for merged-Scan scoring. The conclusion correctly limits the claim. |
| Abstract wording | FAIL — scope | The unqualified CBRS "outperforms" statement is too broad: merged-Scan retention and Slowloris gains are supported on split 42; exact-type macro-F1 is not conclusive and filtered worst-client intervals include zero. |
| Duplicate exclusions | PASS — prior prediction audit | Excluding 9–16 rows preserved the principal federated gains over class-balanced replay; worst-client inferences changed. This does not establish capture, session, or physical-station independence. The complete rescore is not packaged as a repository command. |
| OCPP | PASS — archived evidence | 98.30/98.37/98.03% macro-F1 (RBR/class-balanced/CBRS); the nominal RBR–CBRS interval excludes zero but the 18-comparison adjusted interval does not. The 0.29% false-alarm figure is 22/7,470 predictions of the same 249 benign flows. This is a separate published corpus, not verified station-independent testing. |
| Public code availability | PARTIAL | On 23 November GitHub reported PUBLIC, with main as default. The RBR allocator, CBRS configuration, Scan analysis and additional split manifests checked were on full-multiclass-comparison at f143310aed76cd4d55a6e1b82d17cca57e5e0653, not on main. The local table/figure handoff and OCPP validation source were not on either checked remote tree. |
| Full independent reproduction | NOT VERIFIED | Numerical report regeneration from compact per-run records is verified locally. Fresh installation, permitted raw artifact access and dataset-to-results reproduction have not been verified. |

Relative to November 17, the three table sources differ only by line endings and the two figure assets are identical. The November 23 export reworks prose and references, adds the duplicate-exclusion paragraph, scopes the 57/59 source-file overlap to fitting/evaluation, adds the false-alarm numerator/denominator, and changes the availability statement from private to public. No change was needed to the numerical reference assets. The supplied export is six pages.

To regenerate the evidence, use the commands in the repository README. Numerical verification does not rerun training or verify that a third party can obtain all original per-example checkpoints. The original dataset and the paper itself are maintained outside GitHub.
