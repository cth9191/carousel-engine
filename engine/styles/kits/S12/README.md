# S12 Voxel Costume Explainer: card kit

Every slide of S12 is one of these HTML pages (spec: `engine/styles/S12-voxel-costume-explainer.prompt.md`).
Codex never paints a slide: it only makes optional set pieces and, if you have a mascot, its costume poses. The
kit mirrors a deck folder, so its relative paths (`../mascot/`, `../logos/`, `../sets/`, `../shots/`) work unchanged
once copied.

The kit ships no character. The pose slots are for your own mascot, if you have one: transparent PNG poses you
made, never a licensed character. With no mascot, each slot holds the subject's real logo on a square tile, or is
deleted.

| Path | What it is |
|---|---|
| `cards/s12.css` | Tokens (near-white #FAF9F7, ink, orange #D9551F) and every component: step tag, headline with orange `.l2`, body, `.win` capture frame, pose / logo-tile / set cutouts with contact shadow, the samples' dashed `.slot`, speech bubble (Pixelify Sans; `.mono` for a command, `.tail-r`), icon rows, promise card, sparks, dots, pill, keyword box, `.code` card |
| `cards/s12.js` | Places every `.pose` and `img.set` on its feet line, runs the fit pass, checks the headline has an orange line and every bubble is 4 words or fewer. Any failure overflows the page, so render-card exits 2 instead of hanging. A `.slot` left in a page prints a note |
| `cards/icons.js` | Lucide glyphs used by the pages (regenerate with `lucide-icons.mjs --from`) |
| `cards/page-01.html` | **Cover**: tag, dots, 3-line hook, promise card, set piece + cover pose, bubble, sparks |
| `cards/page-02.html` | **what / why**: headline, body, pose + set piece, objection bubble, old-way pill |
| `cards/page-03.html` | **how / step** (also spine D's step): two captures side by side, pose with a mono command bubble, icon rows |
| `cards/page-04.html` | **CTA**: centred headline, `Comment KEYWORD` box, deliverable line, pose |
| `sets/laptop.png` | A voxel laptop set piece, cut with `pose-check.py cut` (its plate is `engine/styles/refs/s12-ref-set.png`) |
| `shots/capture-a.png`, `capture-b.png` | Placeholder captures (two frames of an animation check) so the split page renders; a deck uses its own |
| `samples/page-0N.png` | The four pages rendered (exit 0 each). Placeholder topic and captures; a dashed box marks each mascot slot |

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/mascot $D/logos $D/sets $D/shots $D/exports
cp engine/styles/kits/S12/cards/{s12.css,s12.js} $D/cards/
# one page per slide: copy the layout page to page-NN.html, set the tag "NN / TT" and label,
# replace every sample string from storyboard strings[], point <img> at $D/shots and $D/sets,
# and swap each dashed .slot for one of the two <img> lines in the comment above it:
#   your mascot:  <img class="pose" src="../mascot/<costume>.png" data-x data-feet data-w data-feet-y>
#   no mascot:    <img class="pose tile" src="../logos/<subject>.png" data-x data-feet data-w>   (or delete the slot)
node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards
node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22
```

Exit 2 means overflow, text under 22 px, a headline without its orange line or a bubble over 4 words:
shorten the copy, never lower the floor. Logos: your own logo file or a simple-icons SVG turned into a
transparent PNG with `node shared/render-card.mjs $D/logos/x.svg $D/logos/x.png --w 512 --h 512 --scale 2`.

## Placement and limits (measured on the kit)

- Cutouts: `data-x` (left), `data-w` (width), `data-feet` (ground y), `data-feet-y` (the pose's lowest foot
  pixel / height; `pose-check.py check` prints it as `feet_y`). Set pieces and logo tiles default to 1.0.
  Cover pose about 500-520 px wide; interior poses 400-470 px; logo tiles 250-320 px; set pieces 330-420 px.
- Cover hook: 3 lines fitted 150 → 112 px in a 952 x 500 box ("Claude Code / can check / its own work." fits at 150).
- Interior headline: 2 lines, 104 → 84 px (why) or 96 → 80 px (step).
- Body: 860 px wide, 36 → 32 px, about 30 words in 4-5 lines.
- Split page: captures 466 x 420 each at y 390 (screen area 466 x 386; `object-position: left top`, so crop
  the shot with `shots.py` to the part that matters). Rows: 2-3, 536 px wide, about 12 words each.
- Bubble: one line, ≤ 4 words, 36 px Pixelify Sans (30 px JetBrains Mono for `.mono`). With a logo tile
  instead of a mascot, keep the bubble only if it still reads as the viewer's voice; otherwise delete it.

## Costume poses (only with a mascot)

The block's COSTUME section is the build recipe: your mascot's canonical sprite as Image 1, the costume
paragraph, one held prop at most. Cut each pose with `python -I shared/pose-check.py cut`; if your mascot fits the
check's shape (see the script's header), run `check --sprite <your sprite> --prop <held prop box>` too, otherwise
compare it with the sprite by eye on near-white and on ink. Keep the poses that pass in your own pose folder and
copy the ones a deck uses into `$D/mascot/`.
