#!/usr/bin/env node
// Style gallery: a numbered sheet of every style in engine/styles/styles.json.
// Each tile = caption band (id, name, usage stats or spines, status) ABOVE an exemplar cover + interior.
// Zero image generation: the art is existing exports / reference images, letterboxed, never cropped.
//
//   node shared/build-gallery.mjs                 # render engine/styles/gallery.jpg; nothing else is written
//   node shared/build-gallery.mjs --only S03,S01  # just those tiles (brief-card crop) -> gallery-pick-S03-S01.jpg
//   node shared/build-gallery.mjs --check         # validate + print the table, render nothing
//   node shared/build-gallery.mjs --sync          # first recompute styles.json stats from your post log
//   options: --today YYYY-MM-DD (cooldown clock, default = local date) · --include-retired
//            --parts (also write phone-sized part sheets) · --part-size 6 · --part-cols 2
//            --out-dir engine/styles · --out FILE (with --only: the pick sheet; without: the full sheet)
//            --deck-map FILE (the post log for --sync)
//
// Writes engine/styles/gallery.jpg (3 tiles per row, every style). With --parts it also writes
// gallery-part-N.jpg (6 tiles each, 2 per row, sized to read on a phone); with --out FILE the parts go
// to <FILE without .jpg>-part-N.jpg. styles.json is only ever written with --sync.
//
// Stats sync is optional and only runs with --sync. If you keep a post log at
// research/catalog/deck-map.json (or pass --deck-map FILE), --sync recomputes posts / interior_posts /
// drafts / stats in styles.json from it. The log is a JSON array with one entry per deck of yours:
//   { "code": "<post id>", "folder": "carousels/<id>", "date": "YYYY-MM-DD", "status": "posted" | "draft",
//     "cover_style": "S01", "interior_style": "S01", "mult": 1.0 }
// mult is the post's performance ratio, e.g. its views / the median views of your carousels posted
// within +-21 days. Median and best per style are taken over it. Without --sync (or without a log),
// the gallery renders from styles.json as it is, and a style with no stats shows the spines it fits.
//
// Cooldown: a style cools for cooldown_days after its own last cover. A style may also carry
// cooldown_group: one object or an array of them, {id, members: [style ids], applies_to: 'cover'|'any',
// cap_days}. It then also cools while any member's last cover ('cover'), or last cover or interior
// ('any'), is under cap_days old. Every member carries an identical copy of each of its groups.
// Groups read the post log too: without one, nothing cools.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const flag = (k) => argv.includes(`--${k}`);
const arg = (k, d) => { const i = argv.indexOf(`--${k}`); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };

const STYLES_PATH = path.join(ROOT, 'engine/styles/styles.json');
const SYNC = flag('sync');
const DECKMAP_GIVEN = argv.includes('--deck-map');
const DECKMAP_PATH = path.resolve(ROOT, arg('deck-map', 'research/catalog/deck-map.json'));
const OUT_DIR = path.resolve(ROOT, arg('out-dir', 'engine/styles'));
const TODAY = arg('today', new Intl.DateTimeFormat('en-CA').format(new Date())); // en-CA = YYYY-MM-DD, local time zone
const PART_SIZE = Number(arg('part-size', 6));
const PART_COLS = Number(arg('part-cols', 2));
const STATUSES = ['card-v1', 'next-wave', 'test-wave', 'retired'];
const PRODUCTIONS = ['html-native', 'image-native', 'hybrid'];
const DEFAULT_COOLDOWN = 14;

// ---------- data ----------
const median = (xs) => { const s = [...xs].sort((a, b) => a - b), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const round2 = (x) => Math.round(x * 100) / 100;
const resolvePath = (p) => (path.isAbsolute(p) ? p : path.resolve(ROOT, p));
const mmdd = (d) => (d ? d.slice(5) : '-');
const daysBetween = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / 86400000);
const addDays = (d, n) => new Date(Date.parse(d) + n * 86400000).toISOString().slice(0, 10);
const rel = (p) => path.relative(ROOT, p).replace(/\\/g, '/');

const catalog = JSON.parse(fs.readFileSync(STYLES_PATH, 'utf8'));
if (!Array.isArray(catalog.styles)) { console.error(`${rel(STYLES_PATH)} has no styles[] array`); process.exit(1); }

