"""Build clean review and raw-result bundles; email and implementation stay separate."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/balanced_rare_report'

def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def build(raw):
    target=ROOT/'outputs'/f"FCL_Balanced_Rare_{'Raw_Results' if raw else 'Review'}_2026_10_26.zip"
    sources={}
    for p in OUT.rglob('*'):
        if not p.is_file() or p.suffix not in {'.md','.pdf','.csv','.json','.npz'}:continue
        if not raw and 'new_merged_results' in p.parts:continue
        sources['results/'+p.relative_to(OUT).as_posix()]=p
    run=ROOT/'outputs/balanced_rare_final'
    for p in run.rglob('*'):
        if not p.is_file():continue
        if not raw and p.relative_to(run).parts[0] in {'runs','calibration'}:continue
        if p.suffix not in {'.json','.csv','.npz','.pt'}:continue
        sources['experiment/'+p.relative_to(run).as_posix()]=p
    sources['FROZEN_DESIGN.md']=ROOT/'docs/research/Balanced_Rare_Frozen_Design_2026_10_26.md'
    sources['config.json']=ROOT/'configs/balanced_rare_final.json'
    rows=[]
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(sources.items()):
            assert 'draft' not in name.lower() and 'supervisor' not in name.lower()
            z.write(p,name);rows.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
        readme='''# Final balanced plus rare-quota experiment

Start with results/SUMMARY.pdf (two pages), then results/INFO.md. Merged-Scan scores are primary; the rare metric is Slowloris recall. Both memories, environments and all orders are reported, including losses. No fragmentation conclusions or equivalence claims are made.

Review bundle: tables, all calibration settings/scores, frozen design, protocols and verification. Raw bundle additionally contains all 120 new final models, 480 original-type checkpoint probability arrays, training logs/memory partitions and new merged results/predictions. Original baseline probabilities are not duplicated; consumed result-table digests appear in analysis_input_hashes.json and original frozen-input hashes appear in the experiment protocol. Code remains in the repository. Neither bundle contains email drafts or manuscripts.

Memory is rows per client (60/300); pooled centralized budgets are five times larger. Rare reservation does not cap total rare occupancy, and benign receives no separate quota. The design and settings were not adjusted after evaluation. Multiple-comparison intervals are unadjusted and describe training randomness on one fixed split.
'''
        z.writestr('README.md',readme)
        rows.append({'path':'README.md','bytes':len(readme.encode()),'sha256':hashlib.sha256(readme.encode()).hexdigest()})
        z.writestr('manifest.json',json.dumps(rows,indent=2))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for row in rows:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
        for name in z.namelist():
            assert Path(name).suffix not in {'.py','.txt'}
            if Path(name).suffix=='.md':assert b'supervisor' not in z.read(name).lower()
    target.with_suffix('.zip.sha256').write_text(sha(target)+'  '+target.name+'\n',encoding='utf-8')
    return {'path':str(target),'bytes':target.stat().st_size,'payload_files':len(rows),'status':'passed','zip_crc':'passed','payload_hashes':'passed','email_drafts':0}

def main():
    assert json.loads((OUT/'verification.json').read_text())['status']=='passed'
    reports=[build(False),build(True)]
    assert reports[0]['bytes']<50_000_000
    (ROOT/'outputs/balanced_rare_package_validation.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
