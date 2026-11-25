/* ======================================================================
   ՎԵՐՋԻՆ ՄՂՈՆ · ԵՐԵՎԱՆ — v3 (novice-friendly, professional 2D)
   Coursework: «Վերջին մղոնի (Last Mile) լոգիստիկայի արդյունավետության
   բարձրացման մարքեթինգային գործիքները», ՀԱՊՀ, 2026
   ====================================================================== */
'use strict';
const $=s=>document.querySelector(s);
const cv=$('#cv');
const rnd=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),pick=a=>a[(Math.random()*a.length)|0];
const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
function fmt(v,dec=0){const s=Math.abs(v).toFixed(dec).split('.');s[0]=s[0].replace(/\B(?=(\d{3})+(?!\d))/g,' ');return (v<0?'−':'')+s.join(',');}
const FONT='"Noto Sans Armenian","Segoe UI",system-ui,sans-serif';
const meters=px=>Math.round(px/TS*10/10)*10; // 1 tile ≈ 10 m

/* ====================== ECONOMIC MODEL (coursework) ====================== */
const P={Q:80000,ac:.35,as:.50,al:.15,c0:1000,f0:.15,cs:480,N0:40,q:300,e:35000,r:70,K:3e6,L:60,beta:.85};
function courseModel(s,f1,d=100){const cc=f=>P.c0/(1-f),A=P.K/P.L;const C0=P.Q*P.ac*cc(P.f0)+P.Q*P.as*P.cs+P.N0*(P.e+A)+P.Q*P.al*P.r;
  const Qc1=P.Q*P.ac*(1-s),Ll=P.Q*P.al+P.Q*P.ac*s,N1=Math.max(P.N0,Math.ceil(Ll/P.q-1e-9)),D=d*P.beta*Ll;const C1=Qc1*cc(f1)+P.Q*P.as*P.cs+N1*(P.e+A)+Ll*P.r+D;
  const dCF=(C0-P.N0*A)-(C1-N1*A),dN=N1-P.N0;return {C0,C1,N1,cpd0:C0/P.Q,cpd1:C1/P.Q,dCF,PP:dN*P.K/dCF,ROI:12*dCF/(dN*P.K)*100};}
(function(){const r=courseModel(.28,.11);const ok=Math.round(r.C0)===56381176&&Math.round(r.C1)===50621885&&r.N1===67&&r.PP.toFixed(1)==='11.4'&&Math.round(r.ROI)===105;console[ok?'log':'error']('[model self-test vs coursework]',ok?'PASS':'FAIL');})();
const sDemand=d=>d<=0?0:Math.min(.40,.06+.22*Math.min(d,300)/100); // game assumption: 100 ֏ → 28 % (coursework)
const COST={slot:9e6},BUDGET=100e6;
const builtN=()=>W.slots.filter(s=>s.built&&!s.pre).length;
function company(){const Q=P.Q,A=P.K/P.L,built=builtN(),N=P.N0+3*built,s=sDemand(G.co.d);
  const Ldem=Q*P.al+Q*P.ac*s,Ll=Math.min(Ldem,N*P.q),Qc1=Q*(P.ac+P.al)-Ll,f=G.co.sms?.11:.15,D=G.co.d*P.beta*Ll;
  const C0=Q*P.ac*P.c0/(1-P.f0)+Q*P.as*P.cs+P.N0*(P.e+A)+Q*P.al*P.r;const C1=Qc1*P.c0/(1-f)+Q*P.as*P.cs+N*(P.e+A)+Ll*P.r+D;
  const dCF=(C0-P.N0*A)-(C1-N*A),inv=built*COST.slot;return {N,s,f,Ll,over:Math.max(0,Ldem-Ll)/Ldem,C0,C1,cpd0:C0/Q,cpd:C1/Q,save:C0-C1,dCF,inv,PP:inv>0&&dCF>0?inv/dCF:null};}
const TARGET=635;

/* ====================== SOUND ====================== */
const SND={on:false,ac:null,mus:null};
function ac(){if(!SND.ac){try{SND.ac=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}}return SND.ac;}
function tone(f,d=.12,type='triangle',v=.07,delay=0){if(!SND.on)return;const a=ac();if(!a)return;const t=a.currentTime+delay;const o=a.createOscillator(),g=a.createGain();o.type=type;o.frequency.setValueAtTime(f,t);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+d+.05);}
const sfx={tap:()=>tone(700,.06,'sine',.05),ok:()=>{tone(660,.1);tone(990,.14,'triangle',.07,.08);},bad:()=>tone(180,.2,'sawtooth',.05),
  coin:()=>{tone(1320,.07,'square',.035);tone(1760,.1,'square',.035,.06);},lvl:()=>[523,659,784,1046,1318].forEach((f,i)=>tone(f,.22,'triangle',.07,i*.1)),
  horn:()=>{tone(392,.18,'square',.04);tone(392,.18,'square',.04,.22);},pop:()=>tone(900,.05,'square',.03),door:()=>{tone(300,.06,'square',.04);tone(260,.08,'square',.04,.09);}};
function music(on){const a=ac();if(!a)return;clearInterval(SND.mus);SND.mus=null;if(!on)return;
  const F=n=>440*2**((n-69)/12);const mel=[69,71,72,74,76,77,76,74,72,71,69,68,69,71,72,69];const bass=[45,45,52,52,50,50,45,45];let k=0;
  SND.mus=setInterval(()=>{const i=k++%16;tone(F(mel[i]),.22,'triangle',.022);if(i%2===0)tone(F(bass[(i/2)%8]),.35,'sine',.04);},240);}

/* ====================== STATE ====================== */
const CAPS=['#ff7a1a','#3d8bff','#22b866','#b04dff','#e8434f'];
let G=null;
function newGame(nick,cap){return {v:3,nick:nick||'Առաքիչ',cap,lvl:1,xp:0,money:1500,boost:0,
  p:{x:W.places.hub.x+30,y:W.places.hub.y+70,dir:3,t:0,moving:false,inVan:false,dance:0},
  van:{x:W.places.van.x,y:W.places.van.y,a:0},inv:[],sel:null,st:{del:0,att:0,fail:0,cost:0,lock:0,pudo:0},
  co:{d:0,sms:false,unlocked:false},q:0,qd:{},side:{},bf:null,flags:{}};}
const SAVEK='lmo3_save';
function save(){try{if(!G)return;const s={...G,slots:W.slots.map(s=>s.built),inv:G.inv.map(p=>({...p,b:p.b?W.buildings.indexOf(p.b):null}))};delete s.pm;localStorage.setItem(SAVEK,JSON.stringify(s));}catch(e){}}
function load(){try{const s=JSON.parse(localStorage.getItem(SAVEK));if(!s||s.v!==3)return null;s.slots.forEach((b,i)=>{if(W.slots[i])W.slots[i].built=b;});s.inv=s.inv.map(p=>({...p,b:p.b!=null?W.buildings[p.b]:null}));delete s.slots;return s;}catch(e){return null;}}

/* ====================== ENTITIES ====================== */
const NPC=[];let bots=[],cars=[],walkers=[],floats=[],parts=[],bubbles=[];
const npc=id=>NPC.find(n=>n.id===id);
function mkNPC(id,name,role,place,look,lines,extra={}){const p=W.places[place];NPC.push({id,name,role,x:p.x+(extra.dx||0),y:p.y+(extra.dy||0),hx:p.x+(extra.dx||0),hy:p.y+(extra.dy||0),look,lines,dir:0,t:Math.random()*9,moving:false,talk:0,...extra});}
function setupNPCs(){NPC.length=0;
  mkNPC('ashot','Աշոտ ձյաձյա','պահեստի ղեկավար','hub',{skin:'#e9b48f',shirt:'#d9d4c8',jacket:'#4a4e57',pants:'#3a3a44',hat:'flat',must:true,belly:true,hair:'#9a9a9a'},TXT.ashotIdle,{dx:-110,dy:20});
  mkNPC('tatik','Սիրանույշ տատիկ','հաճախորդ','market',{skin:'#efc19d',shirt:'#7a5ab8',pants:'#4a3a6a',hat:'scarf',capC:'#d94f70'},TXT.tatikIdle,{dx:-30});
  mkNPC('aram','Արամ','ծրագրավորող','cascade',{skin:'#f1c6a0',shirt:'#3d4f8a',pants:'#2a2a3a',hat:'hood',glasses:true},TXT.aramIdle,{dy:10});
  mkNPC('hayko','Հայկո','քյաբաբանոց','kyabab',{skin:'#e3a87e',shirt:'#fff',pants:'#3a3a44',hat:'chef',must:true,apron:true,belly:true},TXT.haykoIdle);
  mkNPC('samo','Սամո','խորովածի վարպետ','samo',{skin:'#e3a87e',shirt:'#d6453d',pants:'#2a2a3a',hair:'#2a1d1a',must:true,beard:'#2a1d1a'},TXT.samoIdle);
  mkNPC('zhora','Ժորա','նարդու չեմպիոն','zhora',{skin:'#e7b08a',shirt:'#6b8f3a',jacket:'#5a4a3a',pants:'#3a3a44',hat:'flat',must:true,hair:'#bbb'},TXT.zhoraIdle);
  mkNPC('gagik','Գագիկ','բիզնեսմեն','square',{skin:'#e3a87e',shirt:'#f4f4f4',jacket:'#1e1e28',pants:'#1e1e28',hair:'#111',glasses:true,belly:true},TXT.gagikIdle,{dx:90});
  mkNPC('ani','Անի','Shein-ի թագուհի','mall',{skin:'#f6cfae',shirt:'#ff6fa8',pants:'#5a4a8a',hair:'#5a2d1a',long:true},TXT.aniIdle,{dx:-40});
  mkNPC('prof','Պրոֆ. Մկրտչյան','ՀԱՊՀ','uni',{skin:'#efc19d',shirt:'#e8e8e8',jacket:'#3a4a6a',pants:'#2a2a3a',hair:'#bbb',glasses:true,beard:'#ccc'},['Վերջին մղոնը լուրջ գիտություն ա, երիտասարդ','Թվերը չեն ստում։ Ստում ա նա, ով ասում ա «հինգ րոպեից իջնում եմ»'],{dy:8});
  NPC.push({id:'dog',name:'Բոբիկ',role:'բակի շունը',x:W.places.square.x-150,y:W.places.square.y+40,hx:W.places.square.x-150,hy:W.places.square.y+40,dog:true,lines:TXT.dogIdle,t:0,dir:0});}
function setupWorldLife(){
  const N=W.nodes;const near=n=>N.filter(m=>m!==n&&(m.x===n.x||m.y===n.y)&&Math.abs(m.x-n.x)+Math.abs(m.y-n.y)<14*TS);
  W.nodes.forEach(n=>n.nb=near(n));
  const skins=['#f3c49b','#e3a87e','#f6cfae','#d99a72','#c98a5e'];
  bots=TXT.bots.map(([nm,lv,c])=>{const n=pick(N);return {nm,lv,c,x:n.x,y:n.y,from:n,to:pick(n.nb),off:pick([40,-40]),t:Math.random()*9,sp:rnd(50,72),look:{skin:pick(skins),shirt:c,pants:pick(['#3b4a6b','#2a2a3a','#5a4a8a']),hat:pick(['cap','none','hood']),capC:c,hair:pick(['#2a1d1a','#5a2d1a','#111']),bag:true,vest:Math.random()<.4}};});
  const kinds=[['car','#d94b4b'],['car','#3f7fd1'],['taxi','#f2c230'],['taxi','#f2c230'],['car','#8a5cd6'],['car','#e9e9ee'],['marsh','#f5d547'],['car','#4fa860'],['car','#2b2b33'],['taxi','#f2c230'],['car','#e8833a'],['car','#8a8f99']];
  cars=kinds.map(([k,c])=>{const n=pick(N);return {kind:k,color:c,x:n.x,y:n.y,from:n,to:pick(n.nb),sp:k==='marsh'?70:rnd(95,135),stop:0};});
  walkers=Array.from({length:26},()=>{const n=pick(N);return {x:n.x,y:n.y,from:n,to:pick(n.nb),off:pick([42,-42]),t:Math.random()*9,sp:rnd(32,50),look:{skin:pick(skins),shirt:pick(['#e2574c','#4fa3e0','#f2c94c','#9b7be0','#5fbf6a','#f08bc0','#f4f4f4','#7d8596']),pants:pick(['#3b4a6b','#2a2a3a','#5a4a8a','#7a5a3a']),hat:pick(['none','none','cap','scarf','flat']),capC:pick(['#d94f70','#4fa3e0','#f2c94c']),hair:pick(['#2a1d1a','#5a2d1a','#111','#bbb']),must:Math.random()<.3,long:Math.random()<.3}};});}
