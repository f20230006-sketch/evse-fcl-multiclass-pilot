"""Exact feature-vector conflicts in frozen representations; diagnostic oracle only."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.multiclass_pilot import TASKS

def main():
    base=ROOT/'outputs/multiclass_full_comparison';out=ROOT/'outputs/joint_diagnostics'
    summaries=[];conflicts=[];family_names=['Benign',*TASKS]
    for order in ['order_1','order_2','order_3']:
        data=torch.load(base/'splits'/order/'prepared_local_only.pt',weights_only=False,map_location='cpu')
        for role in ['fitting','calibration','evaluation']:
            mask=data['roles']==role;x=np.ascontiguousarray(data['x'].numpy()[mask]);y=data['y'].numpy()[mask]
            _,inverse=np.unique(x.view(np.dtype((np.void,x.dtype.itemsize*x.shape[1]))).ravel(),return_inverse=True)
            counts=np.zeros((inverse.max()+1,len(data['classes'])),dtype=int);np.add.at(counts,(inverse,y),1)
            shared=(counts>0).sum(1)>1;ambiguous_rows=counts[shared].sum();ceiling=counts.max(1).sum()/len(y)
            tofamily=[0 if n=='Benign' else next(family_names.index(k) for k,v in TASKS.items() if n in v) for n in data['classes']]
            fc=np.column_stack([counts[:,np.array(tofamily)==i].sum(1) for i in range(len(family_names))]);family_ceiling=fc.max(1).sum()/len(y)
            summaries.append({'order':order,'role':role,'rows':len(y),'distinct_feature_vectors':len(counts),'vectors_with_multiple_types':int(shared.sum()),'rows_in_conflicting_vectors':int(ambiguous_rows),'oracle_type_accuracy_ceiling':ceiling,'oracle_family_accuracy_ceiling':family_ceiling})
            for i,name in enumerate(data['classes']):
                for j,target in enumerate(data['classes']):
                    if j<=i:continue
                    overlap=(counts[:,i]>0)&(counts[:,j]>0)
                    if overlap.any():conflicts.append({'order':order,'role':role,'class_a':name,'class_b':target,'shared_identical_vectors':int(overlap.sum()),'class_a_rows_in_shared_vectors':int(counts[overlap,i].sum()),'class_b_rows_in_shared_vectors':int(counts[overlap,j].sum())})
    frame=pd.DataFrame(summaries);frame.to_csv(out/'exact_feature_conflict_summary.csv',index=False);pd.DataFrame(conflicts).to_csv(out/'exact_feature_conflict_pairs.csv',index=False)
    lines=['# Exact feature-vector ambiguity audit','','This diagnostic groups byte-identical float32 feature vectors after the original frozen preprocessing. For each persistent role separately, the oracle assigns the most common label to each exact vector. Its accuracy is a same-role, in-sample maximum for deterministic classification using these features, not a trained model, held-out estimate, tuning signal or attainable generalization target. It uses labels only for diagnosis; no model or label grouping is changed. Conflicts may be inherent in the supplied flows or induced by clipping/unknown-category handling; this audit does not distinguish those causes.','','| Order | Role | Rows | Distinct vectors | Rows sharing a vector with another type | Oracle type ceiling | Oracle family ceiling |','|---|---|---:|---:|---:|---:|---:|']
    for r in summaries:lines.append(f"| {r['order']} | {r['role']} | {r['rows']} | {r['distinct_feature_vectors']} | {r['rows_in_conflicting_vectors']} | {100*r['oracle_type_accuracy_ceiling']:.2f}% | {100*r['oracle_family_accuracy_ceiling']:.2f}% |")
    lines+=['','This ceiling is micro accuracy over all samples, so compare it with joint all-type accuracy, not old-task macro accuracy. It does not establish a ceiling for a different feature extractor or merged-label retraining. Inspect the paired CSV to locate specific overlapping types.']
    (out/'FEATURE_AMBIGUITY_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(frame.to_string(index=False))

if __name__=='__main__':main()
