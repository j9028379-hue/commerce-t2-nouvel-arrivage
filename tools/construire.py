from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]; text=(root/'tools/parcours.html.in').read_text()
for k,p in [('__QUESTIONS__','form/questions.json'),('__SCREENS__','capture-guide/ecrans.json')]:
    data=json.loads((root/p).read_text()); text=text.replace(k,json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))
(root/'docs/index.html').write_text(text)
