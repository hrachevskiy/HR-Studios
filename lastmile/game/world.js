/* ======================================================================
   WORLD v3 — procedural Yerevan, high-quality 2D (chunked, retina-sharp)
   ====================================================================== */
'use strict';
const TS=32, MW=125, MH=98, CH=16*TS;
const T={G:0,R:1,S:2,W:3,B:4,P:5,Y:6};
const VR=[8,21,34,47,60,73,86,99,112], HR=[6,19,32,45,58,71,84];
const W={tiles:new Uint8Array(MW*MH),solid:new Uint8Array(MW*MH),buildings:[],trees:[],decor:[],homes:[],slots:[],pudos:[],places:{},blocks:[],paths:[]};
const ti=(x,y)=>y*MW+x;
const tget=(x,y)=>x<0||y<0||x>=MW||y>=MH?T.W:W.tiles[ti(x,y)];
function seeded(s){return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
const R=seeded(20261102);const pickR=a=>a[(R()*a.length)|0];
function hash(x,y,s=0){let h=(x*374761393+y*668265263+s*1442695041)|0;h=(h^(h>>>13))*1274126177|0;return ((h^(h>>>16))>>>0)/4294967296;}

const WALLS=['#e8a08c','#dd8f7b','#efb49c','#e6a58a','#f2cfae','#d79a86','#ecc0a0','#e9b8b0','#f0d9bf','#cf8f7e'];
const ROOFS=['#cdbfae','#d8cbb9','#c4b5a3','#b9aa98','#d5c6b0'];
const PITCH=['#b84a3a','#5b8c5a','#9a5a3a','#4f6f8f','#c0563f'];
// district names by block column/row (i,j) — rough real Yerevan geography: Hrazdan gorge to the west, centre in the middle
const BX=i=>VR[i]+2, BY=j=>j<0?0:HR[j]+2;
function zoneOfBlock(i,j){if(i>=2&&i<=6&&j>=0&&j<=5)return 'Կենտրոն';if(i<=1&&j<=2)return 'Աջափնյակ';if(i<=1)return 'Մալաթիա-Սեբաստիա';if(j<=0&&i<=4)return 'Արաբկիր';if(j<=0)return 'Քանաքեռ-Զեյթուն';if(i>=7&&j<=3)return 'Նոր Նորք';if(i>=7)return 'Էրեբունի';if(j>=6&&i<=4)return 'Շենգավիթ';return 'Էրեբունի';}
function blockAt(tx,ty){let i=-1,j=-1;VR.forEach((x,k)=>{if(tx>=x)i=k;});HR.forEach((y,k)=>{if(ty>=y)j=k;});return [Math.max(0,i),j];}
const zoneAt=(tx,ty)=>{if(tx<VR[0])return 'Հրազդանի կիրճ';const [i,j]=blockAt(tx,ty);return zoneOfBlock(i,j);};
function setT(x,y,t){if(x>=0&&y>=0&&x<MW&&y<MH)W.tiles[ti(x,y)]=t;}
function addBuilding(b){b.floors=b.floors||(2+((R()*3)|0));b.wall=b.wall||pickR(WALLS);b.roofC=b.roofC||pickR(ROOFS);b.pitched=b.pitched!=null?b.pitched:false;b.pitchC=pickR(PITCH);
  b.props=[];for(let k=0;k<6;k++)b.props.push(R());b.win=R();b.balc=R()<.5;
  W.buildings.push(b);for(let y=b.y;y<b.y+b.h;y++)for(let x=b.x;x<b.x+b.w;x++)W.solid[ti(x,y)]=1;
  const dy=b.doorN?b.y-1:(b.y+b.h);b.door={x:(b.x+b.w/2)*TS,y:b.doorN?(b.y*TS-12):((b.y+b.h)*TS+12)};return b;}
function addTree(x,y,r,k){W.trees.push({x,y,r,k:k||(R()<.33?'apricot':R()<.5?'tree':'poplar'),s:R()});}

function buildWorld(){
  W.tiles.fill(T.G);
  // Hrazdan river in its gorge (west)
  for(let y=0;y<MH;y++){const wob=Math.round(Math.sin(y/7)*0.9);for(let x=0;x<=2+wob;x++){setT(x,y,T.W);W.solid[ti(x,y)]=1;}}
  VR.forEach(x=>{for(let y=0;y<MH;y++){setT(x,y,T.R);setT(x+1,y,T.R);}});
  HR.forEach(y=>{for(let x=0;x<MW;x++){if(tget(x,y)===T.W){setT(x,y,T.B);setT(x,y+1,T.B);W.solid[ti(x,y)]=0;W.solid[ti(x,y+1)]=0;}else{setT(x,y,T.R);setT(x,y+1,T.R);}}});
  const xs=VR.map(x=>x+2),xe=[...VR.slice(1).map(x=>x-1),MW-1],ys=[0,...HR.map(y=>y+2)],ye=[...HR.map(y=>y-1),MH-1];
  for(let j=0;j<ys.length;j++)for(let i=0;i<xs.length;i++){const b={i,j:j-1,x0:xs[i],y0:ys[j],x1:xe[i],y1:ye[j]};b.zone=zoneOfBlock(i,j-1);W.blocks.push(b);
    for(let y=b.y0;y<=b.y1;y++)for(let x=b.x0;x<=b.x1;x++){const edge=x===b.x0||x===b.x1||y===b.y0||y===b.y1;setT(x,y,edge?T.S:T.Y);}}
  // gorge edge: wild apricots and poplars
  for(let y=0;y<MH;y++)for(let x=4;x<VR[0];x++)if(tget(x,y)===T.G&&!HR.some(h=>y>=h-1&&y<=h+2)&&R()<.22)addTree((x+.5)*TS,(y+.5)*TS,R()*6+13);
  const blk=(i,j)=>W.blocks.find(b=>b.i===i&&b.j===j);
  const plaza=(b,x0,y0,x1,y1)=>{for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++)setT(x,y,T.P);};
  const used=new Set();const mark=(i,j)=>used.add(i+','+j);
  // ---------- HUB «Մղոն Էքսպրես» (Malatia, near the gorge)
  {const b=blk(1,4);mark(1,4);addBuilding({x:b.x0+2,y:b.y0+1,w:7,h:4,kind:'hub',floors:2,wall:'#9aa7b6',roofC:'#c9d1db',label:'ՄՂՈՆ ԷՔՍՊՐԵՍ'});plaza(b,b.x0+1,b.y0+6,b.x1,b.y1);
   W.places.hub={x:(b.x0+5.5)*TS,y:(b.y0+5.7)*TS,name:'Պահեստ «Մղոն Էքսպրես»'};W.places.van={x:(b.x0+8.6)*TS,y:(b.y0+8)*TS};W.places.niva={x:(b.x0+3)*TS,y:(b.y0+8.4)*TS};
   W.decor.push({k:'pallets',x:(b.x0+2)*TS,y:(b.y0+6.4)*TS},{k:'pallets',x:(b.x0+8.4)*TS,y:(b.y0+6.4)*TS});}
  // ---------- Yerevan Mall
  {const b=blk(1,5);mark(1,5);addBuilding({x:b.x0+1,y:b.y0+1,w:9,h:6,kind:'mall',floors:3,wall:'#9fb4cf',roofC:'#c9d1db',label:'ԵՐԵՎԱՆ ՄՈԼ'});plaza(b,b.x0+1,b.y0+7,b.x1-1,b.y1-1);W.places.mall={x:(b.x0+5.5)*TS,y:(b.y0+8.2)*TS,name:'Երևան Մոլ'};}
  // ---------- Polytechnic (ՀԱՊՀ), Teryan
  {const b=blk(6,1);mark(6,1);addBuilding({x:b.x0+1,y:b.y0+1,w:9,h:5,kind:'uni',floors:4,wall:'#e9c9a0',roofC:'#cdbfae',label:'ՀԱՊՀ · ՊՈԼԻՏԵԽՆԻԿ'});plaza(b,b.x0+1,b.y0+6,b.x1-1,b.y0+8);
   W.places.uni={x:(b.x0+5.5)*TS,y:(b.y0+7)*TS,name:'ՀԱՊՀ'};for(let k=0;k<4;k++)addTree((b.x0+2+k*2.4)*TS,(b.y0+9.4)*TS,13,'tree');}
  // ---------- Cascade (north end of Tamanyan)
  {const b=blk(4,0);mark(4,0);plaza(b,b.x0+1,b.y0+1,b.x1-1,b.y1-1);W.decor.push({k:'cascade',x:(b.x0+3)*TS,y:(b.y0+1)*TS,w:(b.x1-b.x0-5)*TS,h:(b.y1-b.y0-1)*TS});
   for(let y=b.y0+1;y<=b.y1-1;y+=2){addTree((b.x0+1.5)*TS,(y+.5)*TS,12,'poplar');addTree((b.x1-.6)*TS,(y+.5)*TS,12,'poplar');}W.places.cascade={x:(b.x0+5.5)*TS,y:(b.y1-0.1)*TS,name:'Կասկադ'};}
  // ---------- Tamanyan sculpture garden
  {const b=blk(4,1);mark(4,1);plaza(b,b.x0+4,b.y0+1,b.x0+6,b.y1-1);for(let y=b.y0+1;y<=b.y1-1;y++){if(y%2)continue;addTree((b.x0+2)*TS,(y+.5)*TS,14,'tree');addTree((b.x1-1)*TS,(y+.5)*TS,14,'tree');}
   W.decor.push({k:'sculpt',x:(b.x0+5.5)*TS,y:(b.y0+3)*TS,v:0},{k:'sculpt',x:(b.x0+5.5)*TS,y:(b.y0+6.5)*TS,v:1},{k:'sculpt',x:(b.x0+5.5)*TS,y:(b.y0+9.5)*TS,v:2});W.places.tamanyan={x:(b.x0+5.5)*TS,y:(b.y0+5)*TS,name:'Թամանյան'};}
  // ---------- Opera (Freedom square)
  {const b=blk(4,2);mark(4,2);plaza(b,b.x0+1,b.y0+1,b.x1-1,b.y1-1);addBuilding({x:b.x0+3,y:b.y0+3,w:5,h:5,kind:'opera',floors:3,wall:'#e8b493',roofC:'#cdbfae',label:''});
   W.places.opera={x:(b.x0+5.5)*TS,y:(b.y1-0.6)*TS,name:'Օպերա'};[[1.5,1.5],[9.5,1.5],[1.5,9.5],[9.5,9.5]].forEach(([a,c])=>addTree((b.x0+a)*TS,(b.y0+c)*TS,15,'tree'));}
  // ---------- Swan lake (next to the Opera)
  {const b=blk(5,2);mark(5,2);for(let y=b.y0+3;y<=b.y0+6;y++)for(let x=b.x0+3;x<=b.x0+7;x++){setT(x,y,T.W);W.solid[ti(x,y)]=1;}
   W.decor.push({k:'swans',x:(b.x0+5.5)*TS,y:(b.y0+5)*TS});[[1.4,1.4],[9.4,1.6],[1.6,8.6],[5,8.8],[9.2,4.2],[1.3,5]].forEach(([a,c])=>addTree((b.x0+a)*TS,(b.y0+c)*TS,R()*4+13));
   W.places.samo={x:(b.x0+8.8)*TS,y:(b.y0+8.1)*TS,name:'Կարապի լիճ'};W.decor.push({k:'grill',x:(b.x0+9.6)*TS,y:(b.y0+7.6)*TS});}
  // ---------- Northern Avenue (pedestrian, cafés)
  {const b=blk(5,3);mark(5,3);plaza(b,b.x0+4,b.y0,b.x0+6,b.y1);for(let y=b.y0+1;y<=b.y1-1;y+=3){W.decor.push({k:'cafe',x:(b.x0+5.5)*TS,y:(y+.5)*TS});}
   addBuilding({x:b.x0+1,y:b.y0+1,w:3,h:9,kind:'home',floors:9,style:'modern'});addBuilding({x:b.x0+7,y:b.y0+1,w:3,h:9,kind:'home',floors:10,style:'modern'});W.places.northave={x:(b.x0+5.5)*TS,y:(b.y0+5)*TS,name:'Հյուսիսային պողոտա'};}
  // ---------- Republic Square
  {const b=blk(4,4);mark(4,4);plaza(b,b.x0,b.y0,b.x1,b.y1);W.decor.push({k:'square',x:(b.x0+5.5)*TS,y:(b.y0+6)*TS});
   addBuilding({x:b.x0+1,y:b.y0,w:9,h:2,kind:'gov',floors:3,wall:'#e8a87c',roofC:'#d9c3a8',label:''});W.places.square={x:(b.x0+5.5)*TS,y:(b.y0+8)*TS,name:'Հանրապետության հրապարակ'};}
  // ---------- Vernissage (weekend art & carpet market)
  {const b=blk(5,4);mark(5,4);plaza(b,b.x0+1,b.y0+1,b.x1-1,b.y1-1);for(let r=0;r<3;r++)for(let k=0;k<4;k++)W.decor.push({k:'vstall',x:(b.x0+2+k*2.3)*TS,y:(b.y0+2.5+r*3)*TS,v:(r*4+k)%6});W.places.vernissage={x:(b.x0+5.5)*TS,y:(b.y1-.4)*TS,name:'Վերնիսաժ'};}
  // ---------- GUM market on Tigran Mets + pick-up point «Անուշ»
  {const b=blk(3,3);mark(3,3);addBuilding({x:b.x0+1,y:b.y0+1,w:9,h:3,kind:'market',floors:1,wall:'#e9b27a',roofC:'#d0c2ad',label:'ԳՈՒՄ ՇՈՒԿԱ'});plaza(b,b.x0+1,b.y0+5,b.x1-1,b.y0+7);
   for(let k=0;k<4;k++)W.decor.push({k:'stall',x:(b.x0+1.7+k*2.3)*TS,y:(b.y0+5.9)*TS,c:['#e2574c','#f2b33d','#4fa860','#e870a8'][k]});W.places.market={x:(b.x0+5)*TS,y:(b.y0+7.4)*TS,name:'Գում շուկա'};
   addBuilding({x:b.x0+1,y:b.y1-2,w:4,h:2,kind:'home',style:'tuff',floors:3});addBuilding({x:b.x0+6,y:b.y1-2,w:4,h:2,kind:'pudo',floors:1,wall:'#7fc6e6',label:'ԱՆՈՒՇ · ՍՏԱՑՄԱՆ ԿԵՏ'});}
  // ---------- Kyabab Hayko (Abovyan side)
  {const b=blk(4,3);mark(4,3);addBuilding({x:b.x0+1,y:b.y0+1,w:4,h:3,kind:'kyabab',floors:1,wall:'#e8925e',label:'ՔՅԱԲԱԲ ՀԱՅԿՈ'});W.places.kyabab={x:(b.x0+3)*TS,y:(b.y0+4.7)*TS,name:'Քյաբաբ Հայկո'};
   addBuilding({x:b.x0+6,y:b.y0+1,w:4,h:3,kind:'home',style:'tuff',floors:5});addBuilding({x:b.x0+1,y:b.y0+6,w:4,h:4,kind:'home',style:'tuff',floors:6});addBuilding({x:b.x0+6,y:b.y0+6,w:4,h:4,kind:'home',style:'tuff',floors:5});}
  // ---------- Old Kond: small houses, Zhora's yard with nardi
  {const b=blk(2,2);mark(2,2);[[1,1,3,3],[5,1,3,2],[8,1,2,3],[1,5,3,3],[1,8,2,2]].forEach(([x,y,w,h])=>addBuilding({x:b.x0+x,y:b.y0+y,w,h,kind:'home',style:'old',floors:1+((R()*2)|0),pitched:true}));
   W.decor.push({k:'nardi',x:(b.x0+7.5)*TS,y:(b.y0+7)*TS});W.places.zhora={x:(b.x0+7.5)*TS,y:(b.y0+8.3)*TS,name:'Ժորայի բակ (Կոնդ)'};addTree((b.x0+9.2)*TS,(b.y0+6)*TS,17,'apricot');addTree((b.x0+5)*TS,(b.y0+5.5)*TS,16,'apricot');}
  // ---------- Ring park (Օղակաձև այգի) — green belt around the centre
  [[2,1],[2,3],[3,5],[4,5],[5,5],[6,3],[6,2],[3,1]].forEach(([i,j])=>{const b=blk(i,j);if(!b||used.has(i+','+j))return;mark(i,j);b.park=1;
    const cx=Math.floor((b.x0+b.x1)/2),cy=Math.floor((b.y0+b.y1)/2);for(let x=b.x0+1;x<b.x1;x++)setT(x,cy,T.P);for(let y=b.y0+1;y<b.y1;y++)setT(cx,y,T.P);
    for(let y=b.y0+1;y<b.y1;y++)for(let x=b.x0+1;x<b.x1;x++){if(Math.abs(x-cx)<=1||Math.abs(y-cy)<=1)continue;if(R()<.3)addTree((x+.5)*TS,(y+.5)*TS,R()*5+13,R()<.3?'poplar':'tree');}
    W.decor.push({k:'fountain',x:(cx+.5)*TS,y:(cy+.5)*TS});[[-2.5,1.1],[2.5,1.1],[1.1,-2.5],[1.1,2.5]].forEach(([a,c])=>W.decor.push({k:'bench',x:(cx+.5+a)*TS,y:(cy+.5+c)*TS}));
    W.decor.push({k:'oldmen',x:(cx-2.4)*TS,y:(cy+2.4)*TS});W.decor.push({k:'pulpulak',x:(cx+2)*TS,y:(cy-1.6)*TS});});
  // ---------- residential: centre = tuff perimeter blocks with courtyards; outskirts = Soviet panel blocks
  W.blocks.forEach(b=>{if(used.has(b.i+','+b.j))return;const h=b.y1-b.y0-1;const centre=b.zone==='Կենտրոն';
    if(h<6){for(let x=b.x0+1;x+3<b.x1;x+=4){if(R()<.85)addBuilding({x,y:b.y0+1,w:3,h:3,kind:'home',style:centre?'tuff':'panel',floors:centre?4+((R()*2)|0):5});else addTree((x+1.5)*TS,(b.y0+2.2)*TS,14,'apricot');}return;}
    if(centre||R()<.45){// perimeter block: two buildings north, two south, courtyard (hayat) inside
      const fl=()=>centre?4+((R()*3)|0):3+((R()*3)|0);const st=centre?'tuff':(R()<.5?'tuff':'old5');
      addBuilding({x:b.x0+1,y:b.y0+1,w:4,h:3,kind:'home',style:st,floors:fl(),doorS:1});addBuilding({x:b.x0+6,y:b.y0+1,w:4,h:3,kind:'home',style:st,floors:fl()});
      addBuilding({x:b.x0+1,y:b.y1-3,w:4,h:3,kind:'home',style:st,floors:fl()});addBuilding({x:b.x0+6,y:b.y1-3,w:4,h:3,kind:'home',style:st,floors:fl()});
      const cy=b.y0+5;W.decor.push({k:'hayat',x:(b.x0+1)*TS,y:(b.y0+4)*TS,w:9*TS,h:3*TS});addTree((b.x0+2.5)*TS,(cy+.5)*TS,15,R()<.5?'apricot':'tree');addTree((b.x0+8.5)*TS,(cy+.3)*TS,14,'tree');
      W.decor.push({k:'laundry',x:(b.x0+3)*TS,y:(b.y0+4)*TS,y2:(b.y1-3)*TS});if(R()<.6)W.decor.push({k:'garage',x:(b.x0+6.6)*TS,y:(cy+.6)*TS});return;}
    // Soviet microdistrict: long 9-storey panel block + playground
    addBuilding({x:b.x0+1,y:b.y0+1,w:9,h:3,kind:'home',style:'panel',floors:9+((R()*4)|0)});W.decor.push({k:'playground',x:(b.x0+5.5)*TS,y:(b.y0+7)*TS});
    for(let k=0;k<4;k++)addTree((b.x0+1.6+k*2.6)*TS,(b.y1-1.4)*TS,R()*4+13);if(R()<.5)addBuilding({x:b.x0+7,y:b.y0+6,w:3,h:3,kind:'home',style:'panel',floors:5});});
  W.buildings.filter(b=>b.kind==='home').forEach(b=>{b.zone=zoneAt(Math.floor(b.x+b.w/2),Math.floor(b.y+b.h/2));b.owner=pickR(TXT.names);W.homes.push(b);if(R()<.14)b.balcony=1;});
  // street trees (chinar) along sidewalks + kiosks + pulpulaks + stepping stones to doors
  W.blocks.forEach(b=>{if(b.park)return;for(let x=b.x0+2;x<b.x1-1;x+=3){if(!W.solid[ti(x,b.y1)]&&R()<.75)W.trees.push({x:(x+.5)*TS,y:(b.y1+.62)*TS,r:12+R()*3,k:'street',s:R()});if(!W.solid[ti(x,b.y0)]&&R()<.5)W.trees.push({x:(x+.5)*TS,y:(b.y0+.38)*TS,r:12+R()*3,k:'street',s:R()});}
    if(b.zone==='Կենտրոն'&&R()<.55)W.decor.push({k:'kiosk',x:(b.x1-.5)*TS,y:(b.y0+3.5)*TS,v:(R()*8)|0});if(R()<.3)W.decor.push({k:'pulpulak',x:(b.x0+.5)*TS,y:(b.y0+2.5)*TS});});
  W.homes.forEach(b=>{const x=Math.floor(b.x+b.w/2);for(let y=b.y+b.h;y<MH;y++){const t=tget(x,y);if(t!==T.Y)break;W.paths.push({x:(x+.5)*TS,y:(y+.5)*TS});}});
  // parcel-locker sites: 2 already working, 9 to build (numbers match the coursework model: 40 → 67 lockers)
  const SLOTN=['Մալաթիա · պահեստ','Հանրապետության հր.','Աջափնյակ','Կոմիտաս','Կասկադի մոտ','Նոր Նորք','Էրեբունի','Օղակաձև այգի','Շենգավիթ','Սեբաստիա','Արաբկիր'];
  const slotBlocks=[[1,4,'pre'],[4,4,'pre'],[0,1],[2,0],[6,0],[7,2],[8,4],[6,5],[3,6],[0,6],[5,1]];
  slotBlocks.forEach(([i,j,pre])=>{const b=blk(i,j);if(!b)return;let x=(b.x1-.5)*TS,y=(b.y0+1.6)*TS;if(i===1&&j===4){x=(b.x0+6.5)*TS;y=(b.y1-1)*TS;}if(i===4&&j===4){x=(b.x0+9)*TS;y=(b.y1-1)*TS;}
    if(W.solid[ti(Math.floor(x/TS),Math.floor(y/TS))]){x=(b.x1-.5)*TS;y=(b.y1-.5)*TS;}
    const pop=W.homes.filter(h=>h.zone===zoneAt(Math.floor(x/TS),Math.floor(y/TS))).length;W.slots.push({x,y,zone:SLOTN[W.slots.length]||zoneAt(Math.floor(x/TS),Math.floor(y/TS)),built:!!pre,pre:!!pre,pop});});
  const pb=W.buildings.find(b=>b.kind==='pudo');W.pudos.push({x:pb.door.x,y:pb.door.y,name:'Ստացման կետ «Անուշ»'},{x:W.places.mall.x+70,y:W.places.mall.y-4,name:'Ստացման կետ · Մոլ'});
  for(let k=0;k<160;k++){const b=pickR(W.blocks);const x=(b.x0+.6+R()*(b.x1-b.x0-.2))*TS,y=(b.y1+.35)*TS;if(!W.solid[ti(Math.floor(x/TS),Math.floor(y/TS))])W.decor.push({k:R()<.5?'lamp':R()<.6?'bench':'bin',x,y});}
  for(let k=0;k<44;k++){const b=pickR(W.blocks.filter(b=>!used.has(b.i+','+b.j)));const side=R()<.5;W.decor.push({k:'parked',x:side?(b.x0-.55)*TS:(b.x1+1.55)*TS,y:(b.y0+1.5+R()*(b.y1-b.y0-2))*TS,c:pickR(['#d94b4b','#3f7fd1','#e9e9ee','#2b2b33','#7fbf5a','#e8b13c','#8a8f99'])});}
  W.nodes=[];VR.forEach(x=>HR.forEach(y=>W.nodes.push({x:(x+1)*TS,y:(y+1)*TS})));
}
const isSolidPx=(px,py)=>{const x=Math.floor(px/TS),y=Math.floor(py/TS);if(x<0||y<0||x>=MW||y>=MH)return true;return W.solid[ti(x,y)]===1;};
const isRoadT=(x,y)=>{const t=tget(x,y);return t===T.R||t===T.B||t===T.P;};
const isRoadPx=(px,py)=>isRoadT(Math.floor(px/TS),Math.floor(py/TS));

