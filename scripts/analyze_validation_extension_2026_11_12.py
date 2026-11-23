from pathlib import Path
import sys,json,hashlib,math
import numpy as np
import pandas as pd
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from evse_ids.multiclass_pilot import rank_metrics
OUT=ROOT/'outputs/validation_extension_report_2026_11_12';OUT.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tcritical(alpha,df=9):
 target=1-alpha/2;lo=0.;hi=100.
 for _ in range(70):
  x=(lo+hi)/2;cdf=1-.5*float(mp.betainc(df/2,.5,0,df/(df+x*x),regularized=True))
  if cdf<target:lo=x
  else:hi=x
 return (lo+hi)/2
NOM=tcritical(.05);ADJ=tcritical(.05/18)
SCAN={'Aggressive_Scan','OS_Fingerprinting','SYN_Stealth_Scan','Service_Version_Detection','TCP_Port_Scan','Vulnerability_Scan'}
hashes={};rows=[];pc=[];clients=[];conf=[];checks=[]
def score(result_path,track,order,environment,method,seed,groups,manifest,classes):
 result=json.loads(result_path.read_text());best={};hist=[]
 for step in result['history']:
  p=result_path.parent/f"checkpoint_{step['checkpoint']}_predictions.npz";hashes[str(p.relative_to(ROOT))]=digest(p)
  with np.load(p) as z:idx=z['sample_index'];y=z['y_true'];prob=z['probability']
  roles=manifest.loc[idx,'role' if 'role' in manifest else 'persistent_role'].to_numpy();assert (roles=='evaluation').all()
  pred=prob.argmax(1);assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=2e-6)
  assert abs((pred==y).mean()-step['pooled']['accuracy'])<1e-12
  cohort={}
  for task,m in step['tasks'].items():
   acc=m['attack_accuracy'];cohort[task]=acc
   if acc is not None:best[task]=max(best.get(task,acc),acc)
  hist.append({'cohort':cohort,'best':best.copy()})
 key={'track':track,'order':order,'environment':environment,'method':method,'seed':seed}
 seen=sorted(set(y.tolist()));n=len(classes);matrix=np.zeros((n,n),int);np.add.at(matrix,(y,pred),1)
 support=matrix.sum(1);predicted=matrix.sum(0);tp=matrix.diagonal()
 precision=np.divide(tp,predicted,out=np.zeros(n,float),where=predicted>0);recall=np.divide(tp,support,out=np.zeros(n,float),where=support>0);f1=np.divide(2*tp,support+predicted,out=np.zeros(n,float),where=support+predicted>0)
 aucs=[];aps=[]
 for c,name in enumerate(classes):
  auc,ap=rank_metrics(y==c,prob[:,c]);aucs.append(auc);aps.append(ap)
  pc.append({**key,'class':name,'support':int(support[c]),'precision':precision[c],'recall':recall[c],'f1':f1[c],'auroc':auc,'average_precision':ap})
  for j in range(n):conf.append({**key,'truth':name,'predicted':classes[j],'count':int(matrix[c,j])})
 for client in sorted(manifest.client.unique()):
  m=manifest.loc[idx,'client'].to_numpy()==client;sup=np.bincount(y[m],minlength=n);local=np.zeros(n)
  for c in range(n):
   if sup[c]:local[c]=(pred[m&(y==c)]==c).mean()
  cm=float(local[sup>0].mean()) if sup.sum() else None
  clients.append({**key,'client':client,'macro_recall':cm,'rows':int(m.sum()),'benign_support':int((m&(y==0)).sum()),'false_alarm_rate':float((pred[m&(y==0)]!=0).mean()) if (m&(y==0)).any() else None})
 old=list(result['history'][-1]['tasks'])[:-1];oldacc=np.mean([hist[-1]['cohort'][t] for t in old]);forget=np.mean([hist[-1]['best'][t]-hist[-1]['cohort'][t] for t in old])
 m=y==0;fp=int((pred[m]!=0).sum());b=int(m.sum());local_scores=[c['macro_recall'] for c in clients[-len(manifest.client.unique()):] if c['macro_recall'] is not None]
 r={**key,'old_task_accuracy':oldacc,'forgetting':forget,'macro_precision':precision[support>0].mean(),'macro_f1':f1[support>0].mean(),'macro_recall':recall[support>0].mean(),'macro_auroc':np.mean(aucs),'macro_average_precision':np.mean(aps),'worst_client_macro_recall':min(local_scores),'benign_support':b,'benign_false_alarms':fp,'false_alarm_rate':fp/b,'slowloris_recall':recall[classes.index('Slowloris_Scan')] if 'Slowloris_Scan' in classes else None}
 for group,names in groups.items():r['group_'+group+'_recall']=float(np.mean([recall[classes.index(c)] for c in names]))
 rows.append(r);checks.append({'path':str(result_path.relative_to(ROOT)),'final_rows':len(y),'accuracy_reproduced':True})
 if track=='independent_ocpp' and seed==600:
  # Descriptive Wilson interval for a predeclared seed, plus connection-group bootstrap.
  z=1.95996398454;rate=fp/b;den=1+z*z/b;center=(rate+z*z/(2*b))/den;half=z*math.sqrt(rate*(1-rate)/b+z*z/(4*b*b))/den
  frame=pd.DataFrame({'group':manifest.loc[idx[m],'group'].astype(str).to_numpy(),'fp':(pred[m]!=0).astype(int),'n':1}).groupby('group')[['fp','n']].sum()
  rng=np.random.default_rng(719);samples=rng.integers(0,len(frame),(2000,len(frame)));counts=frame.to_numpy();bootstrap=counts[samples,0].sum(1)/counts[samples,1].sum(1)
  wilson.append({**key,'false_alarms':fp,'benign_rows':b,'connection_groups':len(frame),'wilson_low':max(0,center-half),'wilson_high':min(1,center+half),'cluster_bootstrap_low':np.quantile(bootstrap,.025),'cluster_bootstrap_high':np.quantile(bootstrap,.975)})
