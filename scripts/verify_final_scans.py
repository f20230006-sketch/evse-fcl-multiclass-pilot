"""Independent checks of saved re-scores, source immutability, RF roles and contrasts."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.scan_final import SCAN_TYPES,RARE_TYPES

OUT=ROOT/'outputs/final_scan_analysis'

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def check_interval(row,d):
    d=np.asarray(d,dtype=float);assert len(d)==10 and np.isfinite(d).all()
    mean=d.mean();half=2.2621571628*d.std(ddof=1)/np.sqrt(10)
    assert np.allclose([mean,mean-half,mean+half],[row.mean_difference,row.ci95_low,row.ci95_high],atol=1e-12)
    assert row.significance==('significant' if mean-half>0 or mean+half<0 else 'not significant')

def main():
    inputs=json.loads((OUT/'saved_prediction_input_hashes.json').read_text());assert all(sha(ROOT/p)==h for p,h in inputs.items())
    protocol=json.loads((OUT/'rescore_protocol.json').read_text());assert all(sha(ROOT/p)==h for p,h in protocol['source_hashes'].items())
    base=ROOT/'outputs/multiclass_full_comparison';meta={}
    for order in ['order_1','order_2','order_3']:
        m=pd.read_csv(base/'splits'/order/'split_manifest.csv');meta[order]=m
    runs=0;rows=0;checkpoints=0
    for path in sorted((OUT/'merged_predictions').glob('*/*/*/seed_*/results.json')):
        r=json.loads(path.read_text());m=meta[r['order']];source=ROOT/r['source_result'];original=json.loads(source.read_text());oldnames=sorted(json.loads((base/'splits'/r['order']/'class_mapping.json').read_text()),key=lambda n:json.loads((base/'splits'/r['order']/'class_mapping.json').read_text())[n]);newnames=r['classes'];mapping=np.array([newnames.index('Scan' if n in SCAN_TYPES else n) for n in oldnames]);best={};client_best={}
        for h in r['history']:
            number=h['checkpoint']
            with np.load(source.parent/f'checkpoint_{number}_predictions.npz') as z:
                idx=z['sample_index'];truth=mapping[z['y_true']];q=np.zeros((len(idx),len(newnames)),dtype=np.float64)
                for c,new in enumerate(mapping):q[:,new]+=z['probability'][:,c].astype(np.float64)
            assert (m.persistent_role.to_numpy()[idx]=='evaluation').all()
            pred=q.argmax(1)
            with np.load(path.parent/f'checkpoint_{number}_merged.npz') as z:
                assert np.array_equal(idx,z['sample_index']) and np.array_equal(truth,z['y_true']) and np.array_equal(pred,z['y_pred'])
                if 'probability' in z:assert np.allclose(q,z['probability'],atol=1e-12)
            for task,accuracy in h['cohort_accuracy'].items():
                mask=m.task.to_numpy()[idx]==task;value=float((truth[mask]==pred[mask]).mean());assert np.isclose(value,accuracy)
                drop=max(0.,best.get(task,value)-value);assert np.isclose(drop,h['cohort_forgetting'][task]);best[task]=max(best.get(task,value),value)
            rare=np.isin(truth,[newnames.index(c) for c in RARE_TYPES]);recall=float((truth[rare]==pred[rare]).mean()) if rare.any() else None
            assert recall is None if h['pooled']['rare_attack_recall'] is None else np.isclose(recall,h['pooled']['rare_attack_recall'])
            assert np.isclose(h['pooled']['accuracy'],(truth==pred).mean())
            scores=[]
            for client,values in h['per_client'].items():
                mask=m.client.to_numpy()[idx]==client;y=truth[mask];p=pred[mask];macro=float(np.mean([np.mean(p[y==c]==c) for c in np.unique(y)]));scores.append(macro);assert np.isclose(macro,values['macro_recall'])
                benign=y==0
                assert np.isclose(values['false_alarm_rate'],(p[benign]!=0).mean()) if benign.any() else values['false_alarm_rate'] is None
                raremask=np.isin(y,[newnames.index(c) for c in RARE_TYPES])
                assert np.isclose(values['rare_attack_recall'],(p[raremask]==y[raremask]).mean()) if raremask.any() else values['rare_attack_recall'] is None
                for pc in values['per_class']:
                    c=newnames.index(pc['class']);supported=y==c;assert int(supported.sum())==pc['support']
                    assert np.isclose(pc['recall'],(p[supported]==c).mean()) if supported.any() else pc['recall'] is None
                for task,acc in h['per_client_cohort_accuracy'][client].items():
                    cohortmask=mask&(m.task.to_numpy()[idx]==task);value=float((truth[cohortmask]==pred[cohortmask]).mean());assert np.isclose(value,acc)
                    key=(client,task);drop=max(0.,client_best.get(key,value)-value);assert np.isclose(drop,h['per_client_cohort_forgetting'][client][task]);client_best[key]=max(client_best.get(key,value),value)
            rows+=len(idx);checkpoints+=1
        assert np.isclose(r['summary']['worst_client_macro_recall'],min(scores))
        sequence=json.loads((base/'protocol_before_evaluation.json').read_text())['config']['orders'][r['order']]
        assert np.isclose(r['summary']['old_task_accuracy'],np.mean([h['cohort_accuracy'][t] for t in sequence[:-1]]))
        assert r['summary']['forgetting'] is None if r['method']=='joint' else np.isclose(r['summary']['forgetting'],np.mean([h['cohort_forgetting'][t] for t in sequence[:-1]]))
        for client,values in r['per_client_summary'].items():
            old=[h['per_client_cohort_accuracy'][client][t] for t in sequence[:-1] if t in h['per_client_cohort_accuracy'][client]]
            drops=[h['per_client_cohort_forgetting'][client][t] for t in sequence[:-1] if t in h['per_client_cohort_forgetting'][client]]
            assert np.isclose(values['old_task_accuracy'],np.mean(old)) if old else values['old_task_accuracy'] is None
            assert values['forgetting'] is None if r['method']=='joint' or not drops else np.isclose(values['forgetting'],np.mean(drops))
        runs+=1
    assert runs==840
    f=pd.read_csv(OUT/'merged_per_run_metrics.csv');seeds=f.groupby(['environment','method','seed']).mean(numeric_only=True).reset_index();checked=0
    for _,r in pd.read_csv(OUT/'merged_paired_intervals.csv').iterrows():
        group=seeds[seeds.environment==r.environment] if r.order=='averaged' else f[(f.environment==r.environment)&(f.order==r.order)]
        a=group[group.method==r.left].set_index('seed')[r.metric];b=group[group.method==r.right].set_index('seed')[r.metric];check_interval(r,(a-b).sort_index());checked+=1
    for _,r in pd.read_csv(OUT/'merged_federation_interactions.csv').iterrows():
        p=seeds.pivot(index='seed',columns=['environment','method'],values=r.metric);n=int(r.memory_per_client);d=p[('federated',f'protected_{n}')]-p[('federated',f'{r.baseline}_{n}')]-p[('centralized',f'protected_{n}')]+p[('centralized',f'{r.baseline}_{n}')];check_interval(r,d.sort_index());checked+=1
    rare=pd.read_csv(OUT/'rare_classes_per_seed.csv')
    for _,r in pd.read_csv(OUT/'rare_federation_interactions.csv').iterrows():
        group=rare[(rare.score_space==r.score_space)&(rare['class']==r['class'])];p=group.pivot(index='seed',columns=['environment','method'],values='recall');n=int(r.memory_per_client);d=p[('federated',f'protected_{n}')]-p[('federated',f'{r.baseline}_{n}')]-p[('centralized',f'protected_{n}')]+p[('centralized',f'{r.baseline}_{n}')];check_interval(r,d.sort_index());checked+=1
    for _,r in pd.read_csv(OUT/'rare_federated_deficits.csv').iterrows():
        group=rare[(rare.score_space==r.score_space)&(rare['class']==r['class'])&(rare.method==r.method)];p=group.pivot(index='seed',columns='environment',values='recall');check_interval(r,(p.centralized-p.federated).sort_index());checked+=1
    client=pd.read_csv(OUT/'focus_clients_per_run.csv');cols=['old_task_accuracy','forgetting','rare_attack_recall','macro_recall','false_alarm_rate','Slowloris_Scan_recall','ICMP_Fragmentation_recall'];cs=client.groupby(['score_space','environment','client','method','seed'])[cols].mean().reset_index()
    for _,r in pd.read_csv(OUT/'focus_client_paired_intervals.csv').iterrows():
        g=cs[(cs.score_space==r.score_space)&(cs.environment==r.environment)&(cs.client==r.client)];a=g[g.method==r.left].set_index('seed')[r.metric];b=g[g.method==r.right].set_index('seed')[r.metric];d=(a-b).sort_index()
        if r.significance=='not estimable':assert d.isna().all()
        else:check_interval(r,d);checked+=1
    rf=OUT/'random_forest';p=json.loads((rf/'protocol_before_evaluation.json').read_text());assert all(sha(ROOT/x)==h for x,h in p['source_and_input_hashes'].items())
    trials=json.loads((rf/'calibration_trials.json').read_text());assert trials['test_data_used'] is False and len(trials['trials'])==6
    rf_count=0
    for order in ['order_1','order_2','order_3']:
        m=meta[order];roles=json.loads((rf/f'{order}_role_indices.json').read_text())
        assert set(roles['fitting']).isdisjoint(roles['calibration']) and set(roles['fitting']).isdisjoint(roles['evaluation'])
        for role,indices in roles.items():assert (m.persistent_role.to_numpy()[indices]==role).all() and m.label.to_numpy()[indices].tolist() and set(m.label.to_numpy()[indices]).issubset(SCAN_TYPES)
        for path in (rf/order).glob('seed_*/evaluation_predictions.npz'):
            with np.load(path) as z:
                idx=z['sample_index'];assert np.array_equal(idx,np.asarray(roles['evaluation']));assert np.array_equal(z['y_true'],m.class_id.to_numpy()[idx]);assert np.array_equal(z['y_pred'],z['probability_class_ids'][z['probability'].argmax(1)]);assert np.allclose(z['probability'].sum(1),1)
                result=json.loads((path.parent/'results.json').read_text());assert np.isclose(result['accuracy'],(z['y_true']==z['y_pred']).mean());assert result['settings']==trials['selected'][order]
            rf_count+=1
    assert rf_count==30
    reconstruction=pd.read_csv(OUT/'rare_metric_reconstruction.csv');assert np.allclose(reconstruction.rare_attack_recall_saved,reconstruction.rare_attack_recall_reconstructed)
    report={'status':'passed','merged_runs_checked':runs,'merged_checkpoints_checked':checkpoints,'merged_prediction_rows_checked':rows,'paired_interval_rows_checked':checked,'random_forest_evaluation_runs_checked':rf_count,'calibration_trials':6,'rare_metric_reconstruction_runs':len(reconstruction),'original_prediction_and_split_hashes_unchanged':True,'evaluation_rows_excluded_from_RF_fitting_and_selection':True}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
