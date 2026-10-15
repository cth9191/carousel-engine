#!/usr/bin/env node
// Cold-reader gate (G8, engine/spines.md). A context-free Codex model reads ONLY the slide text
// of a storyboard and says what the thing is, why to care and the first step; a second Codex
// call grades that against storyboard.intent.
//
// Usage:  node shared/cold-reader.mjs <path/to/storyboard.json> [--dry]
//   --dry   print the reader input (slide text) and exit; no model calls, no writes.
// Exit:   0 pass · 2 fail · 1 error
//
// Writes: <deck dir>/cold-reader.json (or <name>.cold-reader.json for <name>.storyboard.json)
//         = {pass, reader, judge, codex_version, codex_bin, model, flags, wall_ms, usage, ...}
//         and updates the storyboard in place: cold_reader = that object, gates.G8 = {pass, note}.
// Prompts: engine/cold-reader-prompt.md (READER / JUDGE sections). Schemas: engine/cold-reader*.schema.json
//
// Codex invocation (verified 2026-10-14, codex-cli 0.162.1 from npm, ChatGPT login, Windows 11):
//   codex exec --ignore-user-config -m gpt-6.1-sol -c model_reasoning_effort="medium" -c service_tier="priority"
//     -c web_search="disabled" --disable apps --disable image_generation
//     -s read-only --skip-git-repo-check --ephemeral --json
//     --output-schema <schema> -o <tmp out> -C <empty tmp dir> -      (prompt on stdin, then closed)
//   - --ignore-user-config keeps auth (CODEX_HOME) and drops config.toml, so your own MCP servers and
//     tokens stay out of the reader.
//   - Without --disable apps, the ChatGPT "apps" connector still loads ~816 mcp__codex_apps__* tools
//     even with --ignore-user-config. --disable image_generation removes image_gen entirely.
//   - With these flags the model sees no MCP tools and no web search (probe-confirmed).
// Binary: CODEX_BIN if set, else the `codex` on PATH (the Codex CLI: npm i -g @openai/codex, then
// `codex login`). On Windows that is an npm shim, so we run its codex.js with this node.
// Fallback (Windows): the newest Codex desktop-app binary at %LOCALAPPDATA%/OpenAI/Codex/bin/<hash>/codex.exe,
// used when no codex is on PATH, or retried once when the PATH codex rejects the model as unsupported.
// Hash dirs only: a top-level bin/codex.exe, if present, can be an older build.
// Model settings: CODEX_MODEL (default gpt-6.1-sol), CODEX_EFFORT (medium), CODEX_TIER (priority).
// CODEX_BIN=<path to codex or codex.js> picks the binary. CODEX_HOME (the Codex CLI's home, default
// ~/.codex) is passed through: auth is read from there, and --ephemeral means no session rollout is kept.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PROMPT_FILE = path.join(ROOT, 'engine', 'cold-reader-prompt.md');
const READER_SCHEMA = path.join(ROOT, 'engine', 'cold-reader.schema.json');
const JUDGE_SCHEMA = path.join(ROOT, 'engine', 'cold-reader-judge.schema.json');
const MODEL = process.env.CODEX_MODEL || 'gpt-6.1-sol';
const EFFORT = process.env.CODEX_EFFORT || 'medium';
// Fast mode: Sol 6.1's only extra tier is "priority" = Fast, 2x speed, more usage.
const TIER = process.env.CODEX_TIER || 'priority';
const TIMEOUT_MS = 300_000;
const FLAGS = [
  'exec', '--ignore-user-config', '-m', MODEL,
  '-c', `model_reasoning_effort="${EFFORT}"`, '-c', `service_tier="${TIER}"`, '-c', 'web_search="disabled"',
  '--disable', 'apps', '--disable', 'image_generation',
  '-s', 'read-only', '--skip-git-repo-check', '--ephemeral', '--json',
];

class Fail extends Error {}

// ---------- input ----------

const norm = (s) => String(s ?? '').replace(/\s+/g, ' ').trim().toLowerCase();

