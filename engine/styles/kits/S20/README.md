# S20 Slate Family Tree: card kit

HTML cards for `shared/render-card.mjs`, pasted onto Codex slate plates. Spec: `engine/styles/S20-slate-family-tree.prompt.md`
("Card kit"). All sizes are CSS px on the 1080 x 1350 slide. Every card is **transparent**: render it without `--bg`.

## Use in a deck

1. `cp engine/styles/kits/S20/{kit.css,tree.js} $D/cards/` plus the card files you need.
2. Copy a sample per slide (e.g. `tree-family-4.html` -> `cards/tree-03.html`) and replace the JSON in
   `<script id="data">` (or the `<pre>` text for the recipe card). Change nothing else.
3. Read the zone: `python -I shared/composite.py plates/slide-03.png --zones-only` -> `out bbox` W x H.
4. Render: `node shared/render-card.mjs $D/cards/tree-03.html $D/cards/tree-03.png --w W --h H --scale 2`
   (exit 0 required; it prints `name_px`, `chip_px` and any limit `violations`).
5. Paste (band keyed magenta): `python -I shared/composite.py plates/slide-03.png final/slide-03.png --card M1=cards/tree-03.png --ground fill`
   (`--card C1=…` if the band is cyan). The zone is erased into the slate, then the card is alpha-composited.

## Cards

| File | What | Zone (8–92% wide) | Nominal W x H |
|---|---|---|---|
| `tree-family-3/4/5.html` | Family tree: definition, rule, drops, 3–5 children, ≤ 4 chips | 52–88% high (1.87:1) | 907 x 486 |
| `tree-proof.html` | Proof-slide tree: definition, 3–5 children, ≤ 2 chips | 61–88% (2.49:1) | 907 x 365 |
| `tree-mix.html` | Mix tree: what the pair does together, 2–3 children, ≤ 3 chips | 53–88% (1.92:1) | 907 x 473 |
| `tree-cta.html` | CTA tree: no definition, 3 children, ≤ 2 chips, centred vertically | 44–78% (1.98:1) | 907 x 459 |
| `recipe.html` | Recipe: 2 px cream outline, verbatim JetBrains Mono 30 px, fit floor 28 px | 26–88% (1.08:1) | 907 x 837 |
| `serif-text.html` | Serif fallback: one Instrument Serif string (cover row or family name) that garbled twice; `align` center or left | the flat zone where it sat | e.g. 760 x 116 |

Shared: `kit.css` (tokens and layout), `tree.js` (builds the tree from the JSON, fit pass, limit check).

## Tree JSON

```json
{ "variant": "family", "definition": "≤ 12 words on what the item does.",
  "children": [ { "name": "Block deletes", "start": true, "chips": ["Before any tool", "`rm -rf build/`"] } ] }
```

- A chip in backticks is a code token (JetBrains Mono, exact case); others are Inter Italic.
- Limits (checked; a breach exits 2): names / chips ≤ 13 / 15 characters with 2–3 children, 9 / 11 with 4,
  7 / 9 with 5; code tokens 2 shorter; ≤ 1 code token per child, ≤ 2 per card; ≤ 1 `start` (none with 5 children);
  definition ≤ 12 words. Wide capitals (M, W) can still overflow at the limit; render-card names the column.
- Fit pass: names share one size, 44 -> 38 px (one baseline); chips share one size, 30 -> 26 px only when a chip
  outgrows its column.

## Samples

`samples/*.png` are the cards above at their nominal size, `--scale 2`. `samples/slate-composite-proof.png` is
`tree-family-4.png` pasted with `--card M1=… --ground fill` onto a synthetic `#2F2F2F` slate plate.
