/**
 * sky-tone.mjs - tone pass for styles that set type over painted skies (S13, S14, S15): ink or white type, and the scrim it needs, on sharp.
 *
 * Why outside the browser: render-card loads cards over file://, where canvas getImageData on a
 * file:// image throws SecurityError, so an overlay can't sample its own plate.
 *
 * Usage (from the repo root):
 *   node shared/sky-tone.mjs <deck-dir> [--slides 01,03] [--no-stamp]
 *       Every <deck>/fitted/slide-NN.png that has a <deck>/cards/slide-NN.html. The layout (and an
 *       optional "box" override) is read from the card's slide-data JSON block. Writes
 *       <deck>/runs/tone/slide-NN.json and stamps the choices onto the card's <body> as data attributes.
 *   node shared/sky-tone.mjs <fitted/slide-NN.png> [--layout item] [--card cards/slide-NN.html]
 *                            [--out runs/tone/slide-NN.json] [--box 0.12,0.52] [--no-stamp]
 *       One plate. --out defaults to <plate's deck>/runs/tone/<name>.json; --card is stamped if given.
 *
 * The plate must already be fitted to 1080x1350 (python -I shared/composite.py plates/slide-NN.png
 * fitted/slide-NN.png); another size is scaled to 1080x1350 for sampling, with a warning.
 *
 * Regions, all across x 104-976 (the overlay's 104 px side margins):
 *   mast   3-9% of the height           target 4.5:1
 *   stack  the layout's box (below)     top 60% (kicker + giant) 3:1, bottom 40% (caption, use, proof) 4.5:1
 *   nav    91-98%                       target 4.5:1
 *   Boxes: cover 12-43% · item, stake, combo 12-52% · proof 11-44% · cta 14-50% (same table as overlay.html).
 * Per region: relative luminance of every pixel, p10 and p90. White's contrast is taken against p90 (the
 * brightest sky it must clear), ink #0E0E0E's against p10; the higher one wins (they cross near L 0.19).
 * Short of target: simulate a scrim at 20%, 35%, then 50% (black at that alpha behind white =
 * multiply-darken; white at that alpha behind ink = screen-lighten), full strength inside the region
 * (the overlay feathers it outside: 80 px around the stack box, a 60 px fade on the strips), and take the
 * first step that passes. Still short at 50%: the other colour is tried at 50%; else the region fails
 * (edit job: a calmer sky). Cover only: data-nav-dim="70" when the nav still clears 4.5:1 at 70% opacity.
 *
 * Output runs/tone/slide-NN.json: { plate, layout, box, regions: { mast, stack, nav }, body, pass }; each
 * region keeps its colour, scrim, pass and per-band { target, p10, p90, contrast } measured after the scrim.
 * `body` is what the overlay reads:
 *   <body data-mast="ink|white" data-stack="ink|white" data-nav="ink|white"
 *         data-scrim="0|20|35|50" data-scrim-mast="…" data-scrim-nav="…" [data-nav-dim="70"]>
 * (data-scrim is the stack's scrim; the strips have their own.)
 *
 * Exit: 0 every region passes · 4 some region still short at 50% (JSON and stamp still written, so you can
 * look) · 1 bad usage / missing file.
 */

import sharp from 'sharp';
import fs from 'node:fs';
import path from 'node:path';

const W = 1080, H = 1350, X0 = 104, X1 = 976;
const BOXES = { cover: [0.12, 0.43], item: [0.12, 0.52], stake: [0.12, 0.52], combo: [0.12, 0.52], proof: [0.11, 0.44], cta: [0.14, 0.50] };
const STEPS = [0, 20, 35, 50];
const INK = 14 / 255;                       // #0E0E0E
const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const L_INK = lin(INK);
const LUT = Float64Array.from({ length: 256 }, (_, i) => lin(i / 255));
const cr = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);

const USAGE = 'usage: node shared/sky-tone.mjs <deck-dir> [--slides 01,03] [--no-stamp]\n' +
  '       node shared/sky-tone.mjs <fitted/slide-NN.png> [--layout item] [--card cards/slide-NN.html] [--out file.json] [--box 0.12,0.52] [--no-stamp]';
const argv = process.argv.slice(2);
const opt = (n) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : undefined; };
const flag = (n) => argv.includes(`--${n}`);
const positional = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--') && !['--no-stamp'].includes(argv[i - 1])));
function die(m) { console.error(m); process.exit(1); }
if (!positional[0]) die(USAGE);

