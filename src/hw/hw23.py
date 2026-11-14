# -*- coding: utf-8 -*-
# Homework 1 (liquidity, lesson 2) + Homework 2 (financial stability, lesson 3). "Paper report" look: ink blue / sand.
import sys, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule, DataBarRule
from openpyxl.chart import BarChart, DoughnutChart, Reference
from openpyxl.chart.label import DataLabelList
OUT, AUTHOR = sys.argv[1], sys.argv[2]
INK, SAND, PAPER, RUST, SAGE = "1F3A5F", "E9DFC9", "FBF7EE", "B5452B", "4E7D5B"
thin = Side(style="thin", color="C9BFA8"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
F = lambda **k: Font(name="Georgia", **k)
def head(ws, r, vals, c0=1):
    for j, v in enumerate(vals):
        c = ws.cell(r, c0 + j, v); c.fill = PatternFill("solid", fgColor=INK); c.font = F(bold=True, color="FFFFFF", size=10)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BOX
    ws.row_dimensions[r].height = 30
def row(ws, r, vals, c0=1, fmt=None, bold=False, fill=None):
    for j, v in enumerate(vals):
        c = ws.cell(r, c0 + j, v); c.border = BOX; c.font = F(size=10, bold=bold); c.alignment = Alignment(vertical="center", wrap_text=True)
        c.fill = PatternFill("solid", fgColor=fill or (PAPER if r % 2 else "FFFFFF"))
        if fmt and j >= 1 and not isinstance(v, str) or (fmt and isinstance(v, str) and v.startswith("=")): c.number_format = fmt
def title(ws, txt, sub, width=7):
    ws.sheet_view.showGridLines = False
    ws["A1"] = txt; ws["A1"].font = F(size=16, bold=True, color=INK); ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    ws["A2"] = sub; ws["A2"].font = F(size=10, italic=True, color="7A6A4F"); ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width)
    for c in range(1, width + 1): ws.cell(3, c).fill = PatternFill("solid", fgColor=RUST)
    ws.row_dimensions[3].height = 4
def note(ws, r, txt, width=7, h=90):
    ws.cell(r, 1, txt); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=width)
    c = ws.cell(r, 1); c.alignment = Alignment(wrap_text=True, vertical="top"); c.font = F(size=10, color="3B3326"); c.fill = PatternFill("solid", fgColor=SAND)
    ws.row_dimensions[r].height = h

wb = openpyxl.Workbook()
# ---------- Sheet 1: data / balance ----------
ws = wb.active; ws.title = "Հաշվեկշիռ"
for col, w in zip("ABCDEF", [6, 40, 16, 6, 40, 16]): ws.column_dimensions[col].width = w
title(ws, "<<XXX>> ՍՊԸ · Հաշվեկշիռ 2025թ. (հազ. դրամ)", f"Տնային առաջադրանք 1–2 · Կատարեց՝ {AUTHOR} · ԻՏ-447 · Դասախոս՝ Օ.Ա. Գալստյան", 6)
head(ws, 5, ["№", "ԱԿՏԻՎ", "2025թ.", "№", "ՊԱՍԻՎ", "2025թ."])
A = [("1", "Ոչ ընթացիկ ակտիվներ", 100000), ("2", "Ընթացիկ ակտիվներ", "=SUM(C8:C11)"), ("2.1", "Պաշարներ", 71500), ("2.2", "Դեբիտորական պարտքեր", 60500), ("2.3", "Ընթացիկ ֆինանսական ներդրումներ", 8000), ("2.4", "Դրամական միջոցներ", 20000), ("", "", None)]
P = [("3", "Սեփական կապիտալ", 140000), ("4", "Ոչ ընթացիկ պարտավորություններ", 35790), ("5", "Ընթացիկ պարտավորություններ", "=SUM(F10:F11)"), ("", "այդ թվում՝", None), ("5.1", "Կրեդիտորական պարտքեր", 60800), ("5.2", "Կարճաժամկետ բանկային վարկ", 23410), ("", "", None)]
for i in range(7):
    r = 6 + i; row(ws, r, list(A[i]) + list(P[i]), fmt="#,##0")
    for c in (3, 6):
        v = ws.cell(r, c).value
        if isinstance(v, int): ws.cell(r, c).font = F(size=10, color="1F4FBF")  # inputs blue
