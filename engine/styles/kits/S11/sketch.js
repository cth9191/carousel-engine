/* S11 Sketchnote Diagram Explainer: fit pass + hand-drawn ink for the diagram cards in this kit.
 *
 * In a card:  <div class="sk-stage" data-fit> ...boxes, notes, labels... </div>
 *             <script src="sketch.js"></script>
 *             <script>SK.init({ arrows: [...], minF: 30, maxF: 44 });</script>
 *
 * Fit pass: one font size --f for the whole diagram (every size in sketch.css is in em of it). It
 * binary-searches the largest --f in [minF, maxF] at which the stage and every [data-fit] inside it
 * fit, so the same card fills any zone size. minF (default 30) is the box-text floor: S11 body text is
 * at least 1/45 of the slide height (30 px); labels, notes and code are 0.72-0.85 em, so render with
 * --min-px 22. If the diagram can't fit at minF, render-card reports the overflow (exit 2): cut words
 * or ask for a bigger zone.
 *
 * Ink (drawn after the fit, into one SVG overlay, seeded so every render is identical):
 *  - every .sk-box gets a wobbly ink outline (.dashed: dashed; data-outline="none": no outline);
 *  - every .sk-note[data-underline] gets a scribbled double underline;
 *  - each arrow in `arrows` is a hand-drawn line with an open head:
 *      { from: '#a', to: '#b', fromSide: 'r', toSide: 'l', fromAt: 0.5, toAt: 0.5, bend: 0,
 *        color: 'ink' | 'orange' | 'green' | '#hex', head: true, gap: 0.22 }
 *    sides: 'l' 'r' 't' 'b'; *At = position along that side (0..1); bend = bow as a share of the
 *    length (+ bows left of travel); gap = clearance from the boxes in em.
 */
