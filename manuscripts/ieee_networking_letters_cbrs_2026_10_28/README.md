# Rare-Reserved Balanced Replay manuscript

Four-page IEEE Networking Letters manuscript, prepared 28 October 2026, with a 91-word abstract and 18 references. It incorporates the published CBRS population baseline and retains RBR as the consistent method name. Author and affiliation fields are intentionally present for confirmation, as requested; no internal working header is included.

The CBRS comparison uses original split 42, memory 60 per client/300 pooled, ten training seeds and three orders. Shared task-boundary training and uniform replay isolate the memory population rule. Both scoring views and all losses are retained. The exact-type federated old-accuracy and Slowloris intervals include zero; centralized order 2 favors CBRS on Slowloris. Numerical tables are generated from verified CSVs.

Files: main.tex/main.pdf; tables/; figures/ with plotted data; evidence_manifest.json; verification.json; visual_review.json. No email reply is included. Compile main.tex twice with standard pdfLaTeX and IEEEtran, amsmath, amssymb, graphicx, booktabs, cite and url. No margin or body-font reduction is used.

Implementation details and reproduction: docs/research/Implementation_Details_2026_10_28.md in https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot (private; access required). Dataset: https://www.unb.ca/cic/datasets/evse-dataset-2024.html . CBRS primary source: https://proceedings.mlr.press/v119/chrysakis20a.html . Supplement: https://proceedings.mlr.press/v119/chrysakis20a/chrysakis20a-supp.pdf .