/* ---------------- PATTERNS (textures) ---------------- */
const PAT={};
function mkPattern(size,fn){const c=document.createElement('canvas');c.width=c.height=size;fn(c.getContext('2d'),size);return c;}
function initPatterns(){const r=seeded(99);
  PAT.grass=mkPattern(128,(g,s)=>{g.fillStyle='#8cc96a';g.fillRect(0,0,s,s);for(let i=0;i<900;i++){const x=r()*s,y=r()*s;g.fillStyle=r()<.5?'rgba(70,140,60,.35)':'rgba(190,230,140,.35)';g.fillRect(x,y,1.2,2.6);}
    for(let i=0;i<40;i++){g.fillStyle='rgba(60,120,50,.18)';g.beginPath();g.arc(r()*s,r()*s,4+r()*6,0,7);g.fill();}});
  PAT.asph=mkPattern(128,(g,s)=>{g.fillStyle='#454b57';g.fillRect(0,0,s,s);for(let i=0;i<1400;i++){g.fillStyle=r()<.5?'rgba(255,255,255,.06)':'rgba(0,0,0,.12)';g.fillRect(r()*s,r()*s,1.4,1.4);}
    for(let i=0;i<5;i++){g.strokeStyle='rgba(20,22,28,.25)';g.lineWidth=1;g.beginPath();let x=r()*s,y=r()*s;g.moveTo(x,y);for(let k=0;k<4;k++){x+=r()*20-10;y+=r()*20-10;g.lineTo(x,y);}g.stroke();}});
  PAT.pave=mkPattern(32,(g,s)=>{g.fillStyle='#e5dccd';g.fillRect(0,0,s,s);g.fillStyle='#ddd2c1';g.fillRect(0,0,16,16);g.fillRect(16,16,16,16);g.strokeStyle='rgba(150,130,110,.35)';g.lineWidth=1;g.strokeRect(.5,.5,15,15);g.strokeRect(16.5,.5,15,15);g.strokeRect(.5,16.5,15,15);g.strokeRect(16.5,16.5,15,15);});
  PAT.plaza=mkPattern(64,(g,s)=>{g.fillStyle='#efe2cc';g.fillRect(0,0,s,s);for(let y=0;y<4;y++)for(let x=0;x<4;x++){g.fillStyle=`rgba(${200+r()*30|0},${180+r()*25|0},${150+r()*25|0},.35)`;g.fillRect(x*16+1,y*16+1,14,14);}g.strokeStyle='rgba(170,140,110,.35)';for(let k=0;k<=4;k++){g.beginPath();g.moveTo(k*16,0);g.lineTo(k*16,s);g.moveTo(0,k*16);g.lineTo(s,k*16);g.stroke();}});
  PAT.yard=mkPattern(128,(g,s)=>{g.drawImage(PAT.grass,0,0);g.fillStyle='rgba(205,180,130,.28)';for(let i=0;i<14;i++){g.beginPath();g.ellipse(r()*s,r()*s,10+r()*16,6+r()*10,r()*3,0,7);g.fill();}});
  PAT.water=mkPattern(128,(g,s)=>{const gr=g.createLinearGradient(0,0,s,s);gr.addColorStop(0,'#46b3e6');gr.addColorStop(1,'#3aa3d8');g.fillStyle=gr;g.fillRect(0,0,s,s);g.strokeStyle='rgba(255,255,255,.35)';g.lineWidth=1.5;for(let i=0;i<14;i++){const x=r()*s,y=r()*s;g.beginPath();g.arc(x,y,6+r()*5,Math.PI*1.15,Math.PI*1.85);g.stroke();}});
  PAT.wood=mkPattern(32,(g,s)=>{g.fillStyle='#a8774f';g.fillRect(0,0,s,s);g.fillStyle='#93653f';for(let k=0;k<4;k++)g.fillRect(k*8,0,1.5,s);});
}

