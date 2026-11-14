L = open('hw/v2/app.js').read().split('\n')
eng = '\n'.join(L[242:417])
assert eng.startswith('/* ---- build ---- */'), eng[:40]
eng = eng.replace("  if (k==='d'||k==='D'||k==='դ'){ xmode(xmodeCur==='deck'?'dash':'deck'); return; }\n", "")
eng = eng.replace("else if (o.dataset.open==='dash') xmode('dash');", "")
helpers = '\n'.join(L[418:431]); assert helpers.startswith('const colL')
numcell = '\n'.join(L[446:457]); assert numcell.startswith('const numCell')
fxfn = '\n'.join(L[539:553]); assert fxfn.startswith('function drFx')
dl = '\n'.join(L[561:572]); assert 'XLSX_B64' in dl
pre = '\n'.join(L[585:602]); assert pre.startswith('/* preloader'), pre[:30]
dr = open('platform/deck8/dr8.js').read()
dr = dr.replace('/*__NUMCELL__*/', numcell).replace('/*__FX__*/', fxfn).replace('/*__DL__*/', dl.replace("XLSX_NAME = 'Tema7_Dramakan_mijocner_Hrachya_Aslanyan.xlsx'", "XLSX_NAME = 'Tema8-9_Debitor_Kreditor_Hrachya_Aslanyan.xlsx'")).replace('/*__PRE__*/', pre)
assert 'Tema8-9' in dr
open('platform/deck8/engine8.js','w').write(helpers + '\n' + eng + '\n' + dr)
print('ok')
