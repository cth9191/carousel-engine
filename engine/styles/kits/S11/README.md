# S11 Sketchnote Diagram Explainer: diagram kit

HTML/SVG diagram cards in the S11 look: pastel boxes with wobbly hand-drawn ink outlines, hand-drawn
arrows, handwritten margin notes and the yellow highlighter pill. S11 is image-native: Codex paints
the page (cream paper, tag box + eyebrow, the heavy two-tone headline, footer) with one flat magenta
zone where the diagram goes, and the diagram card is composited into it, so every word in the diagram
is exact. Spec: `engine/styles/S11-sketchnote.prompt.md` (tokens, the DIAGRAM ZONE block).

## Files

| File | What it is |
|---|---|
| `sketch.css` | Tokens (paper `#FBF7EE`, ink `#1B1B1B`, orange `#D9551F`, pastel green `#DDEEDB` / blue `#DCE8F7` / pink `#F8E1E4` / lavender `#E9E3F5`, highlighter `#FBE38E`) and the components: `.sk-stage` (the diagram root), `.sk-box` (+ `green` `blue` `pink` `lavender` `dashed` `big`, `data-outline="none"`), `.sk-chip` (column heading), `.sk-label` (small Inter label, `.accent` orange), `.sk-note` (Kalam margin note, `.tilt`, `.accent`, `data-underline` for a scribbled underline), `.sk-hl` (highlighter pill), `.sk-code` (ink code panel) |
| `sketch.js` | `SK.init({ arrows, minF, maxF })`: the fit pass (one font size `--f` for the whole diagram, the largest in [minF, maxF] that fits the zone), then the ink: box outlines, note underlines and arrows, drawn as seeded wobbly SVG paths (identical on every render). Arrow options are in its header |
| `diagram-flow.html` | Sample FLOW: input → engine → three steps → three results, closing highlighter line |
| `diagram-compare.html` | Sample COMPARE: two columns run the same input (lavender old way, green ours) |
| `diagram-parts.html` | Sample LABELLED PARTS: one object, its parts, a handwritten callout + arrow per part |

Fonts (Google Fonts, as the prompt block's "neat handwritten marker script" for notes and the
hand-lettered box voice): Patrick Hand (box text), Kalam 400 (margin notes), Inter 400/700 (labels),
JetBrains Mono 500 (paths, code). render-card prints the faces that loaded; a fallback shows there.

## Making a diagram

1. Copy `sketch.css`, `sketch.js` and the closest sample into `$D/cards/`.
2. Replace the strings; keep each sample's copy budget (in its header comment). Add or drop boxes and
   their arrows; arrows join elements by id (`{ from: '#a', to: '#b', fromSide: 'b', toSide: 't' }`).
3. Read the zone, then render at its `out bbox`, 2x, on the plate paper sampled beside the zone:

```
python -I shared/composite.py $D/plates/slide-04.png --zones-only --report $D/plates/slide-04.zones.json
node shared/render-card.mjs $D/cards/diagram-flow.html $D/cards/diagram-flow.png --w <bw> --h <bh> --scale 2 --bg "<paper>" --min-px 22
python -I shared/composite.py $D/plates/slide-04.png $D/final/slide-04.png --card M1=$D/cards/diagram-flow.png
```

Box text never goes under `minF` (30 px = 1/45 of the slide height, the S11 body floor); labels and
notes are 0.75-0.88 em of it, so `--min-px 22` guards them. If the diagram can't fit at 30 px,
render-card exits 2 (`LIMIT diagram-does-not-fit-at-minF-30px...`): cut words or ask for a bigger zone
in the plate prompt. Render with `--bg`: plain `--card` flattens transparency onto white.

## Samples (`samples/`, 2x)

| PNG | Zone (CSS px) | Fit |
|---|---|---|
| `diagram-flow.png` | 907 x 560 | `--f` 36.3 px |
| `diagram-compare.png` | 907 x 640 | 35.2 px |
| `diagram-parts.png` | 907 x 600 | 40 px (maxF) |

907 px is the slide width inside S11's 8% side margins. All three also fit 760 px wide zones at
30-38 px; flow at 640 x 400 correctly fails (exit 2).
