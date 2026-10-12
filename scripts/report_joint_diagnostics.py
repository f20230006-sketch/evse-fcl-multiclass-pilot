"""Joint confusion evidence and prespecified family-level re-scoring; no label merging."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.append(str(ROOT/'work/followup_plot_dependencies'))
from evse_ids.multiclass_pilot import TASKS

def main():
    base=ROOT/'outputs/multiclass_full_comparison';out=ROOT/'outputs/joint_diagnostics';out.mkdir(parents=True,exist_ok=True)
    pairs=[];class_rows=[];run_rows=[];loss_rows=[];matrices={}
    for order in ['order_1','order_2','order_3']:
        mapping=json.loads((base/'splits'/order/'class_mapping.json').read_text());names=sorted(mapping,key=mapping.get)
        for env in ['federated','centralized']:
            counts=[]
            for path in sorted((base/'runs'/order/env/'joint').glob('seed_*/results.json')):
                result=json.loads(path.read_text());pred=np.load(path.parent/'checkpoint_4_predictions.npz')
                y,p=pred['y_true'],pred['y_pred'];cm=np.zeros((len(names),len(names)),dtype=int);np.add.at(cm,(y,p),1);counts.append(cm)
                key={'order':order,'environment':env,'seed':result['seed']}
                run_rows.append({**key,'all_type_accuracy':float((y==p).mean()),'all_attack_type_accuracy':float((y[y!=0]==p[y!=0]).mean()),'old_task_accuracy':result['summary']['old_task_accuracy'],'calibration_macro_recall':result['selection_score']})
                for i,name in enumerate(names):
                    support=int(cm[i].sum());recall=cm[i,i]/support if support else None
                    class_rows.append({**key,'class':name,'support':support,'recall':recall})
                    for j,target in enumerate(names):
                        if i!=j and cm[i,j]:pairs.append({**key,'true_class':name,'predicted_class':target,'errors':int(cm[i,j]),'support':support,'confusion_fraction':cm[i,j]/support})
                logs=json.loads((path.parent/'training_log.json').read_text())
                for l in logs:loss_rows.append({**key,'round':l['round'],'client':l['client'],'first_epoch_loss':l['epoch_losses'][0],'last_epoch_loss':l['epoch_losses'][-1],'steps':l['steps']})
            counts=np.stack(counts);total=counts.sum(0);norm=np.divide(total,total.sum(1,keepdims=True),out=np.zeros_like(total,dtype=float),where=total.sum(1,keepdims=True)>0)
            prefix=f'{env}_{order}'
            pd.DataFrame(total,index=names,columns=names).rename_axis('true_class').to_csv(out/f'{prefix}_confusion_counts.csv')
            pd.DataFrame(norm,index=names,columns=names).rename_axis('true_class').to_csv(out/f'{prefix}_confusion_row_normalized.csv')
            matrices[(env,order)]=total
    for env in ['federated','centralized']:
        total=sum(matrices[(env,o)] for o in ['order_1','order_2','order_3']);norm=total/total.sum(1,keepdims=True)
        pd.DataFrame(total,index=names,columns=names).rename_axis('true_class').to_csv(out/f'{env}_confusion_counts.csv')
        pd.DataFrame(norm,index=names,columns=names).rename_axis('true_class').to_csv(out/f'{env}_confusion_row_normalized.csv')
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(12,10));im=ax.imshow(norm,vmin=0,vmax=1,cmap='Blues');ax.set_xticks(range(len(names)),names,rotation=70,ha='right');ax.set_yticks(range(len(names)),names);ax.set_xlabel('Predicted attack type');ax.set_ylabel('True attack type');ax.set_title(f'Joint training: {env}\nRow-normalized, 10 seeds × 3 orders (same evaluation rows repeated)')
        for i in range(len(names)):
            for j in range(len(names)):
                if norm[i,j]>=.05:ax.text(j,i,f'{norm[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if norm[i,j]>.5 else 'black')
        fig.colorbar(im,ax=ax,label='Fraction of true-class observations');fig.tight_layout();fig.savefig(out/f'{env}_confusion.png',dpi=160);fig.savefig(out/f'{env}_confusion.pdf');plt.close(fig)
    frame=pd.DataFrame(pairs);frame.to_csv(out/'confused_pairs_per_run.csv',index=False)
    # Add zero rates for every seed/order before measuring consistency.
    all_pairs=[]
    for env in ['federated','centralized']:
        for i,name in enumerate(names):
            for j,target in enumerate(names):
                if i==j:continue
                values=[]
                for order in ['order_1','order_2','order_3']:
                    for seed in range(42,52):
                        r=frame[(frame.environment==env)&(frame.order==order)&(frame.seed==seed)&(frame.true_class==name)&(frame.predicted_class==target)]
                        values.append(float(r.confusion_fraction.iloc[0]) if len(r) else 0.)
                all_pairs.append({'environment':env,'true_class':name,'predicted_class':target,'mean_confusion_fraction':np.mean(values),'min_fraction':min(values),'max_fraction':max(values),'runs_at_least_10pct':sum(v>=.1 for v in values),'runs':30})
    p=pd.DataFrame(all_pairs).sort_values(['environment','mean_confusion_fraction'],ascending=[True,False]);p.to_csv(out/'confused_pairs_consistency.csv',index=False)
    pd.DataFrame(class_rows).to_csv(out/'per_class_per_run.csv',index=False);pd.DataFrame(run_rows).to_csv(out/'joint_accuracy_per_run.csv',index=False);pd.DataFrame(loss_rows).to_csv(out/'joint_training_losses.csv',index=False)
    lines=['# Joint-training confusion diagnosis','','The original ~55% figure is old-task type accuracy averaged over three tasks; it is not the same quantity as single-task pilot accuracy or all-class accuracy. Single-task near-99% values came from selected easier tasks, not all 15 types.','','Matrices use final predictions from all 60 existing joint runs. Rows=true, columns=predicted. Counts repeat the fixed evaluation observations across 10 seeds and three orders; they are not independent traffic samples. Row-normalized matrices summarize training randomness. No training labels were merged and no settings were selected using these evaluation results.','']
    for env in ['federated','centralized']:
        r=pd.DataFrame(run_rows);r=r[r.environment==env]
        lines += [f'## {env}',f'All-type accuracy mean: {100*r.all_type_accuracy.mean():.2f}%; all-attack type accuracy: {100*r.all_attack_type_accuracy.mean():.2f}%; old-task accuracy: {100*r.old_task_accuracy.mean():.2f}%.','',f'![Confusion matrix]({env}_confusion.png)','','| True type | Predicted type | Mean confused | Runs with ≥10% confusion |','|---|---|---:|---:|']
        for _,row in p[(p.environment==env)&(p.mean_confusion_fraction>=.1)].head(15).iterrows():lines.append(f'| {row.true_class} | {row.predicted_class} | {100*row.mean_confusion_fraction:.1f}% | {row.runs_at_least_10pct}/30 |')
    lines+=['','## Interpretation','Consistent confusion is evidence of errors under this model/training protocol, not proof that types are intrinsically indistinguishable. The frozen Task-1 representation, model capacity, optimization budget, federated client heterogeneity and class support can also limit joint performance. Training-loss traces are supplied for inspection; no single cause is asserted. Family-level scoring uses the already-defined four task groups, without retraining or choosing merged groups from evaluation errors. Supervisor review of these matrices precedes any future merged-label experiment.']
    (out/'JOINT_CONFUSION_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'joint_runs':len(run_rows),'output':str(out)},indent=2))

if __name__=='__main__':main()
