from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
m=json.loads((root/'deliverables_manifest.json').read_text(encoding='utf-8'))
bad=[]
for row in m['files']:
 p=root/row['path']
 if not p.is_file() or p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
print(json.dumps({'checked':len(m['files']),'mismatches':bad},indent=2))
raise SystemExit(bool(bad))
