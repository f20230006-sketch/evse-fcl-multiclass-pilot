"""Bounded follow-up: global teacher coverage and family-consistent distillation."""
from pathlib import Path
import copy,time
import numpy as np
import torch
from torch import nn
from .balanced_rare import train_client as ordinary_train,block_metrics
from .balanced_rare_allocator import update_balanced_rare_buffer
from .continual_ablation import update_replay_buffer
from .multiclass_pilot import TrafficMLP,TASKS,fedavg,seed_everything,union_rows,predict,save_json,masked_logits,metrics
from .continual_stable import ROLE_FIT,ROLE_CAL
from .scan_final import scan_mapping,merge_probabilities
from .asynchronous_replay import client_task,score


def aligned_kl(student,teacher,old_seen,current_seen,mapping=None,temperature=2.):
    if len(old_seen)<2:return student.sum()*0
    if mapping is None:
        a=student[:,old_seen]/temperature;b=teacher[:,old_seen]/temperature
    else:
        families=sorted(set(int(mapping[i])for i in old_seen))
        a=torch.stack([torch.logsumexp(student[:,[i for i in current_seen if mapping[i]==g]]/temperature,dim=1)for g in families],dim=1)
        b=torch.stack([torch.logsumexp(teacher[:,[i for i in old_seen if mapping[i]==g]]/temperature,dim=1)for g in families],dim=1)
    return nn.functional.kl_div(nn.functional.log_softmax(a,dim=1),nn.functional.softmax(b,dim=1),reduction='batchmean')*temperature**2


def make_trainer(mode):
    states={}
    def train(global_model,data,current,memory,seen,c,settings,rng,phase,global_old):
        state=states.setdefault(id(rng),{'phase':None,'seen':[],'teacher':None,'old':[]})
        if state['phase']!=phase:
            old=state['seen'].copy() if mode=='legacy' else list(global_old)
            state['old']=old;state['phase']=phase;state['teacher']=copy.deepcopy(global_model).eval() if len(old)>=2 else None
            if state['teacher']is not None:
                for p in state['teacher'].parameters():p.requires_grad_(False)
        state['seen']=list(seen);teacher=state['teacher'];weight=settings['distillation_weight']
        if teacher is None or weight==0:
            local,info=ordinary_train(global_model,data,current,memory,seen,c,'fixed_rbr',settings,[],rng)
            return local,{**info,'teacher_old_class_ids':[],'teacher_old_classes':0,'teacher_parameter_count':0}
        assert (data['roles'][current]==ROLE_FIT).all()and(data['roles'][memory]==ROLE_FIT).all()
        mapping=scan_mapping(data['classes'])[1]if mode=='family'else None
        local=copy.deepcopy(global_model);opt=torch.optim.Adam(local.parameters(),lr=settings['learning_rate'],weight_decay=c['weight_decay']);fraction=settings['replay_fraction']if len(memory)else 0.
        rb=max(1,int(c['batch_size']*fraction))if fraction else 0;cb=c['batch_size']-rb;steps=0;losses=[];kds=[]
        for _ in range(c['local_epochs']):
            shuffled=rng.permutation(current);total=0.;observations=0
            for start in range(0,len(shuffled),cb):
                rows=shuffled[start:start+cb];opt.zero_grad(set_to_none=True);logits=local(data['x'][rows]);loss=nn.functional.cross_entropy(masked_logits(logits,seen),data['y'][rows])
                with torch.no_grad():targets=teacher(data['x'][rows])
                kd=aligned_kl(logits,targets,state['old'],seen,mapping)
                if rb:
                    old=rng.choice(memory,rb,replace=True);oldlogits=local(data['x'][old]);replay=nn.functional.cross_entropy(masked_logits(oldlogits,seen),data['y'][old]);loss=(1-fraction)*loss+fraction*replay
                    with torch.no_grad():targets=teacher(data['x'][old])
                    kd=(1-fraction)*kd+fraction*aligned_kl(oldlogits,targets,state['old'],seen,mapping)
                objective=loss+weight*kd
                if not torch.isfinite(objective):raise FloatingPointError('Non-finite aligned objective')
                objective.backward()
                if any(p.grad is not None and not torch.isfinite(p.grad).all()for p in local.parameters()):raise FloatingPointError('Non-finite aligned gradient')
                opt.step();steps+=1;total+=float(objective.detach())*len(rows);observations+=len(rows);kds.append(float(kd.detach()))
            losses.append(total/observations)
        return local,{'epoch_losses':losses,'steps':steps,'projections':0,'teacher_old_class_ids':state['old'],'teacher_old_classes':len(state['old']),'teacher_parameter_count':sum(p.numel()for p in teacher.parameters()),'mean_kd_loss':float(np.mean(kds))}
    return train


