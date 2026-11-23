import unittest
import numpy as np
from evse_ids.continual_ablation import update_replay_buffer

class BalancedReplayTests(unittest.TestCase):
    def test_equal_allocation_despite_majority(self):
        labels=np.array(['a']*100+['b']*20+['c']*20)
        rows=update_replay_buffer([],np.arange(len(labels)),labels,capacity=60,strategy='balanced',rng=np.random.default_rng(42))
        self.assertEqual([int((labels[rows]==c).sum()) for c in ['a','b','c']],[20,20,20])

    def test_shortage_redistributed_without_duplicates(self):
        labels=np.array(['a']*100+['b']*2+['c']*100)
        rows=update_replay_buffer([],np.arange(len(labels)),labels,capacity=60,strategy='balanced',rng=np.random.default_rng(42))
        self.assertEqual(len(rows),60);self.assertEqual(len(np.unique(rows)),60)
        self.assertEqual([int((labels[rows]==c).sum()) for c in ['a','b','c']],[29,2,29])

    def test_no_access_to_discarded_history(self):
        labels=np.array(['a']*20+['b']*100)
        rows=update_replay_buffer([1,2,3],np.arange(20,120),labels,capacity=10,strategy='balanced',rng=np.random.default_rng(42))
        self.assertTrue(set(rows).issubset(set([1,2,3])|set(range(20,120))))
        self.assertEqual(int((labels[rows]=='a').sum()),3)

    def test_remainder_is_at_most_one(self):
        labels=np.repeat(['a','b','c'],100)
        rows=update_replay_buffer([],np.arange(300),labels,capacity=61,strategy='balanced',rng=np.random.default_rng(42))
        counts=[int((labels[rows]==c).sum()) for c in ['a','b','c']]
        self.assertLessEqual(max(counts)-min(counts),1)

if __name__=='__main__':unittest.main()
