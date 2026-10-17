/**
 * Playwright export for HTML-template decks (style S01 interiors, or any deck with a slides.html).
 *
 * Usage:
 *   node shared/export.mjs --carousel <id> [--native] [--template <template-id>]
 *
 * --carousel <id>   required: a folder name under carousels/ (a path like carousels/<id>/ also works).
 *                   The source is carousels/<id>/slides.html, the deck's own copy of the template.
 * --template <id>   only used when the deck has no slides.html: bake templates/<id>/slides.html
 *                   (the template's sample slides) into the deck's exports/ instead. Never implied.
 * --native          keep the 2x render (2160x2700 for a 1080x1350 slide). Default: each slide is
 *                   rendered at deviceScaleFactor 2 and downsampled with sharp to its CSS size
 *                   (1080x1350), which is what Instagram takes.
 *
 * Writes carousels/<id>/exports/slide-NN-YYYY-MM-DD.png (date from the folder name; a slide's
 * exportName replaces the slide-NN part). templates/ and carousels/ are resolved from the repo root,
 * whatever the working directory.
 *
 * Exit: 0 ok · 1 usage or missing file, or a template's render() threw (its fit pass names the slide)
 * · 2 a visible <img> on a slide failed to load (every slide is still written so you can look; each
 * broken image is named with its slide and src) · 3 a template reported a fit/copy failure in
 * window.fitReport[idx] or window.qa() issues (templates that define them); every slide is still
 * written, with the template's own red banner visible, and each failure is named.
 * A deck slide that still shows {{BRAND}} or {{MONTH_YEAR}} gets a warning (the exit code is unchanged).
 */

import { chromium } from 'playwright';
import sharp from 'sharp';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const USAGE = 'usage: node shared/export.mjs --carousel <id> [--native] [--template <template-id>]';

function arg(name) {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx < 0) return undefined;
  const v = process.argv[idx + 1];
  return v && !v.startsWith('--') ? v : null; // null = flag given without a value
}
function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

// Accept "2026-10-14-x" or "carousels/2026-10-14-x/" (or templates/<id>/): keep the folder name.
const folderName = (v) => (v ? path.basename(String(v).replace(/[\\/]+$/, '')) : v);

const carouselId = folderName(arg('carousel'));
const templateArg = arg('template');
const templateId = folderName(templateArg);
const native = process.argv.includes('--native');

if (!carouselId) die(`--carousel <id> is required.\n${USAGE}`);
if (templateArg === null) die(`--template needs a template id.\n${USAGE}`);
const deckDir = path.join(ROOT, 'carousels', carouselId);
if (!fs.existsSync(deckDir)) die(`No deck folder at ${rel(deckDir)}.\n${USAGE}`);

const carouselHtml = path.join(deckDir, 'slides.html');
let sourceHtml = carouselHtml;
if (!fs.existsSync(carouselHtml)) {
  if (!templateId) {
    die(`No slides.html in ${rel(deckDir)}.\n` +
      'Copy templates/02-terracotta-zine/slides.html (and its assets/) into the deck and replace {{BRAND}} and\n' +
      '{{MONTH_YEAR}}, or pass --template <id> to bake that template\'s own sample slides.');
  }
  sourceHtml = path.join(ROOT, 'templates', templateId, 'slides.html');
  if (!fs.existsSync(sourceHtml)) die(`No slides.html at ${rel(sourceHtml)}`);
}
const outDir = path.join(deckDir, 'exports');
fs.mkdirSync(outDir, { recursive: true });

// Derive date suffix from carousel folder name (YYYY-MM-DD-...) so PNG names carry the date.
const dateMatch = carouselId.match(/^(\d{4}-\d{2}-\d{2})/);
const dateSuffix = dateMatch ? '-' + dateMatch[1] : '';

console.log(`Carousel: ${carouselId}`);
console.log(`Source:   ${sourceHtml === carouselHtml ? 'deck slides.html' : `template ${templateId} (sample slides)`}`);
console.log(`Output:   ${native ? 'native 2x' : 'downsampled to the slide\'s CSS size'}`);