function moveOnGraph(e,dt,laneOff){const dx=e.to.x-e.from.x,dy=e.to.y-e.from.y,len=Math.hypot(dx,dy)||1;e.k=(e.k||0)+e.sp*dt/len;
  if(e.k>=1){e.k=0;const prev=e.from;e.from=e.to;const opts=e.from.nb.filter(n=>n!==prev);e.to=pick(opts.length?opts:e.from.nb);return moveOnGraph(e,0,laneOff);}
  const nx=-dy/len,ny=dx/len;e.x=e.from.x+dx*e.k+nx*laneOff;e.y=e.from.y+dy*e.k+ny*laneOff;e.ang=Math.atan2(dy,dx);e.dir=Math.abs(dx)>Math.abs(dy)?(dx<0?1:2):(dy<0?3:0);}

/* ====================== INPUT ====================== */
const keys={};let joy={on:false,x:0,y:0,id:null,ox:0,oy:0};
const modalOn=()=>$('#mod').classList.contains('on');
addEventListener('keydown',e=>{if(e.target.tagName==='INPUT'){if(e.key==='Enter')$('#bStart').click();return;}const k=e.key.toLowerCase();keys[k]=true;
  if(!running)return;
  if(['e',' ','enter'].includes(k)){e.preventDefault();if(DLG.on)DLG.next();else if(!modalOn())doAct();}
  if(k==='escape')closeMod();if(DLG.on||modalOn())return;
  if(k==='t')openTerminal();if(k==='c')cycleCam();if(k==='r')radio();if(k==='k')dance();if(k==='m')openMap();if(k==='v')toggleVan();
  if(/^[1-9]$/.test(k)){const p=G.inv[+k-1];if(p){G.sel=p.id;renderTray();sfx.tap();}}});
addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;});
addEventListener('blur',()=>{for(const k in keys)keys[k]=false;});
const knob=$('#knob');const look={on:false,id:null,dx:0,dy:0,lx:0,ly:0};
cv.addEventListener('wheel',e=>{if(!running)return;e.preventDefault();R3.cam.zoom=clamp(R3.cam.zoom*(e.deltaY>0?1.1:.9),.55,1.9);},{passive:false});
cv.addEventListener('pointerdown',e=>{if(!running)return;if(R3.cam.mode!=='top'&&(e.pointerType==='mouse'||e.clientX>innerWidth*.5)){look.on=true;look.id=e.pointerId;look.lx=e.clientX;look.ly=e.clientY;try{cv.setPointerCapture(e.pointerId);}catch(_){}return;}joy={on:true,id:e.pointerId,ox:e.clientX,oy:e.clientY,x:0,y:0};knob.style.display='block';knob.style.left=e.clientX+'px';knob.style.top=e.clientY+'px';try{cv.setPointerCapture(e.pointerId);}catch(_){}if(SND.on&&ac())ac().resume();});
cv.addEventListener('pointermove',e=>{if(look.on&&e.pointerId===look.id){look.dx+=e.clientX-look.lx;look.dy+=e.clientY-look.ly;look.lx=e.clientX;look.ly=e.clientY;return;}if(!joy.on||e.pointerId!==joy.id)return;let dx=e.clientX-joy.ox,dy=e.clientY-joy.oy;const l=Math.hypot(dx,dy),m=48;if(l>m){dx*=m/l;dy*=m/l;}joy.x=dx/m;joy.y=dy/m;knob.firstElementChild.style.transform=`translate(${dx}px,${dy}px)`;});
const jend=e=>{if(e.pointerId===look.id)look.on=false;if(e.pointerId!==joy.id)return;joy.on=false;joy.x=joy.y=0;knob.style.display='none';knob.firstElementChild.style.transform='';};
cv.addEventListener('pointerup',jend);cv.addEventListener('pointercancel',jend);
$('#act').onclick=()=>{if(DLG.on)DLG.next();else doAct();};
$('#tVan').onclick=()=>toggleVan();$('#tCam').onclick=()=>cycleCam();$('#tRadio').onclick=()=>radio();$('#tTerm').onclick=()=>openTerminal();$('#tDance').onclick=()=>dance();$('#tMap').onclick=$('#mmw').onclick=()=>openMap();$('#tHelp').onclick=()=>help();
$('#tSnd').onclick=()=>{SND.on=!SND.on;$('#tSnd').firstChild.textContent=SND.on?'🔊':'🔇';if(SND.on){ac()&&ac().resume();music(true);sfx.ok();}else music(false);};
$('#qcard').onclick=()=>{$('#qcard').classList.toggle('open');$('#qtog').textContent=$('#qcard').classList.contains('open')?'▴':'▾';};

/* ====================== UI: toast queue, chat, dialog, modal ====================== */
const TQ=[];let tBusy=false;
function toast(t,kind){if(TQ.length&&TQ[TQ.length-1].t===t)return;TQ.push({t,kind});if(TQ.length>4)TQ.splice(0,TQ.length-4);if(!tBusy)nextToast();}
function nextToast(){const x=TQ.shift();const el=$('#toast');if(!x){tBusy=false;el.classList.remove('on');return;}tBusy=true;el.className='glass on '+(x.kind||'');el.innerHTML=x.t;
  setTimeout(()=>{el.classList.remove('on');setTimeout(nextToast,330);},Math.min(5200,1900+x.t.length*28));}
function chat(nm,t,sys){const d=document.createElement('div');if(sys)d.className='sys';d.innerHTML=`<b>${nm}:</b> ${t}`;const c=$('#chat');c.appendChild(d);while(c.children.length>4)c.firstChild.remove();setTimeout(()=>{d.style.transition='opacity 1s';d.style.opacity=0;setTimeout(()=>d.remove(),1000);},14000);}
function floatTxt(x,y,t,c='#fff'){floats.push({x,y,t,c,life:1.6});}
function bubble(ent,t,dur=3.4){bubbles=bubbles.filter(b=>b.e!==ent);bubbles.push({e:ent,t,life:dur});}
const DLG={on:false,q:[],cb:null,full:'',typed:0,
  open(lines,cb){this.q=lines.slice();this.cb=cb;this.on=true;$('#dlg').classList.add('on');$('#hud').style.setProperty('--dlg','1');this.show();},
  show(){const L=this.q.shift();if(!L){this.close();return;}this.cur=L;$('#dWho').textContent=L.who||'';this.full=L.t;this.typed=0;$('#dTx').innerHTML='';
    drawPortrait(L.p);const o=$('#dOpts');o.innerHTML='';
    if(L.opts){L.opts.forEach(op=>{const b=document.createElement('button');b.className='bt '+(op.c||'');b.innerHTML=op.t;b.onclick=e=>{e.stopPropagation();sfx.tap();if(op.end)this.close(op.go);else{op.go&&op.go();this.show();}};o.appendChild(b);});}
    else{const b=document.createElement('button');b.className='bt g';b.innerHTML=this.q.length?'Հետո ▶':'Լավ ✓';b.onclick=e=>{e.stopPropagation();this.next();};o.appendChild(b);}},
  next(){if(this.typed<this.full.length){this.typed=this.full.length;$('#dTx').innerHTML=this.full;return;}if(this.cur&&this.cur.opts)return;sfx.tap();this.show();},
  close(go){this.on=false;$('#dlg').classList.remove('on');const cb=this.cb;this.cb=null;go&&go();cb&&cb();}};
$('#dlg').addEventListener('click',()=>DLG.next());
function drawPortrait(id){if(id==='police'&&window.R3&&R3.ready){R3.portrait($('#dlgP'),R3.POLICE);return;}if(window.R3&&R3.ready&&id!=='sys'){const n=npc(id);if(id==='me'||n){R3.portrait($('#dlgP'),id==='me'?meLook():n.dog?'dog':n.look);return;}}const c=$('#dlgP'),g=c.getContext('2d');g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,192,192);
  const n=npc(id);g.save();g.translate(96,176);g.scale(3.9,3.9);
  if(id==='me')drawPerson(g,0,0,meLook());else if(n&&n.dog)drawDog(g,0,0,0,false);else if(n)drawPerson(g,0,0,n.look);
  else{g.restore();g.font='86px '+FONT;g.textAlign='center';g.fillText(id==='sys'?'📦':'💬',96,126);return;}g.restore();}
const MOD={cb:null};
function modal(html,onClose){$('#modBox').innerHTML=html;$('#mod').classList.add('on');$('#modBox').scrollTop=0;MOD.cb=onClose;}
$('#mod').addEventListener('click',e=>{if(e.target.id==='mod'&&!MOD.lock)closeMod();});
function closeMod(){if(!modalOn())return;$('#mod').classList.remove('on');MOD.lock=false;const c=MOD.cb;MOD.cb=null;c&&c();}
function lesson(k,cb){const L=TXT.lessons[k];sfx.ok();G.flags['L_'+k]=1;
  modal(`<div style="text-align:center"><span class="tag">Ի՞ՆՉ ՍՈՎՈՐԵՑԻՆՔ</span></div><div class="big-e">${L.e}</div><h2 style="text-align:center">${L.t}</h2>
  <p class="lesson-s">${L.s}</p><details><summary>📊 Թվերով (կուրսային աշխատանքից)</summary><p>${L.n}</p></details>
  <div class="row" style="margin-top:16px"><button class="bt g" style="flex:1" id="lOk">Հասկանալի է 👍</button></div>`,cb);MOD.lock=true;$('#lOk').onclick=closeMod;}
function intro(cb){let i=0;const L=TXT.intro;MOD.lock=true;
  const r=()=>{const c=L[i];modal(`<div class="big-e">${c.e}</div><h2 style="text-align:center">${c.t}</h2><p class="lesson-s" style="font-size:15.5px!important">${c.x}</p>
    <div class="dots">${L.map((_,k)=>`<i class="${k===i?'on':''}"></i>`).join('')}</div>
    <div class="row" style="margin-top:12px">${i>0?'<button class="bt" id="iB">◀</button>':''}<button class="bt g" style="flex:1" id="iN">${i<L.length-1?'Հետո ▶':'Սկսե՛նք 🚀'}</button></div>`,i===L.length-1?cb:null);MOD.lock=true;
    $('#iN').onclick=()=>{sfx.tap();if(i<L.length-1){i++;r();}else closeMod();};const b=$('#iB');if(b)b.onclick=()=>{i--;r();};};r();}

/* ====================== PROGRESSION ====================== */
const xpNeed=l=>60+l*45;
function addXP(n){G.xp+=n;while(G.xp>=xpNeed(G.lvl)){G.xp-=xpNeed(G.lvl);G.lvl++;sfx.lvl();toast(`⭐ Նոր մակարդակ՝ ${G.lvl}`,'good');burst(G.p.x,G.p.y-30,'#ffd84d');}hud();}
function addMoney(n){G.money+=n;floatTxt(G.p.x+18,G.p.y-56,(n>0?'+':'')+fmt(n)+' ֏',n>0?'#7dffb2':'#ff8a95');if(n>0)sfx.coin();hud();}
function burst(x,y,c){if(window.R3&&R3.ready)R3.burst(x,y+30,c);}

/* ====================== PARCELS ====================== */
let PID=1;
function nearestSlot(x,y,builtOnly=true){let best=null,bd=1e9;W.slots.forEach(s=>{if(builtOnly&&!s.built)return;const d=Math.hypot(s.x-x,s.y-y);if(d<bd){bd=d;best=s;}});return best;}
function mkParcel(b,opt={}){const pr={id:PID++,item:pick(TXT.items),b,to:b?b.owner:'',zone:b?b.zone:'',att:0,dest:'home',...opt};
  if(!opt.dest&&!opt.force&&b){const s=sDemand(G.co.d),slot=nearestSlot(b.door.x,b.door.y);
    if(slot&&Math.random()<Math.max(.12,s*1.8)){pr.dest='locker';pr.slot=W.slots.indexOf(slot);pr.zone=slot.zone;}else if(Math.random()<.12){pr.dest='pudo';pr.pudo=Math.random()<.5?0:1;}}
  return pr;}
function tgOf(p){if(!p)return null;if(p.dest==='locker')return W.slots[p.slot];if(p.dest==='pudo')return W.pudos[p.pudo];if(p.dest==='npc')return npc(p.npc);return p.b&&p.b.door;}
function lbl(p){if(p.dest==='locker')return {ic:'▣',t:'Փոստամատ',s:W.slots[p.slot].zone,cl:'lk'};if(p.dest==='pudo')return {ic:'🏬',t:'Ստացման կետ',s:W.pudos[p.pudo].name.replace('Ստացման կետ ',''),cl:'pu'};
  if(p.dest==='npc')return {ic:'⚡',t:p.to,s:'Էքսպրես',cl:''};return {ic:'🏠',t:p.to,s:p.zone,cl:''};}
