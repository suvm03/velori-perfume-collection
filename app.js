'use strict';
const designs = window.VELORI_DESIGNS || [];
const grid = document.getElementById('product-grid');
const dialog = document.getElementById('design-dialog');
const state = {group: 'all', category: 'all', search: ''};
let selected;
let currentView = 'Hero';
const views = ['3D', 'Hero', 'Front', 'Side', 'Back', 'Perspective', 'Uncapped', 'Views', 'Technical', 'Packaging'];
const escapeHTML = value => String(value).replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const folder = c => `Individual_Bottle_Designs/${c.code}_${c.name.replaceAll(' ', '_').replaceAll('.', '')}`;
const imageURL = (c, view, original = false) => original ? (view === 'Packaging' ? `Packaging_Concepts/${c.code}_Retail.png` : `${folder(c)}/${view}.png`) : `assets/designs/${c.code}/${view}.webp`;

function filteredDesigns() {
  const q = state.search.trim().toLowerCase();
  return designs.filter(c => (state.group === 'all' || c.group === Number(state.group)) && (state.category === 'all' || c.category === state.category) && (!q || [c.name,c.code,c.collection,c.shape,c.description,c.age,c.category,...c.palette].join(' ').toLowerCase().includes(q)));
}
function renderGrid() {
  const results = filteredDesigns();
  grid.innerHTML = results.map(c => `<button type="button" class="product-card" data-code="${c.code}" aria-label="Explore ${escapeHTML(c.name)}, ${escapeHTML(c.collection)}, ages ${c.age}"><div class="product-art"><img src="${imageURL(c,'Front')}" alt="${escapeHTML(c.name)} bottle concept" loading="lazy" width="640" height="605"><span class="product-code">${c.code}</span><span class="product-category">${c.category.toUpperCase()}</span><span class="product-arrow" aria-hidden="true">↗</span></div><div class="product-meta"><h3>${escapeHTML(c.name)}</h3><span class="mini-swatches" aria-hidden="true">${c.palette.slice(0,2).map(col=>`<i style="background:${col}"></i>`).join('')}</span></div><p class="product-sub">${escapeHTML(c.collection)} · ${c.age} years · ${c.capacity_ml} mL</p></button>`).join('');
  document.getElementById('result-count').textContent = `${results.length} ${results.length===1?'design':'designs'}`;
  document.getElementById('empty').hidden = results.length > 0;
}
function setView(view) {
  currentView = view;
  const img = document.getElementById('dialog-image');
  const is3D = view === '3D';
  img.hidden = is3D;
  document.getElementById('dialog-three').hidden = !is3D;
  document.getElementById('full-image').hidden = is3D;
  if (is3D) { window.VELORI3D?.showDialog(selected); document.dispatchEvent(new CustomEvent('velori:3d-open',{detail:selected})); }
  else img.src = imageURL(selected,view);
  img.alt = `${selected.name} / ${view === 'Uncapped' ? 'exposed applicator' : view} concept illustration`;
  document.getElementById('full-image').href = imageURL(selected,view,true);
  document.querySelectorAll('#view-tabs button').forEach(b => {b.classList.toggle('active',b.dataset.view === view);b.setAttribute('aria-pressed',String(b.dataset.view === view));});
}
function openDesign(code, updateHash = true) {
  const c = designs.find(d => d.code === code);
  if (!c) return;
  selected = c;
  dialog.dataset.code = c.code;
  document.getElementById('dialog-kicker').textContent = `${c.code} / DESIGN STUDY`;
  document.getElementById('dialog-collection').textContent = `${c.collection} / ${c.age} years / ${c.category}`;
  document.getElementById('dialog-title').textContent = c.name;
  document.getElementById('dialog-description').textContent = c.description + '.';
  document.getElementById('dialog-palette').innerHTML = c.palette.map(col=>`<span><i style="background:${col}"></i>${col}</span>`).join('');
  const specs = [['Capacity',`${c.capacity_ml} mL`],['Dimensions',`${c.dimensions_mm.join(' × ')} mm (W × H × D)`],['Format',c.format],['Material',c.material],['Label',`${c.label_mm.join(' × ')} mm`],['Carton',`${c.box_mm.join(' × ')} mm`],['Finish',c.finish],['Complexity',c.complexity]];
  document.getElementById('dialog-specs').innerHTML = specs.map(([k,v])=>`<dt>${k}</dt><dd>${escapeHTML(v)}</dd>`).join('');
  document.getElementById('dialog-manufacturing').innerHTML = [c.closure,c.closure_note,c.process,`Logo: ${c.logo}`].map(t=>`<p>${escapeHTML(t)}</p>`).join('');
  document.querySelector('#dialog-manufacturing').parentElement.open = false;
  document.getElementById('dialog-links').innerHTML = `<a href="${folder(c)}/Specifications.json" target="_blank" rel="noopener">Open full design specifications ↗</a><a href="Packaging_Concepts/${c.code}_Carton_Concept.pdf" target="_blank" rel="noopener">Open conceptual carton artwork ↗</a><a href="Packaging_Concepts/${c.code}_Label_Concept.pdf" target="_blank" rel="noopener">Open label artwork ↗</a><a href="downloads/${c.code}_Design_Pack.zip" download>Download this complete design pack ↓</a><a href="Technical_Drawings.pdf#page=${designs.indexOf(c)+1}" target="_blank" rel="noopener">Open technical drawing PDF ↗</a>`;
  document.getElementById('view-tabs').innerHTML = views.map(v=>`<button type="button" data-view="${v}" aria-pressed="false">${v==='Uncapped'?'Applicator':v==='Views'?'All views':v}</button>`).join('');
  if (!dialog.open) dialog.showModal();
  setView('3D');
  document.body.classList.add('body-locked');
  if (updateHash) history.replaceState(null,'',`#design-${c.code}`);
}
function closeDesign() {
  if (dialog.open) dialog.close();
}
document.getElementById('collection-filters').addEventListener('click', e => {
  const b=e.target.closest('button[data-group]');if(!b)return;
  state.group=b.dataset.group;
  document.querySelectorAll('[data-group]').forEach(t=>{t.classList.toggle('active',t===b);t.setAttribute('aria-pressed',String(t===b));});
  renderGrid();
});
document.getElementById('category').addEventListener('change',e=>{state.category=e.target.value;renderGrid();});
document.getElementById('search').addEventListener('input',e=>{state.search=e.target.value;renderGrid();});
grid.addEventListener('click',e=>{const card=e.target.closest('[data-code]');if(card)openDesign(card.dataset.code);});
document.getElementById('view-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-view]');if(b)setView(b.dataset.view);});
document.getElementById('close-dialog').addEventListener('click',closeDesign);
dialog.addEventListener('click',e=>{if(e.target!==dialog)return;const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDesign();});
dialog.addEventListener('close',()=>{document.body.classList.remove('body-locked');if(location.hash.startsWith('#design-'))history.replaceState(null,'','#collection');});
document.getElementById('reset').addEventListener('click',()=>{state.group='all';state.category='all';state.search='';document.getElementById('search').value='';document.getElementById('category').value='all';document.querySelectorAll('[data-group]').forEach(b=>{const active=b.dataset.group==='all';b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});renderGrid();});
window.addEventListener('hashchange',()=>{if(location.hash.startsWith('#design-'))openDesign(location.hash.slice(8),false);});
renderGrid();
document.getElementById('studio-details').addEventListener('click',()=>openDesign(document.getElementById('studio-select').value));
if(location.hash.startsWith('#design-'))openDesign(location.hash.slice(8),false);
