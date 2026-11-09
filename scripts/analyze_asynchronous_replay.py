"""Report every frozen candidate outcome; never select from evaluation results."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from evse_ids.scan_final import paired_interval
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']

def main():
 run=R/'outputs/asynchronous_replay_2026_11_09';out=R/'outputs/asynchronous_replay_report_2026_11_09';out.mkdir(exist_ok=True)
 completion=json.loads((run/'completion.json').read_text());assert completion['evaluation_runs']==160
 c=json.loads((run/'protocol_before_evaluation.json').read_text())['config'];records=[];clients=[];cost=[];trajectories=[];quotas=[]
 for p in sorted((run/'runs').glob('*/*/*/seed_*/results.json')):
  r=json.loads(p.read_text());key={k:r[k]for k in ['schedule','environment','method','seed']}
  for space,m in r['summary'].items():
   records.append({**key,'score_space':space,**m})
   for cl,local in r['history'][-1]['scores'][space]['per_client'].items():clients.append({**key,'score_space':space,'client':cl,**local})
   for h in r['history']:trajectories.append({**key,'score_space':space,'phase':h['checkpoint'],**h['scores'][space]['summary']})
  logs=json.loads((p.parent/'training_log.json').read_text());audit=json.loads((p.parent/'memory_audit.json').read_text())
  cost.append({**key,'elapsed_seconds':r['elapsed_seconds'],'local_updates':len(logs),'optimizer_steps':sum(x['steps']for x in logs),'active_server_rounds':len(set((x['phase'],x['round'])for x in logs)),
   'fitting_row_round_exposures':sum(x['current_fitting_rows']for x in logs),'memory_row_round_exposures':sum(x['replay_rows']for x in logs),'monitor_row_evaluations':sum(len(a['monitor_rows'])for a in audit)})
  quotas.extend({**key,'phase':a['phase'],'client':a['client'],'quota_fraction':a['quota_fraction'],'rare_memory_rows':sum(a['class_counts'][n]for n in ['Slowloris_Scan','ICMP_Fragmentation'])}for a in audit)
 f=pd.DataFrame(records);assert len(f)==320
 for name,df in [('all_per_run_metrics',f),('per_client_metrics',pd.DataFrame(clients)),('training_costs',pd.DataFrame(cost)),('checkpoint_metrics',pd.DataFrame(trajectories)),('quota_trajectories',pd.DataFrame(quotas))]:df.to_csv(out/(name+'.csv'),index=False)
 summary=f.groupby(['score_space','schedule','environment','method'])[METRICS].agg(['mean','std']);summary.columns=['_'.join(x)for x in summary.columns];summary.reset_index().to_csv(out/'summary.csv',index=False)
 pairs=[]
 for space in ['merged_scans','original_type']:
  for schedule in c['schedules']:
   for env in c['environments']:
    d=f[(f.score_space==space)&(f.schedule==schedule)&(f.environment==env)]
    a=d[d.method=='adaptive_rbr'].set_index('seed')
    for baseline in ['fixed_rbr','class_balanced','cbrs']:
     b=d[d.method==baseline].set_index('seed');assert set(a.index)==set(b.index)==set(c['seeds'])
     for metric in METRICS:
      delta=(a[metric]-b[metric]).sort_index();delta=delta.mask(delta.abs()<1e-12,0);ci=paired_interval(delta)
      better=ci['ci95_high']<0 if metric=='forgetting'else ci['ci95_low']>0;worse=ci['ci95_low']>0 if metric=='forgetting'else ci['ci95_high']<0
      pairs.append({'score_space':space,'schedule':schedule,'environment':env,'baseline':baseline,'metric':metric,'outcome':'better'if better else'worse'if worse else'not significant',**ci})
 pc=pd.DataFrame(pairs);pc.to_csv(out/'paired_intervals.csv',index=False)
 interactions=[]
 for space in ['merged_scans','original_type']:
  for metric in METRICS:
   p=f[f.score_space==space].pivot(index='seed',columns=['schedule','environment','method'],values=metric)
   delta={(s,e):p[(s,e,'adaptive_rbr')]-p[(s,e,'fixed_rbr')]for s in c['schedules']for e in c['environments']}
   for e in c['environments']:
    d=delta[('delayed',e)]-delta[('synchronized',e)];d=d.mask(d.abs()<1e-12,0);interactions.append({'score_space':space,'contrast':'delayed minus synchronized benefit','setting':e,'metric':metric,**paired_interval(d)})
   for s in c['schedules']:
    d=delta[(s,'federated')]-delta[(s,'centralized')];d=d.mask(d.abs()<1e-12,0);interactions.append({'score_space':space,'contrast':'federated minus centralized benefit','setting':s,'metric':metric,**paired_interval(d)})
 pd.DataFrame(interactions).to_csv(out/'interactions.csv',index=False)
 primary=pc[(pc.score_space=='merged_scans')&(pc.schedule=='delayed')&(pc.environment=='federated')&(pc.baseline=='fixed_rbr')].set_index('metric')
 screen={'slowloris_positive_lower_bound':bool(primary.loc['slowloris_recall','ci95_low']>0),'old_accuracy_lower_above_minus_one_point':bool(primary.loc['old_task_accuracy','ci95_low']>-.01),'worst_client_lower_above_minus_one_point':bool(primary.loc['worst_client_macro_recall','ci95_low']>-.01)};screen['all_prespecified_conditions_met']=all(screen.values());screen['scope']='Exploratory screen on reused-corpus split62, one rare-first order; unadjusted intervals. Not external validation.'
 (out/'prespecified_screen.json').write_text(json.dumps(screen,indent=2))
 lines=['# Asynchronous adaptive replay results','', 'The current paper and baseline evidence remain frozen. This is a separate exploratory study: one rare-first order, a prospective row partition of the reused corpus (seed62), ten training seeds, two timing schedules and matched-capacity federated/centralized controls. No independent external dataset was available.','', '## Main delayed federated results','', '| Method | Old accuracy | Forgetting | Slowloris recall | Worst client |','|---|---:|---:|---:|---:|']
 for method in c['methods']:
  d=f[(f.score_space=='merged_scans')&(f.schedule=='delayed')&(f.environment=='federated')&(f.method==method)]
  lines.append('| '+method+' | '+' | '.join(f'{100*d[m].mean():.2f} ± {100*d[m].std(ddof=1):.2f}'for m in METRICS)+' |')
 lines+=['','Values are percentages, mean ± sample SD across ten training seeds.','', '## Adaptive minus fixed RBR','']
 for _,r in pc[(pc.score_space=='merged_scans')&(pc.baseline=='fixed_rbr')].iterrows():lines.append(f"- {r['schedule']}, {r['environment']}, {r['metric']}: {100*r.mean_difference:+.2f} points [{100*r.ci95_low:.2f}, {100*r.ci95_high:.2f}]; {r.outcome}.")
 lines+=['','## Prespecified outcome','',json.dumps(screen,indent=2),'','## Interpretation boundaries','', 'The controller uses local labeled calibration monitoring; it is not label-free adaptation. The rare-monitor support threshold means it predominantly monitors Slowloris. Local current-task exposures are matched, while delayed aggregation stages, replay exposures and optimizer resets differ; see training_costs.csv. All baselines, exact-type sensitivity, per-client metrics and interaction intervals are retained. A nonsignificant interaction does not establish a federation-specific advantage.','', 'Evaluation results must not be used to redesign this controller. A favorable screen alone does not justify replacing the frozen paper; external or genuinely independent confirmation and a novelty review would be needed. An unfavorable screen remains a valid finding.']
 (out/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
 print(json.dumps(screen,indent=2));print('\n'.join(lines[6:12]))
if __name__=='__main__':main()
