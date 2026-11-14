# -*- coding: utf-8 -*-
# v2 design layer: logo intro video, "My works" menu, generated imagery, richer motion.
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import gen
from gen import E, ICON, LESSONS, FILES, COURSE, TEACHER, SITE, file_card, slides_of, KIND

WORKS = [
 dict(t='Իրացվելիություն և ֆինանսական կայունություն', l='Դաս 2–3', img='liquidity', items=[('📰','Ինտերակտիվ հաշվետվություն («թերթ»)','hw/dasi-2-3/index.html','Առաջադրանք 1 և 2 · 9 գծապատկեր'),('📗','Excel լուծում','files/Das2-3_Irachvelutyun_Kayunutyun_Hrachya_Aslanyan.xlsx','112 բանաձև · 4 գծապատկեր')], page='lesson-2.html'),
 dict(t='Հիմնական միջոցների վերլուծություն', l='Դաս 4', img='factory', items=[('📐','Ինտերակտիվ «տեխնիկական անձնագիր»','hw/dasi-4/index.html','14 ցուցանիշ · գործոնային վերլուծություն'),('📗','Excel լուծում','files/Das4_Himnakan_mijocner_Hrachya_Aslanyan.xlsx','84 բանաձև · 2 գծապատկեր')], page='lesson-4.html'),
 dict(t='Նյութական պաշարների վերլուծություն', l='Դաս 5', img='warehouse', items=[('🟥','Ինտերակտիվ պաստառ','hw/dasi-5/index.html','Տնային 1 և 2 · շղթայական տեղադրում'),('📗','Excel լուծում','files/Das5_Nyutakan_pasharner_Hrachya_Aslanyan.xlsx','100 բանաձև · 3 գծապատկեր')], page='lesson-5.html'),
 dict(t='Աշխատանքային ռեսուրսների վերլուծություն', l='Դաս 6', img='team', items=[('📒','Ինտերակտիվ «տետր»','hw/dasi-6/index.html','2 վերլուծություն · 12 գործոն'),('📗','Excel լուծում','files/Das6_Ashkhatank_Hrachya_Aslanyan.xlsx','91 բանաձև · 2 գծապատկեր')], page='lesson-6.html'),
 dict(t='1-ին միջանկյալ · տնային (մատյան № 5)', l='Միջանկյալ', img='midterm', items=[('🏅','Ինտերակտիվ դոսյե · 5 խնդիր','hw/midterm-1/index.html','տվյալները փոփոխված են ըստ № 5-ի'),('📗','Excel լուծում','files/Midterm1_Matyan5_Hrachya_Aslanyan.xlsx','344 բանաձև · 10 գծապատկեր')], page='index.html#library'),
 dict(t='Դրամական միջոցների վերլուծություն', l='Դաս 7', img='cashflow', items=[('🎬','Անիմացիոն ներկայացում','t7/index.html','18 սլայդ'),('📊','Տվյալների սրահ (դաշբորդ)','t7/index.html#excel','բոլոր աղյուսակները'),('📗','Excel լուծում','files/Tema7_Dramakan_mijocner_Hrachya_Aslanyan.xlsx','527 բանաձև · 9 գծապատկեր')], page='lesson-7.html'),
 dict(t='Դեբիտորական և կրեդիտորական պարտքեր', l='Դաս 8', img='handshake', items=[('🎬','Անիմացիոն ներկայացում','t8/index.html','16 սլայդ'),('📊','Տվյալների սրահ (դաշբորդ)','t8/index.html#excel','9 բաժին'),('📗','Excel լուծում','files/Tema8-9_Debitor_Kreditor_Hrachya_Aslanyan.xlsx','376 բանաձև · 9 գծապատկեր')], page='lesson-8.html'),
]

