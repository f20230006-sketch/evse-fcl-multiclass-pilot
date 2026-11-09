from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
import numpy as np,pandas as pd,torch
import evse_ids.multiclass_pilot as pilot
from evse_ids.teacher_alignment import run_case

def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()

def execute(j):
 stamp=Path(j['directory'])/'complete.json'
 if stamp.exists():
  old=json.loads(stamp.read_text());assert old['fingerprint']==j['fingerprint'];return {**j,**old['result']}
 data=torch.load(j['prepared'],weights_only=False,map_location='cpu');result=run_case(data,j['config'],j['environment'],j['method'],j['settings'],j['seed'],j['directory'],j['calibration_only'])
 pilot.save_json(stamp,{'fingerprint':j['fingerprint'],'result':result});return {**j,**result}

def pool(jobs,c,out,phase):
 records=[]
 with ProcessPoolExecutor(max_workers=c['workers'])as ex:
  for f in as_completed([ex.submit(execute,j)for j in jobs]):
   records.append(f.result());v={'phase':phase,'completed':len(records),'total':len(jobs)};pilot.save_json(out/'progress.json',v);print(json.dumps(v),flush=True)
 return records

def main():
 cp=R/'configs/teacher_alignment_2026_11_09.json';c=json.loads(cp.read_text());out=R/c['output_dir'];out.mkdir(exist_ok=True,parents=True)
 lock=R/'outputs/current_model_diagnostics_2026_11_09/PRIOR_RESULTS_LOCK.json'
 for x in json.loads(lock.read_text())['files']:assert sha(R/x['path'])==x['sha256'],x['path']
 split=out/'split_64';prepared=split/'prepared_local_only.pt'
 if not prepared.exists():
  frame=pd.read_pickle(R/'outputs/multiclass_full_comparison/sampled_fixed.pkl');original=pilot.reproducible_non_iid_client_partitions;pilot.reproducible_non_iid_client_partitions=lambda labels,seed:original(labels,seed=42)
  try:data=pilot.prepare(frame,c,c['split_seed'],split)
  finally:pilot.reproducible_non_iid_client_partitions=original
  reference=pd.read_csv(R/'outputs/multiclass_full_comparison/splits/order_3/split_manifest.csv');assert np.array_equal(data['clients'],reference.client.to_numpy())and not np.array_equal(data['roles'],reference.persistent_role.to_numpy());torch.save(data,prepared)
 sources=[cp,Path(__file__),R/'src/evse_ids/teacher_alignment.py',R/'docs/research/Teacher_Alignment_Design_2026_11_09.md']
 inherited=json.loads((R/'outputs/distilled_replay_2026_11_09/protocol_before_evaluation.json').read_text())
 hashes={**inherited['source_hashes'],**inherited['inherited_hashes']}
 for p,h in hashes.items():assert sha(R/p)==h,p
 payload={'config':c,'source_hashes':{str(p.relative_to(R)):sha(p)for p in sources},'inherited_hashes':hashes,'prepared_sha256':sha(prepared),'prior_results_lock_sha256':sha(lock)}
 fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();protocol=out/'protocol_before_evaluation.json'
 if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint
 else:pilot.save_json(protocol,{**payload,'fingerprint':fingerprint})
 def job(e,m,g,seed,cal,trial=0,alias=None):
  directory=out/('calibration'if cal else'runs')/e/(m if cal else alias)/(f'trial_{trial}_seed_{seed}'if cal else f'seed_{seed}')
  j={'environment':e,'method':m,'alias':alias,'settings':g,'seed':seed,'calibration_only':cal,'directory':str(directory),'prepared':str(prepared),'config':c};j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,**{k:j[k]for k in ['environment','method','alias','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest();return j
 trials=pool([job(e,m,g,seed,True,i)for e in c['environments']for m,grid in c['grids'].items()for i,g in enumerate(grid)for seed in c['calibration_seeds']],c,out,'calibration')
 selections=[];aggregates=[]
 for e in c['environments']:
  for alias,definition in c['aliases'].items():
   m=definition['population'];criterion=definition['criterion'];candidates=[]
   for i,g in enumerate(c['grids'][m]):
    ts=[r for r in trials if r['environment']==e and r['method']==m and r['settings']==g];assert {t['seed']for t in ts}==set(c['calibration_seeds'])
    row={'environment':e,'alias':alias,'method':m,'settings':g,'criterion':criterion,'selection_score':float(np.mean([t['selection_scores'][criterion]for t in ts])),'trial_index':i,'training_seeds':c['calibration_seeds']};candidates.append(row);aggregates.append(row)
   selections.append(max(candidates,key=lambda r:(r['selection_score'],-r['trial_index'])))
 pilot.save_json(out/'hyperparameter_trials.json',{'evaluation_used':False,'actual_calibration_fits':len(trials),'selected':selections,'candidate_aggregates':aggregates,'trials':[{k:r[k]for k in ['environment','method','settings','seed','selection_scores','elapsed_seconds']}for r in trials]})
 f={s['alias']:s['selection_score']for s in selections if s['environment']=='federated'};gate={'baseline_legacy_merged':f['legacy_merged'],'global_gain':f['global']-f['legacy_merged'],'family_gain':f['family']-f['legacy_merged'],'required_margin':c['gate_margin']};gate['proceed_to_evaluation']=bool(max(gate['global_gain'],gate['family_gain'])>=c['gate_margin']);pilot.save_json(out/'calibration_gate.json',gate);print('CALIBRATION GATE',json.dumps(gate),flush=True)
 if not gate['proceed_to_evaluation']:
  pilot.save_json(out/'completion.json',{'status':'calibration_gate_failed','calibration_runs':len(trials),'evaluation_runs':0,'fingerprint':fingerprint});return
 runs=pool([job(r['environment'],r['method'],r['settings'],seed,False,alias=r['alias'])for r in selections for seed in c['seeds']],c,out,'evaluation')
 pilot.save_json(out/'completion.json',{'status':'complete','calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint})
if __name__=='__main__':main()
