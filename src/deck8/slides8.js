/* ======================= Lesson 8 (Topics 8–9) deck ======================= */
const XL = /*__XL__*/;
const $ = (s, r=document) => r.querySelector(s);
const fmt = (n, d=0) => (n==null||n==='x') ? '–' : Number(n).toLocaleString('en-US',{minimumFractionDigits:d, maximumFractionDigits:d});
const sgn = (n, d=0) => (n>0?'+':(n<0?'−':'')) + fmt(Math.abs(n), d);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const IMG = {yerevan:'../assets/img/yerevan.jpg', desk:'../assets/img/desk.jpg', warehouse:'../assets/img/warehouse.jpg', factory:'../assets/img/factory.jpg', bank:'../assets/img/bank.jpg', hourglass:'../assets/img/hourglass.jpg', team:'../assets/img/team.jpg', cashier:'../assets/img/cashier.jpg'};
const VID = {city:'../assets/bg-city.mp4', flow:'../assets/bg-flow.mp4', bars:'../assets/bg-bars.mp4'};
const G = {in:'#3dff8f', out:'#ff5c7a', net:'#c8ff4d', sky:'#5cd6ff', vio:'#a98bff', gold:'#ffb547', pink:'#ff6bd6', text:'#f2f7f4', sub:'#b9c6c0', dim:'#7f8d88'};
const split = (t, d0=300) => t.split(' ').map((w,i)=>`<span class="w" style="--w:${i};--d0:${d0}ms">${w}</span>`).join(' ');
const X_ = (i, kind='') => `data-x${kind?`="${kind}"`:''} style="--i:${i}"`;
const SD = XL[0], SK = XL[1];
const v = (sh, r, c) => (sh.cells[`${r},${c}`]||{}).v;
const D = (r, y) => v(SD, r, y ? 5 : 4), K = (r, y) => v(SK, r, y ? 5 : 4);

