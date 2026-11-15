# -*- coding: utf-8 -*-
"""v2 homework pages: same data as hwpage.py, but cinematic — per-theme intro curtain, Ken Burns hero slideshow,
parallax chapter breaks, count-up KPIs, animated charts/gauges, photo galleries with lightbox.
Pages: dasi-2-3 (newspaper), dasi-4 (blueprint), dasi-5 (Swiss poster), dasi-6 (notebook), mijankyal (liquid glass, the original submission)."""
import os, sys, shutil, re, openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpage as H
from hwpage import E, n, W, C, table, verdict, svg_pairs, svg_waterfall, SITE

# ---------- gauge override: marker animates from 0 when visible ----------
def gauge(label, v, lo, hi, vmax, d=3):
    p = lambda z: max(0, min(100, z / vmax * 100))
    return (f'<div class="gauge rv"><div class="gl"><span>{E(label)}</span><b data-count="{v}" data-d="{d}">{n(v,d)}</b></div><div class="gt"><i class="zone" style="left:{p(lo):.1f}%;width:{p(hi)-p(lo):.1f}%"></i>'
            f'<i class="mk" style="--v:{p(v):.1f}%"></i></div><div class="gs"><span>0</span><span>նորմա {lo:g}–{hi:g}</span><span>{vmax:g}</span></div></div>')
H.gauge = gauge

A = "../../assets/hw"
def imgs(cat, ids): return [f"{A}/{cat}/{i:02d}.jpg" for i in ids]
def hero_slides(cat, ids, cls=""):
    return '<div class="hs ' + cls + '">' + "".join(f'<img class="{"on" if k == 0 else ""}" src="{u}" alt="" {"" if k == 0 else "loading=lazy"} decoding="async">' for k, u in enumerate(imgs(cat, ids))) + '</div>'
def chapter(cat, i, num, title, sub=""):
    return (f'<section class="chap"><div class="chi" data-par="0.25" style="background-image:url(\'{A}/{cat}/{i:02d}.jpg\')"></div>'
            f'<div class="chc rv"><span class="chn">{E(num)}</span><h2>{E(title)}</h2>{f"<p>{E(sub)}</p>" if sub else ""}</div></section>')
def marquee(cat, ids):
    t = "".join(f'<img src="{A}/{cat}/{i:02d}_s.jpg" alt="" loading="lazy">' for i in ids)
    return f'<div class="mq"><div class="mqt">{t}{t}</div></div>'
def gallery(cat, ids, title):
    g = "".join(f'<a class="gi rv" style="--i:{k}" href="{A}/{cat}/{i:02d}.jpg" data-lb><img src="{A}/{cat}/{i:02d}_s.jpg" alt="" loading="lazy"></a>' for k, i in enumerate(ids))
    return f'<section class="gal"><div class="wrap"><h2 class="rv">{E(title)}</h2><div class="gg">{g}</div></div></section>'
def kpis(items, cls="kp"):
    out = ""
    for k, (val, lab) in enumerate(items):
        raw = re.sub(r"[^\d.\-−+]", "", val.replace(",", "")).replace("−", "-")
        try:
            num = float(raw); d = len(raw.split(".")[1]) if "." in raw else 0
            pre = "+" if val.strip().startswith("+") else ""; suf = "%" if val.strip().endswith("%") else ""
            out += f'<div class="{cls} rv" style="--i:{k}"><b data-count="{num}" data-d="{d}" data-pre="{pre}" data-suf="{suf}">{val}</b><span>{E(lab)}</span></div>'
        except ValueError:
            out += f'<div class="{cls} rv" style="--i:{k}"><b>{val}</b><span>{E(lab)}</span></div>'
    return out