const cap=()=>G.p.inVan?10:5;
function selParcel(){let p=G.inv.find(x=>x.id===G.sel);if(!p&&G.inv.length){p=G.inv.slice().sort((a,b)=>dist(G.p,tgOf(a))-dist(G.p,tgOf(b)))[0];G.sel=p.id;renderTray();}return p;}
let trayKey='';
function renderTray(){if(!G)return;const t=$('#tray');const key=G.inv.map(p=>p.id+(p.dest)).join(',')+'|'+G.sel;
  if(key!==trayKey){trayKey=key;t.innerHTML=G.inv.length?G.inv.map((p,i)=>{const L=lbl(p);return `<button class="chip ${L.cl} ${p.id===G.sel?'sel':''}" data-id="${p.id}" title="${p.item}"><span class="n">${i+1}</span><span class="ic">${L.ic}</span><span><span class="t">${L.t}</span><br><span class="d" data-d="${p.id}">${L.s}</span></span></button>`;}).join(''):'';
    t.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{G.sel=+b.dataset.id;sfx.tap();renderTray();gps.t=0;const p=G.inv.find(x=>x.id===G.sel);toast(`🧭 Նպատակ՝ <b>${lbl(p).ic} ${lbl(p).t}</b> · ${p.item}`);});}
  G.inv.forEach(p=>{const el=t.querySelector(`[data-d="${p.id}"]`);if(el){const tg=tgOf(p);el.textContent=lbl(p).s+(tg?' · '+meters(dist(G.p,tg))+' մ':'');}});}
const FAILS=['Ոչ ոք դուռը չբացեց։ Հարևանն ասում է՝ «Ծաղկաձոր են գնացել»','Դուռը բացեց կատուն։ Ստորագրել չի կարող 🐈','«5 րոպեից իջնում եմ»… 40 րոպե անցավ','Հաճախորդը զոքանչի մոտ է Գյումրիում','Դռան վրա գրված է՝ «Հյուր եմ գնացել, կգամ վաղը»','Շենքի դուռը կոդով է, կոդը ոչ ոք չգիտի'];
function deliverHome(p){G.st.att++;G.st.cost+=1000;p.att++;
  const fail=p.tatik?true:(p.safe?false:Math.random()<(G.co.sms?.11:.15));
  if(fail){G.st.fail++;sfx.bad();sfx.door();bubble(G.pm,'Տանը չկա… 😕');floatTxt(p.b.door.x,p.b.door.y-36,'Իզուր ճանապարհ · −1 000 ֏','#ff8a95');
    if(p.tatik){G.qd.tatikTried=(G.qd.tatikTried||0)+1;toast('🚪 Տատիկը տանը չէ։ Հարևանը՝ «Սիրանույշը <b>Գում շուկայում</b> է, կանաչի է առնում»','bad');
      p.dest='npc';p.npc='tatik';p.to='Սիրանույշ տատիկ';renderTray();if(!G.flags.L_f)setTimeout(()=>lesson('f',()=>questEvent('tatikFail')),900);else questEvent('tatikFail');hud();return;}
    if(G.co.sms&&nearestSlot(p.b.door.x,p.b.door.y)){const sl=nearestSlot(p.b.door.x,p.b.door.y);p.dest='locker';p.slot=W.slots.indexOf(sl);p.zone=sl.zone;renderTray();setTimeout(()=>toast(`💬 SMS ${p.to}-ից՝ «Թողեք փոստամատում, կվերցնեմ» → <b>▣ ${sl.zone}</b>`,'good'),1200);}
    else toast('🚪 '+pick(FAILS)+'։ Փորձիր նորից կամ տար մյուս ծանրոցը','bad');
    if(!G.flags.L_f)setTimeout(()=>lesson('f'),900);hud();return;}
  finishParcel(p,'home');}
function finishParcel(p,how){G.inv=G.inv.filter(x=>x!==p);if(G.sel===p.id)G.sel=null;G.st.del++;if(how==='locker'){G.st.lock++;G.st.cost+=353.33;}else if(how==='pudo'){G.st.pudo++;G.st.cost+=480;}
  addMoney(p.express?3000:400);addXP(how==='home'?12:8);burst(G.p.x,G.p.y-30,'#ffd84d');
  if(how==='home'&&p.b)bubble(G.pm,pick(['Ապրես, ջան!','Վա՜յ, արդեն?','Մի բաժակ սուրճ կխմե՞ս?','Մերսի, ախպեր','Աստված պահի','Տատիկն էլ գաթա ա թխել, վերցրու']));
  questEvent('delivered',{p,how});renderTray();hud();save();}

/* ====================== ACTIONS ====================== */
let ACT=null;
const hubPt=()=>W.places.hub;
function findAct(){const p=G.p,me={x:p.x,y:p.y};let best=null,bd=1e9;const cand=(d,obj)=>{if(d<bd){bd=d;best=obj;}};
  if(p.inVan){if(((G.q===5&&!G.qd.got5)||(G.q===7&&G.bf&&G.bf.n+G.inv.length<8)||G.q===10||(G.q===1&&!G.qd.got))&&dist(me,hubPt())<130)cand(1,{t:'📦 Վերցնել ծանրոցներ',f:takeParcels});
    W.slots.forEach((s,i)=>{if(s.built&&dist(me,s)<100&&G.inv.some(x=>x.dest==='locker'&&x.slot===i))cand(2,{t:'▣ Դնել փոստամատում',f:()=>dropLocker(s)});});
    W.pudos.forEach((u,i)=>{if(dist(me,u)<100&&G.inv.some(x=>x.dest==='pudo'&&x.pudo===i))cand(3,{t:'🏬 Հանձնել կետին',f:()=>dropPudo(i)});});
    const door=G.inv.find(x=>(x.dest==='home'||x.dest==='npc')&&dist(me,tgOf(x))<150);cand(door?4:500,{t:door?'🚶 Իջնել (դուռը մոտ է)':'🚶 Իջնել Նիվայից',f:toggleVan});return best;}
  NPC.forEach(n=>{const d=dist(me,n);if(d<64){const m=questMark(n);cand(d-(m==='main'?60:m?30:0),{t:n.dog?'🐶 Շոյել':m==='main'?'❗ Խոսել':'💬 Խոսել',f:()=>talk(n)});}});
  const hubOK=(G.q===1&&!G.qd.got)||(G.q===5&&!G.qd.got5)||(G.q===7&&G.bf&&G.bf.n+G.inv.length<8)||G.q===10;
  if(hubOK&&dist(me,hubPt())<80)cand(dist(me,hubPt())-30,{t:'📦 Վերցնել ծանրոցներ',f:takeParcels});
  if(dist(me,G.van)<64)cand(dist(me,G.van)+10,{t:'🚙 Նստել Նիվա',f:toggleVan});
  G.inv.forEach(x=>{if(x.dest==='home'&&x.b){const d=dist(me,x.b.door);if(d<58)cand(d-40,{t:`🚪 Հանձնել՝ ${x.to}`,f:()=>deliverHome(x)});}});
  W.slots.forEach((s,i)=>{const d=dist(me,s);if(d<60&&s.built){if(G.inv.some(x=>x.dest==='locker'&&x.slot===i))cand(d-45,{t:'▣ Դնել փոստամատում',f:()=>dropLocker(s)});else cand(d+30,{t:'▣ Փոստամատ',f:()=>toast(`▣ Փոստամատ · ${s.zone}։ 24/7 բաց ա, մարդիկ կոդով են վերցնում։`)});}});
  W.pudos.forEach((u,i)=>{const d=dist(me,u);if(d<60&&G.inv.some(x=>x.dest==='pudo'&&x.pudo===i))cand(d-45,{t:'🏬 Հանձնել կետին',f:()=>dropPudo(i)});});
  if(G.side.lostStone&&!G.side.stoneGot&&dist(me,G.side.lostStone)<46)cand(1,{t:'⚪ Վերցնել քարը',f:()=>{G.side.stoneGot=1;sfx.ok();toast('⚪ Գտար Ժորայի նարդու քարը։ Տար նրան (Ժորայի բակ)','good');}});
  if(EV.nivaPush&&dist(me,EV.nivaPush)<80)cand(1,{t:'💪 Հրել Նիվան',f:pushNiva});
  return best;}
function doAct(){if(!ACT)return;sfx.tap();ACT.f();}
function toggleVan(){const p=G.p;if(DLG.on)return;if(p.inVan){p.inVan=false;radio(true);$('#tRadio').classList.add('hide');G.van.x=p.x;G.van.y=p.y;p.y+=28;if(isSolidPx(p.x,p.y))p.y-=56;if(isSolidPx(p.x,p.y)){p.y+=28;p.x+=30;}toast('🚶 Իջար։ Նիվան էստեղ կսպասի');sfx.door();}
  else{if(dist(p,G.van)>80){toast(`🚙 Նիվան հեռու է (${meters(dist(p,G.van))} մ)։ Այն կանգնած է պահեստի բակում`);return;}p.inVan=true;p.x=G.van.x;p.y=G.van.y;G.van.sp=0;$('#tRadio').classList.remove('hide');G.flags.vanUsed=1;toast('🚙 Աշոտ ձյաձյայի Նիվան հիմա քոնն ա։ 10 ծանրոց ա տանում, բայց միայն ասֆալտով։ 📻 R՝ ռադիո');sfx.horn();}
  gps.t=0;hud();}
function dropLocker(s){const i=W.slots.indexOf(s),list=G.inv.filter(x=>x.dest==='locker'&&x.slot===i);if(!list.length)return;
  list.forEach((p,k)=>setTimeout(()=>{finishParcel(p,'locker');},k*160));sfx.ok();toast(`▣ ${list.length} ծանրոց՝ մեկ կանգառով։ Ոչ ոքի սպասել պետք չէ 👌`,'good');
  if(!G.flags.L_locker)setTimeout(()=>lesson('locker'),list.length*160+700);}
function dropPudo(i){const list=G.inv.filter(x=>x.dest==='pudo'&&x.pudo===i);list.forEach((p,k)=>setTimeout(()=>finishParcel(p,'pudo'),k*160));sfx.ok();toast(`🏬 ${list.length} ծանրոց թողեցիր ստացման կետում։ Մարդիկ իրենք կգան կտանեն`,'good');}
function buyKyabab(){if(G.money<500){toast('💸 Գրպանդ դատարկ ա։ Ամեն ծանրոցը +400 ֏ ա, գնա աշխատի');return;}addMoney(-500);G.boost=30;sfx.ok();
  bubble(npc('hayko'),pick(['Լավաշով, սոխով, ռեհանով!','Էս քյաբաբով մինչև Էրեբունի կհասնես','Կեր, ախպեր, նիհարել ես']));toast('🍢 Քյաբաբ՝ 30 վայրկյան արագություն ⚡','good');questEvent('kyabab');hud();}
function dance(){G.p.dance=2.4;sfx.pop();bubble(G.pm,pick(['Քոչարի՜!','Հոպ-հոպ!','Շալախո!']),2);if(EV.wedding>0&&dist(G.p,W.places.square)<300&&!EV.danced){EV.danced=1;addXP(40);addMoney(1000);toast('💃 Հարսանքավորները զոռով 1 000 ֏ դրեցին գրպանդ','good');}}