// The post log is optional and read only with --sync. Without it the gallery renders from styles.json.
let deckmap = null;
if (SYNC && fs.existsSync(DECKMAP_PATH)) {
  try { deckmap = JSON.parse(fs.readFileSync(DECKMAP_PATH, 'utf8')); } catch (e) { console.error(`cannot read post log ${rel(DECKMAP_PATH)}: ${e.message}`); process.exit(1); }
  if (!Array.isArray(deckmap)) { console.error(`post log ${rel(DECKMAP_PATH)} must be a JSON array of decks`); process.exit(1); }
} else if (SYNC && DECKMAP_GIVEN) {
  console.error(`no post log at ${rel(DECKMAP_PATH)}`); process.exit(1);
} else if (SYNC) {
  console.log(`no post log at ${rel(DECKMAP_PATH)}: nothing to sync (styles.json is left as is)`);
} else if (DECKMAP_GIVEN) {
  console.log('--deck-map is only read with --sync: rendering from styles.json as it is');
}
const posted = (deckmap ?? []).filter((e) => e.status === 'posted' && e.date).sort((a, b) => a.date.localeCompare(b.date));
const byCode = new Map((deckmap ?? []).filter((e) => e.code).map((e) => [e.code, e]));

function derive(style) {
  const covers = posted.filter((e) => e.cover_style === style.id);
  const scored = covers.filter((e) => e.mult != null);
  const best = [...scored].sort((a, b) => b.mult - a.mult)[0];
  return {
    posts: covers.map((e) => e.code ?? null),
    interior_posts: posted.filter((e) => e.interior_style === style.id).map((e) => e.code ?? null),
    drafts: deckmap.filter((e) => e.status !== 'posted' && (e.cover_style === style.id || e.interior_style === style.id))
      .map((e) => ({ folder: path.basename(e.folder ?? ''), date: e.date ?? null })),
    stats: {
      uses: covers.length,
      scored: scored.length,
      median_mult: scored.length ? Number(median(scored.map((e) => e.mult)).toFixed(2)) : null,
      best_mult: best ? best.mult : null,
      best_code: best ? best.code ?? null : null,
      last_used: covers.length ? covers[covers.length - 1].date : null,
      interior_uses: posted.filter((e) => e.interior_style === style.id).length,
    },
  };
}

// JSON with short primitive arrays and flat objects kept on one line, so styles.json stays diffable.
const inline = (x) => JSON.stringify(x, null, 1).replace(/\n\s*/g, ' ');
const isPrim = (x) => x === null || typeof x !== 'object';
const isFlatObj = (x) => x && typeof x === 'object' && !Array.isArray(x) && Object.values(x).every(isPrim);
function stringify(v, ind = '') {
  const inner = ind + '  ';
  if (Array.isArray(v)) {
    if (!v.length) return '[]';
    if (v.every(isPrim) && inline(v).length + inner.length <= 120) return inline(v);
    return '[\n' + v.map((x) => inner + (isPrim(x) || isFlatObj(x) ? inline(x) : stringify(x, inner))).join(',\n') + '\n' + ind + ']';
  }
  if (v && typeof v === 'object') {
    const ks = Object.keys(v);
    if (!ks.length) return '{}';
    return '{\n' + ks.map((k) => `${inner}${JSON.stringify(k)}: ${stringify(v[k], inner)}`).join(',\n') + '\n' + ind + '}';
  }
  return JSON.stringify(v);
}

// ---------- validate ----------
const problems = [];
const ids = new Set();
for (const s of catalog.styles) {
  if (ids.has(s.id)) problems.push(`${s.id}: duplicate id`);
  ids.add(s.id);
  if (!STATUSES.includes(s.status)) problems.push(`${s.id}: bad status ${s.status}`);
  if (!PRODUCTIONS.includes(s.production)) problems.push(`${s.id}: bad production ${s.production}`);
  if (catalog.spines) for (const sp of s.formats?.spines ?? []) if (!catalog.spines[sp]) problems.push(`${s.id}: unknown spine ${sp}`);
  for (const k of ['cover', 'interior']) {
    const p = s.exemplars?.[k];
    if (!p) problems.push(`${s.id}: no ${k} exemplar`);
    else if (!fs.existsSync(resolvePath(p))) problems.push(`${s.id}: ${k} exemplar missing: ${p}`);
  }
  if (s.template && !fs.existsSync(path.join(ROOT, s.template))) problems.push(`${s.id}: template missing: ${s.template}`);
}
for (const e of deckmap ?? []) for (const k of ['cover_style', 'interior_style'])
  if (e[k] && !ids.has(e[k])) problems.push(`post log ${e.code ?? e.folder}: ${k} ${e[k]} not in styles.json`);

