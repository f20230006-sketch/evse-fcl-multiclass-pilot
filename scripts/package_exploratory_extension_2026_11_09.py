"""Package frozen-baseline status and both exploratory outcomes, with no omitted losses."""
from pathlib import Path
import hashlib,json,re,shutil,zipfile
import pandas as pd
from pypdf import PdfReader,PdfWriter
R=Path('D:/EV-charging');D=R/'outputs/exploratory_extension_deliverables_2026_11_09';D.mkdir(exist_ok=True)
P=R/'manuscripts/ieee_networking_letters_extension_2026_11_09';S=(P/'main.tex').read_text(encoding='utf-8');old=R/'manuscripts/ieee_networking_letters_illustrated_2026_11_04'
assert len(PdfReader(P/'main.pdf').pages)==4
assert not re.search(r'Overfull|undefined references|Citation .* undefined',(P/'main.log').read_text())
assert (P/'tables/allocation_results.tex').read_bytes()==(old/'tables/allocation_results.tex').read_bytes()
f1=pd.read_csv(R/'outputs/asynchronous_replay_report_2026_11_09/summary.csv');f2=pd.read_csv(R/'outputs/distilled_replay_report_2026_11_09/summary.csv');pairs=pd.read_csv(R/'outputs/distilled_replay_report_2026_11_09/paired_intervals.csv')
checks=[]
for method in ['fixed_rbr','class_balanced_kd','fixed_rbr_kd']:
 row=f2[(f2.score_space=='merged_scans')&(f2.environment=='federated')&(f2.method==method)].iloc[0]
 for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']:
  for k in ['mean','std']:
   value=f'{100*row[m+"_"+k]:.2f}';assert value in (P/'tables/distillation_results.tex').read_text();checks.append(value)
for _,row in pairs[(pairs.score_space=='merged_scans')&(pairs.environment=='federated')&(pairs.left=='fixed_rbr_kd')&(pairs.right.isin(['fixed_rbr','class_balanced_kd']))&(pairs.metric!='forgetting')].iterrows():
 for name in ['mean_difference','ci95_low','ci95_high']:
  value=f'{100*row[name]:.2f}';assert value in S,(name,value);checks.append(value)
assert 'did not pass its prespecified federated screen' in S and 'exploratory' in S and 'independent confirmation' in S
vp={'status':'passed','pages':4,'original_primary_table_unchanged':True,'new_table_and_interval_values_checked':len(checks),'references':len(re.findall(r'\\bibitem\{',S)),'all_pages_visually_inspected':True,'negative_first_study_disclosed':True}
(P/'verification.json').write_text(json.dumps(vp,indent=2));shutil.copy2(P/'verification.json',D/'manuscript_verification.json')
for source in ['asynchronous_replay','distilled_replay']:
 report=R/f'outputs/{source}_report_2026_11_09';v=json.loads((report/'verification.json').read_text());assert v['status']=='passed' and v['all_frozen_files_unchanged']==19917
 copy=D/source;copy.mkdir(exist_ok=True)
 for p in report.iterdir():
  if p.is_file():shutil.copy2(p,copy/p.name)
 for name in ['protocol_before_evaluation.json','hyperparameter_trials.json','completion.json']:shutil.copy2(R/f'outputs/{source}_2026_11_09'/name,copy/name)
freeze=R/'outputs/frozen_paper_2026_11_09';assert json.loads((freeze/'VERIFICATION.json').read_text())['status']=='passed'
for n in ['SHA256.txt','VERIFICATION.json','README.md']:shutil.copy2(freeze/n,D/('freeze_'+n))
M=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall'];lines=['# Frozen baseline and exploratory extension results','', 'The current paper and all accepted baseline comparisons were frozen before new development. The self-contained archive contains19,917 verified files (2.17GB); every original file remained unchanged after both studies. This is a baseline comparison, not a universal state-of-the-art claim.','', 'Completed88 calibration fits and260 evaluations across two separately fixed designs. Six new unit tests passed. Verification covers260 models,1,560 checkpoints and7,222,280 prediction rows. All calibration fits precede evaluation within each study.','', '## Study1 adaptive quota','', 'Reused corpus, prospective role split62; one rare-first order; synchronized/delayed schedules and federated/centralized controls. The local calibration-driven controller did not pass its prespecified delayed-federated screen.','', '| Method | Old accuracy | Forgetting | Slowloris | Worst client |','|---|---:|---:|---:|---:|']
for method in ['class_balanced','cbrs','fixed_rbr','adaptive_rbr']:
 row=f1[(f1.score_space=='merged_scans')&(f1.environment=='federated')&(f1.schedule=='delayed')&(f1.method==method)].iloc[0];lines.append('| '+method+' | '+' | '.join(f'{100*row[m+"_mean"]:.2f} ± {100*row[m+"_std"]:.2f}'for m in M)+' |')
lines+=['','## Study2 teacher distillation','', 'Separate prospective role split63 of the same corpus; one rare-first delayed order; five methods and matched-capacity federated/centralized controls. The teacher mechanism is established prior art. The original paper remains frozen.','', '| Method | Old accuracy | Forgetting | Slowloris | Worst client |','|---|---:|---:|---:|---:|']
for method in ['class_balanced','cbrs','fixed_rbr','class_balanced_kd','fixed_rbr_kd']:
 row=f2[(f2.score_space=='merged_scans')&(f2.environment=='federated')&(f2.method==method)].iloc[0];lines.append('| '+method+' | '+' | '.join(f'{100*row[m+"_mean"]:.2f} ± {100*row[m+"_std"]:.2f}'for m in M)+' |')