CSS2 = r'''

.ltabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;scrollbar-width:thin}
.ltab{flex:none;text-align:left;border:1px solid var(--line);background:var(--glass);color:var(--sub);font:700 14px var(--body);padding:10px 16px;border-radius:16px;cursor:pointer;transition:all .2s}
.ltab small{display:block;font-weight:500;font-size:11.5px;color:var(--dim)}.ltab.on{background:linear-gradient(135deg,rgba(61,255,143,.2),rgba(92,214,255,.1));color:var(--tx);border-color:rgba(61,255,143,.55);box-shadow:0 10px 30px rgba(61,255,143,.15)}
.lpane{display:none;margin-top:16px;animation:paneIn .45s cubic-bezier(.2,.7,.2,1)}.lpane.on,.lpanes.q .lpane{display:block}.lpanes.q .lphead,.lpanes.q .hrpair{display:none}
@keyframes paneIn{from{opacity:0;transform:translateY(10px)}}
.lphead{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:14px}.lphead h3{margin:6px 0 0;font:800 24px var(--disp)}
.hrpair{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.hrc{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:20px;text-decoration:none;background:linear-gradient(135deg,rgba(61,255,143,.14),rgba(169,139,255,.08));border:1px solid rgba(61,255,143,.4);transition:transform .2s,box-shadow .2s}
.hrc:hover{transform:translateY(-3px);box-shadow:0 16px 40px rgba(61,255,143,.2)}.hrc b{display:block;font-size:15px}.hrc small{color:var(--sub);font-size:12.5px}.hrc i{margin-left:auto;font-style:normal;font-size:20px}
.hrc .ty{flex:none;width:46px;height:52px;border-radius:10px;display:grid;place-items:center;font:800 11px var(--num);color:#fff}
.ib.hrb{background:linear-gradient(135deg,rgba(61,255,143,.3),rgba(169,139,255,.2));border-color:rgba(61,255,143,.5)}
@media (max-width:640px){.hrpair{grid-template-columns:1fr}.lphead{flex-direction:column;align-items:flex-start}}
/* ===== v2 motion & imagery ===== */
.prog{position:fixed;top:0;left:0;height:3px;width:100%;transform-origin:0 50%;transform:scaleX(0);z-index:60;background:linear-gradient(90deg,var(--g),var(--c),var(--v));box-shadow:0 0 12px var(--g)}
.cglow{position:fixed;left:0;top:0;width:520px;height:520px;margin:-260px 0 0 -260px;border-radius:50%;pointer-events:none;z-index:0;background:radial-gradient(circle,rgba(61,255,143,.10),transparent 62%);transform:translate3d(-999px,-999px,0);transition:opacity .4s;will-change:transform}
@media (hover:none){.cglow{display:none}}
.logo .lim{height:34px;width:auto;border-radius:8px;filter:drop-shadow(0 0 12px rgba(61,255,143,.45))}
.works-btn{display:inline-flex;align-items:center;gap:8px;margin-left:6px;padding:8px 14px;border-radius:999px;border:1px solid rgba(61,255,143,.45);background:linear-gradient(135deg,rgba(61,255,143,.18),rgba(92,214,255,.10));color:var(--tx);font:700 13.5px var(--body);cursor:pointer;position:relative;overflow:hidden}
.works-btn::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%);transform:translateX(-120%);animation:shine 3.4s ease-in-out infinite 1s}
@keyframes shine{60%,100%{transform:translateX(120%)}}
.works-btn .dot{width:8px;height:8px;border-radius:50%;background:var(--g);box-shadow:0 0 10px var(--g);animation:pulse 1.8s infinite}
@keyframes pulse{50%{transform:scale(1.6);opacity:.5}}
.wpanel{position:fixed;top:72px;left:max(16px,calc((100vw - 1240px)/2));width:min(760px,calc(100vw - 32px));z-index:70;border-radius:24px;padding:20px;background:rgba(8,14,12,.94);border:1px solid rgba(255,255,255,.14);box-shadow:0 40px 100px rgba(0,0,0,.6),0 0 0 1px rgba(61,255,143,.08);backdrop-filter:blur(16px);opacity:0;transform:translateY(-10px) scale(.98);pointer-events:none;transition:opacity .25s,transform .3s cubic-bezier(.2,.7,.2,1);max-height:calc(100vh - 90px);overflow:auto}
.wpanel.on{opacity:1;transform:none;pointer-events:auto}
.wpanel h3{margin:0 0 4px;font:800 22px var(--disp)}.wpanel .sd2{color:var(--sub);font-size:13.5px;margin:0 0 14px}
.wgrp{display:grid;grid-template-columns:150px 1fr;gap:14px;padding:12px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid var(--line);margin-bottom:10px}
.wgrp .ph{border-radius:12px;background-size:cover;background-position:center;min-height:110px;position:relative}
.wgrp .ph b{position:absolute;left:8px;top:8px;font:800 11px var(--num);padding:3px 8px;border-radius:7px;background:rgba(0,0,0,.6);color:var(--g)}
.wgrp h4{margin:0 0 8px;font:700 16px var(--disp)}
.witem{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:12px;text-decoration:none;transition:background .2s}
.witem:hover{background:rgba(61,255,143,.1)}.witem .ic{font-size:20px}.witem b{display:block;font-size:14px}.witem small{color:var(--dim);font-size:12px}
.wfoot{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:6px}
/* hero v2 */
.hero2{position:relative;min-height:min(820px,96vh);display:flex;align-items:center;overflow:hidden}
.hero2 .bgi{position:absolute;inset:-6%;background-size:cover;background-position:center;opacity:.6;animation:kb 28s ease-in-out infinite alternate;will-change:transform}
@keyframes kb{from{transform:scale(1.02) translate3d(0,0,0)}to{transform:scale(1.14) translate3d(-2%,-2%,0)}}
.hero2::after{content:"";position:absolute;inset:0;background:radial-gradient(70% 70% at 70% 40%,transparent,rgba(5,9,8,.7)),linear-gradient(90deg,rgba(5,9,8,.95),rgba(5,9,8,.55) 55%,rgba(5,9,8,.2)),linear-gradient(0deg,var(--bg),transparent 30%)}
.orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:.55;z-index:1;animation:float 14s ease-in-out infinite alternate}
.orb.a{width:420px;height:420px;background:#3dff8f;right:8%;top:10%;opacity:.18}.orb.b{width:320px;height:320px;background:#5cd6ff;right:26%;bottom:6%;opacity:.16;animation-delay:-5s}.orb.c{width:260px;height:260px;background:#a98bff;right:-4%;bottom:24%;opacity:.14;animation-delay:-9s}
@keyframes float{to{transform:translate3d(-60px,40px,0) scale(1.15)}}
.hero2 .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.25fr .9fr;gap:40px;align-items:center;padding:90px 0 110px}
.hcard{position:relative;border-radius:28px;overflow:hidden;border:1px solid rgba(255,255,255,.16);box-shadow:0 40px 100px rgba(0,0,0,.55),0 0 60px rgba(61,255,143,.15);transform:perspective(1000px) rotateY(-8deg) rotateX(4deg);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.hcard:hover{transform:perspective(1000px) rotateY(0) rotateX(0)}
.hcard img{width:100%;aspect-ratio:16/10;object-fit:cover}
.hcard .cap{position:absolute;left:14px;right:14px;bottom:14px;padding:12px 16px;border-radius:16px;background:rgba(5,9,8,.72);backdrop-filter:blur(10px);border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:10px}
.hcard .cap b{font-size:14px}.hcard .cap small{display:block;color:var(--dim);font-size:12px}
.w{display:inline-block;opacity:0;transform:translateY(.5em);filter:blur(8px);animation:wIn .8s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--k)*90ms + .2s)}
@keyframes wIn{to{opacity:1;transform:none;filter:none}}
.marq{position:relative;overflow:hidden;border-block:1px solid var(--line);background:rgba(255,255,255,.02);padding:16px 0;-webkit-mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.marq .tr{display:flex;gap:46px;width:max-content;animation:mq 40s linear infinite}
.marq span{font:700 clamp(16px,2vw,22px) var(--disp);color:var(--sub);white-space:nowrap;display:flex;align-items:center;gap:46px}
.marq span::after{content:"✦";color:var(--g);font-size:.8em}
@keyframes mq{to{transform:translateX(-50%)}}
.sbg{position:relative;overflow:hidden}
.sbg>.bimg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.16;-webkit-mask:linear-gradient(180deg,transparent,#000 20%,#000 75%,transparent);mask:linear-gradient(180deg,transparent,#000 20%,#000 75%,transparent)}
.sbg>.wrap{position:relative}
.lc .im{height:170px}.lc .im{transition:transform .6s cubic-bezier(.2,.7,.2,1)}.lc:hover .im{transform:scale(1.06)}
.lc{transform-style:preserve-3d;will-change:transform}
.lc .shine{position:absolute;inset:0;pointer-events:none;background:radial-gradient(400px circle at var(--mx,50%) var(--my,0%),rgba(255,255,255,.12),transparent 40%);opacity:0;transition:opacity .3s}
.lc:hover .shine{opacity:1}
.feature{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center}
.feature .pic{border-radius:26px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px rgba(0,0,0,.5);position:relative}
.feature .pic img{width:100%;aspect-ratio:16/10;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.feature .pic:hover img{transform:scale(1.05)}
.feature .pic::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,9,8,.5),transparent 50%)}
.bul{display:grid;gap:10px;margin:18px 0 0}.bul div{display:flex;gap:12px;align-items:flex-start;color:var(--sub)}.bul div::before{content:"✓";flex:none;width:24px;height:24px;border-radius:8px;display:grid;place-items:center;background:rgba(61,255,143,.16);color:var(--g);font-weight:800;font-size:13px}
.wkgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.wk{position:relative;border-radius:26px;overflow:hidden;border:1px solid var(--line);background:#0b1311;display:flex;flex-direction:column}
.wk .im{height:220px;background-size:cover;background-position:center;position:relative}
.wk .im::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#0b1311,transparent 60%)}
.wk .im b{position:absolute;left:16px;top:16px;z-index:2;font:800 12px var(--num);padding:5px 10px;border-radius:9px;background:rgba(0,0,0,.6);color:var(--g)}
.wk .ct{padding:4px 20px 22px}.wk h3{margin:0 0 12px;font:700 21px var(--disp)}
.wk .its{display:grid;gap:8px}.wk .it{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:var(--glass);border:1px solid var(--line);text-decoration:none;transition:background .2s,transform .2s}
.wk .it:hover{background:rgba(61,255,143,.12);transform:translateX(4px)}.wk .it .ic{font-size:22px}.wk .it b{display:block;font-size:14.5px}.wk .it small{color:var(--dim);font-size:12px}.wk .it .ar{margin-left:auto;color:var(--g)}
.ftr{position:relative;overflow:hidden}.ftr .fbg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.14}.ftr .wrap{position:relative}
.lhero .ph{animation:kb 30s ease-in-out infinite alternate}
/* intro v2 */
.intro{background:#000}.intro video{opacity:1}
.intro::after{background:radial-gradient(80% 80% at 50% 50%,transparent 55%,rgba(0,0,0,.65))}
.intro .ct{position:absolute;left:0;right:0;bottom:40px}
.intro .pr{margin-top:0}.intro .ild{font:600 13px var(--body);color:var(--dim);margin-top:10px;letter-spacing:.2em}.intro .iplay{position:absolute;z-index:4;left:50%;top:50%;transform:translate(-50%,-50%)}.intro .snd{position:absolute;bottom:28px;left:28px;z-index:3}
.mag{transition:transform .25s cubic-bezier(.2,.7,.2,1)}
@media (max-width:980px){.hero2 .wrap{grid-template-columns:1fr}.hcard{transform:none}.feature{grid-template-columns:1fr}.wkgrid{grid-template-columns:1fr}.wgrp{grid-template-columns:1fr}.wgrp .ph{min-height:120px}}
@media (max-width:640px){.works-btn .t{display:none}.works-btn{padding:8px 11px}.logo .wd small{display:none}}
@media (prefers-reduced-motion:reduce){.intro.bye{transition:none}.hero2 .bgi,.orb,.marq .tr,.lhero .ph,.works-btn::after{animation:none}.w{animation:none;opacity:1;transform:none;filter:none}}
'''