/* ---------------- CHUNK RENDERER ---------------- */
const CHUNKS=new Map();
function chunkCanvas(cx,cy,sc){const key=cx+','+cy+','+sc;let c=CHUNKS.get(key);if(c){CHUNKS.delete(key);CHUNKS.set(key,c);return c;}
  c=document.createElement('canvas');c.width=c.height=CH*sc;const g=c.getContext('2d');g.scale(sc,sc);g.translate(-cx*CH,-cy*CH);drawRegion(g,cx*CH,cy*CH,CH,CH);
  CHUNKS.set(key,c);while(CHUNKS.size>(window.CHUNK_MAX||20)){CHUNKS.delete(CHUNKS.keys().next().value);}return c;}
function drawRegion(g,X,Y,Wd,Hd){
  const tx0=Math.max(0,Math.floor(X/TS)-1),ty0=Math.max(0,Math.floor(Y/TS)-1),tx1=Math.min(MW-1,Math.floor((X+Wd)/TS)+1),ty1=Math.min(MH-1,Math.floor((Y+Hd)/TS)+1);
  const fillT=(t)=>t===T.G?PAT.grass:t===T.Y?PAT.yard:t===T.R?PAT.asph:t===T.S?PAT.pave:t===T.P?PAT.plaza:t===T.W?PAT.water:PAT.wood;
  const pats={};[T.G,T.Y,T.R,T.S,T.P,T.W,T.B].forEach(t=>{pats[t]=g.createPattern(fillT(t),'repeat');});
  [T.G,T.Y,T.R,T.S,T.P,T.W,T.B].forEach(tt=>{g.fillStyle=pats[tt];g.beginPath();for(let y=ty0;y<=ty1;y++)for(let x=tx0;x<=tx1;x++)if(tget(x,y)===tt)g.rect(x*TS,y*TS,TS+.6,TS+.6);g.fill();});
  for(let y=ty0;y<=ty1;y++)for(let x=tx0;x<=tx1;x++){const t=tget(x,y);
    if(t===T.G||t===T.Y){if(hash(x,y,3)<.08){g.fillStyle=['#ffe27a','#ff9cc9','#ffffff','#c9a5ff'][(hash(x,y,4)*4)|0];for(let k=0;k<3;k++){g.beginPath();g.arc(x*TS+hash(x,y,5+k)*TS,y*TS+hash(x,y,9+k)*TS,2,0,7);g.fill();}}}
    if(t===T.W){[[0,-1],[0,1],[-1,0],[1,0]].forEach(([dx,dy])=>{const n=tget(x+dx,y+dy);if(n!==T.W&&n!==T.B){g.fillStyle='rgba(255,255,255,.35)';if(dx===1)g.fillRect(x*TS+TS-4,y*TS,4,TS);if(dx===-1)g.fillRect(x*TS,y*TS,4,TS);if(dy===1)g.fillRect(x*TS,y*TS+TS-4,TS,4);if(dy===-1)g.fillRect(x*TS,y*TS,TS,4);}});}
    if(t===T.S){[[0,-1],[0,1],[-1,0],[1,0]].forEach(([dx,dy])=>{if(tget(x+dx,y+dy)===T.R){g.fillStyle='#f6f2ea';if(dx===1)g.fillRect(x*TS+TS-4,y*TS,4,TS);if(dx===-1)g.fillRect(x*TS,y*TS,4,TS);if(dy===1)g.fillRect(x*TS,y*TS+TS-4,TS,4);if(dy===-1)g.fillRect(x*TS,y*TS,TS,4);
      g.fillStyle='rgba(0,0,0,.22)';if(dx===1)g.fillRect(x*TS+TS,y*TS,3,TS);if(dx===-1)g.fillRect(x*TS-3,y*TS,3,TS);if(dy===1)g.fillRect(x*TS,y*TS+TS,TS,3);if(dy===-1)g.fillRect(x*TS,y*TS-3,TS,3);}});}
    if(t===T.B){g.fillStyle='#7d5a3c';if(tget(x,y-1)!==T.B)g.fillRect(x*TS,y*TS,TS,4);if(tget(x,y+1)!==T.B)g.fillRect(x*TS,y*TS+TS-4,TS,4);}}
  // road markings
  g.save();g.beginPath();g.rect(X-2,Y-2,Wd+4,Hd+4);g.clip();
  g.strokeStyle='rgba(255,214,90,.9)';g.lineWidth=2.2;g.setLineDash([14,12]);
  VR.forEach(x=>{g.beginPath();g.moveTo((x+1)*TS,0);g.lineTo((x+1)*TS,MH*TS);g.stroke();});HR.forEach(y=>{g.beginPath();g.moveTo(3*TS,(y+1)*TS);g.lineTo(MW*TS,(y+1)*TS);g.stroke();});g.setLineDash([]);
  VR.forEach(x=>HR.forEach(y=>{const px=x*TS,py=y*TS;if(px>X+Wd+64||px<X-128||py>Y+Hd+64||py<Y-128)return;g.fillStyle=pats[T.R];g.fillRect(px,py,2*TS,2*TS);
    g.fillStyle='rgba(255,255,255,.88)';for(let k=0;k<6;k++){g.fillRect(px+3+k*10.5,py-12,6,10);g.fillRect(px+3+k*10.5,py+2*TS+2,6,10);g.fillRect(px-12,py+3+k*10.5,10,6);g.fillRect(px+2*TS+2,py+3+k*10.5,10,6);}
    g.fillStyle='#3a3f4a';g.beginPath();g.arc(px+TS*1.5,py+TS*.5,5,0,7);g.fill();g.strokeStyle='#2c3038';g.lineWidth=1;g.stroke();}));
  g.restore();
  const inR=(x,y,m)=>x>X-m&&x<X+Wd+m&&y>Y-m&&y<Y+Hd+m;
  W.paths.forEach(p=>{if(inR(p.x,p.y,20)){g.fillStyle='#d9ccb6';g.strokeStyle='rgba(120,100,80,.35)';g.lineWidth=1;g.beginPath();g.ellipse(p.x-5,p.y-4,6,4,0,0,7);g.fill();g.stroke();g.beginPath();g.ellipse(p.x+5,p.y+5,6,4,0,0,7);g.fill();g.stroke();}});
  W.decor.forEach(d=>{if(inR(d.x,d.y,(d.w||0)+200))drawDecor(g,d);});
  // building shadows (soft, cast to bottom-right)
  W.buildings.forEach(b=>{const x=b.x*TS,y=b.y*TS,w=b.w*TS,h=b.h*TS;if(!inR(x+w/2,y+h/2,w+h+40))return;const sh=10+b.floors*4;
    const gr=g.createLinearGradient(x+w,y,x+w+sh,y);gr.addColorStop(0,'rgba(30,25,45,.32)');gr.addColorStop(1,'rgba(30,25,45,0)');g.fillStyle=gr;g.beginPath();g.moveTo(x+w,y+8);g.lineTo(x+w+sh,y+8+sh*.6);g.lineTo(x+w+sh,y+h+sh*.6);g.lineTo(x+w,y+h);g.fill();
    const gr2=g.createLinearGradient(0,y+h,0,y+h+12);gr2.addColorStop(0,'rgba(30,25,45,.30)');gr2.addColorStop(1,'rgba(30,25,45,0)');g.fillStyle=gr2;g.fillRect(x+4,y+h,w+sh-4,12);});
  W.buildings.forEach(b=>{if(inR((b.x+b.w/2)*TS,(b.y+b.h/2)*TS,(b.w+b.h)*TS))drawBuilding(g,b);});
  W.trees.forEach(t=>{if(inR(t.x,t.y,t.r+30))drawTree(g,t);});
}
function rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
const roundRect=rr;
function shade(hex,k){const n=parseInt(hex.slice(1),16);const f=v=>Math.max(0,Math.min(255,Math.round(v*k)));return `rgb(${f((n>>16)&255)},${f((n>>8)&255)},${f(n&255)})`;}
const OUT='rgba(52,38,60,.75)';
function drawBuilding(g,b){
  const x=b.x*TS,y=b.y*TS,w=b.w*TS,h=b.h*TS;const wallH=Math.min(h*.62,14+b.floors*13),roofH=h-wallH,wy=y+roofH;
  // facade
  const fg=g.createLinearGradient(0,wy,0,y+h);fg.addColorStop(0,shade(b.wall,1.02));fg.addColorStop(1,shade(b.wall,.86));g.fillStyle=fg;g.fillRect(x,wy,w,wallH);
  if(b.kind==='hub'){g.strokeStyle='rgba(0,0,0,.12)';g.lineWidth=1;for(let k=x+4;k<x+w;k+=5){g.beginPath();g.moveTo(k,wy);g.lineTo(k,y+h);g.stroke();}}
  else if(b.kind!=='mall'){g.strokeStyle='rgba(120,60,50,.12)';g.lineWidth=1;for(let k=wy+6;k<y+h;k+=7){g.beginPath();g.moveTo(x,k);g.lineTo(x+w,k);g.stroke();}}
  g.fillStyle='rgba(0,0,0,.10)';g.fillRect(x,y+h-9,w,9);
  // windows
  if(b.kind==='mall'){const gl=g.createLinearGradient(x,wy,x+w,y+h);gl.addColorStop(0,'#bfe6ff');gl.addColorStop(.5,'#8cc8ee');gl.addColorStop(1,'#d8f1ff');g.fillStyle=gl;g.fillRect(x+6,wy+5,w-12,wallH-18);g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=1;for(let k=x+6;k<x+w-6;k+=18){g.beginPath();g.moveTo(k,wy+5);g.lineTo(k,y+h-13);g.stroke();}}
  else{const fl=Math.max(1,Math.floor((wallH-10)/13)),cols=Math.max(1,Math.floor((w-8)/22));
    for(let f=0;f<fl;f++)for(let c=0;c<cols;c++){const ww=12,wh=8,wx=x+6+c*((w-12)/cols)+((w-12)/cols-ww)/2,wyy=wy+5+f*13;if(f===fl-1&&Math.abs(wx+ww/2-(x+w/2))<14&&b.kind!=='uni')continue;
      g.fillStyle='#f6efe4';g.fillRect(wx-1.5,wyy-1.5,ww+3,wh+3);const gl=g.createLinearGradient(wx,wyy,wx+ww,wyy+wh);const lit=hash(b.x+c,b.y+f,7)<.25;gl.addColorStop(0,lit?'#ffe8a3':'#a9d8f5');gl.addColorStop(1,lit?'#ffd36b':'#6fb3e0');g.fillStyle=gl;g.fillRect(wx,wyy,ww,wh);
      g.fillStyle='rgba(255,255,255,.55)';g.fillRect(wx+1,wyy+1,3,wh-2);g.fillStyle='rgba(60,40,40,.25)';g.fillRect(wx-2,wyy+wh+1.5,ww+4,1.6);
      if(b.balc&&f<fl-1&&c%2===0&&b.kind==='home'){g.fillStyle='rgba(255,255,255,.75)';g.fillRect(wx-3,wyy+wh+1,ww+6,2);g.strokeStyle='rgba(80,60,60,.55)';g.lineWidth=.8;for(let k=0;k<5;k++){g.beginPath();g.moveTo(wx-2+k*4,wyy+wh+1);g.lineTo(wx-2+k*4,wyy+wh+5);g.stroke();}
        g.fillStyle='#4fa860';g.beginPath();g.arc(wx+2,wyy+wh,2,0,7);g.arc(wx+ww-2,wyy+wh,2,0,7);g.fill();g.fillStyle='#e8577b';g.beginPath();g.arc(wx+2,wyy+wh-1.5,1,0,7);g.fill();}}
    if(b.kind==='uni'){g.fillStyle='rgba(255,255,255,.85)';for(let k=0;k<6;k++)g.fillRect(x+w/2-50+k*20,y+h-26,5,20);}}
  // door
  if(b.kind!=='gov'){const dw=b.kind==='hub'?54:b.kind==='mall'?36:15,dh=b.kind==='hub'?24:16;
    if(b.kind==='hub'){g.fillStyle='#6d7684';g.fillRect(x+w/2-dw/2,y+h-dh,dw,dh);g.strokeStyle='rgba(255,255,255,.3)';g.lineWidth=1;for(let k=1;k<6;k++){g.beginPath();g.moveTo(x+w/2-dw/2,y+h-dh+k*4);g.lineTo(x+w/2+dw/2,y+h-dh+k*4);g.stroke();}
      g.fillStyle='#4a535f';g.fillRect(x+12,y+h-dh,dw-20,dh);g.strokeStyle='rgba(255,255,255,.25)';for(let k=1;k<6;k++){g.beginPath();g.moveTo(x+12,y+h-dh+k*4);g.lineTo(x+dw-8,y+h-dh+k*4);g.stroke();}}
    else{const dg=g.createLinearGradient(0,y+h-dh,0,y+h);dg.addColorStop(0,'#8a5a36');dg.addColorStop(1,'#6a4226');g.fillStyle=b.kind==='mall'?'#9fd6f5':dg;rr(g,x+w/2-dw/2,y+h-dh,dw,dh,3);g.fill();g.strokeStyle=OUT;g.lineWidth=1.2;g.stroke();
      if(b.kind==='home'){g.fillStyle='#ffd36b';g.beginPath();g.arc(x+w/2+4,y+h-8,1.3,0,7);g.fill();}
      g.fillStyle='rgba(255,255,255,.55)';g.fillRect(x+w/2-dw/2-3,y+h-1,dw+6,3);}
    if(b.kind==='kyabab'||b.kind==='market'||b.kind==='pudo'){const aw=w-10;for(let k=0;k<Math.floor(aw/10);k++){g.fillStyle=k%2?'#fff':(b.kind==='pudo'?'#2f86c8':'#d9483b');g.beginPath();g.moveTo(x+5+k*10,wy-2);g.lineTo(x+15+k*10,wy-2);g.lineTo(x+15+k*10,wy+8);g.quadraticCurveTo(x+10+k*10,wy+11,x+5+k*10,wy+8);g.fill();}}}
  if(b.kind==='gov'){for(let k=0;k<7;k++){g.fillStyle='#c98a5e';rr(g,x+12+k*((w-24)/7),wy+6,14,wallH-6,7);g.fill();g.fillStyle='#7a4b32';rr(g,x+15+k*((w-24)/7),wy+10,8,wallH-10,4);g.fill();}}
  // roof
  if(b.pitched){const mid=y+roofH/2;g.fillStyle=shade(b.pitchC,1.08);g.beginPath();g.moveTo(x-3,y+roofH);g.lineTo(x-3,mid+2);g.lineTo(x+w+3,mid+2);g.lineTo(x+w+3,y+roofH);g.closePath();g.fill();
    g.fillStyle=shade(b.pitchC,.85);g.beginPath();g.moveTo(x-3,mid+2);g.lineTo(x-3,y-2);g.lineTo(x+w+3,y-2);g.lineTo(x+w+3,mid+2);g.fill();
    g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=1;for(let k=x+4;k<x+w;k+=6){g.beginPath();g.moveTo(k,y-2);g.lineTo(k,y+roofH);g.stroke();}
    g.strokeStyle='rgba(255,255,255,.4)';g.lineWidth=2;g.beginPath();g.moveTo(x-3,mid+2);g.lineTo(x+w+3,mid+2);g.stroke();g.strokeStyle=OUT;g.lineWidth=1.5;g.strokeRect(x-3,y-2,w+6,roofH+2);}
  else{const rg=g.createLinearGradient(x,y,x,y+roofH);rg.addColorStop(0,shade(b.roofC,1.06));rg.addColorStop(1,shade(b.roofC,.94));g.fillStyle=rg;g.fillRect(x-2,y-2,w+4,roofH+2);
    g.fillStyle=shade(b.wall,1.05);g.fillRect(x-2,y-2,w+4,4);g.fillRect(x-2,y-2,4,roofH+2);g.fillRect(x+w-2,y-2,4,roofH+2);g.fillStyle=shade(b.wall,.8);g.fillRect(x-2,y+roofH-2,w+4,3);
    g.fillStyle='rgba(0,0,0,.08)';g.fillRect(x+2,y+2,w-4,4);g.strokeStyle=OUT;g.lineWidth=1.5;g.strokeRect(x-2,y-2,w+4,roofH+2);
    const P=b.props;if(b.kind==='home'||b.kind==='uni'){
      if(P[0]<.75){const tx=x+12+P[1]*(w-30),ty=y+8;g.fillStyle='#4a7fb8';g.fillRect(tx-2,ty+2,22,10);g.fillStyle='#8fc2ee';g.fillRect(tx,ty+3,18,4);g.fillStyle='#e9eef2';g.beginPath();g.ellipse(tx+9,ty+1,10,3.5,0,0,7);g.fill();g.strokeStyle=OUT;g.lineWidth=1;g.stroke();}
      if(P[2]<.65){const tx=x+w-16,ty=y+roofH-16;const cg=g.createLinearGradient(tx-7,0,tx+7,0);cg.addColorStop(0,'#c9d3dc');cg.addColorStop(.5,'#fff');cg.addColorStop(1,'#a9b4bf');g.fillStyle=cg;g.beginPath();g.ellipse(tx,ty,7,7,0,0,7);g.fill();g.strokeStyle=OUT;g.lineWidth=1;g.stroke();}
      if(P[3]<.45){const tx=x+10,ty=y+roofH-12;g.fillStyle='#f4f4f4';g.beginPath();g.arc(tx,ty,5,0,7);g.fill();g.strokeStyle=OUT;g.lineWidth=1;g.stroke();g.beginPath();g.moveTo(tx,ty);g.lineTo(tx+4,ty-4);g.stroke();}
      if(P[4]<.4&&w>80){g.strokeStyle='#777';g.lineWidth=.8;const ly=y+roofH*.55;g.beginPath();g.moveTo(x+14,ly);g.lineTo(x+w-24,ly);g.stroke();const cols=['#e2574c','#5fb7e8','#f2c94c','#fff','#7fcf6a','#c58cf0'];for(let k=0;k<6;k++){g.fillStyle=cols[(k+((P[5]*6)|0))%6];g.fillRect(x+18+k*((w-46)/6),ly,7,8);}}
      if(P[5]<.5){g.fillStyle='#b9c0c8';g.fillRect(x+w*.45,y+6,12,8);g.strokeStyle=OUT;g.lineWidth=1;g.strokeRect(x+w*.45,y+6,12,8);}}
    if(b.kind==='hub'){g.fillStyle='rgba(255,255,255,.35)';for(let k=0;k<4;k++)g.fillRect(x+12+k*((w-24)/4),y+10,(w-24)/4-8,roofH-22);}
    if(b.kind==='mall'){g.fillStyle='#8fb3d6';for(let k=0;k<3;k++)for(let j=0;j<2;j++){g.fillRect(x+20+k*((w-40)/3),y+14+j*30,(w-40)/3-14,18);}}}
  // outline facade
  g.strokeStyle=OUT;g.lineWidth=1.5;g.strokeRect(x,wy,w,wallH);
  if(b.label){const fs=b.kind==='pudo'?9.5:12;g.font=`800 ${fs}px "Noto Sans Armenian",system-ui,sans-serif`;g.textAlign='center';const tw=g.measureText(b.label).width+18,ty=b.kind==='hub'||b.kind==='mall'||b.kind==='uni'?y+roofH/2:wy-12;
    const sg=g.createLinearGradient(0,ty-11,0,ty+11);const cc=b.kind==='hub'?['#ffb347','#ff8a3d']:b.kind==='kyabab'?['#e8573d','#c03a2a']:b.kind==='pudo'?['#3b9ad6','#2577b3']:b.kind==='market'?['#4fa860','#3a8a4b']:b.kind==='mall'?['#7d6bd6','#5f4fb8']:['#3a4a6b','#2a3550'];
    sg.addColorStop(0,cc[0]);sg.addColorStop(1,cc[1]);g.fillStyle='rgba(0,0,0,.25)';rr(g,x+w/2-tw/2+2,ty-9,tw,22,7);g.fill();g.fillStyle=sg;rr(g,x+w/2-tw/2,ty-11,tw,22,7);g.fill();g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=1.2;g.stroke();
    g.fillStyle='#fff';g.fillText(b.label,x+w/2,ty+4.5);}
}
function drawTree(g,t){const {x,y,r}=t;g.fillStyle='rgba(30,40,30,.25)';g.beginPath();g.ellipse(x+6,y+r*.55,r*1.05,r*.45,0,0,7);g.fill();
  g.fillStyle='#7a5234';g.fillRect(x-2.5,y-2,5,r*.6);
  if(t.k==='poplar'){const gr=g.createLinearGradient(x-r,0,x+r,0);gr.addColorStop(0,'#3e8d45');gr.addColorStop(1,'#2c6e35');g.fillStyle=gr;g.beginPath();g.ellipse(x,y-r*.9,r*.6,r*1.5,0,0,7);g.fill();g.strokeStyle='rgba(30,60,30,.6)';g.lineWidth=1.2;g.stroke();g.fillStyle='rgba(255,255,255,.18)';g.beginPath();g.ellipse(x-r*.2,y-r*1.4,r*.2,r*.6,0,0,7);g.fill();return;}
  const base=t.k==='apricot'?['#5aa94a','#3f8a3a','#7cc35f']:['#4a9e4c','#337d3c','#6fbe62'];
  [[-.45,.05,.62],[.45,.08,.6],[0,-.35,.72],[0,.15,.7]].forEach(([dx,dy,s],i)=>{const cx=x+dx*r,cy=y-6+dy*r,rr2=r*s;const gr=g.createRadialGradient(cx-rr2*.35,cy-rr2*.4,rr2*.1,cx,cy,rr2);gr.addColorStop(0,base[2]);gr.addColorStop(.6,base[0]);gr.addColorStop(1,base[1]);g.fillStyle=gr;g.beginPath();g.arc(cx,cy,rr2,0,7);g.fill();});
  g.strokeStyle='rgba(30,60,30,.45)';g.lineWidth=1.1;g.beginPath();g.arc(x,y-6-r*.1,r*.98,Math.PI*.9,Math.PI*2.1);g.stroke();
  if(t.k==='apricot'){for(let k=0;k<7;k++){const a=k*.9+t.s*6,d=r*(.35+hash(k,7,t.x|0)*.4);g.fillStyle='#ff9d2e';g.beginPath();g.arc(x+Math.cos(a)*d,y-8+Math.sin(a)*d*.8,2.4,0,7);g.fill();g.fillStyle='rgba(255,255,255,.6)';g.fillRect(x+Math.cos(a)*d-.8,y-9+Math.sin(a)*d*.8,1,1);}}}
