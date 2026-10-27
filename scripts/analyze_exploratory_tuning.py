"""Score all tuned models and show frozen and matched-baseline comparisons."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'src'))
import analyze_balanced_rare_final as original
from evse_ids.scan_final import paired_interval
OUT=ROOT/'outputs/exploratory_tuning_report_2026_10_27'
METRICS=original.METRICS

def main():
    OUT.mkdir(parents=True,exist_ok=True);original.OUT=OUT
    experiment=ROOT/'outputs/exploratory_tuning_2026_10_27';config=json.loads((experiment/'protocol_before_evaluation.json').read_text())['config']
    assert json.loads((experiment/'completion.json').read_text())['evaluation_runs']==180
    data=[];clients=[];sources={};compute=[]
    for order,sequence in config['orders'].items():
        split=ROOT/config['reference_output']/'splits'/order;manifest=pd.read_csv(split/'split_manifest.csv');mapping=json.loads((split/'class_mapping.json').read_text());classes=sorted(mapping,key=mapping.get)
        for path in (experiment/'runs'/order).glob('*/*/seed_*/results.json'):
            rows,local=original.rescore(path,manifest,classes,sequence);data.extend(rows);clients.extend(local)
            for p in [path,*path.parent.glob('*predictions.npz')]:sources[str(p.relative_to(ROOT))]=original.digest(p)
            logpath=path.parent/'training_log.json';sources[str(logpath.relative_to(ROOT))]=original.digest(logpath)
            record=json.loads(path.read_text());log=json.loads(logpath.read_text())
            compute.append({'order':order,'environment':record['environment'],'method':record['method'],'seed':record['seed'],'replay_fraction':record['settings']['replay_fraction'],'optimizer_steps':sum(r['steps'] for r in log),'elapsed_seconds':record['elapsed_seconds']})
    assert len(data)==360
    pd.DataFrame(compute).to_csv(OUT/'new_training_compute.csv',index=False)
    frame=pd.DataFrame(data);frame.to_csv(OUT/'new_per_run_metrics.csv',index=False);pd.DataFrame(clients).to_csv(OUT/'new_per_client_metrics.csv',index=False)
    old=ROOT/'outputs/balanced_rare_report/all_per_run_metrics.csv';frame=pd.concat([pd.read_csv(old),frame],ignore_index=True);sources[str(old.relative_to(ROOT))]=original.digest(old)
    frame.to_csv(OUT/'all_per_run_metrics.csv',index=False)
    seed=frame.groupby(['score_space','environment','method','seed'])[METRICS].mean().reset_index();seed.to_csv(OUT/'seed_order_averaged.csv',index=False)
    summary=seed.groupby(['score_space','environment','method'])[METRICS].agg(['mean','std']);summary.columns=['_'.join(c) for c in summary.columns];summary.reset_index().to_csv(OUT/'summary.csv',index=False)
    order=frame.groupby(['score_space','environment','method','order'])[METRICS].agg(['mean','std']);order.columns=['_'.join(c) for c in order.columns];order.reset_index().to_csv(OUT/'per_order_summary.csv',index=False)
    comparisons=[('tuned_class_balanced_60','class_balanced_60','overall pipeline'),('tuned_protected_60','protected_60','overall pipeline'),('tuned_balanced_rare_60','balanced_rare_60','overall pipeline'),('tuned_balanced_rare_60','tuned_class_balanced_60','matched backbone'),('tuned_balanced_rare_60','tuned_protected_60','matched backbone'),('tuned_balanced_rare_60','class_balanced_60','overall pipeline'),('tuned_balanced_rare_60','protected_60','overall pipeline')]
    rows=[]
    for space in ['merged_scans','original_type']:
        for environment in config['environments']:
            for o in ['averaged',*config['orders']]:
                part=seed if o=='averaged' else frame[frame.order==o];part=part[(part.score_space==space)&(part.environment==environment)]
                for left,right,interpretation in comparisons:
                    a=part[part.method==left].set_index('seed');b=part[part.method==right].set_index('seed')
                    assert set(a.index)==set(b.index)==set(config['seeds'])
                    for metric in METRICS:
                        d=(a[metric]-b[metric]).sort_index();d=d.mask(d.abs()<1e-12,0.);ci=paired_interval(d)
                        outcome='better' if (ci['ci95_high']<0 if metric=='forgetting' else ci['ci95_low']>0) else 'worse' if (ci['ci95_low']>0 if metric=='forgetting' else ci['ci95_high']<0) else 'not significant'
                        rows.append({'score_space':space,'environment':environment,'order':o,'left':left,'right':right,'interpretation':interpretation,'metric':metric,'outcome':outcome,**ci})
    pd.DataFrame(rows).to_csv(OUT/'paired_intervals.csv',index=False)
    (OUT/'analysis_input_hashes.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
    print('All 180 tuned cases scored; frozen and matched comparisons written.',flush=True)

if __name__=='__main__':main()
