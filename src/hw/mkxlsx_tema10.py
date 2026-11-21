# -*- coding: utf-8 -*-
import sys, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference, PieChart
from openpyxl.chart.label import DataLabelList
from openpyxl.comments import Comment

SRC, OUT = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(SRC)
a, b = wb.worksheets[0], wb.worksheets[1]
F = 'Sylfaen'
GRN = PatternFill('solid', fgColor='FFE2F5E9', bgColor='FFE2F5E9'); HDR = PatternFill('solid', fgColor='FF0F5132', bgColor='FF0F5132'); YEL = PatternFill('solid', fgColor='FFFFF4CC', bgColor='FFFFF4CC')
thin = Side(style='thin', color='9AA5A0'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
def f(c, v, fmt=None, bold=False, fill=GRN, color='000000', sz=12):
    c.value = v; c.font = Font(name=F, sz=sz, bold=bold, color=color); c.border = BOX
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(horizontal='right' if not isinstance(v, str) or v.startswith('=') else 'left', vertical='center', wrap_text=True)

NUM = '#,##0;[Red]-#,##0;"–"'; D2 = '#,##0.00;[Red]-#,##0.00;"–"'; D4 = '0.0000;[Red]-0.0000;"–"'; PCT = '0.00%;[Red]-0.00%;"–"'

# ---------------- Sheet 1 ----------------
a['B2'].value = '«XXX» ՍՊԸ ֆինանսական պարտավորությունների վերլուծություն · Հրաչյա Ասլանյան, ԻՏ-447'
a['B2'].font = Font(name=F, sz=14, bold=True, color='0F5132')
# helper flag column H: bank loan
a['H3'].value = 'Բանկային վարկ (1/0)'; a['H3'].font = Font(name=F, sz=10, bold=True); a.column_dimensions['H'].width = 14
a['H25'].value = 'Բանկային վարկ (1/0)'; a['H25'].font = Font(name=F, sz=10, bold=True)
for r in list(range(4, 9)) + list(range(10, 15)) + list(range(18, 23)) + list(range(26, 35)) + list(range(36, 44)) + list(range(47, 55)):
    f(a.cell(r, 8), f'=IF(ISNUMBER(SEARCH("բանկային",C{r})),1,0)', '0', fill=YEL, sz=10)
a['H2'].value = 'Օժանդակ սյունակ․ 1՝ եթե տողը բանկային վարկ է'; a['H2'].font = Font(name=F, sz=9, italic=True, color='666666')

for col in 'EFG':
    for r in range(66, 78):
        a[f'{col}{r}'].font = Font(name=F, sz=12)
for c, v in (('E', '2024թ.'), ('F', '2025թ.'), ('G', 'Փոփոխություն')):
    pass

E = lambda r, col: f'{col}{r}'
for col in 'EF':
    f(a[f'{col}66'], f'={col}9+{col}15-{col}23', NUM)
    f(a[f'{col}67'], f'={col}35+{col}44-{col}55', NUM)
    f(a[f'{col}68'], f'=({col}82+{col}83)/2', NUM)
    f(a[f'{col}69'], f'={col}84/{col}68', D4)
    f(a[f'{col}70'], f'={col}68/{col}84*{col}65', D2)
    f(a[f'{col}71'], f'={col}67/{col}58', PCT)
    f(a[f'{col}72'], f'={col}57/{col}83', PCT)
    f(a[f'{col}73'], f'={col}88/{col}83', PCT)
    f(a[f'{col}74'], f'={col}60/{col}83', PCT)
for r, fmt in ((66, NUM), (67, NUM), (68, NUM), (69, D4), (70, D2), (71, PCT), (72, PCT), (73, PCT), (74, PCT)):
    f(a[f'G{r}'], f'=F{r}-E{r}', fmt, bold=True)
# factor analysis ShBT = ZSh/H * H/FP
f(a['E75'], 'պայմ.', None, fill=None); f(a['F75'], '=E60/E59*F59/F83', PCT); f(a['G75'], '=F75-E74', PCT, bold=True)
f(a['E76'], '', None, fill=None); f(a['F76'], '', None, fill=None); f(a['G76'], '=F74-F75', PCT, bold=True)
a['F75'].comment = Comment('Պայմանական ցուցանիշ՝ 2024-ի իրացման շահութաբերություն × 2025-ի Հ/ՖՊ (ֆինանսական պարտավորությունների արդյունավետություն)', 'HR')
f(a['C77'], 'Ստուգում՝ 9.1 + 9.2 − ΔՇԲԹՖՊ (պետք է լինի 0)', fill=None, sz=11)
f(a['G77'], '=ROUND(G75+G76-G74,10)', D4, fill=YEL)
a['G64'].value = 'Փոփոխություն'

# helper block
hdr = [('B80', 'ՕԺԱՆԴԱԿ ՀԱՇՎԱՐԿՆԵՐ')]
a['B80'].value = 'ՕԺԱՆԴԱԿ ՀԱՇՎԱՐԿՆԵՐ'; a['B80'].font = Font(name=F, sz=13, bold=True, color='0F5132')
for c, v in (('C81', 'Ցուցանիշ'), ('D81', 'Նշան'), ('E81', '2024թ.'), ('F81', '2025թ.'), ('G81', 'Փոփոխություն')):
    a[c].value = v; a[c].font = Font(name=F, sz=12, bold=True, color='FFFFFF'); a[c].fill = HDR; a[c].border = BOX
rows = [
 (82, 'Ֆինանսական պարտավորություններ տարեսկզբին (ոչ ընթացիկ + ընթացիկ)', 'ՖՊսկիզբ', lambda c: f'={c}9+{c}35', NUM),
 (83, 'Ֆինանսական պարտավորություններ տարեվերջին (ՖՊ)', 'ՖՊ', lambda c: f'={c}66+{c}67', NUM),
 (84, 'Փաստացի մարված ֆինանսական պարտավորություններ\n(առանց ոչ ընթացիկից ընթացիկ տեղափոխման)', 'ՖՊմարվ', lambda c: f'=SUMIF($D$18:$D$22,"ՈԸՖՊմարվ",{c}18:{c}22)+{c}55', NUM),
 (85, 'Ներքին տեղափոխում՝ ոչ ընթացիկից ընթացիկ', 'ՈԸՖՊըպ', lambda c: f'=SUMIF($D$18:$D$22,"ՈԸՖՊըպ",{c}18:{c}22)', NUM),
 (86, 'Բանկային վարկեր տարեվերջին՝ ոչ ընթացիկ', 'ԲՎոըֆպ', lambda c: f'=SUMPRODUCT({c}4:{c}8,$H$4:$H$8)+SUMPRODUCT({c}10:{c}14,$H$10:$H$14)-SUMPRODUCT({c}18:{c}22,$H$18:$H$22)', NUM),
 (87, 'Բանկային վարկեր տարեվերջին՝ ընթացիկ', 'ԲՎըֆպ', lambda c: f'=SUMPRODUCT({c}26:{c}34,$H$26:$H$34)+SUMPRODUCT({c}36:{c}43,$H$36:$H$43)-SUMPRODUCT({c}47:{c}54,$H$47:$H$54)', NUM),
 (88, 'Բանկային վարկեր տարեվերջին՝ ընդամենը', 'ԲՎ', lambda c: f'={c}86+{c}87', NUM),
 (89, 'Իրացման (հասույթի) շահութաբերություն, %', 'ՇԲԹիր', lambda c: f'={c}60/{c}59', PCT),
 (90, 'Ֆինանսական պարտավորությունների արդյունավետություն (Հ ÷ ՖՊ)', 'ՖՊարդյ', lambda c: f'={c}59/{c}83', D4),
 (91, 'Ստուգում՝ 2024 տարեվերջ = 2025 տարեսկիզբ', '', None, None),
 (92, 'Այլընտրանք․ մարվածը՝ ձևանմուշի «մարված կամ տեղափոխված» տողերի ուղիղ գումարով (ներառում է 22 000 ներքին տեղափոխում)', 'ՖՊմարվ*', lambda c: f'={c}23+{c}55', NUM),
 (93, 'Այլընտրանք․ շրջանառելիություն (պտույտ)', 'ՇՐՋՖՊ*', lambda c: f'={c}92/{c}68', D4),
 (94, 'Այլընտրանք․ պտույտի տևողություն (օր)', 'Tօր*', lambda c: f'={c}68/{c}92*{c}65', D2),
]
for r, t, s, fn, fmt in rows:
    f(a[f'C{r}'], t, fill=None); f(a[f'D{r}'], s, fill=None)
    if fn:
        f(a[f'E{r}'], fn('E'), fmt); f(a[f'F{r}'], fn('F'), fmt); f(a[f'G{r}'], f'=F{r}-E{r}', fmt, bold=True)
f(a['E91'], '=IF(AND(E66=F9,E67=F35),"✔ համընկնում է","✖ ստուգել")', None, fill=YEL)
a['C84'].comment = Comment('Ոչ ընթացիկ պարտավորության այն մասը, որը տեղափոխվում է ընթացիկ, իրականում չի մարվում․ այն մեկ անգամ ևս հայտնվում է ընթացիկ ձևավորվածների մեջ և մարվում արդեն այնտեղ։ Կրկնահաշվարկից խուսափելու համար մարվածի մեջ ներառված է միայն փաստացի մարումը։', 'HR')
for r in range(82, 95): a.row_dimensions[r].height = 34
f(a['C95'], 'Հիմնական հաշվարկում (տող 4–5) ընդունված է փաստացի մարումը, քանի որ տեղափոխումը ոչ ընթացիկից ընթացիկ մարում չէ․ այն կրկնակի կհաշվվեր։', fill=None, sz=10)
a.row_dimensions[95].height = 40

CONC = [
 'ԵԶՐԱԿԱՑՈՒԹՅՈՒՆ',
 '1. Ֆինանսական պարտավորությունների ընդհանուր գումարը 2024թ. վերջին կազմել է 197 000, 2025թ. վերջին՝ 171 000 (−26 000)։ Կրճատվել են ոչ ընթացիկ պարտավորությունները (158 000 → 116 000), իսկ ընթացիկները աճել են (39 000 → 55 000)․ պարտքի կառուցվածքը «կարճացել» է, ինչը մեծացնում է մոտակա վճարումների բեռը։',
 '2. Շրջանառելիությունը դանդաղել է՝ 0.4620 → 0.4402 պտույտ, իսկ մեկ պտույտի տևողությունը աճել է 779.2 → 817.8 օր (+38.6 օր)։ Միջին պարտքն աճել է (164 500 → 184 000) ավելի արագ, քան փաստացի մարումները (76 000 → 81 000)։',
 '3. Ընթացիկ պարտավորություններում ֆինանսական պարտավորությունների կշիռը գրեթե չի փոխվել (19.50% → 19.64%)։ Ժամկետանց պարտավորությունների կշիռը նվազել է 2.03% → 1.75%՝ դրական միտում։',
 '4. Բանկային վարկերի կշիռը աճել է 72.59% → 87.72%․ ընկերությունն ավելի կախված է դարձել բանկերից (տոկոսային և վերաֆինանսավորման ռիսկ)։',
 '5. Ֆինանսական պարտավորությունների շահութաբերությունն աճել է 5.08% → 6.43% (+1.36 պ.կ.)։ Գործոնային վերլուծություն․ պարտավորությունների արդյունավետության (Հ/ՖՊ) աճը տվել է +2.31 պ.կ., իսկ իրացման շահութաբերության անկումը (1.05% → 0.92%)՝ −0.95 պ.կ.։',
 'Առաջարկ․ բարելավել իրացման շահութաբերությունը, պլանավորել ընթացիկ մարումների դրամական հոսքերը և դիվերսիֆիկացնել ֆինանսավորման աղբյուրները՝ նվազեցնելով բանկային վարկերի կշիռը։',
]
for i, t in enumerate(CONC):
    r = 97 + i; a.merge_cells(f'B{r}:G{r}'); c = a[f'B{r}']; c.value = t
    c.font = Font(name=F, sz=12, bold=(i == 0), color='0F5132' if i == 0 else '000000'); c.alignment = Alignment(wrap_text=True, vertical='top')
    a.row_dimensions[r].height = 18 if i == 0 else 52

# ---------------- Sheet 2 ----------------
b['D3'].value = 't0'
for col in 'DE':
    f(b[f'{col}8'], f'={col}5/{col}7', D4); f(b[f'{col}9'], f'={col}7/{col}5*360', D2)
f(b['C5'], 'հազ.դր.', fill=None, sz=10)
for r, fmt in ((5, NUM), (7, NUM), (8, D4), (9, D2)): f(b[f'F{r}'], f'=E{r}-D{r}', fmt, bold=True)
# 11.1.5
for col in 'DE':
    f(b[f'{col}18'], f'={col}16/{col}17', D4); f(b[f'{col}19'], f'={col}17/{col}16*360', D2)
f(b['A19'], 4, fill=None); f(b['B19'], 'Շրջանառելիություն՝ ըստ օրերի', fill=None, sz=10); f(b['C19'], 'օր', fill=None, sz=10)
for r, fmt in ((16, NUM), (17, NUM), (18, D4), (19, D2)): f(b[f'F{r}'], f'=E{r}-D{r}', fmt, bold=True)
# 11.1.3 — move misplaced 12500 into the ST-loans row
b['C35'].value = None; b['C34'].value = 12500; b.merge_cells('C34:C36')
data_rows = [26, 27, 29, 31, 32, 34]
f(b['C37'], '=C26+C31', NUM, bold=True); f(b['E37'], '=E26+E31', NUM, bold=True)
for r in data_rows + [37]:
    f(b[f'D{r}'], f'=C{r}/C$37', PCT); f(b[f'F{r}'], f'=E{r}/E$37', PCT)
    f(b[f'G{r}'], f'=E{r}-C{r}', NUM, bold=True); f(b[f'H{r}'], f'=F{r}-D{r}', PCT, bold=True)
f(b['B37'], 'Ընդամենը', fill=None, bold=True, sz=10)
f(b['B38'], 'Ստուգում՝ ենթահոդվածների տարբերություն (հոդված − բաղադրիչներ)', fill=None, sz=9)
f(b['C38'], '=(C26-C27-C29)+(C31-C32-C34)', NUM, fill=YEL); f(b['E38'], '=(E26-E27-E29)+(E31-E32-E34)', NUM, fill=YEL)
b['B39'].value = 'Ծանոթ․ t1-ում ընթացիկ ՖՊ-ն տրված է 52 200, իսկ բաղադրիչների գումարը 30 500 + 19 700 = 50 200 է (2 000 տարբերություն տվյալներում)։ Հոդվածի ընդհանուր գումարը պահպանված է ինչպես տրված է (52 200), կշիռները՝ 227 600-ի նկատմամբ։'
b['B39'].font = Font(name=F, sz=9, italic=True, color='9C2A00'); b['B39'].alignment = Alignment(wrap_text=True); b.merge_cells('B39:H39'); b.row_dimensions[39].height = 42
b['B40'].value = 'Ծանոթ․ դասագրքի աղ. 13.1-ում «Ընդամենը»-ն տրված է 164 200 / 195 100, որը չի համընկնում բաղադրիչների գումարի հետ (151 700 + 45 900 = 197 600, 175 400 + 52 200 = 227 600)։ Այստեղ կշիռները հաշվարկված են ճիշտ ընդհանուր գումարի նկատմամբ։'
b['B40'].font = Font(name=F, sz=9, italic=True, color='9C2A00'); b['B40'].alignment = Alignment(wrap_text=True); b.merge_cells('B40:H40'); b.row_dimensions[40].height = 42
b['B11'].value = 'Ծանոթ․ օրերը հաշվարկված են 360-օրյա տարով (դասախոսության բանաձև). դասագրքի աղ. 13.2-ի 195 և 231 օրը ստացվում են 365 օրով։'
b['B11'].font = Font(name=F, sz=9, italic=True, color='9C2A00'); b['B11'].alignment = Alignment(wrap_text=True); b.merge_cells('B11:F11'); b.row_dimensions[11].height = 30
for c in 'CDEFGH': b.column_dimensions[c].width = max(b.column_dimensions[c].width or 0, 13)
CONC2 = ['ԵԶՐԱԿԱՑՈՒԹՅՈՒՆ',
 '11.1.4․ Մարված ընթացիկ ֆինանսական պարտավորությունները նվազել են 92 400-ով, միջին արժեքը՝ 17 800-ով։ Շրջանառելիությունը դանդաղել է 1.8686 → 1.5781 պտույտ (−0.2905), մեկ պտույտը երկարել է 192.7 → 228.1 օր (+35.5 օր)․ բացասական միտում։',
 '11.1.5․ Մարումները նվազել են (97 200 → 75 400), իսկ միջին արժեքը կրկնապատկվել է (46 400 → 97 600)։ Շրջանառելիությունը կտրուկ ընկել է 2.0948 → 0.7725 պտույտ (−1.3223), պտույտի տևողությունը 171.9 → 466.0 օր․ պարտքերը կուտակվում են։',
 '11.1.3․ Ֆինանսական պարտավորություններն աճել են 30 000-ով (197 600 → 227 600)՝ ոչ ընթացիկների հաշվին (+23 700, կշիռը 76.77% → 77.07%)։ Աճը հիմնականում երկարաժամկետ բանկային վարկերի հաշվին է (+33 000, կշիռը 60.88% → 67.35%), երկարաժամկետ փոխառությունները նվազել են (−9 300)։ Ընթացիկների կշիռը թեթևակի նվազել է (23.23% → 22.93%), կարճաժամկետ փոխառությունների կշիռը աճել է (6.33% → 8.66%)։']
for i, t in enumerate(CONC2):
    r = 43 + i; b.merge_cells(f'B{r}:H{r}'); c = b[f'B{r}']; c.value = t
    c.font = Font(name=F, sz=10, bold=(i == 0), color='0F5132' if i == 0 else '000000'); c.alignment = Alignment(wrap_text=True, vertical='top')
    b.row_dimensions[r].height = 16 if i == 0 else 46


# =====================================================================
#  DESIGNED SHEETS (dashboard / analysis / task 2 / conclusions)
# =====================================================================
from openpyxl.chart import LineChart, DoughnutChart, BarChart, Reference
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import DataBarRule, IconSetRule, FormulaRule, CellIsRule
from openpyxl.worksheet.hyperlink import Hyperlink
import os
BANNER = sys.argv[3] if len(sys.argv) > 3 else None
BOWL = sys.argv[4] if len(sys.argv) > 4 else None

INKc, INDc, IND2c, IND3c, REDc, GOLDc, PAPc, PAP2c, GRN = '1B1A24', '1F3A68', '2F5D8F', '8FB3D1', 'C8102E', 'D4A537', 'EFE3C8', 'F7EFDC', '1D7A3E'
fill = lambda c: PatternFill('solid', fgColor='FF' + c, bgColor='FF' + c)
S1, S2 = "'Տնային 1'", "'Տնային 2'"
a.title = 'Ձևանմուշ · Տնային 1'; b.title = 'Ձևանմուշ · Տնային 2'
S1, S2 = "'Ձևանմուշ · Տնային 1'", "'Ձևանմուշ · Տնային 2'"
for ws in (a, b):
    ws.sheet_properties.tabColor = '9C8F7A'

thinI = Side(style='thin', color='FF8C8170'); ALLB = Border(left=thinI, right=thinI, top=thinI, bottom=thinI); thickI = Side(style='medium', color=INKc)
def box(ws, rng, color=INKc):
    rows = list(ws[rng]); s = Side(style='medium', color=color)
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            c.border = Border(left=s if j == 0 else c.border.left, right=s if j == len(row) - 1 else c.border.right,
                              top=s if i == 0 else c.border.top, bottom=s if i == len(rows) - 1 else c.border.bottom)

def paper(ws, cols=16, rows=80, widths=None):
    ws.sheet_view.showGridLines = False
    for r in range(1, rows + 1):
        for c in range(1, cols + 1): ws.cell(r, c).fill = fill(PAP2c)
    if widths:
        for k, v in widths.items(): ws.column_dimensions[k].width = v

def cell(ws, ref, v, sz=11, bold=False, color=INKc, bg=None, fmt=None, h='left', v_='center', wrap=False, italic=False, font=F, border=None):
    c = ws[ref]; c.value = v; c.font = Font(name=font, sz=sz, bold=bold, color=color, italic=italic)
    if bg: c.fill = fill(bg)
    if fmt: c.number_format = fmt
    c.alignment = Alignment(horizontal=h, vertical=v_, wrap_text=wrap)
    if border: c.border = border
    return c

def banner(ws, title, sub, last='N'):
    ws.merge_cells(f'B2:{last}2'); ws.merge_cells(f'B3:{last}3')
    for r, (t, sz, col, bg) in ((2, (title, 22, PAP2c, INDc)), (3, (sub, 11, 'F6EFE0', IND2c))):
        cell(ws, f'B{r}', t, sz, True if r == 2 else False, col, bg)
        for cc in ws[f'B{r}:{last}{r}'][0]: cc.fill = fill(bg)
    ws.row_dimensions[2].height = 40; ws.row_dimensions[3].height = 22
    # red seal
    cell(ws, f'{last}2', 'ՖՊ', 16, True, 'FFFFFF', REDc, h='center') if False else None

def nav(ws, row, here, last='N'):
    items = [('⌂ Վահանակ', 'Վահանակ'), ('Ա · Շարժ', 'Շարժ'), ('Բ · 9 ցուցանիշ', 'Վերլուծություն'), ('Գ · Տնային 2', 'Տնային 2 ✦'), ('Դ · Եզրակացություն', 'Եզրակացություն'),
             ('Ձևանմուշ 1', 'Ձևանմուշ · Տնային 1'), ('Ձևանմուշ 2', 'Ձևանմուշ · Տնային 2')]
    col = 2
    for lab, sh in items:
        c = ws.cell(row, col, lab); on = sh == here
        c.font = Font(name=F, sz=10, bold=True, color='FFFFFF' if on else INKc, underline=None if on else 'single')
        c.fill = fill(REDc if on else 'E9DCC0'); c.alignment = Alignment(horizontal='center', vertical='center')
        c.border = Border(left=thinI, right=thinI, top=thinI, bottom=thinI)
        if not on: c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'{sh}'!A1", display=lab)
        col += 2 if col < 14 else 1
    ws.row_dimensions[row].height = 22

def hdr(ws, row, c0, labels, bg=INKc):
    for i, t in enumerate(labels):
        c = ws.cell(row, c0 + i, t); c.font = Font(name=F, sz=10, bold=True, color='FFFFFF'); c.fill = fill(bg)
        c.alignment = Alignment(horizontal='center' if i else 'left', vertical='center', wrap_text=True); c.border = Border(left=thinI, right=thinI, top=thinI, bottom=Side(style='medium', color='FF' + REDc))
    ws.row_dimensions[row].height = 30

def rowfmt(ws, row, c0, n, zebra, fmts):
    for i in range(n):
        c = ws.cell(row, c0 + i); c.fill = fill('F1E6CC' if zebra else 'FFFFFF'); c.border = ALLB
        c.font = Font(name=F, sz=11, bold=c.font.bold, color=c.font.color.rgb if c.font and c.font.color and isinstance(c.font.color.rgb, str) else INKc)
        if i: c.alignment = Alignment(horizontal='right', vertical='center')
        else: c.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        if fmts and i < len(fmts) and fmts[i]: c.number_format = fmts[i]
    ws.row_dimensions[row].height = 21

def section(ws, ref_from, ref_to, text, color=REDc):
    ws.merge_cells(f'{ref_from}:{ref_to}'); c = ws[ref_from]; c.value = text
    c.font = Font(name=F, sz=13, bold=True, color=INKc); c.alignment = Alignment(vertical='bottom')
    for cc in ws[f'{ref_from}:{ref_to}'][0]: cc.border = Border(bottom=Side(style='thick', color=color))
    ws.row_dimensions[c.row].height = 26

def colorize(series, color, line=False, w=28000):
    if line:
        series.graphicalProperties.line.solidFill = color; series.graphicalProperties.line.width = w; series.smooth = True
    else:
        series.graphicalProperties.solidFill = color; series.graphicalProperties.line.solidFill = INKc

def style_chart(ch, title, w=16, h=8.2):
    ch.title = title; ch.width = w; ch.height = h; ch.legend.position = 'b'
    ch.graphical_properties = GraphicalProperties(); ch.graphical_properties.solidFill = PAP2c; ch.graphical_properties.line.solidFill = INKc
    try:
        ch.plot_area.graphicalProperties = GraphicalProperties(); ch.plot_area.graphicalProperties.solidFill = 'FBF6EA'
    except Exception: pass
    return ch

def labels(ch, fmt=None):
    ch.dataLabels = DataLabelList(); ch.dataLabels.showVal = True; ch.dataLabels.showSerName = False; ch.dataLabels.showCatName = False; ch.dataLabels.showLegendKey = False
    if fmt: ch.dataLabels.numFmt = fmt

# ---------------- 1) DASHBOARD ----------------
d = wb.create_sheet('Վահանակ', 0); d.sheet_properties.tabColor = REDc
paper(d, 16, 95, {'A': 2, 'B': 22, **{c: 12.5 for c in 'CDEFGHIJKLMN'}, 'O': 2, 'P': 2})
if BANNER and os.path.exists(BANNER):
    img = XLImage(BANNER); img.width, img.height = 1180, 290; d.add_image(img, 'B5')
banner(d, '«XXX» ՍՊԸ · Ֆինանսական պարտավորությունների վերլուծություն', 'Տնտեսական գործունեության վերլուծություն · Թեմա 10 · Դաս 9 · Դասախոս՝ Օ. Ա. Գալստյան · Կատարող՝ Հրաչյա Ասլանյան, ԻՏ-447 · հազ. դրամ')
nav(d, 4, 'Վահանակ')
for r in range(5, 21): d.row_dimensions[r].height = 15
# KPI tiles (rows 21-25), each 3 columns wide
tiles = [('ՖՊ տարեվերջին · 2025', f"={S1}!F83", NUM, f'={S1}!F83-{S1}!E83', NUM, 'նվազում = լավ', 'down'),
         ('Մեկ պտույտ, օր · 2025', f"={S1}!F70", '0.0', f'={S1}!F70-{S1}!E70', '+0.0;-0.0', 'աճ = վատ', 'down'),
         ('Բանկային վարկերի կշիռ', f"={S1}!F73", '0.00%', f'={S1}!F73-{S1}!E73', '+0.00%;-0.00%', 'աճ = ռիսկ ↑', 'down'),
         ('ՖՊ շահութաբերություն', f"={S1}!F74", '0.00%', f'={S1}!F74-{S1}!E74', '+0.00%;-0.00%', 'աճ = լավ', 'up')]
cols = ['B', 'E', 'H', 'K']
for (lab, f1, fm1, f2, fm2, hint, good), c0 in zip(tiles, cols):
    c1 = chr(ord(c0) + 2)
    for r in range(21, 26):
        for cc in d[f'{c0}{r}:{c1}{r}'][0]: cc.fill = fill('FBF6EA')
    d.merge_cells(f'{c0}21:{c1}21'); d.merge_cells(f'{c0}22:{c1}23'); d.merge_cells(f'{c0}24:{c1}24'); d.merge_cells(f'{c0}25:{c1}25')
    cell(d, f'{c0}21', lab, 10, True, REDc, 'FBF6EA')
    cell(d, f'{c0}22', f1, 24, True, INKc, 'FBF6EA', fm1, 'left')
    cell(d, f'{c0}24', f2, 12, True, INKc, 'FBF6EA', fm2)
    cell(d, f'{c0}25', 'Δ 2024 → 2025 · ' + hint, 9, False, '6A5F6E', 'FBF6EA', italic=True)
    for cc in d[f'{c0}26:{c1}26'][0]: cc.fill = fill(REDc if good == 'down' and c0 in 'EH' else GRN if c0 in 'BK' else REDc)
    box(d, f'{c0}21:{c1}26')
    rng = f'{c0}24'; dn = good == 'down'
    d.conditional_formatting.add(rng, CellIsRule(operator='lessThan', formula=['0'], font=Font(name=F, color=GRN if dn else REDc, bold=True)))
    d.conditional_formatting.add(rng, CellIsRule(operator='greaterThan', formula=['0'], font=Font(name=F, color=REDc if dn else GRN, bold=True)))
d.row_dimensions[22].height = 22; d.row_dimensions[23].height = 22; d.row_dimensions[26].height = 5

# chart data block (visible, formula-linked) rows 60+
section(d, 'B58', 'N58', '◆ Գծապատկերների տվյալներ (կապված բանաձևերով)')
hdr(d, 59, 2, ['Ամսաթիվ', 'Ոչ ընթացիկ', 'Ընթացիկ', 'Ընդամենը ՖՊ', 'Բանկային'])
dates = [('01.01.2024', f'={S1}!E9', f'={S1}!E35', f'=SUMPRODUCT({S1}!E4:E8,{S1}!H4:H8)+SUMPRODUCT({S1}!E26:E34,{S1}!H26:H34)'),
         ('31.12.2024', f'={S1}!E66', f'={S1}!E67', f'={S1}!E88'), ('31.12.2025', f'={S1}!F66', f'={S1}!F67', f'={S1}!F88')]
for i, (dt, nc, cu, bk) in enumerate(dates):
    r = 60 + i; d[f'B{r}'] = dt; d[f'C{r}'] = nc; d[f'D{r}'] = cu; d[f'E{r}'] = f'=C{r}+D{r}'; d[f'F{r}'] = bk
    rowfmt(d, r, 2, 5, i % 2, [None, NUM, NUM, NUM, NUM])
hdr(d, 64, 2, ['Կառուցվածք 2025', 'Արժեք'])
for i, (t, f_) in enumerate((('Ոչ ընթացիկ ՖՊ', f'={S1}!F66'), ('Ընթացիկ ՖՊ', f'={S1}!F67'))):
    d[f'B{65+i}'] = t; d[f'C{65+i}'] = f_; rowfmt(d, 65 + i, 2, 2, i % 2, [None, NUM])
hdr(d, 68, 2, ['Պտույտ, օր', '2024', '2025'])
for i, (t, r1) in enumerate((('Փաստացի մարումով', 70), ('Ձևանմուշի գումարով', 94))):
    d[f'B{69+i}'] = t; d[f'C{69+i}'] = f'={S1}!E{r1}'; d[f'D{69+i}'] = f'={S1}!F{r1}'; rowfmt(d, 69 + i, 2, 3, i % 2, [None, '0.0', '0.0'])
hdr(d, 72, 2, ['Գործոնային (պ.կ.)', 'Հիմք', 'Ընդամենը', 'Աճ', 'Նվազում'])
fac = [('ՇԲԹ 2024', '0', f'={S1}!E74*100', '0', '0'),
       ('Հ / ՖՊ', f'={S1}!E74*100+MIN({S1}!G75*100,0)', '0', f'=MAX({S1}!G75*100,0)', f'=MAX(-{S1}!G75*100,0)'),
       ('ԶՇ / Հ', f'=({S1}!E74+{S1}!G75)*100+MIN({S1}!G76*100,0)', '0', f'=MAX({S1}!G76*100,0)', f'=MAX(-{S1}!G76*100,0)'),
       ('ՇԲԹ 2025', '0', f'={S1}!F74*100', '0', '0')]
for i, row in enumerate(fac):
    r = 73 + i
    for j, v in enumerate(row): d.cell(r, 2 + j, float(v) if v == '0' else v)
    rowfmt(d, r, 2, 5, i % 2, [None, '0.00', '0.00', '0.00', '0.00'])
hdr(d, 78, 2, ['Կշիռներ', '2024', '2025'])
for i, (t, rr) in enumerate((('Բանկային վարկեր', 73), ('ԸՖՊ / ԸՊ', 71), ('ՇԲԹֆպ', 74), ('Ժամկետանց', 72))):
    d[f'B{79+i}'] = t; d[f'C{79+i}'] = f'={S1}!E{rr}'; d[f'D{79+i}'] = f'={S1}!F{rr}'; rowfmt(d, 79 + i, 2, 3, i % 2, [None, '0.00%', '0.00%'])

# charts on dashboard (rows 28-56)
section(d, 'B27', 'N27', '◆ Ալիքի շարժը')
lc = LineChart(); style_chart(lc, 'Ֆինանսական պարտավորություններ, հազ. դր.', 19, 8.5)
lc.add_data(Reference(d, min_col=3, max_col=6, min_row=59, max_row=62), titles_from_data=True); lc.set_categories(Reference(d, min_col=2, min_row=60, max_row=62))
for s_, col in zip(lc.series, (INDc, IND3c, INKc, REDc)): colorize(s_, col, True, 38000); s_.marker.symbol = 'circle'; s_.marker.size = 9; s_.marker.graphicalProperties.solidFill = col
lc.series[2].graphicalProperties.line.width = 52000; lc.series[3].graphicalProperties.line.dashStyle = 'dash'
labels(lc, '#,##0'); lc.y_axis.numFmt = '#,##0'; lc.y_axis.majorGridlines = None; lc.y_axis.delete = False; lc.x_axis.delete = False
d.add_chart(lc, 'B28')
dn = DoughnutChart(); style_chart(dn, 'Կառուցվածք 31.12.2025', 9.2, 8.5); dn.holeSize = 55
dn.add_data(Reference(d, min_col=3, min_row=64, max_row=66), titles_from_data=True); dn.set_categories(Reference(d, min_col=2, min_row=65, max_row=66))
from openpyxl.chart.series import DataPoint
for k, col in enumerate((INDc, IND3c)):
    pt = DataPoint(idx=k); pt.graphicalProperties.solidFill = col; pt.graphicalProperties.line.solidFill = 'FFFFFF'; dn.series[0].dPt.append(pt)
dn.dataLabels = DataLabelList(); dn.dataLabels.showPercent = True; dn.dataLabels.showVal = False; dn.dataLabels.showCatName = False; dn.dataLabels.showSerName = False; dn.dataLabels.showLegendKey = False
d.add_chart(dn, 'K28')
section(d, 'B44', 'N44', '◆ Պտույտ և գործոններ')
bc = BarChart(); bc.type = 'bar'; style_chart(bc, 'Մեկ պտույտի տևողություն, օր', 12.5, 7)
bc.add_data(Reference(d, min_col=3, max_col=4, min_row=68, max_row=70), titles_from_data=True); bc.set_categories(Reference(d, min_col=2, min_row=69, max_row=70))
colorize(bc.series[0], '9C8F7A'); colorize(bc.series[1], REDc); labels(bc, '0.0'); bc.y_axis.numFmt = '0'; bc.y_axis.majorGridlines = None; bc.gapWidth = 60; bc.y_axis.delete = False; bc.x_axis.delete = False
d.add_chart(bc, 'B45')
wf = BarChart(); wf.type = 'col'; wf.grouping = 'stacked'; wf.overlap = 100; style_chart(wf, 'ՇԲԹֆպ · գործոնային վերլուծություն, պ.կ.', 12.8, 7)
wf.add_data(Reference(d, min_col=3, max_col=6, min_row=72, max_row=76), titles_from_data=True); wf.set_categories(Reference(d, min_col=2, min_row=73, max_row=76))
wf.series[0].graphicalProperties.noFill = True; wf.series[0].graphicalProperties.line.noFill = True
colorize(wf.series[1], INDc); colorize(wf.series[2], GOLDc); colorize(wf.series[3], REDc); wf.gapWidth = 40; wf.y_axis.majorGridlines = None; wf.y_axis.delete = False; wf.x_axis.delete = False
for s_ in wf.series[1:]:
    s_.dLbls = DataLabelList(); s_.dLbls.showVal = True; s_.dLbls.showSerName = False; s_.dLbls.showCatName = False; s_.dLbls.showLegendKey = False; s_.dLbls.numFmt = '0.00;-0.00;;'
d.add_chart(wf, 'H45')
d.freeze_panes = 'A5'

# ---------------- 2) MOVEMENT ----------------
m = wb.create_sheet('Շարժ', 1); m.sheet_properties.tabColor = INDc
paper(m, 16, 60, {'A': 2, 'B': 46, **{c: 14 for c in 'CDEFGH'}, 'I': 3, 'J': 14, 'K': 14, 'L': 14, 'M': 14, 'N': 14})
banner(m, 'Ա · Ֆինանսական պարտավորությունների շարժ', 'Տարեսկիզբ + ձևավորված − մարված (տեղափոխված) = տարեվերջ · տվյալները՝ «Ձևանմուշ · Տնային 1» թերթից', 'N'); nav(m, 4, 'Շարժ')
section(m, 'B6', 'H6', '◆ Շարժի աղյուսակ')
hdr(m, 7, 2, ['Հոդված', 'Տարեսկիզբ', 'Ձևավորված', 'Մարված / տեղափ.', 'Տարեվերջ', 'Փոփոխ.', 'Աճի տեմպ'])
mvr = [('Ոչ ընթացիկ ՖՊ · 2024', 'E', 9, 15, 23), ('Ոչ ընթացիկ ՖՊ · 2025', 'F', 9, 15, 23), ('Ընթացիկ ՖՊ · 2024', 'E', 35, 44, 55), ('Ընթացիկ ՖՊ · 2025', 'F', 35, 44, 55)]
for i, (t, c_, s_, f_, r_) in enumerate(mvr):
    r = 8 + i; m[f'B{r}'] = t; m[f'C{r}'] = f'={S1}!{c_}{s_}'; m[f'D{r}'] = f'={S1}!{c_}{f_}'; m[f'E{r}'] = f'=-{S1}!{c_}{r_}'
    m[f'F{r}'] = f'=C{r}+D{r}+E{r}'; m[f'G{r}'] = f'=F{r}-C{r}'; m[f'H{r}'] = f'=IF(C{r}=0,"–",F{r}/C{r})'
    rowfmt(m, r, 2, 7, i % 2, [None, NUM, '+#,##0;-#,##0;"–"', '+#,##0;-#,##0;"–"', NUM, '+#,##0;-#,##0;"–"', '0.0%'])
    m[f'F{r}'].font = Font(name=F, sz=11, bold=True, color=INKc)
for i, (t, cc) in enumerate((('Ընդամենը ՖՊ · 2024', 'E'), ('Ընդամենը ՖՊ · 2025', 'F'))):
    r = 12 + i; m[f'B{r}'] = t
    for col in 'CDEFG': m[f'{col}{r}'] = f'={col}{8+i}+{col}{10+i}'
    m[f'H{r}'] = f'=F{r}/C{r}'
    rowfmt(m, r, 2, 7, 0, [None, NUM, '+#,##0;-#,##0;"–"', '+#,##0;-#,##0;"–"', NUM, '+#,##0;-#,##0;"–"', '0.0%'])
    for col in 'BCDEFGH': m[f'{col}{r}'].font = Font(name=F, sz=11, bold=True, color='FFFFFF'); m[f'{col}{r}'].fill = fill(INDc)
m.conditional_formatting.add('G8:G13', IconSetRule('3Arrows', 'num', [-1e-9, 0, 1e-9], showValue=None, reverse=True))
m.conditional_formatting.add('F8:F11', DataBarRule(start_type='num', start_value=0, end_type='max', color=IND3c, showValue=True))
section(m, 'B15', 'H15', '◆ Բանկային վարկեր և փաստացի մարում')
hdr(m, 16, 2, ['Ցուցանիշ', '2024', '2025', 'Փոփոխ.'])
for i, (t, rr, fm) in enumerate((('Բանկային վարկեր՝ ոչ ընթացիկ', 86, NUM), ('Բանկային վարկեր՝ ընթացիկ', 87, NUM), ('Բանկային վարկեր՝ ընդամենը', 88, NUM),
                                 ('Փաստացի մարված ՖՊ (առանց տեղափոխման)', 84, NUM), ('Ներքին տեղափոխում ոչ ընթացիկից ընթացիկ', 85, NUM),
                                 ('Ձևանմուշի «մարված կամ տեղափոխված» ուղիղ գումար', 92, NUM))):
    r = 17 + i; m[f'B{r}'] = t; m[f'C{r}'] = f'={S1}!E{rr}'; m[f'D{r}'] = f'={S1}!F{rr}'; m[f'E{r}'] = f'=D{r}-C{r}'
    rowfmt(m, r, 2, 4, i % 2, [None, fm, fm, '+#,##0;-#,##0;"–"'])
cell(m, 'B24', 'Ստուգում՝ 2024 տարեվերջ = 2025 տարեսկիզբ', 10, True); cell(m, 'C24', f'={S1}!E91', 10, True, GRN)
mc = BarChart(); mc.type = 'col'; style_chart(mc, 'Տարեսկիզբ, ձևավորված, մարված և տարեվերջ', 18, 8)
mc.add_data(Reference(m, min_col=3, max_col=6, min_row=7, max_row=11), titles_from_data=True); mc.set_categories(Reference(m, min_col=2, min_row=8, max_row=11))
for s_, col in zip(mc.series, (IND3c, GOLDc, REDc, INDc)): colorize(s_, col)
labels(mc, '#,##0'); mc.y_axis.majorGridlines = None; mc.y_axis.numFmt = '#,##0'; mc.gapWidth = 50; mc.y_axis.delete = False; mc.x_axis.delete = False
m.add_chart(mc, 'J6')
bk = BarChart(); bk.type = 'col'; bk.grouping = 'stacked'; bk.overlap = 100; style_chart(bk, 'Բանկային վարկեր՝ ոչ ընթացիկ + ընթացիկ', 18, 7.5)
bk.add_data(Reference(m, min_col=3, max_col=4, min_row=17, max_row=18), from_rows=True, titles_from_data=False)
bk.series[0].tx = SeriesLabel(v='Ոչ ընթացիկ'); bk.series[1].tx = SeriesLabel(v='Ընթացիկ')
from openpyxl.chart.reference import Reference as R_
bk.set_categories(Reference(m, min_col=3, max_col=4, min_row=16, max_row=16))
colorize(bk.series[0], INDc); colorize(bk.series[1], REDc); labels(bk, '#,##0'); bk.gapWidth = 60; bk.y_axis.majorGridlines = None; bk.y_axis.delete = False; bk.x_axis.delete = False
m.add_chart(bk, 'J23')
m.freeze_panes = 'A5'

# ---------------- 3) ANALYSIS ----------------
v = wb.create_sheet('Վերլուծություն', 2); v.sheet_properties.tabColor = GOLDc
paper(v, 16, 70, {'A': 2, 'B': 5, 'C': 50, 'D': 15, **{c: 13 for c in 'EFG'}, 'H': 26, 'I': 3, **{c: 13 for c in 'JKLMN'}})
banner(v, 'Բ · Ինը ցուցանիշ և գործոնային վերլուծություն', 'Միջին արժեքը՝ (տարեսկիզբ + տարեվերջ) ÷ 2 · կշիռները՝ տարեվերջի ՖՊ-ի նկատմամբ · t = 360 օր', 'N'); nav(v, 4, 'Վերլուծություն')
section(v, 'B6', 'H6', '◆ Վերլուծության արդյունքներ')
hdr(v, 7, 2, ['№', 'Ցուցանիշ', 'Նշան', '2024', '2025', 'Փոփոխ.', 'Գնահատական'])
ind = [(66, 'Ոչ ընթացիկ ՖՊ (տարեվերջ)', 'ՈԸՖՊ', NUM, 'neu'), (67, 'Ընթացիկ ՖՊ (տարեվերջ)', 'ԸՖՊ', NUM, 'up_bad'), (68, 'ՖՊ միջին արժեք', 'ՖՊ', NUM, 'neu'),
       (69, 'Շրջանառելիություն, պտույտ', 'ՇՐՋֆպ', '0.0000', 'up_good'), (70, 'Մեկ պտույտի տևողություն, օր', 'Tօր', '0.0', 'up_bad'),
       (71, 'ԸՖՊ կշիռ ընթացիկ պարտավորություններում', 'ՏԿֆպ', '0.00%', 'neu'), (72, 'Ժամկետանց ՖՊ կշիռ', 'ՏԿժ.անց', '0.00%', 'up_bad'),
       (73, 'Բանկային վարկերի կշիռ', 'ՏԿբվ', '0.00%', 'up_bad'), (74, 'ՖՊ շահութաբերություն', 'ՇԲԹֆպ', '0.00%', 'up_good')]
dfmt = {NUM: '+#,##0;-#,##0;"–"', '0.0000': '+0.0000;-0.0000', '0.0': '+0.0;-0.0', '0.00%': '+0.00%;-0.00%'}
for i, (rr, t, sg, fm, kind) in enumerate(ind):
    r = 8 + i; v[f'B{r}'] = i + 1; v[f'C{r}'] = t; v[f'D{r}'] = sg; v[f'E{r}'] = f'={S1}!E{rr}'; v[f'F{r}'] = f'={S1}!F{rr}'; v[f'G{r}'] = f'=F{r}-E{r}'
    if kind == 'up_good': v[f'H{r}'] = f'=IF(G{r}>0,"▲ բարելավում",IF(G{r}<0,"▼ վատթարացում","= անփոփոխ"))'
    elif kind == 'up_bad': v[f'H{r}'] = f'=IF(G{r}<0,"▲ բարելավում",IF(G{r}>0,"▼ վատթարացում","= անփոփոխ"))'
    else: v[f'H{r}'] = f'=IF(G{r}>0,"↗ աճ",IF(G{r}<0,"↘ նվազում","= անփոփոխ"))'
    rowfmt(v, r, 2, 7, i % 2, ['0', None, None, fm, fm, dfmt[fm], None])
    v[f'D{r}'].alignment = Alignment(horizontal='center'); v[f'D{r}'].font = Font(name=F, sz=11, bold=True, color=REDc); v[f'H{r}'].alignment = Alignment(horizontal='center')
v.conditional_formatting.add('H8:H16', FormulaRule(formula=['LEFT(H8,1)="▲"'], fill=fill('D6EFD9'), font=Font(name=F, bold=True, color=GRN)))
v.conditional_formatting.add('H8:H16', FormulaRule(formula=['LEFT(H8,1)="▼"'], fill=fill('F8D3D3'), font=Font(name=F, bold=True, color=REDc)))
v.conditional_formatting.add('H8:H16', FormulaRule(formula=['OR(LEFT(H8,1)="↗",LEFT(H8,1)="↘")'], fill=fill('DCE6F2'), font=Font(name=F, bold=True, color=INDc)))
section(v, 'B19', 'H19', '◆ ՇԲԹֆպ = ԶՇ/Հ × Հ/ՖՊ · շղթայական տեղադրում')
hdr(v, 20, 2, ['Քայլ', 'Հաշվարկ', 'ԶՇ / Հ', 'Հ / ՖՊ', 'ՇԲԹֆպ', 'Ազդեցություն, պ.կ.', ''])
steps = [('1', 'Բազիս՝ 2024', f'={S1}!E89', f'={S1}!E90', f'={S1}!E74', '–'), ('2', 'Հ/ՖՊ-ն՝ 2025, ԶՇ/Հ-ն՝ 2024', f'={S1}!E89', f'={S1}!F90', f'={S1}!F75', f'=(F22-F21)*100'),
         ('3', 'Երկուսն էլ՝ 2025', f'={S1}!F89', f'={S1}!F90', f'={S1}!F74', f'=(F23-F22)*100')]
for i, row in enumerate(steps):
    r = 21 + i
    for j, val in enumerate(row): v.cell(r, 2 + j, val)
    rowfmt(v, r, 2, 7, i % 2, [None, None, '0.00%', '0.0000', '0.00%', '+0.00;-0.00', None]); v[f'C{r}'].alignment = Alignment(horizontal='left')
r = 24; v[f'C{r}'] = 'Ընդամենը փոփոխություն = 9.1 + 9.2'; v[f'G{r}'] = '=G22+G23'; v[f'H{r}'] = f'=IF(ROUND(G24-{S1}!G74*100,8)=0,"✔ ստուգված","✖")'
rowfmt(v, r, 2, 7, 0, [None, None, None, None, None, '+0.00;-0.00', None])
for col in 'BCDEFGH': v[f'{col}{r}'].fill = fill(INDc); v[f'{col}{r}'].font = Font(name=F, sz=11, bold=True, color='FFFFFF')
v.conditional_formatting.add('G22:G23', DataBarRule(start_type='min', end_type='max', color=GOLDc, showValue=True))
section(v, 'B26', 'H26', '◆ Ինչպես կարդալ')
txt = ['• ՇՐՋֆպ = Փաստացի մարված ՖՊ ÷ ՖՊ միջին․ որքան բարձր, այնքան արագ է մարվում պարտքը։',
       '• Tօր = ՖՊ միջին ÷ մարված ՖՊ × 360․ քանի օր է միջինում պետք պարտքը մարելու համար։',
       '• Մարվածի մեջ ներառված չէ ոչ ընթացիկից ընթացիկ տեղափոխումը (22 000), քանի որ այն մարում չէ։ Ձևանմուշի ուղիղ գումարով տարբերակը՝ «Շարժ» թերթում։',
       '• Բանկային վարկերը որոշված են ըստ տողի անվանման («բանկային վարկ»), տես ձևանմուշի H սյունակը։']
for i, t in enumerate(txt):
    r = 27 + i; v.merge_cells(f'B{r}:H{r}'); cell(v, f'B{r}', t, 10.5, wrap=True); v.row_dimensions[r].height = 30
sb = BarChart(); sb.type = 'bar'; style_chart(sb, 'Կշիռներ և շահութաբերություն · 2024 vs 2025', 17, 8)
sb.add_data(Reference(d, min_col=3, max_col=4, min_row=78, max_row=82), titles_from_data=True); sb.set_categories(Reference(d, min_col=2, min_row=79, max_row=82))
colorize(sb.series[0], '9C8F7A'); colorize(sb.series[1], REDc); labels(sb, '0.00%'); sb.x_axis.delete = False; sb.y_axis.delete = False; sb.y_axis.numFmt = '0%'; sb.y_axis.majorGridlines = None; sb.gapWidth = 50
v.add_chart(sb, 'J6')
w2 = BarChart(); w2.type = 'col'; w2.grouping = 'stacked'; w2.overlap = 100; style_chart(w2, 'Քարե աստիճաններ՝ ՇԲԹֆպ, պ.կ.', 17, 8)
w2.add_data(Reference(d, min_col=3, max_col=6, min_row=72, max_row=76), titles_from_data=True); w2.set_categories(Reference(d, min_col=2, min_row=73, max_row=76))
w2.series[0].graphicalProperties.noFill = True; w2.series[0].graphicalProperties.line.noFill = True
colorize(w2.series[1], INDc); colorize(w2.series[2], GOLDc); colorize(w2.series[3], REDc); w2.gapWidth = 40; w2.y_axis.majorGridlines = None; w2.y_axis.delete = False; w2.x_axis.delete = False
for s_ in w2.series[1:]:
    s_.dLbls = DataLabelList(); s_.dLbls.showVal = True; s_.dLbls.showSerName = False; s_.dLbls.showCatName = False; s_.dLbls.showLegendKey = False; s_.dLbls.numFmt = '0.00;-0.00;;'
v.add_chart(w2, 'J23')
v.freeze_panes = 'A5'

# ---------------- 4) TASK 2 ----------------
t = wb.create_sheet('Տնային 2 ✦', 3); t.sheet_properties.tabColor = IND3c
paper(t, 16, 70, {'A': 2, 'B': 40, **{c: 13 for c in 'CDEFGH'}, 'I': 3, **{c: 13 for c in 'JKLMN'}})
banner(t, 'Գ · Տնային 2 · խնդիրներ 11.1.3 – 11.1.5', 'Կազմ, կառուցվածք և շրջանառելիություն · տվյալները՝ «Ձևանմուշ · Տնային 2» թերթից', 'N'); nav(t, 4, 'Տնային 2 ✦')
section(t, 'B6', 'H6', '◆ 11.1.4 · շրջանառելիություն')
hdr(t, 7, 2, ['Ցուցանիշ', 'Միավոր', 't0', 't1', 'Շեղում', 'Գնահատական'])
for blk, (r0, rows_) in enumerate(((8, [(5, 'Մարված ընթացիկ ՖՊ', 'հազ.դր.', NUM), (7, 'ԸՖՊ միջին արժեք', 'հազ.դր.', NUM), (8, 'Շրջանառելիություն', 'պտույտ', '0.0000'), (9, 'Շրջանառելիություն', 'օր', '0.0')]),
                                    (16, [(16, 'Մարված ընթացիկ ՖՊ', 'հազ.դր.', NUM), (17, 'ԸՖՊ միջին արժեք', 'հազ.դր.', NUM), (18, 'Շրջանառելիություն', 'պտույտ', '0.0000'), (19, 'Շրջանառելիություն', 'օր', '0.0')]))):
    if blk == 1:
        section(t, 'B14', 'H14', '◆ 11.1.5 · շրջանառելիություն'); hdr(t, 15, 2, ['Ցուցանիշ', 'Միավոր', 't0', 't1', 'Շեղում', 'Գնահատական'])
    for i, (rr, nm, un, fm) in enumerate(rows_):
        r = r0 + i; t[f'B{r}'] = nm; t[f'C{r}'] = un; t[f'D{r}'] = f'={S2}!D{rr}'; t[f'E{r}'] = f'={S2}!E{rr}'; t[f'F{r}'] = f'=E{r}-D{r}'
        if un == 'պտույտ': t[f'G{r}'] = f'=IF(F{r}<0,"▼ դանդաղել է","▲ արագացել է")'
        elif un == 'օր': t[f'G{r}'] = f'=IF(F{r}>0,"▼ երկարել է","▲ կարճացել է")'
        rowfmt(t, r, 2, 6, i % 2, [None, None, fm, fm, dfmt.get(fm, '+#,##0;-#,##0'), None]); t[f'C{r}'].alignment = Alignment(horizontal='center'); t[f'G{r}'].alignment = Alignment(horizontal='center')
t.conditional_formatting.add('G8:G19', FormulaRule(formula=['LEFT(G8,1)="▲"'], fill=fill('D6EFD9'), font=Font(name=F, bold=True, color=GRN)))
t.conditional_formatting.add('G8:G19', FormulaRule(formula=['LEFT(G8,1)="▼"'], fill=fill('F8D3D3'), font=Font(name=F, bold=True, color=REDc)))
section(t, 'B22', 'H22', '◆ 11.1.3 · կազմ և կառուցվածք')
hdr(t, 23, 2, ['Ցուցանիշ', 't0, հազ.դր.', 't0, %', 't1, հազ.դր.', 't1, %', 'Շեղում', 'Շեղում, պ.կ.'])
names = [(26, 'Ոչ ընթացիկ ֆինանսական պարտավորություններ', True), (27, '   երկարաժամկետ բանկային վարկեր', False), (29, '   երկարաժամկետ փոխառություններ', False),
         (31, 'Ընթացիկ ֆինանսական պարտավորություններ', True), (32, '   կարճաժամկետ բանկային վարկեր', False), (34, '   կարճաժամկետ փոխառություններ', False), (37, 'Ընդամենը', True)]
for i, (rr, nm, bo) in enumerate(names):
    r = 24 + i; t[f'B{r}'] = nm; t[f'C{r}'] = f'={S2}!C{rr}'; t[f'D{r}'] = f'={S2}!D{rr}'; t[f'E{r}'] = f'={S2}!E{rr}'; t[f'F{r}'] = f'={S2}!F{rr}'; t[f'G{r}'] = f'={S2}!G{rr}'; t[f'H{r}'] = f'={S2}!H{rr}*100'
    rowfmt(t, r, 2, 7, i % 2, [None, NUM, '0.00%', NUM, '0.00%', '+#,##0;-#,##0;"–"', '+0.00;-0.00;"–"'])
    if bo:
        for col in 'BCDEFGH': t[f'{col}{r}'].font = Font(name=F, sz=11, bold=True, color='FFFFFF' if rr == 37 else INKc)
        if rr == 37:
            for col in 'BCDEFGH': t[f'{col}{r}'].fill = fill(INDc)
t.conditional_formatting.add('D25:D26', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color=IND3c, showValue=True))
t.conditional_formatting.add('F25:F26', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color=IND3c, showValue=True))
t.conditional_formatting.add('D28:D29', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color='E8A0A8', showValue=True))
t.conditional_formatting.add('F28:F29', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color='E8A0A8', showValue=True))
t.conditional_formatting.add('G24:G30', IconSetRule('3Arrows', 'num', [-1e-9, 0, 1e-9]))
cell(t, 'B32', 'Ստուգում՝ t1-ում ընթացիկ ՖՊ − (կարճ. վարկ + կարճ. փոխ.)', 10, True); cell(t, 'E32', f'={S2}!E38', 10, True, REDc, fmt=NUM)
t.merge_cells('B33:H34'); cell(t, 'B33', 'Ծանոթ․ t1-ում ընթացիկ ՖՊ-ն տրված է 52 200, իսկ բաղադրիչների գումարը 50 200 է։ Հոդվածը պահպանված է ինչպես տրված է, կշիռները հաշվարկված են 227 600 ընդհանուր գումարի նկատմամբ։', 9.5, italic=True, color='9C2A00', wrap=True)
# chart data for task2
hdr(t, 37, 2, ['Կառուցվածք', 't0', 't1'])
for i, (nm, rr) in enumerate((('Երկ. բանկային վարկեր', 27), ('Երկ. փոխառություններ', 29), ('Կարճ. բանկային վարկեր', 32), ('Կարճ. փոխառություններ', 34))):
    r = 38 + i; t[f'B{r}'] = nm; t[f'C{r}'] = f'={S2}!C{rr}'; t[f'D{r}'] = f'={S2}!E{rr}'; rowfmt(t, r, 2, 3, i % 2, [None, NUM, NUM])
