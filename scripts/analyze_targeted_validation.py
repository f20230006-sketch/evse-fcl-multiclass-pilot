"""Both reporting views; split-specific paired intervals without pseudoreplication."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'src')]
import numpy as np
import pandas as pd
import analyze_balanced_rare_final as scoring
from evse_ids.scan_final import paired_interval
from evse_ids.multiclass_pilot import save_json
OUT=ROOT/'outputs/targeted_validation_report_2026_10_27'
METRICS=scoring.METRICS
def main():
    OUT.mkdir(exist_ok=True,parents=True);run=ROOT/'outputs/targeted_validation_2026_10_27';scoring.OUT=OUT
    config=json.loads((run/'protocol_before_evaluation.json').read_text())['config']
    assert json.loads((run/'completion.json').read_text())['evaluation_runs']==420
    old=pd.read_csv(ROOT/'outputs/balanced_rare_report/all_per_run_metrics.csv')
    old=old[old.method.isin(['class_balanced_60','balanced_rare_60','protected_60'])].copy();old['split_seed']=42
    rows=[];pcs=[];hashes={str((ROOT/'outputs/balanced_rare_report/all_per_run_metrics.csv').relative_to(ROOT)):scoring.digest(ROOT/'outputs/balanced_rare_report/all_per_run_metrics.csv')}
    for split in [42,*config['additional_split_seeds']]:
        scoring.OUT=OUT/f'split_{split}'
        for order,sequence in config['orders'].items():
            source=(run/'splits'/f'split_{split}'/order) if split!=42 else ROOT/'outputs/multiclass_full_comparison/splits'/order
            manifest=pd.read_csv(source/'split_manifest.csv');mapping=json.loads((source/'class_mapping.json').read_text());classes=sorted(mapping,key=mapping.get)
            for p in sorted((run/'runs'/f'split_{split}'/order).glob('*/*/seed_*/results.json')):
                r,pc=scoring.rescore(p,manifest,classes,sequence)
                rows.extend([{**v,'split_seed':split} for v in r]);pcs.extend([{**v,'split_seed':split} for v in pc])
                for f in [p,*p.parent.glob('*predictions.npz')]:hashes[str(f.relative_to(ROOT))]=scoring.digest(f)
    assert len(rows)==840
    frame=pd.concat([old,pd.DataFrame(rows)],ignore_index=True);frame.to_csv(OUT/'all_per_run_metrics.csv',index=False)
    pd.DataFrame(pcs).to_csv(OUT/'new_per_client_metrics.csv',index=False)
    keys=['split_seed','score_space','environment','method']
    seeds=frame.groupby(keys+['seed'])[METRICS].mean().reset_index();seeds.to_csv(OUT/'seed_order_averaged.csv',index=False)
    summary=seeds.groupby(keys)[METRICS].agg(['mean','std']);summary.columns=['_'.join(c) for c in summary.columns];summary.reset_index().to_csv(OUT/'summary.csv',index=False)
    orders=frame.groupby(keys+['order'])[METRICS].agg(['mean','std']);orders.columns=['_'.join(c) for c in orders.columns];orders.reset_index().to_csv(OUT/'per_order_summary.csv',index=False)
    pairs=[]
    for split in [42,*config['additional_split_seeds']]:
        comparisons=[('balanced_rare_60','class_balanced_60')]
        if split==42:comparisons += [('rare_random_60','protected_60'),('balanced_rare_60','rare_random_60'),('rare_random_60','class_balanced_60')]
        for space in ['merged_scans','original_type']:
            for env in config['environments']:
                for order in ['averaged',*config['orders']]:
                    source=seeds if order=='averaged' else frame[frame.order==order]
                    source=source[(source.split_seed==split)&(source.score_space==space)&(source.environment==env)]
                    for left,right in comparisons:
                        a=source[source.method==left].set_index('seed');b=source[source.method==right].set_index('seed')
                        assert set(a.index)==set(b.index)==set(config['seeds'])
                        for metric in METRICS:
                            d=(a[metric]-b[metric]).sort_index();d=d.mask(d.abs()<1e-12,0.);ci=paired_interval(d)
                            better=ci['ci95_high']<0 if metric=='forgetting' else ci['ci95_low']>0
                            worse=ci['ci95_low']>0 if metric=='forgetting' else ci['ci95_high']<0
                            pairs.append({'split_seed':split,'score_space':space,'environment':env,'order':order,'left':left,'right':right,'metric':metric,'outcome':'better' if better else 'worse' if worse else 'not significant',**ci})
    pd.DataFrame(pairs).to_csv(OUT/'paired_intervals.csv',index=False)
    # Preserve split as the reporting unit: no nominal t interval over correlated split replicates.
    p=pd.DataFrame(pairs);p=p[(p.order=='averaged')&(p.left=='balanced_rare_60')&(p.right=='class_balanced_60')]
    consistency=p.groupby(['score_space','environment','metric']).agg(splits=('split_seed','count'),positive_differences=('mean_difference',lambda v:int((v>0).sum())),negative_differences=('mean_difference',lambda v:int((v<0).sum())),significant_better=('outcome',lambda v:int((v=='better').sum())),significant_worse=('outcome',lambda v:int((v=='worse').sum())))
    consistency.reset_index().to_csv(OUT/'split_consistency.csv',index=False)
    save_json(OUT/'analysis_input_hashes.json',hashes)
    save_json(OUT/'analysis_protocol.json',{'new_evaluation_runs':420,'calibration_runs':132,'primary':'merged_scans','paired_interval_unit':'ten training-seed differences after averaging orders, separately for each split','split_independence_claimed':False,'selection_criterion_unchanged':True,'exploratory_tuned_model_excluded':True})
    print('Rescored 420 new runs in both score spaces; all splits/orders retained.')
if __name__=='__main__':main()
