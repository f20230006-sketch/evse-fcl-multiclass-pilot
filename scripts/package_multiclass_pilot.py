"""Build an allowlisted repository package without raw data, caches, or credentials."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="outputs/multiclass_no_replay_pilot")
    parser.add_argument("--repository-dir", default="work/evse-fcl-multiclass-pilot")
    args = parser.parse_args()
    repository = ROOT/args.repository_dir
    evidence = ROOT/args.output_dir
    sources = ["src/evse_ids/__init__.py", "src/evse_ids/multiclass_pilot.py", "src/evse_ids/continual_stable.py",
        "src/evse_ids/data.py", "src/evse_ids/metrics.py", "src/evse_ids/validation.py",
        "scripts/run_multiclass_no_replay_pilot.py", "scripts/report_multiclass_pilot.py",
        "scripts/verify_multiclass_pilot.py", "scripts/package_multiclass_pilot.py",
        "configs/multiclass_no_replay_pilot.json", "tests/test_multiclass_pilot.py", "requirements-multiclass.txt",
        "docs/research/Multiclass_Pilot_Protocol_2026_10_06.md"]
    for relative in sources:
        destination = repository/relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/relative, destination)
    for source in evidence.rglob("*"):
        if source.is_file() and source.suffix in {".csv", ".json", ".md", ".pt"}:
            destination = repository/args.output_dir/source.relative_to(evidence)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    readme = """# EVSE federated continual learning: multiclass first check

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
"""
    (repository/"README.md").write_text(readme, encoding="utf-8")
    (repository/".gitignore").write_text("__pycache__/\n*.pyc\n.venv/\ndata/\ntmp/\n*.pkl\n*.cache_key\n.env\n", encoding="utf-8")
    # Exact bytes are part of the evidence hashes; disable checkout newline conversion.
    (repository/".gitattributes").write_text("* -text\n", encoding="utf-8")
    (repository/"TESTING.md").write_text("Seven pilot unit tests pass. Independent artifact verification checks all checkpoints and saved final models. The parent project's historical test suite could not import scikit-learn in the bundled runtime; this package's tests do not require it. See outputs/multiclass_no_replay_pilot/verification.json.\n", encoding="utf-8")
    rows = [{"path": str(p.relative_to(repository)).replace("\\", "/"), "bytes": p.stat().st_size,
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(repository.rglob("*")) if p.is_file() and ".git" not in p.parts and p.name != "package_manifest.json" and "__pycache__" not in p.parts]
    (repository/"package_manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    zip_path = ROOT/"outputs"/"multiclass_no_replay_pilot_repository.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for row in rows:
            archive.write(repository/row["path"], row["path"])
        archive.write(repository/"package_manifest.json", "package_manifest.json")
    print(json.dumps({"repository_directory": str(repository), "zip": str(zip_path), "packaged_files": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
