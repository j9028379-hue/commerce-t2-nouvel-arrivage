import sys,zipfile,tempfile
from pathlib import Path as P
sys.path.insert(0,str(P('package').resolve()));from livrer import verify
src=P(sys.argv[1]);m=verify(src)
with tempfile.TemporaryDirectory() as td:
 bad=P(td)/'test.zip'
 with zipfile.ZipFile(src) as srczip,zipfile.ZipFile(bad,'w') as out:
  for n in srczip.namelist():
   b=srczip.read(n);out.writestr(n,b+b'!' if n=='catalogue/catalogue.json' else b)
 try: verify(bad)
 except AssertionError:print('PASS :',len(m['files']),'fichiers vérifiés ; modification du catalogue refusée.')
 else:raise RuntimeError('Altération acceptée')