hdr(t, 43, 2, ['Պտույտ, օր', 't0', 't1'])
t['B44'] = '11.1.4'; t['C44'] = '=D11'; t['D44'] = '=E11'; t['B45'] = '11.1.5'; t['C45'] = '=D19'; t['D45'] = '=E19'
rowfmt(t, 44, 2, 3, 0, [None, '0.0', '0.0']); rowfmt(t, 45, 2, 3, 1, [None, '0.0', '0.0'])
sc = BarChart(); sc.type = 'bar'; sc.grouping = 'percentStacked'; sc.overlap = 100; style_chart(sc, '11.1.3 · կառուցվածք (100%)', 17, 7.5)
sc.add_data(Reference(t, min_col=2, max_col=4, min_row=38, max_row=41), from_rows=True, titles_from_data=True); sc.set_categories(Reference(t, min_col=3, max_col=4, min_row=37, max_row=37))
for s_, col in zip(sc.series, (INDc, IND3c, REDc, GOLDc)): colorize(s_, col)
sc.dataLabels = DataLabelList(); sc.dataLabels.showPercent = False; sc.dataLabels.showVal = True; sc.dataLabels.showSerName = False; sc.dataLabels.showCatName = False; sc.dataLabels.showLegendKey = False; sc.dataLabels.numFmt = '#,##0'
sc.gapWidth = 40; sc.y_axis.delete = False; sc.x_axis.delete = False; sc.y_axis.majorGridlines = None
t.add_chart(sc, 'J6')
tc = BarChart(); tc.type = 'col'; style_chart(tc, 'Պտույտի տևողություն, օր', 17, 7.5)
tc.add_data(Reference(t, min_col=3, max_col=4, min_row=43, max_row=45), titles_from_data=True); tc.set_categories(Reference(t, min_col=2, min_row=44, max_row=45))
colorize(tc.series[0], '9C8F7A'); colorize(tc.series[1], REDc); labels(tc, '0.0'); tc.gapWidth = 60; tc.y_axis.majorGridlines = None; tc.y_axis.delete = False; tc.x_axis.delete = False
t.add_chart(tc, 'J22')
t.freeze_panes = 'A5'

