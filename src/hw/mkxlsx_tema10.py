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
GRN = PatternFill('solid', fgColor='E2F5E9'); HDR = PatternFill('solid', fgColor='0F5132'); YEL = PatternFill('solid', fgColor='FFF4CC')
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

# ---------------- Charts sheet ----------------
ch = wb.create_sheet('Գծապատկերներ')
ch['B2'].value = 'Գծապատկերներ (տվյալները՝ բանաձևերով կապված Տնային 1 և Տնային 2 թերթերին)'; ch['B2'].font = Font(name=F, sz=13, bold=True, color='0F5132')
T = [('', '2024թ.', '2025թ.'), ('Ոչ ընթացիկ ՖՊ', "='Տնային 1'!E66", "='Տնային 1'!F66"), ('Ընթացիկ ՖՊ', "='Տնային 1'!E67", "='Տնային 1'!F67"),
     ('Բանկային վարկեր', "='Տնային 1'!E88", "='Տնային 1'!F88"), ('Միջին ՖՊ', "='Տնային 1'!E68", "='Տնային 1'!F68"), ('Մարված ՖՊ', "='Տնային 1'!E84", "='Տնային 1'!F84")]
for i, row in enumerate(T):
    for j, v in enumerate(row):
        c = ch.cell(4 + i, 2 + j, v); c.font = Font(name=F, sz=11, bold=(i == 0 or j == 0)); c.number_format = NUM; c.border = BOX
R = [('', '2024թ.', '2025թ.'), ('ՏԿՖՊ', "='Տնային 1'!E71", "='Տնային 1'!F71"), ('ՏԿժ.անց', "='Տնային 1'!E72", "='Տնային 1'!F72"),
     ('ՏԿԲՎ', "='Տնային 1'!E73", "='Տնային 1'!F73"), ('ՇԲԹՖՊ', "='Տնային 1'!E74", "='Տնային 1'!F74")]
for i, row in enumerate(R):
    for j, v in enumerate(row):
        c = ch.cell(12 + i, 2 + j, v); c.font = Font(name=F, sz=11, bold=(i == 0 or j == 0)); c.number_format = PCT; c.border = BOX
S = [('', 't0', 't1'), ('Երկ. բանկային վարկեր', "='Տնային 2'!C27", "='Տնային 2'!E27"), ('Երկ. փոխառություններ', "='Տնային 2'!C29", "='Տնային 2'!E29"),
     ('Կարճ. բանկային վարկեր', "='Տնային 2'!C32", "='Տնային 2'!E32"), ('Կարճ. փոխառություններ', "='Տնային 2'!C34", "='Տնային 2'!E34")]
for i, row in enumerate(S):
    for j, v in enumerate(row):
        c = ch.cell(19 + i, 2 + j, v); c.font = Font(name=F, sz=11, bold=(i == 0 or j == 0)); c.number_format = NUM; c.border = BOX
ch.column_dimensions['B'].width = 26; ch.column_dimensions['C'].width = 13; ch.column_dimensions['D'].width = 13

def bar(title, mr, Mr, ytitle, anchor, pct=False, stacked=False):
    c = BarChart(); c.type = 'col'; c.title = title; c.y_axis.title = ytitle; c.height = 8; c.width = 15
    c.add_data(Reference(ch, min_col=3, max_col=4, min_row=mr, max_row=Mr), titles_from_data=True)
    c.set_categories(Reference(ch, min_col=2, min_row=mr + 1, max_row=Mr))
    if stacked: c.grouping = 'stacked'; c.overlap = 100
    c.dataLabels = DataLabelList(); c.dataLabels.showVal = True; c.dataLabels.showSerName = False; c.dataLabels.showCatName = False; c.dataLabels.showLegendKey = False
    if pct: c.y_axis.number_format = '0%'
    c.y_axis.delete = False; c.x_axis.delete = False
    ch.add_chart(c, anchor)
bar('Ֆինանսական պարտավորություններ, հազ. դր.', 4, 9, 'հազ. դր.', 'F4')
bar('Կշիռներ և շահութաբերություն', 12, 16, '%', 'F21', pct=True)
bar('Աղ. 13.1 · կառուցվածք (t0 / t1)', 19, 23, 'հազ. դր.', 'F38')
p = PieChart(); p.title = 'ՖՊ կառուցվածք 2025'; p.height = 8; p.width = 11
p.add_data(Reference(ch, min_col=4, min_row=5, max_row=6)); p.set_categories(Reference(ch, min_col=2, min_row=5, max_row=6))
p.dataLabels = DataLabelList(); p.dataLabels.showPercent = True; p.dataLabels.showVal = False; p.dataLabels.showSerName = False; p.dataLabels.showCatName = False; p.dataLabels.showLegendKey = False; ch.add_chart(p, 'B26')

for ws in wb.worksheets:
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.active = 0
wb.save(OUT); print('saved', OUT)
