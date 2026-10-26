"""Neutral two-page results summary, detailed notes and separate email draft."""
from pathlib import Path
import json
import sys
from xml.sax.saxutils import escape
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/balanced_rare_report'
sys.path.insert(0,str(ROOT/'scripts'))
from analyze_balanced_rare_final import METRICS

LABELS={'no_replay':'No replay','uniform_60':'Uniform','class_balanced_60':'Class-balanced','protected_60':'Protected','balanced_rare_60':'Balanced + rare','ewc':'EWC','agem':'A-GEM','joint':'Joint'}

def number(value):return 'N/A' if pd.isna(value) else f'{100*value:.2f}'
def value(row,metric):return number(row[metric+'_mean'])+' ± '+number(row[metric+'_std']) if pd.notna(row[metric+'_mean']) else 'N/A'
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])

def main():
    s=pd.read_csv(OUT/'summary.csv');ci=pd.read_csv(OUT/'paired_intervals.csv');orders=pd.read_csv(OUT/'per_order_summary.csv')
    mainrows=[[name]+[value(s[(s.score_space=='merged_scans')&(s.environment=='federated')&(s.method==method)].iloc[0],m) for m in METRICS] for method,name in LABELS.items()]
    header=['Method','Old accuracy','Forgetting','Slowloris','Worst client']
    def comparison(cap,base,metric,env='federated',space='merged_scans',order='averaged'):
        r=ci[(ci.score_space==space)&(ci.environment==env)&(ci.capacity==cap)&(ci.right==f'{base}_{cap}')&(ci.metric==metric)&(ci.order==order)].iloc[0]
        return f"{100*r.mean_difference:+.2f} [{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]; {r.outcome}"
    sweep=[]
    for base,label in [('class_balanced','Class-balanced'),('protected','Protected'),('balanced_rare','Balanced + rare')]:
        cells=[]
        for cap in [60,300]:
            r=s[(s.score_space=='merged_scans')&(s.environment=='federated')&(s.method==f'{base}_{cap}')].iloc[0]
            cells.append(' / '.join(number(r[m+'_mean']) for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']))
        sweep.append([label,*cells])
    bullets=['Added balanced + rare replay at memories 60 and 300 per client, with no separate benign quota.',
        'Selected one of four fixed quota/replay configurations on calibration data, then ran ten seeds, three orders and both training settings (48 calibration fits; 120 evaluations).',
        'Used merged-Scan scores as primary, Slowloris recall alone, and paired comparisons against both existing baselines; retained exact-type sensitivity results.']
    keys=[]
    for baseline,label in [('class_balanced','class-balanced'),('protected','protected')]:
        keys.append(f"New − {label}, memory 60: old accuracy {comparison(60,baseline,'old_task_accuracy')}; Slowloris {comparison(60,baseline,'slowloris_recall')}; worst client {comparison(60,baseline,'worst_client_macro_recall')}.")
    interactions=pd.read_csv(OUT/'federation_interactions.csv')
    parts=[]
    for metric,label in [('old_task_accuracy','old accuracy'),('slowloris_recall','Slowloris')]:
        r=interactions[(interactions.score_space=='merged_scans')&(interactions.capacity==60)&(interactions.baseline=='class_balanced')&(interactions.metric==metric)].iloc[0]
        parts.append(f'{label} {100*r.mean_difference:+.2f} [{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]')
    keys.append('Federated − centralized difference in new-over-balanced gains, memory 60: '+'; '.join(parts)+'; both not significant.')
    meaning=['At memory 60, the new method improves federated old accuracy and Slowloris recall over class-balanced replay. Worst-client improvement is not significant. The requested significance pattern is met on order-averaged results in both settings; this does not establish non-inferiority.',
        'The method does not dominate protected replay: federated Slowloris recall is lower at both capacities, and old accuracy is lower at memory 300, while worst-client score is higher. All order-specific losses are retained.',
        'At memory 60, the gain over class-balanced is not significantly different between federated and centralized training. Exact-type sensitivity supports the broad trade-off, but some significance conclusions differ; see INFO.md.']
    problems=['Only 600 Slowloris, five fragmentation and 16 benign evaluation examples exist. No fragmentation conclusions are drawn; benign-starved false alarms remain undefined.',
        'Merged scoring retains original task cohorts, 15-type training and type-level balancing. Scan spans two tasks. Exact-type comparisons are sensitivity results; differences between views must be disclosed.',
        'Intervals reflect ten training seeds on one fixed split, with three orders averaged per seed; multiple comparisons are unadjusted. The earlier Slowloris federation interaction at memory 300 remains exploratory.']
    questions=['Review the paired outcomes and agree on the final trade-off/contribution before manuscript writing. Results and method are now frozen; no further method adjustment or experiment is proposed.']
    cap300=[[label]+[comparison(300,baseline,m) for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']] for baseline,label in [('class_balanced','vs balanced'),('protected','vs protected')]]
    md=['# Final balanced + rare experiment: results summary','','26 October 2026 | Values: percentages; differences: percentage points.','','## 1. What was done','']+['- '+b for b in bullets]
    md+=['','## 2. Main results table','','Merged-Scan primary scores, federated, memory 60/client. Mean ± SD over ten seed averages across three orders. Worst client: supported-class macro recall. Joint forgetting: not applicable.','',table(header,mainrows),'','Memory sweep: old accuracy / Slowloris / worst client (%).','',table(['Method','Memory 60','Memory 300'],sweep),'','## 3. Key comparisons','','Paired 95% intervals; better/worse denotes statistically significant direction.']+['- '+k for k in keys]
    md+=['','## 4. What this means','']+['- '+m for m in meaning]+['','Memory-300 federated comparisons (new minus baseline):','',table(['Comparison','Old accuracy','Slowloris','Worst client'],cap300),'','## 5. Problems or surprises','']+['- '+p for p in problems]+['','## 6. Questions for review','']+['- '+q for q in questions]
    (OUT/'SUMMARY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    info=['# Complete final experiment results','','Merged-Scan scores are primary; Slowloris is the reported rare-attack metric. The combined 605-example metric is not used in this report. All evaluation results are preserved, including losses.','','## Main summary and memory results','',*md[8:]]
    for space in ['merged_scans','original_type']:
        info+=['',f'## {space}: complete mean ± SD tables','']
        for env in ['federated','centralized']:
            sub=s[(s.score_space==space)&(s.environment==env)]
            info+=['',f'### {env}','',table(header,[[r.method]+[value(r,m) for m in METRICS] for _,r in sub.iterrows()])]
        info+=['',f'## {space}: all paired comparisons, including losses','']
        for (env,cap,order),group in ci[ci.score_space==space].groupby(['environment','capacity','order']):
            info+=['',f'### {env}, memory {cap}, {order}','',table(['Baseline','Metric','Difference','95% interval','Outcome'],[[r.right,r.metric,f'{100*r.mean_difference:+.2f}',f'[{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]',r.outcome] for _,r in group.iterrows()])]
        info+=['',f'## {space}: every order, mean ± SD','',table(['Environment','Method','Order']+header[1:],[[r.environment,r.method,r.order]+[value(r,m) for m in METRICS] for _,r in orders[orders.score_space==space].iterrows()])]
    selected=json.loads((ROOT/'outputs/balanced_rare_final/hyperparameter_trials.json').read_text())
    info+=['','## Calibration selections','','Selection criterion remained mean original-type calibration macro recall over checkpoints, as in prior methods. Evaluation scores did not select settings.','',table(['Order','Environment','Memory','Rare quota','Replay fraction'],[[o,e,m.rsplit('_',1)[1],v['rare_quota_fraction'],v['replay_fraction']] for o,a in selected['selected'].items() for e,b in a.items() for m,v in b.items()])]
    screens=pd.read_csv(OUT/'requested_outcome_screen.csv')
    sensitivity=pd.read_csv(OUT/'score_space_sensitivity.csv')
    info+=['','## Requested significance pattern','','This screen requires significantly higher Slowloris recall than class-balanced, and no significantly lower old accuracy or worst-client score. It does not establish equivalence/non-inferiority. Averaging all three orders is distinct from meeting it within each order.','',table(['Score space','Environment','Memory','Order','Screen met'],[[r.score_space,r.environment,r.capacity,r.order,r.requested_significance_screen_met] for _,r in screens.iterrows()]),'','## Sensitivity: significance conclusions that differ','','Broad trade-off agreement does not mean every statistical conclusion matches.','',table(['Environment','Memory','Order','Baseline','Metric','Merged','Exact type'],[[r.environment,r.capacity,r.order,r.right,r.metric,r.outcome_merged,r.outcome_type] for _,r in sensitivity[~sensitivity.same_significance_direction].iterrows()])]
    info+=['','## Audit and interpretation','','The design and training-source hashes were recorded before calibration. All 48 calibrations completed and selected settings were recorded before any new evaluation. No tuning followed evaluation. Raw predictions, final models, memory partitions and training logs are retained separately. Previous baselines and their selected settings were reused without retraining. Paired differences below 1e-12 in absolute value are treated as numerical zero, preventing floating-point ties in near-zero forgetting from being labeled significant. No training result or selected setting was changed.','','Memory is examples, not model parameters: 60 or 300 per client; centralized total 300 or 1500. Rare reservation is a minimum share, not a ceiling; the balanced remainder includes rare types and benign. Within the rare group, the unchanged feasible class-balanced allocator is used.','','See paired_intervals.csv, federation_interactions.csv, per_order_summary.csv and new_per_client_metrics.csv for machine-readable evidence. No fragmentation interpretation or non-inferiority claim is warranted. No manuscript was generated.']
    (OUT/'INFO.md').write_text('\n'.join(info)+'\n',encoding='utf-8')
    notes='''# Final experiment: short findings notes

All 48 calibration fits and 120 evaluation runs are complete. The design was fixed before running and was not changed after evaluation. Verification passed for 120 saved models, 480 checkpoints, 2,365,760 prediction rows and 256 paired comparisons. Merged-Scan scores are primary and recall refers to Slowloris only.

At memory 60 in federated training, balanced + rare achieves 85.52% old accuracy, 14.24% forgetting, 76.62% Slowloris recall and 79.03% worst-client macro recall. Compared with class-balanced, old accuracy improves by 1.53 points (95% interval 0.23–2.84) and Slowloris by 5.06 (1.27–8.84), both significant. Worst-client improvement is 1.06 (-0.07–2.19), not significant. This meets the requested significance pattern averaged over orders; it does not prove equivalence/non-inferiority.

Against protected replay at memory 60, old accuracy and worst-client score improve by 12.68 and 31.87 points, but Slowloris falls by 6.11 points; all three differences are significant. At memory 300, the new method improves all four federated metrics over class-balanced, but loses old accuracy and Slowloris against protected while improving worst-client score. Every memory/order loss appears in INFO.md and paired_intervals.csv. Gains are not significant in every individual order, and exact-type significance conclusions differ in some cases.

At memory 60, new-over-balanced gains do not differ significantly between federated and centralized training. No additional overall federation advantage is established. The previous Slowloris memory-300 federation interaction remains exploratory.

Memory 60/300 means at most 60/300 stored fitting examples per client, not network layers or model parameters. With five clients, centralized storage is 300/1500. The new method first reserves a calibration-selected 10% or 20% rare share, then balances all remaining slots across available original types. Benign has no separate quota. Replay fraction (0.25/0.50) controls minibatch mixing, not storage size.

Only 600 Slowloris, five fragmentation and 16 benign test examples are available on one fixed split. No fragmentation conclusions are made. Intervals describe training-seed uncertainty, not independent stations/captures, and are unadjusted for multiple comparisons. Original cohorts/type-level replay policies are retained under merged scoring.

Send SUMMARY.pdf (two pages) and the small review ZIP. The raw ZIP is a separate evidence bundle; if it exceeds 50 MB, share these notes and the review ZIP instead. Email drafts remain outside both archives. Results are frozen for review before writing.
'''
    (OUT/'FINDINGS_NOTES.md').write_text(notes,encoding='utf-8')
    pdf(header,mainrows,sweep,bullets,keys,meaning,problems,questions,cap300)
    (ROOT/'outputs/BALANCED_RARE_EMAIL_DRAFT_2026_10_26.txt').write_text("Subject: Final balanced + rare replay experiment completed\n\nDear Ma'am,\n\nI have completed the frozen balanced + rare-quota experiment at memory sizes 60 and 300, across the same ten seeds, three orders and both training settings. All four candidate settings were selected using calibration data only.\n\nThe attached two-page summary reports merged-Scan scores, Slowloris recall and paired comparisons with class-balanced and protected replay. The review archive includes every order and memory size, including any losses, plus exact-type sensitivity results. No method changes were made after evaluation.\n\nThe results are now frozen. We can review the findings and agree on the main message before starting the letter.\n\nBest regards,\nYuvaraj\n",encoding='utf-8')

def pdf(headers,rows,sweep,bullets,keys,meaning,problems,questions,cap300):
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pypdf import PdfReader
    pdfmetrics.registerFont(TTFont('FinalArial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('FinalArialBold','C:/Windows/Fonts/arialbd.ttf'))
    body=ParagraphStyle('body',fontName='FinalArial',fontSize=9,leading=11.5,spaceAfter=4)
    head=ParagraphStyle('head',fontName='FinalArialBold',fontSize=10.5,leading=13,spaceBefore=8,spaceAfter=5)
    title=ParagraphStyle('title',fontName='FinalArialBold',fontSize=15,leading=18,spaceAfter=6)
    small=ParagraphStyle('small',parent=body,fontSize=8.1,leading=10)
    def p(t,style=body):return Paragraph(escape(str(t)),style)
    def t(h,r,widths):
        result=Table([[p(c,small) for c in row] for row in [h,*r]],colWidths=widths,repeatRows=1,hAlign='LEFT')
        result.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfe8f2')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f9')]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return result
    story=[p('Balanced + rare replay: final results',title),p('26 October 2026 | Primary scores merge six scan types; recall refers to Slowloris.',small),p('1. What was done',head)]+[p('• '+b) for b in bullets]
    story+=[p('2. Main results table',head),p('Federated, memory 60/client. Mean ± SD across ten seed averages of three orders; all values %. Worst client is macro recall.',small),t(headers,rows,[105,102,94,100,108]),Spacer(1,5),p('Memory sweep: old accuracy / Slowloris / worst client (%).',small),t(['Method','Memory 60','Memory 300'],sweep,[115,197,197]),p('3. Key comparisons',head),p('New minus baseline, percentage points; paired 95% intervals.',small)]+[p('• '+k) for k in keys]
    story+=[PageBreak(),p('4. What this means',head)]+[p('• '+m) for m in meaning]
    story+=[p('Memory-300 federated comparisons (new minus baseline):',small),t(['Comparison','Old accuracy','Slowloris','Worst client'],cap300,[80,143,143,143]),p('5. Problems or surprises',head)]+[p('• '+v) for v in problems]
    story+=[p('6. Questions for review',head)]+[p('• '+q) for q in questions]+[Spacer(1,5),p('All centralized and order-specific values, forgetting comparisons, calibration trials and verification are in INFO.md and the review archive. Email correspondence stays outside archives.',small)]
    def footer(canvas,doc):
        canvas.setFont('FinalArial',8);canvas.drawString(43,24,'EVSE federated continual learning | Frozen final experiment');canvas.drawRightString(A4[0]-43,24,f'{doc.page} / 2')
    SimpleDocTemplate(str(OUT/'SUMMARY.pdf'),pagesize=A4,leftMargin=43,rightMargin=43,topMargin=32,bottomMargin=36,title='Balanced plus rare replay: final results',author='Yuvaraj').build(story,onFirstPage=footer,onLaterPages=footer)
    assert len(PdfReader(OUT/'SUMMARY.pdf').pages)==2
    print('Created two-page summary and complete results notes.',flush=True)

if __name__=='__main__':main()