ENGINE_CSS = r"""
html{scroll-behavior:smooth}body{overflow-x:hidden}
.prog{position:fixed;left:0;top:0;height:3px;width:0;z-index:100;background:var(--acc);box-shadow:0 0 12px var(--acc)}
/* curtain */
.cur{position:fixed;inset:0;z-index:200;display:grid;place-items:center;overflow:hidden;pointer-events:none;transition:opacity .7s .1s,visibility 0s .9s}
body.ready .cur{opacity:0;visibility:hidden}
/* hero slideshow */
.hs{position:absolute;inset:0;overflow:hidden}.hs img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.12);transition:opacity 1.6s ease,transform 7s linear}
.hs img.on{opacity:1;transform:scale(1)}
.hero{position:relative;min-height:100vh;display:flex;align-items:flex-end;overflow:hidden}
.hero .inner{position:relative;z-index:3;width:100%}
.tl .w{display:inline-block;opacity:0;transform:translateY(60%) rotate(4deg);filter:blur(6px);transition:all .9s cubic-bezier(.2,.8,.2,1);transition-delay:calc(var(--k)*.08s + .2s)}
body.ready .tl .w{opacity:1;transform:none;filter:none}
.fade-up{opacity:0;transform:translateY(24px);transition:all .9s cubic-bezier(.2,.8,.2,1) .7s}body.ready .fade-up{opacity:1;transform:none}
.scue{position:absolute;left:50%;bottom:18px;z-index:4;width:22px;height:36px;border:2px solid currentColor;border-radius:12px;opacity:.6;transform:translateX(-50%)}
.scue::after{content:"";position:absolute;left:50%;top:6px;width:4px;height:8px;margin-left:-2px;border-radius:2px;background:currentColor;animation:scue 1.6s infinite}
@keyframes scue{to{transform:translateY(12px);opacity:0}}
/* reveals */
.rv{opacity:0;transform:translateY(30px);transition:opacity .8s,transform .9s cubic-bezier(.2,.8,.2,1);transition-delay:calc(var(--i,0)*.07s)}
.rv.in{opacity:1;transform:none}.rv.sl{transform:translateX(-50px)}.rv.sr{transform:translateX(50px)}.rv.sc{transform:scale(.92)}.rv.sl.in,.rv.sr.in,.rv.sc.in{transform:none}
.tw.in tbody tr{animation:rowin .6s both;animation-delay:calc(var(--r,0)*.045s)}@keyframes rowin{from{opacity:0;transform:translateX(-14px)}}
.tw tbody tr{opacity:1}.tw:not(.in) tbody tr{opacity:0}
/* charts & gauges */
.ch .gr{animation-play-state:paused}.ch.play .gr{animation-play-state:running}
.ch .vl{opacity:0;transition:opacity .6s 1s}.ch.play .vl{opacity:1}.ch .cn{stroke-dashoffset:40;transition:stroke-dashoffset 1.4s .6s}.ch.play .cn{stroke-dashoffset:0}
.gauge .mk{left:0!important;transition:left 1.6s cubic-bezier(.2,.8,.2,1) .2s}.gauge.in .mk{left:var(--v)!important}
.gauge .zone{transform:scaleX(0);transform-origin:left;transition:transform 1.2s .1s}.gauge.in .zone{transform:none}
/* chapter break */
.chap{position:relative;height:72vh;min-height:420px;overflow:hidden;display:grid;place-items:center;text-align:center}
.chi{position:absolute;inset:-18% 0;background:center/cover no-repeat;will-change:transform}
.chc{position:relative;z-index:2;padding:0 20px;max-width:900px}.chn{display:block;font-size:clamp(70px,13vw,170px);line-height:.85;font-weight:900;opacity:.95}
.chc h2{font-size:clamp(28px,4.6vw,58px);margin:10px 0 8px;line-height:1.05}.chc p{font-size:17px;opacity:.85}
/* marquee */
.mq{overflow:hidden;padding:14px 0}.mqt{display:flex;gap:14px;width:max-content;animation:mq 60s linear infinite}.mq:hover .mqt{animation-play-state:paused}
.mqt img{height:150px;width:auto;border-radius:10px;object-fit:cover}@keyframes mq{to{transform:translateX(-50%)}}
/* gallery + lightbox */
.gal{padding:70px 0}.gal h2{font-size:clamp(28px,4vw,46px);margin:0 0 24px}
.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}.gi{display:block;overflow:hidden;border-radius:12px;aspect-ratio:16/9;cursor:zoom-in}
.gi img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.8,.2,1),filter .5s}.gi:hover img{transform:scale(1.08)}
.lb{position:fixed;inset:0;z-index:300;background:rgba(0,0,0,.9);display:none;place-items:center;padding:30px;cursor:zoom-out}.lb.on{display:grid;animation:fi .3s}
.lb img{max-width:100%;max-height:100%;border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.6);animation:zi .45s cubic-bezier(.2,.8,.2,1)}@keyframes zi{from{transform:scale(.9);opacity:0}}@keyframes fi{from{opacity:0}}
[data-tilt]{transition:transform .3s;transform-style:preserve-3d}
.kp b{font-variant-numeric:tabular-nums}
@media (max-width:700px){.chap{height:56vh}.mqt img{height:100px}}
@media (prefers-reduced-motion:reduce){.cur{display:none}.tl .w,.fade-up,.rv{opacity:1!important;transform:none!important;filter:none!important;transition:none}.hs img{transition:opacity .3s}.mqt{animation:none}}
"""
ENGINE_JS = r"""<div class="prog" id="prog"></div><div class="lb" id="lb"><img alt=""></div><script>
(function(){const B=document.body,ms=+B.dataset.cur||1800;let seen=false;try{seen=sessionStorage.getItem('cur-'+location.pathname)==='1'}catch(e){}
const ready=()=>{B.classList.add('ready');try{sessionStorage.setItem('cur-'+location.pathname,'1')}catch(e){}};
if(seen||matchMedia('(prefers-reduced-motion:reduce)').matches){B.classList.add('fast');ready()}else{B.classList.add('cur-on');setTimeout(ready,ms)}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const t=e.target;t.classList.add('in');io.unobserve(t);
 t.querySelectorAll&&t.querySelectorAll('[data-count]').forEach(cnt);if(t.matches('[data-count]'))cnt(t);
 if(t.matches('.tw'))t.querySelectorAll('tbody tr').forEach((r,i)=>r.style.setProperty('--r',i))}}),{threshold:.15,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.rv,.tw,.gauge,svg.ch,.kp b,[data-count]').forEach(el=>io.observe(el));
const io2=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('play');io2.unobserve(e.target)}}),{threshold:.3});document.querySelectorAll('svg.ch').forEach(c=>io2.observe(c));
function cnt(el){if(el.dataset.done)return;el.dataset.done=1;const to=parseFloat(el.dataset.count),d=+el.dataset.d||0,pre=el.dataset.pre||'',suf=el.dataset.suf||'';if(isNaN(to))return;const t0=performance.now(),dur=1600;
 const f=x=>{const s=Math.abs(x).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});return (x<0?'−':(pre))+s+suf};
 const st=n=>{const p=Math.min(1,(n-t0)/dur),e=1-Math.pow(1-p,4);el.textContent=f(to*e);if(p<1)requestAnimationFrame(st);else el.textContent=f(to)};requestAnimationFrame(st)}
document.querySelectorAll('.hs').forEach(h=>{const im=h.querySelectorAll('img');if(im.length<2)return;let k=0;setInterval(()=>{im[k].classList.remove('on');k=(k+1)%im.length;im[k].classList.add('on')},5200)});
const par=[...document.querySelectorAll('[data-par]')],pr=document.getElementById('prog'),hero=document.querySelector('.hero .hs');let tick=false;
function onS(){tick=false;const y=scrollY,h=innerHeight;pr.style.width=(y/(document.documentElement.scrollHeight-h)*100)+'%';
 if(hero&&y<h)hero.style.transform='translateY('+(y*.35)+'px)';
 par.forEach(el=>{const r=el.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>h)return;el.style.transform='translateY('+((r.top+r.height/2-h/2)*-(+el.dataset.par))+'px)'})}
addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(onS)}},{passive:true});onS();
const lb=document.getElementById('lb'),li=lb.querySelector('img');document.querySelectorAll('[data-lb]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();li.src=a.href;lb.classList.add('on')}));lb.onclick=()=>lb.classList.remove('on');
addEventListener('keydown',e=>{if(e.key==='Escape')lb.classList.remove('on')});
if(matchMedia('(pointer:fine)').matches)document.querySelectorAll('[data-tilt]').forEach(c=>{c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateY('+(x*7)+'deg) rotateX('+(-y*7)+'deg)'});c.addEventListener('mouseleave',()=>c.style.transform='')});
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{const g=b.closest('[data-tabs]');g.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('on',x===b));
 g.querySelectorAll('[data-pane]').forEach(p=>{const on=p.dataset.pane===b.dataset.tab;p.classList.toggle('on',on);if(on)p.querySelectorAll('.rv,.tw,.gauge,svg.ch').forEach(el=>{el.classList.add('in','play');el.querySelectorAll('[data-count]').forEach(cnt)})})}));
})();</script>"""

def words(t, k0=0):
    return " ".join(f'<span class="w" style="--k:{i+k0}">{E(x)}</span>' for i, x in enumerate(t.split()))

def page(theme, title, body, css, desc, cur_ms, accent):
    return f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · H/R Studios</title><meta name="description" content="{E(desc)}"><link rel="icon" href="../../assets/logo_sm.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{H.FONTS.get(theme, H.FONTS['gold'])}&display=swap">
<style>:root{{--acc:{accent}}}{H.BASE_CSS}{ENGINE_CSS}{css}</style></head><body class="t-{theme}" data-cur="{cur_ms}">{body}{ENGINE_JS}</body></html>"""

topbar = H.topbar

# ================= 1) PAPER =================
CSS_PAPER2 = H.CSS_PAPER + r"""
.cur{background:#f4efe3}.cur .np{width:min(560px,80vw);aspect-ratio:3/4;background:#fbf7ee;border:1px solid #1d1a16;box-shadow:0 30px 60px rgba(0,0,0,.25);padding:26px;
 animation:spin 1.6s cubic-bezier(.2,.8,.25,1) both;font-family:'Noto Serif Armenian',serif;text-align:center}