// cooldown groups: one object or an array; every copy of a group id identical; every member carries it
const APPLIES_TO = ['cover', 'any'];
const groupsOf = (s) => (s.cooldown_group == null ? [] : [s.cooldown_group].flat());
const groupKey = (g) => JSON.stringify({ id: g.id, members: [...(g.members ?? [])].sort(), applies_to: g.applies_to, cap_days: g.cap_days });
const groups = new Map(); // id -> { def, from }
for (const s of catalog.styles) {
  const seen = new Set();
  for (const g of groupsOf(s)) {
    if (!g || typeof g !== 'object' || Array.isArray(g)) { problems.push(`${s.id}: cooldown_group entries must be objects`); continue; }
    const where = `${s.id} cooldown_group ${g.id ?? '(no id)'}`;
    if (typeof g.id !== 'string' || !g.id) problems.push(`${where}: needs a string id`);
    if (seen.has(g.id)) problems.push(`${where}: listed twice`);
    seen.add(g.id);
    if (!Array.isArray(g.members) || g.members.length < 2) problems.push(`${where}: members needs 2 or more style ids`);
    else {
      for (const m of g.members) if (!ids.has(m)) problems.push(`${where}: unknown member ${m}`);
      if (new Set(g.members).size !== g.members.length) problems.push(`${where}: duplicate member`);
      if (!g.members.includes(s.id)) problems.push(`${where}: ${s.id} carries the group but is not a member`);
    }
    if (!APPLIES_TO.includes(g.applies_to)) problems.push(`${where}: applies_to must be ${APPLIES_TO.join(' or ')}`);
    if (!Number.isInteger(g.cap_days) || g.cap_days < 1) problems.push(`${where}: cap_days must be a positive integer`);
    const prev = groups.get(g.id);
    if (!prev) groups.set(g.id, { def: g, from: s.id });
    else if (groupKey(prev.def) !== groupKey(g)) problems.push(`${where}: differs from ${prev.from}'s copy`);
  }
}
for (const [gid, { def }] of groups) for (const m of def.members ?? []) {
  const ms = catalog.styles.find((x) => x.id === m);
  if (ms && !groupsOf(ms).some((g) => g?.id === gid)) problems.push(`${m}: member of cooldown_group ${gid} but doesn't carry it`);
}

// ---------- sync (only with --sync and a post log) ----------
if (deckmap) {
  for (const s of catalog.styles) Object.assign(s, derive(s));
  const nextText = stringify(catalog) + '\n';
  const prev = fs.readFileSync(STYLES_PATH, 'utf8');
  if (prev !== nextText) { fs.writeFileSync(STYLES_PATH, nextText); console.log(`synced ${rel(STYLES_PATH)} from ${rel(DECKMAP_PATH)} (${posted.length} posted decks)`); }
  else console.log(`styles.json already in sync with ${rel(DECKMAP_PATH)}`);
}

// Render from a normalized view: a hand-written styles.json may have no stats / drafts / cooldown yet.
const BLANK_STATS = { uses: 0, scored: 0, median_mult: null, best_mult: null, best_code: null, last_used: null, interior_uses: 0 };
const styles = catalog.styles.map((s) => ({
  ...s,
  stats: { ...BLANK_STATS, ...(s.stats ?? {}) },
  drafts: Array.isArray(s.drafts) ? s.drafts : [],
  cooldown_days: s.cooldown_days ?? DEFAULT_COOLDOWN,
  exemplars: s.exemplars ?? {},
}));
const hasStats = styles.some((s) => s.stats.uses);

