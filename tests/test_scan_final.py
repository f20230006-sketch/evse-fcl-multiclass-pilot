import unittest
import numpy as np
from evse_ids.scan_final import SCAN_TYPES,scan_mapping,merge_probabilities,paired_interval

class ScanFinalTests(unittest.TestCase):
    def test_only_six_requested_types_merge(self):
        names=['Benign',*sorted(SCAN_TYPES),'Slowloris_Scan','ICMP_Fragmentation'];merged,mapping=scan_mapping(names)
        self.assertEqual(len(merged),4);self.assertNotEqual(mapping[names.index('Slowloris_Scan')],merged.index('Scan'))
        self.assertEqual(len(set(mapping[1:7])),1)

    def test_summing_can_change_winner_and_preserves_mass(self):
        names=['Benign',*SCAN_TYPES,'Slowloris_Scan'];merged,mapping=scan_mapping(names)
        p=np.array([[.01,.1,.1,.1,.1,.1,.1,.39]])
        q=merge_probabilities(p,mapping,len(merged))
        self.assertEqual(names[p.argmax(1)[0]],'Slowloris_Scan');self.assertEqual(merged[q.argmax(1)[0]],'Scan');self.assertAlmostEqual(q.sum(),1)

    def test_interval_requires_ten_seed_pairs(self):
        with self.assertRaises(ValueError):paired_interval([1,2,3])
        self.assertEqual(paired_interval(np.ones(10)*.1)['significance'],'significant')
        self.assertEqual(paired_interval(np.arange(-5,5))['significance'],'not significant')

if __name__=='__main__':unittest.main()
