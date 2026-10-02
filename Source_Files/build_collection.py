from pathlib import Path
import json, math, html, csv
import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Individual_Bottle_Designs'; PACK=ROOT/'Packaging_Concepts'
for p in [OUT,PACK]: p.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/arial.ttf'
NAVY='#152B3C'; PAPER='#F5F2EB'
collections=[('Little Magic','3-5','Parent-controlled dab applicator; no spray'),('Wonder World','6-9','Parent-controlled roll-on; no spray'),('Junior Trend','10-12','Metered pump, subject to inhalation assessment'),('Teen Vibes','13-15','Metered fine-mist pump'),('Signature Youth','16-18','Metered fine-mist pump')]
# Every outline is a distinct manufacturable envelope; curves are smoothed by
# quadratic interpolation. Coordinates describe a 180 x 210 design envelope.
rows=[
('Hush Bear',0,'Unisex','teddy','#CFA985','#F4E7D7',30,62,88,36,'Broad bear silhouette; ears integrated into shell'),
('Cloudlet',0,'Girls','cloud','#B2C9E1','#F6DBE5',30,68,78,34,'Three soft cloud lobes; flat standing base'),
('Little Comet',0,'Boys','star','#E7BE68','#DDE7F2',25,62,85,33,'Rounded five-point star; inset neck'),
('Moon Nest',0,'Unisex','moon','#B5B3D8','#EEE7F6',30,58,90,35,'Crescent relief on an oval, no open handle'),
('Prism Pony',1,'Girls','unicorn','#D7B8DE','#E9DAF2',35,65,103,36,'Unicorn crest relief, broad blunt horn integrated'),
('Orbit One',1,'Boys','rocket','#91AEC9','#E06B54',35,54,112,38,'Rounded rocket shoulders with integral low fins'),
('Tidal Friend',1,'Unisex','dolphin','#77C5C4','#D5ECE7',35,70,96,35,'Dolphin arc embossed in a wave-shaped body'),
('Rainbow Arc',1,'Girls','arch','#E3A783','#C4D9C4',35,66,95,36,'Solid arch body with three recessed colour bands'),
('Cosmo Scout',1,'Boys','astronaut','#CBD5DC','#97B9DF',35,60,103,39,'Helmet silhouette with flush visor panel'),
('Kickoff',2,'Boys','football','#A3C3A2','#F0E8D6',40,65,92,43,'Truncated ball body on a broad stable foot'),
('Flutter Studio',2,'Girls','butterfly','#D8A4B7','#E4D3ED',40,78,98,34,'Broad butterfly wings, rounded internal corners'),
('Pixel Pulse',2,'Unisex','pixel','#B0A5D3','#B9D9D0',40,58,104,36,'Three-step pixel shoulder, softened edges'),
('Aero League',2,'Boys','shield','#7CABC1','#E5C06B',40,60,107,37,'Original shield with shallow centre spine'),
('Palette Pop',2,'Girls','palette','#D9947B','#EBCE87',40,72,93,35,'Asymmetric artist palette without finger hole'),
('Loop Lab',3,'Unisex','loop','#9DB5AA','#E5DBC7',50,64,112,38,'Offset oval with moulded loop relief'),
('Petal Edit',3,'Girls','petal','#C989A1','#E9D6CC',50,60,117,36,'Three fluted petal panels, tapering shoulder'),
('Night Circuit',3,'Boys','bevel','#697D9F','#B8CEDA',50,56,116,38,'Chamfered rectangular prism with diagonal relief'),
('Crystal Mood',3,'Girls','crystal','#ACA3CA','#E0D8EB',50,61,115,39,'Soft eight-facet crystal with broad plateau'),
('Waveform',3,'Unisex','wave','#88B8B7','#D2DCCB',50,63,110,37,'Alternating shallow wave sides, flat base'),
('Quiet Form',4,'Unisex','cylinder','#B7B5A5','#E9E4D9',60,49,127,49,'Minimal oval cylinder with low dome cap'),
('Slate No. 01',4,'Boys','slab','#697E83','#CFD2CA',60,65,115,30,'Wide slim slab, radiused corners'),
('Rose Axis',4,'Girls','teardrop','#BF928B','#EAD9D0',60,53,126,38,'Off-centre teardrop, flat base'),
('Amber Vertex',4,'Boys','hex','#B39367','#D9CDB8',60,58,119,40,'Hexagonal column with rounded vertical edges'),
('Equinox',4,'Unisex','lens','#94A4B1','#D8DDDF',60,70,110,31,'Flattened lens body with an arched shoulder')]
shapes={
'teddy':[(35,200),(20,173),(24,92),(32,55),(18,37),(25,16),(49,14),(62,35),(120,35),(132,14),(157,16),(164,37),(150,55),(158,92),(162,173),(145,200)],
'cloud':[(24,200),(16,172),(14,104),(25,81),(46,79),(45,59),(62,44),(81,45),(94,27),(116,28),(132,47),(151,55),(161,78),(160,173),(151,200)],
'star':[(45,200),(55,154),(15,126),(60,108),(75,45),(95,35),(112,107),(162,123),(122,155),(133,200)],
'moon':[(53,200),(26,169),(22,111),(35,61),(66,39),(110,36),(148,65),(158,116),(145,169),(124,200)],
'unicorn':[(33,200),(28,152),(34,94),(53,73),(47,44),(74,55),(95,24),(110,63),(139,80),(150,119),(147,173),(134,200)],
'rocket':[(42,200),(15,185),(28,134),(48,115),(51,74),(72,39),(90,25),(108,39),(130,74),(134,115),(153,134),(165,185),(139,200)],
'dolphin':[(22,200),(15,167),(33,139),(47,107),(69,85),(92,67),(113,36),(129,63),(159,79),(160,98),(138,107),(142,156),(156,200)],
'arch':[(31,200),(23,103),(28,72),(45,46),(69,31),(111,31),(135,46),(152,72),(157,103),(149,200)],
'astronaut':[(42,200),(29,177),(31,116),(20,98),(24,64),(43,39),(69,26),(112,26),(139,39),(156,64),(160,98),(149,116),(151,177),(138,200)],
'football':[(49,200),(26,172),(16,133),(26,85),(56,53),(90,44),(124,53),(154,85),(164,133),(154,172),(131,200)],
'butterfly':[(44,200),(22,177),(25,140),(12,101),(18,65),(47,49),(75,71),(90,95),(105,71),(133,49),(162,65),(168,101),(155,140),(158,177),(136,200),(90,178)],
'pixel':[(32,200),(32,102),(48,102),(48,73),(66,73),(66,41),(114,41),(114,73),(132,73),(132,102),(148,102),(148,200)],
'shield':[(69,200),(39,176),(23,148),(23,72),(56,48),(90,38),(124,48),(157,72),(157,148),(141,176),(111,200)],
'palette':[(36,200),(19,176),(18,133),(35,90),(64,58),(107,39),(143,56),(159,86),(146,108),(131,127),(143,154),(138,183),(113,200)],
'loop':[(39,200),(25,172),(25,100),(38,67),(69,38),(111,38),(142,64),(155,100),(155,172),(141,200)],
'petal':[(54,200),(33,170),(25,120),(39,84),(62,70),(72,40),(108,40),(118,70),(141,84),(155,120),(147,170),(126,200)],
'bevel':[(43,200),(28,186),(28,71),(50,42),(129,42),(153,66),(153,178),(136,200)],
'crystal':[(43,200),(20,157),(40,69),(69,34),(110,34),(140,69),(160,157),(137,200)],
'wave':[(40,200),(23,177),(33,144),(22,118),(35,89),(26,65),(52,43),(125,43),(153,65),(144,89),(157,118),(146,144),(157,177),(140,200)],
'cylinder':[(42,200),(36,184),(36,65),(47,46),(70,40),(110,40),(133,46),(144,65),(144,184),(138,200)],
'slab':[(22,200),(17,187),(17,57),(28,44),(152,44),(163,57),(163,187),(158,200)],
'teardrop':[(49,200),(27,179),(25,133),(42,92),(69,69),(109,35),(123,62),(144,96),(155,142),(151,178),(131,200)],
'hex':[(48,200),(24,177),(24,67),(49,42),(131,42),(156,67),(156,177),(132,200)],
'lens':[(24,200),(15,177),(18,86),(35,62),(61,46),(119,46),(145,62),(162,86),(165,177),(156,200)]}

