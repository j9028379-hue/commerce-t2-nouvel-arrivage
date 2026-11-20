"""Entrées réelles et mix hors réseau. Les clips de voix IA de la démo ne sont pas utilisés."""
import argparse,hashlib,json,sys,subprocess as sp,os,fcntl
from pathlib import Path as P
import numpy as np
from jsonschema import validate,ValidationError
ROOT=P(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'audio'));from mixer import main as mixer,decode,R,H,db,level;from rotation import choisir
J=lambda p:json.loads(P(p).read_text());
def atom(p,d):
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2));os.replace(tmp,p)
def run(src,out,state,cache,jid):
 src,out,state,cache=(p.resolve() for p in [src,out,state,cache]);out.mkdir(parents=True,exist_ok=True);stage='JOB';
 try:
  job=J(src/'job.json');validate(job,J(ROOT/'schemas/render-job.json'));clips=job['captures'];assert [x['scene'] for x in clips]==['S1','S2','S3','S4'] and len({c['sha256'] for c in clips})==4 and all(H(src/(c['scene']+'.mp4'))==c['sha256'] for c in clips);atom(out/'job.json',job);stage='VIDEO';sp.run([sys.executable,str(ROOT/'render/film.py')],cwd=ROOT,env={**os.environ,'T2_INPUT':str(src),'T2_OUTPUT':str(out)},check=True);stage='AUDIO';v=np.zeros((30*R,2),np.float32)
  for c,sc in zip(clips,J(ROOT/'reverse-engineering/effets.json')['scenes']):
   path=src/(c['scene']+'.mp4');has=sp.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=index','-of','csv=p=0',str(path)]).strip()
   if has:
    a,b=[k*R//30 for k in sc['images_sortie']];raw=decode(path)[:b-a];v[a:a+len(raw)]=raw
  if np.max(abs(v))>.005:
   li,tp=level(v);v*=db(min(-20-li,-3-tp))
  os.environ['COMMERCE_MUSIC_CACHE']=str(cache);ids=[r['id'] for r in J(ROOT/'audio/catalogue.json')['pistes']];state.parent.mkdir(parents=True,exist_ok=True)
  with state.with_suffix('.lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);pick=choisir(ids,jid,J(state)['last_success'] if state.exists() else None);mixer(out/'COMMERCE-T2-Nouvel-arrivage.mp4',out/'mix',v,pick);m,=J(out/'mix/controle-mixes.json')['versions'];result=dict(status='COMPLETED',template_id='COMMERCE-T2',run_id=jid,sha256=m['sha256'],output='mix/'+m['mp4'],music_id=pick);validate(result,J(ROOT/'schemas/render-result.json'));atom(out/'RenderResult.json',result);atom(state,{'last_success':pick});return result
 except (AssertionError,ValueError,ValidationError,KeyError,OSError,sp.CalledProcessError) as exc:
  error=dict(status='FAILED',stage=stage,message=str(exc)[:500] or 'Vérification refusée');validate(error,J(ROOT/'schemas/render-error.json'));atom(out/'RenderError.json',error);return error
if __name__=='__main__':
 a=argparse.ArgumentParser();[a.add_argument('--'+k,type=P,required=True) for k in ['job','out','state','cache']];a.add_argument('--id',required=True);o=a.parse_args();r=run(o.job,o.out,o.state,o.cache,o.id);print(r);sys.exit(r['status']!='COMPLETED')
