"""Operational parallelism only: process far-future cases with identical fingerprints."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from run_targeted_validation import execute
def main():
    out=ROOT/'outputs/targeted_validation_2026_10_27';protocol=json.loads((out/'protocol_before_evaluation.json').read_text());c=protocol['config']
    selection=json.loads((out/'hyperparameter_trials.json').read_text())
    tail='--split44-tail' in sys.argv
    middle='--split44-middle' in sys.argv
    phase='middle' if middle else 'tail' if tail else 'main'
    progress=json.loads((out/'progress.json').read_text());assert progress['phase']=='evaluation' and progress['completed']<(150 if tail else 180)
    jobs=[]
    # Primary queue runs splits 43/44 first. Finish disjoint, later queue cases here.
    for split in ([44] if tail or middle else [42,45]):
        for r in selection['selected']:
            if r['split_seed']!=split:continue
            if tail and not (r['order']=='order_3' or (r['order']=='order_2' and r['environment']=='centralized')):continue
            if middle and not ((r['order']=='order_1' and r['environment']=='centralized') or (r['order']=='order_2' and r['environment']=='federated')):continue
            for seed in c['seeds']:
                o=r['order'];e=r['environment'];m=r['method'];settings=r['settings']
                path=out/'splits'/f'split_{split}'/o/'prepared_local_only.pt' if split!=42 else ROOT/'outputs/multiclass_full_comparison/splits'/o/'prepared_local_only.pt'
                d=out/'runs'/f'split_{split}'/o/e/m/f'seed_{seed}'
                j={'split_seed':split,'order':o,'environment':e,'method':m,'settings':settings,'seed':seed,'calibration_only':False,'prepared':str(path),'config':c,'directory':str(d)}
                j['fingerprint']=hashlib.sha256(json.dumps({'protocol':protocol['fingerprint'],**{k:j[k] for k in ['split_seed','order','environment','method','settings','seed','calibration_only']}},sort_keys=True).encode()).hexdigest();jobs.append(j)
    assert len(jobs)==(40 if middle else 60 if tail else 180)
    (out/(f'execution_resources_{phase}.json' if phase!='main' else 'execution_resources.json')).write_text(json.dumps({'primary_workers':3,'supplementary_workers':6 if tail or middle else 8,'supplementary_cases':len(jobs),'splits':[44] if tail or middle else [42,45],'scientific_settings_changed':False,'reason':'Use available independent CPU processes for far-future primary-queue cases; same source/config, seeds and per-job fingerprint. Primary skips completed stamps. All 132 calibration fits finished before this pool starts.'},indent=2))
    with ProcessPoolExecutor(max_workers=6 if tail or middle else 8) as ex:
        for i,f in enumerate(as_completed([ex.submit(execute,j) for j in jobs]),1):
            f.result();p={'completed':i,'total':len(jobs)};(out/(f'supplementary_{phase}_progress.json' if phase!='main' else 'supplementary_progress.json')).write_text(json.dumps(p));print(json.dumps(p),flush=True)
if __name__=='__main__':main()
