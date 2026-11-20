"""Étape finale seulement, après réussite du job film et publication de l’artefact."""
import subprocess as s,json,base64,os,hashlib
from pathlib import Path as P
repo='repos/'+os.environ['GITHUB_REPOSITORY'];path=repo+'/contents/autoplay/etat.json';api=lambda *a:json.loads(s.check_output(['gh','api',*a]));rr=json.loads(P('rotation.json').read_text());assert rr['commit']==os.environ['GITHUB_SHA'] and rr['apres']['run_id']==os.environ['GITHUB_RUN_ID'];assert hashlib.sha256(P('COMMERCE-T2-Voix-Afrobeat.mp4').read_bytes()).hexdigest()==rr['apres']['render_sha256'];item=api(path+'?ref=state/commerce-autoplay');old=json.loads(base64.b64decode(item['content']));new=rr['apres'];assert old==new or (old==rr['avant'] and old['last_success']!=new['last_success']);
if old!=new:
  commit=api('-X','PUT',path,'-f','branch=state/commerce-autoplay','-f','sha='+item['sha'],'-f','message=Confirmer le rendu contrôlé '+new['run_id'],'-f','content='+base64.b64encode((json.dumps(new,indent=2)+'\n').encode()).decode());print(commit['commit']['html_url'])