/* ====================== QUESTS (step based, plain language) ====================== */
const nN=()=>builtN();
const QUESTS=[
 {t:'Ծանոթացիր Աշոտ ձյաձյայի հետ',why:'Պահեստի գլխավորն ա․ ամեն ինչ ինքը կբացատրի։',
  steps:()=>[{x:'Գնա Աշոտ ձյաձյայի մոտ՝ հետևելով դեղին կետագծին',tg:npc('ashot'),h:'Մոտենալիս ներքևում կհայտնվի «❗ Խոսել» կոճակը։ Սեղմիր այն կամ E։'}]},
 {t:'Առաջին առաքումները',why:'Սկզբում հին ձևով՝ դռնեդուռ։ Տեսնենք՝ ոնց ա գնում։',
  steps:()=>{const S=[{x:'Վերցրու 3 ծանրոց պահեստի դարպասի մոտ',d:!!G.qd.got,tg:hubPt(),h:'Կանգնիր նարնջագույն «📦» նշանի մոտ և սեղմիր «Վերցնել»։'}];
    (G.qd.list||[]).forEach(o=>S.push({x:o.tatik?'Տար ծանրոցը Սիրանույշ տատիկին 🏠':`Տար ծանրոցը ${o.to}-ին 🏠`,d:o.tatik?!!G.qd.tatikTried:!G.inv.some(p=>p.id===o.id),tg:tgOf(G.inv.find(p=>p.id===o.id)),pid:o.id,h:'Հետևիր դեղին գծին մինչև դուռը և սեղմիր «🚪 Հանձնել»։ Ներքևի ցուցակից կարող ես ընտրել, թե որ ծանրոցն ես տանում։'}));
    if(!G.qd.got)S.push({x:'Հանձնիր ծանրոցները տներին',d:false});return S;}},
 {t:'Որտե՞ղ է տատիկը',why:'Տատիկը տանը չէր։ Հարևանը բալկոնից գոռաց՝ «Գումում ա, կանաչի ա առնում»։',
  steps:()=>[{x:'Գնա Գում շուկա և գտիր Սիրանույշ տատիկին',tg:npc('tatik'),h:'Տատիկը վարդագույն գլխաշորով է, գլխի վրա՝ դեղին «!»։'},{x:'Խոսիր նրա հետ և հանձնիր ծանրոցը',d:false}]},
 {t:'Վերադարձիր Աշոտ ձյաձյայի մոտ',why:'Մի ծանրոցի համար երկու անգամ քշեցիր։ Աշոտ ձյաձյան ասում ա՝ «էսպես չի լինի»։',
  steps:()=>[{x:'Գնա պահեստ և խոսիր Աշոտ ձյաձյայի հետ',tg:npc('ashot'),h:'Դեղին գիծը կտանի պահեստ։'}]},
 {t:'Դու հիմա տնօրեն ես',why:'Փոստամատը փողոցի պահարան ա․ մի կանգառով թողնում ես շատ ծանրոց, մարդիկ վերցնում են՝ երբ հարմար ա։',
  steps:()=>[{x:'Բացիր տնօրենի հավելվածը 📊',d:!!G.flags.app,h:'Սեղմիր աջ կողմում թարթող 📊 կոճակը (կամ T)։'},
    {x:`Կառուցիր 2 փոստամատ (${Math.min(2,nN())}/2)`,d:nN()>=2,h:'Հավելվածում ընտրիր «👍 Խորհուրդ» նշված թաղամասերը և սեղմիր «Կառուցել»։'},
    {x:'Դիր 100 ֏ զեղչ՝ փոստամատից վերցնողների համար',d:G.co.d>=100,h:'Հավելվածում «Զեղչ» բաժնում ընտրիր «100 ֏»։'}]},
 {t:'Մեկ կանգառ՝ 5 ծանրոց',why:'Հլը տեսնենք՝ փոստամատով ինչքան արագ ա։',
  steps:()=>{const s=W.slots[G.qd.lk];return [{x:'Վերցրու ծանրոցները պահեստից',d:!!G.qd.got5,tg:hubPt(),h:'Գնա պահեստի դարպաս և սեղմիր «📦 Վերցնել»։'},
    {x:`Դիր 5 ծանրոց փոստամատում${s?' · '+s.zone:''} (${Math.min(5,G.qd.n5||0)}/5)`,d:(G.qd.n5||0)>=5,tg:s,h:'Բոլոր 5-ը գնում են նույն փոստամատ։ Մոտեցիր կանաչ «▣» նշանին և սեղմիր «Դնել փոստամատում»։'}];}},
 {t:'Արամը և SMS-ը',why:'Եթե նախօրոք հարցնես՝ երբ ա տանը, «տանը չկա»-ները կքչանան։ Արամը կարա միացնի, բայց սոված ա։',
  steps:()=>[{x:'Գտիր ծրագրավորող Արամին Կասկադի մոտ',d:!!G.qd.aramAsk,tg:npc('aram'),h:'Արամը կապույտ գլխարկով է, ակնոցով։'},
    {x:'Գնա Հայկոյի քյաբաբանոց և գնիր քյաբաբ (500 ֏)',d:!!G.qd.kyab,tg:npc('hayko'),h:'Խոսիր Հայկոյի հետ և ընտրիր «🍢 Քյաբաբ»։'},
    {x:'Տար քյաբաբը Արամին',d:false,tg:npc('aram')}]},
 {t:'Սև ուրբաթ 🛍️',why:'Զեղչերի օրն ա, պատվերները կրկնապատկվել են։ Նիվան ու փոստամատները քո կողքին են։',
  steps:()=>{const b=G.bf;return [{x:'Խոսիր Աշոտ ձյաձյայի հետ',d:!!b,tg:npc('ashot')},
    {x:b&&b.taken?'Վերցրու մնացած ծանրոցները պահեստից':'Վերցրու ծանրոցները պահեստից',d:!!(b&&b.n+G.inv.length>=8),tg:hubPt(),h:'Նիվան 🚙 տանում է 10 ծանրոց։ Նստիր՝ մոտենալով և սեղմելով «Նստել», հետո քշիր պահեստ։'},
    {x:`Հանձնիր 8 ծանրոց (${b?Math.min(8,b.n):0}/8)${b&&b.left>0?' · ⏱ '+Math.ceil(b.left)+' վ բոնուսի համար':''}`,d:!!(b&&b.n>=8),h:'Սկսիր մոտակա ծանրոցից։ Փոստամատներով ավելի արագ է՝ մեկ կանգառով մի քանիսը։'}];}},
 {t:'Տնօրենի քննություն',why:`Իջեցրու մեկ առաքման ծախսը ամբողջ ընկերությունում մինչև ${TARGET} ֏ (հիմա ≈ 705 ֏)։`,
  steps:()=>{const c=company();return [{x:`Կառուցիր բոլոր 9 փոստամատային կետերը (${nN()}/9)`,d:nN()>=9,h:'Բացիր 📊 և սեղմիր «Կառուցել բոլորը»։'},
    {x:'Զեղչը թող 100 ֏ (ոչ ավելի, ոչ պակաս)',d:G.co.d===100,h:'200 ֏ զեղչը ավելի շատ մարդ է բերում, քան փոստամատները տեղավորում են, ու ծախսը կրկին աճում է։'},
    {x:`Ծախսը ≤ ${TARGET} ֏ (հիմա՝ ${fmt(c.cpd,0)} ֏)`,d:c.cpd<=TARGET}];}},
 {t:'Պաշտպանություն ՀԱՊՀ-ում',why:'Պրոֆեսորը սպասում ա։ Թվերը ցույց տուր։',
  steps:()=>[{x:'Գնա ՀԱՊՀ (Պոլիտեխնիկ) և խոսիր պրոֆեսորի հետ',tg:npc('prof'),h:'Դեղին գիծը կտանի համալսարան։'}]},
 {t:'Ազատ խաղ',why:'Գլխավոր պատմությունը վերջացավ։ Շարունակիր առաքել կամ օգնիր կապույտ «?»-ով մարդկանց։',
  steps:()=>[{x:'Վերցրու ծանրոցներ պահեստից և առաքիր',d:false,tg:G.inv.length?null:hubPt()}]}];
function curStep(){const S=QUESTS[G.q].steps();let c=S.find(s=>!s.d);return {S,c};}
function questTarget(){const {c}=curStep();if(G.inv.length&&(G.q===1||G.q===5||G.q===7||G.q===10||(c&&c.pid))){const p=c&&c.pid?G.inv.find(x=>x.id===c.pid)||selParcel():selParcel();
    if(c&&c.pid&&p){if(G.sel!==p.id&&!G.flags.manualSel){}}
    const sp=selParcel();if(sp)return {pt:tgOf(sp),lab:lbl(sp)};}
  if(c&&c.tg){const t=c.tg;const n=NPC.includes(t)?t:null;return {pt:t,lab:n?{ic:'❗',t:n.name}:t===hubPt()?{ic:'📦',t:'Պահեստ'}:t.zone?{ic:'▣',t:'Փոստամատ'}:{ic:'⭐',t:''}};}
  if(G.inv.length){const sp=selParcel();return {pt:tgOf(sp),lab:lbl(sp)};}
  return null;}
let qKey='';
function updQuest(force){if(!G)return;const Q=QUESTS[G.q],{S,c}=curStep();
  const key=G.q+'|'+S.map(s=>s.x+(s.d?1:0)).join('|');if(key===qKey&&!force)return;qKey=key;
  $('#qnum').textContent=G.q<10?`Առաջադրանք ${G.q+1} / 10`:'Ազատ խաղ';$('#qt').textContent=Q.t;$('#qwhy').textContent=Q.why;
  $('#qsteps').innerHTML=S.map(s=>`<li class="${s.d?'done':s===c?'cur':''}"><i>${s.d?'✓':''}</i><span>${s.x}</span></li>`).join('');
  $('#qhint').innerHTML=c&&c.h?'<span>💡 '+c.h+'</span>':'';}
function setQ(i){G.q=i;G.qd=Object.assign({},i===1||i===5||i===7?{}:{} ,keepQD(i));qKey='';const q=$('#qcard');q.classList.remove('flash');void q.offsetWidth;q.classList.add('flash');sfx.ok();updQuest(true);save();
  if(i===4){G.co.unlocked=true;$('#tTerm').classList.remove('hide');$('#tTerm').classList.add('hot');}
  if(i>0&&i<10)toast(`🎯 Նոր առաջադրանք՝ <b>${QUESTS[i].t}</b>`,'good');hud();}
