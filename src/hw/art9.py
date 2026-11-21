# -*- coding: utf-8 -*-
# Procedural ukiyo-e / kintsugi illustrations for lesson 9 (financial liabilities). Output: SVG files.
import os, math, random
OUT = os.path.join(os.path.dirname(__file__), "..", "site", "assets", "hw", "wave"); os.makedirs(OUT, exist_ok=True)
W, H = 1600, 900
INK, IND, IND2, IND3, FOAM, PAPER, RED, GOLD = "#1b1a24", "#1f3a68", "#2f5d8f", "#6f9cc0", "#f6efe0", "#efe3c8", "#c8102e", "#d4a537"

DEFS = f'''<defs>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 .45  0 0 0 0 .36  0 0 0 0 .2  0 0 0 .16 0"/><feComposite in2="SourceGraphic" operator="in"/><feBlend in="SourceGraphic" mode="multiply"/></filter>
<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter>
<filter id="brush" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".9 .05" numOctaves="2" seed="2" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="9"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="seig" width="80" height="40" patternUnits="userSpaceOnUse"><rect width="80" height="40" fill="{IND}"/>
{''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{IND if k % 2 else IND2}" stroke="{FOAM}" stroke-opacity=".55" stroke-width="2"/>' for cx, cy in ((0, 40), (80, 40), (40, 20), (40, 60), (0, 0), (80, 0)) for k, r in enumerate((38, 30, 22, 14, 6)))}
</pattern>
<pattern id="asa" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M30 0v60M0 30h60" stroke="{GOLD}" stroke-opacity=".18"/></pattern>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbe7a1"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#8a6510"/></linearGradient>
<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d9a8"/><stop offset=".6" stop-color="#efe3c8"/><stop offset="1" stop-color="#e7d6b4"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e1630"/><stop offset="1" stop-color="#22365e"/></linearGradient>
</defs>'''

def svg(body, bg=PAPER, grad=None):
    fill = f'url(#{grad})' if grad else bg
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">{DEFS}'
            f'<rect width="{W}" height="{H}" fill="{fill}" filter="url(#paper)"/>{body}'
            f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{INK}" stroke-width="3" opacity=".55"/></svg>')

def coin(x, y, r, rot=0, op=1):
    s = r * .32
    return (f'<g transform="translate({x} {y}) rotate({rot})" opacity="{op}"><circle r="{r}" fill="url(#gold)" stroke="#6b4c0b" stroke-width="{r*.08:.1f}"/>'
            f'<circle r="{r*.78:.1f}" fill="none" stroke="#7a560e" stroke-width="{r*.05:.1f}"/><rect x="{-s}" y="{-s}" width="{2*s}" height="{2*s}" fill="{PAPER}" stroke="#6b4c0b" stroke-width="{r*.06:.1f}"/>'
            f'<g fill="#7a560e"><rect x="{-r*.08:.1f}" y="{-r*.66:.1f}" width="{r*.16:.1f}" height="{r*.22:.1f}"/><rect x="{-r*.08:.1f}" y="{r*.44:.1f}" width="{r*.16:.1f}" height="{r*.22:.1f}"/>'
            f'<rect x="{-r*.66:.1f}" y="{-r*.08:.1f}" width="{r*.22:.1f}" height="{r*.16:.1f}"/><rect x="{r*.44:.1f}" y="{-r*.08:.1f}" width="{r*.22:.1f}" height="{r*.16:.1f}"/></g></g>')

def fuji(cx, base, w, h, col=IND, snow=FOAM):
    l, r, t = cx - w / 2, cx + w / 2, base - h
    cap = f'M{cx-w*.13} {t+h*.2} L{cx-w*.06} {t+h*.03} L{cx+w*.06} {t+h*.03} L{cx+w*.13} {t+h*.2} L{cx+w*.08} {t+h*.17} L{cx+w*.04} {t+h*.25} L{cx} {t+h*.18} L{cx-w*.05} {t+h*.27} L{cx-w*.09} {t+h*.18} Z'
    return (f'<path d="M{l} {base} Q{cx-w*.2} {t+h*.35} {cx-w*.06} {t+h*.03} L{cx+w*.06} {t+h*.03} Q{cx+w*.2} {t+h*.35} {r} {base} Z" fill="{col}" filter="url(#rough)"/>'
            f'<path d="{cap}" fill="{snow}"/>')