const browser = await chromium.launch();
const broken = [];
const unreplaced = new Set();
const fitFails = [];
let total = 0;
try {
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  await page.goto(pathToFileURL(sourceHtml).href, { waitUntil: 'networkidle' });

  await page.addStyleTag({ content: `
    .ui, .tw-toggle, .tw-panel, #fs { display: none !important; }
    html, body { background: white !important; overflow: hidden !important; }
    .stage { position: static !important; padding: 0 !important; }
    .slide-wrap { transform: none !important; transform-origin: top left !important; }
  `});

  await page.evaluate(() => document.fonts.ready);

  total = await page.evaluate(() => window.totalSlides());
  console.log(`Exporting ${total} slides…`);

  for (let i = 0; i < total; i++) {
    await page.evaluate((idx) => window.goSlide(idx), i);

    // Wait for every visible image to settle (load or error), then fonts.
    await page.evaluate(() => Promise.all(
      Array.from(document.images)
        .filter((img) => img.offsetParent !== null && !img.complete)
        .map((img) => new Promise((res) => {
          img.addEventListener('load', res, { once: true });
          img.addEventListener('error', res, { once: true });
        })),
    ).then(() => document.fonts.ready));

    await page.waitForTimeout(400);

    // A visible <img> that has no pixels is a broken slide: a missing hero, a typo in heroImg.
    const bad = await page.evaluate(() => {
      const root = document.getElementById('slide') || document.body;
      return Array.from(root.querySelectorAll('img'))
        .filter((img) => (img.checkVisibility ? img.checkVisibility({ visibilityProperty: true }) : img.offsetParent !== null))
        .filter((img) => !img.getAttribute('src') || (img.complete && img.naturalWidth === 0))
        .map((img) => img.getAttribute('src') || '(empty src)');
    });
    // Template placeholders the deck copy should have replaced (warning only).
    const placeholders = await page.evaluate(() =>
      [...new Set(((document.getElementById('slide') || document.body).innerText.match(/\{\{[A-Z_]+\}\}/g) || []))]);
    for (const p of placeholders) unreplaced.add(p);

    const slideEl = page.locator('#slide');
    const meta = await page.evaluate((idx) => ({ name: slides[idx].name, exportName: slides[idx].exportName || null }), i);
    const base = meta.exportName || `slide-${String(i + 1).padStart(2, '0')}`;
    const fileName = `${base}${dateSuffix}.png`;
    const out = path.join(outDir, fileName);

    const shot = await slideEl.screenshot();
    let size;
    if (native) {
      fs.writeFileSync(out, shot);
      const m = await sharp(shot).metadata();
      size = `${m.width}x${m.height}`;
    } else {
      const box = await slideEl.boundingBox();
      const w = Math.round(box.width), h = Math.round(box.height);
      await sharp(shot).resize(w, h, { kernel: 'lanczos3' }).png().toFile(out);
      size = `${w}x${h}`;
    }

    // Template fit checks: a fit pass that leaves errors in window.fitReport, or a qa() that returns issues.
    const fit = await page.evaluate((idx) => {
      const r = window.fitReport && window.fitReport[idx];
      const errs = Array.isArray(r) ? r : r ? [String(r)] : [];
      if (typeof window.qa === 'function') {
        const q = window.qa();
        const issues = Array.isArray(q) ? q : (q && Array.isArray(q.issues) ? q.issues : []);
        errs.push(...issues.map(String));
      }
      return errs;
    }, i);
    for (const e of fit) fitFails.push({ slide: base, name: meta.name, e });

    for (const src of bad) broken.push({ slide: base, name: meta.name, src });
    console.log(`${bad.length ? '✗' : '✓'} ${fileName}  ${size}  (${meta.name})${bad.length ? `  BROKEN IMAGE ${bad.join(', ')}` : ''}${fit.length ? `  FIT ${fit.join('; ')}` : ''}`);
  }
} finally {
  await browser.close();
}

if (unreplaced.size && sourceHtml === carouselHtml) {
  console.warn(`\nWARNING: slides still show ${[...unreplaced].join(', ')}: replace {{BRAND}} (engine/brand.json) and ` +
    '{{MONTH_YEAR}} (e.g. "OCTOBER ©2026") in the deck\'s slides.html.');
}
if (broken.length) {
  console.error(`\n${broken.length} visible image(s) failed to load (src is relative to ${rel(path.dirname(sourceHtml))}/):`);
  for (const b of broken) console.error(`  ${b.slide} (${b.name}): ${b.src}`);
  process.exit(2);
}
if (fitFails.length) {
  console.error(`\n${fitFails.length} fit/copy failure(s): rewrite the copy (or fix the slide data), then bake again:`);
  for (const f of fitFails) console.error(`  ${f.slide} (${f.name}): ${f.e}`);
  process.exit(3);
}
console.log(`\nDone. ${total} PNGs in ${rel(outDir)}`);
