"""Rendu silencieux de contrôle : consomme le job exporté du navigateur, jamais les exemples."""
from pathlib import Path as P
import json, hashlib, os, subprocess as sp
import cv2 as cv, numpy as np
from PIL import Image,ImageDraw,ImageFont
cv.setNumThreads(2)
read=lambda p:json.loads(P(p).read_text());sha=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest()
plan=read('reverse-engineering/effets.json'); sources=read('render/demo/rushs.json');job=read('livraison/job.json');ans=job['reponses'];W,H,F,N=[plan['format_propose'][k] for k in ['width','height','fps','frames']];out=P('livraison/COMMERCE-T2-Nouvel-arrivage.mp4');assert job['template_id']==plan['template_id'] and job['ecrans']==list(range(1,13));assert set(ans)=={q['cle'] for q in read('form/questions.json')['champs']};assert [c['scene'] for c in job['captures']]==['S1','S2','S3','S4'];assert len(job['captures'])==len(sources)==len(plan['scenes'])==4
# Réponses seules pour les données commerciales. Les libellés courts sont du lettrage fixe.
def fit(img,w,h,x=.5,y=.5,z=1):
 ih,iw=img.shape[:2];scale=max(w/iw,h/ih)*z;cw,ch=min(iw,round(w/scale)),min(ih,round(h/scale));left=int(np.clip(x*iw-cw/2,0,iw-cw));top=int(np.clip(y*ih-ch/2,0,ih-ch));return cv.resize(img[top:top+ch,left:left+cw],(w,h),interpolation=cv.INTER_LINEAR)
def zoom(img,z):return fit(img,W,H,z=z)
fonts='/usr/share/fonts/truetype/dejavu/';warm=(240,222,186);cream=(251,245,230);sage=(209,192,157)
def layer(j,phase):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 def text(x,y,txt,size=35,face='Sans',color=cream,maxw=624):
  while size>12:
   f=ImageFont.truetype(fonts+'DejaVu'+face+'.ttf',size)
   if d.textlength(txt,font=f)<=maxw:break
   size-=1
  d.text((x,y),txt,font=f,fill=color,anchor='la',stroke_width=1,stroke_fill=(38,27,17,130))
 # Un seul groupe compact, sur la photo, loin des commandes du lecteur.
 if j==0:
  text(46,858,ans['nom'],35,'Sans',warm);text(43,922,ans['produit'],61,'Serif')
 elif j==1:
  if phase==0:text(46,940,ans['accroche'],50,'Serif')
  else:text(46,888,'PRIX',21,'Sans',warm);text(42,930,ans['prix'],65,'Serif')
 elif j==3:
  if phase==0:text(46,884,ans['nom'],49,'Serif');text(47,959,ans['quartier'],31,'Sans',warm)
  else:text(46,881,'Commander sur WhatsApp',30,'Sans',warm);text(43,947,ans['whatsapp'],48,'Serif')
 a=np.array(im);return a[:,:,:3][:,:,::-1],a[:,:,3:4]/255.
