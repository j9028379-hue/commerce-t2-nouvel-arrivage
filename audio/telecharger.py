from pathlib import Path as P
import json,subprocess as s,hashlib
p=P('work/music-cache');p.mkdir(exist_ok=True,parents=True)
for t in json.loads(P('audio/catalogue.json').read_text())['pistes']:
 f=p/(str(t['id'])+'.mp3');s.run(['curl','-fLsS','--retry','3','--max-time','90',t['source_mp3'],'-o',str(f)],check=True);assert f.stat().st_size==t['octets'] and hashlib.sha256(f.read_bytes()).hexdigest()==t['sha256']