function keepQD(i){return {};}
function questEvent(ev,data){
  if(G.q===1){if(ev==='delivered'||ev==='tatikFail'){const left=(G.qd.list||[]).filter(o=>!o.tatik&&G.inv.some(p=>p.id===o.id)).length;if(left===0&&G.qd.tatikTried&&!G.qd.adv){G.qd.adv=1;setTimeout(()=>setQ(2),700);}}}
  if(G.q===5&&ev==='delivered'&&data.how==='locker'){G.qd.n5=(G.qd.n5||0)+1;if(G.qd.n5>=5&&!G.qd.adv){G.qd.adv=1;setTimeout(()=>{setQ(6);DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Տեսա՞ր, ախպերս։ Մի կանգառ, ու սաղ տեղում ա։ Ոնց կարտոֆիլի պարկը։ Մի բան էլ․ Կասկադի մոտ Արամ կա, ծրագրավորող։ Ինքը կարող ա SMS-ով հարցնել մարդկանց՝ երբ են տանը։ Գտի իրեն։'}]);},1400);}}
  if(G.q===6&&ev==='kyabab'&&G.qd.aramAsk&&!G.qd.kyab){G.qd.kyab=1;toast('🍢 Քյաբաբը Արամի համար է։ Հիմա տար Կասկադ 😅');}
  if(G.q===7&&G.bf&&ev==='delivered'){G.bf.n++;if(G.bf.n>=8&&!G.bf.fin){G.bf.fin=1;const inTime=G.bf.left>0;setTimeout(()=>{addXP(150);addMoney(inTime?10000:4000);burst(G.p.x,G.p.y,'#ffd84d');
    lesson('peak',()=>{setQ(8);DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:(inTime?'Ապրե՜ս, ժամանակին հասցրիր։ ':'Մի քիչ ուշացար, բայց հասցրիր, ապրես։ ')+'Հիմա վերջին գործը․ ամբողջ ընկերության համար մեկ առաքման ծախսը իջցրու մինչև 635 ֏։ Բաց արա 📊 հավելվածը։'}]);});},700);}}
  updQuest();hud();}
function questMark(n){const id=n.id,q=G.q;
  if((q===0&&id==='ashot')||(q===2&&id==='tatik')||(q===3&&id==='ashot')||(q===6&&id==='aram'&&(!G.qd.aramAsk||G.qd.kyab))||(q===6&&id==='hayko'&&G.qd.aramAsk&&!G.qd.kyab)||(q===7&&!G.bf&&id==='ashot')||(q===9&&id==='prof'))return 'main';
  if(q>=2&&((id==='zhora'&&(!G.side.zhora||(G.side.stoneGot&&G.side.zhora===1)))||(id==='gagik'&&!G.side.gagik)||(id==='samo'&&!G.side.samo)||(id==='ashot'&&!G.side.nivaDone&&!EV.nivaPush&&q!==3&&q!==7)))return 'side';return null;}

function takeParcels(){
  if(G.q===0){toast('Նախ խոսիր Աշոտ ձյաձյայի հետ (դեղին «!»)');return;}
  const room=cap()-G.inv.length;if(room<=0){toast('🎒 Պայուսակը լիքն է։ Նախ հանձնիր ծանրոցները');sfx.bad();return;}
  if(G.q===1&&!G.qd.got){const near=W.homes.filter(h=>h!==W.tatikHome).sort((a,b)=>dist(a.door,hubPt())-dist(b.door,hubPt()));
    const a=mkParcel(near[3],{force:true,safe:true}),b=mkParcel(near[8],{force:true,safe:true}),t={...mkParcel(W.tatikHome,{force:true}),to:'Սիրանույշ տատիկ',item:'Տատիկի նոր դոլմայի կաթսան',tatik:true};
    G.inv.push(a,b,t);G.qd.list=[a,b,t].map(p=>({id:p.id,to:p.to,tatik:!!p.tatik}));G.qd.got=1;G.sel=a.id;sfx.pop();toast('📦 Վերցրիր 3 ծանրոց։ Ներքևում տեսնում ես, թե ում են։ Դեղին գիծը տանում է ընտրվածի մոտ','good');renderTray();updQuest();return;}
  if(G.q===5&&!G.qd.got5){let s=W.slots.filter(s=>s.built&&!s.pre).sort((a,b)=>dist(a,hubPt())-dist(b,hubPt()))[0]||W.slots.find(s=>s.pre&&dist(s,hubPt())>200);G.qd.lk=W.slots.indexOf(s);
    const n=Math.min(5,room);for(let i=0;i<n;i++){const hs=W.homes.filter(h=>h.zone===s.zone);G.inv.push(mkParcel(pick(hs.length?hs:W.homes),{dest:'locker',slot:G.qd.lk,zone:s.zone}));}
    G.qd.got5=1;sfx.pop();toast(`📦 ${n} ծանրոց, բոլորը՝ <b>▣ փոստամատ ${s.zone}</b>`,'good');renderTray();updQuest();return;}
  if(G.q===7&&G.bf){const left=8-G.bf.n-G.inv.length;if(left<=0){toast('Բոլոր ծանրոցներն արդեն քեզ մոտ են');return;}const n=Math.min(room,left);
    const near=W.homes.filter(h=>dist(h.door,hubPt())<30*TS);for(let i=0;i<n;i++){const h=pick(near);const sl=nearestSlot(h.door.x,h.door.y);G.inv.push(i%2&&sl?mkParcel(h,{dest:'locker',slot:W.slots.indexOf(sl),zone:sl.zone}):mkParcel(h,{force:true}));}
    G.bf.taken=1;sfx.pop();toast(`📦 Վերցրիր ${n} ծանրոց${n<left?` (մնացածը՝ հաջորդ անգամ, կամ նստիր Նիվա)`:''}`);renderTray();updQuest();return;}
  const homes=W.homes.filter(h=>h!==W.tatikHome);for(let i=0;i<room;i++)G.inv.push(mkParcel(pick(homes)));
  sfx.pop();toast(`📦 Վերցրիր ${room} ծանրոց։ Ընտրիր ներքևի ցուցակից և հետևիր գծին`);renderTray();hud();
  bubble(npc('ashot'),pick(['Արագ, բայց զգույշ, ախպեր','Նիվայով կտանեի, բայց կարտոֆիլ ա մեջը','Տատիկներին բարևիր իմ կողմից']));}

/* ====================== NPC TALK ====================== */
function talk(n){n.talk=2.5;n.dir=G.p.y<n.y?3:0;const say=(t,cb)=>DLG.open([{who:n.name,p:n.id,t}],cb);
  if(n.dog){sfx.pop();bubble(n,'Հա՛վ! ❤️');if(!G.side.bobik){G.side.bobik=1;addXP(10);toast('🐶 Բոբիկը քեզ ընկեր ընտրեց։ Հիմա քո հետևից ա գալու','good');}return;}
  if(n.id==='ashot'){
    if(G.q===0){DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:`Հը՞, ${G.nick} ջան, եկա՞ր։ Արի, արի։ Ես Աշոտն եմ, երեսուն տարի ա ղեկին եմ։ Էս Նիվայով ինչ ասես տարել եմ՝ կարտոֆիլ, ծանրոց, մի անգամ էլ՝ այծ 🐐`},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Մեր «Մղոն Էքսպրեսը» դրսից ծանրոց ա բերում։ Ինքնաթիռով բերելը հեշտ ա․ հազարավոր տուփ մի անգամից, էժան։'},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Բա որ տուփը հասնում ա պահեստ… Էստեղից մինչև մարդու դուռը՝ դա ա <b>«վերջին մղոնը»</b>։ Ամեն տուփի համար՝ առանձին դուռ, խցանում, շենքի կոդ։ Փողը հենց էստեղ ա վառվում։'},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Դե լավ, խոսելով չի։ Դարպասի մոտից վերցրու երեք ծանրոց ու տար տերերին։ Ներքևում ցուցակն ա, <b>դեղին գիծն</b> էլ ճամփեն ցույց կտա։',opts:[{t:'Գնացի՜նք 💪',c:'g',end:1}]}],()=>setQ(1));return;}
    if(G.q===3){DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Հը, տատիկին գտա՞ր։ Տեսա՞ր՝ մարդը տանը չէր, ու նույն տուփի համար երկու անգամ գնացիր։ Հիմա պատկերացրու՝ ամիսը ութսուն հազար ծանրոց ենք տանում։'},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Լսի, ախպերս։ Ես ծերացել եմ, Նիվան՝ ինձանից էլ շատ։ <b>Քեզ տնօրեն եմ նշանակում։</b> Ահա հավելվածդ՝ 📊։ Բյուջեն հարյուր միլիոն ա, խնայի։'},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Առաջին գործը՝ <b>փոստամատներ</b> դիր էնտեղ, որտեղ շատ տներ կան։ Ու <b>զեղչ</b> տուր նրանց, ով տուփը փոստամատից կվերցնի։ Թե չէ ժողովուրդը սովորությունը չի փոխի։',opts:[{t:'📊 Բացել հավելվածը',c:'g',end:1,go:()=>setTimeout(openTerminal,250)},{t:'Լավ, ձյաձյա',end:1}]}],()=>setQ(4));return;}
    if(G.q===7&&!G.bf){DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Ախպերս, Սև ուրբաթ ա։ Անին մենակ տասնյոթ զույգ կոշիկ ա պատվիրել։ Պատվերները կրկնապատկվել են, պահեստը լիքն ա։'},
      {who:'Աշոտ ձյաձյա',p:'ashot',t:'Ութ ծանրոց պիտի հանձնես։ Հինգ րոպեում հասցնես՝ լավ բոնուս կա։ Նիվան վերցրու 🚙, տասը տուփ ա տանում։',opts:[{t:'🔥 Սկսել',c:'g',end:1,go:()=>{G.bf={n:0,left:300,taken:0};toast('🛍️ Սև ուրբաթ։ Վերցրու ծանրոցները պահեստից');sfx.horn();updQuest();}},{t:'Մի րոպե',end:1}]}]);return;}
    if(questMark(n)==='side'){DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Ախպերս, Նիվան էլի չի վառվում։ Մի հատ հրի, էլի․ մեջը երեք պարկ կարտոֆիլ ա 🥔 (լրացուցիչ)',opts:[{t:'💪 Հրեմ',c:'g',end:1,go:()=>{EV.nivaPush={x:W.places.niva.x,y:W.places.niva.y,n:0};toast('💪 Մոտեցիր Նիվային և 8 անգամ սեղմիր «Հրել»');}},{t:'Հետո, ձյաձյա',end:1}]}]);return;}
    say(pick(TXT.ashotIdle));return;}
  if(n.id==='tatik'){
    if(G.q===2){const p=G.inv.find(x=>x.tatik);DLG.open([{who:'Սիրանույշ տատիկ',p:'tatik',t:'Վա՜յ, բալես, իմ ծանրոցն ե՞ս բերել։ Ես կանաչի էի առնում, հեռախոսս էլ տանն ա մնացել։ Ցավդ տանեմ, ների։'},
      {who:'Սիրանույշ տատիկ',p:'tatik',t:'Արի մի հատ դոլմա կեր, տաք ա 🫑։ Գիտե՞ս ինչ, ինձ համար հեշտ կլիներ, որ ծանրոցը շուկայի մոտ <b>փոստամատում</b> թողնեիր․ ես ամեն օր էստեղ եմ։',opts:[{t:'🫑 Ուտել դոլման և հանձնել',c:'g',end:1}]}],()=>{if(p)finishParcel(p,'home');G.boost=20;toast('🫑 Դոլմա՝ 20 վայրկյան արագություն','good');setTimeout(()=>setQ(3),500);});return;}
    say(pick(TXT.tatikIdle));return;}
  if(n.id==='aram'){
    if(G.q===6&&!G.qd.aramAsk){DLG.open([{who:'Արամ',p:'aram',t:'Բարև։ SMS հաստատո՞ւմ։ Հեշտ ա․ գալուց առաջ գրում ենք՝ «Ձեր ծանրոցը կգա 14:00–16:00, հարմա՞ր ա»։ Մարդն ինքն ա ժամ ընտրում ու տանն ա լինում։'},
      {who:'Արամ',p:'aram',t:'Մենակ թե… վեց ժամ ա բան չեմ կերել, գլուխս չի աշխատում։ Հայկոյից մի քյաբաբ կբերե՞ս։ Լավաշով, առանց սոխի 😅',opts:[{t:'🍢 Կբերեմ',c:'g',end:1}]}],()=>{G.qd.aramAsk=1;updQuest();});return;}
    if(G.q===6&&G.qd.kyab){DLG.open([{who:'Արամ',p:'aram',t:'Վա՜յ, կյանքս փրկեցիր։ *ուտում ա* … Վերջ, պատրաստ ա։ SMS հաստատումը միացված ա ամբողջ ընկերության համար 🚀'}],()=>{G.co.sms=true;addXP(60);lesson('sms',()=>setQ(7));});return;}
    say(pick(TXT.aramIdle));return;}
  if(n.id==='hayko'){if(G.side.samo===1)G.flags.boughtForSamo=1;DLG.open([{who:'Հայկո',p:'hayko',t:pick(TXT.haykoIdle)+(G.q===6&&G.qd.aramAsk&&!G.qd.kyab?' Արամի՞ համար ա։ Առանց սոխի, գիտեմ 😄':'')+(G.side.samo===1?' Սամոյի լավաշն էլ վերցրու, պատրաստ ա։':''),opts:[{t:`🍢 Քյաբաբ · 500 ֏ (մոտդ ${fmt(G.money)} ֏ կա)`,c:'g',end:1,go:buyKyabab},{t:'Հետո',end:1}]}]);return;}
  if(n.id==='zhora'){
    if(!G.side.zhora){G.side.zhora=1;const c=W.places.cascade;G.side.lostStone={x:c.x+130,y:c.y-90};DLG.open([{who:'Ժորա',p:'zhora',t:'Ախպերս, նարդուս սպիտակ քարը կորել ա։ Վերջին անգամ Կասկադի մոտ էի խաղում, երևի էնտեղ ա ընկել։ Կնայե՞ս։ (լրացուցիչ)',opts:[{t:'Կնայեմ ⚪',c:'g',end:1,go:()=>toast('⚪ Քարը փայլում է Կասկադի մոտ։ Նայիր մինի-քարտեզին')},{t:'Հետո',end:1}]}]);return;}
    if(G.side.stoneGot&&G.side.zhora===1){G.side.zhora=2;DLG.open([{who:'Ժորա',p:'zhora',t:'Գտա՞ր։ Ապրես, ախպերս, հերոս ես։ Վերցրու երկու հազար ու մի խորհուրդ․ Սիրանույշ տատիկի հետ նարդի մի խաղա։ Երբեք։'}],()=>{addMoney(2000);addXP(50);});return;}
    say(pick(TXT.zhoraIdle));return;}
  if(n.id==='gagik'){
    if(!G.side.gagik&&G.q>=2){DLG.open([{who:'Գագիկ',p:'gagik',t:'Ախպեր ջան, շտապ գործ ա։ Էս տուփը երկու րոպեում հասցրու Անիին, Երևան Մոլ։ Երեք հազար ու իմ հարգանքը։ (լրացուցիչ)',opts:[{t:'⚡ Գնացի',c:'g',end:1,go:()=>{if(G.inv.length>=cap()){toast('🎒 Պայուսակը լիքն է');return;}G.side.gagik={left:120};const p={id:PID++,item:'Գագիկի «շատ գաղտնի» տուփը',to:'Անի',dest:'npc',npc:'ani',express:true,att:0};G.inv.push(p);G.sel=p.id;renderTray();toast('⚡ Էքսպրես՝ 2 րոպե դեպի Երևան Մոլ');}},{t:'Հետո',end:1}]}]);return;}
    say(pick(TXT.gagikIdle));return;}
  if(n.id==='ani'){const ex=G.inv.find(p=>p.npc==='ani');if(ex){G.inv=G.inv.filter(p=>p!==ex);const ok=G.side.gagik&&G.side.gagik.left>0;G.side.gagik='done';renderTray();
      DLG.open([{who:'Անի',p:'ani',t:ok?'Գագի՞կն ա ուղարկել։ Էլի կոշիկ… տասնիններորդ զույգս։ Մենակ նայելու համար ա 😍':'Ուշացար, բայց ոչինչ․ ես երեք ժամ ա Մոլում եմ, շտապող չկա։'}],()=>{if(ok){addMoney(3000);addXP(60);}else addXP(20);G.st.del++;G.st.att++;G.st.cost+=1000;hud();});return;}
    say(pick(TXT.aniIdle));return;}
  if(n.id==='samo'){if(!G.side.samo){G.side.samo=1;DLG.open([{who:'Սամո',p:'samo',t:'Ախպերս, խորովածը պատրաստ ա, լավաշը չկա։ Հայկոյից լավաշ բեր (խոսի հետը), կհյուրասիրեմ։ (լրացուցիչ)'}]);return;}
    if(G.side.samo===1&&G.flags.boughtForSamo){G.side.samo=2;DLG.open([{who:'Սամո',p:'samo',t:'Հա՛, լավաշն էլ եկավ։ Վերցրու մի շամփուր, տաք-տաք։ Կեր, ուժ ունենաս 🔥'}],()=>{G.boost=40;addXP(40);toast('🔥 Խորոված՝ 40 վայրկյան արագություն','good');});return;}
    say(pick(TXT.samoIdle));return;}
  if(n.id==='prof'){if(G.q===9){defense();return;}say(pick(n.lines));return;}
  say(pick(n.lines||['…']));}
