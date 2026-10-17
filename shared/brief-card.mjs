#!/usr/bin/env node
// Render the brief card (touch 1: the one message the user approves before any image exists)
// from a deck's storyboard.json + cold-reader.json + engine/styles/styles.json.
//
// Usage: node shared/brief-card.mjs <carousels/<deck>/storyboard.json> [--style S01] [--alt S11] [--out <path>]
// Writes <deck dir>/brief-card.md (or --out) and prints it. Format: engine/templates/brief-card.md.
// The storyboard column shows every string except the reserved places "headline" (its own column),
// "counter" (NN / TT) and "chrome" (brand header/footer).
// The role column adds the slide's style layout ("item · dossier") and ★ marks the star slide;
// a format:"single" storyboard is labelled as a single image.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const sbPath = args.find(a => !a.startsWith('--'));
const opt = k => { const i = args.indexOf(`--${k}`); return i >= 0 ? args[i + 1] : null; };
if (!sbPath || !fs.existsSync(sbPath)) {
  console.error('usage: node shared/brief-card.mjs <storyboard.json> [--style S01] [--alt S11] [--out path]');
  process.exit(1);
}

const sb = JSON.parse(fs.readFileSync(sbPath, 'utf8'));
const deckDir = path.dirname(sbPath);
const crPath = path.join(deckDir, path.basename(sbPath).replace(/storyboard\.json$/, 'cold-reader.json'));
const cr = sb.cold_reader || (fs.existsSync(crPath) ? JSON.parse(fs.readFileSync(crPath, 'utf8')) : null);
const styles = JSON.parse(fs.readFileSync(path.join(ROOT, 'engine/styles/styles.json'), 'utf8'));
const styleList = Array.isArray(styles) ? styles : styles.styles || Object.values(styles);
const findStyle = id => styleList.find(s => s.id === id);

const esc = t => String(t ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
const SKIP = new Set(['chrome', 'counter', 'headline']);
const score = h => (h?.score?.total != null ? `${h.score.total}/12` : '—');

function styleLine(id, label) {
  const s = findStyle(id);
  if (!s) return `${label}: ${id ?? '—'} (not in styles.json)`;
  const st = s.stats || {};
  const stats = st.uses ? `${st.uses} uses · median ${st.median_mult ?? '—'}x · best ${st.best_mult ?? '—'}x · last ${st.last_used ?? '—'}`
    : ([st.last_used && `last used ${st.last_used}`, s.evidence_note].filter(Boolean).join(' · ') || 'no posts logged yet');
  return `${label}: **${s.id} ${s.name}**: ${stats} · ${s.production} · ${s.one_line ?? ''}`;
}

const L = [];
const dl = sb.deliverable || {};
L.push(`# Brief card: ${sb.topic}`, '');
const shape = sb.format === 'single' ? 'single image (format single)' : `${sb.slides.length} slides`;
L.push(`**${sb.topic}** · spine ${sb.spine} · ${shape} · keyword **${sb.keyword}** → ${dl.name ?? '—'} (${dl.exists ? 'exists' : 'needs building'})`, '');

L.push('### Hooks', '', '| | Main line · kicker | Visual promise | Formula | Score |', '|---|---|---|---|---|');
L.push(`| ★1 | "${esc(sb.hook.main)}" · "${esc(sb.hook.kicker)}" | ${esc(sb.hook.visual_promise)} | ${sb.hook.formula} | ${score(sb.hook)} |`);
(sb.alt_hooks || []).slice(0, 2).forEach((h, i) =>
  L.push(`| ${i + 2} | "${esc(h.main)}" · "${esc(h.kicker)}" | ${esc(h.visual_promise ?? h.note ?? '')} | ${h.formula ?? ''} | ${score(h)} |`));
if (sb.hook.score?.note) L.push('', `Why ★1: ${sb.hook.score.note}`);
L.push('');

L.push('### Storyboard', '', '| # | Role | Headline | Everything else on the slide (verbatim) | Evidence |', '|---|---|---|---|---|');
for (const s of sb.slides) {
  const rest = (s.strings || []).filter(x => !SKIP.has(x.place)).map(x => `${x.text}`).join(' / ');
  const ev = s.evidence ? `${s.evidence.kind?.toUpperCase()}: ${s.evidence.describe}` : '—';
  L.push(`| ${s.n}${s.star ? ' ★' : ''} | ${s.role}${s.layout ? ` · ${s.layout}` : ''} | **${esc(s.headline)}** | ${esc(rest)} | ${esc(ev)} |`);
}
L.push('');
if (sb.gates?.G5?.note) L.push(`**Spine test:** ${sb.gates.G5.note}`, '');

L.push('### Gates', '');
const g = sb.gates || {};
L.push(['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'].map(k => `${k} ${g[k] ? (g[k].pass ? '✓' : '✗') : '·'}`).join(' · '));
for (const k of Object.keys(g)) if (g[k] && (!g[k].pass || /WARNING|⚠/.test(g[k].note || ''))) L.push(`- ${k}: ${g[k].note}`);
L.push('');

if (cr) {
  const r = cr.reader || {}, j = cr.judge || {};
  const val = x => (typeof x === 'object' && x ? x.answer ?? x.text ?? JSON.stringify(x) : x);
  L.push('**Cold reader** (another model with no context reads only the slide text):', '');
  L.push('| | Intended | Reader recovered | Grade |', '|---|---|---|---|');
  for (const k of ['what', 'why', 'first_step']) {
    const grade = j[`${k}_match`];
    L.push(`| ${k.replace('_', ' ')} | ${esc(sb.intent?.[k])} | ${esc(val(r[k]))} | ${esc(typeof grade === 'object' ? grade?.grade ?? grade?.match : grade)} |`);
  }
  const blocking = (j.undefined_terms_blocking || []).map(t => t.term || t).join(', ') || 'none';
  L.push('', `Blocking terms: ${blocking} · Verdict: **${(j.verdict || (cr.pass ? 'pass' : 'fail')).toUpperCase()}**`, '');
}

L.push('### Style', '');
L.push(styleLine(opt('style') || sb.style, 'Recommended'));
if (opt('alt')) L.push('', styleLine(opt('alt'), 'Alternative'));
L.push('', '### Caption', '', '```', sb.caption || '', '```', '');
if (sb.deviations?.length) L.push('### Deviations (logged)', '', ...sb.deviations.map(d => `- ${d}`), '');

const out = opt('out') || path.join(deckDir, 'brief-card.md');
fs.writeFileSync(out, L.join('\n'), 'utf8');
console.log(L.join('\n'));
console.error(`\nwrote ${path.relative(process.cwd(), out)}`);
