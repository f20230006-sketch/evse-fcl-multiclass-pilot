# EVSE federated continual learning: multiclass first check

This repository contains the supervisor-requested no-replay forgetting pilot, not a completed full comparison.

The 64/32 ReLU MLP with Adam showed large drops in old attack-type accuracy across three seeds. Benign test support remains insufficient: only 16 genuine benign test flows per seed, and none at the benign-starved client. These are diagnostic results, not evidence of protected replay effectiveness.

Read `outputs/multiclass_no_replay_pilot/SUPERVISOR_FIRST_CHECK.md` and `docs/research/Multiclass_Pilot_Protocol_2026_10_06.md`. Split manifests, calibration trials, per-client metrics, checkpoint probabilities, and model weights are included. Raw traffic and local caches are excluded.

## Reproduce

1. Use Python 3.11 or later; install `requirements-multiclass.txt` in a virtual environment.
2. Obtain the official CICEVSE2024 network-flow CSVs and arrange them under `data/official/network_traffic` with the EVSE-A/EVSE-B filename and directory organization preserved. Input-file inventory and source-file/source-row identifiers are saved with the evidence. Do not merge host-event data into the flow schema.
3. Set `PYTHONPATH` to this repository's `src` directory and run `python -m unittest discover -s tests -p test_multiclass_pilot.py -v`.
4. Run `python scripts/run_multiclass_no_replay_pilot.py --allow-limited-benign-diagnostic` to reproduce the explicitly limited first check. Without the flag the runner stops on benign support.
5. Run `python scripts/verify_multiclass_pilot.py` and `python scripts/report_multiclass_pilot.py` after reproducing the sample caches. The verifier reconstructs final predictions from frozen preprocessing and saved model states, and independently checks checkpoint accuracy against row-level predictions.

The recorded run used Python/runtime versions in `protocol_before_evaluation.json`. Reproduction requires the same source dataset. Training is deterministic on the recorded CPU setup; exact equality across different library/platform versions is not guaranteed.

## Gate

Do not run a full replay/EWC/DER++/joint or centralized comparison before presenting the first-check result to the supervisor and resolving the benign-data evaluation design. Reconnaissance initial learning is also weak and must be disclosed. The ten-seed/three-order study and four-page manuscript are later steps.

## Data and security

This package includes split identifiers and derived experimental evidence, not raw CSVs or PCAPs. Follow the original dataset's distribution terms. No access tokens, passwords, private mail, or local raw-feature caches are included.