def esc(t): return html.escape(str(t))
def txt(x,y,s,size=14,color=NAVY): return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}" text-anchor="middle">{esc(s)}</text>'
def path(points):
    mid=lambda a,b:((a[0]+b[0])/2,(a[1]+b[1])/2)
    st=mid(points[-1],points[0]); d=f'M {st[0]} {st[1]}'
    for i,p in enumerate(points):
        e=mid(p,points[(i+1)%len(points)]); d+=f' Q {p[0]} {p[1]} {e[0]} {e[1]}'
    return d+' Z'
def bottle(c,x,y,scale=1,view='front',cap=True):
    k=c['shape']; pts=shapes[k]; col=c['palette'][0]
    rgb=tuple(int(col[i:i+2],16) for i in (1,3,5))
    def tint(amount):
        return '#'+''.join(f'{round(v+(255-v)*amount) if amount>=0 else round(v*(1+amount)):02x}' for v in rgb)
    gradient='surface'+c['code']
    side=view=='side'; angle=view=='45'; width=.55 if side else .88 if angle else 1
    d=path(pts); s=f'<g transform="translate({x},{y}) scale({scale})"><ellipse cx="94" cy="210" rx="85" ry="9" fill="#152B3C" opacity=".10"/>'
    if angle: s+=f'<path d="{d}" transform="translate(14,0)" fill="{col}" stroke="#526575" stroke-width="1.4"/>'
    s+=f'<defs><linearGradient id="{gradient}"><stop stop-color="{tint(.4)}"/><stop offset=".32" stop-color="{tint(.12)}"/><stop offset=".78" stop-color="{tint(-.12)}"/><stop offset="1" stop-color="{tint(.16)}"/></linearGradient></defs>'
    s+=f'<g transform="translate({90*(1-width)},0) scale({width},1)"><path d="{d}" fill="{col}" stroke="#526575" stroke-width="1.2"/>'
    s+='<path d="M43 107 Q37 144 45 178" fill="none" stroke="#FFFFFF" stroke-width="5" opacity=".32"/>'
    if side or view=='back': k='plain'
    if k in ['arch','unicorn']:
        for j in range(3): s+=f'<path d="M {45+j*12} 152 V 108 Q 90 {39+j*17} {135-j*12} 108 V 152" fill="none" stroke="{c["palette"][1]}" stroke-width="5" opacity=".75"/>'
    elif k=='teddy': s+='<circle cx="60" cy="75" r="4" fill="#526575"/><circle cx="120" cy="75" r="4" fill="#526575"/><ellipse cx="90" cy="93" rx="18" ry="13" fill="#F4E7D7"/>'
    elif k=='football': s+='<path d="M90 65 L115 83 L105 110 L75 110 L65 83 Z M30 110 L65 83 M150 110 L115 83 M75 110 L55 157 M105 110 L125 157" fill="none" stroke="#F5F2EB" stroke-width="3"/>'
    elif k in ['crystal','hex','petal','bevel']: s+='<path d="M65 58 L55 179 M115 58 L125 179 M90 55 L90 183" stroke="#FFFFFF" opacity=".35" fill="none" stroke-width="2"/>'
    elif k=='astronaut': s+='<rect x="43" y="55" width="94" height="49" rx="22" fill="#152B3C" opacity=".75"/>'
    elif k=='rocket': s+='<circle cx="90" cy="88" r="17" fill="#F5F2EB" stroke="#526575" stroke-width="3"/>'
    elif k=='moon': s+='<path d="M113 61 Q58 67 67 113 Q46 72 84 55 Z" fill="#EEE7F6"/>'
    elif k=='dolphin': s+='<path d="M48 108 Q78 59 137 83 Q95 82 63 124 L48 130 Z" fill="#D5ECE7"/>'
    elif k in ['loop','lens','wave']: s+='<path d="M53 100 Q90 51 126 100 Q145 161 91 176 Q42 156 53 100 Z" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".3"/>'
    elif k=='shield': s+='<path d="M90 63 L90 176 M48 88 L90 63 L132 88" stroke="#E5C06B" fill="none" stroke-width="3"/>'
    if not side:
        if view=='back':
            s+='<rect x="49" y="119" width="82" height="53" rx="5" fill="#F5F2EB" opacity=".95"/>'+txt(90,132,'VELORI / '+c['code'],7)+txt(90,143,'INGREDIENTS: PENDING',5)+txt(90,152,'LOT / RP / PAO: PENDING',5)
            for j in range(24): s+=f'<rect x="{60+j*2.4}" y="158" width="{.7 if j%2 else 1.5}" height="9" fill="#152B3C"/>'
        else: s+='<rect x="44" y="122" width="92" height="51" rx="7" fill="#F5F2EB" opacity=".93"/>'+txt(90,137,'V E L O R I',10)+txt(90,150,c['name'].upper(),7)+txt(90,162,str(c['capacity_ml'])+' mL / DESIGN STUDY',5)
    s+='</g>'
    s+='<rect x="77" y="23" width="26" height="20" rx="5" fill="#D5D7D1" stroke="#526575"/>'
    if cap:
        caps=[(59,4,62,36,16),(63,1,54,38,12),(60,4,60,35,7),(65,0,50,39,5),(62,2,56,37,18)]
        cx,cy,cw,ch,cr=caps[c['group']]
        variation=int(c['code'][1:])%5
        cw+=variation*2-4;cx=90-cw/2;cr=max(3,cr-variation)
        s+=f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="{cr}" fill="{c["palette"][1]}" stroke="#526575" stroke-width="1.1"/>'+txt(90,25,'V',15)
    else:
        if c['group']<2: s+='<ellipse cx="90" cy="22" rx="11" ry="8" fill="#EBE5DA" stroke="#526575"/>'
        else: s+='<rect x="76" y="12" width="29" height="15" rx="3" fill="#D5D7D1"/><circle cx="99" cy="20" r="2" fill="#152B3C"/>'
    return s+'</g>'
