# -*- coding: utf-8 -*-
"""H/R Studios v3 — dark premium design system (Linear / Vercel / Apple Pro feel) with quality liquid glass.
Builds: index.html, lesson-1..8.html, works.html, formulas.html. Run AFTER hw/hwpage2.py. Then injects extras assets everywhere."""
import os, re, json, html, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import LESSONS, FILES, COURSE, TEACHER
import gen, gen2, extras
E = html.escape
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, "site"); GEN = os.path.join(BASE, "gen")
strip = extras.strip
ACC = {1: "#7aa2ff", 2: "#5eead4", 3: "#a78bfa", 4: "#fbbf24", 5: "#34d399", 6: "#f472b6", 7: "#a3e635", 8: "#fb7185"}
COVER = lambda n: f"assets/v3/l{n}.jpg"
def CAROUSEL():
    h = extras.carousel()
    for L in LESSONS:
        h = h.replace(f'assets/gen/{L["img"]}_s.jpg', COVER(L["n"]))
    return h

# ---------------- icons (24px line set) ----------------
P = {
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
 "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14v4M8 18h.01M12 18h.01"/>',
 "play": '<polygon points="6 4 20 12 6 20 6 4"/>', "dl": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5M12 15V3"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>', "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
 "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 "check": '<path d="M20 6L9 17l-5-5"/>', "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
 "spark": '<path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/><path d="M19 3v4M17 5h4"/>', "layers": '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "arrowl": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>', "help": '<circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01"/>',
 "sigma": '<path d="M18 7V4H6l6 8-6 8h12v-3"/>', "cards": '<rect x="2" y="6" width="14" height="14" rx="2"/><path d="M8 2h12a2 2 0 0 1 2 2v12"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>', "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a7 7 0 0 1 14 0v1"/>',
 "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>', "film": '<rect x="2" y="3" width="20" height="18" rx="2"/><path d="M7 3v18M17 3v18M2 8h5M17 8h5M2 16h5M17 16h5"/>',
 "table": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>', "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>', "proj": '<rect x="2" y="7" width="20" height="10" rx="2"/><circle cx="8" cy="12" r="2"/><path d="M14 11h4M14 14h2"/>',
 "star": '<polygon points="12 2 15 8.6 22 9.3 16.8 14 18.2 21 12 17.4 5.8 21 7.2 14 2 9.3 9 8.6"/>', "cap": '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
 "wand": '<path d="M15 4V2M15 16v-2M8 9h2M20 9h2M17.8 11.8L19 13M17.8 6.2L19 5M3 21l9-9M12.2 6.2L11 5"/>', "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
}
def I(name, size=18, cls="ico"): return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

def words(t, k0=0, cls="w"):
    return " ".join(f'<span class="{cls}" style="--k:{i+k0}">{E(x)}</span>' for i, x in enumerate(t.split()))

CSS3 = open(os.path.join(GEN, "v3.css"), encoding="utf8").read()
JS3 = "<script>" + open(os.path.join(GEN, "v3.js"), encoding="utf8").read() + "</script>"

def head(title, desc, pre=""):
    return f'''<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#07080a"><link rel="icon" href="assets/logo_sm.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Armenian:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap">
<style>{CSS3}</style></head><body>{pre}<div class="bg" aria-hidden="true"><i class="au a"></i><i class="au b"></i><i class="au c"></i><div class="gridl"></div><div class="noise"></div></div><div class="ptrans"></div>'''

NAV = [("index.html#lessons", "Դասեր", "lessons"), ("index.html#library", "Նյութեր", "library"), ("formulas.html", "Բանաձևեր", "formulas"), ("works.html", "Լուծումներ", "works")]
def header(active=""):
    nav = "".join(f'<a href="{h}" class="{"on" if k == active else ""}">{t}</a>' for h, t, k in NAV)
    return f'''<header class="hdr"><div class="wrap"><a class="logo" href="index.html" aria-label="Գլխավոր"><img src="assets/logo_sm.png" alt=""><span>H/R Studios</span></a>
<nav class="nav" id="nav">{nav}</nav><button class="burger" aria-label="Մենյու" onclick="document.body.classList.toggle('menu-on')">{I("menu", 20)}</button></div></header>'''

def footer():
    links = "".join(f'<a href="{L["slug"]}.html">Դաս {L["n"]} · {E(L["short"])}</a>' for L in LESSONS)
    return f'''<footer class="ftr"><div class="wrap"><div class="fgrid">
<div><a class="logo" href="index.html"><img src="assets/logo_sm.png" alt=""><span>H/R Studios</span></a><p>Ուսումնական հարթակ ՀԱՊՀ ԻՏ-447 խմբի համար։ Բոլոր նյութերը՝ պարզ, գեղեցիկ և անվճար։</p>
<p class="mut">Հեղինակ՝ Հրաչյա Ասլանյան · Դասախոս՝ {E(TEACHER)}</p></div>
<div><h4>Դասեր</h4>{links}</div>
<div><h4>Հարթակ</h4><a href="index.html#lessons">Բոլոր դասերը</a><a href="index.html#library">Նյութերի գրադարան</a><a href="formulas.html">Բանաձևերի թերթիկ</a><a href="works.html">Լուծված առաջադրանքներ</a><a href="index.html#faq">Հաճախ տրվող հարցեր</a></div>
</div><div class="copy"><span>© 2026 H/R Studios</span><span>Դասախոսի նյութերը տեղադրված են ուսումնական նպատակով։</span></div></div></footer>'''

