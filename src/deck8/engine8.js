const colL = n => { let s=''; while(n>0){ const m=(n-1)%26; s=String.fromCharCode(65+m)+s; n=Math.floor((n-1)/26);} return s; };
const colN = L => L.split('').reduce((a,ch)=>a*26+ch.charCodeAt(0)-64,0);
function cellFmt(v, nf){
  if (typeof v !== 'number') return v==null?'':String(v);
  if (nf >= 1) return v.toFixed(nf);
  return Number.isInteger(v) ? v.toLocaleString('en-US') : v.toLocaleString('en-US',{maximumFractionDigits:2});
}
const REFC = ['#2a6bd8','#d8432a','#7b3fd1','#1f9d55','#c2851b','#c12a8f','#138a9e','#5a6b12'];
function parseRefs(f){
  const out = []; const re = /(?:'([^']+)'!|([A-Za-z0-9_Ա-և.]+)!)?\$?([A-Z]{1,2})\$?(\d+)(?::\$?([A-Z]{1,2})\$?(\d+))?/g; let m;
  while ((m = re.exec(f))){ out.push({sheet:m[1]||m[2]||null, c1:colN(m[3]), r1:+m[4], c2:m[5]?colN(m[5]):colN(m[3]), r2:m[6]?+m[6]:+m[4], txt:m[0], idx:m.index}); }
  return out;
}
/* ---- build ---- */
const ACC = [['#3dff8f','#22e0c0'],['#5cd6ff','#a98bff'],['#a98bff','#ff6bd6'],['#ff6bd6','#ffb547'],['#ffb547','#3dff8f'],['#3dffe0','#5cd6ff']];
const xstage = $('#xstage'), xapp = $('#xapp');
SL.forEach((s, i) => {
  const el = document.createElement('section'); el.className = 'x-slide'; el.setAttribute('aria-roledescription','slide'); el.setAttribute('aria-label', `${i+1}. ${s.t}`);
  const bg = s.video ? `<div class="x-bgl"><video muted loop playsinline preload="metadata" src="${s.video}" poster="${s.video.replace('.mp4','.jpg')}"></video></div>`
                     : `<div class="x-bgl" style="background-image:url('${s.bg}')"></div>`;
  const A = ACC[i % ACC.length]; el.style.setProperty('--acc', A[0]); el.style.setProperty('--acc2', A[1]); s.acc = A;
  el.innerHTML = bg + `<div class="x-shade ${s.shade}"></div><div class="x-aur"><i></i><i></i><i></i></div><div class="x-tint"></div><div class="x-big x-par" data-depth="-24">${String(i+1).padStart(2,'0')}</div><div class="x-glow"></div>` + s.html();
  xstage.appendChild(el); s.el = el;
});
const pcv = document.createElement('canvas'); pcv.className = 'x-parts'; xstage.appendChild(pcv);
const xdots = $('#xdots'); SL.forEach((s,i)=>{ const d=document.createElement('i'); d.title=`${i+1}. ${s.t}`; d.onclick=e=>{e.stopPropagation(); xgo(i);}; xdots.appendChild(d); });
$('#xovg').innerHTML = SL.map((s,i)=>`<div class="th" data-go="${i}" style="--i:${i};background-image:url('${s.bg || (s.video||'').replace('.mp4','.jpg')}')"><b>${String(i+1).padStart(2,'0')}</b><span>${s.t}</span></div>`).join('');

/* fit */
let PORTRAIT = false;
function xfit(){
  const w = xapp.clientWidth, h = xapp.clientHeight; if (!w || !h) return;
  const was = PORTRAIT; PORTRAIT = h > w * 1.05 && w < 1000;
  xapp.classList.toggle('portrait', PORTRAIT);
  let sc, W, H;
  if (PORTRAIT){ W = 760; sc = w / W; H = h / sc; }
  else { sc = Math.min(w/1920, h/1080); W = w / sc; H = h / sc; }
  xstage.style.width = W + 'px'; xstage.style.height = H + 'px';
  xstage.style.transform = `translate(-50%,-50%) scale(${sc})`;
  if (was !== PORTRAIT) SL.forEach(s => { if (s.done && s.init){ s.done = false; if (s === SL[xcur]) { s.init(s.el); s.done = true; } } });
}
new ResizeObserver(xfit).observe(xapp); addEventListener('resize', xfit); xfit();