def box(c,x,y,s=1):
    a,b=c['palette'][:2]; return f'<g transform="translate({x},{y}) scale({s})"><polygon points="0,24 100,24 128,5 28,5" fill="{b}"/><polygon points="100,24 128,5 128,188 100,210" fill="{a}"/><rect x="0" y="24" width="100" height="186" fill="{b}" stroke="#526575" stroke-width=".7"/><path d="M14 162 Q50 117 87 162 M14 176 Q50 131 87 176" fill="none" stroke="{a}" stroke-width="3"/>'+txt(50,56,'V E L O R I',11)+txt(50,80,c['name'].upper(),8)+txt(50,98,c['collection'],7)+txt(50,191,str(c['capacity_ml'])+' mL / CONCEPT',6)+'</g>'
def svg(body,w=1000,h=700):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="shine"><stop stop-color="#FFFFFF" stop-opacity=".42"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".8" stop-color="#152B3C" stop-opacity=".10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".25"/></linearGradient></defs><rect width="100%" height="100%" fill="{PAPER}"/>{body}</svg>'
def save_svg(p,s): p.write_text(s,encoding='utf-8')
def raster(s,p,width=3000):
    doc=fitz.open(stream=s.encode(),filetype='svg'); pix=doc[0].get_pixmap(matrix=fitz.Matrix(width/doc[0].rect.width,width/doc[0].rect.width),alpha=False); pix.save(str(p)); doc.close()
