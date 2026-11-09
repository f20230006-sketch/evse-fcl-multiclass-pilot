"""Complete calibration and evaluation analysis for the corrective alignment study."""
from pathlib import Path
import json,sys
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from evse_ids.scan_final import paired_interval
M=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']

def main():
 run=R/'outputs/teacher_alignment_2026_11_09';out=R/'outputs/teacher_alignment_report_2026_11_09';out.mkdir(exist_ok=True)
 completion=json.loads((run/'completion.json').read_text());hp=json.loads((run/'hyperparameter_trials.json').read_text());gate=json.loads((run/'calibration_gate.json').read_text());c=json.loads((run/'protocol_before_evaluation.json').read_text())['config']
 selected=pd.DataFrame([{**{k:s[k]for k in ['environment','alias','method','criterion','selection_score']},**s['settings']}for s in hp['selected']]);selected.to_csv(out/'selected_calibration.csv',index=False)
 pd.DataFrame([{**{k:s[k]for k in ['environment','alias','method','criterion','selection_score','trial_index']},**s['settings']}for s in hp['candidate_aggregates']]).to_csv(out/'calibration_candidates.csv',index=False)
 lines=['# Current model corrective study','', 'The prior paper, comparison studies and manuscript extension are unchanged. Diagnostics identified unprotected late first participation, a calibration/primary-score mismatch, and substantial Slowloris-to-Scan confusion. The old configuration prose also had stale descriptions; executed values and records remain authoritative.','', 'The new design compares teacher coverage, score-aligned selection and family-consistent distillation, with matched class-balanced controls. Calibration averages three initialization seeds. Role split64 reuses the existing corpus and is not independent external validation.','', '## Calibration gate','',json.dumps(gate,indent=2),'','192 actual calibration fits were completed before this gate. The two legacy selection criteria share the same calibration fits.']
 if completion['evaluation_runs']==0:
  lines+=['', 'Neither corrected variant met the prespecified calibration improvement threshold. No new evaluation runs were performed. This is a useful calibration-only negative finding; the current accepted model stays unchanged.']
  (out/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps(gate,indent=2));return
 records=[];clients=[];cost=[];coverage=[]
 for p in sorted((run/'runs').glob('*/*/seed_*/results.json')):
  r=json.loads(p.read_text());alias=p.parents[1].name;key={'environment':r['environment'],'alias':alias,'method':r['method'],'seed':r['seed']}
  for space,v in r['summary'].items():
   records.append({**key,'score_space':space,**v})
   clients.extend({**key,'score_space':space,'client':cl,**met}for cl,met in r['history'][-1]['scores'][space]['per_client'].items())
  logs=json.loads((p.parent/'training_log.json').read_text());cost.append({**key,'elapsed_seconds':r['elapsed_seconds'],'local_updates':len(logs),'optimizer_steps':sum(x['steps']for x in logs),'teacher_parameters':max(x.get('teacher_parameter_count',0)for x in logs)})
  coverage.extend({**key,'phase':x['phase'],'round':x['round'],'client':x['client'],'global_old_classes':len(x['global_old_seen']),'teacher_old_classes':x['teacher_old_classes']}for x in logs)
 f=pd.DataFrame(records);assert len(f)==240
 for name,df in [('all_per_run_metrics',f),('per_client_metrics',pd.DataFrame(clients)),('training_costs',pd.DataFrame(cost)),('teacher_coverage',pd.DataFrame(coverage))]:df.to_csv(out/(name+'.csv'),index=False)
 summary=f.groupby(['score_space','environment','alias'])[M].agg(['mean','std']);summary.columns=['_'.join(x)for x in summary.columns];summary.reset_index().to_csv(out/'summary.csv',index=False)
 comparisons=[('legacy_merged','legacy_exact'),('global','legacy_merged'),('family','legacy_merged'),('family','global'),('family','cb_family'),('family','cb_legacy'),('cb_family','cb_legacy')];pairs=[]
 for space in ['merged_scans','original_type']:
  for e in c['environments']:
   sub=f[(f.score_space==space)&(f.environment==e)]
   for left,right in comparisons:
    a=sub[sub.alias==left].set_index('seed');b=sub[sub.alias==right].set_index('seed');assert set(a.index)==set(b.index)==set(c['seeds'])
    for m in M:
     d=(a[m]-b[m]).sort_index();d=d.mask(d.abs()<1e-12,0);ci=paired_interval(d);better=ci['ci95_high']<0 if m=='forgetting'else ci['ci95_low']>0;worse=ci['ci95_low']>0 if m=='forgetting'else ci['ci95_high']<0
     pairs.append({'score_space':space,'environment':e,'left':left,'right':right,'metric':m,'outcome':'better'if better else'worse'if worse else'not significant',**ci})
 pc=pd.DataFrame(pairs);pc.to_csv(out/'paired_intervals.csv',index=False)
 primary=pc[(pc.score_space=='merged_scans')&(pc.environment=='federated')&(pc.left=='family')&(pc.right=='legacy_merged')].set_index('metric')
 screen={'slowloris_positive_lower_bound':bool(primary.loc['slowloris_recall','ci95_low']>0),'old_accuracy_lower_above_minus_one_point':bool(primary.loc['old_task_accuracy','ci95_low']>-.01),'worst_client_lower_above_minus_one_point':bool(primary.loc['worst_client_macro_recall','ci95_low']>-.01)};screen['all_prespecified_conditions_met']=all(screen.values());(out/'prespecified_screen.json').write_text(json.dumps(screen,indent=2))
 lines+=['','## Matched delayed federated results','','| Alias | Old accuracy | Forgetting | Slowloris | Worst client |','|---|---:|---:|---:|---:|']
 for alias in c['aliases']:
  sub=f[(f.score_space=='merged_scans')&(f.environment=='federated')&(f.alias==alias)];lines.append('| '+alias+' | '+' | '.join(f'{100*sub[m].mean():.2f} ± {100*sub[m].std(ddof=1):.2f}'for m in M)+' |')
 lines+=['','Percentages, mean ± sample SD over ten evaluation seeds. These scores must not be compared directly with earlier partitions.','', '## Primary family correction versus legacy merged selection','']
 for m,row in primary.iterrows():lines.append(f'- {m}: {100*row.mean_difference:+.2f} points [{100*row.ci95_low:.2f},{100*row.ci95_high:.2f}]; {row.outcome}.')
 lines+=['','## Prespecified exploratory screen','',json.dumps(screen,indent=2),'','All controls, both score views and all unfavorable outcomes are retained. Correct teacher coverage is a software/design correction; it does not by itself establish improved generalization. Criterion changes and model changes have distinct ablations. All intervals are unadjusted. The teacher adds RAM/computation, and no new external or capture-separated validation was obtained. The current paper and prior positive extension remain frozen.']
 (out/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps(gate,indent=2));print(json.dumps(screen,indent=2));print('\n'.join(lines[lines.index('## Matched delayed federated results'):lines.index('## Matched delayed federated results')+11]))
if __name__=='__main__':main()
