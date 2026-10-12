# Benign data source and CICEVSE follow-up

## CICEVSE files supplied from Downloads

| File | Rows | New rows beyond existing project files |
|---|---:|---:|
| EVSE-A-Charging-Benign.csv | 14 | 0 |
| EVSE-A-idle-benign.csv | 68 | 0 |

Each supplied CSV has the exact same SHA-256 hash, file length, column order, and row contents as its corresponding file already in `data/official/network_traffic/EVSE-A/csv`. These are replacement copies of the existing data, not additional observations. The available CICEVSE benign total remains 82, with 16 unique evaluation rows per seed under the corrected protocol. Full comparison and training data are unchanged.

Exact comparison evidence is recorded in `cicevse_download_comparison.json`.

## OCPP archive source now identified

The user provided the Benign.zip source from [Al-Mhiqani's OCPP-Centric Hybrid Testbed repository](https://github.com/Al-Mhiqani/OCPP-Centric-Hybrid-Testbed-for-EV-Charging-Dataset-).

The repository README describes a hybrid physical/virtual testbed incorporating real OCPP-compliant chargers, physical EVSE hardware, simulated EVs, and CSMS controllers. It describes message semantics, operational state transitions, timing, payload complexity, and network features. This is the authors' description; the supplied CSVs still do not establish per-row physical/simulated provenance, capture grouping, or feature-extraction settings.

The source repository also lists attack archives for ARP/MiTM, malformed payloads, packet dropping, and replay. They could support a separate, consistently represented OCPP study after checking their schemas, sample counts, sequence grouping, and preprocessing provenance. Those archives have not been downloaded or validated in this follow-up. Switching the main experiment to them would change its dataset and attack sequence, requiring an explicit protocol revision.

The source clarification does not resolve the earlier schema mismatch: the local OCPP benign CSVs have 69 columns and 163,570 exact unique rows, while the CICEVSE CSVs have 86 raw feature columns. Only src_port/dst_port names overlap. Artificially filling absent features would introduce source-based shortcuts. Original captures plus matching extraction settings are required for a defensible common flow representation.

The large OCPP row count does not establish independent sessions. Counter resets suggest a small number of contiguous sequences, so fitting/evaluation grouping must be established before using them for false-alarm estimates. Precomputed anomaly flags and z-scores require extraction documentation and appropriate feature exclusions/refitting.

## Current decision

Do not merge the supplied OCPP CSVs with the CICEVSE experiment. Do not append the supplied CICEVSE files as new data, because they duplicate existing records. The next viable routes are compatible additional CICEVSE-like captures with consistent feature extraction, or an explicitly revised study using both benign and attack data from the OCPP source.
