"""Clean external attachments and results-only archives; mail remains separate."""
from pathlib import Path
import hashlib,json,zipfile
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';RUN=OUT/'cbrs_comparison_2026_10_28';REPORT=OUT/'cbrs_report_2026_10_28';DOC=ROOT/'manuscripts/ieee_networking_letters_cbrs_2026_10_28';DELIVERY=OUT/'cbrs_deliverables_2026_10_28'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def archive(path,files):
    temporary=path.with_suffix('.zip.part');manifest=[]
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for p,name in sorted(files,key=lambda v:v[1]):
            assert 'email' not in name.lower() and 'draft' not in name.lower() and 'supervisor' not in name.lower()
            z.write(p,name,compress_type=zipfile.ZIP_STORED if p.suffix=='.npz' else zipfile.ZIP_DEFLATED);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
        z.writestr('manifest.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for r in manifest:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
    temporary.replace(path);path.with_suffix('.zip.sha256').write_text(sha(path)+'  '+path.name+'\n')
    return {'file':str(path),'bytes':path.stat().st_size,'payload_files':len(manifest),'crc_sha256':'passed','email_files':0}
def main():
    assert json.loads((REPORT/'verification.json').read_text())['status']=='passed';assert json.loads((DOC/'verification.json').read_text())['status']=='passed'
    (DELIVERY/'attachments').mkdir(exist_ok=True,parents=True);attachments=[]
    for source,name,title,pages in [(REPORT/'SUMMARY.pdf','FCL_Results_Summary.pdf','CBRS baseline comparison',2),(DOC/'main.pdf','FCL_IEEE_Networking_Letters.pdf','Rare-Reserved Balanced Replay for Federated Continual Intrusion Detection in EV Charging Networks',4)]:
        p=DELIVERY/'attachments'/name;w=PdfWriter();w.clone_document_from_reader(PdfReader(source));w.metadata=None;w.add_metadata({'/Title':title,'/Subject':'Federated continual intrusion detection in EV charging networks'})
        with p.open('wb') as f:w.write(f)
        pdf=PdfReader(p);assert len(pdf.pages)==pages;s='\n'.join(x.extract_text() for x in pdf.pages)+str(pdf.metadata)
        for word in ['supervisor','draft','working copy','??']:assert word not in s.lower(),word
        attachments.append((p,name))
    common=attachments+[(p,p.name) for p in REPORT.iterdir() if p.is_file() and p.suffix in ['.md','.csv','.json']]
    checks=[archive(OUT/'FCL_CBRS_Review_2026_10_28.zip',common)]
    raw=common+[(p,'raw/'+p.relative_to(RUN).as_posix()) for p in RUN.rglob('*') if p.is_file() and p.suffix in ['.json','.csv','.pt','.npz']]
    for order in ['order_1','order_2','order_3']:
        split=OUT/'multiclass_full_comparison/splits'/order
        raw += [(p,'splits/'+order+'/'+p.name) for p in split.iterdir() if p.suffix in ['.json','.csv']]
    checks.append(archive(OUT/'FCL_CBRS_Raw_Results_2026_10_28.zip',raw))
    source=[(p,p.relative_to(DOC).as_posix()) for p in DOC.rglob('*') if p.is_file() and p.suffix in ['.tex','.cls','.pdf','.md','.json','.csv']]
    checks.append(archive(OUT/'IEEE_Networking_Letters_CBRS_Source_2026_10_28.zip',source))
    (DELIVERY/'package_checks.json').write_text(json.dumps(checks,indent=2))
    email="""Subject: CBRS comparison results and four-page manuscript

Dear Ma'am,

I have completed the CBRS comparison and the requested manuscript edits. Please find attached the two-page results summary and four-page manuscript.

At memory 60 in the federated setting, RBR improved old-attack accuracy by 1.64 percentage points, Slowloris recall by 4.04 points and worst-client score by 1.16 points over CBRS. All three paired 95% intervals exclude zero. Centralized old-attack accuracy and Slowloris gains were also significant; the worst-client difference was not significant.

The report includes every order and both scoring views. CBRS performed better on Slowloris in centralized order 2, and the federated old-accuracy and Slowloris gains were not significant under exact-type scoring. These findings are stated in the manuscript.

The manuscript now uses RBR consistently, includes the fixed-loss allocation framing and GitHub availability statement, moves implementation details to the repository, and keeps the caveats in Limitations. Author and affiliation fields remain as placeholders for confirmation, as requested. The complete supporting results are available separately.

Best regards,
Yuvaraj J. Nayak
"""
    (DELIVERY/'EMAIL_REPLY.txt').write_text(email,encoding='utf-8');print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
