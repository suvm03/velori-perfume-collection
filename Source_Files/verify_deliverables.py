from pathlib import Path
import json
import fitz
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
out=root/'Quality_Checks';out.mkdir(exist_ok=True)
report={'pdfs':{},'image_checks':{},'notes':['All visual assets are conceptual vector artwork.','RGB presentation PDFs are not PDF/X-certified press releases.']}
for filename,expected in [('Perfume_Collection_Master_Catalogue.pdf',60),('Technical_Drawings.pdf',24)]:
    doc=fitz.open(root/filename)
    assert len(doc)==expected
    thumbs=[];blank=[];outside=[]
    for i,p in enumerate(doc):
        # Every page is rasterised at 150 dpi to catch malformed resources.
        pix=p.get_pixmap(dpi=150,alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        extrema=im.getextrema()
        if max(b-a for a,b in extrema)<15: blank.append(i+1)
        for block in p.get_text('dict')['blocks']:
            if block['type']!=0: continue
            for line in block['lines']:
                for span in line['spans']:
                    r=fitz.Rect(span['bbox'])
                    if r.x0 < -1 or r.y0 < -1 or r.x1>p.rect.width+1 or r.y1>p.rect.height+1:outside.append(i+1)
        im.thumbnail((180,255)); thumbs.append(im.copy())
        if filename.startswith('Perfume') and i in [0,4,5,6,25,26,52,53,54,56,57,58,59]:
            pix.save(str(out/f'Catalogue_Page_{i+1:02}.png'))
    for start in range(0,len(thumbs),20):
        sheet=Image.new('RGB',(1000,4*290),'#DDD9D1');draw=ImageDraw.Draw(sheet)
        for j,im in enumerate(thumbs[start:start+20]):
            x=10+(j%5)*200;y=8+(j//5)*290
            sheet.paste(im,(x,y));draw.text((x,y+259),f'Page {start+j+1}',fill='#152B3C')
        sheet.save(out/(filename.replace('.pdf','')+f'_Contact_{start//20+1}.png'))
    report['pdfs'][filename]={'pages':len(doc),'pages_rendered_at_150_dpi':len(doc),'blank_pages':blank,'out_of_bounds_text_pages':sorted(set(outside)),'size_bytes':(root/filename).stat().st_size}
    assert not blank and not outside
    doc.close()
folders=list((root/'Individual_Bottle_Designs').iterdir());assert len(folders)==24
for folder in folders:
    specs=json.loads((folder/'Specifications.json').read_text())
    pngs=list(folder.glob('*.png'));assert len(pngs)==8
    for p in pngs:
        with Image.open(p) as im:
            im.verify()
        with Image.open(p) as im: assert im.width>=2400
    report['image_checks'][specs['code']]={'pngs':len(pngs),'minimum_width_px':2400,'shape':specs['shape']}
assert len({r['shape'] for r in report['image_checks'].values()})==24
cartons=list((root/'Packaging_Concepts').glob('*_Carton_Concept.pdf'));assert len(cartons)==24
for p in cartons:
    with fitz.open(p) as d:d[0].get_pixmap(dpi=100)
extras=list((root/'Packaging_Concepts').glob('*.pdf'))
for path in extras:
    with fitz.open(path) as d:
        for page in d: page.get_pixmap(dpi=100)
report['packaging_carton_pdfs_rendered']=len(cartons)
report['all_packaging_pdfs_rendered']=len(extras)
report['verified']=True
(out/'Verification_Report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'verified':True,'master_pages':60,'technical_pages':24,'bottle_pngs':192,'carton_pdfs':24,'blank_pages':0,'out_of_bounds_text_pages':0},indent=2))
