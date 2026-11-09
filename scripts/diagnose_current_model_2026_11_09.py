from pathlib import Path
import sys,json
import numpy as np,pandas as pd,torch
R=Path('D:/EV-charging');sys.path.insert(0,str(R/'src'))
from evse_ids.multiclass_pilot import TrafficMLP,predict
from evse_ids.scan_final import scan_mapping,merge_probabilities
D=R/'outputs/current_model_diagnostics_2026_11_09';D.mkdir(exist_ok=True)
data=torch.load(R/'outputs/distilled_replay_2026_11_09/split_63/prepared_local_only.pt',weights_only=False,map_location='cpu');torch.set_num_threads(1)
rows=np.flatnonzero(data['roles']=='calibration');y=data['y'][rows].numpy();names,mapping=scan_mapping(data['classes']);records=[];conf=[]
for method in ['fixed_rbr','class_balanced_kd','fixed_rbr_kd']:
 for path in sorted((R/'outputs/distilled_replay_2026_11_09/runs/delayed/federated'/method).glob('seed_*/final_model.pt')):
  model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(path,weights_only=True,map_location='cpu'));p=predict(model,data['x'],rows,list(range(len(data['classes']))));q=merge_probabilities(p,mapping,len(names));truth=mapping[y];pred=q.argmax(1)
  for cl in ['pooled',*data['assigned']]:
   cm=np.ones(len(rows),bool) if cl=='pooled' else data['clients'][rows]==cl
   for cid,name in enumerate(names):
    mask=cm&(truth==cid)
    if mask.any():records.append({'method':method,'seed':int(path.parent.name.split('_')[1]),'client':cl,'class':name,'support':int(mask.sum()),'recall':float((pred[mask]==cid).mean())})
  for i,true in enumerate(names):
   for j,out in enumerate(names):
    n=int(((truth==i)&(pred==j)).sum())
    if n:conf.append({'method':method,'seed':int(path.parent.name.split('_')[1]),'true':true,'predicted':out,'count':n})
f=pd.DataFrame(records);f.to_csv(D/'final_calibration_per_class_client.csv',index=False);pd.DataFrame(conf).to_csv(D/'calibration_confusions.csv',index=False)
g=f.groupby(['method','client','class']).recall.agg(['mean','std']).reset_index();g.to_csv(D/'calibration_recall_summary.csv',index=False)
print('LOWEST POOLED CAL RECALL, RBR+KD');print(g[(g.method=='fixed_rbr_kd')&(g.client=='pooled')].sort_values('mean').to_string(index=False))
print('\nCLIENT MACRO, CALIBRATION');print(f.groupby(['method','client']).recall.mean().unstack(0).round(3).to_string())
# Diagnose teacher mask coverage from the saved training log, without changing any run.
p=R/'outputs/distilled_replay_2026_11_09/runs/delayed/federated/fixed_rbr_kd/seed_200'
r=json.loads((p/'results.json').read_text());logs=json.loads((p/'training_log.json').read_text());coverage=[]
for h in r['history']:
 prior=[0] if h['checkpoint']==1 else r['history'][h['checkpoint']-2]['seen_classes']
 for cl in h['active_clients']:
  x=next(x for x in logs if x['phase']==h['checkpoint']and x['client']==cl)
  coverage.append({'phase':h['checkpoint'],'client':cl,'globally_available_previous_classes':len(prior),'distilled_previous_classes':x.get('teacher_old_classes',0),'teacher_active':bool(x.get('teacher_parameter_count',0))})
pd.DataFrame(coverage).to_csv(D/'teacher_coverage.csv',index=False);print('\nTEACHER COVERAGE');print(pd.DataFrame(coverage).to_string(index=False))
(D/'SCOPE.md').write_text('# Diagnostic scope\n\nFinal-model confusion and client diagnostics use calibration roles only. Historical evaluation numbers are descriptive; no current evaluation partition will be reused to choose another method. Existing protocols, models and paper outputs remain unchanged. Teacher coverage is read from saved execution logs; it is a design limitation under delayed first participation, not evidence of a fabricated prior gain.\n')
