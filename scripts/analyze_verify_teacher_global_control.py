from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd,torch
R=Path('D:/EV-charging');sys.path.insert(0,str(R/'src'))
from evse_ids.scan_final import paired_interval,scan_mapping,merge_probabilities
from evse_ids.multiclass_pilot import TrafficMLP,predict
run=R/'outputs/teacher_global_control_2026_11_09';out=R/'outputs/teacher_alignment_report_2026_11_09';proto=json.loads((run/'protocol_before_evaluation.json').read_text());c=proto['config'];data=torch.load(run/'split_64/prepared_local_only.pt',weights_only=False,map_location='cpu');ref=torch.load(R/'outputs/teacher_alignment_2026_11_09/split_64/prepared_local_only.pt',weights_only=False,map_location='cpu');assert torch.equal(data['x'],ref['x'])and torch.equal(data['y'],ref['y'])and np.array_equal(data['roles'],ref['roles']);torch.set_num_threads(1)
for p,h in {**proto['source_hashes'],**proto['inherited_hashes']}.items():
 with (R/p).open('rb')as f:assert hashlib.file_digest(f,'sha256').hexdigest()==h,p
cal=list((run/'calibration').glob('*/*/trial_*/results.json'));paths=list((run/'runs').glob('*/*/seed_*/results.json'));assert len(cal)==24 and len(paths)==20;assert max(p.stat().st_mtime_ns for p in cal)<min(p.stat().st_mtime_ns for p in paths)
records=[];counts={'models':0,'checkpoints':0,'prediction_rows':0};M=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
for p in paths:
 r=json.loads(p.read_text());logs=json.loads((p.parent/'training_log.json').read_text())
 for l in logs:
  if len(l['global_old_seen'])>=2:assert l['teacher_old_class_ids']==l['global_old_seen']
 previous={}
 for a in json.loads((p.parent/'memory_audit.json').read_text()):
  mem=np.array(a['memory_rows'],int);cur=np.array(a['current_rows'],int);assert len(mem)<= (60 if r['environment']=='federated'else 300)and len(set(mem))==len(mem)and(data['roles'][mem]=='fitting').all()and set(mem)<=set(previous.get(a['client'],[]))|set(cur);previous[a['client']]=mem.tolist()
 for ck in r['history']:
  with np.load(p.parent/f"checkpoint_{ck['checkpoint']}_predictions.npz")as z:
   idx=z['sample_index'];y=z['y_true'];prob=z['probability'];assert(data['roles'][idx]=='evaluation').all()and np.array_equal(y,data['y'][idx].numpy())and np.allclose(prob.sum(1),1,atol=1e-6);names,mapping=scan_mapping(data['classes']);q=merge_probabilities(prob,mapping,len(names));slow=y==data['classes'].index('Slowloris_Scan');assert np.isclose((q.argmax(1)[slow]==mapping[y[slow]]).mean(),ck['scores']['merged_scans']['summary']['slowloris_recall']);counts['checkpoints']+=1;counts['prediction_rows']+=len(idx)
 model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True,map_location='cpu'));assert np.allclose(predict(model,data['x'],idx,r['history'][-1]['seen_classes']),prob,atol=1e-6)
 for space,m in r['summary'].items():records.append({'environment':r['environment'],'alias':'cb_global','method':'cb_global','seed':r['seed'],'score_space':space,**m})
 counts['models']+=1
f=pd.concat([pd.read_csv(out/'all_per_run_metrics.csv'),pd.DataFrame(records)],ignore_index=True);f.to_csv(out/'all_metrics_with_global_control.csv',index=False)
summary=f.groupby(['score_space','environment','alias'])[M].agg(['mean','std']);summary.columns=['_'.join(x)for x in summary.columns];summary.reset_index().to_csv(out/'summary_with_global_control.csv',index=False)
pairs=[]
for space in ['merged_scans','original_type']:
 for env in c['environments']:
  sub=f[(f.score_space==space)&(f.environment==env)].pivot(index='seed',columns='alias',values=M)
  for m in M:
   delta=(sub[(m,'global')]-sub[(m,'cb_global')]).sort_index();delta=delta.mask(delta.abs()<1e-12,0);ci=paired_interval(delta);pairs.append({'score_space':space,'environment':env,'left':'global','right':'cb_global','metric':m,'scope':'post-evaluation matched baseline addition; exploratory',**ci})
pd.DataFrame(pairs).to_csv(out/'matched_global_control_intervals.csv',index=False)
(out/'global_control_verification.json').write_text(json.dumps({'status':'passed','calibration_fits':24,'all_calibration_before_evaluation':True,'identical_input_tensors_and_roles':True,**counts},indent=2))
print('FEDERATED MATCHED GLOBAL CONTROL:');print(f[(f.score_space=='merged_scans')&(f.environment=='federated')&(f.alias.isin(['global','cb_global']))].groupby('alias')[M].mean().to_string());print(pd.DataFrame(pairs).query("score_space=='merged_scans' and environment=='federated'")[['metric','mean_difference','ci95_low','ci95_high']].to_string(index=False));print('Verified',counts)