/* navigation */
let xcur = -1, xbusy = false, lastPt = {x:.5, y:.5};
function xgo(i, dirHint){
  i = Math.max(0, Math.min(SL.length-1, i)); if (i === xcur || xbusy) return;
  const prev = SL[xcur], next = SL[i]; const fwd = dirHint ?? (i > xcur);
  xbusy = true; setTimeout(()=>xbusy=false, reduce ? 50 : 650);
  const el = next.el;
  el.style.setProperty('--cx', (lastPt.x*100).toFixed(1)+'%'); el.style.setProperty('--cy', (lastPt.y*100).toFixed(1)+'%');
  const tr = !prev ? 'zoom' : (fwd ? next.tr : 'wipeback');
  const inCls = {iris:'tr-iris-in', wipe:'tr-wipe-in', zoom:'tr-zoom-in', blinds:'tr-blinds-in', wipeback:'tr-wipe-back'}[tr];
  if (prev){ const p = prev.el; p.classList.remove('on'); p.classList.add('out', tr==='zoom'?'tr-out-z':'tr-out');
    p.querySelectorAll('video').forEach(v=>setTimeout(()=>v.pause(), 1100));
    setTimeout(()=>{ p.classList.remove('out','tr-out','tr-out-z'); }, 1150); }
  el.classList.remove('tr-iris-in','tr-wipe-in','tr-zoom-in','tr-blinds-in','tr-wipe-back');
  void el.offsetWidth; if (!reduce) el.classList.add(inCls);
  el.classList.add('on');
  setTimeout(()=>el.classList.remove(inCls), 1200);
  const fl = $('#xflash'); fl.style.setProperty('--cx', (lastPt.x*100)+'%'); fl.style.setProperty('--cy', (lastPt.y*100)+'%'); fl.classList.remove('go'); void fl.offsetWidth; if(!reduce && prev) fl.classList.add('go');
  xstage.classList.add('anim'); clearTimeout(xgo.t); xgo.t = setTimeout(()=>xstage.classList.remove('anim'), 1150);
  xcur = i;
  el.querySelectorAll('.track').forEach(tr => { const c = tr.querySelector('.coin'); if (c) c.style.setProperty('--run', (tr.clientWidth - 108) + 'px'); });
  el.querySelectorAll('video').forEach(v=>{ const p=v.play(); if(p&&p.catch) p.catch(()=>{}); });
  if (next.init && !next.done){ setTimeout(()=>{ try{ next.init(el); next.done = true; }catch(err){ console.warn(err); } }, 380); }
  else if (next.init) { el.querySelectorAll('.ch').forEach(c=>{ c.classList.remove('go'); void c.offsetWidth; setTimeout(()=>c.classList.add('go'), 420); }); }
  el.querySelectorAll('.kring .arc').forEach(a=>{ a.style.strokeDashoffset = a.getAttribute('stroke-dasharray'); requestAnimationFrame(()=>requestAnimationFrame(()=>a.style.strokeDashoffset = a.dataset.off)); });
  el.querySelectorAll('[data-count]').forEach(n=>xcount(n, +n.dataset.count));
  $('#xamb').style.backgroundImage = `url('${next.bg || next.video.replace('.mp4','.jpg')}')`;
  $('#xcnt').textContent = `${i+1} / ${SL.length}`;
  $('#xprog').style.width = `${(i+1)/SL.length*100}%`;
  xdots.querySelectorAll('i').forEach((d,j)=>d.classList.toggle('on', j===i));
  document.querySelectorAll('#xovg .th').forEach((d,j)=>d.classList.toggle('cur', j===i));
  try{ history.replaceState(null,'',`#s${i+1}`); }catch(e){}
}
function xcount(node, target){
  const d = +(node.dataset.dec||0);
  if (reduce){ node.textContent = fmt(target,d); return; }
  const t0 = performance.now(), dur = 1500, from = target*0.5;
  const step = t => { const p = Math.min(1, (t-t0)/dur), e = 1-Math.pow(1-p,4); node.textContent = fmt(from + (target-from)*e, d); if (p<1) requestAnimationFrame(step); };
  setTimeout(()=>requestAnimationFrame(step), 500);
}
const next = () => xgo(xcur+1, true), prev = () => xgo(xcur-1, false);
$('#x-next').onclick = e=>{ e.stopPropagation(); lastPt={x:.85,y:.5}; next(); };
$('#x-prev').onclick = e=>{ e.stopPropagation(); lastPt={x:.15,y:.5}; prev(); };

