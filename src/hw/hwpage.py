# -*- coding: utf-8 -*-
"""Five homework pages, each with its own visual language:
hw23 = printed financial newspaper, hw4 = engineering blueprint, hw5 = Swiss poster, hw6 = school notebook, mid = black & gold exam dossier."""
import json, html, os, openpyxl, sys
E = lambda s: html.escape("" if s is None else str(s))
HW = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.join(HW, "..", "site")
OUT = os.path.join(HW, "out")
def W(name):
    wb = openpyxl.load_workbook(os.path.join(OUT, name), data_only=True); return {ws.title: ws for ws in wb.worksheets}
def C(name): return json.load(open(os.path.join(OUT, name), encoding="utf8"))

def n(v, d=0, sign=False):
    if v is None or isinstance(v, str): return E(str(v or "–"))
    s = f"{v:,.{d}f}"; return ("+" + s if sign and v > 0 else s).replace("-", "−")

# ---------------- SVG helpers (colours come from CSS classes) ----------------
def svg_pairs(cats, a, b, la, lb, d=0, h=260):
    w = 640; pad = 46; top = 26; base = h - 40; m = max(max(abs(v) for v in a + b), 1e-9)
    gw = (w - pad * 2) / len(cats); bw = min(46, gw / 3)
    out = [f'<svg class="ch pairs" viewBox="0 0 {w} {h}" role="img"><line class="ax" x1="{pad}" x2="{w-pad}" y1="{base}" y2="{base}"/>']
    for i, c in enumerate(cats):
        x0 = pad + gw * i + gw / 2 - bw - 3
        for j, (v, cls) in enumerate(((a[i], "s1"), (b[i], "s2"))):
            hh = (base - top) * abs(v) / m; x = x0 + j * (bw + 6)
            out.append(f'<rect class="{cls} gr" x="{x:.1f}" y="{base-hh:.1f}" width="{bw:.1f}" height="{hh:.1f}" rx="3" style="--d:{i*0.08+j*0.04:.2f}s"/>'
                       f'<text class="vl" x="{x+bw/2:.1f}" y="{base-hh-6:.1f}" text-anchor="middle">{n(v,d)}</text>')
        out.append(f'<text class="cl" x="{pad+gw*i+gw/2:.1f}" y="{base+20}" text-anchor="middle">{E(c)}</text>')
    out.append(f'<g class="lg"><rect class="s1" x="{pad}" y="4" width="12" height="12" rx="2"/><text x="{pad+18}" y="14">{E(la)}</text>'
               f'<rect class="s2" x="{pad+180}" y="4" width="12" height="12" rx="2"/><text x="{pad+198}" y="14">{E(lb)}</text></g></svg>')
    return "".join(out)

def svg_waterfall(start, factors, end, d=2, h=280):
    w = 640; pad = 40; top = 30; bot = h - 54
    steps = [(start[0], 0, start[1], "tot")]; cur = start[1]
    for lab, v in factors: steps.append((lab, cur, cur + v, "pos" if v >= 0 else "neg")); cur += v
    steps.append((end[0], 0, end[1], "tot"))
    lo = min(min(a, b) for _, a, b, _ in steps); hi = max(max(a, b) for _, a, b, _ in steps)
    lo = min(lo, 0); rng = (hi - lo) or 1; y = lambda v: top + (hi - v) / rng * (bot - top)
    gw = (w - 2 * pad) / len(steps); bw = gw * 0.56
    out = [f'<svg class="ch wf" viewBox="0 0 {w} {h}" role="img"><line class="ax" x1="{pad}" x2="{w-pad}" y1="{y(0):.1f}" y2="{y(0):.1f}"/>']
    for i, (lab, a, b, cls) in enumerate(steps):
        x = pad + gw * i + (gw - bw) / 2; y1, y2 = sorted((y(a), y(b))); val = b if cls == "tot" else b - a
        out.append(f'<rect class="{cls} gr" x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(y2-y1,1.5):.1f}" rx="3" style="--d:{i*0.1:.1f}s"/>'
                   f'<text class="vl" x="{x+bw/2:.1f}" y="{y1-6:.1f}" text-anchor="middle">{n(val,d,cls!="tot")}</text>')
        words = lab.split(" "); l1 = " ".join(words[:2]); l2 = " ".join(words[2:])
        out.append(f'<text class="cl" x="{x+bw/2:.1f}" y="{bot+18}" text-anchor="middle">{E(l1)}</text>')
        if l2: out.append(f'<text class="cl" x="{x+bw/2:.1f}" y="{bot+33}" text-anchor="middle">{E(l2)}</text>')
        if i < len(steps) - 1:
            nx = pad + gw * (i + 1) + (gw - bw) / 2; out.append(f'<line class="cn" x1="{x+bw:.1f}" x2="{nx:.1f}" y1="{y(b):.1f}" y2="{y(b):.1f}"/>')
    return "".join(out) + "</svg>"

def gauge(label, v, lo, hi, vmax, d=3):
    p = lambda z: max(0, min(100, z / vmax * 100))
    return (f'<div class="gauge"><div class="gl"><span>{E(label)}</span><b>{n(v,d)}</b></div><div class="gt"><i class="zone" style="left:{p(lo):.1f}%;width:{p(hi)-p(lo):.1f}%"></i>'
            f'<i class="mk" style="left:{p(v):.1f}%"></i></div><div class="gs"><span>0</span><span>նորմա {lo:g}–{hi:g}</span><span>{vmax:g}</span></div></div>')

