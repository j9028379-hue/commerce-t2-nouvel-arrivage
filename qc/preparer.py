from pathlib import Path as P
import sys,json,hashlib,subprocess as sp,os
from jsonschema import validate
from shutil import copyfile
sys.path.insert(0,str(P('audio').resolve()));from rotation import choisir
J=lambda p:json.loads(P(p).read_text());save=lambda p,x:P(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n');H=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest();out=P('livraison');out.mkdir(exist_ok=True);plan=J('reverse-engineering/effets.json');c=J('audio/catalogue.json');entry,=J('catalogue/catalogue.json')['entries'];assert entry['contrat']=='reverse-engineering/effets.json' and all(plan[k]==entry[k] for k in ['version','template_id','audio_profile']) and c['audio_profile']==entry['audio_profile'] and not entry['ota_implemented'];validate(plan,J('schemas/template.json'));job=J('livraison/job.json');validate(job,J('schemas/render-job.json'));assert job==J('golden/job.json'), 'La narration Sillon Studio ne doit jamais être utilisée pour un autre commerce';assert [x['scene'] for x in job['captures']]==['S1','S2','S3','S4'] and len({x['sha256'] for x in job['captures']})==4
ids=[t['id'] for t in c['pistes']];assert ids==[162190,303023,260353,300338] and set(ids).isdisjoint([354907,573944]);seq=set();old=None
for i in range(10000):
 pick=choisir(ids,str(i),old);assert pick!=old and choisir(ids,str(i),old)==pick;seq.add(pick);old=pick
assert seq==set(ids)
for prev in ids:
 for bad in [prev,354907,573944,5]:
  try:choisir(ids,'x',prev,bad)
  except ValueError:continue
  raise AssertionError('piste non autorisée acceptée')
 assert {choisir(ids,str(i),prev) for i in range(100)}==set(ids)-{prev}
for k in ('accroche','prix','produit','nom','quartier','whatsapp'):
 bad=json.loads(json.dumps(job));del bad['reponses'][k]
 from jsonschema import ValidationError
 try:validate(bad,J('schemas/render-job.json'))
 except ValidationError:continue
 raise AssertionError('champ manquant accepté')
assert H('work/master.mp4')==J('audio/voix.json')['master_sha256'];save(out/'cq-architecture.json',dict(canon=entry,reference='P1@c656510 ; Commerce-T1@186e46a',schemas=True,mutations_refusees=6,decisions_simulees=10000,parcours=job['ecrans'],reference_visuelle_sha256=H('work/master.mp4'),worker='handlers lecture seule + Wrangler dry-run',non_certifie=['Android/caméra matérielle','OTA signé, installation et rollback','Cloudflare de production','validation humaine du mix final']))