/* wheel / trackpad */
let wAcc = 0, wLock = 0;
xapp.addEventListener('wheel', e => {
  if ($('#xov').classList.contains('on')) return;
  if (PORTRAIT){ return; }
  e.preventDefault();
  const now = Date.now(); if (now < wLock) { wAcc = 0; return; }
  const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
  wAcc += e.deltaMode === 1 ? d*30 : d;
  if (Math.abs(wAcc) > 45){ lastPt = {x: wAcc>0?.85:.15, y:.5}; (wAcc > 0 ? next : prev)(); wAcc = 0; wLock = now + 900; }
}, {passive:false});

/* pointer: swipe (touch), drag (mouse/pen), tap */
let pd = null;
const interactive = t => t.closest && t.closest('button,a,input,select,[data-go],[data-open],.x-top,.x-bot,.x-ov,.ch,#wf-t');
xapp.addEventListener('pointerdown', e => { if (e.button && e.button!==0) return; pd = {x:e.clientX, y:e.clientY, t:Date.now(), it:interactive(e.target)}; });
xapp.addEventListener('pointerup', e => {
  if (!pd) return; const dx = e.clientX - pd.x, dy = e.clientY - pd.y, adx = Math.abs(dx), ady = Math.abs(dy);
  const r = xapp.getBoundingClientRect(); lastPt = {x:(e.clientX-r.left)/r.width, y:(e.clientY-r.top)/r.height};
  if (e.pointerType==='touch' && Math.max(adx,ady) > 8){ pd = null; return; }
  if (Math.max(adx,ady) > 50 && Date.now()-pd.t < 1600){ if (adx >= ady) (dx < 0 ? next : prev)(); else (dy < 0 ? next : prev)(); }
  else if (Math.max(adx,ady) < 8 && !pd.it && !PORTRAIT && !$('#xov').classList.contains('on')){ (lastPt.x > .3 ? next : prev)(); }
  pd = null;
});
xapp.addEventListener('pointercancel', ()=>pd=null);
let ts = null;
xapp.addEventListener('touchstart', e => { if (e.touches.length===1) ts = {x:e.touches[0].clientX, y:e.touches[0].clientY, t:Date.now()}; }, {passive:true});
xapp.addEventListener('touchmove', e => { if (ts && !PORTRAIT && !e.target.closest('.x-ov')) e.preventDefault(); }, {passive:false});
xapp.addEventListener('touchend', e => {
  if (!ts) return; const t = e.changedTouches[0]; const dx = t.clientX - ts.x, dy = t.clientY - ts.y;
  if (Math.max(Math.abs(dx),Math.abs(dy)) > 45 && Date.now()-ts.t < 1600 && !$('#xov').classList.contains('on')){
    lastPt = {x: dx<0?.85:.15, y:.5};
    if (Math.abs(dx) >= Math.abs(dy) * 1.2) (dx < 0 ? next : prev)(); else if (!PORTRAIT) (dy < 0 ? next : prev)();
  }
  ts = null;
}, {passive:true});

/* delegated buttons */
document.addEventListener('click', e => {
  const g = e.target.closest('[data-go]'); if (g && g.closest('#xapp')){ e.stopPropagation(); closeOv(); const r=xapp.getBoundingClientRect(); lastPt={x:(e.clientX-r.left)/r.width,y:(e.clientY-r.top)/r.height}; xgo(+g.dataset.go); return; }
  const o = e.target.closest('[data-open]'); if (o){ e.stopPropagation(); if (o.dataset.open==='excel') openXL();  }
});

