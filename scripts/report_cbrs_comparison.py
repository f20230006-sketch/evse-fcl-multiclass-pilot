"""Professional two-page comparison summary and complete numerical notes."""
from pathlib import Path
import json
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/cbrs_report_2026_10_28'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
PRETTY={'old_task_accuracy':'old-attack accuracy','slowloris_recall':'Slowloris recall','worst_client_macro_recall':'worst-client score','forgetting':'forgetting'}
def main():
    checks=json.loads((OUT/'verification.json').read_text());assert checks['status']=='passed'
    summary=pd.read_csv(OUT/'summary.csv');pairs=pd.read_csv(OUT/'paired_intervals.csv')
    names={'no_replay':'No replay','uniform_60':'Uniform','class_balanced_60':'Class-balanced','cbrs_60':'CBRS','protected_60':'Protected','balanced_rare_60':'RBR','ewc':'EWC','agem':'A-GEM','joint':'Joint'}
    def value(r,m):return '--' if pd.isna(r[m+'_mean']) else f"{100*r[m+'_mean']:.2f} +/- {100*r[m+'_std']:.2f}"
    def delta(r):return f"{100*r.mean_difference:+.2f} [{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]"
    def mdtable(h,rows):return '\n'.join(['| '+' | '.join(h)+' |','|'+'|'.join(['---']*len(h))+'|']+['| '+' | '.join(str(v) for v in r)+' |' for r in rows])
    fed=summary[(summary.score_space=='merged_scans')&(summary.environment=='federated')].set_index('method')
    mainrows=[[label]+[value(fed.loc[m],k) for k in METRICS] for m,label in names.items()]
    comparisons=[];interpret=[]
    for env in ['federated','centralized']:
        group=pairs[(pairs.score_space=='merged_scans')&(pairs.environment==env)&(pairs.order=='averaged')].set_index('metric')
        comparisons.append([env.capitalize()]+[delta(group.loc[k]) for k in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']])
        for metric in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']:
            r=group.loc[metric];meaning='difference not significant' if r.outcome=='not significant' else r.outcome+' for RBR';interpret.append(f"{env.capitalize()} {PRETTY[metric]}: {delta(r)} points; {meaning}.")
    for r in pairs[(pairs.score_space=='merged_scans')&(pairs.order!='averaged')&(pairs.outcome=='worse')].itertuples():
        interpret.append(f"Order-specific loss: {r.environment}, order {r.order[-1]}, {PRETTY[r.metric]} {delta(r)} points.")
    orderrows=[]
    for env in ['federated','centralized']:
        for order in ['order_1','order_2','order_3']:
            g=pairs[(pairs.score_space=='merged_scans')&(pairs.environment==env)&(pairs.order==order)].set_index('metric');orderrows.append(['Fed.' if env=='federated' else 'Central',order[-1]]+[delta(g.loc[k]) for k in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']])
    exact=[]
    for env in ['federated','centralized']:
        for space in ['merged_scans','original_type']:
            g=pairs[(pairs.score_space==space)&(pairs.environment==env)&(pairs.order=='averaged')].set_index('metric');exact.append(['Fed.' if env=='federated' else 'Central','Merged' if space=='merged_scans' else 'Exact']+[delta(g.loc[k]) for k in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']])
    md='# CBRS baseline comparison - 28 October 2026\n\n## What was done\n\n- Implemented published CBRS population, including persistent full-class flags and within-class reservoir replacement.\n- Original split 42, memory 60/client (300 pooled), same 64/32 MLP, three orders, ten training seeds, federated and centralized.\n- Calibrated only replay fraction 0.25/0.50 using the unchanged calibration criterion; all 12 calibration fits preceded all 60 evaluations.\n- Added CBRS to the main table and shortened the manuscript to four pages with consistent RBR naming.\n\n## Main results\n\nFederated merged-Scan final scores, original split; percentages, mean +/- SD over ten seed averages of three orders.\n\n'+mdtable(['Method','Old accuracy','Forgetting','Slowloris','Worst-client'],mainrows)+'\n\n## RBR minus CBRS\n\nPercentage points [95% paired interval]. An interval excluding zero is significant. Higher is better for the three metrics below.\n\n'+mdtable(['Setting','Old accuracy','Slowloris','Worst-client'],comparisons)+'\n\n## Interpretation\n\n'+'\n\n'.join(interpret)+'\n\n## Each order\n\n'+mdtable(['Setting','Order','Old accuracy','Slowloris','Worst-client'],orderrows)+'\n\n## Scoring sensitivity\n\n'+mdtable(['Setting','View','Old accuracy','Slowloris','Worst-client'],exact)+'\n\n## Scope and verification\n\nThis compares population policies under the accepted task-based training schedule and fixed replay loss. CBRS ingestion is sequential at task boundaries; each fitting flow enters once, while benign reference flows still recur in training. The original paper\'s separate weighted-retrieval recipe is not substituted. All losses and non-significant comparisons are retained. Intervals describe training randomness on the same fixed split and are unadjusted for multiple comparisons.\n\nOnly 16 benign and five fragmentation evaluation flows are available. There are no false-alarm or fragmentation conclusions. Previous cross-split RBR/class-balanced evidence is preserved; CBRS was not run on extra splits or at memory 300/client.\n\nVerification passed for '+str(checks['models_checked'])+' models, '+str(checks['checkpoints'])+' checkpoints, '+format(checks['prediction_rows'],',')+' prediction rows and '+str(checks['paired_intervals'])+' paired intervals. Population state, counts, stream arrivals, role boundaries and calibration selection were checked.\n'
    (OUT/'SUMMARY.md').write_text(md,encoding='utf-8')
    info=md+'\n## Full tables\n'
    for filename in ['summary.csv','paired_intervals.csv','per_order_summary.csv']:
        f=pd.read_csv(OUT/filename);info+='\n### '+filename+'\n\n'+mdtable(list(f.columns),f.itertuples(index=False,name=None))+'\n'
    trials=json.loads((ROOT/'outputs/cbrs_comparison_2026_10_28/hyperparameter_trials.json').read_text());info+='\n## Calibration record\n\n```json\n'+json.dumps(trials,indent=2)+'\n```\n'
    info+='\n## Primary source\n\nChrysakis and Moens, Online Continual Learning from Imbalanced Data, ICML 2020, Algorithm 1: https://proceedings.mlr.press/v119/chrysakis20a.html . The full-class interpretation follows its supplementary proof. RBR is the short name of the unchanged historical balanced_rare method.\n'
    (OUT/'INFO.md').write_text(info,encoding='utf-8')
    styles=getSampleStyleSheet();styles['Normal'].fontSize=8;styles['Normal'].leading=10;styles['Heading1'].fontSize=14;styles['Heading2'].fontSize=10;story=[]
    def para(t,style='Normal'):story.append(Paragraph(escape(t),styles[style]));story.append(Spacer(1,6))
    def table(h,rows,widths):
        t=Table([[Paragraph(escape(str(c)),styles['Normal']) for c in r] for r in [h,*rows]],colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf5')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,0),.5,colors.grey)]));story.append(t);story.append(Spacer(1,8))
    para('CBRS baseline comparison | 28 October 2026','Heading1');para('What was done','Heading2')
    para('Published CBRS population; original split 42; memory 60/client or 300 pooled; unchanged 64/32 MLP, ten seeds, three orders, both environments. Only replay fraction 0.25/0.50 was calibrated. All 12 calibration fits preceded the 60 evaluation runs.')
    para('Main results: federated, merged-Scan','Heading2');para('Percentages; mean +/- SD over ten seed averages of three orders. RBR means rare-reserved balanced replay.')
    table(['Method','Old accuracy','Forgetting','Slowloris','Worst-client'],mainrows,[105,95,95,95,96])
    para('Paired comparison: RBR minus CBRS','Heading2');para('Percentage points [95% interval]; an interval excluding zero is significant.')
    table(['Setting','Old accuracy','Slowloris','Worst-client'],comparisons,[65,139,141,141])
    for t in interpret:para(t)
    story.append(PageBreak());para('Order and scoring sensitivity','Heading1');para('RBR minus CBRS, each order','Heading2')
    table(['Setting','Order','Old accuracy','Slowloris','Worst-client'],orderrows,[46,40,133,133,134]);para('Merged-Scan versus exact-type reporting','Heading2')
    table(['Setting','View','Old accuracy','Slowloris','Worst-client'],exact,[46,49,130,130,131])
    para('Scope and verification','Heading2');para('The published population rule is streamed at the shared task boundaries, using the same replay loss and uniform retrieval as the other allocation policies. Class counters and full flags persist. Each fitting flow arrives once; recurring benign training references are not counted as fresh arrivals. This assesses the population rule under the accepted task-based protocol.')
    para('The same fixed split and constructed clients limit generalization; intervals are unadjusted and non-significance is not equivalence. Sixteen benign and five fragmentation evaluation flows do not support false-alarm or fragmentation claims. No extra CBRS splits, capacity sweep or model tuning was run.')
    para(f"Checks passed: {checks['models_checked']} models, {checks['checkpoints']} checkpoints, {checks['prediction_rows']:,} prediction rows, {checks['stream_arrivals_checked']:,} stream arrivals and {checks['paired_intervals']} paired intervals. Full tables and calibration records are available separately.")
    SimpleDocTemplate(str(OUT/'SUMMARY.pdf'),pagesize=A4,leftMargin=35,rightMargin=35,topMargin=30,bottomMargin=30).build(story)
    print('Two-page summary and full notes generated.')
if __name__=='__main__':main()
