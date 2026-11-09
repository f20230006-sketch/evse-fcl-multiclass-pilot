"""Calibration-only observer; verify identical trajectory after probing aggregation."""
from pathlib import Path
import sys,json
import numpy as np,pandas as pd,torch
R=Path('D:/EV-charging');sys.path.insert(0,str(R/'src'))
import evse_ids.distilled_replay as kd
import evse_ids.asynchronous_replay as base
from evse_ids.multiclass_pilot import predict

def main():
 data=torch.load(R/'outputs/distilled_replay_2026_11_09/split_63/prepared_local_only.pt',weights_only=False,map_location='cpu');rows=np.flatnonzero((data['roles']=='calibration')&(data['labels']=='Slowloris_Scan'));cid=data['classes'].index('Slowloris_Scan');assert len(rows)>0
 p=R/'outputs/distilled_replay_2026_11_09/calibration/delayed/federated/fixed_rbr_kd/trial_5/results.json';r=json.loads(p.read_text());c=json.loads((R/'configs/distilled_replay_2026_11_09.json').read_text());dest=R/'outputs/current_model_diagnostics_2026_11_09/aggregation_probe';record=[];context={};oldmake=kd.make_trainer;oldavg=base.fedavg
 def factory():
  fn=oldmake()
  def train(*args,**kwargs):
   value=fn(*args,**kwargs);context['seen']=args[4];return value
  return train
 def avg(model,updates):
  seen=context['seen'];before=predict(model,data['x'],rows,seen);parts=[predict(m,data['x'],rows,seen)for m,n in updates];w=np.array([n for m,n in updates],float);w/=w.sum();ensemble=sum(a*b for a,b in zip(parts,w));localrec=[float((q.argmax(1)==cid).mean())for q in parts];oldavg(model,updates);after=predict(model,data['x'],rows,seen)
  record.append({'phase':len(record)//5+1,'round':len(record)%5+1,'global_before_recall':float((before.argmax(1)==cid).mean()),'weighted_local_recall':float(np.dot(w,localrec)),'ensemble_recall':float((ensemble.argmax(1)==cid).mean()),'fedavg_recall':float((after.argmax(1)==cid).mean()),'clients':len(updates)})
 try:
  kd.make_trainer=factory;base.fedavg=avg;kd.run_case(data,c,'federated','delayed','fixed_rbr_kd',r['settings'],200,dest,calibration_only=True)
 finally:kd.make_trainer=oldmake;base.fedavg=oldavg
 result=json.loads((dest/'results.json').read_text());a=np.array([h['calibration_macro_recall']for h in r['history']]);b=np.array([h['calibration_macro_recall']for h in result['history']]);assert np.array_equal(a,b)
 f=pd.DataFrame(record);f['fedavg_minus_weighted_local']=f.fedavg_recall-f.weighted_local_recall;f.to_csv(dest.parent/'aggregation_calibration_probe.csv',index=False)
 print(f.sort_values('fedavg_minus_weighted_local').head(6).to_string(index=False));print('Trajectory unchanged; calibration rows only:',len(rows))
 (dest.parent/'aggregation_probe_verification.json').write_text(json.dumps({'status':'passed','calibration_only':True,'calibration_rows':len(rows),'rounds_observed':len(record),'original_trajectory_identical':True,'evaluation_rows_used':0},indent=2))
if __name__=='__main__':main()
