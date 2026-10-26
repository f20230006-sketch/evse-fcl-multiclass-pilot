"""Copy final-analysis code and compact evidence to the existing publication checkout."""
from pathlib import Path
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT/'work/evse-fcl-multiclass-pilot'

def main():
    files=['src/evse_ids/scan_final.py','scripts/run_scan_random_forest.py','scripts/analyze_final_scans.py','scripts/verify_final_scans.py','scripts/report_final_scans.py','scripts/package_final_scans.py','scripts/publish_final_scan_metadata.py','tests/test_scan_final.py','requirements-final-scan.txt']
    for relative in files:
        target=REPO/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/relative,target)
    out=ROOT/'outputs/final_scan_analysis'
    for p in out.rglob('*'):
        if not p.is_file() or 'merged_predictions' in p.parts or p.suffix not in {'.csv','.json','.md','.pdf'}:continue
        target=REPO/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    readme=(REPO/'README.md').read_text(encoding='utf-8')
    section='''## Final checks — 17 October 2026

Read the [two-page summary](outputs/final_scan_analysis/SUMMARY.pdf) or [Markdown summary](outputs/final_scan_analysis/SUMMARY.md), then [INFO.md](outputs/final_scan_analysis/INFO.md) for all merged/rare/client tables. The scan-only Random Forest achieves 34.25% versus 16.67% chance, so intrinsic indistinguishability of all six scans is not established. All 840 saved MLP runs were re-scored without retraining. Separate Slowloris/fragmentation recalls and paired federation interactions are included; the memory-60 protection-over-uniform interaction is not significant. The supported Slowloris interaction at memory 300 is exploratory and unadjusted for multiplicity.

The six merged scan probabilities produce ten output classes; Slowloris stays separate. Original task cohorts and original type-level replay memories are retained for this alternative scoring view. The 33.33% rare metric is explained by last-task order effects over 600 Slowloris and five fragmentation examples, not an always-correct class. All source predictions and splits remain unchanged.

Scripts and compact evidence are in Git. Two clean ZIPs are provided separately: a 2.2 MB review bundle and a 329 MB raw-result bundle. Neither contains email drafts or code. Original MLP probabilities are referenced by digest rather than duplicated; final merged probabilities and RF predictions are in the raw bundle. [Final verification](outputs/final_scan_analysis/verification.json) covers 840 runs, 3,180 checkpoints, 15,811,480 re-scored rows, 592 interval rows and 30 RF evaluations. No manuscript or new MLP training was introduced.

Install `requirements-final-scan.txt` in an isolated environment. The scan diagnostic needs the matching local prepared inputs from the original study; they are excluded from publication. The RF protocol records its source/input hashes, six calibration trials and selected settings before evaluation. Read existing completed evidence first. Any intentional fresh rerun should use a separate output directory/workspace so the frozen evidence remains intact.

'''
    if '## Final checks — 17 October 2026' not in readme:
        first,rest=readme.split('\n',1);(REPO/'README.md').write_text(first+'\n\n'+section+rest,encoding='utf-8')
    (REPO/'VERSION').write_text('0.2.2\n',encoding='utf-8')
    change=(REPO/'CHANGELOG.md').read_text(encoding='utf-8');entry='## 0.2.2 - 2026-10-17\n\nComplete final scan/rare-client checks: calibration-only Random Forest diagnostic, six-scan probability re-scoring, rare-type federation interactions, client tables, and the rare-recall reconstruction. Add a visually verified two-page results summary and separate clean review/raw-results bundles.\n\n'
    if '## 0.2.2' not in change:(REPO/'CHANGELOG.md').write_text(change.replace('# Changelog\n\n','# Changelog\n\n'+entry),encoding='utf-8')
    testing=(REPO/'TESTING.md').read_text(encoding='utf-8');text='\nFinal checks: three new merge/probability/paired-interval unit tests passed (earlier 17-test evidence preserved). Independent final verification covers all 840 re-scored cases, original input hashes, 3,180 checkpoints/15,811,480 rows, focused-client cohort/recall/FPR arithmetic, 592 paired interval rows, 120 rare-metric reconstructions and 30 RF evaluation predictions with fitting/calibration/evaluation isolation. SUMMARY.pdf is exactly two pages and was rendered/visually inspected.\n'
    if 'Final checks: three new' not in testing:(REPO/'TESTING.md').write_text(testing+text,encoding='utf-8')
    rows=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(REPO.rglob('*')) if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and 'tmp' not in p.relative_to(REPO).parts and p.name!='package_manifest.json']
    (REPO/'package_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps({'repository':str(REPO),'files':len(rows)},indent=2))

if __name__=='__main__':main()