// Reader input: per slide, the headline, each visible string once, and evidence.describe in
// brackets. Roles, places, lesson, sources, intent and glossary are never sent. Three place values
// are reserved: "headline" (every headline line; already shown) and "counter" ("03 / 09") are
// skipped, and a "chrome" string (brand header/footer) is shown only on the first slide where it
// appears. Any other place is free-form and its text is sent as is.
export function readerInput(sb) {
  const slides = sb.slides || [];
  const total = slides.length;
  const chromeSeen = new Set();
  return slides.map((s, i) => {
    const n = s.n ?? i + 1;
    const out = [`--- SLIDE ${n} of ${total} ---`];
    if (s.headline) out.push(`Headline: ${s.headline}`);
    const seen = new Set([norm(s.headline)]);
    const lines = [];
    for (const st of s.strings || []) {
      if (!st || !st.text || st.place === 'headline' || st.place === 'counter') continue;
      const k = norm(st.text);
      if (seen.has(k)) continue;
      if (st.place === 'chrome') {
        if (chromeSeen.has(k)) continue;
        chromeSeen.add(k);
      }
      seen.add(k);
      lines.push(`- ${st.text}`);
    }
    if (lines.length) out.push('Text:', ...lines);
    const d = s.evidence && s.evidence.describe;
    if (d) out.push(`[${String(d).replace(/^\[|\]$/g, '')}]`);
    return out.join('\n');
  }).join('\n\n');
}

function promptSection(name) {
  const md = fs.readFileSync(PROMPT_FILE, 'utf8');
  const m = md.match(new RegExp(`<!-- ${name} PROMPT START -->\\r?\\n([\\s\\S]*?)<!-- ${name} PROMPT END -->`));
  if (!m) throw new Fail(`no ${name} section in ${PROMPT_FILE}`);
  return m[1].trim() + '\n';
}

const fill = (tmpl, vars) => tmpl.replace(/\{\{(\w+)\}\}/g, (_, k) => {
  if (!(k in vars)) throw new Fail(`prompt placeholder {{${k}}} has no value`);
  return vars[k];
});

// ---------- codex binary ----------

function findOnPath(names) {
  for (const dir of (process.env.PATH || '').split(path.delimiter)) {
    for (const n of names) {
      const p = path.join(dir, n);
      try { if (fs.statSync(p).isFile()) return p; } catch { /* keep looking */ }
    }
  }
  return null;
}

function asBin(p, label) {
  if (/\.(c?js|mjs)$/i.test(p)) return { cmd: process.execPath, pre: [p], label, path: p };
  return { cmd: p, pre: [], label, path: p };
}

function pathCodex() {
  if (process.env.CODEX_BIN) return asBin(process.env.CODEX_BIN, 'CODEX_BIN');
  if (process.platform !== 'win32') {
    const p = findOnPath(['codex']);
    return p ? asBin(p, 'PATH') : null;
  }
  // Windows: npm installs codex.cmd / codex.ps1 shims next to node_modules/@openai/codex.
  const shim = findOnPath(['codex.cmd', 'codex.exe', 'codex']);
  if (!shim) return null;
  if (/\.exe$/i.test(shim)) return asBin(shim, 'PATH');
  const js = path.join(path.dirname(shim), 'node_modules', '@openai', 'codex', 'bin', 'codex.js');
  return fs.existsSync(js) ? asBin(js, 'PATH (npm)') : null;
}

function desktopCodex() {
  if (process.platform !== 'win32') return null;
  const base = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'), 'OpenAI', 'Codex', 'bin');
  let best = null;
  try {
    for (const d of fs.readdirSync(base, { withFileTypes: true })) {
      if (!d.isDirectory()) continue; // skips a top-level bin/codex.exe (can be an older build)
      const exe = path.join(base, d.name, 'codex.exe');
      try {
        const t = fs.statSync(exe).mtimeMs;
        if (!best || t > best.t) best = { exe, t };
      } catch { /* no codex.exe in this hash dir */ }
    }
  } catch { return null; }
  return best ? asBin(best.exe, 'desktop app') : null;
}

const homeRel = (p) => {
  const h = os.homedir();
  return h && p.toLowerCase().startsWith(h.toLowerCase()) ? `~${p.slice(h.length)}` : p;
};

function version(bin) {
  const r = spawnSync(bin.cmd, [...bin.pre, '--version'], { encoding: 'utf8', windowsHide: true, timeout: 30_000 });
  return (r.stdout || r.stderr || '').trim() || `unknown (exit ${r.status})`;
}

// ---------- one codex call ----------

