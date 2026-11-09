import unittest
import numpy as np
import torch
from evse_ids.distilled_replay import make_trainer,kd_loss
from evse_ids.multiclass_pilot import TrafficMLP
from evse_ids.balanced_rare import train_client

class DistillTests(unittest.TestCase):
 def test_equal_old_predictions_zero_kl(self):
  x=torch.randn(8,15);y=x.clone();y[:,12]+=9
  self.assertLess(abs(float(kd_loss(x,y,[0,1,2]))),1e-6)
 def test_zero_weight_exact_baseline(self):
  torch.manual_seed(1);model=TrafficMLP(4,15);data={'x':torch.randn(30,4),'y':torch.tensor([0,1,2]*10),'roles':np.array(['fitting']*30)}
  config={'batch_size':8,'local_epochs':2,'weight_decay':.0001};settings={'learning_rate':.003,'replay_fraction':.25,'distillation_weight':0.}
  current=np.arange(15);memory=np.arange(15,30);seen=[0,1,2];trainer=make_trainer()
  a,_=train_client(model,data,current,memory,seen,config,'fixed_rbr',settings,[],np.random.default_rng(3))
  b,_=trainer(model,data,current,memory,seen,config,'fixed_rbr',settings,[],np.random.default_rng(3))
  self.assertTrue(all(torch.equal(a.state_dict()[k],b.state_dict()[k])for k in a.state_dict()))
 def test_teacher_active_only_after_first_task(self):
  torch.manual_seed(1);model=TrafficMLP(4,15);data={'x':torch.randn(30,4),'y':torch.tensor([0,1,2]*10),'roles':np.array(['fitting']*30)}
  config={'batch_size':8,'local_epochs':1,'weight_decay':.0001};settings={'learning_rate':.003,'replay_fraction':.25,'distillation_weight':1.};trainer=make_trainer();rng=np.random.default_rng(3)
  a,first=trainer(model,data,np.arange(15),np.array([],int),[0,1,2],config,'fixed_rbr',settings,[],rng)
  b,second=trainer(a,data,np.arange(15,30),np.arange(15),[0,1,2],config,'fixed_rbr',settings,[],rng)
  self.assertNotIn('teacher_old_classes',first);self.assertEqual(second['teacher_old_classes'],3);self.assertTrue(all(torch.isfinite(p).all()for p in b.parameters()))
if __name__=='__main__':unittest.main()