row(ws, 13, ["", "ՀԱՇՎԵԿՇԻՌ", "=C6+C7", "", "ՀԱՇՎԵԿՇԻՌ", "=F6+F7+F8"], fmt="#,##0", bold=True, fill=SAND)
ws["B14"] = "Ստուգում (ակտիվ − պասիվ = 0)"; ws["C14"] = "=C13-F13"; ws["B14"].font = F(size=9, italic=True); ws["C14"].number_format = "#,##0"
ws["B15"] = "Կապույտ թվերը դասախոսի տվյալներն են, մնացածը՝ բանաձևեր։ «X» նշված տողերը հաշվարկված են բանաձևով։"; ws["B15"].font = F(size=9, italic=True, color="7A6A4F")
ws.freeze_panes = "A6"
B = "'Հաշվեկշիռ'!"

# ---------- Sheet 2: liquidity ----------
ws = wb.create_sheet("Իրացվելիություն")
for col, w in zip("ABCDEFGH", [6, 34, 15, 6, 34, 15, 15, 22]): ws.column_dimensions[col].width = w
title(ws, "Առաջադրանք 1 · Հաշվեկշռի իրացվելիություն և վճարունակություն", "Ակտիվները խմբավորում ենք ըստ իրացման արագության, պասիվները՝ ըստ մարման ժամկետի", 8)
head(ws, 5, ["Խումբ", "Ակտիվներ", "Գումար", "Խումբ", "Պասիվներ", "Գումար", "Ավելցուկ (+) / պակաս (−)", "Պայման"])
G = [("Ա1", "Առավել իրացվելի (ԴՄ + ԿՖՆ)", f"={B}C11+{B}C10", "Պ1", "Հրատապ (կրեդիտորական պարտքեր)", f"={B}F10", ">="),
     ("Ա2", "Արագ իրացվելի (դեբիտորական պարտքեր)", f"={B}C9", "Պ2", "Կարճաժամկետ (բանկային վարկ)", f"={B}F11", ">="),
     ("Ա3", "Դանդաղ իրացվելի (պաշարներ)", f"={B}C8", "Պ3", "Երկարաժամկետ (ոչ ընթացիկ պարտ.)", f"={B}F7", ">="),
     ("Ա4", "Դժվար իրացվելի (ոչ ընթացիկ ակտիվներ)", f"={B}C6", "Պ4", "Մշտական (սեփական կապիտալ)", f"={B}F6", "<=")]
for i, (a, an, av, p, pn, pv, op) in enumerate(G):
    r = 6 + i
    row(ws, r, [a, an, av, p, pn, pv, f"=C{r}-F{r}", f'=IF(C{r}{op}F{r},"✔ Ա{i+1} {"≥" if op==">=" else "≤"} Պ{i+1}","✖ խախտված")'], fmt="#,##0")
