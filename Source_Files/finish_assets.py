"""Additional editable brand, gift, label and palette assets; run after build_collection.py."""
from pathlib import Path
import json, html
import fitz

root=Path(__file__).resolve().parents[1]
cs=json.loads((root/'Source_Files/concepts.json').read_text())
paper='#F5F2EB';ink='#152B3C'
def svg(body,w,h,unit=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}{unit}" height="{h}{unit}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="{paper}"/>{body}</svg>'
def render(s,path,width=3000):
    with fitz.open(stream=s.encode(),filetype='svg') as d:
        d[0].get_pixmap(matrix=fitz.Matrix(width/d[0].rect.width,width/d[0].rect.width)).save(str(path))
def text(x,y,t,size,color=ink):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial" font-size="{size}" text-anchor="middle">{html.escape(t)}</text>'
for c in cs:
    folder=root/'Individual_Bottle_Designs'/(c['code']+'_'+c['name'].replace(' ','_').replace('.',''))
    w,h=c['label_mm']
    s=svg(text(w/2,h*.30,'V E L O R I',h*.15)+text(w/2,h*.57,c['name'].upper(),h*.11)+text(w/2,h*.80,f"{c['capacity_ml']} mL / CONCEPT",h*.075),w,h,'mm')
    (folder/'Label.svg').write_text(s,encoding='utf-8')
    with fitz.open(stream=s.encode(),filetype='svg') as d:
        p=fitz.open('pdf',d.convert_to_pdf());p.save(root/'Packaging_Concepts'/(c['code']+'_Label_Concept.pdf'));p.close()

body=text(500,55,'VELORI / COLOUR & MATERIAL ATLAS',27)
for i,c in enumerate(cs):
    x=35+(i%4)*245;y=95+(i//4)*112
    body+=text(x+110,y,c['code']+' / '+c['name'],13)
    for j,col in enumerate(c['palette']):
        body+=f'<rect x="{x+j*54}" y="{y+12}" width="48" height="35" rx="3" fill="{col}" stroke="#BBB6AB"/>'+text(x+j*54+24,y+63,col,8)
palette=svg(body,1000,800)
(root/'Source_Files/Colour_Atlas.svg').write_text(palette,encoding='utf-8')
render(palette,root/'Packaging_Concepts/Colour_Atlas.png')

gift=svg(text(500,55,'VELORI / LITTLE MAGIC / PARENT & CHILD RITUAL',24)+
    '<polygon points="130,165 460,165 545,100 215,100" fill="#F4E7D7"/><polygon points="460,165 545,100 545,500 460,565" fill="#CFA985"/><rect x="130" y="165" width="330" height="400" fill="#F4E7D7" stroke="#526575"/>'+
    text(295,230,'V E L O R I',28)+text(295,305,'LITTLE MAGIC',24)+text(295,350,'A PARENT-CONTROLLED RITUAL',14)+
    '<rect x="610" y="180" width="280" height="345" rx="5" fill="#FFFFFF" stroke="#CFA985"/>'+
    text(750,240,'FOR THE ADULT',23)+text(750,295,'APPLICATION GUIDANCE',14)+text(750,340,'COPY SUBJECT TO SAFETY REVIEW',11)+text(750,395,'ONE BOTTLE / NO LOOSE GIFTS',12)+text(500,625,'PAPERBOARD GIFT CARTON + ADULT INSTRUCTION CARD / CONCEPT ONLY',13),1000,680)
(root/'Packaging_Concepts/Gift_Little_Magic.svg').write_text(gift,encoding='utf-8')
render(gift,root/'Packaging_Concepts/Gift_Little_Magic.png')

with fitz.open() as d:
    for s in [palette,gift]:
        with fitz.open(stream=s.encode(),filetype='svg') as v:
            a=fitz.open('pdf',v.convert_to_pdf());p=d.new_page(width=595.276,height=841.89);p.show_pdf_page(fitz.Rect(20,80,575,760),a,0);a.close()
    d.save(root/'Packaging_Concepts/Brand_And_Gift_Supplement.pdf')
print('Added true-size conceptual labels, colour atlas and parent gift concept.')
with fitz.open(root/'Perfume_Collection_Master_Catalogue.pdf') as d:
    d.set_toc([[1,'VELORI / Collection proposal',1],[1,'Brand & design philosophy',2],[1,'Age groups & collection overview',4]]+[[1,c['collection'],6+2*i] for i,c in enumerate(cs) if i==0 or c['group']!=cs[i-1]['group']]+[[1,'Packaging & campaign',54],[1,'Manufacturing',56],[1,'Safety & regulatory considerations',57],[1,'Product comparison',59],[1,'Final presentation',60]])
    d.saveIncr()
with fitz.open(root/'Technical_Drawings.pdf') as d:
    d.set_toc([[1,c['code']+' / '+c['name'],i+1] for i,c in enumerate(cs)])
    d.saveIncr()
readme=root/'README.md'
readme.write_text(readme.read_text(encoding='utf-8').replace('Run `python Source_Files/build_collection.py` from any directory.','Run `python Source_Files/build_all.py` from any directory to rebuild and verify all deliverables.'),encoding='utf-8')
