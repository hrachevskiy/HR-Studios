/* ======================================================================
   ՎԵՐՋԻՆ ՄՂՈՆ 3D — three.js renderer for the Yerevan world
   (game logic lives in game.js; this module only draws the world)
   ====================================================================== */
import * as THREE from 'three';
import {mergeGeometries} from './lib/BufferGeometryUtils.js';
import {GLTFLoader} from './lib/GLTFLoader.js';
import * as SU from './lib/SkeletonUtils.js';
import {EffectComposer} from './lib/postprocessing/EffectComposer.js';
import {RenderPass} from './lib/postprocessing/RenderPass.js';
import {UnrealBloomPass} from './lib/postprocessing/UnrealBloomPass.js';
import {ShaderPass} from './lib/postprocessing/ShaderPass.js';
import {OutputPass} from './lib/postprocessing/OutputPass.js';

const U=1/16;                       // 1 game px → world units (1 tile = 2 m)
const V3=THREE.Vector3;
const isMobile=matchMedia('(pointer:coarse)').matches||Math.min(innerWidth,innerHeight)<600;
const FONTS='"Noto Sans Armenian","Segoe UI",system-ui,sans-serif';
const rand=seeded(777);
function seeded(s){return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
const rp=a=>a[(rand()*a.length)|0];

/* ---------------------------------------------------------------- renderer */
const canvas=document.getElementById('cv');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(devicePixelRatio||1,isMobile?1.5:1.75));
renderer.setSize(innerWidth,innerHeight,false);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const MAXANISO=renderer.capabilities.getMaxAnisotropy();
const scene=new THREE.Scene();
const HORIZON=new THREE.Color('#e6d8c6');
scene.fog=new THREE.Fog(HORIZON,260,1100);
const camera=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,.1,2600);
addEventListener('resize',()=>{renderer.setSize(innerWidth,innerHeight,false);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();if(composer)composer.setSize(innerWidth,innerHeight);});
// cinematic post-processing on desktop: soft bloom on lights/sky + warm Yerevan grade + vignette
let composer=null;
try{if(!isMobile){composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,camera));composer.addPass(new UnrealBloomPass(new THREE.Vector2(innerWidth,innerHeight),.22,.5,.95));composer.addPass(new OutputPass());
  composer.addPass(new ShaderPass({uniforms:{tDiffuse:{value:null}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:'uniform sampler2D tDiffuse;varying vec2 vUv;void main(){vec4 c=texture2D(tDiffuse,vUv);vec3 col=c.rgb;col=mix(col,col*vec3(1.04,1.0,.95),.5);col=(col-.5)*1.08+.5;float l=dot(col,vec3(.299,.587,.114));col=mix(vec3(l),col,1.15);vec2 d=vUv-.5;float v=1.-dot(d,d)*.45;gl_FragColor=vec4(clamp(col*v,0.,1.),c.a);}'}));}}catch(e){console.warn('post-fx off',e);composer=null;}
// near-camera dither fade: anything between the camera and the courier dissolves instead of blocking the view
const NEARU={value:0};
const MAXANI=Math.min(isMobile?4:8,renderer.capabilities.getMaxAnisotropy());
function nearFade(m){if(!m||!m.isMeshStandardMaterial||m.userData.nf)return;m.userData.nf=1;if(m.map&&m.map.anisotropy<MAXANI){m.map.anisotropy=MAXANI;m.map.needsUpdate=true;}const prev=m.onBeforeCompile;
  m.onBeforeCompile=(sh,r)=>{if(prev)prev.call(m,sh,r);sh.uniforms.uNear=NEARU;sh.fragmentShader='uniform float uNear;\n'+sh.fragmentShader.replace('#include <clipping_planes_fragment>','#include <clipping_planes_fragment>\n if(uNear>0.){float cd=length(vViewPosition);if(cd<uNear){const float BY[16]=float[16](0.,8.,2.,10.,12.,4.,14.,6.,3.,11.,1.,9.,15.,7.,13.,5.);ivec2 bi=ivec2(mod(gl_FragCoord.xy,4.));float th=(BY[bi.x+bi.y*4]+.5)/16.;float k=cd/uNear;if(th>k*k)discard;}}');};
  const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):()=>'';m.customProgramCacheKey=()=>pk()+'|nf';m.needsUpdate=true;}
function patchNear(){scene.traverse(o=>{if(o.isMesh&&o.material){Array.isArray(o.material)?o.material.forEach(nearFade):nearFade(o.material);}});}
const draw=()=>{if(composer)composer.render();else renderer.render(scene,camera);};

