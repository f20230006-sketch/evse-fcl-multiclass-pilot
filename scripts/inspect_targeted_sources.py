"""Read-only provenance/grouping and public baseline feasibility checks."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import pandas as pd
from evse_ids.data import infer_label_from_filename
from evse_ids.multiclass_pilot import save_json
out=ROOT/'outputs/targeted_validation_2026_10_27';out.mkdir(exist_ok=True,parents=True)
records=[]
for p in sorted((ROOT/'data/official/network_traffic').rglob('*.csv')):
    columns=pd.read_csv(p,nrows=0).columns.tolist()
    fields=[c for c in columns if c.lower()=='id' or c.lower().endswith('_id') or any(w in c.lower() for w in ['session','capture','pcap','first_seen','last_seen','src_ip','dst_ip'])]
    records.append({'file':str(p.relative_to(ROOT/'data/official/network_traffic')),'inferred_label':infer_label_from_filename(p.name),'candidate_fields':fields})
frame=pd.read_pickle(ROOT/'outputs/multiclass_full_comparison/sampled_fixed.pkl')
coverage=frame.groupby(['__source_file__','Label']).size().rename('sampled_rows').reset_index();coverage.to_csv(out/'source_file_class_coverage.csv',index=False)
stats=[]
for f,g in frame.groupby('__source_file__'):
    for col in ['id','expiration_id','bidirectional_first_seen_ms','bidirectional_last_seen_ms']:
        if col in g:stats.append({'file':f,'column':col,'sampled_rows':len(g),'unique_values':int(g[col].nunique()),'missing':int(g[col].isna().sum())})
pd.DataFrame(stats).to_csv(out/'identifier_sample_stats.csv',index=False)
save_json(out/'grouping_check.json',{'files':records,'source_file_group_available':True,'explicit_capture_or_session_column':sorted({c for r in records for c in r['candidate_fields'] if any(w in c.lower() for w in ['session','capture','pcap'])}),'interpretation':'Source CSV filename is an available provenance group and can support a file-held-out design. Flow id/expiration id and timestamps are present but are not documented session identities. No explicit capture/session column was found. The fixed sample has 59 source files; benign and Slowloris each span only two files, so whole-file assignment to fitting/calibration/evaluation cannot give those classes support in all three roles. No new group-separated pipeline was built, as requested. Current random-role splits do not establish capture/session independence.','sampled_file_count':len(coverage['__source_file__'].unique())})
repo=ROOT/'work/FedCBDR-public-review'
main=repo/'main.py';tree=ast.parse(main.read_text(encoding='utf-8'));missing=[]
for n in ast.walk(tree):
    if isinstance(n,ast.ImportFrom) and n.module and n.module.startswith(('utils.','methods.')):
        target=repo/(n.module.replace('.','/')+'.py')
        if not target.exists():missing.append(n.module)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
save_json(out/'fedcbdr_feasibility.json',{'url':'https://github.com/qizhuang-qz/FedCBDR','commit':commit,'public_code_exists':True,'missing_direct_local_imports':missing,'readme_method':'C','implemented_methods_in_dispatch':['icarl','ewc','lwf','finetune','target','lander','a','b','re_fed'],'image_pipeline':True,'cuda_calls':True,'decision':'Do not run an invented partial baseline. Checkout lacks several directly imported local modules and README method C is not dispatched. Remaining code expects image arrays/PIL, image datasets/ResNet and CUDA; faithful tabular MLP port requires substantial reconstruction. Use requested explicit related-work distinction instead.','method_difference':'FedCBDR globally coordinates class-level replay construction and changes logit/objective balancing; our allocator uses only local prior memory plus current fitting rows and adds no allocation-related communication.'})
print('Grouping and FedCBDR checks saved; commit',commit,'missing modules',missing)