function drawDecor(g,d){
  if(d.k==='cascade'){const gr=g.createLinearGradient(0,d.y,0,d.y+d.h);gr.addColorStop(0,'#f5ebdc');gr.addColorStop(1,'#e8d7bf');g.fillStyle=gr;g.fillRect(d.x,d.y,d.w,d.h);
    for(let k=0;k<d.h;k+=8){g.fillStyle=k%16?'rgba(150,120,90,.18)':'rgba(255,255,255,.5)';g.fillRect(d.x,d.y+k,d.w,2);}
    const fl=['#ff7aa8','#ffd25f','#b48cff','#ff6b6b'];for(let k=0;k<5;k++){const yy=d.y+12+k*(d.h-20)/5;g.fillStyle='#5aa94a';rr(g,d.x+8,yy,d.w-16,9,4);g.fill();for(let j=0;j<10;j++){g.fillStyle=fl[(j+k)%4];g.beginPath();g.arc(d.x+12+j*(d.w-24)/9,yy+4.5,2.2,0,7);g.fill();}}
    const cx=d.x+d.w/2,cy=d.y+d.h*.5;const wg=g.createRadialGradient(cx,cy,2,cx,cy,26);wg.addColorStop(0,'#bfefff');wg.addColorStop(1,'#4fb6e6');g.fillStyle='#d7c4a8';g.beginPath();g.ellipse(cx,cy,30,16,0,0,7);g.fill();g.fillStyle=wg;g.beginPath();g.ellipse(cx,cy,25,12,0,0,7);g.fill();}
  else if(d.k==='square'){g.fillStyle='rgba(200,150,110,.25)';g.beginPath();g.ellipse(d.x,d.y,150,100,0,0,7);g.fill();g.strokeStyle='rgba(170,120,80,.45)';g.lineWidth=5;g.stroke();
    g.fillStyle='#d6c1a3';g.beginPath();g.ellipse(d.x,d.y,64,36,0,0,7);g.fill();const wg=g.createRadialGradient(d.x,d.y,4,d.x,d.y,56);wg.addColorStop(0,'#c8f1ff');wg.addColorStop(1,'#44aee2');g.fillStyle=wg;g.beginPath();g.ellipse(d.x,d.y,57,30,0,0,7);g.fill();g.strokeStyle='rgba(255,255,255,.5)';g.lineWidth=2;g.beginPath();g.ellipse(d.x,d.y,40,20,0,0,7);g.stroke();}
  else if(d.k==='nardi'){g.fillStyle='rgba(0,0,0,.2)';g.fillRect(d.x-24,d.y-10,54,32);g.fillStyle='#7a4f2c';rr(g,d.x-27,d.y-15,54,30,4);g.fill();g.fillStyle='#e8c690';g.fillRect(d.x-23,d.y-11,46,22);g.fillStyle='#7a4f2c';g.fillRect(d.x-1,d.y-11,2,22);
    for(let k=0;k<6;k++){g.fillStyle=k%2?'#b5482f':'#3a5a8a';g.beginPath();g.moveTo(d.x-23+k*3.8,d.y-11);g.lineTo(d.x-21+k*3.8,d.y-3);g.lineTo(d.x-19+k*3.8,d.y-11);g.fill();}
    g.fillStyle='#fff';g.beginPath();g.arc(d.x+10,d.y+6,3,0,7);g.fill();g.fillStyle='#222';g.beginPath();g.arc(d.x-8,d.y+6,3,0,7);g.fill();
    g.fillStyle='#7a5234';[[-36,0],[36,0]].forEach(([a])=>{rr(g,d.x+a-7,d.y-6,14,14,3);g.fill();});}
  else if(d.k==='stall'){g.fillStyle='rgba(0,0,0,.2)';g.fillRect(d.x-25,d.y+2,54,18);g.fillStyle='#8a5a36';g.fillRect(d.x-26,d.y-2,52,20);g.fillStyle=['#5aa94a','#e2574c','#f2c94c','#ff9f43'][(hash(d.x|0,1)*4)|0];for(let k=0;k<8;k++){g.beginPath();g.arc(d.x-21+k*6,d.y+5+((k%2)*4),3.6,0,7);g.fill();}
    for(let k=0;k<4;k++){g.fillStyle=k%2?'#fff':d.c;g.fillRect(d.x-28+k*14,d.y-16,14,12);}g.strokeStyle=OUT;g.lineWidth=1;g.strokeRect(d.x-28,d.y-16,56,12);}
  else if(d.k==='grill'){g.fillStyle='#3a3a44';rr(g,d.x-22,d.y-6,44,12,3);g.fill();g.fillStyle='#ff6b2b';g.fillRect(d.x-18,d.y-3,36,6);g.strokeStyle='#ccc';g.lineWidth=1.5;for(let k=0;k<5;k++){g.beginPath();g.moveTo(d.x-24,d.y-4+k*2);g.lineTo(d.x+24,d.y-4+k*2);g.stroke();}}
  else if(d.k==='bench'){g.fillStyle='rgba(0,0,0,.18)';g.fillRect(d.x-13,d.y-1,28,8);g.fillStyle='#9b6b43';rr(g,d.x-14,d.y-5,28,9,2);g.fill();g.fillStyle='#b88356';g.fillRect(d.x-14,d.y-5,28,3);g.strokeStyle=OUT;g.lineWidth=1;g.strokeRect(d.x-14,d.y-5,28,9);}
  else if(d.k==='lamp'){g.fillStyle='rgba(0,0,0,.18)';g.beginPath();g.ellipse(d.x+5,d.y+3,7,3,0,0,7);g.fill();g.fillStyle='#454a55';g.beginPath();g.arc(d.x,d.y,4.5,0,7);g.fill();g.fillStyle='#fff6c4';g.beginPath();g.arc(d.x,d.y,2,0,7);g.fill();}
  else if(d.k==='bin'){g.fillStyle='#3f7f4f';rr(g,d.x-5,d.y-6,10,11,2);g.fill();g.strokeStyle=OUT;g.lineWidth=1;g.stroke();}
  else if(d.k==='parked'){drawCar(g,d.x,d.y,Math.PI/2,{kind:'car',color:d.c});}
  else if(d.k==='pallets'){for(let k=0;k<3;k++){g.fillStyle='#b58556';g.fillRect(d.x-16+k*11,d.y-8,10,16);g.fillStyle='#e0b070';g.fillRect(d.x-15+k*11,d.y-12,8,8);g.strokeStyle=OUT;g.lineWidth=1;g.strokeRect(d.x-15+k*11,d.y-12,8,8);}}
}
/* characters & vehicles (shared with game.js) */
function drawPerson(g,x,y,o){
  const s=o.s||1,dir=o.dir||0,t=o.t||0,ph=o.moving?t*11:0,walk=Math.sin(ph),bob=o.moving?Math.abs(Math.sin(ph))*1.4:0,dn=o.dance?Math.sin(t*10):0;
  g.save();g.translate(x,y);g.scale(s,s);
  g.fillStyle='rgba(25,20,40,.26)';g.beginPath();g.ellipse(0,1,10,4,0,0,7);g.fill();
  g.translate(0,-bob-(o.dance?Math.abs(dn)*3:0));g.rotate(dn*.1);
  const skin=o.skin||'#f1c39c',shirt=o.shirt||'#ff8a3d',pants=o.pants||'#3b4a6b';g.lineJoin='round';
  // legs + shoes
  [-1,1].forEach(k=>{const off=k*walk*2.6;g.fillStyle=pants;rr(g,k*4.2-2.6,-9+off*.2,5.2,8,2);g.fill();g.fillStyle='#2b2633';g.beginPath();g.ellipse(k*4.2,-1+off*.5,3.2,2.2,0,0,7);g.fill();});
  // torso
  const tg=g.createLinearGradient(-9,0,9,0);tg.addColorStop(0,shade(shirt,1.08));tg.addColorStop(1,shade(shirt,.82));g.fillStyle=tg;rr(g,-8.5,-21,17,14,6);g.fill();g.strokeStyle=OUT;g.lineWidth=1.2;g.stroke();
  if(o.apron){g.fillStyle='#fafafa';rr(g,-6,-17,12,11,3);g.fill();}
  if(o.vest){g.fillStyle='#ffd23d';g.fillRect(-8.5,-19,4,11);g.fillRect(4.5,-19,4,11);g.fillStyle='rgba(255,255,255,.8)';g.fillRect(-8.5,-12,17,1.6);}
  if(o.bag&&dir!==3){g.fillStyle='#d97a1f';g.fillRect(-7.5,-20,2.4,12);g.fillRect(5.1,-20,2.4,12);}
  // arms
  [-1,1].forEach(k=>{const sw=o.dance?-dn*k*7:-k*walk*2.5;g.fillStyle=shade(shirt,.9);rr(g,k*9.2-2.4,-19,4.8,9,2.4);g.fill();g.fillStyle=skin;g.beginPath();g.arc(k*9.5,-9.5+sw,2.6,0,7);g.fill();});
  if(o.bag&&dir===3){const bg=g.createLinearGradient(-8,0,8,0);bg.addColorStop(0,'#ffb347');bg.addColorStop(1,'#e88a2a');g.fillStyle=bg;rr(g,-7.5,-22,15,13,3);g.fill();g.strokeStyle=OUT;g.lineWidth=1;g.stroke();g.fillStyle='#fff';g.font='800 6px "Noto Sans Armenian",sans-serif';g.textAlign='center';g.fillText('Մ',0,-13.5);}
  // head
  const hy=-29;g.fillStyle=skin;g.beginPath();g.arc(0,hy,9.6,0,7);g.fill();g.strokeStyle=OUT;g.lineWidth=1.2;g.stroke();
  g.fillStyle='rgba(255,255,255,.18)';g.beginPath();g.arc(-3,hy-4,4,0,7);g.fill();
  if(o.hair&&o.hat!=='scarf'){g.fillStyle=o.hair;g.beginPath();g.arc(0,hy-1.5,9.8,Math.PI*1.02,Math.PI*1.98);g.lineTo(9,hy-2);g.fill();if(o.long){g.fillRect(-9.5,hy-2,4,12);g.fillRect(5.5,hy-2,4,12);}}
  if(dir!==3){const fx=dir===1?-2.6:dir===2?2.6:0;
    g.fillStyle='#fff';g.beginPath();g.ellipse(fx-3.4,hy+.8,1.9,2.3,0,0,7);g.ellipse(fx+3.4,hy+.8,1.9,2.3,0,0,7);g.fill();g.fillStyle='#2b2238';g.beginPath();g.arc(fx-3.2+(dir===1?-.5:dir===2?.5:0),hy+1.2,1.2,0,7);g.arc(fx+3.6+(dir===1?-.5:dir===2?.5:0),hy+1.2,1.2,0,7);g.fill();
    g.fillStyle='rgba(255,120,120,.35)';g.beginPath();g.arc(fx-5.8,hy+4,1.8,0,7);g.arc(fx+5.8,hy+4,1.8,0,7);g.fill();
    if(o.must){g.fillStyle='#3a2a26';g.beginPath();g.moveTo(fx-6.5,hy+5);g.quadraticCurveTo(fx-3,hy+2.6,fx,hy+4.6);g.quadraticCurveTo(fx+3,hy+2.6,fx+6.5,hy+5);g.quadraticCurveTo(fx+3,hy+7.5,fx,hy+5.8);g.quadraticCurveTo(fx-3,hy+7.5,fx-6.5,hy+5);g.fill();}
    else{g.strokeStyle='#7a3a32';g.lineWidth=1.1;g.beginPath();g.arc(fx,hy+4.2,2,.2*Math.PI,.8*Math.PI);g.stroke();}
    if(o.glasses){g.fillStyle='#1b1b22';rr(g,fx-7.2,hy-.6,5.6,3.6,1);g.fill();rr(g,fx+1.6,hy-.6,5.6,3.6,1);g.fill();g.fillRect(fx-1.6,hy+.2,3.2,1);}
    if(o.beard){g.fillStyle=o.beard;g.beginPath();g.arc(fx,hy+4,7,.05*Math.PI,.95*Math.PI);g.fill();}}
  g.strokeStyle=OUT;g.lineWidth=1.1;
  if(o.hat==='cap'){const cc=o.capC||'#ff6b3d';const cg=g.createLinearGradient(0,hy-12,0,hy);cg.addColorStop(0,shade(cc,1.12));cg.addColorStop(1,shade(cc,.85));g.fillStyle=cg;g.beginPath();g.arc(0,hy-2.5,9.8,Math.PI,0);g.fill();g.stroke();
    if(dir!==3){const bx=dir===1?-9:dir===2?9:0;g.fillStyle=shade(cc,.75);g.beginPath();g.ellipse(bx*.6,hy-2.6,dir===0?9:7,2.8,0,0,7);g.fill();g.stroke();}
    g.fillStyle='#fff';g.font='900 6px "Noto Sans Armenian",sans-serif';g.textAlign='center';g.fillText('Մ',0,hy-5.5);}
  else if(o.hat==='flat'){g.fillStyle='#5b5b66';g.beginPath();g.ellipse(0,hy-6,11,5.5,0,0,7);g.fill();g.stroke();g.fillStyle='#4a4a54';g.beginPath();g.ellipse(dir===1?-5:dir===2?5:0,hy-3.5,7,2.6,0,0,7);g.fill();g.stroke();}
  else if(o.hat==='scarf'){const cc=o.capC||'#c8426a';g.fillStyle=cc;g.beginPath();g.arc(0,hy-.5,11,Math.PI*.92,Math.PI*2.08);g.lineTo(8,hy+9);g.lineTo(-8,hy+9);g.closePath();g.fill();g.stroke();
    g.fillStyle='rgba(255,255,255,.75)';for(let k=0;k<6;k++){g.beginPath();g.arc(-7+k*2.8,hy-6+Math.sin(k*1.7)*2,1,0,7);g.fill();}g.fillStyle=skin;g.beginPath();g.arc(0,hy+2,7,0,7);g.fill();
    if(dir!==3){g.fillStyle='#2b2238';g.beginPath();g.arc(-2.8,hy+1.5,1.1,0,7);g.arc(2.8,hy+1.5,1.1,0,7);g.fill();g.strokeStyle='#7a3a32';g.beginPath();g.arc(0,hy+4.6,1.8,.2*Math.PI,.8*Math.PI);g.stroke();}}
  else if(o.hat==='hood'){g.fillStyle=shade(shirt,.95);g.beginPath();g.arc(0,hy-1.5,11.2,Math.PI*.88,Math.PI*2.12);g.fill();g.stroke();}
  else if(o.hat==='chef'){g.fillStyle='#fff';g.beginPath();g.arc(-4,hy-11,4.6,0,7);g.arc(4,hy-11,4.6,0,7);g.arc(0,hy-14,5.4,0,7);g.fill();g.stroke();g.fillRect(-6.5,hy-9.5,13,4.5);}
  g.restore();}