# ---------------- 5) CONCLUSIONS ----------------
c = wb.create_sheet('Եզրակացություն', 4); c.sheet_properties.tabColor = GRN
paper(c, 16, 60, {'A': 2, 'B': 6, 'C': 110, 'D': 3, 'E': 14, 'F': 14, 'G': 14})
banner(c, 'Դ · Եզրակացություն և հաշվարկի ծանոթագրություններ', 'Մանրամասն վերլուծությունը՝ նախորդ թերթերում', 'G'); nav(c, 4, 'Եզրակացություն')
section(c, 'B6', 'C6', '◆ Տնային 1')
row = 7
for i, tx in enumerate(CONC[1:]):
    cell(c, f'B{row}', '①②③④⑤⑥⑦'[i], 14, True, REDc, h='center', v_='top'); cell(c, f'C{row}', tx.split('. ', 1)[1] if tx[:2].rstrip('.').isdigit() else tx, 11, wrap=True, v_='top')
    c.row_dimensions[row].height = 48; c[f'C{row}'].fill = fill('FBF6EA' if i % 2 else 'F1E6CC'); row += 1
row += 1; section(c, f'B{row}', f'C{row}', '◆ Տնային 2'); row += 1
for i, tx in enumerate(CONC2[1:]):
    cell(c, f'B{row}', '①②③'[i], 14, True, REDc, h='center', v_='top'); cell(c, f'C{row}', tx, 11, wrap=True, v_='top')
    c.row_dimensions[row].height = 52; c[f'C{row}'].fill = fill('FBF6EA' if i % 2 else 'F1E6CC'); row += 1