.cur .np small{font:600 11px 'Noto Sans Armenian';letter-spacing:.3em;color:#b5452b}.cur .np b{display:block;font-size:clamp(28px,5vw,46px);line-height:1;margin:12px 0;border-top:3px double #1d1a16;border-bottom:3px double #1d1a16;padding:10px 0}
.cur .np i{display:block;height:8px;background:#d9cfb8;margin:9px 0;border-radius:2px}.cur .np i:nth-child(odd){width:86%}
@keyframes spin{0%{transform:rotate(-900deg) scale(.05);opacity:0}70%{opacity:1}100%{transform:rotate(-3deg) scale(1)}}
.hero{color:#fbf7ee;background:#1d1a16}.hero .hs img{filter:sepia(.55) contrast(1.05) brightness(.62)}
.hero::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(29,26,22,.2),rgba(29,26,22,.85)),repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 2px,transparent 2px 4px)}
.hero .inner{padding:0 0 70px}.hero .kick{font:600 12px 'Noto Sans Armenian';letter-spacing:.35em;text-transform:uppercase;color:#e7b49f}
.hero h1{font-size:clamp(40px,7.4vw,104px);line-height:.95;margin:14px 0 18px;font-weight:800;letter-spacing:-.02em}
.hero .dl{display:flex;gap:26px;flex-wrap:wrap;font:400 14px 'Noto Sans Armenian';border-top:1px solid rgba(251,247,238,.4);padding-top:14px;opacity:.9}
.hero .stamp{position:absolute;right:6%;top:22%;z-index:3;font-size:22px;padding:12px 20px;background:rgba(251,247,238,.08);backdrop-filter:blur(4px);transform:rotate(-12deg) scale(2.4);opacity:0;transition:all .5s cubic-bezier(.3,1.6,.5,1) 1.5s}
body.ready .hero .stamp{transform:rotate(-12deg) scale(1);opacity:1}
.kps{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:3px double #1d1a16}.kp{padding:22px 18px;border-right:1px solid #cdbf9f}.kp:last-child{border-right:0}
.kp b{display:block;font-size:clamp(28px,3.4vw,44px);font-weight:800;color:#1f3a5f}.kp span{font:400 13px 'Noto Sans Armenian';opacity:.75}
.mq{background:#1d1a16}.mqt img{filter:sepia(.6) contrast(1.05)}
.chap{color:#fbf7ee}.chap .chi{filter:sepia(.6) brightness(.5)}.chap .chn{font-family:'Noto Serif Armenian';color:#e7b49f}
.gi img{filter:sepia(.4)}.gi:hover img{filter:none}
section.art{padding:56px 0}
.box{transition:box-shadow .4s}.box:hover{box-shadow:10px 10px 0 #1d1a16}
@media (max-width:860px){.kps{grid-template-columns:1fr 1fr}.hero .stamp{display:none}}
"""
def build_hw23():
    V = W("Das2-3_Irachvelutyun_Kayunutyun_Hrachya_Aslanyan.xlsx"); c = C("hw23_concl.json")
    L = H.liq_block(V["Իրացվելիություն"], c["liq"]); S = H.stab_block(V["Կայունություն"], c["stab"])
    ok = str(L["verdict"]).startswith("✔"); w = V["Իրացվելիություն"]; s = V["Կայունություն"]
    k = kpis([(n(w["F14"].value, 0, True), "ընթացիկ իրացվելիություն"), (n(w["F18"].value, 3), "ընթացիկ գործակից"), (n(s["D6"].value, 0), "սեփական ընթացիկ ակտիվներ"), (n(s["D9"].value, 3), "անկախության գործակից")])
    body = topbar("Das2-3_Irachvelutyun_Kayunutyun_Hrachya_Aslanyan.xlsx", "lesson-2.html", "Դաս 2") + f"""
<div class="cur"><div class="np"><small>ՖԻՆԱՆՍԱԿԱՆ ՏԵՂԵԿԱԳԻՐ · №2–3</small><b>Արտակարգ<br>թողարկում</b><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
<section class="hero">{hero_slides("paper", [12, 0, 6, 3, 9])}<div class="inner wrap"><div class="kick fade-up">Ֆինանսական տեղեկագիր · Թողարկում №2–3 · 18.09.2026</div>
<h1 class="tl">{words("«XXX» ՍՊԸ-ն վճարունակ է, բայց ոչ բացարձակ")}</h1>
<div class="dl fade-up"><span>✒ Հրաչյա Ասլանյան, ԻՏ-447</span><span>📰 Դասեր 2 և 3</span><span>📊 Իրացվելիություն · կայունություն</span></div></div>
<span class="stamp {'ok' if ok else ''}">{E(L["verdict"][2:])}</span><span class="scue"></span></section>
<div class="wrap"><div class="kps">{k}</div>
<div class="lead"><div class="rv sl"><p class="dc">Ընկերության հաշվեկշիռը 260 000 հազ. դրամ է։ Ակտիվները դասավորեցինք ըստ այն բանի, թե որքան արագ կարող են դառնալ փող, իսկ պարտքերը՝ ըստ այն բանի, թե երբ պետք է վճարվեն։ Այնուհետև ստուգեցինք՝ արդյոք ընկերությունը կանգնած է սեփական ոտքերի վրա։</p>
<p>{E(c["liq"][0])}</p></div><figure class="rv sr" data-tilt><img src="{A}/paper/06.jpg" alt="" loading="lazy"><figcaption>Նկ. 1 · Չորս բանկա՝ չորս իրացվելիության խումբ</figcaption></figure></div></div>
{chapter("paper", 3, "I", "Չորս կշեռք", "Ա-խմբերն ընդդեմ Պ-խմբերի")}
<div class="wrap"><section class="art" id="excel"><div class="sub rv">Առաջադրանք 1 · Մաս Ա</div><h2 class="rv">Ա1–Ա4 ↔ Պ1–Պ4</h2>
<div class="two"><div class="rv sl">{L["groups"]}</div><div class="box rv sr">{L["pairs"]}</div></div></section>
<section class="art"><div class="sub rv">Առաջադրանք 1 · Մաս Բ</div><h2 class="rv">Գործակիցները նորմայի «միջանցքում»</h2>
<div class="two"><div class="rv sl">{L["ratios"]}</div><div class="box rv sr"><h3>Որտե՞ղ ենք նորմայի նկատմամբ</h3>{L["gauges"]}</div></div></section></div>
{marquee("paper", range(15))}
<div class="wrap"><section class="art"><div class="sub rv">Առաջադրանք 1 · Հարց 9</div><h2 class="rv">Ի՞նչ կլինի, եթե գնենք 30 000-ի պաշար</h2>
<div class="two"><div class="rv sl">{L["scen"]}<p class="pull">{E(c["liq"][1])}</p></div><div class="box rv sr">{L["scen_chart"]}</div></div></section></div>
{chapter("paper", 13, "II", "Կայունություն", "Որքանով է ընկերությունը կանգնած սեփական ոտքերի վրա")}
<div class="wrap"><section class="art"><div class="sub rv">Առաջադրանք 2</div><h2 class="rv">Արդյունք՝ «{E(S["type"])}»</h2>
<div class="two"><div class="rv sl">{S["ratios"]}</div><div class="box rv sr"><h3>Կայունության սանդղակ</h3>{S["gauges"]}</div></div>
<div class="cols rv" style="margin-top:22px"><p>{E(c["stab"][0])}</p><p>{E(c["stab"][1])}</p></div>
<h3 class="rv" style="margin-top:22px">Ինչպե՞ս ամրապնդել (հարց 7)</h3><div class="rv">{S["scen"]}</div></section></div>
{gallery("paper", range(15), "Ֆոտոարխիվ")}
<div class="wrap"><div class="foot">© H/R Studios · Հրաչյա Ասլանյան · Excel-ում բոլոր թվերը հաշվված են բանաձևերով (112 բանաձև, 0 սխալ)</div></div>"""
    return page("paper", "Իրացվելիություն և կայունություն", body, CSS_PAPER2, "Դասեր 2–3 տնային աշխատանք", 1900, "#b5452b")

# ================= 2) BLUEPRINT =================
CSS_BLUE2 = H.CSS_BLUE + r"""
.cur{background:#0b2a4a;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:40px 40px}
.cur svg{width:min(640px,86vw);overflow:visible}.cur svg *{fill:none;stroke:#dcecff;stroke-width:1.4;stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 1.5s cubic-bezier(.4,0,.2,1) forwards}
.cur svg .c2{stroke:#7cc4ff;animation-delay:.3s}.cur svg .c3{animation-delay:.6s}@keyframes draw{to{stroke-dashoffset:0}}
.cur .ty{position:absolute;bottom:14%;font:600 13px 'IBM Plex Mono';letter-spacing:.25em;color:#7cc4ff;overflow:hidden;white-space:nowrap;width:0;animation:type 1.2s steps(28) .4s forwards}@keyframes type{to{width:29ch}}
.cur::after{content:"";position:absolute;left:0;right:0;height:120px;background:linear-gradient(180deg,transparent,rgba(124,196,255,.25),transparent);animation:scan 1.8s linear infinite}@keyframes scan{from{top:-120px}to{top:100%}}
.hero{background:#06223f;margin:0!important}.chap,.gal{margin:0!important}.hero .hs img{filter:grayscale(.3) brightness(.55) saturate(1.2) hue-rotate(-10deg)}
.hero::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(11,42,74,.35),rgba(11,42,74,.95)),linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:auto,50px 50px,50px 50px}
.hero .inner{padding-bottom:60px}.hero h1{font-weight:300;font-size:clamp(38px,6.6vw,92px);line-height:1;margin:14px 0}.hero h1 b{font-weight:700}
.hero p{max-width:640px;color:#cfe3fb;font-size:17px;line-height:1.65}
.xh{position:absolute;z-index:3;inset:0;pointer-events:none}.xh i{position:absolute;background:#7cc4ff;opacity:.5}.xh .h{left:0;right:0;top:38%;height:1px;transform:scaleX(0);transform-origin:left;transition:transform 1.4s .5s}
.xh .v{top:0;bottom:0;left:72%;width:1px;transform:scaleY(0);transform-origin:top;transition:transform 1.4s .7s}body.ready .xh i{transform:none}
.xh b{position:absolute;left:72%;top:38%;width:46px;height:46px;margin:-23px;border:1px solid #7cc4ff;border-radius:50%;opacity:0;transition:opacity .5s 1.6s}body.ready .xh b{opacity:1;animation:pulse 2s 2s infinite}
@keyframes pulse{50%{transform:scale(1.4);opacity:.3}}
.kpis .frame{transition:transform .4s,box-shadow .4s}.kpis .frame:hover{transform:translateY(-6px);box-shadow:0 0 0 1px #7cc4ff,0 20px 40px rgba(0,0,0,.4)}
.chap{color:#fff}.chap .chi{filter:brightness(.45) saturate(1.2)}.chap::after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:40px 40px}
.chap .chn{font:600 clamp(60px,11vw,150px) 'IBM Plex Mono';color:#7cc4ff}
.mq{border-top:1px dashed rgba(220,236,255,.35);border-bottom:1px dashed rgba(220,236,255,.35)}.mqt img{filter:grayscale(.2);border:1px solid rgba(220,236,255,.5);border-radius:0}
.gi{border-radius:0;border:1px solid rgba(220,236,255,.4)}.gal h2{font-weight:300}
"""
def build_hw4():
    V = W("Das4_Himnakan_mijocner_Hrachya_Aslanyan.xlsx"); c = C("hw4_concl.json"); F = H.fa_block(V["Հիմնական միջոցներ"], c["fa"])
    k = "".join(f'<div class="frame rv" style="--i:{i}" data-tilt><b data-count="{re.sub("[^0-9.+-]","",a.replace(",","").replace("−","-"))}" data-d="{len(a.split(".")[1]) if "." in a else 0}" data-pre="{"+" if a.startswith("+") else ""}">{a}</b><span>{E(b)}</span></div>' for i, (a, b) in enumerate(F["kpi"]))
    draw = ('<svg viewBox="0 0 640 360"><rect x="60" y="80" width="300" height="200"/><rect class="c2" x="100" y="120" width="120" height="80"/><circle class="c2" cx="290" cy="180" r="50"/><circle class="c3" cx="290" cy="180" r="22"/>'
            '<path class="c3" d="M360 180 H580 M580 140 V220 M60 300 H360 M60 292 V308 M360 292 V308 M420 60 L560 60 L560 300 L420 300 Z M440 90 H540 M440 120 H540 M440 150 H520"/></svg>')
    body = topbar("Das4_Himnakan_mijocner_Hrachya_Aslanyan.xlsx", "lesson-4.html", "Դաս 4") + f"""
<div class="cur">{draw}<div class="ty">DWG-04 · ԲԵՌՆՎՈՒՄ Է ԳԾԱԳԻՐԸ…</div></div>
<section class="hero">{hero_slides("blue", [9, 12, 0, 6, 3])}<div class="xh"><i class="h"></i><i class="v"></i><b></b></div>
<div class="inner wrap"><div class="tag fade-up">DWG-04 · ԴԱՍ 4 · 25.09.2026 · ՀԵՂԻՆԱԿ՝ Հ. ԱՍԼԱՆՅԱՆ</div><h1 class="tl">{words("Հիմնական միջոցների")}<br><b>{words("տեխնիկական անձնագիր", 2)}</b></h1>
<p class="fade-up">Մեքենաները, շենքերն ու սարքավորումները ընկերության «երկաթե կմախքն» են։ Չափել ենք՝ որքան են դրանք, որքան են մաշված, որքան արագ են նորացվում և քանի դրամ շահույթ է բերում յուրաքանչյուր դրամ ՀՄ։</p></div><span class="scue" style="color:#7cc4ff"></span></section>
<div class="wrap"><div class="kpis" style="margin-top:40px">{k}</div>
<section class="rv" id="excel"><h2><i>01</i>Մուտքային տվյալներ</h2><div class="frame"><span class="lbl">ԱՂՅՈՒՍԱԿ Ա</span>{F["inputs"]}</div></section></div>
{chapter("blue", 0, "02", "Վիճակ և շարժ", "Նորացում, դուրսգրում, մաշվածություն, պիտանելիություն")}
<div class="wrap"><section class="rv"><h2><i>02</i>Արդյունքային ցուցանիշներ</h2><div class="frame"><span class="lbl">ԱՂՅՈՒՍԱԿ Բ · 14 ՑՈՒՑԱՆԻՇ</span>{F["out"]}</div></section>
<section><h2 class="rv"><i>03</i>Վիճակի գործակիցներ</h2><div class="g2"><div class="frame rv sl"><span class="lbl">ԳԾ. 1 · ԳՈՐԾԱԿԻՑՆԵՐ</span>{F["state"]}</div><div class="note rv sr">{E(c["fa"][0])}</div></div></section></div>
{marquee("blue", range(15))}
{chapter("blue", 8, "04", "Շահութաբերություն", "ՇԲԹՀՄ = ՇԲԹիրաց × ՀՏ")}
<div class="wrap"><section><h2 class="rv"><i>04</i>Գործոնային վերլուծություն</h2><div class="g2"><div class="frame rv sl"><span class="lbl">ԳԾ. 2 · ՋՐՎԵԺ</span>{F["wf"]}</div><div class="note rv sr">{E(c["fa"][1])}<br><br><code>Δ(ՇԲԹիրաց) = ΔՇԲԹիրաց × ՀՏ₀</code><br><code>Δ(ՀՏ) = ΔՀՏ × ՇԲԹիրաց₁</code></div></div></section></div>
{gallery("blue", range(15), "Գծագրեր և արտադրամաս")}
<div class="wrap"><div class="foot"><span>H/R STUDIOS · ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ · ԻՏ-447</span><span>ԹԵՐԹ 1/1 · EXCEL՝ 84 ԲԱՆԱՁԵՎ · 0 ՍԽԱԼ</span></div></div>"""
    return page("blueprint", "Հիմնական միջոցներ", body, CSS_BLUE2, "Դաս 4 տնային աշխատանք", 2000, "#7cc4ff")

# ================= 3) SWISS =================
CSS_SWISS2 = H.CSS_SWISS + r"""
.cur{background:#fff}.cur i{position:absolute;top:0;bottom:0;width:34%;animation:bar 1.1s cubic-bezier(.7,0,.2,1) both}
.cur i:nth-child(1){left:0;background:#e30613;animation-delay:.1s}.cur i:nth-child(2){left:33%;background:#111;animation-delay:.25s}.cur i:nth-child(3){left:66%;background:#e30613;animation-delay:.4s}
@keyframes bar{from{transform:translateY(100%)}to{transform:none}}
.cur b{position:relative;z-index:2;color:#fff;font:900 clamp(120px,26vw,320px)/1 'Noto Sans Armenian';letter-spacing:-.06em;animation:pop .6s cubic-bezier(.3,1.6,.5,1) .8s both;mix-blend-mode:difference}
@keyframes pop{from{transform:scale(.3);opacity:0}}
.hero{min-height:92vh;align-items:stretch;display:grid;grid-template-columns:5fr 7fr}
.hero .red{background:#e30613;color:#fff;padding:40px 30px;display:flex;flex-direction:column;justify-content:space-between;position:relative;z-index:3;transform:translateX(-100%);transition:transform 1s cubic-bezier(.7,0,.2,1) .1s}
body.ready .hero .red{transform:none}.hero .red .no{font-weight:900;font-size:clamp(130px,19vw,260px);line-height:.8;letter-spacing:-.06em}
.hero .red p{font-size:15.5px;line-height:1.55;max-width:380px}.hero .ph{position:relative;overflow:hidden;background:#111}
.hero .ph h1{position:absolute;left:30px;bottom:30px;right:30px;margin:0;z-index:3;color:#fff;font-weight:900;font-size:clamp(36px,5.8vw,86px);line-height:.95;letter-spacing:-.03em;text-shadow:0 2px 30px rgba(0,0,0,.4)}
.hero .ph .hs img{filter:contrast(1.1)}.hero .ph::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.65))}
.strip b{color:#111}.strip div{position:relative;overflow:hidden}.strip div::before{content:"";position:absolute;left:0;top:0;height:6px;width:0;background:#e30613;transition:width 1.2s .3s}.strip div.in::before{width:100%}
.chap{color:#fff}.chap .chi{filter:grayscale(.2) contrast(1.15) brightness(.55)}.chap .chn{color:#e30613;font-size:clamp(100px,18vw,240px);letter-spacing:-.06em}
.chap h2{font-weight:900;letter-spacing:-.02em}
.mq{background:#111}.mqt img{border-radius:0}
.gi{border-radius:0}.gal h2{font-weight:900;letter-spacing:-.02em}.gal h2::after{content:".";color:#e30613}
.chap{grid-template-columns:1fr!important}.gal{display:block!important}section>h2{transition:background .4s,color .4s}section:hover>h2{background:#e30613;color:#fff}section:hover>h2 small{color:#fff}
@media (max-width:900px){.hero{grid-template-columns:1fr}.hero .ph{min-height:360px}}
"""
def build_hw5():
    V = W("Das5_Nyutakan_pasharner_Hrachya_Aslanyan.xlsx"); c = C("hw5_concl.json")
    M = H.mat_block(V["ՆՊ 1"], c["mat"]); P = H.np2_block(V["ՆՊ 2"], c["np2"])
    k = kpis(M["kpi"], "rv")
    k = k.replace('class="rv rv"', 'class="rv"')
    body = topbar("Das5_Nyutakan_pasharner_Hrachya_Aslanyan.xlsx", "lesson-5.html", "Դաս 5") + f"""
<div class="cur"><i></i><i></i><i></i><b>05</b></div>
<section class="hero"><div class="red"><div class="no">05</div><p><b>Նյութական պաշարներ.</b> Որքան հումք ու նյութ է «ուտում» միավոր արտադրանքը, և ինչ է փոխվել, երբ գները, նորմաներն ու տեսականին շարժվել են։<br><br>Հրաչյա Ասլանյան · ԻՏ-447 · 03.10.2026</p></div>
<div class="ph">{hero_slides("swiss", [9, 3, 12, 6, 0])}<h1 class="tl">{words("Ավելի քիչ նյութ. Ավելի շատ շահույթ.")}</h1></div></section>
<div class="strip">{k}</div>
<section id="excel"><h2 class="rv"><small>ՏՆԱՅԻՆ 1</small>Յոթ նյութ, երկու տարի</h2><div><div class="g2"><div class="rv sl">{M["mats"]}</div><div class="rv sr">{M["bars"]}</div></div></div></section>
<section><h2 class="rv"><small>ՏՆԱՅԻՆ 1</small>Ութ ցուցանիշ</h2><div><div class="rv">{M["out"]}</div><p class="txt rv" style="margin-top:20px">{E(c["mat"][0])}</p></div></section>
{chapter("swiss", 3, "Δ", "Ինչու՞ աճեց շահութաբերությունը")}
<section><h2 class="rv"><small>ՏՆԱՅԻՆ 1</small>Գործոններ</h2><div><div class="g2"><div class="rv sl">{M["wf"]}</div><p class="txt rv sr">{E(c["mat"][1])}</p></div></div></section>
{marquee("swiss", range(15))}
<section><h2 class="rv"><small>ՏՆԱՅԻՆ 2</small>Երեք արտադրանք՝ «Ա», «Բ», «Գ»</h2><div class="rv">{P["data"]}</div></section>
{chapter("swiss", 9, "Նտ", "Շղթայական տեղադրում", "Տեսականի → նորմա → նյութի գին → արտադրանքի գին")}
<section><h2 class="rv"><small>ՏՆԱՅԻՆ 2</small>Չորս գործոն</h2><div><div class="g2"><div class="rv sl">{P["steps"]}<p class="txt" style="margin-top:16px">{E(c["np2"])}</p></div><div class="rv sr">{P["wf"]}</div></div></div></section>
{gallery("swiss", range(15), "Պատկերներ")}
<div class="foot"><span>H/R Studios</span><span>Excel · 100 բանաձև · 0 սխալ</span></div>"""
    return page("swiss", "Նյութական պաշարներ", body, CSS_SWISS2, "Դաս 5 տնային աշխատանք", 1700, "#e30613")

# ================= 4) NOTEBOOK =================
CSS_NOTE2 = H.CSS_NOTE + r"""
.cur{background:#fdfaf3;perspective:1600px}.cur .cv{width:min(520px,82vw);aspect-ratio:3/4;background:#6a4c93;border-radius:6px 16px 16px 6px;box-shadow:0 30px 60px rgba(106,76,147,.35);
 transform-origin:left center;animation:open 1.2s cubic-bezier(.6,0,.3,1) .6s forwards;display:grid;place-items:center;color:#fff;text-align:center;position:relative}
.cur .cv::before{content:"";position:absolute;left:18px;top:0;bottom:0;width:10px;background:rgba(0,0,0,.15)}.cur .cv b{font:700 52px 'Caveat','Noto Sans Armenian'}.cur .cv small{display:block;font-size:15px;opacity:.8}
.cur .cv i{position:absolute;right:-18px;top:30px;width:90px;height:34px;background:#ffd6e0;transform:rotate(8deg)}
@keyframes open{to{transform:rotateY(-110deg);opacity:.2}}
.hero{min-height:94vh;align-items:center;padding:20px 0 0!important}.hero .inner{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:30px;align-items:center}
.hero h1{font-family:'Caveat','Noto Sans Armenian';font-size:clamp(28px,3.2vw,46px);line-height:1.02;margin:6px 0 14px;color:#6a4c93}
.hero h1 u{text-decoration:none;background:linear-gradient(transparent 62%,#ffe066 62%);background-size:0 100%;background-repeat:no-repeat;transition:background-size 1s 1.4s}body.ready .hero h1 u{background-size:100% 100%}
.hero p{font-size:17px;line-height:1.75;max-width:560px}.hero h1 .w:last-child{background:linear-gradient(transparent 62%,#ffe066 62%) no-repeat;background-size:0 100%;transition:all .9s cubic-bezier(.2,.8,.2,1) calc(var(--k)*.08s + .2s),background-size 1s 1.4s}body.ready .hero h1 .w:last-child{background-size:100% 100%}
.pols{position:relative;height:460px}.pol{position:absolute;width:62%;background:#fff;padding:10px 10px 38px;box-shadow:0 16px 34px rgba(0,0,0,.18);opacity:0;transition:all 1s cubic-bezier(.3,1.4,.5,1)}
.pol img{aspect-ratio:4/3;object-fit:cover;width:100%}.pol span{position:absolute;bottom:8px;left:0;right:0;text-align:center;font:700 22px 'Caveat','Noto Sans Armenian';color:#6a4c93}
.pol:nth-child(1){left:2%;top:4%;transform:rotate(-30deg) translateY(-200px);transition-delay:.5s}.pol:nth-child(2){right:0;top:22%;transform:rotate(30deg) translateY(-200px);transition-delay:.75s}.pol:nth-child(3){left:18%;top:46%;transform:rotate(-20deg) translateY(-200px);transition-delay:1s}
body.ready .pol{opacity:1}body.ready .pol:nth-child(1){transform:rotate(-7deg)}body.ready .pol:nth-child(2){transform:rotate(6deg)}body.ready .pol:nth-child(3){transform:rotate(-2deg)}
.pol:hover{z-index:5;transform:rotate(0) scale(1.06)!important;transition-delay:0s}
.pol::before{content:"";position:absolute;top:-12px;left:50%;width:90px;height:24px;margin-left:-45px;background:rgba(242,132,130,.5);transform:rotate(-3deg)}
.stick div{transition:transform .35s}.stick div:hover{transform:rotate(0) scale(1.05)!important}
.page{transition:transform .5s,box-shadow .5s}.page:hover{box-shadow:0 22px 50px rgba(106,76,147,.22)}
.chap{color:#fff}.chap .chi{filter:saturate(.9) brightness(.62)}.chap .chn{font:700 clamp(80px,14vw,180px) 'Caveat','Noto Sans Armenian';color:#ffe066}
.chap h2{font-family:'Caveat','Noto Sans Armenian';font-size:clamp(40px,6vw,70px)}
.mqt img{border-radius:4px;border:8px solid #fff;box-shadow:0 8px 18px rgba(0,0,0,.12);transform:rotate(-1.5deg)}.mqt img:nth-child(even){transform:rotate(1.5deg)}.mq{padding:24px 0}
.gal h2{font-family:'Caveat','Noto Sans Armenian';color:#6a4c93;font-size:clamp(40px,5vw,60px)}.gi{border:8px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.12);border-radius:4px}
.gi:nth-child(odd){transform:rotate(-1.2deg)}.gi:nth-child(even){transform:rotate(1.2deg)}
@media (max-width:900px){.hero .inner{grid-template-columns:1fr}.pols{height:380px}}
"""
def build_hw6():
    V = W("Das6_Ashkhatank_Hrachya_Aslanyan.xlsx"); c = C("hw6_concl.json"); Ab = H.lab_block(V["Աշխատանք"], c["lab"])
    k = kpis(Ab["kpi"], "rv")
    pols = "".join(f'<div class="pol"><img src="{A}/note/{i:02d}.jpg" alt=""><span>{E(t)}</span></div>' for i, t in [(9, "մեր թիմը ✿"), (6, "ժամացույց ⏱"), (3, "գծապատկեր ✎")])
    body = topbar("Das6_Ashkhatank_Hrachya_Aslanyan.xlsx", "lesson-6.html", "Դաս 6") + f"""
<div class="cur"><div class="cv"><div><b>Տնային № 6</b><small>Հրաչյա Ասլանյան · ԻՏ-447</small></div><i></i></div></div>
<section class="hero"><div class="inner wrap"><div><div class="hand fade-up" style="font-size:28px;color:#f28482">Տնային № 6 · 10.10.2026</div>
<h1 class="tl">{words("Մարդիկ, ժամեր և")}<br>{words("արտադրողականություն", 3)}</h1>
<p class="fade-up">Ընկերությունում 231 մարդ է աշխատում։ Հաշվեցինք՝ քանի ժամ են նրանք իրականում աշխատել, ինչու է փոխվել այդ ժամաքանակը և ինչն է բարձրացրել մեկ աշխատողի արդյունքը։ Ամեն ինչ՝ շղթայական տեղադրման եղանակով։</p></div>
<div class="pols">{pols}</div></div></section>
<div class="wrap"><div class="stick">{k}</div>
<div class="page rv" id="excel"><h2><em>0</em>Ինչ ունենք (տվյալներ)</h2>{Ab["inputs"]}</div></div>
{chapter("note", 6, "1", "Աշխատաժամանակի ֆոնդ", "Ֆ = Թ × Օ × Ժ")}
<div class="wrap"><div class="page rv"><h2><em>1</em>Աշխատաժամանակի ֆոնդ</h2><div class="g2"><div>{Ab["a1"]}<p class="memo" style="margin-top:18px">Ֆ = Թ × Օ × Ժ<br>{E(c["lab"][0])}</p></div><div class="rv sr">{Ab["wf1"]}</div></div></div></div>
{marquee("note", range(15))}
{chapter("note", 11, "2", "Արտադրողականություն", "ՏԱ = ՏԿ × Օ × Ժ × ԺԱ")}
<div class="wrap"><div class="page rv"><h2><em>2</em>Արտադրողականություն</h2>{Ab["a2"]}<div class="g2" style="margin-top:18px"><div>{Ab["f2"]}</div><div class="rv sr">{Ab["wf2"]}</div></div>
<p class="memo" style="margin-top:18px">ՏԱ = ՏԿ × Օ × Ժ × ԺԱ<br>{E(c["lab"][1])}</p></div>
<div class="page rv"><h2><em>+</em>Մեր կողմից ավելացված</h2>{Ab["ex"]}</div></div>
{gallery("note", range(15), "Մեր ալբոմը ✿")}
<div class="wrap"><div class="foot">— Հրաչյա Ասլանյան, ԻՏ-447 · Excel՝ 91 բանաձև, 0 սխալ ✓</div></div>"""
    return page("notebook", "Աշխատանքային ռեսուրսներ", body, CSS_NOTE2, "Դաս 6 տնային աշխատանք", 1900, "#6a4c93")

# ================= 5) MIJANKYAL — the original submission (liquid glass, lime/cyan) =================
CSS_MIJ = r"""
body{background:#07090d;color:#eef3fb;font-family:'Noto Sans Armenian',sans-serif}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:radial-gradient(40% 35% at 15% 10%,rgba(212,255,58,.18),transparent 70%),radial-gradient(40% 40% at 88% 30%,rgba(45,226,230,.16),transparent 70%),radial-gradient(45% 40% at 70% 100%,rgba(255,160,90,.12),transparent 70%)}
.topbar{background:rgba(7,9,13,.6);backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,.08)}.topbar a.b{border:1px solid rgba(255,255,255,.18);border-radius:99px;color:#eef3fb}.topbar a.x{background:#d4ff3a;color:#111;border-color:#d4ff3a}
.g{background:linear-gradient(145deg,rgba(255,255,255,.09),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-radius:26px;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.cur{background:#07090d}.cur .bl{position:absolute;width:44vmin;height:44vmin;border-radius:50%;filter:blur(40px);opacity:.85;animation:blob 2s ease-in-out infinite alternate}
.cur .bl.a{background:#d4ff3a;left:24%;top:24%}.cur .bl.b{background:#2de2e6;right:22%;bottom:22%;animation-delay:-.8s}@keyframes blob{to{transform:translate(40px,-30px) scale(1.15)}}
.cur .gx{position:relative;z-index:2;padding:34px 46px;border-radius:30px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);backdrop-filter:blur(24px);text-align:center;animation:gin .9s cubic-bezier(.2,.8,.2,1) both}
.cur .gx b{display:block;font-size:clamp(60px,12vw,130px);line-height:1;background:linear-gradient(90deg,#d4ff3a,#2de2e6);-webkit-background-clip:text;background-clip:text;color:transparent}.cur .gx small{letter-spacing:.3em;font-size:12px;opacity:.8}
@keyframes gin{from{transform:scale(.7);opacity:0;filter:blur(20px)}}
body.ready .cur .gx{transform:scale(1.3);filter:blur(16px);transition:all .7s}
.hero{min-height:100vh;align-items:center}.hero .hs img{filter:brightness(.55) saturate(1.2)}.hero::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(7,9,13,.2),rgba(7,9,13,.95))}
.hero .inner{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;align-items:center;padding:110px 0 70px}
.pill{display:inline-flex;gap:8px;align-items:center;padding:7px 14px;border-radius:99px;background:rgba(212,255,58,.14);border:1px solid rgba(212,255,58,.4);color:#d4ff3a;font:600 12.5px 'Noto Sans Armenian';letter-spacing:.12em}
.hero h1{font-size:clamp(40px,6.4vw,92px);line-height:.98;margin:18px 0;font-weight:700;letter-spacing:-.02em}.hero h1 .gr{background:linear-gradient(90deg,#d4ff3a,#2de2e6);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:#b8c3d8;font-size:17px;line-height:1.7;max-width:560px}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}.bt{display:inline-flex;align-items:center;gap:8px;padding:12px 18px;border-radius:99px;text-decoration:none;font-weight:700;font-size:14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:#eef3fb;transition:transform .25s,background .25s}
.bt:hover{transform:translateY(-3px);background:rgba(255,255,255,.16)}.bt.p{background:#d4ff3a;color:#111;border-color:#d4ff3a}.bt.p:hover{box-shadow:0 0 30px rgba(212,255,58,.5)}
.dcard{padding:12px;transform:perspective(1200px) rotateY(-10deg) rotateX(4deg);transition:transform .6s}.dcard:hover{transform:none}.dcard img{border-radius:16px}
.meta{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:-40px 0 30px;position:relative;z-index:5}.meta .g{padding:16px 18px;border-radius:20px}.meta b{display:block;font-size:22px}.meta span{font-size:12px;color:#98a3bb;letter-spacing:.1em}
.kpg{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.kp{padding:18px;border-radius:20px}.kp b{display:block;font-size:30px;font-weight:700;color:#d4ff3a}.kp:nth-child(even) b{color:#2de2e6}.kp span{font-size:13px;color:#98a3bb}
.tabs{display:flex;gap:6px;padding:6px;border-radius:99px;width:max-content;max-width:100%;overflow-x:auto;margin:40px 0 22px;position:sticky;top:64px;z-index:20}
.tabs button{all:unset;cursor:pointer;padding:10px 18px;border-radius:99px;color:#98a3bb;font-weight:600;font-size:14px;white-space:nowrap}.tabs button.on{background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.2)}
[data-pane]{display:none}[data-pane].on{display:block;animation:pin .6s cubic-bezier(.2,.8,.2,1)}@keyframes pin{from{opacity:0;transform:translateY(16px)}}
.frame{padding:10px;border-radius:26px}.frame iframe{display:block;width:100%;height:82vh;border:0;border-radius:18px;background:#090b10}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:14px}.shots a{display:block;border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.12)}.shots img{transition:transform .6s}.shots a:hover img{transform:scale(1.05)}
.viewer{display:grid;grid-template-columns:1fr 220px;gap:16px}.vp{position:relative;padding:16px;border-radius:26px;display:grid;place-items:center;min-height:70vh}
.vp img{max-height:78vh;width:auto;border-radius:8px;box-shadow:0 30px 60px rgba(0,0,0,.5);transition:opacity .3s,transform .4s}.vp img.sw{opacity:0;transform:translateX(30px) rotateY(-12deg)}
.vp .nv{position:absolute;top:50%;width:46px;height:46px;margin-top:-23px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:rgba(0,0,0,.4);color:#fff;font-size:20px;cursor:pointer;backdrop-filter:blur(8px)}.vp .nv:hover{background:#d4ff3a;color:#111}
.vp .pv{left:14px}.vp .nx{right:14px}.vp .pc{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);font:600 13px 'Noto Sans Armenian';padding:6px 12px;border-radius:99px;background:rgba(0,0,0,.5)}
.th{max-height:78vh;overflow-y:auto;display:grid;gap:8px;padding:8px;border-radius:20px}.th img{border-radius:6px;cursor:pointer;opacity:.55;transition:opacity .3s,outline-color .3s;outline:2px solid transparent}.th img.on,.th img:hover{opacity:1;outline-color:#d4ff3a}
.sheets{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.sh{padding:20px;border-radius:22px}.sh b{color:#d4ff3a;font-size:13px;letter-spacing:.15em}.sh h3{margin:6px 0 6px;font-size:18px}.sh p{margin:0;color:#98a3bb;font-size:14px;line-height:1.55}
table{color:#eef3fb}thead th{color:#98a3bb;font-weight:600;font-size:12px;border-bottom:1px solid rgba(255,255,255,.15)}tbody tr{border-bottom:1px solid rgba(255,255,255,.07)}tbody tr:hover{background:rgba(255,255,255,.04)}
.chap{color:#fff}.chap .chi{filter:brightness(.5) saturate(1.2)}.chap .chn{background:linear-gradient(90deg,#d4ff3a,#2de2e6);-webkit-background-clip:text;background-clip:text;color:transparent}
.gi{border:1px solid rgba(255,255,255,.12)}.foot{padding:40px 0 70px;text-align:center;color:#98a3bb;font-size:13px}
.dl3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.dl3 a{padding:22px;border-radius:22px;text-decoration:none;color:#eef3fb;transition:transform .3s}.dl3 a:hover{transform:translateY(-5px)}.dl3 b{display:block;font-size:19px;margin:8px 0 4px}.dl3 span{color:#98a3bb;font-size:13px}.dl3 i{font-style:normal;font-size:28px}
@media (max-width:900px){.hero .inner,.viewer{grid-template-columns:1fr}.meta{grid-template-columns:1fr 1fr}.kpg,.sheets,.dl3{grid-template-columns:1fr 1fr}.th{display:flex;max-height:none;overflow-x:auto}.th img{width:80px}.frame iframe{height:70vh}}
"""
MIJ_JS = r"""<script>(function(){const P=[...document.querySelectorAll('.th img')],im=document.getElementById('pimg'),pc=document.getElementById('pcnt');let k=0;
function go(i){k=(i+P.length)%P.length;im.classList.add('sw');setTimeout(()=>{im.src=P[k].dataset.full;im.onload=()=>im.classList.remove('sw')},180);P.forEach((p,j)=>p.classList.toggle('on',j===k));pc.textContent=(k+1)+' / '+P.length;P[k].scrollIntoView({block:'nearest',inline:'nearest'})}
P.forEach((p,i)=>p.onclick=()=>go(i));document.getElementById('ppv').onclick=()=>go(k-1);document.getElementById('pnx').onclick=()=>go(k+1);
addEventListener('keydown',e=>{const pane=document.querySelector('[data-pane="pdf"]');if(!pane.classList.contains('on'))return;if(e.key==='ArrowRight')go(k+1);if(e.key==='ArrowLeft')go(k-1)});
let x0=null;im.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});im.addEventListener('touchend',e=>{if(x0===null)return;const d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)go(k+(d<0?1:-1));x0=null});})();</script>"""

def build_mij():
    src = "/mnt/user-data/attachments/1b9ee954-a10c-534a-9dd9-c7dff3e4538d/ee34ae29-Homework_n5_Excel.xlsx"
    wb = openpyxl.load_workbook(os.path.join(SITE, "files", "Mijankyal_Hrachya_Aslanyan_N5.xlsx"), data_only=True); g = wb["Գլխավոր"]
    rows = [r for r in g.iter_rows(min_row=9, max_row=21, values_only=True)]
    def fv(v):
        if isinstance(v, float): return n(v, 3) if abs(v) < 100 else n(v, 2)
        if isinstance(v, int): return n(v)
        return E(v)
    tbl = table(["Ցուցանիշ", "Արժեք", "Նորմա / նշում", "Խնդիր"], [[E(r[1]), f"<b>{fv(r[2])}</b>", E(r[3] or "—"), f'<span class="pill" style="padding:3px 10px">{E(r[4])}</span>'] for r in rows])
    npdf = len([f for f in os.listdir(os.path.join(SITE, "hw", "mijankyal", "pdf")) if not f.endswith("_s.jpg")])
    th = "".join(f'<img src="pdf/p-{i:02d}_s.jpg" data-full="pdf/p-{i:02d}.jpg" alt="Էջ {i}" class="{"on" if i == 1 else ""}" loading="lazy">' for i in range(1, npdf + 1))
    dnames = ["Վահանակ", "Խ1 · Իրացվելիություն", "Խ2 · Կայունություն", "Խ3 · Հիմնական միջոցներ", "Խ4 · Նյութական պաշարներ", "Խ5 · Աշխատանք"]
    shots = "".join(f'<a href="{f}" data-lb class="rv" style="--i:{i}"><img src="{f}" alt="{E(t)}" loading="lazy"></a>' for i, (f, t) in enumerate(zip(["dash.jpg"] + [f"dash{k}.jpg" for k in range(1, 6)], dnames)))
    sheets = [("Գլխավոր", "Ամփոփում", "Ուսանող, խումբ, մատյանի համար (n)՝ փոխելիս բոլոր թվերը վերահաշվարկվում են։"),
              ("Խ1", "Իրացվելիություն", "Ձևափոխված հաշվեկշիռ (n×10 000), Ա/Պ խմբեր, ԳԲԻ, ԳԱԻ, ԳԸԻ, հարց 9-ի գործարք։"),
              ("Խ2", "Կայունություն", "ՍԸԱ, անկախություն, ֆին. ռիսկ, կայունության տիպ {1;1;1}, սցենարներ։"),
              ("Խ3", "Հիմնական միջոցներ", "Զինվածություն, նորացում, մաշվածություն, ՇԲԹՀՄ, հարաբերական գերածախս։"),
              ("Խ4", "Նյութական պաշարներ", "Նյութատարություն, նյութահատույց, ՇԲԹնծ-ի գործոնային վերլուծություն։"),
              ("Խ5", "Աշխատանք", "Աշխատաժամանակի ֆոնդ, ՏԱ, գործոնների ազդեցություն։")]
    sh = "".join(f'<div class="sh g rv" style="--i:{i}" data-tilt><b>{E(a)}</b><h3>{E(b)}</h3><p>{E(c_)}</p></div>' for i, (a, b, c_) in enumerate(sheets))
    k = kpis([("0.423", "Բացարձակ իրացվելիություն"), ("1.683", "Ընթացիկ իրացվելիություն"), ("0.429", "Ֆին. անկախություն"), ("1.333", "Ֆին. ռիսկ"),
              ("333.3%", "ՇԲԹՀՄ"), ("2.000", "Նյութատարություն"), ("449,314", "Աշխ. ժամանակի ֆոնդ, ժ"), ("+9.16%", "ՏԱ-ի աճ")], "kp g")
    body = topbar("Mijankyal_Hrachya_Aslanyan_N5.xlsx", "works.html", "Աշխատանքներ") + f"""
<div class="cur"><i class="bl a"></i><i class="bl b"></i><div class="gx"><small>1-ԻՆ ՄԻՋԱՆԿՅԱԼ · ՄԱՏՅԱՆ</small><b>n = 5</b><small>ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ · IT447</small></div></div>
<section class="hero">{hero_slides("mij", [6, 12, 9, 3, 0])}<div class="inner wrap"><div><span class="pill fade-up">✓ ՀԱՆՁՆՎԱԾ Է ԴԱՍԱԽՈՍԻՆ · 1-ԻՆ ՄԻՋԱՆԿՅԱԼ</span>
<h1 class="tl">{words("Տնտեսական գործունեության")} <span class="gr">{words("վերլուծություն", 2)}</span></h1>
<p class="fade-up">5 խնդրի ամբողջական լուծում՝ բանաձև → հաշվարկ → եզրակացություն։ Երեք ձևաչափ՝ ինտերակտիվ դաշբորդ, 24 էջանոց PDF հաշվետվություն և Excel ֆայլ, որտեղ մատյանի համարը փոխելիս ամեն ինչ վերահաշվարկվում է։</p>
<div class="btns fade-up"><a class="bt p" href="#view">▶ Դիտել աշխատանքը</a><a class="bt" href="../../files/Mijankyal_Hrachya_Aslanyan_N5.pdf" download>⬇ PDF</a><a class="bt" href="../../files/Mijankyal_Hrachya_Aslanyan_N5.xlsx" download>⬇ Excel</a></div></div>
<a class="dcard g fade-up" href="#view" data-tilt><img src="dash2.jpg" alt="Դաշբորդ"></a></div><span class="scue"></span></section>
<div class="wrap"><div class="meta">{"".join(f'<div class="g rv" style="--i:{i}"><span>{E(a)}</span><b>{E(b)}</b></div>' for i, (a, b) in enumerate([("ՈՒՍԱՆՈՂ", "Հրաչյա Ասլանյան"), ("ԽՈՒՄԲ", "IT447"), ("ՄԱՏՅԱՆ", "n = 5"), ("ԴԱՍԱԽՈՍ", "Օ. Ա. Գալստյան"), ("ՈՒՍ. ՏԱՐԻ", "2026–2027")]))}</div>
<div class="kpg">{k}</div>
<div data-tabs id="view"><div class="tabs g"><button class="on" data-tab="dash">📊 Դաշբորդ</button><button data-tab="pdf">📄 PDF հաշվետվություն</button><button data-tab="xl">📗 Excel</button><button data-tab="dl">⬇ Ներբեռնել</button></div>
<div data-pane="dash" class="on"><div class="frame g"><iframe src="dashboard.html" title="Դաշբորդ" loading="lazy"></iframe></div>
<p style="color:#98a3bb;font-size:14px;margin:12px 4px">Դաշբորդը ինտերակտիվ է՝ սեղմեք ներդիրների վրա։ <a href="dashboard.html" target="_blank" style="color:#d4ff3a">Բացել ամբողջ էկրանով ↗</a></p><div class="shots">{shots}</div></div>
<div data-pane="pdf"><div class="viewer"><div class="vp g"><img id="pimg" src="pdf/p-01.jpg" alt="PDF էջ"><button class="nv pv" id="ppv" aria-label="Նախորդ">‹</button><button class="nv nx" id="pnx" aria-label="Հաջորդ">›</button><span class="pc" id="pcnt">1 / {npdf}</span></div><div class="th g">{th}</div></div></div>
<div data-pane="xl"><div class="sheets">{sh}</div><h3 style="margin:28px 0 12px">Գլխավոր թերթի ամփոփումը</h3><div class="g" style="padding:16px">{tbl}</div></div>
<div data-pane="dl"><div class="dl3"><a class="g" href="../../files/Mijankyal_Hrachya_Aslanyan_N5.pdf" download><i>📄</i><b>PDF հաշվետվություն</b><span>{npdf} էջ · բանաձևեր և եզրակացություններ</span></a>
<a class="g" href="../../files/Mijankyal_Hrachya_Aslanyan_N5.xlsx" download><i>📗</i><b>Excel ֆայլ</b><span>6 թերթ · գծապատկերներ · n-ը փոփոխելի</span></a><a class="g" href="dashboard.html" download="dashboard_mijankyal_hr_aslanyan_n_5.html"><i>📊</i><b>Դաշբորդ (HTML)</b><span>բացվում է ցանկացած բրաուզերում</span></a></div></div></div></div>
{chapter("mij", 9, "5/5", "Բոլոր խնդիրները լուծված են", "Իրացվելիություն · Կայունություն · Հիմնական միջոցներ · Նյութական պաշարներ · Աշխատանք")}
{gallery("mij", range(15), "Կադրեր")}
<div class="wrap"><div class="foot">© H/R Studios · Հրաչյա Ասլանյան · IT447 · 1-ին միջանկյալ, մատյան № 5</div></div>{MIJ_JS}"""
    return page("gold", "1-ին միջանկյալ · Հրաչյա Ասլանյան", body, CSS_MIJ, "1-ին միջանկյալ ստուգման աշխատանքը՝ դաշբորդ, PDF, Excel", 1900, "#d4ff3a")

PAGES = {"dasi-2-3": build_hw23, "dasi-4": build_hw4, "dasi-5": build_hw5, "dasi-6": build_hw6, "mijankyal": build_mij}
if __name__ == "__main__":
    for slug, fn in PAGES.items():
        d = os.path.join(SITE, "hw", slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf8").write(fn()); print("wrote", slug)
    old = os.path.join(SITE, "hw", "midterm-1")
    if os.path.isdir(old): shutil.rmtree(old); print("removed midterm-1")
