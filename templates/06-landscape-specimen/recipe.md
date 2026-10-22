# Template 06 — Landscape Specimen (style S15)

A cinematic landscape per item, the name set giant in the sky as a two-font specimen, a two-column
masthead and a BACK/NEXT nav. Spec: `engine/styles/styles.json` S15 and
`engine/styles/S15-landscape-specimen.prompt.md`. This folder is the **overlay kit**: Codex paints a
text-free plate per slide, and `overlay.html` sets every word and all chrome over it.

Unlike templates 01-03 there is no `slides.html` and no `export.mjs` bake: each slide is one card
rendered by `shared/render-card.mjs` over its own fitted plate.

## When to use

- Top-N tools, plugins, repos (spine C), one item per landscape; "X + Y pairings" decks (combo layout).
- Not head-to-heads (no table vocabulary) or how-it-works explainers.
- Brief-card check by hand: no S15 within 14 days of an S13 deck.

## How a deck uses it

```
carousels/<id>/
  plates/slide-NN.png     Codex plate (text-free; magenta zone only on the cover monitor / in-scene proof)
  fitted/slide-NN.png     1080x1350, from composite.py
  shots/*.png             real captures, pre-cropped with shared/shots.py around a focus box
  logos/*.png             real app icons for combo slides (your logo folder, or simple-icons)
  cards/slide-NN.html     a copy of overlay.html per slide; only its slide-data JSON is edited
  runs/tone/slide-NN.json tone pass output
  final/slide-NN.png      the rendered slide
  exports/slide-NN-YYYY-MM-DD.png
```

Per slide, in this order:

1. **Fit** every plate, keyed or not:
   `python -I shared/composite.py carousels/<id>/plates/slide-NN.png carousels/<id>/fitted/slide-NN.png`
   (centre crop + Lanczos to 1080x1350). A plate with a magenta zone (cover monitor, in-scene proof)
   runs `--zones-only` first, then the same command with `--shot 1=shots/x.png@x,y,w,h`. An unkeyed
   plate exiting 3 has stray magenta: edit job.
2. **Card**: `cp templates/06-landscape-specimen/overlay.html carousels/<id>/cards/slide-NN.html`, fill
   `{{BRAND}}` in the masthead (the skill does this when it copies the file), then replace the JSON inside `<script type="application/json" id="slide-data">` (schema below). Delete
   the `"plate"` key: the card then uses `../fitted/<its own name>.png`.
3. **Tone**: `node shared/sky-tone.mjs carousels/<id>` (all slides; `--slides 03,04` for some). It writes
   `runs/tone/slide-NN.json` and stamps `data-mast / data-stack / data-nav / data-scrim* / data-nav-dim`
   onto each card's `<body>`. Exit 4 = a region misses contrast even at a 50% scrim: edit job for a
   calmer sky. Re-run it whenever a plate changes; stamping is idempotent.
4. **Render**:
   `node shared/render-card.mjs carousels/<id>/cards/slide-NN.html carousels/<id>/final/slide-NN.png --w 1080 --h 1350 --scale 1`
   Exit 2 = something overflowed (the message names it). Check the `card:` line it prints: pairing,
   giant size, notes and warnings from the fit pass.
5. **Export**: copy `final/slide-NN.png` to `exports/slide-NN-YYYY-MM-DD.png` (date from the folder name)
   and look at every slide at 1080x1350.

## slide-data schema

```json
{
  "layout": "item",                 // cover | item | stake | proof | combo | cta
  "n": 3, "total": 9,               // nav: current number (orange pill) and the real total
  "mast": { "label": "CLAUDE CODE PLUGINS", "month": "OCT 2026" },   // label 3 words at most
  "pairing": "auto",                // P1 | P2 | P3 | auto (adjacent slides never share one: set it)
  "kicker": "for memory",           // 1-4 words; cover: count + audience; combo: tool A; cta: "comment"
  "name": "claude-mem",             // the giant line, exact; cta: the comment keyword
  "caption": "…",                   // what it does and what it replaces; 2 lines, about 68 characters
  "use": "recall last week's auth decision",   // "→ " is added; 8 words / 40 characters
  "proof": "★ 18.4k stars · free · MIT",       // verified on posting day; a leading ★ becomes an SVG star
  "outcome": "that do the boring work",        // cover only, mandatory, 8 words
  "capture": { "src": "../shots/x.png", "horizon": 0.64, "width": 0.66 },  // proof only
  "icons": ["../logos/a.png", "../logos/b.png"], "iconsFull": false,       // combo only
  "sprite": { "src": "…", "x": 420, "y": 1010, "w": 160 },                 // optional: your own mascot PNG
  "kickerPx": 88, "caps": false, "box": [0.12, 0.52], "plate": "…"         // rare overrides
}
```