function readCardData(cardPath) {
  const html = fs.readFileSync(cardPath, 'utf8');
  const m = html.match(/<script\s+type="application\/json"\s+id="slide-data"\s*>([\s\S]*?)<\/script>/);
  if (!m) die(`${cardPath}: no <script id="slide-data"> JSON block`);
  try { return JSON.parse(m[1]); } catch (e) { die(`${cardPath}: slide-data is not valid JSON (${e.message})`); }
}

function stampCard(cardPath, attrs) {
  let html = fs.readFileSync(cardPath, 'utf8');
  const m = html.match(/^<body\b[^>]*>/m);   // the real tag, at the start of its line
  if (!m) die(`${cardPath}: no <body> tag at the start of a line`);
  let tag = m[0].replace(/\s+data-(mast|stack|nav|scrim|scrim-mast|scrim-nav|nav-dim)="[^"]*"/g, '');
  const add = Object.entries(attrs).map(([k, v]) => ` ${k}="${v}"`).join('');
  tag = tag.replace(/^<body/, `<body${add}`);
  html = html.replace(m[0], tag);
  fs.writeFileSync(cardPath, html);
}

// Luminance samples of one rectangle (CSS px of the 1080x1350 slide), after an optional scrim.
function sample(raw, y0, y1) {
  const out = new Float64Array((X1 - X0) * (y1 - y0));
  let k = 0;
  for (let y = y0; y < y1; y++) {
    for (let x = X0; x < X1; x++) {
      const i = (y * W + x) * 3;
      out[k++] = (raw[i] << 16) | (raw[i + 1] << 8) | raw[i + 2];
    }
  }
  return out;
}
function percentiles(px, scrimTone, a) {
  // scrimTone 'white' = text is white -> black scrim (c * (1 - a)); 'ink' -> white scrim (c + a (1 - c))
  const hist = new Uint32Array(1001);
  for (let k = 0; k < px.length; k++) {
    const v = px[k];
    let r = (v >> 16) & 255, g = (v >> 8) & 255, b = v & 255;
    let L;
    if (!a) L = 0.2126 * LUT[r] + 0.7152 * LUT[g] + 0.0722 * LUT[b];
    else {
      const f = (c) => (scrimTone === 'white' ? lin((c / 255) * (1 - a)) : lin(c / 255 + a * (1 - c / 255)));
      L = 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    }
    hist[Math.round(L * 1000)]++;
  }
  const at = (q) => { let acc = 0; const n = px.length * q; for (let i = 0; i <= 1000; i++) { acc += hist[i]; if (acc >= n) return i / 1000; } return 1; };
  return { p10: at(0.10), p90: at(0.90) };
}
const contrastFor = (tone, p) => (tone === 'white' ? cr(1, p.p90) : cr(L_INK, p.p10));

// One region: bands = [{px, target}], all sharing one colour and one scrim.
function decide(bands) {
  const at = (tone, step) => bands.map((b) => {
    const p = percentiles(b.px, tone, step / 100);
    return { target: b.target, p10: p.p10, p90: p.p90, contrast: +contrastFor(tone, p).toFixed(2) };
  });
  const worst = (r) => Math.min(...r.map((x) => x.contrast / x.target));
  const base = { ink: at('ink', 0), white: at('white', 0) };
  // the colour with the higher WCAG contrast against the plain plate (ratio to target, so bands weigh fairly)
  const tone = worst(base.white) > worst(base.ink) ? 'white' : 'ink';
  const order = [tone, tone === 'white' ? 'ink' : 'white'];
  for (const step of STEPS) {
    const r = step ? at(tone, step) : base[tone];
    if (worst(r) >= 1) return { color: tone, scrim: step, pass: true, bands: r };
  }
  const other = at(order[1], 50);
  if (worst(other) >= 1) return { color: order[1], scrim: 50, pass: true, bands: other };
  return { color: tone, scrim: 50, pass: false, bands: at(tone, 50) };
}

// Cover nav at 70% opacity: blend the text colour with the background and re-check 4.5:1 (at its scrim).
function navDim(px, res) {
  const a = res.scrim / 100;
  const p = percentiles(px, res.color, a);
  const Lbg = res.color === 'white' ? p.p90 : p.p10;
  const bgS = Lbg <= 0.0031308 ? Lbg * 12.92 : 1.055 * Lbg ** (1 / 2.4) - 0.055;   // grey sRGB of that luminance
  const txt = res.color === 'white' ? 1 : INK;
  const eff = lin(0.7 * txt + 0.3 * bgS);
  return cr(eff, Lbg) >= 4.5;
}

