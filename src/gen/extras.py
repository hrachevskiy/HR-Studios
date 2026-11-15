# -*- coding: utf-8 -*-
"""Extras layer (runs after gen.py, gen2.py and hw/hwpage2.py):
calculators, quizzes + flashcards, formula cheat-sheet page, glossary tooltips, Ctrl+K search, themes (dark/light/projector),
read/done progress, works timeline, animated lesson explainers, 3D lesson carousel."""
import os, re, json, html, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import LESSONS, FILES, COURSE, TEACHER
import gen, gen2
E = html.escape
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, "site"); GEN = os.path.join(BASE, "gen")
strip = lambda s: re.sub(r"<[^>]+>", "", s)

# ---------------- calculators ----------------
CALC = {
 1: dict(title="Շեղումներ, աճի տեմպ, տեսակարար կշիռ և շղթայական տեղադրում",
   inputs=[("x0", "Ցուցանիշ՝ նախորդ տարի (Ց₀)", 8000), ("x1", "Ցուցանիշ՝ հաշվետու տարի (Ց₁)", 9360), ("part", "Մաս", 1500), ("whole", "Ամբողջ", 6000),
           ("a0", "Գործոն a₀", 100), ("b0", "Գործոն b₀", 80), ("a1", "Գործոն a₁", 120), ("b1", "Գործոն b₁", 78)],
   outs=[("Δ · բացարձակ շեղում", "x1-x0", 2, None, None), ("T · աճի տեմպ, %", "x1/x0*100", 2, 100, None), ("Հավելաճի տեմպ, %", "x1/x0*100-100", 2, 0, None),
         ("ՏԿ · տեսակարար կշիռ, %", "part/whole*100", 2, None, None), ("Y₀ = a₀ × b₀", "a0*b0", 2, None, None), ("Y₁ = a₁ × b₁", "a1*b1", 2, None, None),
         ("ΔY՝ a-ի հաշվին", "(a1-a0)*b0", 2, None, None), ("ΔY՝ b-ի հաշվին", "a1*(b1-b0)", 2, None, None)]),
 2: dict(title="Իրացվելիության գործակիցներ (հազ. դրամ)",
   inputs=[("cash", "Դրամական միջոցներ (ԴՄ)", 20000), ("cfi", "Կարճաժամկետ ֆին. ներդրումներ (ԿՖՆ)", 8000), ("rec", "Դեբիտորական պարտքեր (ԴՊ)", 60500), ("inv", "Պաշարներ", 71500),
           ("noa", "Ոչ ընթացիկ ակտիվներ", 100000), ("pay", "Կրեդիտորական պարտքեր", 60800), ("loan", "Կարճաժամկետ վարկ", 23410), ("ltl", "Ոչ ընթացիկ պարտավորություններ", 35790), ("eq", "Սեփական կապիտալ", 140000)],
   outs=[("Գբի · բացարձակ իրացվելիություն", "(cash+cfi)/(pay+loan)", 3, 0.2, 0.5), ("Գաի · արագ իրացվելիություն", "(cash+cfi+rec)/(pay+loan)", 3, 0.7, None),
         ("Գըի · ընթացիկ իրացվելիություն", "(cash+cfi+rec+inv)/(pay+loan)", 3, 1, 2), ("ԸԻ · ընթացիկ իրացվելիություն (գումար)", "(cash+cfi+rec)-(pay+loan)", 0, 0, None),
         ("ՀԻ · հեռանկարային իրացվելիություն", "inv-ltl", 0, 0, None), ("Ա1 ≥ Պ1", "(cash+cfi)-pay", 0, 0, None), ("Ա2 ≥ Պ2", "rec-loan", 0, 0, None),
         ("Ա3 ≥ Պ3", "inv-ltl", 0, 0, None), ("Ա4 ≤ Պ4", "eq-noa", 0, 0, None)]),
 3: dict(title="Ֆինանսական կայունության գործակիցներ (հազ. դրամ)",
   inputs=[("noa", "Ոչ ընթացիկ ակտիվներ", 100000), ("inv", "Պաշարներ", 71500), ("ca", "Ընթացիկ ակտիվներ (ընդամենը)", 160000), ("eq", "Սեփական կապիտալ", 140000),
           ("ltl", "Ոչ ընթացիկ պարտավորություններ", 35790), ("cl", "Ընթացիկ պարտավորություններ", 84210)],
   outs=[("ՍԸԱ · սեփական ընթացիկ ակտիվներ", "eq+ltl-noa", 0, 0, None), ("Գսըա · ապահովվածություն ՍԸԱ-ով", "(eq+ltl-noa)/ca", 3, 0.1, None),
         ("Գպ · պաշարների ապահովվածություն", "(eq+ltl-noa)/inv", 3, 0.6, 0.8), ("Գանկ · անկախություն", "eq/(noa+ca)", 3, 0.5, None),
         ("Գկախ · կախվածություն", "(ltl+cl)/(noa+ca)", 3, None, 0.5), ("Գֆռ · ֆինանսական ռիսկ", "(ltl+cl)/eq", 3, None, 1),
         ("Գկայ · կայունություն", "(eq+ltl)/(noa+ca)", 3, 0.6, None), ("Կայունության պաշար", "eq+ltl-noa-inv", 0, 0, None)]),
 4: dict(title="Հիմնական միջոցների ցուցանիշներ (հազ. դրամ)",
   inputs=[("fa", "ՀՄ միջին տարեկան արժեք", 250000), ("rev", "Հասույթ", 13000000), ("np", "Զուտ շահույթ", 950000), ("emp", "Աշխատողների թիվ", 30), ("mach", "Մեքենասարքավորումներ", 55000),
           ("fin", "ՀՄ մուտք", 60000), ("fout", "ՀՄ ելք", 40000), ("fb", "ՀՄ տարեսկզբին", 300000), ("fe", "ՀՄ տարեվերջին", 340000), ("depb", "Մաշվածություն տարեսկզբին", 100000)],
   outs=[("ՖՀ · ֆոնդահատույց", "rev/fa", 2, None, None), ("ՖՏ · ֆոնդատարություն", "fa/rev", 4, None, None), ("Գազ · աշխատանքի զինվածություն", "fa/emp", 2, None, None),
         ("Գտզ · տեխնիկական զինվածություն", "mach/emp", 2, None, None), ("Գնոր · նորացում", "fin/fe", 3, None, None), ("Գդգ · դուրսգրում", "fout/fb", 3, None, None),
         ("Գմշ · մաշվածություն", "depb/fb", 3, None, 0.5), ("Գպիտ · պիտանելիություն", "1-depb/fb", 3, 0.5, None), ("ՇԲԹ · ՀՄ շահութաբերություն, %", "np/fa*100", 2, None, None)]),
 5: dict(title="Նյութական պաշարների ցուցանիշներ (հազ. դրամ)",
   inputs=[("mc", "Նյութական ծախսեր (Նծ)", 5691120), ("out", "Արտադրանքի ծավալ (Ա)", 9360000), ("pr", "Շահույթ (Շ)", 870000), ("mc0", "Նյութատարություն՝ նախորդ տարի", 0.6594)],
   outs=[("ՆՏ · նյութատարություն", "mc/out", 4, None, None), ("ՆՀ · նյութահատույց", "out/mc", 4, None, None), ("ՇԲԹՆԾ · նյութական ծախսերի շահութաբերություն, %", "pr/mc*100", 2, None, None),
         ("ՇԲԹԱ · արտադրանքի շահութաբերություն, %", "pr/out*100", 2, None, None), ("ΔՆՏ", "mc/out-mc0", 4, None, 0), ("±ΔԻ(ՆՏ) · ազդեցությունն ինքնարժեքի վրա", "(mc/out-mc0)*out", 0, None, 0)]),
 6: dict(title="Աշխատանքային ռեսուրսների ցուցանիշներ",
   inputs=[("emp", "Միջին ցուցակային թիվ (Քա)", 231), ("out", "Արտադրանք, հազ. դրամ (Ա)", 5789100), ("days", "1 աշխատողի օրեր (Օ)", 225), ("hrs", "Օրվա տևողություն, ժ (Ժ)", 7.83),
           ("hired", "Ընդունված աշխատողներ", 20), ("left", "Ազատված աշխատողներ", 15), ("leftv", "Ազատված՝ սեփ. կամքով և խախտումով", 10), ("w0", "ԱՖ նախորդ տարի", 640140), ("w1", "ԱՖ հաշվետու տարի", 711500), ("idx", "Արտադրանքի կատարում, %", 110.8)],
   outs=[("ԱԱ · արտադրողականություն, հազ. դր.", "out/emp", 2, None, None), ("Ֆ · աշխ. ժամանակի ֆոնդ, ժ", "emp*days*hrs", 0, None, None), ("ԺԱ · ժամային արտադրանք, դրամ", "out*1000/(emp*days*hrs)", 2, None, None),
         ("Գընդ · ընդունման գործակից", "hired/emp", 3, None, None), ("Գազ · ազատման գործակից", "left/emp", 3, None, None), ("Գհոս · հոսունություն", "leftv/emp", 3, None, 0.05),
         ("ԱՖ հարաբերական շեղում (− տնտեսում)", "w1-w0*idx/100", 0, None, 0)]),
 7: dict(title="Դրամական միջոցների ցուցանիշներ (հազ. դրամ)",
   inputs=[("inT", "ԴՄ մուտք (ընդամենը)", 3200000), ("outT", "ԴՄ ելք (ընդամենը)", 3050000), ("inO", "Մուտք՝ գործառնական", 2900000), ("outO", "Ելք՝ գործառնական", 2600000),
           ("c0", "ԴՄ տարեսկզբին", 180000), ("c1", "ԴՄ տարեվերջին", 330000), ("rev", "Հասույթ", 3400000)],
   outs=[("ԶԴՀ · զուտ դրամական հոսք", "inT-outT", 0, 0, None), ("ԳԸՎ · ընթացիկ վճարունակություն", "inO/outO", 3, 1, None), ("ԱՊդմ · ապահովվածություն դրամով, օր", "((c0+c1)/2)/(outO/360)", 1, None, None),
         ("ՇՐՋ · ԴՄ շրջանառելիություն", "rev/((c0+c1)/2)", 2, None, None), ("Մեկ պտույտի տևողություն, օր", "360/(rev/((c0+c1)/2))", 1, None, None)]),
 8: dict(title="Դեբիտորական և կրեդիտորական պարտքեր (հազ. դրամ)",
   inputs=[("rev", "Իրացումից հասույթ (ԻՀ)", 14000000), ("r0", "ԴՊ տարեսկզբին", 540000), ("r1", "ԴՊ տարեվերջին", 1215000), ("risk", "Ռիսկային ԴՊ", 105000),
           ("cogs", "Ինքնարժեք / գնումներ (Հ)", 9000000), ("p0", "ԿՊ տարեսկզբին", 700000), ("p1", "ԿՊ տարեվերջին", 650000), ("od", "Ժամկետանց ԿՊ", 40000)],
   outs=[("ՇՐՋդպ · ԴՊ շրջանառելիություն", "rev/((r0+r1)/2)", 2, None, None), ("Tօր · ԴՊ պտույտ, օր", "360/(rev/((r0+r1)/2))", 1, None, None), ("Գռդպ · ռիսկային ԴՊ կշիռ", "risk/r1", 3, None, 0.1),
         ("ՇՐՋկպ · ԿՊ շրջանառելիություն", "cogs/((p0+p1)/2)", 2, None, None), ("ԿՊ պտույտ, օր", "360/(cogs/((p0+p1)/2))", 1, None, None),
         ("ՏԿժ.անց · ժամկետանց ԿՊ, %", "od/p1*100", 2, None, 10), ("Գդկհ · ԴՊ ÷ ԿՊ", "r1/p1", 3, 0.9, 1.1)]),
}

