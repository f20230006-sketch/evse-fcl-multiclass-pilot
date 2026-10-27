"""One finite calibration-first exploration, isolated from the frozen study."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import hashlib,json,platform,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import torch
from evse_ids.exploratory_tuning import run_case
from evse_ids.multiclass_pilot import save_json

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def execute(j):
    directory=Path(j['directory']);stamp=directory/'complete.json'
    if stamp.exists():
        old=json.loads(stamp.read_text());assert old['fingerprint']==j['fingerprint'];return {**j,**old['result']}
    data=torch.load(j['prepared'],weights_only=False,map_location='cpu')
    result=run_case(data,j['config'],j['environment'],j['method'],j['settings'],j['seed'],directory,calibration_only=j['calibration_only'])
    save_json(stamp,{'fingerprint':j['fingerprint'],'result':result})
    return {**j,**result}

def pool(jobs,phase,out,workers):
    result=[]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for future in as_completed([executor.submit(execute,j) for j in jobs]):
            result.append(future.result());progress={'phase':phase,'completed':len(result),'total':len(jobs)}
            save_json(out/'progress.json',progress);print(json.dumps(progress),flush=True)
    return result

def main():
    config=json.loads((ROOT/'configs/exploratory_tuning_2026_10_27.json').read_text());out=ROOT/config['output_dir'];out.mkdir(parents=True,exist_ok=True)
    prior=json.loads((ROOT/'outputs/balanced_rare_final/protocol_before_evaluation.json').read_text())
    for rel,digest in prior['source_hashes'].items():assert sha(ROOT/rel)==digest,rel
    inputs=prior['reference_inputs']
    for rel,digest in inputs.items():assert sha(ROOT/rel)==digest,rel
    files=['src/evse_ids/exploratory_tuning.py','scripts/run_exploratory_tuning.py','configs/exploratory_tuning_2026_10_27.json','docs/research/Exploratory_Tuning_Design_2026_10_27.md',*prior['source_hashes']]
    payload={'config':config,'source_hashes':{p:sha(ROOT/p) for p in files},'reference_inputs':inputs,'exploratory':True}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    protocol=out/'protocol_before_evaluation.json'
    if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint
    save_json(protocol,{**payload,'fingerprint':fingerprint,'python':platform.python_version(),'torch':torch.__version__})
    def job(phase,o,e,m,settings,seed,cal,trial):
        directory=out/phase/o/e/m/(f'trial_{trial}' if cal else f'seed_{seed}')
        j={'order':o,'environment':e,'method':m,'settings':settings,'seed':seed,'calibration_only':cal,'trial':trial,'prepared':str(ROOT/config['reference_output']/'splits'/o/'prepared_local_only.pt'),'config':config,'directory':str(directory)}
        j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,'phase':phase,**{k:j[k] for k in ['order','environment','method','settings','seed','trial']}},sort_keys=True).encode()).hexdigest();return j
    jobs=[job('backbone_calibration',o,e,m,{**s,'replay_fraction':.5,'rare_quota_fraction':.1 if 'balanced_rare' in m else .2 if 'protected' in m else 0.},42,True,i) for i,s in enumerate(config['backbone_candidates']) for o in config['orders'] for e in config['environments'] for m in config['methods']]
    screen=pool(jobs,'backbone_calibration',out,config['workers'])
    scores=[float(np.mean([r['selection_score'] for r in screen if r['trial']==i])) for i in range(len(config['backbone_candidates']))]
    chosen=max(range(len(scores)),key=lambda i:(scores[i],-i));backbone=config['backbone_candidates'][chosen]
    save_json(out/'backbone_selection.json',{'test_data_used':False,'scores':scores,'chosen_index':chosen,'settings':backbone,'trials':[{k:r[k] for k in ['order','environment','method','trial','settings','selection_score']} for r in screen]})
    grids={m:[{**backbone,'rare_quota_fraction':q,'replay_fraction':r} for q in (config['rare_fractions'] if 'balanced_rare' in m else [.2] if 'protected' in m else [0.]) for r in config['replay_fractions']] for m in config['methods']}
    jobs=[job('calibration',o,e,m,s,42,True,i) for o in config['orders'] for e in config['environments'] for m in config['methods'] for i,s in enumerate(grids[m])]
    trials=pool(jobs,'replay_calibration',out,config['workers']);selected={};records=[]
    for o in config['orders']:
        selected[o]={}
        for e in config['environments']:
            selected[o][e]={}
            for m in config['methods']:
                candidates=[r for r in trials if r['order']==o and r['environment']==e and r['method']==m]
                best=max(candidates,key=lambda r:(r['selection_score'],-r['trial']));selected[o][e][m]=best['settings']
                records.extend([{**{k:r[k] for k in ['order','environment','method','trial','settings','selection_score']},'selected':r is best} for r in candidates])
    save_json(out/'hyperparameter_trials.json',{'test_data_used':False,'selected':selected,'trials':records,'grids':grids})
    jobs=[job('runs',o,e,m,selected[o][e][m],seed,False,None) for o in config['orders'] for e in config['environments'] for m in config['methods'] for seed in config['seeds']]
    runs=pool(jobs,'evaluation',out,config['workers'])
    save_json(out/'completion.json',{'status':'complete','backbone_calibration_runs':len(screen),'replay_calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint,'exploratory':True})

if __name__=='__main__':main()