async function tone(platePath, layout, boxOverride) {
  if (!fs.existsSync(platePath)) die(`No such plate: ${platePath}`);
  const meta = await sharp(platePath).metadata();
  if (meta.width !== W || meta.height !== H) {
    console.warn(`! ${path.basename(platePath)} is ${meta.width}x${meta.height}, not ${W}x${H}: fit it with composite.py first (sampling a resize)`);
  }
  const raw = await sharp(platePath).resize(W, H, { fit: 'fill' }).removeAlpha().raw().toBuffer();
  const box = boxOverride || BOXES[layout];
  if (!box) die(`unknown layout "${layout}" (${Object.keys(BOXES).join(', ')})`);
  const Y = (f) => Math.round(f * H);
  const by0 = Y(box[0]), by1 = Y(box[1]), bsplit = Math.round(by0 + 0.6 * (by1 - by0));
  const mastPx = sample(raw, Y(0.03), Y(0.09));
  const navPx = sample(raw, Y(0.91), Y(0.98));
  const mast = decide([{ px: mastPx, target: 4.5 }]);
  const stack = decide([{ px: sample(raw, by0, bsplit), target: 3 }, { px: sample(raw, bsplit, by1), target: 4.5 }]);
  const nav = decide([{ px: navPx, target: 4.5 }]);
  const body = {
    'data-mast': mast.color, 'data-stack': stack.color, 'data-nav': nav.color,
    'data-scrim': String(stack.scrim), 'data-scrim-mast': String(mast.scrim), 'data-scrim-nav': String(nav.scrim),
  };
  if (layout === 'cover' && nav.pass && navDim(navPx, nav)) body['data-nav-dim'] = '70';
  return { plate: platePath.replace(/\\/g, '/'), layout, box, regions: { mast, stack, nav }, body, pass: mast.pass && stack.pass && nav.pass };
}

function line(name, r) {
  const g = r.regions;
  const f = (k) => `${k} ${g[k].color}${g[k].scrim ? '+' + g[k].scrim + '%' : ''} ${g[k].bands.map((b) => b.contrast + ':1').join('/')}${g[k].pass ? '' : ' SHORT'}`;
  console.log(`${name}  ${r.layout.padEnd(5)}  ${f('mast')} | ${f('stack')} | ${f('nav')}${r.body['data-nav-dim'] ? ' | nav-dim 70' : ''}`);
}

let failed = false;
const stamp = !flag('no-stamp');
const boxArg = opt('box') ? opt('box').split(',').map(Number) : undefined;
const target = path.resolve(positional[0]);

if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
  const deck = target;
  const only = opt('slides') ? new Set(opt('slides').split(',').map((s) => s.padStart(2, '0'))) : null;
  const fitted = path.join(deck, 'fitted');
  if (!fs.existsSync(fitted)) die(`${fitted} does not exist: fit the plates first`);
  const plates = fs.readdirSync(fitted).filter((f) => /^slide-\d+\.png$/.test(f)).sort();
  let done = 0;
  for (const f of plates) {
    const nn = f.match(/\d+/)[0];
    if (only && !only.has(nn)) continue;
    const card = path.join(deck, 'cards', `slide-${nn}.html`);
    if (!fs.existsSync(card)) { console.warn(`! slide-${nn}: no cards/slide-${nn}.html, skipped`); continue; }
    const data = readCardData(card);
    if (data.plate && path.resolve(path.dirname(card), data.plate) !== path.join(fitted, f)) {
      console.warn(`! slide-${nn}: the card's "plate" is ${data.plate}, not ../fitted/${f}`);
    }
    const r = await tone(path.join(fitted, f), data.layout || 'item', data.box);
    const out = path.join(deck, 'runs', 'tone', `slide-${nn}.json`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, JSON.stringify(r, null, 1));
    if (stamp) stampCard(card, r.body);
    line(`slide-${nn}`, r);
    failed ||= !r.pass;
    done++;
  }
  if (!done) die('no slides matched');
} else {
  const card = opt('card') ? path.resolve(opt('card')) : null;
  const data = card ? readCardData(card) : {};
  const layout = opt('layout') || data.layout || 'item';
  const r = await tone(target, layout, boxArg || data.box);
  const name = path.basename(target, '.png');
  const out = opt('out') ? path.resolve(opt('out')) : path.join(path.dirname(path.dirname(target)), 'runs', 'tone', `${name}.json`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(r, null, 1));
  if (card && stamp) stampCard(card, r.body);
  line(name, r);
  console.log(`  -> ${path.relative(process.cwd(), out)}${card && stamp ? ` (stamped ${path.relative(process.cwd(), card)})` : ''}`);
  failed = !r.pass;
}
if (failed) {
  console.error('SHORT: a region misses its contrast target even at a 50% scrim: edit job for a calmer sky');
  process.exitCode = 4;
}