row(ws, 10, ["", "Ընդամենը", "=SUM(C6:C9)", "", "Ընդամենը", "=SUM(F6:F9)", "=C10-F10", ""], fmt="#,##0", bold=True, fill=SAND)
ws["B11"] = "Հաշվեկշիռը բացարձակ իրացվելի է, եթե կատարվում են բոլոր չորս պայմանները։"; ws["B11"].font = F(size=9, italic=True)
ws["H12"] = '=IF(COUNTIF(H6:H9,"✔*")=4,"✔ Բացարձակ իրացվելի","✖ Բացարձակ իրացվելի չէ")'; ws["G12"] = "Եզրակացություն՝"; ws["H12"].font = F(bold=True, color=RUST); ws["G12"].font = F(bold=True)
head(ws, 14, ["№", "Ցուցանիշ", "Բանաձև", "", "Մեկնաբանություն", "Արժեք", "Նորմա", "Գնահատական"])
K = [("1", "Ընթացիկ իրացվելիություն (ԸԻ)", "(Ա1+Ա2) − (Պ1+Պ2)", "Մոտ ապագայում վճարունակության պաշարը", "=(C6+C7)-(F6+F7)", "> 0", '=IF(F15>0,"✔ Վճարունակ","✖ Պակասուրդ")', "#,##0"),
     ("2", "Հեռանկարային իրացվելիություն (ՀԻ)", "Ա3 − Պ3", "Ապագա մուտքերի և վճարումների հաշվեկշիռ", "=C8-F8", "> 0", '=IF(F16>0,"✔ Դրական","✖ Բացասական")', "#,##0"),
     ("3", "Բացարձակ իրացվելիության գործակից", "(ԴՄ+ԿՖՆ) ÷ ԸՊ", "Որքան պարտք կփակենք հենց հիմա", f"=C6/{B}F8", "0.2 – 0.5", '=IF(AND(F17>=0.2,F17<=0.5),"✔ Նորմայում",IF(F17<0.2,"✖ Ցածր","▲ Բարձր"))', "0.000"),
     ("4", "Արագ իրացվելիության գործակից", "(ԴՄ+ԿՖՆ+ԴՊ) ÷ ԸՊ", "Նույնը, եթե դեբիտորներն էլ վճարեն", f"=(C6+C7)/{B}F8", "0.7 – 1.0", '=IF(F18>=0.7,IF(F18<=1,"✔ Նորմայում","▲ Նորմայից բարձր"),"✖ Ցածր")', "0.000"),
     ("5", "Ընթացիկ իրացվելիության գործակից", "ԸԱ ÷ ԸՊ", "Բոլոր ընթացիկ ակտիվները՝ պարտքերի համեմատ", f"={B}C7/{B}F8", "1 – 2", '=IF(AND(F19>=1,F19<=2),"✔ Նորմայում",IF(F19<1,"✖ Ցածր","▲ Բարձր"))', "0.000")]
for i, (n, nm, fx, cm, v, nr, ev, fm) in enumerate(K):
    r = 15 + i; row(ws, r, [n, nm, fx, "", cm, v, nr, ev]); ws.cell(r, 6).number_format = fm; ws.cell(r, 6).font = F(size=11, bold=True, color=INK)
    ws.row_dimensions[r].height = 30
for rr in range(6, 20):
    ws.conditional_formatting.add(f"H{rr}", FormulaRule(formula=[f'LEFT(H{rr},1)="✔"'], font=Font(color=SAGE, bold=True)))
    ws.conditional_formatting.add(f"H{rr}", FormulaRule(formula=[f'LEFT(H{rr},1)="✖"'], font=Font(color=RUST, bold=True)))
# scenario Q9
head(ws, 22, ["№", "Հարց 9 · Գործարք՝ պաշարների ձեռքբերում 30 000", "Մինչև", "", "Փոփոխություն", "Հետո", "Նորմա", "Ազդեցություն"])
ws["C21"] = "Գործարքի մուտքային տվյալներ՝"; ws["E21"] = "Վճարում դրամով"; ws["F21"] = 15000; ws["G21"] = "Կրեդիտորական պարտք"; ws["H21"] = 15000
for c in ("C21", "E21", "G21"): ws[c].font = F(size=9, italic=True)
for c in ("F21", "H21"): ws[c].font = F(size=10, color="1F4FBF", bold=True); ws[c].number_format = "#,##0"
S = [("Դրամական միջոցներ", f"={B}C11", "=-F21"), ("Պաշարներ", f"={B}C8", "=F21+H21"), ("Կրեդիտորական պարտքեր", f"={B}F10", "=H21"),
     ("Ընթացիկ ակտիվներ", f"={B}C7", "=E24+E23"), ("Ընթացիկ պարտավորություններ", f"={B}F8", "=E25")]
for i, (nm, b0, d) in enumerate(S):
    r = 23 + i; row(ws, r, [i + 1, nm, b0, "", d, f"=C{r}+E{r}", "", ""], fmt="#,##0")
SK = [("Բացարձակ իրացվելիություն", f"=(C23+{B}C10)/C27", f"=(F23+{B}C10)/F27", "0.2–0.5"),
      ("Արագ իրացվելիություն", f"=(C23+{B}C10+{B}C9)/C27", f"=(F23+{B}C10+{B}C9)/F27", "0.7–1.0"),
      ("Ընթացիկ իրացվելիություն", "=C26/C27", "=F26/F27", "1–2")]