def quiz_data():
    out = []
    for L in LESSONS:
        out.append(dict(n=L["n"], f=[[strip(c), name, strip(fx), m] for c, name, fx, m, d in L["formulas"]], g=[list(x) for x in L["glossary"]]))
    return out

def data_js():
    lessons = [dict(n=L["n"], slug=L["slug"], t=L["t"], short=L["short"], img=L["img"], acc=L["acc"], date=L["date"], idea=L["idea"]) for L in LESSONS]
    files = []
    lab = {L["mat"]: f'Դաս {L["n"]}' for L in LESSONS}; lab["mid"] = "1-ին միջանկյալ"
    for m, lst in FILES.items():
        for f, t, k in lst: files.append([t, f"materials/{m}/{f}", lab[m]])
    for L in LESSONS: files.append([f"✨ H/R ներկայացում · Դաս {L['n']}", f"materials/{L['mat']}/HR_Das{L['n']}_prezentacia.pptx", f"Դաս {L['n']}"]); files.append([f"✨ H/R կոնսպեկտ (PDF) · Դաս {L['n']}", f"materials/{L['mat']}/HR_Das{L['n']}_konspekt.pdf", f"Դաս {L['n']}"])
    works = [[w["t"], it[1], it[2], w["l"]] for w in gen2.WORKS for it in w["items"]]
    tips = {}
    for L in LESSONS:
        for c, name, fx, m, d in L["formulas"]:
            k = strip(c)
            if len(k) >= 2 and k not in ("Մոդել",) and k not in tips: tips[k] = f"{name} · {strip(fx)}"
        for t, d in L["glossary"]:
            if len(t) >= 2 and t not in tips: tips[t] = d
    D = dict(lessons=lessons, files=files, works=works, quiz=quiz_data(), tips=tips, calc={k: dict(t=v["title"], i=v["inputs"], o=v["outs"]) for k, v in CALC.items()})
    return "window.HRD=" + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";"