def hr_pair(L, compact=False):
    mat = L['mat']; n = L['n']
    a = f'materials/{mat}/HR_Das{n}_prezentacia.pptx'; b = f'materials/{mat}/HR_Das{n}_konspekt.pdf'
    return f"""<div class="hrpair{' cmp' if compact else ''}"><a class="hrc" href="{a}" download><span class="ty pptx">PPTX</span><span><b>✨ H/R ներկայացում</b><small>Դասախոսի սլայդները նոր ձևավորմամբ + բանաձևեր և բառարան · {gen.fsize(os.path.join(SITE,a))}</small></span><i>⬇</i></a>
<a class="hrc" href="{b}" target="_blank" rel="noopener"><span class="ty pdf">PDF</span><span><b>✨ H/R կոնսպեկտ</b><small>Ամբողջ դասը մեկ գեղեցիկ PDF-ում · {gen.fsize(os.path.join(SITE,b))}</small></span><i>👁</i></a></div>"""

def file_card2(mat, f, title, kind, lesson_label=''):
    c = gen.file_card_orig(mat, f, title, kind, lesson_label)
    L = next((x for x in LESSONS if x['mat'] == mat), None)
    if L and kind in ('slides', 'lecture'):
        hr = f'materials/{mat}/HR_Das{L["n"]}_' + ('prezentacia.pptx' if kind == 'slides' else 'konspekt.pdf')
        c = c.replace('<div class="ac">', f'<div class="ac"><a class="ib hrb" href="{hr}" {"download" if hr.endswith(".pptx") else "target=_blank"} title="H/R տարբերակ (գեղեցիկ)">✨</a>', 1)
        c = c.replace('title="Ներբեռնել">', 'title="Ներբեռնել բնօրինակը">', 1)
    return c

