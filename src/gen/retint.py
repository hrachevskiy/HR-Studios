"""Apply the dark-premium palette, fonts and lesson covers on top of the classic layout (run after gen2.py + extras.py)."""
import os, re, glob, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = os.path.join(BASE, 'site')
sys.path.insert(0, os.path.join(BASE, 'gen')); from content import LESSONS
MAP = [('#3dff8f', '#8b9bff'), ('61,255,143', '139,155,255'), ('#5cd6ff', '#5eead4'), ('92,214,255', '94,234,212'),
       ('#3dffe0', '#67e8f9'), ('#c8ff4d', '#c4b5fd'), ('#050908', '#07080a'), ('5,9,8', '7,8,10'), ('#0a1210', '#0c0d10'),
       ('10,18,16', '12,13,16'), ('#0b1311', '#0e0f13'), ('11,19,17', '14,15,19'), ('#0d1a14', '#121420'), ('13,26,20', '18,20,32'),
       ('#03140a', '#0a0b18'), ('8,14,12', '9,10,13'), ('3,6,5', '4,5,7'), ('2,5,4', '3,4,6'), ('#eafff2', '#edeef0'),
       ('234,255,242', '237,238,240'), ('#d7ffe6', '#e0e4ff'), ('#9dffc4', '#c7cfff'), ('#1fd97a', '#7c8cff'), ('#16804a', '#4f5bd5'),
       ('#f4f7f5', '#f5f6f8'), ('244,247,245', '245,246,248'), ('#e8efeb', '#e9eaef'), ('#eef3f0', '#eff0f4')]
FONT_OLD = 'family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=Noto+Serif+Armenian:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700'
FONT_NEW = 'family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700'
EXTRA = """<style id="v3tint">:root{--disp:'Inter','Noto Sans Armenian',system-ui,sans-serif;--body:'Inter','Noto Sans Armenian',system-ui,sans-serif;--num:'JetBrains Mono',ui-monospace,monospace}
body{letter-spacing:-.006em}h1,h2,h3{letter-spacing:-.025em}::selection{background:rgba(139,155,255,.35)}
.bgi,.bimg,.fbg,img[src*="assets/gen/"]{filter:grayscale(1) sepia(.45) hue-rotate(195deg) saturate(1.9) brightness(.95)}.ph[style*="assets/gen/"]{background-blend-mode:luminosity}
.bgfx{background:radial-gradient(55% 45% at 85% -10%,rgba(79,70,229,.22),transparent 70%),radial-gradient(45% 45% at -10% 55%,rgba(14,116,144,.16),transparent 70%),radial-gradient(40% 40% at 60% 110%,rgba(124,58,237,.14),transparent 70%),var(--bg)!important}
</style>"""
def tint(s):
    for a, b in MAP: s = s.replace(a, b).replace(a.upper(), b)
    return s
def covers(s):
    for L in LESSONS:
        s = re.sub(rf'assets/gen/{L["img"]}(_s)?\.jpg', f'assets/v3/l{L["n"]}.jpg', s)
    return s
for p in glob.glob(os.path.join(SITE, '*.html')):
    s = open(p, encoding='utf8').read()
    s = covers(tint(s)).replace(FONT_OLD, FONT_NEW)
    if 'id="v3tint"' not in s: s = s.replace('</head>', EXTRA + '</head>', 1)
    open(p, 'w', encoding='utf8').write(s)
for p in [os.path.join(SITE, 'assets', f) for f in ('hr-extra.css', 'hr-extra.js', 'hr-data.js')]:
    if os.path.exists(p): s = open(p, encoding='utf8').read(); open(p, 'w', encoding='utf8').write(covers(tint(s)))
print('retint ok')