def sun(x, y, r, col=RED): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity=".92" filter="url(#rough)"/>'

def cloud(x, y, w, col="#f6efe0", stroke=INK):
    h = w * .18
    return (f'<g transform="translate({x} {y})" filter="url(#rough)"><path d="M0 {h} Q{w*.1} 0 {w*.3} {h*.4} Q{w*.45} {-h*.4} {w*.6} {h*.35} Q{w*.8} {-h*.2} {w} {h} Z" fill="{col}" stroke="{stroke}" stroke-width="3"/>'
            + "".join(f'<path d="M{w*.12} {h*.75+i*7} H{w*.9}" stroke="{stroke}" stroke-opacity=".35" stroke-width="2"/>' for i in range(2)) + '</g>')

def wave_band(y, amp, col, k, phase=0, foam=True, rnd=None):
    pts = [(x, y + amp * math.sin(x / k + phase) + amp * .4 * math.sin(x / (k * .37) + phase * 1.7)) for x in range(-20, W + 40, 20)]
    d = "M" + " L".join(f"{x:.0f} {yy:.1f}" for x, yy in pts) + f" L{W+40} {H} L-20 {H} Z"
    out = f'<path d="{d}" fill="{col}" filter="url(#rough)"/>'
    if foam:
        crest = "M" + " L".join(f"{x:.0f} {yy:.1f}" for x, yy in pts)
        out += f'<path d="{crest}" fill="none" stroke="{FOAM}" stroke-width="5" stroke-linecap="round" filter="url(#brush)"/>'
        for x, yy in pts[::3]:
            if rnd and rnd.random() < .55:
                out += f'<path d="M{x} {yy} q8 -14 18 -4 q-6 -2 -9 6" fill="none" stroke="{FOAM}" stroke-width="3" stroke-linecap="round"/>'
    return out

def great_curl(x, y, s, rnd):
    # stylised Hokusai-like curl: spiral body + foam claws
    body = (f'<path d="M{x} {y+s*.9} C{x-s*.2} {y+s*.2} {x+s*.05} {y-s*.55} {x+s*.6} {y-s*.6} C{x+s*1.05} {y-s*.62} {x+s*1.2} {y-s*.2} {x+s*1.05} {y+s*.05} '
            f'C{x+s*.95} {y-s*.2} {x+s*.7} {y-s*.25} {x+s*.55} {y-s*.05} C{x+s*.4} {y+s*.18} {x+s*.5} {y+s*.55} {x+s*.95} {y+s*.9} Z" fill="url(#seig)" stroke="{INK}" stroke-width="4" filter="url(#rough)"/>')
    claws = ""
    for i in range(14):
        a = math.pi * (1.05 + i * .085); r = s * .62
        cx, cy = x + s * .6 + r * math.cos(a) * .95, y - s * .02 + r * math.sin(a) * .95
        claws += f'<path d="M{cx:.0f} {cy:.0f} q{-10+rnd.random()*6:.0f} -18 {8+rnd.random()*6:.0f} -24 q-4 10 4 14 q-6 -2 -10 8" fill="{FOAM}" stroke="{INK}" stroke-width="2"/>'
    rim = f'<path d="M{x+s*.08} {y+s*.1} C{x+s*.15} {y-s*.45} {x+s*.7} {y-s*.75} {x+s*1.1} {y-s*.2}" fill="none" stroke="{FOAM}" stroke-width="16" stroke-linecap="round" filter="url(#brush)"/>'
    return body + rim + claws

def sakura_branch(x, y, s, rnd, flip=1):
    d = f'M{x} {y} C{x+flip*s*.3} {y+s*.05} {x+flip*s*.5} {y+s*.25} {x+flip*s*.9} {y+s*.2}'
    out = f'<path d="{d}" stroke="{INK}" stroke-width="{s*.035:.0f}" fill="none" stroke-linecap="round" filter="url(#rough)"/>'
    out += f'<path d="M{x+flip*s*.45} {y+s*.12} q{flip*s*.1} {s*.15} {flip*s*.28} {s*.22}" stroke="{INK}" stroke-width="{s*.02:.0f}" fill="none"/>'
    for i in range(16):
        t = rnd.random(); bx = x + flip * s * (.1 + .85 * t) + rnd.uniform(-20, 20); by = y + s * (.02 + .22 * t) + rnd.uniform(-30, 40)
        out += flower(bx, by, rnd.uniform(11, 19), rnd.uniform(0, 72))
    return out

