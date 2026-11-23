"""CBRS memory population: Chrysakis and Moens (ICML 2020), Algorithm 1."""
from __future__ import annotations
import numpy as np

class CBRS:
    def __init__(self, capacity, classes, rng):
        if capacity<=0:raise ValueError('Positive replay capacity required')
        self.capacity=int(capacity);self.rng=rng
        self.slots=np.full(capacity,-1,dtype=np.int64);self.slot_classes=np.full(capacity,-1,dtype=np.int64)
        self.stored=np.zeros(classes,dtype=np.int64);self.encountered=np.zeros(classes,dtype=np.int64)
        self.full=np.zeros(classes,dtype=bool);self.size=0

    def mark_largest_full(self):
        # The supplementary proof defines largest/full status in a FILLED memory.
        if self.size==self.capacity:self.full[self.stored==self.stored.max()]=True

    def add(self, row, label):
        row,label=int(row),int(label);self.encountered[label]+=1
        if self.size<self.capacity:
            position=self.size;self.size+=1
        else:
            self.mark_largest_full()
            if not self.full[label]:
                largest=np.flatnonzero(self.stored==self.stored.max())
                candidates=np.flatnonzero(np.isin(self.slot_classes,largest))
                position=int(self.rng.choice(candidates))
            else:
                probability=self.stored[label]/self.encountered[label]
                u=self.rng.random()
                if self.stored[label]==0 or u>probability:return 'rejected'
                position=int(self.rng.choice(np.flatnonzero(self.slot_classes==label)))
            self.stored[self.slot_classes[position]]-=1
        self.slots[position]=row;self.slot_classes[position]=label;self.stored[label]+=1
        self.mark_largest_full()
        return 'stored'

    def ingest(self, rows, labels):
        outcomes={'stored':0,'rejected':0}
        for row in rows:outcomes[self.add(row,labels[row])]+=1
        memory=np.sort(self.slots[:self.size].copy())
        assert len(memory)==len(set(memory)) and len(memory)<=self.capacity
        return memory,{'reservoir_slots':self.slots[:self.size].tolist(),
            'encountered_class_counts':self.encountered.tolist(),'stored_class_counts':self.stored.tolist(),
            'full_classes':np.flatnonzero(self.full).tolist(),'outcomes':outcomes}
