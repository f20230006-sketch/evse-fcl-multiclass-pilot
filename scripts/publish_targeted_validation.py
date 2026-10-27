"""Copy targeted code and compact verified evidence into existing private checkout."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT/'work/evse-fcl-multiclass-pilot'
def main():
    report=ROOT/'outputs/targeted_validation_report_2026_10_27';run=ROOT/'outputs/targeted_validation_2026_10_27'
    assert json.loads((report/'verification.json').read_text())['status']=='passed'
    paths=[ROOT/'src/evse_ids/targeted_validation.py',ROOT/'configs/targeted_validation_2026_10_27.json',ROOT/'docs/research/Targeted_Validation_Design_2026_10_27.md',ROOT/'tests/test_targeted_validation.py']
    paths+=list((ROOT/'scripts').glob('*targeted*.py'))
    for folder in [report,run,ROOT/'manuscripts/ieee_networking_letters_2026_10_27']:
        paths += [p for p in folder.rglob('*') if p.is_file() and p.suffix in ['.json','.csv','.md','.pdf','.pt','.tex','.cls'] and p.name!='prepared_local_only.pt']
    for p in paths:
        dest=REPO/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    readme=REPO/'README.md';s=readme.read_text(encoding='utf-8');header='# EVSE multiclass federated continual learning\n'
    section='''
## Targeted validation and revised letter - 27 October 2026

Read [two-page summary](outputs/targeted_validation_report_2026_10_27/SUMMARY.pdf), [complete numerical notes](outputs/targeted_validation_report_2026_10_27/INFO.md), and the [revised letter](manuscripts/ieee_networking_letters_2026_10_27/main.pdf). This round preserves the accepted 64/32 MLP and excludes the separate exploratory tuning from the manuscript results.

Three additional persistent-role splits retain the sampled rows and seed-42 client allocation. The key memory-60 class-balanced versus balanced+rare comparison uses ten training seeds, three orders and both environments; an original-split rare+random/no-benign ablation is also included. All 132 calibration fits precede 420 evaluations. Every split/order and both score spaces, including losses, are reported. These overlapping splits do not establish independent capture generalization.

Source-file groups exist; no explicit session/capture column was found. The limited two-file coverage for benign and Slowloris prevents all three roles from being supported under whole-file assignment. Public FedCBDR source was checked at its recorded commit: missing direct imports, an unsupported README method, and image/CUDA dependencies preclude a faithful quick tabular baseline. Its global coordination and objective changes are distinguished from our purely local allocator.

Code, configs, split manifests, calibration records, all final weights, per-run/per-client tables and verification are included. Compressed checkpoint probabilities are in the separate raw archive. Clean review/raw archives omit email drafts. The original sent letter remains preserved; the revised draft retains author placeholders and has not been submitted.

Reproduce in a separate output workspace with the original input sample and hashes. Run `scripts/run_targeted_validation.py`, `scripts/inspect_targeted_sources.py`, `scripts/analyze_targeted_validation.py`, and `scripts/verify_targeted_validation.py`. The public FedCBDR checkout is needed only for its read-only feasibility check. Core numerical runs do not depend on that checkout.

'''
    if '## Targeted validation and revised letter' not in s:s=s.replace(header,header+section,1)
    readme.write_text(s,encoding='utf-8');(REPO/'VERSION').write_text('0.2.5\n')
    changelog=REPO/'CHANGELOG.md';s=changelog.read_text();entry='## 0.2.5 - 2026-10-27\n\n- Added three fixed-allocation role-split checks and a rare+random/no-benign ablation: 132 calibration fits and 420 evaluated models.\n- Added both scoring views, all split/order paired intervals, provenance and FedCBDR feasibility checks, and a revised 17-reference letter.\n- Preserved original study and exploratory tuning separately; no evaluation-based redesign.\n\n'
    if '## 0.2.5' not in s:changelog.write_text(entry+s)
    print('Copied',len(paths),'files into private checkout; version 0.2.5.')
if __name__=='__main__':main()
