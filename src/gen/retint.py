"""Apply the dark-premium palette, fonts and lesson covers on top of the classic layout (run after gen2.py + extras.py)."""
import os, re, glob, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = os.path.join(BASE, 'site')
sys.path.insert(0, os.path.join(BASE, 'gen')); from content import LESSONS
MAP = []  # palette stays the original green
FONT_OLD = 'family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=Noto+Serif+Armenian:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700'
FONT_NEW = 'family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700'
EXTRA = """<style id="v3tint">:root{--disp:'Inter','Noto Sans Armenian',system-ui,sans-serif;--body:'Inter','Noto Sans Armenian',system-ui,sans-serif;--num:'JetBrains Mono',ui-monospace,monospace}
body{letter-spacing:-.006em}h1,h2,h3{letter-spacing:-.025em}::selection{background:rgba(61,255,143,.3)}
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
    s = s.replace(FONT_OLD, FONT_NEW)
    if 'id="v3tint"' not in s: s = s.replace('</head>', EXTRA + '</head>', 1)
    open(p, 'w', encoding='utf8').write(s)
for p in [os.path.join(SITE, 'assets', f) for f in ('hr-extra.css', 'hr-extra.js', 'hr-data.js')]:
    if os.path.exists(p): s = open(p, encoding='utf8').read(); pass
print('retint ok')
