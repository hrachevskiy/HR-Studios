# -*- coding: utf-8 -*-
import os, html, json, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import LESSONS, FILES, COURSE, TEACHER
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, 'site')
E = html.escape
CSS = open(os.path.join(BASE, 'gen', 'site.css')).read()

ICON = {
 'dl': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3v12M7 10l5 5 5-5M4 20h16"/></svg>',
 'eye': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
 'play': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
 'grid': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}
KIND = {'slides': 'Սլայդներ', 'lecture': 'Դասախոսություն', 'task': 'Առաջադրանք', 'doc': 'Փաստաթուղթ', 'book': 'Ձեռնարկ', 'data': 'Տվյալներ'}

def fsize(p):
    s = os.path.getsize(p); return f'{s/1048576:.1f} ՄԲ' if s > 1048576 else f'{max(1, s//1024)} ԿԲ'

def head(title, desc, pre=''):
    return f'''<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#050908">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23050908'/%3E%3Ctext x='32' y='41' font-family='Arial' font-weight='800' font-size='22' fill='%23fff' text-anchor='middle'%3EH/R%3C/text%3E%3Cpath d='M40 10 24 54' stroke='%233dff8f' stroke-width='3'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=Noto+Serif+Armenian:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap">
<style>{CSS}</style></head><body>{pre}<div class="bgfx"></div>'''

def header(active, root=''):
    items = [('index.html#top', 'Գլխավոր', 'home'), ('index.html#lessons', 'Դասեր', 'lessons'), ('index.html#library', 'Նյութեր', 'library'), ('index.html#how', 'Ինչպես օգտվել', 'how'), ('index.html#about', 'Մեր մասին', 'about')]
    nav = ''.join(f'<a href="{root}{h}" class="{"on" if k==active else ""}">{t}</a>' for h, t, k in items)
    return f'''<header class="hdr"><div class="wrap in"><a class="logo" href="{root}index.html"><span class="mk"><b>H/R</b></span><span class="wd">H/R Studios<small>ՈՒՍՈՒՄՆԱԿԱՆ ՀԱՐԹԱԿ</small></span></a>
<nav class="nav" id="nav">{nav}</nav><button class="burger" aria-label="Մենյու" onclick="document.getElementById('nav').classList.toggle('open')">☰</button></div></header>'''

def footer():
    links = ''.join(f'<a href="{L["slug"]}.html">Դաս {L["n"]} · {E(L["short"])}</a>' for L in LESSONS)
    return f'''<footer class="ftr" id="about"><div class="wrap"><div class="in">
<div><a class="logo" href="index.html"><span class="mk"><b>H/R</b></span><span class="wd">H/R Studios<small>SLIDES THAT COME ALIVE</small></span></a>
<p>H/R Studios-ը ստեղծում է կենդանի ներկայացումներ, անիմացիոն սլայդներ և ինտերակտիվ դաշբորդներ։ Այս հարթակը ԻՏ-447 խմբի համար է՝ «{E(COURSE)}» առարկայի բոլոր նյութերը, տնայինները և լուծումները մեկ տեղում։</p>
<p>Հեղինակ՝ <b>Հրաչյա Ասլանյան</b> · ՀԱՊՀ, ԻՏ-447 · Դասախոս՝ {E(TEACHER)}</p></div>
<div><h4>Դասեր</h4>{links}</div>
<div><h4>Հարթակ</h4><a href="index.html#lessons">Բոլոր դասերը</a><a href="index.html#library">Նյութերի գրադարան</a><a href="index.html#midterm">1-ին միջանկյալ</a><a href="index.html#how">Ինչպես օգտվել</a></div>
</div><div class="copy">© 2026 H/R Studios · Դասախոսի նյութերը տեղադրված են ուսումնական նպատակով՝ խմբի ուսանողների համար։</div></div></footer>'''

