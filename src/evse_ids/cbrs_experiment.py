"""Published CBRS population under the frozen task-boundary replay training protocol."""
from pathlib import Path
import time
import numpy as np
import torch
from .cbrs import CBRS
from .balanced_rare import train_client,block_metrics,evaluate,final_summary
from .multiclass_pilot import TrafficMLP,TASKS,fedavg,seed_everything,union_rows,predict,save_json
from .continual_stable import ROLE_FIT,ROLE_CAL

def run_case(data,config,environment,method,settings,seed,directory,*,calibration_only=False):
    start=time.monotonic();directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    seed_everything(seed);torch.set_num_threads(config['torch_threads_per_worker'])
    model=TrafficMLP(data['x'].shape[1],len(data['classes']))
    clients=list(data['assigned']) if environment=='federated' else ['pooled']
    capacity=config['federated_memory_per_client'] if environment=='federated' else config['centralized_memory_total']
    memories={cl:np.array([],int) for cl in clients}
    training={cl:np.random.default_rng(seed*100+i) for i,cl in enumerate(clients)}
    reservoirs={cl:CBRS(capacity,len(data['classes']),np.random.default_rng(seed*100+i+10000)) for i,cl in enumerate(clients)}
    streams={cl:np.random.default_rng(seed*100+i+20000) for i,cl in enumerate(clients)}
    history=[];log=[];buffers=[];scores=[];best={};seen={0};labels=data['y'].numpy()
    for t,task in enumerate(data['tasks']):
        seen.update(data['classes'].index(n) for n in TASKS[task['name']]);seen_list=sorted(seen)
        current={cl:union_rows([task],'train',cl if environment=='federated' else None) for cl in clients}
        for round_index in range(config['rounds_per_task']):
            updates=[]
            for cl in clients:
                local,info=train_client(model,data,current[cl],memories[cl],seen_list,config,method,settings,[],training[cl])
                count=len(np.unique(np.concatenate([current[cl],memories[cl]])));updates.append((local,count))
                log.append({'stage':t+1,'round':round_index+1,'client':cl,'current_fitting_rows':len(current[cl]),'replay_rows':len(memories[cl]),'aggregation_unique_rows':count,**info})
            fedavg(model,updates)
        allowed=data['tasks'][:t+1];cal=union_rows(allowed,'calibration');assert (data['roles'][cal]==ROLE_CAL).all()
        prob=predict(model,data['x'],cal,seen_list);m=block_metrics(labels[cal],prob,data['classes'],seen_list);scores.append(m['macro_recall'])
        checkpoint={'checkpoint':t+1,'learned_task':task['name'],'seen_classes':seen_list,'calibration':m}
        if not calibration_only:
            evaluation,rows,prob=evaluate(model,data,allowed,seen_list,best);checkpoint.update(evaluation)
            np.savez_compressed(directory/f'checkpoint_{t+1}_predictions.npz',sample_index=rows,y_true=labels[rows],y_pred=prob.argmax(1),probability=prob)
        history.append(checkpoint)
        for cl in clients:
            # Benign fitting rows recur for training, but are a single arrival in the population stream.
            new=current[cl] if t==0 else current[cl][labels[current[cl]]!=0]
            assert (data['roles'][new]==ROLE_FIT).all()
            stream=streams[cl].permutation(new);memories[cl],audit=reservoirs[cl].ingest(stream,labels)
            buffers.append({'stage':t+1,'client':cl,'capacity':capacity,'stream_rows':stream.tolist(),'memory_rows':memories[cl].tolist(),**audit})
    result={'environment':environment,'method':method,'seed':seed,'settings':settings,'calibration_only':calibration_only,'history':history,'selection_score':float(np.mean(scores)),'elapsed_seconds':time.monotonic()-start}
    if not calibration_only:
        result['summary'],result['per_client_summary']=final_summary(history,data,method);torch.save(model.state_dict(),directory/'final_model.pt')
    save_json(directory/'results.json',result);save_json(directory/'training_log.json',log);save_json(directory/'memory_audit.json',buffers)
    return {k:result[k] for k in ['selection_score','elapsed_seconds']}
