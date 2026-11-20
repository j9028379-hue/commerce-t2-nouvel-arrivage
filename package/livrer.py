from pathlib import Path as P,PurePosixPath
import sys,json,zipfile,subprocess,hashlib
from jsonschema import validate
H=lambda b:hashlib.sha256(b).hexdigest()
def verify(z):
 with zipfile.ZipFile(z) as f:
  names=f.namelist();m=json.loads(f.read('MANIFEST.json'));validate(m,json.loads(f.read('schemas/package.json')));rows={t['path']:t for t in m['files']};assert len(names)==len(set(names)) and len(rows)==len(m['files']) and set(names)==set(rows)|{'MANIFEST.json'}
  for n,t in rows.items():
   assert not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and not n.endswith('.mp3');b=f.read(n);assert (len(b),H(b))==(t['bytes'],t['sha256'])
  return m
if __name__=='__main__':
 z=P(sys.argv[-1]);
 if sys.argv[1]=='verify':print(len(verify(z)['files']));sys.exit()
 files={n:P(n) for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n};files['media/master-silencieux.mp4']=P('work/master.mp4');q=P('livraison');files.update({'media/'+p.name:p for p in sorted((q/'ecoutes').glob('*.mp4'))});assert len([n for n in files if n.startswith('media/')])==5
 for p in list(q.glob('*.json'))+list((q/'ecoutes').glob('*.json')):files['preuves/'+p.name]=p
 with zipfile.ZipFile(z,'w') as f:
  rows=[]
  def write(n,b):
   info=zipfile.ZipInfo(n,(2026,1,1,0,0,0));info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;f.writestr(info,b)
  for n,p in sorted(files.items()):
   b=p.read_bytes();write(n,b);rows.append(dict(path=n,bytes=len(b),sha256=H(b),role=n.split('/')[0]))
  write('MANIFEST.json',json.dumps(dict(template_id='COMMERCE-T2',version='1.0.0',schema_version='1.0.0',commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),files=rows),ensure_ascii=False).encode())
 verify(z)