def library_tabs():
    tabs = ''; panes = ''
    groups = [(L['mat'], f'Դաս {L["n"]}', L) for L in LESSONS] + [('mid', 'Միջանկյալ', None)]
    for i, (m, lab, L) in enumerate(groups):
        on = ' on' if i == len(LESSONS) - 1 else ''
        tabs += f'<button class="ltab{on}" data-p="{m}">{lab}{f"<small>{E(L["short"])}</small>" if L else "<small>1-ին ստուգում</small>"}</button>'
        head = (f'<div class="lphead"><div><div class="kick">Դաս {L["n"]} · {E(L["date"])}</div><h3>{E(L["t"])}</h3></div><a class="btn gh" href="{L["slug"]}.html">Դասի էջը →</a></div>' + hr_pair(L)) if L else '<div class="lphead"><div><div class="kick">Քննություն</div><h3>1-ին միջանկյալ ստուգում</h3></div></div>'
        files = ''.join(file_card2(m, f, t, k) for f, t, k in FILES[m])
        panes += f'<div class="lpane{on}" data-p="{m}">{head}<div class="kick" style="margin:18px 0 10px">Դասախոսի բնօրինակ ֆայլերը</div><div class="files">{files}</div></div>'
    return f'<div class="ltabs">{tabs}</div><div class="lpanes">{panes}</div>'

LIBJS = r"""<script>(function(){const t=document.querySelectorAll('.ltab'),p=document.querySelectorAll('.lpane');t.forEach(b=>b.onclick=()=>{t.forEach(x=>x.classList.toggle('on',x===b));p.forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.p));});
const s=document.getElementById('srch2');s&&s.addEventListener('input',()=>{const q=s.value.trim().toLowerCase();document.querySelector('.lpanes').classList.toggle('q',!!q);document.querySelectorAll('.lpane .fc').forEach(c=>c.style.display=(!q||c.textContent.toLowerCase().includes(q))?'':'none');});})();</script>"""

