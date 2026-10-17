# S07 page kit

Every S07 slide is one page: `page.html` sets all the type, chrome, brush label, logo tiles, capture windows and exact
text over ONE fitted, text-free Codex network plate (`engine/styles/S07-dark-network-hero.prompt.md`). Inter Black /
Inter / JetBrains Mono; tokens in `kit.css` (near-black #06090B, teal #39C6BF, terracotta #D97757 accent;
`"ground": "ember"` swaps the glow to terracotta/amber for warm plates).

| File | What it is |
|---|---|
| `page.html` | The page: one `<script id="data">` JSON block per slide picks the layout and holds every word |
| `kit.css` | Tokens and components (scrim, chrome, type block, glass window, pins, chips, nodes, stat cells, terminal, rail, covers, CTA pill) |
| `kit.js` | The runtime: reads the JSON, lets the page build, runs the fit pass, resolves `window.cardReady` for `render-card.mjs` |
| `samples/` | Two sample plates, the prompts that made them, placeholder captures, sample JSON and one render per layout |

| Layout | Role | Fields (copy limits enforced; a broken rule prints `LIMIT-<rule>` and exits 2) |
|---|---|---|
| `name` | cover | `kicker`, `name` ≤ 12 chars, `brush` ≤ 22 chars, `tiles[]` ≤ 4 `{src, bg: white\|dark\|none, pad}`, `foot` ≤ 8 words, `tag` |
| `icon` | cover | `name` ≤ 14 chars (e.g. `/<command>`), `tile {src, bg, pad}`, `sub` ≤ 10 words, optional `brush`, `tag` |
| `define` | what | `headline` ≤ 7 words, `body` ≤ 35 words, `strip[]` 2–4 chips ≤ 16 chars, `shot {src, title, focus, contain}` |
| `versus` | why | `headline`, `body` ≤ 25, `cols[2] {tag, value ≤ 7 chars, caption ≤ 10 words, old, shot?}` |
| `parts` | model | `headline`, `body` ≤ 20, `parts[3-4] {name ≤ 14 chars, def ≤ 8 words}`, optional `pos[[x,y]…]` (fractions) |
| `stage` | how / step | `headline`, `body` ≤ 30, `shot`, `pins[≤3] {x, y (fractions of the screenshot), label ≤ 18 chars, side}` |
| `terminal` | peak | `headline`, `body` ≤ 25, `title`, `lines` (≤ 14; `$ ` prompt, `✓` ok, `#` comment), optional `caption` |
| `receipts` | use | `headline`, `body` ≤ 25, `stats[2-3] {value ≤ 7 chars, caption ≤ 6 words}`, `shot` |
| `steps` | start | `headline`, `steps[3-4] {title ≤ 7 words, cmd ≤ 40 chars}` |
| `cta` | cta | `headline` ≤ 4 words, `body`, `keyword` ≤ 12 chars, `deliverable` ≤ 16 words, optional `tiles[]` |

Common: `plate` (default `../fitted/<this file's name>.png`), `ground`, `counter` ("NN / TT"), `label` (the section label,
lowercase, e.g. `02 — why it works`), `footer` (`["<brand>", "swipe →"]`, the brand from `engine/brand.json`; the default
is `["YOUR BRAND", "swipe →"]` so a forgotten brand shows). `*accent*` marks the terracotta phrase in any headline, body,
caption, brush or footnote.

## Fill one

1. Fit the plate: `python -I shared/composite.py $D/plates/slide-NN.png $D/fitted/slide-NN.png` (no zones; it crops to 1080×1350).
2. Copy `kit.css`, `kit.js` and `page.html` (as `slide-NN.html`) into `$D/cards/`. Edit only the JSON. Paths to shots and
   logos are relative to the card (`../shots/x.png`, `../logos/y.png`). Logo tiles are real marks: your own logo files or
   simple-icons SVGs rendered to PNG (`node shared/render-card.mjs $D/logos/<name>.svg $D/logos/<name>.png --w 512 --h 512 --scale 2`);
   never draw one. Words come from `strings[]`, numbers from the dossier.
3. `parts`: open the fitted plate and, if the clusters are not at 27%/73% × 47%/73%, set `pos` to their measured centres.
4. Render straight to the export:

   ```
   node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22
   ```

   Exit 0 is required. Exit 2: overflow, text under 22 px, or a `LIMIT-` rule. Cut copy; never lower the floor.

## samples/

`plates/cover.png` and `plates/parts.png` are two test Codex plates (gpt-6.1-sol, made from the prompts in
`samples/prompts/`), fitted. `<layout>.jpg` is each layout rendered (JPEG to keep the repo light) from
`samples/data/<layout>.json` on the placeholder topic "ORBIT" (a made-up notes tool; every figure is a placeholder). The
captures in `samples/shots/` are placeholder renders, the tiles are Lucide glyphs from `shared/vendor/lucide/` standing in
for real logos. `name.jpg` and `parts.jpg` use the plate made for that layout; the other layouts reuse the parts or cover
plate, so their network figure doesn't match the layout (a deck paints one plate per slide). The parts plate put its top
row at 41% down, so `parts.json` sets a measured `pos`. All render with exit 0 at `--min-px 22`.

To re-render a sample, paste `samples/data/<layout>.json` into the data block of a copy of `page.html` saved in this
folder (sample paths are relative to it), and run the render command above on that copy.
