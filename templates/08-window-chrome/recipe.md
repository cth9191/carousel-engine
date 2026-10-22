# Template 08 — Window Chrome

The template for style **S19 Window-Chrome Build Diary** (`engine/styles/S19-window-chrome-diary.prompt.md`).
A build diary told inside an app window: chrome slides (graphite canvas in a window
frame, white Instrument Serif, real artboards, cut-outs breaking out over the frame) alternate with flat
apricot and cream caption pages. All type is HTML. Codex paints only spot-illustration cut-outs and the
result-page SCENE plate.

## When to use

- Spine D build diaries: "how I built X in N steps", "build your X with Claude Code".
- Spine A explainers of one tool, shown inside its own window (real-frame mode).
- Anything with a raw → refined process row.

Rhythm (storyboard only): chrome slides and caption pages alternate, never two caption pages in a row; two
chrome slides may run back to back for consecutive steps. The cover is chrome, the CTA a caption page.

## Workflow

1. Copy `slides.html` to `carousels/<id>/slides.html`. It links `../../shared/tweak-panel.css`, so the deck
   folder must sit at `carousels/<id>/`.
2. Put real captures in `carousels/<id>/assets/` (`shared/shots.py` crops and scrubs). Cut-outs are transparent
   PNGs in `assets/` too (see "Cut-outs").
3. Edit `DECK` (`repo` shows in the title bar as "{repo} — {owner}"; `owner` and `brand` ship as `{{BRAND}}`,
   and `brand` is the caption-page footer) and
   `slides[]` at the bottom of the file. One entry per slide.
4. Open it (`Invoke-Item carousels/<id>/slides.html`). The nav bar prints QA warnings for the current slide
   (break-out over type or chrome, over a focus box, past 97% of the slide; text outside the safe area; a fit
   pass that ran out of room). `window.qa()` returns the same list. Fix every warning before the bake.
5. Tweak with ⚙, then 📋 Export and sync the JSON into each slide's `defaults` (localStorage never reaches
   the bake).
6. `node shared/export.mjs --carousel <id>` writes `exports/slide-NN-YYYY-MM-DD.png` at 1080 × 1350 (exit 2
   names any image that failed to load; exit 3 lists every `qa()` warning left: fix them and bake again).

## Slide kinds

| kind | layout | ground | what it holds |
|---|---|---|---|
| `chrome` | `cover` | graphite in a frame | headline (2 lines, 92 px, top 14.5%) + subtitle (1 line, 46 px) + a 2 × 2 grid of finished outputs (300 × 375 cells at 4:5, x 228–852, y 462–1236; `span:2` = one wide artboard over a row) + 3–5 break-outs |
| `chrome` | `stage` | graphite | heading (≤ 6 words, 72 px, top 18%) + one artboard (62% wide) or two side by side (≤ 72% together, 24 px gutter; e.g. a real panel + an exact-text card) + caption (1 line, 40 px) + 1–3 break-outs |
| `chrome` | `process` | graphite | `raw[]` captures bottom-aligned at 47% with `rawLabel` above + heading at 52% + `pieces[]` (real-result cut-outs, staggered, rotated ≤ 4°, contact shadow) in 60–82% + caption at 86% |
| `chrome` | `command` | graphite | heading + one exact-text card (≤ 70% wide, auto height) + caption; a piece off the card's top-right corner (`anchor:'card:tr'`) |
| `chrome` | `parts` | graphite | heading + `parts[{src,label}]` in a loose row at 40–75%, each labelled "{part}: {≤ 8 words}" |
| `result` | — | apricot | sentence (≤ 30 words, rust 48 px, 2–3 lines, top 9%) + one artboard with a warm shadow in 25–92%, or `plate` (a composited SCENE plate, full-bleed under the type) + footer |
| `zoom` | — | cream | sentence (≤ 20 words, 52 px) + one 605 × 907 artboard (2:3) at 24–91% holding a cropped real UI panel with its `select` box + footer |
| `cta` | — | apricot | "Comment {keyword}" (110 px, keyword italic) + `line2` (48 px) + `hero` cut-out on an HTML contact shadow + footer |

Every chrome slide shows the stage label and the counter ("NN / TT", auto from the slide order; `counter`
overrides; a `mirrorPrev` slide shares the previous number). Caption pages carry the footer: brand left,
counter right, 4% from the bottom, Inter Medium 30 px caps in rust.

## The frame

- **Kit (default):** your own window. Title bar (traffic lights, "{repo} — {owner}"), control bar (stage
  label left, counter pill right), tab row (`tabs:[...]`, first is active with the orange top line; the
  template widens earlier tabs so the last one runs off the right edge), activity rail (lucide icons; `rail`
  names the active one: `files search branch terminal chat run account settings`; `rail:false` hides it).
  No third-party name, logo or setting anywhere in it.