cache={(j,p):layer(j,p) for j in [0,1,3] for p in [0,1]};xx=np.linspace(0,1,W,dtype='f4')[None,:];yy=np.linspace(0,1,H,dtype='f4')[:,None];grad=(1-.83*np.clip((yy-.56)/.33,0,1))[:,:,None];prev=None;done=set();samples=[];texts=[];video=sp.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(F),'-i','pipe:0','-map','0:v:0','-an','-c:v','libx264','-preset','veryfast','-crf','17','-threads','3','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=sp.PIPE)
for j,(s,meta,capt) in enumerate(zip(plan['scenes'],sources,job['captures'])):
 p=P('work')/(s['id']+'.mp4');assert s['id']==meta['scene']==capt['scene'] and capt['valide'] and sha(p)==capt['sha256']==meta['sha256'];cap=cv.VideoCapture(str(p));rate=cap.get(cv.CAP_PROP_FPS);first,last=s['images_sortie'];cursor=-1;current=None
 for i in range(first,last):
  pos=int((meta['debut_s']+(i-first)/F)*rate);assert pos<cap.get(cv.CAP_PROP_FRAME_COUNT)
  while cursor<pos:
   good,current=cap.read();assert good;cursor+=1
  e=next((g for g in plan['effets'] if g['images_t2'][0]<=i<g['images_t2'][1]),None);z=1;black=0
  if e:
   a,b=e['images_t2'];t=i-a;r=t/max(1,b-a-1);op=e['id'];done.add(op);z=np.interp(r,[0,1],e.get('zoom',[1,1]));alpha=lambda key:np.interp(t,*np.asarray(e[key]).T)
  # Vrai plein cadre : toute la surface vient du rush, à proportions constantes.
  u=(i-first)/max(1,last-first-1);u=u*u*(3-2*u);cx=np.interp(u,*np.array(plan['cadrage']['trajectoires'][j]).T)
  img=fit(current,W,H,cx,z=min(z,plan['cadrage']['zoom_max']))
  if e:
   if op in ('ambre','chaleur','ombre','noir'):
    amt=alpha('opacite');hx=e['couleur_sRGB'].lstrip('#');color=tuple(bytes.fromhex(hx)[::-1]);
    if op=='noir':black=amt
    else:img=cv.addWeighted(img,1-amt,np.full_like(img,color),amt,0)
   elif op=='reflet':
    cx,cy=(1-r)*np.array(e['centre_xy'][0])+r*np.array(e['centre_xy'][1]);rx,ry=e['rayon_xy'];mask=(alpha('opacite')*np.exp(-2*(((xx-cx)/rx)**2+((yy-cy)/ry)**2)))[:,:,None];color=np.array(list(bytes.fromhex(e['couleur_sRGB'][1:]))[::-1])/255;img=np.uint8(img+(255-img)*mask*color)
   elif op=='double':
    amt=alpha('alpha_entrant');img=cv.addWeighted(zoom(prev,np.interp(r,[0,1],e['zoom_sortant'])),1-amt,img,amt,0)
   elif op=='recul':
    amt=alpha('opacite');alt=zoom(img,np.interp(r,[0,1],e['zoom_copie']));img=cv.addWeighted(img,1-amt,cv.GaussianBlur(alt,(0,0),e['sigma_max_px']),amt,0)
  if i==419:prev=img.copy()
  if j!=2:
   phase=int((j==1 and i>=294) or (j==3 and i>=755));a,b=([(8,177)] if j==0 else ([(187,291),(294,408)] if j==1 else [(643,750),(755,878)]))[phase];visibility=np.clip(min((i-a)/8,(b-i)/8),0,1)
   img=np.uint8(img*(1-.36*visibility*np.exp(-((yy-.745)/.15)**2)[:,:,None]))
   rgb,alp=cache[j,phase];v=alp*visibility;img=np.uint8(img*(1-v)+rgb*v)
  if black:img=cv.convertScaleAbs(img,alpha=1-black)
  if i in (75,226,340,524,704,831):samples.append(cv.resize(img,(180,320)))
  video.stdin.write(img.tobytes())
 cap.release();texts.append([ans[k] for k in s['donnees_ecran']]);
video.stdin.close();assert video.wait()==0;assert done=={e['id'] for e in plan['effets']};info=json.loads(sp.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));stream,=info['streams'];assert (stream['codec_type'],stream['codec_name'],stream['width'],stream['height'],stream['nb_read_frames'],stream['avg_frame_rate'])==('video','h264',W,H,str(N),'30/1');assert abs(float(info['format']['duration'])-30)<.001
cv.imwrite('livraison/Controle-images.jpg',np.hstack(samples));P('livraison/controle.json').write_text(json.dumps(dict(run=os.getenv('GITHUB_RUN_ID'),commit=os.getenv('GITHUB_SHA'),images=N,fps=F,dimensions=[W,H],audio_streams=0,sha256=sha(out),cadrage=plan['cadrage'],textes_commerciaux=texts,effets=sorted(done),sources=sources,demo='Commerce, tarif et contact fictifs. Plans Mixkit Stock Video Free License.'),indent=2,ensure_ascii=False));print('PASS 900 images H.264, zéro flux audio, 4 prises, 13 effets, six réponses en provenance du navigateur')
