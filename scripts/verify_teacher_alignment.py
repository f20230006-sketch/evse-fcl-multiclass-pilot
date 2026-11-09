from pathlib import Path
import hashlib,json,sys
import numpy as np,torch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from evse_ids.multiclass_pilot import TrafficMLP,predict
from evse_ids.scan_final import scan_mapping,merge_probabilities

def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
 run=R/'outputs/teacher_alignment_2026_11_09';out=R/'outputs/teacher_alignment_report_2026_11_09';out.mkdir(exist_ok=True);proto=json.loads((run/'protocol_before_evaluation.json').read_text());c=proto['config'];end=json.loads((run/'completion.json').read_text());gate=json.loads((run/'calibration_gate.json').read_text())
 for p,h in {**proto['source_hashes'],**proto['inherited_hashes']}.items():assert sha(R/p)==h,p
 lock=R/'outputs/current_model_diagnostics_2026_11_09/PRIOR_RESULTS_LOCK.json';assert sha(lock)==proto['prior_results_lock_sha256']
 for x in json.loads(lock.read_text())['files']:assert sha(R/x['path'])==x['sha256'],x['path']
 data=torch.load(run/'split_64/prepared_local_only.pt',weights_only=False,map_location='cpu');assert sha(run/'split_64/prepared_local_only.pt')==proto['prepared_sha256'];roles=data['roles'];y=data['y'].numpy()
 cal=list((run/'calibration').glob('*/*/trial_*/results.json'));assert len(cal)==192
 for p in cal:
  r=json.loads(p.read_text());assert r['calibration_only'] and not list(p.parent.glob('*predictions.npz'))and not(p.parent/'final_model.pt').exists();assert len(r['history'])==6
 hp=json.loads((run/'hyperparameter_trials.json').read_text());assert hp['actual_calibration_fits']==192 and not hp['evaluation_used']
 for s in hp['selected']:
  trials=[r for r in hp['trials']if r['environment']==s['environment']and r['method']==s['method']and r['settings']==s['settings']];assert {r['seed']for r in trials}==set(c['calibration_seeds']);assert np.isclose(s['selection_score'],np.mean([t['selection_scores'][s['criterion']]for t in trials]))
 paths=list((run/'runs').glob('*/*/seed_*/results.json'))
 if not gate['proceed_to_evaluation']:assert len(paths)==0 and end['evaluation_runs']==0
 else:assert len(paths)==120 and max(p.stat().st_mtime_ns for p in cal)<min(p.stat().st_mtime_ns for p in paths)
 counts={'evaluation_models':0,'checkpoints':0,'prediction_rows':0,'population_updates':0,'corrected_late_first_tasks':0};torch.set_num_threads(1)
 for p in paths:
  r=json.loads(p.read_text());logs=json.loads((p.parent/'training_log.json').read_text());audit=json.loads((p.parent/'memory_audit.json').read_text());seen_clients=set();capacity=60 if r['environment']=='federated'else 300
  for x in logs:
   if r['mode']in ['global','family']and len(x['global_old_seen'])>=2:assert x['teacher_old_class_ids']==x['global_old_seen']
   if x['round']==1:
    if x['client']not in seen_clients and len(x['global_old_seen'])>=2 and r['mode']in ['global','family']:counts['corrected_late_first_tasks']+=1;assert x['teacher_parameter_count']>0
    seen_clients.add(x['client'])
  previous={}
  for a in audit:
   mem=np.array(a['memory_rows'],int);cur=np.array(a['current_rows'],int);cl=a['client'];assert len(mem)<=capacity and len(mem)==len(set(mem))and(roles[mem]=='fitting').all()and(roles[cur]=='fitting').all();assert set(mem)<=set(previous.get(cl,[]))|set(cur);previous[cl]=mem.tolist();counts['population_updates']+=1
  for h in r['history']:
   with np.load(p.parent/f"checkpoint_{h['checkpoint']}_predictions.npz")as z:
    idx=z['sample_index'];truth=z['y_true'];prob=z['probability'];assert(roles[idx]=='evaluation').all()and np.array_equal(truth,y[idx]);assert np.isfinite(prob).all()and np.allclose(prob.sum(1),1,atol=1e-6)
    names,mapping=scan_mapping(data['classes']);q=merge_probabilities(prob,mapping,len(names));merged_truth=mapping[truth];pred=q.argmax(1);acc=[]
    for task in data['tasks'][:-1]:
     mask=data['manifest'].task.to_numpy()[idx]==task['name']
     if mask.any():acc.append(float((merged_truth[mask]==pred[mask]).mean()))
    assert np.isclose(np.mean(acc),h['scores']['merged_scans']['summary']['old_task_accuracy'])
    slow=truth==data['classes'].index('Slowloris_Scan');assert np.isclose((merged_truth[slow]==pred[slow]).mean(),h['scores']['merged_scans']['summary']['slowloris_recall']);counts['checkpoints']+=1;counts['prediction_rows']+=len(idx)
  model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True,map_location='cpu'));assert np.allclose(predict(model,data['x'],idx,r['history'][-1]['seen_classes']),prob,atol=1e-6);counts['evaluation_models']+=1
 if paths:
  for seed in c['seeds']:
   a=run/'runs/centralized/legacy_merged'/f'seed_{seed}'/'final_model.pt';b=run/'runs/centralized/global'/f'seed_{seed}'/'final_model.pt'
   aa=torch.load(a,weights_only=True,map_location='cpu');bb=torch.load(b,weights_only=True,map_location='cpu');assert all(torch.equal(aa[k],bb[k])for k in aa)
  counts['centralized_no_gap_model_pairs_identical']=len(c['seeds'])
 result={'status':'passed','calibration_fits':192,'calibration_training_seeds':3,'all_calibration_before_evaluation':True,'prior_locked_files_unchanged':len(json.loads(lock.read_text())['files']),**counts,'calibration_gate':gate,'scope':'Same-corpus repartition; exploratory and unadjusted. Correct coverage does not by itself establish higher accuracy.'};(out/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
