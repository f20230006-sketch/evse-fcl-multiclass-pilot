"""Create a self-contained immutable snapshot before exploratory experiments."""
from pathlib import Path
import hashlib,json,zipfile,time
R=Path('D:/EV-charging');D=R/'outputs/frozen_paper_2026_11_09';D.mkdir(exist_ok=True)
manifest=D/'MANIFEST.json'
if manifest.exists():
 print('Existing freeze:',manifest);raise SystemExit(0)
names=['multiclass_full_comparison','replay_followup_essential','replay_followup_sweep','balanced_rare_final','targeted_validation_2026_10_27','cbrs_comparison_2026_10_28','balanced_rare_report','cbrs_report_2026_10_28','targeted_validation_report_2026_10_27','final_scan_analysis','letter_illustrated_2026_11_04']
dirs=[R/'outputs'/n for n in names]+[R/'manuscripts/ieee_networking_letters_illustrated_2026_11_04',R/'src/evse_ids',R/'configs',R/'scripts',R/'tests',R/'docs/research']
files=sorted({p for d in dirs for p in d.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.suffix not in ['.pyc','.log','.aux','.out'] and not p.name.startswith(('review-','support_review-'))})
items=[];start=time.time()
with zipfile.ZipFile(D/'FCL_Paper_and_Baseline_Freeze.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 for i,p in enumerate(files):
  raw=p.read_bytes();name=str(p.relative_to(R)).replace('\\','/');items.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()});z.writestr(name,raw)
  if i%1500==0:print('Frozen',i,'/',len(files),flush=True)
 payload={'status':'frozen','date':'2026-11-09','scope':'Current paper and accepted baseline comparisons; no universal SOTA claim. Historical experiments are preserved as evidence, not promoted to current primary results.','files':items}
 z.writestr('FREEZE_MANIFEST.json',json.dumps(payload,indent=2))
manifest.write_text(json.dumps(payload,indent=2),encoding='utf-8')
archive=D/'FCL_Paper_and_Baseline_Freeze.zip';h=hashlib.sha256()
with archive.open('rb') as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
(D/'SHA256.txt').write_text(h.hexdigest()+'  '+archive.name+'\n')
(D/'README.md').write_text('# Frozen paper and baseline evidence\n\nFrozen on 9 November 2026 before the asynchronous adaptive-replay study. The ZIP contains the current four-page manuscript, clean deliverables, accepted experimental records, prepared split tensors, models, predictions, source, configurations and reports. MANIFEST.json records every original relative path and SHA-256 digest. New work must use separate paths and must not overwrite these results. This is the accepted baseline comparison, not a claim of universal state-of-the-art superiority.\n')
print('FREEZE COMPLETE',len(items),'files',archive.stat().st_size,'bytes',round(time.time()-start,1),'seconds',flush=True)