row += 1; section(c, f'B{row}', f'C{row}', '◆ Կինցուգի․ ինչպես են մշակվել տվյալները', GOLDc); row += 1
NOTES = ['Ոչ ընթացիկից ընթացիկ տեղափոխված մասը (տարեկան 22 000) մարում չէ․ այն երկրորդ անգամ հայտնվում է ընթացիկ ձևավորվածների մեջ։ Հիմնական հաշվարկում վերցված է փաստացի մարումը, իսկ ձևանմուշի ուղիղ գումարով տարբերակը ցույց է տրված «Շարժ» թերթում (604 → 643 օր)։',
         'Բանկային վարկերը որոշված են ըստ տողի անվանման («բանկային վարկ»), քանի որ մի քանի տողում նշանը (ԸՖՊ) և անվանումը չեն համընկնում։ Ստուգում՝ 2024-ի տարեվերջի մնացորդները լրիվ համընկնում են 2025-ի տարեսկզբի տողերի հետ։',
         '11.1.4․ սյունակները՝ t0 և t1, օրերը՝ 360-օրյա տարով (դասախոսության բանաձևով)։',
         '11.1.3․ 12 500-ը տեղադրված է իր տողում, «Ընդամենը»-ն = ոչ ընթացիկ + ընթացիկ (197 600 և 227 600)։ t1-ի ընթացիկ ՖՊ-ի և բաղադրիչների 2 000 տարբերությունը ցույց է տրված առանձին։']
for i, tx in enumerate(NOTES):
    cell(c, f'B{row}', '✦', 14, True, GOLDc, h='center', v_='top'); cell(c, f'C{row}', tx, 10.5, wrap=True, v_='top'); c.row_dimensions[row].height = 46
    c[f'C{row}'].border = Border(left=Side(style='thick', color=GOLDc)); row += 1
if BOWL and os.path.exists(BOWL):
    im2 = XLImage(BOWL); im2.width, im2.height = 300, 240; c.add_image(im2, 'E7')
c.freeze_panes = 'A5'

for ws in wb.worksheets:
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.active = 0
for ws in wb.worksheets: ws.sheet_view.tabSelected = (ws.title == 'Վահանակ')
wb.save(OUT); print('saved', OUT)
