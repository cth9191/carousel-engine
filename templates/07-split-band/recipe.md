# Template 07 — Split Band

The html-native build of style **S17 Split-Band Before/After** (`engine/styles/S17-split-band-before-after.prompt.md`).
Every slide is two flat bands split at half height (cream before, white after), a mono label over a big bold
statement in each band, and at most one orange text selection. Every word, tile, avatar and capture is HTML;
nothing is painted.

## When to use

- Spine C decks where each item replaced an old habit: Flip + proof per item (what it replaces, the item, real proof).
- Opinion takes on how AI changed a job (pure flips: log the deviation, see the style card's `formats.notes`).
- Not for diagrams, two-tool head-to-heads (S03) or system builds. Large screenshots belong in another style.

## Layouts (`layout` in each `slides[]` entry)

| layout | fields | notes |
|---|---|---|
| `cover` | `subject`, `beforePhrase`, `afterPhrase`, `countLine`, `beforeTile`, `tiles[]`, `avatar`, `byline` | Centred. Subject repeated verbatim in both bands; phrases in the selection box. ` ↓` is appended to the count line. |
| `flip` | `before`, `after` | No selection, tiles or proof. |
| `flipProof` | `before`, `after`, and `proof:{src,focus}` **or** `chip:'command'` | Strip 908×220 at y 1035–1255 (after statement one line, ≤ 15 chars); chip y 1149–1255 (after statement may take 2 lines). |
| `twinProof` | `before`, `after`, `beforeProof`, `afterProof` | Both statements one line ≤ 15 chars; strips at y 392–612 and 1035–1255. |
| `cta` | `before`, `keyword`, `deliverable` | After band: "Comment" / KEYWORD (in the selection) / deliverable (1–2 lines). |

- **Labels:** one pair per deck in `DECK` at the top of the script (`'Old habit:'` / `'New habit:'`). A slide can override with `labelBefore` / `labelAfter`.
- **Line breaks:** `|` in a statement or deliverable is a hard break (break by meaning). Without `|` the browser wraps inside 908 px.
- **Tiles:** `{ src, ground:'white'|'ink' }` puts a mark at 70 % on an 80 px tile (radius 18); `ground:'asset'` shows a full tile PNG (press-kit app icon, or a `render-card.mjs` tile) edge to edge. Only the deck's tools, in item order: 0–1 before, 1–5 after.
- **Avatar:** `'assets/avatar.png'` (your square profile photo, circle-cropped) or `null` for a plain grey placeholder circle.
- **Byline:** `byline` on the cover; the template ships `'{{BRAND}}'` (from `engine/brand.json`).
- **Proof:** `{ src:'assets/x.png', focus:[x,y,w,h] }`, the focus box in image pixels from `shared/shots.py`. The strip keeps the focus box visible, fills 908×220 and centres on it. Dark terminals that should not be cropped: `fit:'contain', bg:'#0D1117'` (letterbox on the edge colour).
- **Counter:** `NN / TT` from the slide order, bottom right. `exportName` works as in every template.

## Fit pass (the Copy limits are enforced)

Both statements on a slide share one size: 126 px on a 115 px line, shrinking in 2 px steps to the 96 px floor
until each fits 908 px and its line budget. Cover headlines start at 130 px (floor 96); the deliverable at 74 px
(floor 56). The copy limits from the prompt block are checked on every render: label ≤ 20 chars, statement ≤ 7
words, proof/twin statements ≤ 15 chars, cover subject and phrases ≤ 13, count line ≤ 30, CTA before ≤ 6 words,
keyword ≤ 10, deliverable ≤ 2 lines of ≤ 24, command ≤ 34.

A broken limit or a statement that doesn't fit at the floor puts a **red FIT/COPY banner across the top of the
slide**, in the browser and in the export, plus `console.error` and `window.fitReport`. `export.mjs` writes every
slide and then exits 3, naming each failure: a banner means rewrite the copy, never ship it.

## Workflow

1. `mkdir carousels/<id>/assets`; copy `templates/07-split-band/slides.html` to `carousels/<id>/`.
2. Put the tiles, `avatar.png` (optional) and captures (cropped with `shared/shots.py`, focus boxes from `shots.json`) in `assets/`.
3. Edit `DECK` and `slides[]`. Copy comes from `storyboard.json` (`strings[]`), per the prompt block's Copy section.
4. `Invoke-Item carousels/<id>/slides.html` → tweak (⚙) → 📋 Export → paste JSON → update `slides[]` (`before`, `after`, `defaults.size`, …).
5. `node shared/export.mjs --carousel <id>` → `exports/slide-NN-YYYY-MM-DD.png` (exit 2 = an image didn't load,
   exit 3 = a FIT/COPY failure). Look at every slide.

## Pitfalls

- Never paint any of it: the template replaces the image-native route for S17.
- Never copy a reference deck's words, tool row, marks or cover phrase; no "before/after {tool}" cover phrase.
- Tiles only for tools the deck covers; no tile for a manual old way; no rival tool framed as the loser.
- The proof strip is real proof verified on posting day. An empty strip shows a hatched "908 × 220 capture slot".
- Re-sync localStorage tweaks into `slides[]` before baking, as in every template.
