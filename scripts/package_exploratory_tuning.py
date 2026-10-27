"""Clean exploratory evidence archives; old manuscript and mail drafts excluded."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'outputs/exploratory_tuning_report_2026_10_27'
RUN=ROOT/'outputs/exploratory_tuning_2026_10_27'

def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def build(raw):
    destination=ROOT/'outputs'/f"FCL_Exploratory_Tuning_{'Raw_Results' if raw else 'Review'}_2026_10_27.zip"
    sources={}
    for base,label in [(REPORT,'results'),(RUN,'experiment')]:
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix not in {'.md','.pdf','.json','.csv','.pt','.npz'}:continue
            relative=p.relative_to(base)
            if not raw and relative.parts[0] in {'new_merged_results','runs','calibration','backbone_calibration'}:continue
            sources[label+'/'+relative.as_posix()]=p
    sources['EXPLORATORY_DESIGN.md']=ROOT/'docs/research/Exploratory_Tuning_Design_2026_10_27.md'
    sources['WHAT_CHANGED.md']=ROOT/'docs/research/Exploratory_Tuning_Changes_2026_10_27.md'
    sources['config.json']=ROOT/'configs/exploratory_tuning_2026_10_27.json'
    rows=[]
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(sources.items()):
            assert 'draft' not in name.lower() and 'email' not in name.lower()
            z.write(p,name);rows.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
        readme='''# Exploratory tuning follow-up

Read results/SUMMARY.pdf, SUMMARY.md and INFO.md. This is a separately authorized exploratory study after the earlier evaluation outcomes were known. It is not a new untouched confirmatory test and does not overwrite the previous results or manuscript. All six common model settings, replay trials, matched controls, orders and losses are retained. Memory is 60 rows/client or 300 centrally. Model parameter storage may increase. No email draft, manuscript, implementation file or raw input dataset is included.

Review bundle: aggregate/per-run CSVs, source digests, protocols, all calibration records and verification. Raw bundle additionally includes new final models, checkpoint probabilities, derived merged probabilities, training logs and memory audits. Earlier baseline probabilities are not duplicated; consumed frozen-result digests appear in analysis_input_hashes.json. Code/configuration is maintained in the project repository. No publication submission or email sending was performed.
'''
        z.writestr('README.md',readme);rows.append({'path':'README.md','bytes':len(readme.encode()),'sha256':hashlib.sha256(readme.encode()).hexdigest()})
        z.writestr('manifest.json',json.dumps(rows,indent=2))
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        for r in rows:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
    destination.with_suffix('.zip.sha256').write_text(sha(destination)+'  '+destination.name+'\n',encoding='utf-8')
    return {'path':str(destination),'bytes':destination.stat().st_size,'files':len(rows),'integrity':'passed','email_drafts':0}

def main():
    assert json.loads((REPORT/'verification.json').read_text())['status']=='passed'
    reports=[build(False),build(True)]
    assert reports[0]['bytes']<50_000_000
    (ROOT/'outputs/exploratory_tuning_package_validation.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8');print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