def run_case(data,c,environment,method,settings,seed,directory,calibration_only=False):
    started=time.monotonic();d=Path(directory);d.mkdir(exist_ok=True,parents=True);seed_everything(seed);torch.set_num_threads(c['torch_threads_per_worker'])
    model=TrafficMLP(data['x'].shape[1],len(data['classes']));original=list(data['assigned']);clients=original if environment=='federated'else['pooled'];capacity=60 if environment=='federated'else 300
    mode='family'if'family'in method else'global'if'global'in method else'legacy';trainer=make_trainer(mode)
    memories={cl:np.array([],int)for cl in clients};trng={cl:np.random.default_rng(seed*100+i)for i,cl in enumerate(clients)};mrng={cl:np.random.default_rng(seed*100+i+10000)for i,cl in enumerate(clients)}
    seen={0};exposed=set();history=[];logs=[];audit=[];scores={'original_type':[],'merged_scans':[]};best={};y=data['y'].numpy();merged_names,mapping=scan_mapping(data['classes'])
    for phase in range(6):
        global_old=sorted(seen);indices={cl:client_task(phase,i,'delayed',c['offsets'])for i,cl in enumerate(original)}
        localrows={cl:(union_rows([data['tasks'][i]],'train',cl)if i is not None else np.array([],int))for cl,i in indices.items()}
        for i in indices.values():
            if i is not None:exposed.add(i);seen.update(data['classes'].index(n)for n in TASKS[data['tasks'][i]['name']])
        current=localrows if environment=='federated'else{'pooled':np.unique(np.concatenate(list(localrows.values())))};active=[cl for cl in clients if len(current[cl])];seenlist=sorted(seen);allowed=[data['tasks'][i]for i in sorted(exposed)]
        for rnd in range(c['rounds_per_task']):
            updates=[]
            for cl in active:
                local,info=trainer(model,data,current[cl],memories[cl],seenlist,c,settings,trng[cl],phase,global_old);n=len(np.union1d(current[cl],memories[cl]));updates.append((local,n))
                logs.append({'phase':phase+1,'round':rnd+1,'client':cl,'global_old_seen':global_old,'current_fitting_rows':len(current[cl]),'replay_rows':len(memories[cl]),'aggregation_unique_rows':n,**info})
            if updates:fedavg(model,updates)
        cal=union_rows(allowed,'calibration');assert (data['roles'][cal]==ROLE_CAL).all();prob=predict(model,data['x'],cal,seenlist)
        a=block_metrics(y[cal],prob,data['classes'],seenlist)['macro_recall'];q=merge_probabilities(prob,mapping,len(merged_names));b=metrics(mapping[y[cal]],q,merged_names,sorted(set(mapping[seenlist])))['macro_recall']
        scores['original_type'].append(a);scores['merged_scans'].append(b)
        ck={'checkpoint':phase+1,'client_task_index':indices,'active_clients':active,'seen_classes':seenlist,'global_old_seen':global_old,'calibration_original_macro_recall':a,'calibration_merged_macro_recall':b}
        if not calibration_only:
            hs,rows,p=score(model,data,allowed,seenlist,best);ck['scores']=hs;np.savez_compressed(d/f'checkpoint_{phase+1}_predictions.npz',sample_index=rows,y_true=y[rows],probability=p)
        history.append(ck)
        for cl in active:
            if method.startswith('cb_'):memories[cl]=update_replay_buffer(memories[cl],current[cl],data['labels'],capacity=capacity,strategy='balanced',rng=mrng[cl])
            else:memories[cl],_=update_balanced_rare_buffer(memories[cl],current[cl],data['labels'],capacity=capacity,rng=mrng[cl],rare_group={'Slowloris_Scan','ICMP_Fragmentation'},rare_fraction=settings['rare_quota_fraction'])
            assert len(memories[cl])==len(set(memories[cl]))and len(memories[cl])<=capacity and(data['roles'][memories[cl]]==ROLE_FIT).all()
            audit.append({'phase':phase+1,'client':cl,'current_rows':current[cl].tolist(),'memory_rows':memories[cl].tolist()})
    result={'environment':environment,'method':method,'mode':mode,'seed':seed,'settings':settings,'calibration_only':calibration_only,'selection_scores':{k:float(np.mean(v))for k,v in scores.items()},'history':history,'elapsed_seconds':time.monotonic()-started}
    if not calibration_only:result['summary']={space:history[-1]['scores'][space]['summary']for space in scores};torch.save(model.state_dict(),d/'final_model.pt')
    save_json(d/'results.json',result);save_json(d/'training_log.json',logs);save_json(d/'memory_audit.json',audit)
    return {k:result[k]for k in ['selection_scores','elapsed_seconds']}
