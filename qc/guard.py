"""Conserver un RenderError exploitable et échouer sans modifier le registre de rotation."""
import sys,json,subprocess
from pathlib import Path
from jsonschema import validate
stage,*command=sys.argv[1:];r=subprocess.run(command)
if r.returncode:
 p=Path('livraison/RenderError.json');p.parent.mkdir(exist_ok=True);e=dict(status='FAILED',stage=stage,message=f'Code de sortie {r.returncode} : voir la première erreur du journal GitHub');validate(e,json.loads(Path('schemas/render-error.json').read_text()));p.write_text(json.dumps(e,ensure_ascii=False,indent=2));sys.exit(r.returncode)
