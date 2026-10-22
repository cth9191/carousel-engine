# Template 03 — Command Press

Blueprint / engineering-drawing editorial. Built for **skill & command roundups**: one slide per named command (`/dumbify`, `/storytelling`, …). Reads like a technical spec sheet, not a generic carousel.

Two layouts share the ground, grid, crosshairs, tokens and tweak panel: the default **command sheet** (`hero.type`, below) and the **atlas** (`layout:'atlas'`, style S22 Layered Parts Atlas: one layer of a big grouped list per slide; see [atlas layout](#atlas-layout)). A deck uses one of the two.

## When to use

- "N skills / N levels / N steps" content where each item is a named command or capability
- Before/after, audit, or "I turned X into a skill" explainers
- Anything that benefits from a punchy `/SLASH-COMMAND` headline

If the content isn't command/skill-shaped, use `01-graph-paper-cream` (lists) or `02-terracotta-zine` (process/concept).

## The look (locked spec)

- **Bone bg** `#ECE3D4` + faint ink grid + paper grain
- **Anton** headline, all-caps, slash-prefixed, auto-fits width (long names bleed right deliberately)
- **Two roles for color — this is the rule:**
  - **Ink chrome** = everything structural: grid, dimension line (`1080 PX`), frame, corner labels, `FIG`/`SHEET` text
  - **Terracotta `#D9551F`** = callouts ONLY: accent words, BEFORE/AFTER tags, the "good" chart line, arrow, after-card outline, the 4 corner crosshairs
  - Never let orange do structural duty. The accent stays rare so it keeps meaning "look here."
- Engineering chrome: `SKILL 0N` chip (top-left), `REV A` + triangle (top-right), dimension line, `FIG.N — /name.skill`, `SHEET NN / NN` + `SWIPE →` footer
- Black card has a drop shadow (lift); after-card is a thin orange outline (light = the win)

## Hero block types (`hero.type`)

Body-slide heroes are **HTML, never AI-gen**. Four types:

| type | use | key fields |
|---|---|---|
| `beforeafter` | complexity → simplicity, manual → automated | `before:{tag,title,lines}`, `after:{…}` |
| `video` | "I turned this YouTube video into a skill" | `thumb` (real screenshot → assets/), `title`, `meta`, `caption` |
| `chart` | hook/retention audits, metric comparisons | `auditTag`, `audit:[…]`, `chartTag`, `good`, `bad` (SVG point strings) |
| `image` | framed screenshot (dashboard, UI, app) — orange border + corner brackets | `src` (→ assets/), optional `caption` |
| `none` | CTA / text-only | — |

**Charts are two-tone:** `good` line = terracotta, `bad` line = ink dashed. Never all-orange (kills the comparison read).

## Workflow

1. Copy `slides.html` to `carousels/<id>/`.
2. Edit the `slides[]` array at the bottom — one entry per slide. Set `chip`, `headlineHTML` (with leading `/`), `fig`, `body`, and `hero`.
3. **Cover** is a Codex plate or the S10 HTML cover (`engine/styles/kits/S10/cover.html`) → save as
   `carousels/<id>/cover.png` (slide 0 is `{cover:true}`).
4. Drop real screenshots into `carousels/<id>/assets/` for `video` heroes (`thumb`).
5. `Invoke-Item slides.html` → tweak via ⚙ panel → 📋 Export → paste JSON → update `slides[]` defaults to match (localStorage doesn't reach the baker).
6. `node shared/export.mjs --carousel <id>` → PNGs in `exports/` (the deck's own `slides.html` is baked).

## Tweakable

- **Global:** accent color, headline size, body size, grid opacity
- **Per-slide:** chip, rev, headline, fig, body, body-top, headline size, hero-bottom, video thumb src
- Structured hero content (before/after text, chart point arrays) is edited in `slides[]`, not the panel — too complex for sliders.

## Pitfalls

- **Don't make the grid/chrome orange.** Orange is callout-only. Tested extensively — orange-as-structure muddies the hierarchy.
- **Don't all-orange a chart.** Two-tone (orange good / ink bad) or the before/after read dies.
- **Headline auto-fits** but keep names short-ish; a 14-char `/COMMAND` is the comfortable max before it shrinks small.
- **Video heroes need a real screenshot.** Empty → shows a "DROP A REAL SCREENSHOT" placeholder. Never AI-gen the thumb.
- **Re-sync localStorage → `slides[]` defaults** before baking, same as every template.

## atlas layout

`layout:'atlas'` is style S22 (Layered Parts Atlas): 20–36 skills / MCPs / plugins in 4–6 layers, one
layer per slide, rows numbered 01 to M across the deck. Sheet kinds: `index` (optional, slide 2),
`layer` (one per layer), `combo` (optional) and `cta` (last). The cover is slide 0
(`{cover:true, coverImg:'cover.png'}`, a Codex plate composited per the S22 card). Samples sit at the
end of this template's `slides[]` (`Atlas — …`); a deck keeps only the cover and its atlas sheets.
Preview: `preview-atlas.png`.

### Data

```js
const slides = [
  { name:'Cover', cover:true, coverImg:'cover.png' },
  { name:'Index', layout:'atlas', atlas:{ kind:'index', title:'WHAT IS IN THE KIT', pill:'Install one layer at a time' } },
  { name:'Layer 1 — Design', layout:'atlas',
    atlas:{ kind:'layer', category:'DESIGN', banner:'5 DESIGN PARTS',
      pose:{ src:'assets/poses/set-square.png', prop:'SET-SQUARE', aspect:1.31, prop_anchor:[0.08,0.46], feet_y:0.99 }, // your own pose
      rows:[ { n:1, name:'frontend-design', kind:'SKILL', does:'Gives UIs a real look', start:true } /* … 3–6 rows */ ],
      proof:['START HERE · frontend-design', '41K stars · checked 10-16'],
      pill:'Replaces a hired UI designer' },
    defaults:{ poseH:65, poseDx:0 } },
  { name:'Combo', layout:'atlas', atlas:{ kind:'combo', title:'COMBO: SEE, THEN FIX', pair:[6,1],
      src:'assets/combo.png', maxH:460, focus:'center top',
      steps:[ { n:6, text:'Playwright screenshots your running app' } /* … exactly 3 */ ],
      pill:'A design loop with no designer' } },
  { name:'CTA', layout:'atlas', atlas:{ kind:'cta', title:'GET THE WHOLE KIT', keyword:'ATLAS',
      avatar:'assets/avatar.png',   // your square profile photo, mascot or logo tile
      rows:[ { n:1, name:'frontend-design', cmd:'/plugin install frontend-design@claude-plugins-official' } /* … 3 rows */ ] } },
];
const ATLAS = { label:'CLAUDE CODE · PARTS ATLAS', total:20 };   // Row 1 label · M (the cover count)
```

- `pose` is one pose from your own pose set (optional: your mascot as transparent PNGs, one per prop,
  never a licensed character, checked with `shared/pose-check.py`): `{prop, aspect, prop_anchor:[x,y],
  feet_y}` (anchors as fractions of the trimmed image; `pose-check.py check` prints them) plus `src`:
  copy the PNG into the deck's `assets/poses/`. With no mascot, set `src` to the subject's real logo tile
  (`aspect:1, prop_anchor:[0.5,0.5], feet_y:1`). No `src` draws a dashed "YOUR MASCOT →" placeholder.
  A deck uses each pose once and never its cover pose.
- Derived, never typed: `LAYER n/N` (sheet order), the DETAIL letter (A, B, C…), `RUNNING TOTAL {last} / {M}`,
  `SHEET nn / TT`, the index rows (layer, category in sentence case or `covers`, `01–05`), the index banner
  `{M} PARTS · {N} LAYERS`, the combo banner `{nn} + {nn}`, the CTA's `FIG. {TT} — KEYWORD`, its header
  count and `+ {M − 3} MORE IN YOUR DMS`.
- Kind chips (SKILL / MCP / PLUGIN / HOOK) show only when the deck's rows mix kinds.
- Leader routing: a prop anchor on the pose's left side routes over the pose's head, then down the
  gutter (x 508) to the start-here balloon; a right-side anchor runs straight to the gutter.
- Tweak panel: the global accent and grid sliders apply; per layer sheet, "Atlas pose height" (% of the
  wireframe, default 65) and "Atlas pose x nudge". Export → paste → set `defaults:{poseH, poseDx}`.

### Guards (each throws, so `export.mjs` fails instead of clipping; the slide also shows a red banner)

- A layer has 3–6 rows; a row counts as two-line when `does` > 24 characters or `name` > 18 (14 when
  chips show); with any two-line row the cap is 5 rows, at most 2 of them two-line.
- Exactly one `start:true` row. Row numbers run on from the previous layer sheet; the last layer's last
  row equals `ATLAS.total`. A banner that starts with a number must equal the row count.
- Row 2 below a 36 px cap, the banner below an 80 px cap, the CTA keyword below a 180 px cap, the
  Row 1 label past x 760, a proof line wider than the box (≤ 29 characters), a pill wider than the
  pill at 30 px, a parts list past y 1120 at the 30 px name floor, combo steps past y 1120 with the
  capture at 340 px, an install command past 2 lines, or the CTA stub past y 1290.
- Run the same caps in the storyboard check before touch 1: a layer over the cap is split or trimmed
  there, never at render time.

### Spec (moved from the S22 card's INTERIOR section)

All sheets: 1080 × 1350 with this template's ground, grid, grain, frame (inset 34 px) and crosshairs;
its 80 px side margins (as the `image` hero, so atlas and combo sheets align); content y 52–1290.
`layout:'atlas'` hides the global `.chip`, `.rev`, `.dim-top`, `.sheet` and `.footer-swipe` (and the
command sheet's headline, fig, body and hero zone) and renders its own Row 1 and SWIPE. Row 1
(y 52–92): a dimension line x 80–~640, end ticks, "{deck label}" in its gap; "SHEET {nn} / {TT}" (real
total) right-aligned at x 1000; both JetBrains Mono Bold 22 px, 70% ink. Any deck fact (counter,
dimension label, proof caption, kind chip) is ≥ 22 px JetBrains Mono Bold; 14–17 px is ornament only
(DETAIL tab, list header). Orange is callout-only (banner, start-here balloon and leader, ▸,
crosshairs, SWIPE →); structure is ink.

Layer sheet:
- **Row 2 (y 108–184):** "LAYER {n}/{N}: {CATEGORY}" (category ≤ 3 words), Anton ink at x 80,
  auto-fit to the margins, capped at a 64 px cap height.
- **Row 3 (y 196–356):** square orange banner, x 80–1000: "{k} {NOUN} SKILLS" (≤ 3 words; k = this
  layer's rows) in cream Anton, auto-fit at an 80–120 px cap height.
- **DETAIL box (x 80–496, y 384–1120):** 1.5 px ink frame, tab "DETAIL {A, B, C…} — {PROP}"; a 30°
  isometric wireframe box (1.5 px ink at 35%, faint floor grid) with ONE labelled dimension line on
  top, "RUNNING TOTAL {last} / {M}" (any second: ticks only); the pose on the box floor at ~65% of the
  wireframe's height, CSS ellipse shadow at `feet_y`; one 1.5 px orange SVG leader from `prop_anchor`
  to the start-here balloon, drawn after the fit pass; a ruled proof caption (PROVE) at y ~1010–1112,
  2 lines of JetBrains Mono Bold 22 px ≤ 29 characters: "START HERE · {name}" / "{verified fact} ·
  checked {MM-DD}" (stars, installs or a real UI fact, checked on posting day).
- **Parts list (x 520–1000, y 384–1120):** header "NO. / PART / DOES" (16 px mono, 55% ink) over a
  2 px rule; 3–6 rows of ~104 px split by 1 px rules. Row: 54 px balloon (2 px ink outline, JetBrains
  Mono Bold 26 px digits); the name in JetBrains Mono Bold 34 px exactly as invoked; under it the
  "does" line, Inter SemiBold 30 px, 80% ink, ≤ 24 characters of plain words (no "OKLCH", "4px
  grids"). Only the start-here balloon is filled (orange, cream digits). Outline kind chip (SKILL /
  MCP / PLUGIN / HOOK, 22 px) only when kinds mix.
- **Row cap:** 6 one-line rows. A row takes two lines when its "does" line exceeds 24 characters or
  its name 18 (14 with a chip); the cap is then 5 rows, at most 2 of them two-line. Numbers run on
  across sheets; the last row equals the cover count. Past y 1120 a fit pass shrinks the list evenly
  to a 30 px name floor, then throws so the bake fails; it never clips.
- **No body paragraph:** the rows are the body (~60 words, inside spine C's ~100).
- **Footer:** takeaway pill (x 80–1000, y 1144–1228; 3 px ink outline, bone fill): orange ▸ and ≤ 8
  words (≤ 42 characters) in Inter Black 34 px naming what the layer replaces. SWIPE → in orange
  JetBrains Mono Bold 22 px under its right end (y 1246–1276).
- **Storyboard check (before touch 1):** row counts and string lengths against the cap; a layer over
  it is split or trimmed in the storyboard, never at render time.

Index (optional slide 2, spine C `why`): a ≤ 4-word Anton Row 2; banner "{M} PARTS · {N} LAYERS";
left, an SVG exploded stack of {N} slabs at the same angle, balloons 1–N; right, a ruled index LAYER |
COVERS | ITEMS ("01 | Design | 01–05") at ≥ 26 px; the pill states the list's one stake. No mascot.

Combo (optional, spine C `combo`): banner "{nn} + {nn}"; this template's framed `image` hero (x 80–1000,
≤ 460 px tall) with a real capture of the two items working together (PROVE); 3 numbered steps of ≤ 10
words whose balloons carry the two item numbers; the usual pill. Row 2 is a short Anton title.

CTA: Row 1; an Anton ink headline of ≤ 5 words (Row 2), a statement, not a "Want all N…?" question;
"Comment" in Inter Black 44 px; the keyword as an Anton line in giant ink (cap height ≥ 180 px,
auto-fit, up to 240) with the orange underdim and an orange mono 22 px "FIG. {TT} — KEYWORD"; no quote
marks, no corner-bracket frame. Below, the deliverable stub, a ruled card (2 px ink outline, square
corners, bone fill): header row with the avatar at 56 px and "THE FULL LIST · {M} INSTALL COMMANDS"
(mono bold 22 px); the first 3 real rows (balloon, name, exact install command in JetBrains Mono 24 px,
≤ 2 lines, verified on posting day); a dashed rule and "+ {M − 3} MORE IN YOUR DMS". No takeaway pill
and no SWIPE: the stub's last line is the promise. One action only.

### Atlas workflow

1. Copy `slides.html` into `carousels/<id>/`; delete the command sample sheets and the `Atlas —` samples.
2. Set `ATLAS` and write the atlas sheets from the storyboard's `strings[]` (rows, does lines, proof
   facts, pills, CTA rows). Copy each layer's pose PNG (or logo tile) to `assets/poses/` and its measured
   fields into `pose`; the combo capture to `assets/`; the CTA avatar (your square profile photo, mascot or
   logo tile) to `assets/`.
3. Put the composited cover at `cover.png`.
4. `node shared/export.mjs --carousel <id>`; a guard failure exits non-zero with the slide and reason.