/* ---------------------------------------------------------------- sky + light */
function skyMesh(){const g=new THREE.SphereGeometry(1800,32,16);const m=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,fog:false,
  uniforms:{top:{value:new THREE.Color('#1f63c4')},mid:{value:new THREE.Color('#6fb0ea')},hor:{value:HORIZON.clone()},sun:{value:new V3(-.62,.38,.68).normalize()}},
  vertexShader:'varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:`uniform vec3 top,mid,hor,sun;varying vec3 vP;void main(){float h=vP.y;vec3 c=mix(hor,mid,smoothstep(0.,.11,h));c=mix(c,top,smoothstep(.11,.6,h));
   float s=max(dot(vP,sun),0.);c+=vec3(1.,.78,.5)*pow(s,8.)*.35+vec3(1.,.9,.7)*pow(s,900.)*3.;c=mix(c,hor*.92,smoothstep(0.,-.12,h));gl_FragColor=vec4(c,1.);}`});
  const s=new THREE.Mesh(g,m);s.renderOrder=-10;return s;}
scene.add(skyMesh());
{const pm=new THREE.PMREMGenerator(renderer);const es=new THREE.Scene();es.add(skyMesh());const hemi=new THREE.HemisphereLight('#cfe6ff','#a58a6e',1);es.add(hemi);scene.environment=pm.fromScene(es,.02).texture;scene.environmentIntensity=.55;}
const hemi=new THREE.HemisphereLight('#d6e9ff','#b49376',1.25);scene.add(hemi);
const sun=new THREE.DirectionalLight('#ffe0b4',2.9);const SUNOFF=new V3(-62,78,58);
sun.castShadow=true;sun.shadow.mapSize.set(isMobile?1024:2048,isMobile?1024:2048);
Object.assign(sun.shadow.camera,{left:-48,right:48,top:48,bottom:-48,near:1,far:260});sun.shadow.bias=-.0004;sun.shadow.normalBias=.03;
scene.add(sun);scene.add(sun.target);

/* ---------------------------------------------------------------- canvas textures */
function cnv(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return [c,c.getContext('2d')];}
function tex(c,rep=true){const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=MAXANISO;if(rep){t.wrapS=t.wrapT=THREE.RepeatWrapping;}return t;}
function rr(g,x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
function noise(g,w,h,n,a,dark=true){for(let i=0;i<n;i++){g.fillStyle=(dark&&rand()<.6)?`rgba(70,40,30,${a*rand()})`:`rgba(255,250,240,${a*rand()})`;const s=rand()*2.6+.6;g.fillRect(rand()*w,rand()*h,s,s);}}
const BAY=3,FLOOR=3;   // world units per facade bay / floor; textures hold 4×4 bays
const SHOPS=[['ՄԹԵՐՔ 24/7','#2f6f3e'],['ԴԵՂԱՏՈՒՆ','#1f8a5c'],['ՍՐՃԱՐԱՆ','#6b3f25'],['ՀԱՑԱՏՈՒՆ','#b0662c'],['ԼԱՀՄԱՋՈ','#b23a2a'],['ՇԱՈՒՐՄԱ','#c2452f'],['ԾԱՂԻԿՆԵՐ','#b8457a'],['ՄՍԻ ԽԱՆՈՒԹ','#8e2a2a'],['ՈՍԿԵՐՉԱԿԱՆ','#8a6a1a'],['ԿՈՇԻԿԻ ՎԵՐԱՆՈՐՈԳՈՒՄ','#444a55'],['ԳՐԱԽԱՆՈՒԹ','#2f4f8a'],['ՉԻՐ ԵՎ ԸՆԿՈՒՅԶ','#7a4a1f'],['ԱՐԺՈՒՅԹԻ ՓՈԽԱՆԱԿՈՒՄ','#1f5f8a'],['ՎԱՐՍԱՎԻՐԱՆՈՑ','#5a3a7a'],['ԳԻՆԵՏՈՒՆ','#6e1f3a'],['ՔԱՂՑՐԵՂԵՆ','#c06a8a'],['ՀԵՌԱԽՈՍՆԵՐ','#2a2f3a'],['ԿՈՆՅԱԿ ԵՎ ԳԻՆԻ','#7a3a1a']];
function facadeTex(base,style,shopP=.4){const S=256,[c,g]=cnv(S*4,S*4);
  for(let by=0;by<4;by++)for(let bx=0;bx<4;bx++){const X=bx*S,Y=by*S,ground=by===3;
    g.fillStyle=base;g.fillRect(X,Y,S,S);
    if(style==='panel'){g.strokeStyle='rgba(60,60,70,.35)';g.lineWidth=3;g.strokeRect(X+1.5,Y+1.5,S-3,S-3);for(let i=0;i<700;i++){g.fillStyle=`rgba(0,0,0,${rand()*.07})`;g.fillRect(X+rand()*S,Y+rand()*S,2,2);}
      g.fillStyle='rgba(80,70,60,.12)';for(let k=0;k<3;k++)g.fillRect(X+rand()*S,Y,6+rand()*10,S);}
    else if(style==='old'){for(let i=0;i<1400;i++){g.fillStyle=rand()<.6?`rgba(90,60,40,${rand()*.18})`:`rgba(255,250,240,${rand()*.2})`;g.fillRect(X+rand()*S,Y+rand()*S,3,3);}
      g.strokeStyle='rgba(80,50,35,.35)';g.lineWidth=1.5;for(let k=0;k<5;k++){g.beginPath();let x=X+rand()*S,y=Y+rand()*S;g.moveTo(x,y);for(let j=0;j<5;j++){x+=rand()*16-8;y+=rand()*18;g.lineTo(x,y);}g.stroke();}
      if(rand()<.5){g.fillStyle='rgba(150,120,90,.25)';g.fillRect(X,Y+S*.6,S,S*.4);}}
    else if(style==='modern'){g.fillStyle=shadeHex(base,1.02);g.fillRect(X,Y,S,S);g.fillStyle='rgba(0,0,0,.08)';g.fillRect(X,Y,S,10);}
    else{for(let r=0;r<4;r++){const off=(r%2)*40;for(let k=-1;k<4;k++){const bw=80,bh=64;const sh=.87+rand()*.22;g.fillStyle=shadeHex(base,sh);g.fillRect(X+k*bw+off+2,Y+r*bh+2,bw-4,bh-4);}}
      for(let i=0;i<1000;i++){g.fillStyle=rand()<.65?`rgba(60,25,20,${rand()*.28})`:`rgba(255,240,230,${rand()*.25})`;const s=rand()*3+1;g.beginPath();g.arc(X+rand()*S,Y+rand()*S,s/2,0,7);g.fill();}}
    const lit=rand()<.16;
    if(ground&&rand()<shopP){ // shop front with an Armenian sign
      const [name,col]=rp(SHOPS);g.fillStyle='#2e2622';g.fillRect(X+16,Y+66,S-32,S-66);const gl=g.createLinearGradient(0,Y+80,0,Y+S);gl.addColorStop(0,lit?'#ffe3a8':'#a7d0e8');gl.addColorStop(1,lit?'#d8a050':'#3d6f93');g.fillStyle=gl;g.fillRect(X+24,Y+76,S-48,S-82);
      g.fillStyle='rgba(255,255,255,.18)';g.beginPath();g.moveTo(X+24,Y+76);g.lineTo(X+90,Y+76);g.lineTo(X+24,Y+180);g.fill();g.fillStyle='#2e2622';g.fillRect(X+S/2-3,Y+76,6,S-82);
      g.fillStyle=col;g.fillRect(X+8,Y+30,S-16,34);g.fillStyle='rgba(255,255,255,.12)';g.fillRect(X+8,Y+30,S-16,6);g.fillStyle='#fff';let fs=21;g.font=`800 ${fs}px ${FONTS}`;while(g.measureText(name).width>S-30&&fs>11){fs--;g.font=`800 ${fs}px ${FONTS}`;}g.textAlign='center';g.fillText(name,X+S/2,Y+54);continue;}
    if(style==='modern'){const gl=g.createLinearGradient(X,Y,X+S,Y+S);gl.addColorStop(0,'#cfe6f4');gl.addColorStop(.5,'#6d98b8');gl.addColorStop(1,'#a9c9de');g.fillStyle=gl;g.fillRect(X+18,Y+22,S-36,S-60);g.fillStyle='#55606a';g.fillRect(X+S/2-3,Y+22,6,S-60);g.fillRect(X+18,Y+100,S-36,5);
      if(lit){g.fillStyle='rgba(255,215,140,.55)';g.fillRect(X+22,Y+26,S/2-28,S-68);}continue;}
    const old=style==='old';const ww=old?92:112,wh=old?118:132,wx=X+(S-ww)/2,wy=Y+(old?60:44),arch=!old&&style!=='panel'&&(bx+by)%3===0;
    // recess & frame (arched windows are typical of Yerevan tuff buildings)
    g.fillStyle='rgba(40,25,20,.38)';g.fillRect(wx-9,wy-9,ww+18,wh+22);
    g.fillStyle=style==='panel'?'#ececea':old?'#6a4a32':rp(['#f4efe6','#5c3e2b','#efe9e0','#dcd3c4']);g.fillRect(wx-6,wy-6,ww+12,wh+12);
    if(arch){g.beginPath();g.ellipse(wx+ww/2,wy-4,ww/2+10,28,0,Math.PI,0);g.fillStyle=shadeHex(base,1.12);g.fill();g.strokeStyle='rgba(70,35,25,.45)';g.lineWidth=3;g.stroke();for(let k=0;k<7;k++){g.save();g.translate(wx+ww/2,wy-4);g.rotate(Math.PI+k*Math.PI/6);g.fillStyle='rgba(70,35,25,.3)';g.fillRect(ww/2-6,-2,16,4);g.restore();}}
    const gl=g.createLinearGradient(wx,wy,wx+ww,wy+wh);if(lit){gl.addColorStop(0,'#ffe7a8');gl.addColorStop(1,'#f0b860');}else{gl.addColorStop(0,'#b9e0f7');gl.addColorStop(.5,'#6fa7cf');gl.addColorStop(1,'#42739a');}
    g.fillStyle=gl;g.fillRect(wx,wy,ww,wh);g.fillStyle='rgba(255,255,255,.3)';g.beginPath();g.moveTo(wx,wy);g.lineTo(wx+40,wy);g.lineTo(wx,wy+64);g.fill();
    if(rand()<.55){g.fillStyle=rp(['rgba(240,230,210,.88)','rgba(200,120,120,.7)','rgba(230,220,250,.8)','rgba(250,250,245,.9)']);g.fillRect(wx,wy,26,wh);g.fillRect(wx+ww-26,wy,26,wh);}
    g.fillStyle=style==='panel'?'#ececea':old?'#6a4a32':'#efe7da';g.fillRect(wx+ww/2-3,wy,6,wh);g.fillRect(wx,wy+42,ww,6);
    if(old){g.fillStyle=rp(['#4f6f5a','#7a5232','#46607a']);g.fillRect(wx-30,wy-4,24,wh+8);g.fillRect(wx+ww+6,wy-4,24,wh+8);g.strokeStyle='rgba(0,0,0,.3)';for(let k=0;k<8;k++){g.beginPath();g.moveTo(wx-30,wy+k*16);g.lineTo(wx-6,wy+k*16);g.moveTo(wx+ww+6,wy+k*16);g.lineTo(wx+ww+30,wy+k*16);g.stroke();}}
    g.fillStyle='rgba(255,255,255,.7)';g.fillRect(wx-14,wy+wh+6,ww+28,10);g.fillStyle='rgba(0,0,0,.25)';g.fillRect(wx-14,wy+wh+16,ww+28,5);
    if(!ground&&!old&&style!=='panel'&&rand()<.22){ // open balcony with iron railing + flowers / laundry
      g.fillStyle='rgba(0,0,0,.3)';g.fillRect(X+16,Y+202,S-32,12);g.fillStyle='#d8d2c8';g.fillRect(X+14,Y+192,S-28,12);g.strokeStyle='#2d2a2a';g.lineWidth=4;g.strokeRect(X+16,Y+150,S-32,44);
      for(let k=0;k<11;k++){g.beginPath();g.moveTo(X+22+k*21,Y+152);g.lineTo(X+22+k*21,Y+192);g.stroke();}
      for(let k=0;k<5;k++){g.fillStyle=rp(['#e2574c','#ffd25f','#ff8fb8','#ffffff']);g.beginPath();g.arc(X+40+k*42,Y+146,9,0,7);g.fill();g.fillStyle='#4fa860';g.beginPath();g.arc(X+40+k*42,Y+156,8,0,7);g.fill();}}}
  return tex(c);}
function balconyTex(){const [c,g]=cnv(1024,256);const cols=[['#eef0ec','#8fbfe0'],['#c9b79c','#9cc2dc'],['#8fb6c9','#bcdcef'],['#d8d0c4','#8ab4d4']];
  cols.forEach(([fr,gl],v)=>{const X=v*256;g.fillStyle=fr;g.fillRect(X,0,256,256);g.fillStyle=shadeHex(fr,.86);g.fillRect(X,150,256,106);
    for(let i=0;i<300;i++){g.fillStyle=`rgba(0,0,0,${rand()*.06})`;g.fillRect(X+rand()*256,150+rand()*106,3,3);}
    for(let k=0;k<4;k++){const gx=X+10+k*60;const lit=rand()<.2;const gg=g.createLinearGradient(gx,0,gx+50,140);gg.addColorStop(0,lit?'#ffe3a0':gl);gg.addColorStop(1,lit?'#e8b060':shadeHex(gl,.7));g.fillStyle=gg;g.fillRect(gx+3,12,54,128);
      if(rand()<.5){g.fillStyle=rp(['rgba(255,255,255,.75)','rgba(230,190,190,.7)','rgba(240,235,200,.7)']);g.fillRect(gx+3,12,18,128);}g.fillStyle='rgba(255,255,255,.3)';g.fillRect(gx+5,14,6,124);}
    g.fillStyle=shadeHex(fr,.7);g.fillRect(X,140,256,10);g.fillRect(X,0,256,10);if(v===1){g.fillStyle='rgba(120,60,40,.35)';for(let k=0;k<6;k++)g.fillRect(X+10+k*42,160,30,80);}
    if(rand()<.6){g.fillStyle='#e9ebee';g.fillRect(X+170,175,60,40);g.strokeStyle='#9aa0a8';g.lineWidth=2;g.strokeRect(X+170,175,60,40);g.beginPath();g.arc(X+200,195,14,0,7);g.stroke();}});
  return tex(c,false);}
function shadeHex(hex,k){const n=parseInt(hex.slice(1),16);const f=v=>Math.max(0,Math.min(255,Math.round(v*k)));return `rgb(${f((n>>16)&255)},${f((n>>8)&255)},${f(n&255)})`;}
function roofTex(){const [c,g]=cnv(512,512);g.fillStyle='#b9b2a8';g.fillRect(0,0,512,512);for(let i=0;i<3000;i++){g.fillStyle=`rgba(${rand()<.5?40:255},${rand()<.5?40:255},${rand()<.5?40:255},${rand()*.06})`;g.fillRect(rand()*512,rand()*512,3,3);}
  for(let i=0;i<14;i++){g.fillStyle=`rgba(40,40,45,${.15+rand()*.25})`;g.beginPath();g.ellipse(rand()*512,rand()*512,20+rand()*60,10+rand()*40,rand()*3,0,7);g.fill();}
  g.strokeStyle='rgba(0,0,0,.12)';g.lineWidth=2;for(let k=0;k<=8;k++){g.beginPath();g.moveTo(k*64,0);g.lineTo(k*64,512);g.stroke();}return tex(c);}
function corrugTex(){const [c,g]=cnv(256,256);const gr=g.createLinearGradient(0,0,32,0);gr.addColorStop(0,'#aab6c4');gr.addColorStop(.5,'#d9e1ea');gr.addColorStop(1,'#99a6b5');g.fillStyle=gr;for(let k=0;k<8;k++){g.save();g.translate(k*32,0);g.fillRect(0,0,32,256);g.restore();}
  g.fillStyle='rgba(255,140,40,.9)';g.fillRect(0,200,256,22);return tex(c);}
function glassTex(){const [c,g]=cnv(256,256);const gr=g.createLinearGradient(0,0,256,256);gr.addColorStop(0,'#cdeaff');gr.addColorStop(.5,'#6aa9d6');gr.addColorStop(1,'#a8d4f2');g.fillStyle=gr;g.fillRect(0,0,256,256);g.strokeStyle='#e8f2fa';g.lineWidth=6;g.strokeRect(0,0,256,256);g.lineWidth=3;g.beginPath();g.moveTo(128,0);g.lineTo(128,256);g.moveTo(0,128);g.lineTo(256,128);g.stroke();
  g.fillStyle='rgba(255,255,255,.25)';g.beginPath();g.moveTo(0,0);g.lineTo(90,0);g.lineTo(0,140);g.fill();return tex(c);}
function arcadeTex(){const [c,g]=cnv(256,256);g.fillStyle='#e7a074';g.fillRect(0,0,256,256);for(let i=0;i<700;i++){g.fillStyle=`rgba(120,50,30,${rand()*.2})`;g.fillRect(rand()*256,rand()*256,3,3);}
  g.fillStyle='#7a3d26';g.beginPath();g.moveTo(40,256);g.lineTo(40,110);g.arc(128,110,88,Math.PI,0);g.lineTo(216,256);g.fill();g.fillStyle='#3a2018';g.beginPath();g.moveTo(58,256);g.lineTo(58,114);g.arc(128,114,70,Math.PI,0);g.lineTo(198,256);g.fill();
  g.strokeStyle='#f3c9a6';g.lineWidth=6;g.beginPath();g.arc(128,110,90,Math.PI,0);g.stroke();for(let k=0;k<9;k++){g.save();g.translate(128,110);g.rotate(Math.PI+k*Math.PI/8);g.fillStyle='#f0bf98';g.fillRect(84,-3,14,6);g.restore();}return tex(c);}
function signTex(text,bg1,bg2,w=1024,h=200,fs=110){const [c,g]=cnv(w,h);const gr=g.createLinearGradient(0,0,0,h);gr.addColorStop(0,bg1);gr.addColorStop(1,bg2);g.fillStyle=gr;rr(g,6,6,w-12,h-12,30);g.fill();g.lineWidth=10;g.strokeStyle='rgba(255,255,255,.85)';g.stroke();
  g.fillStyle='#fff';g.font=`900 ${fs}px ${FONTS}`;g.textAlign='center';g.textBaseline='middle';let f=fs;while(g.measureText(text).width>w-80&&f>20){f-=4;g.font=`900 ${f}px ${FONTS}`;}g.shadowColor='rgba(0,0,0,.35)';g.shadowBlur=10;g.fillText(text,w/2,h/2+6);return tex(c,false);}
function lockerTex(){const [c,g]=cnv(256,256);g.fillStyle='#1d9a5e';g.fillRect(0,0,256,256);g.fillStyle='#eafff3';g.fillRect(0,0,256,36);g.fillStyle='#14784a';g.font=`900 22px ${FONTS}`;g.textAlign='center';g.fillText('ՓՈՍՏԱՄԱՏ 24/7',128,26);
  for(let r=0;r<4;r++)for(let k=0;k<4;k++){if(k===1&&r<2)continue;const x=10+k*61,y=46+r*52;g.fillStyle='#c9f5dc';rr(g,x,y,55,46,6);g.fill();g.fillStyle='rgba(0,0,0,.25)';g.fillRect(x+44,y+18,5,10);}
  g.fillStyle='#152530';rr(g,72,46,56,98,6);g.fill();g.fillStyle='#5ad1ff';g.fillRect(80,54,40,32);g.fillStyle='#9ab';for(let k=0;k<9;k++)g.fillRect(82+(k%3)*13,94+((k/3)|0)*13,9,9);return tex(c,false);}
function dashTex(){const [c,g]=cnv(128,32);g.clearRect(0,0,128,32);g.fillStyle='rgba(20,24,43,.55)';g.beginPath();g.arc(64,16,14,0,7);g.fill();g.fillStyle='#ffd84d';g.beginPath();g.moveTo(48,6);g.lineTo(80,16);g.lineTo(48,26);g.lineTo(56,16);g.closePath();g.fill();return tex(c);}
function adTex(i){const ads=[['ՋԵՐՄՈՒԿ','Ամեն ինչ կանցնի 💧','#1f6fb2','#3fa0e0'],['ԶՈՔԱՆՉԻԴ ԶԱՆԳԻ՞Ր','Նա սպասում է 📞','#b8325a','#e2577f'],['ՎԵՐՋԻՆ ՄՂՈՆ','Մեկ կանգառ՝ շատ ծանրոց ▣','#e86b1a','#ffb347'],['ԼԱՀՄԱՋՈ 24/7','2 հատը՝ 1-ի գնով 🫓','#5a7d2a','#8bb04a'],['ԹԱՔՍԻ «ԱԽՊԵՐ»','Կտանենք, ուր ասես 🚕','#2b2b33','#4a4a55'],['ՆԻՎԱ','Ճանապարհ պետք չէ ⛰️','#3d6b2a','#62963f']];
  const a=ads[i%ads.length];const [c,g]=cnv(1024,400);const gr=g.createLinearGradient(0,0,1024,400);gr.addColorStop(0,a[2]);gr.addColorStop(1,a[3]);g.fillStyle=gr;g.fillRect(0,0,1024,400);
  g.fillStyle='rgba(255,255,255,.12)';for(let k=0;k<6;k++){g.beginPath();g.arc(900-k*30,60+k*20,120-k*12,0,7);g.fill();}g.fillStyle='#fff';g.textAlign='center';g.font=`900 104px ${FONTS}`;g.fillText(a[0],512,190);g.font=`700 56px ${FONTS}`;g.fillText(a[1],512,300);
  g.strokeStyle='#fff';g.lineWidth=12;g.strokeRect(6,6,1012,388);return tex(c,false);}
function streetTex(name){const [c,g]=cnv(512,128);g.fillStyle='#1d4f8f';rr(g,4,4,504,120,16);g.fill();g.strokeStyle='#fff';g.lineWidth=6;g.stroke();g.fillStyle='#fff';g.font=`800 50px ${FONTS}`;g.textAlign='center';g.textBaseline='middle';g.fillText(name,256,66);return tex(c,false);}

/* ---------------------------------------------------------------- vertex-colour geometry helpers */
const _m=new THREE.Matrix4(),_q=new THREE.Quaternion(),_e=new THREE.Euler(),_s=new V3(),_p=new V3();
function paint(geo,color){geo=geo.index?geo.toNonIndexed():geo;const n=geo.attributes.position.count,c=new THREE.Color(color),a=new Float32Array(n*3);for(let i=0;i<n;i++){a[i*3]=c.r;a[i*3+1]=c.g;a[i*3+2]=c.b;}geo.setAttribute('color',new THREE.BufferAttribute(a,3));if(!geo.attributes.uv)geo.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(n*2),2));return geo;}
function P(geo,color,x=0,y=0,z=0,rx=0,ry=0,rz=0,sx=1,sy=1,sz=1){geo.applyMatrix4(_m.compose(_p.set(x,y,z),_q.setFromEuler(_e.set(rx,ry,rz)),_s.set(sx,sy,sz)));return paint(geo,color);}
const box=(w,h,d)=>new THREE.BoxGeometry(w,h,d),sph=(r,a=9,b=7)=>new THREE.SphereGeometry(r,a,b),cyl=(r1,r2,h,s=10)=>new THREE.CylinderGeometry(r1,r2,h,s);
const MERGE=l=>mergeGeometries(l.filter(Boolean));
const VCM=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.78,metalness:0});
const CARM=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.32,metalness:.35});
const GLOWM=new THREE.MeshBasicMaterial({vertexColors:true,toneMapped:false});
function mesh(geo,mat=VCM,cast=true,recv=true){const m=new THREE.Mesh(geo,mat);m.castShadow=cast;m.receiveShadow=recv;return m;}

/* ---------------------------------------------------------------- CHARACTERS */
const geoCache=new Map();
function charParts(o){const k=JSON.stringify(o);if(geoCache.has(k))return geoCache.get(k);
  const skin=o.skin||'#f1c39c',shirt=o.shirt||'#ff8a3d',pants=o.pants||'#3b4a6b',hair=o.hair||'#2a1d1a',jk=o.jacket||null,top=jk||shirt;const B=[];
  // torso, pelvis, shoulders (realistic-ish proportions, ~1.8 m)
  B.push(P(cyl(.165,.15,.22,14),pants,0,.99,0,0,0,0,1,1,.72));B.push(P(box(.34,.05,.25),'#2a2420',0,1.09,0));
  B.push(P(new THREE.CapsuleGeometry(.19,.3,6,16),top,0,1.25,0,0,0,0,1,1,.64));B.push(P(sph(.215,16,12),top,0,1.36,0,0,0,0,1.06,.72,.66));
  if(o.belly)B.push(P(sph(.2,14,10),top,0,1.14,.07,0,0,0,1,.95,.9));
  [-1,1].forEach(s=>B.push(P(sph(.085,10,8),top,s*.215,1.43,0)));
  if(jk){B.push(P(box(.09,.42,.02),shirt,0,1.27,.135));B.push(P(box(.05,.36,.03),shadeC(jk,.8),.07,1.28,.13,0,0,.08));B.push(P(box(.05,.36,.03),shadeC(jk,.8),-.07,1.28,.13,0,0,-.08));}
  B.push(P(new THREE.TorusGeometry(.075,.022,6,14),shadeC(shirt,.9),0,1.5,0,Math.PI/2));
  if(o.vest){B.push(P(new THREE.CapsuleGeometry(.2,.26,4,14),'#ffd23d',0,1.26,0,0,0,0,1.02,.95,.68));B.push(P(box(.42,.04,.3),'#f4f4f4',0,1.16,0));B.push(P(box(.42,.04,.3),'#f4f4f4',0,1.3,0));}
  if(o.apron)B.push(P(box(.32,.48,.02),'#fafafa',0,1.1,.145));
  if(o.bag){B.push(P(box(.34,.38,.16),'#e8892a',0,1.27,-.21));B.push(P(box(.36,.06,.18),'#c96f1b',0,1.47,-.21));[-1,1].forEach(s=>B.push(P(box(.04,.44,.24),'#c96f1b',s*.15,1.3,-.06,.25)));B.push(P(box(.14,.08,.01),'#ffffff',0,1.3,-.295));}
  // head
  const hy=1.67;B.push(P(cyl(.055,.06,.12,8),skin,0,1.54,0));B.push(P(sph(.145,18,14),skin,0,hy,0,0,0,0,1,1.12,1.05));B.push(P(sph(.12,14,10),skin,0,hy-.07,.025,0,0,0,1,.85,1));
  [-1,1].forEach(s=>{B.push(P(sph(.035,8,6),shadeC(skin,.95),s*.145,hy,0,0,0,0,.6,1,1));B.push(P(sph(.027,8,6),'#ffffff',s*.052,hy+.03,.13,0,0,0,1,.8,.55));B.push(P(sph(.016,8,6),'#2b2238',s*.052,hy+.03,.146));B.push(P(box(.065,.014,.02),shadeC(hair,.9),s*.054,hy+.068,.142,0,0,-s*.1));});
  B.push(P(box(.042,.07,.06),shadeC(skin,.9),0,hy-.005,.155));B.push(P(box(.06,.012,.02),'#8a3a32',0,hy-.07,.142));
  if(o.must)B.push(P(box(.11,.028,.03),'#3a2a26',0,hy-.048,.152));
  if(o.beard)B.push(P(sph(.14,14,10),o.beard,0,hy-.08,.04,0,0,0,1,.82,.92));
  if(o.glasses){[-1,1].forEach(s=>B.push(P(box(.07,.045,.012),'#18181e',s*.052,hy+.03,.158)));B.push(P(box(.035,.012,.012),'#18181e',0,hy+.04,.158));}
  const h=o.hat;
  if(h!=='scarf'&&h!=='hood'&&h!=='chef'){B.push(P(new THREE.SphereGeometry(.153,18,12,0,Math.PI*2,0,Math.PI*.5),hair,0,hy+.025,-.012,-.32,0,0,1,1.05,1.05));if(o.long)B.push(P(box(.27,.3,.08),hair,0,hy-.12,-.11));}
  if(h==='cap'){const cc=o.capC||'#ff6b3d';B.push(P(new THREE.SphereGeometry(.158,18,10,0,Math.PI*2,0,Math.PI*.5),cc,0,hy+.06,0,0,0,0,1,1,1.05));B.push(P(cyl(.11,.11,.015,16),shadeC(cc,.8),0,hy+.07,.13,0,0,0,1,1,.9));}
  else if(h==='flat'){B.push(P(sph(.172,16,10),'#55555f',0,hy+.1,-.01,0,0,0,1.04,.42,1.14));B.push(P(cyl(.1,.11,.015,14),'#45454e',0,hy+.07,.12,0,0,0,1.15,1,.8));}
  else if(h==='scarf'||h==='hood'){const cc=h==='hood'?shadeC(shirt,.92):(o.capC||'#c8426a');B.push(P(new THREE.SphereGeometry(.17,18,14,Math.PI*.5+.95,Math.PI*2-1.9,0,Math.PI*.82),cc,0,hy+.01,-.005,0,0,0,1,1.1,1.05));B.push(P(sph(.07),cc,0,hy-.15,-.08));}
  else if(h==='chef'){B.push(P(cyl(.13,.12,.14,16),'#ffffff',0,hy+.19,0));B.push(P(sph(.15,14,10),'#ffffff',0,hy+.3,0,0,0,0,1,.6,1));}
  const thigh=MERGE([P(cyl(.085,.07,.46,10),pants,0,-.23,0)]),shin=MERGE([P(cyl(.066,.055,.44,10),pants,0,-.22,0),P(box(.11,.08,.25),'#2b2633',0,-.47,.05)]);
  const upper=MERGE([P(cyl(.056,.05,.3,10),top,0,-.15,0)]),fore=MERGE([P(cyl(.048,.042,.27,10),top,0,-.135,0),P(sph(.05,8,6),skin,0,-.3,0,0,0,0,.8,1.1,.9)]);
  const r={body:MERGE(B),thigh,shin,upper,fore};geoCache.set(k,r);return r;}
function shadeC(hex,k){const c=new THREE.Color(hex);c.multiplyScalar(k);return '#'+c.getHexString();}
function makeChar(look,scale=1){const P2=charParts(look);const root=new THREE.Group(),inner=new THREE.Group();root.add(inner);
  const body=mesh(P2.body);inner.add(body);const knees=[],elbows=[];
  const legs=[-1,1].map(s=>{const m=mesh(P2.thigh);m.position.set(s*.095,.96,0);const kn=new THREE.Group();kn.position.y=-.46;kn.add(mesh(P2.shin));m.add(kn);knees.push(kn);inner.add(m);return m;});
  const arms=[-1,1].map(s=>{const m=mesh(P2.upper);m.position.set(s*.25,1.44,0);m.rotation.z=s*.08;const el=new THREE.Group();el.position.y=-.3;el.rotation.x=-.2;el.add(mesh(P2.fore));m.add(el);elbows.push(el);inner.add(m);return m;});
  root.scale.setScalar(scale);root.userData={inner,legs,arms,knees,elbows,ph:Math.random()*9};scene.add(root);return root;}
function animChar(o,dt,moving,speed=1,dance=0){const u=o.userData;u.ph+=dt*(moving?8*speed:2);const s=Math.sin(u.ph),c=Math.cos(u.ph);
  if(dance){const d=Math.sin(u.ph*1.3);u.inner.position.y=Math.abs(d)*.12;u.inner.rotation.z=d*.1;u.arms[0].rotation.z=-2.5+d*.3;u.arms[1].rotation.z=2.5+d*.3;u.arms[0].rotation.x=u.arms[1].rotation.x=0;u.legs[0].rotation.x=d*.45;u.legs[1].rotation.x=-d*.45;u.knees[0].rotation.x=Math.max(0,d)*.8;u.knees[1].rotation.x=Math.max(0,-d)*.8;return;}
  u.inner.rotation.z=0;u.arms[0].rotation.z=-.08;u.arms[1].rotation.z=.08;
  if(moving){u.legs[0].rotation.x=s*.55;u.legs[1].rotation.x=-s*.55;u.knees[0].rotation.x=.08+Math.max(0,-c)*.85;u.knees[1].rotation.x=.08+Math.max(0,c)*.85;u.arms[0].rotation.x=-s*.45;u.arms[1].rotation.x=s*.45;u.elbows.forEach(e=>e.rotation.x=-.35);u.inner.position.y=Math.abs(c)*.045;}
  else{const k=Math.min(1,dt*10);u.legs.forEach(l=>l.rotation.x*=1-k);u.knees.forEach(l=>l.rotation.x*=1-k);u.arms.forEach(a=>a.rotation.x*=1-k);u.elbows.forEach(e=>e.rotation.x=-.15);u.inner.position.y=Math.sin(u.ph*.5)*.008;}}
function makeDog(){const c='#c98a4b',B=[P(new THREE.CapsuleGeometry(.22,.5,4,10),c,0,.5,0,Math.PI/2),P(sph(.2,12,10),c,0,.72,.42),P(sph(.11,10,8),'#f3d9b6',0,.66,.58),P(sph(.04),'#2b2238',0,.7,.68),
  P(sph(.035),'#2b2238',.08,.78,.58),P(sph(.035),'#2b2238',-.08,.78,.58),P(box(.08,.16,.05),'#7a4b2a',.13,.86,.38,0,0,-.4),P(box(.08,.16,.05),'#7a4b2a',-.13,.86,.38,0,0,.4)];
  [[.12,.25],[-.12,.25],[.12,-.25],[-.12,-.25]].forEach(([x,z])=>B.push(P(cyl(.05,.05,.32,6),c,x,.18,z)));
  const root=new THREE.Group();root.add(mesh(MERGE(B)));const tail=mesh(P(cyl(.03,.04,.3,6),'#a8703a',0,.15,0));tail.position.set(0,.62,-.42);tail.rotation.x=-.8;root.add(tail);root.userData={tail,ph:0};scene.add(root);return root;}

/* ---------------------------------------------------------------- VEHICLES */
function carGeo(kind,color){const B=[];const wheel=(x,z,r=.36)=>{B.push(P(cyl(r,r,.26,16),'#1a1a1f',x,r,z,0,0,Math.PI/2));B.push(P(cyl(r*.55,r*.55,.27,12),'#b8bec6',x,r,z,0,0,Math.PI/2));};
  if(kind==='niva'||kind==='myniva'){const c=color;B.push(P(box(1.72,.78,3.7),c,0,.86,0));B.push(P(box(1.62,.62,1.95),'#22303d',0,1.55,-.35));B.push(P(box(1.66,.1,2.05),c,0,1.9,-.35));
    B.push(P(box(1.74,.18,.22),'#2a2a2e',0,.55,1.86));B.push(P(box(1.74,.18,.22),'#2a2a2e',0,.55,-1.86));B.push(P(box(1.3,.3,.06),'#222',0,1.0,1.86));
    [-1,1].forEach(s=>{B.push(P(cyl(.15,.15,.06,14),'#fff7d0',s*.6,1.0,1.87,Math.PI/2));B.push(P(box(.14,.12,.05),'#ff3b30',s*.7,1.0,-1.86));B.push(P(box(.05,.05,1.1),'#9aa0a8',s*.84,.92,.3));});
    B.push(P(cyl(.36,.36,.24,16),'#1a1a1f',0,1.0,-2.0,Math.PI/2));B.push(P(cyl(.2,.2,.25,12),'#b8bec6',0,1.0,-2.0,Math.PI/2));
    [-1,1].forEach(s=>{B.push(P(box(.05,.08,2.1),'#3a3a40',s*.75,2.02,-.35));});for(let k=0;k<4;k++)B.push(P(box(1.5,.05,.05),'#3a3a40',0,2.02,-1.25+k*.6));
    if(kind==='myniva'){[-1,1].forEach(s=>{B.push(P(box(.02,.22,3.4),'#ff7a1a',s*.87,1.0,0));});B.push(P(box(1.0,.3,.03),'#ff7a1a',0,1.15,-1.86));}
    else{for(let k=0;k<3;k++)B.push(P(sph(.32,10,8),'#c9a36b',-.4+k*.4,2.2,-.35+(k%2)*.3,0,0,0,1,.7,1.3));}
    [[.86,1.15],[-.86,1.15],[.86,-1.15],[-.86,-1.15]].forEach(([x,z])=>wheel(x,z,.4));return MERGE(B);}
  if(kind==='marsh'){B.push(P(box(1.9,1.9,5.2),color,0,1.25,0));B.push(P(box(1.92,.6,4.4),'#22303d',0,1.65,-.3));B.push(P(box(1.7,.7,.05),'#22303d',0,1.6,2.61));B.push(P(box(1.94,.2,5.24),'#d6453d',0,.62,0));
    [-1,1].forEach(s=>B.push(P(box(.2,.14,.05),'#fff7d0',s*.65,.85,2.61)));[[.92,1.7],[-.92,1.7],[.92,-1.7],[-.92,-1.7]].forEach(([x,z])=>wheel(x,z,.42));return MERGE(B);}
  // car / taxi / police
  B.push(P(box(1.74,.58,4.1),color,0,.68,0));B.push(P(box(1.56,.5,2.1),'#22303d',0,1.2,-.2));B.push(P(box(1.6,.08,1.8),color,0,1.48,-.25));
  B.push(P(box(1.7,.06,1.2),shadeC(color,1.05),0,.99,1.35));[-1,1].forEach(s=>{B.push(P(box(.32,.12,.05),'#fff7d0',s*.6,.78,2.06));B.push(P(box(.36,.12,.05),'#ff3b30',s*.6,.8,-2.06));});
  B.push(P(box(1.78,.16,.18),'#2a2a2e',0,.45,2.05));B.push(P(box(1.78,.16,.18),'#2a2a2e',0,.45,-2.05));
  if(kind==='taxi'){B.push(P(box(.62,.2,.3),'#222',0,1.6,-.25));for(let k=0;k<4;k++)B.push(P(box(.15,.1,.32),k%2?'#ffd84d':'#222',-.23+k*.155,1.62,-.25));}
  if(kind==='police'){[-1,1].forEach(s=>B.push(P(box(.03,.25,3.6),'#2350a8',s*.88,.75,0)));}
  [[.86,1.3],[-.86,1.3],[.86,-1.3],[-.86,-1.3]].forEach(([x,z])=>wheel(x,z));return MERGE(B);}
const carGeoCache=new Map();
function makeCar(kind,color){const k=kind+color;if(!carGeoCache.has(k))carGeoCache.set(k,carGeo(kind,color));const g=new THREE.Group();g.add(mesh(carGeoCache.get(k),CARM));scene.add(g);return g;}

/* ---------------------------------------------------------------- WORLD BUILD */
const R3={POLICE:{skin:'#e7b08a',shirt:'#2350a8',pants:'#1d2b4a',hat:'cap',capC:'#1d3f7a',must:true},ready:false,cam:{mode:'top',yaw:Math.PI,pitch:-.12,zoom:1},objs:{}};
const toW=(x,y,h=0)=>new V3(x*U,h,y*U);
const PARKED=[];let procParked=null;
const SITTERS=[],CLOTHES=[],SPIN=[],FLAGS=[],TROLLEYS=[],TLIGHT={im:null,n:0},WHEEL={o:null};
let groundMesh,waterMat,gpsMesh,gpsTex,targetRing,hubRing,stoneMesh,policeCar,policeLights,fountains=[],pigeons,smoke=[],swanObjs=[],lockers=[],freeRings=[],rainMesh,confetti;
const MW_=MW*TS*U,MH_=MH*TS*U;

function paintGround(){const k=Math.min(1.25,4096/(MW*TS),4096/(MH*TS)),[c,g]=cnv(Math.round(MW*TS*k),Math.round(MH*TS*k));
  if(!PAT.grass)initPatterns();const sv={b:W.buildings,t:W.trees,d:W.decor};W.buildings=[];W.trees=[];W.decor=sv.d.filter(d=>d.k==='square');
  g.scale(k,k);drawRegion(g,0,0,MW*TS,MH*TS);W.buildings=sv.b;W.trees=sv.t;W.decor=sv.d;
  W.decor.filter(d=>d.k==='hayat').forEach(d=>{g.fillStyle='#b7a487';g.fillRect(d.x,d.y,d.w,d.h);for(let i=0;i<400;i++){g.fillStyle=`rgba(${rand()<.5?60:240},${rand()<.5?50:230},40,${rand()*.12})`;g.fillRect(d.x+rand()*d.w,d.y+rand()*d.h,3,3);}g.fillStyle='rgba(70,72,80,.55)';g.fillRect(d.x+d.w*.3,d.y+d.h*.25,d.w*.4,d.h*.5);});
  // soft contact shadows under buildings
  g.fillStyle='rgba(40,30,30,.22)';W.buildings.forEach(b=>{g.fillRect(b.x*TS-4,b.y*TS-4,b.w*TS+12,b.h*TS+12);});
  const t=tex(c,false);t.anisotropy=MAXANISO;t.generateMipmaps=true;t.minFilter=THREE.LinearMipmapLinearFilter;return t;}
function quadBuilder(){const pos=[],nor=[],uv=[];return {pos,nor,uv,
  quad(a,b,c2,d,n,u0,v0,u1,v1){pos.push(...a,...b,...c2,...a,...c2,...d);for(let i=0;i<6;i++)nor.push(...n);uv.push(u0,v0,u1,v0,u1,v1,u0,v0,u1,v1,u0,v1);},
  geo(){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(nor,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));return g;}};}
function wallsInto(q,x0,z0,w,d,h,uoff=0){const H=h,su=1/(4*BAY),sv=1/(4*FLOOR);
  q.quad([x0,0,z0+d],[x0+w,0,z0+d],[x0+w,H,z0+d],[x0,H,z0+d],[0,0,1],uoff,0,uoff+w*su,H*sv);          // south (front)
  q.quad([x0+w,0,z0],[x0,0,z0],[x0,H,z0],[x0+w,H,z0],[0,0,-1],uoff+.25,0,uoff+.25+w*su,H*sv);       // north
  q.quad([x0+w,0,z0+d],[x0+w,0,z0],[x0+w,H,z0],[x0+w,H,z0+d],[1,0,0],uoff+.5,0,uoff+.5+d*su,H*sv);   // east
  q.quad([x0,0,z0],[x0,0,z0+d],[x0,H,z0+d],[x0,H,z0],[-1,0,0],uoff+.75,0,uoff+.75+d*su,H*sv);}      // west
function roofInto(q,x0,z0,w,d,h){q.quad([x0,h,z0+d],[x0+w,h,z0+d],[x0+w,h,z0],[x0,h,z0],[0,1,0],x0/8,z0/8,(x0+w)/8,(z0+d)/8);}

function buildWorld3D(){
  // ground
  const gt=paintGround();groundMesh=new THREE.Mesh(new THREE.PlaneGeometry(MW_,MH_),new THREE.MeshStandardMaterial({map:gt,roughness:.92}));groundMesh.rotation.x=-Math.PI/2;groundMesh.position.set(MW_/2,0,MH_/2);groundMesh.receiveShadow=true;scene.add(groundMesh);
  const far=new THREE.Mesh(new THREE.CircleGeometry(1400,48),new THREE.MeshStandardMaterial({color:'#b9a27c',roughness:1}));far.rotation.x=-Math.PI/2;far.position.set(MW_/2,-.05,MH_/2);far.receiveShadow=true;scene.add(far);
  // water (river + swan lake) with sky reflections
  waterMat=new THREE.MeshStandardMaterial({color:'#2f8fc9',roughness:.06,metalness:.1,transparent:true,opacity:.82,envMapIntensity:1.4});
  {const wg=[];for(let y=0;y<MH;y++)for(let x=0;x<MW;x++)if(tget(x,y)===T.W){const g=new THREE.PlaneGeometry(2.02,2.02);g.rotateX(-Math.PI/2);g.translate(x*2+1,.06,y*2+1);wg.push(g);}
   const wm=new THREE.Mesh(mergeGeometries(wg),waterMat);wm.receiveShadow=true;scene.add(wm);
   const rv=new THREE.Mesh(new THREE.PlaneGeometry(34,MH_+400),waterMat);rv.rotation.x=-Math.PI/2;rv.position.set(-15,.05,MH_/2);scene.add(rv);}
  // bridges over the river
  W.buildings;HR.forEach(y=>{const g=mesh(MERGE([P(box(10,.5,4.4),'#9b8f84',-1,.25,(y+1)*2),P(box(10,.6,.25),'#e8dccb',-1,.75,(y+1)*2+2.1),P(box(10,.6,.25),'#e8dccb',-1,.75,(y+1)*2-2.1)]),VCM);scene.add(g);});
  // ---------------- buildings: centre tuff (pink/orange/black), Soviet panel microdistricts, old Kond houses, modern Northern Ave
  const styles={pink:facadeTex('#e7a596','tuff',.65),orange:facadeTex('#e3a374','tuff',.65),beige:facadeTex('#ecd2b0','tuff',.5),rose:facadeTex('#d79a8c','tuff',.6),black:facadeTex('#9a8f8a','tuff',.6),
    panel:facadeTex('#cfcac2','panel',0),panel2:facadeTex('#d9cdb8','panel',0),old:facadeTex('#dcbf9a','old',0),modern:facadeTex('#eadbc6','modern',.9)};
  const WALLC={pink:'#e7a596',orange:'#e3a374',beige:'#ecd2b0',rose:'#d79a8c',black:'#9a8f8a',panel:'#cfcac2',panel2:'#d9cdb8',old:'#dcbf9a',modern:'#eadbc6'};
  const Q={};Object.keys(styles).forEach(k=>Q[k]=quadBuilder());const roofQ=quadBuilder();const props=[];const pitched=[];const balQ=quadBuilder();
  const tanks=[],dishes=[],solars=[],acs=[],antennas=[],fdishes=[];
  const balcony=(cx,y,zf,dir,v,w=2.5,h=2.55,dd=.85)=>{const u0=v*.25,z1=zf+dir*dd,x0=cx-w/2,x1=cx+w/2;const n=[0,0,dir];
    if(dir>0)balQ.quad([x0,y,z1],[x1,y,z1],[x1,y+h,z1],[x0,y+h,z1],n,u0,0,u0+.25,1);else balQ.quad([x1,y,z1],[x0,y,z1],[x0,y+h,z1],[x1,y+h,z1],n,u0,0,u0+.25,1);
    const za=Math.min(zf,z1),zb=Math.max(zf,z1);balQ.quad([x0,y+h,zb],[x1,y+h,zb],[x1,y+h,za],[x0,y+h,za],[0,1,0],u0,.96,u0+.01,1);balQ.quad([x0,y,za],[x1,y,za],[x1,y,zb],[x0,y,zb],[0,-1,0],u0,.96,u0+.01,1);
    balQ.quad([x1,y,zb],[x1,y,za],[x1,y+h,za],[x1,y+h,zb],[1,0,0],u0+.02,0,u0+.05,1);balQ.quad([x0,y,za],[x0,y,zb],[x0,y+h,zb],[x0,y+h,za],[-1,0,0],u0+.02,0,u0+.05,1);};
  W.buildings.forEach((b,i)=>{const x0=b.x*2,z0=b.y*2,w=b.w*2,d=b.h*2;b.x3=x0;b.z3=z0;b.w3=w;b.d3=d;
    if(b.kind!=='home'){special(b,x0,z0,w,d,props);return;}
    const sty=b.style||'tuff';const fl=Math.max(1,b.floors);const h=fl*FLOOR+.3;b.h3=h;const P0=b.props;
    const tex=sty==='panel'?(P0[1]<.5?'panel':'panel2'):sty==='old'?'old':sty==='modern'?'modern':sty==='old5'?(P0[1]<.5?'beige':'rose'):(P0[1]<.08?'black':['pink','orange','pink','rose','orange','beige'][(P0[1]*6)|0]);
    wallsInto(Q[tex],x0,z0,w,d,h,((P0[2]*4)|0)/4);const wc=WALLC[tex];
    // entrance with canopy (door faces the street or the courtyard)
    const dx=x0+w/2;props.push(P(box(1.4,2.3,.14),'#5c3a22',dx,1.15,z0+d+.03),P(box(1.9,.12,1),shadeC(wc,.85),dx,2.55,z0+d+.45),P(box(2,.2,1.2),'#bdb3a6',dx,.1,z0+d+.55),P(box(.1,.1,.1),'#ffe7a0',dx+.55,2.3,z0+d+.1));
    if(sty==='tuff'||sty==='old5'||sty==='modern'){ // cornice + belt course: the classic Tamanyan-style tuff detail
      props.push(P(box(w+.7,.45,d+.7),shadeC(wc,1.07),x0+w/2,h-.1,z0+d/2),P(box(w+.35,.22,d+.35),shadeC(wc,.9),x0+w/2,FLOOR+.15,z0+d/2));
      if(sty!=='modern')for(let k=0;k<Math.floor(w/BAY);k++)props.push(P(box(.28,FLOOR-.2,.18),shadeC(wc,.92),x0+k*BAY+.15,FLOOR/2,z0+d+.06));}
    if(sty==='panel'){props.push(P(box(w+.3,.3,d+.3),'#b9b4ac',x0+w/2,h,z0+d/2));for(let f=1;f<fl;f++)props.push(P(box(w+.06,.06,.06),'#a8a39b',x0+w/2,f*FLOOR,z0+d+.02));}
    // protruding enclosed balconies (glazed «լոջիաներ») + AC units + dishes
    if(sty!=='old'){const bays=Math.floor(w/BAY);[1,-1].forEach(dir=>{const zf=dir>0?z0+d:z0;for(let f=1;f<fl;f++)for(let k=0;k<bays;k++){const r=hash(b.x*7+k,b.y*13+f,dir>0?1:2);const cx=x0+k*BAY+BAY/2;
      if(r<(sty==='panel'?.34:sty==='modern'?.18:.24))balcony(cx,f*FLOOR+.12,zf,dir,(hash(b.x,b.y+k,3)*4)|0,sty==='modern'?2.7:2.5);
      else if(r>.84)acs.push([cx+.95,f*FLOOR+1.75,zf+dir*.22,dir]);else if(r>.8&&r<.815)fdishes.push([cx+.9,f*FLOOR+2.2,zf+dir*.3,dir]);}});}
    else{ // Kond house: wooden veranda
      props.push(P(box(w-.6,.12,1.4),'#8a6243',x0+w/2,FLOOR,z0+d+.7),P(box(w-.6,.8,.06),'#6e4b32',x0+w/2,FLOOR+.5,z0+d+1.38));for(let k=0;k<6;k++)props.push(P(box(.08,FLOOR,.08),'#6e4b32',x0+.5+k*(w-1)/5,FLOOR/2,z0+d+1.35));}
    if(b.pitched){const pc=sty==='old'?rp(['#a3492f','#8c6d4f','#b45a3c','#6f7f86']):b.pitchC,g=new THREE.BufferGeometry();const y=h,ry=h+Math.min(w,d)*.35;
      const v=[x0-.3,y,z0+d+.3, x0+w+.3,y,z0+d+.3, x0+w+.3,ry,z0+d/2, x0-.3,y,z0+d+.3, x0+w+.3,ry,z0+d/2, x0-.3,ry,z0+d/2,  x0+w+.3,y,z0-.3, x0-.3,y,z0-.3, x0-.3,ry,z0+d/2, x0+w+.3,y,z0-.3, x0-.3,ry,z0+d/2, x0+w+.3,ry,z0+d/2,
        x0-.3,y,z0-.3, x0-.3,y,z0+d+.3, x0-.3,ry,z0+d/2, x0+w+.3,y,z0+d+.3, x0+w+.3,y,z0-.3, x0+w+.3,ry,z0+d/2];
      g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.computeVertexNormals();pitched.push(paint(g,pc));roofInto(roofQ,x0,z0,w,d,h-.01);
      if(sty==='old')props.push(P(box(.5,1.2,.5),'#9b8f84',x0+w*.7,ry-.2,z0+d*.4));}
    else{roofInto(roofQ,x0,z0,w,d,h);
      if(sty!=='panel'&&sty!=='modern'&&sty!=='tuff')props.push(P(box(w+.2,.5,.25),wc,x0+w/2,h+.25,z0+d),P(box(w+.2,.5,.25),wc,x0+w/2,h+.25,z0),P(box(.25,.5,d),wc,x0,h+.25,z0+d/2),P(box(.25,.5,d),wc,x0+w,h+.25,z0+d/2));
      if(P0[0]<.8)tanks.push([x0+1.5+P0[1]*(w-3),h,z0+1.5+P0[3]*(d-3)]);if(P0[2]<.7)dishes.push([x0+w-1,h,z0+d-1.2,P0[4]]);if(P0[3]<.55)solars.push([x0+1.6,h,z0+1.6+P0[5]*(d-3)]);
      for(let k=0;k<(sty==='panel'?3:1);k++)if(hash(b.x,b.y,k+9)<.7)antennas.push([x0+1+hash(b.x,k,4)*(w-2),h,z0+1+hash(k,b.y,5)*(d-2)]);
      if(sty==='panel'||fl>6)props.push(P(box(3,2.2,2.4),'#a9a39a',x0+w*.35,h+1.1,z0+d/2));
      if(P0[4]<.35&&w>5){for(let k=0;k<5;k++)props.push(P(box(.5,.6,.02),rp(['#e2574c','#5fb7e8','#f2c94c','#ffffff','#7fcf6a']),x0+1.5+k*(w-3)/5,h+1.2,z0+d/2));props.push(P(box(w-2,.02,.02),'#777',x0+w/2,h+1.55,z0+d/2));
        [-1,1].forEach(s=>props.push(P(cyl(.04,.04,1.6,5),'#777',x0+w/2+s*(w/2-1),h+.8,z0+d/2)));}}});
  Object.entries(Q).forEach(([k,q])=>{if(!q.pos.length)return;const m=new THREE.Mesh(q.geo(),new THREE.MeshStandardMaterial({map:styles[k],roughness:k==='modern'?.45:.85,metalness:k==='modern'?.15:0}));m.castShadow=m.receiveShadow=true;scene.add(m);});
  {const m=new THREE.Mesh(roofQ.geo(),new THREE.MeshStandardMaterial({map:roofTex(),roughness:.95}));m.receiveShadow=true;m.castShadow=true;scene.add(m);}
  if(balQ.pos.length){const m=new THREE.Mesh(balQ.geo(),new THREE.MeshStandardMaterial({map:balconyTex(),roughness:.5,metalness:.1}));m.castShadow=m.receiveShadow=true;scene.add(m);}
  if(pitched.length){const m=mesh(mergeGeometries(pitched));scene.add(m);}
  // rooftop & facade instanced props
  const inst=(geo,list,fn,mat=VCM)=>{if(!list.length)return;const im=new THREE.InstancedMesh(geo,mat,list.length);list.forEach((v,i)=>{fn(v,_m);im.setMatrixAt(i,_m);});im.castShadow=true;im.receiveShadow=true;scene.add(im);return im;};
  inst(MERGE([P(cyl(.6,.6,1.3,14),'#e9eef2',0,1.25,0),P(cyl(.62,.62,.12,14),'#3d77b5',0,1.95,0),P(box(.1,.6,.1),'#666',.4,.3,.4),P(box(.1,.6,.1),'#666',-.4,.3,-.4),P(box(.1,.6,.1),'#666',.4,.3,-.4),P(box(.1,.6,.1),'#666',-.4,.3,.4)]),tanks,(v,m)=>m.makeTranslation(v[0],v[1],v[2]));
  inst(MERGE([P(new THREE.SphereGeometry(.55,14,8,0,Math.PI*2,0,Math.PI*.35),'#f2f2f2',0,.9,0,-1.0),P(cyl(.04,.04,.8,5),'#888',0,.4,0)]),dishes,(v,m)=>m.compose(_p.set(v[0],v[1],v[2]),_q.setFromEuler(_e.set(0,v[3]*6,0)),_s.set(1,1,1)));
  inst(MERGE([P(box(1.6,.06,1.1),'#26425e',0,.8,0,-.6),P(cyl(.22,.22,1.6,10),'#dfe3e8',0,1.25,-.55,0,0,Math.PI/2),P(box(.08,.9,.08),'#888',.7,.45,.3),P(box(.08,.9,.08),'#888',-.7,.45,.3)]),solars,(v,m)=>m.makeTranslation(v[0],v[1],v[2]));
  inst(MERGE([P(box(.85,.55,.36),'#eef0f2',0,0,0),P(cyl(.19,.19,.02,14),'#9aa0a8',.12,0,.19,Math.PI/2),P(box(.04,.4,.04),'#888',-.3,-.4,-.05)]),acs,(v,m)=>m.compose(_p.set(v[0],v[1],v[2]),_q.setFromEuler(_e.set(0,v[3]>0?0:Math.PI,0)),_s.set(1,1,1)));
  inst(MERGE([P(new THREE.SphereGeometry(.35,12,6,0,Math.PI*2,0,Math.PI*.35),'#f4f4f4',0,0,.1,-1.2),P(box(.04,.04,.35),'#888',0,-.05,.05)]),fdishes,(v,m)=>m.compose(_p.set(v[0],v[1],v[2]),_q.setFromEuler(_e.set(0,v[3]>0?0:Math.PI,0)),_s.set(1,1,1)));
  inst(MERGE([P(cyl(.03,.03,2.4,4),'#777',0,1.2,0),P(box(1.2,.03,.03),'#777',0,2.2,0),P(box(.9,.03,.03),'#777',0,1.9,0),P(box(.6,.03,.03),'#777',0,1.6,0)]),antennas,(v,m)=>m.compose(_p.set(v[0],v[1],v[2]),_q.setFromEuler(_e.set(0,v[0]*3,0)),_s.set(1,1,1)));
  scene.add(mesh(MERGE(props)));
  // billboards on a few tall buildings
  W.homes.filter(b=>b.h3>15).slice(0,6).forEach((b,i)=>{const g=new THREE.Group();const bw=Math.min(b.w3-1,9);const pl=new THREE.Mesh(new THREE.PlaneGeometry(bw,bw*.39),new THREE.MeshStandardMaterial({map:adTex(i),roughness:.6,emissive:'#ffffff',emissiveIntensity:.08,emissiveMap:null}));
    pl.position.set(0,3.2,0);g.add(pl);g.add(mesh(MERGE([P(box(bw+.3,bw*.39+.3,.15),'#333',0,3.2,-.1),P(box(.2,2.4,.2),'#555',-bw/3,1.2,-.3),P(box(.2,2.4,.2),'#555',bw/3,1.2,-.3)])));
    g.position.set(b.x3+b.w3/2,b.h3,b.z3+b.d3-1);scene.add(g);});
  // filler city outside the playable map (no hard world edge)
  {const geo=new THREE.BoxGeometry(1,1,1);geo.translate(0,.5,0);const n=220;const m=new THREE.InstancedMesh(geo,new THREE.MeshStandardMaterial({map:styles.beige,roughness:.9}),n);let k=0;
    for(let i=0;i<n*3&&k<n;i++){const a=rand()*Math.PI*2,r=1;const x=MW_/2+Math.cos(a)*(MW_/2+12+rand()*110),z=MH_/2+Math.sin(a)*(MH_/2+12+rand()*110);if(x<-6)continue;const w=6+rand()*10,h=6+rand()*24;m.setMatrixAt(k++,_m.compose(_p.set(x,0,z),_q.identity(),_s.set(w,h,w*(.7+rand()*.6))));}
    m.count=k;m.castShadow=true;m.receiveShadow=true;scene.add(m);}
  // ---------------- trees
  {const kinds={tree:[],apricot:[],poplar:[],street:[]};W.trees.forEach(t=>kinds[t.k].push(t));for(let i=0;i<70;i++){const a=rand()*Math.PI*2;const x=MW_/2+Math.cos(a)*(MW_/2+8+rand()*60),z=MH_/2+Math.sin(a)*(MH_/2+8+rand()*60);if(x>-4)kinds.tree.push({x:x/U,y:z/U,r:14+rand()*4,s:rand()});}
    const trunk=MERGE([P(cyl(.16,.24,2.2,7),'#7a5234',0,1.1,0)]);const crown=new THREE.IcosahedronGeometry(1,3);{const p=crown.attributes.position;for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i);const n=1+.13*Math.sin(x*5.1+y*3.7)+.09*Math.sin(z*7.3-x*2.1)+.06*Math.sin(y*11+z*4);p.setXYZ(i,x*n,y*n*.92,z*n);}crown.computeVertexNormals();}const cm=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.9});
    Object.entries(kinds).forEach(([k,list])=>{if(!list.length)return;const n=list.length;const tr=new THREE.InstancedMesh(trunk,VCM,n),cr=new THREE.InstancedMesh(crown,cm,n*(k==='poplar'?1:3));let ci=0;const c=new THREE.Color();
      list.forEach((t,i)=>{const x=t.x*U,z=t.y*U,r=t.r*U*1.45;tr.setMatrixAt(i,_m.compose(_p.set(x,0,z),_q.identity(),_s.set(1,k==='poplar'?1.4:1,1)));
        if(k==='poplar'){cr.setMatrixAt(ci,_m.compose(_p.set(x,4.2,z),_q.identity(),_s.set(r*.65,r*2.6,r*.65)));c.setHSL(.3,.45,.24+rand()*.06);cr.setColorAt(ci++,c);}
        else for(let j=0;j<3;j++){const a=j*2.1+rand();cr.setMatrixAt(ci,_m.compose(_p.set(x+Math.cos(a)*r*(j===1?.1:.45),2.7+r*.55+(j===1?r*.42:0),z+Math.sin(a)*r*.4),_q.setFromEuler(_e.set(rand(),rand(),rand())),_s.set(r*(j===1?.95:.78),r*(j===1?.85:.7),r*(j===1?.95:.78))));c.setHSL(k==='apricot'?.22:k==='street'?.24:.28,k==='street'?.42:.5,(k==='street'?.33:.3)+rand()*.08);cr.setColorAt(ci++,c);}});
      cr.count=ci;[tr,cr].forEach(m=>{m.castShadow=true;m.receiveShadow=true;scene.add(m);});
      if(k==='apricot'){const fr=new THREE.InstancedMesh(new THREE.SphereGeometry(.12,6,5),new THREE.MeshStandardMaterial({color:'#ff9d2e',roughness:.5}),n*8);let fi=0;list.forEach(t=>{for(let j=0;j<8;j++){const a=rand()*7,r=t.r*U*1.3;fr.setMatrixAt(fi++,_m.makeTranslation(t.x*U+Math.cos(a)*r,2.8+rand()*1.6,t.y*U+Math.sin(a)*r));}});scene.add(fr);}});}
  // ---------------- street furniture
  {const L=W.decor.filter(d=>d.k==='lamp'),Bn=W.decor.filter(d=>d.k==='bench'),Bi=W.decor.filter(d=>d.k==='bin');
    inst(MERGE([P(cyl(.07,.1,4.2,8),'#3a3f4a',0,2.1,0),P(box(.9,.08,.12),'#3a3f4a',.4,4.15,0),P(box(.4,.12,.28),'#2c3038',.8,4.1,0)]),L,(d,m)=>m.makeTranslation(d.x*U,0,d.y*U));
    inst(MERGE([P(box(.42,.1,.3),'#fff3c4',.8,4.03,0)]),L,(d,m)=>m.makeTranslation(d.x*U,0,d.y*U),GLOWM);
    inst(MERGE([P(box(1.8,.1,.5),'#a8774f',0,.48,0),P(box(1.8,.45,.08),'#a8774f',0,.78,-.24,-.15),P(box(.08,.48,.5),'#333',-.8,.24,0),P(box(.08,.48,.5),'#333',.8,.24,0)]),Bn,(d,m)=>m.makeTranslation(d.x*U,0,d.y*U));
    inst(MERGE([P(cyl(.25,.22,.8,10),'#3f7f4f',0,.4,0)]),Bi,(d,m)=>m.makeTranslation(d.x*U,0,d.y*U));
    const pk=W.decor.filter(d=>d.k==='parked');const nv=[];pk.forEach(d=>{const rot=rand()<.5?0:Math.PI;if(rand()<.15){const g=carGeo('niva',d.c).clone();g.rotateY(rot);g.translate(d.x*U,0,d.y*U);nv.push(g);}else PARKED.push({x:d.x*U,z:d.y*U,rot,color:new THREE.Color(d.c)});});
    if(nv.length)scene.add(mesh(mergeGeometries(nv),CARM));
    procParked=new THREE.InstancedMesh(carGeo('car','#ffffff'),CARM,PARKED.length);PARKED.forEach((c,i)=>{c.m=new THREE.Matrix4().compose(new V3(c.x,0,c.z),new THREE.Quaternion().setFromEuler(new THREE.Euler(0,c.rot,0)),new V3(1,1,1));procParked.setMatrixAt(i,c.m);procParked.setColorAt(i,c.color);});procParked.castShadow=procParked.receiveShadow=true;procParked.frustumCulled=false;scene.add(procParked);}
  // street name signs
  {const names=['Մաշտոցի պող.','Աբովյան փ.','Տիգրան Մեծի պող.','Բաղրամյան պող.','Սայաթ-Նովայի պող.','Արշակունյաց պող.','Կոմիտասի պող.','Թումանյան փ.','Պուշկինի փ.','Նալբանդյան փ.','Վազգեն Սարգսյան փ.','Խանջյան փ.'];let k=0;
    VR.forEach((x,i)=>HR.forEach((y,j)=>{if((i+j)%2)return;const g=new THREE.Group();const sm=new THREE.MeshStandardMaterial({map:streetTex(names[k++%names.length]),roughness:.5});[0,Math.PI].forEach(r=>{const pl=new THREE.Mesh(new THREE.PlaneGeometry(2.4,.6),sm);pl.position.y=3;pl.rotation.y=r;pl.position.z=r?-.01:.01;g.add(pl);});g.add(mesh(P(cyl(.05,.05,3.3,6),'#555',0,1.65,0)));g.position.set(x*2-1.2,0,y*2-1.2);g.rotation.y=.6;scene.add(g);}));}
  // ---------------- landmarks
  // Republic square fountain + pigeons
  {const s=W.places.square;const cx=s.x*U,cz=(s.y-64)*U;const g=MERGE([P(cyl(4.2,4.4,.6,40),'#d6c1a3',0,.3,0,0,0,0,1.6,1,.9),P(cyl(3.9,3.9,.62,40),'#47ade2',0,.32,0,0,0,0,1.6,1,.9)]);scene.add(mesh(g));fountains.push({x:cx,z:cz,sx:1.6*3.4,sz:.9*3.4,n:isMobile?220:420,h:3.4});
    const pg=new THREE.InstancedMesh(MERGE([P(sph(.13,8,6),'#8d8f99',0,.16,0,0,0,0,1,.8,1.4),P(sph(.08,8,6),'#6f7180',0,.3,.12),P(box(.02,.02,.05),'#e0a030',0,.3,.2)]),VCM,40);pigeons={im:pg,list:[]};
    for(let i=0;i<40;i++)pigeons.list.push({hx:cx+(rand()-.5)*20,hz:cz+6+(rand()-.5)*10,x:0,y:0,z:0,vy:0,fly:0,a:rand()*7});pigeons.list.forEach(p=>{p.x=p.hx;p.z=p.hz;});pg.castShadow=true;scene.add(pg);}
  // Cascade: travertine terraces rising to the north
  {const d=W.decor.find(d=>d.k==='cascade');const x0=d.x*U,z0=d.y*U,w=d.w*U,h=d.h*U;const tiers=6,B=[];
    for(let i=0;i<tiers;i++){const zz=z0+h-(i+1)*(h-4)/tiers-4,hh=(i+1)*2.2;B.push(P(box(w,hh,(h-4)/tiers),'#efe2cc',x0+w/2,hh/2,zz+(h-4)/tiers/2));B.push(P(box(w-1.2,.25,1),'#5aa94a',x0+w/2,hh+.12,zz+(h-4)/tiers-.6));
      for(let k=0;k<8;k++)B.push(P(sph(.22,6,5),['#ff7aa8','#ffd25f','#b48cff','#ff6b6b'][(k+i)%4],x0+1+k*(w-2)/7,hh+.35,zz+(h-4)/tiers-.6));
      B.push(P(box(1.4,.08,(h-4)/tiers),'#7fd0f0',x0+w/2,hh+.02,zz+(h-4)/tiers/2));}
    B.push(P(cyl(2.4,2.6,.5,24),'#d7c4a8',x0+w/2,.25,z0+h-2.6));B.push(P(cyl(2.1,2.1,.52,24),'#58b9e8',x0+w/2,.27,z0+h-2.6));scene.add(mesh(MERGE(B)));
    fountains.push({x:x0+w/2,z:z0+h-2.6,sx:1.6,sz:1.6,n:isMobile?100:180,h:2.6});
    // walk blocked by terraces (except the plaza in front)
    for(let y=Math.floor(d.y/TS);y<Math.floor((d.y+d.h)/TS)-3;y++)for(let x=Math.floor(d.x/TS);x<Math.floor((d.x+d.w)/TS);x++)W.solid[y*MW+x]=1;}
  // Swan lake swans
  {const sw=W.decor.find(d=>d.k==='swans');for(let k=0;k<2;k++){const g=mesh(MERGE([P(sph(.5,12,10),'#ffffff',0,.35,0,0,0,0,1,.7,1.5),P(cyl(.08,.1,.8,8),'#ffffff',0,.8,.5,-.3),P(sph(.16,10,8),'#ffffff',0,1.2,.62),P(box(.1,.08,.2),'#ff9f43',0,1.18,.8)]));scene.add(g);swanObjs.push({o:g,c:{x:sw.x*U,z:sw.y*U},k});}}
  // grills (kyabab + Samo) smoke
  {const st=new THREE.SpriteMaterial({map:smokeTex(),transparent:true,depthWrite:false,opacity:.6});[W.places.kyabab,W.decor.find(d=>d.k==='grill')].forEach(p=>{for(let i=0;i<10;i++){const s=new THREE.Sprite(st.clone());s.userData={x:p.x*U+(p===W.places.kyabab?0:0),z:p.y*U-(p===W.places.kyabab?3:0),y0:p===W.places.kyabab?4.6:1,t:i/10};scene.add(s);smoke.push(s);}});
    const gr=W.decor.find(d=>d.k==='grill');scene.add(mesh(MERGE([P(box(2.6,.7,.8),'#3a3a44',gr.x*U,.75,gr.y*U),P(box(2.3,.06,.6),'#ff6b2b',gr.x*U,1.12,gr.y*U),...[0,1,2,3,4].map(k=>P(cyl(.025,.025,1.1,4),'#ccc',gr.x*U-.9+k*.45,1.2,gr.y*U,Math.PI/2)),P(box(.08,.7,.08),'#333',gr.x*U-1.1,.35,gr.y*U-.3),P(box(.08,.7,.08),'#333',gr.x*U+1.1,.35,gr.y*U+.3)])));}
  // market stalls, nardi table, pallets
  W.decor.forEach(d=>{const x=d.x*U,z=d.y*U;
    if(d.k==='stall'){const fr=[];for(let k=0;k<10;k++)fr.push(P(sph(.15,8,6),rp(['#e2574c','#f2c94c','#5aa94a','#ff9f43','#8b3a8a']),x-1.1+(k%5)*.55,1.0,z-.2+((k/5)|0)*.4));
      scene.add(mesh(MERGE([P(box(2.9,.9,1.2),'#8a5a36',x,.45,z),...fr,P(box(3.2,.08,1.8),d.c,x,2.4,z,.15),P(box(.08,2.4,.08),'#555',x-1.5,1.2,z-.7),P(box(.08,2.4,.08),'#555',x+1.5,1.2,z-.7),P(box(.08,2.2,.08),'#555',x-1.5,1.1,z+.7),P(box(.08,2.2,.08),'#555',x+1.5,1.1,z+.7)])));}
    if(d.k==='nardi'){const nt=narTex();const g=new THREE.Group();g.add(mesh(MERGE([P(box(2.2,.1,1.4),'#7a4f2c',0,.8,0),P(box(.12,.8,.12),'#5a3a20',-.9,.4,-.5),P(box(.12,.8,.12),'#5a3a20',.9,.4,.5),P(box(.12,.8,.12),'#5a3a20',.9,.4,-.5),P(box(.12,.8,.12),'#5a3a20',-.9,.4,.5),
      P(box(.6,.5,.6),'#7a5234',-1.8,.25,0),P(box(.6,.5,.6),'#7a5234',1.8,.25,0)])));const top=new THREE.Mesh(new THREE.PlaneGeometry(1.9,1.2),new THREE.MeshStandardMaterial({map:nt,roughness:.7}));top.rotation.x=-Math.PI/2;top.position.y=.86;g.add(top);g.position.set(x,0,z);scene.add(g);}
    if(d.k==='pallets'){const zz=z-2.1;scene.add(mesh(MERGE([0,1,2].flatMap(k=>[P(box(1,.15,1),'#b58556',x-1.1+k*1.1,.08,zz),P(box(.8,.7,.8),'#d9a066',x-1.1+k*1.1,.5,zz),P(box(.6,.5,.6),'#e2b27a',x-1.1+k*1.1,1.1,zz,0,k)]))));}});
  // Ararat (Masis & Sis) — on the horizon, south-west
  {const mk=(r,h,x,z,seed)=>{const g=new THREE.ConeGeometry(r,h,96,24,true);const p=g.attributes.position,c=[];const hs=seeded(seed);const nz=[];for(let i=0;i<40;i++)nz.push(hs()*2-1);
      for(let i=0;i<p.count;i++){const y=p.getY(i)+h/2,t=y/h;const a=Math.atan2(p.getZ(i),p.getX(i));let n=0;for(let k=1;k<6;k++)n+=Math.sin(a*k*3+nz[k]*6)*nz[k+6]*.04/k+Math.sin(a*k*7+nz[k+12]*3)*.012;
        const sc=1+n*(1-t)*2.2;p.setX(i,p.getX(i)*sc);p.setZ(i,p.getZ(i)*sc);const snow=t>.6+Math.sin(a*9)*.05+n;const cc=snow?new THREE.Color('#f4f7fb'):new THREE.Color().setHSL(.07,.18,.42+t*.12);c.push(cc.r,cc.g,cc.b);}
      g.setAttribute('color',new THREE.Float32BufferAttribute(c,3));g.computeVertexNormals();const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({vertexColors:true,roughness:1,fog:false,transparent:true,opacity:.92}));m.position.set(x,h/2-2,z);scene.add(m);return m;};
    mk(330,190,-260,MH_+640,3);mk(150,95,-560,MH_+560,9);
    const hills=new THREE.Mesh(new THREE.TorusGeometry(1050,90,8,64),new THREE.MeshStandardMaterial({color:'#b8a487',roughness:1,fog:false,transparent:true,opacity:.6}));hills.rotation.x=Math.PI/2;hills.scale.z=.35;hills.position.set(MW_/2,0,MH_/2);scene.add(hills);}
  // ---------------- Yerevan street life & landmarks (v5)
  {const D=k=>W.decor.filter(d=>d.k===k);const X=d=>d.x*U,Z=d=>d.y*U;
    // kiosks with Armenian signs
    const KN=[['ՇԱՈՒՐՄԱ','#c2452f'],['ԼԱՀՄԱՋՈ','#b23a2a'],['ՄԱՄՈՒԼ','#2f4f8a'],['ԾԱՂԻԿՆԵՐ','#b8457a'],['ԼՈՏՈ «ԲԱԽՏ»','#d9a01a'],['ՍՈՒՐՃ ՏԱՐԱՅՈՎ','#6b3f25'],['ՊԱՂՊԱՂԱԿ','#3a9ad9'],['ՍԵՐՄԵՐ ԵՎ ՉԻՐ','#7a4a1f']];
    D('kiosk').forEach(d=>{const [t,c]=KN[d.v%KN.length];const g=new THREE.Group();g.add(mesh(MERGE([P(box(2.2,2.3,1.6),'#e9e4da',0,1.15,0),P(box(1.9,1.2,.05),'#7fb2d1',0,1.35,.81),P(box(2.5,.12,1.2),c,0,2.45,.9,.25),P(box(2.3,.08,1.8),'#bdb6aa',0,2.34,0)])));
      const s=new THREE.Mesh(new THREE.PlaneGeometry(2.1,.42),new THREE.MeshStandardMaterial({map:signTex(t,c,shadeC(c,.75),768,150,80),emissive:'#ffffff',emissiveIntensity:.1}));s.position.set(0,2.05,.82);g.add(s);g.position.set(X(d),0,Z(d));g.rotation.y=-Math.PI/2;scene.add(g);});
    // pulpulaks — Yerevan's tuff drinking fountains
    const pp=D('pulpulak');inst(MERGE([P(cyl(.24,.3,1.05,8),'#d98f6e',0,.52,0),P(cyl(.32,.32,.12,8),'#c27a5c',0,1.08,0),P(cyl(.4,.42,.1,12),'#9d8f84',0,.05,0),P(cyl(.03,.03,.22,6),'#c9ccd1',0,1.0,.22,Math.PI/2)]),pp,(d,m)=>m.makeTranslation(X(d),0,Z(d)));
    pp.forEach(d=>{const c=new THREE.QuadraticBezierCurve3(new V3(X(d),1.02,Z(d)+.33),new V3(X(d),1.25,Z(d)+.55),new V3(X(d),.12,Z(d)+.72));const w=new THREE.Mesh(new THREE.TubeGeometry(c,10,.025,5),new THREE.MeshStandardMaterial({color:'#bfe6ff',transparent:true,opacity:.75,roughness:.05}));scene.add(w);});
    // park fountains
    D('fountain').forEach(d=>{scene.add(mesh(MERGE([P(cyl(2.4,2.6,.55,28),'#d6c1a3',X(d),.27,Z(d)),P(cyl(2.15,2.15,.57,28),'#4aaee0',X(d),.29,Z(d)),P(cyl(.35,.45,1.2,10),'#cbb79a',X(d),.6,Z(d))])));fountains.push({x:X(d),z:Z(d),sx:1.3,sz:1.3,n:isMobile?60:120,h:2});});
    // old men playing nardi on a bench (very Yerevan)
    D('oldmen').forEach(d=>{const nt=narTex();const t=new THREE.Group();t.add(mesh(MERGE([P(box(1.4,.08,.9),'#7a4f2c',0,.78,0),P(box(.1,.78,.1),'#5a3a20',0,.39,0),P(box(1.6,.45,.45),'#8a6243',0,.23,-1.05),P(box(1.6,.45,.45),'#8a6243',0,.23,1.05)])));
      const top=new THREE.Mesh(new THREE.PlaneGeometry(1.2,.75),new THREE.MeshStandardMaterial({map:nt,roughness:.7}));top.rotation.x=-Math.PI/2;top.position.y=.83;t.add(top);t.position.set(X(d),0,Z(d));scene.add(t);
      [[1,'#5b5b66','#3d4b5c'],[-1,'#4e4a44','#6b5a47']].forEach(([s,cap,sh])=>{const o=makeChar({skin:'#e3a87e',shirt:sh,pants:'#33333b',hat:'flat',must:true,hair:'#bbb'});seat(o);o.position.set(X(d),.02,Z(d)+s*1.05);o.rotation.y=s>0?Math.PI:0;SITTERS.push(o);});});
    // playgrounds in Soviet yards
    D('playground').forEach(d=>{const x=X(d),z=Z(d);scene.add(mesh(MERGE([P(box(.1,2.4,.1),'#c0392b',x-1.2,1.2,z-.6),P(box(.1,2.4,.1),'#c0392b',x+1.2,1.2,z-.6),P(box(2.5,.1,.1),'#c0392b',x,2.4,z-.6),P(box(.6,.06,.3),'#2e86c1',x-.4,.6,z-.6),P(box(.6,.06,.3),'#2e86c1',x+.5,.6,z-.6),
      P(box(.04,1.8,.04),'#888',x-.6,1.5,z-.6),P(box(.04,1.8,.04),'#888',x-.2,1.5,z-.6),P(box(.04,1.8,.04),'#888',x+.3,1.5,z-.6),P(box(.04,1.8,.04),'#888',x+.7,1.5,z-.6),
      P(box(.7,.08,2.4),'#f1c40f',x+2.6,.75,z+.6,.55),P(box(.9,1.5,.9),'#27ae60',x+2.6,.75,z-.6),P(box(2.4,.3,2.4),'#d9c08a',x-2.4,.15,z+1),P(box(2.6,.32,.12),'#a0522d',x-2.4,.16,z+2.2)])));});
    // courtyard: laundry lines between the facing buildings, metal garages
    D('laundry').forEach(d=>{const z1=Z({y:d.y}),z2=Z({y:d.y2}),hgt=6.5+rand()*3;for(let k=0;k<3;k++){const x=X(d)+k*4+rand();const l=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,z2-z1,4),new THREE.MeshBasicMaterial({color:'#555'}));l.rotation.x=Math.PI/2;l.position.set(x,hgt-k*.6,(z1+z2)/2);scene.add(l);
      const n=4+((rand()*5)|0);for(let j=0;j<n;j++){const c=new THREE.Mesh(new THREE.PlaneGeometry(.5+rand()*.4,.6+rand()*.5),new THREE.MeshStandardMaterial({color:rp(['#e2574c','#5fb7e8','#f2c94c','#ffffff','#7fcf6a','#c58cf0','#ff9f43','#2c3e50']),side:THREE.DoubleSide,roughness:.9}));c.position.set(x,hgt-k*.6-.4,z1+.8+j*(z2-z1-1.6)/n);c.rotation.y=Math.PI/2;c.userData.ph=rand()*7;CLOTHES.push(c);scene.add(c);}}});
    D('garage').forEach(d=>scene.add(mesh(MERGE([P(new THREE.CylinderGeometry(1.4,1.4,3.6,14,1,false,0,Math.PI),'#5d7a6a',X(d),.05,Z(d),Math.PI/2,0,0),P(box(.05,2.4,2.6),'#4f6a5b',X(d)+1.8,1.2,Z(d))]),CARM)));
    // cafés of Northern Avenue: tables, umbrellas, people sitting
    D('cafe').forEach((d,i)=>{const x=X(d),z=Z(d);const uc=['#f2efe6','#c0392b','#2c3e50','#d4a017'][i%4];scene.add(mesh(MERGE([P(cyl(.45,.45,.05,14),'#f4f4f4',x-1.6,.75,z),P(cyl(.05,.05,.75,6),'#444',x-1.6,.37,z),P(cyl(.45,.45,.05,14),'#f4f4f4',x+1.6,.75,z),P(cyl(.05,.05,.75,6),'#444',x+1.6,.37,z),
      P(cyl(.04,.04,2.6,6),'#555',x-1.6,1.3,z),P(new THREE.ConeGeometry(1.5,.6,8),uc,x-1.6,2.6,z),P(cyl(.04,.04,2.6,6),'#555',x+1.6,1.3,z),P(new THREE.ConeGeometry(1.5,.6,8),uc,x+1.6,2.6,z)])));
      if(i%2===0){const o=makeChar({skin:'#f1c6a0',shirt:rp(['#e2574c','#f4f4f4','#2c3e50','#8e44ad']),pants:'#2a2a3a',hair:rp(['#2a1d1a','#5a2d1a']),long:rand()<.5});seat(o);o.position.set(x-1.6,.02,z+.75);o.rotation.y=Math.PI;SITTERS.push(o);}});
    // Vernissage: carpets, paintings, souvenirs
    D('vstall').forEach(d=>{const x=X(d),z=Z(d);const g=new THREE.Group();g.add(mesh(MERGE([P(box(2,.08,1),'#8a6243',0,.8,0),P(box(.08,.8,.08),'#555',-.9,.4,-.4),P(box(.08,.8,.08),'#555',.9,.4,.4),P(box(.08,.8,.08),'#555',.9,.4,-.4),P(box(.08,.8,.08),'#555',-.9,.4,.4),P(box(.08,2.4,.08),'#555',-1,1.2,-.6),P(box(.08,2.4,.08),'#555',1,1.2,-.6),P(box(2.1,.06,.06),'#555',0,2.35,-.6)])));
      const cp=new THREE.Mesh(new THREE.PlaneGeometry(1.8,1.4),new THREE.MeshStandardMaterial({map:carpetTex(d.v),side:THREE.DoubleSide,roughness:.95}));cp.position.set(0,1.6,-.58);g.add(cp);g.position.set(x,0,z);scene.add(g);});
    // sculptures in the Tamanyan garden (abstract, modern)
    D('sculpt').forEach(d=>{const bronze=new THREE.MeshStandardMaterial({color:'#5a4632',metalness:.85,roughness:.35});const g=new THREE.Group();g.add(mesh(P(box(1.6,.8,1.6),'#d9cbb6',0,.4,0)));
      const s=new THREE.Mesh(d.v===0?new THREE.TorusKnotGeometry(.55,.16,90,12):d.v===1?new THREE.TorusGeometry(.8,.18,14,40):new THREE.IcosahedronGeometry(.75,0),bronze);s.position.y=1.6;s.castShadow=true;g.add(s);g.position.set(X(d),0,Z(d));scene.add(g);SPIN.push(s);});
    // Armenian flags (government house, Opera, university)
    const flagAt=(x,y,z,s=1)=>{const g=new THREE.Group();g.add(mesh(P(cyl(.05,.06,4.5*s,6),'#ccc',0,2.25*s,0)));const geo=new THREE.PlaneGeometry(2*s,1*s,14,6);geo.translate(1*s,0,0);const f=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({map:flagTex(),side:THREE.DoubleSide,roughness:.8}));f.position.y=3.9*s;f.userData.base=geo.attributes.position.array.slice();g.add(f);FLAGS.push(f);g.position.set(x,y,z);scene.add(g);};
    {const gv=W.buildings.find(b=>b.kind==='gov');if(gv){flagAt(gv.x3+gv.w3/2,gv.h3+8,gv.z3+gv.d3/2,1.2);flagAt(gv.x3+2,0,gv.z3+gv.d3+2);flagAt(gv.x3+gv.w3-2,0,gv.z3+gv.d3+2);}
     const un=W.buildings.find(b=>b.kind==='uni');if(un)flagAt(un.x3+un.w3/2,0,un.z3+un.d3+3.5);const op=W.buildings.find(b=>b.kind==='opera');if(op)flagAt(op.x3+op.w3/2,op.h3+3,op.z3+op.d3/2);}
    // trolleybus line along the avenue (poles + overhead wires) and two trolleybuses
    {const ry=(HR[3]+1)*2,poles=[],wires=[];for(let x=VR[0]*2;x<MW_;x+=12){poles.push([x,ry-2.4]);poles.push([x,ry+2.4]);}
      inst(MERGE([P(cyl(.08,.11,7,6),'#5c636b',0,3.5,0),P(box(.06,.06,2.6),'#5c636b',0,6.8,0)]),poles,(v,m)=>m.compose(_p.set(v[0],0,v[1]),_q.setFromEuler(_e.set(0,0,0)),_s.set(1,1,1)));
      [-1.2,-.8,.8,1.2].forEach(o=>{const w=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,MW_-VR[0]*2,4),new THREE.MeshBasicMaterial({color:'#2a2a2a'}));w.rotation.z=Math.PI/2;w.position.set((MW_+VR[0]*2)/2,6.6,ry+o);scene.add(w);});
      for(let k=0;k<2;k++){const t=makeTrolley();t.userData={x:VR[0]*2+20+k*90,dir:k?-1:1,lane:ry+(k?-1:1)*1.0};TROLLEYS.push(t);}}
    // traffic lights at central crossings
    {const tl=[];VR.forEach((x,i)=>HR.forEach((y,j)=>{if(i>=2&&i<=6&&j>=0&&j<=5)tl.push([x*2-.9,y*2-.9],[x*2+4.9,y*2+4.9]);}));
      inst(MERGE([P(cyl(.07,.09,3.4,6),'#2b2f36',0,1.7,0),P(box(.34,1.0,.3),'#1d2026',0,3.4,0)]),tl,(v,m)=>m.makeTranslation(v[0],0,v[1]));
      TLIGHT.im=new THREE.InstancedMesh(new THREE.SphereGeometry(.11,8,6),new THREE.MeshBasicMaterial({toneMapped:false}),tl.length);tl.forEach((v,i)=>{TLIGHT.im.setMatrixAt(i,_m.makeTranslation(v[0],3.5,v[1]+.16));TLIGHT.im.setColorAt(i,new THREE.Color('#ff3b30'));});TLIGHT.n=tl.length;scene.add(TLIGHT.im);}
    // TV tower on the Nork hill (east) and the Victory park Ferris wheel (north)
    {const g=new THREE.Group();const H=150;for(let k=0;k<10;k++){const r0=9-k*.8,r1=9-(k+1)*.8;g.add(new THREE.Mesh(new THREE.CylinderGeometry(Math.max(.6,r1),Math.max(.8,r0),H/10,8,1,true),new THREE.MeshStandardMaterial({color:k%2?'#f2f2f2':'#d23a2a',wireframe:k<7,fog:false})));g.children[k].position.y=H/20+k*H/10;}
      g.add(new THREE.Mesh(new THREE.CylinderGeometry(4,4,5,12),new THREE.MeshStandardMaterial({color:'#e9e9e9',fog:false})));g.children[10].position.y=H*.72;const sp=new THREE.Mesh(new THREE.CylinderGeometry(.3,.6,30,6),new THREE.MeshStandardMaterial({color:'#d23a2a',fog:false}));sp.position.y=H+15;g.add(sp);
      const hill=new THREE.Mesh(new THREE.SphereGeometry(120,24,12,0,Math.PI*2,0,Math.PI/2),new THREE.MeshStandardMaterial({color:'#9c8a62',roughness:1,fog:false}));hill.scale.y=.35;g.add(hill);g.position.set(MW_+190,0,MH_*.35);scene.add(g);}
    {const g=new THREE.Group();const hill=new THREE.Mesh(new THREE.SphereGeometry(110,24,12,0,Math.PI*2,0,Math.PI/2),new THREE.MeshStandardMaterial({color:'#7f9a5a',roughness:1}));hill.scale.y=.3;g.add(hill);
      const wheel=new THREE.Group();const R=16;const rim=new THREE.Mesh(new THREE.TorusGeometry(R,.35,6,48),new THREE.MeshStandardMaterial({color:'#eaeaea'}));wheel.add(rim);for(let k=0;k<12;k++){const sp=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,R*2,4),new THREE.MeshStandardMaterial({color:'#cfcfcf'}));sp.rotation.z=k*Math.PI/12;wheel.add(sp);
        const cab=new THREE.Mesh(new THREE.BoxGeometry(1.6,1.8,1.6),new THREE.MeshStandardMaterial({color:['#e74c3c','#f1c40f','#3498db','#2ecc71'][k%4]}));cab.position.set(Math.cos(k*Math.PI/6)*R,Math.sin(k*Math.PI/6)*R,0);wheel.add(cab);}
      wheel.position.set(0,33+R,0);g.add(wheel);g.add(mesh(MERGE([P(box(1,34+R,1),'#bdbdbd',-6,(34+R)/2,0,0,0,.18),P(box(1,34+R,1),'#bdbdbd',6,(34+R)/2,0,0,0,-.18)])));
      const ob=mesh(MERGE([P(box(10,6,10),'#b58a6a',30,33,0),P(box(4,40,4),'#a87e60',30,56,0)]));g.add(ob);g.position.set(MW_*.62,0,-95);scene.add(g);WHEEL.o=wheel;}
    // Hrazdan gorge: the far (west) bank rises as a cliff
    {const g=new THREE.PlaneGeometry(36,MH_+300,12,60);const p=g.attributes.position;for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i);const t=(x+18)/36;p.setZ(i,(1-t)*(28+Math.sin(y*.11)*6+Math.sin(y*.37)*2.5)+rand()*1.2);}g.computeVertexNormals();
      const cl=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:'#9b7d5f',roughness:1,flatShading:true}));cl.rotation.x=-Math.PI/2;cl.position.set(-50,0,MH_/2);cl.receiveShadow=true;scene.add(cl);
      HR.forEach(y=>{const z=(y+1)*2;scene.add(mesh(MERGE([P(box(12,.9,.35),'#d9c3a3',-1,.45,z+2.2),P(box(12,.9,.35),'#d9c3a3',-1,.45,z-2.2),...[0,1,2].map(k=>P(cyl(.06,.08,3.5,6),'#3a3f4a',-5+k*4,1.75,z+2.3))])));});}
  }
  // hub gate ring, target ring, lost stone, GPS ribbon
  hubRing=new THREE.Mesh(new THREE.RingGeometry(2.4,2.9,48),new THREE.MeshBasicMaterial({color:'#ffb347',transparent:true,opacity:.85,toneMapped:false,side:THREE.DoubleSide}));hubRing.rotation.x=-Math.PI/2;scene.add(hubRing);
  targetRing=new THREE.Mesh(new THREE.RingGeometry(1.4,1.8,48),new THREE.MeshBasicMaterial({color:'#ffd84d',transparent:true,opacity:.95,toneMapped:false,side:THREE.DoubleSide,depthWrite:false}));targetRing.rotation.x=-Math.PI/2;scene.add(targetRing);
  {const beam=new THREE.Mesh(new THREE.CylinderGeometry(.9,.9,26,24,1,true),new THREE.MeshBasicMaterial({color:'#ffd84d',transparent:true,opacity:.16,toneMapped:false,depthWrite:false,side:THREE.DoubleSide}));beam.position.y=13;targetRing.add(beam);beam.rotation.x=Math.PI/2;beam.position.set(0,0,-13);}
  stoneMesh=new THREE.Mesh(new THREE.SphereGeometry(.28,16,12),new THREE.MeshStandardMaterial({color:'#ffffff',emissive:'#fff6b0',emissiveIntensity:1.2}));scene.add(stoneMesh);
  gpsTex=dashTex();gpsTex.repeat.set(1,1);gpsMesh=new THREE.Mesh(new THREE.BufferGeometry(),new THREE.MeshBasicMaterial({map:gpsTex,transparent:true,depthWrite:false,toneMapped:false,side:THREE.DoubleSide}));gpsMesh.renderOrder=2;scene.add(gpsMesh);
  // lockers (one per slot) + free-slot rings
  const lt=lockerTex(),lfm=new THREE.MeshStandardMaterial({map:lt,roughness:.4}),lmat=[VCM,VCM,VCM,VCM,lfm,lfm];
  W.slots.forEach((s,i)=>{const g=new THREE.Group();const b=new THREE.Mesh(paint(new THREE.BoxGeometry(2.6,2.4,.9),'#1d9a5e'),lmat);b.position.y=1.3;b.castShadow=b.receiveShadow=true;g.add(b);
    g.add(mesh(MERGE([P(box(2.8,.15,1.1),'#e8fff2',0,2.58,0),P(box(2.7,.12,1),'#555',0,.06,0)])));g.position.set(s.x*U,0,s.y*U);scene.add(g);lockers.push(g);
    const r=new THREE.Mesh(new THREE.RingGeometry(1.5,1.75,40),new THREE.MeshBasicMaterial({color:'#ffffff',transparent:true,opacity:.7,toneMapped:false,side:THREE.DoubleSide}));r.rotation.x=-Math.PI/2;r.position.set(s.x*U,.08,s.y*U);scene.add(r);freeRings.push(r);});
  W.pudos.forEach(u=>{scene.add(mesh(MERGE([P(cyl(.06,.06,2.6,6),'#555',u.x*U,1.3,u.y*U),P(box(1.3,.8,.1),'#2f86c8',u.x*U,2.6,u.y*U)])));});
  // fountains particles
  fountains.forEach(f=>{const g=new THREE.BufferGeometry();const pos=new Float32Array(f.n*3);g.setAttribute('position',new THREE.BufferAttribute(pos,3));f.seed=Array.from({length:f.n},()=>[rand()*7,rand(),rand()]);
    f.pts=new THREE.Points(g,new THREE.PointsMaterial({color:'#e6f7ff',size:.22,map:dropTex,transparent:true,opacity:.8,depthWrite:false,alphaTest:.05}));scene.add(f.pts);});
  // police car (event) + rain + confetti
  policeCar=makeCar('police','#f4f6f8');policeCar.visible=false;policeLights=new THREE.Mesh(new THREE.BoxGeometry(.9,.18,.3),new THREE.MeshBasicMaterial({color:'#ff2d2d',toneMapped:false}));policeLights.position.set(0,1.62,-.2);policeCar.add(policeLights);{const cop=makeChar(R3.POLICE);scene.remove(cop);cop.position.set(1.6,0,.6);cop.rotation.y=Math.PI/2;cop.userData.inner.children[0];policeCar.add(cop);policeCar.userData.cop=cop;}
  {const n=1400,g=new THREE.BufferGeometry(),p=new Float32Array(n*6);g.setAttribute('position',new THREE.BufferAttribute(p,3));rainMesh=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:'#cfe7ff',transparent:true,opacity:.45}));rainMesh.visible=false;rainMesh.frustumCulled=false;scene.add(rainMesh);rainMesh.userData.d=Array.from({length:n},()=>[rand()*80-40,rand()*40,rand()*80-40]);}
  confetti={im:new THREE.InstancedMesh(new THREE.PlaneGeometry(.18,.12),new THREE.MeshBasicMaterial({side:THREE.DoubleSide,toneMapped:false}),160),p:[]};confetti.im.count=0;confetti.im.frustumCulled=false;scene.add(confetti.im);
}
const dropTex=(()=>{const [c,g]=cnv(32,32);const gr=g.createRadialGradient(16,16,1,16,16,15);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gr;g.fillRect(0,0,32,32);return tex(c,false);})();
function smokeTex(){const [c,g]=cnv(64,64);const gr=g.createRadialGradient(32,32,2,32,32,30);gr.addColorStop(0,'rgba(240,240,245,.9)');gr.addColorStop(1,'rgba(240,240,245,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);return tex(c,false);}
function carpetTex(v){const [c,g]=cnv(256,200);const pal=[['#8e1b1b','#d9b26a','#1f3c6e','#f2e6c9'],['#6e1420','#e0c08a','#2d5a3a','#f4ead2'],['#1f3c6e','#c9a35a','#8e1b1b','#efe2c4'],['#a3471f','#f0d69a','#3a2a5a','#f6ecd6'],['#5a1a2a','#d8b46a','#245a6a','#f1e4c8'],['#7a2a12','#e7c27a','#20446e','#f3e7cf']][v%6];
  if(v%3===2){g.fillStyle='#f3efe6';g.fillRect(0,0,256,200);g.fillStyle='#6a4a2a';g.fillRect(0,0,256,200);g.fillStyle='#f6f0e2';g.fillRect(14,14,228,172);const gr=g.createLinearGradient(0,14,0,186);gr.addColorStop(0,'#9fc6e6');gr.addColorStop(.55,'#f2d39a');gr.addColorStop(.56,'#9a8a6a');gr.addColorStop(1,'#6f7f4a');g.fillStyle=gr;g.fillRect(22,22,212,156);
    g.fillStyle='#f6f8fb';g.beginPath();g.moveTo(60,110);g.lineTo(120,50);g.lineTo(170,110);g.fill();g.fillStyle='#e9eef4';g.beginPath();g.moveTo(150,112);g.lineTo(185,80);g.lineTo(215,112);g.fill();return tex(c,false);}
  g.fillStyle=pal[0];g.fillRect(0,0,256,200);g.strokeStyle=pal[1];g.lineWidth=8;g.strokeRect(10,10,236,180);g.strokeStyle=pal[2];g.lineWidth=5;g.strokeRect(22,22,212,156);
  for(let k=0;k<3;k++){const cx=64+k*64,cy=100;g.fillStyle=pal[1];g.beginPath();g.moveTo(cx,cy-38);g.lineTo(cx+26,cy);g.lineTo(cx,cy+38);g.lineTo(cx-26,cy);g.fill();g.fillStyle=pal[2];g.beginPath();g.moveTo(cx,cy-22);g.lineTo(cx+14,cy);g.lineTo(cx,cy+22);g.lineTo(cx-14,cy);g.fill();g.fillStyle=pal[3];g.fillRect(cx-4,cy-4,8,8);}
  for(let i=0;i<30;i++){g.fillStyle=pal[(i%3)+1];g.fillRect(28+i*7,28,4,6);g.fillRect(28+i*7,166,4,6);}return tex(c,false);}
function flagTex(){const [c,g]=cnv(240,120);['#d90012','#0033a0','#f2a800'].forEach((col,i)=>{g.fillStyle=col;g.fillRect(0,i*40,240,40);});return tex(c,false);}
function seat(o){const u=o.userData;u.sit=true;u.inner.position.y=-.43;u.legs.forEach(l=>l.rotation.x=-1.5);u.knees.forEach(k=>k.rotation.x=1.5);u.arms.forEach(a=>a.rotation.x=-.6);u.elbows.forEach(e=>e.rotation.x=-.7);}
function makeTrolley(){const B=[];const c='#3d7fc4';B.push(P(box(2.5,2.6,11),c,0,1.6,0),P(box(2.52,1.1,9.6),'#22303d',0,2.15,-.2),P(box(2.3,.95,.06),'#22303d',0,2.1,5.52),P(box(2.54,.35,11.04),'#e9eef2',0,.55,0),P(box(1.6,.25,3),'#9aa3ad',0,3.05,-1),
  P(box(.06,.06,5.5),'#333',-.5,4.2,-2.5,-.38),P(box(.06,.06,5.5),'#333',.5,4.2,-2.5,-.38));[[1.1,3.6],[-1.1,3.6],[1.1,-3.4],[-1.1,-3.4]].forEach(([x,z])=>{B.push(P(cyl(.5,.5,.3,14),'#1a1a1f',x,.5,z,0,0,Math.PI/2));});
  [-1,1].forEach(s=>B.push(P(box(.3,.14,.05),'#fff7d0',s*.8,.9,5.52)));const g=new THREE.Group();g.add(mesh(MERGE(B),CARM));scene.add(g);return g;}
function narTex(){const [c,g]=cnv(256,160);g.fillStyle='#e8c690';g.fillRect(0,0,256,160);g.fillStyle='#7a4f2c';g.fillRect(124,0,8,160);g.strokeStyle='#7a4f2c';g.lineWidth=8;g.strokeRect(4,4,248,152);
  for(let k=0;k<12;k++){g.fillStyle=k%2?'#b5482f':'#3a5a8a';const x=10+(k%6)*19+(k>=6?128:0);g.beginPath();g.moveTo(x,8);g.lineTo(x+9,62);g.lineTo(x+18,8);g.fill();g.beginPath();g.moveTo(x,152);g.lineTo(x+9,98);g.lineTo(x+18,152);g.fill();}
  [[40,80,'#fff'],[60,84,'#fff'],[180,76,'#222'],[200,82,'#222']].forEach(([x,y,cc])=>{g.fillStyle=cc;g.beginPath();g.arc(x,y,9,0,7);g.fill();});return tex(c,false);}
function special(b,x0,z0,w,d,props){const k=b.kind;let h=8,mat;
  const addSign=(text,c1,c2,y,wd=Math.min(w-1,14),z=z0+d+.12)=>{const s=new THREE.Mesh(new THREE.PlaneGeometry(wd,wd*.2),new THREE.MeshStandardMaterial({map:signTex(text,c1,c2),roughness:.5,emissive:'#ffffff',emissiveIntensity:.12}));s.position.set(x0+w/2,y,z);scene.add(s);return s;};
  const blk=(m,hh)=>{const q=quadBuilder();wallsInto(q,x0,z0,w,d,hh);const mm=new THREE.Mesh(q.geo(),m);mm.castShadow=mm.receiveShadow=true;scene.add(mm);const r=quadBuilder();roofInto(r,x0,z0,w,d,hh);const rm=new THREE.Mesh(r.geo(),new THREE.MeshStandardMaterial({color:'#bdb6ad',roughness:.95}));rm.receiveShadow=true;scene.add(rm);};
  if(k==='hub'){h=7;const t=corrugTex();t.repeat.set(5,1.6);blk(new THREE.MeshStandardMaterial({map:t,roughness:.45,metalness:.4}),h);
    for(let i=0;i<3;i++)props.push(P(box(3.2,4.2,.15),'#5b6472',x0+3+i*4.2,2.1,z0+d+.05),...[0,1,2,3,4,5].map(j=>P(box(3.2,.05,.17),'#7d8794',x0+3+i*4.2,.6+j*.65,z0+d+.06)));
    props.push(P(box(w,.3,1.6),'#9aa3ad',x0+w/2,.15,z0+d+.8));addSign('ՄՂՈՆ ԷՔՍՊՐԵՍ','#ffb347','#ff7a1a',h-1.2,Math.min(w-2,11));}
  else if(k==='uni'){h=15;blk(new THREE.MeshStandardMaterial({map:facadeTex('#e9c9a0','tuff'),roughness:.85}),h);
    for(let i=0;i<6;i++)props.push(P(cyl(.4,.45,7,14),'#f2e3cc',x0+w/2-6.25+i*2.5,3.5,z0+d+1.3));props.push(P(box(16,.8,2.6),'#efdcc0',x0+w/2,7.3,z0+d+1.2),P(box(16,.4,3),'#d9c4a6',x0+w/2,.2,z0+d+1.3));
    addSign('ՀԱՊՀ · ՊՈԼԻՏԵԽՆԻԿ','#3a4a6b','#2a3550',8.6,12,z0+d+2.55);}
  else if(k==='gov'){h=12;const t=arcadeTex();t.repeat.set(3,1.4);blk(new THREE.MeshStandardMaterial({map:t,roughness:.8}),h);
    props.push(P(box(4,8,4),'#e7a074',x0+w/2,h+4,z0+d/2),P(cyl(1.3,1.3,.2,24),'#f5f0e6',x0+w/2,h+6,z0+d/2+2.05,Math.PI/2),P(box(4.4,.6,4.4),'#c98a5e',x0+w/2,h+8.3,z0+d/2),P(new THREE.ConeGeometry(2.6,3,4),'#7a8f5e',x0+w/2,h+10,z0+d/2,0,Math.PI/4));}
  else if(k==='market'){h=7;blk(new THREE.MeshStandardMaterial({map:facadeTex('#e9b27a','tuff'),roughness:.85}),h);
    const vault=new THREE.Mesh(new THREE.CylinderGeometry(d/2,d/2,w,24,1,false,0,Math.PI),new THREE.MeshStandardMaterial({map:glassTex(),roughness:.15,metalness:.3,transparent:true,opacity:.92}));vault.rotation.z=Math.PI/2;vault.position.set(x0+w/2,h,z0+d/2);vault.castShadow=true;scene.add(vault);
    addSign('ԳՈՒՄ ՇՈՒԿԱ','#4fa860','#3a8a4b',h-1.3);}
  else if(k==='opera'){h=12;const cx=x0+w/2,cz=z0+d/2;const at=arcadeTex();at.repeat.set(8,1);const am=new THREE.MeshStandardMaterial({map:at,roughness:.8});
    const drum=new THREE.Mesh(new THREE.CylinderGeometry(w*.44,w*.46,8,40,1,true),am);drum.position.set(cx,4.6,cz);drum.castShadow=drum.receiveShadow=true;scene.add(drum);
    const t2=arcadeTex();t2.repeat.set(10,1);const up=new THREE.Mesh(new THREE.CylinderGeometry(w*.33,w*.34,3.4,40,1,true),new THREE.MeshStandardMaterial({map:t2,roughness:.8}));up.position.set(cx,10.2,cz);up.castShadow=true;scene.add(up);
    props.push(P(cyl(w*.5,w*.52,.6,40),'#cdb79a',cx,.3,cz),P(cyl(w*.47,w*.47,.5,40),'#d9b08a',cx,8.75,cz),P(cyl(w*.35,w*.35,.4,40),'#d9b08a',cx,12,cz),P(new THREE.SphereGeometry(w*.33,30,10,0,Math.PI*2,0,Math.PI/2),'#a9a39a',cx,12.1,cz,0,0,0,1,.28,1));
    for(let i=0;i<8;i++)props.push(P(cyl(.32,.36,6.4,12),'#efe0c8',cx-4.4+i*1.25,3.8,z0+d+.9));props.push(P(box(11,.7,2.4),'#e3c9a6',cx,7.3,z0+d+.9),P(box(11,.3,3.2),'#cdb79a',cx,.15,z0+d+1.1));
    addSign('ՕՊԵՐԱՅԻ ԵՎ ԲԱԼԵՏԻ ԹԱՏՐՈՆ','#6b3f25','#4e2c18',8.2,10,z0+d+2.15);}
  else if(k==='mall'){h=11;const t=glassTex();t.repeat.set(4,4);blk(new THREE.MeshStandardMaterial({map:t,roughness:.08,metalness:.5}),h);addSign('ԵՐԵՎԱՆ ՄՈԼ','#7d6bd6','#5f4fb8',h-1.4);}
  else if(k==='kyabab'){h=4;blk(new THREE.MeshStandardMaterial({map:facadeTex('#e8925e','tuff'),roughness:.85}),h);
    for(let i=0;i<8;i++)props.push(P(box(w/8,.08,1.6),i%2?'#ffffff':'#d9483b',x0+w/16+i*w/8,3.1,z0+d+.7,.35));props.push(P(cyl(.25,.25,2,8),'#555',x0+w-1,h+1,z0+1.2));addSign('ՔՅԱԲԱԲ ՀԱՅԿՈ','#e8573d','#c03a2a',h+.9,7,z0+d-.2);}
  else if(k==='pudo'){h=3.4;{const t=glassTex();t.repeat.set(4,4);blk(new THREE.MeshStandardMaterial({map:t,roughness:.2,metalness:.3,color:'#bfe6ff'}),h);}addSign('ԱՆՈՒՇ · ՍՏԱՑՄԱՆ ԿԵՏ','#3b9ad6','#2577b3',h+.6,7.5);}
  else{blk(new THREE.MeshStandardMaterial({map:facadeTex('#e3a374','tuff')}),h);}
  b.h3=h;}

/* ---------------------------------------------------------------- DYNAMIC OBJECTS */
const O={player:null,myNiva:null,ashotNiva:null,npc:new Map(),bots:[],walkers:[],cars:[],dancers:[]};
function initDynamic(){
  O.myNiva=makeCar('myniva','#f2efe8');
  O.cargo=new THREE.InstancedMesh(paint(new THREE.BoxGeometry(.5,.38,.5),'#d9a066'),VCM,10);O.cargo.castShadow=true;O.myNiva.add(O.cargo);
  O.ashotNiva=makeCar('niva','#5f8a3a');
  NPC.forEach(n=>{O.npc.set(n.id,n.dog?makeDog():makeChar(n.look,n.id==='prof'?1.02:1));});
  O.bots=bots.map(b=>makeChar({...b.look,hat:b.look.hat==='none'?undefined:b.look.hat}));
  O.walkers=walkers.map(w=>makeChar({...w.look,hat:w.look.hat==='none'?undefined:w.look.hat},.97));
  O.cars=cars.map(c=>makeCar(c.kind,c.color));
  O.dancers=Array.from({length:8},(_,k)=>{const o=makeChar({skin:'#f1c39c',shirt:k===0?'#ffffff':['#e2574c','#4fa3e0','#f2c94c','#9b7be0'][k%4],pants:k===0?'#ffffff':'#2a2a3a',hair:'#2a1d1a',long:k===0});o.visible=false;return o;});
  O.eventNiva=makeCar('niva','#5f8a3a');O.eventNiva.visible=false;}
let playerLookKey='';
function ensurePlayer(){const k=JSON.stringify(meLook());if(k!==playerLookKey){if(O.player)scene.remove(O.player);O.player=makeChar(meLook());playerLookKey=k;}}

/* ---------------------------------------------------------------- LABELS (DOM, crisp Armenian text) */
const labRoot=document.getElementById('lab');const LBL=new Map();let frameId=0;const _v=new V3();
function L(key,x,y,h,html,cls='',maxD=1e9){const W2=innerWidth,H2=innerHeight;_v.set(x*U,h,y*U);const dd=_v.distanceTo(camera.position);if(dd>maxD)return null;_v.project(camera);if(_v.z>1||_v.x<-1.2||_v.x>1.2||_v.y<-1.2||_v.y>1.2)return null;
  let e=LBL.get(key);if(!e){const el=document.createElement('div');el.className='lb';labRoot.appendChild(el);e={el,html:'',cls:''};LBL.set(key,e);}
  if(e.html!==html){e.el.innerHTML=html;e.html=html;}if(e.cls!==cls){e.el.className='lb '+cls;e.cls=cls;}
  e.el.style.transform=`translate(${((_v.x*.5+.5)*W2).toFixed(1)}px,${((-_v.y*.5+.5)*H2).toFixed(1)}px) translate(-50%,-100%)`;e.el.style.display='';e.f=frameId;e.el.style.zIndex=String(1000-Math.round(dd));return e;}
function labelsEnd(){LBL.forEach(e=>{if(e.f!==frameId&&e.el.style.display!=='none')e.el.style.display='none';});}

/* ---------------------------------------------------------------- CAMERA */
const camPos=new V3(),camLook=new V3(),tgt=new V3();let camInit=false;
function camUpdate(dt,px,py,inCar,heading3){const C=R3.cam;tgt.set(px*U,0,py*U);let wantPos,wantLook;
  if(C.mode==='top'){const z=C.zoom*(inCar?1.25:1);wantPos=tgt.clone().add(new V3(0,26*z,15*z));wantLook=tgt.clone().add(new V3(0,0,-1));}
  else if(C.mode==='third'){if(inCar){let d=heading3-C.yaw;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;C.yaw+=d*Math.min(1,dt*3.5);}
    const f=new V3(Math.sin(C.yaw),0,Math.cos(C.yaw));let dist=(inCar?9.5:6.2)*C.zoom,up=inCar?3.6:2.6+C.pitch*-6;
    let blocked=false;for(let s=1;s<=dist;s+=.3){const p=tgt.clone().addScaledVector(f,-s);const sx=-f.z*.8,sz=f.x*.8;if(isSolidPx(p.x/U,p.z/U)||isSolidPx((p.x+sx)/U,(p.z+sz)/U)||isSolidPx((p.x-sx)/U,(p.z-sz)/U)){dist=Math.max(1.4,s-.8);blocked=true;break;}}if(blocked)up+=.5;
    wantPos=tgt.clone().addScaledVector(f,-dist);wantPos.y=up;wantLook=tgt.clone().addScaledVector(f,3);wantLook.y=inCar?1.5:1.5;}
  else{if(inCar){let d=heading3-C.yaw;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;C.yaw+=d*Math.min(1,dt*6);}
    const f=new V3(Math.sin(C.yaw)*Math.cos(C.pitch),Math.sin(C.pitch),Math.cos(C.yaw)*Math.cos(C.pitch));wantPos=tgt.clone();wantPos.y=inCar?1.75:1.72;if(inCar)wantPos.addScaledVector(new V3(Math.sin(C.yaw),0,Math.cos(C.yaw)),.2);wantLook=wantPos.clone().add(f);}
  const k=C.mode==='first'?1:Math.min(1,dt*7);if(!camInit){camPos.copy(wantPos);camLook.copy(wantLook);camInit=true;}camPos.lerp(wantPos,k);camLook.lerp(wantLook,C.mode==='first'?1:Math.min(1,dt*9));
  NEARU.value=C.mode==='third'?(inCar?3.2:2.6):C.mode==='first'?.28:0;camera.position.copy(camPos);camera.lookAt(camLook);camera.fov=C.mode==='first'?72:C.mode==='third'?60:46;camera.updateProjectionMatrix();
  sun.position.copy(tgt).add(SUNOFF);sun.target.position.copy(tgt);sun.target.updateMatrixWorld();}

/* ---------------------------------------------------------------- FRAME */
const yawOf=a=>Math.PI/2-a;   // 2D angle (x right, y down) → three rotation.y (models face +z)
function place(o,x,y,a,h=0){o.position.set(x*U,h,y*U);if(a!=null)o.rotation.y=yawOf(a);}
const dirAng=d=>d===1?Math.PI:d===2?0:d===3?-Math.PI/2:Math.PI/2;
let T0=0;
R3.frame=function(dt){if(!R3.ready)return;frameId++;if(frameId%90===1)patchNear();T0+=dt;const tm=T0,p=G.p,C=R3.cam;
  ensurePlayer();const inCar=p.inVan;
  // player + niva
  const pl=O.player;pl.visible=!(inCar)&&C.mode!=='first';if(!inCar){place(pl,p.x,p.y,p.a!=null?p.a:Math.PI/2);animChar(pl,dt,p.moving,1.1,p.dance>0);}
  place(O.myNiva,G.van.x,G.van.y,G.van.a||0);if(R3.heroWheels){const w=(G.van.sp||0)*U*dt;R3.heroWheels.forEach(h=>{if(!h.stock)h.spin.rotation.x+=h.side*w/h.r;});}O.myNiva.visible=!(inCar&&C.mode==='first');
  {const n=Math.min(10,G.inv.length);O.cargo.count=n;for(let i=0;i<n;i++)O.cargo.setMatrixAt(i,_m.compose(_p.set(-.42+(i%3)*.42,2.25+((i/6)|0)*.4,-1.1+((i%6)/3|0)*.55+((i/6)|0)*.2),_q.setFromEuler(_e.set(0,i*.4,0)),_s.set(1,1,1)));O.cargo.instanceMatrix.needsUpdate=true;}
  {const n=W.places.niva,sh=EV.nivaShake>0?Math.sin(tm*60)*.06:0;O.ashotNiva.position.set(n.x*U+sh,0,n.y*U);O.ashotNiva.rotation.y=Math.PI/2;}
  if(EV.niva){O.eventNiva.visible=true;place(O.eventNiva,EV.niva.x,EV.niva.y,0);}else O.eventNiva.visible=false;
  const near=(x,y,r)=>Math.hypot(x*U-camLook.x,y*U-camLook.z)<r;
  // NPCs
  NPC.forEach(n=>{const o=O.npc.get(n.id);const vis=near(n.x,n.y,90);o.visible=vis;if(!vis)return;
    let a;if(n.talk>0)a=Math.atan2(p.y-n.y,p.x-n.x);else if(n.dog)a=n._a=n.moving?Math.atan2((n._py!=null?n.y-n._py:0),(n._px!=null?n.x-n._px:1)):(n._a||Math.PI/2);else a=n.moving?dirAng(n.dir):Math.PI/2;n._px=n.x;n._py=n.y;
    place(o,n.x,n.y,a);if(n.dog){o.userData.tail.rotation.z=Math.sin(tm*18)*.6;o.position.y=n.moving?Math.abs(Math.sin(tm*14))*.08:0;}else animChar(o,dt,n.moving,.8);});
  bots.forEach((b,i)=>{const o=O.bots[i];const v=near(b.x,b.y,80);o.visible=v;if(v){place(o,b.x,b.y,b.ang||0);animChar(o,dt,true,.9);}});
  walkers.forEach((w,i)=>{const v=near(w.x,w.y,75);const cr=O.crowd&&O.crowd[i];const o=O.walkers[i];o.visible=v&&!cr;if(cr){cr.visible=v;if(v){place(cr,w.x,w.y,w.ang||0);cr.userData.mx.update(dt);}}else if(v){place(o,w.x,w.y,w.ang||0);animChar(o,dt,true,.7);}});
  cars.forEach((c,i)=>{const o=O.cars[i];place(o,c.x,c.y,c.ang||0);o.visible=near(c.x,c.y,160);});updateFleet();
  // wedding dancers
  O.dancers.forEach((o,k)=>{o.visible=EV.wedding>0;if(!o.visible)return;const s=W.places.square,a=k/8*Math.PI*2+tm*.6;place(o,s.x+Math.cos(a)*90,s.y-40+Math.sin(a)*46,a+Math.PI);animChar(o,dt,false,1,1);});
  // police
  if(EV.police){policeCar.visible=true;place(policeCar,EV.police.x,EV.police.y,EV.police.a);policeLights.material.color.set(Math.sin(tm*14)>0?'#ff2d2d':'#2d6bff');}else policeCar.visible=false;
  // lockers
  W.slots.forEach((s,i)=>{lockers[i].visible=!!s.built;freeRings[i].visible=!s.built&&G.co.unlocked;if(freeRings[i].visible)freeRings[i].rotation.z=tm*.5;});
  // rings
  {const h=W.places.hub;hubRing.position.set(h.x*U,.07,h.y*U);const hubAct=(G.q===1&&!G.qd.got)||(G.q===5&&!G.qd.got5)||(G.q===7&&G.bf&&G.bf.n+G.inv.length<8)||G.q===10;hubRing.visible=hubAct;hubRing.scale.setScalar(1+Math.sin(tm*4)*.05);}
  const qt=gps.target;if(qt&&qt.pt){targetRing.visible=true;targetRing.position.set(qt.pt.x*U,.09,qt.pt.y*U);targetRing.scale.setScalar(1+Math.sin(tm*5)*.12);}else targetRing.visible=false;
  if(G.side.lostStone&&!G.side.stoneGot){stoneMesh.visible=true;stoneMesh.position.set(G.side.lostStone.x*U,.3+Math.sin(tm*4)*.08,G.side.lostStone.y*U);}else stoneMesh.visible=false;
  // GPS ribbon
  if(gps.path!==R3._lastPath){R3._lastPath=gps.path;buildRibbon(gps.path);}gpsTex.offset.x=-tm*1.6;gpsMesh.visible=!!(gps.path&&gps.path.length>1);
  // ambient animation
  animFountains(dt,tm);animDetails(dt,tm);animPigeons(dt,tm,p);animSmoke(dt);swanObjs.forEach(s=>{const a=tm*.25+s.k*3;s.o.position.set(s.c.x+Math.cos(a)*3.2,.06,s.c.z+Math.sin(a)*1.6);s.o.rotation.y=-a;});
  waterMat.color.setHSL(.56,.62,.4+Math.sin(tm*.7)*.02);
  rainMesh.visible=EV.rain>0;if(rainMesh.visible)animRain(dt);
  animConfetti(dt);
  // camera
  const heading3=yawOf(inCar?G.van.a||0:(p.a!=null?p.a:Math.PI/2));camUpdate(dt,inCar?G.van.x:p.x,inCar?G.van.y:p.y,inCar,heading3);
  draw();
  drawLabels(tm,qt);};
function buildRibbon(path){if(!path||path.length<2){gpsMesh.geometry.dispose();gpsMesh.geometry=new THREE.BufferGeometry();return;}
  const pos=[],uv=[],idx=[];let acc=0;const wdt=.55;const pts=path.map(p=>new V3(p.x*U,.12,p.y*U));
  for(let i=0;i<pts.length;i++){const a=pts[Math.max(0,i-1)],b=pts[Math.min(pts.length-1,i+1)];const d=b.clone().sub(a).normalize();const n=new V3(-d.z,0,d.x).multiplyScalar(wdt);if(i>0)acc+=pts[i].distanceTo(pts[i-1]);
    pos.push(pts[i].x+n.x,.12,pts[i].z+n.z,pts[i].x-n.x,.12,pts[i].z-n.z);uv.push(acc/1.4,1,acc/1.4,0);if(i>0){const k=i*2;idx.push(k-2,k-1,k,k-1,k+1,k);}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);gpsMesh.geometry.dispose();gpsMesh.geometry=g;}
function animDetails(dt,tm){SITTERS.forEach((o,i)=>{const u=o.userData;u.inner.rotation.z=Math.sin(tm*1.1+i)*.03;u.arms[i%2].rotation.x=-.5+Math.sin(tm*1.7+i)*.18;});
  CLOTHES.forEach(c=>{c.rotation.x=Math.sin(tm*1.8+c.userData.ph)*.2;});SPIN.forEach(s=>s.rotation.y+=dt*.25);
  FLAGS.forEach(f=>{const a=f.geometry.attributes.position,b=f.userData.base;for(let i=0;i<a.count;i++){const x=b[i*3];a.array[i*3+2]=Math.sin(x*2.4-tm*5.5)*.13*x;}a.needsUpdate=true;});
  TROLLEYS.forEach(t=>{const u=t.userData;u.x+=u.dir*dt*7;if(u.x>MW_+12)u.x=VR[0]*2;if(u.x<VR[0]*2)u.x=MW_+12;t.position.set(u.x,0,u.lane);t.rotation.y=u.dir>0?Math.PI/2:-Math.PI/2;});
  if(TLIGHT.im&&((tm*2)|0)!==TLIGHT.t){TLIGHT.t=(tm*2)|0;const c=new THREE.Color();for(let i=0;i<TLIGHT.n;i++){const ph=((tm/7+(i%2)*.5)%1);c.set(ph<.45?'#38e05a':ph<.55?'#ffc21a':'#ff3b30');TLIGHT.im.setColorAt(i,c);}TLIGHT.im.instanceColor.needsUpdate=true;}
  if(WHEEL.o)WHEEL.o.rotation.z+=dt*.06;}
function animFountains(dt,tm){fountains.forEach(f=>{const a=f.pts.geometry.attributes.position.array;f.seed.forEach((s,i)=>{const t=((tm*.55+s[1])%1);const ang=s[0],r=.35+s[2]*.5;const sp=1+t*1.6;
    a[i*3]=f.x+Math.cos(ang)*r*sp*(f.sx/3.4);a[i*3+2]=f.z+Math.sin(ang)*r*sp*(f.sz/3.4);a[i*3+1]=.5+(f.h*4*t*(1-t))*(.6+s[2]*.5);});f.pts.geometry.attributes.position.needsUpdate=true;});}
function animPigeons(dt,tm,p){const im=pigeons.im;const px=p.x*U,pz=p.y*U;pigeons.list.forEach((b,i)=>{const d=Math.hypot(b.x-px,b.z-pz);
  if(!b.fly&&d<4.5){b.fly=7;b.vy=4+Math.random()*2;b.vx=(b.x-px)/d*3;b.vz=(b.z-pz)/d*3;}
  if(b.fly>0){b.fly-=dt;b.y+=b.vy*dt;b.x+=b.vx*dt;b.z+=b.vz*dt;b.vy-=dt*.6;if(b.fly<=0){b.y=0;b.x=b.hx+(Math.random()-.5)*4;b.z=b.hz+(Math.random()-.5)*4;b.fly=0;}}
  else{b.a+=Math.sin(tm*2+i)*.02;}
  im.setMatrixAt(i,_m.compose(_p.set(b.x,b.y+(b.fly?0:Math.abs(Math.sin(tm*6+i))*.03),b.z),_q.setFromEuler(_e.set(b.fly?-.4:Math.sin(tm*5+i)*.25,b.a,0)),_s.set(1,1,1)));});im.instanceMatrix.needsUpdate=true;}
function animSmoke(dt){smoke.forEach(s=>{const u=s.userData;u.t=(u.t+dt*.35)%1;s.position.set(u.x+Math.sin(u.t*6)*.4,u.y0+u.t*4.5,u.z);s.scale.setScalar(.6+u.t*2.6);s.material.opacity=.55*(1-u.t);});}
function animRain(dt){const g=rainMesh.geometry.attributes.position.array,d=rainMesh.userData.d,c=camLook;d.forEach((r,i)=>{r[1]-=dt*28;if(r[1]<0)r[1]+=40;const x=c.x+r[0],z=c.z+r[2];g.set([x,r[1],z,x-.12,r[1]+.9,z],i*6);});rainMesh.geometry.attributes.position.needsUpdate=true;}
function animConfetti(dt){const c=confetti;c.p=c.p.filter(q=>(q.life-=dt)>0);c.im.count=c.p.length;const col=new THREE.Color();c.p.forEach((q,i)=>{q.vy-=dt*9;q.x+=q.vx*dt;q.y=Math.max(.05,q.y+q.vy*dt);q.z+=q.vz*dt;q.r+=dt*8;
  c.im.setMatrixAt(i,_m.compose(_p.set(q.x,q.y,q.z),_q.setFromEuler(_e.set(q.r,q.r*.7,0)),_s.set(1,1,1)));col.set(q.c);c.im.setColorAt(i,col);});c.im.instanceMatrix.needsUpdate=true;if(c.im.instanceColor)c.im.instanceColor.needsUpdate=true;}
R3.burst=(x,y,color)=>{for(let i=0;i<40;i++)confetti.p.push({x:x*U,y:1.6,z:y*U,vx:(Math.random()-.5)*7,vy:4+Math.random()*5,vz:(Math.random()-.5)*7,r:Math.random()*6,life:1.6,c:[color,'#ff8ab8','#6cc8ff','#7ff0b0','#ffd84d'][i%5]});if(confetti.p.length>160)confetti.p.splice(0,confetti.p.length-160);};

function drawLabels(tm,qt){const p=G.p,C=R3.cam;
  if(!(C.mode==='first'))L('me',p.inVan?G.van.x:p.x,p.inVan?G.van.y:p.y,p.inVan?3.1:2.5,`<span class="nm me">${G.nick}</span>`);
  NPC.forEach(n=>{const m=questMark(n);const o=O.npc.get(n.id);if(!o.visible&&!m)return;const h=n.dog?1.4:2.45;
    L('n_'+n.id,n.x,n.y,h,`${m?`<b class="qm ${m}">${m==='main'?'!':'?'}</b>`:''}<span class="nm npc">${n.name}<small>${n.role}</small></span>`,'',m?1e9:30);});
  bots.forEach((b,i)=>{if(O.bots[i].visible)L('b_'+i,b.x,b.y,2.4,`<span class="nm bot">${b.nm}</span>`,'',32);});
  // parcels: numbered pins
  const sp=G.inv.find(x=>x.id===G.sel);
  G.inv.forEach((x,i)=>{const t=tgOf(x);if(!t||x===sp||x.dest==='npc')return;L('p_'+x.id,t.x,t.y,3.2,`<span class="pin sm"><i>${i+1}</i>${lbl(x).ic}</span>`);});
  if(qt&&qt.pt&&!NPC.includes(qt.pt)){const num=sp&&tgOf(sp)===qt.pt?G.inv.indexOf(sp)+1:null;L('tg',qt.pt.x,qt.pt.y,4+Math.sin(tm*4)*.25,`<span class="pin big">${num?`<i>${num}</i>`:''}${qt.lab.ic||''} ${qt.lab.t||''}</span>`);}
  if(G.co.unlocked)W.slots.forEach((s,i)=>{if(!s.built)L('fs_'+i,s.x,s.y,1.6,'<span class="free">+ ազատ տեղ</span>','',60);});
  if(!p.inVan&&G.q>=1&&(G.q===7||!G.flags.vanUsed)&&Math.hypot(G.van.x-p.x,G.van.y-p.y)<300)L('niva',G.van.x,G.van.y,3.2,'<span class="nm npc">🚙 Քո Նիվան</span>');
  if(EV.nivaPush)L('push',W.places.niva.x,W.places.niva.y,3.4,`<span class="pin big">💨 Հրիր ինձ ${EV.nivaPush.n}/8</span>`);
  bubbles.forEach((b,i)=>{const e=b.e;if(!e)return;const isP=e===G.pm;const h=(e.dog?1.6:isP&&p.inVan?3.4:2.9);const el=L('bb_'+i,isP?(p.inVan?G.van.x:p.x):e.x,isP?(p.inVan?G.van.y:p.y):e.y,h,`<span class="bub">${b.t}</span>`,'',70);if(el)el.el.style.opacity=Math.min(1,b.life*3);});
  floats.forEach((f,i)=>{const el=L('fl_'+i,f.x,f.y,2.6+(1.6-f.life)*1.4,`<span class="flt" style="color:${f.c}">${f.t}</span>`);if(el)el.el.style.opacity=Math.min(1,f.life);});
  labelsEnd();
  // off-screen arrow
  const ea=document.getElementById('edge');if(qt&&qt.pt){_v.set(qt.pt.x*U,1,qt.pt.y*U).project(camera);const behind=_v.z>1;let x=_v.x,y=_v.y;if(behind){x=-x;y=-y;}
    if(behind||Math.abs(x)>.92||Math.abs(y)>.88){const a=Math.atan2(-y,x);const W2=innerWidth,H2=innerHeight;const rx=W2/2-(W2<700?70:90),ry=H2/2-(W2<700?140:120);const k=Math.min(Math.abs(rx/Math.cos(a)),Math.abs(ry/Math.sin(a)));
      ea.style.display='block';ea.style.transform=`translate(${W2/2+Math.cos(a)*k}px,${H2/2+Math.sin(a)*k}px)`;ea.firstElementChild.style.transform=`rotate(${a}rad)`;const t=`${qt.lab.ic||''} ${Math.round(Math.hypot(qt.pt.x-(p.inVan?G.van.x:p.x),qt.pt.y-(p.inVan?G.van.y:p.y))/TS*10/10)*10} մ`;if(ea.lastChild.textContent!==t)ea.lastChild.textContent=t;}else ea.style.display='none';}else ea.style.display='none';}

/* ---------------------------------------------------------------- TITLE CINEMATIC */
R3.title=function(dt){if(!R3.ready)return;T0+=dt;const tm=T0;const s=W.places.square;const c=new V3(s.x*U,0,s.y*U);const a=tm*.05+2.2;
  const sw=Math.sin(tm*.06);camera.position.set(MW_*.78+sw*18,42+Math.sin(tm*.1)*3,22+sw*6);camera.lookAt(MW_*.3+sw*10,14,MH_+120);camera.fov=50;camera.updateProjectionMatrix();
  sun.position.copy(c).add(SUNOFF);sun.target.position.copy(c);sun.target.updateMatrixWorld();
  cars.forEach((cc,i)=>{moveOnGraph(cc,dt,14);place(O.cars[i],cc.x,cc.y,cc.ang||0);O.cars[i].visible=true;});walkers.forEach((w,i)=>{moveOnGraph(w,dt,w.off);const cr=O.crowd&&O.crowd[i];if(cr){O.walkers[i].visible=false;cr.visible=true;place(cr,w.x,w.y,w.ang||0);cr.userData.mx.update(dt);}else{place(O.walkers[i],w.x,w.y,w.ang||0);animChar(O.walkers[i],dt,true,.7);O.walkers[i].visible=true;}});camLook.set(MW_*.4,0,MH_*.6);updateFleet();
  NPC.forEach(n=>{const o=O.npc.get(n.id);place(o,n.x,n.y,Math.PI/2);if(!n.dog)animChar(o,dt,false);});
  animFountains(dt,tm);animDetails(dt,tm);animSmoke(dt);animPigeons(dt,tm,{x:-999,y:-999});O.player&&(O.player.visible=false);draw();};

/* ---------------------------------------------------------------- PORTRAITS (3D) */
let pr=null;
R3.portrait=function(target,look){try{if(!pr){const c=document.createElement('canvas');c.width=c.height=256;const r=new THREE.WebGLRenderer({canvas:c,alpha:true,antialias:true,preserveDrawingBuffer:true});r.outputColorSpace=THREE.SRGBColorSpace;r.toneMapping=THREE.ACESFilmicToneMapping;
    const s=new THREE.Scene();s.add(new THREE.HemisphereLight('#ffffff','#b49376',1.6));const d=new THREE.DirectionalLight('#fff0dd',2.4);d.position.set(2,3,4);s.add(d);s.environment=scene.environment;const cam=new THREE.PerspectiveCamera(30,1,.1,50);pr={r,s,cam,c,cur:null};}
  if(pr.cur){pr.s.remove(pr.cur);}let o;if(look==='dog'){o=makeDog();scene.remove(o);pr.cam.position.set(1.4,1.3,2.2);pr.cam.lookAt(0,.6,.1);}else{o=makeChar(look);scene.remove(o);pr.cam.position.set(.35,1.72,1.25);pr.cam.lookAt(0,1.6,0);}
  o.rotation.y=.25;pr.s.add(o);pr.cur=o;pr.r.render(pr.s,pr.cam);const g=target.getContext('2d');g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,target.width,target.height);g.drawImage(pr.c,0,0,target.width,target.height);}catch(e){console.warn(e);}};

/* ---------------------------------------------------------------- INIT */
/* ---------------------------------------------------------------- HERO NIVA (real 3D model, CC BY 4.0)
   Body : «Lada Niva» by tiunov.se — sketchfab.com/3d-models/lada-niva-5a83c0cc63df418fa5bb9a2bf98dc9a6
   Rims : «Lada Niva Car Rims Armenian Style Tuning» by Hambar1an — sketchfab.com/3d-models/5e685c8c870646d596229519c34366b2
   Files are optional: put the unzipped glTF exports into models/niva_tuned/ and models/rims_am/.
   If they are missing the procedural Niva is used. models/niva_tuned/config.json may hold {"yaw":0,"length":3.9}. */
const WHEEL_RE=/wheel|rim|tire|tyre|disk|disc|koleso|колес|шин|диск|шина/i;
async function tryLoad(url){if(window.GLTF_EXT)url=url.replace(/\.gltf$/,'.'+window.GLTF_EXT);try{return await new GLTFLoader().loadAsync(url);}catch(e){return null;}}
async function getJSON(url){try{const r=await fetch(url);return r.ok?await r.json():null;}catch(e){return null;}}
function normalize(obj,len,yaw){const g=new THREE.Group();g.add(obj);obj.updateMatrixWorld(true);let b=new THREE.Box3().setFromObject(obj),s=b.getSize(new V3());
  if(s.x>s.z)obj.rotation.y+=Math.PI/2;obj.rotation.y+=yaw||0;obj.updateMatrixWorld(true);b=new THREE.Box3().setFromObject(obj);s=b.getSize(new V3());
  const k=len/Math.max(s.z,1e-6);obj.scale.multiplyScalar(k);obj.updateMatrixWorld(true);b=new THREE.Box3().setFromObject(obj);const c=b.getCenter(new V3());obj.position.x-=c.x;obj.position.z-=c.z;obj.position.y-=b.min.y;g.updateMatrixWorld(true);return g;}
async function loadHeroNiva(){const gl=await tryLoad('models/niva_tuned/scene.gltf')||await tryLoad('models/niva_tuned/scene.glb');if(!gl)return;
  const cfg=(await getJSON('models/niva_tuned/config.json'))||{};const body=gl.scene;
  body.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(m&&'envMapIntensity' in m)m.envMapIntensity=1.25;});}});
  const hero=normalize(body,cfg.length||3.9,cfg.yaw||0);
  // tuned paint: pearl body
  if(cfg.paint)body.traverse(o=>{if(o.isMesh){(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(m&&/kuzov/i.test(m.name)){m.color.set(cfg.paint);m.metalness=.55;m.roughness=.2;m.envMapIntensity=1.5;}});}});
  // Armenian-style rims replace the stock wheels (each stock wheel is a node named "wheel")
  const rims=await tryLoad('models/rims_am/scene.gltf')||await tryLoad('models/rims_am/scene.glb');
  hero.updateMatrixWorld(true);const wheels=[];hero.traverse(o=>{if(!o.isMesh&&/^wheel/i.test(o.name))wheels.push(o);});
  if(!wheels.length)hero.traverse(o=>{if(o.isMesh&&WHEEL_RE.test(o.name))wheels.push(o);});
  R3.heroWheels=[];
  if(rims&&wheels.length>=4){const src=rims.scene;src.updateMatrixWorld(true);const rb=new THREE.Box3().setFromObject(src),rs=rb.getSize(new V3()),rc=rb.getCenter(new V3());const rimDia=Math.max(rs.y,rs.z);
    src.traverse(o=>{if(o.isMesh){o.castShadow=true;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(m&&'envMapIntensity' in m)m.envMapIntensity=1.6;});}});
    wheels.forEach(w=>{const bb=new THREE.Box3().setFromObject(w),c=bb.getCenter(new V3()),sz=bb.getSize(new V3());const dia=Math.max(sz.y,sz.z);w.visible=false;
      const inner=src.clone(true);inner.position.copy(rc).multiplyScalar(-1);const spin=new THREE.Group();spin.add(inner);const pivot=new THREE.Group();pivot.add(spin);
      pivot.scale.setScalar(dia/rimDia*1.02);if(c.x<0)pivot.rotation.y=Math.PI;pivot.position.copy(c);hero.add(pivot);R3.heroWheels.push({spin,side:c.x<0?-1:1,r:dia/2});});}
  else wheels.forEach(w=>R3.heroWheels.push({spin:w,side:1,r:.37,stock:true}));
  // swap the procedural body for the real one, keep roof cargo
  const old=O.myNiva.children.find(c=>c.isMesh);if(old)old.visible=false;O.myNiva.add(hero);
  const hb=new THREE.Box3().setFromObject(hero);O.cargo.position.y=hb.max.y-2.0;R3.heroNiva=true;console.log('[3D] tuned Niva model loaded');}
/* ---------------------------------------------------------------- MORE REAL MODELS (CC BY 4.0, see credits)
   Lada 2107 tun — Aslan · Low Detail Animated Crowd — Shahriar Shahrabi · Cardboard Boxes Pack — Alex human */
const FLEET={parts:[],max:isMobile?10:28,taxiSign:null};const _cm=new THREE.Matrix4(),_pm=new THREE.Matrix4();
const LADA_COLORS=['#f2f0ea','#e9dfc8','#8e1f2b','#1f3c6e','#141518','#2f5d3a','#b9bec6','#d7d2c4','#6b1d2a','#355e8c'];
async function loadLada(){const gl=await tryLoad('models/lada2107/scene.gltf');if(!gl)return;const root=gl.scene;const g=normalize(root,4.15,Math.PI);g.updateMatrixWorld(true);
  const SKIP=/INTERIOR|Suspension|Brakes|Steering|Wipers/i;
  g.traverse(o=>{if(!o.isMesh)return;let n=o,skip=false;while(n){if(SKIP.test(n.name)){skip=true;break;}n=n.parent;}if(skip)return;
    let mat=o.material;const body=/^Body2?$/.test(mat.name||'');if(body){mat=mat.clone();mat.color.set('#ffffff');mat.metalness=.45;mat.roughness=.28;}if('envMapIntensity' in mat)mat.envMapIntensity=1.3;
    const im=new THREE.InstancedMesh(o.geometry,mat,FLEET.max);im.count=0;im.castShadow=true;im.receiveShadow=true;im.frustumCulled=false;if(body)for(let i=0;i<FLEET.max;i++)im.setColorAt(i,new THREE.Color('#ffffff'));scene.add(im);
    FLEET.parts.push({im,m:o.matrixWorld.clone(),body});});
  const sign=new THREE.InstancedMesh(MERGE([P(box(.62,.22,.3),'#222',0,1.5,0),...[0,1,2,3].map(k=>P(box(.15,.12,.32),k%2?'#ffd84d':'#222',-.23+k*.155,1.52,0))]),VCM,12);sign.count=0;sign.frustumCulled=false;scene.add(sign);FLEET.taxiSign=sign;
  cars.forEach((c,i)=>{if(c.kind==='car'||c.kind==='taxi')c.lcol=new THREE.Color(c.kind==='taxi'?'#f2c230':LADA_COLORS[i%LADA_COLORS.length]);});
  PARKED.forEach((p,i)=>p.lcol=new THREE.Color(LADA_COLORS[(i*3)%LADA_COLORS.length]));R3.lada=true;}
function updateFleet(){if(!R3.lada)return;const cx=camLook.x,cz=camLook.z,R2=(R3.cam.mode==='top'?70:95)**2;const near=[];
  PARKED.forEach((p,i)=>{const d=(p.x-cx)**2+(p.z-cz)**2;p._d=d;});cars.forEach((c,i)=>{c._d=c.lcol?((c.x*U-cx)**2+(c.y*U-cz)**2):1e12;});
  const cand=PARKED.filter(p=>p._d<R2).map(p=>({p,d:p._d})).concat(cars.filter(c=>c._d<R2).map(c=>({c,d:c._d}))).sort((a,b)=>a.d-b.d).slice(0,FLEET.max);const chosen=new Set(cand.map(x=>x.p||x.c));
  PARKED.forEach((p,i)=>{procParked.setMatrixAt(i,chosen.has(p)?_pm.makeScale(0,0,0):p.m);});procParked.instanceMatrix.needsUpdate=true;
  let ts=0;cand.forEach((x,i)=>{let col;if(x.p){_cm.copy(x.p.m);col=x.p.lcol;}else{const c=x.c;_cm.compose(_p.set(c.x*U,0,c.y*U),_q.setFromEuler(_e.set(0,yawOf(c.ang||0),0)),_s.set(1,1,1));col=c.lcol;O.cars[cars.indexOf(c)].visible=false;if(c.kind==='taxi'&&ts<12)FLEET.taxiSign.setMatrixAt(ts++,_cm);}
    FLEET.parts.forEach(pt=>{pt.im.setMatrixAt(i,_pm.multiplyMatrices(_cm,pt.m));if(pt.body)pt.im.setColorAt(i,col);});});
  FLEET.parts.forEach(pt=>{pt.im.count=cand.length;pt.im.instanceMatrix.needsUpdate=true;if(pt.body&&pt.im.instanceColor)pt.im.instanceColor.needsUpdate=true;});FLEET.taxiSign.count=ts;FLEET.taxiSign.instanceMatrix.needsUpdate=true;}
async function loadCrowd(){const gl=await tryLoad('models/crowd/scene.gltf');if(!gl)return;const root=gl.scene;root.updateMatrixWorld(true);const arms=[];root.traverse(o=>{if(/^Armature/.test(o.name))arms.push(o);});if(!arms.length)return;
  const clip0=gl.animations[0];const types=arms.map(a=>{const names=new Set();a.traverse(o=>names.add(o.name));const clip=clip0.clone();clip.tracks=clip.tracks.filter(t=>names.has(t.name.split('.')[0]));return {a,clip};});
  O.crowd=walkers.map((w,i)=>{const t=types[i%types.length];const inner=new THREE.Group();t.a.parent.matrixWorld.decompose(inner.position,inner.quaternion,inner.scale);const c=SU.clone(t.a);inner.add(c);
    c.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;o.frustumCulled=false;}});const outer=new THREE.Group();outer.add(inner);inner.updateMatrixWorld(true);
    const b=new THREE.Box3().setFromObject(inner),ctr=b.getCenter(new V3());inner.position.x-=ctr.x;inner.position.z-=ctr.z;inner.position.y-=b.min.y;const k=(1.68+((i*37)%10)/50)/Math.max(.1,b.max.y-b.min.y);outer.scale.setScalar(k);
    const mx=new THREE.AnimationMixer(c);const act=mx.clipAction(t.clip);act.play();act.time=(i*.37)%1.2;outer.userData.mx=mx;outer.visible=false;scene.add(outer);w.sp=Math.min(w.sp,24+((i*7)%6));return outer;});R3.crowd=true;}
async function loadBoxes(){const gl=await tryLoad('models/boxes/scene.gltf');if(!gl)return;const root=gl.scene;root.updateMatrixWorld(true);let grp=null;root.traverse(o=>{if(!grp&&/^120.*100.*80/.test(o.name))grp=o;});if(!grp)root.traverse(o=>{if(!grp&&o.children.length===2&&o.children.every(c=>c.isMesh))grp=o;});if(!grp)return;
  const parts=[];grp.children.forEach(m=>{if(!m.isMesh)return;const g=m.geometry.clone();g.applyMatrix4(m.matrixWorld);const geo=g.index?g.toNonIndexed():g;const n=geo.attributes.position.count,a=new Float32Array(n*3),c=m.material.color;for(let i=0;i<n;i++){a[i*3]=c.r;a[i*3+1]=c.g;a[i*3+2]=c.b;}geo.setAttribute('color',new THREE.BufferAttribute(a,3));['uv','uv1','tangent'].forEach(k=>{if(geo.attributes[k]&&k!=='uv')geo.deleteAttribute(k);});if(!geo.attributes.uv)geo.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(n*2),2));parts.push(geo);});
  const geo=mergeGeometries(parts);geo.computeBoundingBox();const bb=geo.boundingBox,sz=bb.getSize(new V3()),c=bb.getCenter(new V3());geo.translate(-c.x,-bb.min.y,-c.z);geo.scale(.56/sz.x,.42/sz.y,.48/sz.z);geo.translate(0,-.21,0);geo.computeVertexNormals();
  O.cargo.geometry=geo;
  // a proper pile of parcels at the warehouse gate
  const h=W.places.hub,pile=new THREE.InstancedMesh(geo,VCM,22);let k=0;for(let i=0;i<4;i++)for(let j=0;j<3-(i>1?1:0);j++)for(let l=0;l<(i%2?2:3);l++){if(k>=22)break;pile.setMatrixAt(k++,_m.compose(_p.set(h.x*U+3.4+i*.62,.21+l*.42,h.y*U-1.6+j*.55),_q.setFromEuler(_e.set(0,(k*.37)%.4-.2,0)),_s.set(1,1,1)));}
  pile.count=k;pile.castShadow=pile.receiveShadow=true;scene.add(pile);R3.boxes=true;}
R3.init=function(){buildWorld3D();initDynamic();patchNear();R3.ready=true;loadHeroNiva();loadLada();loadCrowd();loadBoxes();};
R3.camModes=['top','third','first'];
R3.cycleCam=function(){const C=R3.cam;const i=(R3.camModes.indexOf(C.mode)+1)%3;C.mode=R3.camModes[i];camInit=C.mode==='first'?true:camInit;
  if(C.mode!=='top'){const p=G.p;C.yaw=yawOf(p.inVan?G.van.a||0:(p.a!=null?p.a:Math.PI/2));C.pitch=C.mode==='first'?-.08:-.12;}return C.mode;};
R3.renderer=renderer;R3.scene=scene;R3.camera=camera;R3.THREE=THREE;
window.R3=R3;
const fontsReady=document.fonts&&document.fonts.ready?Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,2500))]):Promise.resolve();
fontsReady.then(()=>{try{R3.init();}catch(e){console.error(e);const l=document.querySelector('#loading div:last-child');if(l)l.textContent='3D-ն չբեռնվեց՝ թարմացրու էջը կամ փորձիր այլ բրաուզեր 🙏';}});
