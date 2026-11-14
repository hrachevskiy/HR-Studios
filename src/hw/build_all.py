# -*- coding: utf-8 -*-
"""Builds the Excel workbooks for homeworks 2-3, 4, 5, 6 and the midterm (journal number 5).
Two passes: build -> recalc -> read values -> rebuild with conclusions -> recalc."""
import sys, json, subprocess, glob, openpyxl
from openpyxl.styles import Alignment, PatternFill
import hwlib as H
AUTHOR = sys.argv[1] if len(sys.argv) > 1 else "Հրաչյա Ասլանյան"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else "out"
RECALC = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
J = 5  # journal number for the midterm

BAL = dict(noa=100000, inv=71500, rec=60500, cfi=8000, cash=20000, eq=140000, ltl=35790, pay=60800, loan=23410, scen=(30000, 15000, 15000), reinv=20000, equip=40000)
add = 10000 * J
BALM = dict(noa=200000 + add, inv=71500 + add, rec=60500 + add, cfi=8000, cash=20000 + add, eq=190000 + add, ltl=85790 + add, pay=60800 + add, loan=23410 + add,
            scen=(42000, 25000, 17000), reinv=20000, equip=40000,
            src=f"Մատյանի №{J}. դեղին նշված 8 հոդվածին գումարվել է {add:,} (4 ակտիվ + 4 պասիվ), հաշվեկշիռը մնում է հավասարակշռված։")
FA = {"ՀՄ": (200000, 250000), "ՀՄտս": (300000, 300000), "ԿՄտս": (80000, 100000), "ՀՄմուտք": (30000, 60000), "ՀՄելք": (50000, 40000), "ՀՄտվ": (300000, 340000),
      "ԿՄտվ": (60000, 80000), "ՀՄդ.մաշվ": (40000, 50000), "ՄՍ": (50000, 55000), "Հ": (10000000, 13000000), "ԶՇ": (800000, 950000), "Քա": (30, 30), "Ա": (8000000, 9360000)}
FAM = {k: ((a + add, b + add) if k != "Քա" else (a, b)) for k, (a, b) in FA.items()}
MAT = dict(years=("2020", "2021"), mats=[(5, 300, 5, 320), (20, 2000, 18, 2000), (10, 1000, 10, 800), (3, 50, 3, 70), (8, 100, 10, 120), (50, 2, 52, 3), (50, 4, 52, 5)],
           prod=(100, 80000, 120, 78000), profit=(650000, 870000))
a2 = 100 * J
MATM = dict(years=("2020", "2021"), mats=[(4, 300 + a2, 5, 320 + a2), (30, 2000 + a2, 25, 2000 + a2), (15, 1000 + a2, 20, 800 + a2), (3, 50 + a2, 3, 70 + a2), (7, 100 + a2, 10, 120 + a2),
           (40, 2 + a2, 50, 3 + a2), (55, 4 + a2, 62, 5 + a2)], prod=(100, 80000 + a2, 120, 78000 + a2), profit=(540000 + a2, 750000 + a2))
NP2 = dict(rows=[("«Ա»", 700, 0.5, 1600, 1800, 820, 0.6, 930, 5060), ("«Բ»", 950, 0.7, 950, 980, 930, 0.4, 1100, 4500), ("«Գ»", 1300, 0.3, 820, 1320, 1600, 0.5, 730, 3200)])
LAB = {"ԸԱ": (227, 231), "Թ": (192, 198), "Օ": (223, 225), "Ժ": (7.88, 7.83), "ՍԱ": (5223050, 5789100), "Հ": (5108200, 5526500), "ԶՇ": (1072000, 1271100),
       "ԱՖ": (640140, 711500), "Կ": (730600, 930000), "ԿՇ": (420000, 230000)}
small = 10 * J
LABM = {k: ((a + small, b + small) if k in ("ԸԱ", "Թ", "Օ") else (a, b) if k == "Ժ" else (a + add, b + add)) for k, (a, b) in LAB.items()}

