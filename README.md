# EVSE federated continual learning: multiclass comparison

The requested full study is complete: **10 training seeds, three attack orders, federated and centralized environments, seven methods**, with 84 calibration-only trials and 420 evaluated runs. Supplied additional datasets were excluded as instructed. Original no-replay pilot evidence remains preserved.

Read [the results](outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md), [the protocol](docs/research/Full_Comparison_Protocol_2026_10_06.md), and [verification](outputs/multiclass_full_comparison/verification.json).

## Methods

No replay, uniform replay 60 per client, protected replay 60 per client, EWC, A-GEM with Adam (documented adaptation), joint/offline reference, and FedProx/no replay. Centralized replay uses 300 total slots to match the five-client system budget. The MLP uses 64/32 hidden units, ReLU, Adam and five local epochs per round. No aggressive gradient clipping is applied.

## Evidence

Per-run and per-client metrics, per-order summaries, paired contrasts, per-class supports/AUROC/AP, all calibration trials, split manifests, local loss logs, memory/Fisher provenance, and final models are included in Git. Compressed row-level checkpoint probabilities are distributed in the accompanying evidence ZIP rather than large Git blobs. Raw CSVs/PCAPs, pickle sample caches, and prepared feature tensors are excluded. The archive can be reconstructed with the packaging script after restoring local prerequisites.

## Reproduce

Use an isolated Python environment with `requirements-multiclass.txt`. The exact recorded versions are in each experiment's protocol JSON. Obtain the original CICEVSE2024 network-flow CSVs under `data/official/network_traffic` with filenames/directories preserved. Library and platform changes may change exact numeric results.

```powershell
$env:PYTHONPATH = "$PWD/src"
python -m unittest discover -s tests -p 'test_*comparison.py' -v
python -m unittest discover -s tests -p test_multiclass_pilot.py -v
python scripts/run_full_multiclass_comparison.py
python scripts/report_full_multiclass_comparison.py
python scripts/verify_full_multiclass_comparison.py
```

For a fresh experiment, copy the configuration and use a new output directory, preserving published evidence. To verify published model/probability evidence locally, restore checkpoint probabilities from the evidence ZIP and recreate original local prepared tensors; the `--prepare-only` runner path recreates tensors from matching original raw inputs, subject to inventory/source checks. Prepared tensors are deliberately not distributed. Published completion stamps represent original completed jobs; use a fresh output directory to retrain instead of resuming them.

## Interpretation

The user authorized proceeding despite imbalance. Only 16 original benign evaluation flows are available; FPR at the zero-benign client is undefined. These limitations are disclosed rather than silently repaired. Ten seeds vary training randomness on one fixed split, not ten independent datasets. Separately calibrated environments/order settings affect interpretation of the federated-centralized interaction. All claims must follow the measured protected-versus-uniform and station-level results.

The target manuscript venue is IEEE Networking Letters (four pages). This repository is reproducibility evidence, not a claim that the study is publication-ready.
