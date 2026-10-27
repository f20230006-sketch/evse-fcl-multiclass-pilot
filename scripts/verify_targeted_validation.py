"""Independent boundary, model, allocation and statistical verification."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
import numpy as np
import pandas as pd
import torch
from evse_ids.multiclass_pilot import TrafficMLP
from evse_ids.scan_final import SCAN_TYPES
from verify_exploratory_tuning import balanced_counts
OUT=ROOT/'outputs/targeted_validation_2026_10_27';REPORT=ROOT/'outputs/targeted_validation_report_2026_10_27'
def main():
    protocol=json.loads((OUT/'protocol_before_evaluation.json').read_text());c=protocol['config']
    assert json.loads((OUT/'completion.json').read_text())['evaluation_runs']==420
    for section in ['source_hashes','inherited_hashes']:
        for rel,h in protocol[section].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
    selection=json.loads((OUT/'hyperparameter_trials.json').read_text());selection_time=(OUT/'hyperparameter_trials.json').stat().st_mtime_ns
    snapshot=OUT/'prepared_input_hashes_before_evaluation.json'
    assert snapshot.stat().st_mtime_ns<=selection_time
    for rel,h in json.loads(snapshot.read_text()).items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
    assert hashlib.sha256((ROOT/'outputs/multiclass_full_comparison/sampled_fixed.pkl').read_bytes()).hexdigest()==protocol['sample_hash']
    trials=list((OUT/'calibration').glob('split_*/*/*/*/trial_*/results.json'));assert len(trials)==132
    for p in trials:
        r=json.loads(p.read_text());assert r['calibration_only'] and not list(p.parent.glob('*predictions.npz'))
        assert p.stat().st_mtime_ns<=selection_time
        assert np.isclose(r['selection_score'],np.mean([h['calibration']['macro_recall'] for h in r['history']]))
    for selected in selection['selected']:
        grid=c['ablation_grid'] if selected['method']=='rare_random_60' else c['grids'][selected['method']]
        records=[r for r in selection['trials'] if all(r[k]==selected[k] for k in ['split_seed','order','environment','method'])]
        best=max(records,key=lambda r:(r['selection_score'],-grid.index(r['settings'])))
        assert best['settings']==selected['settings']
    frame=pd.read_csv(REPORT/'all_per_run_metrics.csv');torch.set_num_threads(1)
    counts=0;checkpoints=0;prediction_rows=0
    for split in [42,*c['additional_split_seeds']]:
        for order,sequence in c['orders'].items():
            sd=OUT/'splits'/f'split_{split}'/order if split!=42 else ROOT/'outputs/multiclass_full_comparison/splits'/order
            data=torch.load(sd/'prepared_local_only.pt',weights_only=False,map_location='cpu');manifest=pd.read_csv(sd/'split_manifest.csv')
            reference=pd.read_csv(ROOT/'outputs/multiclass_full_comparison/splits'/order/'split_manifest.csv')
            assert np.array_equal(manifest.client.to_numpy(),reference.client.to_numpy())
            if split!=42:assert not np.array_equal(manifest.persistent_role.to_numpy(),reference.persistent_role.to_numpy())
            roles=manifest.persistent_role.to_numpy();labels=manifest.label.to_numpy();classes=manifest.class_id.to_numpy();clients=manifest.client.to_numpy();tasks=manifest.task.to_numpy()
            assert manifest.loc[manifest.preprocessing_fit,'persistent_role'].eq('fitting').all()
            assert set(manifest.loc[manifest.preprocessing_fit,'task'])<={sequence[0],'benign_reference_all_tasks'}
            names=data['classes'];merged=['Benign']+sorted((set(names)-set(SCAN_TYPES)-{'Benign'})|{'Scan'});mapping=np.array([merged.index('Scan' if n in SCAN_TYPES else n) for n in names])
            for p in (OUT/'runs'/f'split_{split}'/order).glob('*/*/seed_*/results.json'):
                r=json.loads(p.read_text());assert (p.parent/'complete.json').exists()
                s=next(x for x in selection['selected'] if x['split_seed']==split and x['order']==order and x['environment']==r['environment'] and x['method']==r['method']);assert r['settings']==s['settings']
                best={}
                for h in r['history']:
                    f=p.parent/f"checkpoint_{h['checkpoint']}_predictions.npz";assert f.stat().st_mtime_ns>=selection_time
                    with np.load(f) as z:idx=z['sample_index'];y=z['y_true'];prob=z['probability'];pred=z['y_pred']
                    assert np.array_equal(y,classes[idx]) and (roles[idx]=='evaluation').all() and len(set(idx))==len(idx)
                    assert np.isfinite(prob).all() and np.allclose(prob.sum(1),1,atol=1e-6) and np.array_equal(pred,prob.argmax(1))
                    q=np.zeros((len(idx),len(merged)))
                    for col in range(prob.shape[1]):q[:,mapping[col]]+=prob[:,col]
                    truth=mapping[y];prediction=q.argmax(1);task=tasks[idx];localclients=clients[idx]
                    acc={t:float((truth[task==t]==prediction[task==t]).mean()) for t in h['tasks']};drops={t:max(0.,best.get(t,v)-v) for t,v in acc.items()};best={t:max(best.get(t,v),v) for t,v in acc.items()}
                    checkpoints+=1;prediction_rows+=len(idx)
                model=TrafficMLP(data['x'].shape[1],len(names));model.load_state_dict(torch.load(p.parent/'final_model.pt',weights_only=True));model.eval()
                with torch.no_grad():actual=np.concatenate([torch.softmax(model(data['x'][idx[a:a+4096]]),1).numpy() for a in range(0,len(idx),4096)])
                assert np.allclose(actual,prob,atol=1e-6)
                expected={'old_task_accuracy':np.mean([acc[t] for t in sequence[:-1]]),'forgetting':np.mean([drops[t] for t in sequence[:-1]]),'slowloris_recall':np.mean(prediction[truth==merged.index('Slowloris_Scan')]==merged.index('Slowloris_Scan'))}
                macros=[np.mean([np.mean(prediction[(localclients==cl)&(truth==lab)]==lab) for lab in np.unique(truth[localclients==cl])]) for cl in np.unique(localclients)];expected['worst_client_macro_recall']=min(macros)
                row=frame[(frame.split_seed==split)&(frame.order==order)&(frame.environment==r['environment'])&(frame.method==r['method'])&(frame.seed==r['seed'])&(frame.score_space=='merged_scans')];assert len(row)==1
                for k,v in expected.items():assert np.isclose(row.iloc[0][k],v)
                previous={};capacity=60 if r['environment']=='federated' else 300
                for entry in json.loads((p.parent/'memory_audit.json').read_text()):
                    cl=entry['client'];rows=np.asarray(entry['memory_rows'],int)
                    current=np.flatnonzero((roles=='fitting')&np.isin(tasks,[sequence[entry['stage']-1],'benign_reference_all_tasks'])&((clients==cl) if r['environment']=='federated' else True))
                    pool=np.unique(np.concatenate([previous.get(cl,np.array([],int)),current]));assert len(rows)==min(capacity,len(pool)) and len(rows)==len(set(rows)) and np.isin(rows,pool).all()
                    assert (roles[rows]=='fitting').all()
                    rare=pool[np.isin(labels[pool],['Slowloris_Scan','ICMP_Fragmentation'])]
                    if r['method'].startswith('class_balanced'):balanced_counts(pool,rows,labels)
                    elif r['method'].startswith('balanced_rare'):
                        reserved=np.asarray(entry['reserved_rows'],int);balanced=np.asarray(entry['balanced_rows'],int)
                        assert len(reserved)==min(int(capacity*r['settings']['rare_quota_fraction']),len(rare))
                        assert set(rows)==set(reserved)|set(balanced) and not set(reserved)&set(balanced)
                        balanced_counts(rare,reserved,labels);balanced_counts(np.setdiff1d(pool,reserved),balanced,labels)
                    else:assert np.isin(rows,rare).sum()>=min(int(capacity*r['settings']['rare_quota_fraction']),len(rare))
                    previous[cl]=rows
                counts+=1
    assert counts==420 and checkpoints==1680
    intervals=pd.read_csv(REPORT/'paired_intervals.csv')
    for _,r in intervals.iterrows():
        f=frame[(frame.split_seed==r.split_seed)&(frame.score_space==r.score_space)&(frame.environment==r.environment)]
        if r.order!='averaged':f=f[f.order==r.order]
        f=f.groupby(['method','seed'])[r.metric].mean().unstack(0);d=(f[r.left]-f[r.right]).to_numpy(copy=True);d[np.abs(d)<1e-12]=0
        assert len(d)==10;half=2.2621571628*d.std(ddof=1)/np.sqrt(10)
        assert np.allclose([r.mean_difference,r.ci95_low,r.ci95_high],[d.mean(),d.mean()-half,d.mean()+half])
    for rel,h in json.loads((REPORT/'analysis_input_hashes.json').read_text()).items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
    report={'status':'passed','calibration_runs':132,'evaluation_runs':counts,'models_checked':counts,'checkpoints':checkpoints,'prediction_rows':prediction_rows,'paired_intervals':len(intervals),'fixed_client_allocation':True,'new_role_splits':True,'task1_fitting_only_preprocessing':True,'calibration_only_selection':True,'all_calibration_before_evaluation':True,'memory_boundaries_verified':True,'independent_merged_scores_verified':True}
    for d in [OUT,REPORT]:(d/'verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
