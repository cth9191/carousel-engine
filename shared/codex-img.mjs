#!/usr/bin/env node
// Codex image worker. Claude writes the prompts; Codex only makes pixels.
//
//   node shared/codex-img.mjs gen <jobs.json> [--only id1,id2] [--concurrency 4]
//   node shared/codex-img.mjs board <out.jpg> <img1>=<label1> <img2>=<label2> ... [--cols 2] [--w 540] [--title "..."]
//
// jobs.json:
//   { "deck": "carousels/<id>",            // paths below are relative to this (or absolute)
//     "model": "gpt-6.1-sol", "effort": "high", "tier": "priority",   // per jobs file; these are the defaults
//     "concurrency": 4,
//     "jobs": [ { "id": "cover-a", "prompt_file": "prompts/cover-a.txt",
//                 "refs": ["refs/style.png", "..."], "out": "plates/cover-a.png" } ] }
//
// Each job is ONE separate `codex exec` session (image calls inside one session run serially), started
// 2 s apart (simultaneous starts race on system-skill install). The worker prompt tells Codex to call
// its image tool exactly once with the given prompt and references, and nothing else. The PNG is found via
// thread_id -> $CODEX_HOME/generated_images/<thread_id>/ (--json has no image event), copied to `out`
// with a version suffix (plate-03.png, then plate-03.v2.png ...; never overwritten), and logged to
// <deck>/runs/runs.jsonl. An edit is just another job whose first ref is the plate to change.
// CODEX_HOME is the Codex CLI's own variable (default ~/.codex); the worker inherits it, so images and
// session rollouts ($CODEX_HOME/sessions/, named by thread id) land where your Codex keeps them.
// runs.jsonl holds ~-relative local paths and Codex thread ids: it is gitignored. Per-job logs go to
// <deck>/runs/logs/. On the worked example a job took about 46 s (29-57 s) and about 50K tokens.
//
// Flags (Codex CLI 0.162.x): --ignore-user-config (keeps your own MCP servers and tokens out of the
// worker, so it can't reach for another image tool) --disable apps (drops ~816 ChatGPT connector tools)
// -c web_search="disabled" -s <sandbox> -C <empty dir>, prompt on stdin (closed, or exec hangs).
// Sandbox defaults to read-only; set CODEX_IMG_SANDBOX=workspace-write if image generation needs it.
//
// Binary: CODEX_BIN if set, else the `codex` on PATH (the Codex CLI: npm i -g @openai/codex, then
// `codex login`). On Windows that is an npm shim, so its codex.js runs with this node. Only if no
// codex is on PATH (Windows): the newest Codex desktop-app binary under
// %LOCALAPPDATA%/OpenAI/Codex/bin/<hash>/codex.exe. Same resolution as shared/cold-reader.mjs.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CODEX_HOME = process.env.CODEX_HOME ? path.resolve(process.env.CODEX_HOME) : path.join(os.homedir(), '.codex');
const GEN_DIR = path.join(CODEX_HOME, 'generated_images');
const TIMEOUT_MS = 900_000;
const STAGGER_MS = 2_000;

