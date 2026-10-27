"""Exploratory update: all gains/losses, matched controls, and separate reply draft."""
from pathlib import Path
import json,sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/exploratory_tuning_report_2026_10_27'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
LABELS={'class_balanced_60':'Frozen balanced','protected_60':'Frozen protected','balanced_rare_60':'Frozen balanced+rare','tuned_class_balanced_60':'Tuned balanced','tuned_protected_60':'Tuned protected','tuned_balanced_rare_60':'Tuned balanced+rare'}

def value(r,m):return f'{100*r[m+"_mean"]:.2f} ± {100*r[m+"_std"]:.2f}'
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])

def main():
    s=pd.read_csv(OUT/'summary.csv');ci=pd.read_csv(OUT/'paired_intervals.csv');orders=pd.read_csv(OUT/'per_order_summary.csv')
    run=ROOT/'outputs/exploratory_tuning_2026_10_27';selection=json.loads((run/'backbone_selection.json').read_text());settings=selection['settings']
    header=['Method','Old accuracy','Forgetting','Slowloris','Worst client']
    def rows(env):
        return [[label]+[value(s[(s.score_space=='merged_scans')&(s.environment==env)&(s.method==m)].iloc[0],k) for k in METRICS] for m,label in LABELS.items()]
    def contrast(baseline,metric,env='federated'):
        r=ci[(ci.score_space=='merged_scans')&(ci.environment==env)&(ci.order=='averaged')&(ci.left=='tuned_balanced_rare_60')&(ci.right==baseline)&(ci.metric==metric)].iloc[0]
        return f'{100*r.mean_difference:+.2f} [{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]; {r.outcome}'
    configtext=f"Shared selected MLP: {settings['hidden_sizes'][0]}/{settings['hidden_sizes'][1]}, learning rate {settings['learning_rate']}, dropout {settings['dropout']}, weight decay {settings['weight_decay']}, {settings['local_epochs']} local epochs, five rounds/task."
    a,b=settings['hidden_sizes'];parameters={o:n*a+a+a*b+b+b*15+15 for o,n in zip(['order_1','order_2','order_3'],[138,86,130])}
    (OUT/'model_profile.json').write_text(json.dumps({'selected':settings,'parameter_counts':parameters,'frozen_parameter_counts':{'order_1':11471,'order_2':8143,'order_3':10959},'replay_examples_per_client':60,'centralized_replay_examples':300,'total_memory_bytes_not_matched':a!=64 or b!=32},indent=2)+'\n',encoding='utf-8')
    bullets=['Completed 108 common-configuration calibration fits, 72 replay calibration fits, then 180 evaluations: three methods × three orders × two settings × ten seeds.',configtext,'Storage remains 60 examples/client and 300 centrally. Original labels, splits, client allocations and Task-1 preprocessing remain unchanged.',f'Model parameter counts by order: {parameters["order_1"]:,}, {parameters["order_2"]:,}, {parameters["order_3"]:,}; model_profile.json records the frozen-model comparison.']
    key=['Tuned balanced+rare − frozen balanced+rare: old accuracy '+contrast('balanced_rare_60','old_task_accuracy')+'; forgetting '+contrast('balanced_rare_60','forgetting')+'; Slowloris '+contrast('balanced_rare_60','slowloris_recall')+'; worst client '+contrast('balanced_rare_60','worst_client_macro_recall')+'.']
    matched=[[label]+[contrast(m,k) for k in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']] for m,label in [('tuned_class_balanced_60','vs tuned balanced'),('tuned_protected_60','vs tuned protected')]]
    interpretation=['The tuned policy improves federated retention, forgetting and Slowloris versus its frozen version, but worst-client score falls by 1.77 points significantly. This is not an across-the-board improvement. A larger model and changed selection/training pipeline contribute; gains cannot automatically be credited to the quota.',
        'Against newly tuned class-balanced, old accuracy and Slowloris improve significantly; worst-client difference is not significant. Against tuned protected, old accuracy and worst-client score improve significantly, while the Slowloris difference is not significant. Non-significance does not establish equivalence.',
        'Selection used the new final-calibration retention/Slowloris/worst-client objective. Earlier evaluation outcomes were already known: this is exploratory, not untouched-test confirmation. All orders and losses are included; ten-seed intervals describe one fixed split and are unadjusted for multiplicity.']
    md=['# Exploratory model tuning: results update','','27 October 2026 | Percentages; paired differences in percentage points.','','## 1. Work completed','']+['- '+b for b in bullets]
    md+=['','## 2. Federated results','','Mean ± SD over ten seed averages of three orders; merged-Scan primary scoring.','',table(header,rows('federated')),'','## 3. Frozen-to-tuned comparison','','Paired 95% intervals; better/worse denotes significant direction.']+['- '+k for k in key]
    md+=['','## 4. Centralized results','',table(header,rows('centralized')),'','## 5. Matched-backbone federated comparisons','','Tuned balanced+rare minus the other tuned method.','',table(['Comparison','Old accuracy','Slowloris','Worst client'],matched),'','## Interpretation','']+['- '+i for i in interpretation]
    md+=['','Only 16 benign and five fragmentation evaluation examples exist. No fragmentation or false-alarm improvement is inferred. Larger models, if selected, increase parameter storage; replay budgets count examples, not all memory bytes. The previously sent manuscript and results remain unchanged.']
    (OUT/'SUMMARY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    info=md+['','## Common model calibration scores','',table(['Candidate','Settings','Mean calibration objective'],[[i,json.dumps(v),f'{selection["scores"][i]:.6f}'] for i,v in enumerate(json.loads((ROOT/'configs/exploratory_tuning_2026_10_27.json').read_text())['backbone_candidates'])])]
    selected=json.loads((run/'hyperparameter_trials.json').read_text())
    info+=['','## Replay selections','',table(['Order','Environment','Method','Rare share','Replay fraction'],[[o,e,m,v['rare_quota_fraction'],v['replay_fraction']] for o,a in selected['selected'].items() for e,b in a.items() for m,v in b.items()]),'','The protected allocator always reserves 20% benign and 20% rare; class-balanced has no reservation. The new policy uses its selected rare share. All share the selected model configuration. The new criterion is an equal-weight final-calibration average of old accuracy, Slowloris recall and worst-client macro recall, replacing the earlier mean-checkpoint original-type criterion. This change is part of the pipeline comparison.']
    compute=pd.read_csv(OUT/'new_training_compute.csv').groupby(['environment','method'])[['optimizer_steps','elapsed_seconds']].mean().reset_index()
    info+=['','## Training work and model size','','The actual per-run settings and selected backbone are authoritative. Some top-level configuration fields are inherited frozen defaults and are overridden by these settings. A larger replay fraction reduces current examples per minibatch and increases optimizer steps for the same number of current-data epochs; compute is not matched. Elapsed times below are concurrent desktop execution observations, not controlled latency benchmarks or deployment measurements.','',table(['Environment','Method','Mean optimizer steps','Mean elapsed seconds'],[[r.environment,r.method,f'{r.optimizer_steps:.1f}',f'{r.elapsed_seconds:.2f}'] for _,r in compute.iterrows()]),'',json.dumps(parameters),'','Replay example counts remain matched; total model-memory bytes and optimizer work can differ from the frozen study.']
    info+=['','## Offline proof-of-concept demonstration','','Run scripts/demo_exploratory_model.py to load a saved tuned model and classify one deterministically selected evaluation example per merged class. Examples are selected before inspecting predictions; errors are retained. This is offline inference on prepared flow features, not a live packet IDS, a fresh test, calibrated probabilities or an accuracy estimate from ten examples. The 60-row replay budget is a logical access constraint in the offline simulator; full feature tensors remain resident for auditing, so it is not a measured physical-RAM limit.']
    for space in ['merged_scans','original_type']:
        for env in ['federated','centralized']:
            part=s[(s.score_space==space)&(s.environment==env)&s.method.isin(LABELS)]
            info+=['',f'## {space} / {env}','',table(header,[[r.method]+[value(r,k) for k in METRICS] for _,r in part.iterrows()])]
        for (env,o),group in ci[ci.score_space==space].groupby(['environment','order']):
            info+=['',f'## {space} / {env} / {o}: all comparisons','',table(['Left','Right','Metric','Difference','95% interval','Outcome','Scope'],[[r.left,r.right,r.metric,f'{100*r.mean_difference:+.2f}',f'[{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]',r.outcome,r.interpretation] for _,r in group.iterrows()])]
        info+=['',f'## {space}: every order','',table(['Environment','Method','Order']+header[1:],[[r.environment,r.method,r.order]+[value(r,k) for k in METRICS] for _,r in orders[(orders.score_space==space)&orders.method.isin(LABELS)].iterrows()])]
    (OUT/'INFO.md').write_text('\n'.join(info)+'\n',encoding='utf-8')
    pdf(header,rows('federated'),rows('centralized'),bullets,key,matched,interpretation)
    email="Subject: Exploratory model-tuning results\n\nDear Ma'am,\n\nI carried out a separate exploratory tuning comparison while preserving the original results and manuscript. Calibration selected a 128/64 MLP with learning rate 0.001. I applied the same selected model setup to all three replay methods and selected their replay settings using calibration data only.\n\nFor federated balanced + rare, old-attack accuracy increased from 85.52% to 87.53%, Slowloris recall from 76.62% to 81.77%, and forgetting fell from 14.24% to 11.69%; all three changes are significant. However, worst-client score decreased significantly from 79.03% to 77.26%, so this is a trade-off rather than an improvement in every metric.\n\nAgainst the newly tuned class-balanced baseline, old-attack accuracy and Slowloris recall also improved significantly, while the worst-client difference was not significant. The attached update includes paired intervals, both settings and every attack order, including losses.\n\nThe larger model and increased replay change model size and training work. Since the earlier evaluation results were already known, I have labelled this follow-up exploratory. Please review these findings before we change the manuscript's claims.\n\nBest regards,\nYuvaraj\n"
    (ROOT/'outputs/EXPLORATORY_TUNING_EMAIL_DRAFT_2026_10_27.txt').write_text(email,encoding='utf-8')

def pdf(headers,federated,centralized,bullets,keys,matched,interpretation):
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from xml.sax.saxutils import escape
    from pypdf import PdfReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont('TuneArial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('TuneArialBold','C:/Windows/Fonts/arialbd.ttf'))
    body=ParagraphStyle('b',fontName='TuneArial',fontSize=9.2,leading=12,spaceAfter=5);small=ParagraphStyle('s',parent=body,fontSize=8,leading=10)
    head=ParagraphStyle('h',fontName='TuneArialBold',fontSize=11,leading=14,spaceBefore=9,spaceAfter=5);title=ParagraphStyle('t',parent=head,fontSize=16,leading=19)
    def p(t,style=body):return Paragraph(escape(str(t)),style)
    def table(h,rows,widths):
        result=Table([[p(c,small) for c in row] for row in [h,*rows]],colWidths=widths,repeatRows=1)
        result.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfe8f2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return result
    story=[p('Exploratory model tuning: results update',title),p('27 October 2026 | Memory 60/client | Merged-Scan scores; Slowloris recall',small),p('1. Work completed',head)]+[p('• '+b) for b in bullets]
    story+=[p('2. Federated results',head),p('Percentages; mean ± SD over ten seed means across three orders.',small),table(headers,federated,[125,96,94,96,98]),p('3. Frozen-to-tuned comparison',head),p('Paired 95% intervals, percentage points.',small)]+[p('• '+k) for k in keys]
    story+=[PageBreak(),p('4. Centralized results',head),table(headers,centralized,[125,96,94,96,98]),p('5. Matched-backbone federated comparisons',head),p('Tuned balanced+rare minus the other tuned method; percentage points with 95% intervals.',small),table(['Comparison','Old accuracy','Slowloris','Worst client'],matched,[90,140,140,139]),p('Interpretation',head)]+[p('• '+i) for i in interpretation]
    story+=[Spacer(1,4),p('No fragmentation or false-alarm claim: only five fragmentation and 16 benign evaluation examples. Full setting/order tables and losses are in INFO.md. Earlier results and manuscript are preserved.',small)]
    def footer(c,d):c.setFont('TuneArial',8);c.drawString(43,24,'Exploratory follow-up | Not an untouched-test confirmation');c.drawRightString(A4[0]-43,24,f'{d.page} / 2')
    SimpleDocTemplate(str(OUT/'SUMMARY.pdf'),pagesize=A4,leftMargin=43,rightMargin=43,topMargin=32,bottomMargin=36,title='Exploratory model tuning results',author='Yuvaraj').build(story,onFirstPage=footer,onLaterPages=footer)
    assert len(PdfReader(OUT/'SUMMARY.pdf').pages)==2
    print('Exploratory summary, complete tables and separate reply draft created.')

if __name__=='__main__':main()