/* ---- small HTML/SVG chart builders (animate when the slide is .on) ---- */
function ringSVG(val, base, color, id, dec=0, cap='2025'){
  const r = 92, C = 2*Math.PI*r, frac = Math.max(.05, Math.min(1, Math.abs(val)/Math.max(Math.abs(val),Math.abs(base))));
  return `<svg viewBox="0 0 220 220"><defs><linearGradient id="rg${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="${color}"/><stop offset="1" stop-color="${color}" stop-opacity=".55"/></linearGradient></defs>
    <circle cx="110" cy="110" r="${r}" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.1)" stroke-width="16"/>
    <circle class="arc" cx="110" cy="110" r="${r}" fill="none" stroke="url(#rg${id})" stroke-width="16" stroke-linecap="round" transform="rotate(-90 110 110)" stroke-dasharray="${C}" stroke-dashoffset="${C}" data-off="${C*(1-frac)}" style="filter:drop-shadow(0 0 10px ${color})"/>
    <text x="110" y="104" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-weight="600" font-size="${dec?36:(Math.abs(val)>=1e7?24:30)}" fill="${G.text}" data-count="${val}" data-dec="${dec}">${fmt(val,dec)}</text>
    <text x="110" y="134" text-anchor="middle" font-size="15" fill="${G.sub}" font-family="Noto Sans Armenian, sans-serif">${cap}</text></svg>`;
}
/* bridge (waterfall) in HTML: start, +in, −out, =end */
function bridge(vals, labels, colors, h=430){
  const mx = Math.max(vals[0]+vals[1], vals[3]) * 1.08; let run = 0;
  return `<div class="bridge" style="--h:${h}px">${vals.map((x,i)=>{
    let lo, hi; if (i===0){ lo=0; hi=x; run=x; } else if (i===1){ lo=run; hi=run+x; run=hi; } else if (i===2){ hi=run; lo=run-x; run=lo; } else { lo=0; hi=x; }
    return `<div class="bc" style="--i:${i}"><div class="bv">${i===1?'+':(i===2?'−':'')}${fmt(x)}</div><div class="bt"><i style="bottom:${(lo/mx*100).toFixed(2)}%;height:${((hi-lo)/mx*100).toFixed(2)}%;--c:${colors[i]}"></i></div><div class="bl">${labels[i]}</div></div>`; }).join('')}</div>`;
}
/* grouped bars 2024 vs 2025 */
function pairBars(cats, a, b, opts={}){
  const mx = Math.max(...a, ...b) * 1.1, ca = opts.ca || 'rgba(255,255,255,.45)', cb = opts.cb || G.in, d = opts.dec||0;
  return `<div class="pbx" style="--h:${opts.h||380}px">${cats.map((c,i)=>`<div class="pgx" style="--i:${i}">
     <div class="ppx"><span class="pvx a">${fmt(a[i],d)}</span><i class="a" style="height:${(a[i]/mx*100).toFixed(2)}%;--c:${ca}"></i></div>
     <div class="ppx"><span class="pvx b">${fmt(b[i],d)}</span><i class="b" style="height:${(b[i]/mx*100).toFixed(2)}%;--c:${cb}"></i></div>
     <div class="plx">${c}</div></div>`).join('')}</div>
   <div class="plg"><span><i style="background:${ca}"></i>2024</span><span><i style="background:${cb}"></i>2025</span></div>`;
}
function donutSVG(parts, cols, label, sub){
  const tot = parts.reduce((s,p)=>s+p.v,0); let a0 = -90; const R = 120, r = 74;
  const P = (a, rr) => { const t = a*Math.PI/180; return [150 + rr*Math.cos(t), 150 + rr*Math.sin(t)]; };
  const seg = parts.map((p,i)=>{ const a1 = a0 + p.v/tot*360 - .6; const L = a1-a0 > 180 ? 1 : 0;
    const [x0,y0]=P(a0,R),[x1,y1]=P(a1,R),[x2,y2]=P(a1,r),[x3,y3]=P(a0,r);
    const d = `M${x0} ${y0} A${R} ${R} 0 ${L} 1 ${x1} ${y1} L${x2} ${y2} A${r} ${r} 0 ${L} 0 ${x3} ${y3}Z`; a0 = a1 + .6;
    return `<path class="dseg" style="--i:${i}" d="${d}" fill="${cols[i%cols.length]}"><title>${esc(p.n)}: ${fmt(p.v)}</title></path>`; }).join('');
  return `<svg viewBox="0 0 300 300" class="donut">${seg}<text x="150" y="146" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="30" font-weight="700" fill="${G.text}">${label}</text><text x="150" y="174" text-anchor="middle" font-size="15" fill="${G.sub}" font-family="Noto Sans Armenian, sans-serif">${sub}</text></svg>`;
}
function clockSVG(days, color, id){
  const a = Math.min(1, days/30) * 360; const R = 86, C = 2*Math.PI*R;
  let ticks = ''; for (let k=0;k<30;k++){ const t=(k*12-90)*Math.PI/180, r1=k%5?96:92; ticks += `<line x1="${110+r1*Math.cos(t)}" y1="${110+r1*Math.sin(t)}" x2="${110+102*Math.cos(t)}" y2="${110+102*Math.sin(t)}" stroke="rgba(255,255,255,${k%5?.25:.6})" stroke-width="${k%5?1.5:3}"/>`; }
  return `<svg viewBox="0 0 220 220" class="clock">${ticks}<circle cx="110" cy="110" r="${R}" fill="rgba(0,0,0,.25)" stroke="rgba(255,255,255,.08)" stroke-width="12"/>
    <circle class="arc" cx="110" cy="110" r="${R}" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round" transform="rotate(-90 110 110)" stroke-dasharray="${C}" stroke-dashoffset="${C}" data-off="${C*(1-a/360)}" style="filter:drop-shadow(0 0 10px ${color})"/>
    <g class="hand" style="--a:${a}deg"><line x1="110" y1="110" x2="110" y2="40" stroke="${G.text}" stroke-width="4" stroke-linecap="round"/></g><circle cx="110" cy="110" r="7" fill="${color}"/>
    <text x="110" y="150" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="26" font-weight="700" fill="${G.text}" data-count="${days}" data-dec="1">${fmt(days,1)}</text><text x="110" y="172" text-anchor="middle" font-size="13" fill="${G.sub}" font-family="Noto Sans Armenian, sans-serif">օր</text></svg>`;
}
function miniPair(a, b, d, better){ // two horizontal bars + verdict
  const mx = Math.max(a,b)*1.15 || 1; const good = better==='down' ? b<=a : b>=a;
  return `<div class="mp"><div class="r"><span>2024</span><b style="width:${(a/mx*100).toFixed(1)}%" class="a"></b><em>${fmt(a,d)}</em></div>
    <div class="r"><span>2025</span><b style="width:${(b/mx*100).toFixed(1)}%" class="${good?'g':'r'}"></b><em>${fmt(b,d)}</em></div></div>
    <span class="x-pill ${good?'x-good':'x-bad'}">${good?'✔ Լավացել է':'✖ Վատացել է'} ${sgn(b-a,d)}</span>`;
}
const frac = (a,b) => `<span class="frac"><span>${a}</span><span>${b}</span></span>`;
function ornament(){
  let arms = '';
  for (let i=0;i<8;i++){ arms += `<path d="M310 310 C 330 250, 400 230, 420 170 C 432 130, 400 100, 370 112" transform="rotate(${i*45} 310 310)" fill="none" stroke="url(#og)" stroke-width="14" stroke-linecap="round"/>`; }
  return `<div class="ornament x-par" data-depth="-14" aria-hidden="true">
   <svg viewBox="0 0 620 620"><defs><radialGradient id="orb" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="rgba(255,255,255,.32)"/><stop offset=".5" stop-color="rgba(61,255,143,.07)"/><stop offset="1" stop-color="rgba(61,255,143,0)"/></radialGradient></defs>
     <circle cx="310" cy="310" r="300" fill="url(#orb)" stroke="rgba(255,255,255,.18)" stroke-width="1.5"/>
     <circle cx="310" cy="310" r="268" fill="none" stroke="rgba(61,255,143,.35)" stroke-width="1.5" stroke-dasharray="2 14"/>
     <ellipse cx="230" cy="150" rx="120" ry="44" fill="rgba(255,255,255,.10)" transform="rotate(-28 230 150)"/></svg>
   <svg class="orn-spin" viewBox="0 0 620 620"><defs><linearGradient id="og" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d7ffe6"/><stop offset=".45" stop-color="#3dff8f"/><stop offset="1" stop-color="#18b9a0"/></linearGradient>
     <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
     <g filter="url(#glow)">${arms}<circle cx="310" cy="310" r="36" fill="none" stroke="url(#og)" stroke-width="12"/></g></svg>
  </div>`;
}
const ICO = {
  play:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
  grid:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>',
  home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l9-7 9 7v9a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1z"/></svg>',
  dl:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M7 10l5 5 5-5M4 19h16"/></svg>'
};