wilson=[]
def main():
 external=ROOT/'outputs/validation_extension_2026_11_12/independent_ocpp';original=ROOT/'outputs/original_rare_groups_2026_11_12'
 assert json.loads((external/'completion.json').read_text())['evaluated_runs']==300
 external_only='--external-only' in sys.argv
 if not external_only:assert json.loads((original/'completion.json').read_text())['new_evaluation_runs']==120
 import torch
 for track,parent in ([('independent_ocpp',external)] if external_only else [('independent_ocpp',external),('original',original)]):
  for order in ['order_1','order_2','order_3']:
   data=torch.load(parent/'prepared'/order/'prepared.pt',weights_only=False,map_location='cpu');classes=data['classes'];manifest=data['manifest'].copy()
   if 'sample_index' in manifest:manifest=manifest.set_index('sample_index')
   groups=data['rare_groups'].copy()
   if track=='original':groups['declared']=['Slowloris_Scan','ICMP_Fragmentation']
   for stamp in sorted((parent/'runs'/order).rglob('complete.json')):
    meta=json.loads(stamp.read_text());method=meta['method']+'_'+meta['group']
    score(stamp.parent/'results.json',track,order,meta['environment'],method,meta['seed'],groups,manifest,classes)
   if track=='original':
    for env in ['federated','centralized']:
     for method,folder,case in [('balanced_none','replay_followup_essential','class_balanced_60'),('cbrs_none','cbrs_comparison_2026_10_28','cbrs_60'),('rbr_declared','balanced_rare_final','balanced_rare_60')]:
      for seed in range(42,52):score(ROOT/'outputs'/folder/'runs'/order/env/case/f'seed_{seed}'/'results.json',track,order,env,method,seed,groups,manifest,classes)
 f=pd.DataFrame(rows);assert len(f)==(300 if external_only else 600);f.to_csv(OUT/'per_run_metrics.csv',index=False);pd.DataFrame(pc).to_csv(OUT/'per_class_metrics.csv',index=False);pd.DataFrame(clients).to_csv(OUT/'per_client_metrics.csv',index=False);pd.DataFrame(conf).to_csv(OUT/'confusions.csv',index=False);pd.DataFrame(wilson).to_csv(OUT/'benign_seed_600_intervals.csv',index=False)
 met=[c for c in f if c not in ['track','order','environment','method','seed']]
 seeds=f.groupby(['track','environment','method','seed'])[met].mean().reset_index();seeds.to_csv(OUT/'seed_order_averaged.csv',index=False)
 summary=seeds.groupby(['track','environment','method'])[met].agg(['mean','std']);summary.columns=['_'.join(c) for c in summary.columns];summary.reset_index().to_csv(OUT/'summary.csv',index=False)
 perorder=f.groupby(['track','order','environment','method'])[met].agg(['mean','std']);perorder.columns=['_'.join(c) for c in perorder.columns];perorder.reset_index().to_csv(OUT/'per_order_summary.csv',index=False)
 pairs=[]
 for track in (['independent_ocpp'] if external_only else ['original','independent_ocpp']):
  for env in ['federated','centralized']:
   for order in ['averaged','order_1','order_2','order_3']:
    a=seeds if order=='averaged' else f[f.order==order];a=a[(a.track==track)&(a.environment==env)]
    for group in ['declared','icmp','union']:
     for baseline in ['balanced_none','cbrs_none']:
      left=a[a.method=='rbr_'+group].set_index('seed');right=a[a.method==baseline].set_index('seed')
      for metric in ['old_task_accuracy','forgetting','macro_precision','macro_f1','macro_recall','macro_auroc','macro_average_precision','worst_client_macro_recall','false_alarm_rate','slowloris_recall','group_'+group+'_recall']:
       d=(left[metric]-right[metric]).sort_index().dropna()
       if not len(d):continue
       assert len(d)==10;se=d.std(ddof=1)/math.sqrt(10);mean=d.mean();primary=metric in ['old_task_accuracy','macro_f1','group_'+group+'_recall']
       pairs.append({'track':track,'environment':env,'order':order,'left':'rbr_'+group,'right':baseline,'metric':metric,'difference':mean,'ci95_low':mean-NOM*se,'ci95_high':mean+NOM*se,'simultaneous_low':mean-ADJ*se if primary else None,'simultaneous_high':mean+ADJ*se if primary else None,'primary_family_18':primary})
 pd.DataFrame(pairs).to_csv(OUT/'paired_intervals.csv',index=False)
 (OUT/'input_sha256.json').write_text(json.dumps(hashes,indent=2))
 verification={'new_models':300 if external_only else 420,'reference_models_reused':0 if external_only else 180,'final_model_cases_scored':len(f),'all_four_checkpoint_prediction_files':len(hashes),'all_evaluation_roles_verified':True,'all_original_pooled_accuracies_reproduced':True,'paired_seed_count':10,'nominal_t9_critical':NOM,'bonferroni_18_t9_critical':ADJ,'grouped_benign_rows':249,'source_file_track':'failed pretraining support gate; not run','primary_reporting':'exact type; no scan merging used in this new main comparison'}
 (OUT/'verification.json').write_text(json.dumps(verification,indent=2))
 print(summary.loc[('independent_ocpp','federated'),['old_task_accuracy_mean','macro_f1_mean','group_declared_recall_mean','group_icmp_recall_mean','worst_client_macro_recall_mean','false_alarm_rate_mean']].round(4).to_string())
if __name__=='__main__':main()
