"""Run the browser checks against the published GitHub Pages site."""
from pathlib import Path
import urllib.request
import json

base='https://suvm03.github.io/velori-perfume-collection/'
paths=['','assets/vendor/three.module.js','assets/bottle-profiles.js','Perfume_Collection_Master_Catalogue.pdf','Technical_Drawings.pdf','downloads/VELORI_Complete_Collection.zip','downloads/V01_Design_Pack.zip']
responses=[]
for path in paths:
    with urllib.request.urlopen(urllib.request.Request(base+path,method='HEAD'),timeout=30) as response:
        assert response.status==200
        responses.append({'path':path,'status':response.status})
print(json.dumps(responses,indent=2),flush=True)
script=Path(__file__).with_name('check_website.py')
source=script.read_text(encoding='utf-8').replace("url=f'http://127.0.0.1:{server.server_address[1]}/'",f'url={base!r}')
exec(compile(source,str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})
