"""Published population baseline, both reporting views and all paired outcomes."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'src')]
import numpy as np
import pandas as pd
import analyze_balanced_rare_final as scoring
from evse_ids.scan_final import paired_interval
from evse_ids.multiclass_pilot import save_json
OUT=ROOT/'outputs/cbrs_report_2026_10_28';METRICS=scoring.METRICS
def main():
    OUT.mkdir(exist_ok=True,parents=True);scoring.OUT=OUT;run=ROOT/'outputs/cbrs_comparison_2026_10_28'
    c=json.loads((run/'protocol_before_evaluation.json').read_text())['config'];assert json.loads((run/'completion.json').read_text())['evaluation_runs']==60
    base=ROOT/'outputs/balanced_rare_report/all_per_run_metrics.csv';old=pd.read_csv(base)
    # Retain all accepted comparators for the updated main table and capacity evidence.
    records=[];clients=[];hashes={str(base.relative_to(ROOT)):scoring.digest(base)}
    for order,sequence in c['orders'].items():
        split=ROOT/'outputs/multiclass_full_comparison/splits'/order;manifest=pd.read_csv(split/'split_manifest.csv');mapping=json.loads((split/'class_mapping.json').read_text());classes=sorted(mapping,key=mapping.get)
        for p in sorted((run/'runs'/order).glob('*/*/seed_*/results.json')):
            rows,pc=scoring.rescore(p,manifest,classes,sequence);records.extend(rows);clients.extend(pc)
            for f in [p,*p.parent.glob('*predictions.npz')]:hashes[str(f.relative_to(ROOT))]=scoring.digest(f)
    assert len(records)==120
    frame=pd.concat([old,pd.DataFrame(records)],ignore_index=True);frame.to_csv(OUT/'all_per_run_metrics.csv',index=False);pd.DataFrame(clients).to_csv(OUT/'cbrs_per_client_metrics.csv',index=False)
    seeds=frame.groupby(['score_space','environment','method','seed'])[METRICS].mean().reset_index();seeds.to_csv(OUT/'seed_order_averaged.csv',index=False)
    summary=seeds.groupby(['score_space','environment','method'])[METRICS].agg(['mean','std']);summary.columns=['_'.join(x) for x in summary.columns];summary.reset_index().to_csv(OUT/'summary.csv',index=False)
    orders=frame.groupby(['score_space','environment','method','order'])[METRICS].agg(['mean','std']);orders.columns=['_'.join(x) for x in orders.columns];orders.reset_index().to_csv(OUT/'per_order_summary.csv',index=False)
    pairs=[]
    for space in ['merged_scans','original_type']:
        for env in c['environments']:
            for order in ['averaged',*c['orders']]:
                f=seeds if order=='averaged' else frame[frame.order==order];f=f[(f.score_space==space)&(f.environment==env)]
                a=f[f.method=='balanced_rare_60'].set_index('seed');b=f[f.method=='cbrs_60'].set_index('seed');assert set(a.index)==set(b.index)==set(c['seeds'])
                for metric in METRICS:
                    d=(a[metric]-b[metric]).sort_index();d=d.mask(d.abs()<1e-12,0);ci=paired_interval(d)
                    better=ci['ci95_high']<0 if metric=='forgetting' else ci['ci95_low']>0;worse=ci['ci95_low']>0 if metric=='forgetting' else ci['ci95_high']<0
                    pairs.append({'score_space':space,'environment':env,'order':order,'left':'balanced_rare_60','right':'cbrs_60','metric':metric,'outcome':'better' if better else 'worse' if worse else 'not significant',**ci})
    pd.DataFrame(pairs).to_csv(OUT/'paired_intervals.csv',index=False)
    save_json(OUT/'analysis_input_hashes.json',hashes);save_json(OUT/'analysis_protocol.json',{'new_evaluation_runs':60,'primary':'merged_scans','comparison':'RBR minus CBRS','seed_unit':'ten training seeds, orders averaged within each seed; per-order intervals also retained','all_losses_retained':True,'original_split':42,'prior_outputs_preserved':True})
    print('Sixty CBRS runs scored in both views; 64 paired intervals.')
if __name__=='__main__':main()