# ---------------- lesson sections ----------------
def explainer(L):
    f = L["formulas"]; f0 = f[0]; f1 = f[1] if len(f) > 1 else f[0]
    pts = "".join(f'<li style="--i:{i}"><b>{E(a)}</b><span>{E(b)}</span></li>' for i, (a, b) in enumerate(L["points"][:4]))
    parts = re.split(r"(\s[=÷×−+]\s|\s→\s)", strip(f0[2]))
    fx = "".join(f'<span class="fp" style="--i:{i}">{E(p)}</span>' for i, p in enumerate(parts) if p)
    bars = "".join(f'<i style="--h:{h}%;--i:{i}"></i>' for i, h in enumerate([38, 62, 47, 80, 66, 92]))
    return f'''<section class="sec" id="explain"><div class="wrap"><div class="kick rv">Անիմացիոն բացատրություն · ~25 վրկ</div><h2 class="rv">Դասը՝ 25 վայրկյանում</h2>
<div class="exp rv" data-exp><div class="exs">
<div class="sc on"><div class="exbg" style="background-image:url('assets/gen/{L["img"]}.jpg')"></div><div class="exc"><span class="exn">ԴԱՍ {L["n"]:02d}</span><h3>{E(L["t"])}</h3></div></div>
<div class="sc"><div class="exc c2"><span class="exi">💡</span><p class="big">{E(L["idea"])}</p></div></div>
<div class="sc"><div class="exc c3"><span class="exi">🧭</span><p>{E(L["analogy"])}</p><div class="exbars">{bars}</div></div></div>
<div class="sc"><div class="exc c4"><h4>Գլխավորը</h4><ul class="expts">{pts}</ul></div></div>
<div class="sc"><div class="exc c5"><span class="fcode">{E(strip(f0[0]))}</span><div class="fx">{fx}</div><p>{E(f0[1])}՝ {E(f0[3])}</p></div></div>
<div class="sc"><div class="exc c6"><span class="exi">✅</span><h3>Հիշիր</h3><p><b>{E(strip(f1[0]))}</b> · {E(f1[1])}՝ {E(f1[3])}</p><a class="btn" href="#calc">Փորձել հաշվիչով →</a></div></div>
</div><div class="exbar"><button class="expl" aria-label="Դադար">❚❚</button><div class="exprog">{"<i><b></b></i>" * 6}</div><button class="exrp" aria-label="Կրկնել">↻</button></div></div></div></section>'''