def flower(x, y, r, rot):
    pet = "".join(f'<ellipse cx="0" cy="{-r*.62:.1f}" rx="{r*.42:.1f}" ry="{r*.62:.1f}" transform="rotate({k*72})"/>' for k in range(5))
    return f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" fill="#f2b8c6" stroke="#b8536b" stroke-width="1.2">{pet}<circle r="{r*.22:.1f}" fill="{RED}" stroke="none"/></g>'

def hanko(x, y, s, txt, rot=-6):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="{s*.08}" fill="{RED}" filter="url(#rough)"/>'
            f'<rect x="{-s*.4}" y="{-s*.4}" width="{s*.8}" height="{s*.8}" fill="none" stroke="{PAPER}" stroke-width="{s*.05}"/>'
            f'<text y="{s*.14}" text-anchor="middle" font-family="Noto Serif Armenian,serif" font-weight="700" font-size="{s*.36}" fill="{PAPER}">{txt}</text></g>')

def crane(x, y, s, col=PAPER):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{col}" stroke="{INK}" stroke-width="1.5"><path d="M0 0 C-40 -30 -90 -40 -140 -20 C-90 -15 -50 -5 -10 10 Z"/>'
            f'<path d="M0 0 C40 -40 90 -60 150 -50 C100 -30 60 -10 12 12 Z"/><path d="M-10 6 C10 0 40 2 70 14 L95 4 L78 18 C50 20 20 22 -10 16 Z"/><circle cx="92" cy="6" r="4" fill="{RED}" stroke="none"/>'
            f'<path d="M-10 14 L-60 30" stroke="{INK}" stroke-width="2"/></g>')

def lantern(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})"><line x1="0" y1="-60" x2="0" y2="-30" stroke="{INK}" stroke-width="2"/><rect x="-16" y="-32" width="32" height="6" fill="{INK}"/>'
            f'<ellipse cx="0" cy="0" rx="26" ry="30" fill="{RED}" filter="url(#glow)"/>' + "".join(f'<path d="M-26 {k} Q0 {k+4} 26 {k}" stroke="#7a0a1b" fill="none"/>' for k in (-18, -6, 6, 18)) +
            f'<rect x="-16" y="27" width="32" height="6" fill="{INK}"/></g>')

def temple_bank(cx, base, s):
    w = 520 * s; h = 300 * s; top = base - h
    cols = "".join(f'<rect x="{cx-w/2+40*s+i*(w-80*s)/5:.0f}" y="{top+70*s:.0f}" width="{26*s:.0f}" height="{h-110*s:.0f}" fill="{RED}" stroke="{INK}" stroke-width="3"/>' for i in range(6))
    roof = f'<path d="M{cx-w/2-80*s} {top+70*s} Q{cx-w/2} {top+30*s} {cx-w/2+30*s} {top+20*s} L{cx+w/2-30*s} {top+20*s} Q{cx+w/2} {top+30*s} {cx+w/2+80*s} {top+70*s} Z" fill="{INK}" filter="url(#rough)"/>'
    roof2 = f'<path d="M{cx-w/3} {top+20*s} Q{cx-w/4} {top-40*s} {cx} {top-60*s} Q{cx+w/4} {top-40*s} {cx+w/3} {top+20*s} Z" fill="{IND}" stroke="{INK}" stroke-width="3" filter="url(#rough)"/>'
    steps = "".join(f'<rect x="{cx-w/2-20*s-i*20*s:.0f}" y="{base-40*s+i*14*s:.0f}" width="{w+40*s+i*40*s:.0f}" height="{14*s:.0f}" fill="#cbb994" stroke="{INK}" stroke-width="2"/>' for i in range(3))
    return roof2 + roof + cols + f'<rect x="{cx-w/2+20*s}" y="{top+60*s}" width="{w-40*s}" height="{14*s}" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>' + steps + coin(cx, top - 10 * s, 34 * s)

def torii(x, base, s):
    return (f'<g transform="translate({x} {base}) scale({s})" filter="url(#rough)"><rect x="-90" y="-240" width="22" height="240" fill="{RED}"/><rect x="68" y="-240" width="22" height="240" fill="{RED}"/>'
            f'<rect x="-120" y="-200" width="240" height="18" fill="{RED}"/><path d="M-150 -258 Q0 -236 150 -258 L140 -236 Q0 -220 -140 -236 Z" fill="{INK}"/></g>')