// ---------- codex binary: CODEX_BIN, then PATH, then (Windows) the desktop app ----------
function findOnPath(names) {
  for (const dir of (process.env.PATH || '').split(path.delimiter)) {
    for (const n of names) {
      const p = path.join(dir, n);
      try { if (fs.statSync(p).isFile()) return p; } catch { /* keep looking */ }
    }
  }
  return null;
}
const asBin = (p, label) => (/\.(c?js|mjs)$/i.test(p) ? { cmd: process.execPath, pre: [p], label, path: p } : { cmd: p, pre: [], label, path: p });
function resolveCodex() {
  if (process.env.CODEX_BIN) return asBin(process.env.CODEX_BIN, 'CODEX_BIN');
  if (process.platform !== 'win32') { const p = findOnPath(['codex']); return p ? asBin(p, 'PATH') : null; }
  const shim = findOnPath(['codex.cmd', 'codex.exe', 'codex']);
  if (!shim) return null;
  if (/\.exe$/i.test(shim)) return asBin(shim, 'PATH');
  const js = path.join(path.dirname(shim), 'node_modules', '@openai', 'codex', 'bin', 'codex.js');
  return fs.existsSync(js) ? asBin(js, 'PATH (npm)') : null;
}
// Fallback when no codex is on PATH: the newest Codex desktop-app binary (Windows layout). Hash dirs
// only; a top-level bin/codex.exe, if present, can be an older build.
function desktopCodex() {
  if (process.platform !== 'win32') return null;
  const base = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'), 'OpenAI', 'Codex', 'bin');
  let best = null;
  try {
    for (const d of fs.readdirSync(base, { withFileTypes: true })) {
      if (!d.isDirectory()) continue;
      const exe = path.join(base, d.name, 'codex.exe');
      try { const t = fs.statSync(exe).mtimeMs; if (!best || t > best.t) best = { exe, t }; } catch { /* no codex.exe here */ }
    }
  } catch { return null; }
  return best ? asBin(best.exe, 'desktop app') : null;
}
const codexVersion = (bin) => {
  const r = spawnSync(bin.cmd, [...bin.pre, '--version'], { encoding: 'utf8', windowsHide: true, timeout: 30_000 });
  return (r.stdout || r.stderr || '').trim();
};

// ---------- helpers ----------
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// ~-relative path for logs, so runs.jsonl doesn't carry your user folder
const homeRel = (p) => { const h = os.homedir(); return h && p.toLowerCase().startsWith(h.toLowerCase()) ? `~${p.slice(h.length)}` : p; };
const abs = (base, p) => (path.isAbsolute(p) ? p : path.resolve(base, p));
function versioned(out) {
  if (!fs.existsSync(out)) return out;
  const ext = path.extname(out), stem = out.slice(0, -ext.length);
  for (let v = 2; ; v++) { const c = `${stem}.v${v}${ext}`; if (!fs.existsSync(c)) return c; }
}
function pngSize(file) {
  const b = fs.readFileSync(file);
  return b.slice(1, 4).toString() === 'PNG' ? { w: b.readUInt32BE(16), h: b.readUInt32BE(20) } : null;
}

function workerPrompt(imagePrompt, refs) {
  const refLines = refs.length
    ? refs.map((r, i) => `  ${i + 1}. ${r}`).join('\n')
    : '  (none)';
  return [
    'You are an image-generation worker. Do exactly this and nothing else:',
    '- Call your image generation tool exactly ONE time.',
    '- Pass the IMAGE PROMPT below as the prompt, verbatim, without rewriting, shortening or adding to it.',
    refs.length ? '- Pass these local files as referenced_image_paths, in exactly this order:' : '- Do not pass any reference images.',
    refLines,
    '- Do not read files, run shell commands, browse, or load skills. Do not write any files.',
    '- When the image has been generated, reply with the single word DONE.',
    '',
    'IMAGE PROMPT:',
    '<<<PROMPT',
    imagePrompt.trim(),
    'PROMPT>>>',
  ].join('\n');
}

