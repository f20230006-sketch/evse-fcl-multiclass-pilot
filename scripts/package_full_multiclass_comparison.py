"""Publishable evidence package; never includes raw or prepared feature caches."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="outputs/multiclass_full_comparison")
    parser.add_argument("--repository-dir",default="work/evse-fcl-multiclass-pilot")
    args = parser.parse_args()
    evidence,repository = ROOT/args.output_dir,ROOT/args.repository_dir
    assert json.loads((evidence/"completion.json").read_text())["evaluation_runs"]==420
    assert json.loads((evidence/"verification.json").read_text())["status"]=="passed"
    files = ["src/evse_ids/full_comparison.py","src/evse_ids/continual_ablation.py","scripts/run_full_multiclass_comparison.py",
             "scripts/report_full_multiclass_comparison.py","scripts/verify_full_multiclass_comparison.py",
             "scripts/package_full_multiclass_comparison.py","configs/multiclass_full_comparison.json",
             "scripts/run_full_comparison_supplementary_pool.py","tests/test_full_comparison.py","docs/research/Full_Comparison_Protocol_2026_10_06.md"]
    for relative in files:
        destination = repository/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/relative,destination)
    for source in evidence.rglob("*"):
        if not source.is_file() or source.suffix not in {".json",".csv",".md",".pt"} or source.name=="prepared_local_only.pt":
            continue
        destination = repository/args.output_dir/source.relative_to(evidence)
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,destination)
    readme = """# EVSE federated continual learning: multiclass comparison

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
"""
    (repository/"README.md").write_text(readme,encoding="utf-8")
    (repository/"VERSION").write_text("0.2.0\n",encoding="utf-8")
    (repository/"CHANGELOG.md").write_text("# Changelog\n\n## 0.2.0 - 2026-10-06\n\nComplete the multiclass full comparison with 10 training seeds, three orders, two environments and seven methods; add calibration-only grids, matched system replay budgets, station metrics and independently verified checkpoint/model evidence. Preserve the pilot and disclose the user's benign-support override.\n",encoding="utf-8")
    (repository/"TESTING.md").write_text("Thirteen unit tests cover the pilot and full-comparison methods. Artifact verification checks all 420 evaluated cases, saved final models, checkpoint probabilities, fitting/calibration/evaluation boundaries, memory budgets and Task-1 preprocessing. Historical parent-project tests require scikit-learn and are outside this isolated package.\n",encoding="utf-8")
    (repository/"TODOS.md").write_text("# Remaining scientific work\n\n- Obtain adequate independent benign evaluation coverage; current runs use the explicitly authorized original-data limitation.\n- Assess unseen-capture/station generalization with a separately specified holdout.\n- Review measured results with the supervisor before finalizing four-page manuscript claims.\n",encoding="utf-8")
    rows = [{"path":p.relative_to(repository).as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(repository.rglob("*")) if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
            and "tmp" not in p.relative_to(repository).parts and p.name!="package_manifest.json"]
    assert not any(r["path"].endswith((".pkl",".cache_key","prepared_local_only.pt")) for r in rows)
    (repository/"package_manifest.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    path = ROOT/"outputs/full_multiclass_comparison_repository.zip"
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED) as archive:
        for row in rows:
            archive.write(repository/row["path"],row["path"])
        archive.write(repository/"package_manifest.json","package_manifest.json")
        prediction_manifest = []
        for prediction in sorted(evidence.rglob("*.npz")):
            relative = (Path(args.output_dir)/prediction.relative_to(evidence)).as_posix()
            archive.write(prediction,relative)
            prediction_manifest.append({"path":relative,"bytes":prediction.stat().st_size,"sha256":hashlib.sha256(prediction.read_bytes()).hexdigest()})
        archive.writestr("prediction_archive_manifest.json",json.dumps(prediction_manifest,indent=2))
    print(json.dumps({"repository":str(repository),"files":len(rows),"archive":str(path),"archive_bytes":path.stat().st_size},indent=2))


if __name__=="__main__": main()
