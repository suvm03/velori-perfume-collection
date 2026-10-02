"""Create compact web previews and complete downloadable design archives."""
from pathlib import Path
import json
import zipfile
from PIL import Image

root=Path(__file__).resolve().parents[1]
assets=root/'assets';downloads=root/'downloads'
assets.mkdir(exist_ok=True);downloads.mkdir(exist_ok=True)
designs=json.loads((root/'Source_Files/concepts.json').read_text())
(assets/'collection-data.js').write_text('window.VELORI_DESIGNS = '+json.dumps(designs,ensure_ascii=False)+';\n',encoding='utf-8')
paper=(245,242,235)
for c in designs:
    f=root/'Individual_Bottle_Designs'/(c['code']+'_'+c['name'].replace(' ','_').replace('.',''))
    output=assets/'designs'/c['code'];output.mkdir(parents=True,exist_ok=True)
    paths={p.stem:p for p in f.glob('*.png')}
    paths['Packaging']=root/'Packaging_Concepts'/(c['code']+'_Retail.png')
    for name,p in paths.items():
        with Image.open(p) as im:
            if name=='Front':
                # Remove the external image caption while retaining the label.
                ratio=im.width/720
                im=im.crop(tuple(round(v*ratio) for v in (40,25,680,580)))
            width=640 if name=='Front' else 1200
            im.thumbnail((width,1600),Image.Resampling.LANCZOS)
            im.save(output/(name+'.webp'),quality=88,method=6)
    with zipfile.ZipFile(downloads/(c['code']+'_Design_Pack.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(f.iterdir()):
            if p.is_file():z.write(p,p.relative_to(root))
        for p in sorted((root/'Packaging_Concepts').glob(c['code']+'_*')):z.write(p,p.relative_to(root))
hero=Image.new('RGB',(1500,720),paper)
for j,code in enumerate(['V01','V18','V24']):
    c=next(c for c in designs if c['code']==code)
    f=root/'Individual_Bottle_Designs'/(c['code']+'_'+c['name'].replace(' ','_').replace('.',''))
    with Image.open(f/'Perspective.png') as im:
        ratio=im.width/720
        im=im.crop(tuple(round(v*ratio) for v in (150,55,590,555)))
        im.thumbnail((490,600 if j==1 else 510),Image.Resampling.LANCZOS)
        hero.paste(im,(j*500+(500-im.width)//2,110 if j==1 else 170))
hero.save(assets/'hero.webp',quality=92,method=6)
for name in ['Gift_Discovery','Gift_Little_Magic','Display_Campaign','Colour_Atlas']:
    with Image.open(root/'Packaging_Concepts'/(name+'.png')) as im:
        im.thumbnail((1200,1400),Image.Resampling.LANCZOS);im.save(assets/(name+'.webp'),quality=88,method=6)
with zipfile.ZipFile(downloads/'VELORI_Complete_Collection.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['Individual_Bottle_Designs','Packaging_Concepts','Source_Files','assets']:
        for p in sorted((root/name).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(root))
    for name in ['Perfume_Collection_Master_Catalogue.pdf','Technical_Drawings.pdf','README.md','index.html','styles.css','app.js','Quality_Checks/Verification_Report.json']:
        z.write(root/name,name)
print(f'Generated {len(designs)} web galleries, 24 individual ZIPs and complete collection ZIP.')
from package_downloads import refresh_complete_archive
refresh_complete_archive()