function runJob(bin, cfg, job, deckDir, runDir) {
  const prompt = fs.readFileSync(abs(deckDir, job.prompt_file), 'utf8');
  const refs = (job.refs || []).map((r) => abs(deckDir, r));
  for (const r of refs) if (!fs.existsSync(r)) return Promise.resolve({ id: job.id, status: 'error', error: `missing ref ${r}` });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), `codex-img-${job.id}-`));
  const args = [...bin.pre, 'exec', '--ignore-user-config', '-m', cfg.model,
    '-c', `model_reasoning_effort="${cfg.effort}"`, '-c', `service_tier="${cfg.tier}"`,
    '-c', 'web_search="disabled"', '--disable', 'apps',
    '-s', process.env.CODEX_IMG_SANDBOX || 'read-only', '--skip-git-repo-check', '--json', '-C', tmp, '-'];
  for (const r of (job.attach === false ? [] : refs)) args.splice(args.length - 1, 0, '-i', r);
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
      fs.writeFileSync(path.join(runDir, `${job.id}.events.jsonl`), stdout);
      fs.writeFileSync(path.join(runDir, `${job.id}.stderr.txt`), stderr);
      fs.rmSync(tmp, { recursive: true, force: true }); // the empty -C dir
      let thread_id = null, usage = null, lastMsg = null;
      const errors = [];
      for (const line of stdout.split(/\r?\n/)) {
        if (!line.trim().startsWith('{')) continue;
        let ev; try { ev = JSON.parse(line); } catch { continue; }
        if (ev.type === 'thread.started') thread_id = ev.thread_id;
        if (ev.type === 'turn.completed' && ev.usage) usage = ev.usage;
        if (ev.type === 'item.completed' && ev.item?.type === 'agent_message') lastMsg = ev.item.text;
        if (ev.type === 'error' || ev.type === 'turn.failed') errors.push(ev.message || ev.error?.message || JSON.stringify(ev));
      }
      const rec = { id: job.id, thread_id, code, timedOut, wall_ms, usage, last_message: lastMsg, errors };
      const dir = thread_id ? path.join(GEN_DIR, thread_id) : null;
      const pngs = dir && fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => /\.png$/i.test(f))
        .map((f) => ({ f: path.join(dir, f), t: fs.statSync(path.join(dir, f)).mtimeMs })).sort((a, b) => a.t - b.t) : [];
      if (!pngs.length) {
        resolve({ ...rec, status: 'error', error: timedOut ? 'timed out' : `no image in ${dir ? homeRel(dir) : '(no thread id)'};${errors.join(' | ') || stderr.split('\n').filter((l) => /error/i.test(l)).slice(-2).join(' | ')}` });
        return;
      }
      const src = pngs[pngs.length - 1].f;
      const out = versioned(abs(deckDir, job.out));
      fs.mkdirSync(path.dirname(out), { recursive: true });
      fs.copyFileSync(src, out);
      resolve({ ...rec, status: 'ok', images_in_thread: pngs.length, saved_path: homeRel(src), out: path.relative(deckDir, out).replace(/\\/g, '/'), size: pngSize(out) });
    });
    child.stdin.on('error', () => {});
    child.stdin.end(workerPrompt(prompt, refs), 'utf8');
  });
}

async function gen(jobsPath, opts) {
  const spec = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
  const deckDir = abs(ROOT, spec.deck || path.dirname(jobsPath));
  const cfg = { model: spec.model || 'gpt-6.1-sol', effort: spec.effort || 'high', tier: spec.tier || 'priority' };
  const only = opts.only ? new Set(opts.only.split(',')) : null;
  const jobs = spec.jobs.filter((j) => !only || only.has(j.id));
  const conc = Number(opts.concurrency || spec.concurrency || 4);
  const bin = resolveCodex() || desktopCodex();
  if (!bin) throw new Error('codex not found: install the Codex CLI (npm i -g @openai/codex) so `codex` is on PATH, or set CODEX_BIN');
  const ver = codexVersion(bin);
  const runDir = path.join(deckDir, 'runs', 'logs');
  fs.mkdirSync(runDir, { recursive: true });
  console.error(`codex-img: ${jobs.length} job(s), concurrency ${conc}, ${cfg.model} / ${cfg.effort} / ${cfg.tier}, ${ver} (${bin.label})`);
  const results = [];
  let next = 0, lastStart = 0;
  async function lane() {
    while (next < jobs.length) {
      const job = jobs[next++];
      const wait = lastStart + STAGGER_MS - Date.now();
      lastStart = Date.now() + Math.max(0, wait);
      if (wait > 0) await sleep(wait);
      console.error(`  start ${job.id}`);
      const r = await runJob(bin, cfg, job, deckDir, runDir);
      r.codex_version = ver; r.model = cfg.model; r.effort = cfg.effort; r.tier = cfg.tier;
      r.prompt_file = job.prompt_file; r.refs = job.refs || []; r.finished = new Date().toISOString();
      fs.appendFileSync(path.join(deckDir, 'runs', 'runs.jsonl'), JSON.stringify(r) + '\n');
      console.error(`  ${r.status === 'ok' ? 'done ' : 'FAIL '} ${job.id} ${(r.wall_ms / 1000).toFixed(0)}s ${r.out ?? r.error}${r.size ? ` ${r.size.w}x${r.size.h}` : ''}`);
      results.push(r);
    }
  }
  await Promise.all(Array.from({ length: Math.min(conc, jobs.length) }, lane));
  console.log(JSON.stringify(results.map(({ id, status, out, size, wall_ms, error, usage }) => ({ id, status, out, size, wall_s: Math.round(wall_ms / 1000), tokens: usage && (usage.input_tokens + usage.output_tokens), error })), null, 1));
  return results.every((r) => r.status === 'ok') ? 0 : 2;
}

