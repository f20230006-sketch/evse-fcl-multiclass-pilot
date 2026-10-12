"""Publish follow-up metadata and package all raw original/follow-up evidence."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT if (ROOT/'.git').exists() else ROOT/'work/evse-fcl-multiclass-pilot'
ARCHIVE=ROOT/'outputs/FCL_Oct07_Followup_All_Deliverables_2026_10_12.zip'
OUT=ROOT/'outputs/replay_followup_report'
SOURCE_FILES=['src/evse_ids/replay_followup.py','scripts/run_replay_followup.py','scripts/report_replay_followup.py','scripts/verify_replay_followup.py','scripts/verify_followup_reports.py','scripts/summarize_replay_followup.py','scripts/report_joint_diagnostics.py','scripts/audit_joint_fit_quality.py','scripts/audit_joint_feature_aliases.py','scripts/package_replay_followup.py','configs/replay_followup_essential.json','configs/replay_followup_sweep.json','tests/test_replay_followup.py','requirements-followup.txt','docs/research/Replay_Followup_Protocol_2026_10_12.md','docs/research/Excluded_Datasets_Reply_2026_10_12.md']
SOURCE_FILES+=['WORKSPACE_INDEX.md','docs/research/Replay_Followup_Checkpoint_2026_10_12.md']

INDEX='''# Deliverables responding to the 7 October supervisor email

Prepared 12 October 2026. Start with **outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md** and the draft email in the same directory.

| Request | Deliverables | Status |
|---|---|---|
| 1. Class-balanced replay 60 | replay_followup_essential/; type_summary.csv and paired_intervals.csv | 12 calibration trials, 60 evaluation runs; verified |
| 2. Joint-training diagnosis | joint_diagnostics/ PNG/PDF and count/normalized CSV matrices, per-type confusion consistency, fit-quality and exact-feature audits | All 60 joint models analyzed; no training-label merges |
| 2. Family-level results | replay_followup_report/family_per_run_metrics.csv, family_summary.csv, family_checkpoint_metrics.json | Existing task groups; summed probabilities and mapped winning-type conventions both reported |
| 3. Memory sweep | replay_followup_sweep/; memory_sweep_*.png/.pdf; summary/paired CSVs | 72 calibration trials, 360 evaluation runs |
| 4. EWC/A-GEM | supervisor summary section 4; paired_intervals.csv | Four requested metrics and matched-seed intervals against protected replay |
| 5. Every attack order | type_per_order_summary.csv; paired_intervals.csv; FOLLOWUP_RESULTS.md | All three orders, both environments and every tested replay capacity |
| 6. Excluded datasets | docs/research/Excluded_Datasets_Reply_2026_10_12.md; additional_benign_audit/ | Source, counts, duplicate evidence, compatibility and independence limits |
| Implementation/protocol | src/, scripts/, configs/, tests/, requirements-followup.txt; Replay_Followup_Protocol_2026_10_12.md | Reproducible runner with calibration/source/input guards |
| Raw evidence | original/full and both follow-up runs/calibration directories | Models, every saved NPZ prediction, logs, metrics, memory audits, completion stamps |
| Checks | verification.json in each follow-up directory; report_verification.json | Models/predictions, roles, budgets, feasible quotas, paired arithmetic and confusion counts |
| Correspondence | SUPERVISOR_REPLY_DRAFT.txt | Draft only; not sent |

Short output paths above are relative to `outputs/` in this archive. The original 6 October study is preserved in `outputs/multiclass_full_comparison/`. There are 840 combined evaluations; 420 are new. The original forgetting pilot and earlier audit evidence are preserved. Historical binary/logistic claims are not used to interpret this follow-up.

## Read raw results

Each evaluated `runs/order/environment/method/seed_*/` directory contains `results.json`, `final_model.pt`, `training_log.json`, `memory_audit.json`, `complete.json` and task checkpoint NPZ files. NPZ keys are `sample_index`, `y_true`, `y_pred`, `probability`. Indices and output columns use the original order's `splits/order_*/split_manifest.csv` and `class_mapping.json`. The follow-up reuses these original split files rather than allocating new rows. Every attempted calibration trial is in `calibration/`; calibration never emits evaluation prediction files.

Confusion counts repeat the fixed test observations across seeds/orders. All confidence intervals describe paired training randomness on one split. Family correctness differs from exact attack-type correctness; summed-family probabilities may change the winning prediction whereas mapped-type scoring retains it.

## Exclusions and integrity

Original input CSV/PCAP data, pickle sample caches, prepared feature tensors, Git metadata/credentials, dependency installation folders and Python caches are excluded. These are not raw experiment results. All saved row-level prediction NPZs are included in this ZIP; Git retains the lighter code/metadata/model evidence. The full archive does not need nested copies of earlier ZIPs.

`deliverables_manifest.json` hashes every payload member; `archive_validation.json` verifies member count, CRC and every digest. Verify after extraction with `python verify_deliverables_manifest.py`. Original full-model verification additionally needs the matching prepared feature tensors, recreated locally from the original data with the documented frozen protocol. Integrity verification alone does not reproduce training.

The private repository draft PR remains https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot/pull/1 . Repository access and transfer permission for this large ZIP must be granted separately. No email, dataset import, new training-label merge, manuscript submission or PR merge is performed by packaging.
'''

VERIFY='''from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
m=json.loads((root/'deliverables_manifest.json').read_text(encoding='utf-8'))
bad=[]
for row in m['files']:
 p=root/row['path']
 if not p.is_file() or p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
print(json.dumps({'checked':len(m['files']),'mismatches':bad},indent=2))
raise SystemExit(bool(bad))
'''

def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    for name,expected in [('replay_followup_essential',60),('replay_followup_sweep',360)]:
        folder=ROOT/'outputs'/name
        assert json.loads((folder/'completion.json').read_text())['evaluation_runs']==expected
        assert json.loads((folder/'verification.json').read_text())['status']=='passed'
    assert json.loads((OUT/'report_verification.json').read_text())['status']=='passed'
    for relative in SOURCE_FILES:
        target=REPO/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if (ROOT/relative).resolve()!=target.resolve():shutil.copy2(ROOT/relative,target)
    folders=['replay_followup_essential','replay_followup_sweep','replay_followup_report','joint_diagnostics','additional_benign_audit']
    for name in folders:
        for p in (ROOT/'outputs'/name).rglob('*'):
            if not p.is_file() or p.suffix in {'.npz','.pkl','.cache_key','.zip','.sha256'} or p.name in {'prepared_local_only.pt','deliverables_manifest.json','archive_validation.json'}:continue
            target=REPO/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
            if p.resolve()!=target.resolve():shutil.copy2(p,target)
    readme='''# EVSE multiclass federated continual learning

The 7 October follow-up is complete: class-balanced replay, joint confusion diagnostics, a 60/120/300 memory sweep, paired EWC/A-GEM comparisons, every attack order, and an excluded-dataset reply. **84 new calibration trials and 420 new evaluations**, alongside the original 420 evaluations. Original evidence is preserved.

Read the [follow-up supervisor summary](outputs/replay_followup_report/SUPERVISOR_FOLLOWUP_SUMMARY.md), [full tables](outputs/replay_followup_report/FOLLOWUP_RESULTS.md), [joint confusion report](outputs/joint_diagnostics/JOINT_CONFUSION_REPORT.md), [follow-up protocol](docs/research/Replay_Followup_Protocol_2026_10_12.md), [dataset reply](docs/research/Excluded_Datasets_Reply_2026_10_12.md), and [deliverables index](DELIVERABLES_INDEX_2026_10_12.md). The [original results](outputs/multiclass_full_comparison/FULL_COMPARISON_RESULTS.md) remain available.

At memory 60, class-balanced replay exceeds protected replay on old-type retention; protected replay has higher rare-type recall. Benefits depend on metric, capacity and attack order. Do not claim uniform dominance or intrinsic type indistinguishability. Only 16 benign evaluation flows are available, and benign-starved FPR is undefined. Seeds vary training randomness on one fixed split. Joint is an empirical offline reference.

## Evidence and reproduction

Code/configs, split manifests, all calibration trials, per-run/station metrics, diagnostics, final weights and verification are in Git. All raw compressed checkpoint predictions are distributed in the accompanying deliverables ZIP. Raw datasets, prepared feature tensors and input caches are excluded. [TESTING.md](TESTING.md) records checks; [TODOS.md](TODOS.md) records scientific work remaining.

Install `requirements-followup.txt` in an isolated environment. Obtain the matching original CICEVSE flow CSVs. The full comparison `--prepare-only` path recreates the original prepared features, subject to protocol/input checks. Follow-up protocols fingerprint exact original source and prepared-input bytes; platform/library changes can affect serialization and numeric results.

```powershell
$env:PYTHONPATH = "$PWD/src"
python scripts/run_replay_followup.py --config configs/replay_followup_essential.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_essential
python scripts/run_replay_followup.py --config configs/replay_followup_sweep.json
python scripts/verify_replay_followup.py --output-dir outputs/replay_followup_sweep
python scripts/report_replay_followup.py --family
python scripts/verify_followup_reports.py
python scripts/summarize_replay_followup.py
```

Published completed-case stamps are original evidence. To retrain intentionally, use fresh original-study and follow-up output directories, updating `reference_output` to the fresh original study; keep published results untouched. Library versions/source/input fingerprints are recorded in the experiment protocols. No new merged-label model or manuscript is claimed.
'''
    (REPO/'README.md').write_text(readme,encoding='utf-8');(REPO/'VERSION').write_text('0.2.1\n',encoding='utf-8')
    old=(REPO/'CHANGELOG.md').read_text();entry='## 0.2.1 - 2026-10-12\n\nAdd class-balanced replay and memory sweeps; diagnose joint-type confusion and fitting quality; report prespecified family scores, paired method/order intervals and excluded-data provenance. Preserve all original runs and expose the retention/rare-recall trade-off.\n\n'
    if '## 0.2.1' not in old:(REPO/'CHANGELOG.md').write_text(old.replace('# Changelog\n\n','# Changelog\n\n'+entry),encoding='utf-8')
    (REPO/'TESTING.md').write_text('Seventeen relevant unit tests passed (seven pilot, six original methods, four balanced-allocator tests). All 420 new evaluation models and checkpoint probabilities are independently checked against the original frozen inputs; original 420-run verification is preserved. Report verification independently checks every paired interval, all joint confusion counts, and mapped-family correctness monotonicity. Inspect verification JSONs for exact row counts.\n',encoding='utf-8')
    (REPO/'DELIVERABLES_INDEX_2026_10_12.md').write_text(INDEX,encoding='utf-8')
    (OUT/'DELIVERABLES_INDEX.md').write_text(INDEX,encoding='utf-8');(OUT/'verify_deliverables_manifest.py').write_text(VERIFY,encoding='utf-8')
    (REPO/'outputs/replay_followup_report/DELIVERABLES_INDEX.md').write_text(INDEX,encoding='utf-8')
    repo_rows=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(REPO.rglob('*')) if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and 'tmp' not in p.relative_to(REPO).parts and p.name!='package_manifest.json']
    (REPO/'package_manifest.json').write_text(json.dumps(repo_rows,indent=2),encoding='utf-8')
    sources={r['path']:REPO/r['path'] for r in repo_rows};sources['package_manifest.json']=REPO/'package_manifest.json'
    for name in ['multiclass_full_comparison',*folders,'multiclass_no_replay_pilot']:
        for p in sorted((ROOT/'outputs'/name).rglob('*.npz')):sources[p.relative_to(ROOT).as_posix()]=p
    sources['DELIVERABLES_INDEX.md']=OUT/'DELIVERABLES_INDEX.md';sources['SUPERVISOR_REPLY_DRAFT.txt']=OUT/'SUPERVISOR_REPLY_DRAFT.txt';sources['verify_deliverables_manifest.py']=OUT/'verify_deliverables_manifest.py'
    rows=[{'path':k,'bytes':p.stat().st_size,'sha256':digest(p)} for k,p in sorted(sources.items())]
    manifest={'date':'2026-10-12','files':rows,'input_features_excluded':True,'raw_checkpoint_predictions_included':True}
    (OUT/'deliverables_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in rows:z.write(sources[row['path']],row['path'])
        z.write(OUT/'deliverables_manifest.json','deliverables_manifest.json')
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        for row in rows:
            payload=z.read(row['path']);assert len(payload)==row['bytes'] and hashlib.sha256(payload).hexdigest()==row['sha256'],row['path']
    validation={'status':'passed','zip_crc':'passed','payload_files':len(rows),'hash_mismatches':0,'raw_npz_files':sum(p.suffix=='.npz' for p in sources.values()),'new_evaluation_runs':420,'combined_evaluation_runs':840}
    (OUT/'archive_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    with zipfile.ZipFile(ARCHIVE,'a',compression=zipfile.ZIP_DEFLATED) as z:z.write(OUT/'archive_validation.json','archive_validation.json')
    ARCHIVE.with_suffix('.zip.sha256').write_text(f'{digest(ARCHIVE)}  {ARCHIVE.name}\n',encoding='utf-8')
    print(json.dumps({'archive':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,**validation},indent=2))

if __name__=='__main__':main()