function pushNiva(){EV.nivaPush.n++;sfx.pop();floatTxt(EV.nivaPush.x,EV.nivaPush.y-30,'💪 '+EV.nivaPush.n+'/8','#ffd84d');EV.nivaShake=.3;
  if(EV.nivaPush.n>=8){EV.nivaPush=null;G.side.nivaDone=1;sfx.horn();DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Վառվե՜ց 🚗💨 Ապրես, ախպերս։ Մի պարկ կարտոֆիլ տամ… չէ, լավ, հազար հինգ հարյուր դրամ վերցրու․ կարտոֆիլը Մարտունուց ա, ինձ պետք ա։'}],()=>{addMoney(1500);addXP(40);});}}

/* ====================== DIRECTOR APP (simplified) ====================== */
function openTerminal(){if(!G)return;if(!G.co.unlocked){toast('📊 Հավելվածը կբացվի, երբ դառնաս տնօրեն (առաջադրանք 4)');return;}
  $('#tTerm').classList.remove('hot');if(!G.flags.app){G.flags.app=1;updQuest();}
  const render=()=>{const c=company(),built=builtN(),left=BUDGET-c.inv;
    const pct=clamp((705-c.cpd)/(705-600),0,1)*100,tp=(705-TARGET)/(705-600)*100;
    const free=W.slots.map((s,i)=>({s,i})).filter(o=>!o.s.pre&&!o.s.built);
    const rec=new Set(free.slice().sort((a,b)=>G.q<=5?dist(a.s,hubPt())-dist(b.s,hubPt()):b.s.pop-a.s.pop).slice(0,2).map(o=>o.i));
    const cost=n=>fmt(n*9)+' մլն ֏';
    $('#modBox').innerHTML=`<div class="row"><h2 style="flex:1">📊 Տնօրենի հավելված</h2><button class="x" id="tx">✕</button></div>
    <p class="mut" style="margin-top:4px">«Մղոն Էքսպրես» · ամսական 80 000 ծանրոց · մնացած բյուջե՝ <b style="color:#fff">${fmt(left/1e6)} մլն ֏</b></p>
    <div class="big-kpi"><div class="l">💰 Մեկ ծանրոց առաքելու միջին ծախսը</div><div class="v" style="color:${c.cpd<=TARGET?'#3ddc84':'#fff'}">${fmt(c.cpd,0)} ֏ <small>${c.cpd<704?'(սկզբում՝ 705 ֏)':''}</small></div>
      <div class="meter"><i style="width:${pct}%"></i><b style="left:${tp}%"></b></div><div class="meter-l"><span>705 ֏ · թանկ</span><span>թիրախ՝ ${TARGET} ֏</span><span>էժան</span></div>
      <div class="chk"><span class="${built?'y':''}">▣ ${3*built+40} փոստամատ</span><span class="${G.co.d>0?'y':''}">🏷️ զեղչ ${G.co.d} ֏</span><span class="${G.co.sms?'y':''}">💬 SMS ${G.co.sms?'միացված':'— կմիացնի Արամը'}</span>${c.save>0?`<span class="y">📉 −${fmt(c.save/1e6,1)} մլն ֏ ամսական</span>`:''}</div>
      ${c.over>.02?'<p style="color:#ffb3b3;font-size:13px;margin-top:8px">⚠ Փոստամատները չեն բավարարում բոլոր ցանկացողներին։ Կառուցիր ավելին կամ իջեցրու զեղչը։</p>':''}</div>
    <h3>1 · ▣ Փոստամատներ</h3>
    <p class="mut" style="margin:-4px 0 8px">1 կետ = 3 փոստամատ = 9 մլն ֏։ Որտեղ շատ տներ կան, այնտեղ փոստամատը ավելի օգտակար է։</p>
    ${free.length?`<button class="bt ${left>=COST.slot*free.length?'ok':''}" id="ball" style="width:100%;margin-bottom:8px" ${left<COST.slot*free.length?'disabled':''}>⚡ Կառուցել բոլորը (${free.length} կետ · ${cost(free.length)})</button>`:''}
    ${W.slots.map((s,i)=>s.pre?'':`<div class="slotrow"><span style="font-size:20px">▣</span><span class="z">${s.zone}${rec.has(i)&&!s.built?'<span class="rec">👍 Խորհուրդ</span>':''}<small>🏠 ${s.pop} տուն · ${meters(dist(s,hubPt()))} մ պահեստից</small></span>${s.built?'<b style="color:#3ddc84">✓ Կառուցված</b>':`<button class="bt ${left>=COST.slot?'g':''}" data-b="${i}" ${left<COST.slot?'disabled':''}>Կառուցել</button>`}</div>`).join('')}
    <h3>2 · 🏷️ Զեղչ փոստամատից վերցնողներին</h3>
    <p class="mut" style="margin:-4px 0 8px">Զեղչը տրվում է, եթե մարդը ծանրոցը վերցնում է 24 ժամում։ Որքան մեծ զեղչ, այնքան շատ մարդ կընտրի փոստամատ, բայց զեղչն էլ փող արժե։</p>
    <div class="seg">${[[0,'Զեղչ չկա','քիչ մարդ'],[100,'100 ֏','28% մարդ · ✓ լավագույնը'],[200,'200 ֏','40% մարդ · թանկ']].map(([v,a,b])=>`<button data-d="${v}" class="${G.co.d===v?'on':''}">${a}<small>${b}</small></button>`).join('')}</div>
    <h3>3 · 💬 SMS հաստատում</h3><div class="slotrow"><span style="font-size:20px">💬</span><span class="z">Մարդուն նախապես հարցնում ենք հարմար ժամը<small>«տանը չկա» դեպքերը՝ 15% → 11%</small></span>${G.co.sms?'<b style="color:#3ddc84">✓ Միացված</b>':'<b style="color:#ffb347">🔒 Արամը (առաջադրանք 7)</b>'}</div>
    <details><summary>🎓 Ինչ է ասում կուրսային աշխատանքը</summary><p>Կուրսային աշխատանքի լուծումը՝ +27 փոստամատ, 100 ֏ զեղչ և SMS հաստատում։ Արդյունքը՝ ծախսը 704,76 → 632,77 ֏ մեկ առաքման վրա, ամսական 5,76 մլն ֏ խնայողություն, ներդրումը (81 մլն ֏) հետ է գալիս ≈ 11,4 ամսում։</p></details>`;
    $('#tx').onclick=closeMod;
    const build=list=>{list.forEach(i=>W.slots[i].built=true);sfx.coin();burst(G.p.x,G.p.y-30,'#7ff0b0');toast(`▣ ${list.length>1?list.length+' կետ կառուցվեց':'Փոստամատներ՝ '+W.slots[list[0]].zone}։ Դրանք երևում են քարտեզին`,'good');render();checkDir();};
    document.querySelectorAll('[data-b]').forEach(b=>b.onclick=()=>build([+b.dataset.b]));
    const ba=$('#ball');if(ba)ba.onclick=()=>build(free.map(o=>o.i));
    document.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{G.co.d=+b.dataset.d;sfx.tap();render();checkDir();});};
  modal('',()=>{save();updQuest();});render();}
function checkDir(){const c=company();hud();updQuest();
  if(G.q===4&&builtN()>=2&&G.co.d>=100&&!G.qd.adv){G.qd.adv=1;setTimeout(()=>{closeMod();lesson('discount',()=>{setQ(5);DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:'Կեցցե՛ս։ Հիմա պահեստից ծանրոցներ վերցրու․ բոլորը գնում են քո նոր փոստամատը։ Տեսնենք՝ ինչքան արագ կստացվի։'}]);});},500);}
  if(G.q===8&&c.cpd<=TARGET&&!G.qd.adv){G.qd.adv=1;setTimeout(()=>{closeMod();sfx.lvl();burst(G.p.x,G.p.y-30,'#7ff0b0');setQ(9);DLG.open([{who:'Աշոտ ձյաձյա',p:'ashot',t:`Մեկ առաքումը՝ ${fmt(c.cpd,0)} ֏… Ախպերս, աչքերս լցվեցին։ Ոնց կարտոֆիլը՝ մեծ պարկով էժան ա։ Հիմա գնա ՀԱՊՀ, ցույց տուր պրոֆեսորին։`}]);},600);}}

/* ====================== DEFENSE / FINAL ====================== */
function defense(){const c=company(),cm=courseModel(.28,.11);const score=(c.cpd<=TARGET?2:0)+(c.PP&&c.PP<=14?1:0)+(G.st.del>=20?1:0)+(G.co.sms?1:0)+(G.st.lock>=5?1:0);
  const grade=score>=6?'Գերազանց ✨':score>=4?'Լավ 👍':'Բավարար 🙂';sfx.lvl();burst(G.p.x,G.p.y-40,'#ffd84d');
  DLG.open([{who:'Պրոֆ. Մկրտչյան',p:'prof',t:'Բարև Ձեզ, երիտասարդ։ Հանձնաժողովը լսում ա։ Ի՞նչ արեցիք վերջին մղոնի հետ։'},
    {who:G.nick,p:'me',t:`Քաղաքում հիմա ${c.N} փոստամատ ա, 100 ֏ զեղչ ու SMS հաստատում։ Մեկ առաքման ծախսը ${fmt(c.cpd0,0)}-ից իջավ ${fmt(c.cpd,0)} ֏, ամսական ${fmt(c.save/1e6,1)} մլն ֏ ենք խնայում։`},
    {who:'Պրոֆ. Մկրտչյան',p:'prof',t:'Իսկ Սիրանույշ տատի՞կը։'},{who:G.nick,p:'me',t:'Հիմա ինքը ծանրոցը շուկայի մոտի փոստամատից ա վերցնում՝ կանաչու հետ միասին 🌿'},
    {who:'Պրոֆ. Մկրտչյան',p:'prof',t:`Գնահատականը՝ «${grade}»։ Ու հիշեք․ մեկ գործիքով չի ստացվում, միայն բոլորը միասին։`}],()=>finalScreen(c,cm,grade));}
function finalScreen(c,cm,grade){setQ(10);save();
  const tile=(l,v,t,ok)=>`<div class="big-kpi" style="margin:0;padding:12px"><div class="l">${l}</div><div class="v" style="font-size:24px;color:${ok?'#3ddc84':'#fff'}">${v}</div><div class="mut" style="font-size:11.5px!important">${t}</div></div>`;
  modal(`<div class="big-e">🎓</div><h2 style="text-align:center">Պաշտպանված է՝ «${grade}»</h2><p class="mut" style="text-align:center">${G.nick} · ${G.st.del} առաքում · ${G.st.lock} փոստամատով · ${G.st.fail} «տանը չկա»</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px">
   ${tile('💰 Ծախսը մեկ առաքման վրա',fmt(c.cpd,0)+' ֏','սկզբում՝ 705 ֏',c.cpd<=TARGET)}${tile('📉 Ամսական խնայողություն',fmt(c.save/1e6,1)+' մլն ֏','կուրսային՝ '+fmt((cm.C0-cm.C1)/1e6,2)+' մլն',c.save>0)}
   ${tile('⏳ Ներդրումը հետ կգա',c.PP?fmt(c.PP,1)+' ամսում':'—','կուրսային՝ '+fmt(cm.PP,1)+' ամիս',c.PP&&c.PP<=14)}${tile('▣ Փոստամատներ',c.N+' հատ','սկզբում՝ 40',true)}</div>
  <p class="lesson-s" style="margin-top:14px">${TXT.lessons.final.s}</p>
  <div class="row" style="margin-top:14px;flex-wrap:wrap"><button class="bt g" id="fs" style="flex:1">📤 Կիսվել</button><button class="bt" id="fc" style="flex:1">▶ Շարունակել խաղալ</button></div>`);
  $('#fc').onclick=closeMod;$('#fs').onclick=async()=>{const t=`«Վերջին մղոն» խաղում ես դարձա տնօրեն և իջեցրի առաքման ծախսը մինչև ${fmt(c.cpd,0)} ֏ 🎓 Փորձիր դու էլ՝ ${location.href}`;try{if(navigator.share)await navigator.share({title:'Վերջին մղոն',text:t});else{await navigator.clipboard.writeText(t);toast('📋 Պատճենվեց');}}catch(e){}};}

/* ====================== MAP + HELP ====================== */
function openMap(){if(!G)return;const S=7;modal(`<div class="row"><h2 style="flex:1">🗺️ Երևանի քարտեզ</h2><button class="x" id="mx">✕</button></div><canvas id="bigm" width="${MW*S}" height="${MH*S}" style="width:100%;border-radius:14px;margin-top:10px;display:block"></canvas>
  <p class="mut" style="margin-top:8px">🔴 դու · 🟡 ընտրված նպատակ և դեղին գիծը · 1-5 թվերը՝ քո ծանրոցները · ▣ փոստամատներ · 📦 պահեստ</p>`);$('#mx').onclick=closeMod;
  const g=$('#bigm').getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(MINI,0,0,MW*S,MH*S);const sc=S/TS;
  Object.entries(W.places).forEach(([k,p])=>{if(!p.name)return;g.font='800 14px '+FONT;g.textAlign='center';g.lineWidth=4;g.strokeStyle='rgba(20,24,43,.8)';g.strokeText(p.name,p.x*sc,p.y*sc-10);g.fillStyle='#fff';g.fillText(p.name,p.x*sc,p.y*sc-10);});
  drawMarkers(g,sc,8);}
