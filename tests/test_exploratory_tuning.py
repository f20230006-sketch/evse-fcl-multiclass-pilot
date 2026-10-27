import unittest
import numpy as np
import torch
from evse_ids.exploratory_tuning import TunedMLP,calibration_primary
from evse_ids.multiclass_pilot import TrafficMLP,predict,TASKS
from evse_ids.continual_stable import ROLE_CAL,ROLE_EVAL

class ExploratoryTuningTests(unittest.TestCase):
    def test_reference_initialization_matches(self):
        torch.manual_seed(42);a=TrafficMLP(12,15)
        torch.manual_seed(42);b=TunedMLP(12,15,[64,32],0.)
        x=torch.randn(10,12)
        self.assertTrue(torch.equal(a(x),b(x)))

    def test_dropout_predict_is_deterministic(self):
        model=TunedMLP(8,15,[128,64],.1);x=torch.randn(10,8)
        a=predict(model,x,np.arange(10),list(range(15)))
        b=predict(model,x,np.arange(10),list(range(15)))
        self.assertTrue(np.array_equal(a,b));self.assertFalse(model.training)
        model.train();self.assertFalse(torch.equal(model(x),model(x)))

    def test_calibration_role_boundary(self):
        names=['Benign']+sorted(set.union(*TASKS.values()))
        data={'classes':names,'y':torch.arange(15),'roles':np.array([ROLE_EVAL]*15),'clients':np.array(['a']*15),'assigned':{'a':np.arange(15)}}
        with self.assertRaises(AssertionError):calibration_primary(data,np.arange(15),np.eye(15),[{'name':n} for n in TASKS],list(range(15)))
        data['roles']=np.array([ROLE_CAL]*15)
        score=calibration_primary(data,np.arange(15),np.eye(15),[{'name':n} for n in TASKS],list(range(15)))
        self.assertEqual(score['objective'],1.)

if __name__=='__main__':unittest.main()
