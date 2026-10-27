"""Verify revised letter format, cited references and all added table values."""
from pathlib import Path
import hashlib,json,re
import pandas as pd
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];DOC=ROOT/'manuscripts/ieee_networking_letters_2026_10_27';REPORT=ROOT/'outputs/targeted_validation_report_2026_10_27'
def main():
    source=(DOC/'main.tex').read_text();log=(DOC/'main.log').read_text(errors='replace')
    assert 'Overfull' not in log and 'undefined' not in log and '! LaTeX Error' not in log
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1);words=len(abstract.split());assert 75<=words<=100
    pdf=PdfReader(DOC/'main.pdf');assert len(pdf.pages)<=5
    assert all('??' not in p.extract_text() for p in pdf.pages)
    refs=set(re.findall(r'\\bibitem\{([^}]+)\}',source));cites={key for v in re.findall(r'\\cite\{([^}]+)\}',source) for key in v.split(',')};assert len(refs)==17 and refs==cites
    assert r'\documentclass[journal,10pt]{IEEEtran}' in source
    for p in DOC.rglob('*'):
        if p.is_file() and p.suffix in ['.tex','.md']:assert 'supervisor' not in p.read_text().lower()
    pairs=pd.read_csv(REPORT/'paired_intervals.csv');table=(DOC/'tables/targeted_validation.tex').read_text();checked=0
    def verify(r):
        nonlocal checked
        expected=f"${r.mean_difference*100:+.2f}$ $[{r.ci95_low*100:.2f},{r.ci95_high*100:.2f}]$"
        assert expected in table;checked+=1
    for split in [42,43,44,45]:
        for env in ['federated','centralized']:
            for metric in ['old_task_accuracy','slowloris_recall']:
                r=pairs[(pairs.split_seed==split)&(pairs.environment==env)&(pairs.score_space=='merged_scans')&(pairs.order=='averaged')&(pairs.left=='balanced_rare_60')&(pairs.right=='class_balanced_60')&(pairs.metric==metric)].iloc[0];verify(r)
    sensitivity=(DOC/'tables/type_sensitivity.tex').read_text();newsummary=pd.read_csv(REPORT/'summary.csv')
    for space in ['merged_scans','original_type']:
        for method in ['class_balanced_60','balanced_rare_60']:
            r=newsummary[(newsummary.split_seed==42)&(newsummary.environment=='federated')&(newsummary.score_space==space)&(newsummary.method==method)].iloc[0]
            for metric in ['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']:
                assert f"{100*r[metric+'_mean']:.2f} $\\pm$ {100*r[metric+'_std']:.2f}" in sensitivity;checked+=1
    baseline=pd.read_csv(ROOT/'outputs/balanced_rare_report/summary.csv');tab=(DOC/'tables/main_results.tex').read_text()+(DOC/'tables/capacity_results.tex').read_text()
    for _,r in baseline[(baseline.score_space=='merged_scans')&(baseline.environment=='federated')].iterrows():
        if r.method not in ['no_replay','uniform_60','class_balanced_60','protected_60','balanced_rare_60','ewc','agem','joint','class_balanced_300','protected_300','balanced_rare_300']:continue
        for metric in ['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']:
            if pd.notna(r[metric+'_mean']):assert f"{100*r[metric+'_mean']:.2f} $\\pm$ {100*r[metric+'_std']:.2f}" in tab
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REPORT/'paired_intervals.csv',REPORT/'summary.csv',ROOT/'outputs/balanced_rare_report/summary.csv',ROOT/'outputs/targeted_validation_2026_10_27/fedcbdr_feasibility.json']}
    (DOC/'evidence_manifest.json').write_text(json.dumps(manifest,indent=2))
    visual=DOC/'visual_review.json'
    visual_status='all five rendered pages inspected; passed' if visual.exists() and json.loads(visual.read_text())['status']=='passed' else 'required separately before delivery'
    result={'status':'passed','pages':len(pdf.pages),'abstract_words':words,'references':len(refs),'new_table_values_checked':checked,'original_main_results_preserved':True,'undefined_references':0,'overfull_boxes':0,'authors':'pending confirmation','visual_review':visual_status}
    (DOC/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    (DOC/'README.md').write_text(f'''# IEEE Networking Letters revised draft

Prepared 27 October 2026. This working review draft has {len(pdf.pages)} pages, a {words}-word abstract and 17 references in IEEEtran 10-point two-column format. It has not been submitted. Author names, affiliations and contact details remain to be confirmed.

The accepted 64/32 MLP protocol is retained. This revision adds three persistent-role splits, the rare+random/no-benign allocation ablation, compact exact-type sensitivity, source-file grouping information and a public FedCBDR code feasibility check. All 132 calibration fits precede 420 new evaluation runs; all losses remain in the accompanying numerical evidence. The separate exploratory larger-model tuning is excluded from these paper results.

`main.tex` is the editable source; `tables/` contains the original and targeted numerical tables; `figures/` contains the attack-order plot and data. `evidence_manifest.json` records source digests and `verification.json` records artifact/evidence checks. No email reply draft is included.

Compile twice with `pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex`. Standard packages: IEEEtran, amsmath, amssymb, graphicx, booktabs, cite, url and balance. Source ZIP can be opened in Overleaf with main.tex selected.

The official author page specifies at most five pages including references, IEEE 10-point two-column formatting, and a 75-100-word abstract: https://www.comsoc.org/publications/journals/ieee-lnet/policies-guidelines . Primary literature URLs and the inspected FedCBDR commit are documented in the targeted results bundle. Prior works are context rather than unrun performance baselines.
''',encoding='utf-8')
if __name__=='__main__':main()
