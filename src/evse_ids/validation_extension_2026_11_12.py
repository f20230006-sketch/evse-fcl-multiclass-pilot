"""Separate locked source-file and independent connection-group validations."""
from pathlib import Path
import hashlib,json,copy,time
import numpy as np
import pandas as pd
import torch
from . import balanced_rare as base
from . import cbrs_experiment as cbrs
from . import multiclass_pilot as pilot
from .continual_stable import build_persistent_tasks,fit_frozen_preprocessor,client_for_each_row
from .multiclass_pilot import save_json

ORIGINAL_TASKS=copy.deepcopy(pilot.TASKS)
EXTERNAL_TASKS={
 'reconnaissance':{'cyberattack_ocpp16_doc_idtag'},
 'flooding':{'cyberattack_ocpp16_dos_flooding_heartbeat'},
 'low_rate_rare':{'cyberattack_ocpp16_fdi_chargingprofile'},
 'post_rare_vulnerability':{'cyberattack_ocpp16_unauthorized_access'}}
ORDERS={'order_1':['reconnaissance','flooding','low_rate_rare','post_rare_vulnerability'],
 'order_2':['flooding','reconnaissance','post_rare_vulnerability','low_rate_rare'],
 'order_3':['low_rate_rare','post_rare_vulnerability','flooding','reconnaissance']}
CLIENTS=['reconnaissance_heavy','flooding_heavy','low_rate_rare_heavy','mixed_open_set','benign_starved']
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def group_roles(groups,seed=712):
 names=sorted(set(groups));rng=np.random.default_rng(seed)
 assign=dict(zip(names,rng.choice(['fitting','calibration','evaluation'],len(names),p=[.55,.15,.30])))
 return np.array([assign[g] for g in groups],dtype=object)
