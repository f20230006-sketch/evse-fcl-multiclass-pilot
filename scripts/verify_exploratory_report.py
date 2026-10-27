"""Independent merged-cohort/Slowloris statistics verification."""
from pathlib import Path
import ast
import hashlib
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.scan_final import SCAN_TYPES
OUT=ROOT/'outputs/exploratory_tuning_report_2026_10_27'

def main():
    assert json.loads((ROOT/'outputs/exploratory_tuning_2026_10_27/verification.json').read_text())['status']=='passed'
    frame=pd.read_csv(OUT/'all_per_run_metrics.csv');new=frame[frame.method.str.startswith('tuned_')]
    rows_checked=0;runs=0
    config=json.loads((ROOT/'configs/exploratory_tuning_2026_10_27.json').read_text())
    for order,sequence in config['orders'].items():
        split=ROOT/'outputs/multiclass_full_comparison/splits'/order
        manifest=pd.read_csv(split/'split_manifest.csv');mapping=json.loads((split/'class_mapping.json').read_text());names=sorted(mapping,key=mapping.get)
        merged=['Benign']+sorted((set(names)-set(SCAN_TYPES)-{'Benign'})|{'Scan'})
        to_new=np.array([merged.index('Scan' if c in SCAN_TYPES else c) for c in names]);best={}
        for path in (ROOT/'outputs/exploratory_tuning_2026_10_27/runs'/order).glob('*/*/seed_*/results.json'):
            r=json.loads(path.read_text());best={}
            for h in r['history']:
                with np.load(path.parent/f"checkpoint_{h['checkpoint']}_predictions.npz") as z:
                    idx=z['sample_index'];raw=z['probability'];truth=to_new[z['y_true']]
                q=np.zeros((len(idx),len(merged)),dtype=np.float64)
                for col in range(raw.shape[1]):q[:,to_new[col]]+=raw[:,col]
                pred=q.argmax(1);tasks=manifest.task.to_numpy()[idx];clients=manifest.client.to_numpy()[idx]
                accuracy={t:float((pred[tasks==t]==truth[tasks==t]).mean()) for t in h['tasks']}
                drops={t:max(0.,best.get(t,a)-a) for t,a in accuracy.items()}
                best={t:max(best.get(t,a),a) for t,a in accuracy.items()}
                rows_checked+=len(idx)
            expected={'old_task_accuracy':np.mean([accuracy[t] for t in sequence[:-1]]),'forgetting':np.mean([drops[t] for t in sequence[:-1]]),
                'slowloris_recall':np.mean(pred[truth==merged.index('Slowloris_Scan')]==merged.index('Slowloris_Scan'))}
            macros=[]
            for c in sorted(manifest.client.unique()):
                mask=clients==c;macros.append(np.mean([np.mean(pred[mask&(truth==label)]==label) for label in np.unique(truth[mask])]))
            expected['worst_client_macro_recall']=min(macros)
            record=new[(new.score_space=='merged_scans')&(new.order==order)&(new.environment==r['environment'])&(new.method==r['method'])&(new.seed==r['seed'])]
            assert len(record)==1
            for k,v in expected.items():assert np.isclose(record.iloc[0][k],v),k
            saved=OUT/'new_merged_results'/order/r['environment']/r['method']/f"seed_{r['seed']}"/'final_merged_predictions.npz'
            with np.load(saved) as z:
                assert np.array_equal(z['y_pred'],pred)
                assert np.allclose(z['probability'],q,atol=1e-12)
            runs+=1
    assert runs==180
    metrics=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
    for p in (OUT/'paired_intervals.csv',):
        intervals=pd.read_csv(p)
        for _,r in intervals.iterrows():
            f=frame[(frame.score_space==r.score_space)&(frame.environment==r.environment)]
            if r.order!='averaged':f=f[f.order==r.order]
            f=f.groupby(['method','seed'])[metrics].mean().reset_index()
            left=f[f.method==r.left].set_index('seed')[r.metric];right=f[f.method==r.right].set_index('seed')[r.metric]
            d=(left-right).sort_index().to_numpy(copy=True);d[np.abs(d)<1e-12]=0;assert len(d)==10
            half=2.2621571628*np.std(d,ddof=1)/np.sqrt(10)
            assert np.allclose([r.mean_difference,r.ci95_low,r.ci95_high],[d.mean(),d.mean()-half,d.mean()+half])
    for relative,digest in json.loads((OUT/'analysis_input_hashes.json').read_text()).items():
        with (ROOT/relative).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==digest
    report={'status':'passed','new_runs':runs,'merged_checkpoint_rows':rows_checked,'paired_intervals_checked':len(intervals),'exploratory':True,'original_inputs_preserved':True,'merged_probabilities_and_slowloris_verified':True}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