function drawCar(g,x,y,ang,o){g.save();g.translate(x,y);g.rotate(ang);const L=o.kind==='marsh'?60:o.kind==='van'?52:o.kind==='niva'?40:46,Wd=o.kind==='marsh'?26:o.kind==='niva'?24:23;
  g.fillStyle='rgba(20,20,30,.28)';rr(g,-L/2+3,-Wd/2+4,L,Wd,8);g.fill();
  g.fillStyle='#1d1d24';[[-L/2+8,-Wd/2-1.5],[L/2-14,-Wd/2-1.5],[-L/2+8,Wd/2-2.5],[L/2-14,Wd/2-2.5]].forEach(([a,b])=>g.fillRect(a,b,7,4));
  const bg=g.createLinearGradient(0,-Wd/2,0,Wd/2);bg.addColorStop(0,shade(o.color,1.15));bg.addColorStop(.5,o.color);bg.addColorStop(1,shade(o.color,.72));g.fillStyle=bg;rr(g,-L/2,-Wd/2,L,Wd,o.kind==='niva'?4:8);g.fill();g.strokeStyle=OUT;g.lineWidth=1.3;g.stroke();
  if(o.kind==='van'||o.kind==='marsh'){g.fillStyle=shade(o.color,1.12);rr(g,-L/2+3,-Wd/2+3,L-16,Wd-6,4);g.fill();g.fillStyle='#2b3440';rr(g,L/2-13,-Wd/2+3,8,Wd-6,3);g.fill();g.fillStyle='rgba(160,220,255,.6)';g.fillRect(L/2-12,-Wd/2+4,2,Wd-8);}
  else{g.fillStyle='#2b3440';rr(g,L/2-17,-Wd/2+3,8,Wd-6,3);g.fill();rr(g,-L/2+5,-Wd/2+3,6,Wd-6,2);g.fill();const rg=g.createLinearGradient(0,-Wd/2,0,Wd/2);rg.addColorStop(0,shade(o.color,1.25));rg.addColorStop(1,shade(o.color,.9));g.fillStyle=rg;rr(g,-L/2+12,-Wd/2+3,L-30,Wd-6,4);g.fill();
    g.fillStyle='rgba(170,225,255,.55)';g.fillRect(L/2-16,-Wd/2+4,2,Wd-8);}
  g.fillStyle='#fff7c2';g.beginPath();g.arc(L/2-1.5,-Wd/2+4,2.2,0,7);g.arc(L/2-1.5,Wd/2-4,2.2,0,7);g.fill();g.fillStyle='#ff4b4b';g.fillRect(-L/2,-Wd/2+2,2,4);g.fillRect(-L/2,Wd/2-6,2,4);
  if(o.kind==='taxi'){g.fillStyle='#2b2238';rr(g,-6,-4,12,8,2);g.fill();g.fillStyle='#ffe066';g.font='800 5.5px sans-serif';g.textAlign='center';g.fillText('TAXI',0,2);}
  if(o.kind==='marsh'){g.save();g.rotate(-ang);g.fillStyle='#2b2238';g.font='900 12px sans-serif';g.textAlign='center';g.fillText('22',0,4.5);g.restore();}
  if(o.kind==='niva'){g.fillStyle='#3a3a3a';g.fillRect(-12,-Wd/2+2,14,Wd-4);g.fillStyle='#c9a36b';[[-8,-4],[-8,4],[0,0]].forEach(([a,b])=>{g.beginPath();g.ellipse(a,b,5,4.4,0,0,7);g.fill();g.strokeStyle=OUT;g.lineWidth=.8;g.stroke();});}
  if(o.kind==='van'){g.save();g.rotate(-ang);g.fillStyle='#ff7a1a';g.font='900 9px "Noto Sans Armenian",sans-serif';g.textAlign='center';g.fillText('ՄՂՈՆ',0,3.5);g.restore();}
  g.restore();}
