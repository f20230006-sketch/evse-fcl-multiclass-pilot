from pathlib import Path
import json,sys
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from evse_ids.scan_final import paired_interval
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']

def main():
 run=R/'outputs/distilled_replay_2026_11_09';out=R/'outputs/distilled_replay_report_2026_11_09';out.mkdir(exist_ok=True)
 assert json.loads((run/'completion.json').read_text())['evaluation_runs']==100
 c=json.loads((run/'protocol_before_evaluation.json').read_text())['config'];records=[];clients=[];cost=[];history=[]
 for p in sorted((run/'runs').glob('*/*/*/seed_*/results.json')):
  r=json.loads(p.read_text());key={k:r[k]for k in ['schedule','environment','method','seed']}
  for space,m in r['summary'].items():
   records.append({**key,'score_space':space,**m})
   for cl,m in r['history'][-1]['scores'][space]['per_client'].items():clients.append({**key,'score_space':space,'client':cl,**m})
   history.extend({**key,'score_space':space,'phase':h['checkpoint'],**h['scores'][space]['summary']}for h in r['history'])
  logs=json.loads((p.parent/'training_log.json').read_text());cost.append({**key,'elapsed_seconds':r['elapsed_seconds'],'local_updates':len(logs),'optimizer_steps':sum(x['steps']for x in logs),'maximum_teacher_parameters':max(x.get('teacher_parameter_count',0)for x in logs),'mean_kd_loss':float(np.mean([x['mean_kd_loss']for x in logs if 'mean_kd_loss'in x]))if any('mean_kd_loss'in x for x in logs)else 0.})
 f=pd.DataFrame(records);assert len(f)==200
 for name,df in [('all_per_run_metrics',f),('per_client_metrics',pd.DataFrame(clients)),('training_costs',pd.DataFrame(cost)),('checkpoint_metrics',pd.DataFrame(history))]:df.to_csv(out/(name+'.csv'),index=False)
 summary=f.groupby(['score_space','environment','method'])[METRICS].agg(['mean','std']);summary.columns=['_'.join(x)for x in summary.columns];summary.reset_index().to_csv(out/'summary.csv',index=False)
 pairs=[]
 comparisons=[('fixed_rbr_kd','fixed_rbr'),('fixed_rbr_kd','class_balanced_kd'),('fixed_rbr_kd','class_balanced'),('fixed_rbr_kd','cbrs'),('class_balanced_kd','class_balanced')]
 for space in ['merged_scans','original_type']:
  for env in c['environments']:
   subset=f[(f.score_space==space)&(f.environment==env)]
   for left,right in comparisons:
    a=subset[subset.method==left].set_index('seed');b=subset[subset.method==right].set_index('seed');assert set(a.index)==set(b.index)==set(c['seeds'])
    for m in METRICS:
     delta=(a[m]-b[m]).sort_index();delta=delta.mask(delta.abs()<1e-12,0);ci=paired_interval(delta);better=ci['ci95_high']<0 if m=='forgetting'else ci['ci95_low']>0;worse=ci['ci95_low']>0 if m=='forgetting'else ci['ci95_high']<0
     pairs.append({'score_space':space,'environment':env,'left':left,'right':right,'metric':m,'outcome':'better'if better else'worse'if worse else'not significant',**ci})
 pc=pd.DataFrame(pairs);pc.to_csv(out/'paired_intervals.csv',index=False)
 interactions=[]
 for space in ['merged_scans','original_type']:
  for m in METRICS:
   pivot=f[f.score_space==space].pivot(index='seed',columns=['environment','method'],values=m)
   delta=(pivot[('federated','fixed_rbr_kd')]-pivot[('federated','fixed_rbr')])-(pivot[('centralized','fixed_rbr_kd')]-pivot[('centralized','fixed_rbr')]);delta=delta.mask(delta.abs()<1e-12,0)
   interactions.append({'score_space':space,'contrast':'federated minus centralized distillation benefit','metric':m,**paired_interval(delta)})
 pd.DataFrame(interactions).to_csv(out/'interactions.csv',index=False)
 primary=pc[(pc.score_space=='merged_scans')&(pc.environment=='federated')&(pc.left=='fixed_rbr_kd')&(pc.right=='fixed_rbr')].set_index('metric')
 screen={'slowloris_positive_lower_bound':bool(primary.loc['slowloris_recall','ci95_low']>0),'old_accuracy_lower_above_minus_one_point':bool(primary.loc['old_task_accuracy','ci95_low']>-.01),'worst_client_lower_above_minus_one_point':bool(primary.loc['worst_client_macro_recall','ci95_low']>-.01)};screen['all_prespecified_conditions_met']=all(screen.values());screen['scope']='Second exploratory mechanism, split63 of reused corpus, one rare-first delayed order; unadjusted intervals and extra teacher RAM. Not external validation or novel distillation.'
 (out/'prespecified_screen.json').write_text(json.dumps(screen,indent=2))
 lines=['# Teacher-distilled replay results','',screen['scope'],'','## Delayed federated merged-Scan results','','| Method | Old accuracy | Forgetting | Slowloris recall | Worst client |','|---|---:|---:|---:|---:|']
 for method in c['methods']:
  d=f[(f.score_space=='merged_scans')&(f.environment=='federated')&(f.method==method)];lines.append('| '+method+' | '+' | '.join(f'{100*d[m].mean():.2f} ± {100*d[m].std(ddof=1):.2f}'for m in METRICS)+' |')
 lines+=['','Percentages, mean ± sample SD over ten training seeds.','','## Distilled RBR minus fixed RBR','']
 for _,r in pc[(pc.score_space=='merged_scans')&(pc.left=='fixed_rbr_kd')&(pc.right=='fixed_rbr')].iterrows():lines.append(f"- {r.environment}, {r.metric}: {100*r.mean_difference:+.2f} points [{100*r.ci95_low:.2f}, {100*r.ci95_high:.2f}]; {r.outcome}.")
 lines+=['','## Prespecified screen','',json.dumps(screen,indent=2),'','## Interpretation','', 'The teacher mechanism changes the training objective and adds model state; gains cannot be credited solely to memory allocation. Distilled class-balanced replay is included to assess that distinction. The current paper stays frozen. Complete original-type, centralized, per-client and interaction results are included. Favorable exploration requires independent confirmation before replacing accepted claims; unfavorable results are retained without further evaluation-driven tuning.']
 (out/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps(screen,indent=2));print('\n'.join(lines[6:13]))
if __name__=='__main__':main()
