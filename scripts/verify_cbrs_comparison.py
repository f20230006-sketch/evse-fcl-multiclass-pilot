"""Audit every model, stream, population state, merged score and paired interval."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
import torch
from evse_ids.cbrs import CBRS
from evse_ids.multiclass_pilot import TrafficMLP
from evse_ids.scan_final import SCAN_TYPES
RUN=ROOT/'outputs/cbrs_comparison_2026_10_28';OUT=ROOT/'outputs/cbrs_report_2026_10_28'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    protocol=json.loads((RUN/'protocol_before_evaluation.json').read_text());c=protocol['config']
    assert json.loads((RUN/'completion.json').read_text())['evaluation_runs']==60
    for section in ['source_hashes','inherited_hashes','input_hashes']:
        for rel,h in protocol[section].items():assert sha(ROOT/rel)==h,rel
    chosen=json.loads((RUN/'hyperparameter_trials.json').read_text());selection_time=(RUN/'hyperparameter_trials.json').stat().st_mtime_ns
    trials=list((RUN/'calibration').glob('*/*/*/trial_*/results.json'));assert len(trials)==12
    for p in trials:
        r=json.loads(p.read_text());assert r['calibration_only'] and not list(p.parent.glob('*predictions.npz'));assert p.stat().st_mtime_ns<=selection_time
        assert np.isclose(r['selection_score'],np.mean([h['calibration']['macro_recall'] for h in r['history']]))
    for selection in chosen['selected']:
        records=[r for r in chosen['trials'] if all(r[k]==selection[k] for k in ['order','environment'])];best=max(records,key=lambda r:(r['selection_score'],-c['grid'].index(r['settings'])));assert best['settings']==selection['settings']
        d=RUN/'calibration'/selection['order']/selection['environment']/'cbrs_60'
        assert (d/'trial_0/memory_audit.json').read_bytes()==(d/'trial_1/memory_audit.json').read_bytes()
    # Before any replay exists, both implementations must produce the exact frozen checkpoint.
    a=json.loads((RUN/'calibration/order_1/federated/cbrs_60/trial_0/results.json').read_text())
    b=json.loads((ROOT/'outputs/balanced_rare_final/calibration/order_1/federated/balanced_rare_60/trial_0/results.json').read_text())
    assert a['history'][0]['calibration']==b['history'][0]['calibration']
    frame=pd.read_csv(OUT/'all_per_run_metrics.csv');count=0;checkpoints=0;prediction_rows=0;stream_rows=0;torch.set_num_threads(1)
    for order,sequence in c['orders'].items():
        split=ROOT/'outputs/multiclass_full_comparison/splits'/order;data=torch.load(split/'prepared_local_only.pt',weights_only=False,map_location='cpu');manifest=pd.read_csv(split/'split_manifest.csv');labels=data['y'].numpy();roles=data['roles'];names=data['classes']
        merged=['Benign']+sorted((set(names)-set(SCAN_TYPES)-{'Benign'})|{'Scan'});mapping=np.array([merged.index('Scan' if n in SCAN_TYPES else n) for n in names])
        for p in (RUN/'runs'/order).glob('*/*/seed_*/results.json'):
            r=json.loads(p.read_text());assert not r['calibration_only'];assert r['settings']==next(x for x in chosen['selected'] if x['order']==order and x['environment']==r['environment'])['settings'];best={}
            for h in r['history']:
                source=p.parent/f"checkpoint_{h['checkpoint']}_predictions.npz";assert source.stat().st_mtime_ns>=selection_time
                with np.load(source) as z:idx=z['sample_index'];y=z['y_true'];raw=z['probability'];pred=z['y_pred']
                assert (roles[idx]=='evaluation').all() and np.array_equal(y,labels[idx]);assert np.isfinite(raw).all() and np.allclose(raw.sum(1),1,atol=1e-6);assert np.array_equal(pred,raw.argmax(1))
                q=np.zeros((len(idx),len(merged)))
                for col in range(raw.shape[1]):q[:,mapping[col]]+=raw[:,col]
                truth=mapping[y];predicted=q.argmax(1);tasks=manifest.task.to_numpy()[idx];clients=manifest.client.to_numpy()[idx]
                acc={t:float((truth[tasks==t]==predicted[tasks==t]).mean()) for t in h['tasks']};drops={t:max(0.,best.get(t,a)-a) for t,a in acc.items()};best={t:max(best.get(t,a),a) for t,a in acc.items()};checkpoints+=1;prediction_rows+=len(idx)
            expected={'old_task_accuracy':np.mean([acc[t] for t in sequence[:-1]]),'forgetting':np.mean([drops[t] for t in sequence[:-1]]),'slowloris_recall':np.mean(predicted[truth==merged.index('Slowloris_Scan')]==merged.index('Slowloris_Scan'))}
            expected['worst_client_macro_recall']=min(np.mean([np.mean(predicted[(clients==cl)&(truth==lab)]==lab) for lab in np.unique(truth[clients==cl])]) for cl in np.unique(clients))
            record=frame[(frame.method=='cbrs_60')&(frame.order==order)&(frame.environment==r['environment'])&(frame.seed==r['seed'])&(frame.score_space=='merged_scans')];assert len(record)==1
            for k,v in expected.items():assert np.isclose(record.iloc[0][k],v)
            model=TrafficMLP(data['x'].shape[1],len(names));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True));model.eval()
            with torch.no_grad():actual=np.concatenate([torch.softmax(model(data['x'][idx[i:i+4096]]),1).numpy() for i in range(0,len(idx),4096)])
            assert np.allclose(actual,raw,atol=1e-6)
            clnames=list(data['assigned']) if r['environment']=='federated' else ['pooled'];capacity=60 if r['environment']=='federated' else 300
            states={cl:CBRS(capacity,len(names),np.random.default_rng(r['seed']*100+i+10000)) for i,cl in enumerate(clnames)};rngs={cl:np.random.default_rng(r['seed']*100+i+20000) for i,cl in enumerate(clnames)};observed={cl:set() for cl in clnames}
            for entry in json.loads((p.parent/'memory_audit.json').read_text()):
                cl=entry['client'];t=entry['stage']-1;current=data['tasks'][t]['train'][cl] if r['environment']=='federated' else np.unique(np.concatenate(list(data['tasks'][t]['train'].values())))
                current=np.unique(current);new=current if t==0 else current[labels[current]!=0];stream=rngs[cl].permutation(new);assert np.array_equal(stream,entry['stream_rows']);assert not observed[cl].intersection(stream.tolist());observed[cl].update(stream.tolist());assert (roles[stream]=='fitting').all();stream_rows+=len(stream)
                memory,audit=states[cl].ingest(stream,labels);assert memory.tolist()==entry['memory_rows'] and len(set(memory))==len(memory)<=capacity
                for k,v in audit.items():assert v==entry[k],k
                assert set(memory).issubset(observed[cl]);assert np.array_equal(np.bincount(labels[list(observed[cl])],minlength=len(names)),states[cl].encountered)
            assert sum(len(v) for v in observed.values())==int((roles=='fitting').sum());count+=1
    assert count==60 and checkpoints==240
    pairs=pd.read_csv(OUT/'paired_intervals.csv');assert len(pairs)==64
    for _,r in pairs.iterrows():
        f=frame[(frame.score_space==r.score_space)&(frame.environment==r.environment)]
        if r.order!='averaged':f=f[f.order==r.order]
        f=f.groupby(['method','seed'])[r.metric].mean().unstack(0);d=(f[r.left]-f[r.right]).to_numpy(copy=True);d[np.abs(d)<1e-12]=0;assert len(d)==10;half=2.2621571628*d.std(ddof=1)/np.sqrt(10)
        assert np.allclose([r.mean_difference,r.ci95_low,r.ci95_high],[d.mean(),d.mean()-half,d.mean()+half])
    for rel,h in json.loads((OUT/'analysis_input_hashes.json').read_text()).items():assert sha(ROOT/rel)==h
    result={'status':'passed','calibration_fits':12,'evaluation_runs':count,'models_checked':count,'checkpoints':checkpoints,'prediction_rows':prediction_rows,'stream_arrivals_checked':stream_rows,'paired_intervals':64,'selection_calibration_only':True,'all_calibration_before_evaluation':True,'persistent_counters_and_full_flags':True,'population_independent_of_replay_fraction':True,'first_checkpoint_matches_frozen_training':True,'original_inputs_unchanged':True}
    for folder in [RUN,OUT]:(folder/'verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