def sec_head(kick, title, sub="", center=False):
    return f'<div class="shead{" c" if center else ""}"><span class="kick rv">{E(kick)}</span><h2 class="rv">{title}</h2>{f"<p class=\"sub rv\">{sub}</p>" if sub else ""}</div>'

def fext(f): return f.rsplit(".", 1)[1].lower()
def fcard(mat, f, title, kind, lab=""):
    p = os.path.join(SITE, "materials", mat, f); ext = fext(f); url = f"materials/{mat}/{f}"
    L = next((x for x in LESSONS if x["mat"] == mat), None)
    hr = ""
    if L and kind in ("slides", "lecture"):
        h = f'materials/{mat}/HR_Das{L["n"]}_' + ("prezentacia.pptx" if kind == "slides" else "konspekt.pdf")
        hr = f'<a class="ibtn hr" href="{h}" {"download" if h.endswith(".pptx") else "target=_blank rel=noopener"} data-tipx="H/R տարբերակ (գեղեցիկ)">{I("spark", 16)}<span>H/R</span></a>'
    view = f'<a class="ibtn" href="{url}" target="_blank" rel="noopener" data-tipx="Բացել">{I("eye", 16)}</a>' if ext == "pdf" else ""
    return (f'<div class="fcd gc rv" data-k="{kind}"><span class="ext e-{ext}">{ext.upper()}</span><div class="fm">{f"<small class=lt>{E(lab)}</small>" if lab else ""}<b>{E(title)}</b>'
            f'<small>{gen.KIND.get(kind, "")} · {gen.fsize(p)}</small></div><div class="fa">{hr}{view}<a class="ibtn" href="{url}" download data-tipx="Ներբեռնել բնօրինակը">{I("dl", 16)}</a></div></div>')

def hrpair(L):
    mat, n = L["mat"], L["n"]; a = f"materials/{mat}/HR_Das{n}_prezentacia.pptx"; b = f"materials/{mat}/HR_Das{n}_konspekt.pdf"
    return (f'<div class="hrp"><a class="hrc glass rv" href="{a}" download><span class="hico">{I("film", 22)}</span><span><b>H/R ներկայացում</b><small>Դասախոսի սլայդները՝ նոր ձևավորմամբ · PPTX · {gen.fsize(os.path.join(SITE, a))}</small></span>{I("dl", 18, "ico go")}</a>'
            f'<a class="hrc glass rv" href="{b}" target="_blank" rel="noopener"><span class="hico">{I("book", 22)}</span><span><b>H/R կոնսպեկտ</b><small>Ամբողջ դասը մեկ PDF-ում · {gen.fsize(os.path.join(SITE, b))}</small></span>{I("eye", 18, "ico go")}</a></div>')

def slides_of(mat): return gen.slides_of(mat)

