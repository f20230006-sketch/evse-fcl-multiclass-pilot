"""Teacher-distilled replay; distinct learning mechanism, not a new allocation claim."""
from pathlib import Path
import copy,json
import numpy as np
import torch
from torch import nn
from . import asynchronous_replay as base
from .balanced_rare import train_client as ordinary_train
from .multiclass_pilot import masked_logits,save_json
from .continual_stable import ROLE_FIT


def kd_loss(student,teacher,old_seen,temperature=2.):
    if not old_seen:return student.sum()*0
    return nn.functional.kl_div(nn.functional.log_softmax(student[:,old_seen]/temperature,dim=1),nn.functional.softmax(teacher[:,old_seen]/temperature,dim=1),reduction='batchmean')*(temperature**2)


def make_trainer():
    states={}
    def train(global_model,data,current,memory,seen,c,method,settings,terms,rng):
        key=id(rng);state=states.setdefault(key,{'current':None,'seen':[],'teacher':None,'old_seen':[]})
        signature=tuple(map(int,current))
        if state['current']!=signature:
            state['old_seen']=state['seen'].copy();state['teacher']=copy.deepcopy(global_model).eval() if state['old_seen']else None
            if state['teacher'] is not None:
                for p in state['teacher'].parameters():p.requires_grad_(False)
            state['current']=signature
        state['seen']=list(seen)
        teacher=state['teacher'];weight=settings.get('distillation_weight',0.)
        if teacher is None or weight==0:
            return ordinary_train(global_model,data,current,memory,seen,c,method,settings,terms,rng)
        assert (data['roles'][current]==ROLE_FIT).all() and (data['roles'][memory]==ROLE_FIT).all()
        local=copy.deepcopy(global_model);opt=torch.optim.Adam(local.parameters(),lr=settings['learning_rate'],weight_decay=c['weight_decay'])
        fraction=settings['replay_fraction'] if len(memory)else 0.;replay_batch=max(1,int(c['batch_size']*fraction))if fraction else 0;current_batch=c['batch_size']-replay_batch
        steps=0;losses=[];distills=[]
        for _ in range(c['local_epochs']):
            shuffled=rng.permutation(current);total=0.;observations=0
            for start in range(0,len(shuffled),current_batch):
                rows=shuffled[start:start+current_batch];opt.zero_grad(set_to_none=True)
                current_logits=local(data['x'][rows]);loss=nn.functional.cross_entropy(masked_logits(current_logits,seen),data['y'][rows])
                with torch.no_grad():target=teacher(data['x'][rows])
                distill=kd_loss(current_logits,target,state['old_seen'])
                if replay_batch:
                    old=rng.choice(memory,replay_batch,replace=True);old_logits=local(data['x'][old]);replay=nn.functional.cross_entropy(masked_logits(old_logits,seen),data['y'][old]);loss=(1-fraction)*loss+fraction*replay
                    with torch.no_grad():target=teacher(data['x'][old])
                    distill=(1-fraction)*distill+fraction*kd_loss(old_logits,target,state['old_seen'])
                objective=loss+weight*distill
                if not torch.isfinite(objective):raise FloatingPointError('Non-finite distilled objective')
                objective.backward()
                if any(p.grad is not None and not torch.isfinite(p.grad).all()for p in local.parameters()):raise FloatingPointError('Non-finite distilled gradient')
                opt.step();steps+=1;total+=float(objective.detach())*len(rows);observations+=len(rows);distills.append(float(distill.detach()))
            losses.append(total/observations)
        return local,{'epoch_losses':losses,'steps':steps,'projections':0,'teacher_parameter_count':sum(p.numel()for p in teacher.parameters()),'teacher_old_classes':len(state['old_seen']),'distillation_weight':weight,'mean_kd_loss':float(np.mean(distills))}
    return train


def run_case(data,c,environment,schedule,method,settings,seed,directory,calibration_only=False):
    distilled=method.endswith('_kd');population=method.removesuffix('_kd') if distilled else method
    old=base.train_client
    try:
        if distilled:base.train_client=make_trainer()
        result=base.run_case(data,c,environment,schedule,population,settings,seed,directory,calibration_only)
    finally:base.train_client=old
    p=Path(directory)/'results.json';r=json.loads(p.read_text());r['method']=method;r['distillation_scope']='Frozen phase-start teacher; old-class temperature2 KL on current and replay fitting examples; extra teacher model RAM, no extra replay rows or allocation communication.'if distilled else 'none';save_json(p,r)
    return result