(function () {
  const COLORS = { ink: '#1B1B1B', orange: '#D9551F', green: '#2F6B3A', grey: '#4A4A4A' };

  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Smooth open/closed path through points (Catmull-Rom -> cubic Bezier).
  function smooth(pts, closed) {
    const n = pts.length;
    const P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
    let d = `M${pts[0][0].toFixed(2)},${pts[0][1].toFixed(2)}`;
    const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) {
      const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C${c1[0].toFixed(2)},${c1[1].toFixed(2)} ${c2[0].toFixed(2)},${c2[1].toFixed(2)} ${p2[0].toFixed(2)},${p2[1].toFixed(2)}`;
    }
    return d + (closed ? 'Z' : '');
  }

  function roughRect(x, y, w, h, r, jit, rand) {
    // Sample a rounded rectangle's perimeter every ~22 px, jitter each point, start a little past the
    // first corner and overshoot the start like a pen that doesn't quite close.
    const pts = [];
    const step = 22;
    const corner = (cx, cy, a0) => {
      for (let k = 0; k <= 3; k++) {
        const a = a0 + (Math.PI / 2) * (k / 3);
        pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
      }
    };
    const edge = (x0, y0, x1, y1) => {
      const L = Math.hypot(x1 - x0, y1 - y0), n = Math.max(1, Math.round(L / step));
      for (let k = 1; k < n; k++) pts.push([x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n]);
    };
    corner(x + w - r, y + r, -Math.PI / 2);
    edge(x + w, y + r, x + w, y + h - r);
    corner(x + w - r, y + h - r, 0);
    edge(x + w - r, y + h, x + r, y + h);
    corner(x + r, y + h - r, Math.PI / 2);
    edge(x, y + h - r, x, y + r);
    corner(x + r, y + r, Math.PI);
    edge(x + r, y, x + w - r, y);
    const j = pts.map(([px, py]) => [px + (rand() - 0.5) * 2 * jit, py + (rand() - 0.5) * 2 * jit]);
    // open path with a short overlap past the start
    const over = j.slice(0, 3).map(([px, py]) => [px + (rand() - 0.5) * jit, py + jit * 0.8]);
    return smooth([...j, ...over], false);
  }

  function anchor(rect, side, at) {
    const t = at == null ? 0.5 : at;
    switch (side) {
      case 'l': return { p: [rect.left, rect.top + rect.height * t], n: [-1, 0] };
      case 'r': return { p: [rect.right, rect.top + rect.height * t], n: [1, 0] };
      case 't': return { p: [rect.left + rect.width * t, rect.top], n: [0, -1] };
      default:  return { p: [rect.left + rect.width * t, rect.bottom], n: [0, 1] };
    }
  }

  function wobblyLine(a, b, bend, jit, rand) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
    const nx = -dy / L, ny = dx / L;
    const n = Math.max(3, Math.round(L / 34));
    const pts = [];
    for (let k = 0; k <= n; k++) {
      const t = k / n;
      const bow = bend * L * Math.sin(Math.PI * t);
      const w = (k === 0 || k === n) ? 0 : (rand() - 0.5) * 2 * jit;
      pts.push([a[0] + dx * t + nx * (bow + w), a[1] + dy * t + ny * (bow + w)]);
    }
    return pts;
  }

  function init(opts) {
    opts = opts || {};
    const minF = opts.minF || 30, maxF = opts.maxF || 46;
    const stage = document.querySelector('.sk-stage');
    const root = document.documentElement;
    const violations = [];
    const violate = rule => {
      violations.push(rule);
      const el = document.createElement('div');
      el.setAttribute('data-fit', '');
      el.className = 'LIMIT ' + rule.replace(/[^A-Za-z0-9/.-]+/g, '_');
      el.innerHTML = '<i></i>';
      document.body.appendChild(el);
    };

    window.cardReady = (async () => {
      await document.fonts.ready;
      const fitEls = [stage, ...stage.querySelectorAll('[data-fit]')];
      const fits = () => fitEls.every(e => e.scrollWidth <= e.clientWidth + 0.5 && e.scrollHeight <= e.clientHeight + 0.5);
      const setF = f => root.style.setProperty('--f', f + 'px');
      let lo = minF, hi = maxF;
      setF(hi);
      if (!fits()) {
        setF(lo);
        if (fits()) {
          for (let i = 0; i < 20; i++) { const mid = (lo + hi) / 2; setF(mid); if (fits()) lo = mid; else hi = mid; }
        }
        setF(lo);
      } else lo = hi;
      const f = lo;

      // Ink overlay
      const NS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('class', 'sk-ink');
      stage.appendChild(svg);
      const S = stage.getBoundingClientRect();
      const rel = r => ({ left: r.left - S.left, top: r.top - S.top, right: r.right - S.left, bottom: r.bottom - S.top, width: r.width, height: r.height });
      const stroke = Math.max(2, f * 0.085);
      const add = (d, color, extra) => {
        const p = document.createElementNS(NS, 'path');
        p.setAttribute('d', d);
        p.setAttribute('fill', 'none');
        p.setAttribute('stroke', color);
        p.setAttribute('stroke-width', (extra && extra.width) || stroke);
        p.setAttribute('stroke-linecap', 'round');
        p.setAttribute('stroke-linejoin', 'round');
        if (extra && extra.dash) p.setAttribute('stroke-dasharray', extra.dash);
        svg.appendChild(p);
      };

      let seed = 7;
      for (const box of stage.querySelectorAll('.sk-box')) {
        if (box.dataset.outline === 'none') continue;
        const r = rel(box.getBoundingClientRect());
        const rad = Math.min(parseFloat(getComputedStyle(box).borderTopLeftRadius) || 0, r.width / 2, r.height / 2);
        const dashed = box.classList.contains('dashed');
        add(roughRect(r.left, r.top, r.width, r.height, rad, f * 0.035, rng(seed++)),
            dashed ? '#7A7A7A' : COLORS.ink, dashed ? { dash: `${f * 0.32} ${f * 0.26}`, width: stroke * 0.8 } : null);
      }

      for (const note of stage.querySelectorAll('.sk-note[data-underline]')) {
        const rand = rng(seed++);
        const r = rel(note.getBoundingClientRect());
        const w = Math.min(r.width * 0.55, f * 3.2);
        const x0 = r.right - w - f * 0.1, y0 = r.bottom + f * 0.18;
        const z = [[x0, y0 + f * 0.05], [x0 + w, y0 - f * 0.12], [x0 + w * 0.12, y0 + f * 0.16], [x0 + w * 0.92, y0 + f * 0.02]];
        add(smooth(z.map(([x, y]) => [x + (rand() - 0.5) * 2, y + (rand() - 0.5) * 2]), false),
            note.classList.contains('accent') ? COLORS.orange : COLORS.grey, { width: stroke * 0.85 });
      }

      for (const a of (opts.arrows || [])) {
        const fromEl = stage.querySelector(a.from), toEl = stage.querySelector(a.to);
        if (!fromEl || !toEl) { violate(`arrow-${a.from}-to-${a.to}-missing-element`); continue; }
        const rand = rng(seed++);
        const gap = (a.gap == null ? 0.22 : a.gap) * f;
        const A = anchor(rel(fromEl.getBoundingClientRect()), a.fromSide || 'r', a.fromAt);
        const B = anchor(rel(toEl.getBoundingClientRect()), a.toSide || 'l', a.toAt);
        const p0 = [A.p[0] + A.n[0] * gap, A.p[1] + A.n[1] * gap];
        const p1 = [B.p[0] + B.n[0] * gap, B.p[1] + B.n[1] * gap];
        const color = COLORS[a.color] || a.color || COLORS.ink;
        const pts = wobblyLine(p0, p1, a.bend || 0, f * 0.05, rand);
        add(smooth(pts, false), color);
        if (a.head !== false) {
          const e = pts[pts.length - 1], q = pts[pts.length - 2];
          const ang = Math.atan2(e[1] - q[1], e[0] - q[0]);
          const hl = f * 0.42;
          for (const s of [-1, 1]) {
            const t = ang + Math.PI + s * (0.5 + (rand() - 0.5) * 0.12);
            add(`M${e[0].toFixed(2)},${e[1].toFixed(2)} L${(e[0] + Math.cos(t) * hl).toFixed(2)},${(e[1] + Math.sin(t) * hl).toFixed(2)}`, color);
          }
        }
      }

      if (f <= minF && !fits()) violate(`diagram-does-not-fit-at-minF-${minF}px-cut-words-or-use-a-bigger-zone`);
      window.cardInfo = Object.assign({ f_px: +f.toFixed(2), minF, maxF, arrows: (opts.arrows || []).length, violations }, opts.info || {});
    })();
  }

  window.SK = { init };
})();
