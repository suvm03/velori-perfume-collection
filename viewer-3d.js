import * as THREE from 'three';
import { OrbitControls } from './assets/vendor/OrbitControls.js';
import { RoomEnvironment } from './assets/vendor/RoomEnvironment.js';
import { RoundedBoxGeometry } from './assets/vendor/RoundedBoxGeometry.js';
import { profiles } from './assets/bottle-profiles.js';

const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
function surface(colour, glass = false) {
  return new THREE.MeshPhysicalMaterial({color:colour,roughness:glass?.12:.28,metalness:glass?.04:.01,clearcoat:glass?1:.55,clearcoatRoughness:.15,transmission:glass?.28:0,thickness:glass?.16:0,ior:1.46});
}
function mesh(geometry,material,parent,x=0,y=0,z=0) {
  const m=new THREE.Mesh(geometry,material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function printTexture(c,back=false,carton=false) {
  const canvas=document.createElement('canvas');canvas.width=768;canvas.height=carton?1024:384;
  const ctx=canvas.getContext('2d');ctx.fillStyle=carton?c.palette[1]:'#f5f2eb';ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#152b3c';ctx.textAlign='center';
  ctx.font='500 62px Georgia';ctx.fillText('V E L O R I',384,carton?170:95);
  if(back){ctx.font='22px Arial';ctx.fillText(c.code+' / DESIGN CONCEPT',384,170);ctx.font='18px Arial';ctx.fillText('INGREDIENTS & LABEL COPY PENDING',384,225);ctx.fillText('FORMULATION & SAFETY REVIEW REQUIRED',384,270);}
  else {ctx.font='32px Arial';ctx.fillText(c.name.toUpperCase(),384,carton?280:196);ctx.font='20px Arial';ctx.fillText(carton?c.collection:`${c.capacity_ml} mL / DESIGN CONCEPT`,384,carton?340:285);}
  if(carton){ctx.strokeStyle=c.palette[0];ctx.lineWidth=14;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(384,860+i*55,240,Math.PI,Math.PI*2);ctx.stroke();}ctx.font='22px Arial';ctx.fillText(`${c.capacity_ml} mL / CONCEPT`,384,955);}
  const t=new THREE.CanvasTexture(canvas);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t;
}
function outlineGeometry(c) {
  const points=profiles[c.shape];const [w,h,d]=c.dimensions_mm.map(n=>n/10);
  const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
  const bevel=Math.min(.18,d*.065);const bodyH=h*.79;
  const projected=points.map(([x,y])=>new THREE.Vector2(((x-minX)/(maxX-minX)-.5)*(w-2*bevel),.18+(1-(y-minY)/(maxY-minY))*(bodyH-.25)));
  const shape=new THREE.Shape();const mid=(a,b)=>a.clone().add(b).multiplyScalar(.5);const start=mid(projected.at(-1),projected[0]);shape.moveTo(start.x,start.y);
  for(let i=0;i<projected.length;i++){const p=projected[i],end=mid(p,projected[(i+1)%projected.length]);shape.quadraticCurveTo(p.x,p.y,end.x,end.y);}
  shape.closePath();const geometry=new THREE.ExtrudeGeometry(shape,{depth:d-2*bevel,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel,bevelSegments:5,curveSegments:10,steps:1});geometry.translate(0,0,-(d-2*bevel)/2);geometry.computeVertexNormals();
  return {geometry,w,h,d,bodyH,bevel};
}
export function buildBottle(c) {
  const group=new THREE.Group();group.name=c.code+' / '+c.name;
  const {geometry,w,h,d,bodyH}=outlineGeometry(c);const glass=c.group>=3;
  const body=mesh(geometry,surface(c.palette[0],glass),group);body.name='Bottle body / preliminary envelope';
  if(glass){const liquidMat=new THREE.MeshPhysicalMaterial({color:c.palette[0],roughness:.12,transmission:.38,thickness:.7,ior:1.33});const liquid=mesh(geometry.clone(),liquidMat,group,0,.2,0);liquid.scale.set(.81,.72,.70);liquid.name='Illustrative liquid volume';}
  const silver=new THREE.MeshStandardMaterial({color:'#c4c8c4',metalness:.85,roughness:.2});
  const neckY=bodyH+.32;mesh(new THREE.CylinderGeometry(w*.13,w*.14,.55,48),silver,group,0,neckY,0);
  if(c.group<2){mesh(new THREE.SphereGeometry(w*.11,32,24),surface('#eee9dd'),group,0,neckY+.29,0);}
  else{mesh(new RoundedBoxGeometry(w*.28,.35,d*.35,3,.08),silver,group,0,neckY+.44,0);mesh(new THREE.CircleGeometry(.055,20),surface('#152b3c'),group,w*.1,neckY+.44,d*.177);}
  const cap=new THREE.Group();group.add(cap);cap.name='Closure design preview';const capHeight=h*.15;const capWidth=w*(.4+(Number(c.code.slice(1))%5)*.023);const capDepth=Math.min(d*.9,capWidth);
  if(c.group===4){mesh(new THREE.CylinderGeometry(capWidth*.5,capWidth*.5,capHeight,64),surface(c.palette[1]),cap);}
  else {mesh(new RoundedBoxGeometry(capWidth,capHeight,capDepth,6,Math.min(capWidth,capHeight,capDepth)*(c.group===0?.28:.14)),surface(c.palette[1]),cap);}
  cap.position.y=neckY+.32;const capClosedY=cap.position.y;
  const monogram=document.createElement('canvas');monogram.width=128;monogram.height=128;const mc=monogram.getContext('2d');mc.clearRect(0,0,128,128);mc.font='78px Georgia';mc.textAlign='center';mc.fillStyle='#152b3c';mc.fillText('V',64,92);const mt=new THREE.CanvasTexture(monogram);mt.colorSpace=THREE.SRGBColorSpace;
  mesh(new THREE.PlaneGeometry(capWidth*.46,capHeight*.75),new THREE.MeshStandardMaterial({map:mt,transparent:true,roughness:.5}),cap,0,0,capDepth*.5+.015);
  const labelW=Math.min(w*.56,4.2),labelH=Math.min(bodyH*.26,2);const label=mesh(new THREE.PlaneGeometry(labelW,labelH),new THREE.MeshStandardMaterial({map:printTexture(c),roughness:.58,polygonOffset:true,polygonOffsetFactor:-1}),group,0,bodyH*.38,d*.5+.012);label.name='Front label concept';
  const back=mesh(new THREE.PlaneGeometry(labelW*.88,labelH),new THREE.MeshStandardMaterial({map:printTexture(c,true),roughness:.65}),group,0,bodyH*.38,-d*.5-.012);back.rotation.y=Math.PI;
  const accent=surface(c.palette[1]);const ink=surface('#233d4b');const z=d*.5+.045;
  const sphere=(x,y,r,mat)=>{const m=mesh(new THREE.SphereGeometry(r,24,16),mat,group,x,y,z);m.scale.z=.28;return m;};
  if(c.shape==='teddy'){sphere(-w*.17,bodyH*.69,.11,ink);sphere(w*.17,bodyH*.69,.11,ink);const nose=sphere(0,bodyH*.59,w*.10,accent);nose.scale.y=.72;}
  if(c.shape==='rocket'){mesh(new THREE.TorusGeometry(w*.15,.065,12,48),silver,group,0,bodyH*.72,z);mesh(new THREE.CircleGeometry(w*.13,40),surface('#bdd9e1',true),group,0,bodyH*.72,z-.02);}
  if(c.shape==='astronaut'){mesh(new RoundedBoxGeometry(w*.55,bodyH*.20,.08,5,.18),surface('#263c50'),group,0,bodyH*.75,z);}
  if(c.shape==='football'){const points=[];for(let j=0;j<6;j++){const a=j*Math.PI*2/5+Math.PI/2;points.push(new THREE.Vector3(Math.cos(a)*w*.14,bodyH*.68+Math.sin(a)*w*.14,z));}const hex=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:c.palette[1]}));group.add(hex);}
  if(['crystal','hex','petal','bevel'].includes(c.shape)){for(const x of [-.24,.24])mesh(new RoundedBoxGeometry(.045,bodyH*.50,.05,2,.018),accent,group,w*x,bodyH*.62,z);}
  if(['arch','unicorn'].includes(c.shape)){for(let i=0;i<3;i++){const curve=new THREE.EllipseCurve(0,bodyH*.57,w*(.25-i*.045),bodyH*(.29-i*.045),0,Math.PI,false,0);const pts=curve.getPoints(50).map(p=>new THREE.Vector3(p.x,p.y,z));mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),50,.033,8,false),accent,group);}}
  const retail=new THREE.Group();retail.name='Retail carton';const [bw,bh,bd]=c.box_mm.map(v=>v/10);
  const materials=Array.from({length:6},()=>new THREE.MeshStandardMaterial({color:c.palette[1],roughness:.85}));materials[4]=new THREE.MeshStandardMaterial({map:printTexture(c,false,true),roughness:.85});
  mesh(new THREE.BoxGeometry(bw,bh,bd),materials,retail,0,bh/2,0);retail.position.set(w*.7+bw*.62,0,-d*.35);retail.visible=false;group.add(retail);
  return {group,cap,capClosedY,retail,height:h,width:w,depth:d};
}
class BottleViewer {
  constructor(host,toolbar) {
    this.host=host;this.toolbar=toolbar;this.autoRotate=!reducedMotion;this.openCap=false;this.showBox=false;
    this.renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true});this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));this.renderer.setClearColor('#e9e5dc');this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFSoftShadowMap;this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=.85;
    host.replaceChildren(this.renderer.domElement);this.renderer.domElement.tabIndex=0;this.renderer.domElement.setAttribute('aria-label','3D bottle. Drag or arrow keys to rotate. Scroll, pinch or plus and minus keys to zoom.');
    this.scene=new THREE.Scene();const room=new RoomEnvironment();const pmrem=new THREE.PMREMGenerator(this.renderer);this.environment=pmrem.fromScene(room,.035,.1,100,{size:64}).texture;this.scene.environment=this.environment;this.scene.environmentIntensity=.8;room.dispose();pmrem.dispose();
    this.camera=new THREE.PerspectiveCamera(34,1,.1,200);this.controls=new OrbitControls(this.camera,this.renderer.domElement);this.controls.enableDamping=true;this.controls.dampingFactor=.07;this.controls.enablePan=false;this.controls.autoRotate=this.autoRotate;this.controls.autoRotateSpeed=.55;this.controls.minPolarAngle=.3;this.controls.maxPolarAngle=Math.PI*.67;
    this.scene.add(new THREE.HemisphereLight('#fffaf0','#897c6e',.65));const key=new THREE.DirectionalLight('#fff8ec',2);key.position.set(-10,20,14);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-20;key.shadow.camera.right=20;key.shadow.camera.top=25;key.shadow.camera.bottom=-15;key.shadow.normalBias=.025;key.shadow.bias=-.00015;this.scene.add(key);const fill=new THREE.DirectionalLight('#d7e7f7',.7);fill.position.set(12,8,-5);this.scene.add(fill);
    const ground=mesh(new THREE.PlaneGeometry(500,500),new THREE.MeshStandardMaterial({color:'#e9e5dc',roughness:.85}),this.scene);ground.rotation.x=-Math.PI/2;ground.position.y=-.08;ground.castShadow=false;
    const base=mesh(new THREE.CylinderGeometry(6.8,7,.22,96),new THREE.MeshStandardMaterial({color:'#ddd6c8',roughness:.7}),this.scene,0,-.01,0);base.castShadow=false;this.base=base;
    this.visible=true;new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting;}).observe(host);
    new ResizeObserver(()=>this.resize()).observe(host);
    toolbar.addEventListener('click',e=>{const b=e.target.closest('[data-action]');if(!b)return;this.action(b.dataset.action);});
    this.renderer.domElement.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){this.model.group.rotation.y+=e.key==='ArrowLeft'?.12:-.12;e.preventDefault();}else if(['+','=','-'].includes(e.key)){this.camera.position.multiplyScalar(e.key==='-'?1.08:.92);e.preventDefault();}else if(e.key==='Home')this.reset();});
    this.resize();this.updateButtons();this.animate();
  }
  resize(){const w=this.host.clientWidth,h=this.host.clientHeight;if(w<1||h<1)return;this.renderer.setSize(w,h,false);this.camera.aspect=w/h;this.camera.updateProjectionMatrix();}
  load(c){
    if(this.c?.code===c.code){this.resize();return;}
    if(this.model){this.scene.remove(this.model.group);const geometries=new Set(),materials=new Set(),textures=new Set();this.model.group.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of (Array.isArray(o.material)?o.material:o.material?[o.material]:[])){materials.add(m);if(m.map)textures.add(m.map);}});geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());}
    this.c=c;this.model=buildBottle(c);this.scene.add(this.model.group);this.openCap=false;this.showBox=false;this.base.scale.set(c.dimensions_mm[0]/65,1,c.dimensions_mm[0]/65);this.reset();this.updateButtons();this.host.dataset.model=c.code;this.host.dataset.ready='true';
  }
  reset(){if(!this.model)return;const h=this.model.height;const extra=this.showBox?1.35:1;this.controls.target.set(this.showBox?this.model.width*.6:0,h*.46,0);this.camera.position.set(h*.95*extra,h*.72,h*2.55*extra);this.controls.minDistance=h*.9;this.controls.maxDistance=h*5;this.model.group.rotation.y=-.13;this.controls.update();this.resize();}
  action(a){if(a==='rotate'){this.autoRotate=!this.autoRotate;this.controls.autoRotate=this.autoRotate;}if(a==='cap')this.openCap=!this.openCap;if(a==='box'){this.showBox=!this.showBox;this.model.retail.visible=this.showBox;this.reset();}if(a==='reset')this.reset();if(a==='snapshot'){this.renderer.render(this.scene,this.camera);const link=document.createElement('a');link.download=`${this.c.code}_${this.c.name.replaceAll(' ','_')}_3D_Preview.png`;link.href=this.renderer.domElement.toDataURL('image/png');link.click();}this.updateButtons();}
  updateButtons(){for(const b of this.toolbar.querySelectorAll('[data-action]')){if(b.dataset.action==='rotate'){b.textContent=this.autoRotate?'Pause rotation':'Auto rotate';b.setAttribute('aria-pressed',String(this.autoRotate));}if(b.dataset.action==='cap'){b.textContent=this.openCap?'Close cap':'Open cap';b.setAttribute('aria-pressed',String(this.openCap));}if(b.dataset.action==='box'){b.textContent=this.showBox?'Hide packaging':'Show packaging';b.setAttribute('aria-pressed',String(this.showBox));}}}
  animate(){requestAnimationFrame(()=>this.animate());if(!this.visible||!this.host.getClientRects().length||document.hidden)return;if(this.model){const target=this.model.capClosedY+(this.openCap?this.model.height*.22:0);this.model.cap.position.y=THREE.MathUtils.lerp(this.model.cap.position.y,target,.12);this.model.cap.rotation.z=THREE.MathUtils.lerp(this.model.cap.rotation.z,this.openCap?.12:0,.12);}this.controls.update();this.renderer.render(this.scene,this.camera);}
}
let studio,detail;
function showDialog(c){try{if(!detail)detail=new BottleViewer(document.getElementById('dialog-canvas'),document.querySelector('#dialog-three .three-toolbar'));detail.load(c);}catch(error){fallback(document.getElementById('dialog-canvas'));console.error(error);}}
function fallback(host){host.innerHTML='<p class="viewer-status">3D requires WebGL in your browser. You can still explore every bottle using the image-view tabs and PDF catalogue.</p>';host.dataset.ready='false';}
function showStudio(c){studio.load(c);document.getElementById('studio-collection').textContent=`${c.collection} / ${c.age} YEARS`;document.getElementById('studio-name').textContent=c.name;document.getElementById('studio-description').textContent=c.description+'.';document.getElementById('studio-colours').innerHTML=c.palette.slice(0,2).map(col=>`<span><i style="background:${col}"></i>${col}</span>`).join('');document.getElementById('studio-specs').innerHTML=`<dt>Capacity</dt><dd>${c.capacity_ml} mL</dd><dt>Dimensions</dt><dd>${c.dimensions_mm.join(' × ')} mm</dd><dt>Material direction</dt><dd>${c.material}</dd>`;}
function init(){const designs=window.VELORI_DESIGNS||[];if(!designs.length)return;const select=document.getElementById('studio-select');for(const c of designs){const option=document.createElement('option');option.value=c.code;option.textContent=`${c.code} / ${c.name} · ${c.collection}`;select.append(option);}try{studio=new BottleViewer(document.getElementById('studio-canvas'),document.querySelector('#studio .three-toolbar'));showStudio(designs[0]);select.addEventListener('change',()=>showStudio(designs.find(c=>c.code===select.value)));}catch(error){fallback(document.getElementById('studio-canvas'));console.error(error);}window.VELORI3D={showDialog,buildBottle,get studio(){return studio;},get detail(){return detail;}};const dialog=document.getElementById('design-dialog');if(dialog.open&&!document.getElementById('dialog-three').hidden)showDialog(designs.find(c=>c.code===dialog.dataset.code));}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();