def table(head, rows, cls=""):
    th = "".join(f"<th>{E(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def verdict(s):
    s = str(s or ""); k = "ok" if s[:1] in "✔▲" else "no" if s[:1] in "✖▼" else ""
    return f'<span class="vd {k}">{E(s)}</span>'

# ---------------- content blocks (shared data, themed by CSS) ----------------
def liq_block(w, concl, lab="Առաջադրանք 1"):
    g = [[f"<b>Ա{i+1}</b> {E(w[f'B{6+i}'].value)}", n(w[f"C{6+i}"].value), f"<b>Պ{i+1}</b> {E(w[f'E{6+i}'].value)}", n(w[f"F{6+i}"].value), n(w[f"G{6+i}"].value, 0, True), verdict(w[f"H{6+i}"].value)] for i in range(4)]
    k = [[E(w[f"B{r}"].value), f'<code>{E(w[f"C{r}"].value)}</code>', n(w[f"F{r}"].value, 0 if r < 16 else 3), E(w[f"G{r}"].value), verdict(w[f"H{r}"].value)] for r in range(14, 19)]
    s = [[E(w[f"B{r}"].value), n(w[f"C{r}"].value, 3), n(w[f"F{r}"].value, 3), n(w[f"E{r}"].value, 3, True), verdict(w[f"H{r}"].value)] for r in range(27, 30)]
    pairs = svg_pairs(["Ա1/Պ1", "Ա2/Պ2", "Ա3/Պ3", "Ա4/Պ4"], [w[f"C{6+i}"].value for i in range(4)], [w[f"F{6+i}"].value for i in range(4)], "Ակտիվներ", "Պասիվներ")
    gg = gauge("Բացարձակ իրացվելիություն", w["F16"].value, 0.2, 0.5, 1) + gauge("Արագ իրացվելիություն", w["F17"].value, 0.7, 1.0, 2) + gauge("Ընթացիկ իրացվելիություն", w["F18"].value, 1, 2, 3)
    gg2 = svg_pairs(["Բացարձակ", "Արագ", "Ընթացիկ"], [w[f"C{r}"].value for r in range(27, 30)], [w[f"F{r}"].value for r in range(27, 30)], "Գործարքից առաջ", "Գործարքից հետո", 3, 230)
    return dict(
        groups=table(["Ակտիվների խումբ", "Գումար", "Պասիվների խումբ", "Գումար", "±", "Պայման"], g, "grp"), pairs=pairs,
        ratios=table(["Ցուցանիշ", "Բանաձև", "Արժեք", "Նորմա", "Գնահատական"], k), gauges=gg,
        scen=table(["Գործակից", "Մինչև", "Հետո", "Փոփոխություն", "Ազդեցություն"], s), scen_chart=gg2, txt=concl[0], txt2=concl[1], verdict=w["H10"].value)

def stab_block(w, concl):
    k = [[E(w[f"B{r}"].value), f'<code>{E(w[f"C{r}"].value)}</code>', n(w[f"D{r}"].value, 0 if r in (6, 12) else 1 if r == 13 else 3), E(w[f"E{r}"].value), verdict(w[f"F{r}"].value)] for r in range(6, 15)]
    s = [[f"<b>{E(w[f'A{r}'].value)}</b> {E(w[f'B{r}'].value)}", n(w[f"D{r}"].value, 3), n(w[f"E{r}"].value, 3), verdict(w[f"F{r}"].value)] for r in range(19, 22)]
    gg = gauge("Ֆինանսական անկախություն", w["D9"].value, 0.5, 1, 1) + gauge("Ֆինանսական ռիսկ", w["D11"].value, 0, 1, 2) + gauge("Ֆինանսական կայունություն", w["D14"].value, 0.6, 1, 1)
    return dict(ratios=table(["Ցուցանիշ", "Բանաձև", "Արժեք", "Նորմա", "Գնահատական"], k), gauges=gg, type=w["C16"].value,
                scen=table(["Սցենար", "Գկայ հետո", "Գֆռ հետո", "Արդյունք"], s), txt=concl[0], txt2=concl[1])

def fa_block(w, concl):
    inp = [[E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"D{r}"].value), n(w[f"E{r}"].value), n(w[f"F{r}"].value, 0, True)] for r in range(6, 19)]
    rows = []
    for r in range(22, 36):
        d = 0 if r in (22, 23, 24) else 2 if r in (31, 32, 33, 34, 35) else 3
        rows.append([E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"D{r}"].value, d), n(w[f"E{r}"].value, d), n(w[f"F{r}"].value, d, True), f"<small>{E(w[f'G{r}'].value)}</small>"])
    wf = svg_waterfall(("ՇԲԹՀՄ 2024", w["D31"].value), [("Իրացման շահութաբերություն", w["F34"].value), ("Ֆոնդահատույց", w["F35"].value)], ("ՇԲԹՀՄ 2025", w["E31"].value), 2)
    st = svg_pairs(["Նորացում", "Դուրսգրում", "Մաշվ. տս", "Մաշվ. տվ", "Պիտ. տս", "Պիտ. տվ"], [w[f"D{r}"].value for r in range(25, 31)], [w[f"E{r}"].value for r in range(25, 31)], "2024", "2025", 3)
    return dict(inputs=table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ"], inp), out=table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ", "Բանաձև"], rows), wf=wf, state=st,
                kpi=[(n(w["E22"].value, 0), "Գազ 2025"), (n(w["E24"].value, 0, True), "±ΔՀՄ հար."), (n(w["E28"].value, 3), "Մաշվ. տարեվերջին"), (n(w["E33"].value, 2), "Ֆոնդահատույց")],
                txt=concl[0], txt2=concl[1])

def mat_block(w, concl, y0="2020", y1="2021"):
    m = [[f"Նյութ-{i+1}", n(w[f"C{6+i}"].value, 0), n(w[f"D{6+i}"].value, 1), n(w[f"E{6+i}"].value), n(w[f"F{6+i}"].value, 0), n(w[f"G{6+i}"].value, 1), n(w[f"H{6+i}"].value)] for i in range(7)]
    m.append(["<b>Միավորի նյութական ծախս</b>", "", "", f"<b>{n(w['E13'].value)}</b>", "", "", f"<b>{n(w['H13'].value)}</b>"])
    m.append(["Արտադրանք (Ա)", n(w["C14"].value), n(w["D14"].value), n(w["E14"].value), n(w["F14"].value), n(w["G14"].value), n(w["H14"].value)])
    m.append(["<b>Նյութական ծախս (Նծ)</b>", "", "", f"<b>{n(w['E15'].value)}</b>", "", "", f"<b>{n(w['H15'].value)}</b>"])
    o = []
    for r in range(20, 28):
        d = 4 if r in (20, 23) else 0 if r in (26, 27) else 2
        o.append([E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"E{r}"].value, d) if w[f"E{r}"].value != "-" else "—", n(w[f"F{r}"].value, d, r > 23),
                  n(w[f"G{r}"].value, d, True) if w[f"G{r}"].value not in ("-", None) else "—", verdict(w[f"H{r}"].value)])
    bars = svg_pairs([f"Ն{i+1}" for i in range(7)], [w[f"E{6+i}"].value for i in range(7)], [w[f"H{6+i}"].value for i in range(7)], y0, y1)
    wf = svg_waterfall(("ՇԲԹՆԾ " + y0, w["E21"].value), [("Արտադրանքի շահութաբերություն", w["F24"].value), ("Նյութահատույց", w["F25"].value)], ("ՇԲԹՆԾ " + y1, w["F21"].value), 2)
    return dict(mats=table(["", f"{y0} նորմա", f"{y0} գին", f"{y0} ընդամենը", f"{y1} նորմա", f"{y1} գին", f"{y1} ընդամենը"], m, "mats"),
                out=table(["Ցուցանիշ", "Նշան", y0, y1, "Δ", ""], o), bars=bars, wf=wf, txt=concl[0], txt2=concl[1],
                kpi=[(n(w["F20"].value, 4), "Նյութատարություն " + y1), (n(w["G20"].value, 4, True), "ΔՆՏ"), (n(w["F23"].value, 3), "Նյութահատույց"), (n(w["F26"].value, 0, True), "±ΔԻ(ՆՏ)")])