- **Real frame** (the default for a deck about one app): `frame:{ src:'assets/frame-<app>.png', canvas:{x,y,w,h} }`.
  `src` is a 4:5 capture of the app's real window (VS Code or Terminal for Claude Code; the real Cursor or n8n
  window) with side panels closed and the right and bottom edges cropped off, scaled to 1080 × 1350.
  `canvas` is its editor rect in slide px: the template lays flat graphite over it (no alpha cut) and floats
  the stage pill (#2F2F2F) and counter pill 16 px below it. Keep the chrome above 15% of the height
  (`canvas.y` ≤ 202) and any side bar inside 12% of the width (`canvas.x` ≤ 130). Scrub personal info first.
  Example: a Windows Terminal capture 1716 × 917, crop `(0, 0, 734, 917)`, resize to 1080 × 1350, tab bar ends
  at 63 px → `canvas:{x:0,y:63,w:1080,h:1287}`.

## Artboards

`{ src, focus:[x,y,w,h], select:[x,y,w,h], focusFill, fit, aspect, span, bg }`, square corners, no border.

- `focus` (fractions of the capture) is what must stay visible: the capture is cover-fit around it, scaled so
  it fills about 86% of the artboard (`focusFill`, 1 = edge to edge), so the corners stay free for break-outs.
  A focus box whose aspect is far from the artboard's still shows its neighbours; crop it tighter.
- `select` (fractions of the capture) draws the orange selection box with 8 square handles in HTML. Never paint it.
- `fit:'contain'` letterboxes on `bg` instead of cropping.
- Exact text (prompt, command, config, file tree, table) is a card artboard: `{ card:{ text } }` or
  `{ card:{ html } }` (spans `.hl` orange, `.dim` grey), cream, JetBrains Mono in ink, `size` default 30 (the
  floor; cut copy instead of shrinking). On a stage slide give it an `aspect`.

## Cut-outs (the break-out layer)

`cutouts:[{ src, x, y, w, scale, rotation, shadow }]`: transparent PNGs, top-left at `x, y` (slide px), `w`
wide × `scale`, rotated in degrees, above everything. Or anchor one to a corner of the first artboard or card:
`anchor:'board:bl'` / `'card:tr'` (corners `tl tr bl br`) centres it on that corner, then `dx, dy`.

Sources, never through `composite.py --card` (it flattens alpha onto white):
1. Single elements cropped from that slide's own capture, scaled only. Line art on a dark capture keys cleanly
   by brightness (alpha from the max channel); trim to the alpha bbox.
2. Exact-text pieces: `node shared/render-card.mjs <card>.html assets/cut-<name>.png --w W --h H --scale 2 --min-px 30`,
   placed at `w = W` so the text stays at 30 px or more.
3. Codex CUT-OUT jobs (`shared/codex-img.mjs`), background removed with any background-removal tool (or a
   flood fill of the flat ground).
4. Your own mascot (optional; transparent PNG poses you made, never a licensed character), only when its pose
   comments on the slide. Never painted by the model. With no mascot, leave this source out.

Rules the QA checks: a break-out may cover one outer corner or edge of an artboard but never its focus box,
reaches over the rail by at most a quarter of its own width, stays inside 97% of the right and bottom edges,
and never covers type, the stage label, the counter, the active tab or the footer.

## Fit passes

Each type block has a line budget (cover headline 2, subtitle 1, chrome headings 1, captions 1, result and zoom
sentences 3, CTA line 1 + 2). The fit pass shrinks a block 2 px at a time until it fits, never below 30 px, and
warns when it had to go under 80% of the spec size. In practice, within the 18–82% text band: a 92 px cover hook
holds about 2 × 20 characters, a 72 px heading about 29 characters, a 40 px caption about 50 characters
(9–10 short words). Longer copy shrinks; cut it instead.

## Tweakable

- Global: orange accent, type scale.
- Per slide: stage label, headline / sentence, subtitle / line 2, caption, headline size, headline nudge,
  artboard scale, break-outs on/off. Grids, focus boxes and cut-out positions are edited in `slides[]`.

## Pitfalls

- **No third-party app UI or chrome.** The kit is generic IDE vocabulary. Real logos only inside a real
  frame or capture, on the canvas as a logo file, or in a SCENE cyan slot.
- **The frame is chrome, not proof.** Stage, counter and real file names only: no model pills, fake status or
  fake run results.
- **No pink or maroon.** Caption pages are apricot `#F5C9A0` or cream `#F5EBE0`, type rust `#7A2C14`. Orange
  `#D9551F` is for UI accents and illustrations, never a type colour; accent words take the italic cut only.
- **Never paint a selection box, frame, artboard or exact text.** Codex paints only CUT-OUTs and SCENE plates.
- **Don't send a rendered frame or any reference deck's slides to Codex.** SCENE jobs take
  `engine/styles/refs/s19-scene-layout.png` as Image 1 until a result page is locked.
- **Re-sync localStorage → `slides[]` defaults** before baking, as with every template.
