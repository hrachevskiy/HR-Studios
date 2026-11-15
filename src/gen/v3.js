(function(){'use strict';
const $=(q,r=document)=>r.querySelector(q),$$=(q,r=document)=>[...r.querySelectorAll(q)],B=document.body,RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(pointer:fine)').matches;
/* ready after intro */
const go=()=>requestAnimationFrame(()=>B.classList.add('ready'));
const intro=$('#intro');if(!intro)go();else{const mo=new MutationObserver(()=>{if(!document.getElementById('intro')||intro.classList.contains('bye')){mo.disconnect();setTimeout(go,150)}});mo.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});setTimeout(go,26000)}
/* header */
const hdr=$('.hdr');const onS=()=>{hdr&&hdr.classList.toggle('sc',scrollY>8)};addEventListener('scroll',onS,{passive:true});onS();
$$('.nav a').forEach(a=>a.addEventListener('click',()=>B.classList.remove('menu-on')));
/* counters */
function cnt(el){if(el.dataset.done)return;el.dataset.done=1;const raw=el.dataset.count.replace(/[^\d.\-]/g,''),to=parseFloat(raw);if(isNaN(to)||RM){return}
 const d=(raw.split('.')[1]||'').length,pre=el.textContent.trim().startsWith('+')?'+':'',suf=/%$/.test(el.textContent.trim())?'%':'',t0=performance.now(),dur=1500;
 const f=x=>pre+x.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d}).replace(/,/g,to>=10000?',':'')+suf;
 const st=n=>{const p=Math.min(1,(n-t0)/dur),e=1-Math.pow(1-p,4);el.textContent=f(to*e);if(p<1)requestAnimationFrame(st)};requestAnimationFrame(st)}
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');e.target.querySelectorAll&&e.target.querySelectorAll('[data-count]').forEach(cnt);if(e.target.matches('[data-count]'))cnt(e.target);io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
$$('.rv,[data-count]').forEach(el=>io.observe(el));
/* spotlight on glass cards */
if(FINE){document.addEventListener('pointermove',e=>{const c=e.target.closest&&e.target.closest('.gc');if(!c)return;const r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');c.classList.add('lit')},{passive:true});
 document.addEventListener('pointerout',e=>{const c=e.target.closest&&e.target.closest('.gc');if(c&&!c.contains(e.relatedTarget))c.classList.remove('lit')});}
/* hero parallax */
const hv=$('[data-par]');if(hv&&FINE&&!RM){addEventListener('pointermove',e=>{const x=(e.clientX/innerWidth-.5),y=(e.clientY/innerHeight-.5);hv.style.setProperty('--px',(x*26).toFixed(1)+'px');hv.style.setProperty('--py',(y*26).toFixed(1)+'px')},{passive:true})}
/* magnetic buttons */
if(FINE&&!RM)$$('.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.28)+'px)'});b.addEventListener('pointerleave',()=>b.style.transform='')});
/* story */
const stps=$$('.stp'),svs=$$('.sv');if(stps.length){const so=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const k=e.target.dataset.step;stps.forEach(s=>s.classList.toggle('on',s===e.target));svs.forEach(v=>v.classList.toggle('on',v.dataset.sv===k))}}),{rootMargin:'-45% 0px -45% 0px'});stps.forEach(s=>so.observe(s));stps[0].classList.add('on')}
/* lesson sub-nav */
const ln=$$('.lnin a');if(ln.length){const ob=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)ln.forEach(a=>{const on=a.getAttribute('href')==='#'+e.target.id;a.classList.toggle('on',on);if(on)a.scrollIntoView({block:'nearest',inline:'center',behavior:'smooth'})})}),{rootMargin:'-35% 0px -60% 0px'});ln.forEach(a=>{const t=$(a.getAttribute('href'));t&&ob.observe(t)})}
/* slides lightbox */
const lb=$('#lb');if(lb){const im=$('img',lb),lab=$('span',lb),list=$$('.sld');let k=0;const show=i=>{k=(i+list.length)%list.length;im.src=list[k].dataset.src;lab.textContent=(k+1)+' / '+list.length};
 list.forEach((b,i)=>b.onclick=()=>{show(i);lb.classList.add('on');document.documentElement.style.overflow='hidden'});const close=()=>{lb.classList.remove('on');document.documentElement.style.overflow=''};
 $('.cl',lb).onclick=close;$('.pv',lb).onclick=()=>show(k-1);$('.nx',lb).onclick=()=>show(k+1);lb.addEventListener('click',e=>{if(e.target===lb)close()});
 addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(k+1);if(e.key==='ArrowLeft')show(k-1)});
 let sx=null;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(sx==null)return;const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50)show(k+(d<0?1:-1));sx=null},{passive:true})}
/* page transition */
const pt=$('.ptrans');document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('a');if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey)return;const h=a.getAttribute('href')||'';
 if(a.target||a.hasAttribute('download')||h.startsWith('#')||/^(https?:|mailto:)/.test(h)||!/\.html(#.*)?$/.test(h.split('?')[0]))return;
 if(h.split('#')[0]===location.pathname.split('/').pop())return;e.preventDefault();pt&&pt.classList.add('on');setTimeout(()=>location.href=h,230)});
addEventListener('pageshow',()=>pt&&pt.classList.remove('on'));
})();