def np2_block(w, concl):
    rows = [[f"<b>{E(w[f'A{r}'].value)}</b>"] + [n(w.cell(r, c).value, 1 if c in (3, 7) else 0) for c in range(2, 10)] for r in range(6, 9)]
    st = [[f"<b>{E(w[f'A{r}'].value)}</b>", f"<code>{E(w[f'B{r}'].value)}</code>", n(w[f"E{r}"].value, 4), E(w[f"F{r}"].value or ""), n(w[f"H{r}"].value, 4, True) if w[f"H{r}"].value not in (None, "") else ""] for r in range(19, 24)]
    wf = svg_waterfall(("Նտ₀", w["E19"].value), [("Տեսականի", w["H20"].value), ("Ծախսի նորմա", w["H21"].value), ("Նյութի գին", w["H22"].value), ("Արտադրանքի գին", w["H23"].value)], ("Նտ₁", w["E23"].value), 4)
    return dict(data=table(["", "Ա₀", "Ն₀", "Գն₀", "Գա₀", "Ա₁", "Ն₁", "Գն₁", "Գա₁"], rows), steps=table(["Քայլ", "Հաշվարկ", "Նտ", "Գործոն", "Ազդեցություն"], st), wf=wf, txt=concl)

def lab_block(w, concl):
    inp = [[E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"D{r}"].value, 2 if r in (9, 10, 11) else 0), n(w[f"E{r}"].value, 2 if r in (9, 10, 11) else 0), n(w[f"F{r}"].value, 2 if r in (9, 10, 11) else 0, True), n(w[f"G{r}"].value, 2, True)] for r in range(6, 18)]
    a1 = [[E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"F{r}"].value, 2, r > 20)] for r in range(20, 25)]
    a2 = [[E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"D{r}"].value, 4 if r == 32 else 2), n(w[f"E{r}"].value, 4 if r == 32 else 2), n(w[f"F{r}"].value, 4 if r == 32 else 2, True), n(w[f"G{r}"].value, 2, True)] for r in range(28, 33)]
    f2 = [[E(w[f"B{r}"].value), f"<code>{E(w[f'C{r}'].value)}</code>", n(w[f"F{r}"].value, 2, True)] for r in list(range(34, 37)) + list(range(39, 43))]
    ex = [[E(w[f"B{r}"].value), n(w[f"D{r}"].value, 3 if r == 48 else 2), n(w[f"E{r}"].value, 3 if r == 48 else 2), n(w[f"G{r}"].value, 2, True) + "%"] for r in range(47, 51)]
    wf1 = svg_waterfall(("Ֆ 2024", w["D20"].value), [("Թվաքանակ", w["F21"].value), ("Օրեր", w["F22"].value), ("Օրվա տևողություն", w["F23"].value)], ("Ֆ 2025", w["E20"].value), 0)
    wf2 = svg_waterfall(("ՏԱ 2024", w["D28"].value), [("Տեսակարար կշիռ", w["F39"].value), ("Օրեր", w["F40"].value), ("Տևողություն", w["F41"].value), ("Ժամային արտադրող.", w["F42"].value)], ("ՏԱ 2025", w["E28"].value), 0)
    return dict(inputs=table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ", "%"], inp), a1=table(["Վերլուծություն 1", "Նշան", "Փոփոխություն, ժամ"], a1), a2=table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ", "%"], a2),
                f2=table(["Գործոն", "Նշան", "Ազդեցություն, հազ. դր."], f2), ex=table(["Լրացուցիչ ցուցանիշ", "2024", "2025", "Աճ"], ex), wf1=wf1, wf2=wf2, txt=concl[0], txt2=concl[1],
                kpi=[(n(w["F20"].value, 0, True), "ΔՖ, ժամ"), (n(w["E31"].value, 0), "ԺԱ 2025, դրամ"), (n(w["G31"].value, 1, True) + "%", "ԺԱ աճ"), (n(w["F28"].value, 0, True), "ΔՏԱ, հազ. դր.")])

# ---------------- page shell ----------------
FONTS = {
 "paper": "family=Noto+Serif+Armenian:wght@400;600;800&family=Noto+Sans+Armenian:wght@400;600",
 "blueprint": "family=Noto+Sans+Armenian:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600",
 "swiss": "family=Noto+Sans+Armenian:wght@400;700;900",
 "notebook": "family=Noto+Sans+Armenian:wght@400;600;800&family=Caveat:wght@600;700",
 "gold": "family=Noto+Serif+Armenian:wght@400;600;700&family=Noto+Sans+Armenian:wght@300;400;600",
}
BASE_CSS = r"""
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;-webkit-font-smoothing:antialiased}img{max-width:100%;display:block}
a{color:inherit}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px 10px;text-align:right;vertical-align:middle}
th:first-child,td:first-child{text-align:left}code{font-size:12.5px;white-space:nowrap}td small{opacity:.75}
.vd{font-weight:700;white-space:nowrap;font-size:13px}
.ch{width:100%;height:auto;display:block;overflow:visible}.ch text{font-size:12px}.ch .vl{font-size:11.5px;font-weight:700}
.gr{transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0s)}
@keyframes grow{from{transform:scaleY(0)}}.cn{stroke-dasharray:3 3}
.gauge{margin:14px 0}.gl{display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px}.gt{position:relative;height:12px;border-radius:99px}
.gt .zone{position:absolute;top:0;bottom:0;border-radius:99px}.gt .mk{position:absolute;top:-5px;width:4px;height:22px;margin-left:-2px;border-radius:2px;transition:left 1s}
.gs{display:flex;justify-content:space-between;font-size:11px;opacity:.6;margin-top:4px}
.rv{opacity:0;transform:translateY(16px);transition:opacity .7s,transform .7s cubic-bezier(.2,.7,.2,1)}.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none}.gr{animation:none}}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;padding:10px 20px}
.topbar .lg{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:800}.topbar .lg img{height:30px;border-radius:6px}.topbar .sp{flex:1}
.topbar a.b{text-decoration:none;font-weight:700;font-size:13.5px;padding:8px 14px}
@media (max-width:700px){.topbar .hide{display:none}th,td{padding:7px 6px;font-size:12.5px}}
"""
JS = r"""<script>
(function(){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
document.querySelectorAll('[data-tab]').forEach(function(b){b.addEventListener('click',function(){var g=b.closest('[data-tabs]');
g.querySelectorAll('[data-tab]').forEach(function(x){x.classList.toggle('on',x===b)});g.querySelectorAll('[data-pane]').forEach(function(p){p.classList.toggle('on',p.dataset.pane===b.dataset.tab)})})});
var ch=document.querySelectorAll('svg.ch');var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('play');io2.unobserve(e.target)}})});ch.forEach(function(c){io2.observe(c)});
})();</script>"""

def page(theme, title, body, css, desc):
    return f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · H/R Studios</title><meta name="description" content="{E(desc)}"><link rel="icon" href="../../assets/logo_sm.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[theme]}&display=swap">