function runCodex(bin, prompt, schema, tmp, tag) {
  const out = path.join(tmp, `${tag}.out.json`);
  const empty = path.join(tmp, 'empty');
  const args = [...bin.pre, ...FLAGS, '--output-schema', schema, '-o', out, '-C', empty, '-'];
  const t0 = Date.now();
  return new Promise((resolve) => {
    const child = spawn(bin.cmd, args, { stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true });
    let stdout = '', stderr = '', timedOut = false;
    const timer = setTimeout(() => { timedOut = true; child.kill(); }, TIMEOUT_MS);
    child.stdout.on('data', (d) => { stdout += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', (e) => { stderr += `\nspawn error: ${e.message}`; });
    child.on('close', (code) => {
      clearTimeout(timer);
      const wall_ms = Date.now() - t0;
      fs.writeFileSync(path.join(tmp, `${tag}.events.jsonl`), stdout);
      fs.writeFileSync(path.join(tmp, `${tag}.stderr.txt`), stderr);
      let usage = null, thread_id = null, lastMsg = null;
      const errors = [];
      for (const line of stdout.split(/\r?\n/)) {
        if (!line.trim().startsWith('{')) continue;
        let ev; try { ev = JSON.parse(line); } catch { continue; }
        if (ev.type === 'thread.started') thread_id = ev.thread_id;
        if (ev.type === 'turn.completed' && ev.usage) usage = ev.usage;
        if (ev.type === 'item.completed' && ev.item && ev.item.type === 'agent_message') lastMsg = ev.item.text;
        if (ev.type === 'error' || ev.type === 'turn.failed') errors.push(ev.message || (ev.error && ev.error.message) || JSON.stringify(ev));
      }
      let json = null;
      const raw = fs.existsSync(out) ? fs.readFileSync(out, 'utf8') : lastMsg;
      if (raw) { try { json = JSON.parse(raw); } catch { /* reported below */ } }
      resolve({ code, timedOut, wall_ms, usage, thread_id, json, raw, errors, stderr });
    });
    child.stdin.on('error', () => { /* child exited early; reported via close */ });
    child.stdin.end(prompt, 'utf8'); // stdin must be closed or `codex exec` hangs
  });
}

const modelRejected = (r) => /model/i.test(r.stderr + r.errors.join(' ')) &&
  /(not supported|unsupported|does not exist|not found|not available|invalid model)/i.test(r.stderr + r.errors.join(' '));

function describeFailure(tag, r) {
  const why = r.timedOut ? `timed out after ${TIMEOUT_MS / 1000}s`
    : r.json ? 'unexpected' : r.raw ? 'output is not JSON' : `exit ${r.code}, no output`;
  const detail = (r.errors.join(' | ') || r.stderr.trim().split(/\r?\n/).slice(-5).join(' | ')).slice(0, 800);
  return `${tag} call failed: ${why}${detail ? ` :: ${detail}` : ''}`;
}

// ---------- gate ----------

function ruleCheck(j) {
  const grades = [j.what_match, j.why_match, j.first_step_match].map((m) => m && m.match);
  const problems = [];
  if (grades.includes('no')) problems.push('a match is "no"');
  if (grades.filter((g) => g === 'partial').length > 1) problems.push('more than one "partial"');
  if ((j.undefined_terms_blocking || []).length) problems.push('blocking undefined terms');
  return problems;
}

function outPathFor(sbPath) {
  const dir = path.dirname(sbPath);
  const base = path.basename(sbPath);
  if (base === 'storyboard.json') return path.join(dir, 'cold-reader.json');
  return path.join(dir, `${base.replace(/\.?storyboard\.json$/i, '').replace(/\.json$/i, '') || 'deck'}.cold-reader.json`);
}

async function main() {
  const argv = process.argv.slice(2);
  const dry = argv.includes('--dry');
  const sbArg = argv.find((a) => !a.startsWith('--'));
  if (!sbArg) throw new Fail('usage: node shared/cold-reader.mjs <path/to/storyboard.json> [--dry]');
  const sbPath = path.resolve(sbArg);
  let sb;
  try { sb = JSON.parse(fs.readFileSync(sbPath, 'utf8')); } catch (e) { throw new Fail(`cannot read storyboard ${sbPath}: ${e.message}`); }
  if (!Array.isArray(sb.slides) || !sb.slides.length) throw new Fail('storyboard has no slides[]');

  const slides = readerInput(sb);
  if (dry) { process.stdout.write(slides + '\n'); return 0; }

  const intent = sb.intent || {};
  for (const k of ['what', 'why', 'first_step']) if (!intent[k]) throw new Fail(`storyboard.intent.${k} is missing`);

  let bin = pathCodex() || desktopCodex();
  if (!bin) throw new Fail('no codex binary found: install the Codex CLI (npm i -g @openai/codex) so `codex` is on PATH, or set CODEX_BIN');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'cold-reader-'));
  fs.mkdirSync(path.join(tmp, 'empty'));
  const notes = [];

  const call = async (tag, prompt, schema) => {
    let r = await runCodex(bin, prompt, schema, tmp, tag);
    if (!r.json && modelRejected(r)) {
      const alt = desktopCodex();
      if (alt && alt.path !== bin.path) {
        notes.push(`${bin.label} codex rejected ${MODEL}; switched to ${alt.path}`);
        bin = alt;
        r = await runCodex(bin, prompt, schema, tmp, `${tag}-retry`);
      }
    }
    if (!r.json) throw new Fail(`${describeFailure(tag, r)} (logs: ${tmp})`);
    return r;
  };

  const t0 = Date.now();
  const reader = await call('reader', fill(promptSection('READER'), { SLIDES: slides }), READER_SCHEMA);
  const judge = await call('judge', fill(promptSection('JUDGE'), {
    SLIDES: slides,
    INTENT: JSON.stringify({ what: intent.what, why: intent.why, first_step: intent.first_step }, null, 2),
    READER: JSON.stringify(reader.json, null, 2),
  }), JUDGE_SCHEMA);
  const total_ms = Date.now() - t0;

  const j = judge.json;
  const problems = ruleCheck(j);
  const pass = j.verdict === 'pass' && problems.length === 0;
  if (j.verdict === 'pass' && problems.length) notes.push(`judge said pass but the rule fails: ${problems.join(', ')}`);
  if (j.verdict === 'fail' && !problems.length) notes.push('judge said fail although the rule alone would pass');

  const grades = `what ${j.what_match.match} · why ${j.why_match.match} · first_step ${j.first_step_match.match}`;
  const blocking = (j.undefined_terms_blocking || []).map((t) => `${t.term} (s${t.slide})`);
  const note = `${grades} · ${blocking.length ? `blocking: ${blocking.join(', ')}` : 'no blocking terms'}` +
    (pass ? '' : ` · fix: ${(j.fix_hints || [])[0] || problems.join(', ')}`);

  const result = {
    pass,
    ran_at: new Date().toISOString(),
    model: MODEL,
    reasoning_effort: EFFORT,
    codex_version: version(bin),
    codex_bin: homeRel(bin.path), // ~-relative, so a published deck doesn't carry your user folder
    flags: FLAGS.join(' '),
    wall_ms: { reader: reader.wall_ms, judge: judge.wall_ms, total: total_ms },
    usage: { reader: reader.usage, judge: judge.usage },
    notes,
    reader: reader.json,
    judge: j,
    reader_input: slides,
  };

  const outFile = outPathFor(sbPath);
  fs.writeFileSync(outFile, JSON.stringify(result, null, 2) + '\n');
  sb.cold_reader = result;
  sb.gates = sb.gates && typeof sb.gates === 'object' ? sb.gates : {};
  sb.gates.G8 = { pass, note };
  fs.writeFileSync(sbPath, JSON.stringify(sb, null, 2) + '\n');
  fs.rmSync(tmp, { recursive: true, force: true });

  const s = (ms) => `${(ms / 1000).toFixed(1)}s`;
  const row = (k, m) => `  ${k.padEnd(11)} ${m.match.padEnd(8)} ${m.reason}`;
  console.log(`G8 cold reader: ${pass ? 'PASS' : 'FAIL'}   (reader ${s(reader.wall_ms)}, judge ${s(judge.wall_ms)}; ${result.codex_version}, ${bin.label})`);
  console.log(`  reader saw: ${reader.json.summary}`);
  console.log(row('what', j.what_match));
  console.log(row('why', j.why_match));
  console.log(row('first_step', j.first_step_match));
  console.log(`  blocking terms: ${blocking.length ? blocking.join(', ') : 'none'}`);
  const flagged = (reader.json.undefined_terms || []).map((t) => `${t.term} (s${t.slide}${t.impact === 'blocking' ? ', blocking' : ''})`);
  if (flagged.length) console.log(`  reader flagged: ${flagged.join(', ')}`);
  for (const h of j.fix_hints || []) console.log(`  fix: ${h}`);
  for (const n of notes) console.log(`  note: ${n}`);
  console.log(`  wrote ${path.relative(process.cwd(), outFile)} and gates.G8 in ${path.relative(process.cwd(), sbPath)}`);
  return pass ? 0 : 2;
}

main().then((code) => { process.exitCode = code; }).catch((e) => {
  console.error(`cold-reader: ${e instanceof Fail ? e.message : e.stack || e}`);
  process.exitCode = 1;
});
