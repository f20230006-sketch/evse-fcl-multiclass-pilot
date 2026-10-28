"""Verify four-page letter, all numerical tables, paired findings and editing requests."""
from pathlib import Path
import json,re,hashlib
import numpy as np
import pandas as pd
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];DOC=ROOT/'manuscripts/ieee_networking_letters_cbrs_2026_10_28';REPORT=ROOT/'outputs/cbrs_report_2026_10_28'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
def main():
    assert json.loads((REPORT/'verification.json').read_text())['status']=='passed'
    s=(DOC/'main.tex').read_text();log=(DOC/'main.log').read_text(errors='replace')
    assert 'Overfull' not in log and 'undefined' not in log and '! LaTeX Error' not in log
    pdf=PdfReader(DOC/'main.pdf');assert len(pdf.pages)==4
    text='\n'.join(p.extract_text() for p in pdf.pages);assert '??' not in text and '\ufffd' not in text
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',s,re.S).group(1);words=len(abstract.split());assert 75<=words<=100
    refs=set(re.findall(r'\\bibitem\{([^}]+)\}',s));cites={k for group in re.findall(r'\\cite\{([^}]+)\}',s) for k in group.split(',')};assert refs==cites and 15<=len(refs)<=20
    for phrase in ['working draft','supervisor','not an implementation of streaming CBRS','rather than','not a guaranteed accuracy ceiling','descriptive means','per-run minima','balanced+rare','Adam state','calibration seed','calibration fits','input widths','10^{-12}']:assert phrase.lower() not in s.lower(),phrase
    assert 'D-IoT' in s and 'D'+chr(92)+chr(34)+'IoT' not in s
    assert '[Author names]' in s and '[Affiliations and contact information]' in s
    assert 'https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot' in s
    limits=s[s.index('\\section{Limitations and Conclusion}'):];assert 'EWC was calibrated over a limited lambda range.' in limits
    assert 'fixed replay loss' in s and 'complementary and could be combined' in s
    assert 'client_results' not in s and len(re.findall('profiles have RBR macro recall',s))==1
    summary=pd.read_csv(REPORT/'summary.csv');table=(DOC/'tables/main_results.tex').read_text()+(DOC/'tables/capacity_results.tex').read_text();checked=0
    methods=['no_replay','uniform_60','class_balanced_60','cbrs_60','protected_60','balanced_rare_60','ewc','agem','joint','class_balanced_300','protected_300','balanced_rare_300']
    for method in methods:
        r=summary[(summary.score_space=='merged_scans')&(summary.environment=='federated')&(summary.method==method)].iloc[0]
        for metric in METRICS:
            if pd.notna(r[metric+'_mean']):assert f"{100*r[metric+'_mean']:.2f} $\\pm$ {100*r[metric+'_std']:.2f}" in table;checked+=1
    sensitivity=(DOC/'tables/type_results.tex').read_text()
    for space in ['merged_scans','original_type']:
        for method in ['class_balanced_60','cbrs_60','balanced_rare_60']:
            r=summary[(summary.score_space==space)&(summary.environment=='federated')&(summary.method==method)].iloc[0]
            for metric in METRICS:assert f"{100*r[metric+'_mean']:.2f} $\\pm$ {100*r[metric+'_std']:.2f}" in sensitivity;checked+=1
    pairs=pd.read_csv(REPORT/'paired_intervals.csv');narratives=0
    for _,r in pairs.iterrows():
        required=(r.score_space=='merged_scans' and r.order=='averaged' and r.metric!='forgetting') or (r.score_space=='merged_scans' and r.order!='averaged' and r.outcome=='worse') or (r.score_space=='original_type' and r.environment=='federated' and r.order=='averaged' and r.metric in ['old_task_accuracy','slowloris_recall'])
        if required:
            expected=f"${r.mean_difference*100:+.2f}$ $[{r.ci95_low*100:.2f},{r.ci95_high*100:.2f}]$";assert expected in s,(r.metric,r.order);narratives+=1
    split=pd.read_csv(ROOT/'outputs/targeted_validation_report_2026_10_27/paired_intervals.csv');t=(DOC/'tables/split_results.tex').read_text()
    subset=split[(split.score_space=='merged_scans')&(split.order=='averaged')&(split.left=='balanced_rare_60')&(split.right=='class_balanced_60')&split.metric.isin(['old_task_accuracy','slowloris_recall'])]
    assert len(subset)==16
    for _,r in subset.iterrows():assert f"${100*r.mean_difference:+.2f}$ $[{100*r.ci95_low:.2f},{100*r.ci95_high:.2f}]$" in t
    figure=pd.read_csv(DOC/'figures/order_effects_data.csv');original=pd.read_csv(ROOT/'manuscripts/ieee_networking_letters_2026_10_27/figures/order_effects_data.csv')
    assert len(figure)==12
    for k in ['mean_difference','ci95_low','ci95_high']:assert np.allclose(figure[k],original[k],atol=1e-14)
    figuretext=' '.join(p.extract_text() for p in PdfReader(DOC/'figures/order_effects.pdf').pages);assert 'RBR' in figuretext
    for rel,h in json.loads((DOC/'evidence_manifest.json').read_text()).items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
    report=PdfReader(REPORT/'SUMMARY.pdf');assert len(report.pages)==2;reporttext='\n'.join(p.extract_text() for p in report.pages)
    assert 'supervisor' not in reporttext.lower() and 'draft' not in reporttext.lower()
    result={'status':'passed','manuscript_pages':4,'summary_pages':2,'abstract_words':words,'references':len(refs),'table_cells_checked':checked,'paired_narratives_checked':narratives,'cross_split_intervals_checked':16,'figure_intervals_preserved':12,'RBR_naming_consistent':True,'author_affiliation_placeholders_present_as_requested':True,'fixed_loss_and_complementary_framing':True,'implementation_details_moved_to_repository':True,'limited_EWC_range_in_limitations':True,'focused_client_table_replaced_by_one_sentence':True,'code_availability_link_present':True,'D_IoT_spelling_fixed':True,'overfull_boxes':0,'undefined_references':0,'visual_review':'recorded separately after rendering'}
    (DOC/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