def recalc(p):
    r = json.loads(subprocess.run(["python3", RECALC, p, "90"], capture_output=True, text=True).stdout)
    assert r.get("status") == "success", (p, r); return r["total_formulas"]
def vals(p):
    wb = openpyxl.load_workbook(p, data_only=True); return {ws.title: ws for ws in wb.worksheets}
f0 = lambda v, d=0: f"{v:,.{d}f}"
f3 = lambda v: f"{v:.3f}"
sg = lambda v, d=2: ("+" if v > 0 else "") + f"{v:,.{d}f}"

# ---------- conclusion writers ----------
def concl_liq(V, sh="Իրացվելիություն", q=None):
    w = V[sh]; ok = [str(w[f"H{r}"].value).startswith("✔") for r in range(6, 10)]
    bad = [f"Ա{i+1}–Պ{i+1}" for i, o in enumerate(ok) if not o]
    t = (f"Առավել իրացվելի ակտիվները {f0(w['C6'].value)} են, հրատապ պարտավորությունները՝ {f0(w['F6'].value)} (տարբերություն {sg(w['G6'].value,0)}). "
         f"Արագ իրացվելի ակտիվներ {f0(w['C7'].value)} ↔ կարճաժամկետ պարտավորություններ {f0(w['F7'].value)} ({sg(w['G7'].value,0)}). "
         f"Դանդաղ իրացվելի {f0(w['C8'].value)} ↔ երկարաժամկետ {f0(w['F8'].value)} ({sg(w['G8'].value,0)}). Դժվար իրացվելի {f0(w['C9'].value)} ↔ մշտական պասիվներ {f0(w['F9'].value)} ({sg(w['G9'].value,0)}). ")
    t += ("Բոլոր չորս պայմանները կատարվում են՝ հաշվեկշիռը բացարձակ իրացվելի է։ " if not bad else f"Խախտված է {', '.join(bad)} {'պայմանը' if len(bad)==1 else 'պայմանները'}, ուստի հաշվեկշիռը բացարձակ իրացվելի չէ։ ")
    t += (f"Ընթացիկ իրացվելիությունը {sg(w['F14'].value,0)} է, հեռանկարայինը՝ {sg(w['F15'].value,0)}։ Գործակիցներ՝ բացարձակ {f3(w['F16'].value)} ({w['H16'].value[2:]}), "
          f"արագ {f3(w['F17'].value)} ({w['H17'].value[2:]}), ընթացիկ {f3(w['F18'].value)} ({w['H18'].value[2:]})։")
    s = (f"Հարց 9. պաշարներ գնելուց հետո դրամական միջոցները կլինեն {f0(w['F22'].value)}, կրեդիտորական պարտքը՝ {f0(w['F24'].value)}։ "
         f"Բացարձակ իրացվելիությունը {f3(w['C27'].value)} → {f3(w['F27'].value)}, արագը՝ {f3(w['C28'].value)} → {f3(w['F28'].value)}, ընթացիկը՝ {f3(w['C29'].value)} → {f3(w['F29'].value)}։ "
         "Ամենաշատը տուժում է բացարձակ իրացվելիությունը, քանի որ «կենդանի» փողը վերածվում է պահեստում ընկած պաշարի։ Ռիսկ՝ հրատապ պարտքերը ժամանակին չվճարելու հավանականությունը մեծանում է։")
    return t, s
