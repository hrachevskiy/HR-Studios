
/* ============ Data room (lesson 8) ============ */
let xvOpen = false, xmodeCur = 'deck';
const cv = (sh, r, c) => (sh.cells[`${r},${c}`] || {});
const lbl = (sh, r) => String(cv(sh, r, 2).v ?? cv(sh, r, 1).v ?? '').replace(/\s+/g, ' ').trim();
const SM = XL[3];
const C4 = [{c:4,h:'2024'},{c:5,h:'2025'},{c:6,h:'Փոփոխ.',k:'chg'},{c:7,h:'Աճի տեմպ',k:'gr'}];
const CA = [{c:4,h:'2024'},{c:5,h:'2025'},{c:6,h:'Փոփոխ.',k:'chg'},{c:7,h:'Գնահատական',k:'vd'}];
const DRS = [
  {id:'d0', t:'ԴՊ · ելակետային տվյալներ', s:'Թերթ 1 · դասախոսի տվյալներ', acc:'#3dff8f', sh:SD, rows:[3,4,5,6,7,8,9,10,12,15,16,17,18,20,21,23,24,25,26], cols:C4, code:true},
  {id:'d1', t:'ԴՊ · վերլուծություն', s:'Շրջանառելիություն և գործակիցներ', acc:'#5cd6ff', sh:SD, rows:[32,33,34,35,36,37,38,39], cols:CA, code:true, note:'Եզրակացություն 1'},
  {id:'d2', t:'ԴՊ · կազմ և կառուցվածք', s:'Ըստ դեբիտորների', acc:'#3dffe0', sh:SD, rows:[44,45,46,47,48,49,50,51], cols:[{c:3,h:'2024'},{c:4,h:'Կառ. %',k:'st'},{c:5,h:'2025'},{c:6,h:'Կառ. %',k:'st'},{c:7,h:'Շեղում',k:'chg'},{c:8,h:'Շեղ. կառ.',k:'chg',d:2}]},
  {id:'d3', t:'ԴՊ · շարժ և մարում', s:'Մնացորդների հաշվեկշիռ', acc:'#c8ff4d', sh:SD, rows:[55,56,57,58,59,60,61], cols:[{c:4,h:'2024'},{c:5,h:'2025'},{c:6,h:'Փոփոխ.',k:'chg'}]},
  {id:'k0', t:'ԿՊ · ելակետային տվյալներ', s:'Թերթ 2 · դասախոսի տվյալներ', acc:'#a98bff', sh:SK, rows:[3,4,5,6,7,8,9,10,11,12,14,17,18,19,20,22,24,25,26,27,28], cols:C4, code:true},
  {id:'k1', t:'ԿՊ · վերլուծություն', s:'Շրջանառելիություն, կշիռներ, Գդկհ', acc:'#ff6bd6', sh:SK, rows:[32,33,34,35,36,37,38,39,40,41,42,43,44], cols:CA, code:true, note:'Եզրակացություն 2'},
  {id:'k2', t:'ԿՊ · կառուցվածք', s:'Ըստ տեսակի', acc:'#ffb547', sh:SK, rows:[49,50,51,52], cols:[{c:4,h:'2024'},{c:5,h:'Կառ. %',k:'st'},{c:6,h:'2025'},{c:7,h:'Կառ. %',k:'st'},{c:8,h:'Շեղ. կառ.',k:'chg',d:2}]},
  {id:'k3', t:'Գործոնային վերլուծություն', s:'Գդկհ = ՏԿդպ × ԳԸԻ ÷ ՏԿկպ', acc:'#ffd36b', custom:'fa'},
  {id:'sm', t:'Ամփոփում', s:'Գլխավոր ցուցանիշներ և եզրակացություն', acc:'#3dff8f', custom:'sm'},
];
let drCur = 'd0';
/*__NUMCELL__*/
function vdCell(sh, r, c){ const s = String(cv(sh,r,c).v ?? ''); if (!s) return '<td></td>';
  const cls = s.startsWith('✔') ? 'up' : (s.startsWith('✖') ? 'dn' : 'nt'); return `<td><span class="vd ${cls}">${esc(s)}</span></td>`; }
