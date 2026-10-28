import sys,unittest
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from evse_ids.cbrs import CBRS

def reference(labels,capacity,seed):
    rng=np.random.default_rng(seed);memory=[];counts=Counter();full=set();trace=[]
    def mark():
        if len(memory)==capacity:
            sizes=Counter(labels[i] for i in memory);largest=max(sizes.values());full.update(c for c,n in sizes.items() if n==largest)
    for row,c in enumerate(labels):
        c=int(c);counts[c]+=1
        if len(memory)<capacity:memory.append(row)
        else:
            mark();sizes=Counter(labels[i] for i in memory)
            if c not in full:
                largest=max(sizes.values());candidates=[i for i,r in enumerate(memory) if sizes[labels[r]]==largest]
                memory[int(rng.choice(candidates))]=row
            else:
                u=rng.random();own=[i for i,r in enumerate(memory) if labels[r]==c]
                if own and u<=len(own)/counts[c]:memory[int(rng.choice(own))]=row
        mark();trace.append((memory.copy(),full.copy(),dict(counts)))
    return trace

class CBRSTests(unittest.TestCase):
    def test_independent_reference_every_step(self):
        labels=np.array([0]*17+[1]*3+[2]*40+[3]+[4]*22+[0]*8+[1]*6)
        for capacity in [2,7,15]:
            for seed in range(8):
                state=CBRS(capacity,5,np.random.default_rng(seed));expected=reference(labels,capacity,seed)
                for row,c in enumerate(labels):
                    state.add(row,c);slots,full,counts=expected[row]
                    self.assertEqual(state.slots[:state.size].tolist(),slots)
                    self.assertEqual(set(np.flatnonzero(state.full)),full)
                    self.assertEqual(state.encountered.tolist(),[counts.get(i,0) for i in range(5)])
    def test_full_only_after_fill_and_persistent(self):
        s=CBRS(4,3,np.random.default_rng(2))
        for i,c in enumerate([0,1,1]):s.add(i,c)
        self.assertFalse(s.full.any());s.add(3,1);self.assertTrue(s.full[1])
        s.add(4,2);s.add(5,2);self.assertTrue(s.full[1]);self.assertEqual(s.encountered.sum(),6)
    def test_rare_class_preserved(self):
        labels=np.array([0]+[1]*100+[2]*100)
        s=CBRS(12,3,np.random.default_rng(42));rows,_=s.ingest(np.arange(len(labels)),labels)
        self.assertIn(0,rows);self.assertEqual(len(rows),12);self.assertEqual(len(set(rows)),12)
    def test_chunking_does_not_reset_state(self):
        labels=np.array([0]*20+[1]*20+[2]*20)
        a=CBRS(9,3,np.random.default_rng(7));b=CBRS(9,3,np.random.default_rng(7))
        whole,_=a.ingest(np.arange(60),labels)
        for rows in [np.arange(20),np.arange(20,40),np.arange(40,60)]:part,_=b.ingest(rows,labels)
        self.assertTrue(np.array_equal(whole,part));self.assertTrue(np.array_equal(a.encountered,b.encountered))

if __name__=='__main__':unittest.main()
