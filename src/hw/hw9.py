# -*- coding: utf-8 -*-
# Lesson 9 (teacher's topic 10) — financial liabilities. Theme: amber trading terminal.
import os, sys, openpyxl
sys.path.insert(0, os.path.dirname(__file__))
import hwpage as H
import hwpage2 as P
from hwpage import E, n, table, svg_pairs, svg_waterfall, SITE

XL = "Tema10_Finansakan_partavorutyunner_Hrachya_Aslanyan.xlsx"

CSS_TERM = r"""
html,body{overflow-x:clip}
body{background:#050505;color:#ffcf66;font-family:'IBM Plex Mono','Noto Sans Armenian',monospace;font-size:15px}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:150;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 1px,transparent 1px 3px);mix-blend-mode:multiply}
.am{color:#ffb000}.gn{color:#3dff8f}.rd{color:#ff5c5c}.cy{color:#5cd6ff}.wh{color:#f4ecd8}.dim{color:#a2864a}
.topbar{background:#0b0b0b;border-bottom:1px solid #ffb000;font-family:'Noto Sans Armenian'}.topbar a.b{border:1px solid #6b5520;color:#ffcf66}.topbar a.x{background:#ffb000;color:#000;border-color:#ffb000}
/* boot curtain */
.cur{background:#050505;place-items:start;padding:8vh 6vw}.boot{font:500 clamp(13px,1.6vw,17px)/1.9 'IBM Plex Mono','Noto Sans Armenian',monospace;color:#ffb000;white-space:pre}
.boot span{display:block;opacity:0;animation:bl .01s forwards}.boot span:nth-child(1){animation-delay:.1s}.boot span:nth-child(2){animation-delay:.35s}.boot span:nth-child(3){animation-delay:.6s}.boot span:nth-child(4){animation-delay:.85s}.boot span:nth-child(5){animation-delay:1.1s}.boot span:nth-child(6){animation-delay:1.35s}
.boot span:last-child::after{content:"█";animation:blink .8s steps(1) infinite}@keyframes bl{to{opacity:1}}@keyframes blink{50%{opacity:0}}
/* ticker */
.tick{position:sticky;top:0;z-index:40;overflow:hidden;background:#ffb000;color:#000;font:600 13px 'IBM Plex Mono','Noto Sans Armenian';white-space:nowrap;border-bottom:1px solid #000}
.tick .tt{display:inline-flex;gap:38px;padding:6px 0;animation:mq 40s linear infinite}.tick .tt b{font-weight:700}.tick i{font-style:normal}.tick .u{color:#004d1f}.tick .d{color:#8a0000}
/* hero */
.hero{min-height:92vh;align-items:center}.hero .hs img{filter:grayscale(1) sepia(1) hue-rotate(-12deg) saturate(2.2) brightness(.32) contrast(1.2)}
.hero::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,rgba(5,5,5,.96) 0%,rgba(5,5,5,.7) 55%,rgba(5,5,5,.3)),linear-gradient(180deg,transparent 70%,#050505)}
.hero .inner{max-width:1180px;margin:0 auto;padding:110px 20px 60px}
.prompt{font-size:13px;color:#a2864a;letter-spacing:.08em}.prompt b{color:#3dff8f;font-weight:500}
.hero h1{font:600 clamp(32px,5.4vw,76px)/1.05 'Noto Sans Armenian';color:#ffb000;margin:16px 0 18px;text-shadow:0 0 24px rgba(255,176,0,.35);letter-spacing:-.01em}
.hero p{max-width:640px;color:#e6d3a3;font:400 17px/1.75 'Noto Sans Armenian'}
.fkeys{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}.fkeys a{font:600 12.5px 'IBM Plex Mono','Noto Sans Armenian';text-decoration:none;color:#000;background:#ffb000;padding:7px 12px}.fkeys a i{font-style:normal;background:#000;color:#ffb000;padding:1px 5px;margin-right:7px}
.fkeys a:hover{background:#ffd36b}
/* screens */
.wrap9{max-width:1240px;margin:0 auto;padding:0 20px}
.kp9{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#3a2e12;border:1px solid #3a2e12;margin:-40px 0 50px;position:relative;z-index:4}
.k9{background:#0b0b0b;padding:18px 16px}.k9 small{display:block;color:#a2864a;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}.k9 b{display:block;font:600 clamp(24px,2.8vw,36px) 'IBM Plex Mono';color:#ffb000;margin:6px 0 2px}.k9 em{font-style:normal;font-size:13px}
.scr{border:1px solid #3a2e12;background:#0a0a0a;margin:0 0 26px}.scr>header{display:flex;justify-content:space-between;align-items:center;gap:10px;background:#1a1407;border-bottom:1px solid #3a2e12;padding:7px 12px;font:600 12.5px 'IBM Plex Mono','Noto Sans Armenian';color:#ffb000;letter-spacing:.06em;text-transform:uppercase}
.scr>header span{color:#a2864a;font-weight:500;text-transform:none;letter-spacing:0}.scr .bd{padding:16px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:22px}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
h2.h9{font:600 clamp(24px,3vw,38px) 'Noto Sans Armenian';color:#f4ecd8;margin:60px 0 6px}h2.h9 i{font-style:normal;color:#ffb000;font-family:'IBM Plex Mono';margin-right:12px}
.sub9{color:#bfa56a;font:400 15.5px/1.7 'Noto Sans Armenian';margin:0 0 22px;max-width:820px}
table{width:100%;border-collapse:collapse;font:400 14px 'IBM Plex Mono','Noto Sans Armenian';color:#ffcf66}
thead th{color:#000;background:#ffb000;font-weight:600;font-size:12px;text-align:right;padding:7px 9px;white-space:nowrap}thead th:first-child{text-align:left}
tbody td{padding:7px 9px;border-bottom:1px solid #221b0b;text-align:right;white-space:nowrap}tbody td:first-child{text-align:left;white-space:normal;color:#f0e2bd;font-family:'Noto Sans Armenian'}
tbody tr:hover{background:#1a1407}tbody tr.t td{color:#ffb000;font-weight:600;border-top:1px solid #6b5520}code{color:#5cd6ff;font-family:'IBM Plex Mono','Noto Sans Armenian'}
.tw{overflow-x:auto}.sb{margin:0 0 14px}.sbt{height:9px;background:#1a1407;margin-top:4px}.sbt i{display:block;height:100%;transform-origin:left;transform:scaleX(0);transition:transform 1.2s cubic-bezier(.2,.8,.2,1)}.sb.in .sbt i{transform:none}.sbt .s0{background:#6b5520}.sbt .s1{background:#ffb000}.scr svg.ch{max-height:420px}
.ch .s1{fill:#6b5520}.ch .s2,.ch .tot{fill:#ffb000}.ch .pos{fill:#3dff8f}.ch .neg{fill:#ff5c5c}.ch .ax,.ch .cn{stroke:#6b5520}.ch text{fill:#ffcf66;font-family:'IBM Plex Mono','Noto Sans Armenian'}
.gauge{margin:0 0 18px}.gl{display:flex;justify-content:space-between;font-family:'Noto Sans Armenian'}.gl b{color:#ffb000;font-family:'IBM Plex Mono'}
.gt{position:relative;height:12px;background:#1a1407;margin:8px 0 4px}.gt .zone{position:absolute;top:0;bottom:0;background:rgba(61,255,143,.35)}.gt .mk{position:absolute;top:-4px;width:3px;height:20px;background:#ffb000;box-shadow:0 0 10px #ffb000}
.gs{display:flex;justify-content:space-between;font-size:11.5px;color:#a2864a}
.log{font:400 14.5px/1.85 'IBM Plex Mono','Noto Sans Armenian';color:#e6d3a3}.log p{margin:0 0 10px;padding-left:22px;position:relative}.log p::before{content:">";position:absolute;left:0;color:#3dff8f}
.note{border-left:3px solid #5cd6ff;padding:10px 14px;background:#07131a;color:#bfe9ff;font:400 14px/1.7 'Noto Sans Armenian';margin-top:14px}
.chap{color:#ffb000}.chap .chi{filter:grayscale(1) sepia(1) hue-rotate(-12deg) saturate(2) brightness(.3)}.chap .chn{font-family:'IBM Plex Mono';text-shadow:0 0 30px rgba(255,176,0,.5)}.chap h2{font-family:'Noto Sans Armenian';color:#f4ecd8}
.mq{border-top:1px solid #3a2e12;border-bottom:1px solid #3a2e12;background:#0a0a0a}.mqt img{border-radius:0;filter:grayscale(1) sepia(1) hue-rotate(-12deg) saturate(1.6) brightness(.7)}.mqt img:hover{filter:none}
.foot{text-align:center;padding:40px 0 70px;color:#a2864a;font:500 12.5px 'IBM Plex Mono','Noto Sans Armenian';letter-spacing:.2em}
@media (max-width:600px){.hero h1{font-size:clamp(20px,6vw,34px);overflow-wrap:anywhere}.prompt{font-size:11px;word-break:break-all}.k9 b{font-size:22px}}
@media (max-width:900px){.kp9{grid-template-columns:1fr 1fr;margin-top:20px}.g2,.g3{grid-template-columns:1fr}.hero .inner{padding-top:80px}}
"""