function drawDog(g,x,y,t,moving){g.save();g.translate(x,y);const b=moving?Math.sin(t*14)*1.4:0;g.fillStyle='rgba(25,20,40,.25)';g.beginPath();g.ellipse(0,1,10,3.6,0,0,7);g.fill();
  g.strokeStyle=OUT;g.lineWidth=1.1;g.fillStyle='#c98a4b';g.beginPath();g.ellipse(0,-7-b,10,6,0,0,7);g.fill();g.stroke();g.fillStyle='#f3d9b6';g.beginPath();g.ellipse(2,-4-b,5,3,0,0,7);g.fill();
  g.fillStyle='#c98a4b';g.beginPath();g.arc(9,-12-b,5.5,0,7);g.fill();g.stroke();g.fillStyle='#7a4b2a';g.beginPath();g.ellipse(6.5,-16-b,2.4,4,-.4,0,7);g.fill();g.fillStyle='#2b2238';g.beginPath();g.arc(11,-13-b,1.1,0,7);g.arc(14,-11.5-b,1.4,0,7);g.fill();
  g.strokeStyle='#a8703a';g.lineWidth=2.6;g.beginPath();g.moveTo(-9,-8-b);g.lineTo(-14,-14-b+Math.sin(t*20)*3);g.stroke();g.restore();}
function renderMini(){const s=4,c=document.createElement('canvas');c.width=MW*s;c.height=MH*s;const g=c.getContext('2d');
  for(let y=0;y<MH;y++)for(let x=0;x<MW;x++){const t=tget(x,y);g.fillStyle=t===T.R?'#5d6472':t===T.W?'#4db4e6':t===T.G?'#8cc96a':t===T.Y?'#9fd17c':t===T.P?'#efe2cc':t===T.B?'#a8774f':'#e2d8c8';g.fillRect(x*s,y*s,s,s);}
  W.buildings.forEach(b=>{g.fillStyle=b.kind==='home'?shade(b.wall,.95):b.kind==='hub'?'#ffb347':b.kind==='mall'?'#9a8ae0':b.kind==='market'?'#5ab36a':b.kind==='uni'?'#6f86b8':b.kind==='kyabab'?'#e8573d':b.kind==='pudo'?'#3b9ad6':'#e8a87c';g.fillRect(b.x*s,b.y*s,b.w*s,b.h*s);});return c;}
