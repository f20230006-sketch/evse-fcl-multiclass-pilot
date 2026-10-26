# Final experiment: short findings notes

All 48 calibration fits and 120 evaluation runs are complete. The design was fixed before running and was not changed after evaluation. Verification passed for 120 saved models, 480 checkpoints, 2,365,760 prediction rows and 256 paired comparisons. Merged-Scan scores are primary and recall refers to Slowloris only.

At memory 60 in federated training, balanced + rare achieves 85.52% old accuracy, 14.24% forgetting, 76.62% Slowloris recall and 79.03% worst-client macro recall. Compared with class-balanced, old accuracy improves by 1.53 points (95% interval 0.23–2.84) and Slowloris by 5.06 (1.27–8.84), both significant. Worst-client improvement is 1.06 (-0.07–2.19), not significant. This meets the requested significance pattern averaged over orders; it does not prove equivalence/non-inferiority.

Against protected replay at memory 60, old accuracy and worst-client score improve by 12.68 and 31.87 points, but Slowloris falls by 6.11 points; all three differences are significant. At memory 300, the new method improves all four federated metrics over class-balanced, but loses old accuracy and Slowloris against protected while improving worst-client score. Every memory/order loss appears in INFO.md and paired_intervals.csv. Gains are not significant in every individual order, and exact-type significance conclusions differ in some cases.

At memory 60, new-over-balanced gains do not differ significantly between federated and centralized training. No additional overall federation advantage is established. The previous Slowloris memory-300 federation interaction remains exploratory.

Memory 60/300 means at most 60/300 stored fitting examples per client, not network layers or model parameters. With five clients, centralized storage is 300/1500. The new method first reserves a calibration-selected 10% or 20% rare share, then balances all remaining slots across available original types. Benign has no separate quota. Replay fraction (0.25/0.50) controls minibatch mixing, not storage size.

Only 600 Slowloris, five fragmentation and 16 benign test examples are available on one fixed split. No fragmentation conclusions are made. Intervals describe training-seed uncertainty, not independent stations/captures, and are unadjusted for multiple comparisons. Original cohorts/type-level replay policies are retained under merged scoring.

Send SUMMARY.pdf (two pages) and the small review ZIP. The raw ZIP is a separate evidence bundle; if it exceeds 50 MB, share these notes and the review ZIP instead. Email drafts remain outside both archives. Results are frozen for review before writing.
