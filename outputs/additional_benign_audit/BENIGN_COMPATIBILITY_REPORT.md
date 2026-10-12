# Additional benign archive audit

The two supplied ZIP files are byte-identical and count as one dataset.

Three CSV files contain 163,570 rows, with 163,570 exact unique rows across the combined files. Exact-row uniqueness does not establish independent sessions or real-world provenance.

| File | Rows | Columns | Label values | Shared CICEVSE feature names |
|---|---:|---:|---|---|
| Benign/benign_1.csv | 17,142 | 69 | {'0': 17142} | dst_port, src_port |
| Benign/benign_2.csv | 70,902 | 69 | {'0': 70902} | dst_port, src_port |
| Benign/benign_3.csv | 75,526 | 69 | {'0': 75526} | dst_port, src_port |

## Compatibility decision

Do not concatenate these CSVs into the current attack/benign experiment. Only src_port and dst_port overlap with the CICEVSE input schema; filling the other flow features with zeros or missing values would allow the model to distinguish data sources instead of attacks.

The CSVs include OCPP action indicators, payload/message measurements, cumulative session measurements, precomputed z-scores, and anomaly/detection flags. No README, capture provenance, extraction script, session identifier, raw PCAP, or label definition is included. Label 0 appears in every row; its interpretation as benign currently comes from the supplied filenames/user description, not an independently documented mapping.

Across the files, the cumulative packets_per_session counter equals one five times and drops three times; session_duration shows the same three resets. This suggests five contiguous counter segments, not proof of five independent physical sessions. Randomly splitting correlated messages from the same sequence would not establish independent held-out traffic. Capture/session provenance is needed to define appropriate grouping.

## Next usable paths

1. Obtain raw captures and extraction documentation, then extract the same flow features with consistent settings for both benign and attack data. Confirm whether observations are captured, simulated, or transformed, and retain source/session groups for splitting.
2. Alternatively, use a complete OCPP dataset with matching benign and attack schemas in a separately specified study. Do not rename session/message fields into flow fields without verifying definitions, units, aggregation boundaries, and extraction settings.

Treat precomputed detection flags as potential target shortcuts and upstream z-scores as a preprocessing-provenance concern. Independent fitting/calibration/evaluation roles should be assigned after a compatible representation and session/capture grouping are defined; fit preprocessing using Task-1 fitting data only.

The existing pilot and publication package have not been modified. Source hashes, complete schema differences, missingness, duplicates, and continuity indicators are recorded in audit.json.
