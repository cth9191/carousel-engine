// S14 helpers: plate + tone scrims + pose placement + list checks + fit pass, then window.cardReady.
//
// Every page carries <script type="application/json" id="slide-data">{ "layout", "box", "plate"? }</script>.
//   layout/box feed shared/sky-tone.mjs (box = the headline stack's [top, bottom] as fractions of the height);
//   plate defaults to ../fitted/<this file's name>.png.
// Scrims: from sky-tone's data-scrim / data-scrim-mast / data-scrim-nav (0/20/35/50), black behind cream type,
//   white behind ink, feathered 80 px (stack) or 60 px (strips).
// Pose (optional): your own mascot, if you have one (never a licensed character), as
//   <img class="pose" src="../mascot/x.png" data-x data-feet data-w data-feet-y>: it stands its feet on the plate's
//   clear spot (feet-y = lowest foot pixel / height; pose-check.py check prints it) over a soft painted-ground shadow.
//   No mascot: leave it out; the plate's painted object holds the spot.
// List: at most 6 .item rows, each with a name, one what-it-does line and a proof figure (spine C's item contract).
// Fit: every [data-fit][data-max] steps down 2 px (floor data-min) until it stops overflowing; a failure (overflow,
//   list rule, missing image) never hangs the render: it lands in cardInfo and the page overflows (render-card exit 2).
window.S14 = {
  data() { return JSON.parse(document.getElementById('slide-data').textContent); },
  scrim(top, bottom, tone, pct, feather, dir) {
    if (!+pct) return;
    const c = tone === 'white' ? `rgba(20,14,8,${pct / 100})` : `rgba(255,250,240,${pct / 100})`;
    const s = document.createElement('div');
    s.className = 'scrim';
    const bg = dir === 'box'
      ? `linear-gradient(180deg, transparent 0, ${c} ${feather}px, ${c} calc(100% - ${feather}px), transparent 100%)`
      : `linear-gradient(${dir}, ${c} 0, ${c} calc(100% - ${feather}px), transparent 100%)`;
    Object.assign(s.style, { left: '0', right: '0', top: (dir === 'box' ? top - feather : top) + 'px',
      height: (bottom - top + (dir === 'box' ? 2 * feather : 0)) + 'px', background: bg });
    document.body.prepend(s);
  },
  async place(img) {
    if (!img.complete || !img.naturalWidth) await new Promise((ok, bad) => { img.onload = ok; img.onerror = () => bad(new Error('missing ' + img.getAttribute('src'))); if (img.complete && img.naturalWidth) ok(); });
    const x = +img.dataset.x, w = +img.dataset.w, feet = +img.dataset.feet;
    const fy = img.dataset.feetY ? +img.dataset.feetY : 0.99;
    const h = w * img.naturalHeight / img.naturalWidth;
    Object.assign(img.style, { left: x + 'px', top: (feet - h * fy) + 'px', width: w + 'px', height: h + 'px' });
    const s = document.createElement('div');
    s.className = 'shadow';
    const sw = w * 0.95, sh = Math.max(20, w * 0.09);
    Object.assign(s.style, { left: (x + (w - sw) / 2) + 'px', top: (feet - sh * 0.55) + 'px', width: sw + 'px', height: sh + 'px' });
    img.before(s);
  },
  async ready() {
    const d = S14.data();
    const b = document.body, a = (k) => b.getAttribute(k) || '0';
    const name = location.pathname.split('/').pop().replace(/\.html$/, '.png');
    b.style.backgroundImage = `url("${d.plate || '../fitted/' + name}")`;
    const [t, bt] = (d.box || [0.07, 0.30]).map((f) => Math.round(f * 1350));
    S14.scrim(t, bt, b.dataset.stack, a('data-scrim'), 80, 'box');
    S14.scrim(0, Math.round(0.11 * 1350), b.dataset.mast, a('data-scrim-mast'), 60, 'to bottom');
    S14.scrim(Math.round(0.89 * 1350), 1350, b.dataset.nav, a('data-scrim-nav'), 60, 'to top');
    await document.fonts.ready;
    await Promise.all([...document.querySelectorAll('img.pose')].map(S14.place));
    const over = (el) => el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
    for (const el of document.querySelectorAll('[data-fit][data-max]')) {
      let px = +el.dataset.max;
      const min = +el.dataset.min;
      el.style.fontSize = px + 'px';
      while (over(el) && px > min) { px -= 2; el.style.fontSize = px + 'px'; }
    }
    const problems = [];
    for (const list of document.querySelectorAll('.list')) {
      const items = list.querySelectorAll('.item');
      if (items.length > 6) problems.push(`list has ${items.length} rows (6 at most)`);
      items.forEach((it, i) => {
        if (!it.querySelector('.wh')?.textContent.trim()) problems.push(`row ${i + 1} has no what-it-does line`);
        if (!it.querySelector('.pf')?.textContent.trim()) problems.push(`row ${i + 1} has no proof figure`);
        const nm = it.querySelector('.nm');
        if (nm && nm.scrollWidth > nm.clientWidth + 1) problems.push(`row ${i + 1} name is cut off: ${nm.textContent}`);
      });
    }
    window.cardInfo = { layout: d.layout, tone: { mast: b.dataset.mast, stack: b.dataset.stack, nav: b.dataset.nav, scrim: a('data-scrim') }, problems };
    if (problems.length) throw new Error(problems.join('; '));
  },
};
window.cardReady = new Promise((ok) => window.addEventListener('DOMContentLoaded', () => S14.ready().catch((e) => {
  window.cardInfo = Object.assign(window.cardInfo || {}, { error: String(e.message || e) });
  document.documentElement.style.overflow = 'visible'; document.body.style.overflow = 'visible'; document.body.style.height = '1500px';
}).then(ok)));
