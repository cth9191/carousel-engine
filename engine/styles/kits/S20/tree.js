// S20 Slate Family Tree: builds a tree card from the page's <script id="data" type="application/json">.
// Data: { "variant": "family"|"proof"|"mix"|"cta", "definition": "...", "children": [
//          { "name": "Block deletes", "start": true, "chips": ["Before any tool", "`rm -rf build/`"] } ] }
// A chip wrapped in backticks is a code token (JetBrains Mono, exact case); every other chip is Inter Italic.
// Fit pass (window.cardReady): all names share one size, 44 px down to 38 px in 0.5 px steps, so they keep
// one baseline; chips likewise share one size, 30 px down to 26 px. The card's limits (prompt block, "Card kit") are checked; a breach is listed in
// window.cardInfo.violations and makes render-card exit 2.
(() => {
  const LIMITS = {
    names: { 2: 13, 3: 13, 4: 9, 5: 7 },
    chips: { 2: 15, 3: 15, 4: 11, 5: 9 },
    maxChips: { family: 4, proof: 2, mix: 3, cta: 2 },
    children: { family: [3, 5], proof: [3, 5], mix: [2, 3], cta: [3, 3] },
  };
  const data = JSON.parse(document.getElementById('data').textContent);
  const variant = data.variant || 'family';
  const kids = data.children || [];
  const n = kids.length;
  const violations = [];
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };

  // ---- limits
  const [cmin, cmax] = LIMITS.children[variant] || [2, 5];
  if (n < cmin || n > cmax) violations.push(`${variant} takes ${cmin}-${cmax} children, got ${n}`);
  const nameMax = LIMITS.names[n] ?? 7, chipMax = LIMITS.chips[n] ?? 9;
  let codeCount = 0, startCount = 0;
  if (variant !== 'cta') {
    const words = (data.definition || '').trim().split(/\s+/).filter(Boolean).length;
    if (!words) violations.push('definition missing');
    if (words > 12) violations.push(`definition has ${words} words (max 12)`);
  }
  kids.forEach((k, i) => {
    if ([...k.name].length > nameMax) violations.push(`child ${i + 1} name "${k.name}" > ${nameMax} chars`);
    const chips = k.chips || [];
    if (chips.length > LIMITS.maxChips[variant]) violations.push(`child ${i + 1} has ${chips.length} chips (max ${LIMITS.maxChips[variant]} on ${variant})`);
    let code = 0;
    for (const c of chips) {
      const isCode = /^`.*`$/.test(c);
      const t = isCode ? c.slice(1, -1) : c;
      const max = isCode ? chipMax - 2 : chipMax;
      if ([...t].length > max) violations.push(`child ${i + 1} chip "${t}" > ${max} chars`);
      if (isCode) code++;
    }
    if (code > 1) violations.push(`child ${i + 1} has ${code} code tokens (max 1)`);
    codeCount += code;
    if (k.start) startCount++;
  });
  if (codeCount > 2) violations.push(`${codeCount} code tokens on the card (max 2)`);
  if (startCount > 1) violations.push(`${startCount} START HERE tags (max 1)`);
  if (startCount && n >= 5) violations.push('no START HERE with 5 children');

  // ---- build
  const card = el('div', `card ${variant}`);
  card.setAttribute('data-fit', '');
  if (variant !== 'cta') {
    const def = el('div', 'def');
    def.setAttribute('data-fit', '');
    def.append(el('span', null, data.definition || ''));
    card.append(def);
  }
  card.append(el('div', 'rule'));
  const cols = el('div', 'cols');
  const names = [];
  for (const k of kids) {
    const col = el('div', 'col');
    const drop = el('div', 'drop');
    if (k.start) {
      drop.append(el('div', 'stub'), el('div', 'start', 'Start here'));
    } else {
      drop.append(el('div', 'line'));
      drop.insertAdjacentHTML('beforeend',
        '<svg viewBox="0 0 14 8"><polyline points="1,1 7,7 13,1" fill="none" stroke="rgba(245,235,224,0.75)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>');
    }
    const name = el('div', 'name', k.name);
    name.setAttribute('data-fit', '');
    names.push(name);
    const chips = el('div', 'chips');
    chips.setAttribute('data-fit', '');
    for (const c of k.chips || []) {
      const isCode = /^`.*`$/.test(c);
      chips.append(el('div', isCode ? 'chip code' : 'chip', isCode ? c.slice(1, -1) : c));
    }
    col.append(drop, name, el('div', 'plus', '+'), chips);
    cols.append(col);
  }
  card.append(cols);
  document.body.append(card);
  if (violations.length) {
    const v = el('div', 'limit-violation');
    v.setAttribute('data-fit', '');
    v.append(el('i'));
    document.body.append(v);
  }

  window.cardReady = (async () => {
    await document.fonts.ready;
    const fits = () => names.every(e => e.scrollWidth <= e.clientWidth + 0.5);
    let px = 44;
    for (; px >= 38; px -= 0.5) {
      names.forEach(e => { e.style.fontSize = px + 'px'; });
      if (fits()) break;
    }
    px = Math.max(px, 38);
    // Chips share one size too: 30 px, stepping down to 26 px only when a chip is wider than its column
    // (a 9-character Inter Italic chip runs 185-191 px against the 181 px column of a 5-child tree).
    const chipEls = [...document.querySelectorAll('.chip')];
    const stacks = [...document.querySelectorAll('.chips')];
    const chipsFit = () => stacks.every(e => e.scrollWidth <= e.clientWidth + 0.5);
    let cpx = 30;
    for (; cpx >= 26; cpx -= 0.5) {
      chipEls.forEach(e => { e.style.fontSize = cpx + 'px'; e.style.lineHeight = cpx + 'px'; });
      if (chipsFit()) break;
    }
    cpx = Math.max(cpx, 26);
    const loaded = f => [...document.fonts].some(x => x.family.replace(/"/g, '') === f && x.status === 'loaded');
    window.cardInfo = {
      variant, children: n, name_px: px, chip_px: cpx,
      fonts: { inter: loaded('Inter'), mono: loaded('JetBrains Mono') },
      violations: violations.length ? violations : undefined,
    };
  })();
})();
