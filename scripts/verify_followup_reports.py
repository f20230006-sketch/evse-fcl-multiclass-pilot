"""Independent arithmetic, pairing, confusion, and family-convention checks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'outputs/replay_followup_report';f=pd.read_csv(out/'all_type_per_run_metrics.csv');p=pd.read_csv(out/'paired_intervals.csv')
    assert len(f)==840 and not f.duplicated(['order','environment','method','seed']).any()
    for _,r in p.iterrows():
        env,methods=r.contrast.split(' ',1);left,right=methods.split('_minus_');group=f[f.environment==env]
        if r.order=='averaged':group=group.groupby(['method','seed'])[r.metric].mean().reset_index()
        else:group=group[group.order==r.order]
        a=group[group.method==left].set_index('seed')[r.metric];b=group[group.method==right].set_index('seed')[r.metric]
        assert set(a.index)==set(b.index)==set(range(42,52));d=(a-b).sort_index();assert len(d)==10 and d.notna().all()
        mean=d.mean();half=2.2621571628*d.std(ddof=1)/np.sqrt(10)
        assert np.isclose(mean,r.mean_difference) and np.isclose(mean-half,r.ci95_low) and np.isclose(mean+half,r.ci95_high)
    family=pd.read_csv(out/'family_per_run_metrics.csv');merged=family.merge(f,on=['order','environment','method','seed'],suffixes=('_family','_type'),validate='one_to_one');assert len(merged)==840
    assert (merged.mapped_old_task_accuracy+1e-12>=merged.old_task_accuracy_type).all()
    assert (merged.mapped_rare_attack_recall+1e-12>=merged.rare_attack_recall_type).all()
    base=ROOT/'outputs/multiclass_full_comparison';diag=ROOT/'outputs/joint_diagnostics';checked=0
    for env in ['federated','centralized']:
        pooled=None
        for order in ['order_1','order_2','order_3']:
            mapping=json.loads((base/'splits'/order/'class_mapping.json').read_text());names=sorted(mapping,key=mapping.get);counts=np.zeros((len(names),len(names)),dtype=int)
            for seed in range(42,52):
                q=np.load(base/'runs'/order/env/'joint'/f'seed_{seed}'/'checkpoint_4_predictions.npz');np.add.at(counts,(q['y_true'],q['y_pred']),1);checked+=1
            exported=pd.read_csv(diag/f'{env}_{order}_confusion_counts.csv',index_col=0)
            assert list(exported.columns)==names and np.array_equal(exported.to_numpy(),counts)
            norm=pd.read_csv(diag/f'{env}_{order}_confusion_row_normalized.csv',index_col=0).to_numpy();assert np.allclose(norm,counts/counts.sum(1,keepdims=True))
            pooled=counts if pooled is None else pooled+counts
        assert np.array_equal(pd.read_csv(diag/f'{env}_confusion_counts.csv',index_col=0).to_numpy(),pooled)
    result={'status':'passed','type_runs_checked':len(f),'paired_interval_rows_checked':len(p),'family_mapping_monotonicity_runs_checked':len(merged),'joint_confusion_runs_checked':checked,'seed_pairing':'10 matched seeds; orders averaged within seed','family_conventions':'winning-type mapping preserves exact-type correct predictions; sum-probability scoring separately labeled'}
    (out/'report_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
