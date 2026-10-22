// S13 helpers: plate + grain + scrim + fit pass, then window.cardReady for render-card.
//
// Every page carries <script type="application/json" id="slide-data">{ "layout", "box", "plate"? }</script>.
//   layout/box are read by shared/sky-tone.mjs (box = the stack's [top, bottom] as fractions of the height);
//   plate defaults to ../fitted/<this file's name>.png. Quiet pages (body.quiet) have no plate and no tone pass.
// Scrim: sky-tone stamps data-scrim (stack), data-scrim-mast, data-scrim-nav (0/20/35/50). Black behind white
//   type, white behind ink, full strength inside the region, feathered 80 px (stack) or 60 px (strips).
// Fit: every [data-fit][data-max] steps down 2 px (floor data-min) until its box stops overflowing; what still
//   overflows makes render-card exit 2. .giant[data-fill=W] instead grows to span W px on one line (floor data-min,
//   ceiling data-max); below the floor the page throws: rewrite the word.
window.S13 = {
  data() { return JSON.parse(document.getElementById('slide-data').textContent); },
  grain() {
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'grain'); svg.setAttribute('width', '1080'); svg.setAttribute('height', '1350');
    svg.innerHTML = '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>' +
      '<feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1350" filter="url(#g)"/>';
    document.body.appendChild(svg);
    if (document.body.classList.contains('quiet')) {   // photocopy streaks: noise fast across, slow down the page
      const st = document.createElementNS(NS, 'svg');
      st.setAttribute('class', 'streaks'); st.setAttribute('width', '1080'); st.setAttribute('height', '1350');
      st.innerHTML = '<filter id="s"><feTurbulence type="fractalNoise" baseFrequency="0.06 0.0015" numOctaves="2" seed="7"/>' +
        '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.05"/></filter><rect width="1080" height="1350" filter="url(#s)"/>';
      document.body.prepend(st);
    }
  },
  scrim(top, bottom, tone, pct, feather, dir) {
    if (!+pct) return;
    const c = tone === 'white' ? `rgba(0,0,0,${pct / 100})` : `rgba(255,255,255,${pct / 100})`;
    const s = document.createElement('div');
    s.className = 'scrim';
    if (dir === 'box') {
      Object.assign(s.style, { left: '0', right: '0', top: (top - feather) + 'px', height: (bottom - top + 2 * feather) + 'px',
        background: `linear-gradient(180deg, transparent 0, ${c} ${feather}px, ${c} calc(100% - ${feather}px), transparent 100%)` });
    } else {
      Object.assign(s.style, { left: '0', right: '0', top: top + 'px', height: (bottom - top) + 'px',
        background: `linear-gradient(${dir}, ${c} 0, ${c} calc(100% - ${feather}px), transparent 100%)` });
    }
    document.body.prepend(s);
  },
  async ready() {
    const d = S13.data();
    const b = document.body, a = (k) => b.getAttribute(k) || '0';
    if (!b.classList.contains('quiet')) {
      const name = location.pathname.split('/').pop().replace(/\.html$/, '.png');
      b.style.backgroundImage = `url("${d.plate || '../fitted/' + name}")`;
      const [t, bt] = (d.box || [0.1, 0.6]).map((f) => Math.round(f * 1350));
      S13.scrim(t, bt, b.dataset.stack, a('data-scrim'), 80, 'box');
      S13.scrim(0, Math.round(0.11 * 1350), b.dataset.mast, a('data-scrim-mast'), 60, 'to bottom');
      S13.scrim(Math.round(0.89 * 1350), 1350, b.dataset.nav, a('data-scrim-nav'), 60, 'to top');
    }
    S13.grain();
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((ok) => { i.onload = ok; i.onerror = ok; })));
    const over = (el) => el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
    for (const el of document.querySelectorAll('[data-fit][data-max]')) {
      let px = +el.dataset.max;
      const min = +el.dataset.min;
      el.style.fontSize = px + 'px';
      while (over(el) && px > min) { px -= 2; el.style.fontSize = px + 'px'; }
    }
    // .giant[data-fill]: grow (to data-max) until the word spans data-fill px, one line, never past it.
    for (const el of document.querySelectorAll('.giant[data-fill]')) {
      const target = +el.dataset.fill;
      let lo = +el.dataset.min, hi = +el.dataset.max;
      el.style.height = 'auto'; el.style.display = 'inline-block';
      while (hi - lo > 1) { const mid = (lo + hi) / 2; el.style.fontSize = mid + 'px'; if (el.scrollWidth <= target) lo = mid; else hi = mid; }
      el.style.fontSize = Math.floor(lo) + 'px';
      if (el.scrollWidth > target + 1) throw new Error('giant word does not fit at ' + Math.floor(lo) + 'px: rewrite it');
      el.style.display = 'block';
      // a descender (g j p q y) would hit the trailing line: drop the line below it
      const trail = el.nextElementSibling;
      if (trail && /[gjpqy]/.test(el.textContent)) trail.style.marginTop = Math.round(0.14 * Math.floor(lo)) + 'px';
    }
    window.cardInfo = { layout: d.layout, box: d.box, tone: { mast: b.dataset.mast, stack: b.dataset.stack, nav: b.dataset.nav, scrim: a('data-scrim') } };
  },
};
// A failure never hangs the render: it is reported in cardInfo and the page is made to overflow (render-card exit 2).
window.cardReady = new Promise((ok) => window.addEventListener('DOMContentLoaded', () => S13.ready().catch((e) => {
  window.cardInfo = { error: String(e.message || e) };
  document.documentElement.style.overflow = 'visible'; document.body.style.overflow = 'visible'; document.body.style.height = '1500px';
}).then(ok)));
