/**
 * Renders one HTML card (or an SVG file, e.g. a logo) to a PNG at an exact CSS size, for compositing
 * into a plate zone.
 *
 * Usage:
 *   node shared/render-card.mjs <card.html> <out.png> --w 900 --h 600 [--scale 2] [--bg "#FBF7EE"] [--min-px 14]
 *   node shared/render-card.mjs <logo.svg>  <out.png> --w 512 --h 512 [--scale 2]
 *
 * - Viewport = W x H CSS px, deviceScaleFactor = scale, so the PNG is (W*scale) x (H*scale).
 *   Render a card at the zone's `out bbox` from composite.py --zones-only, so 1 CSS px = 1 px of the
 *   final 1080x1350 slide.
 * - Transparent-safe: the page is shot with omitBackground, so anything the card leaves
 *   transparent (e.g. outside rounded corners) stays transparent. --bg paints the page ground
 *   instead (any CSS colour), for an opaque PNG.
 * - An .svg input is drawn contain-fitted and centred in W x H on a transparent ground (no text
 *   checks): a transparent logo PNG for composite.py --logo.
 * - Waits for network idle (Google Fonts), document.fonts.ready, an optional
 *   window.cardReady promise (the card's own fit pass), and two animation frames.
 * - Fails (exit 2) if the document scrolls beyond W x H, if any [data-fit] element
 *   overflows its box, or if the smallest visible text is under --min-px (default 14) CSS px:
 *   "TOO SMALL". Text is measured in the DOM after the fit pass (computed font size, scaled by
 *   any transform or SVG viewBox), so a card that clips text or shrinks it out of reach on a
 *   phone never ships silently. The PNG is still written so you can look.
 * - Prints which font faces actually loaded, so a silent fallback is visible, and window.cardInfo
 *   if the card sets one.
 */

import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const USAGE = 'usage: node shared/render-card.mjs <card.html|logo.svg> <out.png> --w W --h H [--scale 2] [--bg css-colour] [--min-px 14]';

function arg(name, fallback) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}
function die(msg) {
  console.error(msg);
  process.exit(1);
}

const [htmlArg, outArg] = process.argv.slice(2).filter((a, i, all) =>
  !a.startsWith('--') && !(i > 0 && all[i - 1].startsWith('--')));
if (!htmlArg || !outArg) die(USAGE);
const W = Number(arg('w'));
const H = Number(arg('h'));
const scale = Number(arg('scale', '2'));
const minPx = Number(arg('min-px', '14'));
const bg = arg('bg');
if (!(W > 0 && H > 0 && scale > 0)) die(`--w and --h (CSS px) are required; --scale must be > 0.\n${USAGE}`);
if (!(minPx >= 0)) die(`--min-px must be a number >= 0.\n${USAGE}`);

const htmlPath = path.resolve(htmlArg);
const outPath = path.resolve(outArg);
if (!fs.existsSync(htmlPath)) die(`No such file: ${htmlPath}`);
const isSvg = /\.svg$/i.test(htmlPath);
fs.mkdirSync(path.dirname(outPath), { recursive: true });

