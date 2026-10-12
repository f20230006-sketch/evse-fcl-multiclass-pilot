# Response about the excluded benign datasets

**Yes, one supplied source has substantially more nominally benign traffic, but its files are not directly compatible with the current attack data.** No new data were added to the completed study.

| Supplied files | Observations | What they add | Why excluded |
|---|---:|---|---|
| CICIDS2017-OCPP-Centric-Benign.zip and Benign.zip | 163,570 rows total across three CSVs | Substantially more nominal benign rows | ZIPs are identical; one source, not two. The 69-column OCPP message/session schema overlaps current 86-field CICEVSE data only on port names. Capture grouping and matching extraction are not established. |
| EVSE-A-Charging-Benign.csv | 14 rows | Zero new rows | Byte-identical to the existing project CSV. |
| EVSE-A-idle-benign.csv | 68 rows | Zero new rows | Byte-identical to the existing project CSV. |

The OCPP source provided by the user is the [OCPP-Centric Hybrid Testbed for EV Charging dataset](https://github.com/Al-Mhiqani/OCPP-Centric-Hybrid-Testbed-for-EV-Charging-Dataset-). The `CICIDS2017` prefix on one local ZIP filename should not be treated as evidence that its contents use CICIDS2017 flow features; its SHA-256 matches the supplied OCPP `Benign.zip` exactly. Source attribution here follows the earlier source audit; no new capture provenance is asserted.

All supplied OCPP labels are 0, interpreted as benign from the source/user description. Exact uniqueness of 163,570 rows does not establish that they are independent flows or sessions. The existing audit finds only a small number of counter segments. The CSVs also contain upstream z-scores and anomaly flags, which require preprocessing/feature provenance checks.

Using these files to support the present false-alarm analysis requires original captures and consistent flow extraction, verified feature definitions and units, capture/session-separated fitting/calibration/evaluation roles, and a domain-shift-aware protocol. Filling absent attack-data features with zeros would introduce source shortcuts. Alternatively, a separately specified OCPP study could use benign and attack data with a shared representation; the accompanying OCPP attack archives have not been validated.

Supporting evidence remains in `outputs/additional_benign_audit/audit.json`, `cicevse_download_comparison.json`, `BENIGN_COMPATIBILITY_REPORT.md` and `SOURCE_AND_CICEVSE_FOLLOWUP.md`. The present CICEVSE benign count remains 82, including only 16 persistent evaluation examples.