def bowl(cx, cy, s, rnd):
    w = 520 * s; h = 260 * s
    shape = f'M{cx-w/2} {cy} Q{cx-w/2} {cy+h} {cx} {cy+h} Q{cx+w/2} {cy+h} {cx+w/2} {cy} Z'
    out = f'<ellipse cx="{cx}" cy="{cy+h+18*s}" rx="{w*.42}" ry="{18*s}" fill="{INK}" opacity=".25"/><path d="{shape}" fill="{IND}" stroke="{INK}" stroke-width="4" filter="url(#rough)"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{40*s}" fill="#13284a" stroke="{INK}" stroke-width="4"/><path d="M{cx-w*.42} {cy+h*.25} Q{cx} {cy+h*.4} {cx+w*.42} {cy+h*.25}" stroke="{IND3}" stroke-width="6" fill="none" opacity=".6"/>'
    for k in range(4):
        x0 = cx - w * .45 + rnd.random() * w * .9; y0 = cy + 10; pts = [(x0, y0)]
        for j in range(6): pts.append((pts[-1][0] + rnd.uniform(-40, 40) * s, pts[-1][1] + rnd.uniform(25, 45) * s))
        d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts if b < cy + h * .95)
        out += f'<path class="kin" d="{d}" stroke="url(#gold)" stroke-width="{6*s:.1f}" fill="none" stroke-linejoin="round" filter="url(#glow)"/>'
    return out

def scroll_ledger(x, y, w, h, rnd):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f8f0dc" stroke="{INK}" stroke-width="3"/><rect x="{x-24}" y="{y-12}" width="24" height="{h+24}" rx="10" fill="{INK}"/><rect x="{x+w}" y="{y-12}" width="24" height="{h+24}" rx="10" fill="{INK}"/>'
    cols = 9
    for i in range(cols):
        cx = x + w - 60 - i * (w - 100) / (cols - 1)
        out += f'<line x1="{cx+30}" y1="{y+30}" x2="{cx+30}" y2="{y+h-30}" stroke="{RED}" stroke-opacity=".35"/>'
        yy = y + 50
        while yy < y + h - 60:
            L = rnd.uniform(14, 40); out += f'<path d="M{cx} {yy} q{rnd.uniform(-4,4):.0f} {L/2:.0f} 0 {L:.0f}" stroke="{INK}" stroke-width="{rnd.uniform(4,8):.0f}" stroke-linecap="round" fill="none"/>'; yy += L + rnd.uniform(10, 26)
    return out

def enso(cx, cy, r, col=INK, w=34):
    return (f'<path d="M{cx+r*math.cos(-1.2):.0f} {cy+r*math.sin(-1.2):.0f} A{r} {r} 0 1 1 {cx+r*math.cos(-1.55):.0f} {cy+r*math.sin(-1.55):.0f}" stroke="{col}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round" filter="url(#brush)" opacity=".92"/>')

def rain_coins(rnd, n, y0, y1, x0=0, x1=W, rmin=16, rmax=36):
    return "".join(coin(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(rmin, rmax), rnd.uniform(0, 90), rnd.uniform(.75, 1)) for _ in range(n))

def chart_ridge(x0, x1, base, rnd):
    pts = []; y = base
    for i, x in enumerate(range(x0, x1 + 1, 40)):
        y = base - (x - x0) * .32 + rnd.uniform(-35, 35); pts.append((x, y))
    d = "M" + " L".join(f"{a} {b:.0f}" for a, b in pts)
    return (f'<path d="{d} L{x1} {base+200} L{x0} {base+200} Z" fill="{IND}" opacity=".9" filter="url(#rough)"/>'
            f'<path d="{d}" stroke="url(#gold)" stroke-width="9" fill="none" stroke-linejoin="round" filter="url(#glow)"/>' +
            "".join(f'<circle cx="{a}" cy="{b:.0f}" r="8" fill="{RED}" stroke="{PAPER}" stroke-width="3"/>' for a, b in pts[::4]))