// A member's latest posted use that counts for a group: its cover, or (applies_to 'any') cover or interior.
function lastUse(id, appliesTo) {
  const hits = posted.filter((e) => e.cover_style === id || (appliesTo === 'any' && e.interior_style === id));
  const e = hits[hits.length - 1]; // posted is sorted by date
  return e ? { date: e.date, kind: e.cover_style === id ? 'cover' : 'interior' } : null;
}

// The latest-ending cooldown still running decides; `via` names the group use behind it (null = own cover).
function availability(s) {
  let until = null, via = null;
  const consider = (date, days, why) => {
    if (!date || daysBetween(date, TODAY) >= days) return;
    const end = addDays(date, days);
    if (!until || end > until) { until = end; via = why; }
  };
  consider(s.stats.last_used, s.cooldown_days, null);
  for (const g of groupsOf(s)) for (const m of g.members ?? []) {
    const u = lastUse(m, g.applies_to);
    if (u) consider(u.date, g.cap_days, { group: g.id, cap: g.cap_days, applies_to: g.applies_to, member: m, ...u });
  }
  if (until) {
    const base = `cooling until ${mmdd(until)}`;
    if (!via) return { cooling: true, text: base, tile: base };
    const who = via.member === s.id ? `own ${via.kind}` : `${via.member} ${via.kind}`;
    return {
      cooling: true,
      text: `${base} · group ${via.group} (${via.applies_to}, ${via.cap}d): ${who} ${mmdd(via.date)}`,
      tile: `${base} · ${via.member === s.id ? `${via.cap}d group cap` : `via ${via.member}`}`,
    };
  }
  const last = s.stats.last_used;
  const text = last ? `rested ${daysBetween(last, TODAY)}d` : deckmap ? 'never posted' : 'no posts logged';
  return { cooling: false, text, tile: text };
}

// table for the terminal / report
console.log(`\n| id | name | status | production | uses | median | best | last | availability (${TODAY}) |\n|---|---|---|---|---|---|---|---|---|`);
for (const s of styles) {
  const t = s.stats;
  console.log(`| ${s.id} | ${s.name} | ${s.status} | ${s.production} | ${t.uses} | ${t.median_mult?.toFixed(2) ?? '-'} | ${t.best_mult != null ? `${t.best_mult.toFixed(2)}${t.best_code ? ` ${t.best_code}` : ''}` : '-'} | ${t.last_used ?? '-'} | ${availability(s).text}${s.drafts.length ? ` · ${s.drafts.length} unposted draft(s)` : ''} |`);
}
if (groups.size) {
  console.log(`\n| cooldown group | members | applies to | cap | latest counted use | cooling until |\n|---|---|---|---|---|---|`);
  for (const [gid, { def }] of groups) {
    const uses = (def.members ?? []).map((m) => ({ m, u: lastUse(m, def.applies_to) })).filter((x) => x.u)
      .sort((a, b) => a.u.date.localeCompare(b.u.date));
    const latest = uses[uses.length - 1];
    const end = latest && addDays(latest.u.date, def.cap_days);
    console.log(`| ${gid} | ${(def.members ?? []).join(', ')} | ${def.applies_to} | ${def.cap_days}d | ${latest ? `${latest.m} ${latest.u.kind} ${latest.u.date}` : 'none posted'} | ${end && end > TODAY ? end : '-'} |`);
  }
}
if (problems.length) { console.log(`\nPROBLEMS (${problems.length}):\n- ` + problems.join('\n- ')); process.exit(1); }
if (flag('check')) process.exit(0);

// ---------- render ----------
const C = {
  sheet: '#0F0F0F', tile: '#1A1A1A', tileEdge: '#2B2B2B', box: '#050505',
  text: '#F2F2F2', sub: '#C9C9C9', dim: '#8E8E8E', cool: '#F2A65A',
};
const STATUS_STYLE = {
  'card-v1': { accent: '#EF8A62', chip: '#A9472A', label: 'CARD v1' },
  'next-wave': { accent: '#E9C46A', chip: '#6E5410', label: 'NEXT WAVE' },
  'test-wave': { accent: '#86BDF0', chip: '#1F5689', label: 'TEST WAVE' },
  retired: { accent: '#8A8A8A', chip: '#444444', label: 'RETIRED' },
};
const FONT = 'Segoe UI, Helvetica Neue, Arial';
const PAD = 26, ART_W = 360, ART_H = 450, GAP = 14;
const TILE_W = PAD * 2 + ART_W * 2 + GAP, INNER_W = TILE_W - PAD * 2;
// caption rows (top offsets inside the tile); the art starts below all of them
const ROW = { title: PAD, stats: PAD + 80, status: PAD + 128, labels: PAD + 176 };
const ART_Y = PAD + 212;
const TILE_H = ART_Y + ART_H + PAD;
const GUTTER = 24, MARGIN = 40;