# ================= INDEX =================
def build_index():
    nfiles = sum(len(v) for v in FILES.values()); nform = sum(len(L["formulas"]) for L in LESSONS)
    stack = "".join(f'<div class="hs-card glass" style="--i:{i}"><img src="{COVER(n)}" alt=""><span>Դաս {n} · {E(LESSONS[n-1]["short"])}</span></div>' for i, n in enumerate([2, 7, 3]))
    hero = f'''<section class="hero" id="top"><div class="wrap hgrid"><div class="htxt">
<a class="pill rv" href="works.html"><span class="dot"></span>Նոր՝ 7 լուծված առաջադրանք {I("arrow", 14)}</a>
<h1 class="tl">{words("Տնտեսական վերլուծությունը՝")} <span class="grd">{words("պարզ և հասկանալի", 2)}</span></h1>
<p class="lead fu">Բոլոր դասերը, դասախոսի ֆայլերը, բանաձևերը և լուծված տնայինները մեկ տեղում։ Առանց բարդ բառերի. ամեն ինչ բացատրված է այնպես, որ հասկանալի լինի բոլորին։</p>
<div class="ctas fu"><a class="btn pri mag" href="lesson-1.html">{I("play", 16)}Սկսել առաջին դասից</a><a class="btn mag" href="#library">{I("folder", 16)}Գտնել ֆայլ</a></div>
<div class="hmeta fu"><span>{I("check", 15)}Անվճար</span><span>{I("phone", 15)}Աշխատում է հեռախոսով</span><span>{I("cap", 15)}ԻՏ-447 · 2026–2027</span></div></div>
<div class="hvis" data-par><div class="orbimg"><img src="assets/v3/hero.jpg" alt=""></div><div class="hstack">{stack}</div></div></div>
<div class="wrap"><div class="stats">{"".join(f'<div class="st rv" style="--i:{i}"><b data-count="{v}">{v}</b><span>{t}</span></div>' for i, (v, t) in enumerate([(len(LESSONS), "դաս"), (nfiles, "դասախոսի ֆայլ"), (nform, "բանաձև"), (7, "լուծված առաջադրանք")]))}</div></div></section>'''
    steps = [("Ընտրիր դասը", "Յուրաքանչյուր դաս ունի իր էջը։ Սեղմիր քարտի վրա և կտեսնես ամբողջ նյութը մեկ տեղում։", "grid"),
             ("Կարդա պարզ բացատրությունը", "«Պարզ լեզվով» բաժինը, կյանքից օրինակը և 25 վայրկյանանոց անիմացիան կօգնեն արագ հասկանալ թեման։", "book"),
             ("Ստուգիր քեզ", "Լրացրու թվերը հաշվիչում կամ անցիր թեստը. կտեսնես՝ ճիշտ ես հասկացել, թե ոչ։", "list"),
             ("Ներբեռնիր ֆայլերը", "Դասախոսի բնօրինակը կամ մեր գեղեցիկ H/R տարբերակը՝ մեկ սեղմումով։", "dl")]
    st_txt = "".join(f'<div class="stp" data-step="{i}"><span class="sn">0{i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d, ic) in enumerate(steps))
    st_vis = "".join(f'<div class="sv glass{" on" if i == 0 else ""}" data-sv="{i}">{v}</div>' for i, v in enumerate([
        '<div class="mini-grid">' + "".join(f'<div style="--i:{k}"><img src="{COVER(n)}" alt=""><b>Դաս {n}</b></div>' for k, n in enumerate([1, 2, 3, 4, 5, 6])) + '</div>',
        f'<div class="mini-read"><span class="kick">Դասը պարզ լեզվով</span><p class="q">«{E(LESSONS[1]["idea"])}»</p><div class="mbars">' + "".join(f'<i style="--h:{h}%;--i:{k}"></i>' for k, h in enumerate([35, 60, 45, 80, 70])) + '</div></div>',
        '<div class="mini-quiz"><b>Ի՞նչ է ցույց տալիս Գբի-ն</b>' + "".join(f'<span class="{c}">{t}</span>' for t, c in [("Բացարձակ իրացվելիություն", "ok"), ("Ֆոնդահատույց", ""), ("Նյութատարություն", "")]) + '<div class="mres">✓ Ճիշտ է · 8/8</div></div>',
        '<div class="mini-files">' + "".join(f'<div style="--i:{k}"><span class="ext e-{e}">{e.upper()}</span><b>{t}</b>{I("dl", 16)}</div>' for k, (e, t) in enumerate([("pdf", "Դաս 2 · սլայդներ"), ("pptx", "H/R ներկայացում"), ("xlsx", "Տնային · Excel")])) + '</div>']))
    how = f'''<section class="sec" id="how"><div class="wrap">{sec_head("Ինչպես օգտվել", "Չորս պարզ քայլ", "Կայքը ստեղծված է այնպես, որ հասկանալի լինի առանց որևէ տեխնիկական գիտելիքի։", True)}
<div class="story"><div class="stxt">{st_txt}</div><div class="svis">{st_vis}</div></div></div></section>'''
    cards = ""
    for L in LESSONS:
        n = L["n"]; st = f'<span class="badge ok">{I("check", 13)}Լուծված</span>' if L["hw"] else '<span class="badge">Տեսություն</span>'
        cards += f'''<a class="lcard gc rv" href="{L["slug"]}.html" style="--a:{ACC[n]};--i:{(n-1)%4}"><div class="lcimg"><img src="{COVER(n)}" alt="" loading="lazy"></div>
<div class="lcb"><div class="lct"><span class="num">{n:02d}</span>{st}</div><h3>{E(L["t"])}</h3><p>{E(L["idea"][:105])}…</p>
<div class="lcf"><span>{I("file", 14)}{len(FILES[L["mat"]])} ֆայլ</span><span>{I("sigma", 14)}{len(L["formulas"])} բանաձև</span><span class="go">{I("arrow", 16)}</span></div></div><span class="dmark">{I("check", 14)}</span></a>'''
    lessons = f'''<section class="sec" id="lessons"><div class="wrap">{sec_head("Դասընթաց", "Ութ դաս՝ մեկ ճանապարհ", "Յուրաքանչյուր դասում՝ պարզ բացատրություն, անիմացիա, բանաձևեր, հաշվիչ, թեստ, սլայդներ և ֆայլեր։")}</div>
{CAROUSEL().replace('<section class="sec car3"><div class="wrap"><div class="kick rv">Ընտրիր դասը</div><h2 class="rv">Դասերի կարուսել</h2><p class="sd rv">Քաշիր մկնիկով կամ մատով, սեղմիր քարտի վրա՝ դասը բացելու համար։</p></div>', '<div class="car3">').replace('</div></div></section>', '</div></div></div>', 1)}
<div class="wrap"><div class="lgrid">{cards}</div></div></section>'''
    bento = f'''<section class="sec" id="tools"><div class="wrap">{sec_head("Գործիքներ", "Ամեն ինչ՝ սովորելու համար", "Օգտակար գործիքներ, որոնք աշխատում են հենց բրաուզերում. ոչինչ տեղադրել պետք չէ։", True)}
<div class="bento">
<a class="bt gc rv b1" href="lesson-2.html#calc"><div class="bvis calcv"><span>Գբի</span><b data-tick="0.333">0.333</b><em>✔ նորմայում</em></div><h3>{I("calc")}Հաշվիչ</h3><p>Գրիր քո թվերը՝ գործակիցները և եզրակացությունը կհայտնվեն անմիջապես։</p></a>
<a class="bt gc rv b2" href="lesson-2.html#quiz"><div class="bvis quizv"><span>Ա) 0.5-ից պակաս</span><span class="ok">Բ) 1-ից մեծ ✓</span><span>Գ) Միշտ զրո</span></div><h3>{I("list")}Թեստ և քարտեր</h3><p>8 հարց յուրաքանչյուր դասից, արդյունքը պահպանվում է։</p></a>
<a class="bt gc rv b3" href="formulas.html"><div class="bvis formv"><code>Գբի = (ԴՄ + ԿՖՆ) ÷ ԸՊ</code></div><h3>{I("sigma")}Բանաձևերի թերթիկ</h3><p>Բոլոր {nform} բանաձևերը մեկ էջում, տպելու համար՝ մեկ A4։</p></a>
<button class="bt gc rv b4" onclick="document.querySelector('.ksb')&&document.querySelector('.ksb').click()"><div class="bvis srchv"><span>{I("search", 16)}<em class="typ">իրացվելիություն</em></span><kbd>Ctrl K</kbd></div><h3>{I("search")}Արագ որոնում</h3><p>Գտիր ցանկացած դաս, բանաձև, տերմին կամ ֆայլ վայրկյանում։</p></button>
<a class="bt gc rv b5" href="lesson-4.html#explain"><div class="bvis animv"><i></i><i></i><i></i><i></i><i></i></div><h3>{I("film")}Անիմացիոն բացատրություններ</h3><p>Յուրաքանչյուր դաս՝ 25 վայրկյանում։</p></a>
<div class="bt gc rv b6"><div class="bvis projv">{I("proj", 40)}</div><h3>{I("proj")}Պրոյեկտորի ռեժիմ</h3><p>Մեծ տառեր և բարձր կոնտրաստ՝ դասարանում ցուցադրելու համար։</p></div>
</div></div></section>'''
    tabs = panes = ""
    groups = [(L["mat"], f'Դաս {L["n"]}', L) for L in LESSONS] + [("mid", "Միջանկյալ", None)]
    for i, (m, lab, L) in enumerate(groups):
        on = " on" if i == 0 else ""
        tabs += f'<button class="ltab{on}" data-p="{m}">{lab}</button>'
        headp = (f'<div class="lph"><div><span class="kick">Դաս {L["n"]} · {E(L["date"])}</span><h3>{E(L["t"])}</h3></div><a class="btn sm" href="{L["slug"]}.html">Դասի էջը {I("arrow", 14)}</a></div>'
                 f'<span class="lbl2">{I("spark", 14)}Մեր գեղեցիկ տարբերակը</span>{hrpair(L)}') if L else '<div class="lph"><div><span class="kick">Քննություն</span><h3>1-ին միջանկյալ ստուգում</h3></div><a class="btn sm" href="hw/mijankyal/index.html">Տեսնել լուծումը {I("arrow", 14)}</a></div>'
        fl = "".join(fcard(m, f, t, k) for f, t, k in FILES[m])
        panes += f'<div class="lpane{on}" data-p="{m}">{headp}<span class="lbl2">{I("folder", 14)}Դասախոսի բնօրինակ ֆայլերը</span><div class="files">{fl}</div></div>'
    library = f'''<section class="sec" id="library"><div class="wrap">{sec_head("Գրադարան", "Դասախոսի բոլոր նյութերը", "Ընտրիր դասը։ PDF ֆայլերը բացվում են հենց բրաուզերում, մնացածը կարող ես ներբեռնել։ Կողքին՝ մեր նոր, գեղեցիկ տարբերակը։")}
<div class="libbar rv"><div class="ltabs">{tabs}</div><label class="lsrch">{I("search", 16)}<input id="srch2" placeholder="Որոնել ֆայլ…"></label></div><div class="lpanes glass rv">{panes}</div></div></section>'''
    faq = [("Ի՞նչ է այս կայքը", "Սա ուսումնական հարթակ է «Տնտեսական գործունեության վերլուծություն» առարկայի համար։ Այստեղ կան բոլոր դասերը, դասախոսի ֆայլերը և լուծված օրինակներ։"),
           ("Պե՞տք է արդյոք ինչ-որ բան տեղադրել", "Ոչ։ Ամեն ինչ աշխատում է բրաուզերում՝ համակարգչով թե հեռախոսով։ Պարզապես բացիր դասը։"),
           ("Excel չունեմ, ինչպե՞ս բացեմ .xlsx ֆայլը", "Կարող ես բացել անվճար Google Sheets-ով (sheets.google.com → Ֆայլ → Ներմուծել) կամ հեռախոսի Excel հավելվածով։"),
           ("Ի՞նչ է «H/R տարբերակը»", "Դա դասախոսի նույն նյութն է՝ մեր կողմից նոր, ավելի գեղեցիկ ու հասկանալի ձևավորմամբ, բանաձևերով և բառարանով։ Բնօրինակը նույնպես հասանելի է։"),
           ("Ինչպե՞ս արագ գտնել բանաձևը կամ տերմինը", "Սեղմիր վերևի 🔍 կոճակը կամ Ctrl + K և գրիր բառը։ Իսկ տեքստում ընդգծված կրճատման վրա մկնիկը պահելով կտեսնես դրա բացատրությունը։"),
           ("Կարո՞ղ եմ ցուցադրել պրոյեկտորով", "Այո։ Վերևում ընտրիր «Պրոյեկտոր» ռեժիմը. տառերը կմեծանան, իսկ կոնտրաստը՝ կբարձրանա։")]
    faqh = "".join(f'<details class="fq glass rv" style="--i:{i}"><summary>{E(q)}<span class="pm"></span></summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faq))
    faqs = f'<section class="sec" id="faq"><div class="wrap narrow">{sec_head("Հարցեր", "Հաճախ տրվող հարցեր", "", True)}<div class="faq">{faqh}</div></div></section>'
    cta = f'''<section class="sec"><div class="wrap"><div class="cta glass rv"><div><h2>Պատրա՞ստ ես սկսել</h2><p>Առաջին դասը տևում է ընդամենը 10 րոպե։</p></div><a class="btn pri mag" href="lesson-1.html">{I("play", 16)}Սկսել հիմա</a></div></div></section>'''
    body = f"{header('home')}<main>{hero}{how}{lessons}{bento}{library}{faqs}{cta}</main>{footer()}{gen2.LIBJS}{JS3}</body></html>"
    open(os.path.join(SITE, "index.html"), "w", encoding="utf8").write(head(f"{COURSE} · H/R Studios", "Ուսումնական հարթակ ԻՏ-447 խմբի համար", gen2.INTRO2) + body)

# ================= LESSON =================
DIRT = {"up": ("Որքան բարձր, այնքան լավ", "up"), "down": ("Որքան ցածր, այնքան լավ", "down"), "norm": ("Պետք է լինի նորմայում", "norm")}
def build_lesson(i, L):
    n = L["n"]; mat = L["mat"]; sl = slides_of(mat); hw = L["hw"]; acc = ACC[n]
    pts = "".join(f'<div class="pt gc rv" style="--i:{k}"><span class="pn">{k+1}</span><b>{E(a)}</b><p>{E(b)}</p></div>' for k, (a, b) in enumerate(L["points"]))
    fx = "".join(f'''<div class="fx gc rv" style="--i:{k%3}"><div class="fxh"><span class="code">{c}</span>{f'<span class="dir {DIRT[d][1]}">{DIRT[d][0]}</span>' if d else ""}</div><b>{E(nm)}</b><div class="eq">{c} = {f}</div><p>{E(m)}</p></div>''' for k, (c, nm, f, m, d) in enumerate(L["formulas"]))
    gl = "".join(f'<div class="gli rv" style="--i:{k%4}"><code>{E(a)}</code><span>{E(b)}</span></div>' for k, (a, b) in enumerate(L["glossary"]))
    slides = "".join(f'<button class="sld" data-src="materials/{mat}/slides/{s}" aria-label="Սլայդ {k+1}"><img loading="lazy" src="materials/{mat}/slides/{s}" alt=""><i>{k+1:02d}</i></button>' for k, s in enumerate(sl))
    files = "".join(fcard(mat, f, t, k) for f, t, k in FILES[mat])
    if hw:
        stx = "".join(f'<div><b data-count="{a}">{a}</b><span>{E(b)}</span></div>' for a, b in hw["stats"])
        rs = "".join(f'<div class="rr"><span>{E(a)}</span><b>{E(b)}</b></div>' for a, b in hw["result"])
        hwh = f'''<div class="hwg"><div class="glass hwc rv"><span class="kick">Առաջադրանք</span><p class="big">{E(hw["task"])}</p><div class="hst">{stx}</div>
<div class="ctas"><a class="btn pri" href="{hw["deck"]}">{I("play", 16)}Բացել լուծումը</a><a class="btn" href="{hw["file"]}" download>{I("table", 16)}Excel լուծումը</a>{f'<a class="btn" href="{hw["tpl"]}" download>{I("dl", 16)}Դատարկ ձևանմուշ</a>' if hw.get("tpl") else ""}</div></div>
<div class="glass hwr rv"><span class="kick">Գլխավոր արդյունքները</span>{rs}</div></div>'''
    else:
        hwh = f'<div class="glass empty rv">{I("book", 28)}<div><b>Այս դասը տեսական է</b><p>Տնային աշխատանք չկա. կարդացեք բացատրությունը, ստուգեք ձեզ թեստով և օգտագործեք հաշվիչը։</p></div></div>'
    steps = ["Կարդացեք «Պարզ լեզվով» բաժինը և դիտեք անիմացիան։", "Ուսումնասիրեք բանաձևերի քարտերը և բառարանը։", "Բացեք դասախոսի սլայդները՝ լուծված օրինակով։",
             "Ներբեռնեք առաջադրանքը «Ֆայլեր» բաժնից։", "Excel-ում ամեն գործակից հաշվեք բանաձևով (= նշանով), ոչ թե ձեռքով։", "Ստուգեք արդյունքը հաշվիչով և լուծված ֆայլով։"]
    stp = "".join(f'<div class="dstep gc rv" style="--i:{k%3}"><span>{k+1}</span><p>{E(s)}</p></div>' for k, s in enumerate(steps))
    prev = LESSONS[i-1] if i > 0 else None; nxt = LESSONS[i+1] if i < len(LESSONS) - 1 else None
    pn = (f'<a class="pnl glass" href="{prev["slug"]}.html">{I("arrowl", 18)}<span><small>Նախորդ դաս</small><b>Դաս {prev["n"]} · {E(prev["short"])}</b></span></a>' if prev else '<span></span>') + \
         (f'<a class="pnl nx glass" href="{nxt["slug"]}.html"><span><small>Հաջորդ դաս</small><b>Դաս {nxt["n"]} · {E(nxt["short"])}</b></span>{I("arrow", 18)}</a>' if nxt else '<span></span>')
    subnav = [("simple", "Պարզ լեզվով"), ("explain", "Անիմացիա"), ("formulas", "Բանաձևեր"), ("glossary", "Բառարան"), ("calc", "Հաշվիչ"), ("quiz", "Թեստ")] + ([("slides", "Սլայդներ")] if sl else []) + [("files", "Ֆայլեր"), ("homework", "Տնային"), ("diy", "Ինչպես կատարել")]
    sn = "".join(f'<a href="#{a}">{t}</a>' for a, t in subnav)
    facts = [(I("clock", 15), L["date"]), (I("file", 15), f'{len(FILES[mat])} ֆայլ'), (I("sigma", 15), f'{len(L["formulas"])} բանաձև')] + ([(I("layers", 15), f"{len(sl)} սլայդ")] if sl else []) + [(I("check", 15) if hw else I("book", 15), "Լուծված տնային" if hw else "Տեսական դաս")]
    exp = extras.explainer(L).replace('<section class="sec" id="explain"><div class="wrap"><div class="kick rv">Անիմացիոն բացատրություն · ~25 վրկ</div><h2 class="rv">Դասը՝ 25 վայրկյանում</h2>', f'<section class="sec" id="explain"><div class="wrap">{sec_head("Անիմացիա · 25 վրկ", "Դասը՝ 25 վայրկյանում")}').replace(f"assets/gen/{L['img']}.jpg", COVER(n))
    calc = extras.calc_html(n).replace(f'<div class="kick rv">Ինտերակտիվ</div><h2 class="rv">Հաշվիչ</h2><p class="sd rv">', f'{sec_head("Ինտերակտիվ", "Հաշվիչ")}<p class="sub rv" style="margin-top:-18px;margin-bottom:24px">')
    quiz = extras.quiz_html(n).replace('<div class="kick rv">Ստուգիր քեզ</div><h2 class="rv">Թեստ և քարտեր</h2>', sec_head("Ստուգիր քեզ", "Թեստ և քարտեր"))
    body = f'''{header('lessons')}<main style="--acc:{acc}" data-lesson-page>
<section class="lhero"><div class="wrap lhg"><div><a class="back rv" href="index.html#lessons">{I("arrowl", 15)}Բոլոր դասերը</a><span class="lnum rv">ԴԱՍ {n:02d}</span><h1 class="tl">{words(L["t"])}</h1><p class="lead fu">{E(L["idea"])}</p>
<div class="ctas fu">{f'<a class="btn pri mag" href="{hw["deck"]}">{I("play", 16)}Դիտել լուծումը</a>' if hw else f'<a class="btn pri mag" href="#simple">{I("book", 16)}Սկսել կարդալ</a>'}<a class="btn mag" href="#files">{I("dl", 16)}Ֆայլեր</a></div>
<div class="facts fu">{"".join(f"<span>{a}{E(b)}</span>" for a, b in facts)}</div></div><div class="lvis fu" data-par><div class="glass lcov"><img src="{COVER(n)}" alt=""></div><span class="bign">{n:02d}</span></div></div></section>
<nav class="lnav"><div class="wrap"><div class="lnin">{sn}</div></div></nav>
<section class="sec" id="simple"><div class="wrap">{sec_head("Դասը պարզ լեզվով", "Ի՞նչ ենք սովորում")}
<div class="idea"><div class="glass ideac rv"><span class="qmark">“</span><p>{E(L["idea"])}</p></div><div class="glass anc rv"><span class="kick">{I("spark", 14)} Կյանքից օրինակ</span><p>{E(L["analogy"])}</p></div></div><div class="pts">{pts}</div></div></section>
{exp}
<section class="sec" id="formulas"><div class="wrap">{sec_head("Բանաձևեր", "Գլխավոր ցուցանիշները", "Յուրաքանչյուր քարտում՝ բանաձևը, դրա իմաստը և թե որ ուղղությամբ է փոփոխությունը լավ։")}<div class="fxg">{fx}</div></div></section>
<section class="sec" id="glossary"><div class="wrap">{sec_head("Բառարան", "Կրճատումներ")}<div class="glg">{gl}</div></div></section>
{calc}{quiz}
{f'<section class="sec" id="slides"><div class="wrap">{sec_head("Դասախոսի սլայդներ", f"{len(sl)} սլայդ", "Սեղմեք սլայդի վրա՝ մեծ դիտելու համար։ Սլաքներով կամ մատով սահեցնելով անցեք հաջորդին։")}<div class="slides">{slides}</div></div></section>' if sl else ""}
<section class="sec" id="files"><div class="wrap">{sec_head("Ֆայլեր", "Դասի նյութերը")}<span class="lbl2">{I("spark", 14)}Մեր գեղեցիկ տարբերակը</span>{hrpair(L)}<span class="lbl2">{I("folder", 14)}Դասախոսի բնօրինակները</span><div class="files">{files}</div></div></section>
<section class="sec" id="homework"><div class="wrap">{sec_head("Տնային աշխատանք", "Լուծում")}{hwh}</div></section>
<section class="sec" id="diy"><div class="wrap">{sec_head("Ինքնուրույն", "Ինչպես կատարել քայլ առ քայլ")}<div class="dsteps">{stp}</div></div></section>
{extras.done_btn(n)}<div class="wrap"><div class="pnav">{pn}</div></div></main>
<div class="lb" id="lb"><img alt=""><div class="lbar"><button class="pv" aria-label="Նախորդ">{I("arrowl", 18)}</button><span></span><button class="nx" aria-label="Հաջորդ">{I("arrow", 18)}</button><button class="cl" aria-label="Փակել">✕</button></div></div>
{footer()}{JS3}</body></html>'''
    open(os.path.join(SITE, L["slug"] + ".html"), "w", encoding="utf8").write(head(f'Դաս {n} · {L["t"]} · H/R Studios', L["idea"]).replace("<body>", f'<body data-lesson="{n}">', 1) + body)

# ================= WORKS =================
def build_works():
    cards = ""
    for k, w in enumerate(gen2.WORKS):
        its = "".join(f'<a class="wit" href="{u}"{" download" if u.endswith((".xlsx", ".pdf")) else ""}><span class="wi">{I("table" if u.endswith(".xlsx") else "file" if u.endswith(".pdf") else "play", 18)}</span><span><b>{E(nm)}</b><small>{E(s)}</small></span>{I("arrow", 16, "ico go")}</a>' for ic, nm, u, s in w["items"])
        cards += f'<div class="wcard gc rv" style="--i:{k%2}"><div class="wimg" style="background-image:url(\'assets/gen/{w["img"]}.jpg\')"><span class="badge">{E(w["l"])}</span></div><div class="wb"><h3>{E(w["t"])}</h3>{its}</div></div>'
    tl = extras.timeline().replace('<section class="sec"><div class="wrap"><div class="kick rv">Ժամանակագրություն</div><h2 class="rv">Առաջադրանքները՝ դասից դաս</h2><p class="sd rv">Յուրաքանչյուր առաջադրանք՝ իր ամսաթվով և իր ձևավորմամբ։</p>',
                                   f'<section class="sec"><div class="wrap">{sec_head("Ժամանակագրություն", "Առաջադրանքները՝ դասից դաս", "Յուրաքանչյուր առաջադրանք՝ իր ամսաթվով և իր ձևավորմամբ։", True)}')
    body = f'''{header('works')}<main><section class="phero"><div class="wrap"><span class="kick rv">Օրինակելի լուծումներ</span><h1 class="tl">{words("Լուծված առաջադրանքներ")}</h1>
<p class="lead fu">Տնային առաջադրանքների պատրաստի լուծումներ. ինտերակտիվ ներկայացումներ, դաշբորդներ, PDF և Excel ֆայլեր՝ բանաձևերով։ Օգտագործիր որպես օրինակ կամ ստուգիր քո պատասխանը։</p></div></section>
{tl}<section class="sec"><div class="wrap">{sec_head("Բոլոր ֆայլերը", "Բացել կամ ներբեռնել")}<div class="wgrid">{cards}</div></div></section></main>{footer()}{JS3}</body></html>'''
    open(os.path.join(SITE, "works.html"), "w", encoding="utf8").write(head("Լուծված առաջադրանքներ · H/R Studios", "Տնային առաջադրանքների լուծված օրինակներ") + body)

# ================= FORMULAS =================
def build_formulas():
    blocks = ""
    for L in LESSONS:
        n = L["n"]
        rows = "".join(f'''<div class="fcard gc" data-s="{E((strip(c)+' '+nm+' '+strip(fx)+' '+m).lower())}"><div class="fh"><code>{c}</code><b>{E(nm)}</b><button class="cp" data-cp="{E(strip(c)+' = '+strip(fx))}" aria-label="Պատճենել">⧉</button></div><div class="ff">{fx}</div><p>{E(m)}</p></div>''' for c, nm, fx, m, d in L["formulas"])
        blocks += f'<section class="fles rv" style="--a:{ACC[n]}"><h2><span>Դաս {n}</span>{E(L["t"])}<a href="{L["slug"]}.html" aria-label="Դասի էջը">{I("arrow", 18)}</a></h2><div class="fgrid">{rows}</div></section>'
    body = f'''{header('formulas')}<main><section class="phero"><div class="wrap"><span class="kick rv">Թերթիկ · A4</span><h1 class="tl">{words("Բանաձևերի թերթիկ")}</h1>
<p class="lead fu">Բոլոր {sum(len(L["formulas"]) for L in LESSONS)} բանաձևերը՝ ըստ դասերի։ Որոնեք, պատճենեք մեկ սեղմումով, տպեք մեկ A4 էջի վրա։</p>
<div class="ctas fu"><label class="lsrch big">{I("search", 18)}<input class="fsrch" id="fsrch" placeholder="Որոնել՝ ՇԲԹ, իրացվելիություն, ÷ …" autocomplete="off"></label><button class="btn pri" onclick="print()">Տպել</button></div></div></section>
<div class="wrap fsheet"><div class="phead">H/R Studios · {E(COURSE)} · բանաձևերի թերթիկ · Հրաչյա Ասլանյան, ԻՏ-447</div>{blocks}</div></main>{footer()}{JS3}
<script>(function(){{const q=document.getElementById('fsrch');q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();document.querySelectorAll('.fcard').forEach(c=>c.style.display=!v||c.dataset.s.includes(v)?'':'none');document.querySelectorAll('.fles').forEach(s=>s.style.display=[...s.querySelectorAll('.fcard')].some(c=>c.style.display!=='none')?'':'none')}});
document.querySelectorAll('[data-cp]').forEach(b=>b.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(b.dataset.cp);b.textContent='✓';setTimeout(()=>b.textContent='⧉',1200)}})}})();</script></body></html>'''
    open(os.path.join(SITE, "formulas.html"), "w", encoding="utf8").write(head("Բանաձևերի թերթիկ · H/R Studios", "Բոլոր բանաձևերը մեկ էջում") + body)

def main():
    build_index(); build_works(); build_formulas()
    for i, L in enumerate(LESSONS): build_lesson(i, L)
    shutil.copy(os.path.join(GEN, "extras.css"), os.path.join(SITE, "assets", "hr-extra.css"))
    shutil.copy(os.path.join(GEN, "extras.js"), os.path.join(SITE, "assets", "hr-extra.js"))
    open(os.path.join(SITE, "assets", "hr-data.js"), "w", encoding="utf8").write(extras.data_js())
    for f in os.listdir(SITE):
        if f.endswith(".html") and f != "404.html": extras.inject(os.path.join(SITE, f), "")
    for d in os.listdir(os.path.join(SITE, "hw")):
        p = os.path.join(SITE, "hw", d, "index.html")
        if os.path.exists(p): extras.inject(p, "../../")
    open(os.path.join(SITE, ".nojekyll"), "w").write("")
    print("v3 ok")

if __name__ == "__main__":
    main()
