# -*- coding: utf-8 -*-
# Lesson 9 (teacher's topic 10) — financial liabilities. Theme: UKIYO-E & KINTSUGI («Ալիք և ոսկի»).
import os, sys, math, random, openpyxl
sys.path.insert(0, os.path.dirname(__file__))
import hwpage as H
import hwpage2 as P
from hwpage import E, n, table, SITE

XL = "Tema10_Finansakan_partavorutyunner_Hrachya_Aslanyan.xlsx"
ART = "../../assets/hw/wave"
INK, IND, IND2, IND3, PAPER, RED, GOLD = "#1b1a24", "#1f3a68", "#2f5d8f", "#8fb3d1", "#efe3c8", "#c8102e", "#d4a537"
ARM = "ԱԲԳԴԵԶԷԸԹԺ"

CSS = r"""
:root{--ink:#1b1a24;--ind:#1f3a68;--ind2:#2f5d8f;--ind3:#8fb3d1;--paper:#efe3c8;--paper2:#f7efdc;--red:#c8102e;--gold:#d4a537}
html,body{overflow-x:clip}
body{background:var(--paper);color:var(--ink);font-family:'Noto Serif Armenian',Georgia,serif;font-size:16px}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.5;background:
 radial-gradient(rgba(120,90,40,.09) 1px,transparent 1.2px) 0 0/4px 4px,radial-gradient(ellipse at 20% 0%,rgba(212,165,55,.18),transparent 60%),radial-gradient(ellipse at 100% 100%,rgba(31,58,104,.12),transparent 55%)}
.num,b[data-count],.kv b,table td{font-family:'Zen Old Mincho','Noto Serif Armenian',serif;font-variant-numeric:tabular-nums}
.topbar{background:rgba(239,227,200,.9);backdrop-filter:blur(8px);border-bottom:2px solid var(--ink);font-family:'Noto Sans Armenian'}
.topbar a.b{border:1.5px solid var(--ink);color:var(--ink)}.topbar a.x{background:var(--red);color:#fff;border-color:var(--red)}
#petals{position:fixed;inset:0;z-index:30;pointer-events:none}
/* ---------- curtain: unrolling scroll ---------- */
.cur{background:rgba(20,18,26,.94)}
.cur .pp{position:relative;width:min(760px,86vw);height:min(440px,62vh);background:var(--paper2);clip-path:inset(0 50% 0 50%);animation:unr 1.25s cubic-bezier(.7,0,.2,1) .15s forwards;
 display:grid;place-items:center;box-shadow:0 40px 90px rgba(0,0,0,.5)}
.cur .pp::before{content:"";position:absolute;inset:14px;border:2px solid var(--ink);opacity:.6}
@keyframes unr{to{clip-path:inset(0 0 0 0)}}
.cur .rl{position:absolute;top:50%;width:26px;height:min(480px,68vh);margin-top:calc(min(480px,68vh)/-2);border-radius:12px;background:linear-gradient(90deg,#000,#3a3442 50%,#000);left:calc(50% - 13px);z-index:2}
.cur .rl.a{animation:rla 1.25s cubic-bezier(.7,0,.2,1) .15s forwards}.cur .rl.b{animation:rlb 1.25s cubic-bezier(.7,0,.2,1) .15s forwards}
@keyframes rla{to{transform:translateX(calc(min(760px,86vw)/-2 - 13px))}}@keyframes rlb{to{transform:translateX(calc(min(760px,86vw)/2 + 13px))}}
.cur .ct{text-align:center;position:relative}.cur .ct small{display:block;font:600 12px 'Noto Sans Armenian';letter-spacing:.5em;color:var(--red)}
.cur .ct b{display:block;font:900 clamp(40px,7vw,84px)/1 'Noto Serif Armenian';margin:10px 0}
.cur .hk{position:absolute;right:8%;bottom:12%;width:92px;height:92px;background:var(--red);color:#fff;display:grid;place-items:center;font:800 34px 'Noto Serif Armenian';border-radius:8px;
 transform:scale(3) rotate(-25deg);opacity:0;animation:stamp .45s cubic-bezier(.3,1.6,.5,1) 1.35s forwards;box-shadow:inset 0 0 0 6px var(--red),inset 0 0 0 9px #fff}
@keyframes stamp{to{transform:scale(1) rotate(-8deg);opacity:1}}
/* ---------- hero ---------- */
.hero{min-height:100vh;align-items:center;color:var(--ink);background:var(--paper)}
.hero .bgart{position:absolute;inset:-30px;z-index:0;will-change:transform;transition:transform .25s ease-out}.hero .bgart img{width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 8s ease-out}body.ready .hero .bgart img{transform:scale(1)}
.hero::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(239,227,200,.97) 0%,rgba(239,227,200,.85) 40%,rgba(239,227,200,0) 72%)}
.hero .inner{max-width:1240px;margin:0 auto;padding:120px 20px 130px;position:relative;z-index:3}
.vtag{position:absolute;right:28px;top:110px;z-index:4;writing-mode:vertical-rl;font:700 14px 'Noto Sans Armenian';letter-spacing:.3em;color:#fff;background:var(--red);padding:16px 8px;box-shadow:4px 4px 0 var(--ink)}
.kick9{font:600 13px 'Noto Sans Armenian';letter-spacing:.3em;color:var(--red);text-transform:uppercase}
.hero h1{font:900 clamp(34px,4.9vw,74px)/1.04 'Noto Serif Armenian';margin:16px 0 8px;letter-spacing:-.01em}
.brush{display:block;clip-path:inset(0 100% 0 0);transition:clip-path 1.3s cubic-bezier(.7,0,.2,1)}body.ready .brush{clip-path:inset(-20% -60% -20% 0)}
.brush:nth-child(2){transition-delay:.35s}.brush:nth-child(3){transition-delay:.7s}.brush em{font-style:normal;color:var(--red)}
.uline{width:min(520px,80%);height:26px;margin:0 0 16px;display:block}.uline path{stroke-dasharray:700;stroke-dashoffset:700;transition:stroke-dashoffset 1.4s ease 1.2s}body.ready .uline path{stroke-dashoffset:0}
.hero p.lead{max-width:560px;font:400 18px/1.75 'Noto Sans Armenian';color:#3a3442}
.seals{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.seals a{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font:600 14px 'Noto Sans Armenian';color:var(--ink);background:var(--paper2);border:2px solid var(--ink);padding:9px 14px;box-shadow:3px 3px 0 var(--ink);transition:transform .2s,box-shadow .2s}
.seals a:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--red)}.seals a i{font-style:normal;background:var(--red);color:#fff;width:24px;height:24px;display:grid;place-items:center;font-weight:800;font-size:13px}
.seals a.x{background:var(--red);color:#fff;border-color:var(--red)}.seals a.x i{background:#fff;color:var(--red)}
.waveband{position:absolute;left:0;right:0;bottom:0;height:90px;z-index:2;overflow:hidden}.waveband svg{width:200%;height:100%;display:block;animation:wb 26s linear infinite}
.waveband.b2{height:56px}.waveband.b2 svg{animation-duration:15s;animation-direction:reverse}@keyframes wb{to{transform:translateX(-50%)}}
/* ---------- layout ---------- */
.w9{max-width:1240px;margin:0 auto;padding:0 20px}
.sec9{padding:80px 0 30px;position:relative}
.sh{display:flex;align-items:center;gap:22px;margin:0 0 26px}.sh svg.en{width:96px;height:96px;flex:none}
.sh svg.en circle{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round;stroke-dasharray:230 300;stroke-dashoffset:230;transition:stroke-dashoffset 1.4s cubic-bezier(.6,0,.2,1)}
.sh.in svg.en circle{stroke-dashoffset:0}.sh svg.en text{font:900 44px 'Noto Serif Armenian';fill:var(--red)}
.sh h2{font:900 clamp(28px,3.6vw,48px)/1.1 'Noto Serif Armenian';margin:0}.sh p{margin:6px 0 0;font:400 16px/1.6 'Noto Sans Armenian';color:#5a5160;max-width:760px}
.kin{display:block;width:100%;height:60px;margin:10px 0}.kin path{fill:none;stroke:url(#kg);stroke-width:4;stroke-linecap:round;stroke-dasharray:1800;stroke-dashoffset:1800;transition:stroke-dashoffset 2.2s cubic-bezier(.6,0,.2,1);filter:drop-shadow(0 0 4px rgba(212,165,55,.8))}
.kin.in path{stroke-dashoffset:0}
.kin path.gl{stroke:#fffbe6;stroke-width:6;stroke-dasharray:70 2400;stroke-dashoffset:0;opacity:0;filter:drop-shadow(0 0 8px #ffe9a0)}.kin.in path.gl{opacity:1;animation:glint 4.5s linear 2.2s infinite}@keyframes glint{from{stroke-dashoffset:70}to{stroke-dashoffset:-2400}}
.sh.in svg.en{animation:enrot 40s linear 1.5s infinite}@keyframes enrot{to{transform:rotate(360deg)}}.sh svg.en text{transform-box:fill-box;transform-origin:center}.sh.in svg.en text{animation:enrot 40s linear 1.5s infinite reverse}
.kpi .hk{animation:none}.kpi.in .hk{animation:restamp 6s ease-in-out 3s infinite}@keyframes restamp{0%,88%,100%{transform:scale(1) rotate(-8deg)}93%{transform:scale(1.25) rotate(-2deg)}97%{transform:scale(.95) rotate(-10deg)}}
.ic::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,transparent 40%,rgba(212,165,55,.28) 50%,transparent 60%) no-repeat;background-size:250% 100%;background-position:150% 0;transition:background-position 1s}.ic:hover::after{background-position:-50% 0}
.pn{transition:transform .35s,box-shadow .35s}.pn:hover{transform:translate(-3px,-3px);box-shadow:10px 10px 0 var(--red)}
.byobu figure img{transition:filter .5s}.byobu figure:hover img{filter:saturate(1.2)}
.pn{background:var(--paper2);border:2px solid var(--ink);box-shadow:6px 6px 0 rgba(27,26,36,.85);padding:20px;position:relative}
.pn h3{margin:0 0 12px;font:800 18px 'Noto Serif Armenian';display:flex;justify-content:space-between;gap:10px;align-items:baseline;flex-wrap:wrap}.pn h3 small{font:500 12.5px 'Noto Sans Armenian';color:#7a6f7e}
.pn::after{content:"";position:absolute;right:-2px;top:-2px;width:0;height:0;border-top:22px solid var(--red);border-left:22px solid transparent}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:26px}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.mt{margin-top:26px}
/* KPI hanko cards */
.kpi{position:relative;background:var(--paper2);border:2px solid var(--ink);padding:22px 18px 18px;overflow:hidden;box-shadow:6px 6px 0 var(--ink)}
.kpi small{font:600 12px 'Noto Sans Armenian';letter-spacing:.14em;text-transform:uppercase;color:#6a5f6e}.kpi b{display:block;font:900 clamp(26px,3vw,40px) 'Zen Old Mincho','Noto Serif Armenian';margin:8px 0 4px}
.kpi em{font:600 13px 'Noto Sans Armenian';font-style:normal}.kpi .hk{position:absolute;right:12px;top:12px;width:46px;height:46px;background:var(--red);color:#fff;display:grid;place-items:center;font:800 13px 'Noto Sans Armenian';border-radius:5px;box-shadow:inset 0 0 0 3px var(--red),inset 0 0 0 5px #fff;transform:scale(2.6) rotate(-30deg);opacity:0;transition:all .45s cubic-bezier(.3,1.6,.5,1)}
.kpi.in .hk{transform:scale(1) rotate(-8deg);opacity:1;transition-delay:calc(var(--i)*.15s + .4s)}.kpi .hk.g{background:var(--ind);box-shadow:inset 0 0 0 3px var(--ind),inset 0 0 0 5px #fff}
.kpi::before{content:"";position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,var(--red),var(--gold));transition:width 1.2s .3s}.kpi.in::before{width:100%}
.up{color:#1d7a3e}.dn{color:var(--red)}
/* chapter art */
.chap{height:78vh;color:#fff}.chap .chi{inset:-28% 0;background-size:cover!important;background-position:center!important}.chap::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(27,26,36,.1),rgba(27,26,36,.5))}
.chc{position:relative;z-index:2}.chap .chn{font-family:'Noto Serif Armenian';font-weight:900;color:var(--red);text-shadow:0 6px 30px rgba(0,0,0,.3);-webkit-text-stroke:3px #fff;paint-order:stroke fill}
.chap h2{font:900 clamp(30px,4.6vw,60px) 'Noto Serif Armenian';text-shadow:0 4px 18px rgba(0,0,0,.55)}.chap p{font:500 17px 'Noto Sans Armenian';text-shadow:0 2px 10px rgba(0,0,0,.7)}
/* tables */
table{font:400 14.5px 'Noto Sans Armenian';color:var(--ink)}thead th{font:700 12px 'Noto Sans Armenian';letter-spacing:.06em;text-transform:uppercase;border-bottom:2px solid var(--ink);color:var(--red);white-space:nowrap}
tbody td{border-bottom:1px dashed rgba(27,26,36,.25)}tbody td:first-child{font-family:'Noto Sans Armenian'}tbody tr:hover{background:rgba(212,165,55,.14)}
code{color:var(--ind);font:700 12.5px 'Noto Sans Armenian'}
/* charts */
.ch{overflow:visible}.ch text{font-family:'Noto Sans Armenian';fill:var(--ink)}.ch .lbl{font-size:13px}.ch .val{font:700 14px 'Zen Old Mincho','Noto Serif Armenian'}.ch .sm{font-size:11.5px;fill:#6a5f6e}.ch .val,.ch .sm,.ch .lbl{paint-order:stroke;stroke:#f7efdc;stroke-width:4px;stroke-linejoin:round}
.ch .arc{transition:stroke-dashoffset 1.6s cubic-bezier(.6,0,.2,1);transition-delay:var(--d,0s)}.ch.play .arc{stroke-dashoffset:0!important}
.ch .wipe{transition:transform 2s cubic-bezier(.6,0,.2,1) .2s;transform-box:fill-box;transform-origin:right}.ch.play .wipe{transform:scaleX(0)}
.ch .ndl{transition:transform 1.8s cubic-bezier(.3,1.3,.5,1) .3s}
.ch .pop{opacity:0;transition:opacity .6s;transition-delay:var(--d,1s)}.ch.play .pop{opacity:1}
.ch .hb{transform-box:fill-box;transform-origin:left;transform:scaleX(0);transition:transform 1.3s cubic-bezier(.6,0,.2,1);transition-delay:var(--d,0s)}.ch.play .hb{transform:none}
.leg{display:flex;gap:16px;flex-wrap:wrap;font:500 13px 'Noto Sans Armenian';margin-top:8px}.leg i{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-2px;border:1.5px solid var(--ink)}
/* indicator cards */
.ic{background:var(--paper2);border:2px solid var(--ink);padding:16px;position:relative;transition:transform .3s,box-shadow .3s}.ic:hover{transform:translateY(-4px) rotate(-.4deg);box-shadow:6px 8px 0 var(--ink)}
.ic code{font-size:14px;color:var(--red)}.ic h4{margin:4px 90px 10px 0;font:600 14px/1.35 'Noto Sans Armenian';min-height:38px}
.ic .kv{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.ic .kv b{font-size:22px}.ic .kv s{text-decoration:none;color:#8a8090;font-size:15px}
.ic .vb{display:inline-block;margin-top:10px;font:700 12px 'Noto Sans Armenian';padding:4px 9px;color:#fff;background:var(--ink)}.ic .vb.good{background:#1d7a3e}.ic .vb.bad{background:var(--red)}.ic .vb.neu{background:var(--ind2)}
.ic svg{position:absolute;right:12px;top:12px;width:76px;height:38px}
.ic svg path{stroke-dasharray:90;stroke-dashoffset:90;transition:stroke-dashoffset 1.2s .4s}.ic.in svg path{stroke-dashoffset:0}
/* scroll (kakemono) conclusions */
.kake{position:relative;padding:46px 40px;background:var(--paper2);box-shadow:0 30px 60px rgba(0,0,0,.22);border-left:2px solid var(--ink);border-right:2px solid var(--ink)}
.kake .rod{position:absolute;left:-22px;right:-22px;height:22px;border-radius:11px;background:linear-gradient(180deg,#000,#3a3442 50%,#000);z-index:2}.kake .rod.t{top:-11px}.kake .rod.b{bottom:-11px}
.kake .bdy{clip-path:inset(0 0 100% 0);transition:clip-path 1.8s cubic-bezier(.6,0,.2,1) .2s}.kake.in .bdy{clip-path:inset(0 0 0 0)}
.kake p{font:400 15.5px/1.85 'Noto Sans Armenian';margin:0 0 14px;padding-left:36px;position:relative}.kake p::before{content:attr(data-k);position:absolute;left:0;top:3px;width:24px;height:24px;background:var(--red);color:#fff;display:grid;place-items:center;font:800 12px 'Noto Serif Armenian'}
.kake h3{font:900 28px 'Noto Serif Armenian';margin:0 0 18px;text-align:center}.kake h3::after{content:"";display:block;width:80px;height:4px;background:var(--red);margin:10px auto 0}
/* kintsugi notes */
.kgrid{display:grid;grid-template-columns:420px 1fr;gap:30px;align-items:center}.kgrid img{width:100%;border:2px solid var(--ink);box-shadow:8px 8px 0 var(--gold)}
.knote{border-left:5px solid var(--gold);background:linear-gradient(90deg,rgba(212,165,55,.18),transparent);padding:12px 16px;margin:0 0 12px;font:400 15px/1.75 'Noto Sans Armenian'}
.knote b{color:var(--ind)}
/* byobu gallery */
.byobu{display:flex;overflow-x:auto;padding:40px 20px 60px;perspective:1600px;scroll-snap-type:x mandatory;scrollbar-width:thin}
.byobu figure{flex:none;width:min(380px,72vw);margin:0;scroll-snap-align:center;transform-style:preserve-3d;border:3px solid var(--ink);background:var(--paper2);transition:transform .6s}
.byobu figure:nth-child(odd){transform:rotateY(14deg)}.byobu figure:nth-child(even){transform:rotateY(-14deg)}.byobu figure:hover{transform:rotateY(0) scale(1.04);z-index:2}
.byobu img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}.byobu figcaption{font:600 13px 'Noto Sans Armenian';padding:8px 12px;border-top:2px solid var(--ink);display:flex;justify-content:space-between}
.byobu figcaption i{font-style:normal;color:var(--red)}
.foot9{text-align:center;padding:50px 20px 80px;font:600 13px 'Noto Sans Armenian';letter-spacing:.25em;color:#5a5160}.foot9 .hk2{display:inline-grid;place-items:center;width:64px;height:64px;background:var(--red);color:#fff;font:900 22px 'Noto Serif Armenian';border-radius:6px;transform:rotate(-8deg);margin-bottom:16px;box-shadow:inset 0 0 0 4px var(--red),inset 0 0 0 7px #fff}
.mq{background:var(--ink);padding:16px 0}.mqt img{height:140px;border-radius:0;border:2px solid var(--paper)}
@media (max-width:980px){.g4{grid-template-columns:1fr 1fr}.g3{grid-template-columns:1fr 1fr}.kgrid{grid-template-columns:1fr}}
@media (max-width:700px){.g2,.g3{grid-template-columns:1fr}.vtag{display:none}.hero::after{background:linear-gradient(180deg,rgba(239,227,200,.92),rgba(239,227,200,.85) 70%,rgba(239,227,200,.35))}
 .hero h1{font-size:clamp(22px,6.5vw,40px);overflow-wrap:anywhere}.kake{padding:36px 20px}.sh svg.en{width:66px;height:66px}.sh{gap:14px}.pn{padding:14px}.g4{gap:12px}.kpi b{font-size:22px}.kpi .hk{width:36px;height:36px;font-size:11px}}
@media (prefers-reduced-motion:reduce){.brush{clip-path:none!important}.kake .bdy{clip-path:none}#petals{display:none}.waveband svg{animation:none}}
"""

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="kg" x1="0" x2="1"><stop offset="0" stop-color="#fbe7a1"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#8a6510"/></linearGradient>
<filter id="rgh" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
<filter id="brs" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".8 .04" numOctaves="2" seed="5" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="6"/></filter>
<pattern id="sg" width="40" height="20" patternUnits="userSpaceOnUse"><rect width="40" height="20" fill="{IND}"/>
{''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{IND if k % 2 else IND2}" stroke="#f6efe0" stroke-opacity=".5" stroke-width="1"/>' for cx, cy in ((0, 20), (40, 20), (20, 10), (20, 30), (0, 0), (40, 0)) for k, r in enumerate((19, 15, 11, 7, 3)))}<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 0" dur="6s" repeatCount="indefinite"/></pattern>
</defs></svg>'''

def kin(seed=1):
    r = random.Random(seed); x, y = 0, 30; d = f"M{x} {y}"
    while x < 1200:
        x += r.uniform(40, 110); y = max(6, min(54, y + r.uniform(-22, 22))); d += f" L{x:.0f} {y:.0f}"
    br = "".join(f'<path d="M{bx:.0f} {r.uniform(15,45):.0f} l{r.uniform(20,50):.0f} {r.uniform(-18,18):.0f} l{r.uniform(15,30):.0f} {r.uniform(-10,10):.0f}"/>' for bx in (r.uniform(100, 1100) for _ in range(4)))
    return f'<div class="w9"><svg class="kin rv" viewBox="0 0 1200 60" preserveAspectRatio="none"><path d="{d}"/>{br}<path class="gl" d="{d}"/></svg></div>'

def sh(i, title, sub=""):
    return (f'<div class="sh rv"><svg class="en" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" transform="rotate(-60 50 50)"/><text x="50" y="66" text-anchor="middle">{ARM[i]}</text></svg>'
            f'<div><h2>{E(title)}</h2>{f"<p>{sub}</p>" if sub else ""}</div></div>')

def pn(title, sub, body, cls=""): return f'<div class="pn rv {cls}"><h3>{E(title)}<small>{E(sub)}</small></h3>{body}</div>'
def fm(v, d=0): return n(v, d)
def pc(v, d=2): return n(v * 100, d) + "%"

# ---------------- charts ----------------
def tide(pts, labels):
    w, h, L, R, T, B = 700, 340, 60, 40, 40, 290
    xs = [L + i * (w - L - R) / (len(labels) - 1) for i in range(len(labels))]
    mx = max(a + b for a, b, c in pts) * 1.15; Y = lambda v: B - v / mx * (B - T)
    nc = [Y(a) for a, b, c in pts]; tot = [Y(a + b) for a, b, c in pts]; bk = [Y(c) for a, b, c in pts]
    def area(top, bot): return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in zip(xs, top)) + " L" + " L".join(f"{x:.0f} {y:.0f}" for x, y in reversed(list(zip(xs, bot)))) + " Z"
    g = "".join(f'<line x1="{L}" x2="{w-R}" y1="{Y(v):.0f}" y2="{Y(v):.0f}" stroke="#000" stroke-opacity=".08"/><text class="sm" x="{L-8}" y="{Y(v)+4:.0f}" text-anchor="end">{v//1000:.0f}k</text>' for v in range(0, int(mx), 50000))
    out = f'<svg class="ch" viewBox="0 0 {w} {h}">{g}<path d="{area(nc, [B]*3)}" fill="url(#sg)" stroke="{INK}" stroke-width="2" filter="url(#rgh)"/><path d="{area(tot, nc)}" fill="{IND3}" stroke="{INK}" stroke-width="2" filter="url(#rgh)"/>'
    out += '<path d="M' + " L".join(f"{x:.0f} {y:.0f}" for x, y in zip(xs, bk)) + f'" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="10 6"/>'
    for i, (x, (a, b, c)) in enumerate(zip(xs, pts)):
        out += (f'<g class="pop" style="--d:{1.2+i*.25}s"><circle cx="{x:.0f}" cy="{tot[i]:.0f}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><text class="val" x="{x:.0f}" y="{tot[i]-14:.0f}" text-anchor="{"start" if i==0 else "end" if i==len(pts)-1 else "middle"}">{fm(a+b)}</text>'
                f'<circle cx="{x:.0f}" cy="{bk[i]:.0f}" r="6" fill="{RED}"/><text class="sm" x="{x:.0f}" y="{bk[i]+24:.0f}" text-anchor="{"start" if i==0 else "end" if i==len(pts)-1 else "middle"}" style="fill:{RED};font-weight:700">ԲՎ {fm(c)}</text></g>'
                f'<text class="lbl" x="{x:.0f}" y="{B+24}" text-anchor="middle">{E(labels[i])}</text>')
    out += f'<rect class="wipe" x="{L-4}" y="0" width="{w-L-R+44}" height="{B+2}" style="fill:#f7efdc"/></svg>'
    return out + f'<div class="leg"><span><i style="background:{IND}"></i>Ոչ ընթացիկ ՖՊ</span><span><i style="background:{IND3}"></i>Ընթացիկ ՖՊ</span><span><i style="background:{RED};border-color:{RED}"></i>Բանկային վարկեր</span></div>'

def steps_chart(steps, d=0, h=320, unit=""):
    w, L, R, T, B = 640, 20, 20, 40, h - 50
    run = 0; bars = []
    for lab, kind, v in steps:
        if kind == "tot": bars.append((lab, 0, v, kind)); run = v
        else: bars.append((lab, run, run + v, kind)); run += v
    mx = max(max(a, b) for _, a, b, _ in bars) * 1.15; mn = min(0, min(min(a, b) for _, a, b, _ in bars))
    Y = lambda v: B - (v - mn) / (mx - mn) * (B - T)
    gw = (w - L - R) / len(bars); bw = gw * .6; out = f'<svg class="ch" viewBox="0 0 {w} {h}"><line x1="{L}" x2="{w-R}" y1="{Y(0):.0f}" y2="{Y(0):.0f}" stroke="{INK}" stroke-width="2"/>'
    for i, (lab, a, b, kind) in enumerate(bars):
        x = L + i * gw + (gw - bw) / 2; y1, y2 = Y(max(a, b)), Y(min(a, b)); col = {"tot": "url(#sg)", "pos": GOLD, "neg": RED}[kind]
        sign = "+" if kind == "pos" else "−" if kind == "neg" else ""
        out += (f'<rect class="gr" style="--d:{i*.25}s" x="{x:.0f}" y="{y1:.0f}" width="{bw:.0f}" height="{max(2,y2-y1):.0f}" rx="{min(10,bw/5):.0f}" fill="{col}" stroke="{INK}" stroke-width="2.5" filter="url(#rgh)"/>'
                f'<text class="val pop" style="--d:{.8+i*.2}s" x="{x+bw/2:.0f}" y="{y1-10:.0f}" text-anchor="middle">{sign}{n(abs(b-a), d)}{unit}</text>'
                f'<text class="lbl" x="{x+bw/2:.0f}" y="{B+22}" text-anchor="middle">{E(lab)}</text>')
        if i < len(bars) - 1: out += f'<line x1="{x+bw:.0f}" x2="{x+gw:.0f}" y1="{Y(b):.0f}" y2="{Y(b):.0f}" stroke="{INK}" stroke-dasharray="4 4"/>'
    return out + "</svg>"

def enso_ring(parts, center_top, center_bot, size=260):
    c = size / 2; r = size * .36; tot = sum(p[0] for p in parts); acc = 0; out = f'<svg class="ch" viewBox="0 0 {size} {size}">'
    out += f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{INK}" stroke-opacity=".08" stroke-width="{size*.14:.0f}"/>'
    for i, (v, col) in enumerate(parts):
        p = v / tot * 100
        out += (f'<circle class="arc" style="--d:{i*.5}s;stroke-dashoffset:{p:.2f}" cx="{c}" cy="{c}" r="{r}" pathLength="100" fill="none" stroke="{col}" stroke-width="{size*.14:.0f}" '
                f'stroke-dasharray="{p:.2f} 100" transform="rotate({-90+acc*3.6:.1f} {c} {c})" filter="url(#brs)"/>')
        acc += p
    out += (f'<text x="{c}" y="{c+4}" text-anchor="middle" class="val" style="font-size:{size*.1:.0f}px">{center_top}</text>'
            f'<text x="{c}" y="{c+size*.1:.0f}" text-anchor="middle" class="sm">{E(center_bot)}</text></svg>')
    return out

def fan(title, items, vmax, unit="օր"):
    w, h, cx, cy, R = 360, 210, 180, 195, 165
    ribs = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx+R*math.cos(math.pi*(1-k/12)):.0f}" y2="{cy-R*math.sin(math.pi*(1-k/12)):.0f}" stroke="{INK}" stroke-opacity=".3"/>' for k in range(13))
    out = (f'<svg class="ch" viewBox="0 0 {w} {h+16}"><path d="M{cx-R} {cy} A{R} {R} 0 0 1 {cx+R} {cy} L{cx+R*.28:.0f} {cy} A{R*.28:.0f} {R*.28:.0f} 0 0 0 {cx-R*.28:.0f} {cy} Z" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M{cx-R+11} {cy} A{R-11} {R-11} 0 0 1 {cx+R-11} {cy}" fill="none" stroke="url(#sg)" stroke-width="22"/>{ribs}')
    for i, (lab, v, col) in enumerate(items):
        ang = 180 * min(v, vmax) / vmax; rr = R * (.8 - i * .18)
        out += (f'<g class="ndl" style="transform-origin:{cx}px {cy}px;transform:rotate(0deg)" data-rot="{ang:.1f}"><line x1="{cx}" y1="{cy}" x2="{cx-rr:.0f}" y2="{cy}" stroke="{col}" stroke-width="{7-i*2}" stroke-linecap="round"/>'
                f'<circle cx="{cx-rr:.0f}" cy="{cy}" r="{8-i*2}" fill="{col}" stroke="{INK}" stroke-width="2"/></g>')
    out += f'<circle cx="{cx}" cy="{cy}" r="12" fill="{RED}" stroke="{INK}" stroke-width="3"/><text class="sm" x="{cx-R}" y="{cy+16}" text-anchor="middle">0</text><text class="sm" x="{cx+R}" y="{cy+16}" text-anchor="middle">{vmax}</text></svg>'
    leg = "".join(f'<span><i style="background:{col}"></i>{E(lab)} · <b class="num">{n(v,1)}</b> {unit}</span>' for lab, v, col in items)
    return f'<div style="text-align:center;font:800 15px Noto Serif Armenian;margin:10px 0 4px">{E(title)}</div>{out}<div class="leg" style="justify-content:center">{leg}</div>'

def hbars(rows, vmax, unit="%", d=2):
    w = 640; rh = 66; h = len(rows) * rh + 10; L = 200; ww = w - L - 120; out = f'<svg class="ch" viewBox="0 0 {w} {h}">'
    for i, (lab, a, b, la, lb) in enumerate(rows):
        y = 10 + i * rh
        out += (f'<text class="lbl" x="0" y="{y+30}">{E(lab)}</text>'
                f'<rect class="hb" style="--d:{i*.2}s" x="{L}" y="{y+4}" width="{max(3,ww*a/vmax):.0f}" height="20" fill="#9c8f7a" stroke="{INK}" stroke-width="1.5" filter="url(#brs)"/>'
                f'<rect class="hb" style="--d:{i*.2+.15}s" x="{L}" y="{y+28}" width="{max(3,ww*b/vmax):.0f}" height="20" fill="{RED if b>a else IND}" stroke="{INK}" stroke-width="1.5" filter="url(#brs)"/>'
                f'<text class="sm pop" style="--d:1.2s" x="{L+ww*a/vmax+8:.0f}" y="{y+19}">{E(la)} · {n(a,d)}{unit}</text><text class="val pop" style="--d:1.4s" x="{L+ww*b/vmax+8:.0f}" y="{y+44}">{E(lb)} · {n(b,d)}{unit}</text>')
    return out + "</svg>"

def tatami(rows, parts):
    w, L = 680, 40; rh = 70; h = len(rows) * rh + 70; out = f'<svg class="ch" viewBox="0 0 {w} {h}">'
    for i, (lab, vals) in enumerate(rows):
        y = 10 + i * rh; tot = sum(vals); x = L
        out += f'<text class="val" x="0" y="{y+30}">{E(lab)}</text>'
        for k, v in enumerate(vals):
            if not v: continue
            ww = (w - L - 10) * v / tot; nm, col = parts[k]
            out += (f'<rect class="hb" style="--d:{i*.3+k*.15}s" x="{x:.1f}" y="{y}" width="{ww:.1f}" height="46" fill="{col}" stroke="{INK}" stroke-width="2"/>'
                    + (f'<text class="pop" style="--d:{1+k*.1}s;font:700 12.5px Zen Old Mincho,serif;fill:{"#fff" if k in (0, 2) else INK}" x="{x+ww/2:.0f}" y="{y+28}" text-anchor="middle">{v/tot*100:.1f}%</text>' if ww > 46 else ""))
            x += ww
    leg = "".join(f'<rect x="{(k%3)*220}" y="{h-50+(k//3)*22}" width="14" height="14" fill="{col}" stroke="{INK}"/><text class="sm" x="{(k%3)*220+20}" y="{h-38+(k//3)*22}">{E(nm)}</text>' for k, (nm, col) in enumerate(parts))
    return out + leg + "</svg>"

def spark(a, b, good):
    col = "#1d7a3e" if good == "good" else RED if good == "bad" else IND2
    y0, y1 = (30, 8) if b > a else (8, 30) if b < a else (19, 19)
    return f'<svg viewBox="0 0 76 38"><path d="M4 {y0} C28 {y0} 48 {y1} 70 {y1}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/><circle cx="70" cy="{y1}" r="5" fill="{col}"/></svg>'

PETALS_JS = r"""<canvas id="petals"></canvas><script>
(function(){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.querySelectorAll('.ndl').forEach(n=>n.style.transform='rotate('+n.dataset.rot+'deg)');e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.3});
document.querySelectorAll('svg.ch,.sh,.kin,.kake,.ic,.kpi').forEach(s=>io.observe(s));
const art=document.querySelector('.hero .bgart');let my=0,mx=0,sy=0;const ap=()=>{if(art)art.style.transform='translate('+mx+'px,'+(sy*.3+my)+'px)'};
addEventListener('scroll',()=>{if(scrollY<innerHeight){sy=scrollY;ap()}},{passive:true});
if(matchMedia('(pointer:fine)').matches)addEventListener('mousemove',e=>{if(scrollY>innerHeight)return;mx=(e.clientX/innerWidth-.5)*-24;my=(e.clientY/innerHeight-.5)*-16;ap()},{passive:true});
if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;const c=document.getElementById('petals'),x=c.getContext('2d');let W,H,P=[],dpr=Math.min(2,devicePixelRatio||1);
function rs(){W=c.width=innerWidth*dpr;H=c.height=innerHeight*dpr;c.style.width=innerWidth+'px';c.style.height=innerHeight+'px'}rs();addEventListener('resize',rs);
const N=innerWidth<700?12:26;function mk(y){return{x:Math.random()*W,y:y==null?Math.random()*H:y,s:(6+Math.random()*7)*dpr,r:Math.random()*6.28,vr:(Math.random()-.5)*.04,vx:(.3+Math.random()*.8)*dpr,vy:(.5+Math.random()*1)*dpr,p:Math.random()*6.28}}
for(let i=0;i<N;i++)P.push(mk());
function petal(p){x.save();x.translate(p.x,p.y);x.rotate(p.r);x.scale(1,.6+.4*Math.sin(p.p));x.beginPath();x.moveTo(0,-p.s);x.bezierCurveTo(p.s*.9,-p.s*.6,p.s*.7,p.s*.7,0,p.s);x.bezierCurveTo(-p.s*.7,p.s*.7,-p.s*.9,-p.s*.6,0,-p.s);
x.fillStyle='rgba(242,184,198,.85)';x.fill();x.strokeStyle='rgba(184,83,107,.5)';x.stroke();x.restore()}
let run=true;document.addEventListener('visibilitychange',()=>{run=!document.hidden;if(run)requestAnimationFrame(t)});
function t(){if(!run)return;x.clearRect(0,0,W,H);for(const p of P){p.x+=p.vx+Math.sin(p.p)*.6;p.y+=p.vy;p.r+=p.vr;p.p+=.03;if(p.y>H+20||p.x>W+20)Object.assign(p,mk(-20));petal(p)}requestAnimationFrame(t)}requestAnimationFrame(t);
addEventListener('click',e=>{if(e.target.closest('a'))return;for(let i=0;i<10;i++){const p=mk(e.clientY*dpr);p.x=e.clientX*dpr;p.vx=(Math.random()-.3)*3*dpr;p.vy=(Math.random()*2+.4)*dpr;P.push(p)}if(P.length>80)P.splice(0,P.length-80)});
})();</script>"""

def waveband(cls=""):
    pts = [(x, 40 + 14 * math.sin(x / 70 * 1.0) + 6 * math.sin(x / 23)) for x in range(0, 3201, 20)]
    # make it seamless at the 1600 mark by mirroring the first half
    half = [(x, y) for x, y in pts if x <= 1600]; pts = half + [(x + 1600, y) for x, y in half[1:]]
    d = "M" + " L".join(f"{x} {y:.1f}" for x, y in pts)
    foam = "".join(f'<path d="M{x} {y:.0f} q6 -12 15 -3 q-5 -2 -7 5" fill="none" stroke="#f6efe0" stroke-width="2.4"/>' for x, y in pts[::4])
    return f'<div class="waveband {cls}"><svg viewBox="0 0 3200 90" preserveAspectRatio="none"><path d="{d} L3200 90 L0 90 Z" fill="url(#sg)" stroke="#f6efe0" stroke-width="3"/>{foam}</svg></div>'

def build_hw9():
    wb = openpyxl.load_workbook(os.path.join(SITE, "files", XL), data_only=True); a, b = wb["Ձևանմուշ · Տնային 1"], wb["Ձևանմուշ · Տնային 2"]
    g = lambda ws, r, c: ws.cell(r, c).value
    E5 = lambda r: g(a, r, 5); F6 = lambda r: g(a, r, 6); G7 = lambda r: g(a, r, 7)
    vv = lambda x, d, p, s=False: (n(x * 100, d, s) + "%") if p else n(x, d, s)
    kp = [("ՖՊ · 2025", fm(g(a, 83, 6)), g(a, 83, 6), 0, "", f'<em class="up">▼ {fm(-g(a, 83, 7))} 2024-ի համեմատ</em>', "▼", "g"),
          ("Մեկ պտույտ, օր", n(F6(70), 1), F6(70), 1, "", f'<em class="dn">▲ +{n(G7(70),1)} օր</em>', "օր", ""),
          ("Բանկային վարկեր", pc(F6(73)), F6(73) * 100, 2, "%", f'<em class="dn">▲ +{n(G7(73)*100,2)} պ.կ.</em>', "ԲՎ", ""),
          ("ՇԲԹֆպ", pc(F6(74)), F6(74) * 100, 2, "%", f'<em class="up">▲ +{n(G7(74)*100,2)} պ.կ.</em>', "✓", "g")]
    kps = "".join(f'<div class="kpi rv" style="--i:{i}"><span class="hk {c}">{hk}</span><small>{E(l)}</small><b data-count="{v}" data-d="{d}" data-suf="{suf}">{t}</b>{em}</div>'
                  for i, (l, t, v, d, suf, em, hk, c) in enumerate(kp))
    mv = []
    for lab, s, fo, rp, en in (("Ոչ ընթացիկ ՖՊ", 9, 15, 23, 66), ("Ընթացիկ ՖՊ", 35, 44, 55, 67)):
        for y, c in (("2024", 5), ("2025", 6)):
            mv.append([f"{E(lab)} · {y}", fm(g(a, s, c)), "+" + fm(g(a, fo, c)), "−" + fm(g(a, rp, c)), f"<b>{fm(g(a, en, c))}</b>"])
    mvt = table(["Հոդված", "Տարեսկիզբ", "Ձևավորված", "Մարված / տեղափ.", "Տարեվերջ"], mv)
    new = lambda c: g(a, 15, c) + g(a, 44, c) - g(a, 85, c)
    wf = lambda c: steps_chart([("Սկիզբ", "tot", g(a, 82, c)), ("Նոր ՖՊ", "pos", new(c)), ("Մարված", "neg", -g(a, 84, c)), ("Վերջ", "tot", g(a, 83, c))])
    bank0 = g(a, 5, 5) + g(a, 27, 5) + g(a, 28, 5)
    td = tide([(g(a, 9, 5), g(a, 35, 5), bank0), (E5(66), E5(67), E5(88)), (F6(66), F6(67), F6(88))], ["01.01.2024", "31.12.2024", "31.12.2025"])
    r24 = enso_ring([(E5(66), IND), (E5(67), IND3)], fm(E5(83)), "ՖՊ · 31.12.2024")
    r25 = enso_ring([(F6(66), IND), (F6(67), IND3)], fm(F6(83)), "ՖՊ · 31.12.2025")
    rb0 = enso_ring([(E5(88), RED), (E5(83) - E5(88), "#cbb994")], pc(E5(73), 1), "բանկային · 2024")
    rb = enso_ring([(F6(88), RED), (F6(83) - F6(88), "#cbb994")], pc(F6(73), 1), "բանկային · 2025")
    rleg = f'<div class="leg"><span><i style="background:{IND}"></i>Ոչ ընթացիկ</span><span><i style="background:{IND3}"></i>Ընթացիկ</span><span><i style="background:{RED}"></i>Բանկային վարկեր</span><span><i style="background:#cbb994"></i>Այլ ՖՊ</span></div>'
    helper = table(["Օժանդակ ցուցանիշ", "2024", "2025"], [[E(str(g(a, r, 3)).split("\n")[0]), (pc(E5(r)) if r == 89 else n(E5(r), 4 if r == 90 else 0)), (pc(F6(r)) if r == 89 else n(F6(r), 4 if r == 90 else 0))] for r in (82, 83, 84, 85, 86, 87, 88, 89, 90)])
    rows = [(66, "Ոչ ընթացիկ ՖՊ (տարեվերջ)", "ՈԸՖՊ", 0, False, "neu", "նվազել է"), (67, "Ընթացիկ ՖՊ (տարեվերջ)", "ԸՖՊ", 0, False, "bad", "կարճաժամկետ բեռ ↑"),
            (68, "ՖՊ միջին արժեք", "ՖՊ", 0, False, "neu", "աճել է"), (69, "Շրջանառելիություն, պտույտ", "ՇՐՋֆպ", 4, False, "bad", "դանդաղել է"),
            (70, "Մեկ պտույտի տևողություն, օր", "Tօր", 1, False, "bad", "երկարել է"), (71, "ԸՖՊ կշիռ ընթացիկ պարտավորություններում", "ՏԿֆպ", 2, True, "neu", "գրեթե անփոփոխ"),
            (72, "Ժամկետանց ՖՊ կշիռ", "ՏԿժ.անց", 2, True, "good", "բարելավվել է"), (73, "Բանկային վարկերի կշիռ", "ՏԿբվ", 2, True, "bad", "ռիսկ ↑"), (74, "ՖՊ շահութաբերություն", "ՇԲԹֆպ", 2, True, "good", "բարելավվել է")]
    cards = "".join(f'<div class="ic rv" style="--i:{i%3}">{spark(E5(r), F6(r), gd)}<code>{E(c)}</code><h4>{E(t)}</h4><div class="kv"><s>{vv(E5(r),d,p)}</s><span>→</span><b>{vv(F6(r),d,p)}</b></div>'
                    f'<div style="margin-top:4px;font:600 13px Noto Sans Armenian">Δ {vv(G7(r),d,p,True)}</div><span class="vb {gd}">{E(vt)}</span></div>' for i, (r, t, c, d, p, gd, vt) in enumerate(rows))
    an = [[E(t), f"<code>{E(c)}</code>", vv(E5(r), d, p), vv(F6(r), d, p), vv(G7(r), d, p, True)] for r, t, c, d, p, gd, vt in rows]
    an += [["9.1 · ըստ ՖՊ արդյունավետության (Հ/ՖՊ)", "<code>±ΔՇԲԹ(ՖՊարդյ)</code>", "—", "—", vv(G7(75), 2, 1, True)], ["9.2 · ըստ իրացման շահութաբերության (ԶՇ/Հ)", "<code>±ΔՇԲԹ(ՇԲԹիր)</code>", "—", "—", vv(G7(76), 2, 1, True)]]
    ant = table(["Ցուցանիշ", "Նշան", "2024", "2025", "Δ"], an)
    fanA = fan("Փաստացի մարումով", [("2024", E5(70), "#9c8f7a"), ("2025", F6(70), RED)], 1000)
    fanB = fan("Եթե տեղափոխումն էլ հաշվենք մարում", [("2024", E5(94), "#9c8f7a"), ("2025", F6(94), RED)], 1000)
    sharebars = hbars([("ՏԿբվ · բանկային", E5(73) * 100, F6(73) * 100, "2024", "2025"), ("ՏԿֆպ · ԸՖՊ/ԸՊ", E5(71) * 100, F6(71) * 100, "2024", "2025"),
                       ("ՏԿժ.անց · ժամկետանց", E5(72) * 100, F6(72) * 100, "2024", "2025"), ("ՇԲԹֆպ", E5(74) * 100, F6(74) * 100, "2024", "2025")], 100)
    fw = steps_chart([("ՇԲԹ 2024", "tot", E5(74) * 100), ("Հ/ՖՊ", "pos", G7(75) * 100), ("ԶՇ/Հ", "neg", G7(76) * 100), ("ՇԲԹ 2025", "tot", F6(74) * 100)], 2, 340, "%")
    ft = table(["Քայլ", "ԶՇ/Հ", "Հ/ՖՊ", "ՇԲԹֆպ"], [["1 · 2024 (բազիս)", pc(g(a, 89, 5)), n(g(a, 90, 5), 4), pc(E5(74))], ["2 · Հ/ՖՊ → 2025", pc(g(a, 89, 5)), n(g(a, 90, 6), 4), pc(F6(75))],
        ["3 · ԶՇ/Հ → 2025", pc(g(a, 89, 6)), n(g(a, 90, 6), 4), pc(F6(74))], ["±Δ Հ/ՖՊ (2 − 1)", "", "", vv(G7(75), 2, 1, True)], ["±Δ ԶՇ/Հ (3 − 2)", "", "", vv(G7(76), 2, 1, True)], ["<b>Ընդամենը = ΔՇԲԹֆպ</b>", "", "", f"<b>{vv(G7(74), 2, 1, True)}</b>"]])
    def t45(r1, r2, r3, r4, cap):
        return table([cap, "t0", "t1", "Δ"], [["Մարված ընթացիկ ՖՊ", fm(g(b, r1, 4)), fm(g(b, r1, 5)), n(g(b, r1, 6), 0, True)], ["ԸՖՊ միջին արժեք", fm(g(b, r2, 4)), fm(g(b, r2, 5)), n(g(b, r2, 6), 0, True)],
                                         ["Շրջանառելիություն, պտույտ", n(g(b, r3, 4), 4), n(g(b, r3, 5), 4), n(g(b, r3, 6), 4, True)], ["Շրջանառելիություն, օր", n(g(b, r4, 4), 1), n(g(b, r4, 5), 1), n(g(b, r4, 6), 1, True)]])
    t4, t5 = t45(5, 7, 8, 9, "11.1.4"), t45(16, 17, 18, 19, "11.1.5")
    f4 = fan("11.1.4 · պտույտ, օր", [("t0", g(b, 9, 4), "#9c8f7a"), ("t1", g(b, 9, 5), RED)], 500)
    f5 = fan("11.1.5 · պտույտ, օր", [("t0", g(b, 19, 4), "#9c8f7a"), ("t1", g(b, 19, 5), RED)], 500)
    names = {26: "Ոչ ընթացիկ ՖՊ", 27: "· երկարաժամկետ բանկային վարկեր", 29: "· երկարաժամկետ փոխառություններ", 31: "Ընթացիկ ՖՊ", 32: "· կարճաժամկետ բանկային վարկեր", 34: "· կարճաժամկետ փոխառություններ", 37: "Ընդամենը"}
    t3 = table(["11.1.3", "t0", "%", "t1", "%", "Δ", "Δ, պ.կ."], [[E(nm), fm(g(b, r, 3)), pc(g(b, r, 4)), fm(g(b, r, 5)), pc(g(b, r, 6)), n(g(b, r, 7), 0, True), n(g(b, r, 8) * 100, 2, True)] for r, nm in names.items()])
    tt = tatami([("t0", [g(b, 27, 3), g(b, 29, 3), g(b, 32, 3), g(b, 34, 3), g(b, 38, 3) or 0]), ("t1", [g(b, 27, 5), g(b, 29, 5), g(b, 32, 5), g(b, 34, 5), g(b, 38, 5)])],
                [("Երկ. բանկային վարկ", IND), ("Երկ. փոխառություն", IND3), ("Կարճ. բանկային վարկ", RED), ("Կարճ. փոխառություն", GOLD), ("Չբացված տարբերություն", "#9c8f7a")])
    st3 = steps_chart([("t0", "tot", g(b, 37, 3)), ("Երկ.վ.", "pos", g(b, 27, 7)), ("Երկ.փ.", "neg", g(b, 29, 7)), ("Կարճ.վ.", "neg", g(b, 32, 7)), ("Կարճ.փ.", "pos", g(b, 34, 7)), ("Չբաց.", "pos", g(b, 38, 5)), ("t1", "tot", g(b, 37, 5))], 0, 330)
    def strip_num(s): s = str(s); return s.split(". ", 1)[1] if s[:2].rstrip(".").isdigit() and ". " in s[:4] else s
    concl = "".join(f'<p data-k="{ARM[i]}">{E(strip_num(g(a, r, 2)))}</p>' for i, r in enumerate(r for r in range(98, 104) if g(a, r, 2)))
    concl2 = "".join(f'<p data-k="{ARM[i]}">{E(str(g(b, r, 2)))}</p>' for i, r in enumerate(r for r in range(44, 47) if g(b, r, 2)))
    notes = ("<div class='knote rv'><b>Մարվածը՝ առանց կրկնահաշվարկի։</b> Ոչ ընթացիկից ընթացիկ տեղափոխված մասը (տարեկան 22 000) մարում չէ․ այն նորից հայտնվում է ընթացիկ ձևավորվածների մեջ։ Հիմնական հաշվարկում վերցված է փաստացի մարումը, Excel-ում ցույց է տրված նաև ձևանմուշի ուղիղ գումարով տարբերակը (604 → 643 օր)։</div>"
             "<div class='knote rv'><b>Բանկային վարկերը՝ ըստ տողի անվանման։</b> Մի քանի տողում նշանը (ԸՖՊ) և անվանումը («բանկային վարկ») չեն համընկնում, ուստի որոշիչը անվանումն է (օժանդակ H սյունակ)։ Ստուգում՝ 2024-ի տարեվերջը լրիվ համընկնում է 2025-ի տարեսկզբի հետ ✔</div>"
             "<div class='knote rv'><b>11.1.3․</b> 12 500-ը տեղադրված է իր տողում, «Ընդամենը»-ն՝ ոչ ընթացիկ + ընթացիկ (197 600 և 227 600)։ t1-ի ընթացիկ ՖՊ-ն (52 200) 2 000-ով մեծ է բաղադրիչներից (30 500 + 19 700)․ հոդվածը պահպանված է, տարբերությունը ցույց է տրված առանձին։</div>"
             "<div class='knote rv'><b>11.1.4․</b> Սյունակները՝ t0 և t1, օրերը՝ 360-օրյա տարով (դասախոսության բանաձևով)։</div>")
    caps = ["Մեծ ալիք", "Աճի գրաֆիկ Ֆուձիի վրա", "Գիշերային կռունկներ", "Կինցուգի", "Սակուրա և մետաղադրամներ", "Բանկ-տաճար", "Մատյան-մագաղաթ", "Էնսո և արև", "Բյոբու", "Մետաղադրամների լեռ"]
    byobu = "".join(f'<figure><a href="{ART}/{k:02d}.svg" data-lb><img src="{ART}/{k:02d}.svg" alt="{E(c)}" loading="lazy"></a><figcaption>{E(c)}<i>{ARM[k]}</i></figcaption></figure>' for k, c in enumerate(caps))
    mq = "".join(f'<img src="{ART}/{k:02d}_s.svg" alt="" loading="lazy">' for k in range(10))
    chap = lambda k, num, t, s: (f'<section class="chap"><div class="chi" data-par="0.25" style="background-image:url(\'{ART}/{k:02d}.svg\')"></div>'
                                 f'<div class="chc rv"><span class="chn">{E(num)}</span><h2>{E(t)}</h2><p>{E(s)}</p></div></section>')
    body = DEFS + H.topbar(XL, "lesson-9.html", "Դաս 9") + f"""
<div class="cur"><i class="rl a"></i><i class="rl b"></i><div class="pp"><div class="ct"><small>ԹԵՄԱ 10 · ԴԱՍ 9</small><b>Ալիք և ոսկի</b><small style="color:#1b1a24;letter-spacing:.3em">ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ</small></div><span class="hk">ՖՊ</span></div></div>
<section class="hero"><div class="bgart"><img src="{ART}/00.svg" alt=""></div><span class="vtag">ՖԻՆԱՆՍԱԿԱՆ ՊԱՐՏԱՎՈՐՈՒԹՅՈՒՆՆԵՐ</span>
<div class="inner"><div class="kick9 fade-up">Դաս 9 · Թեմա 10 · 21.11.2026 · Օ. Ա. Գալստյան</div>
<h1><span class="brush">Ֆինանսական</span><span class="brush"><em>պարտավորությունների</em></span><span class="brush">վերլուծություն</span></h1>
<svg class="uline" viewBox="0 0 520 26"><path d="M6 16 C120 4 260 26 514 10" stroke="{RED}" stroke-width="9" fill="none" stroke-linecap="round" filter="url(#brs)"/></svg>
<p class="lead fade-up">Պարտքը նման է ալիքի․ եթե այն կառավարում ես, տանում է առաջ, եթե ոչ՝ ծածկում է։ Չափում ենք ալիքը՝ կազմ, շարժ, պտույտի արագություն, բանկային կախվածություն և շահութաբերություն։</p>
<nav class="seals fade-up"><a href="#a1"><i>Ա</i>Շարժ</a><a href="#a2"><i>Բ</i>9 ցուցանիշ</a><a href="#a3"><i>Գ</i>Գործոններ</a><a href="#a4"><i>Դ</i>Տնային 2</a><a href="#a5"><i>Ե</i>Եզրակացություն</a><a class="x" href="../../files/{XL}" download><i>⬇</i>Excel</a></nav></div>
{waveband()}{waveband("b2")}</section>
<div class="w9" style="margin-top:-40px;position:relative;z-index:5"><div class="g4">{kps}</div></div>
<section class="sec9" id="a1"><div class="w9">{sh(0, "Ալիքի շարժը", "Տարեսկիզբ + ձևավորված − մարված = տարեվերջ։ Ֆինանսական պարտավորությունները երեք ամսաթվով և երկու տարվա հոսքերով։")}
{pn("Ալիքի բարձրությունը", "հազ. դր. · 3 ամսաթիվ", td)}
<div class="g2 mt">{pn("Հոսքեր 2024", "սկիզբ → վերջ", wf(5))}{pn("Հոսքեր 2025", "սկիզբ → վերջ", wf(6))}</div>
<div class="g4 mt">{pn("Կառուցվածք 2024", "ոչ ընթ. / ընթ.", r24)}{pn("Կառուցվածք 2025", "ոչ ընթ. / ընթ.", r25)}{pn("Բանկային 2024", "ՏԿբվ", rb0)}{pn("Բանկային 2025", "ՏԿբվ", rb)}</div>{rleg}
<div class="g2 mt">{pn("Շարժի աղյուսակ", "Տնային 1", mvt)}{pn("Օժանդակ հաշվարկներ", "Excel · տողեր 82–90", helper)}</div></div></section>
{kin(1)}
{chap(1, "Բ", "Ինտենսիվություն", "Որքան արագ է պտտվում պարտքը և ում է այն պատկանում")}
<section class="sec9" id="a2"><div class="w9" id="excel">{sh(1, "Ինը ցուցանիշ", "Միջինը՝ (տարեսկիզբ + տարեվերջ) ÷ 2, կշիռները՝ տարեվերջի ՖՊ-ի նկատմամբ, t = 360 օր։")}
<div class="g3">{cards}</div>
<div class="g2 mt">{pn("Պտույտի հովհար", "Տնային 1 · օր", fanA)}{pn("Համեմատություն", "ձևանմուշի ուղիղ գումարով", fanB)}</div>
{pn("Կշիռներ և շահութաբերություն", "2024 (մոխրագույն) → 2025", sharebars, "mt")}
<div class="mt">{pn("Վերլուծության աղյուսակ", "Տնային 1 · տողեր 66–76", ant)}</div></div></section>
{kin(2)}
<section class="sec9" id="a3"><div class="w9">{sh(2, "ՇԲԹֆպ-ի գործոնային վերլուծություն", f"ՇԲԹֆպ = ԶՇ/Հ × Հ/ՖՊ · շղթայական տեղադրում։ Գործոնների գումարը = ընդհանուր փոփոխություն ({vv(G7(74),2,1,True)}) ✔")}
<div class="g2">{pn("Քարե աստիճաններ", "պ.կ.", fw)}{pn("Շղթայական տեղադրում", "%", ft)}</div></div></section>
<div class="mq"><div class="mqt">{mq}{mq}</div></div>
<section class="sec9" id="a4"><div class="w9">{sh(3, "Տնային 2 · խնդիրներ 11.1.3–11.1.5", "Կազմ, կառուցվածք և շրջանառելիություն։")}
<div class="g2">{pn("11.1.4", "շրջանառելիություն", t4 + f4)}{pn("11.1.5", "շրջանառելիություն", t5 + f5)}</div>
<div class="mt">{pn("11.1.3 · կազմ և կառուցվածք", "հազ. դր. և %", t3)}</div>
<div class="g2 mt">{pn("Տատամի․ կառուցվածք", "100% = ընդամենը", tt)}{pn("Ինչից աճեց 30 000-ը", "t0 → t1", st3)}</div></div></section>
{chap(5, "Ե", "Եզրակացություն", "Մագաղաթը բացվում է")}
<section class="sec9" id="a5"><div class="w9"><div class="g2"><div class="kake"><i class="rod t"></i><div class="bdy"><h3>Տնային 1</h3>{concl}</div><i class="rod b"></i></div>
<div class="kake"><i class="rod t"></i><div class="bdy"><h3>Տնային 2</h3>{concl2}</div><i class="rod b"></i></div></div></div></section>
{kin(3)}
<section class="sec9"><div class="w9">{sh(5, "Կինցուգի․ հաշվարկի ծանոթագրություններ", "Կոտրված տեղերը չենք թաքցնում, այլ ոսկով ենք նշում։")}
<div class="kgrid"><img class="rv" src="{ART}/03.svg" alt="Կինցուգի"><div>{notes}</div></div></div></section>
<section class="sec9" style="padding-bottom:0"><div class="w9">{sh(6, "Բյոբու․ պատկերասրահ", "Բոլոր նկարազարդումները ստեղծված են կոդով՝ ուկիյո-է ոճով, հատուկ այս աշխատանքի համար։ Սեղմեք՝ մեծացնելու համար։")}</div><div class="byobu">{byobu}</div></section>
<div class="foot9"><div class="hk2">ՀԱ</div><br>H/R STUDIOS · ՀՐԱՉՅԱ ԱՍԼԱՆՅԱՆ · ԻՏ-447 · EXCEL՝ 397 ԲԱՆԱՁԵՎ · 0 ՍԽԱԼ</div>
{PETALS_JS}"""
    return P.page("wave", "Ֆինանսական պարտավորություններ", body, CSS, "Դաս 9 (Թեմա 10) տնային աշխատանք", 2000, RED)

H.FONTS["wave"] = "family=Noto+Serif+Armenian:wght@400;600;800;900&family=Noto+Sans+Armenian:wght@400;500;600;700&family=Zen+Old+Mincho:wght@600;900"
P.PAGES["dasi-9"] = build_hw9
if __name__ == "__main__":
    d = os.path.join(SITE, "hw", "dasi-9"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf8").write(build_hw9()); print("wrote dasi-9")
