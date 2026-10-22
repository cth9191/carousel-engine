# S14 Scenic Painterly: overlay kit

Every word on an S14 slide is one of these HTML overlays, set over a fitted, text-free painted Codex plate
(spec: `engine/styles/S14-scenic-painterly.prompt.md`). The kit mirrors a deck folder (`../fitted/`, `../mascot/`,
`../shots/`), so its paths work unchanged once copied.

The kit ships no character. Each page has a commented-out pose line for your own mascot, if you have one: a
transparent PNG pose you made (never a licensed character) standing on the plate's clear spot, a different
activity on every slide. With no mascot, leave the lines out: the plate's one small painted object holds the spot.

| Path | What it is |
|---|---|
| `cards/s14.css` | Tokens (cream #F5EBE0, warm ink #2A1E16, orange #D9551F, paper #F4ECDD) and components: header row with counter box, Didone headline (tone from sky-tone: "white" = cream), paper list card (label, rows of number / name / figure / what line), tilted capture window (with the samples' dashed stand-in `.ph`), giant cover numeral, optional pose + painted-ground shadow, footer mantra, CTA keyword card |
| `cards/s14.js` | Sets the plate, draws sky-tone's scrims, stands each `img.pose` on its feet line, runs the fit pass and checks the list (≤ 6 rows; every row has a what line and a figure; no name cut off). Any failure overflows the page (render-card exit 2), never hangs |
| `cards/slide-01.html` | **Cover**: header, giant count + 2-line hook, capture window, footer (optional cover pose). Box `[0.07, 0.40]` |
| `cards/slide-02.html` | **Item group**: header, 2-line headline, list card (4 sample rows; up to 6), footer (optional activity pose). Box `[0.07, 0.30]` |
| `cards/slide-03.html` | **CTA**: headline, keyword card, footer (optional pose). The sample reuses the cover plate via `"plate"`; a deck gives it a dusk plate. Box `[0.09, 0.31]` |
| `fitted/slide-01.png`, `slide-02.png` | Two approved Codex plates (golden-hour cover, morning item), fitted; the morning one is also `engine/styles/refs/s14-ref-item.png` |
| `samples/slide-0N.png` | The three pages rendered with no mascot (exit 0 each). Placeholder topic; **every figure is a placeholder** (`★ 00.0k`), and the cover's capture is a dashed stand-in |

The cards still carry the `<body>` tone stamps from the sample plates; sky-tone re-stamps them in every deck.

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/fitted $D/shots $D/exports
cp engine/styles/kits/S14/cards/{s14.css,s14.js} $D/cards/
# optional, only with your own mascot: mkdir -p $D/mascot and copy one activity pose per slide into it, never repeated
# per slide: copy the layout page to cards/slide-NN.html, replace every sample string from storyboard strings[],
# put the real capture in the cover window (<img src="../shots/list.png"> in place of the .ph div), and, with a mascot,
# uncomment the pose line and set its data-x / data-feet / data-w to the plate's clear spot (read it off fitted/slide-NN.png)
python -I shared/composite.py $D/plates/slide-NN.png $D/fitted/slide-NN.png
node shared/sky-tone.mjs $D                                           # exit 4 = busy sky: edit the plate
node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22
```

## Fit and limits (measured on the kit)

- Header and footer: 22 px JetBrains Mono caps; footer mantra ≤ 6 words, the same on every slide.
- Item headline: 2 lines, 118 → 92 px in 872 x 250 ("Search &" / "Sources" fits at 118).
- List card: 920 px wide from y 420. Rows: name 29 px Inter 700 on one line (`firecrawl/firecrawl-mcp-server`,
  30 characters, fits), figure 22 px mono, what line 24 px, ≤ 8 words. About 103 px a row: 4 rows end near y 835, 6 rows at
  y 1041, so with 6 rows a pose needs a spot whose ground line is at 88% or lower and stays under 300 px wide.
- Cover: numeral 250 → 180 px; hook 92 → 76 px on 2 lines; capture window 400 x 380, rotated 2 degrees.
- Pose widths (with a mascot): 300-340 px. The painted-ground shadow sits at the feet line; if the pose looks
  pasted, move `data-feet` 6-10 px lower so the feet sink into the grass. `data-feet-y` is the pose's lowest foot
  pixel / height (`python -I shared/pose-check.py check` prints it as `feet_y`).
