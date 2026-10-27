"""Verify exploratory fits, data boundaries, memory allocation and selection."""
from pathlib import Path
import argparse,hashlib,json,sys,zipfile
import numpy as np
import pandas as pd
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.exploratory_tuning import TunedMLP
OUT=ROOT/'outputs/exploratory_tuning_2026_10_27'

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def balanced_counts(candidates,selected,labels):
    available={c:int((labels[candidates]==c).sum()) for c in sorted(set(labels[candidates]))};target={c:0 for c in available};remaining=len(selected)
    while remaining:
        for c in available:
            if target[c]<available[c] and remaining:target[c]+=1;remaining-=1
    assert target=={c:int((labels[selected]==c).sum()) for c in available}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--allow-partial',action='store_true');args=parser.parse_args()
    protocol=json.loads((OUT/'protocol_before_evaluation.json').read_text());config=protocol['config']
    if not args.allow_partial:
        completion=json.loads((OUT/'completion.json').read_text());assert completion['evaluation_runs']==180
    for key in ['source_hashes','reference_inputs']:
        for p,digest in protocol[key].items():assert sha(ROOT/p)==digest,p
    manuscript=ROOT/'outputs/IEEE_Networking_Letters_Draft_Source_2026_10_26.zip'
    manuscript_unchanged=None
    if manuscript.exists():
        with zipfile.ZipFile(manuscript) as z:
            records=json.loads(z.read('manifest.json'))
            expected=next(x['sha256'] for x in records if x['path']=='main.pdf')
            assert sha(ROOT/'outputs/IEEE_Networking_Letters_Draft_2026_10_26.pdf')==expected
            manuscript_unchanged=True
    selection=json.loads((OUT/'hyperparameter_trials.json').read_text());backbone=json.loads((OUT/'backbone_selection.json').read_text())
    selection_time=(OUT/'hyperparameter_trials.json').stat().st_mtime_ns
    screen=[];trials=[]
    for phase in ['backbone_calibration','calibration']:
        paths=list((OUT/phase).glob('*/*/*/trial_*/results.json'));assert len(paths)==(108 if phase=='backbone_calibration' else 72)
        for p in paths:
            r=json.loads(p.read_text());assert r['calibration_only'];assert not list(p.parent.glob('*predictions.npz'))
            assert p.stat().st_mtime_ns<=selection_time
            score=r['history'][-1]['calibration_primary'];assert np.isclose(r['selection_score'],np.mean([score['old_task_accuracy'],score['slowloris_recall'],score['worst_client_macro_recall']]))
            (screen if phase=='backbone_calibration' else trials).append((p,r))
    scores=[np.mean([r['selection_score'] for p,r in screen if p.parent.name==f'trial_{i}']) for i in range(6)]
    chosen=max(range(6),key=lambda i:(scores[i],-i));assert chosen==backbone['chosen_index'] and np.allclose(scores,backbone['scores'])
    assert backbone['settings']==config['backbone_candidates'][chosen]
    for order in config['orders']:
        for env in config['environments']:
            for method in config['methods']:
                records=[(p,r) for p,r in trials if p.parents[3].name==order and r['environment']==env and r['method']==method]
                p,best=max(records,key=lambda x:(x[1]['selection_score'],-int(x[0].parent.name.split('_')[1])))
                assert selection['selected'][order][env][method]==best['settings']
    # Reference backbone must reproduce the unchanged original calibration run.
    a=json.loads((OUT/'backbone_calibration/order_1/federated/tuned_balanced_rare_60/trial_0/results.json').read_text())
    b=json.loads((ROOT/'outputs/balanced_rare_final/calibration/order_1/federated/balanced_rare_60/trial_1/results.json').read_text())
    assert all(x['calibration']==y['calibration'] for x,y in zip(a['history'],b['history']))
    torch.set_num_threads(1);runs=0;rows_checked=0;checkpoints=0
    for order,sequence in config['orders'].items():
        split=ROOT/config['reference_output']/'splits'/order;manifest=pd.read_csv(split/'split_manifest.csv')
        data=torch.load(split/'prepared_local_only.pt',weights_only=False,map_location='cpu')
        labels=manifest.label.to_numpy();roles=manifest.persistent_role.to_numpy();classes=manifest.class_id.to_numpy();clients=manifest.client.to_numpy();tasks=manifest.task.to_numpy()
        for p in (OUT/'runs'/order).glob('*/*/seed_*/results.json'):
            if not (p.parent/'complete.json').exists():continue
            r=json.loads(p.read_text());settings=r['settings'];assert settings==selection['selected'][order][r['environment']][r['method']]
            for h in r['history']:
                path=p.parent/f"checkpoint_{h['checkpoint']}_predictions.npz";assert path.stat().st_mtime_ns>=selection_time
                with np.load(path) as z:idx=z['sample_index'];y=z['y_true'];pred=z['y_pred'];prob=z['probability']
                assert (roles[idx]=='evaluation').all() and np.array_equal(y,classes[idx]);assert len(idx)==len(set(idx))
                assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=1e-6)
                assert np.array_equal(pred,prob.argmax(1));rows_checked+=len(idx);checkpoints+=1
            model=TunedMLP(data['x'].shape[1],len(data['classes']),settings['hidden_sizes'],settings['dropout']);model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True));model.eval()
            with torch.no_grad():actual=np.concatenate([torch.softmax(model(data['x'][idx[s:s+4096]]),1).numpy() for s in range(0,len(idx),4096)])
            assert np.array_equal(actual.argmax(1),pred) and np.allclose(actual,prob,atol=1e-6)
            previous={};capacity=60*(1 if r['environment']=='federated' else 5)
            for entry in json.loads((p.parent/'memory_audit.json').read_text()):
                client=entry['client'];rows=np.asarray(entry['memory_rows'],int)
                current=np.flatnonzero((roles=='fitting')&np.isin(tasks,[sequence[entry['stage']-1],'benign_reference_all_tasks'])&((clients==client) if r['environment']=='federated' else True))
                pool=np.unique(np.concatenate([previous.get(client,np.array([],int)),current]))
                assert len(rows)==min(capacity,len(pool)) and len(set(rows))==len(rows) and np.isin(rows,pool).all()
                assert (roles[rows]=='fitting').all()
                if 'balanced_rare' in r['method']:
                    reserved=np.asarray(entry['reserved_rows'],int);balanced=np.asarray(entry['balanced_rows'],int)
                    rare=pool[np.isin(labels[pool],['Slowloris_Scan','ICMP_Fragmentation'])]
                    assert len(reserved)==min(int(np.floor(capacity*settings['rare_quota_fraction'])),len(rare))
                    assert set(rows)==set(reserved)|set(balanced) and not set(reserved)&set(balanced)
                    assert np.isin(reserved,rare).all();balanced_counts(rare,reserved,labels);balanced_counts(np.setdiff1d(pool,reserved),balanced,labels)
                elif 'class_balanced' in r['method']:balanced_counts(pool,rows,labels)
                else:
                    for group in [['Benign'],['Slowloris_Scan','ICMP_Fragmentation']]:
                        assert np.isin(labels[rows],group).sum()>=min(int(np.floor(capacity*.2)),np.isin(labels[pool],group).sum())
                previous[client]=rows
            runs+=1
    if not args.allow_partial:assert runs==180 and checkpoints==720
    result={'status':'partial_checks_passed' if args.allow_partial else 'passed','exploratory':True,'calibration_fits':180,'evaluation_runs':runs,'saved_models_checked':runs,'checkpoints_checked':checkpoints,'prediction_rows_checked':rows_checked,'source_and_input_hashes_match':True,'sent_manuscript_unchanged':manuscript_unchanged,'all_calibration_before_evaluation':True,'calibration_only_selection':True,'capacities_roles_and_allocations':True,'reference_calibration_reproduced_exactly':True,'dropout_inference_mode_verified':True}
    (OUT/('verification_partial.json' if args.allow_partial else 'verification.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