def concl_stab(V, sh="Կայունություն"):
    w = V[sh]
    t = (f"Սեփական ընթացիկ ակտիվները {f0(w['D6'].value)} են։ Դրանք ծածկում են ընթացիկ ակտիվների {w['D7'].value*100:.1f}%-ը ({f3(w['D7'].value)}) իսկ պաշարների ապահովվածությունը՝ {f3(w['D8'].value)}։ "
         f"Անկախության գործակիցը {f3(w['D9'].value)} է, կախվածությունը՝ {f3(w['D10'].value)}, ֆինանսական ռիսկը՝ {f3(w['D11'].value)} ({w['F11'].value[2:]})։ "
         f"Կայունության պաշարը {sg(w['D12'].value,0)} է ({sg(w['D13'].value,1)}% պաշարների նկատմամբ), կայունության գործակիցը՝ {f3(w['D14'].value)}։ Տեսակը՝ {w['C16'].value}։")
    s = (f"Սցենարներ. Ա (շահույթի վերաներդրում) → Գկայ {f3(w['D19'].value)}, Գֆռ {f3(w['E19'].value)}; Բ (վարկի երկարաձգում) → {f3(w['D20'].value)} / {f3(w['E20'].value)}; "
         f"Գ (սարքավորում կարճաժամկետ վարկով) → {f3(w['D21'].value)} / {f3(w['E21'].value)}։ " + scen_txt(w))
    return t, s
def scen_txt(w):
    ok = [n for n, r in (("Ա", 19), ("Բ", 20), ("Գ", 21)) if str(w[f"F{r}"].value).startswith("✔")]
    bad = [n for n in "ԱԲԳ" if n not in ok]
    t = (f"{', '.join(ok)} {'սցենարն' if len(ok)==1 else 'սցենարներն'} ամրապնդում են կայունությունը" if ok else "Ոչ մի սցենար չի ամրապնդում կայունությունը")
    if bad: t += f", իսկ {', '.join(bad)}-ն թուլացնում է այն"
    return t + "։ Լավագույն ճանապարհը սեփական կապիտալի և երկարաժամկետ ֆինանսավորման մեծացումն է։"
def concl_fa(V, sh="Հիմնական միջոցներ"):
    w = V[sh]; d = lambda r: w[f"D{r}"].value; e = lambda r: w[f"E{r}"].value; f = lambda r: w[f"F{r}"].value
    sav = e(24)
    t = (f"Աշխատանքի զինվածությունն աճել է {f0(d(22),1)} → {f0(e(22),1)}, տեխնիկականը՝ {f0(d(23),1)} → {f0(e(23),1)} հազ. դր./աշխատող։ "
         f"Հիմնական միջոցների {'հարաբերական տնտեսումը' if sav < 0 else 'հարաբերական գերածախսը'} կազմել է {f0(abs(sav))} հազ. դր.՝ "
         f"{'ՀՄ-ն աճել է ավելի դանդաղ, քան արտադրանքը (լավ է)' if sav < 0 else 'ՀՄ-ն աճել է ավելի արագ, քան արտադրանքը'}։ "
         f"Նորացում {f3(d(25))} → {f3(e(25))}, դուրսգրում {f3(d(26))} → {f3(e(26))}; մաշվածություն տարեսկզբին {f3(d(27))} → {f3(e(27))}, տարեվերջին {f3(d(28))} → {f3(e(28))}։")
    s = (f"ՀՄ շահութաբերությունը փոխվել է {f0(d(31),2)}% → {f0(e(31),2)}% ({sg(f(31))} պ.պ.)։ Իրացման շահութաբերության ազդեցությունը {sg(f(34))} պ.պ. է, "
         f"ֆոնդահատույցինը ({f0(d(33),2)} → {f0(e(33),2)})՝ {sg(f(35))} պ.պ.։ Գործոնների գումարը ճշգրիտ հավասար է ընդհանուր փոփոխությանը։")
    return t, s