function drTable(sec){
  const sh = sec.sh;
  const head = `<tr><th>Ցուցանիշ</th>${sec.code?'<th>Կոդ</th>':''}${sec.cols.map(c=>`<th>${c.h}</th>`).join('')}</tr>`;
  const body = sec.rows.map((r,i) => {
    const bold = /Ընդամեն|տարեվերջին|տարեսկզբին|Մնացորդ/.test(lbl(sh,r)) && !/^Ռիսկ|^Անհուս|^Ընթացիկ/.test(lbl(sh,r));
    const n = cv(sh,r,1).v; const num = (typeof n === 'number' || /^\d/.test(String(n??''))) && cv(sh,r,2).v != null ? `<b class="rn">${esc(n)}</b>` : '';
    const code = sec.code ? `<td class="cd">${esc(String(cv(sh,r,3).v ?? '').trim())}</td>` : '';
    return `<tr class="${bold?'k-total':''}" style="--i:${i}"><td class="lb">${num}${esc(lbl(sh,r))}</td>${code}${sec.cols.map(c => c.k==='vd' ? vdCell(sh,r,c.c) : numCell(sh,r,c.c,{kind:c.k, dec:c.d})).join('')}</tr>`; }).join('');
  return `<div class="dtw"><table class="dt"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
}
function noteText(sh, key){ for (const k in sh.cells){ const x = sh.cells[k].v; if (typeof x==='string' && x.startsWith(key)) return x; } return ''; }
function drFA(){
  const f = [[61,'ՏԿդպ = ԴՊ ÷ ԸԱ'],[62,'ԳԸԻ = ԸԱ ÷ ԸՊ'],[63,'ՏԿկպ = ԿՊ ÷ ԸՊ']];
  const t1 = `<div class="dtw"><table class="dt"><thead><tr><th>Գործոն</th><th>2024 (0)</th><th>2025 (1)</th><th>Փոփոխ.</th></tr></thead><tbody>${f.map((x,i)=>`<tr style="--i:${i}"><td class="lb"><b>${x[1]}</b><br><small class="mu">${esc(lbl(SK,x[0]))}</small></td>${numCell(SK,x[0],4,{dec:4})}${numCell(SK,x[0],5,{dec:4})}${numCell(SK,x[0],6,{kind:'chg',dec:4})}</tr>`).join('')}</tbody></table></div>`;
  const steps = [66,67,68,69].map((r,i)=>`<div class="stp" style="--i:${i}"><div class="sn">${esc(v(SK,r,1))}</div><div class="sd">${esc(v(SK,r,2))}</div><div class="sv cell" data-sh="1" data-ref="D${r}" tabindex="0">${fmt(v(SK,r,4),3)}</div>${i?`<div class="si ${v(SK,r,5)>=0?'up':'dn'} cell" data-sh="1" data-ref="E${r}" tabindex="0">${sgn(v(SK,r,5),3)}<small>${esc(v(SK,r,6))}</small></div>`:'<div class="si nt">բազային</div>'}</div>`).join('<div class="sa">→</div>');
  return `<h4 class="dh">Գործոններ</h4>${t1}<h4 class="dh">Շղթայական տեղադրում</h4><div class="steps">${steps}</div>
    <div class="dpan" style="margin-top:14px"><b>Σ = ${sgn(v(SK,70,5),3)}</b> <span class="mu">= Գդկհ¹ − Գդկհ⁰ = ${fmt(K(41,1),3)} − ${fmt(K(41,0),3)} · ստուգում՝ ${fmt(v(SK,71,5),3)}</span></div>`;
}
function drSM(){
  let rows = ''; for (let r=5; r<=14; r++){ const s = String(v(SM,r,6)); rows += `<tr style="--i:${r-5}"><td class="lb">${esc(v(SM,r,2))}</td>${numCell(SM,r,3,{})}${numCell(SM,r,4,{})}${numCell(SM,r,5,{kind:'chg'})}<td><span class="vd ${s.startsWith('✔')?'up':(s.startsWith('✖')?'dn':'nt')}">${esc(s)}</span></td></tr>`; }
  return `<div class="dtw"><table class="dt"><thead><tr><th>Ցուցանիշ</th><th>2024</th><th>2025</th><th>Փոփոխ.</th><th>Գնահատական</th></tr></thead><tbody>${rows}</tbody></table></div>
    <div class="dnote"><b>Ընդհանուր եզրակացություն</b>${esc(String(v(SM,18,1)).replace(/^Ընդհանուր եզրակացություն\.\s*/,'')).replace(/\n/g,'<br>')}</div>`;
}
function drSection(id){
  drCur = id; const s = DRS.find(x=>x.id===id);
  $('#dr').style.setProperty('--acc', s.acc);
  document.querySelectorAll('#dr-nav button').forEach(b => b.classList.toggle('on', b.dataset.s===id));
  const body = s.custom === 'fa' ? drFA() : (s.custom === 'sm' ? drSM() : drTable(s));
  const note = s.note ? noteText(s.sh, s.note) : '';
  $('#dr-main').innerHTML = `<header class="drh"><div class="k">${esc(s.s)}</div><h2>${esc(s.t)}</h2></header>${body}${note?`<div class="dnote"><b>Եզրակացություն</b>${esc(note.replace(/^Եզրակացություն \d[^.]*\.\s*/,'')).replace(/\n/g,'<br>')}</div>`:''}`;
  $('#dr-main').scrollTop = 0; const m = $('#dr-main'); m.classList.remove('in'); void m.offsetWidth; m.classList.add('in');
  drFx(null);
}
/*__FX__*/
$('#dr-nav').innerHTML = DRS.map((s,i) => `<button data-s="${s.id}" style="--a:${s.acc}"><i>${String(i+1).padStart(2,'0')}</i><span><b>${esc(s.t)}</b><small>${esc(s.s)}</small></span></button>`).join('');
$('#dr-nav').addEventListener('click', e => { const b = e.target.closest('button'); if (b) drSection(b.dataset.s); });
$('#dr-main').addEventListener('click', e => { const c = e.target.closest('[data-ref]'); if (c) drFx(c); });
$('#dr-main').addEventListener('keydown', e => { if (e.key==='Enter'){ const c = e.target.closest('[data-ref]'); if (c) drFx(c); } });
function openXL(){ if (!xvOpen) drSection(drCur); xvOpen = true; const s = SL[xcur]; s && s.el.querySelectorAll('video').forEach(v=>v.pause()); $('#dr').classList.add('on'); try{ history.replaceState(null,'','#excel'); }catch(e){} }
function closeXL(){ xvOpen = false; $('#dr').classList.remove('on'); const s = SL[xcur]; s && s.el.querySelectorAll('video').forEach(v=>v.play().catch(()=>{})); try{ history.replaceState(null,'', `#s${xcur+1}`); }catch(e){} }
$('#dr-close').onclick = closeXL;
/*__DL__*/
/*__PRE__*/
/* boot */
(function(){
  preload();
  const h = location.hash, m = /^#s(\d+)$/.exec(h);
  xgo(m ? Math.min(SL.length, +m[1]) - 1 : 0);
  document.body.style.overflow = 'hidden';
  if (h === '#excel') openXL();
  idleT = setTimeout(()=>xapp.classList.add('idle'), 4000);
})();
