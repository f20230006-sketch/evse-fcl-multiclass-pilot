from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd,torch
R=Path('D:/EV-charging');sys.path.insert(0,str(R/'src'))
from evse_ids.multiclass_pilot import TrafficMLP,predict
from evse_ids.scan_final import paired_interval,scan_mapping,merge_probabilities
D=R/'outputs/teacher_global_parameter_control_2026_11_09';out=R/'outputs/teacher_alignment_report_2026_11_09';ref=R/'outputs/teacher_alignment_2026_11_09';proto=json.loads((D/'protocol_before_evaluation.json').read_text());assert hashlib.sha256((ref/'hyperparameter_trials.json').read_bytes()).hexdigest()==proto['source_selection_sha256'];expected={k:v for k,v in proto['source_selection']['settings'].items()if k!='rare_quota_fraction'};assert expected==proto['settings']
data=torch.load(ref/'split_64/prepared_local_only.pt',weights_only=False,map_location='cpu');torch.set_num_threads(1);records=[];checkpoints=0;rowscount=0
paths=list((D/'runs/federated/cb_global_parameter').glob('seed_*/results.json'));assert len(paths)==10
for p in paths:
 r=json.loads(p.read_text());assert r['settings']==expected
 for a in json.loads((p.parent/'memory_audit.json').read_text()):assert len(a['memory_rows'])<=60 and(data['roles'][a['memory_rows']]=='fitting').all()
 for x in json.loads((p.parent/'training_log.json').read_text()):
  if len(x['global_old_seen'])>=2:assert x['teacher_old_class_ids']==x['global_old_seen']
 for h in r['history']:
  with np.load(p.parent/f"checkpoint_{h['checkpoint']}_predictions.npz")as z:
   idx=z['sample_index'];y=z['y_true'];prob=z['probability'];assert(data['roles'][idx]=='evaluation').all()and np.array_equal(y,data['y'][idx].numpy())and np.allclose(prob.sum(1),1,atol=1e-6);names,mapping=scan_mapping(data['classes']);q=merge_probabilities(prob,mapping,len(names));slow=y==data['classes'].index('Slowloris_Scan');assert np.isclose((q.argmax(1)[slow]==mapping[y[slow]]).mean(),h['scores']['merged_scans']['summary']['slowloris_recall']);checkpoints+=1;rowscount+=len(idx)
 model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True,map_location='cpu'));assert np.allclose(predict(model,data['x'],idx,r['history'][-1]['seen_classes']),prob,atol=1e-6)
 for space,m in r['summary'].items():records.append({'environment':'federated','alias':'cb_global_parameter','method':'cb_global','seed':r['seed'],'score_space':space,**m})
f=pd.concat([pd.read_csv(out/'all_metrics_with_global_control.csv'),pd.DataFrame(records)],ignore_index=True);f.to_csv(out/'all_metrics_with_all_controls.csv',index=False);M=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall'];summary=f.groupby(['score_space','environment','alias'])[M].agg(['mean','std']);summary.columns=['_'.join(x)for x in summary.columns];summary.reset_index().to_csv(out/'summary_with_all_controls.csv',index=False)
contrasts=[]
for space in ['merged_scans','original_type']:
 sub=f[(f.score_space==space)&(f.environment=='federated')].pivot(index='seed',columns='alias',values=M)
 for m in M:
  delta=(sub[(m,'global')]-sub[(m,'cb_global_parameter')]).sort_index();delta=delta.mask(delta.abs()<1e-12,0);contrasts.append({'score_space':space,'metric':m,'left':'global','right':'cb_global_parameter','scope':'post-evaluation-added fixed parameter control; not retuned','fixed_settings':json.dumps(expected,sort_keys=True),**paired_interval(delta)})
pd.DataFrame(contrasts).to_csv(out/'parameter_matched_intervals.csv',index=False)
(out/'parameter_control_verification.json').write_text(json.dumps({'status':'passed','models':len(paths),'checkpoints':checkpoints,'prediction_rows':rowscount,'parameter_source':'RBR pre-evaluation calibration selection, no new tuning','settings':expected},indent=2))
print(f[(f.environment=='federated')&(f.score_space=='merged_scans')&(f.alias.isin(['global','cb_global','cb_global_parameter','cb_legacy']))].groupby('alias')[M].mean().to_string());print(pd.DataFrame(contrasts).query("score_space=='merged_scans'")[['metric','mean_difference','ci95_low','ci95_high']].to_string(index=False))
