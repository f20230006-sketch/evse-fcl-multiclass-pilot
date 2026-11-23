"""Finite targeted additions, all calibration before evaluation; immutable resume."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
import torch
import evse_ids.multiclass_pilot as pilot
from evse_ids.targeted_validation import run_case
from evse_ids.multiclass_pilot import save_json

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def execute(j):
    d=Path(j['directory']);stamp=d/'complete.json'
    if stamp.exists():
        old=json.loads(stamp.read_text());assert old['fingerprint']==j['fingerprint'];return {**j,**old['result']}
    data=torch.load(j['prepared'],weights_only=False,map_location='cpu')
    result=run_case(data,j['config'],j['environment'],j['method'],j['settings'],j['seed'],d,calibration_only=j['calibration_only'])
    save_json(stamp,{'fingerprint':j['fingerprint'],'result':result});return {**j,**result}
def pool(jobs,phase,out,workers):
    results=[]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(execute,j) for j in jobs]):
            results.append(f.result());p={'phase':phase,'completed':len(results),'total':len(jobs)}
            save_json(out/'progress.json',p);print(json.dumps(p),flush=True)
    return results
def main():
    cp=ROOT/'configs/targeted_validation_2026_10_27.json';c=json.loads(cp.read_text());out=ROOT/c['output_dir'];out.mkdir(parents=True,exist_ok=True)
    old=json.loads((ROOT/'outputs/balanced_rare_final/protocol_before_evaluation.json').read_text())
    for p,h in old['source_hashes'].items():assert sha(ROOT/p)==h,p
    sources=[cp,Path(__file__),ROOT/'src/evse_ids/targeted_validation.py',ROOT/'docs/research/Targeted_Validation_Design_2026_10_27.md']
    payload={'config':c,'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},'inherited_hashes':old['source_hashes'],'sample_hash':sha(ROOT/'outputs/multiclass_full_comparison/sampled_fixed.pkl')}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();protocol=out/'protocol_before_evaluation.json'
    if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint
    save_json(protocol,{**payload,'fingerprint':fingerprint})
    frame=pd.read_pickle(ROOT/'outputs/multiclass_full_comparison/sampled_fixed.pkl')
    original_partition=pilot.reproducible_non_iid_client_partitions
    pilot.reproducible_non_iid_client_partitions=lambda labels,seed: original_partition(labels,seed=c['allocation_seed'])
    prepared={}
    for split in c['additional_split_seeds']:
        for order,sequence in c['orders'].items():
            d=out/'splits'/f'split_{split}'/order;path=d/'prepared_local_only.pt'
            if not path.exists():
                data=pilot.prepare(frame,{**c,'attack_order':sequence},split,d)
                reference=pd.read_csv(ROOT/'outputs/multiclass_full_comparison/splits'/order/'split_manifest.csv')
                assert np.array_equal(data['manifest'].client.to_numpy(),reference.client.to_numpy())
                assert not np.array_equal(data['roles'],reference.persistent_role.to_numpy())
                torch.save(data,path)
            prepared[(split,order)]=path
    cases=[(s,o,e,m,c['grids'][m]) for s in c['additional_split_seeds'] for o in c['orders'] for e in c['environments'] for m in c['methods']]
    cases += [(42,o,e,'rare_random_60',c['ablation_grid']) for o in c['orders'] for e in c['environments']]
    def job(split,o,e,m,settings,seed,cal,trial=0):
        d=out/('calibration' if cal else 'runs')/f'split_{split}'/o/e/m/(f'trial_{trial}' if cal else f'seed_{seed}')
        d.mkdir(parents=True,exist_ok=True)
        path=prepared[(split,o)] if split!=42 else ROOT/'outputs/multiclass_full_comparison/splits'/o/'prepared_local_only.pt'
        j={'split_seed':split,'order':o,'environment':e,'method':m,'settings':settings,'seed':seed,'calibration_only':cal,'prepared':str(path),'config':c,'directory':str(d)}
        j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,**{k:j[k] for k in ['split_seed','order','environment','method','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest();return j
    jobs=[job(s,o,e,m,settings,42,True,t) for s,o,e,m,grid in cases for t,settings in enumerate(grid)]
    trials=pool(jobs,'calibration',out,c['workers']);selected=[]
    for s,o,e,m,grid in cases:
        candidates=[r for r in trials if (r['split_seed'],r['order'],r['environment'],r['method'])==(s,o,e,m)]
        best=max(candidates,key=lambda r:(r['selection_score'],-grid.index(r['settings'])))
        selected.append({'split_seed':s,'order':o,'environment':e,'method':m,'settings':best['settings']})
    save_json(out/'hyperparameter_trials.json',{'test_data_used':False,'selected':selected,'trials':[{k:r[k] for k in ['split_seed','order','environment','method','settings','selection_score']} for r in trials]})
    jobs=[job(r['split_seed'],r['order'],r['environment'],r['method'],r['settings'],seed,False) for r in selected for seed in c['seeds']]
    runs=pool(jobs,'evaluation',out,c['workers'])
    save_json(out/'completion.json',{'status':'complete','calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint})
if __name__=='__main__':main()
