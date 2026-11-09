"""Prospective asynchronous replay study; historical paper outputs are read-only."""
from pathlib import Path
import time
import numpy as np
import torch
from .balanced_rare import train_client,block_metrics
from .balanced_rare_allocator import update_balanced_rare_buffer
from .continual_ablation import update_replay_buffer
from .cbrs import CBRS
from .multiclass_pilot import TrafficMLP,TASKS,RARE,fedavg,seed_everything,union_rows,predict,save_json,metrics
from .continual_stable import ROLE_FIT,ROLE_CAL,ROLE_EVAL
from .scan_final import scan_mapping,merge_probabilities


def client_task(phase,index,schedule,offsets):
    task=phase-(offsets[index] if schedule=='delayed' else 0)
    return task if 0<=task<4 else None


def adaptive_quota(recalls,best,maximum):
    """Bounded calibration-only controller: acquisition error or recall erosion."""
    pressure=max([max(1-v,2*max(0,best.get(c,v)-v)) for c,v in recalls.items()] or [0.])
    return .10+(maximum-.10)*float(np.clip(pressure,0,1))


def score(model,data,allowed,seen,best):
    rows=union_rows(allowed,'test');assert (data['roles'][rows]==ROLE_EVAL).all()
    p=predict(model,data['x'],rows,seen);y=data['y'][rows].numpy()
    histories={};summaries={}
    for space in ['merged_scans','original_type']:
        if space=='merged_scans':
            names,mapping=scan_mapping(data['classes']);q=merge_probabilities(p,mapping,len(names));truth=mapping[y];seen_=sorted(set(mapping[seen]))
        else:names=data['classes'];q=p;truth=y;seen_=seen
        pred=q.argmax(1);acc={};drops={}
        for t in allowed:
            mask=np.isin(y,[data['classes'].index(c) for c in TASKS[t['name']]])
            acc[t['name']]=float((pred[mask]==truth[mask]).mean());key=(space,t['name'])
            drops[t['name']]=max(0,best.get(key,acc[t['name']])-acc[t['name']]);best[key]=max(best.get(key,acc[t['name']]),acc[t['name']])
        local={}
        for cl in data['assigned']:
            mask=data['clients'][rows]==cl;m=metrics(truth[mask],q[mask],names,seen_)
            slow=next((c['recall'] for c in m['per_class'] if c['class']=='Slowloris_Scan'),None)
            local[cl]={'macro_recall':m['macro_recall'],'slowloris_recall':slow,'false_alarm_rate':m['false_alarm_rate']}
        slowmask=y==data['classes'].index('Slowloris_Scan')
        old=[t['name'] for t in data['tasks'][:-1] if t['name'] in acc]
        summaries[space]={'old_task_accuracy':float(np.mean([acc[t] for t in old])), 'forgetting':float(np.mean([drops[t] for t in old])),
            'slowloris_recall':float((pred[slowmask]==truth[slowmask]).mean()) if slowmask.any() else None,
            'worst_client_macro_recall':min(m['macro_recall'] for m in local.values() if m['macro_recall'] is not None)}
        histories[space]={'cohort_accuracy':acc,'cohort_forgetting':drops,'per_client':local,'summary':summaries[space]}
    return histories,rows,p


