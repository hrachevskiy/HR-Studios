/* H/R Studios extras: search (Ctrl+K), themes, glossary tooltips, read/done progress, calculators, quizzes, explainers, 3D carousel */
(function () {
  'use strict';
  const S = document.currentScript, BASE = (S && S.dataset.base) || '', D = window.HRD || {};
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  const LS = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (v, d) => { if (!isFinite(v)) return '—'; const s = Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); return (v < 0 ? '−' : '') + s; };

  /* ---------- header tools ---------- */
  const THEMES = [['dark', '☾', 'Մուգ'], ['light', '☀', 'Լուսավոր'], ['proj', '📽', 'Պրոյեկտոր']];
  const host = $('.hdr .wrap') || $('.topbar');
  if (host) {
    const t = document.createElement('div'); t.className = 'hrtools';
    const own = host.classList.contains('topbar'); if (own) delete document.documentElement.dataset.theme;
    t.innerHTML = '<button class="ksb" aria-label="Որոնում">🔍 <span class="lbl">Որոնում</span> <kbd>Ctrl K</kbd></button>' + (own ? '' : '<button class="thb" aria-label="Թեմա"></button>');
    const burger = $('.burger', host); burger ? host.insertBefore(t, burger) : host.appendChild(t);
    const thb = $('.thb', t) || document.createElement('button');
    const curT = () => document.documentElement.dataset.theme || 'dark';
    const paint = () => { const x = THEMES.find(z => z[0] === curT()) || THEMES[0]; thb.innerHTML = x[1] + ' <span class="lbl">' + x[2] + '</span>'; };
    thb.onclick = () => { const i = THEMES.findIndex(z => z[0] === curT()); const nx = THEMES[(i + 1) % THEMES.length][0];
      if (nx === 'dark') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = nx; try { if (nx === 'dark') localStorage.removeItem('hr-theme'); else localStorage.setItem('hr-theme', nx); } catch (e) {} paint(); };
    paint(); $('.ksb', t).onclick = () => openK();
    const pb = document.createElement('div'); pb.className = 'projbadge'; pb.textContent = '📽 Պրոյեկտորի ռեժիմ'; document.body.appendChild(pb);
  }

  /* ---------- search palette ---------- */
  let K = null, kSel = 0, kItems = [];
  function buildIndex() {
    const it = [];
    (D.lessons || []).forEach(L => {
      it.push({ g: 'Դասեր', i: '📘', t: 'Դաս ' + L.n + ' · ' + L.t, s: L.idea, h: BASE + L.slug + '.html' });
      it.push({ g: 'Գործիքներ', i: '🧮', t: 'Հաշվիչ · Դաս ' + L.n, s: L.short, h: BASE + L.slug + '.html#calc' });
      it.push({ g: 'Գործիքներ', i: '📝', t: 'Թեստ և քարտեր · Դաս ' + L.n, s: L.short, h: BASE + L.slug + '.html#quiz' });
      it.push({ g: 'Գործիքներ', i: '🎬', t: 'Անիմացիոն բացատրություն · Դաս ' + L.n, s: L.short, h: BASE + L.slug + '.html#explain' });
    });
    (D.quiz || []).forEach(q => { const L = (D.lessons || []).find(x => x.n === q.n) || {};
      q.f.forEach(f => it.push({ g: 'Բանաձևեր', i: 'ƒ', t: f[0] + ' · ' + f[1], s: f[2] + ' — Դաս ' + q.n, h: BASE + L.slug + '.html#formulas' }));
      q.g.forEach(g => it.push({ g: 'Բառարան', i: '📖', t: g[0], s: g[1] + ' — Դաս ' + q.n, h: BASE + L.slug + '.html#glossary' })); });
    (D.works || []).forEach(w => it.push({ g: 'Իմ աշխատանքները', i: '🎨', t: w[1] + ' · ' + w[3], s: w[0], h: BASE + w[2] }));
    (D.files || []).forEach(f => it.push({ g: 'Ֆայլեր', i: '📄', t: f[0], s: f[2], h: BASE + f[1] }));
    it.push({ g: 'Էջեր', i: '∑', t: 'Բանաձևերի շպարգալկա', s: 'բոլոր բանաձևերը մեկ էջում · տպել A4', h: BASE + 'formulas.html' });
    it.push({ g: 'Էջեր', i: '🎨', t: 'Իմ աշխատանքները', s: 'ժամանակագրություն և բոլոր լուծումները', h: BASE + 'works.html' });
    it.push({ g: 'Էջեր', i: '🗂', t: 'Նյութերի գրադարան', s: 'դասախոսի ֆայլերը ըստ դասերի', h: BASE + 'index.html#library' });
    return it;
  }
  function openK() {
    if (!K) {
      K = document.createElement('div'); K.className = 'kpal';
      K.innerHTML = '<div class="kbox" role="dialog" aria-label="Որոնում"><input placeholder="Որոնել դասեր, բանաձևեր, տերմիններ, ֆայլեր…" autocomplete="off"><div class="kres"></div><div class="kfoot">↑↓ ընտրել · Enter՝ բացել · Esc՝ փակել</div></div>';
      document.body.appendChild(K); K.addEventListener('click', e => { if (e.target === K) closeK(); });
      K._idx = buildIndex(); const inp = $('input', K); inp.addEventListener('input', () => renderK(inp.value));
      inp.addEventListener('keydown', e => { if (e.key === 'ArrowDown') { kSel = Math.min(kSel + 1, kItems.length - 1); paintSel(); e.preventDefault(); }
        if (e.key === 'ArrowUp') { kSel = Math.max(kSel - 1, 0); paintSel(); e.preventDefault(); } if (e.key === 'Enter' && kItems[kSel]) location.href = kItems[kSel].h; if (e.key === 'Escape') closeK(); });
    }
    K.classList.add('on'); const inp = $('input', K); inp.value = ''; renderK(''); setTimeout(() => inp.focus(), 30);
  }
  function closeK() { K && K.classList.remove('on'); }
  function renderK(q) {
    const toks = q.trim().toLowerCase().split(/\s+/).filter(Boolean), box = $('.kres', K);
    let res = K._idx.filter(x => { const h = (x.t + ' ' + x.s).toLowerCase(); return toks.every(t => h.includes(t)); });
    if (!toks.length) res = res.filter(x => x.g === 'Դասեր' || x.g === 'Էջեր');
    kItems = res.slice(0, 60); kSel = 0;
    if (!kItems.length) { box.innerHTML = '<div class="kempty">Ոչինչ չի գտնվել 🙈</div>'; return; }
    const hl = s => { let o = esc(s); toks.forEach(t => { o = o.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>'); }); return o; };
    let g = '', html = ''; kItems.forEach((x, i) => { if (x.g !== g) { g = x.g; html += '<div class="kg">' + esc(g) + '</div>'; }
      html += '<a href="' + esc(x.h) + '" data-i="' + i + '"><span class="ki">' + x.i + '</span><span><b>' + hl(x.t) + '</b><small>' + hl(String(x.s).slice(0, 110)) + '</small></span></a>'; });
    box.innerHTML = html; paintSel(); $$('a', box).forEach(a => a.addEventListener('mousemove', () => { kSel = +a.dataset.i; paintSel(); }));
  }
  function paintSel() { $$('.kres a', K).forEach(a => a.classList.toggle('on', +a.dataset.i === kSel)); const a = $('.kres a.on', K); a && a.scrollIntoView({ block: 'nearest' }); }
  addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openK(); }
    else if (e.key === '/' && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); openK(); } else if (e.key === 'Escape') closeK(); });

  /* ---------- glossary tooltips ---------- */
  function tips() {
    const T = D.tips || {}, keys = Object.keys(T).sort((a, b) => b.length - a.length); if (!keys.length) return;
    let re; try { re = new RegExp('(?<![\\p{L}\\p{N}])(' + keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')(?![\\p{L}\\p{N}])', 'gu'); } catch (e) { return; }
    const skip = /^(SCRIPT|STYLE|SVG|TEXT|BUTTON|INPUT|TEXTAREA|SELECT|ABBR|TITLE|NOSCRIPT|IFRAME|A|H1)$/;
    const bad = el => { for (let p = el; p && p !== document.body; p = p.parentElement) { if (skip.test(p.tagName.toUpperCase()) || p.matches('.hdr,.topbar,.kpal,.nav,.lnav,.wpanel,.cur,.hero,.hero2,.exp,.qz,.calc,.ring-wrap,.c3d,.tipbox,svg')) return true; } return false; };
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.nodeValue.trim().length > 1 && !bad(n.parentElement) ? 1 : 2 });
    const nodes = []; while (tw.nextNode()) nodes.push(tw.currentNode);
    let count = 0;
    for (const n of nodes) { if (count > 900) break; const v = n.nodeValue; re.lastIndex = 0; if (!re.test(v)) continue; re.lastIndex = 0;
      const f = document.createDocumentFragment(); let last = 0, m;
      while ((m = re.exec(v))) { f.appendChild(document.createTextNode(v.slice(last, m.index))); const a = document.createElement('abbr'); a.className = 'tip'; a.dataset.k = m[1]; a.textContent = m[1]; f.appendChild(a); last = m.index + m[1].length; count++; }
      f.appendChild(document.createTextNode(v.slice(last))); n.parentNode.replaceChild(f, n); }
    const box = document.createElement('div'); box.className = 'tipbox'; document.body.appendChild(box);
    const show = a => { box.innerHTML = '<b>' + esc(a.dataset.k) + '</b>' + esc(T[a.dataset.k] || ''); const r = a.getBoundingClientRect(); box.classList.add('on');
      const w = box.offsetWidth, h = box.offsetHeight; box.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + 'px'; box.style.top = (r.top - h - 8 < 4 ? r.bottom + 8 : r.top - h - 8) + 'px'; };
    document.addEventListener('mouseover', e => { const a = e.target.closest && e.target.closest('abbr.tip'); if (a) show(a); });
    document.addEventListener('mouseout', e => { if (e.target.closest && e.target.closest('abbr.tip')) box.classList.remove('on'); });
    document.addEventListener('click', e => { const a = e.target.closest && e.target.closest('abbr.tip'); if (a) { show(a); setTimeout(() => box.classList.remove('on'), 2600); } });
    addEventListener('scroll', () => box.classList.remove('on'), { passive: true });
  }
  (window.requestIdleCallback || (f => setTimeout(f, 300)))(tips);

  /* ---------- read / done progress ---------- */
  const done = () => LS.get('hr-done', {});
  function paintDone() {
    const d = done(), nTot = (D.lessons || []).length, nDone = Object.keys(d).filter(k => d[k]).length;
    $$('[data-done]').forEach(b => { const on = !!d[b.dataset.done]; b.classList.toggle('on', on); $('.tx', b).textContent = on ? 'Կարդացած է ✓ (սեղմեք՝ չեղարկելու համար)' : 'Նշել որպես կարդացած'; });
    $$('a.lc').forEach(a => { const m = (a.getAttribute('href') || '').match(/lesson-(\d+)/); if (!m) return; if (!$('.dmark', a)) { const s = document.createElement('span'); s.className = 'dmark'; s.textContent = '✓'; a.appendChild(s); } a.classList.toggle('isdone', !!d[m[1]]); });
    $$('a.c3d').forEach(a => { const m = (a.getAttribute('href') || '').match(/lesson-(\d+)/); m && a.classList.toggle('isdone', !!d[m[1]]); });
    $$('[data-prog-n]').forEach(e => e.textContent = nDone); $$('[data-prog-bar]').forEach(e => setTimeout(() => e.style.width = (nDone / nTot * 100) + '%', 200));
    const qs = LS.get('hr-quiz', {}), vals = Object.values(qs); $$('[data-quiz-avg]').forEach(e => e.textContent = vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) + '%' : '—');
  }
  $$('[data-done]').forEach(b => b.addEventListener('click', () => { const d = done(); d[b.dataset.done] = !d[b.dataset.done]; LS.set('hr-done', d); paintDone(); }));
  paintDone();

  /* ---------- calculators ---------- */
  $$('[data-calc]').forEach(box => {
    const C = (D.calc || {})[box.dataset.calc]; if (!C) return; const keys = C.i.map(x => x[0]);
    const fns = C.o.map(o => { try { return new Function(...keys, 'return (' + o[1] + ');'); } catch (e) { return () => NaN; } });
    const res = $('.cres', box), conc = $('.cconc', box), ins = $$('input', box);
    res.innerHTML = C.o.map((o, i) => '<div class="cr" data-i="' + i + '"><span>' + esc(o[0]) + '</span><b>—</b><span class="st na">—</span></div>').join('');
    let prev = [];
    function run() {
      const v = keys.map(k => parseFloat((ins.find(x => x.dataset.k === k) || {}).value) || 0); let ok = 0, bad = 0, badN = [], okN = [];
      C.o.forEach((o, i) => { let r = NaN; try { r = fns[i](...v); } catch (e) {} const row = $('[data-i="' + i + '"]', res), lo = o[3], hi = o[4];
        const b = $('b', row), st = $('.st', row), txt = fmt(r, o[2]); if (b.textContent !== txt) { b.textContent = txt; row.classList.remove('flash'); void row.offsetWidth; row.classList.add('flash'); }
        if ((lo == null && hi == null) || !isFinite(r)) { st.className = 'st na'; st.textContent = lo == null && hi == null ? 'տեղեկատվական' : '—'; return; }
        const good = (lo == null || r >= lo) && (hi == null || r <= hi); st.className = 'st ' + (good ? 'ok' : 'no');
        st.textContent = (good ? '✔ ' : '✖ ') + (lo != null && hi != null ? lo + '–' + hi : lo != null ? '≥ ' + lo : '≤ ' + hi); good ? (ok++, okN.push(o[0].split(' · ')[0])) : (bad++, badN.push(o[0].split(' · ')[0])); });
      const tot = ok + bad;
      conc.innerHTML = '<b>Եզրակացություն.</b> ' + (tot ? ('Նորմայով ստուգվող ' + tot + ' ցուցանիշից ' + ok + '-ը նորմայում է' + (bad ? ', ' + bad + '-ը՝ ոչ (' + badN.join(', ') + ')։ Ուշադրություն դարձրեք այս ցուցանիշներին. ' + (bad > tot / 2 ? 'իրավիճակը մտահոգիչ է։' : 'մնացած պատկերը բավարար է։') : '։ Իրավիճակը բարենպաստ է։')) : 'Ցուցանիշները հաշվարկված են. համեմատեք դրանք նախորդ տարվա հետ՝ փոփոխության ուղղությունը գնահատելու համար։');
    }
    ins.forEach(x => x.addEventListener('input', run));
    $('[data-reset]', box).onclick = () => { C.i.forEach(([k, , d]) => { const x = ins.find(y => y.dataset.k === k); if (x) x.value = d; }); run(); };
    $('[data-copy]', box).onclick = e => { const t = $$('.cr', res).map(r => $('span', r).textContent + ' = ' + $('b', r).textContent + ' (' + $('.st', r).textContent + ')').join('\n') + '\n' + conc.textContent;
      navigator.clipboard && navigator.clipboard.writeText(t); e.target.textContent = '✓ Պատճենված է'; setTimeout(() => e.target.textContent = '⧉ Պատճենել եզրակացությունը', 1500); };
    run();
  });

  /* ---------- quiz + flashcards ---------- */
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  $$('[data-quiz]').forEach(box => {
    const n = +box.dataset.quiz, Q = (D.quiz || []).find(x => x.n === n); if (!Q) return; const all = D.quiz;
    const allF = all.flatMap(x => x.f), allG = all.flatMap(x => x.g), body = $('.qbody', box), best = $('.qbest', box);
    const paintBest = () => { const b = LS.get('hr-quiz', {})[n]; best.textContent = b != null ? '🏆 Լավագույն արդյունք՝ ' + b + '%' : ''; }; paintBest();
    function makeQs() {
      const qs = [];
      Q.f.forEach(f => {
        const wrongN = shuffle(allF.filter(x => x[1] !== f[1])).slice(0, 3).map(x => x[1]);
        qs.push({ q: 'Ի՞նչ է ցույց տալիս «' + f[0] + '» ցուցանիշը (' + f[2] + ')։', a: f[1], o: shuffle([f[1], ...wrongN]), e: f[3] });
        if (f[2].length > 3) { const wrongF = shuffle(allF.filter(x => x[2] !== f[2] && x[2].length > 3)).slice(0, 3).map(x => x[2]);
          qs.push({ q: 'Ո՞րն է «' + f[1] + '»-ի բանաձևը։', a: f[2], o: shuffle([f[2], ...wrongF]), e: f[3], mono: 1 }); }
      });
      Q.g.forEach(g => { const wrong = shuffle(allG.filter(x => x[1] !== g[1])).slice(0, 3).map(x => x[1]); qs.push({ q: 'Ի՞նչ է նշանակում «' + g[0] + '»-ը։', a: g[1], o: shuffle([g[1], ...wrong]) }); });
      return shuffle(qs).slice(0, 8);
    }
    let qs = [], k = 0, score = 0;
    function test() { qs = makeQs(); k = 0; score = 0; step(); }
    function step() {
      if (k >= qs.length) { const p = Math.round(score / qs.length * 100), r = LS.get('hr-quiz', {}); if (r[n] == null || p > r[n]) { r[n] = p; LS.set('hr-quiz', r); } paintBest(); paintDone();
        body.innerHTML = '<div class="qfin qq"><div class="sc2">' + p + '%</div><p>' + score + ' ճիշտ պատասխան ' + qs.length + '-ից · ' + (p >= 85 ? 'Գերազանց է 🔥' : p >= 60 ? 'Լավ է, բայց կարելի է ավելի լավ 💪' : 'Կրկնիր դասը և փորձիր նորից 📘') + '</p><button class="btn">↻ Նորից</button></div>';
        $('button', body).onclick = test; return; }
      const q = qs[k];
      body.innerHTML = '<div class="qq"><div class="qhead"><span>Հարց ' + (k + 1) + ' / ' + qs.length + '</span><span>✔ ' + score + '</span></div><div class="qpb"><i style="width:' + (k / qs.length * 100) + '%"></i></div><h3>' + esc(q.q) + '</h3><div class="qopts">' +
        q.o.map(o => '<button' + (q.mono ? ' style="font-family:IBM Plex Mono,monospace"' : '') + '>' + esc(o) + '</button>').join('') + '</div><div class="qexp"></div></div>';
      $$('.qopts button', body).forEach(b => b.onclick = () => { const ok = b.textContent === q.a; if (ok) score++; $('.qopts', body).classList.add('done');
        $$('.qopts button', body).forEach(x => { if (x.textContent === q.a) x.classList.add('ok'); }); if (!ok) b.classList.add('no');
        $('.qexp', body).innerHTML = (ok ? '✅ Ճիշտ է։ ' : '❌ Ճիշտ պատասխանը՝ <b>' + esc(q.a) + '</b>։ ') + (q.e ? esc(q.e) : '') + '<div class="qnext"><button class="btn">' + (k + 1 < qs.length ? 'Հաջորդը →' : 'Արդյունքը') + '</button></div>';
        $('.qnext button', body).onclick = () => { k++; step(); }; });
    }
    function cards() {
      const cs = [...Q.f.map(f => ({ a: f[0], s: f[1], b: '<b>' + esc(f[1]) + '</b><code>' + esc(f[2]) + '</code>' })), ...Q.g.map(g => ({ a: g[0], s: 'տերմին', b: esc(g[1]) }))];
      body.innerHTML = '<p style="opacity:.7;margin:0 0 12px">Սեղմեք քարտի վրա՝ այն շրջելու համար։</p><div class="cards">' + cs.map(c => '<div class="fc3"><div class="in2"><div class="fa"><b>' + esc(c.a) + '</b><small>' + esc(c.s) + '</small></div><div class="fb">' + c.b + '</div></div></div>').join('') + '</div>';
      $$('.fc3', body).forEach(c => c.onclick = () => c.classList.toggle('fl'));
    }
    $$('[data-qm]', box).forEach(b => b.onclick = () => { $$('[data-qm]', box).forEach(x => x.classList.toggle('on', x === b)); b.dataset.qm === 'test' ? test() : cards(); });
    test();
  });

  /* ---------- animated explainer ---------- */
  $$('[data-exp]').forEach(ex => {
    const sc = $$('.sc', ex), bars = $$('.exprog b', ex), pl = $('.expl', ex), DUR = 4300; let k = 0, t0 = 0, el = 0, playing = false, raf = 0, started = false;
    const show = i => { k = i; sc.forEach((s, j) => s.classList.toggle('on', j === i)); bars.forEach((b, j) => b.style.width = j < i ? '100%' : '0'); el = 0; t0 = performance.now(); };
    function loop(t) { if (!playing) return; el = t - t0; bars[k].style.width = Math.min(100, el / DUR * 100) + '%';
      if (el >= DUR) { if (k < sc.length - 1) show(k + 1); else { playing = false; pl.textContent = '▶'; return; } } raf = requestAnimationFrame(loop); }
    const play = () => { if (playing) return; playing = true; pl.textContent = '❚❚'; t0 = performance.now() - el; raf = requestAnimationFrame(loop); };
    const pause = () => { playing = false; pl.textContent = '▶'; cancelAnimationFrame(raf); };
    pl.onclick = () => { if (!playing && k === sc.length - 1 && el >= DUR) { show(0); } playing ? pause() : play(); };
    $('.exrp', ex).onclick = () => { show(0); pause(); play(); };
    $$('.exprog i', ex).forEach((seg, i) => { seg.style.cursor = 'pointer'; seg.onclick = () => { show(i); pause(); play(); }; });
    new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && !started) { started = true; show(0); play(); } else if (!e.isIntersecting && playing) pause(); }), { threshold: .45 }).observe(ex);
    pl.textContent = '▶';
  });

  /* ---------- 3D carousel ---------- */
  $$('[data-ring]').forEach(w => {
    const ring = $('.ring', w), n = $$('.c3d', ring).length, step = 360 / n; let ang = 0, drag = null, moved = 0, auto;
    const set = (smooth = true) => { ring.style.transition = smooth ? '' : 'none'; ring.style.transform = 'rotateY(' + ang + 'deg)'; };
    const go = d => { ang -= d * step; ang = Math.round(ang / step) * step; set(); };
    $('.pv', w).onclick = () => { go(-1); reset(); }; $('.nx', w).onclick = () => { go(1); reset(); };
    const startAuto = () => { if (matchMedia('(prefers-reduced-motion:reduce)').matches) return; auto = setInterval(() => go(1), 3600); };
    const reset = () => { clearInterval(auto); startAuto(); };
    w.addEventListener('pointerdown', e => { drag = e.clientX; moved = 0; clearInterval(auto); });
    addEventListener('pointermove', e => { if (drag == null) return; const dx = e.clientX - drag; drag = e.clientX; moved += Math.abs(dx); ang += dx * .35; set(false); });
    addEventListener('pointerup', () => { if (drag == null) return; drag = null; ang = Math.round(ang / step) * step; set(); startAuto(); });
    $$('.c3d', ring).forEach(a => a.addEventListener('click', e => { if (moved > 8) e.preventDefault(); }));
    w.addEventListener('mouseenter', () => clearInterval(auto)); w.addEventListener('mouseleave', reset);
    set(); startAuto();
  });
})();