def scr(title, sub, body):
    return f'<div class="scr rv"><header>{E(title)}<span>{E(sub)}</span></header><div class="bd">{body}</div></div>'

def build_hw9():
    wb = openpyxl.load_workbook(os.path.join(SITE, "files", XL), data_only=True); a, b = wb.worksheets[0], wb.worksheets[1]
    g = lambda ws, r, c: ws.cell(r, c).value
    E5 = lambda r: g(a, r, 5); F6 = lambda r: g(a, r, 6); G7 = lambda r: g(a, r, 7)
    # ---- movement table ----
    mv = []
    for lab, s, fo, rp in (("Ոչ ընթացիկ ՖՊ", 9, 15, 23), ("Ընթացիկ ՖՊ", 35, 44, 55)):
        for y, c in (("2024", 5), ("2025", 6)):
            mv.append([f"{E(lab)} · {y}", n(g(a, s, c)), "+" + n(g(a, fo, c)), "−" + n(g(a, rp, c)), f"<b>{n(g(a, 66 if s == 9 else 67, c))}</b>"])
    mvt = table(["Հոդված", "Տարեսկիզբ", "Ձևավորված", "Մարված / տեղափոխված", "Տարեվերջ"], mv)
    # waterfall total FP 2025: start, new external, repaid, end
    new25 = g(a, 15, 6) + g(a, 44, 6) - g(a, 85, 6)
    wf = svg_waterfall(("Սկիզբ 2025", g(a, 82, 6)), [("Նոր ՖՊ", new25), ("Մարված", -g(a, 84, 6))], ("Վերջ 2025", g(a, 83, 6)), 0)
    # ---- analysis ----
    rows = [(66, "Ոչ ընթացիկ ՖՊ (տարեվերջ)", "ՈԸՖՊ", 0, ""), (67, "Ընթացիկ ՖՊ (տարեվերջ)", "ԸՖՊ", 0, ""), (68, "ՖՊ միջին արժեք", "ՖՊ", 0, ""),
            (69, "Շրջանառելիություն, պտույտ", "ՇՐՋֆպ", 4, ""), (70, "Մեկ պտույտի տևողություն, օր", "Tօր", 1, ""),
            (71, "ԸՖՊ կշիռ ընթացիկ պարտավորություններում", "ՏԿֆպ", 2, "%"), (72, "Ժամկետանց ՖՊ կշիռ", "ՏԿժ.անց", 2, "%"),
            (73, "Բանկային վարկերի կշիռ", "ՏԿբվ", 2, "%"), (74, "ՖՊ շահութաբերություն", "ՇԲԹֆպ", 2, "%")]
    def v(x, d, pct, sign=False): return n(x * 100 if pct else x, d, sign) + ("%" if pct else "")
    an = [[E(t), f"<code>{E(c)}</code>", v(E5(r), d, p), v(F6(r), d, p), v(G7(r), d, p, True) + (" п.к." if False else "")] for r, t, c, d, p in rows]
    an += [["9.1 · ըստ ՖՊ արդյունավետության", "<code>±ΔՇԲԹ(ՖՊարդյ)</code>", "—", "—", v(G7(75), 2, "%", True)],
           ["9.2 · ըստ իրացման շահութաբերության", "<code>±ΔՇԲԹ(ՇԲԹիր)</code>", "—", "—", v(G7(76), 2, "%", True)]]
    ant = table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ"], an)
    fw = svg_waterfall(("ՇԲԹ 2024", E5(74) * 100), [("Հ/ՖՊ", G7(75) * 100), ("ԶՇ/Հ", G7(76) * 100)], ("ՇԲԹ 2025", F6(74) * 100), 2)
    days = svg_pairs(["Պտույտ, օր (փաստ.)", "Պտույտ, օր (ձևանմուշ)"], [E5(70), E5(94)], [F6(70), F6(94)], "2024", "2025", 0, 240)
    st = svg_pairs(["Ոչ ընթացիկ", "Ընթացիկ", "Բանկային վարկեր"], [E5(66), E5(67), E5(88)], [F6(66), F6(67), F6(88)], "2024", "2025", 0, 260)
    helper = table(["Օժանդակ ցուցանիշ", "2024", "2025"], [[E(str(g(a, r, 3)).split("\n")[0]), n(E5(r), 4 if r == 90 else 0) if r not in (89,) else v(E5(r), 2, 1), n(F6(r), 4 if r == 90 else 0) if r not in (89,) else v(F6(r), 2, 1)] for r in (82, 83, 84, 85, 88, 89, 90)])
    # ---- task 2 ----
    t4 = table(["11.1.4", "t0", "t1", "Δ"], [["Մարված ընթացիկ ՖՊ", n(g(b, 5, 4)), n(g(b, 5, 5)), n(g(b, 5, 6), 0, True)], ["ԸՖՊ միջին արժեք", n(g(b, 7, 4)), n(g(b, 7, 5)), n(g(b, 7, 6), 0, True)],
                                                  ["Շրջանառելիություն, պտույտ", n(g(b, 8, 4), 4), n(g(b, 8, 5), 4), n(g(b, 8, 6), 4, True)], ["Շրջանառելիություն, օր", n(g(b, 9, 4), 1), n(g(b, 9, 5), 1), n(g(b, 9, 6), 1, True)]])
    t5 = table(["11.1.5", "t0", "t1", "Δ"], [["Մարված ընթացիկ ՖՊ", n(g(b, 16, 4)), n(g(b, 16, 5)), n(g(b, 16, 6), 0, True)], ["ԸՖՊ միջին արժեք", n(g(b, 17, 4)), n(g(b, 17, 5)), n(g(b, 17, 6), 0, True)],
                                                  ["Շրջանառելիություն, պտույտ", n(g(b, 18, 4), 4), n(g(b, 18, 5), 4), n(g(b, 18, 6), 4, True)], ["Շրջանառելիություն, օր", n(g(b, 19, 4), 1), n(g(b, 19, 5), 1), n(g(b, 19, 6), 1, True)]])
    names = {26: "Ոչ ընթացիկ ՖՊ", 27: "· երկարաժամկետ բանկային վարկեր", 29: "· երկարաժամկետ փոխառություններ", 31: "Ընթացիկ ՖՊ", 32: "· կարճաժամկետ բանկային վարկեր", 34: "· կարճաժամկետ փոխառություններ", 37: "Ընդամենը"}
    t3 = table(["11.1.3", "t0", "%", "t1", "%", "Δ", "Δ, պ.կ."], [[E(nm), n(g(b, r, 3)), v(g(b, r, 4), 2, 1), n(g(b, r, 5)), v(g(b, r, 6), 2, 1), n(g(b, r, 7), 0, True), n(g(b, r, 8) * 100, 2, True)] for r, nm in names.items()])
    t3p = svg_pairs(["Երկ. վարկ", "Երկ. փոխ.", "Կարճ. վարկ", "Կարճ. փոխ."], [g(b, r, 3) for r in (27, 29, 32, 34)], [g(b, r, 5) for r in (27, 29, 32, 34)], "t0", "t1", 0, 260)
    ft = table(["Քայլ", "ԶՇ/Հ", "Հ/ՖՊ", "ՇԲԹֆպ"], [["1 · 2024 (բազիս)", v(g(a, 89, 5), 2, 1), n(g(a, 90, 5), 4), v(E5(74), 2, 1)], ["2 · Հ/ՖՊ → 2025", v(g(a, 89, 5), 2, 1), n(g(a, 90, 6), 4), v(F6(75), 2, 1)],
        ["3 · ԶՇ/Հ → 2025", v(g(a, 89, 6), 2, 1), n(g(a, 90, 6), 4), v(F6(74), 2, 1)], ["±Δ Հ/ՖՊ (2 − 1)", "", "", v(G7(75), 2, 1, True)], ["±Δ ԶՇ/Հ (3 − 2)", "", "", v(G7(76), 2, 1, True)], ["<b>Ընդամենը</b>", "", "", f"<b>{v(G7(74), 2, 1, True)}</b>"]])
    def sbar(nm, p0, p1): return (f'<div class="sb rv"><div class="gl"><span>{E(nm)}</span><b>{p0*100:.2f}% → {p1*100:.2f}%</b></div>'
                                  f'<div class="sbt"><i class="s0" style="width:{p0*100:.1f}%"></i></div><div class="sbt"><i class="s1" style="width:{p1*100:.1f}%"></i></div></div>')
    sh = "".join(sbar(nm, g(b, r, 4), g(b, r, 6)) for r, nm in ((26, "Ոչ ընթացիկ ՖՊ"), (27, "· երկ. բանկային վարկեր"), (29, "· երկ. փոխառություններ"), (31, "Ընթացիկ ՖՊ"), (32, "· կարճ. բանկային վարկեր"), (34, "· կարճ. փոխառություններ"))) + '<div class="gs"><span>▮ t0 (մուգ)</span><span>▮ t1 (ամբեր)</span></div>'
    gg = ''.join(sbar(nm, E5(r), F6(r)) for r, nm in ((73, 'ՏԿբվ · բանկային վարկերի կշիռ'), (72, 'ՏԿժ.անց · ժամկետանց ՖՊ կշիռ'), (71, 'ՏԿֆպ · ԸՖՊ ÷ ԸՊ'), (74, 'ՇԲԹֆպ · շահութաբերություն'))) + '<div class="gs"><span>▮ 2024 (մուգ)</span><span>▮ 2025 (ամբեր)</span></div>'
    concl = "".join(f"<p>{E(str(g(a, r, 2)))}</p>" for r in range(98, 104) if g(a, r, 2))
    concl2 = "".join(f"<p>{E(str(g(b, r, 2)))}</p>" for r in range(44, 47) if g(b, r, 2))
    kp = [("ՖՊ 2025", n(g(a, 83, 6)), f'<em class="gn">▼ {n(-g(a, 83, 7))} 2024-ի համեմատ</em>'), ("Պտույտ, օր", n(F6(70), 1), f'<em class="rd">▲ +{n(G7(70), 1)} օր</em>'),
          ("Բանկային վարկեր", v(F6(73), 2, 1), f'<em class="rd">▲ +{n(G7(73) * 100, 2)} պ.կ.</em>'), ("ՇԲԹֆպ", v(F6(74), 2, 1), f'<em class="gn">▲ +{n(G7(74) * 100, 2)} պ.կ.</em>')]
    kps = "".join(f'<div class="k9 rv" style="--i:{i}"><small>{E(l)}</small><b>{val}</b>{d}</div>' for i, (l, val, d) in enumerate(kp))
    tk = (f'<b>ՖՊ</b> {n(g(a, 83, 6))} <i class="d">▼{n(-g(a, 83, 7) / g(a, 83, 5) * 100, 1)}%</i>', f'<b>ՈԸՖՊ</b> {n(F6(66))} <i class="d">▼{n(-G7(66))}</i>', f'<b>ԸՖՊ</b> {n(F6(67))} <i class="u">▲{n(G7(67))}</i>',
          f'<b>ՇՐՋֆպ</b> {n(F6(69), 4)} <i class="d">▼{n(-G7(69), 4)}</i>', f'<b>Tօր</b> {n(F6(70), 1)} <i class="d">▲{n(G7(70), 1)}</i>', f'<b>ՏԿբվ</b> {v(F6(73), 2, 1)}',
          f'<b>ՏԿժ.անց</b> {v(F6(72), 2, 1)} <i class="u">▼{n(-G7(72) * 100, 2)}</i>', f'<b>ՇԲԹֆպ</b> {v(F6(74), 2, 1)} <i class="u">▲{n(G7(74) * 100, 2)}</i>')
    tks = "".join(f"<span>{x}</span>" for x in tk)
    notes = ("<p>Ոչ ընթացիկից ընթացիկ տեղափոխված մասը (22 000) մարում չէ․ այն երկրորդ անգամ հայտնվում է ընթացիկ ձևավորվածների մեջ։ Հիմնական հաշվարկում մարվածը վերցված է առանց կրկնահաշվարկի, իսկ Excel-ում ցույց է տրված նաև ձևանմուշի ուղիղ գումարով տարբերակը։</p>"
             "<p>Բանկային վարկերը որոշված են ըստ տողի անվանման «(բանկային վարկ)» նշման (օժանդակ H սյունակ)։ Ստուգում՝ 2024-ի տարեվերջի մնացորդները լրիվ համընկնում են 2025-ի տարեսկզբի տողերի հետ։</p>"
             "<p>11.1.3-ում t1-ի ընթացիկ ՖՊ-ն (52 200) 2 000-ով մեծ է բաղադրիչների գումարից (30 500 + 19 700)․ հոդվածը վերցված է ինչպես տրված է, տարբերությունը նշված է։ 11.1.4-ի օրերը հաշվարկված են 360 օրով։</p>")
    boot = "".join(f"<span>{E(x)}</span>" for x in ("H/R TERMINAL v9.0  ·  ԻՏ-447", "> load «XXX» ՍՊԸ · ֆինանսական պարտավորություններ", "> 194 բանաձև ............ OK", "> 0 սխալ ................ OK",
                                                   "> ՇԲԹֆպ գործոնային մոդել ... OK", "> ready_"))
    body = H.topbar(XL, "lesson-9.html", "Դաս 9") + f"""
<div class="cur"><div class="boot">{boot}</div></div>
<div class="tick"><div class="tt">{tks}{tks}</div></div>
<section class="hero">{P.hero_slides("term", [0, 1, 2, 3])}<div class="inner"><div class="prompt fade-up">hrachya@hr-studios:~$ <b>analyze --topic 10 --company "XXX ՍՊԸ" --years 2024..2025</b></div>
<h1 class="tl">{P.words("Ֆինանսական պարտավորությունների վերլուծություն")}</h1>
<p class="fade-up">Վարկեր և փոխառություններ՝ ինչպես շարժվեցին, որքան արագ են մարվում, որքան է բանկային կախվածությունը և որքան շահույթ է բերում պարտքի յուրաքանչյուր դրամը։ Դաս 9 · Թեմա 10 · Օ. Ա. Գալստյան</p>
<nav class="fkeys fade-up"><a href="#f1"><i>F1</i>Շարժ</a><a href="#f2"><i>F2</i>9 ցուցանիշ</a><a href="#f3"><i>F3</i>Գործոններ</a><a href="#f4"><i>F4</i>Տնային 2</a><a href="#f5"><i>F5</i>Եզրակացություն</a><a href="../../files/{XL}" download><i>XL</i>Excel</a></nav></div></section>
<div class="wrap9"><div class="kp9">{kps}</div>
<h2 class="h9 rv" id="f1"><i>F1</i>Պարտավորությունների շարժ</h2><p class="sub9 rv">Տարեսկիզբ + ձևավորված − մարված = տարեվերջ։ 2024-ի վերջը համընկնում է 2025-ի սկզբի հետ ✔</p>
<div class="g2"><div>{scr("MOVE · Տնային 1", "հազ. դր.", mvt)}{scr("AUX · օժանդակ հաշվարկներ", "Excel, տողեր 82–90", helper)}</div><div>{scr("WTRF · ՖՊ 2025", "սկիզբ → վերջ", wf)}{scr("STRC · կառուցվածք", "2024 vs 2025", st)}</div></div></div>
{P.chapter("term", 4, "F2", "Ինտենսիվություն", "Շրջանառելիություն, կշիռներ, շահութաբերություն")}
<div class="wrap9" id="excel"><h2 class="h9 rv" id="f2"><i>F2</i>Վերլուծություն՝ 9 ցուցանիշ</h2><p class="sub9 rv">Միջին արժեքը՝ (տարեսկիզբ + տարեվերջ) ÷ 2, կշիռները՝ տարեվերջի ՖՊ-ի նկատմամբ, t = 360 օր։</p>
{scr("ANLZ · ՎԵՐԼՈՒԾՈՒԹՅՈՒՆ", "Տնային 1 · տողեր 66–76", ant)}
<div class="g2">{scr("DAYS · պտույտի տևողություն", "փաստացի և ձևանմուշի տարբերակ", days)}{scr("RISK · կշիռներ", "2024 → 2025", gg)}</div>
<h2 class="h9 rv" id="f3"><i>F3</i>ՇԲԹֆպ-ի գործոնային վերլուծություն</h2><p class="sub9 rv">ՇԲԹֆպ = ԶՇ/Հ × Հ/ՖՊ · շղթայական տեղադրում։ Գործոնների գումարը = ընդհանուր փոփոխություն ({v(G7(74), 2, 1)}) ✔</p>
<div class="g2">{scr("FCTR · ±ΔՇԲԹֆպ", "պ.կ.", fw)}{scr("CHAIN · շղթայական տեղադրում", "%", ft)}</div></div>
{P.marquee("term", range(10))}
<div class="wrap9"><h2 class="h9 rv" id="f4"><i>F4</i>Տնային 2 · խնդիրներ 11.1.3–11.1.5</h2><p class="sub9 rv">Կազմ, կառուցվածք և շրջանառելիություն։</p>
<div class="g2">{scr("11.1.4", "շրջանառելիություն", t4)}{scr("11.1.5", "շրջանառելիություն", t5)}</div>
{scr("11.1.3 · կազմ և կառուցվածք", "հազ. դր. և %", t3)}<div class="g2">{scr("11.1.3 · գծապատկեր", "t0 vs t1", t3p)}{scr("11.1.3 · կառուցվածք", "կշիռ, %", sh)}</div>
<h2 class="h9 rv" id="f5"><i>F5</i>Եզրակացություն</h2>
<div class="g2">{scr("LOG · Տնային 1", "", f'<div class="log">{concl}</div>')}{scr("LOG · Տնային 2", "", f'<div class="log">{concl2}</div>')}</div>
{scr("NOTE · հաշվարկի ծանոթագրություններ", "", f'<div class="note">{notes}</div>')}</div>
<div class="foot">H/R STUDIOS · ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ · ԻՏ-447 · EXCEL՝ 194 ԲԱՆԱՁԵՎ · 0 ՍԽԱԼ</div>"""
    return P.page("term", "Ֆինանսական պարտավորություններ", body, CSS_TERM, "Դաս 9 (Թեմա 10) տնային աշխատանք", 1900, "#ffb000")

H.FONTS["term"] = "family=IBM+Plex+Mono:wght@400;500;600;700&family=Noto+Sans+Armenian:wght@400;500;600;700"
P.PAGES["dasi-9"] = build_hw9
if __name__ == "__main__":
    d = os.path.join(SITE, "hw", "dasi-9"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf8").write(build_hw9()); print("wrote dasi-9")
