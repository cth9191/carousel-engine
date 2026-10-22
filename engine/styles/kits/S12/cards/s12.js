// S12 helpers shared by every page: Lucide swap (icons.js), cutout placement (poses, logo tiles and set
// pieces stand on a feet line with a soft contact shadow), and the fit pass render-card waits on (window.cardReady).
//
// Cutouts: <img class="pose" src="../mascot/x.png" data-x="60" data-feet="1250" data-w="420" data-feet-y="0.995">
//   data-x = left edge, data-w = width (CSS px of the 1080 x 1350 slide), data-feet = the ground line's y,
//   data-feet-y = the pose's feet_y (lowest foot pixel / height; pose-check.py check prints it; default 0.99,
//   set pieces and logo tiles 1.0). The image is placed so its feet sit on the line, with a contact shadow under it.
// No mascot: <img class="pose tile" src="../logos/x.png" ...> is the subject's real logo on a square tile, placed the
//   same way. <div class="pose slot" data-h="..."> is the kit samples' dashed placeholder (data-h defaults to data-w);
//   render-card prints a note while one is left in a page.
// Fit: every [data-fit][data-max] steps down 2 px (floor data-min) until its box stops overflowing.
//   What still overflows makes render-card exit 2: shorten the copy, never lower the floor.
window.S12 = {
  async place(img) {
    const slot = img.tagName !== 'IMG', tile = img.classList.contains('tile');
    if (!slot && !img.complete) await new Promise((ok, bad) => { img.onload = ok; img.onerror = () => bad(new Error('missing ' + img.src)); });
    const x = +img.dataset.x, w = +img.dataset.w, feet = +img.dataset.feet;
    const fy = img.dataset.feetY ? +img.dataset.feetY : (img.classList.contains('set') || slot || tile ? 1.0 : 0.99);
    const h = slot ? (img.dataset.h ? +img.dataset.h : w) : tile ? w : w * img.naturalHeight / img.naturalWidth;
    Object.assign(img.style, { left: x + 'px', top: (feet - h * fy) + 'px', width: w + 'px', height: h + 'px' });
    if (img.dataset.shadow !== 'off') {
      const s = document.createElement('div');
      s.className = 'shadow';
      const sw = w * 0.86, sh = Math.max(18, w * 0.075);
      Object.assign(s.style, { left: (x + (w - sw) / 2) + 'px', top: (feet - sh / 2) + 'px', width: sw + 'px', height: sh + 'px' });
      img.before(s);
    }
  },
  async ready() {
    await document.fonts.ready;
    if (window.lucide) window.lucide();
    await Promise.all([...document.querySelectorAll('.pose, img.set')].map(S12.place));
    const over = (el) => el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
    for (const el of document.querySelectorAll('[data-fit][data-max]')) {
      let px = +el.dataset.max;
      const min = +el.dataset.min;
      el.style.fontSize = px + 'px';
      while (over(el) && px > min) { px -= 2; el.style.fontSize = px + 'px'; }
    }
    // The headline's second line must be the orange one, and a bubble holds one line only.
    const hl = document.querySelector('.hl');
    const problems = [];
    if (hl && !hl.querySelector('.l2')) problems.push('headline has no .l2 (orange) line');
    for (const b of document.querySelectorAll('.bubble')) if (b.textContent.trim().split(/\s+/).length > 4) problems.push('bubble over 4 words: ' + b.textContent.trim());
    const notes = document.querySelector('.pose.slot') ? ['mascot placeholder still in the page: put your own pose, a logo tile, or delete it'] : [];
    window.cardInfo = { problems, notes };
    if (problems.length) { document.documentElement.style.overflow = 'visible'; document.body.style.overflow = 'visible'; document.body.style.height = '1500px'; }
  },
};
// A failure (a missing cutout, say) never hangs the render: it lands in cardInfo and the page overflows (exit 2).
window.cardReady = new Promise((ok) => window.addEventListener('DOMContentLoaded', () => S12.ready().catch((e) => {
  window.cardInfo = { error: String(e.message || e) };
  document.documentElement.style.overflow = 'visible'; document.body.style.overflow = 'visible'; document.body.style.height = '1500px';
}).then(ok)));
