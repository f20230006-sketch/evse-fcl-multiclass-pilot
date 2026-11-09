import unittest
import numpy as np
import torch
from evse_ids.teacher_alignment import aligned_kl,make_trainer
from evse_ids.distilled_replay import kd_loss
from evse_ids.multiclass_pilot import TrafficMLP,TASKS
from evse_ids.scan_final import scan_mapping

class TeacherAlignmentTests(unittest.TestCase):
 def test_type_kl_matches_legacy(self):
  torch.manual_seed(1);a=torch.randn(8,15);b=torch.randn(8,15);old=[0,2,3,9]
  self.assertTrue(torch.equal(aligned_kl(a,b,old,list(range(15))),kd_loss(a,b,old)))
 def test_family_invariance_to_scan_redistribution(self):
  classes=['Benign']+sorted(set.union(*TASKS.values()));mapping=scan_mapping(classes)[1];scans=[i for i,c in enumerate(classes)if c in ['Aggressive_Scan','Vulnerability_Scan']]
  torch.manual_seed(2);a=torch.randn(8,15);b=a.clone();b[:,scans]=a[:,list(reversed(scans))]
  self.assertLess(abs(float(aligned_kl(a,b,list(range(15)),list(range(15)),mapping))),1e-6)
  self.assertGreater(float(aligned_kl(a,b,list(range(15)),list(range(15)))),.001)
 def test_late_first_participation_gets_global_teacher(self):
  torch.manual_seed(1);classes=['Benign']+sorted(set.union(*TASKS.values()));model=TrafficMLP(4,15)
  data={'x':torch.randn(30,4),'y':torch.tensor([0,3,9]*10),'roles':np.array(['fitting']*30),'classes':classes};c={'batch_size':8,'local_epochs':1,'weight_decay':.0001};s={'learning_rate':.003,'replay_fraction':.5,'distillation_weight':.1};seen=[0,3,9]
  a=make_trainer('legacy');b=make_trainer('global')
  _,i=a(model,data,np.arange(30),np.array([],int),seen,c,s,np.random.default_rng(3),1,seen)
  _,j=b(model,data,np.arange(30),np.array([],int),seen,c,s,np.random.default_rng(3),1,seen)
  self.assertEqual(i['teacher_old_classes'],0);self.assertEqual(j['teacher_old_class_ids'],seen);self.assertGreater(j['teacher_parameter_count'],0)
 def test_global_alignment_is_noop_without_participation_gaps(self):
  torch.manual_seed(5);classes=['Benign']+sorted(set.union(*TASKS.values()));model=TrafficMLP(4,15)
  data={'x':torch.randn(30,4),'y':torch.tensor([0,3,9]*10),'roles':np.array(['fitting']*30),'classes':classes};c={'batch_size':8,'local_epochs':1,'weight_decay':.0001};settings={'learning_rate':.003,'replay_fraction':.5,'distillation_weight':.1}
  legacy=make_trainer('legacy');aligned=make_trainer('global');ra=np.random.default_rng(4);rb=np.random.default_rng(4);seen=[0,3,9]
  a,_=legacy(model,data,np.arange(15),np.array([],int),seen,c,settings,ra,0,[0]);b,_=aligned(model,data,np.arange(15),np.array([],int),seen,c,settings,rb,0,[0])
  a,_=legacy(a,data,np.arange(15,30),np.arange(15),seen,c,settings,ra,1,seen);b,_=aligned(b,data,np.arange(15,30),np.arange(15),seen,c,settings,rb,1,seen)
  self.assertTrue(all(torch.equal(a.state_dict()[k],b.state_dict()[k])for k in a.state_dict()))
 def test_first_global_phase_has_no_unlearned_teacher_constraint(self):
  self.assertEqual(float(aligned_kl(torch.randn(3,15),torch.randn(3,15),[0],[0,3,9])),0.)
if __name__=='__main__':unittest.main()
