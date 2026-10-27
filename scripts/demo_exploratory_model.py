"""Offline inference example; deterministic rows, not a live IDS or new test."""
from pathlib import Path
import argparse,json,sys
import numpy as np
import pandas as pd
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from evse_ids.exploratory_tuning import TunedMLP
from evse_ids.scan_final import scan_mapping,merge_probabilities

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order',default='order_1',choices=['order_1','order_2','order_3'])
    parser.add_argument('--environment',default='federated',choices=['federated','centralized'])
    parser.add_argument('--method',default='tuned_balanced_rare_60',choices=['tuned_class_balanced_60','tuned_protected_60','tuned_balanced_rare_60'])
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--output',default='outputs/exploratory_tuning_report_2026_10_27/demo_predictions.csv')
    args=parser.parse_args();torch.set_num_threads(1)
    run=ROOT/'outputs/exploratory_tuning_2026_10_27/runs'/args.order/args.environment/args.method/f'seed_{args.seed}'
    assert (run/'complete.json').exists()
    record=json.loads((run/'results.json').read_text());settings=record['settings']
    split=ROOT/'outputs/multiclass_full_comparison/splits'/args.order;manifest=pd.read_csv(split/'split_manifest.csv')
    data=torch.load(split/'prepared_local_only.pt',weights_only=False,map_location='cpu')
    names,mapping=scan_mapping(data['classes']);evaluation=manifest[manifest.persistent_role=='evaluation']
    # First available row for each merged true class, fixed without inspecting predictions.
    indices=np.array([evaluation[evaluation.class_id.map(lambda c:mapping[c])==i].sample_index.min() for i in range(len(names))],dtype=int)
    model=TunedMLP(data['x'].shape[1],len(data['classes']),settings['hidden_sizes'],settings['dropout']);model.load_state_dict(torch.load(run/'final_model.pt',weights_only=True));model.eval()
    with torch.no_grad():probability=torch.softmax(model(data['x'][indices]),1).numpy()
    merged=merge_probabilities(probability,mapping,len(names));pred=merged.argmax(1);truth=mapping[data['y'][indices].numpy()]
    frame=pd.DataFrame({'sample_index':indices,'client':manifest.client.to_numpy()[indices],'actual':[names[i] for i in truth],'predicted':[names[i] for i in pred],'uncalibrated_max_probability':merged.max(1),'correct':pred==truth})
    target=ROOT/args.output;target.parent.mkdir(parents=True,exist_ok=True);frame.to_csv(target,index=False)
    print(frame.to_string(index=False));print('\nOffline illustrative predictions only; ten examples do not estimate accuracy or establish deployment readiness.')

if __name__=='__main__':main()
