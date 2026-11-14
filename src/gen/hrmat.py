# -*- coding: utf-8 -*-
# Builds the "H/R version" of the teacher materials for every lesson:
#  1) materials/tN/HR_DasN.pptx  - branded deck: cover, idea, formulas, glossary, every teacher slide framed, end
#  2) materials/tN/HR_DasN_konspekt.pdf - designed A4 study notes (theory, formulas, glossary, slide gallery)
import os, sys, html, re, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from content import LESSONS, COURSE, TEACHER
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = os.path.join(BASE, 'site')
E = html.escape
strip = lambda s: re.sub(r'<[^>]+>', '', s)
W, H = Emu(12192000), Emu(6858000)
BG = RGBColor(0x05, 0x09, 0x08); TX = RGBColor(0xEA, 0xFF, 0xF2); SUB = RGBColor(0xA8, 0xBF, 0xB4)
def rgb(h): h = h.lstrip('#'); return RGBColor(int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16))
FONT = 'Noto Sans Armenian'

def slides_of(mat):
    d = os.path.join(SITE, 'materials', mat, 'slides'); return sorted(os.listdir(d)) if os.path.isdir(d) else []

def bg(s, img=None, dim=True):
    f = s.background.fill; f.solid(); f.fore_color.rgb = BG
    if img:
        s.shapes.add_picture(img, 0, 0, W, H)
        if dim:
            r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H); r.fill.solid(); r.fill.fore_color.rgb = BG; r.line.fill.background()
            r.fill.transparency = 0.25
            from pptx.oxml.ns import qn
            sf = r.fill._xPr.find(qn('a:solidFill')); clr = sf[0]
            a = clr.makeelement(qn('a:alpha'), {'val': '68000'}); clr.append(a)

def tb(s, x, y, w, h, text, size=20, color=TX, bold=False, align=PP_ALIGN.LEFT, font=FONT):
    t = s.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)); tf = t.text_frame; tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        r = p.add_run(); r.text = ln; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return t

def bar(s, acc):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Emu(60000)); r.fill.solid(); r.fill.fore_color.rgb = rgb(acc); r.line.fill.background()

def footer(s, L, n):
    logo = os.path.join(SITE, 'assets', 'logo_sm.png')
    s.shapes.add_picture(logo, Emu(11000000), Emu(6250000), height=Emu(420000))
    tb(s, 500000, 6300000, 9000000, 400000, f'H/R Studios · Դաս {L["n"]} · {strip(L["t"])}', 11, SUB)
    if n: tb(s, 10300000, 6300000, 600000, 400000, str(n), 11, SUB, align=PP_ALIGN.RIGHT)

def card(s, x, y, w, h, acc, alpha=None):
    r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h)); r.adjustments[0] = 0.08
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor(0x10, 0x1A, 0x17); r.line.color.rgb = rgb(acc); r.line.width = Pt(1.2)
    return r