def wpanel():
    g = ''.join(f'''<div class="wgrp"><div class="ph" style="background-image:url('assets/gen/{w["img"]}_s.jpg')"><b>{w["l"]}</b></div><div><h4>{E(w["t"])}</h4>{"".join(f'<a class="witem" href="{u}"{" download" if u.endswith(".xlsx") else ""}><span class="ic">{ic}</span><span><b>{E(n)}</b><small>{E(s)}</small></span></a>' for ic,n,u,s in w["items"])}</div></div>''' for w in WORKS)
    return f'''<div class="wpanel" id="wpanel" role="dialog" aria-label="Իմ աշխատանքները"><h3>Իմ աշխատանքները</h3><p class="sd2">Բոլոր ներկայացումները, դաշբորդները և Excel լուծումները՝ Հրաչյա Ասլանյան · H/R Studios</p>{g}
<div class="wfoot"><span class="tag">Շուտով՝ դասեր 1–6-ի լուծումները</span><a class="btn gh" href="works.html">Բոլորը մեկ էջում →</a></div></div>'''

def header(active, root=''):
    items = [('index.html#top', 'Գլխավոր', 'home'), ('index.html#lessons', 'Դասեր', 'lessons'), ('index.html#library', 'Նյութեր', 'library'), ('index.html#how', 'Ինչպես օգտվել', 'how'), ('index.html#about', 'Մեր մասին', 'about')]
    nav = ''.join(f'<a href="{root}{h}" class="{"on" if k==active else ""}">{t}</a>' for h, t, k in items)
    return f'''<div class="prog" id="prog"></div><div class="cglow" id="cglow"></div><header class="hdr"><div class="wrap in"><a class="logo" href="{root}index.html"><img class="lim" src="assets/logo_sm.png" alt="H/R Studios"><span class="wd">H/R Studios<small>ՈՒՍՈՒՄՆԱԿԱՆ ՀԱՐԹԱԿ</small></span></a>
<button class="works-btn" id="wbtn" aria-expanded="false"><span class="dot"></span><span class="t">Իմ աշխատանքները</span><span>▾</span></button>
<nav class="nav" id="nav">{nav}</nav><button class="burger" aria-label="Մենյու" onclick="document.getElementById('nav').classList.toggle('open')">☰</button></div></header>{wpanel()}'''

def footer():
    f = gen.footer_orig()
    f = f.replace('<footer class="ftr" id="about"><div class="wrap">', '<footer class="ftr" id="about"><div class="fbg" style="background-image:url(\'assets/gen/studio.jpg\')"></div><div class="wrap">')
    f = f.replace('<span class="mk"><b>H/R</b></span>', '<img class="lim" src="assets/logo_sm.png" alt="H/R Studios" style="height:44px">')
    return f

JS2 = r'''<script>
(function(){
  const red = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // works panel
  const wb = document.getElementById('wbtn'), wp = document.getElementById('wpanel');
  if (wb && wp){ wb.onclick = e => { e.stopPropagation(); const on = !wp.classList.contains('on'); wp.classList.toggle('on', on); wb.setAttribute('aria-expanded', on); };
    document.addEventListener('click', e => { if (!wp.contains(e.target) && e.target !== wb) wp.classList.remove('on'); });
    addEventListener('keydown', e => { if (e.key === 'Escape') wp.classList.remove('on'); }); }
  // scroll progress + cursor glow (rAF throttled)
  const pr = document.getElementById('prog'), cg = document.getElementById('cglow'); let tk = 0, mx = -999, my = -999;
  const frame = () => { tk = 0; const h = document.documentElement.scrollHeight - innerHeight; pr && (pr.style.transform = `scaleX(${h>0? scrollY/h : 0})`); cg && (cg.style.transform = `translate3d(${mx}px,${my}px,0)`); };
  addEventListener('scroll', () => { if (!tk) tk = requestAnimationFrame(frame); }, {passive:true});
  if (!red) addEventListener('pointermove', e => { if (e.pointerType !== 'mouse') return; mx = e.clientX; my = e.clientY; if (!tk) tk = requestAnimationFrame(frame); }, {passive:true});
  // tilt + shine on lesson cards
  if (!red && matchMedia('(hover:hover)').matches) document.querySelectorAll('.lc,.wk').forEach(c => {
    c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(), x = (e.clientX-r.left)/r.width, y = (e.clientY-r.top)/r.height;
      c.style.transform = `perspective(900px) rotateY(${(x-.5)*8}deg) rotateX(${(.5-y)*8}deg) translateY(-6px)`; c.style.setProperty('--mx', x*100+'%'); c.style.setProperty('--my', y*100+'%'); });
    c.addEventListener('pointerleave', () => c.style.transform = ''); });
  // counters
  const cnt = el => { const t = +el.dataset.n, t0 = performance.now(); const st = n => { const p = Math.min(1,(n-t0)/1400), e = 1-Math.pow(1-p,3); el.textContent = Math.round(t*e); if (p<1) requestAnimationFrame(st); }; requestAnimationFrame(st); };
  if ('IntersectionObserver' in window){ const o = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting){ red ? (e.target.textContent = e.target.dataset.n) : cnt(e.target); o.unobserve(e.target); } })); document.querySelectorAll('[data-n]').forEach(x => o.observe(x)); }
  // magnetic buttons
  if (!red && matchMedia('(hover:hover)').matches) document.querySelectorAll('.btn').forEach(b => { b.classList.add('mag'); b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX-r.left-r.width/2)*.15}px,${(e.clientY-r.top-r.height/2)*.25}px)`; }); b.addEventListener('pointerleave', () => b.style.transform = ''); });
})();
</script>'''