JS = r'''<script>
(function(){
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin:'0px 0px -8% 0px'}) : null;
  document.querySelectorAll('.rv').forEach((el,i) => { el.style.transitionDelay = (Math.min(i%6,5)*60)+'ms'; io ? io.observe(el) : el.classList.add('in'); });
  // lightbox
  const lb = document.getElementById('lb'); if (lb){ const im = lb.querySelector('img'), lab = lb.querySelector('span'); const list = [...document.querySelectorAll('.slides button')]; let k = 0;
    const show = i => { k = (i + list.length) % list.length; im.src = list[k].dataset.src; lab.textContent = (k+1) + ' / ' + list.length; };
    list.forEach((b,i) => b.onclick = () => { show(i); lb.classList.add('on'); document.body.style.overflow='hidden'; });
    const close = () => { lb.classList.remove('on'); document.body.style.overflow=''; };
    lb.querySelector('.cl').onclick = close; lb.querySelector('.pv').onclick = () => show(k-1); lb.querySelector('.nx').onclick = () => show(k+1);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    addEventListener('keydown', e => { if (!lb.classList.contains('on')) return; if (e.key==='Escape') close(); if (e.key==='ArrowRight') show(k+1); if (e.key==='ArrowLeft') show(k-1); });
    let sx = null; lb.addEventListener('touchstart', e => sx = e.touches[0].clientX, {passive:true}); lb.addEventListener('touchend', e => { if (sx==null) return; const d = e.changedTouches[0].clientX - sx; if (Math.abs(d) > 50) show(k + (d<0?1:-1)); sx = null; }, {passive:true}); }
  // library filter
  const lib = document.getElementById('libf'); if (lib){ let fl = 'all', fk = 'all', q = '';
    const apply = () => document.querySelectorAll('#libf .fc').forEach(c => { const ok = (fl==='all'||c.dataset.l===fl) && (fk==='all'||c.dataset.k===fk) && (!q || c.textContent.toLowerCase().includes(q)); c.style.display = ok ? '' : 'none'; });
    document.querySelectorAll('[data-fl]').forEach(b => b.onclick = () => { fl = b.dataset.fl; document.querySelectorAll('[data-fl]').forEach(x => x.classList.toggle('on', x===b)); apply(); });
    document.querySelectorAll('[data-fk]').forEach(b => b.onclick = () => { fk = b.dataset.fk; document.querySelectorAll('[data-fk]').forEach(x => x.classList.toggle('on', x===b)); apply(); });
    const s = document.getElementById('srch'); s && s.addEventListener('input', () => { q = s.value.trim().toLowerCase(); apply(); }); }
  // lesson sub-nav highlight
  const ln = document.querySelectorAll('.lnav a'); if (ln.length && io){ const ob = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) ln.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#'+e.target.id)); }), {rootMargin:'-40% 0px -55% 0px'});
    ln.forEach(a => { const t = document.querySelector(a.getAttribute('href')); t && ob.observe(t); }); }
  // pause hero video when hidden / off-screen (weak laptops)
  document.querySelectorAll('video[data-auto]').forEach(v => { if (io){ new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? v.play().catch(()=>{}) : v.pause())).observe(v); } });
  document.addEventListener('visibilitychange', () => document.querySelectorAll('video[data-auto]').forEach(v => document.hidden ? v.pause() : v.play().catch(()=>{})));
})();
</script>'''

INTRO = '''<div class="intro" id="intro"><video src="assets/intro.mp4" muted autoplay playsinline loop poster="assets/bg-flow.jpg"></video>
<div class="ct"><div class="bigmk">H<i>/</i>R</div><div class="st2">STUDIOS</div><div class="pr"><i id="ipr"></i></div></div>
<button class="btn gh sk" id="iskip">Բաց թողնել →</button></div>
<script>(function(){const I=document.getElementById('intro');let seen=false;try{seen=sessionStorage.getItem('hr-intro')==='1'}catch(e){}
if(seen||matchMedia('(prefers-reduced-motion: reduce)').matches){I.remove();return}
const bar=document.getElementById('ipr');let p=0,done=false;const fin=()=>{if(done)return;done=true;bar.style.width='100%';try{sessionStorage.setItem('hr-intro','1')}catch(e){}setTimeout(()=>{I.classList.add('bye');setTimeout(()=>{I.querySelector('video').pause();I.remove()},950)},300)};
const t=setInterval(()=>{p=Math.min(92,p+7+Math.random()*9);bar.style.width=p+'%'},180);
const ready=()=>{clearInterval(t);setTimeout(fin,500)};if(document.readyState==='complete')setTimeout(ready,1600);else addEventListener('load',()=>setTimeout(ready,1200));
setTimeout(()=>{clearInterval(t);fin()},5200);document.getElementById('iskip').onclick=()=>{clearInterval(t);fin()};})();</script>'''