def build_pptx(L):
    acc = L['acc']; mat = L['mat']; img = os.path.join(SITE, 'assets', 'gen', L['img'] + '.jpg')
    p = Presentation(); p.slide_width, p.slide_height = W, H; blank = p.slide_layouts[6]; n = 0
    # cover
    s = p.slides.add_slide(blank); bg(s, img); bar(s, acc)
    tb(s, 700000, 1300000, 9000000, 500000, f'ԴԱՍ {L["n"]} · {L["date"]}', 16, rgb(acc), True)
    tb(s, 700000, 1850000, 10000000, 2200000, strip(L['t']), 44, TX, True, font='Noto Serif Armenian')
    tb(s, 700000, 4300000, 9500000, 900000, L['idea'], 18, SUB)
    tb(s, 700000, 5400000, 9000000, 500000, f'{COURSE} · Դասախոս՝ {TEACHER} · H/R տարբերակ', 13, SUB)
    s.shapes.add_picture(os.path.join(SITE, 'assets', 'logo_crop.png'), Emu(9300000), Emu(300000), height=Emu(1100000))
    # idea + analogy
    n += 1; s = p.slides.add_slide(blank); bg(s); bar(s, acc)
    tb(s, 600000, 450000, 11000000, 600000, 'Դասը պարզ լեզվով', 30, TX, True, font='Noto Serif Armenian')
    card(s, 600000, 1300000, 5300000, 3000000, acc); tb(s, 850000, 1450000, 4800000, 2700000, L['idea'], 20, TX)
    card(s, 6200000, 1300000, 5300000, 3000000, acc); tb(s, 6450000, 1400000, 4800000, 400000, 'ԿՅԱՆՔԻՑ ՕՐԻՆԱԿ', 12, rgb(acc), True); tb(s, 6450000, 1850000, 4800000, 2400000, L['analogy'], 16, SUB)
    pts = L['points'][:6]; cw = 11000000 // max(1, min(3, len(pts)))
    for k, (a, b) in enumerate(pts[:3]):
        x = 600000 + k * cw; card(s, x, 4500000, cw - 150000, 1550000, acc)
        tb(s, x + 200000, 4600000, cw - 500000, 400000, a, 14, rgb(acc), True); tb(s, x + 200000, 5000000, cw - 500000, 1000000, b, 12, SUB)
    footer(s, L, n)
    # formulas (3 per row, 2 rows per slide)
    F = L['formulas']
    for page in range(0, len(F), 6):
        n += 1; s = p.slides.add_slide(blank); bg(s); bar(s, acc)
        tb(s, 600000, 450000, 11000000, 600000, 'Գլխավոր բանաձևերը' + (f' ({page//6+1})' if len(F) > 6 else ''), 30, TX, True, font='Noto Serif Armenian')
        for k, (c, nm, f, m, d) in enumerate(F[page:page+6]):
            x = 600000 + (k % 3) * 3700000; y = 1300000 + (k // 3) * 2450000
            card(s, x, y, 3550000, 2300000, acc)
            tb(s, x + 200000, y + 120000, 3200000, 450000, strip(c), 22, rgb(acc), True)
            tb(s, x + 200000, y + 560000, 3200000, 400000, nm, 13, TX, True)
            tb(s, x + 200000, y + 950000, 3200000, 450000, f'{strip(c)} = {strip(f)}', 14, TX, font='Consolas')
            tb(s, x + 200000, y + 1400000, 3200000, 850000, m, 11, SUB)
        footer(s, L, n)
    # glossary
    n += 1; s = p.slides.add_slide(blank); bg(s); bar(s, acc)
    tb(s, 600000, 450000, 11000000, 600000, 'Բառարան', 30, TX, True, font='Noto Serif Armenian')
    for k, (a, b) in enumerate(L['glossary']):
        y = 1300000 + k * 820000; card(s, 600000, y, 11000000, 700000, acc)
        tb(s, 850000, y + 150000, 2200000, 450000, a, 18, rgb(acc), True); tb(s, 3100000, y + 170000, 8200000, 450000, b, 16, SUB)
    footer(s, L, n)
    # teacher slides framed
    sl = slides_of(mat)
    if sl:
        n += 1; s = p.slides.add_slide(blank); bg(s, img); bar(s, acc)
        tb(s, 700000, 2500000, 10000000, 900000, 'Դասախոսի սլայդները', 40, TX, True, font='Noto Serif Armenian')
        tb(s, 700000, 3400000, 10000000, 500000, f'{len(sl)} սլայդ՝ նոր ձևավորմամբ', 18, SUB)
    for k, f in enumerate(sl):
        n += 1; s = p.slides.add_slide(blank); bg(s); bar(s, acc)
        im = os.path.join(SITE, 'materials', mat, 'slides', f)
        fw = 9600000; fh = int(fw * 9 / 16)
        fr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu((12192000 - fw)//2 - 60000), Emu(380000 - 60000), Emu(fw + 120000), Emu(fh + 120000))
        fr.adjustments[0] = 0.03; fr.fill.solid(); fr.fill.fore_color.rgb = rgb(acc); fr.line.fill.background()
        s.shapes.add_picture(im, Emu((12192000 - fw)//2), Emu(380000), Emu(fw), Emu(fh))
        tb(s, 600000, 5950000, 6000000, 350000, f'Սլայդ {k+1} / {len(sl)}', 12, rgb(acc), True)
        footer(s, L, n)
    # end
    s = p.slides.add_slide(blank); bg(s, os.path.join(SITE, 'assets', 'gen', 'studio.jpg')); bar(s, acc)
    s.shapes.add_picture(os.path.join(SITE, 'assets', 'logo_crop.png'), Emu(4300000), Emu(1400000), height=Emu(1700000))
    tb(s, 0, 3500000, 12192000, 700000, 'Շնորհակալություն', 40, TX, True, PP_ALIGN.CENTER, font='Noto Serif Armenian')
    tb(s, 0, 4300000, 12192000, 500000, 'H/R Studios · Հրաչյա Ասլանյան · ԻՏ-447 · hrachevskiy.github.io/HR-Studios', 14, SUB, align=PP_ALIGN.CENTER)
    out = os.path.join(SITE, 'materials', mat, f'HR_Das{L["n"]}_prezentacia.pptx'); p.save(out); return out

PDFCSS = '''@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans Armenian',sans-serif;color:#eafff2;background:#050908;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:210mm;min-height:297mm;padding:16mm 15mm 18mm;position:relative;page-break-after:always;background:radial-gradient(80% 50% at 90% 0%,color-mix(in srgb,var(--a) 16%,transparent),transparent 70%),#050908}
.cover{padding:0;display:flex;flex-direction:column;justify-content:flex-end}.cover .im{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.55}
.cover .sh{position:absolute;inset:0;background:linear-gradient(0deg,#050908 30%,rgba(5,9,8,.2))}.cover .ct{position:relative;padding:0 15mm 22mm}
.k{font-weight:700;font-size:11pt;letter-spacing:.2em;color:var(--a);text-transform:uppercase}h1{font-family:'Noto Serif Armenian',serif;font-size:32pt;line-height:1.1;margin:6mm 0}h2{font-family:'Noto Serif Armenian',serif;font-size:20pt;margin:0 0 6mm;color:#fff}
.lead{font-size:12pt;color:#b9cdc3;line-height:1.6}.logo{position:absolute;top:14mm;right:15mm;height:18mm}
.box{border:1px solid color-mix(in srgb,var(--a) 50%,transparent);background:rgba(255,255,255,.04);border-radius:5mm;padding:5mm 6mm;margin-bottom:5mm}.box b.t{display:block;color:var(--a);font-size:9pt;letter-spacing:.18em;margin-bottom:2mm}
.box p{margin:0;font-size:11pt;line-height:1.6;color:#d8e8e0}.g2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.pt{border-left:3px solid var(--a);padding:2mm 4mm;background:rgba(255,255,255,.03);border-radius:0 3mm 3mm 0}.pt b{display:block;color:var(--a);font-size:10.5pt}.pt span{font-size:10pt;color:#b9cdc3}
.fc{border:1px solid rgba(255,255,255,.12);border-radius:4mm;padding:4mm 5mm;background:rgba(255,255,255,.04);break-inside:avoid}.fc .c{font-family:'Noto Serif Armenian',serif;font-size:16pt;font-weight:800;color:var(--a)}
.fc .n{font-weight:700;font-size:10.5pt;margin:1mm 0 2mm}.fc .e{font-family:'IBM Plex Mono',monospace;font-size:10pt;background:rgba(0,0,0,.4);padding:2mm 3mm;border-radius:2mm;margin-bottom:2mm}.fc .m{font-size:9.5pt;color:#b9cdc3}
.gl{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.gl div{padding:3mm 4mm;border-radius:3mm;background:rgba(255,255,255,.04);font-size:10pt}.gl b{color:var(--a);margin-right:3mm}
.sl{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.sl figure{margin:0;border-radius:3mm;overflow:hidden;border:1px solid rgba(255,255,255,.12);break-inside:avoid}.sl img{width:100%;display:block}.sl figcaption{font-size:8pt;color:#8aa298;padding:1.5mm 3mm}
.ft{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:8pt;color:#6f857b}'''

def build_pdf_html(L):
    acc = L['acc']; mat = L['mat']; sl = slides_of(mat); root = 'file://' + SITE + '/'
    ft = lambda n: f'<div class="ft"><span>H/R Studios · Դաս {L["n"]} · {E(strip(L["t"]))}</span><span>{n}</span></div>'
    pages = [f'''<section class="pg cover"><div class="im" style="background-image:url('{root}assets/gen/{L["img"]}.jpg')"></div><div class="sh"></div><img class="logo" src="{root}assets/logo_crop.png">
<div class="ct"><div class="k">Դաս {L["n"]} · {E(L["date"])} · Կոնսպեկտ</div><h1>{E(strip(L["t"]))}</h1><p class="lead">{E(L["idea"])}</p><p class="lead" style="font-size:10pt;margin-top:8mm">{E(COURSE)} · Դասախոս՝ {E(TEACHER)}<br>H/R Studios · Հրաչյա Ասլանյան · ԻՏ-447</p></div></section>''']
    pts = ''.join(f'<div class="pt"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in L['points'])
    pages.append(f'''<section class="pg"><div class="k">01</div><h2>Դասը պարզ լեզվով</h2><div class="box"><b class="t">ԳԼԽԱՎՈՐԸ</b><p style="font-size:13pt">{E(L["idea"])}</p></div>
<div class="box"><b class="t">ԿՅԱՆՔԻՑ ՕՐԻՆԱԿ</b><p>{E(L["analogy"])}</p></div><div class="g2">{pts}</div>{ft(2)}</section>''')
    fx = ''.join(f'<div class="fc"><div class="c">{c}</div><div class="n">{E(nm)}</div><div class="e">{c} = {f}</div><div class="m">{E(m)}</div></div>' for c, nm, f, m, d in L['formulas'])
    gl = ''.join(f'<div><b>{E(a)}</b>{E(b)}</div>' for a, b in L['glossary'])
    pages.append(f'''<section class="pg"><div class="k">02</div><h2>Բանաձևեր</h2><div class="g2">{fx}</div><h2 style="margin-top:8mm">Բառարան</h2><div class="gl">{gl}</div>{ft(3)}</section>''')
    for k in range(0, len(sl), 6):
        figs = ''.join(f'<figure><img src="{root}materials/{mat}/slides/{f}"><figcaption>Սլայդ {k+i+1}</figcaption></figure>' for i, f in enumerate(sl[k:k+6]))
        pages.append(f'<section class="pg"><div class="k">03</div><h2>Դասախոսի սլայդները{" (" + str(k//6+1) + ")" if len(sl) > 6 else ""}</h2><div class="sl">{figs}</div>{ft(4 + k//6)}</section>')
    return f'''<!doctype html><html lang="hy"><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Armenian:wght@400;600;700;800&family=Noto+Serif+Armenian:wght@700;800&family=IBM+Plex+Mono:wght@500&display=swap"><style>{PDFCSS}</style></head><body style="--a:{acc}">{"".join(pages)}</body></html>'''

async def build_pdfs():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page()
        for L in LESSONS:
            tmp = os.path.join(BASE, 'work', f'konspekt{L["n"]}.html'); open(tmp, 'w').write(build_pdf_html(L))
            await pg.goto('file://' + tmp); await pg.wait_for_timeout(700)
            out = os.path.join(SITE, 'materials', L['mat'], f'HR_Das{L["n"]}_konspekt.pdf')
            await pg.pdf(path=out, format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            print('pdf', L['n'], os.path.getsize(out) // 1024, 'KB')
        await b.close()

if __name__ == '__main__':
    for L in LESSONS:
        o = build_pptx(L); print('pptx', L['n'], os.path.getsize(o) // 1024, 'KB')
    asyncio.run(build_pdfs())