INTRO2 = '''<div class="intro" id="intro"><video id="ivid" muted playsinline preload="auto" poster="assets/intro_end.jpg"><source src="assets/intro.mp4" type="video/mp4"></video>
<div class="ct"><div class="pr"><i id="ipr"></i></div><div class="ild" id="ild">Բեռնվում է…</div></div><button class="btn iplay" id="iplay" hidden>▶ Դիտել ինտրոն</button>
<button class="btn gh snd" id="isnd" aria-label="Ձայն">🔇 Ձայն</button><button class="btn gh sk" id="iskip">Բաց թողնել →</button></div>
<script>(function(){const I=document.getElementById('intro'),V=document.getElementById('ivid'),bar=document.getElementById('ipr'),L=document.getElementById('ild'),P=document.getElementById('iplay');
let seen=false;try{seen=sessionStorage.getItem('hr-intro3')==='1'}catch(e){}if(/[?&]intro=1/.test(location.search))seen=false;if(seen){I.remove();return}
document.documentElement.style.overflow='hidden';let done=false,started=false;
const fin=()=>{if(done)return;done=true;try{sessionStorage.setItem('hr-intro3','1')}catch(e){}I.classList.add('bye');document.documentElement.style.overflow='';setTimeout(()=>{try{V.pause()}catch(e){}I.remove()},950)};
V.addEventListener('progress',()=>{try{if(!started&&V.buffered.length&&V.duration)bar.style.width=Math.min(100,V.buffered.end(V.buffered.length-1)/V.duration*100)+'%'}catch(e){}});
V.addEventListener('timeupdate',()=>{if(V.duration){started=true;L.textContent='';bar.style.width=(V.currentTime/V.duration*100)+'%'}});
V.addEventListener('ended',()=>setTimeout(fin,400));V.addEventListener('error',()=>setTimeout(fin,1500));
const go=()=>{const p=V.play();if(p&&p.catch)p.catch(()=>{P.hidden=false;L.textContent=''})};
if(V.readyState>=3)go();else V.addEventListener('canplay',go,{once:true});V.load();
P.onclick=()=>{P.hidden=true;V.play().catch(fin)};setTimeout(()=>{if(!started)fin()},15000);setTimeout(fin,25000);
document.getElementById('iskip').onclick=fin;const S=document.getElementById('isnd');S.onclick=()=>{V.muted=!V.muted;S.textContent=V.muted?'🔇 Ձայն':'🔊 Ձայն';if(!started)go()};})();</script>'''

def words(t, cls='', k0=0):
    return ' '.join(f'<span class="w {cls}" style="--k:{i+k0}">{E(x)}</span>' for i, x in enumerate(t.split()))