def calc_html(n):
    c = CALC[n]
    ins = "".join(f'<label class="ci"><span>{E(lbl)}</span><input type="number" step="any" data-k="{k}" value="{v}"></label>' for k, lbl, v in c["inputs"])
    return f'''<section class="sec" id="calc"><div class="wrap"><div class="kick rv">Ինտերակտիվ</div><h2 class="rv">Հաշվիչ</h2><p class="sd rv">{E(c["title"])}։ Մուտքագրեք ձեր տվյալները (օրինակ՝ ձեր տարբերակից)՝ արդյունքները, նորմայի ստուգումը և եզրակացությունը կթարմանան անմիջապես։</p>
<div class="calc rv" data-calc="{n}"><div class="cins">{ins}<div class="cbtns"><button class="btn gh" data-reset>↺ Օրինակային տվյալներ</button><button class="btn gh" data-copy>⧉ Պատճենել եզրակացությունը</button></div></div>
<div class="couts"><div class="cres"></div><div class="cconc"></div></div></div></div></section>'''

def quiz_html(n):
    return f'''<section class="sec" id="quiz"><div class="wrap"><div class="kick rv">Ստուգիր քեզ</div><h2 class="rv">Թեստ և քարտեր</h2>
<div class="qz rv" data-quiz="{n}"><div class="qtabs"><button class="on" data-qm="test">📝 Թեստ</button><button data-qm="cards">🃏 Քարտեր</button><span class="qbest"></span></div><div class="qbody"></div></div></div></section>'''

