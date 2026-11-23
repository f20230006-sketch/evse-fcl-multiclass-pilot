# Rare-Reserved Balanced Replay for Federated Continual Intrusion Detection in EV Charging Networks

Research software accompanying a manuscript prepared for IEEE Networking Letters. Overleaf is the authoritative manuscript. See the [November 23 verification and public-branch status](docs/manuscript_verification_2026_11_23.md). No acceptance, publication record, or DOI is claimed.

This study compares local replay allocation policies for continual intrusion detection on EV charging network flows. Five constructed clients train local 64–32 ReLU MLPs and exchange model updates through weighted FedAvg. At each task boundary, RBR reserves up to floor(qB) of B buffer slots for available Slowloris and ICMP-fragmentation fitting examples, then balances the remaining capacity across eligible classes, including benign and remaining rare examples. Allocation is local, without extra allocation messages.

On CICEVSE2024, RBR improves merged-Scan retention and Slowloris recall against class-balanced replay on four constructed role splits. Evidence for exact-type superiority is weaker, and worst-client conclusions are sensitive to exclusion of matching flows. A separate OCPP dataset study is included as supporting evidence; neither study demonstrates deployment or independent physical-station performance.

## Regenerate the paper outputs

Use Python 3.13. From the repository root:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-paper.txt
.venv/Scripts/python scripts/reproduce_paper_results.py --out paper_generated
.venv/Scripts/python scripts/verify_paper_results.py paper_generated paper
```

The output directory must be new. The command recomputes Tables I–III and Figure 2 from per-run evidence, without data downloads, checkpoints, or retraining. It verifies numerical agreement, not byte identity of the plotted PDF. See [what is and is not reproducible](docs/reproducibility.md), the [experiment protocol](docs/experiment_protocol.md), and [dataset acquisition](docs/datasets.md).

- `src/evse_ids/`: training, partitioning and replay policies.
- `configs/` and `scripts/`: original experiment settings, runners and verification.
- `outputs/paper/evidence/`: compact per-run evidence and checksums; older experiment reports retain their original paths.
- `paper/`: manuscript reference table and figure values for verification.
- [Historical README](docs/research/README_BEFORE_PAPER_HANDOFF.md) and [pilot testing record](TESTING.md): preliminary pilot evidence preserved from main.

Cite the research software using [CITATION.cff](CITATION.cff). Original software is available under the [MIT License](LICENSE); see [scope and third-party attribution](NOTICE.md). External datasets and archived artifacts are outside the software license.
