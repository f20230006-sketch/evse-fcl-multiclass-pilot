"""Paired seed/order comparisons and prespecified family scoring from saved predictions."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.append(str(ROOT/'work/followup_plot_dependencies'))
from evse_ids.multiclass_pilot import TASKS,metrics
CORE=['old_task_accuracy','forgetting','rare_attack_recall','worst_client_macro_recall']
EXTRA=['false_alarm_rate','accuracy','attack_accuracy','macro_recall','auroc_macro_ovr','auprc_macro_ovr_average_precision']

def contrast(frame,left,right,label,order='averaged'):
    joined=frame[frame.method==left].set_index('seed')[CORE].join(frame[frame.method==right].set_index('seed')[CORE],lsuffix='_left',rsuffix='_right',how='inner')
    assert len(joined)==10 and joined.index.is_unique,(label,order,len(joined))
    rows=[]
    for m in CORE:
        d=(joined[m+'_left']-joined[m+'_right']).dropna();assert len(d)==10
        mean=float(d.mean());sd=float(d.std(ddof=1));half=2.2621571628*sd/np.sqrt(10)
        rows.append({'order':order,'contrast':label,'metric':m,'n_seed_pairs':10,'mean_difference':mean,'ci95_low':mean-half,'ci95_high':mean+half})
    return rows

def family_scores(path,base,config):
    r=json.loads(path.read_text());order=path.parents[3].name
    manifest=pd.read_csv(base/'splits'/order/'split_manifest.csv')
    names=sorted(json.loads((base/'splits'/order/'class_mapping.json').read_text()),key=lambda n:json.loads((base/'splits'/order/'class_mapping.json').read_text())[n])
    families=['Benign',*TASKS];tofamily=np.array([0 if n=='Benign' else next(families.index(k) for k,v in TASKS.items() if n in v) for n in names])
    best={};hard_best={};history=[]
    clients=manifest.client.to_numpy()
    for h in r['history']:
        p=np.load(path.parent/f"checkpoint_{h['checkpoint']}_predictions.npz")
        prob=np.column_stack([p['probability'][:,tofamily==i].sum(1) for i in range(len(families))]);y=tofamily[p['y_true']];pred=prob.argmax(1)
        hard=tofamily[p['y_pred']];seen=sorted(set(tofamily[h['seen_classes']].tolist()))
        m=metrics(y,prob,families,seen);local=clients[p['sample_index']]
        taskvals={};drops={};hardvals={};harddrops={}
        for task in h['tasks']:
            k=families.index(task);mask=y==k;acc=float((pred[mask]==y[mask]).mean());taskvals[task]=acc;drops[task]=max(0.,best.get(task,acc)-acc);best[task]=max(best.get(task,acc),acc)
            hardacc=float((hard[mask]==y[mask]).mean());hardvals[task]=hardacc;harddrops[task]=max(0.,hard_best.get(task,hardacc)-hardacc);hard_best[task]=max(hard_best.get(task,hardacc),hardacc)
        supported=[float(np.mean([np.mean(pred[(local==c)&(y==k)]==k) for k in np.unique(y[local==c])])) for c in np.unique(local)]
        hard_supported=[float(np.mean([np.mean(hard[(local==c)&(y==k)]==k) for k in np.unique(y[local==c])])) for c in np.unique(local)]
        rare=y==families.index('low_rate_rare')
        values={'checkpoint':h['checkpoint'],'accuracy':m['accuracy'],'attack_accuracy':m['attack_accuracy'],'macro_recall':m['macro_recall'],'auroc_macro_ovr':m['auroc_macro_ovr'],'auprc_macro_ovr_average_precision':m['auprc_macro_ovr_average_precision'],'rare_attack_recall':float((pred[rare]==y[rare]).mean()) if rare.any() else None,'worst_client_macro_recall':min(supported),'task_accuracy':taskvals,'task_forgetting':drops,'mapped_type_prediction_accuracy':float((hard==y).mean())}
        values.update({'mapped_old_task_accuracy':float(np.mean([hardvals[t] for t in h['tasks'] if t in config['orders'][order][:-1]])) if any(t in config['orders'][order][:-1] for t in h['tasks']) else None,'mapped_rare_attack_recall':float((hard[rare]==y[rare]).mean()) if rare.any() else None,'mapped_worst_client_macro_recall':min(hard_supported),'mapped_task_accuracy':hardvals,'mapped_task_forgetting':harddrops})
        history.append(values)
    old=config['orders'][order][:-1];last=history[-1]
    return {**{k:last[k] for k in CORE+EXTRA if k in last},'old_task_accuracy':float(np.mean([last['task_accuracy'][t] for t in old])),'forgetting':None if r['method']=='joint' else float(np.mean([last['task_forgetting'][t] for t in old])),'mapped_type_prediction_accuracy':last['mapped_type_prediction_accuracy'],'mapped_old_task_accuracy':last['mapped_old_task_accuracy'],'mapped_forgetting':None if r['method']=='joint' else float(np.mean([last['mapped_task_forgetting'][t] for t in old])),'mapped_rare_attack_recall':last['mapped_rare_attack_recall'],'mapped_worst_client_macro_recall':last['mapped_worst_client_macro_recall']},history

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--essential-only',action='store_true');parser.add_argument('--family',action='store_true');args=parser.parse_args()
    base=ROOT/'outputs/multiclass_full_comparison';config=json.loads((base/'protocol_before_evaluation.json').read_text())['config']
    out=ROOT/'outputs/replay_followup_report';out.mkdir(parents=True,exist_ok=True)
    roots=[base,ROOT/'outputs/replay_followup_essential']+([] if args.essential_only else [ROOT/'outputs/replay_followup_sweep'])
    rows=[];client_rows=[];class_rows=[];checkpoint_rows=[];family_rows=[];family_checkpoints=[]
    for root in roots:
        expected=420 if root==base else 60 if root.name.endswith('essential') else 360
        paths=sorted((root/'runs').glob('*/*/*/seed_*/results.json'));assert len(paths)==expected,(root,len(paths),expected)
        assert json.loads((root/'completion.json').read_text())['status']=='complete'
        for path in paths:
            r=json.loads(path.read_text());key={'order':path.parents[3].name,'environment':r['environment'],'method':r['method'],'seed':r['seed']}
            rows.append({**key,**r['summary']})
            for client,values in r['per_client_summary'].items():client_rows.append({**key,'client':client,**values})
            for h in r['history']:
                checkpoint_rows.append({**key,'checkpoint':h['checkpoint'],'client':'pooled',**{k:v for k,v in h['pooled'].items() if k!='per_class'}})
                for client,values in h['per_client'].items():checkpoint_rows.append({**key,'checkpoint':h['checkpoint'],'client':client,**{k:v for k,v in values.items() if k!='per_class'}})
            for pc in r['history'][-1]['pooled']['per_class']:class_rows.append({**key,'client':'pooled',**pc})
            for client,values in r['history'][-1]['per_client'].items():
                for pc in values['per_class']:class_rows.append({**key,'client':client,**pc})
            if args.family:
                values,history=family_scores(path,base,config);family_rows.append({**key,**values})
                for h in history:family_checkpoints.append({**key,**h})
    frame=pd.DataFrame(rows);frame.to_csv(out/'all_type_per_run_metrics.csv',index=False)
    pd.DataFrame(client_rows).to_csv(out/'all_type_per_client_per_run_metrics.csv',index=False)
    clients=pd.DataFrame(client_rows);client_metrics=[m for m in CORE+EXTRA if m in clients]
    cs=clients.groupby(['environment','method','client','seed'])[client_metrics].mean().groupby(['environment','method','client']).agg(['mean','std']);cs.columns=['_'.join(x) for x in cs.columns];cs.reset_index().to_csv(out/'all_type_per_client_summary.csv',index=False)
    pd.DataFrame(class_rows).to_csv(out/'all_type_per_class_metrics.csv',index=False)
    pd.DataFrame(checkpoint_rows).to_csv(out/'all_type_checkpoint_metrics.csv',index=False)
    seed=frame.groupby(['environment','method','seed'])[CORE+EXTRA].mean().reset_index();seed.to_csv(out/'type_per_seed_order_averaged.csv',index=False)
    summary=seed.groupby(['environment','method'])[CORE+EXTRA].agg(['mean','std']);summary.columns=['_'.join(x) for x in summary.columns];summary=summary.reset_index();summary.to_csv(out/'type_summary.csv',index=False)
    order_summary=frame.groupby(['order','environment','method'])[CORE].agg(['mean','std']);order_summary.columns=['_'.join(x) for x in order_summary.columns];order_summary.reset_index().to_csv(out/'type_per_order_summary.csv',index=False)
    pairs=[];sizes=[60] if args.essential_only else [60,120,300]
    for env in config['environments']:
        for n in sizes:
            for baseline in ['uniform','class_balanced']:
                left,right=f'protected_{n}',f'{baseline}_{n}'
                pairs+=contrast(seed[seed.environment==env],left,right,f'{env} {left}_minus_{right}')
                for order in config['orders']:
                    pairs+=contrast(frame[(frame.environment==env)&(frame.order==order)],left,right,f'{env} {left}_minus_{right}',order)
        for method in ['ewc','agem']:
            pairs+=contrast(seed[seed.environment==env],'protected_60',method,f'{env} protected_60_minus_{method}')
    pd.DataFrame(pairs).to_csv(out/'paired_intervals.csv',index=False)
    lines=['# Follow-up replay results','','All values are percentages; paired differences are percentage points. Three orders are averaged within each of ten training seeds before pooled intervals. Per-order intervals use ten matched seeds. Intervals describe training randomness on one fixed split, are unadjusted for multiple comparisons, and do not represent independent capture uncertainty.','','Memory sizes 60/120/300 mean slots per federated client. Centralized totals are 300/600/1500, matching the five-client system budget. Original 60-slot uniform/protected and other-method evidence is reused exactly, not retrained.','','## Type-level summary','','| Environment | Method | Old accuracy | Forgetting | Rare recall | Worst-client macro recall |','|---|---|---:|---:|---:|---:|']
    for _,r in summary.iterrows():
        lines.append('| '+' | '.join([r.environment,r.method]+['N/A' if pd.isna(r[m+'_mean']) else f"{100*r[m+'_mean']:.2f}" for m in CORE])+' |')
    lines+=['','## Paired comparisons, including each attack order','','Difference = protected minus comparison. Higher old accuracy/recall is favorable; lower forgetting is favorable.','','| Environment/method contrast | Order | Metric | Difference | 95% interval |','|---|---|---|---:|---|']
    for r in pairs:lines.append(f"| {r['contrast']} | {r['order']} | {r['metric']} | {100*r['mean_difference']:.2f} | [{100*r['ci95_low']:.2f}, {100*r['ci95_high']:.2f}] |")
    if args.family:
        f=pd.DataFrame(family_rows);f.to_csv(out/'family_per_run_metrics.csv',index=False);pd.DataFrame(family_checkpoints).to_json(out/'family_checkpoint_metrics.json',orient='records',indent=2)
        s=f.groupby(['environment','method','seed'])[CORE+['accuracy','attack_accuracy','macro_recall','auroc_macro_ovr','auprc_macro_ovr_average_precision','mapped_type_prediction_accuracy','mapped_old_task_accuracy','mapped_forgetting','mapped_rare_attack_recall','mapped_worst_client_macro_recall']].mean().reset_index();s.to_csv(out/'family_per_seed_order_averaged.csv',index=False)
        fs=s.groupby(['environment','method']).mean(numeric_only=True).reset_index();fs.to_csv(out/'family_summary.csv',index=False)
        lines+=['','## Prespecified family-level scoring','','The four original task groups plus benign are the reporting families. Class probabilities are summed within each family before argmax. This re-scores the existing type-trained models, does not retrain merged labels, and does not use confusion matrices to choose group membership. The additional mapped-type-prediction accuracy uses the family of the highest-probability type instead; both conventions are supplied. These task-defined groups should not be confused with a newly validated semantic taxonomy. Family correctness is an easier outcome than exact attack-type correctness.','','| Environment | Method | Family old accuracy | Family rare recall | Family worst-client macro recall |','|---|---|---:|---:|---:|']
        for _,r in fs.iterrows():lines.append(f'| {r.environment} | {r.method} | {100*r.old_task_accuracy:.2f} | {100*r.rare_attack_recall:.2f} | {100*r.worst_client_macro_recall:.2f} |')
        lines+=['','Mapping the winning type preserves the original prediction decision, whereas summing probabilities can change it; the two conventions need not have the same old-task accuracy. The `mapped_*` CSV columns provide the alternative explicitly.','','| Environment | Method | Mapped family old accuracy | Mapped family rare recall | Mapped family worst-client macro recall |','|---|---|---:|---:|---:|']
        for _,r in fs.iterrows():lines.append(f'| {r.environment} | {r.method} | {100*r.mapped_old_task_accuracy:.2f} | {100*r.mapped_rare_attack_recall:.2f} | {100*r.mapped_worst_client_macro_recall:.2f} |')
    lines+=['','## Qualification','Use the signed intervals and per-order tables to assess whether protected replay exceeds class-balanced replay and whether its advantage persists with memory. Neither positive point estimates alone nor pooled results establish a benefit in every order. The original benign evaluation support remains 16; benign-starved FPR is undefined. Joint confusion and excluded-dataset reports are separate deliverables.']
    name='ESSENTIAL_REPLAY_RESULTS.md' if args.essential_only else 'FOLLOWUP_RESULTS.md';(out/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if not args.essential_only:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for metric in ['old_task_accuracy','rare_attack_recall']:
            fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
            for ax,env in zip(axes,config['environments']):
                for method in ['uniform','class_balanced','protected']:
                    r=summary[(summary.environment==env)&summary.method.isin([f'{method}_{n}' for n in sizes])].copy();r['memory']=r.method.str.rsplit('_',n=1).str[-1].astype(int);r=r.sort_values('memory');ax.errorbar(r.memory,100*r[metric+'_mean'],yerr=100*2.2621571628*r[metric+'_std']/np.sqrt(10),marker='o',label=method)
                ax.set_title(env);ax.set_xlabel('Memory slots per client (centralized: ×5)');ax.set_xticks(sizes);ax.grid(alpha=.2);ax.legend()
            axes[0].set_ylabel(metric.replace('_',' ')+' (%)');fig.suptitle('Means and 95% seed intervals on the fixed split');fig.tight_layout();fig.savefig(out/f'memory_sweep_{metric}.png',dpi=170);fig.savefig(out/f'memory_sweep_{metric}.pdf');plt.close(fig)
    print(summary[['environment','method','old_task_accuracy_mean','rare_attack_recall_mean']].to_string(index=False))

if __name__=='__main__':main()