def build():
    S = {}
    r = random.Random(1)
    S["00"] = svg(sun(1210, 250, 120) + fuji(1180, 640, 620, 300) + cloud(860, 210, 300) + wave_band(640, 18, IND2, 90, 0, True, r)
                  + great_curl(150, 330, 560, r) + wave_band(720, 26, "url(#seig)", 120, 1.3, True, r) + wave_band(810, 22, IND, 70, 2.1, True, r)
                  + rain_coins(r, 9, 260, 560, 320, 900, 18, 30) + hanko(1460, 790, 110, "ՖՊ"))
    r = random.Random(2)
    S["01"] = svg(sun(300, 220, 90) + cloud(120, 330, 380) + cloud(1050, 170, 320) + fuji(1050, 760, 900, 460, IND2) + chart_ridge(80, 1520, 760, r)
                  + wave_band(800, 14, IND, 80, .4, True, r) + hanko(1450, 120, 96, "9"), grad="dawn")
    r = random.Random(3)
    S["02"] = svg(sun(1220, 210, 110, "#f4e6b6") + "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,500):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#f6efe0" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(120))
                  + fuji(400, 700, 900, 360, "#2b4475", "#d9e3f0") + crane(860, 300, 1.4) + crane(1050, 420, .8) + crane(650, 460, .6)
                  + "".join(lantern(220 + i * 300, 640 + (i % 2) * 30, 1.1) for i in range(5)) + wave_band(760, 16, "#122440", 70, 1, True, r), grad="night")
    r = random.Random(4)
    S["03"] = svg(enso(800, 420, 330, INK, 46) + bowl(800, 380, 1.15, r) + rain_coins(r, 6, 120, 260, 260, 1340, 22, 34) + hanko(1420, 760, 110, "ՀԱ") + hanko(180, 140, 80, "Ո", 8))
    r = random.Random(5)
    S["04"] = svg(sun(1300, 200, 100) + wave_band(560, 12, IND3, 120, 0, False) + wave_band(620, 14, IND2, 90, 1, True, r) + wave_band(700, 18, "url(#seig)", 110, 2, True, r)
                  + rain_coins(r, 10, 600, 860, 100, 1500, 16, 28) + sakura_branch(-40, 40, 1100, r) + sakura_branch(1640, 520, 700, r, -1)
                  + "".join(flower(r.uniform(0, W), r.uniform(200, 860), r.uniform(8, 14), r.uniform(0, 72)) for _ in range(26)))
    r = random.Random(6)
    S["05"] = svg(sun(800, 230, 140) + cloud(80, 300, 360) + cloud(1170, 260, 360) + temple_bank(800, 720, 1.25) + torii(230, 780, 1.1) + torii(1370, 780, 1.1)
                  + wave_band(800, 12, IND, 90, .5, True, r) + rain_coins(r, 5, 120, 320, 300, 1300, 18, 26))
    r = random.Random(7)
    S["06"] = svg(scroll_ledger(170, 150, 1260, 560, r) + hanko(1250, 640, 120, "ՀԱ") + hanko(1120, 660, 90, "ԻՏ", 5) + coin(320, 780, 46, 12) + coin(410, 800, 34, 40) + sakura_branch(1700, 40, 600, r, -1))
    r = random.Random(8)
    S["07"] = svg(sun(800, 450, 300) + enso(800, 450, 360, INK, 40) + wave_band(720, 20, "url(#seig)", 110, .2, True, r) + wave_band(800, 18, IND, 80, 1.4, True, r) + rain_coins(r, 12, 120, 620, 200, 1400, 14, 30))
    r = random.Random(9)
    S["08"] = svg("".join(f'<rect x="{i*W/4}" y="0" width="{W/4}" height="{H}" fill="url(#asa)" stroke="{INK}" stroke-opacity=".4" stroke-width="3"/>' for i in range(4))
                  + sun(1200, 260, 120, GOLD) + great_curl(260, 360, 460, r) + fuji(1150, 700, 700, 320) + wave_band(720, 22, "url(#seig)", 100, 0, True, r) + hanko(160, 120, 90, "10"), bg="#e9d9b5")
    r = random.Random(10)
    S["09"] = svg(cloud(120, 160, 420) + cloud(1060, 120, 420) + "".join(coin(400 + i * 200, 650 - (i % 2) * 40 - i * 60, 70 - i * 4, i * 15) for i in range(5))
                  + chart_ridge(200, 1400, 820, r) + hanko(1460, 790, 100, "Δ"), grad="dawn")
    for k, v in S.items():
        open(os.path.join(OUT, f"{k}.svg"), "w", encoding="utf8").write(v)
    print("art", len(S))

if __name__ == "__main__":
    build()
