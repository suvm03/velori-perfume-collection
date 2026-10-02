"""Download pinned, MIT-licensed Three.js modules for self-hosted previews."""
from pathlib import Path
import urllib.request
root=Path(__file__).resolve().parents[1]/'assets/vendor'
version='0.180.0'
files={'three.module.js':'build/three.module.js','three.core.js':'build/three.core.js','OrbitControls.js':'examples/jsm/controls/OrbitControls.js','RoomEnvironment.js':'examples/jsm/environments/RoomEnvironment.js','RoundedBoxGeometry.js':'examples/jsm/geometries/RoundedBoxGeometry.js','LICENSE':'LICENSE'}
root.mkdir(parents=True,exist_ok=True)
for name,path in files.items():
    request=urllib.request.Request(f'https://cdn.jsdelivr.net/npm/three@{version}/{path}',headers={'User-Agent':'VELORI-site-build'})
    data=urllib.request.urlopen(request,timeout=30).read()
    (root/name).write_bytes(data)
    print(name,len(data))