function help(){modal(`<div class="row"><h2 style="flex:1">❓ Օգնություն</h2><button class="x" id="hx">✕</button></div>
 <h3>🕹️ Կառավարում</h3><div class="gl"><b>Քայլել</b><span>W A S D / սլաքներ · հեռախոսում՝ մատը սեղմիր էկրանին ու քաշիր</span><b>Գործողություն</b><span>E / Space կամ ներքևի մեծ նարնջագույն կոճակը</span><b>Ծանրոց ընտրել</b><span>սեղմիր ներքևի ցուցակում կամ 1–9 ստեղները</span><b>Նիվա</b><span>V կամ 🚙 կոճակը (մոտ լինելիս)</span><b>Տեսախցիկ</b><span>C կամ 🎥 կոճակը՝ վերևից → 3-րդ դեմք → 1-ին դեմք · մկնիկով պտտիր, անիվով մոտեցրու</span><b>Ռադիո</b><span>R կամ 📻 (Նիվայում)</span><b>Քարտեզ</b><span>M կամ սեղմիր մինի-քարտեզին</span></div>
 <h3>🧭 Ինչպես չմոլորվել</h3><p>Վերևի ձախ քարտը ցույց է տալիս <b>ընթացիկ քայլը</b> (դեղին կետով) և հուշում 💡։ Աշխարհում <b>դեղին կետագիծը</b> միշտ տանում է դեպի նպատակը։ Դեղին <b>«!»</b>՝ գլխավոր առաջադրանք, կապույտ <b>«?»</b>՝ լրացուցիչ։</p>
 <h3>📖 Բառարան</h3><div class="gl">${TXT.glossary.map(([a,b])=>`<b>${a}</b><span>${b}</span>`).join('')}</div>
 <p class="mut" style="margin-top:12px">🚙 3D Նիվա՝ «Lada Niva» — tiunov.se · անվահեծաններ՝ «Lada Niva Car Rims Armenian Style Tuning» — Hambar1an · «Lada 2107 tun» — Aslan · «Low Detail Animated Crowd» — Shahriar Shahrabi · «Cardboard Boxes Pack» — Alex human · Sketchfab, CC BY 4.0 · 3D շարժիչ՝ three.js (MIT)</p><div class="row" style="margin-top:16px"><button class="bt" id="hr" style="flex:1">↺ Սկսել նորից</button><button class="bt g" id="hk" style="flex:1">Լավ</button></div>`);
 $('#hx').onclick=$('#hk').onclick=closeMod;$('#hr').onclick=()=>{if(confirm('Ջնջե՞լ առաջընթացը և սկսել նորից')){try{localStorage.removeItem(SAVEK);}catch(e){}location.reload();}};}

/* ====================== EVENTS ====================== */
const EV={t:70,niva:null,wedding:0,bobik:0,rain:0,nivaPush:null,nivaShake:0,danced:0};
function worldEvent(){const k=pick(['niva','wedding','marsh','bobik','rain','wedding','call','lavash','taxi','tatbalcony']);chat('ՔԱՂԱՔՈՒՄ',TXT.events[k].t,1);if(k!=='marsh')toast(TXT.events[k].t);
  if(k==='niva'){const n=pick(W.nodes);EV.niva={x:n.x+50,y:n.y,life:40};}if(k==='wedding'){EV.wedding=45;EV.danced=0;}if(k==='bobik')EV.bobik=40;if(k==='rain')EV.rain=30;
  if(k==='taxi'){const c=cars.find(c=>c.kind==='taxi');if(c){c.stop=6;bubble(c,'Ախպեր, ու՞ր ենք գնում։ Մեկ ա, 600 դրամ 🚕',4);}}
  if(k==='marsh'){const m=cars.find(c=>c.kind==='marsh');if(m)m.stop=12;}}

/* ====================== GPS (BFS on tile grid) ====================== */
const gps={t:0,path:null,key:''};
function bfsPath(from,to,road){const sx=clamp(Math.floor(from.x/TS),0,MW-1),sy=clamp(Math.floor(from.y/TS),0,MH-1),gx=clamp(Math.floor(to.x/TS),0,MW-1),gy=clamp(Math.floor(to.y/TS),0,MH-1);
  const N=MW*MH,prev=new Int32Array(N).fill(-1),q=new Int32Array(N);let h=0,tl=0;const s=sy*MW+sx;prev[s]=s;q[tl++]=s;let best=s,bd=1e9;
  const pass=(x,y)=>road?isRoadT(x,y):!W.solid[y*MW+x];
  while(h<tl){const i=q[h++],x=i%MW,y=(i/MW)|0;const d=Math.abs(x-gx)+Math.abs(y-gy);if(d<bd){bd=d;best=i;if(d===0)break;}
    for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy;if(nx<0||ny<0||nx>=MW||ny>=MH)continue;const j=ny*MW+nx;if(prev[j]!==-1||!pass(nx,ny))continue;prev[j]=i;q[tl++]=j;}}
  const pts=[];let i=best;while(i!==s){pts.push(i);i=prev[i];}pts.push(s);pts.reverse();
  const out=[];pts.forEach((i,k)=>{const p={x:(i%MW+.5)*TS,y:(((i/MW)|0)+.5)*TS};if(out.length>=2){const a=out[out.length-2],b=out[out.length-1];if((a.x===b.x&&b.x===p.x)||(a.y===b.y&&b.y===p.y)){out[out.length-1]=p;return;}}out.push(p);});
  if(out.length)out[0]={x:from.x,y:from.y};if(!road)out.push({x:to.x,y:to.y});else if(bd>0)out.push({x:to.x,y:to.y,walk:1});return out;}

/* ====================== HUD ====================== */
function meLook(){return {skin:'#f1c39c',shirt:G?G.cap:CAPS[0],pants:'#2f3b57',hat:'cap',capC:G?G.cap:CAPS[0],bag:true,vest:false};}
function hud(){if(!G)return;$('#lv').textContent=G.lvl;$('#nick').textContent=G.nick;$('#money').textContent=fmt(G.money);
  const c=company(),k=$('#kpi');
  if(G.co.unlocked){const pct=clamp((705-c.cpd)/(705-TARGET),0,1)*100;k.innerHTML=`<div class="mut" style="font-size:11px!important">💰 Ծախս մեկ առաքման վրա</div><div class="big" style="color:${c.cpd<=TARGET?'#3ddc84':'#fff'}">${fmt(c.cpd,0)} ֏ <span class="mut" style="font-size:11px!important;font-weight:600">/ թիրախ ${TARGET}</span></div><div class="bar"><i style="width:${pct}%"></i></div>`;}
  else k.innerHTML=`<div class="mut" style="font-size:11px!important">Քո առաքումները</div><div class="big">✓ ${G.st.del} <span style="color:#ff8a95;font-size:14px">· ✕ ${G.st.fail} տանը չկար</span></div>`;
  $('#tVan').classList.toggle('on',G.p.inVan);
  if(window.R3&&R3.ready&&hud._k!==G.cap){hud._k=G.cap;R3.portrait($('#meAv'),meLook());}renderTray();}

/* ====================== 3D BRIDGE: movement, Niva driving, camera, radio ====================== */
let MINI,last=0,chatT=5,running=false;
function cycleCam(){if(!window.R3||!R3.ready)return;const m=R3.cycleCam();$('#tCam').dataset.m=m;
  toast(m==='top'?'🎥 Վերևից (դասական տեսք)':m==='third'?'🎥 3-րդ դեմք · պտտիր մկնիկով կամ A/D-ով':'🎥 1-ին դեմք · նայիր մկնիկով, W՝ առաջ');sfx.tap();}
const angDiff=(a,b)=>{let d=a-b;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;return d;};
function walk(dt,kx,ky,il){const p=G.p,C=R3.cam;const sp=118*(G.boost>0?1.35:1)*(G.side.bobik?1.08:1);let dx=0,dy=0;
  if(C.mode==='top'){dx=kx;dy=ky;}else{C.yaw-=kx*dt*(C.mode==='first'?2.2:2.6);const f=-ky;dx=Math.sin(C.yaw)*f;dy=Math.cos(C.yaw)*f;}
  const l=Math.hypot(dx,dy);p.moving=l>.15;if(!p.moving)return;if(C.mode!=='top'&&Math.abs(ky)<.15)return;
  const nx=p.x+dx*sp*dt,ny=p.y+dy*sp*dt;const ok=(x,y)=>!(isSolidPx(x-8,y-3)||isSolidPx(x+8,y-3)||isSolidPx(x-8,y+3)||isSolidPx(x+8,y+3));
  if(ok(nx,p.y))p.x=nx;if(ok(p.x,ny))p.y=ny;const ta=Math.atan2(dy,dx);p.a=p.a==null?ta:p.a+angDiff(ta,p.a)*Math.min(1,dt*14);}
function driveNiva(dt,kx,ky,il){const p=G.p,C=R3.cam,v=G.van;v.sp=v.sp||0;v.a=v.a||0;const max=310*(G.boost>0?1.15:1);let thr=0,steer=0;
  if(C.mode==='top'){if(il>.15){const ta=Math.atan2(ky,kx);const da=angDiff(ta,v.a);steer=clamp(da*1.8,-1,1);thr=il*(Math.cos(da)>-.2?1:.35);}}
  else{thr=-ky;steer=kx;}
  v.sp+=thr*560*dt;v.sp*=1-dt*(Math.abs(thr)>.05?.55:1.9);v.sp=clamp(v.sp,-110,max);
  v.a+=steer*dt*2.7*clamp(v.sp/120,-1,1);
  const ca=Math.cos(v.a),sa=Math.sin(v.a);const nx=v.x+ca*v.sp*dt,ny=v.y+sa*v.sp*dt;
  const ok=(x,y)=>isRoadPx(x,y)&&isRoadPx(x+ca*26,y+sa*26)&&isRoadPx(x-ca*26,y-sa*26)&&!(EV.niva&&Math.hypot(x-EV.niva.x,y-EV.niva.y)<40)&&!(EV.police&&Math.hypot(x-EV.police.x,y-EV.police.y)<40);
  if(ok(nx,ny)){v.x=nx;v.y=ny;}else if(ok(nx,v.y)){v.x=nx;v.sp*=.9;}else if(ok(v.x,ny)){v.y=ny;v.sp*=.9;}
  else{if(Math.abs(v.sp)>60){sfx.bad();if(!G.flags.vanTip){G.flags.vanTip=1;toast('🚙 Նիվան քշում է միայն ասֆալտով։ Բակեր մտնելու համար իջիր (V)');}}v.sp*=-.25;}
  p.x=v.x;p.y=v.y;p.moving=Math.abs(v.sp)>8;
  // speeding → traffic police (ՃՈ)
  if(v.sp>285&&G.q>=2&&!EV.police&&!DLG.on){EV.fast=(EV.fast||0)+dt;if(EV.fast>4&&(EV.policeCD||0)<=0)policeStop();}else EV.fast=0;}
function policeStop(){const v=G.van;EV.policeCD=150;EV.police={x:v.x+Math.cos(v.a)*92,y:v.y+Math.sin(v.a)*92,a:v.a+Math.PI};v.sp=0;sfx.horn();
  DLG.open([{who:'Ճանապարհային ոստիկան Վազգեն',p:'police',t:pick(TXT.police.open)},{who:'Ոստիկան Վազգեն',p:'police',t:'Ի՞նչ ասենք, ախպերս։',opts:[
    {t:'«Ես Աշոտ ձյաձյայի տղեն եմ» 😎',c:'g',end:1,go:()=>{toast('👮 '+pick(TXT.police.ashot));}},
    {t:'«Ծանրոց եմ տանում տատիկին» 📦',end:1,go:()=>{toast('👮 '+pick(TXT.police.tatik));}},
    {t:'Վճարել տուգանք · 5 000 ֏',end:1,go:()=>{addMoney(-Math.min(G.money,5000));toast('🧾 Տուգանքը տվեցիր։ Ռադարը սուտ չի խոսում 😅');}}]}],()=>{setTimeout(()=>{EV.police=null;},5000);});}
