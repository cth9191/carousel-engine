// S23 proof-card kit runtime: reads the card's JSON from <script id="data">, lets the card build its DOM,
// then runs the fit pass (each [data-fit] box shrinks its font-size in 0.5 px steps down to data-min, default 14)
// and resolves window.cardReady for shared/render-card.mjs.
// A broken copy rule (too many words, too long a name) adds an overflowing [data-fit] .LIMIT-<rule> box, so
// render-card exits 2 and prints the rule.
(function () {
  window.DATA = JSON.parse(document.getElementById('data').textContent);
  const KIT = window.KIT = {
    esc: (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])),
    words: (s) => String(s ?? '').trim().split(/\s+/).filter(Boolean).length,
    limit(ok, rule) {
      if (ok) return;
      const d = document.createElement('div');
      d.setAttribute('data-fit', '');
      d.className = 'LIMIT-' + rule;
      d.style.cssText = 'position:absolute;left:0;top:0;width:2px;height:2px;overflow:hidden';
      d.innerHTML = '<div style="width:40px;height:40px"></div>';
      document.body.appendChild(d);
    },
    fit() {
      for (const el of document.querySelectorAll('[data-fit]')) {
        if (/^LIMIT-/.test(el.className)) continue;
        const min = +(el.dataset.min || 14);
        let fs = parseFloat(getComputedStyle(el).fontSize), n = 0;
        while ((el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1) && fs > min && n++ < 300) {
          fs = Math.max(min, fs - 0.5);
          el.style.fontSize = fs + 'px';
        }
      }
    },
    ready(build) {
      window.cardReady = document.fonts.ready
        .then(() => { const p = build(window.DATA); void document.body.offsetHeight; return Promise.resolve(p).then(() => document.fonts.ready); })
        .then(() => new Promise((r) => requestAnimationFrame(r)))
        .then(() => KIT.fit());
    },
  };
})();