def file_card(mat, f, title, kind, lesson_label=''):
    p = os.path.join(SITE, 'materials', mat, f); ext = f.rsplit('.', 1)[1].lower(); url = f'materials/{mat}/{f}'
    view = f'<a class="ib" href="{url}" target="_blank" rel="noopener" title="Բացել">{ICON["eye"]}</a>' if ext == 'pdf' else ''
    return f'''<div class="fc rv" data-l="{mat}" data-k="{kind}"><span class="ty {ext}">{ext.upper()}</span><div class="mt">{f'<span class="ltag">{E(lesson_label)}</span>' if lesson_label else ''}<b>{E(title)}</b><small>{KIND.get(kind,"")} · {fsize(p)}</small></div>
<div class="ac">{view}<a class="ib" href="{url}" download title="Ներբեռնել">{ICON["dl"]}</a></div></div>'''

def slides_of(mat):
    d = os.path.join(SITE, 'materials', mat, 'slides')
    return sorted(os.listdir(d)) if os.path.isdir(d) else []

def lesson_img(L):
    s = slides_of(L['mat'])
    return f'materials/{L["mat"]}/slides/{s[0]}' if s else f'assets/img/{L["img"]}.jpg'

# ---------------- index ----------------
def build_index():
    nfiles = sum(len(v) for v in FILES.values()); nsl = sum(len(slides_of(k)) for k in FILES)
    cards = ''
    for L in LESSONS:
        st = '<span class="st ok">✔ Լուծված</span>' if L['hw'] else '<span class="st wip">⏳ Լուծումը՝ շուտով</span>'
        tags = f'<span class="tag">{len(FILES[L["mat"]])} ֆայլ</span>' + (f'<span class="tag">{len(slides_of(L["mat"]))} սլայդ</span>' if slides_of(L['mat']) else '') + ('<span class="tag">🎬 Ներկայացում</span>' if L['hw'] else '')
        cards += f'''<a class="lc rv" href="{L["slug"]}.html" style="--a:{L["acc"]}"><div class="im" style="background-image:url('{lesson_img(L)}')"></div><span class="n">ԴԱՍ {L["n"]:02d}</span>{st}
<div class="ct"><h3>{E(L["t"])}</h3><p>{E(L["idea"][:118])}…</p><div class="ft">{tags}</div></div></a>'''
    lib_chips = '<button class="chip on" data-fl="all">Բոլորը</button>' + ''.join(f'<button class="chip" data-fl="{L["mat"]}">Դաս {L["n"]}</button>' for L in LESSONS) + '<button class="chip" data-fl="mid">Միջանկյալ</button>'
    kind_chips = '<button class="chip on" data-fk="all">Բոլոր տեսակները</button>' + ''.join(f'<button class="chip" data-fk="{k}">{v}</button>' for k, v in KIND.items())
    lab = {L['mat']: f'Դաս {L["n"]}' for L in LESSONS}; lab['mid'] = '1-ին միջանկյալ'
    lib = ''.join(file_card(m, f, t, k, lab[m]) for m, lst in FILES.items() for f, t, k in lst)
    mid = ''.join(file_card('mid', f, t, k) for f, t, k in FILES['mid'])
    body = f'''{header('home')}
<section class="hero" id="top"><video data-auto src="assets/bg-city.mp4" poster="assets/bg-city.jpg" muted loop playsinline autoplay></video>
<div class="wrap"><div class="kick">H/R Studios · ԻՏ-447 · 2026–2027</div>
<h1>{E(COURSE)}<br><span class="gr">բոլոր դասերը մեկ տեղում</span></h1>
<p class="lead">Դասախոսի սլայդները և ֆայլերը՝ պարզ ու գեղեցիկ տեսքով, յուրաքանչյուր թեմայի բացատրությունը պարզ լեզվով, լուծված տնայինները, Excel ֆայլերը և անիմացիոն ներկայացումները։</p>
<div class="ctas"><a class="btn" href="#lessons">{ICON["play"]}Դիտել դասերը</a><a class="btn gh" href="#library">{ICON["grid"]}Նյութերի գրադարան</a></div>
<div class="author"><span class="av">ՀԱ</span><div><b>Հրաչյա Ասլանյան</b><small>Հեղինակ · ՀԱՊՀ, ԻՏ-447 · Դասախոս՝ {E(TEACHER)}</small></div></div></div></section>
<div class="wrap"><div class="stats"><div class="stat rv"><b>{len(LESSONS)}</b><span>դաս</span></div><div class="stat rv"><b>{nfiles}</b><span>դասախոսի ֆայլ</span></div><div class="stat rv"><b>{nsl}</b><span>սլայդ դիտելու համար</span></div><div class="stat rv"><b>{sum(1 for L in LESSONS if L["hw"])}</b><span>լուծված տնային + ներկայացում</span></div></div></div>
<section class="sec" id="lessons"><div class="wrap"><div class="kick rv">Դասընթաց</div><h2 class="rv">Դասեր</h2><p class="sd rv">Ընտրեք դասը․ ներսում կգտնեք պարզ բացատրություն, բանաձևերի քարտեր, դասախոսի սլայդները, ֆայլերը և տնային աշխատանքի լուծումը։</p>
<div class="lgrid">{cards}</div></div></section>
<section class="sec" id="how"><div class="wrap"><div class="kick rv">Ինչպես օգտվել</div><h2 class="rv">Երեք քայլ</h2>
<div class="grid g3 how"><div class="card rv"><div class="ic">📖</div><h3>1 · Կարդացեք պարզ տարբերակը</h3><p>Յուրաքանչյուր դասում կա «Դասը պարզ լեզվով» բաժինը՝ օրինակով, բանաձևերի բացատրությամբ և բառարանով։</p></div>
<div class="card rv"><div class="ic">📊</div><h3>2 · Նայեք լուծված օրինակը</h3><p>Բացեք ներկայացումը և «Տվյալների սրահը»․ սեղմեք ցանկացած թվի վրա և կտեսնեք՝ ինչ բանաձևով է հաշվված։</p></div>
<div class="card rv"><div class="ic">✍️</div><h3>3 · Կատարեք ինքնուրույն</h3><p>Ներբեռնեք դասախոսի Excel ձևանմուշը և հետևեք «Ինչպես կատարել» քայլերին։ Ամեն ինչ կարող եք ստուգել լուծված ֆայլով։</p></div></div></div></section>
<section class="sec" id="library"><div class="wrap"><div class="kick rv">Գրադարան</div><h2 class="rv">Դասախոսի բոլոր նյութերը</h2><p class="sd rv">PDF ֆայլերը բացվում են հենց բրաուզերում, մնացածը՝ կարող եք ներբեռնել։ Ֆիլտրեք ըստ դասի կամ տեսակի։</p>
<div class="lib-ctl rv">{lib_chips}</div><div class="lib-ctl rv">{kind_chips}<input class="srch" id="srch" placeholder="Որոնում՝ օրինակ «իրացվելիություն»"></div>
<div class="files" id="libf">{lib}</div></div></section>
<section class="sec" id="midterm"><div class="wrap"><div class="kick rv">Քննություն</div><h2 class="rv">1-ին միջանկյալ ստուգում</h2><p class="sd rv">Տնային առաջադրանքը (5 խնդիր՝ իրացվելիություն, կայունություն, հիմնական միջոցներ և այլն) և տեսական հարցաշարը։</p>
<div class="files">{mid}</div></div></section>
{footer()}{JS}</body></html>'''
    open(os.path.join(SITE, 'index.html'), 'w').write(head(f'{COURSE} · H/R Studios', 'Ուսումնական հարթակ ԻՏ-447 խմբի համար', INTRO) + body)