concepts=[]
for i,r in enumerate(rows):
    name,g,cat,shape,a,b,ml,w,h,d,desc=r
    c=dict(code=f'V{i+1:02}',name=name,group=g,collection=collections[g][0],age=collections[g][1],category=cat,shape=shape,palette=[a,b,NAVY,PAPER],capacity_ml=ml,dimensions_mm=[w,h,d],description=desc)
    c.update(material='Fragrance-compatible PP bottle with integral moulded silhouette; PP closure' if g<2 else 'PET candidate with PP pump overcap' if g==2 else 'Annealed glass candidate with PP overcap; pump separated at disposal',closure='Captive hinged cover over metered dab valve; parent opens and applies' if g==0 else 'Captive hinged cover over retained roll-on ball; parent controls use' if g==1 else 'Threaded pump collar, gasket, integral travel lock; retained overcap',label_mm=[round(w*.56),round(h*.25)],logo='Front centre, above product name; V monogram on cap',process='Extrusion blow moulding plus injection-moulded cap; screen print' if g<3 else 'Custom moulded glass; annealing; screen print; injection-moulded overcap',complexity='High' if shape in ['teddy','unicorn','rocket','butterfly','dolphin','pixel'] else 'Medium',box_mm=[w+16,h+20,d+16],finish='Matte body, restrained satin accent; no detachable decoration',format=collections[g][2])
    c['closure_note']='Illustrations show cover closed/open as capped/uncapped states. Hinge and retention require engineering; no loose decorative cap.' if g<2 else 'Illustrations show closed and exposed applicator states; retention hardware requires supplier engineering.'
    concepts.append(c)
(ROOT/'Source_Files'/'concepts.json').write_text(json.dumps(concepts,indent=2),encoding='utf-8')

def hero(c):
    return svg(txt(500,55,'VELORI  /  '+c['name'].upper(),24)+txt(500,83,c['collection']+'  |  '+c['age']+' years  |  '+c['category'],13)+bottle(c,190,135,2.1,'45')+box(c,635,145,2)+txt(500,650,'VECTOR CONCEPT VISUALISATION / NOT A PHOTOREALISTIC RENDER',11))
