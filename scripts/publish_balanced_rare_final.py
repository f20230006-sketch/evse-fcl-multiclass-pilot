"""Synchronize new implementation and compact frozen evidence to publication checkout."""
from pathlib import Path
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT/'work/evse-fcl-multiclass-pilot'

def main():
    report=ROOT/'outputs/balanced_rare_report'
    assert json.loads((report/'verification.json').read_text())['status']=='passed'
    for relative in ['src/evse_ids/balanced_rare.py','src/evse_ids/balanced_rare_allocator.py','configs/balanced_rare_final.json',
        'scripts/run_balanced_rare_final.py','scripts/analyze_balanced_rare_final.py','scripts/report_balanced_rare_final.py',
        'scripts/verify_balanced_rare_final.py','scripts/verify_balanced_rare_report.py','scripts/package_balanced_rare_final.py',
        'scripts/publish_balanced_rare_final.py','tests/test_balanced_rare.py','docs/research/Balanced_Rare_Frozen_Design_2026_10_26.md']:
        target=REPO/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/relative,target)
    for folder in [ROOT/'outputs/balanced_rare_final',report]:
        for p in folder.rglob('*'):
            if not p.is_file() or p.suffix not in {'.json','.csv','.md','.pdf','.pt'}:continue
            if 'new_merged_results' in p.parts:continue
            target=REPO/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    readme=(REPO/'README.md').read_text(encoding='utf-8')
    section='''## Frozen final replay experiment — 26 October 2026

The final balanced-plus-rare-quota method is complete at memory 60 and 300 per client: 48 calibration fits followed by 120 evaluations, ten seeds, three orders, federated and centralized. Read [SUMMARY.pdf](outputs/balanced_rare_report/SUMMARY.pdf) (two pages), [SUMMARY.md](outputs/balanced_rare_report/SUMMARY.md) and [INFO.md](outputs/balanced_rare_report/INFO.md) before older reports. Merged-Scan scoring is primary and the rare metric is now Slowloris recall alone. Exact-type results are sensitivity checks, including any differences in conclusions. No inference is made from five fragmentation examples.

The [frozen design](docs/research/Balanced_Rare_Frozen_Design_2026_10_26.md) reserves a feasible 10% or 20% rare share, then fills remaining slots using the existing class-balanced allocator, including benign as an ordinary class. Replay fractions are 0.25/0.50. Choices use the unchanged original-type calibration criterion, not evaluation outcomes. No post-evaluation adjustment or extra experiment was performed. Statistical non-significance does not establish non-inferiority. Both environments and every memory/order result, including losses, are retained.

Code, configs, all calibration records, memory partitions and final weights are here; checkpoint probabilities are provided in the separate raw-results bundle. Clean review/raw bundles contain no email drafts or implementation files. Verification checks every new model, checkpoint, role, quota, merged decision and paired comparison. Results are frozen for review before writing; no manuscript is included.

Reproduce only intentionally in a separate output workspace, retaining original prepared inputs. Run `scripts/run_balanced_rare_final.py`, `scripts/verify_balanced_rare_final.py`, `scripts/analyze_balanced_rare_final.py`, then `scripts/verify_balanced_rare_report.py`. Read the recorded protocols and existing evidence first. The frozen source/input hashes prevent silently resuming changed experiments.

'''
    if '## Frozen final replay experiment' not in readme:
        first,rest=readme.split('\n',1);(REPO/'README.md').write_text(first+'\n\n'+section+rest,encoding='utf-8')
    change=(REPO/'CHANGELOG.md').read_text(encoding='utf-8')
    entry='## 0.2.3 - 2026-10-26\n\nComplete the frozen balanced-plus-rare-quota experiment at memories 60/300, with calibration-only selection, merged-Scan primary scores, Slowloris recall, all-order paired comparisons and independent verification. Add clean review/raw bundles and a two-page results summary. Preserve previous numerical evidence; remove audience-role wording from the latest documents.\n\n'
    if '## 0.2.3' not in change:(REPO/'CHANGELOG.md').write_text(change.replace('# Changelog\n\n','# Changelog\n\n'+entry),encoding='utf-8')
    (REPO/'VERSION').write_text('0.2.3\n',encoding='utf-8')
    testing=(REPO/'TESTING.md').read_text(encoding='utf-8')
    text='\nFinal balanced-plus-rare experiment: four allocator boundary/redistribution/isolation tests passed. Independent experiment verification covers all 120 saved models and 480 checkpoint prediction files, exact rare reservations, equal feasible remainder quotas, persistent roles, frozen inputs and calibration-only selection. Independent report verification checks merged decisions, cohort forgetting, Slowloris/worst-client recall and all 256 paired interval rows. Inherited training helper ASTs are identical. The two-page PDF was rendered and inspected; clean archives passed CRC and payload-digest checks.\n'
    if 'Final balanced-plus-rare experiment:' not in testing:(REPO/'TESTING.md').write_text(testing+text,encoding='utf-8')
    # Keep latest prose neutral; historical evidence paths stay intact.
    for rel in ['README.md','CHANGELOG.md','TODOS.md']:
        p=REPO/rel;s=p.read_text(encoding='utf-8');s=s.replace('supervisor summary','results summary').replace('with the supervisor','during review');p.write_text(s,encoding='utf-8')
    rows=[]
    for p in sorted(REPO.rglob('*')):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts or 'tmp' in p.relative_to(REPO).parts or p.name=='package_manifest.json':continue
        with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
        rows.append({'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest})
    (REPO/'package_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps({'publication_files':len(rows),'version':'0.2.3'}))

if __name__=='__main__':main()
