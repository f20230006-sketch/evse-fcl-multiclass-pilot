"""Role, schedule, weight, numerical-score and frozen-paper verification."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import torch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from evse_ids.asynchronous_replay import adaptive_quota
from evse_ids.multiclass_pilot import TrafficMLP,predict
from evse_ids.scan_final import scan_mapping,merge_probabilities

def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
 run=R/'outputs/distilled_replay_2026_11_09';out=R/'outputs/distilled_replay_report_2026_11_09';out.mkdir(exist_ok=True)
 protocol=json.loads((run/'protocol_before_evaluation.json').read_text());c=protocol['config'];assert json.loads((run/'completion.json').read_text())['evaluation_runs']==100
 for p,h in {**protocol['source_hashes'],**protocol['inherited_hashes']}.items():assert sha(R/p)==h,p
 data=torch.load(run/'split_63/prepared_local_only.pt',weights_only=False,map_location='cpu');assert sha(run/'split_63/prepared_local_only.pt')==protocol['prepared_sha256']
 labels=data['y'].numpy();roles=data['roles'];cal=list((run/'calibration').glob('*/*/*/trial_*/results.json'));paths=list((run/'runs').glob('*/*/*/seed_*/results.json'));assert len(cal)==40 and len(paths)==100
 assert max(p.stat().st_mtime_ns for p in cal)<=min(p.stat().st_mtime_ns for p in paths)
 for p in cal:
  r=json.loads(p.read_text());assert r['calibration_only'] and not list(p.parent.glob('*predictions.npz'))
 counters={'evaluated_models':0,'checkpoints':0,'prediction_rows':0,'population_updates':0,'monitor_rows_checked':0}
 torch.set_num_threads(1)
 for p in paths:
  r=json.loads(p.read_text());audit=json.loads((p.parent/'memory_audit.json').read_text());prior={};best={};exposures={}
  for a in audit:
   cl=a['client'];mem=np.array(a['memory_rows'],int);cur=np.array(a['current_rows'],int);mon=np.array(a['monitor_rows'],int);capacity=60 if r['environment']=='federated'else 300
   assert len(mem)==len(set(mem)) and len(mem)<=capacity and (roles[mem]=='fitting').all() and (roles[cur]=='fitting').all()
   assert set(mem)<=set(prior.get(cl,[]))|set(cur)
   for name,i in zip(data['classes'],range(len(data['classes']))):assert a['class_counts'][name]==int((labels[mem]==i).sum())
   if len(mon):
    assert (roles[mon]=='calibration').all()
    if cl!='pooled':assert (data['clients'][mon]==cl).all()
    assert set(data['labels'][mon])<={'Slowloris_Scan','ICMP_Fragmentation'}
   if r['method']=='adaptive_rbr':
    b=best.setdefault(cl,{});q=adaptive_quota(a['monitor_recalls'],b,r['settings']['maximum_rare_fraction']);assert abs(q-a['quota_fraction'])<1e-12
    for name,v in a['monitor_recalls'].items():b[name]=max(b.get(name,v),v)
   prior[cl]=mem.tolist();exposures[cl]=exposures.get(cl,0)+1;counters['population_updates']+=1;counters['monitor_rows_checked']+=len(mon)
  if r['environment']=='federated':assert set(exposures.values())=={4}
  for ck in r['history']:
   with np.load(p.parent/f"checkpoint_{ck['checkpoint']}_predictions.npz")as z:
    idx=z['sample_index'];y=z['y_true'];prob=z['probability'];assert len(set(idx))==len(idx) and (roles[idx]=='evaluation').all() and np.array_equal(y,labels[idx]);assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=1e-6)
    names,mapping=scan_mapping(data['classes']);merged=merge_probabilities(prob,mapping,len(names));truth=mapping[y];pred=merged.argmax(1)
    acc=[]
    for task in data['tasks'][:-1]:
     mask=data['manifest'].task.to_numpy()[idx]==task['name']
     if mask.any():acc.append(float((truth[mask]==pred[mask]).mean()))
    assert np.isclose(np.mean(acc),ck['scores']['merged_scans']['summary']['old_task_accuracy'])
    slow=y==data['classes'].index('Slowloris_Scan');assert np.isclose((truth[slow]==pred[slow]).mean(),ck['scores']['merged_scans']['summary']['slowloris_recall'])
    counters['checkpoints']+=1;counters['prediction_rows']+=len(idx)
  model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True,map_location='cpu'));actual=predict(model,data['x'],idx,r['history'][-1]['seen_classes']);assert np.allclose(actual,prob,atol=1e-6)
  counters['evaluated_models']+=1
 # Verify that the teacher was used with its declared old-class state after the first phase.
 for p in paths:
  r=json.loads(p.read_text());logs=json.loads((p.parent/'training_log.json').read_text())
  if r['method'].endswith('_kd'):
   assert any(x.get('teacher_parameter_count',0)>0 for x in logs)
   assert all(x.get('teacher_old_classes',0)<=15 for x in logs)
   assert all(x.get('mean_kd_loss',0)>=-1e-5 for x in logs)
 # The original paper's complete source/output state is checked, excluding new files added later.
 freeze=json.loads((R/'outputs/frozen_paper_2026_11_09/MANIFEST.json').read_text());unchanged=0
 for item in freeze['files']:
  assert sha(R/item['path'])==item['sha256'],item['path'];unchanged+=1
 result={'status':'passed',**counters,'calibration_fits':40,'all_calibration_before_evaluation':True,'all_frozen_files_unchanged':unchanged,'scope':'Prospective partition of reused data; not independent external validation.'}
 (out/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