const browser = await chromium.launch();
try {
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  if (isSvg) {
    // As an <img> from a data: URI: no scripts, no external loads, scaled by its viewBox.
    const data = `data:image/svg+xml;base64,${fs.readFileSync(htmlPath).toString('base64')}`;
    await page.setContent(`<!doctype html><html><head><style>
      html, body { margin: 0; width: 100%; height: 100%; background: transparent; overflow: hidden; }
      img { display: block; width: 100%; height: 100%; object-fit: contain; }
    </style></head><body><img alt="" src="${data}"></body></html>`);
    await page.evaluate(() => { const img = document.querySelector('img'); return img.complete ? null : img.decode().catch(() => null); });
  } else {
    const url = pathToFileURL(htmlPath);
    url.searchParams.set('w', String(W));
    url.searchParams.set('h', String(H));
    try {
      await page.goto(url.href, { waitUntil: 'networkidle', timeout: 15000 });
    } catch (e) {
      // offline or a slow font CDN: carry on with whatever loaded, the font report shows it
      console.warn(`! page load: ${e.message.split('\n')[0]}`);
    }
  }
  if (bg) await page.addStyleTag({ content: `html, body { background: ${bg} !important; }` });
  await page.evaluate(async () => {
    await document.fonts.ready;
    if (window.cardReady) await window.cardReady;
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  });

  const report = await page.evaluate(({ W, H, isSvg }) => {
    const de = document.documentElement;
    const problems = [];
    if (isSvg) {
      const img = document.querySelector('img');
      if (!img.naturalWidth) problems.push('the SVG did not load (is it valid SVG with a viewBox or width/height?)');
      return { problems, fonts: [], info: null, smallest: null };
    }
    if (de.scrollWidth > W + 1 || de.scrollHeight > H + 1) {
      problems.push(`document is ${de.scrollWidth}x${de.scrollHeight}, viewport ${W}x${H}`);
    }
    for (const el of document.querySelectorAll('[data-fit]')) {
      if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) {
        problems.push(`[data-fit] ${el.className || el.tagName} overflows: ` +
          `${el.scrollWidth}x${el.scrollHeight} in ${el.clientWidth}x${el.clientHeight}`);
      }
      const r = el.getBoundingClientRect();
      if (r.left < -0.5 || r.top < -0.5 || r.right > W + 0.5 || r.bottom > H + 0.5) {
        problems.push(`[data-fit] ${el.className || el.tagName} leaves the viewport`);
      }
    }

    // Smallest visible text: every non-blank text node whose box is on screen, at its rendered size.
    const SKIP = new Set(['SCRIPT', 'STYLE', 'TITLE', 'NOSCRIPT', 'TEMPLATE', 'HEAD']);
    let smallest = null;
    const walker = document.createTreeWalker(document.body || de, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const el = n.parentElement;
      if (!el || SKIP.has(el.tagName) || !n.textContent.trim()) continue;
      if (el.checkVisibility && !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) continue;
      const range = document.createRange();
      range.selectNodeContents(n);
      const onScreen = [...range.getClientRects()].some((r) =>
        r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && r.left < W && r.top < H);
      if (!onScreen) continue;
      let px = parseFloat(getComputedStyle(el).fontSize);
      if (el instanceof SVGElement && el.getScreenCTM) {
        const m = el.getScreenCTM();
        if (m) px *= Math.sqrt(Math.abs(m.a * m.d - m.b * m.c));
      } else if (el.offsetWidth > 0) {
        // a CSS transform: scale() on it or an ancestor (offsetWidth is pre-transform, and whole px)
        const k = el.getBoundingClientRect().width / el.offsetWidth;
        if (k > 0 && Math.abs(k - 1) > 0.05) px *= k;
      }
      if (!(px > 0)) continue;
      if (!smallest || px < smallest.px) {
        const tag = el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : '');
        smallest = { px: Math.round(px * 10) / 10, text: n.textContent.trim().replace(/\s+/g, ' ').slice(0, 40), tag };
      }
    }

    const fonts = [...document.fonts]
      .filter(f => f.status === 'loaded')
      .map(f => `${f.family.replace(/"/g, '')} ${f.weight}`);
    return { problems, fonts: [...new Set(fonts)], info: window.cardInfo || null, smallest };
  }, { W, H, isSvg });

  await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: W, height: H }, omitBackground: !bg });
  console.log(`${path.relative(process.cwd(), outPath)}  ${W}x${H} css @${scale}x = ${W * scale}x${H * scale}px`);
  if (!isSvg) {
    console.log(`  fonts loaded: ${report.fonts.join(', ') || '(none: system fallbacks only)'}`);
    if (report.info) console.log(`  card: ${JSON.stringify(report.info)}`);
    const sm = report.smallest;
    console.log(sm ? `  smallest text: ${sm.px}px ("${sm.text}" in ${sm.tag}), floor ${minPx}px` : '  smallest text: (no visible text)');
    if (sm && sm.px < minPx) {
      report.problems.push({ kind: 'TOO SMALL', msg: `smallest text is ${sm.px}px ("${sm.text}" in ${sm.tag}), under --min-px ${minPx}: give the card a bigger zone or less text` });
    }
  }
  if (report.problems.length) {
    for (const p of report.problems) {
      if (typeof p === 'string') console.error(`  ${isSvg ? 'ERROR' : 'OVERFLOW'} ${p}`);
      else console.error(`  ${p.kind} ${p.msg}`);
    }
    process.exitCode = 2;
  }
} finally {
  await browser.close();
}