def build_index():
    nfiles = sum(len(v) for v in FILES.values()); nsl = sum(len(slides_of(k)) for k in FILES)
    cards = ''
    for L in LESSONS:
        st = '<span class="st ok">✔ Լուծված</span>' if L['hw'] else '<span class="st wip">⏳ Շուտով</span>'
        tags = f'<span class="tag">{len(FILES[L["mat"]])} ֆայլ</span>' + (f'<span class="tag">{len(slides_of(L["mat"]))} սլայդ</span>' if slides_of(L['mat']) else '') + ('<span class="tag">🎬 Ներկայացում</span>' if L['hw'] else '')
        cards += f'''<a class="lc rv" href="{L["slug"]}.html" style="--a:{L["acc"]}"><div class="im" style="background-image:url('assets/gen/{L["img"]}_s.jpg')"></div><span class="n">ԴԱՍ {L["n"]:02d}</span>{st}
<div class="ct"><h3>{E(L["t"])}</h3><p>{E(L["idea"][:110])}…</p><div class="ft">{tags}</div></div><span class="shine"></span></a>'''
    lib_chips = '<button class="chip on" data-fl="all">Բոլորը</button>' + ''.join(f'<button class="chip" data-fl="{L["mat"]}">Դաս {L["n"]}</button>' for L in LESSONS) + '<button class="chip" data-fl="mid">Միջանկյալ</button>'
    kind_chips = '<button class="chip on" data-fk="all">Բոլոր տեսակները</button>' + ''.join(f'<button class="chip" data-fk="{k}">{v}</button>' for k, v in KIND.items())
    lab = {L['mat']: f'Դաս {L["n"]}' for L in LESSONS}; lab['mid'] = '1-ին միջանկյալ'
    lib = ''.join(file_card(m, f, t, k, lab[m]) for m, lst in FILES.items() for f, t, k in lst)
    mid = ''.join(file_card2('mid', f, t, k) for f, t, k in FILES['mid'])
    marq = ''.join(f'<span>{E(L["short"])}</span>' for L in LESSONS) * 2
    wk = works_cards()
    body = f'''{header('home')}
<section class="hero2" id="top"><div class="bgi" style="background-image:url('assets/gen/waves.jpg')"></div><i class="orb a"></i><i class="orb b"></i><i class="orb c"></i>
<div class="wrap"><div><div class="kick rv">H/R Studios · ԻՏ-447 · 2026–2027</div>
<h1>{words("Տնտեսական գործունեության վերլուծություն")}<br>{words("բոլոր դասերը մեկ տեղում", "gr", 3)}</h1>
<p class="lead rv">Դասախոսի սլայդները և ֆայլերը՝ պարզ ու գեղեցիկ տեսքով, յուրաքանչյուր թեմայի բացատրությունը պարզ լեզվով, լուծված տնայինները, Excel ֆայլերը և անիմացիոն ներկայացումները։</p>
<div class="ctas rv"><a class="btn" href="#lessons">{ICON["play"]}Դիտել դասերը</a><a class="btn gh" href="#works">🎬 Իմ աշխատանքները</a><a class="btn gh" href="#library">{ICON["grid"]}Գրադարան</a></div>
<div class="author rv"><span class="av">ՀԱ</span><div><b>Հրաչյա Ասլանյան</b><small>Հեղինակ · ՀԱՊՀ, ԻՏ-447 · Դասախոս՝ {E(TEACHER)}</small></div></div></div>
<a class="hcard rv" href="t8/index.html"><img src="assets/gen/desk.jpg" alt=""><div class="cap"><div><b>Նոր՝ Դաս 8 ներկայացում</b><small>Դեբիտորական և կրեդիտորական պարտքեր</small></div><span class="btn" style="padding:9px 14px">{ICON["play"]}</span></div></a></div></section>
<div class="marq"><div class="tr">{marq}</div></div>
<div class="wrap"><div class="stats" style="margin-top:30px"><div class="stat rv"><b data-n="{len(LESSONS)}">0</b><span>դաս</span></div><div class="stat rv"><b data-n="{nfiles}">0</b><span>դասախոսի ֆայլ</span></div><div class="stat rv"><b data-n="{nsl}">0</b><span>սլայդ դիտելու համար</span></div><div class="stat rv"><b data-n="{sum(1 for L in LESSONS if L["hw"])}">0</b><span>լուծված տնային + ներկայացում</span></div></div></div>
<section class="sec sbg" id="lessons"><div class="bimg" style="background-image:url('assets/gen/lecture.jpg')"></div><div class="wrap"><div class="kick rv">Դասընթաց</div><h2 class="rv">Դասեր</h2><p class="sd rv">Ընտրեք դասը․ ներսում կգտնեք պարզ բացատրություն, բանաձևերի քարտեր, դասախոսի սլայդները, ֆայլերը և տնային աշխատանքի լուծումը։</p>
<div class="lgrid">{cards}</div></div></section>
<section class="sec" id="works"><div class="wrap"><div class="feature"><div><div class="kick rv">H/R Studios</div><h2 class="rv">Իմ աշխատանքները</h2><p class="sd rv">Յուրաքանչյուր տնային աշխատանք՝ երեք ձևաչափով․ անիմացիոն ներկայացում, ինտերակտիվ «Տվյալների սրահ» և Excel ֆայլ՝ բանաձևերով և գծապատկերներով։</p>
<div class="bul rv"><div>Սեղմեք ցանկացած թվի վրա՝ կտեսնեք Excel-ի բանաձևը</div><div>Աշխատում է համակարգչում և հեռախոսում</div><div>Excel-ը կարելի է ներբեռնել հենց ներկայացման միջից</div></div></div>
<div class="pic rv"><img src="assets/gen/works.jpg" alt=""></div></div><div class="wkgrid" style="margin-top:30px">{wk}</div></div></section>
<section class="sec sbg" id="how"><div class="bimg" style="background-image:url('assets/gen/students.jpg')"></div><div class="wrap"><div class="kick rv">Ինչպես օգտվել</div><h2 class="rv">Երեք քայլ</h2>
<div class="grid g3 how"><div class="card rv"><div class="ic">📖</div><h3>1 · Կարդացեք պարզ տարբերակը</h3><p>Յուրաքանչյուր դասում կա «Դասը պարզ լեզվով» բաժինը՝ օրինակով, բանաձևերի բացատրությամբ և բառարանով։</p></div>
<div class="card rv"><div class="ic">📊</div><h3>2 · Նայեք լուծված օրինակը</h3><p>Բացեք ներկայացումը և «Տվյալների սրահը»․ սեղմեք ցանկացած թվի վրա և կտեսնեք՝ ինչ բանաձևով է հաշվված։</p></div>
<div class="card rv"><div class="ic">✍️</div><h3>3 · Կատարեք ինքնուրույն</h3><p>Ներբեռնեք դասախոսի Excel ձևանմուշը և հետևեք «Ինչպես կատարել» քայլերին։ Ամեն ինչ կարող եք ստուգել լուծված ֆայլով։</p></div></div></div></section>
<section class="sec" id="library"><div class="wrap"><div class="feature" style="margin-bottom:30px"><div class="pic rv"><img src="assets/gen/papers.jpg" alt=""></div><div><div class="kick rv">Գրադարան</div><h2 class="rv">Դասախոսի բոլոր նյութերը</h2><p class="sd rv">Ընտրեք դասը․ յուրաքանչյուր դասի համար կա դասախոսի բնօրինակը և մեր «✨ H/R տարբերակը»՝ գեղեցիկ ներկայացում և կոնսպեկտ։</p></div></div>
<input class="srch" id="srch2" placeholder="Որոնում բոլոր դասերում՝ օրինակ «իրացվելիություն»" style="width:100%;margin-bottom:14px">{library_tabs()}</div></section>
<section class="sec" id="midterm"><div class="wrap"><div class="feature"><div><div class="kick rv">Քննություն</div><h2 class="rv">1-ին միջանկյալ ստուգում</h2><p class="sd rv">Տնային առաջադրանքը (5 խնդիր) և տեսական հարցաշարը։</p><div class="files">{mid}</div></div><div class="pic rv"><img src="assets/gen/midterm.jpg" alt=""></div></div></div></section>
{footer()}{gen.JS}{LIBJS}</body></html>'''
    open(os.path.join(SITE, 'index.html'), 'w').write(gen.head(f'{COURSE} · H/R Studios', 'Ուսումնական հարթակ ԻՏ-447 խմբի համար', INTRO2) + body)

