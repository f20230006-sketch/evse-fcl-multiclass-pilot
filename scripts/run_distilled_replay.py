"""All48 calibration fits precede160 evaluations; separate frozen protocol and resume."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
import numpy as np
import pandas as pd
import torch
import evse_ids.multiclass_pilot as pilot
from evse_ids.distilled_replay import run_case

def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def execute(j):
 p=Path(j['directory'])/'complete.json'
 if p.exists():
  old=json.loads(p.read_text());assert old['fingerprint']==j['fingerprint'];return {**j,**old['result']}
 d=torch.load(j['prepared'],weights_only=False,map_location='cpu')
 res=run_case(d,j['config'],j['environment'],j['schedule'],j['method'],j['settings'],j['seed'],j['directory'],j['calibration_only'])
 pilot.save_json(p,{'fingerprint':j['fingerprint'],'result':res});return {**j,**res}

def pool(jobs,c,out,phase):
 rows=[]
 with ProcessPoolExecutor(max_workers=c['workers'])as ex:
  for f in as_completed([ex.submit(execute,j)for j in jobs]):
   rows.append(f.result());p={'phase':phase,'completed':len(rows),'total':len(jobs)};pilot.save_json(out/'progress.json',p);print(json.dumps(p),flush=True)
 return rows

def main():
 cp=R/'configs/distilled_replay_2026_11_09.json';c=json.loads(cp.read_text());out=R/c['output_dir'];out.mkdir(exist_ok=True,parents=True)
 freeze=R/'outputs/frozen_paper_2026_11_09/MANIFEST.json';assert freeze.exists()
 prior=json.loads(freeze.read_text());inherited={v['path']:v['sha256']for v in prior['files'] if v['path'].startswith('src/evse_ids/')}
 for p,h in inherited.items():assert sha(R/p)==h,p
 split=out/'split_63';prepared=split/'prepared_local_only.pt'
 if not prepared.exists():
  frame=pd.read_pickle(R/'outputs/multiclass_full_comparison/sampled_fixed.pkl');original=pilot.reproducible_non_iid_client_partitions
  pilot.reproducible_non_iid_client_partitions=lambda labels,seed:original(labels,seed=42)
  try:data=pilot.prepare(frame,c,c['split_seed'],split)
  finally:pilot.reproducible_non_iid_client_partitions=original
  old=pd.read_csv(R/'outputs/multiclass_full_comparison/splits/order_3/split_manifest.csv')
  assert np.array_equal(data['clients'],old.client.to_numpy()) and not np.array_equal(data['roles'],old.persistent_role.to_numpy())
  torch.save(data,prepared)
 sources=[cp,Path(__file__),R/'src/evse_ids/asynchronous_replay.py',R/'src/evse_ids/distilled_replay.py',R/'docs/research/Distilled_Replay_Design_2026_11_09.md']
 payload={'config':c,'source_hashes':{str(p.relative_to(R)):sha(p)for p in sources},'inherited_hashes':inherited,'prepared_sha256':sha(prepared),'paper_freeze_manifest_sha256':sha(freeze)}
 fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();protocol=out/'protocol_before_evaluation.json'
 if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint
 else:pilot.save_json(protocol,{**payload,'fingerprint':fingerprint})
 def job(e,s,m,settings,seed,cal,t=0):
  directory=out/('calibration' if cal else 'runs')/s/e/m/(f'trial_{t}'if cal else f'seed_{seed}')
  j={'environment':e,'schedule':s,'method':m,'settings':settings,'seed':seed,'calibration_only':cal,'directory':str(directory),'prepared':str(prepared),'config':c}
  j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,**{k:j[k]for k in ['environment','schedule','method','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest();return j
 trials=pool([job(e,s,m,g,c['calibration_seed'],True,i)for e in c['environments']for s in c['schedules']for m in c['methods']for i,g in enumerate(c['grids'][m])],c,out,'calibration')
 selected=[]
 for e in c['environments']:
  for s in c['schedules']:
   for m in c['methods']:
    candidates=[r for r in trials if(r['environment'],r['schedule'],r['method'])==(e,s,m)]
    best=max(candidates,key=lambda r:(r['selection_score'],-c['grids'][m].index(r['settings'])))
    selected.append({k:best[k]for k in ['environment','schedule','method','settings','selection_score']})
 pilot.save_json(out/'hyperparameter_trials.json',{'evaluation_used':False,'selected':selected,'trials':[{k:r[k]for k in ['environment','schedule','method','settings','selection_score','elapsed_seconds']}for r in trials]})
 runs=pool([job(r['environment'],r['schedule'],r['method'],r['settings'],seed,False)for r in selected for seed in c['seeds']],c,out,'evaluation')
 pilot.save_json(out/'completion.json',{'status':'complete','calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint})
if __name__=='__main__':main()