const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const span = (t, { size, weight = 'normal', color = C.text, bg, family = FONT }) =>
  `<span font_desc="${family} ${size}" weight="${weight}" foreground="${color}"${bg ? ` background="${bg}"` : ''}>${esc(t)}</span>`;

const warnings = [];
// Render Pango markup; shrink (down to 60%) until it fits maxW, then hard-crop and warn.
async function textBlock(build, { maxW, wrapW, label }) {
  for (let scale = 1; ; scale = round2(scale - 0.04)) {
    const opts = { text: build(scale), rgba: true, dpi: 72 };
    if (wrapW) Object.assign(opts, { width: wrapW, wrap: 'word' });
    const { data, info } = await sharp({ text: opts }).png().toBuffer({ resolveWithObject: true });
    if (!maxW || info.width <= maxW) { if (scale < 1) warnings.push(`shrunk ${label} to ${Math.round(scale * 100)}%`); return { input: data, w: info.width, h: info.height }; }
    if (scale <= 0.6) {
      warnings.push(`OVERFLOW ${label}: ${info.width}px > ${maxW}px, cropped`);
      const cropped = await sharp(data).extract({ left: 0, top: 0, width: maxW, height: info.height }).png().toBuffer();
      return { input: cropped, w: maxW, h: info.height };
    }
  }
}

async function artPanel(p) {
  const src = resolvePath(p);
  const img = await sharp(src).resize(ART_W, ART_H, { fit: 'contain', background: C.box }).flatten({ background: C.box }).png().toBuffer();
  const meta = await sharp(src).metadata();
  return { input: img, ratio: meta.width / meta.height };
}

