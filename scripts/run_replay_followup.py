"""Frozen-split, calibration-first follow-up; resume requires matching source hashes."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import sys
import platform

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import torch
import pandas as pd
from evse_ids.replay_followup import run_case
from evse_ids.multiclass_pilot import save_json

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def execute(job):
    directory=Path(job['directory']); stamp=directory/'complete.json'
    if stamp.exists():
        old=json.loads(stamp.read_text())
        assert old['fingerprint']==job['fingerprint'], 'Changed source/config: use new output directory'
        return {**job,**old['result'],'resumed':True}
    data=torch.load(job['prepared_path'],weights_only=False,map_location='cpu')
    capacity=int(job['method'].rsplit('_',1)[1])
    config={**job['config'],'federated_memory_per_client':capacity,'centralized_memory_total':capacity*5}
    result=run_case(data,config,job['environment'],job['method'],job['settings'],job['seed'],directory,calibration_only=job['calibration_only'])
    save_json(stamp,{'fingerprint':job['fingerprint'],'result':result})
    return {**job,**result,'resumed':False}

def pool(jobs,config,phase,out):
    results=[]
    with ProcessPoolExecutor(max_workers=config['workers']) as executor:
        futures=[executor.submit(execute,j) for j in jobs]
        for f in as_completed(futures):
            r=f.result();results.append(r)
            progress={'phase':phase,'completed':len(results),'total':len(jobs),'last':{k:r[k] for k in ['order','environment','method','seed']}}
            save_json(out/'progress.json',progress);print(json.dumps(progress),flush=True)
    return results

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',default='configs/replay_followup_essential.json');args=parser.parse_args()
    config=json.loads((ROOT/args.config).read_text());out=ROOT/config['output_dir'];out.mkdir(parents=True,exist_ok=True)
    reference=ROOT/config['reference_output'];prior=json.loads((reference/'protocol_before_evaluation.json').read_text())
    assert json.loads((reference/'verification.json').read_text())['status']=='passed'
    for p,h in prior['source_hashes'].items(): assert digest(ROOT/p)==h,p
    for k in ['orders','seeds','split_seed','sampling_seed','local_epochs','rounds_per_task','batch_size','weight_decay','numeric_z_clip','max_rows_per_attack']:
        assert config[k]==prior['config'][k],k
    paths=['src/evse_ids/replay_followup.py','scripts/run_replay_followup.py',args.config]+list(prior['source_hashes'])
    hashes={p:digest(ROOT/p) for p in paths}
    prepared={order:str(reference/'splits'/order/'prepared_local_only.pt') for order in config['orders']}
    inputs={str(Path(p).relative_to(ROOT)):digest(p) for p in prepared.values()}
    for order in config['orders']:
        inputs[str((reference/'splits'/order/'split_manifest.csv').relative_to(ROOT))]=digest(reference/'splits'/order/'split_manifest.csv')
    payload={'config':config,'source_hashes':hashes,'reference_inputs':inputs,'reference_fingerprint':prior['fingerprint']}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    protocol=out/'protocol_before_evaluation.json'
    if protocol.exists(): assert json.loads(protocol.read_text())['fingerprint']==fingerprint,'Protocol changed'
    save_json(protocol,{**payload,'fingerprint':fingerprint,'versions':{'python':platform.python_version(),'torch':torch.__version__,'pandas':pd.__version__}})
    def job(order,env,method,settings,seed,cal,trial=None):
        directory=out/('calibration' if cal else 'runs')/order/env/method/(f'trial_{trial}' if cal else f'seed_{seed}')
        j={'order':order,'environment':env,'method':method,'settings':settings,'seed':seed,'calibration_only':cal,'prepared_path':prepared[order],'config':config,'directory':str(directory)}
        j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,**{k:j[k] for k in ['order','environment','method','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest()
        return j
    jobs=[job(o,e,m,s,config['calibration_seed'],True,t) for o in config['orders'] for e in config['environments'] for m in config['methods'] for t,s in enumerate(config['grids'][m])]
    trials=pool(jobs,config,'calibration',out);selected={};records=[]
    for o in config['orders']:
        selected[o]={}
        for e in config['environments']:
            selected[o][e]={}
            for m in config['methods']:
                candidates=[r for r in trials if r['order']==o and r['environment']==e and r['method']==m]
                best=max(candidates,key=lambda r:(r['selection_score'],-config['grids'][m].index(r['settings'])))
                selected[o][e][m]=best['settings']
                for r in candidates: records.append({**{k:r[k] for k in ['order','environment','method','settings']},'calibration_score':r['selection_score'],'selected':r is best})
    save_json(out/'hyperparameter_trials.json',{'test_data_used':False,'selected':selected,'trials':records,'selection_basis':'mean checkpoint calibration macro recall, ties first candidate'})
    pd.DataFrame(records).to_csv(out/'hyperparameter_trials.csv',index=False)
    jobs=[job(o,e,m,selected[o][e][m],s,False) for o in config['orders'] for e in config['environments'] for m in config['methods'] for s in config['seeds']]
    runs=pool(jobs,config,'evaluation',out)
    save_json(out/'completion.json',{'status':'complete','calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint})

if __name__=='__main__':main()