# ---------------- lesson pages ----------------
DIRT = {'up': '▲ Որքան բարձր, այնքան լավ', 'down': '▼ Որքան ցածր, այնքան լավ', 'norm': '◎ Պետք է լինի նորմայի սահմաններում'}
def build_lesson(i, L):
    acc = L['acc']; mat = L['mat']; sl = slides_of(mat)
    pts = ''.join(f'<div class="pt rv"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in L['points'])
    fx = ''.join(f'''<div class="card fcard rv"><div class="cd">{c}</div><div class="nm">{E(n)}</div><div class="eq">{c} = {f}</div><div class="mn">{E(m)}</div>{f'<span class="dir {d}">{DIRT[d]}</span>' if d else ''}</div>''' for c, n, f, m, d in L['formulas'])
    gl = ''.join(f'<div class="rv"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in L['glossary'])
    slides = ''.join(f'<button data-src="materials/{mat}/slides/{s}" aria-label="Սլայդ {k+1}"><img loading="lazy" src="materials/{mat}/slides/{s}" alt="Սլայդ {k+1}"><i>{k+1:02d}</i></button>' for k, s in enumerate(sl))
    files = ''.join(file_card(mat, f, t, k) for f, t, k in FILES[mat])
    hw = L['hw']
    if hw:
        st = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in hw['stats'])
        rs = ''.join(f'<div><span>{E(a)}</span><b>{E(b)}</b></div>' for a, b in hw['result'])
        hwhtml = f'''<div class="hwbox"><div class="card rv"><div class="kick">Առաջադրանք</div><p style="font-size:17px">{E(hw["task"])}</p><div class="hstats">{st}</div>
<div class="ctas" style="margin-top:8px"><a class="btn" href="{hw["deck"]}">{ICON["play"]}Բացել ներկայացումը</a><a class="btn gh" href="{hw["deck"]}#excel">{ICON["grid"]}Տվյալների սրահ</a><a class="btn gh" href="{hw["file"]}" download>{ICON["dl"]}Excel լուծումը</a></div></div>
<div class="card rv res"><div class="kick">Գլխավոր արդյունքներ</div>{rs}</div></div>'''
        tpl = hw['tpl']
    else:
        hwhtml = '''<div class="card rv wip"><span class="ic">⏳</span><div><b>Լուծումը պատրաստվում է</b><p style="margin:4px 0 0;color:var(--sub)">Այս դասի տնային աշխատանքի ամբողջական լուծումը (Excel + ներկայացում + բացատրություն) շուտով կհայտնվի այստեղ։ Առայժմ առաջադրանքը կարող եք գտնել «Ֆայլեր» բաժնում։</p></div></div>'''
        tpl = None
    steps = ['Կարդացեք «Դասը պարզ լեզվով» բաժինը և բանաձևերի քարտերը։', 'Բացեք դասախոսի սլայդները և գտեք լուծված օրինակը։',
             'Ներբեռնեք առաջադրանքը կամ Excel ձևանմուշը «Ֆայլեր» բաժնից։', 'Յուրաքանչյուր գործակից հաշվեք բանաձևով (Excel-ում՝ = նշանով), ոչ թե ձեռքով։',
             'Համեմատեք 2024 և 2025 տարիները, գրեք՝ լավացե՞լ է, թե՞ վատացել։', 'Ստուգեք ձեր արդյունքը լուծված ֆայլով, եթե այն արդեն կա։']
    stp = ''.join(f'<div class="rv">{E(s)}</div>' for s in steps)
    prev = LESSONS[i-1] if i > 0 else None; nxt = LESSONS[i+1] if i < len(LESSONS)-1 else None
    pn = (f'<a href="{prev["slug"]}.html"><small>← Նախորդ դաս</small><b>Դաս {prev["n"]} · {E(prev["short"])}</b></a>' if prev else '<span></span>') + (f'<a class="nx" href="{nxt["slug"]}.html"><small>Հաջորդ դաս →</small><b>Դաս {nxt["n"]} · {E(nxt["short"])}</b></a>' if nxt else '<span></span>')
    hero_bg = f'<div class="ph" style="background-image:url(\'assets/img/{L["img"]}.jpg\')"></div>'
    body = f'''{header('lessons')}<div style="--acc:{acc}">
<section class="hero lhero">{hero_bg}<div class="wrap"><div class="kick">Դաս {L["n"]} · {E(L["date"])}</div><h1>{E(L["t"])}</h1><p class="lead">{E(L["idea"])}</p>
<div class="ctas">{f'<a class="btn" href="{hw["deck"]}">{ICON["play"]}Ներկայացում</a>' if hw else ''}<a class="btn {'gh' if hw else ''}" href="#simple">📖 Դասը պարզ լեզվով</a><a class="btn gh" href="#files">{ICON["dl"]}Ֆայլեր</a></div></div></section>
<nav class="lnav"><div class="wrap in"><a href="#simple">Պարզ լեզվով</a><a href="#formulas">Բանաձևեր</a><a href="#glossary">Բառարան</a>{'<a href="#slides">Սլայդներ</a>' if sl else ''}<a href="#files">Ֆայլեր</a><a href="#homework">Տնային</a><a href="#diy">Ինչպես կատարել</a></div></nav>
<section class="sec" id="simple"><div class="wrap"><div class="kick rv">Դասը պարզ լեզվով</div><h2 class="rv">Ի՞նչ ենք սովորում</h2>
<div class="idea"><div class="card rv"><div class="big">{E(L["idea"])}</div></div><div class="card an rv"><b>Կյանքից օրինակ</b>{E(L["analogy"])}</div></div><div class="pts">{pts}</div></div></section>
<section class="sec" id="formulas"><div class="wrap"><div class="kick rv">Բանաձևեր</div><h2 class="rv">Գլխավոր ցուցանիշները</h2><p class="sd rv">Յուրաքանչյուր քարտում՝ բանաձևը, թե ինչ է այն ցույց տալիս և ո՞ր ուղղությամբ է լավ փոփոխությունը։</p><div class="fx">{fx}</div></div></section>
<section class="sec" id="glossary"><div class="wrap"><div class="kick rv">Բառարան</div><h2 class="rv">Կրճատումներ</h2><div class="gl">{gl}</div></div></section>
{f'<section class="sec" id="slides"><div class="wrap"><div class="kick rv">Դասախոսի սլայդներ</div><h2 class="rv">{len(sl)} սլայդ</h2><p class="sd rv">Սեղմեք սլայդի վրա՝ մեծ դիտելու համար։ Սլաքներով կամ սահեցնելով անցեք հաջորդին։</p><div class="slides">{slides}</div></div></section>' if sl else ''}
<section class="sec" id="files"><div class="wrap"><div class="kick rv">Ֆայլեր</div><h2 class="rv">Դասախոսի նյութերը</h2><div class="files">{files}</div></div></section>
<section class="sec" id="homework"><div class="wrap"><div class="kick rv">Տնային աշխատանք</div><h2 class="rv">Լուծում</h2>{hwhtml}</div></section>
<section class="sec" id="diy"><div class="wrap"><div class="kick rv">Ուսանողների համար</div><h2 class="rv">Ինչպես կատարել ինքնուրույն</h2><div class="steps">{stp}</div>
{f'<div class="ctas"><a class="btn gh" href="{tpl}" download>{ICON["dl"]}Ներբեռնել դատարկ ձևանմուշը</a></div>' if tpl else ''}
<div class="pn">{pn}</div></div></section></div>
<div class="lb" id="lb"><img alt=""><div class="bar"><button class="btn gh pv">←</button><span></span><button class="btn gh nx">→</button><button class="btn gh cl">✕</button></div></div>
{footer()}{JS}</body></html>'''
    open(os.path.join(SITE, L['slug'] + '.html'), 'w').write(head(f'Դաս {L["n"]} · {L["t"]} · H/R Studios', L['idea']) + body)

if __name__ == '__main__':
    if not os.path.exists(os.path.join(SITE, 'assets', 'intro.mp4')):
        shutil.copy(os.path.join(SITE, 'assets', 'bg-flow.mp4'), os.path.join(SITE, 'assets', 'intro.mp4'))
    build_index()
    for i, L in enumerate(LESSONS): build_lesson(i, L)
    hp = os.path.join(SITE, '_headers')
    if os.path.exists(hp): os.remove(hp)
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    print('ok', len(LESSONS))
