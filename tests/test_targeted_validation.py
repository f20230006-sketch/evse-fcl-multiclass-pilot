import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from evse_ids.continual_ablation import update_replay_buffer
from evse_ids.balanced_rare_allocator import update_balanced_rare_buffer

def test_balanced_rare_zero_quota_reproduces_balanced():
    labels=np.array(['Benign']*20+['Slowloris_Scan']*8+['TCP_Flood']*20)
    rows=np.arange(len(labels))
    actual,_=update_balanced_rare_buffer([],rows,labels,capacity=12,rng=np.random.default_rng(42),rare_group={'Slowloris_Scan'},rare_fraction=0)
    expected=update_replay_buffer([],rows,labels,capacity=12,strategy='balanced',rng=np.random.default_rng(42))
    assert np.array_equal(actual,expected)

def test_rare_random_has_no_benign_minimum_and_preserves_quota():
    labels=np.array(['Benign']*1+['Slowloris_Scan']*30+['TCP_Flood']*100)
    rows=update_replay_buffer([],np.arange(len(labels)),labels,capacity=20,strategy='protected',rng=np.random.default_rng(3),protected_groups=[{'Slowloris_Scan'}],minimum_fraction=.2)
    assert len(rows)==len(set(rows))==20
    assert (labels[rows]=='Slowloris_Scan').sum()>=4

def test_rare_random_shortage_redistributes():
    labels=np.array(['Slowloris_Scan']+['TCP_Flood']*100)
    rows=update_replay_buffer([],np.arange(len(labels)),labels,capacity=20,strategy='protected',rng=np.random.default_rng(4),protected_groups=[{'Slowloris_Scan'}],minimum_fraction=.2)
    assert len(rows)==20 and 0 in rows

def test_local_training_matches_frozen_implementation():
    import torch
    from evse_ids.multiclass_pilot import TrafficMLP
    from evse_ids.balanced_rare import train_client as frozen
    from evse_ids.targeted_validation import train_client as targeted
    torch.set_num_threads(1);torch.manual_seed(42)
    model=TrafficMLP(5,3)
    data={'x':torch.randn(24,5),'y':torch.arange(24)%3,'roles':np.array(['fitting']*24)}
    config={'weight_decay':.0001,'batch_size':8,'local_epochs':2,'gradient_clip_norm':None}
    settings={'learning_rate':.003,'replay_fraction':.5}
    args=(model,data,np.arange(16),np.arange(16,24),[0,1,2],config,'balanced_rare_60',settings,[])
    a,info_a=frozen(*args,np.random.default_rng(42));b,info_b=targeted(*args,np.random.default_rng(42))
    assert info_a==info_b
    assert all(torch.equal(a.state_dict()[k],b.state_dict()[k]) for k in a.state_dict())

class TargetedValidationTests(unittest.TestCase):
    def test_balanced_zero_quota(self):test_balanced_rare_zero_quota_reproduces_balanced()
    def test_rare_random_quota(self):test_rare_random_has_no_benign_minimum_and_preserves_quota()
    def test_shortage(self):test_rare_random_shortage_redistributes()
    def test_frozen_training_parity(self):test_local_training_matches_frozen_implementation()

if __name__=='__main__':unittest.main()
