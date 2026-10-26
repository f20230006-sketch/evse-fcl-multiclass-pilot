"""Clean final-check archives: small review bundle and complete new raw results."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'outputs/final_scan_analysis'
ALLOWED={'.md','.pdf','.csv','.json','.npz'}

README='''# Final checks — 17 October 2026

Start with **SUMMARY.pdf** (exactly two pages), then **INFO.md** for details. The archive contains results/data/Markdown information only; email drafts and implementation files stay outside it.

Completed: a pooled six-scan Random Forest diagnostic (6 calibration fits, 30 evaluation fits), merged-Scan re-scoring of all 840 existing runs without MLP retraining, individual rare-class and focused-client results, and reconstruction of the 33.33% metric. The Random Forest achieves 34.25% against 16.67% chance, so intrinsic indistinguishability of all six scans is not established. Merged scores are an alternative reporting view pending review.

The small review bundle contains the summary, information, aggregate CSVs/protocols and verification. The full raw-results bundle additionally contains every per-run merged result and compact checkpoint prediction, plus Random Forest predictions and role indices. Original MLP probability files, input data and prepared feature tensors are not duplicated; their original paths and digests are in saved_prediction_input_hashes.json. They remain in the earlier full evidence package/workspace.

In merged_predictions/, checkpoint NPZs contain sample_index, merged y_true and merged y_pred. Final checkpoints additionally contain full merged probabilities. Map IDs using each run's results.json classes; sample indices refer to the unchanged original order's split_manifest.csv. The sum of the six scan probabilities determines the new Scan probability; Slowloris stays separate. Scan spans two original task cohorts, and memories remain the original type-level policies.

rare_classes_*.csv distinguish original_type and merged_scans score spaces. rare_federated_deficits.csv uses centralized minus federated recall. rare_federation_interactions.csv uses (F_protected−F_baseline)−(C_protected−C_baseline); positive values reduce the signed federated deficit. Per-client tables preserve undefined recalls/FPR as N/A where support is absent.

manifest.json hashes all payload members. archive_validation.json verifies ZIP CRC, counts and every SHA-256. Source code/configuration is maintained separately in the research workspace/repository. This bundle contains no manuscript and no email correspondence.
'''

def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def build(raw):
    name='FCL_Final_Checks_Raw_Results_2026_10_17.zip' if raw else 'FCL_Final_Checks_Review_2026_10_17.zip'
    target=ROOT/'outputs'/name;rows=[];sources={}
    for p in sorted(SOURCE.rglob('*')):
        if not p.is_file() or p.suffix not in ALLOWED or 'draft' in p.name.lower():continue
        relative=p.relative_to(SOURCE)
        if not raw and (relative.parts[0]=='merged_predictions' or (relative.parts[0]=='random_forest' and (p.suffix=='.npz' or p.name.endswith('_role_indices.json') or any(part.startswith('seed_') for part in relative.parts)))):continue
        sources[relative.as_posix()]=p
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for key,p in sources.items():
            z.write(p,key);rows.append({'path':key,'bytes':p.stat().st_size,'sha256':digest(p)})
        data=README.encode('utf-8');z.writestr('README.md',data);rows.append({'path':'README.md','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        z.writestr('manifest.json',json.dumps({'date':'2026-10-17','bundle':'raw_results' if raw else 'review','files':rows},indent=2))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert not any('draft' in n.lower() or Path(n).suffix in {'.py','.txt','.pkl','.pt'} for n in z.namelist())
        for r in rows:
            data=z.read(r['path']);assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    validation={'status':'passed','payload_files':len(rows),'hash_mismatches':0,'zip_crc':'passed','email_draft_files':0,'bundle':'raw_results' if raw else 'review'}
    with zipfile.ZipFile(target,'a',compression=zipfile.ZIP_DEFLATED) as z:z.writestr('archive_validation.json',json.dumps(validation,indent=2))
    target.with_suffix('.zip.sha256').write_text(f'{digest(target)}  {target.name}\n',encoding='utf-8')
    return {'path':str(target),'bytes':target.stat().st_size,**validation}

def main():
    assert json.loads((SOURCE/'verification.json').read_text())['status']=='passed'
    reports=[build(False),build(True)]
    (ROOT/'outputs/final_scan_package_validation.json').write_text(json.dumps(reports,indent=2),encoding='utf-8');print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