`samples/slides.sample.json` holds the data of every sample render.

## What the fit pass does (`window.cardReady`)

- **Pairing by name length** (`auto`): 6 characters or fewer → P3, up to 10 → P1, up to 12 → P2. A
  requested pairing whose limit the name exceeds falls back to this rule (noted in `card:`).
- **Long-name rule**: past 12 characters (or the requested pairing's limit), the name breaks at a
  hyphen, slash or space into two balanced lines (hyphen and slash stay on line 1), cap 160 px. No
  break, or a part over 12 characters: a warning to use the README's own short name and put the exact
  name in the caption.
- **Giant size**: fitted to 864 of the 872 px column; cap 260 px (160 on two lines or a proof slide;
  cover hero 240, or 200 when the outcome runs past 30 characters), floor 140 px.
- **Vertical fit**: while the stack is taller than its box, the giant steps down to its floor, then the
  kicker to 64 px, then the gaps go to the low end of their ranges. Still too tall: render-card fails
  (a storyboard rewrite: cut the caption or use line).
- Caps: P2/P3 uppercase only a capitalised-word name (Playwright); own casing (claude-mem, n8n, GitHub)
  stays. CTA and `"caps": true` force caps.
- `data-fit` on the stack, giant, caption, outcome, use and proof: an overflow is exit 2, never a
  silent clip.

## Tone and scrims

`shared/sky-tone.mjs` samples x 104-976 of the fitted plate: masthead 3-9%, the stack box (top 60% at
3:1 for kicker and giant, bottom 40% at 4.5:1 for caption, use and proof), nav 91-98% (4.5:1). Ink
#0E0E0E or white, whichever has the higher WCAG contrast against p10 / p90 luminance; short of target,
the first scrim step that passes (20, 35, 50%). The overlay draws the scrim under the type: black
behind white, white behind ink, full strength over the stack box with an 80 px feather, a band fading
over 60 px on the strips. The cover nav drops to 70% opacity only when it still clears 4.5:1.
Stack boxes: cover 12-43%, item / stake / combo 12-52%, proof 11-44%, cta 14-50% (the same table is in
both files; a `"box"` override in the JSON is read by both).

## Pitfalls

- **Card length limits** (measured): combo caption about 30 characters (it sits between two 72 px
  icons on one line); proof line about 47 characters at 30 px mono; proof-slide caption one line,
  about 36 characters. An item with a two-line name plus a two-line caption, use and proof is at the
  edge of its box: keep the caption to one line there.
- A plate whose sky isn't clear (trees or peaks above 44%) forces a heavy scrim (the dusk sample needed
  35%). Re-roll the plate before you accept a muddy scrim.
- Capture key text must render at 30 px or more: crop the shot so its width is at most about 1.2x the
  card's inner width (a 700 px card takes a crop under about 860 px of 2x-DPR capture).
- The overlay can't sample its plate (file:// canvas taint); the tone pass must run before rendering,
  or every region stays at the ink default.
- Never AI-paint words, logos or UI onto the plate: everything readable comes from this overlay or a
  real capture.

## Samples

`samples/plates/` are stand-in test plates borrowed from two other styles' sample Codex plates, not house
plates: `photo-golden-grass.jpg` and `photo-overcast-sea.jpg` (S13's film photos), `painted-golden-meadow.jpg` and
`painted-morning-river.jpg` (S14's paintings), and `photo-overcast-sea-night.jpg` (a navy-graded copy of the sea).
Real decks use text-free Codex photo plates per the prompt block. `samples/slide-0N-*.jpg` are renders of every layout with the
brand shown as `YOUR BRAND`; `samples/slides.sample.json` holds their data (`_plates` says which plate each one
used). In them, the proof slide's capture is a dashed placeholder and the combo slide's icons are two Lucide
glyphs standing in for real app icons. `preview.png` is cover / item / proof / CTA.