const RADIO={st:0,iv:null,dj:0,names:['','📻 Ռադիո «Ռաբիզ FM»','📻 «Երևան Ջազ»','📻 «Կարտոֆիլ FM» · ռաբիզ նոնստոպ']};
function radio(off){if(off||!G.p.inVan){RADIO.st=0;}else RADIO.st=(RADIO.st+1)%4;clearInterval(RADIO.iv);RADIO.iv=null;$('#tRadio').classList.toggle('on',RADIO.st>0);if(off)return;
  if(!RADIO.st){toast('📻 Ռադիոն անջատված է');if(SND.on)music(true);return;}if(!SND.on){SND.on=true;$('#tSnd').firstChild.textContent='🔊';}ac()&&ac().resume();music(false);
  toast(RADIO.names[RADIO.st]+' · '+pick(TXT.radio));const F=n=>440*2**((n-69)/12);let k=0;
  const songs={1:{m:[64,65,68,69,68,65,64,62,64,65,64,62,60,62,64,64],b:[40,40,47,47,45,45,40,40],sp:170,w:'sawtooth',v:.018},2:{m:[62,65,69,72,71,67,64,62,60,64,67,71,69,65,62,60],b:[38,45,43,36,41,45,38,43],sp:260,w:'sine',v:.03},3:{m:[69,70,73,74,73,70,69,67,69,70,69,67,65,67,69,69],b:[45,45,52,52,50,50,45,45],sp:140,w:'square',v:.012}}[RADIO.st];
  RADIO.iv=setInterval(()=>{const i=k++%16;tone(F(songs.m[i]),songs.sp/1000*1.4,songs.w,songs.v);if(i%2===0)tone(F(songs.b[(i/2)%8]),.25,'triangle',.05);if(i%4===0)tone(90,.08,'square',.03);
    if(k%96===0)chat('DJ Արտո',pick(TXT.radio));},songs.sp);}
function update(dt){const p=G.p,C=R3.cam;
  let kx=(keys['d']||keys['arrowright']?1:0)-(keys['a']||keys['arrowleft']?1:0)+joy.x,ky=(keys['s']||keys['arrowdown']?1:0)-(keys['w']||keys['arrowup']?1:0)+joy.y;
  let il=Math.hypot(kx,ky);if(il>1){kx/=il;ky/=il;il=1;}if(DLG.on||modalOn()){kx=ky=0;il=0;}
  if(G.boost>0)G.boost-=dt;if(EV.policeCD>0)EV.policeCD-=dt;
  if(look.dx||look.dy){if(C.mode!=='top'){C.yaw-=look.dx*.0052;C.pitch=clamp(C.pitch-look.dy*.004,-1.1,.55);}look.dx=look.dy=0;}
  if(p.inVan)driveNiva(dt,kx,ky,il);else{walk(dt,kx,ky,il);}
  if(p.moving&&p.dance>0)p.dance=0;
  p.t+=dt;if(p.dance>0)p.dance-=dt;
  const sp=118*(G.boost>0?1.35:1);
  bots.forEach(b=>{moveOnGraph(b,dt,b.off);b.t+=dt;});walkers.forEach(w=>{moveOnGraph(w,dt,w.off);w.t+=dt;});
  if(Math.random()<.004){const b=pick(bots);if(dist(b,p)<500){const c=pick(TXT.chat)[1];bubble(b,c.length>60?c.slice(0,58)+'…':c,4);}}
  cars.forEach(c=>{if(c.stop>0){c.stop-=dt;if(c.kind==='marsh'&&Math.random()<.01)bubble(c,'Վարորդ ջան, կանգնի՜',2);return;}if(Math.hypot(c.x-p.x,c.y-p.y)<46&&!p.inVan){c.stop=.8;if(Math.random()<.02){sfx.horn();bubble(c,pick(TXT.drivers),2.5);}return;}moveOnGraph(c,dt,14);});
  NPC.forEach(n=>{n.t+=dt;if(n.talk>0){n.talk-=dt;n.moving=false;return;}
    if(n.dog){const tgt=EV.bobik>0||G.side.bobik?{x:p.x-30,y:p.y+12}:{x:n.hx+Math.sin(n.t*.4)*80,y:n.hy+Math.cos(n.t*.3)*40};const d=dist(n,tgt);n.moving=d>22;if(n.moving){const v=Math.min(d,(G.side.bobik||EV.bobik>0?sp*1.05:60)*dt);n.x+=(tgt.x-n.x)/d*v;n.y+=(tgt.y-n.y)/d*v;}if(G.p.inVan&&G.side.bobik){n.x=n.hx;n.y=n.hy;}return;}
    const wx=n.hx+Math.sin(n.t*.35)*16;n.moving=Math.abs(wx-n.x)>1.5;if(n.moving){n.x+=(wx-n.x)*dt*1.5;n.dir=wx<n.x?1:2;}else n.dir=0;
    if(dist(n,p)<120&&Math.random()<.003&&!questMark(n))bubble(n,pick(n.lines),3);});
  if(Math.random()<.003){const w=pick(walkers);if(dist(w,p)<320)bubble(w,pick(TXT.walkers),3);}
  if(Math.random()<.0018){const h=W.homes.filter(h=>h.balcony&&Math.hypot(h.door.x-p.x,h.door.y-p.y)<420);if(h.length){const b=pick(h);bubbles.push({e:{x:b.door.x,y:b.door.y-20},t:'👵 '+pick(TXT.balcony),life:3.5});}}
  if(!DLG.on&&!modalOn()){EV.t-=dt;if(EV.t<=0&&G.q>=2){EV.t=rnd(70,110);worldEvent();}}
  ['wedding','bobik','rain'].forEach(k=>{if(EV[k]>0)EV[k]-=dt;});if(EV.niva){EV.niva.life-=dt;if(EV.niva.life<=0)EV.niva=null;}if(EV.nivaShake>0)EV.nivaShake-=dt;
  if(G.side.gagik&&typeof G.side.gagik==='object')G.side.gagik.left-=dt;
  if(G.bf&&!G.bf.fin&&G.bf.left>0){G.bf.left-=dt;if(G.bf.left<=0)toast('⏱ Բոնուսի ժամանակը վերջացավ, բայց մի հուսահատվի՝ դեռ կհասցնես');}
  chatT-=dt;if(chatT<=0){chatT=rnd(7,12);const c=pick(TXT.chat);chat(c[0],c[1]);}
  floats.forEach(f=>{f.life-=dt;});floats=floats.filter(f=>f.life>0);
  bubbles.forEach(b=>b.life-=dt);bubbles=bubbles.filter(b=>b.life>0);
  gps.t-=dt;if(gps.t<=0){gps.t=.3;const qt=questTarget();gps.target=qt;gps.path=qt&&qt.pt?bfsPath(p,qt.pt,p.inVan):null;}
  ACT=DLG.on||modalOn()?null:findAct();const ab=$('#act');if(ACT){const h=ACT.t+'<small>E · Space</small>';if(ab.innerHTML!==h)ab.innerHTML=h;ab.classList.add('on');}else ab.classList.remove('on');
  if(!G.pm)G.pm={x:p.x,y:p.y};G.pm.x=p.x;G.pm.y=p.y;}
function drawMarkers(g,sc,r){const dot=(x,y,c,rr2=r,txt)=>{g.fillStyle=c;g.strokeStyle='#14182b';g.lineWidth=1.5;g.beginPath();g.arc(x*sc,y*sc,rr2,0,7);g.fill();g.stroke();if(txt){g.fillStyle='#14182b';g.font=`900 ${rr2*1.3}px ${FONT}`;g.textAlign='center';g.fillText(txt,x*sc,y*sc+rr2*.45);}};
  if(gps.path&&gps.path.length>1){g.save();g.strokeStyle='#ffd84d';g.lineWidth=Math.max(2,r*.45);g.lineJoin='round';g.beginPath();g.moveTo(gps.path[0].x*sc,gps.path[0].y*sc);gps.path.forEach(p=>g.lineTo(p.x*sc,p.y*sc));g.stroke();g.restore();}
  W.slots.forEach(s=>{if(s.built)dot(s.x,s.y,'#2bbf73',r*.7);});W.pudos.forEach(u=>dot(u.x,u.y,'#4fb3ff',r*.6));dot(hubPt().x,hubPt().y,'#ffb347',r*.8);
  G.inv.forEach((x,i)=>{const t=tgOf(x);if(t)dot(t.x,t.y,x.id===G.sel?'#ffd84d':'#ffffff',r*.95,String(i+1));});
  const qt=gps.target;if(qt&&qt.pt&&!G.inv.length)dot(qt.pt.x,qt.pt.y,'#ffd84d',r,'★');
  NPC.forEach(n=>{const m=questMark(n);if(m)dot(n.x,n.y,m==='main'?'#ffd84d':'#4fb3ff',r*.8,m==='main'?'!':'?');});
  dot(G.p.x,G.p.y,'#ff3b5c',r*1.05);}
function drawMini(){const c=$('#mm'),g=c.getContext('2d'),S=4,sc=S/TS;const cx=G.p.x*sc-c.width/2,cy=G.p.y*sc-c.height/2;g.setTransform(1,0,0,1,0,0);g.fillStyle='#3aa3d8';g.fillRect(0,0,c.width,c.height);
  g.save();g.translate(-cx,-cy);g.drawImage(MINI,0,0);drawMarkers(g,sc,7);g.restore();
  const z=zoneAt(Math.floor(G.p.x/TS),Math.floor(G.p.y/TS));if($('#zone').textContent!=='📍 '+z)$('#zone').textContent='📍 '+z;}
let lastSave=0,trayT=0;
document.addEventListener('visibilitychange',()=>{if(document.hidden){if(SND.on)music(false);clearInterval(RADIO.iv);for(const k in keys)keys[k]=false;joy.on=false;joy.x=joy.y=0;}else{last=performance.now();if(SND.on&&!RADIO.st)music(true);if(RADIO.st){RADIO.st--;radio();}}});
function frame(t){if(document.hidden){last=t;requestAnimationFrame(frame);return;}const dt=Math.min(.05,(t-last)/1000||0);last=t;
  if(running&&G){update(dt);R3.frame(dt);drawMini();trayT-=dt;if(trayT<=0){trayT=.5;renderTray();updQuest();}
    if(DLG.on&&DLG.typed<DLG.full.length){DLG.typed=Math.min(DLG.full.length,DLG.typed+dt*95);const s=DLG.full.slice(0,Math.floor(DLG.typed));$('#dTx').innerHTML=s.replace(/<[^>]*$/,'');}
    if(t-lastSave>15000){lastSave=t;save();}}
  else if(window.R3&&R3.ready)R3.title(dt);requestAnimationFrame(frame);}

/* ====================== BOOT ====================== */
buildWorld();initPatterns();
(function(){const m=W.places.market;W.tatikHome=W.homes.slice().sort((a,b)=>Math.hypot(a.door.x-m.x,a.door.y-m.y)-Math.hypot(b.door.x-m.x,b.door.y-m.y))[3];})();
setupNPCs();setupWorldLife();
function boot(){if(MINI)return;MINI=renderMini();const l=$('#loading');l.style.opacity=0;setTimeout(()=>l.remove(),500);requestAnimationFrame(frame);}
(function waitR3(){if(window.R3&&R3.ready)boot();else setTimeout(waitR3,60);})();
let capSel=CAPS[0];$('#caps').innerHTML=CAPS.map((c,i)=>`<button style="background:${c}" data-c="${c}" class="${i?'':'on'}" aria-label="գույն"></button>`).join('');
document.querySelectorAll('#caps button').forEach(b=>b.onclick=()=>{capSel=b.dataset.c;document.querySelectorAll('#caps button').forEach(x=>x.classList.toggle('on',x===b));});
$('#tip').textContent=pick(TXT.tips);
const saved=load();if(saved){$('#bCont').style.display='';$('#bStart').textContent='▶ Նոր խաղ';}
$('#bStart').onclick=()=>{if(!window.R3||!R3.ready)return;try{localStorage.removeItem(SAVEK);}catch(e){}W.slots.forEach(s=>s.built=s.pre);const g=newGame($('#nickIn').value.trim(),capSel);start(g);intro(()=>{toast('🎯 Գնա Աշոտ ձյաձյայի մոտ՝ հետևելով դեղին կետագծին');});};
$('#bCont').onclick=()=>{if(window.R3&&R3.ready)start(saved);};
function start(g){G=g;PID=Math.max(1,...G.inv.map(p=>p.id+1));G.pm={x:G.p.x,y:G.p.y};G.van.a=G.van.a||0;G.p.a=Math.PI/2;$('#title').style.display='none';$('#hud').classList.add('on');running=true;
  if(G.p.inVan)$('#tRadio').classList.remove('hide');if(G.co.unlocked)$('#tTerm').classList.remove('hide');qKey='';trayKey='';hud();updQuest(true);
  chat('SYSTEM',`Բարի գալուստ Երևան, ${G.nick}! 🎉`,1);setTimeout(()=>chat('Gugo_2007','բարև նորեկ 👋 Աշոտ ձյաձյան պահեստի մոտ ա'),3000);}
window.DBG={tp:(x,y)=>{G.p.x=x;G.p.y=y;if(G.p.inVan){G.van.x=x;G.van.y=y;}gps.t=0;},G:()=>G,W,setQ,company,NPC,questTarget,findAct:()=>ACT,talk,takeParcels,openTerminal,checkDir,cycleCam,toggleVan,policeStop};