def concl_mat(V, sh="Նյութական պաշարներ"):
    w = V[sh]; e = lambda r: w[f"E{r}"].value; f = lambda r: w[f"F{r}"].value; g = lambda r: w[f"G{r}"].value
    t = (f"Միավոր արտադրանքի նյութական ծախսը {f0(w['E13'].value)} → {f0(w['H13'].value)}, ընդհանուր նյութական ծախսը՝ {f0(w['E15'].value)} → {f0(w['H15'].value)}։ "
         f"Նյութատարությունը {e(20):.4f} → {f(20):.4f} ({sg(g(20),4)}), նյութահատույցը՝ {e(23):.4f} → {f(23):.4f}։ "
         f"Նյութական ծախսերի շահութաբերությունը {e(21):.2f}% → {f(21):.2f}%, արտադրանքի շահութաբերությունը՝ {e(22):.2f}% → {f(22):.2f}%։")
    s = (f"ΔՇԲԹՆԾ = {sg(g(21))} պ.պ., որից արտադրանքի շահութաբերության հաշվին {sg(f(24))}, նյութահատույցի հաշվին {sg(f(25))}։ "
         f"Նյութատարության փոփոխությունն ինքնարժեքի վրա տվել է {sg(f(26),0)} հազ. դր. ({'տնտեսում' if f(26) < 0 else 'գերածախս'}), իսկ արտադրանքի ծավալի վրա՝ {sg(f(27),0)}։")
    return t, s
def concl_np2(V, sh="Նյութատարություն"):
    w = V[sh]; h = lambda r: w[f"H{r}"].value
    big = max([("տեսականու", h(20)), ("ծախսի նորմայի", h(21)), ("նյութի գնի", h(22)), ("արտադրանքի գնի", h(23))], key=lambda z: abs(z[1]))
    return (f"Նյութատարությունը {w['E19'].value:.4f} → {w['E23'].value:.4f} ({sg(w['E24'].value,4)})։ Ազդեցություններ՝ տեսականի {sg(h(20),4)}, ծախսի նորմա {sg(h(21),4)}, "
            f"նյութի գին {sg(h(22),4)}, արտադրանքի գին {sg(h(23),4)}։ Ամենաուժեղ գործոնը {big[0]} փոփոխությունն է։ Գործոնների գումարը հավասար է ընդհանուր շեղմանը։")
def concl_lab(V, sh="Աշխատանք"):
    w = V[sh]; d = lambda r: w[f"D{r}"].value; e = lambda r: w[f"E{r}"].value; f = lambda r: w[f"F{r}"].value
    t = (f"Աշխատաժամանակի ֆոնդը {f0(d(20),2)} → {f0(e(20),2)} ժամ ({sg(f(20))})։ Թվաքանակի հաշվին {sg(f(21))}, օրերի հաշվին {sg(f(22))}, օրվա տևողության հաշվին {sg(f(23))} ժամ։ "
         "Օրվա տևողության կրճատումը ներօրյա պարապուրդների նշան է։")
    s = (f"Ժամային արտադրողականությունն աճել է {f0(d(31),2)} → {f0(e(31),2)} դրամ։ Արդյունք ստեղծող 1 աշխատողի արդյունքը {f0(d(29),1)} → {f0(e(29),1)} հազ. դր.՝ "
         f"օրերի հաշվին {sg(f(34))}, օրվա տևողության հաշվին {sg(f(35))}, ժամային արտադրողականության հաշվին {sg(f(36))}։ "
         f"Անձնակազմի միավորի արդյունքը {f0(d(28),1)} → {f0(e(28),1)}՝ տեսակարար կշռի հաշվին {sg(f(39))}, օրերի {sg(f(40))}, տևողության {sg(f(41))}, արտադրողականության {sg(f(42))}։ "
         "Աճի հիմնական աղբյուրը ժամային արտադրողականությունն է։")
    return t, s

