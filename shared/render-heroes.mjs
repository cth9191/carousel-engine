/**
 * Renders HTML hero compositions to PNGs for a carousel's assets folder.
 *
 * Usage:
 *   node shared/render-heroes.mjs --carousel YYYY-MM-DD-slug [--template 02-terracotta-zine]
 *
 * Reads:  carousels/<carousel>/heroes/*.html if that folder exists, else templates/<template>/heroes/*.html
 * Writes: carousels/<carousel>/assets/hero-<filename>.png  (e.g. hero-step1-inspiration.png)
 * templates/ and carousels/ are resolved from the repo root, whatever the working directory.
 * --carousel is required; --template defaults to 02-terracotta-zine.
 */

import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function arg(name, fallback) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

// Accept "2026-10-14-x" or "carousels/2026-10-14-x/" (or templates/<id>/): keep the folder name.
const folderName = (v) => (v ? path.basename(String(v).replace(/[\\/]+$/, '')) : v);

const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const USAGE = 'usage: node shared/render-heroes.mjs --carousel <id> [--template 02-terracotta-zine]';
const die = (msg) => { console.error(msg); process.exit(1); };

const templateId = folderName(arg('template', '02-terracotta-zine'));
const carouselId = folderName(arg('carousel'));
if (!carouselId || carouselId.startsWith('--')) die(`--carousel <id> is required.\n${USAGE}`);
if (!fs.existsSync(path.join(ROOT, 'carousels', carouselId))) die(`No deck folder at carousels/${carouselId}.\n${USAGE}`);

// Carousel-local heroes/ takes precedence over the template's bundled set,
// mirroring how export.mjs prefers the carousel's slides.html fork.
const localHeroesDir = path.join(ROOT, 'carousels', carouselId, 'heroes');
const heroesDir = fs.existsSync(localHeroesDir)
  ? localHeroesDir
  : path.join(ROOT, 'templates', templateId, 'heroes');
const outDir = path.join(ROOT, 'carousels', carouselId, 'assets');
if (!fs.existsSync(heroesDir)) die(`No heroes folder at ${rel(heroesDir)}`);
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const heroFiles = fs.readdirSync(heroesDir)
  .filter(f => f.endsWith('.html'))
  .sort();

if (!heroFiles.length) die(`No .html files in ${rel(heroesDir)}`);

const VIEWPORT = { width: 1600, height: 1000 };

console.log(`Template: ${templateId}`);
console.log(`Carousel: ${carouselId}`);
console.log(`Heroes:   ${heroFiles.length}`);

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: VIEWPORT,
  deviceScaleFactor: 2,
});
const page = await ctx.newPage();

for (const file of heroFiles) {
  const skill = file.replace(/\.html$/, '');
  const heroUrl = pathToFileURL(path.join(heroesDir, file)).href;
  await page.goto(heroUrl, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const out = path.join(outDir, `hero-${skill}.png`);
  await page.screenshot({
    path: out,
    clip: { x: 0, y: 0, width: VIEWPORT.width, height: VIEWPORT.height },
  });
  console.log(`✓ hero-${skill}.png`);
}

await browser.close();
console.log(`\nDone. ${heroFiles.length} heroes in ${rel(outDir)}`);
