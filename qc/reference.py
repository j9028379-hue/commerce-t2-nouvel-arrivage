from pathlib import Path as P
import cv2,numpy as np,json
r=P('livraison');a=cv2.VideoCapture('work/master.mp4');b=cv2.VideoCapture(str(r/'COMMERCE-T2-Nouvel-arrivage.mp4'));errors=[]
for i in range(900):
  ok,x=a.read();ok2,y=b.read();assert ok and ok2 and x.shape==y.shape==(1280,720,3);small=lambda z:cv2.resize(z,(36,64),interpolation=cv2.INTER_AREA).astype(float);errors.append(float(abs(small(x)-small(y)).mean()))
assert not a.read()[0] and not b.read()[0] and max(errors)<1.5,max(errors);q=json.loads((r/'cq-architecture.json').read_text());q['comparaison_900_images']={'max_mae_sur_miniature':max(errors),'seuil':1.5,'master_utilise_dans_le_mix':'fichier public approuvé, pas sa reconstruction'};(r/'cq-architecture.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
