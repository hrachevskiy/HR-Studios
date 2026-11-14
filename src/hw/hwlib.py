# -*- coding: utf-8 -*-
"""Excel builders for homeworks 2–6 and the 1st midterm. Each homework gets its own theme."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, LineChart, DoughnutChart, Reference
from openpyxl.chart.label import DataLabelList

THEMES = {
  "paper":     dict(font="Georgia", head="1F3A5F", acc="B5452B", good="4E7D5B", bad="B5452B", alt="FBF7EE", band="E9DFC9", sub="7A6A4F", inp="1F4FBF", c2="C9BFA8"),
  "blueprint": dict(font="Consolas", head="0B3D6E", acc="1E88E5", good="00897B", bad="D84315", alt="EEF5FC", band="D6E7F7", sub="3F6E9A", inp="0000FF", c2="90CAF9"),
  "swiss":     dict(font="Arial", head="111111", acc="E30613", good="0A7C2F", bad="E30613", alt="F4F4F4", band="FFE9E9", sub="666666", inp="0000FF", c2="BDBDBD"),
  "notebook":  dict(font="Calibri", head="6A4C93", acc="F28482", good="2A9D8F", bad="E76F51", alt="FFF8E7", band="FDE2E4", sub="8D7AA8", inp="1D4ED8", c2="CDB4DB"),
  "gold":      dict(font="Cambria", head="1C1C1C", acc="B8860B", good="2E7D32", bad="B71C1C", alt="FAF6EC", band="EFE3C2", sub="7D6A3A", inp="1F4FBF", c2="D9C38A"),
}

class X:
    def __init__(self, theme, author, course="ԻՏ-447 · Դասախոս՝ Օ.Ա. Գալստյան"):
        self.t = THEMES[theme]; self.author = author; self.course = course
        self.wb = openpyxl.Workbook(); self._first = True
        s = Side(style="thin", color=self.t["c2"]); self.box = Border(left=s, right=s, top=s, bottom=s)
    def F(self, **k): return Font(name=self.t["font"], **k)
    def sheet(self, name, title, sub, widths):
        if self._first: ws = self.wb.active; ws.title = name; self._first = False
        else: ws = self.wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        for i, w in enumerate(widths): ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
        n = len(widths)
        ws["A1"] = title; ws["A1"].font = self.F(size=15, bold=True, color=self.t["head"])
        ws["A2"] = f"{sub} · Կատարեց՝ {self.author} · {self.course}"; ws["A2"].font = self.F(size=9, italic=True, color=self.t["sub"])
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n); ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n)
        for c in range(1, n + 1): ws.cell(3, c).fill = PatternFill("solid", fgColor=self.t["acc"])
        ws.row_dimensions[3].height = 4; ws.row_dimensions[1].height = 24
        return ws
    def head(self, ws, r, vals, c0=1):
        for j, v in enumerate(vals):
            c = ws.cell(r, c0 + j, v); c.fill = PatternFill("solid", fgColor=self.t["head"]); c.font = self.F(bold=True, color="FFFFFF", size=10)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = self.box
        ws.row_dimensions[r].height = 32
    def row(self, ws, r, vals, c0=1, fmt=None, bold=False, fill=None, inputs=(), h=None):
        for j, v in enumerate(vals):
            c = ws.cell(r, c0 + j, v); c.border = self.box
            c.font = self.F(size=10, bold=bold, color=self.t["inp"] if (c0 + j) in inputs and not (isinstance(v, str) and v.startswith("=")) else "000000")
            c.alignment = Alignment(vertical="center", wrap_text=True, horizontal="left" if j < 3 else "right")
            c.fill = PatternFill("solid", fgColor=fill or (self.t["alt"] if r % 2 else "FFFFFF"))
            if fmt and j >= 3: c.number_format = fmt
        if h: ws.row_dimensions[r].height = h
    def fmt(self, ws, rng, f):
        for row in ws[rng]:
            for c in row: c.number_format = f
    def verdict_cf(self, ws, rng):
        a = rng.split(":")[0]
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({a},1)="✔"'], font=Font(color=self.t["good"], bold=True)))
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({a},1)="✖"'], font=Font(color=self.t["bad"], bold=True)))
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({a},1)="▲"'], font=Font(color=self.t["good"], bold=True)))
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({a},1)="▼"'], font=Font(color=self.t["bad"], bold=True)))
    def note(self, ws, r, txt, width, h=110):
        ws.cell(r, 1, txt); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=width)
        c = ws.cell(r, 1); c.alignment = Alignment(wrap_text=True, vertical="top"); c.font = self.F(size=10, color="2B2B2B"); c.fill = PatternFill("solid", fgColor=self.t["band"])
        ws.row_dimensions[r].height = h
    def dl(self, fm):
        d = DataLabelList(); d.showVal = True; d.showSerName = d.showCatName = d.showLegendKey = d.showPercent = False; d.numFmt = fm; return d
    def bar(self, ws, data_ref, cats_ref, title, anchor, colors, fm="#,##0", w=16, h=8, horiz=False):
        ch = BarChart(); ch.type = "bar" if horiz else "col"; ch.title = title; ch.style = 10
        ch.add_data(data_ref, titles_from_data=True); ch.set_categories(cats_ref); ch.width, ch.height = w, h
        for s, c in zip(ch.series, colors): s.graphicalProperties.solidFill = c; s.graphicalProperties.line.solidFill = c
        ch.dataLabels = self.dl(fm); ch.y_axis.majorGridlines = None; ch.y_axis.delete = False; ch.x_axis.delete = False
        ws.add_chart(ch, anchor); return ch
    def donut(self, ws, data_ref, cats_ref, title, anchor, w=12, h=8):
        dn = DoughnutChart(); dn.title = title; dn.holeSize = 55; dn.add_data(data_ref, titles_from_data=True); dn.set_categories(cats_ref)
        d = DataLabelList(); d.showPercent = True; d.showVal = d.showCatName = d.showSerName = d.showLegendKey = False; dn.dataLabels = d
        dn.width, dn.height = w, h; ws.add_chart(dn, anchor)
    def save(self, path): self.wb.save(path)

# ======================= LIQUIDITY + STABILITY (lessons 2–3, midterm 1–2) =======================
def balance_sheet(x, D, name="Հաշվեկշիռ", title="Հաշվեկշիռ 2025թ. (հազ. դրամ)"):
    ws = x.sheet(name, title, "Մուտքային տվյալներ", [6, 40, 16, 6, 40, 16])
    x.head(ws, 5, ["№", "ԱԿՏԻՎ", "2025թ.", "№", "ՊԱՍԻՎ", "2025թ."])
    A = [("1", "Ոչ ընթացիկ ակտիվներ", D["noa"]), ("2", "Ընթացիկ ակտիվներ", "=SUM(C8:C11)"), ("2.1", "Պաշարներ", D["inv"]), ("2.2", "Դեբիտորական պարտքեր", D["rec"]),
         ("2.3", "Ընթացիկ ֆինանսական ներդրումներ", D["cfi"]), ("2.4", "Դրամական միջոցներ", D["cash"])]
    P = [("3", "Սեփական կապիտալ", D["eq"]), ("4", "Ոչ ընթացիկ պարտավորություններ", D["ltl"]), ("5", "Ընթացիկ պարտավորություններ", "=SUM(F9:F10)"),
         ("5.1", "Կրեդիտորական պարտքեր", D["pay"]), ("5.2", "Կարճաժամկետ բանկային վարկ", D["loan"]), ("", "", None)]
    for i in range(6): x.row(ws, 6 + i, list(A[i]) + list(P[i]), fmt="#,##0", inputs=(3, 6))
    x.fmt(ws, "C6:C11", "#,##0")
    x.row(ws, 12, ["", "ՀԱՇՎԵԿՇԻՌ", "=C6+C7", "", "ՀԱՇՎԵԿՇԻՌ", "=F6+F7+F8"], fmt="#,##0", bold=True, fill=x.t["band"]); ws["C12"].number_format = "#,##0"
    ws["B13"] = "Ստուգում (ակտիվ − պասիվ = 0)"; ws["C13"] = "=C12-F12"; ws["C13"].number_format = "#,##0"; ws["B13"].font = x.F(size=9, italic=True)
    ws["B14"] = D.get("src", "Կապույտ թվերը դասախոսի տվյալներն են, մնացածը՝ բանաձևեր։"); ws["B14"].font = x.F(size=9, italic=True, color=x.t["sub"])
    ws.freeze_panes = "A6"
    return f"'{name}'!"

def liquidity(x, B, D, name="Իրացվելիություն", title="Հաշվեկշռի իրացվելիություն և վճարունակություն"):
    ws = x.sheet(name, title, "Ակտիվներն ըստ իրացման արագության, պասիվներն՝ ըստ մարման ժամկետի", [6, 36, 15, 6, 34, 15, 15, 24])
    x.head(ws, 5, ["Խումբ", "Ակտիվներ", "Գումար", "Խումբ", "Պասիվներ", "Գումար", "Ավելցուկ (+) / պակաս (−)", "Պայման"])
    G = [("Ա1", "Առավել իրացվելի (ԴՄ + ԿՖՆ)", f"={B}C11+{B}C10", "Պ1", "Հրատապ (կրեդիտորական պարտքեր)", f"={B}F9", ">="),
         ("Ա2", "Արագ իրացվելի (դեբիտորական պարտքեր)", f"={B}C9", "Պ2", "Կարճաժամկետ (բանկային վարկ)", f"={B}F10", ">="),
         ("Ա3", "Դանդաղ իրացվելի (պաշարներ)", f"={B}C8", "Պ3", "Երկարաժամկետ (ոչ ընթացիկ պարտ.)", f"={B}F7", ">="),
         ("Ա4", "Դժվար իրացվելի (ոչ ընթացիկ ակտիվներ)", f"={B}C6", "Պ4", "Մշտական (սեփական կապիտալ)", f"={B}F6", "<=")]
    for i, (a, an, av, p, pn, pv, op) in enumerate(G):
        r = 6 + i; sym = "≥" if op == ">=" else "≤"
        x.row(ws, r, [a, an, av, p, pn, pv, f"=C{r}-F{r}", f'=IF(C{r}{op}F{r},"✔ Ա{i+1} {sym} Պ{i+1}","✖ Ա{i+1} {sym} Պ{i+1} խախտված")'])
    x.fmt(ws, "C6:G9", "#,##0"); x.fmt(ws, "C6:C9", "#,##0")
    x.row(ws, 10, ["", "Ընդամենը", "=SUM(C6:C9)", "", "Ընդամենը", "=SUM(F6:F9)", "=C10-F10", '=IF(COUNTIF(H6:H9,"✔*")=4,"✔ Բացարձակ իրացվելի","✖ Բացարձակ իրացվելի չէ")'], bold=True, fill=x.t["band"])
    x.fmt(ws, "C10:G10", "#,##0"); ws["C10"].number_format = "#,##0"
    x.head(ws, 13, ["№", "Ցուցանիշ", "Բանաձև", "", "Մեկնաբանություն", "Արժեք", "Նորմա", "Գնահատական"])
    K = [("1", "Ընթացիկ (կարճաժամկետ) իրացվելիություն", "(Ա1+Ա2) − (Պ1+Պ2)", "Մոտ ապագայի վճարունակություն", "=(C6+C7)-(F6+F7)", "> 0", '=IF(F14>0,"✔ Վճարունակ","✖ Պակասուրդ")', "#,##0"),
         ("2", "Հեռանկարային իրացվելիություն", "Ա3 − Պ3", "Ապագա մուտքեր և վճարումներ", "=C8-F8", "> 0", '=IF(F15>0,"✔ Դրական","✖ Բացասական")', "#,##0"),
         ("3", "Բացարձակ իրացվելիության գործակից", "(ԴՄ+ԿՖՆ) ÷ ԸՊ", "Որքան պարտք կփակենք հենց հիմա", f"=C6/{B}F8", "0.2 – 0.5", '=IF(AND(F16>=0.2,F16<=0.5),"✔ Նորմայում",IF(F16<0.2,"✖ Ցածր","▲ Նորմայից բարձր"))', "0.000"),
         ("4", "Արագ իրացվելիության գործակից", "(ԴՄ+ԿՖՆ+ԴՊ) ÷ ԸՊ", "Եթե դեբիտորներն էլ վճարեն", f"=(C6+C7)/{B}F8", "0.7 – 1.0", '=IF(AND(F17>=0.7,F17<=1),"✔ Նորմայում",IF(F17<0.7,"✖ Ցածր","▲ Նորմայից բարձր"))', "0.000"),
         ("5", "Ընթացիկ իրացվելիության գործակից", "ԸԱ ÷ ԸՊ", "Բոլոր ընթացիկ ակտիվները՝ պարտքերի դիմաց", f"={B}C7/{B}F8", "1 – 2", '=IF(AND(F18>=1,F18<=2),"✔ Նորմայում",IF(F18<1,"✖ Ցածր","▲ Նորմայից բարձր"))', "0.000")]
    for i, (n, nm, fx, cm, v, nr, ev, fm) in enumerate(K):
        r = 14 + i; x.row(ws, r, [n, nm, fx, "", cm, v, nr, ev], h=30); ws.cell(r, 6).number_format = fm; ws.cell(r, 6).font = x.F(size=11, bold=True, color=x.t["head"])
    x.verdict_cf(ws, "H6:H18")
    q, c, p = D["scen"]
    ws["B20"] = f"Հարց 9 · պաշարների ձեռքբերում {q:,}"; ws["B20"].font = x.F(bold=True, color=x.t["acc"])
    ws["E20"] = "Վճարում դրամով"; ws["F20"] = c; ws["G20"] = "Կրեդիտորական պարտք"; ws["H20"] = p
    for k in ("F20", "H20"): ws[k].font = x.F(bold=True, color=x.t["inp"]); ws[k].number_format = "#,##0"
    x.head(ws, 21, ["№", "Հոդված", "Մինչև", "", "Փոփոխություն", "Հետո", "Նորմա", "Ազդեցություն"])
    S = [("Դրամական միջոցներ", f"={B}C11", "=-F20"), ("Պաշարներ", f"={B}C8", "=F20+H20"), ("Կրեդիտորական պարտքեր", f"={B}F9", "=H20"),
         ("Ընթացիկ ակտիվներ", f"={B}C7", "=E22+E23"), ("Ընթացիկ պարտավորություններ", f"={B}F8", "=E24")]
    for i, (nm, b0, d) in enumerate(S): r = 22 + i; x.row(ws, r, [i + 1, nm, b0, "", d, f"=C{r}+E{r}", "", ""]); x.fmt(ws, f"C{r}:F{r}", "#,##0")
    SK = [("Բացարձակ իրացվելիություն", f"=(C22+{B}C10)/C26", f"=(F22+{B}C10)/F26", "0.2–0.5"),
          ("Արագ իրացվելիություն", f"=(C22+{B}C10+{B}C9)/C26", f"=(F22+{B}C10+{B}C9)/F26", "0.7–1.0"),
          ("Ընթացիկ իրացվելիություն", "=C25/C26", "=F25/F26", "1–2")]
    for i, (nm, b0, a1, nr) in enumerate(SK):
        r = 27 + i; x.row(ws, r, [f"Գ{i+1}", nm, b0, "", f"=F{r}-C{r}", a1, nr, f'=IF(F{r}<C{r},"▼ վատթարանում է","▲ բարելավվում է")']); x.fmt(ws, f"C{r}:F{r}", "0.000")
    x.verdict_cf(ws, "H27:H29")
    # chart data block (right side)
    ws["J5"] = "Խումբ"; ws["K5"] = "Ակտիվ"; ws["L5"] = "Պասիվ"
    for i in range(4): ws.cell(6 + i, 10, f"{i+1}"); ws.cell(6 + i, 11, f"=C{6+i}"); ws.cell(6 + i, 12, f"=F{6+i}")
    ws["J13"] = "Գործակից"; ws["K13"] = "Մինչև"; ws["L13"] = "Հետո"
    for i, n in enumerate(["Բացարձակ", "Արագ", "Ընթացիկ"]): ws.cell(14 + i, 10, n); ws.cell(14 + i, 11, f"=C{27+i}"); ws.cell(14 + i, 12, f"=F{27+i}")
    for r in range(5, 17):
        for c in (10, 11, 12): ws.cell(r, c).font = x.F(size=8, color="999999")
    x.bar(ws, Reference(ws, min_col=11, max_col=12, min_row=5, max_row=9), Reference(ws, min_col=10, min_row=6, max_row=9), "Ա1–Ա4 ընդդեմ Պ1–Պ4", "N4", [x.t["head"], x.t["acc"]])
    x.bar(ws, Reference(ws, min_col=11, max_col=12, min_row=13, max_row=16), Reference(ws, min_col=10, min_row=14, max_row=16), "Գործակիցները՝ գործարքից առաջ և հետո", "N21", [x.t["head"], x.t["acc"]], "0.00")
    return ws

def stability(x, B, D, name="Կայունություն", title="Ֆինանսական կայունություն"):
    ws = x.sheet(name, title, "Որքանով է ընկերությունը կանգնած սեփական ոտքերի վրա", [6, 42, 26, 15, 14, 28])
    x.head(ws, 5, ["№", "Ցուցանիշ", "Բանաձև", "Արժեք", "Նորմա", "Գնահատական"])
    T = [("1", "Սեփական ընթացիկ ակտիվներ (ՍԸԱ)", "ՍԿ + ՈԸՊ − ՈԸԱ", f"={B}F6+{B}F7-{B}C6", "> 0", '=IF(D6>0,"✔ Դրական","✖ Բացասական")', "#,##0"),
         ("2", "Ընթացիկ ակտիվների ապահովվածություն ՍԸԱ-ով", "ՍԸԱ ÷ ԸԱ", f"=D6/{B}C7", "≥ 0.1", '=IF(D7>=0.1,"✔ Ապահովված","✖ Անբավարար")', "0.000"),
         ("3", "Պաշարների ապահովվածություն ՍԸԱ-ով", "ՍԸԱ ÷ Պաշարներ", f"=D6/{B}C8", "0.6 – 0.8", '=IF(D8>=0.6,"✔ Ապահովված","✖ Անբավարար")', "0.000"),
         ("4", "Ֆինանսական անկախության գործակից", "ՍԿ ÷ Ակտիվներ", f"={B}F6/{B}C12", "≥ 0.5", '=IF(D9>=0.5,"✔ Անկախ","✖ Կախյալ")', "0.000"),
         ("5", "Ֆինանսական կախվածության գործակից", "ՓԿ ÷ Ակտիվներ", f"=({B}F7+{B}F8)/{B}C12", "≤ 0.5", '=IF(D10<=0.5,"✔ Նորմայում","✖ Բարձր")', "0.000"),
         ("6", "Ֆինանսական ռիսկի գործակից", "ՓԿ ÷ ՍԿ", f"=({B}F7+{B}F8)/{B}F6", "≤ 1", '=IF(D11<=1,"✔ Ցածր ռիսկ","✖ Բարձր ռիսկ")', "0.000"),
         ("7", "Ֆինանսական կայունության պաշար", "ՍԸԱ − Պաշարներ", f"=D6-{B}C8", "> 0", '=IF(D12>0,"✔ Պաշար կա","✖ Պակասուրդ")', "#,##0"),
         ("8", "Պաշարը պաշարների նկատմամբ, %", "Պաշար ÷ Պաշարներ × 100", f"=D12/{B}C8*100", "> 0", '=IF(D13>0,"✔ Դրական","✖ Բացասական")', "0.0"),
         ("9", "Ֆինանսական կայունության գործակից", "(ՍԿ + ՈԸՊ) ÷ Ակտիվներ", f"=({B}F6+{B}F7)/{B}C12", "≥ 0.6", '=IF(D14>=0.6,"✔ Կայուն","✖ Անկայուն")', "0.000")]
    for i, (n, nm, fx, v, nr, ev, fm) in enumerate(T):
        r = 6 + i; x.row(ws, r, [n, nm, fx, v, nr, ev], h=26); ws.cell(r, 4).number_format = fm; ws.cell(r, 4).font = x.F(size=11, bold=True, color=x.t["head"])
    x.verdict_cf(ws, "F6:F14")
    ws["B16"] = "Կայունության տեսակը՝"; ws["B16"].font = x.F(bold=True)
    ws["C16"] = f'=IF(D6>={B}C8,"Բացարձակ կայունություն",IF(D6+{B}F10>={B}C8,"Նորմալ կայունություն",IF(D6+{B}F10+{B}F9>={B}C8,"Անկայուն վիճակ","Ճգնաժամային վիճակ")))'
    ws["C16"].font = x.F(bold=True, color=x.t["good"], size=12); ws.merge_cells("C16:F16")
    x.head(ws, 18, ["№", "Սցենար (հարց 7)", "Ինչ ենք անում", "Գկայ հետո", "Գֆռ հետո", "Արդյունք"])
    R = D["reinv"]; E = D["equip"]
    SC = [("Ա", f"Շահույթը վերաներդնել (+{R:,} ՍԿ և ԴՄ)", "Սեփական կապիտալ ↑", f"=({B}F6+{R}+{B}F7)/({B}C12+{R})", f"=({B}F7+{B}F8)/({B}F6+{R})"),
          ("Բ", "Կարճաժամկետ վարկը դարձնել երկարաժամկետ", "Վերաֆինանսավորում", f"=({B}F6+{B}F7+{B}F10)/{B}C12", f"=({B}F7+{B}F8)/{B}F6"),
          ("Գ", f"Սարքավորում {E:,}՝ կարճաժամկետ վարկով", "Ռիսկային քայլ", f"=({B}F6+{B}F7)/({B}C12+{E})", f"=({B}F7+{B}F8+{E})/{B}F6")]
    for i, (n, a, b, c, d) in enumerate(SC):
        r = 19 + i; x.row(ws, r, [n, a, b, c, d, f'=IF(AND(D{r}>=D14,E{r}<=D11),"✔ Կամրապնդի կայունությունը","✖ Կթուլացնի կայունությունը")'], h=34); x.fmt(ws, f"D{r}:E{r}", "0.000")
    x.verdict_cf(ws, "F19:F21")
    ws["H5"] = "Գործակից"; ws["I5"] = "Արժեք"; ws["J5"] = "Նորմա"
    for i, (n, r, nm) in enumerate([("Անկախություն", 9, 0.5), ("Կախվածություն", 10, 0.5), ("Ֆին. ռիսկ", 11, 1.0), ("Կայունություն", 14, 0.6)]):
        ws.cell(6 + i, 8, n); ws.cell(6 + i, 9, f"=D{r}"); ws.cell(6 + i, 10, nm)
    ws["H12"] = "Պասիվ"; ws["I12"] = "Գումար"
    for i, (n, r) in enumerate([("Սեփական կապիտալ", "F6"), ("Ոչ ընթացիկ պարտ.", "F7"), ("Կրեդիտորական պարտք", "F9"), ("Կարճ. վարկ", "F10")]):
        ws.cell(13 + i, 8, n); ws.cell(13 + i, 9, f"={B}{r}")
    for r in range(5, 17):
        for c in (8, 9, 10): ws.cell(r, c).font = x.F(size=8, color="999999")
    x.bar(ws, Reference(ws, min_col=9, max_col=10, min_row=5, max_row=9), Reference(ws, min_col=8, min_row=6, max_row=9), "Կայունության գործակիցներ և նորմա", "L4", [x.t["good"], x.t["c2"]], "0.00")
    x.donut(ws, Reference(ws, min_col=9, min_row=12, max_row=16), Reference(ws, min_col=8, min_row=13, max_row=16), "Պասիվի կառուցվածք", "L21")
    return ws

# ======================= FIXED ASSETS (lesson 4, midterm 3) =======================
FA_ROWS = [("Հիմնական միջոցների միջին տարեկան արժեք", "ՀՄ"), ("Հիմնական միջոցների տարեսկզբի մնացորդ", "ՀՄտս"), ("Տարեսկզբի կուտակված մաշվածություն", "ԿՄտս"),
           ("Հիմնական միջոցների մուտք", "ՀՄմուտք"), ("Հիմնական միջոցների ելք", "ՀՄելք"), ("Հիմնական միջոցների տարեվերջի մնացորդ", "ՀՄտվ"),
           ("Տարեվերջի կուտակված մաշվածություն", "ԿՄտվ"), ("Դուրսգրված մաշվածություն", "ՀՄդ.մաշվ"), ("Մեքենասարքավորումների միջին տարեկան արժեք", "ՄՍ"),
           ("Հասույթ", "Հ"), ("Զուտ շահույթ", "ԶՇ"), ("Աշխատողների միջին ցուցակային թվաքանակ", "Քա"), ("Արտադրանքի ծավալ", "Ա")]
def fixed_assets(x, D, name="Հիմնական միջոցներ", title="Հիմնական միջոցներով ապահովվածություն և օգտագործում"):
    ws = x.sheet(name, title, "Գործոնային և արդյունքային ցուցանիշներ, հազ. դրամ", [6, 46, 16, 15, 15, 15, 12])
    x.head(ws, 5, ["№", "Գործոնային ցուցանիշ", "Նշան", "2024թ.", "2025թ.", "Փոփոխություն", "Աճ, %"])
    for i, (nm, code) in enumerate(FA_ROWS):
        r = 6 + i; v0, v1 = D[code]; x.row(ws, r, [i + 1, nm, code, v0, v1, f"=E{r}-D{r}", f"=IF(D{r}=0,0,E{r}/D{r}*100-100)"], fmt="#,##0", inputs=(4, 5))
        ws.cell(r, 7).number_format = "0.0"
    rr = {code: 6 + i for i, (_, code) in enumerate(FA_ROWS)}
    g = lambda c, col: f"{col}{rr[c]}"
    x.head(ws, 21, ["№", "Արդյունքային ցուցանիշ", "Նշան", "2024թ.", "2025թ.", "Փոփոխություն", "Բանաձև"])
    OUT = [("Աշխատանքի զինվածություն", "Գազ", lambda c: f"={g('ՀՄ',c)}/{g('Քա',c)}", "#,##0.00", "ՀՄ ÷ Քա"),
           ("Տեխնիկական զինվածություն", "Գտզ", lambda c: f"={g('ՄՍ',c)}/{g('Քա',c)}", "#,##0.00", "ՄՍ ÷ Քա"),
           ("ՀՄ հարաբերական տնտեսում (−) / գերածախս (+)", "±ΔՀՄհար.տնտ", None, "#,##0", "ՀՄ₁ − ՀՄ₀ × Ա₁/Ա₀"),
           ("Նորացման գործակից", "Գնոր", lambda c: f"={g('ՀՄմուտք',c)}/{g('ՀՄտվ',c)}", "0.000", "ՀՄմուտք ÷ ՀՄտվ"),
           ("Դուրսգրման գործակից", "Գդգ", lambda c: f"={g('ՀՄելք',c)}/{g('ՀՄտս',c)}", "0.000", "ՀՄելք ÷ ՀՄտս"),
           ("Տարեսկզբի մաշվածության գործակից", "Գմշ.տս", lambda c: f"={g('ԿՄտս',c)}/{g('ՀՄտս',c)}", "0.000", "ԿՄտս ÷ ՀՄտս"),
           ("Տարեվերջի մաշվածության գործակից", "Գմշ.տվ", lambda c: f"={g('ԿՄտվ',c)}/{g('ՀՄտվ',c)}", "0.000", "ԿՄտվ ÷ ՀՄտվ"),
           ("Տարեսկզբի պիտանելիության գործակից", "Գպտ.տս", lambda c: f"=1-{c}27", "0.000", "1 − Գմշ.տս"),
           ("Տարեվերջի պիտանելիության գործակից", "Գպտ.տվ", lambda c: f"=1-{c}28", "0.000", "1 − Գմշ.տվ"),
           ("ՀՄ շահութաբերություն, %", "ՇԲԹՀՄ", lambda c: f"={g('ԶՇ',c)}/{g('ՀՄ',c)}*100", "0.00", "ԶՇ ÷ ՀՄ × 100"),
           ("Իրացման շահութաբերություն, %", "ՇԲԹիրաց", lambda c: f"={g('ԶՇ',c)}/{g('Հ',c)}*100", "0.00", "ԶՇ ÷ Հ × 100"),
           ("ՀՄ հատույց (ֆոնդահատույց)", "ՀՏ", lambda c: f"={g('Հ',c)}/{g('ՀՄ',c)}", "0.00", "Հ ÷ ՀՄ"),
           ("ΔՇԲԹՀՄ՝ իրացման շահութաբերության հաշվին", "±ΔՇԲԹ(ՀՄ)(ՇԲԹիրաց)", None, "+0.00;-0.00", "ΔՇԲԹիրաց × ՀՏ₀"),
           ("ΔՇԲԹՀՄ՝ ֆոնդահատույցի հաշվին", "±ΔՇԲԹ(ՀՄ)(ՀՏ)", None, "+0.00;-0.00", "ΔՀՏ × ՇԲԹիրաց₁")]
    for i, (nm, code, f, fm, fx) in enumerate(OUT):
        r = 22 + i
        if f: vals = [i + 1, nm, code, f("D"), f("E"), f"=E{r}-D{r}", fx]
        elif code == "±ΔՀՄհար.տնտ": vals = [i + 1, nm, code, "x", f"={g('ՀՄ','E')}-{g('ՀՄ','D')}*{g('Ա','E')}/{g('Ա','D')}", "x", fx]
        elif code.endswith("(ՇԲԹիրաց)"): vals = [i + 1, nm, code, "x", "x", "=F32*D33", fx]
        else: vals = [i + 1, nm, code, "x", "x", "=F33*E32", fx]
        x.row(ws, r, vals, h=22); x.fmt(ws, f"D{r}:F{r}", fm)
    x.row(ws, 36, ["", "Ստուգում՝ գործոնների գումար = ΔՇԲԹՀՄ", "", "", "", "=F34+F35-F31", "պետք է լինի 0"], bold=True, fill=x.t["band"]); ws["F36"].number_format = "0.0000"
    # chart data
    ws["I5"] = "Գործակից"; ws["J5"] = "2024"; ws["K5"] = "2025"
    for i, r in enumerate(range(25, 31)): ws.cell(6 + i, 9, f"=C{r}"); ws.cell(6 + i, 10, f"=D{r}"); ws.cell(6 + i, 11, f"=E{r}")
    ws["I14"] = "Գործոն"; ws["J14"] = "Ազդեցություն"
    ws["I15"] = "Իրացման շահութաբերություն"; ws["J15"] = "=F34"; ws["I16"] = "Ֆոնդահատույց"; ws["J16"] = "=F35"; ws["I17"] = "Ընդամենը"; ws["J17"] = "=F31"
    for r in range(5, 18):
        for c in (9, 10, 11): ws.cell(r, c).font = x.F(size=8, color="999999")
    x.bar(ws, Reference(ws, min_col=10, max_col=11, min_row=5, max_row=11), Reference(ws, min_col=9, min_row=6, max_row=11), "Վիճակի գործակիցներ 2024 ↔ 2025", "M4", [x.t["c2"], x.t["head"]], "0.00", w=18)
    x.bar(ws, Reference(ws, min_col=10, min_row=14, max_row=17), Reference(ws, min_col=9, min_row=15, max_row=17), "ՇԲԹՀՄ փոփոխության գործոններ (պ.պ.)", "M21", [x.t["acc"]], "+0.00;-0.00", w=18)
    return ws

# ======================= MATERIALS (lesson 5, midterm 4) =======================
def materials1(x, D, name="Նյութական պաշարներ", title="Նյութական պաշարների օգտագործման վերլուծություն"):
    ws = x.sheet(name, title, "Նյութական ծախս, նյութատարություն, նյութահատույց, գործոնային վերլուծություն", [6, 34, 13, 13, 15, 13, 13, 15])
    y0, y1 = D["years"]
    x.head(ws, 5, ["№", "Ցուցանիշ", f"{y0} նորմա/քանակ", f"{y0} գին", f"{y0} ընդամենը", f"{y1} նորմա/քանակ", f"{y1} գին", f"{y1} ընդամենը"])
    for i, (n0, p0, n1, p1) in enumerate(D["mats"]):
        r = 6 + i; x.row(ws, r, [i + 1, f"Նյութ-{i+1}", n0, p0, f"=C{r}*D{r}", n1, p1, f"=F{r}*G{r}"], inputs=(3, 4, 6, 7))
        x.fmt(ws, f"C{r}:H{r}", "#,##0.0")
    x.row(ws, 13, ["", "Միավոր արտադրանքի նյութական ծախս", "x", "x", "=SUM(E6:E12)", "x", "x", "=SUM(H6:H12)"], bold=True, fill=x.t["band"])
    q0, P0, q1, P1 = D["prod"]
    x.row(ws, 14, [8, "Արտադրանք (քանակ × գին = ծավալ Ա)", q0, P0, "=C14*D14", q1, P1, "=F14*G14"], inputs=(3, 4, 6, 7))
    x.row(ws, 15, ["", "Ընդամենը նյութական ծախս (Նծ)", "x", "x", "=E13*C14", "x", "x", "=H13*F14"], bold=True, fill=x.t["band"])
    x.row(ws, 16, [9, "Շահույթ (Շ)", "x", "x", D["profit"][0], "x", "x", D["profit"][1]], inputs=(5, 8))
    x.fmt(ws, "C13:H16", "#,##0")
    x.head(ws, 19, ["№", "Ցուցանիշ", "Նշան", "Բանաձև", y0, y1, "Փոփոխություն", "Գնահատական"])
    O = [("Նյութատարություն", "ՆՏ", "Նծ ÷ Ա", "=E15/E14", "=H15/H14", "0.0000", '=IF(G20<0,"▲ նվազել է (լավ է)","▼ աճել է")'),
         ("Նյութական ծախսերի շահութաբերություն, %", "ՇԲԹՆԾ", "Շ ÷ Նծ × 100", "=E16/E15*100", "=H16/H15*100", "0.00", '=IF(G21>0,"▲ աճել է","▼ նվազել է")'),
         ("Արտադրանքի շահութաբերություն, %", "ՇԲԹԱ", "Շ ÷ Ա × 100", "=E16/E14*100", "=H16/H14*100", "0.00", '=IF(G22>0,"▲ աճել է","▼ նվազել է")'),
         ("Նյութահատույց", "ՆՀ", "Ա ÷ Նծ", "=E14/E15", "=H14/H15", "0.0000", '=IF(G23>0,"▲ աճել է","▼ նվազել է")'),
         ("ΔՇԲԹՆԾ՝ արտադրանքի շահութաբերության հաշվին", "±ΔՇԲԹ(ՆԾ)(ՇԲԹԱ)", "ΔՇԲԹԱ × ՆՀ₀", "-", "=G22*E23", "+0.00;-0.00", ""),
         ("ΔՇԲԹՆԾ՝ նյութահատույցի հաշվին", "±ΔՇԲԹ(ՆԾ)(ՆՀ)", "ΔՆՀ × ՇԲԹԱ₁", "-", "=G23*F22", "+0.00;-0.00", ""),
         ("Նյութատարության ազդեցությունն ինքնարժեքի վրա", "±ΔԻ(ՆՏ)", "ΔՆՏ × Ա₁", "-", "=G20*H14", "+#,##0;-#,##0", '=IF(F26<0,"▲ տնտեսում","▼ գերածախս")'),
         ("Նյութատարության ազդեցությունն արտադրանքի ծավալի վրա", "±ΔԱ(ՆՏ)", "Նծ₁ ÷ ՆՏ₁ − Նծ₁ ÷ ՆՏ₀", "-", "=H15/F20-H15/E20", "+#,##0;-#,##0", '=IF(F27>0,"▲ ծավալն աճել է","▼ ծավալը կորել է")')]
    for i, (nm, code, fx, a, b, fm, ev) in enumerate(O):
        r = 20 + i; ch = f"=F{r}-E{r}" if a != "-" else "-"
        x.row(ws, r, [i + 1, nm, code, fx, a, b, ch, ev], h=26); x.fmt(ws, f"E{r}:G{r}", fm)
    x.row(ws, 28, ["", "Ստուգում՝ ΔՇԲԹՆԾ − (5 + 6)", "", "", "", "=G21-F24-F25", "պետք է լինի 0", ""], bold=True, fill=x.t["band"]); ws["F28"].number_format = "0.0000"
    x.verdict_cf(ws, "H20:H27")
    ws["J5"] = "Նյութ"; ws["K5"] = str(y0); ws["L5"] = str(y1)
    for i in range(7): ws.cell(6 + i, 10, f"Նյութ-{i+1}"); ws.cell(6 + i, 11, f"=E{6+i}"); ws.cell(6 + i, 12, f"=H{6+i}")
    for r in range(5, 13):
        for c in (10, 11, 12): ws.cell(r, c).font = x.F(size=8, color="999999")
    x.bar(ws, Reference(ws, min_col=11, max_col=12, min_row=5, max_row=12), Reference(ws, min_col=10, min_row=6, max_row=12), "Միավորի նյութական ծախսն ըստ նյութերի", "N4", [x.t["c2"], x.t["acc"]], "#,##0", w=18)
    x.donut(ws, Reference(ws, min_col=12, min_row=5, max_row=12), Reference(ws, min_col=10, min_row=6, max_row=12), f"Նյութական ծախսի կառուցվածք {y1}", "N21", w=14)
    return ws

def materials2(x, D, name="Նյութատարություն", title="Նյութատարության գործոնային վերլուծություն (շղթայական տեղադրում)"):
    ws = x.sheet(name, title, "Արտադրանքի տեսականի, ծախսի նորմա, նյութի գին, արտադրանքի գին", [12, 13, 11, 12, 13, 13, 11, 12, 13])
    x.head(ws, 5, ["Արտադրանք", "Ա₀ (քանակ)", "Ն₀ (նորմա)", "Գն₀ (նյութի գին)", "Գա₀ (արտ. գին)", "Ա₁ (քանակ)", "Ն₁ (նորմա)", "Գն₁ (նյութի գին)", "Գա₁ (արտ. գին)"])
    for i, (nm, *v) in enumerate(D["rows"]):
        r = 6 + i
        for j, val in enumerate([nm] + v):
            c = ws.cell(r, 1 + j, val); c.border = x.box; c.font = x.F(size=10, color=x.t["inp"] if j else "000000"); c.number_format = "#,##0.0#"
            c.fill = PatternFill("solid", fgColor=x.t["alt"] if r % 2 else "FFFFFF")
    x.head(ws, 11, ["Արտադրանք", "Ա₀·Ն₀·Գն₀", "Ա₀·Գա₀", "Ա₁·Ն₀·Գն₀", "Ա₁·Գա₀", "Ա₁·Ն₁·Գն₀", "Ա₁·Ն₁·Գն₁", "Ա₁·Գա₁", ""])
    for i in range(3):
        r = 12 + i; s = 6 + i
        vals = [f"=A{s}", f"=B{s}*C{s}*D{s}", f"=B{s}*E{s}", f"=F{s}*C{s}*D{s}", f"=F{s}*E{s}", f"=F{s}*G{s}*D{s}", f"=F{s}*G{s}*H{s}", f"=F{s}*I{s}"]
        for j, v in enumerate(vals):
            c = ws.cell(r, 1 + j, v); c.border = x.box; c.number_format = "#,##0"; c.font = x.F(size=10)
    for j in range(2, 9):
        col = openpyxl.utils.get_column_letter(j); c = ws.cell(15, j, f"=SUM({col}12:{col}14)"); c.number_format = "#,##0"; c.font = x.F(bold=True); c.border = x.box
        c.fill = PatternFill("solid", fgColor=x.t["band"])
    ws.cell(15, 1, "Σ").font = x.F(bold=True)
    x.head(ws, 18, ["Քայլ", "Հաշվարկ", "", "", "Նյութատարություն", "Գործոն", "", "Ազդեցություն", ""])
    ST = [("Նտ₀", "Σ(Ա₀Ն₀Գն₀) ÷ Σ(Ա₀Գա₀)", "=B15/C15", "", ""),
          ("Նտ′", "Σ(Ա₁Ն₀Գն₀) ÷ Σ(Ա₁Գա₀)", "=D15/E15", "Տեսականի (կառուցվածք)", "=E20-E19"),
          ("Նտ″", "Σ(Ա₁Ն₁Գն₀) ÷ Σ(Ա₁Գա₀)", "=F15/E15", "Նյութի ծախսի նորմա", "=E21-E20"),
          ("Նտ‴", "Σ(Ա₁Ն₁Գն₁) ÷ Σ(Ա₁Գա₀)", "=G15/E15", "Նյութի գին", "=E22-E21"),
          ("Նտ₁", "Σ(Ա₁Ն₁Գն₁) ÷ Σ(Ա₁Գա₁)", "=G15/H15", "Արտադրանքի գին", "=E23-E22")]
    for i, (a, b, c, d, e) in enumerate(ST):
        r = 19 + i; x.row(ws, r, [a, b, "", "", c, d, "", e, ""], h=22); ws.merge_cells(f"B{r}:D{r}"); ws.merge_cells(f"F{r}:G{r}")
        ws.cell(r, 5).number_format = "0.0000"; ws.cell(r, 8).number_format = "+0.0000;-0.0000"
    x.row(ws, 24, ["Ընդամենը", "ΔՆտ = Նտ₁ − Նտ₀", "", "", "=E23-E19", "Գործոնների գումար", "", "=SUM(H20:H23)", '=IF(ROUND(H24-E24,8)=0,"✔ համընկնում է","✖")'], bold=True, fill=x.t["band"])
    ws.merge_cells("B24:D24"); ws.merge_cells("F24:G24"); ws["E24"].number_format = "+0.0000;-0.0000"; ws["H24"].number_format = "+0.0000;-0.0000"
    x.verdict_cf(ws, "I24:I24")
    x.bar(ws, Reference(ws, min_col=8, min_row=19, max_row=23), Reference(ws, min_col=6, min_row=20, max_row=23), "Գործոնների ազդեցությունը նյութատարության վրա", "K4", [x.t["acc"]], "+0.0000;-0.0000", w=18)
    return ws

# ======================= LABOUR (lesson 6, midterm 5) =======================
def labour(x, D, name="Աշխատանք", title="Աշխատաժամանակի ֆոնդ և աշխատանքի արտադրողականություն"):
    ws = x.sheet(name, title, "Գործոնային վերլուծություն շղթայական տեղադրման (բացարձակ տարբերությունների) եղանակով", [7, 50, 12, 15, 15, 15, 11])
    x.head(ws, 5, ["№", "Գործոնային ցուցանիշ", "Նշան", "2024թ.", "2025թ.", "Տարբերություն", "%-ով"])
    I = [("1", "Անձնակազմի միջին տարեկան ցուցակային թիվ", "ԸԱ", *D["ԸԱ"]), ("2", "Արդյունք ստեղծող աշխատողների թիվ", "Թ", *D["Թ"]),
         ("3.1", "1 աշխատողի աշխատած օրեր", "Օ", *D["Օ"]), ("3.2", "1 աշխատողի աշխատած ժամեր (Օ × Ժ)", "Օ×Ժ", "=D8*D10", "=E8*E10"),
         ("4", "Աշխատանքային օրվա միջին տևողություն, ժամ", "Ժ", *D["Ժ"]), ("5", "Աշխատաժամանակի ֆոնդ, ժամ (Թ × Օ × Ժ)", "Ֆաշ.ժ", "=D7*D8*D10", "=E7*E8*E10"),
         ("6", "Ստացված արդյունք, հազ. դրամ", "ՍԱ", *D["ՍԱ"]), ("7", "Հասույթ, հազ. դրամ", "Հ", *D["Հ"]), ("8", "Զուտ շահույթ, հազ. դրամ", "ԶՇ", *D["ԶՇ"]),
         ("9", "Աշխատավարձի ֆոնդ, հազ. դրամ", "ԱՖ", *D["ԱՖ"]), ("10", "Կապիտալի միջին տարեկան արժեք, հազ. դրամ", "Կ", *D["Կ"]),
         ("11", "Կապիտալացված շահույթ", "ԿՇ", *D["ԿՇ"])]
    for i, (n, nm, code, a, b) in enumerate(I):
        r = 6 + i; x.row(ws, r, [n, nm, code, a, b, f"=E{r}-D{r}", f"=E{r}/D{r}*100-100"], inputs=(4, 5)); x.fmt(ws, f"D{r}:F{r}", "#,##0.00" if code in ("Ժ", "Օ×Ժ", "Ֆաշ.ժ") else "#,##0")
        ws.cell(r, 7).number_format = "+0.00;-0.00"
    # Analysis 1
    x.head(ws, 19, ["№", "Վերլուծություն 1 · Աշխատաժամանակի ֆոնդ", "Նշան", "2024թ.", "2025թ.", "Փաստ.", "%-ով"])
    A1 = [("1", "Աշխատաժամանակի ֆոնդ (ժամ)", "Ֆաշ.ժ", "=D11", "=E11", "=E20-D20", "=E20/D20*100-100"),
          ("1.1", "ըստ աշխատողների թվաքանակի փոփոխության", "±ΔՖ(Թ)", "x", "x", "=(E7-D7)*D8*D10", "x"),
          ("1.2", "ըստ աշխատանքային օրերի փոփոխության", "±ΔՖ(Օ)", "x", "x", "=E7*(E8-D8)*D10", "x"),
          ("1.3", "ըստ օրվա տևողության փոփոխության", "±ΔՖ(Ժ)", "x", "x", "=E7*E8*(E10-D10)", "x"),
          ("", "Ընդամենը փոփոխություն", "", "x", "x", "=SUM(F21:F23)", '=IF(ROUND(F24-F20,4)=0,"✔ = ΔՖ","✖")')]
    for i, v in enumerate(A1):
        r = 20 + i; x.row(ws, r, list(v), bold=(i in (0, 4)), fill=x.t["band"] if i == 4 else None); x.fmt(ws, f"D{r}:F{r}", "+#,##0.00;-#,##0.00" if i else "#,##0.00")
        ws.cell(r, 7).number_format = "+0.00;-0.00"
    x.verdict_cf(ws, "G24:G24")
    # Analysis 2
    x.head(ws, 27, ["№", "Վերլուծություն 2 · Աշխատանքի արտադրողականություն", "Նշան", "2024թ.", "2025թ.", "Փաստ.", "%-ով"])
    A2 = [("1", "Անձնակազմի միավորի միջին տարեկան արդյունք, հազ. դր.", "ՏԱ", "=D12/D6", "=E12/E6"),
          ("2", "Արդյունք ստեղծող 1 աշխատողի տարեկան արդյունք, հազ. դր.", "ՏԱ′", "=D12/D7", "=E12/E7"),
          ("3", "1 աշխատողի միջին օրական արդյունք, հազ. դր.", "ՕԱ", "=D12/(D7*D8)", "=E12/(E7*E8)"),
          ("4", "Միջին ժամային արտադրողականություն, դրամ", "ԺԱ", "=D12*1000/D11", "=E12*1000/E11"),
          ("5", "Արդյունք ստեղծողների տեսակարար կշիռ", "ՏԿ", "=D7/D6", "=E7/E6")]
    for i, (n, nm, code, a, b) in enumerate(A2):
        r = 28 + i; x.row(ws, r, [n, nm, code, a, b, f"=E{r}-D{r}", f"=E{r}/D{r}*100-100"]); x.fmt(ws, f"D{r}:F{r}", "0.0000" if code == "ՏԿ" else "#,##0.00")
        ws.cell(r, 7).number_format = "+0.00;-0.00"
    x.row(ws, 33, ["", "Արդյունք ստեղծող 1 աշխատողի տարեկան արդյունքի փոփոխություն", "", "x", "x", "x", "x"], bold=True, fill=x.t["band"])
    B2 = [("6", "ըստ աշխատանքային օրերի", "±ΔՏԱ′(Օ)", "=(E8-D8)*D10*D31/1000"), ("7", "ըստ օրվա տևողության", "±ΔՏԱ′(Ժ)", "=E8*(E10-D10)*D31/1000"),
          ("8", "ըստ ժամային արտադրողականության", "±ΔՏԱ′(ԺԱ)", "=E8*E10*(E31-D31)/1000")]
    for i, (n, nm, code, f) in enumerate(B2): r = 34 + i; x.row(ws, r, [n, nm, code, "x", "x", f, "x"]); ws.cell(r, 6).number_format = "+#,##0.00;-#,##0.00"
    x.row(ws, 37, ["", "Ստուգում՝ գումարը = ΔՏԱ′", "", "x", "x", "=SUM(F34:F36)", '=IF(ROUND(F37-F29,4)=0,"✔","✖")'], bold=True); ws["F37"].number_format = "+#,##0.00;-#,##0.00"
    x.row(ws, 38, ["", "Անձնակազմի միավորի միջին տարեկան արդյունքի փոփոխություն", "", "x", "x", "x", "x"], bold=True, fill=x.t["band"])
    B3 = [("9", "ըստ արդյունք ստեղծողների տեսակարար կշռի", "±ΔՏԱ(ՏԿ)", "=(E32-D32)*D8*D10*D31/1000"), ("10", "ըստ աշխատանքային օրերի", "±ΔՏԱ(Օ)", "=E32*(E8-D8)*D10*D31/1000"),
          ("11", "ըստ օրվա տևողության", "±ΔՏԱ(Ժ)", "=E32*E8*(E10-D10)*D31/1000"), ("12", "ըստ ժամային արտադրողականության", "±ΔՏԱ(ԺԱ)", "=E32*E8*E10*(E31-D31)/1000")]
    for i, (n, nm, code, f) in enumerate(B3): r = 39 + i; x.row(ws, r, [n, nm, code, "x", "x", f, "x"]); ws.cell(r, 6).number_format = "+#,##0.00;-#,##0.00"
    x.row(ws, 43, ["", "Ստուգում՝ գումարը = ΔՏԱ", "", "x", "x", "=SUM(F39:F42)", '=IF(ROUND(F43-F28,4)=0,"✔","✖")'], bold=True); ws["F43"].number_format = "+#,##0.00;-#,##0.00"
    x.verdict_cf(ws, "G37:G43")
    # extra
    x.head(ws, 46, ["№", "Լրացուցիչ (մեր կողմից)", "Նշան", "2024թ.", "2025թ.", "Փաստ.", "%-ով"])
    EX = [("Ա", "Միջին տարեկան աշխատավարձ, հազ. դր.", "ԱՖ/ԸԱ", "=D15/D6", "=E15/E6"), ("Բ", "Աշխատավարձատարություն (ԱՖ ÷ ՍԱ)", "ԱՖ/ՍԱ", "=D15/D12", "=E15/E12"),
          ("Գ", "Զուտ շահույթ 1 աշխատողի հաշվով, հազ. դր.", "ԶՇ/ԸԱ", "=D14/D6", "=E14/E6"), ("Դ", "Կապիտալի շահութաբերություն, %", "ԶՇ/Կ", "=D14/D16*100", "=E14/E16*100")]
    for i, (n, nm, code, a, b) in enumerate(EX):
        r = 47 + i; x.row(ws, r, [n, nm, code, a, b, f"=E{r}-D{r}", f"=E{r}/D{r}*100-100"]); x.fmt(ws, f"D{r}:F{r}", "0.000" if code == "ԱՖ/ՍԱ" else "#,##0.00")
        ws.cell(r, 7).number_format = "+0.00;-0.00"
    ws["I5"] = "Գործոն"; ws["J5"] = "ΔՖ, ժամ"
    for i, (n, r) in enumerate([("Թվաքանակ", 21), ("Օրեր", 22), ("Օրվա տևողություն", 23)]): ws.cell(6 + i, 9, n); ws.cell(6 + i, 10, f"=F{r}")
    ws["I11"] = "Գործոն"; ws["J11"] = "ΔՏԱ, հազ. դր."
    for i, (n, r) in enumerate([("Տեսակարար կշիռ", 39), ("Օրեր", 40), ("Օրվա տևողություն", 41), ("Ժամային արտադրող.", 42)]): ws.cell(12 + i, 9, n); ws.cell(12 + i, 10, f"=F{r}")
    for r in range(5, 17):
        for c in (9, 10): ws.cell(r, c).font = x.F(size=8, color="999999")
    x.bar(ws, Reference(ws, min_col=10, min_row=5, max_row=8), Reference(ws, min_col=9, min_row=6, max_row=8), "Աշխատաժամանակի ֆոնդի փոփոխության գործոններ", "L4", [x.t["head"]], "+#,##0;-#,##0", w=18)
    x.bar(ws, Reference(ws, min_col=10, min_row=11, max_row=15), Reference(ws, min_col=9, min_row=12, max_row=15), "ՏԱ փոփոխության գործոններ", "L21", [x.t["acc"]], "+#,##0.0;-#,##0.0", w=18)
    return ws

def summary(x, lines, name="Եզրակացություն", title="Եզրակացություններ"):
    ws = x.sheet(name, title, "Ամփոփում պարզ լեզվով", [110])
    r = 5
    for h, txt in lines:
        ws.cell(r, 1, h).font = x.F(bold=True, size=12, color=x.t["head"]); r += 1
        c = ws.cell(r, 1, txt); c.alignment = Alignment(wrap_text=True, vertical="top"); c.font = x.F(size=10); c.fill = PatternFill("solid", fgColor=x.t["band"])
        ws.row_dimensions[r].height = max(30, 15 * (len(txt) // 95 + 1)); r += 2
    return ws