def connection_components(frame,feature_columns):
 # Canonical bidirectional 5-tuple. Same tuple over distant captures is kept together conservatively.
 endpoints=[]
 for _,r in frame.iterrows():
  a=(str(r['Src IP']),int(r['Src Port']));b=(str(r['Dst IP']),int(r['Dst Port']))
  endpoints.append(repr((tuple(sorted([a,b])),int(r['Protocol']))))
 parent=list(range(len(frame)))
 def find(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 def union(a,b):
  a,b=find(a),find(b)
  if a!=b:parent[max(a,b)]=min(a,b)
 vec=pd.util.hash_pandas_object(frame[feature_columns].replace([np.inf,-np.inf],np.nan).fillna(0),index=False).to_numpy()
 for keys in [endpoints,vec.tolist()]:
  seen={}
  for i,k in enumerate(keys):
   if k in seen:union(i,seen[k])
   else:seen[k]=i
 return np.array([str(find(i)) for i in range(len(frame))]),vec
def external_clients(labels,tasks):
 rng=np.random.default_rng(712);assigned={c:[] for c in CLIENTS}
 for label in sorted(set(labels)):
  rows=np.flatnonzero(labels==label);rng.shuffle(rows)
  if label=='Benign':weights=np.array([55,15,10,20,0])
  elif label in tasks['reconnaissance']:weights=np.array([55,10,5,20,10])
  elif label in tasks['flooding']:weights=np.array([10,55,5,20,10])
  else:weights=np.array([5,5,55,25,10])
  raw=weights*len(rows)/100;n=np.floor(raw).astype(int)
  for i in np.argsort(-(raw-n),kind='stable')[:len(rows)-n.sum()]:n[i]+=1
  start=0
  for c,count in zip(CLIENTS,n):assigned[c].extend(rows[start:start+count]);start+=count
 return {c:np.array(v,dtype=int) for c,v in assigned.items()}
def prepare_track(root,track,output,config):
 root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
 if track=='source_file':
  frame=pd.read_pickle(root/'outputs/multiclass_full_comparison/sampled_fixed.pkl').reset_index(drop=True)
  labels=frame.Label.to_numpy();tasks=ORIGINAL_TASKS
  previous=pd.read_csv(root/'outputs/multiclass_full_comparison/splits/order_1/split_manifest.csv')
  assigned={c:np.flatnonzero(previous.client.to_numpy()==c) for c in CLIENTS}
  files={}
  for label,g in frame.groupby('Label'):
   names=sorted(g.__source_file__.unique(),key=lambda p:hashlib.sha256(('712'+label+p).encode()).hexdigest())
   assert len(names)>=2;files[label]=names[0]
  evalmask=np.array([f==files[l] for f,l in zip(frame.__source_file__,labels)])
  roles=np.full(len(frame),'fitting',dtype=object);roles[evalmask]='evaluation'
  rng=np.random.default_rng(712)
  for c,rows in assigned.items():
   for label in sorted(set(labels)):
    available=rows[(labels[rows]==label)&~evalmask[rows]];available=rng.permutation(available)
    n=int(np.floor(len(available)*.1875))
    if len(available)>=3:n=max(n,1)
    roles[available[:n]]='calibration'
  # Hash only modelling features after removing known identifier/provenance columns.
  from .continual_stable import DEFAULT_CAPTURE_IDENTIFIER_COLUMNS
  from .data import ABSOLUTE_TIMESTAMP_COLUMNS,PROVENANCE_COLUMNS
  drop=set(DEFAULT_CAPTURE_IDENTIFIER_COLUMNS)|set(ABSOLUTE_TIMESTAMP_COLUMNS)|set(PROVENANCE_COLUMNS)|{'Label'}
  featurecols=[c for c in frame if c not in drop]
  hashes=pd.util.hash_pandas_object(frame[featurecols].astype(str),index=False).to_numpy()
  duplicates=evalmask & np.isin(hashes,hashes[~evalmask]);roles[duplicates]='excluded_duplicate'
  groups=frame.__source_file__.to_numpy()
  audit={'heldout_files':files,'excluded_identical_evaluation_vectors':int(duplicates.sum()),'split_unit':'whole source file for evaluation; client/type rows within other files for calibration','independent_capture_claim':False}
  rare_groups={'declared':['Slowloris_Scan','ICMP_Fragmentation'],'icmp':['ICMP_Flood'],'union':['Slowloris_Scan','ICMP_Fragmentation','ICMP_Flood']}
 else:
  directory=root/'data/external_validation_2026_11_12/Balanced_OCPP16_TCP-IP_Layer'
  parts=[]
  for p in sorted(directory.rglob('Combined/*.csv')):
   f=pd.read_csv(p);f['__source_file__']=p.name;f['__source_row__']=np.arange(len(f));parts.append(f)
  frame=pd.concat(parts,ignore_index=True)
  frame['Label']=frame.Label.replace({'normal':'Benign'})
  excluded={'Flow ID','Src IP','Src Port','Dst IP','Dst Port','Timestamp','Total Connection Flow Time','Label','__source_file__','__source_row__'}
  features=[c for c in frame if c not in excluded]
  frame[features]=frame[features].apply(pd.to_numeric,errors='coerce').replace([np.inf,-np.inf],np.nan).fillna(0)
  groups,hashes=connection_components(frame,features)
  assert pd.DataFrame({'h':hashes,'l':frame.Label}).groupby('h').l.nunique().max()==1
  keep=~pd.Series(hashes).duplicated().to_numpy();removed=int((~keep).sum())
  frame=frame.loc[keep].reset_index(drop=True);groups=groups[keep];hashes=hashes[keep]
  roles=group_roles(groups);labels=frame.Label.to_numpy();tasks=EXTERNAL_TASKS
  assigned=external_clients(labels,tasks)
  minority=tasks['reconnaissance']|tasks['low_rate_rare']
  for label in sorted(minority):
   ids=np.flatnonzero((labels==label)&(roles=='fitting'))
   ids=sorted(ids,key=lambda i:hashlib.sha256(('712'+str(hashes[i])).encode()).hexdigest())
   roles[np.array(ids[max(1,int(len(ids)*.20)):],int)]='excluded_minority_fit'
  metadata=frame[['__source_file__','__source_row__','Label']].copy()
  frame=frame[features+['Label','__source_file__','__source_row__']].copy()
  frame['__evse__']='independent_ocpp';frame['__operating_state__']='unspecified'
  audit={'split_unit':'canonical bidirectional TCP 5-tuple components, unioned through duplicate feature vectors','deduplicated_rows':removed,'benign_evaluation_flows':int(((labels=='Benign')&(roles=='evaluation')).sum()),'independent_capture_claim':False,'independent_dataset':True,'modelling_features':features,'fit_minority_fraction':.20,'publisher_balanced_subset':True}
  rare_groups={'declared':sorted(tasks['reconnaissance']),'icmp':sorted(tasks['low_rate_rare']),'union':sorted(minority)}
  assert audit['benign_evaluation_flows']>=200,audit
 labels=frame.Label.astype(str).to_numpy();classes=['Benign']+sorted(set.union(*tasks.values()));y=np.array([classes.index(l) for l in labels]);clients=client_for_each_row(assigned,len(frame))
 manifest=frame[['__source_file__','__source_row__','Label']].copy();manifest['sample_index']=np.arange(len(frame));manifest['client']=clients;manifest['role']=roles;manifest['group']=groups
 manifest.to_csv(output/'split_manifest.csv',index=False)
 counts=pd.crosstab(labels,roles);counts.to_csv(output/'class_role_counts.csv')
 eligible=all((counts.get(role,pd.Series(0,index=counts.index))>0).all() for role in ['fitting','calibration','evaluation'])
 if not eligible:
  audit['eligible']=False;audit['reason']='Some class/role cells have no support after locked de-duplication.';audit['class_role_counts']=counts.to_dict();save_json(output/'ineligible.json',audit)
  raise ValueError('Validation eligibility failed; see ineligible.json')
 evalgroups=set(groups[roles=='evaluation']);assert not evalgroups&set(groups[np.isin(roles,['fitting','calibration'])])
 if track!='source_file':assert not set(groups[roles=='fitting'])&set(groups[roles=='calibration'])
 audit['class_role_counts']=counts.to_dict();audit['role_disjoint_groups_verified']=True
 audit['groups_by_role']={role:int(len(set(groups[roles==role]))) for role in ['fitting','calibration','evaluation']}
 audit['benign_groups_by_role']={role:int(len(set(groups[(roles==role)&(labels=='Benign')]))) for role in ['fitting','calibration','evaluation']}
 save_json(output/'audit.json',audit)
 for order,sequence in ORDERS.items():
  od=output/order;od.mkdir(exist_ok=True)
  tasklist=build_persistent_tasks(labels,assigned,roles,[(n,tasks[n]) for n in sequence],benign_names={'Benign'})
  prep=np.unique(np.concatenate(list(tasklist[0]['train'].values())))
  assert len(prep)>0 and (roles[prep]=='fitting').all()
  x,state,preprocessing=fit_frozen_preprocessor(frame,'Label',prep,z_clip=5)
  data={'x':torch.tensor(x,dtype=torch.float32),'y':torch.tensor(y,dtype=torch.long),'labels':labels,'classes':classes,'roles':roles,'clients':clients,'tasks':tasklist,'assigned':assigned,'manifest':manifest,'custom_tasks':tasks,'rare_groups':rare_groups,'track':track}
  torch.save(data,od/'prepared.pt');save_json(od/'preprocessing.json',preprocessing)
 return audit
def run_job(job):
 data=torch.load(job['prepared'],weights_only=False,map_location='cpu'); directory=Path(job['directory']);config=job['config']
 stamp=directory/'complete.json'
 if stamp.exists():
  r=json.loads(stamp.read_text());assert r['fingerprint']==job['fingerprint'];return r
 group=data['rare_groups'][job['group']] if job['method']=='rbr' else []
 base.TASKS=data['custom_tasks'];pilot.TASKS=data['custom_tasks'];cbrs.TASKS=data['custom_tasks']
 base.RARE=set(group);pilot.RARE=set(group)
 settings=job['settings'].copy()
 if job['method']=='cbrs':
  result=cbrs.run_case(data,config,job['environment'],'cbrs_60',settings,job['seed'],directory,calibration_only=job['calibration_only'])
 else:
  if job['method']=='balanced':settings['rare_quota_fraction']=0.
  result=base.run_case(data,config,job['environment'],'balanced_rare_60',settings,job['seed'],directory,calibration_only=job['calibration_only'])
 record={k:job[k] for k in ['fingerprint','method','group','environment','order','seed','settings','calibration_only']};record.update(result);save_json(stamp,record)
 return record