def run_case(data,c,environment,schedule,method,settings,seed,directory,calibration_only=False):
    started=time.monotonic();d=Path(directory);d.mkdir(parents=True,exist_ok=True)
    seed_everything(seed);torch.set_num_threads(c['torch_threads_per_worker'])
    model=TrafficMLP(data['x'].shape[1],len(data['classes']));original_clients=list(data['assigned']);clients=original_clients if environment=='federated' else ['pooled']
    capacity=60 if environment=='federated' else 300
    memories={cl:np.array([],int) for cl in clients};trainrng={cl:np.random.default_rng(seed*100+i) for i,cl in enumerate(clients)}
    memrng={cl:np.random.default_rng(seed*100+i+10000) for i,cl in enumerate(clients)};streamrng={cl:np.random.default_rng(seed*100+i+20000) for i,cl in enumerate(clients)}
    reservoirs={cl:CBRS(capacity,len(data['classes']),memrng[cl]) for cl in clients};arrived={cl:set() for cl in clients}
    bestcal={cl:{} for cl in clients};history=[];audit=[];logs=[];scores=[];best={};seen={0};exposed=set();y=data['y'].numpy()
    for phase in range(c['phases']):
        indices={cl:client_task(phase,i,schedule,c['offsets']) for i,cl in enumerate(original_clients)}
        localrows={cl:(union_rows([data['tasks'][idx]],'train',cl) if idx is not None else np.array([],int)) for cl,idx in indices.items()}
        for idx in indices.values():
            if idx is not None:exposed.add(idx);seen.update(data['classes'].index(n) for n in TASKS[data['tasks'][idx]['name']])
        current=localrows if environment=='federated' else {'pooled':np.unique(np.concatenate(list(localrows.values())))}
        seenlist=sorted(seen);active=[cl for cl in clients if len(current[cl])];allowed=[data['tasks'][i] for i in sorted(exposed)]
        for rnd in range(c['rounds_per_task']):
            updates=[]
            for cl in active:
                local,info=train_client(model,data,current[cl],memories[cl],seenlist,c,method,settings,[],trainrng[cl]);n=len(np.union1d(current[cl],memories[cl]));updates.append((local,n))
                logs.append({'phase':phase+1,'round':rnd+1,'client':cl,'current_fitting_rows':len(current[cl]),'replay_rows':len(memories[cl]),'aggregation_unique_rows':n,**info})
            if updates:fedavg(model,updates)
        cal=union_rows(allowed,'calibration');assert (data['roles'][cal]==ROLE_CAL).all()
        cp=predict(model,data['x'],cal,seenlist);m=block_metrics(y[cal],cp,data['classes'],seenlist);scores.append(m['macro_recall'])
        checkpoint={'checkpoint':phase+1,'active_clients':active,'client_task_index':indices,'seen_classes':seenlist,'calibration_macro_recall':m['macro_recall']}
        if not calibration_only:
            hs,rows,p=score(model,data,allowed,seenlist,best);checkpoint['scores']=hs
            np.savez_compressed(d/f'checkpoint_{phase+1}_predictions.npz',sample_index=rows,y_true=y[rows],probability=p)
        history.append(checkpoint)
        for cl in active:
            assert (data['roles'][current[cl]]==ROLE_FIT).all()
            q=settings.get('rare_quota_fraction',.1);monitor=[];recalls={}
            if method=='adaptive_rbr':
                localcal=cal if cl=='pooled' else cal[data['clients'][cal]==cl]
                for name in sorted(RARE):
                    cid=data['classes'].index(name);selected=localcal[y[localcal]==cid]
                    if len(selected)>=c['monitor_min_examples']:
                        assert (data['roles'][selected]==ROLE_CAL).all();pr=predict(model,data['x'],selected,seenlist)
                        recalls[name]=float((pr.argmax(1)==cid).mean());monitor.extend(selected.tolist())
                q=adaptive_quota(recalls,bestcal[cl],settings['maximum_rare_fraction'])
                for name,value in recalls.items():bestcal[cl][name]=max(bestcal[cl].get(name,value),value)
            if method=='class_balanced':memories[cl]=update_replay_buffer(memories[cl],current[cl],data['labels'],capacity=capacity,strategy='balanced',rng=memrng[cl])
            elif method in ['fixed_rbr','adaptive_rbr']:
                memories[cl],_=update_balanced_rare_buffer(memories[cl],current[cl],data['labels'],capacity=capacity,rng=memrng[cl],rare_group=RARE,rare_fraction=q)
            elif method=='cbrs':
                new=np.array([r for r in current[cl] if int(r) not in arrived[cl]],dtype=int);arrived[cl].update(map(int,new))
                memories[cl],_=reservoirs[cl].ingest(streamrng[cl].permutation(new),y)
            else:raise ValueError(method)
            assert len(memories[cl])==len(set(memories[cl])) and len(memories[cl])<=capacity and (data['roles'][memories[cl]]==ROLE_FIT).all()
            audit.append({'phase':phase+1,'client':cl,'current_rows':current[cl].tolist(),'memory_rows':memories[cl].tolist(),'quota_fraction':q if 'rbr' in method else None,
                'monitor_rows':monitor,'monitor_recalls':recalls,'class_counts':{name:int((y[memories[cl]]==i).sum()) for i,name in enumerate(data['classes'])}})
    result={'environment':environment,'schedule':schedule,'method':method,'seed':seed,'settings':settings,'calibration_only':calibration_only,'selection_score':float(np.mean(scores)),'elapsed_seconds':time.monotonic()-started,'history':history}
    if not calibration_only:
        result['summary']={space:history[-1]['scores'][space]['summary'] for space in ['merged_scans','original_type']};torch.save(model.state_dict(),d/'final_model.pt')
    save_json(d/'results.json',result);save_json(d/'memory_audit.json',audit);save_json(d/'training_log.json',logs)
    return {k:result[k] for k in ['selection_score','elapsed_seconds']}
