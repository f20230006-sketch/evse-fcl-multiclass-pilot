import copy
import tempfile
import unittest
from pathlib import Path

import numpy as np
import torch

from evse_ids.full_comparison import empirical_fisher, projected_gradient, quadratic_penalty, train_client
from evse_ids.multiclass_pilot import TrafficMLP, seed_everything
from evse_ids.continual_ablation import update_replay_buffer


class FullComparisonTests(unittest.TestCase):
    def test_agem_projection_respects_reference_gradient(self):
        current = torch.tensor([-2., 1.])
        reference = torch.tensor([1., 0.])
        projected, changed = projected_gradient(current,reference)
        self.assertTrue(changed)
        self.assertGreaterEqual(float(torch.dot(projected,reference)),0)
        unchanged, changed = projected_gradient(reference,reference)
        self.assertFalse(changed)
        self.assertTrue(torch.equal(unchanged,reference))

    def test_fisher_is_mean_of_individual_squared_gradients(self):
        seed_everything(42)
        model = TrafficMLP(2,3)
        x = torch.tensor([[1.,-1.],[-1.,1.],[2.,1.]])
        y = torch.tensor([0,1,2])
        fisher, rows = empirical_fisher(model,x,y,np.arange(3),[0,1,2],np.random.default_rng(42),128)
        manual = {name:torch.zeros_like(p) for name,p in model.named_parameters()}
        for row in rows:
            loss = torch.nn.functional.cross_entropy(model(x[row:row+1]),y[row:row+1])
            gradients = torch.autograd.grad(loss,list(model.parameters()))
            for (name,_),g in zip(model.named_parameters(),gradients):
                manual[name] += g.square()/3
        self.assertTrue(all(torch.allclose(fisher[name],value,atol=1e-6) for name,value in manual.items()))

    def test_ewc_penalty_zero_at_anchor_and_positive_after_movement(self):
        model = TrafficMLP(2,3)
        anchor = {name:p.detach().clone() for name,p in model.named_parameters()}
        importance = {name:torch.ones_like(p) for name,p in model.named_parameters()}
        self.assertEqual(float(quadratic_penalty(model,anchor,importance).detach()),0)
        with torch.no_grad(): next(model.parameters()).add_(1)
        self.assertGreater(float(quadratic_penalty(model,anchor,importance).detach()),0)

    def test_protected_memory_preserves_available_groups_and_capacity(self):
        labels = np.array(["Benign"]*20+["Slowloris_Scan"]*20+["UDP_Flood"]*200)
        rows = update_replay_buffer([],np.arange(len(labels)),labels,capacity=60,strategy="protected",rng=np.random.default_rng(42),
                                   protected_groups=[{"Benign"},{"Slowloris_Scan"}],minimum_fraction=.2)
        self.assertEqual(len(rows),60)
        self.assertGreaterEqual(int((labels[rows]=="Benign").sum()),12)
        self.assertGreaterEqual(int((labels[rows]=="Slowloris_Scan").sum()),12)

    def test_all_methods_reject_evaluation_rows_in_memory(self):
        data = {"x":torch.zeros(3,2),"y":torch.tensor([0,1,2]),"roles":np.array(["fitting","fitting","evaluation"])}
        with self.assertRaises(AssertionError):
            train_client(TrafficMLP(2,3),data,np.array([0,1]),np.array([2]),[0,1,2],
                         {"local_epochs":1,"batch_size":2,"weight_decay":0},"uniform_60",{"learning_rate":.003,"replay_fraction":.5},[],np.random.default_rng(42))

    def test_optimizer_baselines_produce_finite_local_models(self):
        seed_everything(42)
        data = {"x":torch.tensor([[-1.,0.],[1.,0.],[0.,1.]]*5),"y":torch.tensor([0,1,2]*5),"roles":np.array(["fitting"]*15)}
        model = TrafficMLP(2,3)
        anchor = {name:p.detach().clone() for name,p in model.named_parameters()}
        fisher = {name:torch.ones_like(p) for name,p in model.named_parameters()}
        for method,settings,terms in [("ewc",{"ewc_lambda":1},[(anchor,fisher)]),
                                      ("agem",{"reference_batch_size":4},[]),
                                      ("fedprox_no_replay",{"proximal_mu":.01},[]),
                                      ("protected_60",{"replay_fraction":.5},[])]:
            local,info = train_client(model,data,np.arange(12),np.arange(12,15),[0,1,2],
                {"local_epochs":1,"batch_size":4,"weight_decay":0},method,{"learning_rate":.003,**settings},terms,np.random.default_rng(42))
            self.assertTrue(all(torch.isfinite(p).all() for p in local.parameters()))
            self.assertGreater(info["steps"],0)


if __name__ == "__main__": unittest.main()
