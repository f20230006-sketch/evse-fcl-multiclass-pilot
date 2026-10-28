"""Publish code, compact evidence and manuscript into the existing private checkout."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT/'work/evse-fcl-multiclass-pilot'
def main():
    assert json.loads((ROOT/'outputs/cbrs_report_2026_10_28/verification.json').read_text())['status']=='passed'
    files=list((ROOT/'scripts').glob('*cbrs*.py'))+list((ROOT/'src/evse_ids').glob('cbrs*.py'))+[ROOT/'tests/test_cbrs.py',ROOT/'configs/cbrs_comparison_2026_10_28.json',ROOT/'docs/research/CBRS_Frozen_Design_2026_10_28.md',ROOT/'docs/research/Implementation_Details_2026_10_28.md']
    for folder in [ROOT/'outputs/cbrs_comparison_2026_10_28',ROOT/'outputs/cbrs_report_2026_10_28',ROOT/'manuscripts/ieee_networking_letters_cbrs_2026_10_28']:
        files += [p for p in folder.rglob('*') if p.is_file() and p.suffix in ['.json','.csv','.md','.pdf','.pt','.tex','.cls']]
    for p in files:
        target=REPO/p.relative_to(ROOT);target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,target)
    readme=REPO/'README.md';s=readme.read_text();header='# EVSE multiclass federated continual learning\n'
    section='''
## CBRS population comparison and four-page letter - 28 October 2026

The requested sole additional baseline is complete: published CBRS Algorithm 1, original split 42, capacity 60/client (300 pooled), three orders, ten training seeds and both environments. Only replay fraction 0.25/0.50 is calibrated, using the unchanged criterion. Twelve calibration fits finish before sixty evaluations. The [frozen design](docs/research/CBRS_Frozen_Design_2026_10_28.md) fixes stream handling, persistent full flags/counters and task-boundary integration under the shared replay loss.

Read [SUMMARY.pdf](outputs/cbrs_report_2026_10_28/SUMMARY.pdf), [complete notes and tables](outputs/cbrs_report_2026_10_28/INFO.md), [four-page manuscript](manuscripts/ieee_networking_letters_cbrs_2026_10_28/main.pdf) and [implementation details](docs/research/Implementation_Details_2026_10_28.md). RBR is the short name for unchanged historical balanced_rare outputs. At federated memory 60, merged old-accuracy/Slowloris/worst-client gains over CBRS are 1.64/4.04/1.16 points with intervals excluding zero. The exact-type old/Slowloris comparisons are not significant; centralized order-2 Slowloris favors CBRS. All losses remain visible. This is the published population policy under the accepted task-based training protocol, not the paper's complete weighted-retrieval online-learning recipe.

Verification covers 60 saved models, 240 checkpoints, 1,182,880 prediction rows, 1,410,780 stream arrivals and 64 paired intervals. Independent-reference tests check population updates and persistent state. The manuscript has four pages, a 91-word abstract and 18 references; it uses RBR in text/tables/figure, moves implementation details here, and retains requested author/affiliation placeholders. No submission or email was sent. Clean result archives exclude reply files; raw probabilities are supplied separately.

Reproduction: `python tests/test_cbrs.py`, `python scripts/run_cbrs_comparison.py`, `python scripts/analyze_cbrs_comparison.py`, `python scripts/verify_cbrs_comparison.py`, then report and letter builders. Obtain original flow CSVs and matching prepared inputs; immutable fingerprints prevent overwriting earlier experiments with a changed design.

'''
    if '## CBRS population comparison and four-page letter' not in s:s=s.replace(header,header+section,1)
    readme.write_text(s,encoding='utf-8');(REPO/'VERSION').write_text('0.2.6\n')
    changelog=REPO/'CHANGELOG.md';s=changelog.read_text();entry='## 0.2.6 - 2026-10-28\n\n- Added published streaming CBRS population under the fixed replay protocol: 12 calibration fits and 60 evaluations, both environments, all orders and ten seeds.\n- Added all paired comparisons, exact-type uncertainty and order-specific losses with full model/population verification.\n- Revised the IEEE letter to four pages with consistent RBR naming, implementation details in the repository and requested author fields.\n\n'
    if '## 0.2.6' not in s:changelog.write_text(entry+s,encoding='utf-8')
    print('Copied',len(files),'files; version 0.2.6.')
if __name__=='__main__':main()
