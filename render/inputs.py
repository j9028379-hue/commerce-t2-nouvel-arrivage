import json,hashlib,subprocess
from pathlib import Path
p=Path('work');p.mkdir(exist_ok=True)
for r in json.loads(Path('render/demo/rushs.json').read_text()):
 f=p/(r['scene']+'.mp4');subprocess.run(['curl','-fLsS','--retry','3','--max-time','120',r['url'],'-o',str(f)],check=True);assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
