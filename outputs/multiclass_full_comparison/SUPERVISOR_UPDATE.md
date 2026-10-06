# Supervisor update: completed multiclass comparison

The requested experiment has been executed on the original CICEVSE data: 10 training seeds, three attack orders, both federated and pooled centralized learning, and seven methods. The additional supplied datasets were excluded. Persistent roles and Task-1-only preprocessing were retained.

## Protected versus uniform replay

**Federated:** protected replay old-task accuracy = 42.78%, uniform = 35.31%; rare-attack recall = 86.48% versus 67.18%; worst-client macro recall = 30.85% versus 29.43%.

**Centralized:** protected replay old-task accuracy = 51.61%, uniform = 43.75%; rare-attack recall = 95.28% versus 69.52%; worst-client macro recall = 39.57% versus 38.68%.

The federated-minus-centralized difference in the protected-over-uniform old-task improvement is **-0.39 percentage points**, with paired-seed 95% interval [-4.28, 3.50]. This compares separately calibrated procedures on a fixed split, not a general causal claim that federation improves retention.

## What is included

The full result table includes no replay, EWC, A-GEM (Adam adaptation), joint/offline reference and FedProx. Every client, attack type and task checkpoint is reported in the CSV evidence, alongside all tried calibration settings and recorded fixed choices.

## What remains limited

The original test set still has 16 genuine benign flows and the benign-starved client has no benign evaluation examples. Proceeding despite this was explicitly authorized; this unmet data requirement is not described as solved. The study has ten training seeds on one fixed sample/split, not ten independent datasets. Source/session-level generalization and manuscript readiness require separate assessment.

Please assess the actual protected-versus-uniform and federated-versus-centralized results before finalizing the four-page Networking Letters claims. No old logistic-result improvement claims were reused.