/* ---------------- slides ---------------- */
const debt = [4,5,6,7,8,9,10].map(r => ({n:`ԴՊ-${r-3}`, a:D(r,0), b:D(r,1)}));
const SL = [
 {t:'Տիտղոսաթերթ', bg:IMG.yerevan, shade:'shade-left', tr:'zoom', html:()=>`
   ${ornament()}
   <div class="x-pad" style="justify-content:center">
     <div class="x-kick" ${X_(0)}>Դաս 8 · Թեմա 8–9 · Տնային աշխատանք</div>
     <h1 class="x-h1" style="max-width:1150px;font-size:96px">${split('Դեբիտորական և կրեդիտորական',350)}<br><span class="x-grad">${split('պարտքերի վերլուծություն',650)}</span></h1>
     <p class="x-lead" ${X_(3)}>Ո՞վ է մեզ պարտք, ո՞ւմ ենք մենք պարտք և որքա՞ն արագ է փողը վերադառնում · 2024 և 2025</p>
     <div class="author" ${X_(4,'left')}>
       <div class="av">ՀԱ</div>
       <div><div class="nm">Հրաչյա Ասլանյան</div><div class="rl">Հեղինակ · ՀԱՊՀ, ԻՏ447 խումբ · Դասախոս՝ Օ.Ա. Գալստյան</div></div>
     </div>
     <div class="cta" ${X_(5)}>
       <button class="x-btn" data-go="1">${ICO.play}Սկսել ներկայացումը</button>
       <button class="x-btn xl" data-open="excel">${ICO.grid}Բացել աղյուսակները</button>
       <a class="x-btn ghost" href="../lesson-8.html">${ICO.home}Դասի էջ</a>
     </div>
   </div>`},
 {t:'Ճանապարհային քարտեզ', bg:IMG.desk, shade:'shade-full', tr:'wipe', html:()=>{
   const st = [[40,400,'Ի՞նչ են պարտքերը','ԴՊ և ԿՊ պարզ բառերով',2],[310,160,'Գլխավոր թվերը','2024 → 2025',3],[580,340,'Դեբիտորական','Շարժ, կազմ, պտույտ',4],[850,130,'Կրեդիտորական','Շարժ, կառուցվածք, պտույտ',8],[1120,310,'Համեմատություն','Օրերի «մրցավազք» և Գդկհ',11],[1360,90,'Եզրակացություն','Աղյուսակներ և առաջարկներ',13]];
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Ճանապարհային քարտեզ</div><h2 class="x-h2">${split('Ինչ ենք անելու այսօր')}</h2>
   <div class="road">
     <svg class="path" viewBox="0 0 1660 560" preserveAspectRatio="none"><defs><linearGradient id="rdg" x1="0" x2="1"><stop offset="0" stop-color="#3dff8f"/><stop offset="1" stop-color="#5cd6ff"/></linearGradient></defs>
       <path class="dash" d="M79 439 C 214 439 212 199 349 199 S 484 379 619 379 S 754 169 889 169 S 1024 349 1159 349 S 1264 129 1399 129" fill="none" stroke="url(#rdg)" stroke-width="5" stroke-linecap="round" style="filter:drop-shadow(0 0 10px rgba(61,255,143,.6))"/></svg>
     ${st.map((s,i)=>`<div class="stop" data-go="${s[4]}" data-x="pop" style="left:${s[0]}px;top:${s[1]}px;--i:${2+i}"><div class="n">${i+1}</div><h5>${s[2]}</h5><p>${s[3]}</p></div>`).join('')}
   </div></div>`}},
 {t:'Ի՞նչ են ԴՊ-ն և ԿՊ-ն', video:VID.flow, shade:'shade-full', tr:'iris', html:()=>`
   <div class="x-pad"><div class="x-kick" ${X_(0)}>Նախ՝ պարզ բառերով</div><h2 class="x-h2">${split('Ո՞վ ում է պարտք')}</h2>
   <div class="chain">
     <div class="x-card nd" ${X_(2,'pop')}><div class="ic">🏭</div><h4>Մատակարար</h4><p>Տվել է մեզ հումք, բայց փողը դեռ չի ստացել</p></div>
     <div class="ar" ${X_(3)}><span class="lb x-vio">ԿՊ</span><svg viewBox="0 0 200 40"><path d="M190 20H10M30 6L10 20l20 14" fill="none" stroke="${G.vio}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><small>մենք ենք պարտք</small></div>
     <div class="x-card nd me" ${X_(4,'pop')}><div class="ic">🏢</div><h4>Մեր ընկերությունը</h4><p>&lt;&lt;XXX&gt;&gt; ՍՊԸ</p></div>
     <div class="ar" ${X_(5)}><span class="lb x-in">ԴՊ</span><svg viewBox="0 0 200 40"><path d="M10 20h180M170 6l20 14-20 14" fill="none" stroke="${G.in}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><small>մեզ են պարտք</small></div>
     <div class="x-card nd" ${X_(6,'pop')}><div class="ic">🛒</div><h4>Գնորդ</h4><p>Ստացել է ապրանքը, բայց դեռ չի վճարել</p></div>
   </div>
   <div class="defs">
     <div class="x-card" ${X_(7,'left')}><h4><span class="x-in">ԴՊ</span> · Դեբիտորական պարտք</h4><p class="x-p">Այն փողը, որ <b>ուրիշները պետք է մեզ վճարեն</b>։ Որքան արագ են վերադարձնում, այնքան լավ։</p></div>
     <div class="x-card" ${X_(8,'right')}><h4><span class="x-vio">ԿՊ</span> · Կրեդիտորական պարտք</h4><p class="x-p">Այն փողը, որ <b>մենք պետք է վճարենք ուրիշներին</b>։ Դա «անվճար վարկ» է, բայց ժամկետանցը վտանգավոր է։</p></div>
   </div></div>`},
 {t:'Գլխավոր թվերը', video:VID.city, shade:'shade-full', tr:'zoom', html:()=>{
   const it=[['ԴՊ տարեվերջին',D(21,0),D(21,1),G.out,-1,0,'դրամ'],['Իրացումից հասույթ',D(26,0),D(26,1),G.in,1,0,'դրամ'],['ԿՊ տարեվերջին',K(33,0),K(33,1),G.vio,0,0,'դրամ'],['Գդկհ = ԴՊ ÷ ԿՊ',K(41,0),K(41,1),G.gold,0,3,'']];
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Գլխավոր թվերը</div><h2 class="x-h2">${split('2024 → 2025․ ինչ փոխվեց')}</h2>
   <div class="kgrid">${it.map((k,i)=>{const d=k[2]-k[1]; const cls = k[4]===0 ? '' : (d*k[4]>0?'x-good':'x-bad'); return `<div class="x-card kring" ${X_(2+i,'pop')}>${ringSVG(k[2],k[1],k[3],i,k[5])}
     <div class="lb">${k[0]}</div><div class="from">2024՝ ${fmt(k[1],k[5])}</div><div style="margin-top:12px"><span class="x-pill ${cls}">${sgn(d,k[5])}${k[5]?'':` · ${sgn((k[2]/k[1]-1)*100,1)}%`}</span></div></div>`}).join('')}</div>
   <p class="x-lead" style="font-size:27px" ${X_(7)}>Վաճառքն աճել է <b class="x-in">+47%</b>, բայց մեզ տրված պարտքերն աճել են <b class="x-out">2.25 անգամ</b>։ Գնորդներն ավելի ուշ են վճարում, իսկ մենք մեր պարտքերը մարում ենք ավելի արագ։</p></div>`}},
 {t:'ԴՊ շարժը', video:VID.bars, shade:'shade-solid', tr:'wipe', html:()=>`
   <div class="x-pad"><div style="display:flex;justify-content:space-between;align-items:flex-end;gap:30px">
     <div><div class="x-kick" ${X_(0)}>Դեբիտորական պարտքերի «կամուրջ»</div><h2 class="x-h2">${split('Որտեղի՞ց աճեց պարտքը')}</h2></div>
     <div class="x-card yt" ${X_(2)}><button class="x-btn ghost" data-y="0">2024</button><button class="x-btn" data-y="1">2025</button></div></div>
   <div class="split2">
     <div class="x-card" style="padding:28px 34px" ${X_(3,'left')}><div class="br-host"></div></div>
     <div class="side" ${X_(4,'right')}>
       <div class="x-card"><h4>Բանաձևը</h4><p class="x-p">Սկզբի մնացորդ <b class="x-in">+ ձևավորված</b> <b class="x-out">− մարված</b> = վերջի մնացորդ</p></div>
       <div class="x-card br-txt"></div></div></div></div>`,
   init(el){ const set = y => { $('.br-host',el).innerHTML = bridge([D(3,y),D(12,y),D(20,y),D(21,y)],['Տարեսկզբին','Ձևավորվեց','Մարվեց','Տարեվերջին'],[G.sky,G.in,G.out,G.gold]);
       const rate = D(20,y)/(D(3,y)+D(12,y))*100;
       $('.br-txt',el).innerHTML = `<h4>${y?2025:2024}</h4><p class="x-p">Տարվա ընթացքում ձևավորվեց <b class="x-in">${fmt(D(12,y))}</b>, բայց մարվեց ընդամենը <b class="x-out">${fmt(D(20,y))}</b>։ Մարման մակարդակը՝ <b class="x-net">${fmt(rate,1)}%</b>։</p>`;
       el.querySelectorAll('.yt button').forEach(b => b.className = 'x-btn' + (+b.dataset.y===y?'':' ghost')); };
     el.querySelectorAll('.yt button').forEach(b => b.onclick = e => { e.stopPropagation(); set(+b.dataset.y); }); set(1); }},
 {t:'Դեբիտորների կառուցվածք', bg:IMG.cashier, shade:'shade-solid', tr:'blinds', html:()=>{ const tot1 = debt.reduce((s,x)=>s+x.b,0);
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Կազմ և կառուցվածք</div><h2 class="x-h2">${split('Ո՞վ է ամենաշատը պարտք')}</h2>
   <div class="split2" style="grid-template-columns:1fr 520px">
     <div class="x-card" style="padding:26px 30px" ${X_(2,'left')}>${pairBars(debt.map(x=>x.n), debt.map(x=>x.a), debt.map(x=>x.b), {h:400, cb:G.in})}</div>
     <div class="side" ${X_(3,'right')}><div class="x-card" style="display:flex;align-items:center;gap:20px">${donutSVG(debt.map(x=>({n:x.n,v:x.b})), ['#3dff8f','#5cd6ff','#a98bff','#ff6bd6','#ffb547','#c8ff4d','#3dffe0'], fmt(tot1/1e6,3), 'մլն · 2025')}
       <div class="lgd">${debt.map((x,i)=>`<span><i style="background:${['#3dff8f','#5cd6ff','#a98bff','#ff6bd6','#ffb547','#c8ff4d','#3dffe0'][i]}"></i>${x.n} · ${fmt(x.b/tot1*100,1)}%</span>`).join('')}</div></div>
       <div class="x-card"><p class="x-p">2025-ին ամենամեծ պարտապանը <b class="x-sky">ԴՊ-2</b>-ն է (<b>32%</b>), իսկ <b class="x-in">ԴՊ-6</b>-ի պարտքը 4.6 անգամ աճեց։ Փոխարենը <b class="x-out">ԴՊ-3</b>-ը գրեթե ամբողջությամբ փակեց պարտքը։</p></div></div></div></div>`}},
 {t:'ԴՊ շրջանառելիություն', bg:IMG.hourglass, shade:'shade-left', tr:'zoom', html:()=>`
   <div class="x-pad"><div class="x-kick" ${X_(0)}>Շրջանառելիություն</div><h2 class="x-h2">${split('Գնորդները վճարում են երկու անգամ ավելի ուշ')}</h2>
   <div class="trio">
     <div class="x-card st" ${X_(2,'pop')}><div class="k">ՇՐՋ<sub>դպ</sub> = ԻՀ ÷ ԴՊ<sub>միջին</sub></div><div class="dual"><div><small>2024</small><b>${fmt(D(33,0),1)}</b></div><span>→</span><div><small>2025</small><b class="x-out">${fmt(D(33,1),1)}</b></div></div><p class="x-p">Տարվա ընթացքում պարտքը քանի՞ անգամ է «պտտվում»՝ գոյանում և վերադառնում։ Քիչ պտույտ՝ դանդաղ փող։</p></div>
     <div class="x-card st clk" ${X_(3,'pop')}><div class="k">T<sub>օր</sub> = 360 ÷ ՇՐՋ<sub>դպ</sub></div><div class="clocks"><div>${clockSVG(D(34,0),'rgba(255,255,255,.6)','c0')}<small>2024</small></div><div>${clockSVG(D(34,1),G.out,'c1')}<small>2025</small></div></div><p class="x-p">Միջինում քանի՞ օր է սպասում ընկերությունը, որ գնորդը վճարի։</p></div>
     <div class="x-card st warn" ${X_(4,'pop')}><div class="k">±ΔԴՄ = (T¹ − T⁰) × ԻՀ¹ ÷ 360</div><div class="big x-out" data-count="${D(39,0)==='x'?v(SD,39,6):0}">${fmt(v(SD,39,6))}</div><p class="x-p">դրամ «սառեցվեց» գնորդների մոտ։ Այդքան փող ընկերությունը ստիպված էր լրացուցիչ գտնել շրջանառության համար։</p></div>
   </div></div>`},
 {t:'ԴՊ որակը', bg:IMG.bank, shade:'shade-solid', tr:'iris', html:()=>{
   const it=[['Գտկ','ԴՊ-ի կշիռը ընթացիկ ակտիվներում','ԴՊ ÷ ԸԱ',35,'down','Ակտիվների որքան մասն է «պարտքի տեսքով»'],['Գդպ','Վաճառքի որքան մասն է դարձել պարտք','ԴՊ<sub>ձևավ</sub> ÷ ԻՀ',36,'down','Որքան քիչ, այնքան շատ ենք կանխիկ վաճառում'],['Գռդպ','Ռիսկային պարտքերի կշիռ','ՌԴՊ ÷ ԴՊ',37,'down','Պարտքեր, որոնք կարող են չվերադառնալ'],['Գադպ','Անհուսալի պարտքերի կշիռ','ԱԴՊ ÷ ԴՊ',38,'down','Գրեթե կորած փող']];
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Պարտքերի որակը</div><h2 class="x-h2">${split('Չորս գործակից՝ մեկ հայացքով')}</h2>
   <div class="q4">${it.map((q,i)=>`<div class="x-card qc" ${X_(2+i,'pop')}><div class="code">${q[0]}</div><h4>${q[1]}</h4><div class="fx">${q[0]} = ${q[2]}</div>${miniPair(D(q[3],0),D(q[3],1),3,q[4])}<p class="x-p" style="font-size:18px;margin-top:12px">${q[5]}</p></div>`).join('')}</div>
   <p class="x-lead" style="font-size:25px" ${X_(6)}>Երեքը լավացել են, բայց <b class="x-out">ռիսկային պարտքերի կշիռը 2.3 անգամ աճել է</b>՝ սա գլխավոր ահազանգն է։</p></div>`}},
 {t:'ԿՊ շարժը', video:VID.bars, shade:'shade-solid', tr:'wipe', html:()=>`
   <div class="x-pad"><div style="display:flex;justify-content:space-between;align-items:flex-end;gap:30px">
     <div><div class="x-kick" ${X_(0)}>Կրեդիտորական պարտքերի «կամուրջ»</div><h2 class="x-h2">${split('Մեր պարտքերը ուրիշներին')}</h2></div>
     <div class="x-card yt" ${X_(2)}><button class="x-btn ghost" data-y="0">2024</button><button class="x-btn" data-y="1">2025</button></div></div>
   <div class="split2">
     <div class="x-card" style="padding:28px 34px" ${X_(3,'left')}><div class="br-host"></div></div>
     <div class="side" ${X_(4,'right')}>
       <div class="x-card"><h4>Բանաձևը</h4><p class="x-p">ԿՊ<sub>վերջ</sub> = ԿՊ<sub>սկիզբ</sub> <b class="x-vio">+ ձևավորված</b> <b class="x-in">− մարված</b></p></div>
       <div class="x-card br-txt"></div></div></div></div>`,
   init(el){ const set = y => { $('.br-host',el).innerHTML = bridge([K(6,y),K(14,y),K(22,y),K(33,y)],['Տարեսկզբին','Ձևավորվեց','Մարվեց','Տարեվերջին'],[G.sky,G.vio,G.in,G.gold]);
       $('.br-txt',el).innerHTML = `<h4>${y?2025:2024}</h4><p class="x-p">Նոր պարտքեր՝ <b class="x-vio">${fmt(K(14,y))}</b>, մարվել է <b class="x-in">${fmt(K(22,y))}</b>։ Միջին պարտքը՝ <b class="x-net">${fmt(K(34,y))}</b>։</p>`;
       el.querySelectorAll('.yt button').forEach(b => b.className = 'x-btn' + (+b.dataset.y===y?'':' ghost')); };
     el.querySelectorAll('.yt button').forEach(b => b.onclick = e => { e.stopPropagation(); set(+b.dataset.y); }); set(1); }},
 {t:'ԿՊ կառուցվածք', bg:IMG.warehouse, shade:'shade-solid', tr:'blinds', html:()=>{ const g=[[49,'Մատակարարներ',G.vio],[50,'Կանխավճարներ',G.sky],[51,'Այլ',G.gold]];
   const sh=[['ՏԿ<sub>կպ</sub>','ԿՊ-ի կշիռը ընթացիկ պարտավորություններում',37,'down'],['ՏԿ<sub>մատ</sub>','Մատակարարներ + կանխավճարներ ԿՊ-ում',38,'info'],['ՏԿ<sub>ժ.անց</sub>','Ժամկետանց պարտքերի կշիռ',39,'down']];
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Կազմ և կշիռներ</div><h2 class="x-h2">${split('Ում ենք պարտք և որքան է ժամկետանց')}</h2>
   <div class="split2" style="grid-template-columns:560px 1fr">
     <div class="x-card" style="display:flex;align-items:center;gap:24px" ${X_(2,'left')}>${donutSVG(g.map(x=>({n:x[1],v:v(SK,x[0],6)})), g.map(x=>x[2]), fmt(v(SK,52,6)), 'ձևավորված · 2025')}
       <div class="lgd">${g.map(x=>`<span><i style="background:${x[2]}"></i>${x[1]} · ${fmt(v(SK,x[0],7),1)}%</span>`).join('')}</div></div>
     <div class="side" ${X_(3,'right')}>${sh.map(s=>`<div class="x-card shr"><div class="hd"><b>${s[0]}</b><span>${s[1]}</span></div>
       <div class="pctbar"><i class="a" style="width:${K(s[2],0)}%"></i><em>${fmt(K(s[2],0),1)}%</em></div><div class="pctbar"><i class="b ${s[3]==='down'?'g':''}" style="width:${K(s[2],1)}%"></i><em>${fmt(K(s[2],1),1)}%</em></div></div>`).join('')}</div></div>
   <p class="x-lead" style="font-size:24px" ${X_(5)}>Ժամկետանց պարտքերի կշիռն իջել է <b class="x-in">21.8% → 17.6%</b>, իսկ ընթացիկ պարտավորություններում ԿՊ-ի բաժինը՝ <b class="x-in">43.5% → 36.4%</b>։</p></div>`}},
 {t:'ԿՊ շրջանառելիություն', bg:IMG.hourglass, shade:'shade-left', tr:'zoom', html:()=>`
   <div class="x-pad"><div class="x-kick" ${X_(0)}>Շրջանառելիություն</div><h2 class="x-h2">${split('Մենք մեր պարտքերն ավելի արագ ենք մարում')}</h2>
   <div class="trio">
     <div class="x-card st" ${X_(2,'pop')}><div class="k">ՇՐՋ<sub>կպ</sub> = Հ ÷ ԿՊ<sub>միջին</sub></div><div class="dual"><div><small>2024</small><b>${fmt(K(35,0),1)}</b></div><span>→</span><div><small>2025</small><b class="x-sky">${fmt(K(35,1),1)}</b></div></div><p class="x-p">Տարվա մեջ քանի անգամ ենք ամբողջությամբ «փակում» մեր պարտքերը։</p></div>
     <div class="x-card st clk" ${X_(3,'pop')}><div class="k">T<sub>օր</sub> = ԿՊ<sub>միջին</sub> ÷ Հ × 360</div><div class="clocks"><div>${clockSVG(K(36,0),'rgba(255,255,255,.6)','k0')}<small>2024</small></div><div>${clockSVG(K(36,1),G.sky,'k1')}<small>2025</small></div></div><p class="x-p">Քանի՞ օր ենք օգտվում ուրիշի փողից՝ մինչև վճարելը։</p></div>
     <div class="x-card st" ${X_(4,'pop')}><div class="k">±ΔԴՄ = (T¹ − T⁰) × Հ¹ ÷ 360</div><div class="big x-out">${fmt(v(SK,40,6))}</div><p class="x-p">դրամ դուրս եկավ շրջանառությունից, որովհետև կրեդիտորներին սկսեցինք վճարել 5.4 օր ավելի շուտ։</p></div>
   </div></div>`},
 {t:'Օրերի մրցավազք', video:VID.city, shade:'shade-full', tr:'iris', html:()=>{ const mx = 30;
   const row=(y)=>`<div class="race" ${X_(3+y,'left')}><div class="yr">${y?2025:2024}</div><div>
      <div class="lane"><span class="nm x-in">Գնորդները մեզ վճարում են</span><div class="tr"><i class="lg" style="width:${(D(34,y)/mx*100).toFixed(1)}%"></i></div><b>${fmt(D(34,y),1)} օր</b></div>
      <div class="lane"><span class="nm x-vio">Մենք վճարում ենք մատակարարներին</span><div class="tr"><i class="lv" style="width:${(K(36,y)/mx*100).toFixed(1)}%"></i></div><b>${fmt(K(36,y),1)} օր</b></div></div></div>`;
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Համեմատություն</div><h2 class="x-h2">${split('Ո՞վ է ավելի երկար սպասում')}</h2>
   <div class="x-card" style="margin-top:30px;padding:34px 40px" ${X_(2)}>${row(0)}${row(1)}</div>
   <div class="duo2"><div class="x-card" ${X_(5,'pop')}><h4 class="x-in">2024 · լավ էր</h4><p class="x-p">Գնորդներից փողը ստանում էինք 11 օրում, իսկ մատակարարներին վճարում 27 օրում։ Մոտ 16 օր օգտվում էինք «ուրիշի փողից»։</p></div>
     <div class="x-card" ${X_(6,'pop')}><h4 class="x-out">2025 · պատկերը շրջվեց</h4><p class="x-p">Հիմա գնորդները վճարում են 22.6 օրում, իսկ մենք՝ 21.5 օրում։ Մենք ենք «վարկավորում» գնորդներին մեր հաշվին։</p></div></div></div>`}},
 {t:'Գդկհ և գործոններ', bg:IMG.team, shade:'shade-solid', tr:'wipe', html:()=>{ const f=[['ՏԿ<sub>կպ</sub>',v(SK,42,6)],['ԳԸԻ',v(SK,43,6)],['ՏԿ<sub>դպ</sub>',v(SK,44,6)]]; const mx=1.8;
   const pos = x => Math.max(0, Math.min(100, x/1.5*100));
   return `<div class="x-pad"><div class="x-kick" ${X_(0)}>Դեբիտորական ÷ կրեդիտորական</div><h2 class="x-h2">${split('Գդկհ-ն դուրս եկավ օպտիմալ գոտուց')}</h2>
   <div class="split2" style="grid-template-columns:1fr 1fr">
     <div class="x-card" ${X_(2,'left')}><h4>Գդկհ = ԴՊ ÷ ԿՊ <small class="x-p" style="font-size:18px">(նորման՝ 0.9–1.0)</small></h4>
       <div class="zone"><div class="sc"><i class="ok" style="left:${pos(.9)}%;width:${pos(1)-pos(.9)}%"></i><span class="mk a" style="left:${pos(K(41,0))}%"><b>${fmt(K(41,0),3)}</b><small>2024</small></span><span class="mk b" style="left:${pos(K(41,1))}%"><b>${fmt(K(41,1),3)}</b><small>2025</small></span></div>
       <div class="ax"><span>0</span><span>0.5</span><span>1.0</span><span>1.5</span></div></div>
       <p class="x-p">1-ից մեծ՝ մեզ ավելի շատ են պարտք, քան մենք։ 0.9-ից փոքր՝ ավելի շատ ենք պարտք, քան մեզ են պարտք → վճարունակության ռիսկ։</p></div>
     <div class="x-card" ${X_(3,'right')}><h4>Ինչո՞ւ փոխվեց․ շղթայական տեղադրում</h4>
       <div class="fbars">${f.map((x,i)=>`<div class="fb" style="--i:${i}"><span class="n">${x[0]}</span><div class="t"><u></u><i class="${x[1]>=0?'p':'m'}" style="${x[1]>=0?'left:50%':'right:50%'};width:${(Math.abs(x[1])/mx*50).toFixed(1)}%"></i></div><b class="${x[1]>=0?'x-in':'x-out'}">${sgn(x[1],3)}</b></div>`).join('')}</div>
       <div class="fsum">Ընդամենը՝ <b class="x-out">${sgn(v(SK,70,5),3)}</b> = ${fmt(K(41,1),3)} − ${fmt(K(41,0),3)}</div>
       <p class="x-p" style="font-size:19px">Ամենաուժեղ «հարվածը» տվեց ԴՊ-ի կշռի կտրուկ նվազումը ընթացիկ ակտիվներում (0.050 → 0.016), որովհետև ակտիվներն աճեցին 2.5 անգամ։</p></div></div></div>`}},
 {t:'Աղյուսակներ', bg:IMG.desk, shade:'shade-left', tr:'blinds', html:()=>`
   <div class="x-pad" style="justify-content:center"><div class="split2" style="grid-template-columns:1fr 820px;align-items:center">
   <div><div class="x-kick" ${X_(0)}>Տվյալների սրահ</div><h2 class="x-h2">${split('Բոլոր աղյուսակները՝ կենդանի')}</h2>
     <div class="feat" ${X_(2)}>
       <div><i>9</i><span>բաժին՝ ելակետային տվյալներ, գործակիցներ, կառուցվածք, շարժ, գործոնային վերլուծություն</span></div>
       <div><i>fx</i><span>սեղմեք ցանկացած թվի վրա՝ կտեսնեք Excel-ի բանաձևը, իսկ մասնակից թվերը կլուսավորվեն</span></div>
       <div><i>376</i><span>բանաձև, 0 սխալ․ նույն հաշվարկները կան Excel ֆայլում՝ 9 գծապատկերով</span></div></div>
     <div class="cta" ${X_(4)}><button class="x-btn xl" data-open="excel">${ICO.grid}Բացել աղյուսակները</button></div></div>
   <div ${X_(3,'right')}>${previewTable()}</div></div></div>`},
 {t:'Եզրակացություն', bg:IMG.team, shade:'shade-solid', tr:'zoom', html:()=>`
   <div class="x-pad"><div class="x-kick" ${X_(0)}>Եզրակացություն և առաջարկներ</div><h2 class="x-h2">${split('Վաճառում ենք շատ, բայց փողը ուշ է գալիս')}</h2>
   <div class="recs-x">
     ${[['Սահմանել վճարման հստակ ժամկետներ և տույժեր․ ԴՊ-ի պտույտը 11-ից հասել է 22.6 օրի։',G.out],
        ['Վաղ վճարման զեղչ (օրինակ՝ 2% 10 օրում), որպեսզի գնորդները շուտ վճարեն։',G.in],
        ['Ռիսկային պարտքերի համար ձևավորել պահուստ և առանձին հսկել ԴՊ-2-ին ու ԴՊ-6-ին։',G.gold],
        ['Մատակարարների հետ բանակցել ավելի երկար ժամկետների շուրջ՝ առանց ժամկետանցի։',G.vio]].map((r,i)=>`
     <div class="x-card" ${X_(2+i,'pop')}><span class="n" style="color:${r[1]};text-shadow:0 0 30px ${r[1]}88">${i+1}</span><p>${r[0]}</p></div>`).join('')}</div></div>`},
 {t:'Շնորհակալություն', bg:IMG.yerevan, shade:'shade-bottom', tr:'iris', html:()=>`
   ${ornament()}
   <div class="x-pad" style="justify-content:flex-end;padding-bottom:170px">
     <h1 class="x-h1" style="font-size:120px">${split('Շնորհակալություն',300)}</h1>
     <p class="x-lead" ${X_(2)}>Հրաչյա Ասլանյան · ՀԱՊՀ, ԻՏ447 · Դասախոս՝ Օ.Ա. Գալստյան</p>
     <div class="cta" ${X_(3)}><a class="x-btn" href="../index.html">${ICO.home}Վերադառնալ հարթակ</a><button class="x-btn xl" data-open="excel">${ICO.grid}Աղյուսակներ</button><a class="x-btn ghost" href="../lesson-8.html#lecture">Դասախոսությունը՝ պարզ</a></div>
   </div>`}
];
function previewTable(){
  const rows=[['ՇՐՋդպ, պտույտ',D(33,0),D(33,1),2,'down'],['Tօր (ԴՊ), օր',D(34,0),D(34,1),1,'up'],['Գռդպ',D(37,0),D(37,1),3,'up'],['ՇՐՋկպ, պտույտ',K(35,0),K(35,1),2,''],['Tօր (ԿՊ), օր',K(36,0),K(36,1),1,''],['ՏԿժ.անց, %',K(39,0),K(39,1),1,'down2'],['Գդկհ',K(41,0),K(41,1),3,'down']];
  return `<div class="drp"><div class="drp-h"><span class="dot"></span><b>Տվյալների սրահ</b><span>Թեմա 8–9 · 2024 → 2025</span><em>fx</em></div>
    <div class="drp-tabs">${['ԴՊ','ԴՊ գործակիցներ','ԿՊ','ԿՊ գործակիցներ','Գործոններ'].map((t,i)=>`<span class="${i?'':'on'}">${t}</span>`).join('')}</div>
    ${rows.map((r,i)=>{ const d=r[2]-r[1]; const bad = r[4]==='down'? d<0 : (r[4]==='up'? d>0 : false); const good = r[4]==='down2' ? d<0 : (!bad && r[4]!=='');
      return `<div class="drp-r" style="--i:${i};--c:${bad?'#ff5c7a':(good?'#3dff8f':'#5cd6ff')};grid-template-columns:1.4fr .8fr .8fr .9fr"><span class="l">${r[0]}</span><span class="v" style="opacity:.6">${fmt(r[1],r[3])}</span><span class="v">${fmt(r[2],r[3])}</span><span class="chg ${bad?'dn':(good?'up':'eq')}">${d>0?'▲':'▼'} ${sgn(d,r[3])}</span></div>`; }).join('')}
    <div class="drp-fx"><span>E34</span><code>=E32/E33</code><span class="r">= ${fmt(D(34,1),1)}</span></div></div>`;
}
