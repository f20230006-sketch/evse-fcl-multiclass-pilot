"""Clean results-only archives with digests; separate manuscript source bundle."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';RUN=OUT/'targeted_validation_2026_10_27';REPORT=OUT/'targeted_validation_report_2026_10_27';DOC=ROOT/'manuscripts/ieee_networking_letters_2026_10_27'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build(path,files):
    records=[]
    temporary=path.with_suffix('.zip.part')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for i,(p,name) in enumerate(sorted(files,key=lambda v:v[1]),1):
            assert 'email' not in name.lower() and 'reply_draft' not in name.lower()
            z.write(p,name,compress_type=zipfile.ZIP_STORED if p.suffix=='.npz' else zipfile.ZIP_DEFLATED);records.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
            if i%250==0:print(path.name,i,'/',len(files),flush=True)
        z.writestr('manifest.json',json.dumps(records,indent=2))
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for r in records:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
    temporary.replace(path)
    path.with_suffix('.zip.sha256').write_text(sha(path)+'  '+path.name+'\n')
    return {'path':str(path),'bytes':path.stat().st_size,'payload_files':len(records),'crc_and_sha256':'passed','email_drafts':0}
def main():
    assert json.loads((REPORT/'verification.json').read_text())['status']=='passed'
    common=[(p,p.name) for p in REPORT.iterdir() if p.is_file() and p.suffix in ['.csv','.json','.md','.pdf']]
    for n in ['grouping_check.json','source_file_class_coverage.csv','identifier_sample_stats.csv','fedcbdr_feasibility.json','reference_sources.md']:
        common.append((RUN/n,'checks/'+n))
    common.extend([(ROOT/'docs/research/Targeted_Validation_Design_2026_10_27.md','DESIGN.md'),(ROOT/'configs/targeted_validation_2026_10_27.json','config.json')])
    report1=build(OUT/'FCL_Targeted_Validation_Review_2026_10_27.zip',common)
    raw=list(common)
    for p in RUN.rglob('*'):
        if p.is_file() and p.suffix in ['.json','.csv','.npz','.pt'] and p.name!='prepared_local_only.pt':raw.append((p,'raw/'+p.relative_to(RUN).as_posix()))
    report2=build(OUT/'FCL_Targeted_Validation_Raw_Results_2026_10_27.zip',raw)
    manuscript=[(p,p.relative_to(DOC).as_posix()) for p in DOC.rglob('*') if p.is_file() and p.suffix in ['.tex','.cls','.pdf','.md','.json','.csv']]
    report3=build(OUT/'IEEE_Networking_Letters_Revised_Source_2026_10_27.zip',manuscript)
    (OUT/'targeted_validation_package_checks.json').write_text(json.dumps([report1,report2,report3],indent=2));print(json.dumps([report1,report2,report3],indent=2))
if __name__=='__main__':main()
