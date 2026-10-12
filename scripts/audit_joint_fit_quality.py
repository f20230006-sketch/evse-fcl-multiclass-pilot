"""Post-hoc fitting/calibration/evaluation diagnostics of frozen joint models."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.multiclass_pilot import TrafficMLP,predict

def main():
    torch.set_num_threads(1);base=ROOT/'outputs/multiclass_full_comparison';out=ROOT/'outputs/joint_diagnostics';rows=[]
    for order in ['order_1','order_2','order_3']:
        data=torch.load(base/'splits'/order/'prepared_local_only.pt',weights_only=False,map_location='cpu')
        for path in sorted((base/'runs'/order).glob('*/joint/seed_*/results.json')):
            r=json.loads(path.read_text());model=TrafficMLP(data['x'].shape[1],len(data['classes']));model.load_state_dict(torch.load(path.parent/'final_model.pt',weights_only=True));model.eval()
            for role in ['fitting','calibration','evaluation']:
                ids=np.flatnonzero(data['roles']==role);prob=predict(model,data['x'],ids,list(range(len(data['classes']))));y=data['y'][ids].numpy();pred=prob.argmax(1)
                rows.append({'order':order,'environment':r['environment'],'seed':r['seed'],'role':role,'rows':len(ids),'all_type_accuracy':float((y==pred).mean()),'macro_type_recall':float(np.mean([np.mean(pred[y==c]==c) for c in np.unique(y)])),'cross_entropy':float(-np.log(np.maximum(prob[np.arange(len(y)),y],1e-30)).mean())})
    f=pd.DataFrame(rows);f.to_csv(out/'joint_fit_calibration_evaluation_quality.csv',index=False)
    s=f.groupby(['environment','role'])[['all_type_accuracy','macro_type_recall','cross_entropy']].mean().reset_index();s.to_csv(out/'joint_fit_quality_summary.csv',index=False)
    lines=['# Joint model fit quality','','Frozen final models are diagnosed after the study; no hyperparameters or training labels were changed. These all-type micro accuracies differ from the old-task macro accuracy in the original summary.','','| Environment | Role | All-type accuracy | Macro type recall | Cross entropy |','|---|---|---:|---:|---:|']
    for _,r in s.iterrows():lines.append(f'| {r.environment} | {r.role} | {100*r.all_type_accuracy:.2f}% | {100*r.macro_type_recall:.2f}% | {r.cross_entropy:.3f} |')
    lines+=['','Compare fitting and evaluation performance before attributing the result to generalization. Low fitting accuracy shows that the existing small-MLP/training protocol also struggles on its training examples; it does not prove irreducible type ambiguity. Confusion matrices locate the affected types. The separate exact-feature audit finds virtually no cross-type byte-identical features, so it does not establish an intrinsic 55% ceiling. More optimization/capacity or alternate-feature studies would require a new calibration-only protocol rather than retroactively changing this published reference.']
    (out/'JOINT_FIT_QUALITY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(s.to_string(index=False))

if __name__=='__main__':main()
