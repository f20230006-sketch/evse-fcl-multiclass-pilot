from pathlib import Path
import sys,json,hashlib,itertools,datetime,os
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from evse_ids.validation_extension_2026_11_12 import prepare_track,run_job,digest,ORDERS
from evse_ids.multiclass_pilot import save_json
OUT=ROOT/'outputs/validation_extension_2026_11_12'
CONFIG={'local_epochs':5,'rounds_per_task':5,'batch_size':128,'weight_decay':.0001,'gradient_clip_norm':None,'torch_threads_per_worker':1,'federated_memory_per_client':60,'centralized_memory_total':300,'fisher_max_examples_per_client_task':128}
def job(track,order,env,method,group,settings,seed,cal,number):
 prepared=OUT/track/'prepared'/order/'prepared.pt'
 directory=OUT/track/('calibration' if cal else 'runs')/order/env/(method+'_'+group)/(f'candidate_{number}' if cal else f'seed_{seed}')
 j={'prepared':str(prepared),'directory':str(directory),'config':CONFIG,'order':order,'environment':env,'method':method,'group':group,'settings':settings,'seed':seed,'calibration_only':cal,'prepared_sha256':digest(prepared)}
 j['fingerprint']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest();return j
def execute(jobs,track,phase):
 records=[]
 with ProcessPoolExecutor(max_workers=3) as pool:
  for future in as_completed([pool.submit(run_job,j) for j in jobs]):
   records.append(future.result());save_json(OUT/'progress.json',{'track':track,'phase':phase,'done':len(records),'total':len(jobs),'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
   print(f'{track} {phase} {len(records)}/{len(jobs)}',flush=True)
 return records
def main():
 OUT.mkdir(exist_ok=True,parents=True)
 design=ROOT/'docs/research/Independent_Validation_Design_2026_11_12.md'
 lock={'design_sha256':digest(design),'config':CONFIG,'orders':ORDERS,'model':'64/32 MLP','new_evaluation_seeds':{'source_file':list(range(500,510)),'independent_ocpp':list(range(600,610))},'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 path=OUT/'protocol_before_training.json'
 if path.exists():
  prior=json.loads(path.read_text());assert prior['design_sha256']==lock['design_sha256'] and prior['config']==CONFIG
 else:save_json(path,lock)
 for track in ['source_file','independent_ocpp']:
  requested=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--track=')),None)
  if requested and track!=requested:continue
  prepared=OUT/track/'prepared'
  if (prepared/'ineligible.json').exists():
   print(track,'ineligible under locked data-support checks; no fitting launched',flush=True);continue
  if not (prepared/'audit.json').exists():
   audit=prepare_track(ROOT,track,prepared,CONFIG);print(track,json.dumps(audit),flush=True)
  if '--prepare-only' in sys.argv:continue
  selected_path=OUT/track/'selected_before_evaluation.json'
  if not selected_path.exists():
   jobs=[];selections={};cal_seed=490 if track=='source_file' else 590
   for order,env in itertools.product(ORDERS,['federated','centralized']):
    for method,group in [('balanced','none'),('cbrs','none'),('rbr','declared'),('rbr','icmp'),('rbr','union')]:
     candidates=[{'learning_rate':.003,'replay_fraction':r,**({'rare_quota_fraction':q} if method=='rbr' else {})} for q in ([.1,.2] if method=='rbr' else [0]) for r in [.25,.5]]
     for n,setting in enumerate(candidates):jobs.append(job(track,order,env,method,group,setting,cal_seed,True,n))
   records=execute(jobs,track,'calibration');assert len(records)==96
   save_json(OUT/track/'all_calibration_candidates.json',records)
   for r in records:
    k='|'.join(r[x] for x in ['order','environment','method','group'])
    if k not in selections or r['selection_score']>selections[k]['selection_score']+1e-15:selections[k]=r
   # Tie selection is independent of asynchronous completion order.
   for k in selections:
    candidates=sorted([r for r in records if '|'.join(r[x] for x in ['order','environment','method','group'])==k],key=lambda r:json.dumps(r['settings'],sort_keys=True))
    selections[k]=max(candidates,key=lambda r:r['selection_score'])
   save_json(selected_path,{'calibration_complete_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidates':96,'selected':selections,'evaluation_not_started':True})
  selected=json.loads(selected_path.read_text())['selected'];jobs=[];start=500 if track=='source_file' else 600
  for key,r in selected.items():
   for seed in range(start,start+10):jobs.append(job(track,r['order'],r['environment'],r['method'],r['group'],r['settings'],seed,False,0))
  assert len(jobs)==300
  records=execute(jobs,track,'evaluation');save_json(OUT/track/'completion.json',{'calibration_fits':96,'evaluated_runs':len(records),'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
if __name__=='__main__':main()