def done_btn(n):
    return f'<div class="donebar"><div class="wrap"><button class="donebtn" data-done="{n}"><span class="ck">✓</span><span class="tx">Նշել որպես կարդացած</span></button></div></div>'

def patch_lesson(L):
    p = os.path.join(SITE, L["slug"] + ".html"); s = open(p, encoding="utf8").read()
    n = L["n"]
    ins = explainer(L) + calc_html(n) + quiz_html(n)
    s = s.replace('<section class="sec" id="glossary"', '<section class="sec" id="glossary"', 1)
    i = s.find('<section class="sec" id="glossary"'); j = s.find('</section>', i) + len('</section>')
    s = s[:j] + ins + s[j:]
    s = s.replace('<a href="#glossary">Բառարան</a>', '<a href="#glossary">Բառարան</a><a href="#explain">Անիմացիա</a><a href="#calc">Հաշվիչ</a><a href="#quiz">Թեստ</a>', 1)
    s = s.replace("</footer>", "</footer>", 1)
    s = re.sub(r'(<footer class="ftr")', done_btn(n) + r"\1", s, count=1)
    s = s.replace("<body>", f'<body data-lesson="{n}">', 1)
    open(p, "w", encoding="utf8").write(s)

# ---------------- index: carousel + progress ----------------
def carousel():
    cards = "".join(f'<a class="c3d" href="{L["slug"]}.html" style="--i:{i};--a:{L["acc"]}"><img src="assets/gen/{L["img"]}_s.jpg" alt="" loading="lazy"><span class="cn">ԴԱՍ {L["n"]:02d}</span><b>{E(L["short"])}</b><em class="cdone">✓</em></a>' for i, L in enumerate(LESSONS))
    return f'''<section class="sec car3"><div class="wrap"><div class="kick rv">Ընտրիր դասը</div><h2 class="rv">Դասերի կարուսել</h2><p class="sd rv">Քաշիր մկնիկով կամ մատով, սեղմիր քարտի վրա՝ դասը բացելու համար։</p></div>
<div class="ring-wrap" data-ring><div class="ring" style="--n:{len(LESSONS)}">{cards}</div><button class="rnav pv" aria-label="Նախորդ">‹</button><button class="rnav nx" aria-label="Հաջորդ">›</button></div>
<div class="wrap"><div class="cprog rv"><div><b>Իմ առաջընթացը</b><small><span data-prog-n>0</span> / {len(LESSONS)} դաս կարդացած · թեստերի միջին՝ <span data-quiz-avg>—</span></small></div><div class="pbar"><i data-prog-bar></i></div></div></div></section>'''