lines+=['','Percentages, mean ± sample SD over ten training seeds. Do not compare scores directly across the two studies or with the original paper: partitions, training seeds and timing protocols differ.','', '## Matched primary gains in Study2','']
for _,r in pairs[(pairs.score_space=='merged_scans')&(pairs.environment=='federated')&(pairs.left=='fixed_rbr_kd')&(pairs.right=='fixed_rbr')].iterrows():lines.append(f'- {r.metric}: {100*r.mean_difference:+.2f} points;95% paired interval [{100*r.ci95_low:.2f},{100*r.ci95_high:.2f}].')
lines+=['','The prespecified exploratory screen passed: Slowloris improved and old/worst lower interval bounds exceeded the-1-point tolerance; all three improvements in fact had positive lower bounds.','', '## Qualifications that change the interpretation','', 'Against class-balanced plus the same teacher, distilled RBR improves Slowloris by9.60 points [0.76,18.44], while old accuracy+1.58 [-1.50,4.66] and worst-client-1.00 [-2.99,0.99] are not significant. Thus the teacher contributes to gains; non-inferiority to this stronger control is not established.','', 'The federated-minus-centralized distillation interaction is+4.79 points [0.93,8.65] for old accuracy and+11.08 [1.05,21.11] for Slowloris. These are exploratory, unadjusted intervals on one delayed order, not proof of a general federation-specific effect.','', 'The teacher adds model state and computation; the60-row/client budget matches stored replay examples, not total RAM. Both prospective partitions reuse a corpus already examined in earlier work. There is no independent external validation, and benign/fragmentation support remains limited.','', '## Paper status and next step','', 'FCL_IEEE_Networking_Letters_Extension.pdf is a separate four-page manuscript extension. Its original main comparison remains unchanged, new results are explicitly separated, and the unsuccessful adaptive study is disclosed. The original frozen manuscript is not replaced. Before promoting the new findings to main claims, prioritize predeclared confirmation across additional orders or independently collected/capture-separated data. Do not keep tuning against these evaluation partitions.','', '## Files','', '- The two study folders contain complete CSVs, paired intervals, interactions, client metrics, calibration records and verification.','- The raw archive contains the new models, predictions, prepared split tensors, memory audits, training logs, source and configurations.','- The2.17GB frozen archive stays separately at outputs/frozen_paper_2026_11_09/FCL_Paper_and_Baseline_Freeze.zip.','', 'Related primary sources: Learning without Forgetting (https://arxiv.org/abs/1606.09282); Online Continual Learning from Imbalanced Data/CBRS (https://proceedings.mlr.press/v119/chrysakis20a.html).']
(D/'RESULTS_SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')
w=PdfWriter();w.clone_document_from_reader(PdfReader(P/'main.pdf'));w.add_metadata({'/Title':'Rare-Reserved Balanced Replay with Exploratory Delayed-Client Extension','/Subject':'Original baseline comparison preserved with separately evaluated teacher-distillation extension'})
with (D/'FCL_IEEE_Networking_Letters_Extension.pdf').open('wb')as f:w.write(f)
source_paths=[p for p in (R/'src/evse_ids').glob('*.py')]
source_paths += [R/'configs'/f'{name}_2026_11_09.json'for name in ['asynchronous_replay','distilled_replay']]
source_paths += [R/'docs/research'/f'{name}_Design_2026_11_09.md'for name in ['Asynchronous_Replay','Distilled_Replay']]
source_paths += [R/'scripts'/f'{name}_{study}.py'for name in ['run','analyze','verify']for study in ['asynchronous_replay','distilled_replay']]
source_paths += [R/'tests'/f'test_{name}.py'for name in ['asynchronous_replay','distilled_replay']]
with zipfile.ZipFile(D/'FCL_Exploratory_Results_2026_11_09.zip','w',zipfile.ZIP_DEFLATED)as z:
 for p in D.rglob('*'):
  if p.is_file()and p.suffix!='.zip':z.write(p,str(p.relative_to(D)))
 for p in source_paths:z.write(p,'source/'+str(p.relative_to(R)))
 for p in P.rglob('*'):
  if p.is_file() and p.suffix in ['.tex','.pdf','.svg','.json','.md']and p.name!='main.pdf':z.write(p,'manuscript_source/'+str(p.relative_to(P)))
print('Small review package bytes:',(D/'FCL_Exploratory_Results_2026_11_09.zip').stat().st_size)
# Complete raw evidence for both new studies, separately from the small review package.
items=[]
with zipfile.ZipFile(D/'FCL_Exploratory_Raw_2026_11_09.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True)as z:
 for name in ['asynchronous_replay_2026_11_09','distilled_replay_2026_11_09']:
  for p in sorted((R/'outputs'/name).rglob('*')):
   if not p.is_file():continue
   raw=p.read_bytes();arc=str(p.relative_to(R));items.append({'path':arc,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()});z.writestr(arc,raw)
 for p in source_paths:z.write(p,'source/'+str(p.relative_to(R)))
 z.writestr('RAW_MANIFEST.json',json.dumps(items,indent=2))
for name in ['FCL_Exploratory_Results_2026_11_09.zip','FCL_Exploratory_Raw_2026_11_09.zip']:
 p=D/name
 with zipfile.ZipFile(p)as z:assert z.testzip()is None
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 (D/(name+'.sha256')).write_text(h+'  '+name+'\n')
 print(name,p.stat().st_size,'bytes; CRC passed')
print('All deliverables:',D)
