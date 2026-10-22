// S25 helpers shared by the deck's pages: Lucide swap (icons.js) and the hub module's layout + wires.
// Each page keeps its own inline window.cardReady fit pass and calls S25.prep() first.
window.S25 = {
  prep() {
    if (window.lucide) window.lucide();
    document.querySelectorAll('.hub').forEach(S25.hub);
  },
  // Up to 6 .spoke tiles: the first half down the left column, the rest down the right, each wired
  // to the centre card's nearest edge by a dashed curve ending in orange dots.
  hub(hub) {
    const W = hub.clientWidth, H = hub.clientHeight;
    const spokes = [...hub.querySelectorAll('.spoke')];
    if (spokes.length > 6) throw new Error('hub: 6 spokes at most');
    const centre = hub.querySelector('.centre');
    const cw = centre.offsetWidth, ch = centre.offsetHeight;
    const cx0 = (W - cw) / 2, cx1 = (W + cw) / 2, cy = H / 2;
    const nl = Math.ceil(spokes.length / 2);
    const sides = [spokes.slice(0, nl), spokes.slice(nl)];
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'wires');
    sides.forEach((list, s) => {
      list.forEach((el, i) => {
        const h = el.offsetHeight, w = el.offsetWidth;
        const y = (H / list.length) * (i + 0.5) - h / 2;
        const x = s === 0 ? 0 : W - w;
        el.style.left = x + 'px'; el.style.top = y + 'px';
        const x1 = s === 0 ? x + w : x, y1 = y + h / 2;
        const x2 = s === 0 ? cx0 : cx1, y2 = cy + (y1 - cy) * 0.35;
        const xm = (x1 + x2) / 2;
        const p = document.createElementNS(NS, 'path');
        p.setAttribute('d', `M${x1} ${y1} C${xm} ${y1} ${xm} ${y2} ${x2} ${y2}`);
        svg.appendChild(p);
        for (const [cx, cyy] of [[x1, y1], [x2, y2]]) {
          const c = document.createElementNS(NS, 'circle');
          c.setAttribute('cx', cx); c.setAttribute('cy', cyy); c.setAttribute('r', 5);
          svg.appendChild(c);
        }
      });
    });
    hub.prepend(svg);
    void ch;
  },
};