def patch_index():
    p = os.path.join(SITE, "index.html"); s = open(p, encoding="utf8").read()
    s = re.sub(r'(<section class="sec[^"]*" id="lessons")', lambda m: carousel() + m.group(1), s, count=1)
    open(p, "w", encoding="utf8").write(s)

# ---------------- works: timeline ----------------
TL = [("18.09.2026", "Դասեր 2–3", "Իրացվելիություն և կայունություն", "Ֆինանսական թերթ", "#b5452b", "assets/hw/paper/12_s.jpg", "hw/dasi-2-3/index.html"),
      ("25.09.2026", "Դաս 4", "Հիմնական միջոցներ", "Ինժեներական գծագիր", "#1e88e5", "assets/hw/blue/09_s.jpg", "hw/dasi-4/index.html"),
      ("03.10.2026", "Դաս 5", "Նյութական պաշարներ", "Շվեյցարական պաստառ", "#e30613", "assets/hw/swiss/09_s.jpg", "hw/dasi-5/index.html"),
      ("10.10.2026", "Դաս 6", "Աշխատանքային ռեսուրսներ", "Դպրոցական տետր", "#6a4c93", "assets/hw/note/09_s.jpg", "hw/dasi-6/index.html"),
      ("27.10.2026", "1-ին միջանկյալ", "5 խնդիր · մատյան № 5", "Liquid glass դաշբորդ", "#d4ff3a", "assets/hw/mij/06_s.jpg", "hw/mijankyal/index.html"),
      ("08.11.2026", "Դաս 7", "Դրամական միջոցներ", "Նեոնային ներկայացում", "#3dff8f", "assets/gen/cashflow_s.jpg", "t7/index.html"),
      ("14.11.2026", "Դաս 8", "Դեբիտորական և կրեդիտորական պարտքեր", "Կինեմատոգրաֆիկ ներկայացում", "#5cd6ff", "assets/gen/handshake_s.jpg", "t8/index.html")]
def timeline():
    it = "".join(f'''<a class="tli rv {'r' if i % 2 else 'l'}" href="{h}" style="--c:{c}"><span class="tdot"></span><div class="tcard"><img src="{im}" alt="" loading="lazy"><div><small>{E(d)} · {E(l)}</small><b>{E(t)}</b><em>🎨 {E(st)}</em></div></div></a>''' for i, (d, l, t, st, c, im, h) in enumerate(TL))
    return f'<section class="sec"><div class="wrap"><div class="kick rv">Ժամանակագրություն</div><h2 class="rv">Իմ ճանապարհը առարկայում</h2><p class="sd rv">Յուրաքանչյուր աշխատանք արված է իր ժամանակին և իր ոճով։</p><div class="tline"><i class="tax"></i>{it}</div></div></section>'
def patch_works():
    p = os.path.join(SITE, "works.html"); s = open(p, encoding="utf8").read()
    s = s.replace('<section class="sec"><div class="wrap"><div class="wkgrid">', timeline() + '<section class="sec"><div class="wrap"><div class="wkgrid">', 1)
    open(p, "w", encoding="utf8").write(s)

