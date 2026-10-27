"""Publish compact, explicitly exploratory evidence without altering frozen runs."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT/'work/evse-fcl-multiclass-pilot'

def main():
    out=ROOT/'outputs/exploratory_tuning_report_2026_10_27'
    assert json.loads((out/'verification.json').read_text())['status']=='passed'
    files=['src/evse_ids/exploratory_tuning.py','configs/exploratory_tuning_2026_10_27.json','docs/research/Exploratory_Tuning_Design_2026_10_27.md','docs/research/Exploratory_Tuning_Changes_2026_10_27.md','tests/test_exploratory_tuning.py',*[f'scripts/{name}.py' for name in ['run_exploratory_tuning','verify_exploratory_tuning','analyze_exploratory_tuning','verify_exploratory_report','report_exploratory_tuning','demo_exploratory_model','package_exploratory_tuning','publish_exploratory_tuning']]]
    for relative in files:
        target=REPO/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/relative,target)
    for folder in [ROOT/'outputs/exploratory_tuning_2026_10_27',out]:
        for p in folder.rglob('*'):
            if not p.is_file() or p.suffix not in {'.md','.pdf','.json','.csv','.pt'} or 'new_merged_results' in p.parts:continue
            target=REPO/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    readme=(REPO/'README.md').read_text(encoding='utf-8')
    section='''## Exploratory model tuning — 27 October 2026

A separately authorized follow-up tests six common model configurations, then replay fractions 0.25/0.50/0.75 and rare shares 0.10/0.20. Class-balanced, protected and balanced+rare share the calibration-selected backbone; 180 calibration fits finish before 180 evaluations across both environments, all orders and ten seeds, memory 60/client. Read [SUMMARY.pdf](outputs/exploratory_tuning_report_2026_10_27/SUMMARY.pdf), [complete results](outputs/exploratory_tuning_report_2026_10_27/INFO.md) and the [design](docs/research/Exploratory_Tuning_Design_2026_10_27.md).

This is exploratory: the earlier evaluation outcomes were already known. The calibration objective changes to the equal-weight final-checkpoint mean of merged old accuracy, Slowloris recall and worst-client macro recall. Frozen-to-tuned gains are overall pipeline differences; matched-backbone controls address conditional allocator differences. All losses and calibration candidates remain visible. Original data roles, task cohorts, 15-type training, memory capacity, earlier numerical evidence and the previously sent manuscript are preserved. No untouched-test confirmation, universal superiority or novelty claim follows from this follow-up alone.

Verification covers all new models, predictions, buffer policies, frozen digests and selection timing. An initial Windows output-directory permission failure occurred before fitting one calibration job; identical-config recovery reused 179 finished calibration fits. See execution_incidents.json. Clean review/raw archives and a separate email draft are provided locally; no email was sent. Reproduction should use a separate output workspace and matching recorded input hashes.

'''
    if '## Exploratory model tuning — 27 October 2026' not in readme:
        first,rest=readme.split('\n',1);(REPO/'README.md').write_text(first+'\n\n'+section+rest,encoding='utf-8')
    (REPO/'VERSION').write_text('0.2.4\n',encoding='utf-8')
    p=REPO/'CHANGELOG.md';change=p.read_text(encoding='utf-8');entry='## 0.2.4 - 2026-10-27\n\nAdd isolated exploratory model/replay tuning with matched baselines, calibration-only choices, all-order reporting and saved evidence. Preserve the frozen study and disclose the changed selection criterion and already-observed evaluation set.\n\n'
    if '## 0.2.4' not in change:p.write_text(change.replace('# Changelog\n\n','# Changelog\n\n'+entry),encoding='utf-8')
    p=REPO/'TESTING.md';s=p.read_text(encoding='utf-8');note='\nExploratory tuning: three model/dropout/role-boundary unit tests passed. Reference calibration exactly reproduces the frozen identical configuration. Verification checks all 180 new models, 720 checkpoints, capacities/quotas, calibration choices and timing, frozen hashes and 448 paired interval rows. The new PDF was rendered and inspected, and both archives passed CRC/payload-hash checks.\n'
    if 'Exploratory tuning: three model/' not in s:p.write_text(s+note,encoding='utf-8')
    manifest=[]
    for p in sorted(REPO.rglob('*')):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts or 'tmp' in p.relative_to(REPO).parts or p.name=='package_manifest.json':continue
        with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
        manifest.append({'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest})
    (REPO/'package_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps({'files':len(manifest),'version':'0.2.4'}))

if __name__=='__main__':main()
