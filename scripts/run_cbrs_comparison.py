"""Twelve calibration fits before sixty evaluated CBRS runs; immutable resume."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import torch
from evse_ids.cbrs_experiment import run_case
from evse_ids.multiclass_pilot import save_json

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def execute(j):
    d=Path(j['directory']);stamp=d/'complete.json'
    if stamp.exists():
        old=json.loads(stamp.read_text());assert old['fingerprint']==j['fingerprint'];return {**j,**old['result']}
    data=torch.load(j['prepared'],weights_only=False,map_location='cpu')
    result=run_case(data,j['config'],j['environment'],'cbrs_60',j['settings'],j['seed'],d,calibration_only=j['calibration_only'])
    save_json(stamp,{'fingerprint':j['fingerprint'],'result':result});return {**j,**result}
def pool(jobs,c,phase,out):
    results=[]
    with ProcessPoolExecutor(max_workers=c['workers']) as ex:
        for f in as_completed([ex.submit(execute,j) for j in jobs]):
            results.append(f.result());p={'phase':phase,'completed':len(results),'total':len(jobs)};save_json(out/'progress.json',p);print(json.dumps(p),flush=True)
    return results
def main():
    cp=ROOT/'configs/cbrs_comparison_2026_10_28.json';c=json.loads(cp.read_text());out=ROOT/c['output_dir'];out.mkdir(exist_ok=True,parents=True)
    prior=json.loads((ROOT/'outputs/balanced_rare_final/protocol_before_evaluation.json').read_text())
    for p,h in prior['source_hashes'].items():assert sha(ROOT/p)==h,p
    prepared={o:ROOT/'outputs/multiclass_full_comparison/splits'/o/'prepared_local_only.pt' for o in c['orders']}
    sources=[cp,Path(__file__),ROOT/'src/evse_ids/cbrs.py',ROOT/'src/evse_ids/cbrs_experiment.py',ROOT/'docs/research/CBRS_Frozen_Design_2026_10_28.md']
    payload={'config':c,'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},'inherited_hashes':prior['source_hashes'],'input_hashes':{str(p.relative_to(ROOT)):sha(p) for p in prepared.values()}}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();protocol=out/'protocol_before_evaluation.json'
    if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint
    else:save_json(protocol,{**payload,'fingerprint':fingerprint})
    def job(o,e,settings,seed,cal,t=0):
        d=out/('calibration' if cal else 'runs')/o/e/'cbrs_60'/(f'trial_{t}' if cal else f'seed_{seed}');d.mkdir(exist_ok=True,parents=True)
        j={'order':o,'environment':e,'settings':settings,'seed':seed,'calibration_only':cal,'prepared':str(prepared[o]),'directory':str(d),'config':c}
        j['fingerprint']=hashlib.sha256(json.dumps({'protocol':fingerprint,**{k:j[k] for k in ['order','environment','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest();return j
    trials=pool([job(o,e,s,42,True,i) for o in c['orders'] for e in c['environments'] for i,s in enumerate(c['grid'])],c,'calibration',out)
    selected=[]
    for o in c['orders']:
        for e in c['environments']:
            candidates=[r for r in trials if r['order']==o and r['environment']==e];best=max(candidates,key=lambda r:(r['selection_score'],-c['grid'].index(r['settings'])))
            selected.append({'order':o,'environment':e,'settings':best['settings']})
    save_json(out/'hyperparameter_trials.json',{'test_data_used':False,'selected':selected,'trials':[{k:r[k] for k in ['order','environment','settings','selection_score']} for r in trials]})
    runs=pool([job(r['order'],r['environment'],r['settings'],seed,False) for r in selected for seed in c['seeds']],c,'evaluation',out)
    save_json(out/'completion.json',{'status':'complete','calibration_runs':len(trials),'evaluation_runs':len(runs),'fingerprint':fingerprint})
if __name__=='__main__':main()
