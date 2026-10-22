// S26 Whiteboard Doodle Showcase: shared builder + fit pass for head / cover / CTA / caption cards.
// Each card page holds <script id="data" type="application/json"> and <body data-card="head|cover|cta|cap">.
// render-card.mjs awaits window.cardReady (this file's fit pass) and fails (exit 2) on any [data-fit] overflow;
// a card-limit breach is listed in window.cardInfo.violations and also makes it exit 2.
(() => {
  const kind = document.body.dataset.card;
  const data = JSON.parse(document.getElementById('data').textContent);
  const violations = [];
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };
  const fit = e => { e.setAttribute('data-fit', ''); return e; };
  const words = s => s.trim().split(/\s+/).filter(Boolean).length;

  if (data.counter) document.body.append(el('div', 'counter', data.counter));
  const top = data.counter ? 34 : 0;

  // ---- one line of hand lettering; "{keyword}" becomes the orange keyword in curly quotes
  const lineEl = (text, cls) => {
    const ln = el('span', 'ln' + (cls ? ' ' + cls : ''));
    const parts = String(text).split('{keyword}');
    parts.forEach((p, i) => {
      if (p) ln.append(document.createTextNode(p));
      if (i < parts.length - 1) ln.append(el('span', 'kw', `“${data.keyword || ''}”`));
    });
    return ln;
  };

  let stack, lines, aside, keyLn, capEl;
  if (kind === 'cap') {
    capEl = fit(el('div', 'cap'));
    const paras = Array.isArray(data.caption) ? data.caption : [data.caption];
    for (const p of paras) capEl.append(el('p', null, p));
    document.body.append(capEl);
    const n = words(paras.join(' '));
    if (n > 34) violations.push(`caption has ${n} words (max 34)`);
  } else {
    stack = fit(el('div', 'stack'));
    stack.style.top = top + 'px';
    lines = el('div', 'lines');
    const src = kind === 'head' ? [data.name] : data.lines;
    src.forEach((t, i) => {
      const isKey = kind === 'head' || (kind === 'cover' && i === data.key);
      const ln = fit(lineEl(t, isKey ? 'key' : ''));
      if (isKey) keyLn = ln;
      lines.append(ln);
    });
    stack.append(lines);
    if (data.aside) { aside = fit(el('div', 'aside', data.aside)); stack.append(aside); }
    // room for the marker underline under the key line
    if (keyLn) keyLn.style.paddingBottom = '0.26em';
    document.body.append(stack);
    if (kind === 'cta' && !/\{keyword\}/.test((data.lines || []).join(' '))) violations.push('CTA needs a {keyword} line');
  }
  if (violations.length) {
    const v = fit(el('div', 'limit-violation'));
    v.append(el('i'));
    document.body.append(v);
  }

  // visual lines of an element (one rect per line box)
  const visualLines = e => {
    const r = document.createRange();
    r.selectNodeContents(e);
    const rows = [];
    for (const q of r.getClientRects()) {
      if (q.width < 1) continue;
      const row = rows.find(w => Math.abs(w.top - q.top) < 4);
      if (row) { row.left = Math.min(row.left, q.left); row.right = Math.max(row.right, q.right); row.bottom = Math.max(row.bottom, q.bottom); }
      else rows.push({ top: q.top, left: q.left, right: q.right, bottom: q.bottom });
    }
    return rows.sort((a, b) => a.top - b.top);
  };

  const drawUnderline = ln => {
    const rows = visualLines(ln);
    const last = rows[rows.length - 1];
    const w = (last.right - last.left) * 1.04;
    const x = (last.left + last.right) / 2 - w / 2;
    const rise = Math.min(14, w * 0.012);
    const y = last.bottom + 2;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'ul');
    svg.setAttribute('width', w + 12);
    svg.setAttribute('height', rise + 24);
    svg.setAttribute('viewBox', `-6 -6 ${w + 12} ${rise + 24}`);
    svg.style.left = (x - 6) + 'px';
    svg.style.top = (y - 6 - rise) + 'px';
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    // one marker stroke, rising slightly to the right, with a faint belly
    p.setAttribute('d', `M0,${rise + 6} C${w * 0.3},${rise + 4} ${w * 0.62},${rise * 0.55 + 4} ${w},${4}`);
    svg.append(p);
    document.body.append(svg);
    return { x: Math.round(x), y: Math.round(y), w: Math.round(w) };
  };

  window.cardReady = (async () => {
    await document.fonts.ready;
    const info = { card: kind };
    if (kind === 'cap') {
      const fits = px => {
        capEl.style.fontSize = px + 'px';
        const n = [...capEl.querySelectorAll('p')].reduce((s, p) => s + visualLines(p).length, 0);
        info.lines = n;
        return n <= 4 && capEl.scrollHeight <= capEl.clientHeight + 0.5 && capEl.scrollWidth <= capEl.clientWidth + 0.5;
      };
      let px = 46;
      for (; px >= 36; px -= 0.5) if (fits(px)) break;
      if (px < 36) { px = 36; fits(px); if (info.lines > 4) violations.push(`caption needs ${info.lines} lines at 36 px (max 4)`); }
      info.caption_px = px;
    } else {
      const max = 120, min = 64;
      const maxRows = 2; // a line that cannot fit at 64 px may wrap once
      const asideRatio = 0.42;
      const fits = (px, wrap) => {
        lines.style.fontSize = px + 'px';
        lines.classList.toggle('wrap', wrap);
        if (aside) aside.style.fontSize = Math.max(30, px * asideRatio) + 'px';
        const lns = [...lines.querySelectorAll('.ln')];
        if (!lns.every(l => l.scrollWidth <= l.clientWidth + 0.5 && l.scrollHeight <= l.clientHeight + 0.5)) return false;
        if (wrap && !lns.every(l => visualLines(l).length <= maxRows)) return false;
        if (aside && (aside.scrollWidth > aside.clientWidth + 0.5 || aside.scrollHeight > aside.clientHeight + 0.5)) return false;
        return stack.scrollHeight <= stack.clientHeight + 0.5;
      };
      let px = max, wrap = false, ok = false;
      for (const w of [false, true]) {
        for (px = max; px >= min; px -= 1) if (fits(px, w)) { ok = true; wrap = w; break; }
        if (ok) break;
      }
      if (!ok) { px = min; wrap = true; fits(px, true); violations.push('lettering does not fit at 64 px with at most 2 rows per line: shorten it'); }
      info.px = px;
      info.rows = [...lines.querySelectorAll('.ln')].reduce((n, l) => n + visualLines(l).length, 0);
      info.wrapped = wrap;
      if (keyLn) info.underline = drawUnderline(keyLn);
    }
    const loaded = f => [...document.fonts].some(x => x.family.replace(/"/g, '') === f && x.status === 'loaded');
    info.font = loaded('Shantell Sans') ? 'Shantell Sans' : 'fallback';
    if (violations.length) {
      info.violations = violations;
      if (!document.querySelector('.limit-violation')) {
        const v = fit(el('div', 'limit-violation'));
        v.append(el('i'));
        document.body.append(v);
      }
    }
    window.cardInfo = info;
  })();
})();
