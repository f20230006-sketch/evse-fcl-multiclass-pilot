"""Two-page results summary and detailed final-analysis information."""
from pathlib import Path
import json
import sys
from xml.sax.saxutils import escape
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.scan_final import CORE,RARE_TYPES,paired_interval
OUT=ROOT/'outputs/final_scan_analysis'
LABELS={'no_replay':'No replay','uniform_60':'Uniform','class_balanced_60':'Class-balanced','protected_60':'Protected','ewc':'EWC','agem':'A-GEM','joint':'Joint'}

def pct(x):return 'N/A' if pd.isna(x) else f'{100*x:.2f}'
def mean_sd(r,m):return 'N/A' if pd.isna(r[m+'_mean']) else f'{100*r[m+"_mean"]:.2f} ± {100*r[m+"_std"]:.2f}'
def interval(r):return f"{100*r.mean_difference:+.2f} [{100*r.ci95_low:.2f}, {100*r.ci95_high:.2f}]; {r.significance}"
def table_md(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers)]+['| '+' | '.join(str(x) for x in r)+' |' for r in rows])

def main():
    s=pd.read_csv(OUT/'merged_summary.csv');p=pd.read_csv(OUT/'merged_paired_intervals.csv');interaction=pd.read_csv(OUT/'merged_federation_interactions.csv');rf=json.loads((OUT/'random_forest/summary.json').read_text());rare=pd.read_csv(OUT/'rare_classes_summary.csv');ri=pd.read_csv(OUT/'rare_federation_interactions.csv');clients=pd.read_csv(OUT/'focus_clients_summary.csv')
    def lookup(env,m):return s[(s.environment==env)&(s.method==m)].iloc[0]
    def comparison(b,m='old_task_accuracy'):
        return p[(p.environment=='federated')&(p.order=='averaged')&(p.left=='protected_60')&(p.right==b)&(p.metric==m)].iloc[0]
    main_rows=[[LABELS[m]]+[mean_sd(lookup('federated',m),k) for k in CORE] for m in LABELS]
    sweep_rows=[]
    for n in [60,120,300]:sweep_rows.append([str(n)]+[pct(lookup('federated',f'{m}_{n}').old_task_accuracy_mean)+' / '+pct(lookup('federated',f'{m}_{n}').rare_attack_recall_mean) for m in ['uniform','class_balanced','protected']])
    rare_rows=[]
    for method in ['joint','uniform_60','class_balanced_60','protected_60']:
        row=[LABELS[method]]
        for c in RARE_TYPES:
            vals=[]
            for env in ['federated','centralized']:vals.append(pct(rare[(rare.score_space=='original_type')&(rare.environment==env)&(rare.method==method)&(rare['class']==c)].iloc[0].recall_mean))
            row.append(' / '.join(vals))
        rare_rows.append(row)
    old_interaction=interaction[(interaction.memory_per_client==60)&(interaction.baseline=='uniform')&(interaction.metric=='old_task_accuracy')].iloc[0]
    high_memory=p[(p.environment=='federated')&(p.order=='averaged')&(p.left=='protected_300')&(p.right=='uniform_300')&(p.metric=='old_task_accuracy')].iloc[0]
    slow=ri[(ri.score_space=='original_type')&(ri['class']=='Slowloris_Scan')&(ri.memory_per_client==300)&(ri.baseline=='uniform')].iloc[0]
    bullets=[
        'Trained a scan-only Random Forest to test whether six scan types can be distinguished.',
        'Re-scored all 840 saved runs with the six scan probabilities summed into one Scan class; no MLP retraining.',
        'Compared Slowloris and ICMP fragmentation separately, federated versus centralized, and examined the rare-heavy and benign-starved clients.',
        'Reconstructed the 33.33% rare-recall result from class counts and attack orders.'
    ]
    key_lines=[
        'Protected − uniform: old accuracy '+interval(comparison('uniform_60'))+'. At memory 300: '+interval(high_memory)+'.',
        'Protected − class-balanced: old accuracy '+interval(comparison('class_balanced_60'))+'; rare recall '+interval(comparison('class_balanced_60','rare_attack_recall'))+'.',
        'Federated − centralized difference in protected-over-uniform old-accuracy improvement: '+interval(old_interaction)+'.'
    ]
    interpretation=[
        f'Random Forest accuracy is {100*rf["accuracy_mean"]:.2f}% ± {100*rf["accuracy_std"]:.2f}% versus 16.67% chance (100% fitting accuracy). The six scans are not shown to be indistinguishable; merged results are an alternative view.',
        'At memory 60, protected replay improves merged rare recall over class-balanced replay but gives lower old accuracy and worst-client score. There is no supported extra overall retention benefit from federation.',
        'Federated training shows large rare-type deficits under joint training (table below). Protection does not narrow the gap more than uniform at memory 60. For Slowloris at memory 300, extra gap reduction: '+interval(slow)+' (percentage points; exploratory, unadjusted for multiple comparisons).'
    ]
    problems=[
        'ICMP fragmentation has only 5 test examples, versus 600 Slowloris examples. Benign test support remains 16; benign-starved false alarm rate is undefined.',
        'The original rare metric is (correct Slowloris + correct ICMP fragmentation) / 605. Federated no replay is 0%, 100%, 0% across orders, averaging 33.33%. Both types are correct only when rare attacks come last; neither is always correct across orders. EWC is 33.31% ± 0.03%, not exactly 33.33% ± 0.00%.',
        'Merged scores retain original old-task cohorts and type-level replay policies. Coarsening changes task overlap; it is not evidence that forgetting was fixed. Intervals describe training randomness on one split, not new independent captures.'
    ]
    questions=[
        'Given the above-chance Random Forest result, should exact attack types remain primary and merged-Scan scores be a sensitivity analysis?',
        'Should the letter emphasize the retention/rare-recall trade-off, with the Slowloris federation interaction labeled exploratory? No further experiments are proposed.'
    ]
    headers=['Method','Old accuracy','Forgetting','Rare recall','Worst-client score']
    summary=['# Final checks: short results summary','', '17 October 2026 | All table values are percentages; comparisons are percentage points.','', '## 1. What was done','']+['- '+b for b in bullets]
    summary+=['','## 2. Main results table','','Merged-Scan scores, federated setting, final checkpoint. Mean ± SD over ten seed averages across three orders; replay capacity 60 per client. Old accuracy refers to original old-task cohorts. Worst-client score is supported-class macro recall.','',table_md(headers,main_rows),'','Memory sweep: old accuracy / rare recall. Size is per client; centralized totals are five times larger.','',table_md(['Memory','Uniform','Class-balanced','Protected'],sweep_rows),'','## 3. Key comparisons','']+['- '+t for t in key_lines]
    summary+=['','## 4. What this means','']+['- '+t for t in interpretation]
    summary+=['','Original type-level rare recall (federated / centralized), memory 60 for replay:','',table_md(['Method','Slowloris','ICMP fragmentation'],rare_rows),'','## 5. Problems or surprises','']+['- '+t for t in problems]
    summary+=['','## 6. Questions for review','']+['- '+t for t in questions]
    (OUT/'SUMMARY.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
    # Full information: include every requested setting, client and interval outside the short summary.
    info=['# Final analysis information','','Read SUMMARY.pdf first (two pages). This file and the CSVs provide the detailed reference. No email drafts or implementation files are included in the results archives.','','## Scan-only Random Forest check','',f'Pooled fitting rows from the six scan types only. The original fitting/calibration/evaluation roles and three frozen first-task representations were retained. Two prespecified forest settings were screened on calibration data at seed 42, then the selected setting was run with seeds 42–51 for each representation: 6 calibration fits and 30 evaluation fits. These are diagnostic classifiers, not new continual-learning runs. No calibration rows were added to fitting.','',f'Accuracy / balanced accuracy: {100*rf["accuracy_mean"]:.2f}% ± {100*rf["accuracy_std"]:.2f}%; six-class chance 16.67%; fitting accuracy 100%. Above-chance difference: '+interval(pd.Series(rf['accuracy_above_chance']))+' points. The six classes each have 600 evaluation examples. These fixed-split seed intervals do not establish cross-capture generalization. This result does not support the condition that all six types are near chance, so merging is not justified as proven intrinsic indistinguishability. The original MLP loss plateau alone does not establish an irreducible error floor.','',table_md(['Scan type','RF recall (%)'],[[c,pct(g.recall.mean())] for c,g in pd.read_csv(OUT/'random_forest/per_class_metrics.csv').groupby('class')]),'','## Exact merged scoring definition','','Only Aggressive_Scan, OS_Fingerprinting, SYN_Stealth_Scan, Service_Version_Detection, TCP_Port_Scan and Vulnerability_Scan map to Scan. Slowloris_Scan stays separate. Six probabilities are summed before argmax; the resulting output space has 10 labels. No training labels, weights or stored replay examples changed. The class-balanced memories were originally balanced over 15 types, not the 10 merged labels. Scan spans the original reconnaissance and vulnerability cohorts; retention/forgetting use those original cohorts rather than pretending a new independent merged task sequence was trained.','', 'Raw re-scores are in merged_predictions/. Every checkpoint stores indices, merged truth and predicted labels. The final checkpoint also stores full merged probabilities. Original source probability arrays are referenced and hashed in saved_prediction_input_hashes.json; they remain in the earlier evidence archive rather than being duplicated here.','', '## All merged main results','',table_md(['Environment','Method']+headers[1:],[[r.environment,r.method]+[mean_sd(r,k) for k in CORE] for _,r in s.iterrows()]),'','## Key comparisons at every memory and order','',table_md(['Environment','Order','Protected method','Comparison','Metric','Difference [95% interval]; result'],[[r.environment,r.order,r.left,r.right,r.metric,interval(r)] for _,r in p.iterrows()]),'','## What federation adds','','The experimental question is how local fitting and per-client bounded memories under heterogeneous client profiles affect retention and rare-type recall compared with pooled training at the same system memory budget. A replay benefit that appears equally in both settings is not a federation-specific contribution. The clear observed joint-model rare-type deficits locate a federated robustness problem, but do not by themselves show that protection uniquely solves it. These comparisons include the separately calibrated procedures; they do not isolate a pure causal effect of averaging alone.','', 'Signed deficit is centralized recall minus federated recall. A positive interaction means protection reduces that signed deficit more than its comparison method.','',table_md(['Score space','Class','Method','Centralized−federated recall [95% interval]'],[[r.score_space,r['class'],r.method,interval(r)] for _,r in pd.read_csv(OUT/'rare_federated_deficits.csv').iterrows()]),'','## Per-class protection interactions','',table_md(['Score space','Class','Memory/client','Baseline','Extra gap reduction [95% interval]'],[[r.score_space,r['class'],int(r.memory_per_client),r.baseline,interval(r)] for _,r in ri.iterrows()]),'','The memory-60 protected-versus-uniform interactions are not significant for either rare type. Original-type Slowloris at memory 300 has an interaction of '+interval(slow)+' points. This is a secondary comparison among many unadjusted contrasts; it should be described as exploratory, not selected after viewing results as a new confirmatory primary endpoint. ICMP fragmentation does not show a supported protection-over-uniform gap reduction.','', '## Rare-heavy and benign-starved clients','','Both original-type and merged scores are reported below for every replay capacity and joint reference, in both environments. Full seed/order rows and paired client intervals are supplied as CSVs. N/A means no supported evaluation examples, not zero recall. FPR at the benign-starved client is undefined. These are synthetic allocation profiles evaluated with the global model, not personalized local models or five independently captured physical stations.']
    replay_methods=['joint']+[f'{m}_{n}' for n in [60,120,300] for m in ['uniform','class_balanced','protected']]
    columns=['old_task_accuracy','forgetting','macro_recall','rare_attack_recall','Slowloris_Scan_recall','ICMP_Fragmentation_recall','false_alarm_rate']
    for (space,env,client),group in clients[clients.method.isin(replay_methods)].groupby(['score_space','environment','client']):
        info+=['',f'### {space} / {env} / {client}','',table_md(['Method','Old accuracy','Forgetting','Macro recall','Combined rare','Slowloris','Fragmentation','FPR'],[[r.method]+[mean_sd(r,k) for k in columns] for _,r in group.iterrows()])]
    info+=['','## Clarification of 33.33%','','The original combined rare recall weights 600 Slowloris examples and 5 ICMP-fragmentation examples by their supports; it is not the unweighted mean of two recalls or a mean over three classes. The separate macro-rare metric is distinct. For federated no replay, both types have 100% recall only in order 2, where rare attacks are last, and both have 0% in orders 1/3. Each seed therefore averages (0 + 1 + 0)/3 = 1/3, giving zero seed SD. Neither class is always correct across attack orders. EWC has some fragmentation misses in order 2, giving 33.31% ± 0.03% federated. Centralized no replay and EWC also have misses and differ slightly from 33.33%. See rare_metric_reconstruction.csv and rare_baseline_class_breakdown.csv.','','## Evidence and limitations','','All 840 original runs were re-scored; no MLP was retrained. The independent verification JSON checks every merged checkpoint against original probabilities, input hash preservation, paired calculations, RF role boundaries, and rare-metric reconstruction. Three new unit tests cover the mapping, probability-sum decision rule and ten-pair interval requirement. Original results and the earlier 17-test evidence remain preserved. Five fragmentation test examples and sixteen benign examples limit claims. Results are frozen for review; manuscript writing and additional experiments remain on hold.']
    (OUT/'INFO.md').write_text('\n'.join(info)+'\n',encoding='utf-8')
    create_pdf(headers,main_rows,sweep_rows,rare_rows,bullets,key_lines,interpretation,problems,questions)
    email="""Subject: Final FCL checks and short summary

Dear Ma'am,

I have completed the requested final analyses. Please find the two-page summary attached; the detailed results archive is provided separately for reference.

The scan-only Random Forest achieved 34.25% accuracy versus 16.67% chance, so the assumption that all six scans are indistinguishable is not supported. The summary also includes the merged-scan results, separate rare-attack/client comparisons, and the explanation of the 33.33% recall value.

The original models and results have been preserved. I will hold off on manuscript writing until we review these findings and agree on the main message.

Best regards,
Yuvaraj
"""
    (ROOT/'outputs/FINAL_SCAN_EMAIL_DRAFT.txt').write_text(email,encoding='utf-8')
    print(OUT/'SUMMARY.pdf')

def create_pdf(headers,main_rows,sweep_rows,rare_rows,bullets,keys,meaning,problems,questions):
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from pypdf import PdfReader
    font='Helvetica';bold='Helvetica-Bold'
    if Path('C:/Windows/Fonts/arial.ttf').exists():
        pdfmetrics.registerFont(TTFont('ReportArial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ReportArialBold','C:/Windows/Fonts/arialbd.ttf'));pdfmetrics.registerFontFamily('ReportArial',normal='ReportArial',bold='ReportArialBold');font='ReportArial';bold='ReportArialBold'
    styles=getSampleStyleSheet();body=ParagraphStyle('BodyFinal',fontName=font,fontSize=9.4,leading=12.4,spaceAfter=4);small=ParagraphStyle('SmallFinal',parent=body,fontSize=8.5,leading=10.8);heading=ParagraphStyle('HeadingFinal',fontName=bold,fontSize=11,leading=14,spaceBefore=9,spaceAfter=5);title=ParagraphStyle('TitleFinal',fontName=bold,fontSize=16,leading=19,spaceAfter=5)
    def para(t,style=body):return Paragraph(escape(t),style)
    def section(t):return para(t,heading)
    def bullet(t):return Paragraph('• '+escape(t),body)
    def table(head,rows,widths):
        data=[[Paragraph(escape(str(c)),ParagraphStyle('Cell',parent=small,fontName=bold)) for c in head]]+[[para(str(c),small) for c in r] for r in rows]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8edf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#9aa9bb')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f8fa')]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return t
    story=[para('Final FCL checks: results summary',title),para('17 October 2026 | Main numbers and decisions',small),section('1. What was done')]+[bullet(t) for t in bullets]
    story += [section('2. Main results table'),para('Merged-Scan scores; federated final checkpoint. Mean ± SD over ten seed averages across three orders. Replay memory: 60/client. Old accuracy uses the original old-task cohorts; worst-client score is macro recall.',small),table(headers,main_rows,[105,102,94,100,108]),Spacer(1,5),para('Memory sweep: old accuracy / rare recall (%). Size is per client; centralized totals are ×5.',small),table(['Memory','Uniform','Class-balanced','Protected'],sweep_rows,[65,148,148,148]),section('3. Key comparisons'),para('Differences are percentage points with paired-seed 95% intervals.',small)]+[bullet(t) for t in keys]
    story += [PageBreak(),section('4. What this means')]+[bullet(t) for t in meaning]
    story += [Spacer(1,5),para('Separate rare recalls: original type scores, federated / centralized (%); memory 60 for replay.',small),table(['Method','Slowloris','ICMP fragmentation'],rare_rows,[145,182,182]),section('5. Problems or surprises')]+[bullet(t) for t in problems]
    story += [section('6. Questions for review')]+[bullet(t) for t in questions]
    story += [Spacer(1,5),para('Full client tables, all memory/order comparisons, protocols and verification remain in INFO.md and the reference archive. No manuscript has been drafted.',small)]
    def footer(canvas,doc):
        canvas.setFont(font,8);canvas.setFillColor(colors.HexColor('#526172'));canvas.drawString(43,24,'EVSE federated continual learning | Final checks');canvas.drawRightString(A4[0]-43,24,f'{doc.page} / 2')
    SimpleDocTemplate(str(OUT/'SUMMARY.pdf'),pagesize=A4,rightMargin=43,leftMargin=43,topMargin=33,bottomMargin=36,title='Final FCL checks — results summary',author='Yuvaraj').build(story,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(OUT/'SUMMARY.pdf');assert len(reader.pages)==2,f'Summary must be two pages, got {len(reader.pages)}'
    print('PDF verified: two pages')

if __name__=='__main__':main()
