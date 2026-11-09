"""Fixed parameter-matched class-balanced control; no evaluation-driven tuning."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
import torch
from evse_ids.teacher_alignment import run_case
from evse_ids.multiclass_pilot import save_json

def execute(j):
 d=Path(j['directory']);stamp=d/'complete.json'
 if stamp.exists():return
 data=torch.load(j['prepared'],weights_only=False,map_location='cpu');r=run_case(data,j['config'],'federated','cb_global',j['settings'],j['seed'],d,False);save_json(stamp,{'fingerprint':j['fingerprint'],'result':r})

def main():
 source=R/'outputs/teacher_alignment_2026_11_09';c=json.loads((source/'protocol_before_evaluation.json').read_text())['config'];hp=json.loads((source/'hyperparameter_trials.json').read_text());selected=next(r for r in hp['selected']if r['environment']=='federated'and r['alias']=='global');settings={k:v for k,v in selected['settings'].items()if k!='rare_quota_fraction'}
 out=R/'outputs/teacher_global_parameter_control_2026_11_09';out.mkdir(exist_ok=True)
 payload={'scope':'Post-evaluation-added parameter-matched baseline. Values come solely from the corrected RBR pre-evaluation calibration selection, with rare quota removed. No new parameter search. Same split64 and seeds310-319. Exploratory, not confirmation.','settings':settings,'source_selection':selected,'source_selection_sha256':hashlib.sha256((source/'hyperparameter_trials.json').read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();p=out/'protocol_before_evaluation.json'
 if p.exists():assert json.loads(p.read_text())['fingerprint']==fingerprint
 else:save_json(p,{**payload,'fingerprint':fingerprint})
 jobs=[{'config':c,'prepared':str(source/'split_64/prepared_local_only.pt'),'directory':str(out/'runs/federated/cb_global_parameter'/f'seed_{seed}'),'settings':settings,'seed':seed,'fingerprint':fingerprint}for seed in c['seeds']]
 with ProcessPoolExecutor(max_workers=8)as ex:
  for i,f in enumerate(as_completed([ex.submit(execute,j)for j in jobs]),1):f.result();print(json.dumps({'completed':i,'total':len(jobs)}),flush=True)
 save_json(out/'completion.json',{'status':'complete','new_calibration_fits':0,'evaluation_runs':len(jobs),'fingerprint':fingerprint})
if __name__=='__main__':main()
