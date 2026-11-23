"""Re-score frozen predictions with six scans merged; audit rare-class/FL effects."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.scan_final import SCAN_TYPES,RARE_TYPES,CORE,EXTRA,scan_mapping,merge_probabilities,paired_interval
from evse_ids.multiclass_pilot import metrics,save_json

OUT=ROOT/'outputs/final_scan_analysis'

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def summarize(frame,keys,columns,path):
    seed=frame.groupby(keys+['seed'],dropna=False)[columns].mean().reset_index()
    result=seed.groupby(keys,dropna=False)[columns].agg(['mean','std']);result.columns=['_'.join(v) for v in result.columns];result=result.reset_index();result.to_csv(path,index=False)
    return seed,result

def paired(frame,left,right,columns,**key):
    a=frame[frame.method==left].set_index('seed');b=frame[frame.method==right].set_index('seed');assert set(a.index)==set(b.index)==set(range(42,52))
    rows=[]
    for m in columns:
        d=(a[m]-b[m]).sort_index()
        if not d.notna().all():
            rows.append({**key,'left':left,'right':right,'metric':m,'n_seed_pairs':int(d.notna().sum()),'mean_difference':None,'ci95_low':None,'ci95_high':None,'significance':'not estimable'})
        else:rows.append({**key,'left':left,'right':right,'metric':m,**paired_interval(d.to_numpy())})
    return rows

def run_rescore():
    OUT.mkdir(parents=True,exist_ok=True);base=ROOT/'outputs/multiclass_full_comparison'
    roots=[base,ROOT/'outputs/replay_followup_essential',ROOT/'outputs/replay_followup_sweep']
    config=json.loads((base/'protocol_before_evaluation.json').read_text())['config'];metas={};sources={}
    for order in config['orders']:
        folder=base/'splits'/order;manifest=pd.read_csv(folder/'split_manifest.csv');mapping=json.loads((folder/'class_mapping.json').read_text());classes=sorted(mapping,key=mapping.get);names,to_new=scan_mapping(classes)
        assert np.array_equal(manifest.sample_index,np.arange(len(manifest)))
        metas[order]=(manifest,classes,names,to_new)
        for p in [folder/'split_manifest.csv',folder/'class_mapping.json']:sources[p.relative_to(ROOT).as_posix()]=sha(p)
    protocol={'source':'existing saved probabilities only','scan_types':list(SCAN_TYPES),'output_classes':names,'rule':'sum the six probabilities, then argmax in the 10-class space','retention_definition':'original old-task cohorts, scored in merged label space; Scan spans reconnaissance and vulnerability cohorts','no_retraining':True,'no_changes_to_original_task_order':True,'source_hashes':{p:sha(ROOT/p) for p in ['src/evse_ids/scan_final.py','scripts/analyze_final_scans.py']}}
    save_json(OUT/'rescore_protocol.json',protocol)
    all_rows=[];clients=[];classes_out=[];checkpoints=[];count=0
    for root in roots:
        paths=sorted((root/'runs').glob('*/*/*/seed_*/results.json'))
        assert len(paths)==(420 if root==base else 60 if root.name.endswith('essential') else 360)
        for path in paths:
            original=json.loads(path.read_text());order=path.parents[3].name;key={'order':order,'environment':original['environment'],'method':original['method'],'seed':original['seed']}
            manifest,old_names,names,mapping=metas[order];roles=manifest.persistent_role.to_numpy();cohorts=manifest.task.to_numpy();station=manifest.client.to_numpy();true_types=manifest.class_id.to_numpy();all_clients=sorted(manifest.client.unique())
            destination=OUT/'merged_predictions'/order/key['environment']/key['method']/f"seed_{key['seed']}";destination.mkdir(parents=True,exist_ok=True)
            best={};best_client={};history=[];summary=None;local_summary={}
            sources[path.relative_to(ROOT).as_posix()]=sha(path)
            for h in original['history']:
                source=path.parent/f"checkpoint_{h['checkpoint']}_predictions.npz";sources[source.relative_to(ROOT).as_posix()]=sha(source)
                with np.load(source) as z:indices=z['sample_index'];old_y=z['y_true'];old_prob=z['probability']
                assert (roles[indices]=='evaluation').all() and np.array_equal(old_y,true_types[indices])
                y=mapping[old_y];q=merge_probabilities(old_prob,mapping,len(names));pred=q.argmax(1);seen=sorted(set(mapping[h['seen_classes']].tolist()))
                pooled=metrics(y,q,names,seen);rare_recalls=[r['recall'] for r in pooled['per_class'] if r['class'] in RARE_TYPES and r['recall'] is not None];pooled['rare_attack_macro_recall']=float(np.mean(rare_recalls)) if rare_recalls else None
                local={};cohort_values={};cohort_drops={};local_cohorts={c:{} for c in all_clients};local_drops={c:{} for c in all_clients}
                for c in all_clients:
                    mask=station[indices]==c;local[c]=metrics(y[mask],q[mask],names,seen)
                for task in h['tasks']:
                    mask=cohorts[indices]==task;assert mask.any()
                    acc=float((y[mask]==pred[mask]).mean());cohort_values[task]=acc;cohort_drops[task]=max(0.,best.get(task,acc)-acc);best[task]=max(best.get(task,acc),acc)
                    for c in all_clients:
                        mask=(cohorts[indices]==task)&(station[indices]==c)
                        if not mask.any():continue
                        acc=float((y[mask]==pred[mask]).mean());k=(c,task);local_cohorts[c][task]=acc;local_drops[c][task]=max(0.,best_client.get(k,acc)-acc);best_client[k]=max(best_client.get(k,acc),acc)
                checkpoints.append({**key,'checkpoint':h['checkpoint'],**{k:v for k,v in pooled.items() if k!='per_class'}})
                record={'checkpoint':h['checkpoint'],'seen_merged_class_ids':seen,'cohort_accuracy':cohort_values,'cohort_forgetting':cohort_drops,'per_client_cohort_accuracy':local_cohorts,'per_client_cohort_forgetting':local_drops,'pooled':pooled,'per_client':local};history.append(record)
                arrays={'sample_index':indices,'y_true':y,'y_pred':pred}
                if h is original['history'][-1]:arrays['probability']=q
                np.savez_compressed(destination/f"checkpoint_{h['checkpoint']}_merged.npz",**arrays)
            old=config['orders'][order][:-1]
            summary={k:v for k,v in pooled.items() if k!='per_class'};summary.update({'old_task_accuracy':float(np.mean([cohort_values[t] for t in old])),'forgetting':None if key['method']=='joint' else float(np.mean([cohort_drops[t] for t in old])),'worst_client_macro_recall':min(v['macro_recall'] for v in local.values() if v['macro_recall'] is not None)})
            for c,m in local.items():
                values=[local_cohorts[c][t] for t in old if t in local_cohorts[c]];drops=[local_drops[c][t] for t in old if t in local_drops[c]]
                local_summary[c]={**{k:v for k,v in m.items() if k!='per_class'},'old_task_accuracy':float(np.mean(values)) if values else None,'forgetting':None if key['method']=='joint' or not drops else float(np.mean(drops))}
                clients.append({**key,'client':c,**local_summary[c]})
                for pc in m['per_class']:classes_out.append({**key,'client':c,**pc})
            for pc in pooled['per_class']:classes_out.append({**key,'client':'pooled',**pc})
            all_rows.append({**key,**summary});save_json(destination/'results.json',{**key,'classes':names,'source_result':path.relative_to(ROOT).as_posix(),'summary':summary,'per_client_summary':local_summary,'history':history})
            count+=1
            if count%60==0:print(f'Rescored {count}/840',flush=True)
    frame=pd.DataFrame(all_rows);frame.to_csv(OUT/'merged_per_run_metrics.csv',index=False);pd.DataFrame(clients).to_csv(OUT/'merged_per_client_per_run.csv',index=False);pd.DataFrame(classes_out).to_csv(OUT/'merged_per_class_metrics.csv',index=False);pd.DataFrame(checkpoints).to_csv(OUT/'merged_checkpoint_metrics.csv',index=False)
    seed,summary=summarize(frame,['environment','method'],CORE+EXTRA,OUT/'merged_summary.csv');seed.to_csv(OUT/'merged_per_seed_order_averaged.csv',index=False)
    order=frame.groupby(['environment','method','order'])[CORE].agg(['mean','std']);order.columns=['_'.join(v) for v in order.columns];order.reset_index().to_csv(OUT/'merged_per_order_summary.csv',index=False)
    differences=[]
    for env in config['environments']:
        for size in [60,120,300]:
            for baseline in ['uniform','class_balanced']:
                a,b=f'protected_{size}',f'{baseline}_{size}';differences+=paired(seed[seed.environment==env],a,b,CORE,environment=env,order='averaged')
                for order in config['orders']:differences+=paired(frame[(frame.environment==env)&(frame.order==order)],a,b,CORE,environment=env,order=order)
    pd.DataFrame(differences).to_csv(OUT/'merged_paired_intervals.csv',index=False)
    interactions=[]
    for size in [60,120,300]:
        for b in ['uniform','class_balanced']:
            for metric in CORE:
                p=seed.pivot(index='seed',columns=['environment','method'],values=metric);d=(p[('federated',f'protected_{size}')]-p[('federated',f'{b}_{size}')])-(p[('centralized',f'protected_{size}')]-p[('centralized',f'{b}_{size}')])
                interactions.append({'memory_per_client':size,'baseline':b,'metric':metric,'definition':'(F_protected-F_baseline)-(C_protected-C_baseline)',**paired_interval(d.sort_index().to_numpy())})
    pd.DataFrame(interactions).to_csv(OUT/'merged_federation_interactions.csv',index=False)
    save_json(OUT/'saved_prediction_input_hashes.json',sources)
    assert all(sha(ROOT/p)==h for p,h in sources.items()),'Original evidence changed during analysis'
    save_json(OUT/'rescore_completion.json',{'status':'complete','evaluations_rescored':count,'classes_after_merge':len(names),'source_files_unchanged':True,'saved_prediction_inputs':sum(p.endswith('.npz') for p in sources)})

def rare_and_clients():
    previous=ROOT/'outputs/replay_followup_report';raw=pd.read_csv(previous/'all_type_per_class_metrics.csv');raw['score_space']='original_type'
    merged=pd.read_csv(OUT/'merged_per_class_metrics.csv');merged['score_space']='merged_scans'
    all_classes=pd.concat([raw,merged],ignore_index=True)
    rare=all_classes[all_classes['class'].isin(RARE_TYPES)].copy();rare.to_csv(OUT/'rare_classes_per_run.csv',index=False)
    pooled=rare[rare.client=='pooled'];seed,summary=summarize(pooled,['score_space','environment','method','class'],['recall','support'],OUT/'rare_classes_summary.csv');seed.to_csv(OUT/'rare_classes_per_seed.csv',index=False)
    order=pooled.groupby(['score_space','environment','method','order','class'])[['recall','support']].agg(['mean','std']);order.columns=['_'.join(c) for c in order.columns];order.reset_index().to_csv(OUT/'rare_classes_per_order.csv',index=False)
    gaps=[];interactions=[]
    for space in ['original_type','merged_scans']:
        for c in RARE_TYPES:
            part=seed[(seed.score_space==space)&(seed['class']==c)];pivot=part.pivot(index='seed',columns=['environment','method'],values='recall')
            for method in ['joint']+[f'{m}_{n}' for n in [60,120,300] for m in ['uniform','class_balanced','protected']]:
                d=pivot[('centralized',method)]-pivot[('federated',method)]
                gaps.append({'score_space':space,'class':c,'method':method,'definition':'centralized minus federated recall; positive means federated deficit',**paired_interval(d.sort_index().to_numpy())})
            for n in [60,120,300]:
                for b in ['uniform','class_balanced']:
                    d=(pivot[('federated',f'protected_{n}')]-pivot[('federated',f'{b}_{n}')])-(pivot[('centralized',f'protected_{n}')]-pivot[('centralized',f'{b}_{n}')])
                    interactions.append({'score_space':space,'class':c,'memory_per_client':n,'baseline':b,'definition':'positive means protection reduces the signed federated deficit relative to baseline',**paired_interval(d.sort_index().to_numpy())})
    pd.DataFrame(gaps).to_csv(OUT/'rare_federated_deficits.csv',index=False);pd.DataFrame(interactions).to_csv(OUT/'rare_federation_interactions.csv',index=False)
    type_clients=pd.read_csv(previous/'all_type_per_client_per_run_metrics.csv');type_clients['score_space']='original_type'
    merge_clients=pd.read_csv(OUT/'merged_per_client_per_run.csv');merge_clients['score_space']='merged_scans'
    cf=pd.concat([type_clients,merge_clients],ignore_index=True);cf=cf[cf.client.isin(['low_rate_rare_heavy','benign_starved'])]
    for c in RARE_TYPES:
        x=rare[rare['class']==c][['score_space','order','environment','method','seed','client','recall','support']].rename(columns={'recall':c+'_recall','support':c+'_support'})
        cf=cf.merge(x,on=['score_space','order','environment','method','seed','client'],how='left',validate='one_to_one')
    cf.to_csv(OUT/'focus_clients_per_run.csv',index=False)
    cm=[m for m in CORE if m!='worst_client_macro_recall']+['macro_recall','false_alarm_rate']+[c+'_recall' for c in RARE_TYPES]
    cs,_=summarize(cf,['score_space','environment','method','client'],cm,OUT/'focus_clients_summary.csv')
    client_pairs=[]
    for (space,env,client),group in cs.groupby(['score_space','environment','client']):
        for n in [60,120,300]:
            for b in ['uniform','class_balanced']:client_pairs+=paired(group,f'protected_{n}',f'{b}_{n}',[m for m in cm if m!='worst_client_macro_recall'],score_space=space,environment=env,client=client,memory_per_client=n)
    pd.DataFrame(client_pairs).to_csv(OUT/'focus_client_paired_intervals.csv',index=False)
    # Trace the original 33.33% metric: it is micro recall over two types, then an average over orders.
    baseline=pooled[(pooled.score_space=='original_type')&pooled.method.isin(['no_replay','ewc'])].copy()
    baseline['correct']=baseline.recall*baseline.support
    baseline.to_csv(OUT/'rare_baseline_class_breakdown.csv',index=False)
    runs=baseline.groupby(['environment','method','order','seed']).agg(correct=('correct','sum'),support=('support','sum')).reset_index();runs['rare_attack_recall']=runs.correct/runs.support
    original=pd.read_csv(previous/'all_type_per_run_metrics.csv');joined=runs.merge(original[['environment','method','order','seed','rare_attack_recall']],on=['environment','method','order','seed'],suffixes=('_reconstructed','_saved'),validate='one_to_one');assert np.allclose(joined.rare_attack_recall_reconstructed,joined.rare_attack_recall_saved)
    joined.to_csv(OUT/'rare_metric_reconstruction.csv',index=False)
    seeds,_=summarize(runs,['environment','method'],['rare_attack_recall'],OUT/'rare_baseline_reconstructed_summary.csv')
    save_json(OUT/'rare_metric_definition.json',{'classes':list(RARE_TYPES),'evaluation_support':{'Slowloris_Scan':600,'ICMP_Fragmentation':5},'within_run':'(correct Slowloris + correct ICMP fragmentation)/605; not an equal-class mean','across_runs':'average three orders within seed, then mean and sample SD over ten training seeds','no_replay_federated':'both types correct in order_2 where rare task is last; both forgotten in orders1/3; (0+1+0)/3 = 1/3','ewc_correction':'not exactly 33.33 ± 0.00 in saved evidence; finite fragmentation errors in last-rare order','neither_class_always_correct_across_orders':True,'reconstruction_matches_saved_metrics':True})

def main():
    run_rescore();rare_and_clients();print('Merged scores, rare-class diagnostics and client reports complete',flush=True)

if __name__=='__main__':main()
