# S25 Soft-UI Step Guide: card kit

A complete 10-page starter deck for S25 (spec: `engine/styles/S25-soft-ui-step-guide.prompt.md`). Every
word is HTML; Codex paints only the cover plate. The kit mirrors a deck folder, so its relative paths
(`../fitted/`, `../shots/`, `../logos/`) work unchanged once copied.

| Path | What it is |
|---|---|
| `cards/s25.css` | Tokens, chrome (header, counter, traces) and every component: kicker, step pill, headline, body, module shell, terminal, capture mat, stat card, logo tile, logo grid, hub, command trio, rows (+ reasons variant), code chip, chip row, callout pill, quote card, composer, cover overlay (stack, hub, chips, terminal card, sticky, UI fragment, banner) |
| `cards/s25.js` | `S25.prep()`: swaps Lucide glyphs in, lays out and wires the hub module |
| `cards/icons.js` | The Lucide glyphs the pages use (generated, see below) |
| `cards/page-01.html` | **Cover**, over `../fitted/cover.png`: headline stack, logo hub + tilted chips, UI fragment, step sticky, terminal card, payoff banner |
| `cards/page-02.html` | **Definition** (what): capture + stat card, three-word chip row |
| `cards/page-03.html` | **Step without pill** (why): old way / new way, capture module, callout |
| `cards/page-04.html` | **Step 01**: terminal module, OS chip row |
| `cards/page-05.html` | **Step 02**: hub module (up to 6 spokes), callout |
| `cards/page-06.html` | **Step 03**: command trio, quote card |
| `cards/page-07.html` | **Step without pill** (model): 2x3 logo grid, callout |
| `cards/page-08.html` | **Rows** (use): 3-4 numbered rows with inline code chips + chip-row footer |
| `cards/page-09.html` | **Rows, reasons variant**: 5 rows, no footer |
| `cards/page-10.html` | **CTA**: keyword headline, composer card, chip row (keyword appears exactly twice) |
| `placeholder/plate-cover.html` → `fitted/cover.png` | A drawn laptop over paper. **Placeholder only, labelled as such; never ship it** |
| `shots/capture-a.png`, `capture-b.png` | Placeholder captures (stills from the author's own explainer video) |
| `logos/` | Real marks (Claude, Anthropic, OpenAI, GitHub; SVG sources plus transparent PNGs) and `avatar.png`, a neutral grey "YB" placeholder for the byline. Replace it with your square profile photo (or your brand mark) in each deck |
| `samples/` | The ten pages rendered (exit 0 each) with `{{BRAND}}` filled in as `YOUR BRAND` |

Every page's header reads `<img src="../logos/avatar.png">` + `{{BRAND}}`. The skill fills `{{BRAND}}`
from `engine/brand.json` when it copies the cards into a deck; replace it by hand if you render the kit
directly.

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/logos $D/shots $D/fitted $D/exports
cp engine/styles/kits/S25/cards/* $D/cards/
cp engine/styles/kits/S25/logos/github-ink.png $D/logos/   # + the deck's own marks
cp <your square profile photo>.png $D/logos/avatar.png      # or your brand mark
# fill {{BRAND}} in every page; one page per slide: copy the layout page you need to page-NN.html,
# renumber the counter ("NN / TT"), replace every sample string from storyboard strings[],
# point <img> at $D/shots and $D/logos
node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards   # after adding data-lucide glyphs
node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22
```

Exit 2 means overflow or text under 22 px: shorten the copy, never shrink the floor.

## Fit and limits (measured on the kit)

- Headline: 1-2 lines, fitted 112 → 96 px. At 96 px a 2-line headline holds about 32 characters
  ("Add the tools you use every day" fits; a third line fails).
- Body: 640 px wide, 4 lines, fitted 32 → 30 px. Four lines hold about **30-32 words**, not the card's
  40; a 37-word body exits 2.
- Module: one per page, ending at y 1120. Footer: at most one of chip row / callout / quote card at y 1160-1270.
- Rows: 3-5 cards share the zone (112-150 px each); with a footer the rows end at y 1160.
- Hub: 1-6 spokes, first half left, rest right. A tool with no mark file gets `.logo.mono-tile` (its
  initial in ink); a generic surface (terminal, browser) gets `.logo.glyph-tile` with a Lucide glyph.
  Neither stands in for a product's mark: put the real file in `$D/logos/` when it exists.
- Cover: the stack lines fit to 940 px (giants 136 → 110). Cards keep off the laptop screen
  (x 270-810, y 756-1093) except 60 px of its edge; the terminal card may sit over the base.

## The cover plate

`page-01.html` uses `body.on-plate` = `url(../fitted/cover.png)`. Make it with Codex (SYSTEM + COVER
plate + KEYING, text-only, 2 variants), then
`python -I shared/composite.py $D/plates/cover.png --zones-only` (one magenta zone, fill ≥ 0.97) and
`python -I shared/composite.py $D/plates/cover.png $D/fitted/cover.png --shot 1=$D/shots/<s>.png@x,y,w,h`.
Until then the kit's placeholder shows where things sit.
