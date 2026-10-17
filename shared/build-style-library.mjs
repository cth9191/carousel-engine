#!/usr/bin/env node
// Style Library page: the browsable version of engine/styles/styles.json, a static HTML page.
// One card per style (cover + interior), filters, and a detail view with more slides from the
// exemplar deck, the attributes, the record (your own usage stats, when you sync a post log), the
// requirements and the prompt block. Zero image generation: the art is the exemplars on disk.
//
//   node shared/build-style-library.mjs            # writes engine/styles/library/index.html + img/
//   node shared/build-style-library.mjs --max 8    # slides per style in the detail view (default 8)
//
// If you keep a post log, run `node shared/build-gallery.mjs --sync` first so styles.json stats are current.
// Open engine/styles/library/index.html in a browser, or host it (with img/) anywhere static.
// The output folder is a build product and is git-ignored.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(`--${k}`); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const MAX = Number(arg('max', 8));
const STYLES_DIR = path.join(ROOT, 'engine/styles');
const OUT = path.join(STYLES_DIR, 'library');
const IMG = path.join(OUT, 'img');
const TEMPLATE = path.join(ROOT, 'shared/style-library.template.html');
const IMG_W = 720;

const catalog = JSON.parse(fs.readFileSync(path.join(STYLES_DIR, 'styles.json'), 'utf8'));
const resolvePath = (p) => (path.isAbsolute(p) ? p : path.resolve(ROOT, p));

// Siblings of an exemplar in the same deck: same stem before the slide number
// (slide-01-2026-06-14.png, post-s0.jpg, post-01.jpg, slide-01.webp).
const SLIDE_RE = /^(.*?)(\d+)(-\d{4}-\d{2}-\d{2})?\.(png|jpe?g|webp)$/i;
function deckSlides(file) {
  const m = path.basename(file).match(SLIDE_RE);
  if (!m) return [];
  const dir = path.dirname(file);
  return fs.readdirSync(dir)
    .map((f) => ({ f, m: f.match(SLIDE_RE) }))
    .filter(({ m: n }) => n && n[1] === m[1] && (n[3] ?? '') === (m[3] ?? '') && n[4].toLowerCase() === m[4].toLowerCase())
    .sort((a, b) => Number(a.m[2]) - Number(b.m[2]))
    .map(({ f }) => path.join(dir, f));
}

function slidesFor(s) {
  const cover = resolvePath(s.exemplars.cover);
  const interior = resolvePath(s.exemplars.interior);
  const list = [{ src: cover, role: 'cover' }];
  if (interior !== cover) list.push({ src: interior, role: 'interior' });
  for (const src of deckSlides(cover)) {
    if (list.length >= MAX) break;
    if (!list.some((x) => x.src === src)) list.push({ src, role: 'more' });
  }
  return list.filter((x) => fs.existsSync(x.src));
}

function promptFor(id) {
  const f = fs.readdirSync(STYLES_DIR).find((n) => n.startsWith(`${id}-`) && n.endsWith('.prompt.md'));
  return f ? { file: `engine/styles/${f}`, text: fs.readFileSync(path.join(STYLES_DIR, f), 'utf8') } : null;
}

fs.rmSync(IMG, { recursive: true, force: true });
fs.mkdirSync(IMG, { recursive: true });

const styles = [];
let bytes = 0;
for (const s of catalog.styles) {
  const slides = [];
  for (const [i, x] of slidesFor(s).entries()) {
    const name = `${s.id}-${i}.jpg`;
    const info = await sharp(x.src).resize({ width: IMG_W, withoutEnlargement: true }).flatten({ background: '#000' })
      .jpeg({ quality: 80, mozjpeg: true }).toFile(path.join(IMG, name));
    bytes += info.size;
    slides.push({ img: `img/${name}`, role: x.role, w: info.width, h: info.height });
  }
  const blocked = /^BLOCKED/.test(s.formats?.notes ?? '');
  styles.push({
    id: s.id, name: s.name, one_line: s.one_line, status: s.status, production: s.production,
    formats: s.formats, attributes: s.attributes, stats: s.stats, cooldown_days: s.cooldown_days,
    cooldown_group: s.cooldown_group ?? null, exemplars: s.exemplars, evidence: s.evidence ?? [],
    evidence_note: s.evidence_note, requires: s.requires, template: s.template, posts: s.posts,
    drafts: s.drafts, blocked, slides, prompt: promptFor(s.id),
  });
}

const data = { updated: catalog.updated, built: new Date().toISOString().slice(0, 10), spines: catalog.spines, styles };
const json = JSON.stringify(data).replace(/</g, '\\u003c');
const html = fs.readFileSync(TEMPLATE, 'utf8').replace('/*__DATA__*/null', () => json);
fs.writeFileSync(path.join(OUT, 'index.html'), html);

const nImg = styles.reduce((n, s) => n + s.slides.length, 0);
console.log(`wrote ${path.relative(ROOT, OUT)}/index.html (${(html.length / 1024).toFixed(0)} KB) + ${nImg} images (${(bytes / 1048576).toFixed(1)} MB) for ${styles.length} styles`);
