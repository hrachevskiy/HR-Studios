import base64, os
SP = '/tmp/claude-0/-home-claude/1b9ee954-a10c-534a-9dd9-c7dff3e4538d/scratchpad'
os.chdir(SP)
exec(open('platform/deck8/mk_engine.py').read())
T = open('hw/template.html').read()
head = T[:T.index('<style>')].replace('<title>Դրամական հոսքերի վերլուծություն</title>', '<title>Դաս 8 · Դեբիտորական և կրեդիտորական պարտքեր</title>')
css1 = T[T.index('<style>')+7:T.index('</style>')]
css2 = open('hw/v2/v2.css').read() + open('platform/deck8/deck8.css').read()
html = open('platform/deck8/app8.html').read()
xl = open('platform/deck8/xl8.json').read()
b64 = base64.b64encode(open('t8/x/main8.xlsx','rb').read()).decode()
js = open('platform/deck8/slides8.js').read().replace('/*__XL__*/', xl) + '\n' + open('platform/deck8/engine8.js').read().replace('/*__XLSX__*/', b64)
doc = ('<!doctype html>\n<html lang="hy">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '<style>' + css1 + '</style>\n<style>' + css2 + '</style>\n</head>\n<body>\n' + html + '\n<script>\n' + js + '\n</script>\n</body>\n</html>\n')
os.makedirs('platform/site/t8', exist_ok=True)
open('platform/site/t8/index.html','w').write(doc)
print(len(doc))