def put_note(ws, row, width, text, x):
    x.note(ws, row, text, width, h=max(60, 15 * (len(text) // 120 + 2)))

# ---------- builders ----------
def hw23(concl=None):
    x = H.X("paper", AUTHOR); B = H.balance_sheet(x, BAL, title="<<XXX>> ՍՊԸ · Հաշվեկշիռ 2025թ. (հազ. դրամ)")
    l = H.liquidity(x, B, BAL, title="Առաջադրանք 1 · Հաշվեկշռի իրացվելիություն և վճարունակություն"); s = H.stability(x, B, BAL, title="Առաջադրանք 2 · Ֆինանսական կայունություն")
    if concl:
        put_note(l, 31, 8, "Եզրակացություն. " + concl["liq"][0], x); put_note(l, 32, 8, concl["liq"][1], x); put_note(s, 23, 6, "Եզրակացություն. " + concl["stab"][0], x); put_note(s, 24, 6, concl["stab"][1], x)
        H.summary(x, [("Առաջադրանք 1 · Իրացվելիություն", concl["liq"][0]), ("Հարց 9 · Գործարքի ազդեցություն", concl["liq"][1]), ("Առաջադրանք 2 · Կայունություն", concl["stab"][0]), ("Սցենարներ", concl["stab"][1])])
    return x
def hw4(concl=None):
    x = H.X("blueprint", AUTHOR); w = H.fixed_assets(x, FA)
    if concl:
        put_note(w, 38, 7, "Եզրակացություն. " + concl["fa"][0], x); put_note(w, 39, 7, concl["fa"][1], x)
        H.summary(x, [("Ապահովվածություն և վիճակ", concl["fa"][0]), ("Արդյունավետություն", concl["fa"][1])])
    return x
def hw5(concl=None):
    x = H.X("swiss", AUTHOR); w = H.materials1(x, MAT, name="ՆՊ 1", title="Տնային 1 · Նյութական պաշարների օգտագործում"); w2 = H.materials2(x, NP2, name="ՆՊ 2", title="Տնային 2 · Նյութատարության գործոնային վերլուծություն")
    if concl:
        put_note(w, 30, 8, "Եզրակացություն. " + concl["mat"][0], x); put_note(w, 31, 8, concl["mat"][1], x); put_note(w2, 26, 9, "Եզրակացություն. " + concl["np2"], x)
        H.summary(x, [("Տնային 1 · ցուցանիշներ", concl["mat"][0]), ("Տնային 1 · գործոններ", concl["mat"][1]), ("Տնային 2 · շղթայական տեղադրում", concl["np2"])])
    return x
def hw6(concl=None):
    x = H.X("notebook", AUTHOR); w = H.labour(x, LAB)
    if concl:
        put_note(w, 52, 7, "Եզրակացություն 1. " + concl["lab"][0], x); put_note(w, 53, 7, "Եզրակացություն 2. " + concl["lab"][1], x)
        H.summary(x, [("Աշխատաժամանակի ֆոնդ", concl["lab"][0]), ("Աշխատանքի արտադրողականություն", concl["lab"][1])])
    return x
def mid(concl=None):
    x = H.X("gold", AUTHOR, course=f"ԻՏ-447 · Մատյանի № {J} · Դասախոս՝ Օ.Ա. Գալստյան")
    ws = x.sheet("Տվյալներ №5", f"1-ին միջանկյալ · Տվյալների փոփոխություն ըստ մատյանի № {J}", "Ինչ ենք ավելացրել դասախոսի դեղին նշված տվյալներին", [8, 60, 18])
    rules = [("Խնդիր 1–2", f"Հաշվեկշռի 8 դեղին հոդված + {add:,} (4 ակտիվ, 4 պասիվ, հաշվեկշիռը չի խախտվում)", f"+{add:,}"),
             ("Խնդիր 3", f"Հիմնական միջոցների բոլոր դեղին տվյալները + {add:,} (թվաքանակը՝ առանց փոփոխության)", f"+{add:,}"),
             ("Խնդիր 4", f"Նյութերի և արտադրանքի գները, շահույթը + {a2:,} (№ × 100)", f"+{a2:,}"),
             ("Խնդիր 5", f"Մեծ թվեր + {add:,}; փոքր թվեր (թվաքանակ, օրեր) + {small} (№ × 10). Ժամերն ու ֆոնդը վերահաշվարկված են բանաձևով", f"+{add:,} / +{small}")]
    x.head(ws, 5, ["Խնդիր", "Կանոն", "Գումարվող"])
    for i, rr in enumerate(rules): x.row(ws, 6 + i, list(rr), h=34)
    B = H.balance_sheet(x, BALM, name="Խ1-2 Հաշվեկշիռ", title=f"Խնդիր 1–2 · Հաշվեկշիռ (մատյան № {J})")
    l = H.liquidity(x, B, BALM, name="Խ1 Իրացվելիություն", title="Խնդիր 1 · Իրացվելիություն և վճարունակություն")
    s = H.stability(x, B, BALM, name="Խ2 Կայունություն", title="Խնդիր 2 · Ֆինանսական կայունություն")
    fa = H.fixed_assets(x, FAM, name="Խ3 ՀՄ", title="Խնդիր 3 · Հիմնական միջոցներ")
    m = H.materials1(x, MATM, name="Խ4 ՆՊ", title="Խնդիր 4 · Նյութական պաշարներ")
    lb = H.labour(x, LABM, name="Խ5 Աշխատանք", title="Խնդիր 5 · Աշխատաժամանակ և արտադրողականություն")
    if concl:
        put_note(l, 31, 8, "Եզրակացություն. " + concl["liq"][0], x); put_note(l, 32, 8, concl["liq"][1], x)
        put_note(s, 23, 6, "Եզրակացություն. " + concl["stab"][0], x); put_note(s, 24, 6, concl["stab"][1], x)
        put_note(fa, 38, 7, "Եզրակացություն. " + concl["fa"][0], x); put_note(fa, 39, 7, concl["fa"][1], x)
        put_note(m, 30, 8, "Եզրակացություն. " + concl["mat"][0], x); put_note(m, 31, 8, concl["mat"][1], x)
        put_note(lb, 52, 7, "Եզրակացություն 1. " + concl["lab"][0], x); put_note(lb, 53, 7, "Եզրակացություն 2. " + concl["lab"][1], x)
        H.summary(x, [("Խնդիր 1 · Իրացվելիություն", concl["liq"][0] + " " + concl["liq"][1]), ("Խնդիր 2 · Կայունություն", concl["stab"][0] + " " + concl["stab"][1]),
                      ("Խնդիր 3 · Հիմնական միջոցներ", concl["fa"][0] + " " + concl["fa"][1]), ("Խնդիր 4 · Նյութական պաշարներ", concl["mat"][0] + " " + concl["mat"][1]),
                      ("Խնդիր 5 · Աշխատանք", concl["lab"][0] + " " + concl["lab"][1])])
    return x

JOBS = {
  "hw23": (hw23, "Das2-3_Irachvelutyun_Kayunutyun", lambda V: dict(liq=concl_liq(V), stab=concl_stab(V))),
  "hw4": (hw4, "Das4_Himnakan_mijocner", lambda V: dict(fa=concl_fa(V))),
  "hw5": (hw5, "Das5_Nyutakan_pasharner", lambda V: dict(mat=concl_mat(V, "ՆՊ 1"), np2=concl_np2(V, "ՆՊ 2"))),
  "hw6": (hw6, "Das6_Ashkhatank", lambda V: dict(lab=concl_lab(V))),
  "mid": (mid, "Midterm1_Matyan5", lambda V: dict(liq=concl_liq(V, "Խ1 Իրացվելիություն"), stab=concl_stab(V, "Խ2 Կայունություն"), fa=concl_fa(V, "Խ3 ՀՄ"),
                                                   mat=concl_mat(V, "Խ4 ՆՊ"), lab=concl_lab(V, "Խ5 Աշխատանք"))),
}
if __name__ == "__main__":
    import os; os.makedirs(OUTDIR, exist_ok=True)
    which = sys.argv[3].split(",") if len(sys.argv) > 3 else list(JOBS)
    tag = sys.argv[4] if len(sys.argv) > 4 else "Hrachya_Aslanyan"
    for k in which:
        fn, base, cf = JOBS[k]; p = f"{OUTDIR}/{base}_{tag}.xlsx"
        fn().save(p); recalc(p); c = cf(vals(p))
        fn(c).save(p); n = recalc(p)
        json.dump(c, open(f"{OUTDIR}/{k}_concl.json", "w"), ensure_ascii=False, indent=1)
        print(k, p, n, "formulas OK")
