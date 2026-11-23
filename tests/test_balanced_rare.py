import unittest
import numpy as np
from evse_ids.balanced_rare_allocator import update_balanced_rare_buffer


class BalancedRareTests(unittest.TestCase):
    def allocate(self, labels, cap=60, fraction=.2):
        return update_balanced_rare_buffer([], np.arange(len(labels)), labels, capacity=cap,
            rng=np.random.default_rng(42), rare_group={'rare_a','rare_b'}, rare_fraction=fraction)

    def test_reservation_and_remaining_balance(self):
        labels=np.repeat(['Benign','common','rare_a','rare_b'],100)
        rows, audit=self.allocate(labels)
        self.assertEqual(len(rows),60)
        self.assertEqual(len(set(rows)),60)
        self.assertEqual(len(audit['reserved_rows']),12)
        self.assertTrue(np.isin(labels[audit['reserved_rows']],['rare_a','rare_b']).all())
        counts=[sum(labels[audit['balanced_rows']]==c) for c in np.unique(labels)]
        self.assertEqual(counts,[12]*4)

    def test_absent_rare_and_shortages_redistributed(self):
        labels=np.array(['Benign']*2+['common']*100)
        rows,a=self.allocate(labels)
        self.assertEqual(len(rows),60)
        self.assertEqual(len(a['reserved_rows']),0)
        self.assertEqual(sum(labels[rows]=='Benign'),2)

    def test_rare_shortage_and_small_pool(self):
        labels=np.array(['common']*100+['rare_a']*3)
        rows,a=self.allocate(labels)
        self.assertEqual(len(a['reserved_rows']),3)
        self.assertEqual(len(rows),60)
        rows,a=self.allocate(['Benign','rare_a'],cap=60)
        self.assertEqual(rows.tolist(),[0,1])

    def test_no_discarded_history(self):
        labels=np.array(['common']*200)
        rows,_=update_balanced_rare_buffer([1,2], [9,10],labels,capacity=60,
            rng=np.random.default_rng(0),rare_group={'rare_a'},rare_fraction=.1)
        self.assertEqual(rows.tolist(),[1,2,9,10])

if __name__=='__main__': unittest.main()