for i, (nm, b0, a1, nr) in enumerate(SK):
    r = 28 + i; row(ws, r, [f"Գ{i+1}", nm, b0, "", f"=F{r}-C{r}", a1, nr, f'=IF(F{r}<C{r},"▼ վատթարանում է","▲ բարելավվում է")'])
    for c in (3, 5, 6): ws.cell(r, c).number_format = "0.000"
ws.conditional_formatting.add("H28:H30", FormulaRule(formula=['LEFT(H28,1)="▼"'], font=Font(color=RUST, bold=True)))
note(ws, 32, "Եզրակացություն (առաջադրանք 1). Հաշվեկշիռը բացարձակ իրացվելի չէ, որովհետև առավել իրացվելի ակտիվները (28 000) չեն ծածկում հրատապ պարտավորությունները (60 800)՝ պակասը 32 800 է։ "
     "Մյուս երեք պայմանները կատարվում են։ Ընթացիկ իրացվելիությունը դրական է (+4 290), հեռանկարայինը՝ +35 710, ուստի ընկերությունը մոտ ապագայում վճարունակ է։ "
     "Բոլոր երեք գործակիցները նորմայի սահմաններում են կամ բարձր (0.333, 1.051, 1.900)։\n"
     "Հարց 9. 30 000-ի պաշարներ գնելով (15 000 դրամով, 15 000 պարտքով) դրամական միջոցները կնվազեն մինչև 5 000, իսկ կրեդիտորական պարտքը կաճի մինչև 75 800։ "
     "Բացարձակ իրացվելիությունը կիջնի 0.333 → 0.131 (նորմայից ցածր), արագը՝ 1.051 → 0.741, ընթացիկը՝ 1.900 → 1.764։ Խնդիր կառաջանա հրատապ վճարումների հարցում․ "
     "ընկերությունը կունենա ավելի շատ «սառեցված» պաշար և ավելի քիչ ազատ փող։", 8, 130)

# ---------- Sheet 3: stability ----------
ws = wb.create_sheet("Կայունություն")
for col, w in zip("ABCDEFG", [6, 40, 26, 15, 14, 24, 6]): ws.column_dimensions[col].width = w
title(ws, "Առաջադրանք 2 · Ֆինանսական կայունություն", "Որքանով է ընկերությունը կանգնած սեփական ոտքերի վրա", 6)
head(ws, 5, ["№", "Ցուցանիշ", "Բանաձև", "Արժեք", "Նորմա", "Գնահատական"])
T = [("1", "Սեփական ընթացիկ ակտիվներ (ՍԸԱ)", "ՍԿ + ՈԸՊ − ՈԸԱ", f"={B}F6+{B}F7-{B}C6", "> 0", '=IF(D6>0,"✔ Դրական","✖ Բացասական")', "#,##0"),
     ("2", "Ընթացիկ ակտիվների ապահովվածություն ՍԸԱ-ով", "ՍԸԱ ÷ ԸԱ", f"=D6/{B}C7", "≥ 0.1", '=IF(D7>=0.1,"✔ Ապահովված","✖ Անբավարար")', "0.000"),
     ("3", "Պաշարների ապահովվածություն ՍԸԱ-ով", "ՍԸԱ ÷ Պաշարներ", f"=D6/{B}C8", "0.6 – 0.8", '=IF(D8>=0.6,"✔ Ապահովված","✖ Անբավարար")', "0.000"),
     ("4", "Ֆինանսական անկախության գործակից", "ՍԿ ÷ Ակտիվներ", f"={B}F6/{B}C13", "≥ 0.5", '=IF(D9>=0.5,"✔ Անկախ","✖ Կախյալ")', "0.000"),
     ("5", "Ֆինանսական կախվածության գործակից", "ՓԿ ÷ Ակտիվներ", f"=({B}F7+{B}F8)/{B}C13", "≤ 0.5", '=IF(D10<=0.5,"✔ Նորմայում","✖ Բարձր")', "0.000"),
     ("6", "Ֆինանսական ռիսկի գործակից", "ՓԿ ÷ ՍԿ", f"=({B}F7+{B}F8)/{B}F6", "≤ 1", '=IF(D11<=1,"✔ Ցածր ռիսկ","✖ Բարձր ռիսկ")', "0.000"),
     ("7", "Ֆինանսական կայունության պաշար", "ՍԸԱ − Պաշարներ", f"=D6-{B}C8", "> 0", '=IF(D12>0,"✔ Պաշար կա","✖ Պակասուրդ")', "#,##0"),
     ("8", "Պաշարի մեծությունը պաշարների նկատմամբ, %", "Պաշար ÷ Պաշարներ × 100", f"=D12/{B}C8*100", "> 0", '=IF(D13>0,"✔","✖")', "0.0"),
     ("9", "Ֆինանսական կայունության գործակից", "(ՍԿ + ՈԸՊ) ÷ Ակտիվներ", f"=({B}F6+{B}F7)/{B}C13", "≥ 0.6", '=IF(D14>=0.6,"✔ Կայուն","✖ Անկայուն")', "0.000")]
