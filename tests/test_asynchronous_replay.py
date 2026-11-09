import unittest
import numpy as np
from evse_ids.asynchronous_replay import client_task,adaptive_quota
from evse_ids.balanced_rare_allocator import update_balanced_rare_buffer

class AsyncReplayTests(unittest.TestCase):
 def test_delayed_exposure_once_per_client(self):
  offsets=[0,1,0,2,1]
  for s in ['synchronized','delayed']:
   for i in range(5):
    tasks=[client_task(p,i,s,offsets)for p in range(6)]
    self.assertEqual([t for t in tasks if t is not None],list(range(4)))
 def test_controller_bounds_and_missing_support(self):
  self.assertEqual(adaptive_quota({}, {},.3),.1)
  self.assertAlmostEqual(adaptive_quota({'slow':1},{'slow':1},.3),.1)
  self.assertAlmostEqual(adaptive_quota({'slow':0},{'slow':1},.3),.3)
  self.assertAlmostEqual(adaptive_quota({'slow':.5},{'slow':.5},.3),.2)
  self.assertAlmostEqual(adaptive_quota({'slow':.5},{'slow':1},.3),.3)
 def test_rare_minimum_does_not_recover_discarded_rows(self):
  labels=np.array(['rare']*20+['common']*80);existing=np.array([0,1,20,21]);current=np.arange(22,70)
  result,_=update_balanced_rare_buffer(existing,current,labels,capacity=10,rng=np.random.default_rng(3),rare_group={'rare'},rare_fraction=.3)
  self.assertEqual(len(result),10);self.assertEqual(len(set(result)),10)
  self.assertTrue(set(result)<=set(existing)|set(current));self.assertEqual(sum(labels[result]=='rare'),2)
if __name__=='__main__':unittest.main()
