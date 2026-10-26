"""Final frozen experiment: merged primary scores and exact-type sensitivity."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.scan_final import scan_mapping, merge_probabilities, paired_interval
from evse_ids.multiclass_pilot import metrics, save_json

OUT=ROOT/'outputs/balanced_rare_report'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
KEY=['order','environment','method','seed']

def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def slow(m):
    return next((x['recall'] for x in m['per_class'] if x['class']=='Slowloris_Scan'),None)

def rescore(path,manifest,classes,sequence):
    r=json.loads(path.read_text()); names,mapping=scan_mapping(classes)
    key={k:r[k] for k in ['environment','method','seed']};key['order']=path.parents[3].name
    best={};history=[];pc=[]
    for checkpoint in r['history']:
        source=path.parent/f"checkpoint_{checkpoint['checkpoint']}_predictions.npz"
        with np.load(source) as z: idx=z['sample_index'];y=z['y_true'];p=z['probability']
        assert (manifest.persistent_role.to_numpy()[idx]=='evaluation').all()
        q=merge_probabilities(p,mapping,len(names));truth=mapping[y];pred=q.argmax(1)
        seen=sorted(set(mapping[checkpoint['seen_classes']].tolist()))
        pooled=metrics(truth,q,names,seen);tasks=manifest.task.to_numpy()[idx];clients=manifest.client.to_numpy()[idx]
        acc={};drops={};local={}
        for task in checkpoint['tasks']:
            mask=tasks==task;acc[task]=float((truth[mask]==pred[mask]).mean())
            drops[task]=max(0.,best.get(task,acc[task])-acc[task]);best[task]=max(best.get(task,acc[task]),acc[task])
        for client in sorted(manifest.client.unique()):
            mask=clients==client;local[client]=metrics(truth[mask],q[mask],names,seen)
        history.append({'checkpoint':checkpoint['checkpoint'],'cohort_accuracy':acc,'cohort_forgetting':drops,'pooled':pooled,'per_client':local})
    merged={**key,'score_space':'merged_scans','old_task_accuracy':np.mean([acc[t] for t in sequence[:-1]]),
        'forgetting':np.mean([drops[t] for t in sequence[:-1]]),'slowloris_recall':slow(pooled),
        'worst_client_macro_recall':min(m['macro_recall'] for m in local.values() if m['macro_recall'] is not None)}
    original={**key,'score_space':'original_type',**{k:r['summary'][k] for k in METRICS if k!='slowloris_recall'},'slowloris_recall':slow(r['history'][-1]['pooled'])}
    for client,m in local.items():
        pc.append({**key,'score_space':'merged_scans','client':client,'macro_recall':m['macro_recall'],'slowloris_recall':slow(m),'false_alarm_rate':m['false_alarm_rate']})
    destination=OUT/'new_merged_results'/key['order']/key['environment']/key['method']/f"seed_{key['seed']}"
    destination.mkdir(parents=True,exist_ok=True)
    save_json(destination/'results.json',{**key,'classes':names,'summary':merged,'history':history})
    np.savez_compressed(destination/'final_merged_predictions.npz',sample_index=idx,y_true=truth,y_pred=pred,probability=q)
    return [merged,original],pc

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    run=ROOT/'outputs/balanced_rare_final';base=ROOT/'outputs/final_scan_analysis'
    config=json.loads((run/'protocol_before_evaluation.json').read_text())['config']
    assert json.loads((run/'completion.json').read_text())['evaluation_runs']==120
    sources={};frames=[]
    for space,name in [('merged_scans',base/'merged_per_run_metrics.csv'),('original_type',ROOT/'outputs/replay_followup_report/all_type_per_run_metrics.csv')]:
        frame=pd.read_csv(name);rare=pd.read_csv(base/'rare_classes_per_run.csv')
        rare=rare[(rare.score_space==space)&(rare.client=='pooled')&(rare['class']=='Slowloris_Scan')]
        frame=frame.merge(rare[KEY+['recall']].rename(columns={'recall':'slowloris_recall'}),on=KEY,validate='one_to_one')
        frame['score_space']=space;frames.append(frame[KEY+['score_space']+METRICS]);sources[str(name.relative_to(ROOT))]=digest(name)
    sources[str((base/'rare_classes_per_run.csv').relative_to(ROOT))]=digest(base/'rare_classes_per_run.csv')
    new=[];clients=[]
    for order,sequence in config['orders'].items():
        split=ROOT/config['reference_output']/'splits'/order
        manifest=pd.read_csv(split/'split_manifest.csv');mapping=json.loads((split/'class_mapping.json').read_text());classes=sorted(mapping,key=mapping.get)
        for path in sorted((run/'runs'/order).glob('*/*/seed_*/results.json')):
            rows,pc=rescore(path,manifest,classes,sequence);new.extend(rows);clients.extend(pc)
            for p in [path,*path.parent.glob('*predictions.npz')]:sources[str(p.relative_to(ROOT))]=digest(p)
    assert len(new)==240
    frame=pd.concat(frames+[pd.DataFrame(new)],ignore_index=True)
    frame.to_csv(OUT/'all_per_run_metrics.csv',index=False);pd.DataFrame(clients).to_csv(OUT/'new_per_client_metrics.csv',index=False)
    seeds=frame.groupby(['score_space','environment','method','seed'])[METRICS].mean().reset_index()
    seeds.to_csv(OUT/'seed_order_averaged.csv',index=False)
    summary=seeds.groupby(['score_space','environment','method'])[METRICS].agg(['mean','std']);summary.columns=['_'.join(c) for c in summary.columns];summary.reset_index().to_csv(OUT/'summary.csv',index=False)
    order=frame.groupby(['score_space','environment','method','order'])[METRICS].agg(['mean','std']);order.columns=['_'.join(c) for c in order.columns];order.reset_index().to_csv(OUT/'per_order_summary.csv',index=False)
    comparisons=[]
    for space in ['merged_scans','original_type']:
        for env in config['environments']:
            for capacity in [60,300]:
                for baseline in ['class_balanced','protected']:
                    for order in ['averaged',*config['orders']]:
                        subset=(seeds if order=='averaged' else frame[frame.order==order]);subset=subset[(subset.score_space==space)&(subset.environment==env)]
                        left=subset[subset.method==f'balanced_rare_{capacity}'].set_index('seed');right=subset[subset.method==f'{baseline}_{capacity}'].set_index('seed')
                        assert set(left.index)==set(right.index)==set(config['seeds'])
                        for metric in METRICS:
                            d=(left[metric]-right[metric]).sort_index()
                            d=d.mask(d.abs()<1e-12,0.)  # Remove binary round-off at mathematical ties.
                            ci=paired_interval(d)
                            direction='better' if (ci['ci95_high']<0 if metric=='forgetting' else ci['ci95_low']>0) else 'worse' if (ci['ci95_low']>0 if metric=='forgetting' else ci['ci95_high']<0) else 'not significant'
                            comparisons.append({'score_space':space,'environment':env,'capacity':capacity,'order':order,'left':f'balanced_rare_{capacity}','right':f'{baseline}_{capacity}','metric':metric,'outcome':direction,**ci})
    comparison_frame=pd.DataFrame(comparisons)
    comparison_frame.to_csv(OUT/'paired_intervals.csv',index=False)
    screens=[]
    for (space,env,capacity,order),group in comparison_frame[comparison_frame.right.str.startswith('class_balanced_')].groupby(['score_space','environment','capacity','order']):
        results=group.set_index('metric')
        slow_better=results.loc['slowloris_recall','ci95_low']>0
        old_worse=results.loc['old_task_accuracy','ci95_high']<0
        worst_worse=results.loc['worst_client_macro_recall','ci95_high']<0
        screens.append({'score_space':space,'environment':env,'capacity':capacity,'order':order,
            'slowloris_significantly_better':bool(slow_better),'old_accuracy_significantly_worse':bool(old_worse),
            'worst_client_significantly_worse':bool(worst_worse),'requested_significance_screen_met':bool(slow_better and not old_worse and not worst_worse),
            'noninferiority_established':False})
    pd.DataFrame(screens).to_csv(OUT/'requested_outcome_screen.csv',index=False)
    alignment=['environment','capacity','order','right','metric']
    agreement=comparison_frame[comparison_frame.score_space=='merged_scans'][alignment+['outcome']].merge(
        comparison_frame[comparison_frame.score_space=='original_type'][alignment+['outcome']],on=alignment,suffixes=('_merged','_type'),validate='one_to_one')
    agreement['same_significance_direction']=agreement.outcome_merged==agreement.outcome_type
    agreement.to_csv(OUT/'score_space_sensitivity.csv',index=False)
    interactions=[]
    for space in ['merged_scans','original_type']:
        for capacity in [60,300]:
            for baseline in ['class_balanced','protected']:
                for metric in METRICS:
                    p=seeds[seeds.score_space==space].pivot(index='seed',columns=['environment','method'],values=metric)
                    d=(p[('federated',f'balanced_rare_{capacity}')]-p[('federated',f'{baseline}_{capacity}')])-(p[('centralized',f'balanced_rare_{capacity}')]-p[('centralized',f'{baseline}_{capacity}')])
                    d=d.mask(d.abs()<1e-12,0.)
                    interactions.append({'score_space':space,'capacity':capacity,'baseline':baseline,'metric':metric,**paired_interval(d)})
    pd.DataFrame(interactions).to_csv(OUT/'federation_interactions.csv',index=False)
    save_json(OUT/'analysis_input_hashes.json',sources)
    save_json(OUT/'analysis_protocol.json',{'primary':'merged_scans','rare_metric':'Slowloris recall only','original_task_cohorts_retained':True,'training_labels_unchanged':True,'seed_sd':'sample SD over ten seed averages of three orders','paired_intervals':'two-sided t9, unadjusted multiple comparisons','roundoff_rule':'Absolute paired differences below 1e-12 are zero; prevents floating point ties being labeled significant. Training/selection unchanged.','not_significant_is_not_noninferiority':True,'new_evaluation_runs':120,'original_evaluation_runs_reused':840,'source_hash':digest(Path(__file__))})
    print('Analyzed 120 new runs and 840 prior runs in both scoring views.',flush=True)

if __name__=='__main__':main()
