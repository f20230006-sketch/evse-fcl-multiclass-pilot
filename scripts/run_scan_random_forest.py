"""The only new training: pooled six-scan Random Forest, calibration-only selection."""
from pathlib import Path
import hashlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.append(str(ROOT/'work/scan_diagnostic_dependencies'))
import numpy as np
import pandas as pd
import torch
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,balanced_accuracy_score,confusion_matrix,log_loss
from evse_ids.scan_final import SCAN_TYPES,paired_interval
from evse_ids.multiclass_pilot import save_json

def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    out=ROOT/'outputs/final_scan_analysis/random_forest';out.mkdir(parents=True,exist_ok=True)
    base=ROOT/'outputs/multiclass_full_comparison';orders=['order_1','order_2','order_3'];prepared={};source={}
    config={'scan_types':list(SCAN_TYPES),'seeds':list(range(42,52)),'calibration_seed':42,'orders':orders,'n_estimators':200,'max_features':'sqrt','class_weight':None,'bootstrap':True,'n_jobs':3,'grid':[{'max_depth':None,'min_samples_leaf':1},{'max_depth':16,'min_samples_leaf':5}],'selection':'calibration balanced accuracy, tie first candidate','training_scope':'pooled scan-only fitting rows; no continual model training','near_chance_band_percentage_points':5,'no_refit_on_calibration':True}
    for order in orders:
        path=base/'splits'/order/'prepared_local_only.pt';prepared[order]=torch.load(path,weights_only=False,map_location='cpu');source[str(path.relative_to(ROOT))]=sha(path)
    for p in ['scripts/run_scan_random_forest.py','src/evse_ids/scan_final.py']:source[p]=sha(ROOT/p)
    fingerprint=hashlib.sha256(json.dumps({'config':config,'inputs':source},sort_keys=True).encode()).hexdigest()
    protocol=out/'protocol_before_evaluation.json'
    if protocol.exists():assert json.loads(protocol.read_text())['fingerprint']==fingerprint,'Changed scan protocol: use a new output'
    save_json(protocol,{'config':config,'source_and_input_hashes':source,'fingerprint':fingerprint,'sklearn_version':sklearn.__version__,'numpy_version':np.__version__})
    datasets={};trials=[];chosen={}
    for order,data in prepared.items():
        ids=[data['classes'].index(c) for c in SCAN_TYPES];mask=np.isin(data['y'].numpy(),ids)
        role_rows={r:np.flatnonzero(mask&(data['roles']==r)) for r in ['fitting','calibration','evaluation']}
        for r in role_rows:
            assert len(role_rows[r]) and len(np.unique(role_rows[r]))==len(role_rows[r])
        assert not set(role_rows['fitting'])&set(role_rows['evaluation'])
        datasets[order]=(data,role_rows,ids)
        x=data['x'].numpy();y=data['y'].numpy()
        for i,settings in enumerate(config['grid']):
            start=time.monotonic();model=RandomForestClassifier(n_estimators=config['n_estimators'],max_features='sqrt',n_jobs=3,random_state=42,**settings)
            model.fit(x[role_rows['fitting']],y[role_rows['fitting']]);pred=model.predict(x[role_rows['calibration']])
            trials.append({'order':order,'trial':i,**settings,'calibration_balanced_accuracy':balanced_accuracy_score(y[role_rows['calibration']],pred),'elapsed_seconds':time.monotonic()-start})
            print(json.dumps(trials[-1]),flush=True)
        best=max([r for r in trials if r['order']==order],key=lambda r:(r['calibration_balanced_accuracy'],-r['trial']));chosen[order]=config['grid'][best['trial']]
    save_json(out/'calibration_trials.json',{'test_data_used':False,'trials':trials,'selected':chosen});pd.DataFrame(trials).to_csv(out/'calibration_trials.csv',index=False)
    records=[];classes=[]
    for order,(data,role_rows,ids) in datasets.items():
        x=data['x'].numpy();y=data['y'].numpy()
        save_json(out/f'{order}_role_indices.json',{r:rows.tolist() for r,rows in role_rows.items()})
        for seed in config['seeds']:
            path=out/order/f'seed_{seed}';path.mkdir(parents=True,exist_ok=True)
            model=RandomForestClassifier(n_estimators=200,max_features='sqrt',n_jobs=3,random_state=seed,**chosen[order]);model.fit(x[role_rows['fitting']],y[role_rows['fitting']])
            rows=role_rows['evaluation'];prob=model.predict_proba(x[rows]);pred=model.classes_[prob.argmax(1)];truth=y[rows];cm=confusion_matrix(truth,pred,labels=model.classes_)
            training_pred=model.predict(x[role_rows['fitting']]);values={'order':order,'seed':seed,'settings':chosen[order],'accuracy':accuracy_score(truth,pred),'balanced_accuracy':balanced_accuracy_score(truth,pred),'fitting_accuracy':accuracy_score(y[role_rows['fitting']],training_pred),'log_loss':log_loss(truth,prob,labels=model.classes_),'rows':len(rows),'feature_importance':model.feature_importances_.tolist()}
            np.savez_compressed(path/'evaluation_predictions.npz',sample_index=rows,y_true=truth,y_pred=pred,probability=prob,probability_class_ids=model.classes_)
            save_json(path/'results.json',values);records.append(values)
            pd.DataFrame(cm,index=[data['classes'][i] for i in model.classes_],columns=[data['classes'][i] for i in model.classes_]).rename_axis('true_class').to_csv(path/'confusion_matrix.csv')
            for i,c in enumerate(model.classes_):classes.append({'order':order,'seed':seed,'class':data['classes'][c],'support':int(cm[i].sum()),'recall':float(cm[i,i]/cm[i].sum())})
            print(json.dumps({k:values[k] for k in ['order','seed','accuracy','fitting_accuracy']}),flush=True)
    f=pd.DataFrame([{k:v for k,v in r.items() if k!='feature_importance'} for r in records]);f.to_csv(out/'per_run_metrics.csv',index=False);pd.DataFrame(classes).to_csv(out/'per_class_metrics.csv',index=False)
    seed_mean=f.groupby('seed')[['accuracy','balanced_accuracy','fitting_accuracy','log_loss']].mean();seed_mean.to_csv(out/'per_seed_order_averaged.csv')
    chance=1/6;ci=paired_interval(seed_mean.balanced_accuracy.to_numpy()-chance)
    summary={'runs':30,'calibration_trials':6,'chance_accuracy':chance,'accuracy_mean':seed_mean.accuracy.mean(),'accuracy_std':seed_mean.accuracy.std(ddof=1),'balanced_accuracy_mean':seed_mean.balanced_accuracy.mean(),'balanced_accuracy_std':seed_mean.balanced_accuracy.std(ddof=1),'fitting_accuracy_mean':seed_mean.fitting_accuracy.mean(),'accuracy_above_chance':ci,'practically_near_chance':bool(abs(seed_mean.balanced_accuracy.mean()-chance)<=.05),'near_chance_definition':'within 5 percentage points of balanced six-class chance; descriptive, not proof of equivalence','selected':chosen}
    save_json(out/'summary.json',summary);save_json(out/'completion.json',{'status':'complete','runs':30,'fingerprint':fingerprint});print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
