# Locked validation extension design

12 November 2026. This is a separate prospective extension; no frozen study or current paper is overwritten. All outcomes, including losses, will be retained. No teacher mechanism, architecture search or evaluation-directed retuning is permitted.

## Two validation tracks

1. CICEVSE2024 source-file holdout: reuse the original fixed sample and five constructed clients. For each class, choose one complete source filename for evaluation by a fixed seeded hash. Assign fitting/calibration only among remaining files. Calibration may share a source file with fitting, but evaluation must not share source files with either. Remove evaluation feature vectors identical to development vectors and report removals. This is source-file separation, not a guarantee of independent underlying captures.
2. Independent Federated OCPP 1.6 dataset (Zenodo 14887131): use the TCP/IP Combined CSVs only; do not double-count the publisher's client copies. Repartition rather than assuming its published row split is session-independent. Group canonical bidirectional endpoint/port/protocol tuples; merge groups linked by duplicate feature vectors. Remove exact feature duplicates globally. No group may cross fitting/calibration/evaluation. Use 55/15/30 group-level role assignment, seed 712, with predeclared eligibility requiring every class in all roles and at least 200 independent evaluation benign flow rows. Group size and dependence remain reported; this is TCP-connection grouping, not proof of independent captures or charging sessions.

The independent dataset has a different feature schema and attacks. Train a fresh 64/32 MLP on that schema; do not append unrelated benign rows to the CICEVSE2024 model or pretend this is zero-shot transfer. Exclude flow IDs, addresses, ports, absolute timestamps and Total Connection Flow Time from model inputs. Fit transformations only on first-task fitting rows, then freeze. Deduplication and grouping use metadata only and precede training.

## Comparisons and rarity

For each track compare class-balanced allocation, CBRS population under the shared replay loss, and three RBR group definitions. Original groups: (a) Slowloris + ICMP fragmentation, (b) ICMP flood, (c) their union. Independent groups: (a) denial of charge/idTag manipulation, (b) charging-profile manipulation, (c) their union. On the independent dataset only, keep a deterministic 20% of fitting rows from the two designated minority attack classes. Calibration/evaluation class counts are not downsampled. This explicitly constructed fitting imbalance tests changing protected-class definitions; it is not a claim of naturally occurring prevalence or temporal rarity drift.

Use memory 60/client, pooled memory 300; five constructed client profiles; the same four-cohort 3-order pattern, 10 paired training seeds, both federated and pooled environments. The independent dataset's four attack types form four cohorts. Learning rate 0.003, ReLU/Adam, five epochs/round, five rounds/task, batch 128, weight decay 0.0001, no gradient clipping. No teacher. Keep all settings fixed except replay fraction 0.25/0.50 and RBR rare quota 0.10/0.20, selected using mean-checkpoint exact-type calibration macro recall. Use one fixed calibration initialization distinct from evaluation seeds, consistent with the original comparison's criterion; selection noise remains a limitation.

There are 16 calibration candidates per environment/order: 2 balanced, 2 CBRS, 4 for each of three RBR groups. Per track: 96 calibration fits before 300 evaluation runs. Evaluation seeds are 500–509 for source-file holdout and 600–609 for independent data; calibration seeds 490 and 590 respectively. All candidates and selected configurations must be recorded before any evaluation starts in that track. Ties use candidate order. Do not choose a successful group, metric or order after evaluation.

## Outcomes and inference

Primary detection view: exact-type labels. Report old-cohort accuracy, forgetting, macro precision/recall/F1, each attack's precision/recall, protected-group macro recall, Slowloris where present, worst-client macro recall and benign false-positive counts/rates. Report one-vs-rest AUROC/AP. Original merged-Scan scoring remains a secondary view for continuity. The independent attacks have no equivalent six-scan merger.

Compute paired intervals over ten within-seed order averages. For each RBR group versus both baselines, report all differences and nominal 95% intervals. Also give Bonferroni-adjusted simultaneous intervals for the primary three outcomes (old accuracy, macro-F1, declared-group recall), across six contrasts × three outcomes = 18 per track. Do not claim superiority if the prespecified evidence does not support it. Failure to prove an improvement is a valid outcome, not a reason to keep tuning against the evaluation set.

Benign false-positive intervals must not treat ten predictions of the same row as independent new examples. Report per-run counts and descriptive seed variability, plus a flow-level descriptive Wilson interval for one predeclared seed; connection dependence and balanced sampling limit population interpretation.

## Dataset search and fallback

Official CICEVSE2024 confirms the existing network/power/host modalities. Independent OCPP sources found: Zenodo Federated OCPP 1.6 (2025), and Al-Mhiqani's OCPP-centric hybrid dataset. The latter's semantic message-level schema is incompatible with the original NFStream inputs and will be audited rather than blindly concatenated. CICIDS2017 and CSE-CIC-IDS2018 are generic network alternatives, not EVSE benign captures. If no suitable EVSE benign evaluation survives grouping/support checks, explicitly report that and ask for additional compatible independent benign recordings. No synthetic or duplicated rows count as new evaluation support.