def views(c):
    b=txt(500,45,c['code']+' / '+c['name'].upper()+' / STUDY VIEWS',22)
    for j,(v,cap,label) in enumerate([('front',True,'FRONT / CLOSED'),('side',True,'SIDE / CLOSED'),('back',True,'BACK / CLOSED'),('45',True,'45 DEG / CLOSED'),('front',False,'APPLICATOR EXPOSED'),('45',False,'45 DEG / EXPOSED')]):
        x=55+(j%3)*325;y=85+(j//3)*295
        b+=bottle(c,x+40,y,1.08,v,cap)+txt(x+133,y+252,label,11)
    return svg(b)
def technical(c):
    w,h,d=c['dimensions_mm']; b=txt(500,42,c['code']+' / '+c['name'].upper()+' / ENVELOPE STUDY',21)
    b+=bottle(c,145,105,1.8)+bottle(c,635,105,1.8,'side')
    b+='<g stroke="#152B3C" stroke-width="1" fill="none"><path d="M130 100 H105 V480 H130 M160 495 V515 H455 V495 M646 495 V515 H835 V495"/></g>'
    b+=txt(70,295,str(h)+' mm',14)+txt(305,540,str(w)+' mm',14)+txt(740,540,str(d)+' mm',14)
    b+=txt(500,587,'OVERALL W x H x D, INCLUDING CLOSURE / NOT TO SCALE',12)+txt(500,612,'Capacity '+str(c['capacity_ml'])+' mL; usable fill volume and headspace require CAD validation.',12)+txt(500,640,'Rounded envelope only. Not production CAD; tolerances and neck finish are not specified.',11)
    return svg(b)
def dieline(c):
    w,h,d=c['box_mm']; total=2*w+2*d+14; hh=h+2*d
    b=''; x=14
    for j,pw in enumerate([w,d,w,d]):
        color=c['palette'][1] if j%2==0 else c['palette'][0]
        b+=f'<rect x="{x}" y="{d}" width="{pw}" height="{h}" fill="{color}" stroke="#152B3C" stroke-width=".5"/><rect x="{x}" y="0" width="{pw}" height="{d}" fill="none" stroke="#152B3C" stroke-width=".5"/><rect x="{x}" y="{d+h}" width="{pw}" height="{d}" fill="none" stroke="#152B3C" stroke-width=".5"/>'
        b+=f'<path d="M{x} {d} H{x+pw} M{x} {d+h} H{x+pw}" stroke="#DD6370" stroke-dasharray="3 2" fill="none"/>'
        b+=txt(x+pw/2,d+28,'VELORI',min(10,pw/5))+txt(x+pw/2,d+45,c['name'] if j==0 else 'COPY PENDING',min(7,pw/6))
        x+=pw
    b+=f'<rect x="0" y="{d}" width="14" height="{h}" fill="none" stroke="#152B3C"/>'
    return svg(b,total,hh).replace(f'width="{total}" height="{hh}"',f'width="{total}mm" height="{hh}mm"',1)

doc=fitz.open(); techdoc=fitz.open(); W,H=595.276,841.89
def page(title,kicker='VELORI / PRODUCT DEVELOPMENT',dark=False,target=None):
    p=(target if target is not None else doc).new_page(width=W,height=H); p.draw_rect(p.rect,color=None,fill=fitz.sRGB_to_pdf(int(('152B3C' if dark else 'F5F2EB'),16)))
    color=(.96,.94,.90) if dark else (.08,.17,.24)
    p.insert_text((38,38),kicker,fontsize=9,color=color)
    p.insert_textbox(fitz.Rect(38,65,W-38,140),title,fontsize=28,fontname='helv',color=color)
    p.insert_text((38,H-26),'CONCEPT PROPOSAL / 02 OCT 2026 / SUPPLIER VALIDATION REQUIRED',fontsize=7,color=color)
    p.insert_text((W-55,H-26),str(len(target if target is not None else doc)),fontsize=8,color=color)
    return p
def text(p,s,y=155,size=11,x=38,width=519):
    result=p.insert_textbox(fitz.Rect(x,y,x+width,H-55),s,fontsize=size,lineheight=1.45,color=(.08,.17,.24))
    if result<0: raise RuntimeError('Text overflow: '+s[:60])
def art(p,s,rect):
    d=fitz.open(stream=s.encode(),filetype='svg'); pdf=fitz.open('pdf',d.convert_to_pdf());p.show_pdf_page(fitz.Rect(rect),pdf,0);pdf.close();d.close()

# Five opening pages + forty-eight concept pages + seven closing pages = 60.
p=page('Small worlds.\nExtraordinary presence.','VELORI / THE YOUTH FRAGRANCE COLLECTION')
art(p,svg(bottle(concepts[0],20,40,1.5,'45')+bottle(concepts[17],330,20,1.65,'45')+bottle(concepts[23],660,40,1.5,'45'),1000,400),(30,240,565,650))
text(p,'24 original packaging directions / ages 3-18\nFive collections. One considered design language.\nVector concept edition | Manufacturer & investor proposal',680,12)
p=page('A name for becoming.')
text(p,'VELORI is a fictional master brand built around curiosity, personal expression and a calmer approach to youth fragrance. The name is a creative proposal; trademark and domain clearance have not been performed.\n\nThe wordmark uses widely spaced uppercase letters. A V monogram suggests two paths meeting: imagination and responsibility. Warm paper, deep ink and restrained colour pairings carry across all five collections.\n\nBoys, girls and unisex are merchandising categories, not restrictions on who may enjoy a design. The sensory brief, formula and suitability remain open development decisions.\n\nBrand assets: editable wordmark and monogram SVG, individual labels, retail cartons, gift systems and campaign visuals are included in the source package.',155,13)
art(p,svg(txt(500,140,'V',110)+txt(500,245,'V E L O R I',65)+txt(500,310,'SMALL WORLDS. EXTRAORDINARY PRESENCE.',18),1000,370),(45,490,550,715))
p=page('Design with care. Build with evidence.')
text(p,'01 / A distinctive silhouette\nTwenty-four different body envelopes, not a repeated bottle with new colours. Child-oriented motifs are abstracted into integral forms with broad radii and standing bases.\n\n02 / A controlled experience\nThe youngest collection proposes parent-applied dab formats; ages 6-9 propose parent-controlled roll-ons. There is no assumption that fragrance is suitable for a particular child. Formulation and exposure assessment must precede any launch.\n\n03 / A disciplined manufacturing brief\nDimensions are target envelopes. Capacity, headspace, neck finish, wall thickness, draft, tooling access and closure retention require engineering. Concept artwork is not production CAD.\n\n04 / A material hierarchy\nPlastic candidates for younger users; glass considered for older teens only after breakage assessment. Uncoated paperboard and removable components support disposal where local facilities accept them.\n\nVisual honesty: all product images are vector concept illustrations with shaded surfaces and schematic perspective. They are not Blender models or photorealistic 3D renders.',155,12)
p=page('Five stages. Five visual languages.')
for j,(name,age,fmt) in enumerate(collections):
    y=155+j*115;text(p,name+' / '+age+' years\n'+['Soft forms, muted pastels, adult-controlled application.','Exploration, broad silhouettes, retained applicators.','Movement, creativity and confident colour blocking.','Fashion-led sculptural surfaces and tonal finishes.','Minimal forms, restrained details and mature proportions.'][j]+'\n'+fmt,y,11)
p=page('The complete collection.')
for j,c in enumerate(concepts):
    x=35+(j%4)*135;y=150+(j//4)*100
    art(p,svg(bottle(c,20,0,.8),180,180),(x,y,x+95,y+75))
    p.insert_text((x,y+86),c['code']+' / '+c['name'],fontsize=7.5,color=(.08,.17,.24))

for c in concepts:
    folder=OUT/(c['code']+'_'+c['name'].replace(' ','_').replace('.',''));folder.mkdir(exist_ok=True)
    for name,s in [('Hero',hero(c)),('Views',views(c)),('Technical',technical(c))]:
        save_svg(folder/(name+'.svg'),s);raster(s,folder/(name+'.png'))
    # Individual view images are each 2400 px wide and retain actual artwork.
    for v,cap,label in [('front',True,'Front'),('side',True,'Side'),('back',True,'Back'),('45',True,'Perspective'),('front',False,'Uncapped')]:
        s=svg(bottle(c,160,70,2.2,v,cap)+txt(360,610,c['name']+' / '+label,18),720,680)
        save_svg(folder/(label+'.svg'),s);raster(s,folder/(label+'.png'),2400)
    (folder/'Specifications.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
    note='\n'.join(f'{k}: {v}' for k,v in c.items())+'\n\nPreliminary design estimates. No safety, cost, compliance or production certification.\n'
    (folder/'Specifications.txt').write_text(note,encoding='utf-8')
    labelsvg=svg(txt(150,38,'V E L O R I',22)+txt(150,69,c['name'].upper(),16)+txt(150,95,str(c['capacity_ml'])+' mL / CONCEPT',10),300,120)
    save_svg(folder/'Label.svg',labelsvg)
    ps=svg(box(c,75,45,2)+bottle(c,420,50,2,'45')+txt(500,535,c['name']+' / RETAIL PACKAGING CONCEPT',20),1000,600)
    save_svg(PACK/(c['code']+'_Retail.svg'),ps);raster(ps,PACK/(c['code']+'_Retail.png'))
    ds=dieline(c);save_svg(PACK/(c['code']+'_Carton_Artwork.svg'),ds)
    dd=fitz.open(stream=ds.encode(),filetype='svg'); dpf=fitz.open('pdf',dd.convert_to_pdf()); dpf[0].set_mediabox(fitz.Rect(0,0,dd[0].rect.width,dd[0].rect.height));dpf.save(str(PACK/(c['code']+'_Carton_Concept.pdf')));dpf.close();dd.close()
    p=page(c['name'],c['code']+' / '+c['collection'].upper()+' / '+c['age']+' YEARS / '+c['category'].upper())
    art(p,hero(c),(20,145,575,555));art(p,views(c),(35,555,560,790))
    p=page('The design brief.',c['code']+' / '+c['name'].upper()+' / TECHNICAL & MATERIAL DIRECTION')
    art(p,technical(c),(35,135,560,455))
    w,h,d=c['dimensions_mm'];lw,lh=c['label_mm']
    body=f"FORM / {c['description']}\nENVELOPE / {w} x {h} x {d} mm; {c['capacity_ml']} mL target fill.\nMATERIAL / {c['material']}\nCLOSURE / {c['closure']}\nLABEL / {lw} x {lh} mm nominal; {c['logo']}.\nPROCESS / {c['process']}. Complexity: {c['complexity']}.\nCARTON / {' x '.join(map(str,c['box_mm']))} mm; 350 gsm uncoated board candidate, folded paper insert.\nFINISH / {c['finish']}\nPALETTE / {' / '.join(c['palette'])}\nVALIDATION / Compatibility, leak/drop, applicator retention, fill volume, tooling feasibility."
    text(p,body,465,9.5)
    tp=page(c['name']+' / envelope',c['code']+' / TECHNICAL DRAWING / PRELIMINARY',target=techdoc)
    art(tp,technical(c),(25,135,570,540));text(tp,c['material']+'\n'+c['process']+'\n'+c['closure']+'\n'+c['closure_note']+'\nLabel target: '+str(lw)+' x '+str(lh)+' mm. Neck finish, wall thickness and tolerances: supplier to define.\nNo internal section or volume calculation is represented.',555,11)
    print('Built',c['code'],c['name'],flush=True)

p=page('A gift, thoughtfully assembled.')
gift=svg('<rect x="75" y="140" width="810" height="330" rx="20" fill="#E4DDCD" stroke="#152B3C"/><rect x="75" y="90" width="810" height="80" rx="14" fill="#152B3C"/>'+txt(480,140,'V E L O R I / DISCOVERY',28,'#F5F2EB')+bottle(concepts[14],170,180,1.1)+bottle(concepts[18],395,180,1.1)+bottle(concepts[23],620,180,1.1)+txt(500,545,'FOLDED BOARD TRAY / REMOVABLE PAPER SLEEVES / NO MAGNETS',14),1000,600)
art(p,gift,(25,140,570,490));text(p,'Discovery Trio / Junior & Teen\nThree products from a single assessed age range, in a paperboard tray. The visual shows shape options, not an approved age combination. Outer gift carton target: 260 x 145 x 65 mm; supplier to validate fit.\n\nLittle Magic / Parent & Child Ritual\nA single bottle with an adult instruction card in a tuck-top carton. No loose toys, glitter, magnetic closures or sweet-like accessories. Gift box target: 100 x 130 x 65 mm.\n\nRetail artwork includes trim outlines and fold guides. Flaps, glue areas and bleed must be revised against the supplier dieline before printing.',505,12)
save_svg(PACK/'Gift_Discovery.svg',gift);raster(gift,PACK/'Gift_Discovery.png')
p=page('A quiet stage for bold shapes.')
display=svg('<path d="M70 420 H930 V510 H70 Z" fill="#DAD6CA"/><path d="M140 310 H850 V420 H140 Z" fill="#E9E3D7"/>'+bottle(concepts[1],170,100,1.5)+bottle(concepts[6],440,80,1.6)+bottle(concepts[17],700,105,1.5)+txt(500,580,'VELORI / YOUR NEXT CHAPTER',32),1000,650)
art(p,display,(25,145,570,545));text(p,'Counter display / 600 x 280 x 220 mm target\nFolded paperboard stepped riser with reusable base; removable printed headers. Final stability, load rating and transit durability need prototype testing.\n\nCampaign direction\nLarge-scale silhouettes, warm studio backgrounds and one direct line: "Your next chapter." Parent-facing instructions accompany younger ranges. No claims of wellbeing, clinical benefit or child safety are implied.\n\nRetail logic\nOrganise by collection and application format; make adult supervision information easy to find. The illustrated arrangement is a merchandising study.',560,11)
save_svg(PACK/'Display_Campaign.svg',display);raster(display,PACK/'Display_Campaign.png')
p=page('From silhouette to sample.')
text(p,'GATE 1 / Feasibility and supplier quotation\nValidate cavity volume against target fill and headspace. Confirm neck finish, wall thickness, draft angles, minimum radii, mould seams, shrinkage and standing stability. Obtain tooling and unit-cost quotes at multiple order quantities. No manufacturing cost is asserted in this proposal.\n\nGATE 2 / Functional prototypes\nPrototype body envelopes and retained closures. Test adult operability, accidental opening, leakage, drop resistance, pump or roll-on retention, cap torque and repeated-use wear. Neither a captive cap nor a travel lock is certified child-resistant.\n\nGATE 3 / Formula and packaging interaction\nCheck migration, swelling, stress cracking, seal compatibility, odour carry-over and shelf-life stability using the final formulation and assembled pack. Assess colourants and coatings; external finishes should not contaminate the formula.\n\nGATE 4 / Production and disposal\nApprove tooling samples, colour masters and print proofs. Record quality limits, lot traceability and transport validation. Prefer light decoration and paper inserts; confirm recycling routes locally. Recycled polymers require purity and compatibility assessment.\n\nComplexity is a comparative design estimate: High = sculptural tooling or complex relief; Medium = simpler asymmetric or geometric envelope. It is not a supplier quotation.',155,11.5)
p=page('Safety is a development requirement.')
text(p,'For ages 3-5, the fragrance proposition itself requires qualified assessment. Parent-applied, non-spray formats may reduce airborne exposure but do not establish suitability. Assess intended use, foreseeable misuse, ingestion, eye contact, skin exposure and access by younger siblings.\n\nA qualified cosmetic safety assessor must evaluate the complete formula, ingredient restrictions, impurities, fragrance allergens and exposure for each target age and application site. Consider sensitisation and irritation; natural ingredients are not automatically less sensitising. Select an exposure-appropriate formula only after this review.\n\nFor water-containing formulas, establish microbiological quality and preservative efficacy. Conduct stability and packaging compatibility studies. Determine evidence needed for any product claim; do not use "hypoallergenic", "non-toxic", "dermatologically tested" or "safe for children" without substantiation.\n\nPackaging risk work must address breakage, sharp edges, choking-size parts, leakage and retained applicators. Motifs are integral relief, not attachable toys. The carton should clearly distinguish fragrance from toys or edible products.\n\nThe younger-use closures are concepts, not certified child-resistant devices. Show adult supervision and keep-away instructions in the final assessed label. Evaluate flammability and transit requirements if the final formula contains alcohol.\n\nRelease gate: documented formula assessment, packaging tests, approved label copy and market-specific review. The current proposal authorises none of these claims.',155,11)
p=page('Choose the market. Confirm the rules.')
text(p,'This is a market-selection checklist, not a compliance opinion. Destination markets are not specified. Regulatory counsel and the responsible manufacturer must confirm current requirements at launch.\n\nUNITED STATES\nFDA describes the responsible person\'s duty to ensure adequate safety substantiation and maintain supporting records. Assess applicable MoCRA registration, listing, adverse-event and labelling obligations, including whether any exemptions apply. Cosmetic labels require a market-specific review.\n\nEUROPEAN UNION\nThe European Commission requires an expert scientific safety assessment before market entry. Assess responsible-person, product information file, notification and label obligations under Regulation (EC) No 1223/2009. Fragrance allergen labelling depends on the binding Annex III list and applicable transition arrangements.\n\nOTHER DESTINATIONS\nFor India and other launch countries, obtain local review of classification, manufacturing/import permissions, ingredient restrictions, mandatory pack declarations and applicable language requirements. No jurisdiction is treated as approved here.\n\nBACK-PANEL COPY TO COMPLETE\nProduct identity, net contents, ingredient list, appropriate allergen declarations, responsible entity/contact, batch, durability or period-after-opening, use instructions and warnings as applicable. The illustrated barcode is decorative, not a registered retail barcode.',155,10.5)
links=[('FDA safety substantiation and labelling','https://www.fda.gov/cosmetics/resources-industry-cosmetics/small-businesses-homemade-cosmetics-fact-sheet'),('European Commission safety assessment','https://single-market-economy.ec.europa.eu/sectors/cosmetics/scientific-and-technical-assessment_en'),('European Commission fragrance allergen labelling','https://single-market-economy.ec.europa.eu/sectors/cosmetics/cosmetic-products-specific-topics/fragrance-allergens-labelling_en')]
for i,(label,url) in enumerate(links):
    y=703+i*23;p.insert_text((38,y),label+' / checked 02 Oct 2026',fontsize=8,color=(.08,.17,.24));p.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(38,y-10,550,y+5),'uri':url})
p=page('Twenty-four directions, compared.')
headers='CODE   PRODUCT                     AGE     CATEGORY    mL     W x H x D mm       TOOLING'
text(p,headers,145,8)
for i,c in enumerate(concepts):
    y=177+i*23
    values=[c['code'],c['name'],c['age'],c['category'],str(c['capacity_ml']),'x'.join(map(str,c['dimensions_mm'])),c['complexity']]
    for x,v in zip([38,73,220,270,347,384,505],values):p.insert_text((x,y),v,fontsize=8,color=(.08,.17,.24))
    p.draw_line((38,y+7),(557,y+7),color=(.82,.82,.78),width=.4)
text(p,'All dimensions include closure and are preliminary target envelopes.\nAll capacities require supplier validation; costs are intentionally unquoted.',750,9)
p=page('The next chapter starts here.')
art(p,svg(bottle(concepts[3],20,60,1.2,'45')+bottle(concepts[7],215,25,1.4,'45')+bottle(concepts[12],445,50,1.3,'45')+bottle(concepts[18],650,20,1.4,'45')+bottle(concepts[21],865,60,1.2,'45'),1100,430),(15,155,580,440))
text(p,'A coherent brand. Twenty-four individual forms.\nAn editable foundation for manufacturer conversations.\n\nIncluded: 24 hero illustrations, front/side/back/perspective and exposed-applicator images, technical envelopes, specifications, retail mockups, conceptual carton artwork, gift and campaign assets, vector brand files and a reusable build script.\n\nRequired next: brand clearance; market definition; professional formula and safety review; detailed CAD; closure engineering; supplier quotations; physical prototypes; validated print dielines and approved label copy.\n\nThis is a high-resolution design presentation, not a production release. RGB vector artwork requires printer-specific CMYK conversion, bleed, paper selection and contract proofing. No PDF/X certification is claimed.',490,12)

assert len(doc)==60,len(doc)
doc.set_toc([[1,'VELORI / Collection proposal',1],[1,'Brand & design philosophy',2],[1,'Age groups & collection overview',4]]+[[1,c['collection'],6+2*i] for i,c in enumerate(concepts) if i==0 or c['group']!=concepts[i-1]['group']]+[[1,'Packaging & campaign',54],[1,'Manufacturing',56],[1,'Safety & regulatory considerations',57],[1,'Product comparison',59],[1,'Final presentation',60]])
techdoc.set_toc([[1,c['code']+' / '+c['name'],i+1] for i,c in enumerate(concepts)])
doc.save(str(ROOT/'Perfume_Collection_Master_Catalogue.pdf'),garbage=4,deflate=True)
techdoc.save(str(ROOT/'Technical_Drawings.pdf'),garbage=4,deflate=True)
save_svg(ROOT/'Source_Files'/'VELORI_Logo.svg',svg(txt(500,120,'V',100)+txt(500,235,'V E L O R I',62),1000,300))
with (ROOT/'Source_Files'/'Product_Comparison.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f);writer.writerow(['Code','Product','Collection','Age','Category','mL','W mm','H mm','D mm','Complexity']);writer.writerows([[c['code'],c['name'],c['collection'],c['age'],c['category'],c['capacity_ml'],*c['dimensions_mm'],c['complexity']] for c in concepts])
(ROOT/'README.md').write_text('''# VELORI design collection

60-page master catalogue and 24-page technical drawing book. All artwork is original vector concept visualisation, not photorealistic 3D rendering. Blender was unavailable in the execution environment.

Individual_Bottle_Designs contains eight 2400-3000 px PNGs per design, editable SVGs, label artwork and JSON/text specifications. Packaging_Concepts contains 24 retail mockups, conceptual carton artwork PDFs/SVGs, gift and display/campaign images.

## Rebuild
Use Python 3.11+ with PyMuPDF and Pillow installed. Run `python Source_Files/build_all.py` from any directory to regenerate the catalogue, supplemental assets and verification. Edit the rows, shapes and collection metadata in build_collection.py to change designs; concepts.json records the generated specifications. The build uses the Arial font convention for SVG artwork. No Blender dependency is required.

## Production status
Dimensions and capacities are preliminary. Technical drawings show overall envelopes, not production sections, tolerances or engineered closures. Young-user cap-open views depict exposed applicators; retained hinges remain an engineering proposal. Carton PDFs are conceptual RGB artwork, not approved press files: supplier must create a validated dieline with proper flap geometry, glue allowances, bleed, CMYK profile and barcode/label copy. Brand clearance, formula development, age-specific safety assessment, physical tests and destination-market review remain required. No production-ready or child-safety certification is implied.

## Regulatory references
FDA: https://www.fda.gov/cosmetics/resources-industry-cosmetics/small-businesses-homemade-cosmetics-fact-sheet
European Commission: https://single-market-economy.ec.europa.eu/sectors/cosmetics/scientific-and-technical-assessment_en
European Commission allergens: https://single-market-economy.ec.europa.eu/sectors/cosmetics/cosmetic-products-specific-topics/fragrance-allergens-labelling_en
Reviewed 02 October 2026. These are selected US/EU references, not worldwide compliance clearance.
''',encoding='utf-8')
print('Saved master catalogue (60 pages) and technical drawings (24 pages).')


