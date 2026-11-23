from pathlib import Path
import sys,json,hashlib,datetime
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from evse_ids.multiclass_pilot import TrafficMLP,predict
OUT=ROOT/'outputs/validation_extension_report_2026_11_12';torch.set_num_threads(1)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 model_count=0;checkpoint_count=0;prediction_rows=0;memory_updates=0;max_diff=0.;calibration_count=0;timing={}
 for track,parent in [('independent_ocpp',ROOT/'outputs/validation_extension_2026_11_12/independent_ocpp'),('original',ROOT/'outputs/original_rare_groups_2026_11_12')]:
  selection=parent/'selected_before_evaluation.json'; selected=json.loads(selection.read_text())['selected']
  evalstamps=list((parent/'runs').rglob('complete.json'));calstamps=list((parent/'calibration').rglob('complete.json'))
  assert len(evalstamps)==(300 if track=='independent_ocpp' else 120);assert len(calstamps)==(96 if track=='independent_ocpp' else 48)
  assert max(p.stat().st_mtime for p in calstamps)<=selection.stat().st_mtime<=min(p.stat().st_mtime for p in evalstamps)
  timing[track]={'all_calibration_finished_before_selection_and_evaluation':True,'calibration_fits':len(calstamps),'evaluated_models':len(evalstamps)}
  cache={order:torch.load(parent/'prepared'/order/'prepared.pt',weights_only=False,map_location='cpu') for order in ['order_1','order_2','order_3']}
  for stamp in calstamps+evalstamps:
   meta=json.loads(stamp.read_text());data=cache[meta['order']];directory=stamp.parent
   if meta['calibration_only']:calibration_count+=1
   else:
    model=TrafficMLP(data['x'].shape[1],len(data['classes']));state=torch.load(directory/'final_model.pt',weights_only=True,map_location='cpu');assert all(torch.isfinite(t).all() for t in state.values());model.load_state_dict(state)
    result=json.loads((directory/'results.json').read_text())
    for step in result['history']:
     with np.load(directory/f"checkpoint_{step['checkpoint']}_predictions.npz") as z:
      assert (data['roles'][z['sample_index']]=='evaluation').all();prediction_rows+=len(z['y_true']);checkpoint_count+=1
    last=result['history'][-1]
    with np.load(directory/f"checkpoint_{last['checkpoint']}_predictions.npz") as z:
     q=predict(model,data['x'],z['sample_index'],last['seen_classes']);difference=float(np.max(np.abs(q-z['probability'])));assert difference<1e-6;max_diff=max(max_diff,difference)
    model_count+=1
    key='|'.join(meta[k] for k in (['order','environment','method','group'] if track=='independent_ocpp' else ['order','environment','group']))
    assert selected[key]['settings']==meta['settings']
   for audit in json.loads((directory/'memory_audit.json').read_text()):
    ids=np.array(audit['memory_rows'],int);assert len(ids)==len(set(ids.tolist())) and len(ids)<=audit['capacity'];assert (data['roles'][ids]=='fitting').all();memory_updates+=1
  if track=='independent_ocpp':
   data=cache['order_1'];manifest=data['manifest'];roles=data['roles'];groups=manifest.group.astype(str).to_numpy()
   for a,b in [('fitting','calibration'),('fitting','evaluation'),('calibration','evaluation')]:assert not set(groups[roles==a])&set(groups[roles==b])
 assert model_count==420 and calibration_count==144
 prior=json.loads((ROOT/'outputs/validation_extension_2026_11_12/prior_artifact_lock.json').read_text());assert all(sha(ROOT/p)==h for p,h in prior.items())
 inputs=json.loads((OUT/'input_sha256.json').read_text());assert all(sha(ROOT/p)==h for p,h in inputs.items())
 verification={'status':'passed','new_models_reproduced':model_count,'calibration_fits_checked':calibration_count,'new_checkpoints_checked':checkpoint_count,'new_prediction_rows_checked':prediction_rows,'memory_updates_checked':memory_updates,'maximum_probability_reproduction_difference':max_diff,'reference_prediction_files_unchanged':len(inputs),'prior_paper_report_locks_unchanged':len(prior),'calibration_timing':timing,'no_evaluation_rows_in_replay':True,'all_new_models_finite':True,'all_selected_settings_used_without_retuning':True,'connection_groups_role_disjoint':True,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (OUT/'deep_verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps(verification,indent=2))
if __name__=='__main__':main()