# ---------------- formulas cheat-sheet ----------------
def build_formulas():
    if not hasattr(gen, "footer_orig"): gen.footer_orig = gen.footer
    blocks = ""
    for L in LESSONS:
        rows = "".join(f'''<div class="fcard" data-s="{E((strip(c)+' '+name+' '+strip(fx)+' '+m).lower())}"><div class="fh"><code>{c}</code><b>{E(name)}</b><button class="cp" data-cp="{E(strip(c)+' = '+strip(fx))}" aria-label="Պատճենել">⧉</button></div><div class="ff">{fx}</div><p>{E(m)}</p></div>''' for c, name, fx, m, d in L["formulas"])
        blocks += f'<section class="fles" style="--a:{L["acc"]}"><h2><span>Դաս {L["n"]}</span>{E(L["t"])} <a href="{L["slug"]}.html">→</a></h2><div class="fgrid">{rows}</div></section>'
    body = f'''{gen2.header('formulas')}
<section class="hero2" style="min-height:min(420px,60vh)"><div class="bgi" style="background-image:url('assets/gen/analysis.jpg')"></div><i class="orb a"></i><i class="orb b"></i>
<div class="wrap" style="grid-template-columns:1fr"><div><div class="kick">Ծալովի թերթիկ · A4</div><h1>{gen2.words("Բանաձևերի շպարգալկա")}</h1><p class="lead">Բոլոր {sum(len(L["formulas"]) for L in LESSONS)} բանաձևերը՝ ըստ դասերի։ Որոնեք նշանով կամ անունով, պատճենեք մեկ սեղմումով, տպեք մեկ A4 էջի վրա։</p>
<div class="ctas"><input class="fsrch" id="fsrch" placeholder="🔍  Որոնել՝ ՇԲԹ, իրացվելիություն, ÷ …" autocomplete="off"><button class="btn" onclick="print()">🖨 Տպել</button></div></div></div></section>
<div class="wrap fsheet"><div class="phead">H/R Studios · {E(COURSE)} · բանաձևերի թերթիկ · Հրաչյա Ասլանյան, ԻՏ-447</div>{blocks}</div>
{gen2.footer()}{gen.JS}{gen2.JS2}<script>(function(){{const q=document.getElementById('fsrch');q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();document.querySelectorAll('.fcard').forEach(c=>c.style.display=!v||c.dataset.s.includes(v)?'':'none');document.querySelectorAll('.fles').forEach(s=>s.style.display=[...s.querySelectorAll('.fcard')].some(c=>c.style.display!=='none')?'':'none')}});
document.querySelectorAll('[data-cp]').forEach(b=>b.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(b.dataset.cp);b.textContent='✓';setTimeout(()=>b.textContent='⧉',1200)}})}})();</script></body></html>'''
    if gen2.CSS2 not in gen.CSS: gen.CSS += gen2.CSS2
    gen.footer_orig = getattr(gen, "footer_orig", gen.footer)
    open(os.path.join(SITE, "formulas.html"), "w", encoding="utf8").write(gen.head("Բանաձևերի շպարգալկա · H/R Studios", "Բոլոր բանաձևերը մեկ էջում") + body)

# ---------------- inject assets into every page ----------------
def inject(path, base):
    s = open(path, encoding="utf8").read()
    if "hr-extra.js" in s: return
    tag = f'<link rel="stylesheet" href="{base}assets/hr-extra.css">' + ('' if base else '<script>try{var t=localStorage.getItem("hr-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>')
    s = s.replace("</head>", tag + "</head>", 1)
    s = s.replace("</body>", f'<script src="{base}assets/hr-data.js" defer></script><script src="{base}assets/hr-extra.js" data-base="{base}" defer></script></body>', 1)
    # nav link to cheat-sheet (main-site header only)
    s = s.replace('<a href="index.html#how"', '<a href="formulas.html">Բանաձևեր</a><a href="index.html#how"', 1)
    s = s.replace('<span class="tag">Շուտով՝ դասեր 1–6-ի լուծումները</span>', '<span class="tag">7 աշխատանք</span>')
    open(path, "w", encoding="utf8").write(s)

def main():
    shutil.copy(os.path.join(GEN, "extras.css"), os.path.join(SITE, "assets", "hr-extra.css"))
    shutil.copy(os.path.join(GEN, "extras.js"), os.path.join(SITE, "assets", "hr-extra.js"))
    open(os.path.join(SITE, "assets", "hr-data.js"), "w", encoding="utf8").write(data_js())
    for L in LESSONS: patch_lesson(L)
    patch_index(); patch_works(); build_formulas()
    for f in os.listdir(SITE):
        if f.endswith(".html") and f != "404.html": inject(os.path.join(SITE, f), "")
    for d in os.listdir(os.path.join(SITE, "hw")):
        p = os.path.join(SITE, "hw", d, "index.html")
        if os.path.exists(p): inject(p, "../../")
    print("extras ok")

if __name__ == "__main__":
    main()
