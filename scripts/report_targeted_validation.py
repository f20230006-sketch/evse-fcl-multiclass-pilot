"""Short review summary plus full numerical notes; mail stays outside archives."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape
OUT=ROOT/'outputs/targeted_validation_report_2026_10_27'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
LABELS={'class_balanced_60':'Class-balanced','protected_60':'Protected','balanced_rare_60':'Balanced+rare','rare_random_60':'Rare+random'}
def main():
    verify=json.loads((OUT/'verification.json').read_text());assert verify['status']=='passed'
    summary=pd.read_csv(OUT/'summary.csv');pairs=pd.read_csv(OUT/'paired_intervals.csv');cons=pd.read_csv(OUT/'split_consistency.csv')
    def row(split,env,method,space='merged_scans'):return summary[(summary.split_seed==split)&(summary.environment==env)&(summary.method==method)&(summary.score_space==space)].iloc[0]
    def pair(split,env,metric,left='balanced_rare_60',right='class_balanced_60',space='merged_scans'):
        return pairs[(pairs.split_seed==split)&(pairs.environment==env)&(pairs.metric==metric)&(pairs.left==left)&(pairs.right==right)&(pairs.score_space==space)&(pairs.order=='averaged')].iloc[0]
    def value(r,m):return f"{100*r[m+'_mean']:.2f} +/- {100*r[m+'_std']:.2f}"
    def delta(r):return f"{100*r.mean_difference:+.2f} [{100*r.ci95_low:+.2f}, {100*r.ci95_high:+.2f}]"
    mainrows=[[LABELS[m]]+[value(row(42,'federated',m),k) for k in METRICS] for m in LABELS]
    splitrows=[]
    for split in [42,43,44,45]:
        for env in ['federated','centralized']:
            a=pair(split,env,'old_task_accuracy');b=pair(split,env,'slowloris_recall');w=pair(split,env,'worst_client_macro_recall')
            splitrows.append([str(split),'Fed.' if env=='federated' else 'Central',delta(a),delta(b),delta(w)])
    ablation=[]
    for left,right in [('rare_random_60','protected_60'),('balanced_rare_60','rare_random_60')]:
        ablation.append([LABELS[left]+' - '+LABELS[right]]+[delta(pair(42,'federated',m,left,right)) for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']])
    exact=[]
    for env in ['federated','centralized']:
        for space in ['merged_scans','original_type']:
            exact.append(['Fed.' if env=='federated' else 'Central','Merged' if space=='merged_scans' else 'Exact']+[delta(pair(42,env,m,space=space)) for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']])
    consistency=[]
    for env in ['federated','centralized']:
        f=cons[(cons.score_space=='merged_scans')&(cons.environment==env)].set_index('metric')
        consistency.append(f"{env.capitalize()}: old-accuracy differences are positive on {int(f.loc['old_task_accuracy','positive_differences'])}/4 splits, significantly better on {int(f.loc['old_task_accuracy','significant_better'])}/4; Slowloris differences are positive on {int(f.loc['slowloris_recall','positive_differences'])}/4, significantly better on {int(f.loc['slowloris_recall','significant_better'])}/4. Worst-client score is significantly worse on {int(f.loc['worst_client_macro_recall','significant_worse'])}/4.")
    def mdtable(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(r)+' |' for r in rows])
    md='# Targeted validation results - 27 October 2026\n\n## What was done\n\n- Repeated the key memory-60 comparison on three additional persistent-role splits, using the accepted model and calibration-only selection.\n- Added rare reservation with random remainder and no benign quota on the original split.\n- Re-scored merged-Scan and exact-type views, checked grouping metadata and inspected public FedCBDR code.\n- Revised the letter with the validation results, allocation ablation and 17 references.\n\n## Main results\n\nFederated, original split; percentages, mean +/- SD of ten seed averages across three orders.\n\n'+mdtable(['Method','Old accuracy','Forgetting','Slowloris','Worst-client'],mainrows)+'\n\n## Cross-split comparisons\n\nBalanced+rare minus class-balanced, percentage points [95% paired interval]. Each split uses ten paired training seeds averaged across the three orders. An interval excluding zero is significant; negative forgetting is better.\n\n'+mdtable(['Split','Setting','Old accuracy','Slowloris','Worst-client'],splitrows)+'\n\n## What this means\n\n'+'\n\n'.join(consistency)+'\n\n## Allocation ablation\n\nOriginal split, federated differences [95% interval].\n\n'+mdtable(['Comparison','Old accuracy','Slowloris','Worst-client'],ablation)+'\n\n## Exact-type sensitivity\n\nOriginal split, balanced+rare minus class-balanced [95% interval].\n\n'+mdtable(['Setting','View','Old accuracy','Slowloris','Worst-client'],exact)+'\n\n## Evidence scope\n\nThe extra splits reuse overlapping flows from the same dataset, not new captures. Source filenames are available provenance groups, but no explicit session/capture column was found. Flow IDs and timestamps are not established session groups. File-level coverage is documented; no new splitting pipeline was built. Benign evaluation remains 16 flows and fragmentation five, so neither false-alarm nor fragmentation gains are claimed. The class-balanced and rare reservations operate on original types even for merged reporting.\n\nPublic FedCBDR code exists but the inspected checkout has missing imported modules, an unsupported README method name, and an image/CUDA pipeline. It was not reconstructed or presented as a baseline. Our allocation is local, with no additional coordination messages, whereas FedCBDR uses global memory coordination and objective/logit balancing.\n\nAll 132 calibration fits precede all 420 new evaluation runs. Saved models, roles, replay boundaries, '+str(verify['prediction_rows'])+' checkpoint prediction rows and '+str(verify['paired_intervals'])+' intervals passed verification. No exploratory tuned-model results replace the accepted protocol.\n'
    (OUT/'SUMMARY.md').write_text(md,encoding='utf-8')
    full=md+'\n\n# Full tables\n\n'
    for filename in ['summary.csv','paired_intervals.csv','per_order_summary.csv','split_consistency.csv']:
        f=pd.read_csv(OUT/filename);full+='\n## '+filename+'\n\n'+mdtable(list(f.columns),[[str(v) for v in r] for r in f.itertuples(index=False,name=None)])+'\n'
    trials=json.loads((ROOT/'outputs/targeted_validation_2026_10_27/hyperparameter_trials.json').read_text());full+='\n## Calibration choices\n\n```json\n'+json.dumps(trials,indent=2)+'\n```\n'
    full+='\n## Memory and allocation components\n\nMemory 60 means at most 60 stored fitting flows per client, not epochs or test examples. Five clients can retain 300 flows in total; centralized comparison receives 300 slots. A 10% rare reservation means up to six reserved slots per client when candidates exist, and 20% means up to twelve. The remainder can retain additional rare examples; the reservation is a minimum, not a cap. This round does not change the accepted MLP or sweep additional model hyperparameters.\n\n| Policy | Rare reservation | Remaining slots | Separate benign reservation |\n|---|---|---|---|\n| Class-balanced | None | Feasible class-balanced | None; ordinary class |\n| Protected | Fixed 20% | Uniform random | Fixed 20% when feasible |\n| Balanced+rare | Calibration-selected 10%/20%, balanced within rare group | Feasible class-balanced | None; ordinary class |\n| Rare+random | Calibration-selected 10%/20%, uniform within rare group | Uniform random | None; ordinary class |\n\n## Ablation interpretation\n\nRare+random removes the benign reservation and random-fills after a rare minimum. Its quota is calibrated at 10%/20%, while the historical protected quota was fixed at 20%. Thus comparisons show allocation-policy performance and do not isolate a single causal benign-quota effect when selected rare quotas differ. Balanced+rare also balances inside the reserved group, whereas the protected-style rare+random reservation samples uniformly within that group. This is not a fully crossed component factorial. All losses are reported.\n'
    (OUT/'INFO.md').write_text(full,encoding='utf-8')
    styles=getSampleStyleSheet();styles['Normal'].fontSize=8;styles['Normal'].leading=10;styles['Heading1'].fontSize=14;styles['Heading2'].fontSize=10
    story=[]
    def para(text,style='Normal'):story.append(Paragraph(escape(text),styles[style]));story.append(Spacer(1,5))
    def table(headers,rows,widths):
        t=Table([[Paragraph(escape(str(c)),styles['Normal']) for c in r] for r in [headers,*rows]],colWidths=widths,repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,colors.grey),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4)]));story.append(t);story.append(Spacer(1,8))
    para('Targeted validation results | 27 October 2026','Heading1')
    para('What was done','Heading2')
    para('Three additional role splits; the same 64/32 MLP and calibration-only replay selection. Memory is 60 stored flows per client, with 300 pooled slots centrally. A rare+random/no-benign ablation, both scoring views, provenance check and public FedCBDR feasibility review complete the requested additions.')
    para('Main results: original split, federated, memory 60','Heading2');para('Percentages; mean +/- SD over ten seed averages of three attack orders.')
    table(['Method','Old acc.','Forget','Slowloris','Worst-client'],mainrows,[110,94,94,94,94])
    para('Key comparison across splits','Heading2');para('Balanced+rare minus class-balanced, percentage points [95% interval]. Intervals excluding zero are significant. Split 42 is the original reference.')
    table(['Split','Setting','Old accuracy','Slowloris','Worst-client'],splitrows,[30,44,134,139,139])
    for text in consistency:para(text)
    story.append(PageBreak())
    para('Allocation and sensitivity results','Heading1')
    para('Allocation ablation: original split, federated','Heading2');table(['Comparison','Old accuracy','Slowloris','Worst-client'],ablation,[122,120,122,122])
    para('Rare+random has no benign minimum. Quota selection and within-rare sampling can also differ from protected/balanced+rare; this is an allocation-policy comparison, not a complete causal factorial.')
    para('Merged versus exact-type sensitivity','Heading2');table(['Setting','View','Old accuracy','Slowloris','Worst-client'],exact,[44,43,131,134,134])
    para('Evidence and verification','Heading2')
    para('The extra splits reuse the same sampled traffic and fixed client allocation. Source filenames, flow IDs and timestamps exist; no explicit session/capture column was found. File class coverage is documented. No new group-splitting pipeline was built. Benign support remains 16 and fragmentation support five; no false-alarm or fragmentation claims are made.')
    para('FedCBDR public code exists, but the checked version has missing local imports and an unsupported README method, and expects image/CUDA processing. A faithful baseline needs reconstruction. The letter explains its globally coordinated replay/objective design versus our local allocator with no added allocation communication.')
    para(f"All 132 calibration fits and 420 new evaluation runs completed. Verification passed for {verify['models_checked']} models, {verify['checkpoints']} checkpoints, {verify['prediction_rows']:,} prediction rows and {verify['paired_intervals']} paired intervals. Intervals are unadjusted; overlapping random splits are sensitivity checks rather than independent capture validation.")
    para('The separate exploratory larger-MLP study is excluded. Full per-order results, all losses and calibration choices are retained in INFO.md and CSV tables.')
    SimpleDocTemplate(str(OUT/'SUMMARY.pdf'),pagesize=A4,rightMargin=35,leftMargin=35,topMargin=30,bottomMargin=30).build(story)
    email="Subject: Additional validation results and revised Networking Letters draft\n\nDear Ma'am,\n\nI completed the requested additions using the agreed model and calibration-only selection. Please find attached the short results summary and revised Networking Letters draft.\n\nBalanced+rare significantly improved old-attack accuracy and Slowloris recall over class-balanced replay on the original and all three additional federated splits, with no statistically significant worst-client decline. On the new splits, old-attack accuracy improved by 2.06-3.37 percentage points and Slowloris recall by 6.09-11.28 points. Centralized gains were also positive, although significance varied across splits.\n\nThe rare+random ablation retained higher Slowloris recall but lower retention and worst-client scores. I included both scoring views, checked the grouping information and public FedCBDR code, and expanded the related work. All detailed results and limitations are documented in the accompanying notes. The complete raw evidence is available separately.\n\nBest regards,\nYuvaraj J. Nayak\n"
    (ROOT/'outputs/TARGETED_VALIDATION_EMAIL_DRAFT_2026_10_27.txt').write_text(email,encoding='utf-8')
    print('Summary PDF, full notes and separate mail draft created.')
if __name__=='__main__':main()