def works_cards():
    return ''.join(f'''<div class="wk rv"><div class="im" style="background-image:url('assets/gen/{w["img"]}.jpg')"><b>{w["l"]}</b></div><div class="ct"><h3>{E(w["t"])}</h3><div class="its">{"".join(f'<a class="it" href="{u}"{" download" if u.endswith(".xlsx") else ""}><span class="ic">{ic}</span><span><b>{E(n)}</b><small>{E(s)}</small></span><span class="ar">→</span></a>' for ic,n,u,s in w["items"])}<a class="it" href="{w["page"]}"><span class="ic">📘</span><span><b>{"Դասի էջը" if w["page"].startswith("lesson") else "Առաջադրանքը գրադարանում"}</b><small>{"բացատրություն, բանաձևեր, սլայդներ" if w["page"].startswith("lesson") else "դասախոսի ֆայլերը"}</small></span><span class="ar">→</span></a></div></div></div>''' for w in WORKS)

def build_works():
    body = f'''{header('')}
<section class="hero2" style="min-height:min(560px,80vh)"><div class="bgi" style="background-image:url('assets/gen/works.jpg')"></div><i class="orb a"></i><i class="orb b"></i>
<div class="wrap" style="grid-template-columns:1fr"><div><div class="kick">H/R Studios · Հրաչյա Ասլանյան</div><h1>{words("Իմ աշխատանքները")}</h1><p class="lead">Ներկայացումներ, դաշբորդներ և Excel լուծումներ՝ «{E(COURSE)}» առարկայից։</p></div></div></section>
<section class="sec"><div class="wrap"><div class="wkgrid">{works_cards()}</div></div></section>
{footer()}{gen.JS}</body></html>'''
    open(os.path.join(SITE, 'works.html'), 'w').write(gen.head('Իմ աշխատանքները · H/R Studios', 'Հրաչյա Ասլանյանի աշխատանքները') + body)

if __name__ == '__main__':
    gen.CSS += CSS2
    gen.file_card_orig = gen.file_card; gen.file_card = file_card2
    gen.footer_orig = gen.footer
    gen.header = header; gen.footer = footer
    gen.JS = gen.JS + JS2 if JS2 not in gen.JS else gen.JS
    JSALL = gen.JS
    gen.JS = JSALL
    build_index(); build_works()
    for i, L in enumerate(LESSONS):
        gen.build_lesson(i, L)
        p = os.path.join(SITE, L['slug'] + '.html'); s = open(p).read()
        s = s.replace(f"assets/img/{L['img']}.jpg", f"assets/gen/{L['img']}.jpg")
        s = s.replace('<h2 class="rv">Դասախոսի նյութերը</h2><div class="files">', '<h2 class="rv">Դասախոսի նյութերը</h2><div class="kick" style="margin-bottom:10px">✨ Մեր գեղեցիկ տարբերակը</div>' + hr_pair(L) + '<div class="kick" style="margin:22px 0 10px">Դասախոսի բնօրինակները</div><div class="files">', 1)
        open(p, 'w').write(s)
    print('v2 ok')