const fmtX = (m) => (m == null ? '-' : `${m.toFixed(2)}x`);
const spineLabel = (k) => String(catalog.spines?.[k] ?? '').replace(/\s*\(.*$/, '');
function statsLine(s) {
  const t = s.stats;
  const ev = s.evidence?.[0]; // evidence[0] is the headline reference
  if (ev && (s.status === 'test-wave' || !t.uses)) return `third-party reference · ${short(ev.likes)} likes / ${short(ev.comments)} comments`;
  if (t.uses) return `${t.uses} use${t.uses === 1 ? '' : 's'} · median ${fmtX(t.median_mult)} · best ${fmtX(t.best_mult)} · last ${mmdd(t.last_used)}`;
  const sp = s.formats?.spines ?? [];
  return sp.length ? `spine ${sp.map((k) => `${k} ${spineLabel(k)}`.trim()).join(' · ')}` : 'no posts logged yet';
}
const num = (v) => { if (v == null) return 0; const m = String(v).replace(/,/g, '').match(/([\d.]+)\s*([KM]?)/i); return m ? Number(m[1]) * (m[2].toUpperCase() === 'K' ? 1e3 : m[2].toUpperCase() === 'M' ? 1e6 : 1) : 0; };
const short = (v) => { const n = num(v); return n >= 1000 ? `${(n / 1000).toFixed(1).replace(/\.0$/, '')}K` : String(n); };

function artLabel(s, kind) {
  const code = s.exemplars[`${kind}_from`];
  const slide = kind === 'interior' && s.exemplars.interior_slide ? ` · slide ${s.exemplars.interior_slide}` : '';
  const own = code && byCode.get(code);
  if (own) return `${kind.toUpperCase()}${slide} · ${code} · ${fmtX(own.mult)}${own.interior_style && kind === 'interior' && own.interior_style !== s.id ? ` (${own.interior_style})` : ''}`;
  const ev = code && s.evidence?.find((e) => e.code === code);
  if (ev) return `${kind.toUpperCase()}${slide} · ${code} · ${short(ev.likes)} / ${short(ev.comments)}`;
  return `${kind.toUpperCase()}${slide}${code ? ` · ${code}` : ''}`;
}

async function renderTile(s) {
  const st = STATUS_STYLE[s.status];
  const av = availability(s);
  const comps = [];
  const put = (b, left, top) => comps.push({ input: b.input, left: Math.round(left), top: Math.round(top) });

  const title = await textBlock((k) => span(s.id, { size: Math.round(66 * k), weight: 'heavy', color: st.accent }) + span('  ', { size: Math.round(40 * k) }) + span(s.name, { size: Math.round(40 * k), weight: 'bold' }), { maxW: INNER_W, label: `${s.id} title` });
  put(title, PAD, ROW.title + Math.max(0, (62 - title.h) / 2));

  const stats = await textBlock((k) => span(statsLine(s), { size: Math.round(29 * k), weight: 'semibold', color: C.sub }), { maxW: INNER_W, label: `${s.id} stats` });
  put(stats, PAD, ROW.stats);

  const draftNote = s.drafts.length ? ` · ${s.drafts.length} unposted draft${s.drafts.length === 1 ? '' : 's'}` : '';
  const status = await textBlock((k) =>
    span(` ${st.label} `, { size: Math.round(25 * k), weight: 'bold', color: '#FFFFFF', bg: st.chip }) +
    span(`   ${s.production}   `, { size: Math.round(25 * k), weight: 'semibold', color: C.sub }) +
    span(av.tile + draftNote, { size: Math.round(25 * k), weight: av.cooling ? 'bold' : 'normal', color: av.cooling ? C.cool : C.dim }),
  { maxW: INNER_W, label: `${s.id} status` });
  put(status, PAD, ROW.status);

  for (const [i, kind] of ['cover', 'interior'].entries()) {
    const x = PAD + i * (ART_W + GAP);
    const lab = await textBlock((k) => span(artLabel(s, kind), { size: Math.round(18 * k), weight: 'semibold', color: C.dim }), { maxW: ART_W, label: `${s.id} ${kind} label` });
    put(lab, x, ROW.labels + 6);
    const art = await artPanel(s.exemplars[kind]);
    if (Math.abs(art.ratio - 0.8) > 0.02) warnings.push(`${s.id} ${kind} letterboxed (aspect ${art.ratio.toFixed(3)} vs 0.800)`);
    put(art, x, ART_Y);
  }
  const frame = Buffer.from(`<svg width="${TILE_W}" height="${TILE_H}"><rect x="0.5" y="0.5" width="${TILE_W - 1}" height="${TILE_H - 1}" rx="14" fill="${C.tile}" stroke="${C.tileEdge}"/></svg>`);
  return sharp(frame).composite(comps).png().toBuffer();
}

async function renderSheet(tiles, cols, heading, sub, file) {
  const rows = Math.ceil(tiles.length / cols);
  const W = MARGIN * 2 + cols * TILE_W + (cols - 1) * GUTTER;
  const head = await textBlock((k) => span(heading, { size: Math.round(54 * k), weight: 'heavy' }), { maxW: W - MARGIN * 2, label: `${path.basename(file)} heading` });
  const subB = await textBlock(() => span(sub, { size: 24, color: C.sub }), { wrapW: W - MARGIN * 2, label: `${path.basename(file)} sub` });
  const HEAD_H = MARGIN + head.h + 18 + subB.h + 32;
  const H = HEAD_H + rows * TILE_H + (rows - 1) * GUTTER + MARGIN;
  const comps = [{ input: head.input, left: MARGIN, top: MARGIN }, { input: subB.input, left: MARGIN, top: MARGIN + head.h + 18 }];
  tiles.forEach((t, i) => comps.push({ input: t, left: MARGIN + (i % cols) * (TILE_W + GUTTER), top: HEAD_H + Math.floor(i / cols) * (TILE_H + GUTTER) }));
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sharp({ create: { width: W, height: H, channels: 3, background: C.sheet } }).composite(comps).jpeg({ quality: 86, mozjpeg: true }).toFile(file);
  console.log(`wrote ${rel(file)} (${W}x${H}, ${tiles.length} tiles)`);
}

fs.mkdirSync(OUT_DIR, { recursive: true });
const hasEvidence = styles.some((s) => s.evidence?.length);
const statsKey = hasStats ? 'median = typical, best = ceiling. ' : '';

// --only S03,S01 [--out file.jpg]: just those tiles (in the order given), for a brief card. Full sheets are left alone.
const only = arg('only');
if (only) {
  const pick = only.split(',').map((id) => id.trim()).map((id) => styles.find((s) => s.id === id) ?? (console.error(`unknown style ${id}`), process.exit(1)));
  const out = path.resolve(ROOT, arg('out', path.join(OUT_DIR, `gallery-pick-${pick.map((s) => s.id).join('-')}.jpg`)));
  const pickTiles = [];
  for (const s of pick) pickTiles.push(await renderTile(s));
  await renderSheet(pickTiles, Math.min(2, pickTiles.length), `STYLE PICK · ${pick.map((s) => s.id).join(' / ')}`,
    `First = recommended, then the alternative. ${statsKey}Built ${TODAY}.`, out);
  if (warnings.length) console.log(`\nNOTES (${warnings.length}):\n- ` + warnings.join('\n- '));
  process.exit(0);
}

const shown = styles.filter((s) => flag('include-retired') || s.status !== 'retired')
  .sort((a, b) => a.id.localeCompare(b.id, 'en', { numeric: true }));
const tiles = [];
for (const s of shown) tiles.push(await renderTile(s));

const fullOut = path.resolve(ROOT, arg('out', path.join(OUT_DIR, 'gallery.jpg')));
const partStem = path.basename(fullOut).replace(/\.jpe?g$/i, '');
const scoredPosts = posted.filter((e) => e.mult != null).length;
const cooldowns = [...new Set(shown.map((s) => s.cooldown_days))];
const sub = `Pick by number: reply "S03". ` +
  (deckmap ? `Stats: your posted decks grouped by COVER style (${scoredPosts} scored posts in your post log). ` : '') +
  (hasStats ? `median = the typical result, best = the ceiling; trust the median. ` : 'Each tile shows the story spines the style fits, its status and production, then an exemplar cover and interior. ') +
  (hasEvidence ? `Third-party tiles show that creator's likes / comments, a different metric that is not comparable to x. ` : '') +
  (hasStats ? `Cooldown: a style posted in the last ${cooldowns.length === 1 ? cooldowns[0] : DEFAULT_COOLDOWN} days is cooling, and so is a style whose cooldown group (look-alikes in the feed) had a member post inside the group's cap ("via S08"). ` : '') +
  `Built ${TODAY}.`;
await renderSheet(tiles, 3, `STYLE GALLERY · ${shown.length} styles`, sub, fullOut);

const parts = !flag('parts') ? 0 : Math.ceil(tiles.length / PART_SIZE);
for (let p = 0; p < parts; p++) {
  const chunk = shown.slice(p * PART_SIZE, (p + 1) * PART_SIZE);
  await renderSheet(tiles.slice(p * PART_SIZE, (p + 1) * PART_SIZE), Math.min(PART_COLS, chunk.length),
    `STYLE GALLERY · part ${p + 1}/${parts} · ${chunk[0].id}–${chunk[chunk.length - 1].id}`,
    `Reply with a number ("S03"). ${statsKey}${hasEvidence ? 'Third-party tiles: likes / comments, not comparable to x. ' : ''}Built ${TODAY}.`,
    path.join(path.dirname(fullOut), `${partStem}-part-${p + 1}.jpg`));
}
// remove stale parts from a previous run with more styles (without --parts, existing parts are left alone)
const partRe = new RegExp(`^${partStem.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}-part-(\\d+)\\.jpg$`);
if (parts) for (const f of fs.readdirSync(path.dirname(fullOut))) {
  const m = f.match(partRe);
  if (m && Number(m[1]) > parts) { fs.unlinkSync(path.join(path.dirname(fullOut), f)); console.log(`removed stale ${f}`); }
}
if (warnings.length) console.log(`\nNOTES (${warnings.length}):\n- ` + warnings.join('\n- '));
