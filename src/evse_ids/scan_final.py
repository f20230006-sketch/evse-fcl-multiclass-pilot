"""Final scan merge and paired-statistics helpers; no continual-model training."""
import numpy as np

SCAN_TYPES = ('Aggressive_Scan','OS_Fingerprinting','SYN_Stealth_Scan',
              'Service_Version_Detection','TCP_Port_Scan','Vulnerability_Scan')
RARE_TYPES = ('Slowloris_Scan','ICMP_Fragmentation')
CORE = ['old_task_accuracy','forgetting','rare_attack_recall','worst_client_macro_recall']
EXTRA = ['accuracy','attack_accuracy','macro_recall','false_alarm_rate',
         'auroc_macro_ovr','auprc_macro_ovr_average_precision','rare_attack_macro_recall']

def scan_mapping(classes):
    if not set(SCAN_TYPES).issubset(classes):raise ValueError('Six original scan types are required')
    names=['Benign']+sorted((set(classes)-set(SCAN_TYPES)-{'Benign'})|{'Scan'})
    mapping=np.array([names.index('Scan' if c in SCAN_TYPES else c) for c in classes])
    return names,mapping

def merge_probabilities(probability,mapping,count):
    probability=np.asarray(probability)
    if probability.shape[1]!=len(mapping):raise ValueError('Class mapping mismatch')
    result=np.column_stack([probability[:,mapping==i].sum(axis=1,dtype=np.float64) for i in range(count)])
    if not np.isfinite(result).all() or not np.allclose(result.sum(1),1,atol=1e-6):raise ValueError('Invalid merged probabilities')
    return result

def paired_interval(values):
    a=np.asarray(values,dtype=float)
    if len(a)!=10 or not np.isfinite(a).all():raise ValueError('Require all ten finite seed differences')
    mean=float(a.mean());sd=float(a.std(ddof=1));half=2.2621571628*sd/np.sqrt(10)
    return {'n_seed_pairs':10,'mean_difference':mean,'std_difference':sd,
            'ci95_low':mean-half,'ci95_high':mean+half,
            'significance':'significant' if mean-half>0 or mean+half<0 else 'not significant'}