/* keyboard */
addEventListener('keydown', e => {
  if (e.target.closest && e.target.closest('input,textarea')) return;
  const k = e.key;
  if (xvOpen){ if (k==='Escape') closeXL(); return; }
  if (k==='f'||k==='F'||k==='ֆ'){ xfs(); return; }
  if (k==='e'||k==='E'||k==='է'){ openXL(); return; }
  if (xmodeCur!=='deck') return;
  if (k==='o'||k==='O'||k==='օ'||k==='Escape'){ $('#xov').classList.contains('on') ? closeOv() : (k!=='Escape' && openOv()); return; }
  if (['ArrowRight','ArrowDown','PageDown',' ','Enter'].includes(k)){ e.preventDefault(); lastPt={x:.85,y:.5}; next(); }
  else if (['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k)){ e.preventDefault(); lastPt={x:.15,y:.5}; prev(); }
  else if (k==='Home') xgo(0); else if (k==='End') xgo(SL.length-1);
  else if (/^[1-9]$/.test(k)) xgo(+k-1);
});
function xfs(){ try{ if(!document.fullscreenElement) document.documentElement.requestFullscreen().catch(()=>{}); else document.exitFullscreen().catch(()=>{}); }catch(e){} }
$('#b-fs').onclick = xfs;
function openOv(){ $('#xov').classList.add('on'); } function closeOv(){ $('#xov').classList.remove('on'); }
$('#b-ov').onclick = e=>{ e.stopPropagation(); $('#xov').classList.contains('on') ? closeOv() : openOv(); };
$('#xov').addEventListener('click', e => { if (e.target.id==='xov') closeOv(); });

/* particles: pre-rendered glow sprites, half-res canvas, 30 fps, paused when not visible */
(function(){
  if (reduce) return; const ctx = pcv.getContext('2d'); const RES = .5; let P = [], W = 0, H = 0, last = 0, spr = {};
  function sprite(col){ if (spr[col]) return spr[col]; const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
    const gr = g.createRadialGradient(32,32,0,32,32,32); gr.addColorStop(0, col); gr.addColorStop(.22, col+'99'); gr.addColorStop(1, col+'00'); g.fillStyle = gr; g.fillRect(0,0,64,64); return spr[col] = c; }
  function size(){ W = pcv.width = Math.round(xstage.offsetWidth*RES); H = pcv.height = Math.round(xstage.offsetHeight*RES); }
  size(); new ResizeObserver(size).observe(xstage);
  for (let i=0;i<60;i++) P.push({x:Math.random(), y:Math.random(), r:(6+Math.random()*16), v:.0006+Math.random()*.0016, a:Math.random()*6.28, k:Math.random()});
  function tick(t){
    requestAnimationFrame(tick);
    if (t - last < 33 || xapp.hidden || document.hidden || xvOpen) return; last = t;
    ctx.clearRect(0,0,W,H); const A = (SL[xcur] && SL[xcur].acc) || ['#3dff8f','#5cd6ff'];
    const s0 = sprite(A[0]), s1 = sprite(A[1]);
    for (const p of P){ p.y -= p.v; p.a += .02; if (p.y < -.05){ p.y = 1.05; p.x = Math.random(); }
      const sz = p.r*RES*2, x = (p.x + Math.sin(p.a)*.01)*W - sz/2, y = p.y*H - sz/2;
      ctx.globalAlpha = .25 + .45*Math.sin(p.a)**2; ctx.drawImage(p.k > .5 ? s0 : s1, x, y, sz, sz); }
    ctx.globalAlpha = 1;
  }
  requestAnimationFrame(tick);
})();

/* parallax + cursor light + idle chrome — throttled to one update per frame */
let idleT, pmRaf = 0, pmE = null;
xapp.addEventListener('pointermove', e => {
  if (xapp.classList.contains('idle')) xapp.classList.remove('idle');
  clearTimeout(idleT); idleT = setTimeout(()=>xapp.classList.add('idle'), 3200);
  if (reduce || e.pointerType !== 'mouse') return;
  pmE = e; if (pmRaf) return;
  pmRaf = requestAnimationFrame(() => { pmRaf = 0; const ev = pmE; const s = SL[xcur]; if (!s) return;
    const r = xapp.getBoundingClientRect(); const nx = (ev.clientX-r.left)/r.width - .5, ny = (ev.clientY-r.top)/r.height - .5;
    s.el.querySelectorAll('.x-par').forEach(p => { const d = +(p.dataset.depth||8); p.style.transform = `translate3d(${(-nx*d).toFixed(1)}px,${(-ny*d).toFixed(1)}px,0)`; });
    const gl = s.el.querySelector('.x-glow'); if (gl){ gl.classList.add('v'); gl.style.transform = `translate3d(${((nx+.5)*xstage.offsetWidth).toFixed(0)}px,${((ny+.5)*xstage.offsetHeight).toFixed(0)}px,0)`; }
    const c = ev.target.closest && ev.target.closest('.x-card,.act'); if (c){ const cr = c.getBoundingClientRect(); c.style.setProperty('--mx', ((ev.clientX-cr.left)/cr.width*100).toFixed(0)+'%'); c.style.setProperty('--my', ((ev.clientY-cr.top)/cr.height*100).toFixed(0)+'%'); }
  });
});
document.addEventListener('visibilitychange', () => { const s = SL[xcur]; if (!s) return; s.el.querySelectorAll('video').forEach(v => document.hidden ? v.pause() : (!xapp.hidden && v.play().catch(()=>{}))); });


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
const numCell = (sh, r, c, opts={}) => {
  const d = cv(sh, r, c); const v = d.v; const ref = colL(c) + r;
  if (typeof v !== 'number') return `<td class="dc0">${v==null?'':esc(v)}</td>`;
  const dec = opts.dec ?? (d.nf || 0);
  let inner = `<span class="nv">${fmt(v, dec)}</span>`;
  if (opts.kind === 'chg') inner = `<span class="chg ${v>1e-9?'up':(v<-1e-9?'dn':'eq')}">${v>1e-9?'▲':(v<-1e-9?'▼':'●')} ${sgn(v, dec)}</span>`;
  if (opts.kind === 'gr'){ const t = Math.max(0, Math.min(1, v/200)); inner = `<span class="grw ${v>=100?'up':'dn'}"><span class="gm"><i style="width:${(t*100).toFixed(1)}%"></i></span>${fmt(v,1)}%</span>`; }
  if (opts.kind === 'st') inner = `<span class="nv">${fmt(v,2)}</span><span class="stb"><i style="width:${Math.max(0,Math.min(100,Math.abs(v))).toFixed(1)}%"></i></span>`;
  if (opts.kind === 'bar'){ const w = Math.min(100, Math.abs(v)/opts.max*100); inner = `<span class="vb"><i style="width:${w.toFixed(1)}%;background:${opts.col}"></i></span><span class="nv">${fmt(v, dec)}</span>`; }
  return `<td class="num${d.f?' fx':''}" data-sh="${XL.indexOf(sh)}" data-ref="${ref}" tabindex="0">${inner}</td>`;
};
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
function drFx(el){
  document.querySelectorAll('#dr .sel,#dr .prec').forEach(x => { x.classList.remove('sel','prec'); x.style.removeProperty('--pc'); });
  if (!el){ $('#dr-fx').innerHTML = `<span class="fxk">fx</span><span class="fxh">Սեղմեք ցանկացած թվի վրա՝ Excel-ի բանաձևը տեսնելու համար</span>`; return; }
  const sh = XL[+el.dataset.sh]; const ref = el.dataset.ref; const m = /([A-Z]+)(\d+)/.exec(ref); const d = cv(sh, +m[2], colN(m[1]));
  el.classList.add('sel');
  let fx = '';
  if (d.f){ const refs = parseRefs(d.f); let last = 0;
    refs.forEach((rf,k) => { const col = DRC[k % DRC.length]; fx += esc(d.f.slice(last, rf.idx)) + `<b style="color:${col}">${esc(rf.txt)}</b>`; last = rf.idx + rf.txt.length;
      if (!rf.sheet) for (let rr=rf.r1; rr<=rf.r2; rr++) for (let cc=rf.c1; cc<=rf.c2; cc++){ document.querySelectorAll(`#dr [data-sh="${el.dataset.sh}"][data-ref="${colL(cc)}${rr}"]`).forEach(t => { t.classList.add('prec'); t.style.setProperty('--pc', col); }); } });
    fx += esc(d.f.slice(last));
  } else fx = '<span class="fxh">մուտքային արժեք (դասախոսի տվյալ)</span>';
  $('#dr-fx').innerHTML = `<span class="fxk">${esc(ref)}</span><span class="fxf">${fx}</span><span class="fxr">= ${fmt(d.v, d.nf ?? 3)}</span>`;
}
const DRC = ['#5cd6ff','#ff6bd6','#ffb547','#3dff8f','#a98bff','#c8ff4d','#3dffe0','#ff5c7a'];
$('#dr-nav').innerHTML = DRS.map((s,i) => `<button data-s="${s.id}" style="--a:${s.acc}"><i>${String(i+1).padStart(2,'0')}</i><span><b>${esc(s.t)}</b><small>${esc(s.s)}</small></span></button>`).join('');
$('#dr-nav').addEventListener('click', e => { const b = e.target.closest('button'); if (b) drSection(b.dataset.s); });
$('#dr-main').addEventListener('click', e => { const c = e.target.closest('[data-ref]'); if (c) drFx(c); });
$('#dr-main').addEventListener('keydown', e => { if (e.key==='Enter'){ const c = e.target.closest('[data-ref]'); if (c) drFx(c); } });
function openXL(){ if (!xvOpen) drSection(drCur); xvOpen = true; const s = SL[xcur]; s && s.el.querySelectorAll('video').forEach(v=>v.pause()); $('#dr').classList.add('on'); try{ history.replaceState(null,'','#excel'); }catch(e){} }
function closeXL(){ xvOpen = false; $('#dr').classList.remove('on'); const s = SL[xcur]; s && s.el.querySelectorAll('video').forEach(v=>v.play().catch(()=>{})); try{ history.replaceState(null,'', `#s${xcur+1}`); }catch(e){} }
$('#dr-close').onclick = closeXL;
const XLSX_B64 = '/*__XLSX__*/', XLSX_NAME = 'Tema8-9_Debitor_Kreditor_Hrachya_Aslanyan.xlsx';
let dlApi; try{ dlApi = window.claude && window.claude.use ? window.claude.use('downloads').catch(()=>null) : Promise.resolve(null); }catch(e){ dlApi = Promise.resolve(null); }
$('#dr-dl').onclick = async () => {
  const b = $('#dr-dl'); const bin = atob(XLSX_B64); const u8 = new Uint8Array(bin.length); for (let i=0;i<bin.length;i++) u8[i] = bin.charCodeAt(i);
  const blob = new Blob([u8], {type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
  const api = await Promise.race([dlApi, new Promise(r=>setTimeout(()=>r(null),1500))]);
  if (api){ try{ await api.save({filename:XLSX_NAME, data:blob}); b.classList.add('ok'); setTimeout(()=>b.classList.remove('ok'),2000); return; }catch(e){ if (e && e.code==='declined') return; } }
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = XLSX_NAME; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
  b.classList.add('ok'); setTimeout(()=>b.classList.remove('ok'),2000);
}; $('#b-xl').onclick = e => { e.stopPropagation(); openXL(); };

/* preloader: waits for images + first video (max 9s), shows real progress */
function preload(){
  const pl = $('#pl'); if (!pl) return Promise.resolve();
  const list = [...new Set(Object.values(IMG))].map(u => ({u, t:'img'})).concat(Object.values(VID).map(u => ({u, t:'vid'})));
  let done = 0; const arc = $('#pl-arc'), pct = $('#pl-pct');
  const tick = () => { done++; const p = done / list.length; arc.style.strokeDashoffset = (326.7*(1-p)).toFixed(1); pct.textContent = Math.round(p*100) + '%'; };
  const one = a => new Promise(res => {
    let fin = false; const ok = () => { if (fin) return; fin = true; tick(); res(); };
    if (a.t === 'img'){ const im = new Image(); im.onload = im.onerror = ok; im.decoding = 'async'; im.src = a.u; if (im.complete) ok(); }
    else { const v = document.createElement('video'); v.muted = true; v.preload = 'auto'; v.onloadeddata = v.onerror = ok; v.src = a.u; v.load(); setTimeout(ok, 6000); }
  });
  return Promise.race([Promise.all(list.map(one)), new Promise(r => setTimeout(r, 9000))]).then(() => {
    arc.style.strokeDashoffset = 0; pct.textContent = '100%'; $('#pl-s').textContent = 'Պատրաստ է';
    return new Promise(r => setTimeout(() => { pl.classList.add('bye'); setTimeout(() => pl.remove(), 900); r(); }, 250));
  });
}

/* boot */
(function(){
  preload();
  const h = location.hash, m = /^#s(\d+)$/.exec(h);
  xgo(m ? Math.min(SL.length, +m[1]) - 1 : 0);
  document.body.style.overflow = 'hidden';
  if (h === '#excel') openXL();
  idleT = setTimeout(()=>xapp.classList.add('idle'), 4000);
})();
