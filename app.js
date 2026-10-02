(() => {
'use strict';
const $=id=>document.getElementById(id), esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const languages=[['pt-BR','br','Português'],['en-US','us','English'],['es-ES','es','Español'],['zh-CN','cn','中文'],['hi-IN','in','हिन्दी'],['ar-SA','sa','العربية'],['fr-FR','fr','Français'],['bn-BD','bd','বাংলা'],['ru-RU','ru','Русский'],['de-DE','de','Deutsch'],['it-IT','it','Italiano'],['ja-JP','jp','日本語']];
const read=(key,fallback)=>{try{return localStorage.getItem(key)||fallback}catch{return fallback}},save=(key,value)=>{try{localStorage.setItem(key,value)}catch{}};
let lang=read('materialcodex-language',read('factorytoolbox-language',navigator.language));if(!MaterialTranslations[lang])lang=languages.find(x=>x[0].startsWith(lang.split('-')[0]))?.[0]||'en-US';
const t=key=>MaterialTranslations[lang][key]??key;
const units={density:'kg/m³',specificWeight:'kN/m³',specificGravity:'',young:'GPa',shear:'GPa',poisson:'',tensile:'MPa',yield:'MPa',flexural:'MPa',flexuralModulus:'GPa',compressive:'MPa',elongation:'%',hardness:'',toughness:'MPa·√m',thermal:'W/(m·K)',heat:'J/(kg·K)',cv:'J/(kg·K)',expansion:'µm/(m·K)',melting:'°C',boiling:'°C',service:'°C',resistivity:'Ω·m',conductivity:'S/m',iacs:'% IACS',permittivity:'',molarMass:'g/mol',viscosity:'Pa·s',z:'',gamma:'',waterAbsorption:'%'};
const groups={physical:['density','specificWeight','specificGravity','molarMass','viscosity','z','gamma'],mechanical:['young','shear','poisson','tensile','yield','flexural','flexuralModulus','compressive','elongation','hardness','toughness'],thermalGroup:['thermal','heat','cv','expansion','melting','boiling','service'],electrical:['resistivity','conductivity','iacs','permittivity'],other:['waterAbsorption']};
const order=Object.values(groups).flat(),families=['metal','polymer','ceramic','gas','liquid','composite'];
const data=MaterialData.materials,byId=new Map(data.map(m=>[m.id,m]));
const mapValue=(v,fn)=>Array.isArray(v)?v.map(fn).sort((a,b)=>a-b):fn(v);
function properties(m){
 const p={...m.properties};
 if(p.density)p.specificWeight={...p.density,v:mapValue(p.density.v,x=>x*9.80665/1000),kind:'derived',parentKind:p.density.kind,formula:'γ = ρ × 9.80665 / 1000 [kN/m³]'};
 if(p.resistivity){const q=p.resistivity;p.conductivity={...q,v:mapValue(q.v,x=>1/x),kind:'derived',parentKind:({greater:'less',less:'greater',minimum:'maximum',maximum:'minimum'}[q.kind]||q.kind),formula:'σ = 1 / ρe [S/m]'};}
 else if(p.iacs)p.conductivity={...p.iacs,v:mapValue(p.iacs.v,x=>x*580000),kind:'derived',parentKind:p.iacs.kind,formula:'σ = IACS [%] × 580000 [S/m]',formulaSource:'https://archive.copper.org/publications/newsletters/innovations/2006/09/high_cu_alloys.php'};
 return p;
}
let current=byId.get(decodeHash())||byId.get(read('materialcodex-material',''))||data[0],selected=[];
try{const saved=JSON.parse(read('materialcodex-comparison','[]'));if(Array.isArray(saved))selected=[...new Set(saved)].filter(id=>byId.has(id)).slice(0,4)}catch{}
function decodeHash(){try{return decodeURIComponent(location.hash.slice(1))}catch{return ''}}
function number(v){return new Intl.NumberFormat(lang,{maximumSignificantDigits:6,notation:Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e7)?'scientific':'standard'}).format(v)}
function value(v){return Array.isArray(v)?v.map(number).join(' – '):typeof v==='number'?number(v):t(v)}
function prefix(p){return ({minimum:'≥ ',maximum:'≤ ',greater:'> ',less:'< '}[p.parentKind||p.kind]||'')}
function display(p,key){return prefix(p)+value(p.v)+(units[key]?' '+units[key]:'')}
function name(m){return ['gas','liquid'].includes(m.family)?t(m.identity)+' · '+m.name:m.name}
function sourceOf(m,p){return MaterialData.sources[p?.source||m.source]}
function metadata(m,p){const src=sourceOf(m,p);return `<span class="kind">${esc(t(p.kind))}${p.parentKind?' · '+esc(t(p.parentKind)):''}</span><span class="meta">${esc([t(p.condition),p.method].filter(Boolean).join(' · '))}${p.formula?'<br><bdi dir="ltr">'+esc(p.formula)+'</bdi>':''}<br><a href="${esc(src.url)}" target="_blank" rel="noopener noreferrer">${esc(t('source'))} ↗</a>${p.formulaSource?' · <a href="'+esc(p.formulaSource)+'" target="_blank" rel="noopener noreferrer">IACS ↗</a>':''}</span>`}
function cell(m,key){const p=properties(m)[key];return p?`<bdi class="value">${esc(display(p,key))}</bdi><br>${metadata(m,p)}`:`<span class="missing">${esc(t('missing'))}</span>`}
function notify(key){$('status').textContent=t(key);$('status').hidden=false;clearTimeout(notify.timer);notify.timer=setTimeout(()=>$('status').hidden=true,4500)}
function selectMaterial(id,scroll=false){if(!byId.has(id))return;current=byId.get(id);save('materialcodex-material',id);history.replaceState(null,'','#'+encodeURIComponent(id));renderList();renderDetail();if(scroll&&innerWidth<701){$('detail').scrollIntoView({behavior:'smooth',block:'start'});$('detail').focus({preventScroll:true})}}
function searchText(m){return [m.id,m.name,m.identity,m.aliases,m.family,...Object.values(MaterialTranslations).flatMap(dict=>[dict[m.identity]||'',dict[m.family]||'']),...Object.keys(m.composition.items)].join(' ')}
const normalize=s=>s.normalize('NFKD').replace(/\p{M}/gu,'').toLowerCase();
const haystacks=new Map(data.map(m=>[m.id,normalize(searchText(m))]));
function renderList(){const query=normalize($('search').value).trim().split(/\s+/).filter(Boolean),family=$('family').value,property=$('propertyFilter').value;const shown=data.filter(m=>(!family||m.family===family)&&(!property||properties(m)[property])&&query.every(q=>haystacks.get(m.id).includes(q)));
 $('resultCount').textContent=number(shown.length)+' '+t('results');$('materialList').innerHTML=shown.length?shown.map(m=>`<button type="button" class="material-row" data-material="${m.id}" aria-current="${m.id===current.id}"><strong>${esc(name(m))}${selected.includes(m.id)?' ✓':''}</strong><small>${esc(t(m.identity))} · ${esc(t(m.family))}</small></button>`).join(''):`<p class="empty">${esc(t('noResults'))}</p>`;
 $('materialList').querySelectorAll('[data-material]').forEach(b=>b.addEventListener('click',()=>selectMaterial(b.dataset.material,true)));
}
function renderDetail(){const m=current,p=properties(m),src=sourceOf(m),metricKeys=['density',m.family==='gas'||m.family==='liquid'?'molarMass':p.tensile?'tensile':'flexural','thermal'];if(!p.density&&p.specificGravity)metricKeys[0]='specificGravity';
 const composition=Object.entries(m.composition.items).map(([key,v])=>`<div class="element"><b>${esc(key)}</b><span>${esc(value(v))}${(typeof v==='number'||Array.isArray(v))&&m.composition.mode.includes('Mass')?' %':''}</span></div>`).join('');
 const sections=Object.entries(groups).map(([group,keys])=>{const present=keys.filter(key=>p[key]);return present.length?`<section><h3>${esc(t(group))}</h3><table class="properties"><tbody>${present.map(key=>`<tr data-property="${key}"><th scope="row">${esc(t(key))}</th><td>${cell(m,key)}</td></tr>`).join('')}</tbody></table></section>`:''}).join('');
 const missing=order.filter(key=>!p[key]);
 $('detail').innerHTML=`<div class="detail-head"><span class="tag">${esc(t(m.family))}</span><h2>${esc(name(m))}</h2><p class="subtitle">${esc(t(m.identity))}</p><p class="condition">${esc(t(m.condition))}</p><div class="actions"><button id="compareCurrent" class="primary" aria-pressed="${selected.includes(m.id)}">${esc(t(selected.includes(m.id)?'removeCompare':'addCompare'))}${selected.length?' · '+selected.length+'/4':''}</button>${selected.length?`<button id="goComparison">${esc(t('sideBySide'))} ↓</button>`:''}<button id="exportCurrent">${esc(t('exportCSV'))}</button><button id="printCurrent">${esc(t('print'))}</button></div></div><div class="detail-body"><div class="summary-grid">${metricKeys.map(key=>`<div class="metric"><span>${esc(t(key))}</span><strong>${p[key]?esc(display(p[key],key)):esc(t('missing'))}</strong><small>${p[key]?esc(t(p[key].condition)):''}</small></div>`).join('')}</div><section><h3>${esc(t('composition'))}</h3><p class="note composition-note">${esc(t(m.composition.mode))}</p><div class="composition">${composition||`<p class="note">${esc(t('emptyComposition'))}</p>`}</div><p class="note composition-note">${esc(t('compositionNote'))}</p></section>${sections}<details><summary>${esc(t('undocumented'))} (${missing.length})</summary><p>${missing.map(key=>esc(t(key))).join(' · ')}</p></details><div class="source-box"><h3>${esc(t('source'))}</h3><a href="${esc(src.url)}" target="_blank" rel="noopener noreferrer">${esc(src.title)} ↗</a><p>${esc(t('dataVersion'))}: ${esc(src.accessed)}</p><p>${esc(t('derivedNote'))}</p></div></div>`;
 $('compareCurrent').addEventListener('click',()=>toggleCompare(m.id));$('goComparison')?.addEventListener('click',()=>{$('comparison').scrollIntoView({behavior:'smooth'});$('comparisonTable').focus({preventScroll:true})});$('exportCurrent').addEventListener('click',()=>exportCSV([m]));$('printCurrent').addEventListener('click',()=>window.print());
}
function toggleCompare(id){if(selected.includes(id))selected=selected.filter(x=>x!==id);else{if(selected.length>=4){notify('maxCompare');return}selected.push(id)}save('materialcodex-comparison',JSON.stringify(selected));renderDetail();renderList();renderComparison()}
function renderComparison(){const materials=selected.map(id=>byId.get(id));$('comparison').hidden=!materials.length;if(!materials.length){$('comparisonTable').innerHTML='';return}const keys=order.filter(key=>materials.some(m=>properties(m)[key]));
 $('comparisonTable').innerHTML=`<table class="compare-table"><thead><tr><th scope="col">${esc(t('properties'))}</th>${materials.map(m=>`<th scope="col"><a href="#${m.id}" data-select="${m.id}">${esc(name(m))}</a><span class="meta">${esc(t(m.condition))}</span><button class="remove" data-remove="${m.id}">${esc(t('remove'))}</button></th>`).join('')}</tr></thead><tbody>${keys.map(key=>`<tr><th scope="row">${esc(t(key))}</th>${materials.map(m=>'<td>'+cell(m,key)+'</td>').join('')}</tr>`).join('')}</tbody></table>`;
 $('comparisonTable').querySelectorAll('[data-remove]').forEach(b=>b.addEventListener('click',()=>toggleCompare(b.dataset.remove)));
 $('comparisonTable').querySelectorAll('[data-select]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();selectMaterial(a.dataset.select);$('detail').scrollIntoView({behavior:'smooth'})}));
}
function csvCell(v){let s=String(v??'');if(/^[=+@\t\r]/.test(s)||(/^\s*-/.test(s)&&!/^\s*-\d+(\.\d+)?([eE][+-]?\d+)?$/.test(s)))s="'"+s;return '"'+s.replace(/"/g,'""')+'"'}
function csvText(materials){const rows=[['material_id','material','family','product_condition','property_id','property','value','range_max','unit','qualifier','origin_qualifier','test_condition','method','calculation','source_title','source_url','source_accessed','calculation_source_url']];
 for(const m of materials){for(const [key,p] of Object.entries(properties(m))){const src=sourceOf(m,p);rows.push([m.id,name(m),t(m.family),t(m.condition),key,t(key),Array.isArray(p.v)?p.v[0]:p.v,Array.isArray(p.v)?p.v[1]:'',units[key],p.kind,p.parentKind||'',t(p.condition),p.method||'',p.formula||'',src.title,src.url,src.accessed,p.formulaSource||''])}
 const src=sourceOf(m);for(const [element,v] of Object.entries(m.composition.items)){rows.push([m.id,name(m),t(m.family),t(m.condition),'composition:'+element,t('composition')+' · '+element,Array.isArray(v)?v[0]:typeof v==='number'?v:t(v),Array.isArray(v)?v[1]:'',m.composition.mode.includes('Mass')?'mass %':'',m.composition.mode,'','','','',src.title,src.url,src.accessed,''])}}
 return '\uFEFF'+rows.map(row=>row.map(csvCell).join(',')).join('\r\n')+'\r\n';
}
function exportCSV(materials){const blob=new Blob([csvText(materials)],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='MaterialCodex-'+(materials.length===1?materials[0].id:'comparison')+'.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('exported')}
function renderLanguage(){document.documentElement.lang=lang;document.documentElement.dir=lang==='ar-SA'?'rtl':'ltr';document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=t(el.dataset.i18n));document.querySelector('.search-bar').setAttribute('aria-label',t('search'));$('search').setAttribute('aria-label',t('search'));
 const option=languages.find(x=>x[0]===lang);$('languageButton').innerHTML=`<img src="flags/${option[1]}.svg" alt=""><span class="language-name">${esc(option[2])}</span><span aria-hidden="true">⌄</span>`;$('languageButton').setAttribute('aria-label',option[2]);
 $('languageMenu').innerHTML=languages.map(([code,flag,label])=>`<button type="button" data-language="${code}" lang="${code}" aria-pressed="${code===lang}"><img src="flags/${flag}.svg" alt="">${esc(label)}</button>`).join('');
 $('languageMenu').querySelectorAll('[data-language]').forEach(b=>b.addEventListener('click',()=>{lang=b.dataset.language;save('materialcodex-language',lang);closeMenu();renderLanguage();$('languageButton').focus()}));
 const family=$('family').value,property=$('propertyFilter').value;$('family').innerHTML=`<option value="">${esc(t('all'))}</option>`+families.map(f=>`<option value="${f}">${esc(t(f))}</option>`).join('');$('family').value=family;
 $('propertyFilter').innerHTML=`<option value="">${esc(t('all'))}</option>`+order.map(key=>`<option value="${key}">${esc(t(key))}</option>`).join('');$('propertyFilter').value=property;
 $('familiesCount').textContent=families.map(f=>t(f)).join(' · ');$('total').textContent=number(data.length);$('version').textContent=MaterialData.version;renderList();renderDetail();renderComparison();
}
function closeMenu(){$('languageMenu').hidden=true;$('languageButton').setAttribute('aria-expanded','false')}
function openMenu(focus=false){$('languageMenu').hidden=false;$('languageButton').setAttribute('aria-expanded','true');if(focus)$('languageMenu').querySelector('[data-language]').focus()}
$('languageButton').addEventListener('click',()=>{$('languageMenu').hidden?openMenu():closeMenu()});
$('languagePicker').addEventListener('keydown',e=>{const buttons=[...$('languageMenu').querySelectorAll('button')],i=buttons.indexOf(document.activeElement);if(e.key==='Escape'){closeMenu();$('languageButton').focus();e.preventDefault()}else if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();openMenu();const next=e.key==='Home'?0:e.key==='End'?buttons.length-1:e.key==='ArrowDown'?(i+1)%buttons.length:(i-1+buttons.length)%buttons.length;buttons[next].focus()}});
$('languagePicker').addEventListener('focusout',e=>{if(!$('languagePicker').contains(e.relatedTarget))closeMenu()});document.addEventListener('click',e=>{if(!$('languagePicker').contains(e.target))closeMenu()});
$('search').addEventListener('input',renderList);$('family').addEventListener('change',renderList);$('propertyFilter').addEventListener('change',renderList);
$('clearFilters').addEventListener('click',()=>{$('search').value='';$('family').value='';$('propertyFilter').value='';renderList();$('search').focus()});
$('clearComparison').addEventListener('click',()=>{selected=[];save('materialcodex-comparison','[]');renderDetail();renderList();renderComparison()});$('exportComparison').addEventListener('click',()=>exportCSV(selected.map(id=>byId.get(id))));
window.addEventListener('hashchange',()=>{const id=decodeHash();if(byId.has(id))selectMaterial(id)});
renderLanguage();
// Read-only helpers for reproducible data validation; no network or user data is sent.
window.MaterialCodex=Object.freeze({properties,csvText,units});
})();