<style>{BASE_CSS}{css}</style></head><body class="t-{theme}">{body}{JS}</body></html>"""

def topbar(xl, lesson_href, label):
    return (f'<header class="topbar"><a class="lg" href="../../index.html"><img src="../../assets/logo_sm.png" alt="H/R">H/R Studios</a><span class="sp"></span>'
            f'<a class="b hide" href="../../{lesson_href}">← {E(label)}</a><a class="b hide" href="../../works.html">Իմ աշխատանքները</a><a class="b x" href="../../files/{xl}" download>⬇ Excel</a></header>')

# ======================= 1) PAPER — financial newspaper =======================
CSS_PAPER = r"""
body{background:#f4efe3;color:#1d1a16;font-family:'Noto Serif Armenian',Georgia,serif}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.35;background-image:radial-gradient(rgba(80,60,30,.12) 1px,transparent 1px);background-size:3px 3px}
.topbar{background:#f4efe3ee;border-bottom:3px double #1d1a16;backdrop-filter:blur(6px)}.topbar a.b{border:1px solid #1d1a16}.topbar a.x{background:#1f3a5f;color:#fff;border-color:#1f3a5f}
.mast{text-align:center;padding:34px 0 10px;border-bottom:1px solid #1d1a16}.mast .kick{font:600 12px 'Noto Sans Armenian';letter-spacing:.3em;text-transform:uppercase;color:#b5452b}
.mast h1{font-size:clamp(34px,6vw,72px);line-height:1;margin:10px 0;font-weight:800;letter-spacing:-.01em}
.dateline{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font:400 13px 'Noto Sans Armenian';border-top:1px solid #1d1a16;border-bottom:3px double #1d1a16;padding:6px 0;margin-top:14px}
.lead{display:grid;grid-template-columns:1.25fr 1fr;gap:34px;padding:30px 0;border-bottom:1px solid #1d1a16}
.lead img{filter:grayscale(1) contrast(1.1) sepia(.25);border:1px solid #1d1a16}.lead figcaption{font:italic 12.5px 'Noto Serif Armenian';margin-top:6px;opacity:.7}
.lead p.dc::first-letter{float:left;font-size:64px;line-height:.85;padding:6px 8px 0 0;font-weight:800;color:#b5452b}
.lead p{font-size:17px;line-height:1.7;margin:0 0 12px;text-align:justify;hyphens:auto}
.stamp{display:inline-block;transform:rotate(-6deg);border:3px solid #b5452b;color:#b5452b;padding:8px 14px;font:800 15px 'Noto Sans Armenian';letter-spacing:.06em;text-transform:uppercase;margin-top:6px}
.stamp.ok{border-color:#4e7d5b;color:#4e7d5b}
section.art{padding:34px 0;border-bottom:1px solid #1d1a16}section.art h2{font-size:clamp(26px,3.6vw,40px);margin:0 0 4px}
.sub{font:600 13px 'Noto Sans Armenian';letter-spacing:.18em;text-transform:uppercase;color:#b5452b}
.cols{columns:2;column-gap:34px;column-rule:1px solid #cdbf9f;font-size:16px;line-height:1.7;text-align:justify}
.two{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:18px}
table{font-family:'Noto Sans Armenian'}thead th{border-top:2px solid #1d1a16;border-bottom:1px solid #1d1a16;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
tbody tr{border-bottom:1px dotted #a99b7c}tbody tr:hover{background:#ebe2cd}.vd.ok{color:#4e7d5b}.vd.no{color:#b5452b}
.box{border:1px solid #1d1a16;padding:18px;background:#fbf7ee}.box h3{margin:0 0 6px;font-size:18px}
.ch .s1,.ch .tot{fill:#1f3a5f}.ch .s2{fill:#b5452b}.ch .pos{fill:#4e7d5b}.ch .neg{fill:#b5452b}.ch .ax,.ch .cn{stroke:#1d1a16}.ch text{fill:#1d1a16;font-family:'Noto Sans Armenian'}
.gt{background:#e2d7bd}.gt .zone{background:#9fb8a5}.gt .mk{background:#1d1a16}.gl b{font-family:'Noto Sans Armenian'}
.pull{font-size:24px;line-height:1.35;font-style:italic;border-top:3px solid #1d1a16;border-bottom:1px solid #1d1a16;padding:14px 0;margin:20px 0}
.foot{padding:30px 0 60px;text-align:center;font:400 13px 'Noto Sans Armenian';opacity:.75}
@media (max-width:860px){.lead,.two{grid-template-columns:1fr}.cols{columns:1}}
"""
def build_hw23():
    V = W("Das2-3_Irachvelutyun_Kayunutyun_Hrachya_Aslanyan.xlsx"); c = C("hw23_concl.json")
    L = liq_block(V["Իրացվելիություն"], c["liq"]); S = stab_block(V["Կայունություն"], c["stab"])
    ok = str(L["verdict"]).startswith("✔")
    body = topbar("Das2-3_Irachvelutyun_Kayunutyun_Hrachya_Aslanyan.xlsx", "lesson-2.html", "Դաս 2") + f"""
<div class="wrap"><div class="mast"><div class="kick">Ֆինանսական տեղեկագիր · Թողարկում №2–3</div><h1>«XXX» ՍՊԸ-ն վճարունակ է,<br>բայց ոչ բացարձակ</h1>
<div class="dateline"><span>Երևան · 18 սեպտեմբերի 2026</span><span>Հեղինակ՝ Հրաչյա Ասլանյան, ԻՏ-447</span><span>Դասեր 2 և 3 · Իրացվելիություն և կայունություն</span></div></div>
<div class="lead"><div><p class="dc">Ընկերության հաշվեկշիռը 260 000 հազ. դրամ է։ Մենք ակտիվները դասավորեցինք ըստ այն բանի, թե որքան արագ կարող են դառնալ փող, իսկ պարտքերը՝ ըստ այն բանի, թե երբ պետք է վճարվեն։ Այնուհետև ստուգեցինք՝ արդյոք ընկերությունը կանգնած է սեփական ոտքերի վրա։</p>
<p>{E(c["liq"][0])}</p><span class="stamp {'ok' if ok else ''}">{E(L["verdict"][2:])}</span></div>
<figure class="rv"><img src="../../assets/gen/liquidity.jpg" alt="" loading="lazy"><figcaption>Նկ. 1 · Իրացվելիությունը՝ որքան արագ է ակտիվը դառնում փող</figcaption></figure></div>
<section class="art rv" id="excel"><div class="sub">Առաջադրանք 1 · Մաս Ա</div><h2>Չորս կշեռք՝ Ա-խմբեր ընդդեմ Պ-խմբերի</h2>
<div class="two"><div>{L["groups"]}</div><div class="box">{L["pairs"]}</div></div></section>
<section class="art rv"><div class="sub">Առաջադրանք 1 · Մաս Բ</div><h2>Գործակիցները նորմայի «միջանցքում»</h2>
<div class="two"><div>{L["ratios"]}</div><div class="box"><h3>Որտե՞ղ ենք նորմայի նկատմամբ</h3>{L["gauges"]}</div></div></section>
<section class="art rv"><div class="sub">Առաջադրանք 1 · Հարց 9</div><h2>Ի՞նչ կլինի, եթե գնենք 30 000-ի պաշար</h2>
<div class="two"><div>{L["scen"]}<p class="pull">{E(c["liq"][1])}</p></div><div class="box">{L["scen_chart"]}</div></div></section>
<section class="art rv"><div class="sub">Առաջադրանք 2</div><h2>Ֆինանսական կայունություն. «{E(S["type"])}»</h2>
<div class="two"><div>{S["ratios"]}</div><div class="box"><h3>Կայունության սանդղակ</h3>{S["gauges"]}</div></div>
<div class="cols" style="margin-top:22px"><p>{E(c["stab"][0])}</p><p>{E(c["stab"][1])}</p></div>
<h3 style="margin-top:22px">Ինչպե՞ս ամրապնդել (հարց 7)</h3>{S["scen"]}</section>
<div class="foot">© H/R Studios · Հրաչյա Ասլանյան · Բոլոր թվերը Excel ֆայլում հաշվված են բանաձևերով (112 բանաձև, 0 սխալ)</div></div>"""
    return page("paper", "Իրացվելիություն և կայունություն", body, CSS_PAPER, "Դասեր 2–3 տնային աշխատանք")

# ======================= 2) BLUEPRINT — engineering drawing =======================
CSS_BLUE = r"""
body{background:#0b2a4a;color:#dcecff;font-family:'Noto Sans Armenian',sans-serif;
background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
background-size:100px 100px,100px 100px,20px 20px,20px 20px}
.topbar{background:rgba(11,42,74,.92);border-bottom:1px solid rgba(220,236,255,.35);font-family:'IBM Plex Mono',monospace}.topbar a.b{border:1px dashed rgba(220,236,255,.6)}.topbar a.x{background:#dcecff;color:#0b2a4a;border-style:solid}
.hero{display:grid;grid-template-columns:1fr 420px;gap:30px;padding:46px 0 30px;align-items:center}
.tag{font:600 12px 'IBM Plex Mono';letter-spacing:.2em;color:#7cc4ff}.hero h1{font-weight:300;font-size:clamp(32px,5vw,58px);line-height:1.08;margin:12px 0}
.hero h1 b{font-weight:700;color:#fff}.hero p{color:#a9c7e8;font-size:16.5px;line-height:1.65;max-width:620px}
.frame{position:relative;border:1px solid rgba(220,236,255,.6);padding:18px;background:rgba(11,42,74,.55)}
.frame::before,.frame::after{content:"";position:absolute;width:18px;height:18px;border:2px solid #7cc4ff}.frame::before{top:-6px;left:-6px;border-right:0;border-bottom:0}.frame::after{bottom:-6px;right:-6px;border-left:0;border-top:0}
.frame .lbl{position:absolute;top:-11px;left:22px;background:#0b2a4a;padding:0 8px;font:600 11px 'IBM Plex Mono';letter-spacing:.15em;color:#7cc4ff}
.hero img{filter:grayscale(1) brightness(1.1) contrast(1.2);mix-blend-mode:screen;opacity:.85}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:10px 0 30px}.kpis .frame b{display:block;font:600 28px 'IBM Plex Mono';color:#fff}.kpis .frame span{font-size:12.5px;color:#a9c7e8}
section{margin:34px 0}section h2{font-weight:300;font-size:30px;margin:0 0 16px}section h2 i{font-style:normal;font:600 13px 'IBM Plex Mono';color:#7cc4ff;margin-right:12px}
.g2{display:grid;grid-template-columns:1.1fr .9fr;gap:22px}
table{font-family:'IBM Plex Mono','Noto Sans Armenian',monospace;font-size:13px}td:first-child{font-family:'Noto Sans Armenian'}thead th{color:#7cc4ff;border-bottom:1px solid #7cc4ff;font-weight:600;font-size:11.5px}
tbody tr{border-bottom:1px dashed rgba(220,236,255,.18)}tbody tr:hover{background:rgba(124,196,255,.08)}code{color:#ffd27c}
.ch .s1{fill:rgba(220,236,255,.25);stroke:#dcecff}.ch .s2,.ch .tot{fill:#7cc4ff}.ch .pos{fill:#4fd1a5}.ch .neg{fill:#ff8a65}.ch .ax,.ch .cn{stroke:#dcecff}.ch text{fill:#dcecff;font-family:'IBM Plex Mono'}
.note{border-left:3px solid #7cc4ff;padding:4px 0 4px 16px;color:#cfe3fb;line-height:1.7;font-size:15.5px}
.foot{padding:20px 0 60px;font:400 12px 'IBM Plex Mono';color:#7cc4ff;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;border-top:1px solid rgba(220,236,255,.35)}
@media (max-width:900px){.hero,.g2{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}}
"""
def build_hw4():
    V = W("Das4_Himnakan_mijocner_Hrachya_Aslanyan.xlsx"); c = C("hw4_concl.json"); F = fa_block(V["Հիմնական միջոցներ"], c["fa"])
    k = "".join(f'<div class="frame rv"><b>{a}</b><span>{E(b)}</span></div>' for a, b in F["kpi"])
    body = topbar("Das4_Himnakan_mijocner_Hrachya_Aslanyan.xlsx", "lesson-4.html", "Դաս 4") + f"""
<div class="wrap"><div class="hero"><div><div class="tag">DWG-04 · ԴԱՍ 4 · 25.09.2026</div><h1>Հիմնական միջոցների<br><b>տեխնիկական անձնագիր</b></h1>
<p>Մեքենաները, շենքերն ու սարքավորումները ընկերության «երկաթե կմախքն» են։ Այստեղ չափել ենք՝ որքան են դրանք, որքան են մաշված, որքան արագ են նորացվում և քանի դրամ շահույթ է բերում յուրաքանչյուր դրամ ՀՄ։ Հեղինակ՝ Հրաչյա Ասլանյան։</p></div>
<div class="frame"><span class="lbl">ՆԿ. 01</span><img src="../../assets/gen/factory.jpg" alt=""></div></div>
<div class="kpis">{k}</div>
<section class="rv" id="excel"><h2><i>01</i>Մուտքային տվյալներ</h2><div class="frame"><span class="lbl">ԱՂՅՈՒՍԱԿ Ա</span>{F["inputs"]}</div></section>
<section class="rv"><h2><i>02</i>Արդյունքային ցուցանիշներ</h2><div class="frame"><span class="lbl">ԱՂՅՈՒՍԱԿ Բ · 14 ՑՈՒՑԱՆԻՇ</span>{F["out"]}</div></section>
<section class="rv"><h2><i>03</i>Վիճակ և շարժ</h2><div class="g2"><div class="frame"><span class="lbl">ԳԾ. 1 · ԳՈՐԾԱԿԻՑՆԵՐ</span>{F["state"]}</div><div class="note">{E(c["fa"][0])}</div></div></section>
<section class="rv"><h2><i>04</i>Շահութաբերության գործոնային վերլուծություն</h2><div class="g2"><div class="frame"><span class="lbl">ԳԾ. 2 · ՋՐՎԵԺ</span>{F["wf"]}</div><div class="note">{E(c["fa"][1])}<br><br><code>ՇԲԹՀՄ = ՇԲԹիրաց × ՀՏ</code><br><code>Δ(ՇԲԹիրաց) = ΔՇԲԹիրաց × ՀՏ₀</code><br><code>Δ(ՀՏ) = ΔՀՏ × ՇԲԹիրաց₁</code></div></div></section>
<div class="foot"><span>H/R STUDIOS · ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ · ԻՏ-447</span><span>ԹԵՐԹ 1/1 · EXCEL՝ 84 ԲԱՆԱՁԵՎ · 0 ՍԽԱԼ</span></div></div>"""
    return page("blueprint", "Հիմնական միջոցներ", body, CSS_BLUE, "Դաս 4 տնային աշխատանք")

# ======================= 3) SWISS — international typographic poster =======================
CSS_SWISS = r"""
body{background:#fff;color:#111;font-family:'Noto Sans Armenian',Helvetica,Arial,sans-serif}
.topbar{background:#fff;border-bottom:6px solid #e30613}.topbar a.b{background:#111;color:#fff}.topbar a.x{background:#e30613}
.poster{display:grid;grid-template-columns:repeat(12,1fr);gap:0;border-bottom:1px solid #111;min-height:72vh}
.poster .red{grid-column:span 5;background:#e30613;color:#fff;padding:40px 30px;display:flex;flex-direction:column;justify-content:space-between}
.poster .red .no{font-weight:900;font-size:clamp(120px,18vw,240px);line-height:.8;letter-spacing:-.06em}
.poster .red p{font-size:15px;line-height:1.55;max-width:360px}.poster .img{grid-column:span 7;background:#111 center/cover no-repeat;position:relative}
.poster .img h1{position:absolute;left:30px;bottom:26px;right:30px;margin:0;color:#fff;font-weight:900;font-size:clamp(34px,5.4vw,76px);line-height:.95;letter-spacing:-.03em;text-shadow:0 2px 30px rgba(0,0,0,.35)}
.strip{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #111}.strip div{padding:22px 20px;border-right:1px solid #111}.strip div:last-child{border-right:0}
.strip b{display:block;font-weight:900;font-size:clamp(28px,3.4vw,44px);letter-spacing:-.03em}.strip span{font-size:12.5px;text-transform:uppercase;letter-spacing:.1em}
section{display:grid;grid-template-columns:240px 1fr;border-bottom:1px solid #111}section>h2{margin:0;padding:24px 20px;font-weight:900;font-size:26px;line-height:1.05;border-right:1px solid #111}
section>h2 small{display:block;color:#e30613;font-size:13px;letter-spacing:.12em;margin-bottom:8px}section>div{padding:24px 24px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:28px}
thead th{background:#111;color:#fff;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.05em}tbody tr{border-bottom:1px solid #ddd}tbody tr:nth-child(even){background:#f4f4f4}
table.mats tr:nth-last-child(-n+3){font-weight:700}.vd.ok{color:#0a7c2f}.vd.no{color:#e30613}
.ch .s1{fill:#bdbdbd}.ch .s2,.ch .neg{fill:#e30613}.ch .tot{fill:#111}.ch .pos{fill:#111}.ch .ax{stroke:#111}.ch .cn{stroke:#e30613}.ch text{fill:#111}
.txt{font-size:17px;line-height:1.6;max-width:760px}.txt b{background:#e30613;color:#fff;padding:0 4px}
.foot{display:flex;justify-content:space-between;padding:20px;font-size:12px;text-transform:uppercase;letter-spacing:.1em}
@media (max-width:900px){.poster .red,.poster .img{grid-column:span 12}.poster .img{min-height:340px}section{grid-template-columns:1fr}section>h2{border-right:0;border-bottom:1px solid #111}.g2,.strip{grid-template-columns:1fr 1fr}}
"""
def build_hw5():
    V = W("Das5_Nyutakan_pasharner_Hrachya_Aslanyan.xlsx"); c = C("hw5_concl.json")
    M = mat_block(V["ՆՊ 1"], c["mat"]); P = np2_block(V["ՆՊ 2"], c["np2"])
    k = "".join(f"<div><b>{a}</b><span>{E(b)}</span></div>" for a, b in M["kpi"])
    body = topbar("Das5_Nyutakan_pasharner_Hrachya_Aslanyan.xlsx", "lesson-5.html", "Դաս 5") + f"""
<div class="poster"><div class="red"><div class="no">05</div><p><b>Նյութական պաշարներ.</b> Որքան հումք ու նյութ է «ուտում» միավոր արտադրանքը, և ինչ է փոխվել, երբ գները, նորմաներն ու տեսականին շարժվել են։<br><br>Հրաչյա Ասլանյան · ԻՏ-447 · 03.10.2026</p></div>
<div class="img" style="background-image:url('../../assets/gen/warehouse.jpg')"><h1>Ավելի քիչ նյութ.<br>Ավելի շատ շահույթ.</h1></div></div>
<div class="strip">{k}</div>
<section class="rv" id="excel"><h2><small>ՏՆԱՅԻՆ 1</small>Յոթ նյութ, երկու տարի</h2><div><div class="g2"><div>{M["mats"]}</div><div>{M["bars"]}</div></div></div></section>
<section class="rv"><h2><small>ՏՆԱՅԻՆ 1</small>Ութ ցուցանիշ</h2><div>{M["out"]}<p class="txt" style="margin-top:20px">{E(c["mat"][0])}</p></div></section>
<section class="rv"><h2><small>ՏՆԱՅԻՆ 1</small>Ինչու՞ աճեց շահութաբերությունը</h2><div><div class="g2"><div>{M["wf"]}</div><p class="txt">{E(c["mat"][1])}</p></div></div></section>
<section class="rv"><h2><small>ՏՆԱՅԻՆ 2</small>Երեք արտադրանք՝ «Ա», «Բ», «Գ»</h2><div>{P["data"]}</div></section>
<section class="rv"><h2><small>ՏՆԱՅԻՆ 2</small>Շղթայական տեղադրում</h2><div><div class="g2"><div>{P["steps"]}<p class="txt" style="margin-top:16px">{E(c["np2"])}</p></div><div>{P["wf"]}</div></div></div></section>
<div class="foot"><span>H/R Studios</span><span>Excel · 100 բանաձև · 0 սխալ</span></div>"""
    return page("swiss", "Նյութական պաշարներ", body, CSS_SWISS, "Դաս 5 տնային աշխատանք")

# ======================= 4) NOTEBOOK — school notebook with stickers =======================
CSS_NOTE = r"""
body{background:#fdfaf3;color:#2d2a32;font-family:'Noto Sans Armenian',sans-serif;
background-image:linear-gradient(90deg,transparent 78px,#f4a7a7 78px,#f4a7a7 80px,transparent 80px),repeating-linear-gradient(#fdfaf3 0 31px,#cfe0f3 31px 32px)}
.topbar{background:#fdfaf3f0;border-bottom:2px dashed #cdb4db}.topbar a.b{border-radius:99px;background:#fff;border:2px solid #6a4c93;color:#6a4c93}.topbar a.x{background:#6a4c93;color:#fff}
.wrap{padding-left:100px}.hand{font-family:'Caveat',cursive}
.hero{padding:40px 0 20px;position:relative}.hero{padding-right:330px}.hero h1{font-family:'Caveat','Noto Sans Armenian';font-size:clamp(34px,4.3vw,56px);line-height:1.05;margin:0;color:#6a4c93}
.hero h1 u{text-decoration:none;background:linear-gradient(transparent 60%,#ffe066 60%)}.hero p{max-width:640px;font-size:17px;line-height:1.75}
.polar{position:absolute;right:0;top:30px;width:300px;background:#fff;padding:12px 12px 40px;box-shadow:0 14px 30px rgba(0,0,0,.15);transform:rotate(4deg)}
.polar::before{content:"";position:absolute;top:-14px;left:50%;width:110px;height:28px;margin-left:-55px;background:rgba(242,132,130,.55);transform:rotate(-3deg)}
.polar span{position:absolute;bottom:8px;left:0;right:0;text-align:center;font:700 22px 'Caveat';color:#6a4c93}
.stick{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:26px 0}.stick div{padding:16px;box-shadow:0 8px 18px rgba(0,0,0,.1);transform:rotate(-1.5deg)}
.stick div:nth-child(1){background:#fff3b0}.stick div:nth-child(2){background:#cdeac0;transform:rotate(1.2deg)}.stick div:nth-child(3){background:#ffd6e0;transform:rotate(-.6deg)}.stick div:nth-child(4){background:#d0e8ff;transform:rotate(1.8deg)}
.stick b{display:block;font:700 34px 'Caveat'}.stick span{font-size:13px}
.page{background:#fff;border-radius:6px;padding:24px 26px;margin:30px 0;box-shadow:0 10px 30px rgba(106,76,147,.12);position:relative}
.page h2{font:700 38px 'Caveat';margin:0 0 10px;color:#6a4c93}.page h2 em{font-style:normal;background:#f28482;color:#fff;border-radius:99px;padding:0 12px;font-size:24px;margin-right:10px;vertical-align:middle}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:24px}
thead th{color:#6a4c93;border-bottom:2px solid #cdb4db;font-size:12.5px}tbody tr{border-bottom:1px solid #f0e6f6}tbody tr:hover{background:#fff8e7}code{background:#f3eefa;padding:1px 6px;border-radius:6px;color:#6a4c93}
.vd.ok{color:#2a9d8f}.vd.no{color:#e76f51}
.ch .s1{fill:#cdb4db}.ch .s2,.ch .tot{fill:#6a4c93}.ch .pos{fill:#2a9d8f}.ch .neg{fill:#e76f51}.ch .ax,.ch .cn{stroke:#6a4c93}.ch text{fill:#2d2a32}
.memo{font:600 21px/1.4 'Caveat','Noto Sans Armenian';color:#3d348b;background:#fff3b0;padding:16px 20px;box-shadow:0 8px 18px rgba(0,0,0,.08);transform:rotate(-.5deg)}
.foot{padding:20px 0 60px;font:700 22px 'Caveat';color:#6a4c93}
@media (max-width:900px){.hero{padding-right:0}.wrap{padding-left:20px}.polar{position:static;transform:rotate(2deg);margin:20px auto 0}.g2{grid-template-columns:1fr}.stick{grid-template-columns:1fr 1fr}}
"""
def build_hw6():
    V = W("Das6_Ashkhatank_Hrachya_Aslanyan.xlsx"); c = C("hw6_concl.json"); A = lab_block(V["Աշխատանք"], c["lab"])
    k = "".join(f"<div class='rv'><b>{a}</b><span>{E(b)}</span></div>" for a, b in A["kpi"])
    body = topbar("Das6_Ashkhatank_Hrachya_Aslanyan.xlsx", "lesson-6.html", "Դաս 6") + f"""
<div class="wrap"><div class="hero"><div class="hand" style="font-size:26px;color:#f28482">Տնային № 6 · 10.10.2026</div><h1>Մարդիկ, ժամեր<br>և <u>արտադրողականություն</u></h1>
<p>Ընկերությունում 231 մարդ է աշխատում։ Հաշվեցինք՝ քանի ժամ են նրանք իրականում աշխատել, ինչու է փոխվել այդ ժամաքանակը և ինչն է բարձրացրել մեկ աշխատողի արդյունքը։ Ամեն ինչ՝ շղթայական տեղադրման եղանակով։</p>
<div class="polar"><img src="../../assets/gen/team.jpg" alt=""><span>մեր թիմը ✿</span></div></div>
<div class="stick">{k}</div>
<div class="page rv" id="excel"><h2><em>0</em>Ինչ ունենք (տվյալներ)</h2>{A["inputs"]}</div>
<div class="page rv"><h2><em>1</em>Աշխատաժամանակի ֆոնդ</h2><div class="g2"><div>{A["a1"]}<p class="memo" style="margin-top:18px">Ֆ = Թ × Օ × Ժ<br>{E(c["lab"][0])}</p></div><div>{A["wf1"]}</div></div></div>
<div class="page rv"><h2><em>2</em>Արտադրողականություն</h2>{A["a2"]}<div class="g2" style="margin-top:18px"><div>{A["f2"]}</div><div>{A["wf2"]}</div></div>
<p class="memo" style="margin-top:18px">ՏԱ = ՏԿ × Օ × Ժ × ԺԱ<br>{E(c["lab"][1])}</p></div>
<div class="page rv"><h2><em>+</em>Մեր կողմից ավելացված</h2>{A["ex"]}</div>
<div class="foot">— Հրաչյա Ասլանյան, ԻՏ-447 · Excel՝ 91 բանաձև, 0 սխալ ✓</div></div>"""
    return page("notebook", "Աշխատանքային ռեսուրսներ", body, CSS_NOTE, "Դաս 6 տնային աշխատանք")

# ======================= 5) GOLD — exam dossier =======================
CSS_GOLD = r"""
body{background:#0e0d0b;color:#e9e2d0;font-family:'Noto Sans Armenian',sans-serif;font-weight:300}
.topbar{background:rgba(14,13,11,.9);border-bottom:1px solid #3a3221}.topbar a.b{border:1px solid #b8860b;color:#e9c46a}.topbar a.x{background:linear-gradient(135deg,#e9c46a,#b8860b);color:#111;font-weight:700}
.cover{min-height:78vh;display:grid;place-items:center;text-align:center;position:relative;overflow:hidden;border-bottom:1px solid #3a3221}
.cover::before{content:"";position:absolute;inset:0;background:url('../../assets/gen/midterm.jpg') center/cover;opacity:.22;filter:grayscale(1)}
.cover>div{position:relative;padding:40px 20px}.seal{width:120px;height:120px;margin:0 auto 24px;border-radius:50%;border:2px solid #b8860b;display:grid;place-items:center;font:700 44px 'Noto Serif Armenian';color:#e9c46a;box-shadow:0 0 0 8px #0e0d0b,0 0 0 9px #3a3221}
.cover h1{font:600 clamp(36px,6vw,74px)/1.05 'Noto Serif Armenian';margin:0;background:linear-gradient(180deg,#f7e7b4,#b8860b);-webkit-background-clip:text;background-clip:text;color:transparent}
.cover p{color:#bfb59c;letter-spacing:.25em;text-transform:uppercase;font-size:12.5px}
.rule{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#3a3221;margin:40px 0}.rule div{background:#141210;padding:18px}.rule b{display:block;color:#e9c46a;font:600 20px 'Noto Serif Armenian'}.rule span{font-size:13px;color:#bfb59c}
.tabs{display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid #3a3221;position:sticky;top:52px;background:#0e0d0b;z-index:10;padding-top:8px}
.tabs button{background:none;border:0;color:#bfb59c;font:600 15px 'Noto Serif Armenian';padding:12px 16px;cursor:pointer;border-bottom:2px solid transparent}.tabs button.on{color:#e9c46a;border-color:#e9c46a}
[data-pane]{display:none;padding:30px 0}[data-pane].on{display:block;animation:fi .5s}@keyframes fi{from{opacity:0;transform:translateY(8px)}}
h2{font:600 32px 'Noto Serif Armenian';color:#f3e3b3;margin:0 0 6px}h3{font:600 20px 'Noto Serif Armenian';color:#e9c46a;margin:26px 0 10px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:26px}.card{background:#141210;border:1px solid #3a3221;padding:20px}
thead th{color:#e9c46a;font-weight:600;border-bottom:1px solid #b8860b;font-size:12px;letter-spacing:.05em}tbody tr{border-bottom:1px solid #2a251a}tbody tr:hover{background:#1b1813}code{color:#e9c46a}
.vd.ok{color:#8bc34a}.vd.no{color:#ef5350}.concl{border-left:2px solid #b8860b;padding-left:18px;line-height:1.75;color:#ddd3bb}
.ch .s1{fill:#5a4c2e}.ch .s2,.ch .tot{fill:#e9c46a}.ch .pos{fill:#8bc34a}.ch .neg{fill:#ef5350}.ch .ax,.ch .cn{stroke:#7d6a3a}.ch text{fill:#e9e2d0}
.gt{background:#2a251a}.gt .zone{background:#5d6b34}.gt .mk{background:#e9c46a}
.foot{padding:30px 0 70px;text-align:center;color:#7d6a3a;font-size:12.5px;letter-spacing:.2em;text-transform:uppercase}
@media (max-width:900px){.g2,.rule{grid-template-columns:1fr}}
"""
def build_mid():
    V = W("Midterm1_Matyan5_Hrachya_Aslanyan.xlsx"); c = C("mid_concl.json")
    L = liq_block(V["Խ1 Իրացվելիություն"], c["liq"]); S = stab_block(V["Խ2 Կայունություն"], c["stab"]); F = fa_block(V["Խ3 ՀՄ"], c["fa"])
    M = mat_block(V["Խ4 ՆՊ"], c["mat"]); A = lab_block(V["Խ5 Աշխատանք"], c["lab"])
    rules = V["Տվյալներ №5"]; rl = "".join(f"<div><b>{E(rules[f'A{r}'].value)}</b><span>{E(rules[f'B{r}'].value)}</span></div>" for r in range(6, 10))
    body = topbar("Midterm1_Matyan5_Hrachya_Aslanyan.xlsx", "index.html#library", "Գրադարան") + f"""
<div class="cover"><div><div class="seal">5</div><p>1-ին միջանկյալ ստուգում · Տնային առաջադրանք · 30.10.2026</p><h1>Հինգ խնդիր.<br>Մեկ ընկերություն</h1>
<p style="margin-top:18px">Հրաչյա Ասլանյան · ԻՏ-447 · Մատյանի № 5</p></div></div>
<div class="wrap"><div class="rule">{rl}</div>
<div data-tabs><div class="tabs"><button class="on" data-tab="1">I · Իրացվելիություն</button><button data-tab="2">II · Կայունություն</button><button data-tab="3">III · Հիմնական միջոցներ</button><button data-tab="4">IV · Նյութական պաշարներ</button><button data-tab="5">V · Աշխատանք</button></div>
<div data-pane="1" class="on" id="excel"><h2>Խնդիր 1. Իրացվելիություն և վճարունակություն</h2><div class="g2"><div>{L["groups"]}</div><div class="card">{L["pairs"]}</div></div>
<h3>Գործակիցներ</h3><div class="g2"><div>{L["ratios"]}</div><div class="card">{L["gauges"]}</div></div><p class="concl">{E(c["liq"][0])}</p>
<h3>Հարց 9 · պաշարներ 42 000 (25 000 դրամով + 17 000 պարտքով)</h3><div class="g2"><div>{L["scen"]}</div><div class="card">{L["scen_chart"]}</div></div><p class="concl">{E(c["liq"][1])}</p></div>
<div data-pane="2"><h2>Խնդիր 2. Ֆինանսական կայունություն</h2><div class="g2"><div>{S["ratios"]}</div><div class="card">{S["gauges"]}</div></div><p class="concl">{E(c["stab"][0])}</p><h3>Սցենարներ</h3>{S["scen"]}<p class="concl">{E(c["stab"][1])}</p></div>
<div data-pane="3"><h2>Խնդիր 3. Հիմնական միջոցներ</h2>{F["inputs"]}<h3>Արդյունքային ցուցանիշներ</h3>{F["out"]}<div class="g2" style="margin-top:20px"><div class="card">{F["state"]}</div><div class="card">{F["wf"]}</div></div><p class="concl">{E(c["fa"][0])} {E(c["fa"][1])}</p></div>
<div data-pane="4"><h2>Խնդիր 4. Նյութական պաշարներ</h2>{M["mats"]}<h3>Ցուցանիշներ</h3>{M["out"]}<div class="g2" style="margin-top:20px"><div class="card">{M["bars"]}</div><div class="card">{M["wf"]}</div></div><p class="concl">{E(c["mat"][0])} {E(c["mat"][1])}</p></div>
<div data-pane="5"><h2>Խնդիր 5. Աշխատաժամանակ և արտադրողականություն</h2>{A["inputs"]}<h3>Վերլուծություն 1</h3><div class="g2"><div>{A["a1"]}</div><div class="card">{A["wf1"]}</div></div>
<h3>Վերլուծություն 2</h3>{A["a2"]}<div class="g2" style="margin-top:16px"><div>{A["f2"]}</div><div class="card">{A["wf2"]}</div></div><p class="concl">{E(c["lab"][0])} {E(c["lab"][1])}</p></div></div>
<div class="foot">H/R Studios · Excel՝ 344 բանաձև · 10 գծապատկեր · 0 սխալ</div></div>"""
    return page("gold", "1-ին միջանկյալ · Մատյան №5", body, CSS_GOLD, "1-ին միջանկյալի տնային առաջադրանք")

PAGES = {"dasi-2-3": build_hw23, "dasi-4": build_hw4, "dasi-5": build_hw5, "dasi-6": build_hw6, "midterm-1": build_mid}
if __name__ == "__main__":
    for slug, fn in PAGES.items():
        d = os.path.join(SITE, "hw", slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf8").write(fn()); print("wrote", slug)