async function board(outPath, items, opts) {
  const sharp = (await import('sharp')).default;
  const cols = Number(opts.cols || 2), W = Number(opts.w || 540), pad = 24, labelH = 44, titleH = opts.title ? 70 : 10;
  const tiles = [];
  for (const it of items) {
    const eq = it.indexOf('=');
    const file = eq < 0 ? it : it.slice(0, eq);
    const label = eq < 0 ? path.basename(file) : it.slice(eq + 1);
    if (!fs.existsSync(file)) throw new Error(`board: no such image ${file}`);
    const img = sharp(file).resize({ width: W, height: Math.round(W * 1.25), fit: 'contain', background: '#161616' });
    tiles.push({ buf: await img.png().toBuffer(), label });
  }
  const rows = Math.ceil(tiles.length / cols), H = Math.round(W * 1.25);
  const width = pad + cols * (W + pad), height = titleH + rows * (H + labelH + pad) + pad;
  const escXml = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
  if (opts.title) svg += `<text x="${pad}" y="46" font-family="Arial" font-weight="bold" font-size="32" fill="#f2f2f2">${escXml(opts.title)}</text>`;
  const comps = [];
  tiles.forEach((t, i) => {
    const x = pad + (i % cols) * (W + pad), y = titleH + Math.floor(i / cols) * (H + labelH + pad);
    svg += `<text x="${x}" y="${y + 30}" font-family="Arial" font-weight="bold" font-size="24" fill="#ffc850">${escXml(t.label)}</text>`;
    comps.push({ input: t.buf, left: x, top: y + labelH });
  });
  svg += '</svg>';
  fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
  await sharp({ create: { width, height, channels: 3, background: '#161616' } })
    .composite([{ input: Buffer.from(svg), left: 0, top: 0 }, ...comps]).jpeg({ quality: 88 }).toFile(outPath);
  console.log(outPath);
}

// ---------- cli ----------
const argv = process.argv.slice(2);
const flag = (k) => { const i = argv.indexOf(`--${k}`); if (i < 0) return null; const v = argv[i + 1]; argv.splice(i, 2); return v; };
const opts = { only: flag('only'), concurrency: flag('concurrency'), cols: flag('cols'), title: flag('title'), w: flag('w') };
const [cmd, ...rest] = argv;
try {
  if (cmd === 'gen' && rest[0]) process.exit(await gen(rest[0], opts));
  else if (cmd === 'board' && rest.length >= 2) { await board(rest[0], rest.slice(1), opts); process.exit(0); }
  else { console.error('usage: node shared/codex-img.mjs gen <jobs.json> [--only a,b] [--concurrency N]\n       node shared/codex-img.mjs board <out.jpg> <img>=<label> ... [--cols 2] [--w 540] [--title "..."]'); process.exit(1); }
} catch (e) { console.error(`codex-img: ${e.message}`); process.exit(1); }