for i, (n, nm, fx, v, nr, ev, fm) in enumerate(T):
    r = 6 + i; row(ws, r, [n, nm, fx, v, nr, ev]); ws.cell(r, 4).number_format = fm; ws.cell(r, 4).font = F(size=11, bold=True, color=INK); ws.row_dimensions[r].height = 26
ws.conditional_formatting.add("F6:F14", FormulaRule(formula=['LEFT(F6,1)="✔"'], font=Font(color=SAGE, bold=True)))
ws.conditional_formatting.add("F6:F14", FormulaRule(formula=['LEFT(F6,1)="✖"'], font=Font(color=RUST, bold=True)))
ws["B16"] = "Կայունության տեսակը՝"; ws["B16"].font = F(bold=True)
ws["C16"] = f'=IF(D6>={B}C8,"Բացարձակ կայունություն",IF(D6+{B}F11>={B}C8,"Նորմալ կայունություն",IF(D6+{B}F11+{B}F10>={B}C8,"Անկայուն վիճակ","Ճգնաժամային վիճակ")))'
ws["C16"].font = F(bold=True, color=SAGE, size=12); ws.merge_cells("C16:F16")
# scenarios
head(ws, 18, ["№", "Սցենար (առաջադրանք 2, հարց 7)", "Ինչ ենք անում", "Գկայ հետո", "Գֆռ հետո", "Արդյունք"])
SC = [("Ա", "Շահույթը վերաներդնել կապիտալում (+20 000 ՍԿ, +20 000 ԴՄ)", "Սեփական կապիտալ ↑", f"=({B}F6+20000+{B}F7)/({B}C13+20000)", f"=({B}F7+{B}F8)/({B}F6+20000)"),
      ("Բ", "Կարճաժամկետ վարկը փոխարինել երկարաժամկետով (23 410)", "Վարկի վերաֆինանսավորում", f"=({B}F6+{B}F7+{B}F11)/{B}C13", f"=({B}F7+{B}F8)/{B}F6"),
      ("Գ", "Նոր սարքավորում 40 000՝ կարճաժամկետ վարկով", "Ռիսկային քայլ", f"=({B}F6+{B}F7)/({B}C13+40000)", f"=({B}F7+{B}F8+40000)/{B}F6")]
for i, (n, a, b, c, d) in enumerate(SC):
    r = 19 + i; row(ws, r, [n, a, b, c, d, f'=IF(AND(D{r}>=D14,E{r}<=D11),"✔ Կամրապնդի կայունությունը","✖ Կթուլացնի կայունությունը")'])
    ws.cell(r, 4).number_format = "0.000"; ws.cell(r, 5).number_format = "0.000"; ws.row_dimensions[r].height = 34
ws.conditional_formatting.add("F19:F21", FormulaRule(formula=['LEFT(F19,1)="✔"'], font=Font(color=SAGE, bold=True)))
ws.conditional_formatting.add("F19:F21", FormulaRule(formula=['LEFT(F19,1)="✖"'], font=Font(color=RUST, bold=True)))
note(ws, 23, "Եզրակացություն (առաջադրանք 2). Սեփական ընթացիկ ակտիվները 75 790 են, դրանք ծածկում են ընթացիկ ակտիվների 47.4%-ը և ամբողջ պաշարները (1.060)։ "
     "Ընկերությունն ունի բացարձակ ֆինանսական կայունություն՝ 4 290 հազ. դրամի «անվտանգության պաշարով» (պաշարների 6%-ը)։ Անկախության գործակիցը 0.538 է (≥0.5), "
     "կախվածությունը՝ 0.462, ֆինանսական ռիսկը՝ 0.857 (≤1). ընկերությունը ավելի շատ օգտվում է սեփական, քան փոխառու միջոցներից։ Կայունության գործակիցը 0.676 է։\n"
     "Սցենարներ․ Ա-ն և Բ-ն ամրապնդում են կայունությունը (կապիտալի աճ կամ վարկի երկարացում), իսկ Գ-ն (կարճաժամկետ վարկով սարքավորում) ռիսկը բարձրացնում է մինչև 1.14 և խախտում նորման։", 6, 120)

# ---------- Sheet 4: charts ----------
cs = wb.create_sheet("Գծապատկերներ"); cs.sheet_view.showGridLines = False
title(cs, "Գծապատկերներ", "Ակտիվների և պասիվների խմբերի համադրում, իրացվելիության և կայունության գործակիցներ", 16)
L = "'Իրացվելիություն'!"; K2 = "'Կայունություն'!"
head(cs, 5, ["Խումբ", "Ակտիվ", "Պասիվ"])
for i in range(4): row(cs, 6 + i, [f"{i+1}", f"={L}C{6+i}", f"={L}F{6+i}"], fmt="#,##0")
head(cs, 12, ["Գործակից", "Արժեք", "Նորմայի ստորին սահման"])
for i, (n, r, lo) in enumerate([("Բացարձակ", 17, 0.2), ("Արագ", 18, 0.7), ("Ընթացիկ", 19, 1.0)]): row(cs, 13 + i, [n, f"={L}F{r}", lo], fmt="0.000")
head(cs, 18, ["Կայունություն", "Արժեք", "Նորմա"])
for i, (n, r, nm) in enumerate([("Անկախություն", 9, 0.5), ("Կախվածություն", 10, 0.5), ("Ֆին. ռիսկ", 11, 1.0), ("Կայունություն", 14, 0.6)]): row(cs, 19 + i, [n, f"={K2}D{r}", nm], fmt="0.000")
head(cs, 25, ["Պասիվի կառուցվածք", "Գումար"])
for i, (n, r) in enumerate([("Սեփական կապիտալ", "F6"), ("Ոչ ընթացիկ պարտ.", "F7"), ("Կրեդիտորական պարտք", "F10"), ("Կարճ. վարկ", "F11")]): row(cs, 26 + i, [n, f"={B}{r}"], fmt="#,##0")
def dl():
    d = DataLabelList(); d.showVal = True; d.showSerName = d.showCatName = d.showLegendKey = d.showPercent = False; return d
def bar(r1, r2, ttl, anchor, cols, fm):
    ch = BarChart(); ch.type = "col"; ch.title = ttl; ch.style = 10; ch.add_data(Reference(cs, min_col=2, max_col=3, min_row=r1, max_row=r2), titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=r1 + 1, max_row=r2)); ch.width, ch.height = 16, 8
    for s, c in zip(ch.series, cols): s.graphicalProperties.solidFill = c; s.graphicalProperties.line.solidFill = c
    ch.dataLabels = dl(); ch.dataLabels.numFmt = fm; ch.y_axis.majorGridlines = None; ch.y_axis.delete = False; ch.x_axis.delete = False; cs.add_chart(ch, anchor)
bar(5, 9, "Ա1–Ա4 ընդդեմ Պ1–Պ4", "E5", [INK, RUST], "#,##0"); bar(12, 15, "Իրացվելիության գործակիցներ և նորմա", "N5", [INK, "C9BFA8"], "0.00")
bar(18, 22, "Կայունության գործակիցներ և նորմա", "E22", [SAGE, "C9BFA8"], "0.00")
dn = DoughnutChart(); dn.title = "Պասիվի կառուցվածք"; dn.holeSize = 55; dn.add_data(Reference(cs, min_col=2, min_row=25, max_row=29), titles_from_data=True)
dn.set_categories(Reference(cs, min_col=1, min_row=26, max_row=29)); d = DataLabelList(); d.showPercent = True; d.showVal = d.showCatName = d.showSerName = d.showLegendKey = False; dn.dataLabels = d
dn.width, dn.height = 14, 8; cs.add_chart(dn, "N22")
cs.column_dimensions["A"].width = 22
wb.save(OUT); print("saved", OUT)
