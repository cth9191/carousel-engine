# S06 card kit

Cards for the S06 statue cover (`engine/styles/S06-statue-graph-paper.prompt.md`). The interiors need no kit: they are
`templates/01-graph-paper-cream/slides.html`, copied into the deck.

| Card | What it is | Render | Copy limits (enforced) |
|---|---|---|---|
| `tile.html` | The held object: one real mark (`$D/logos/`) centred on a rounded app-icon tile (cream, white, ink or terracotta ground) | at the slot's aspect (`--zones-only` bbox, e.g. `--w 534 --h 512`) `--scale 2`, no `--bg` (transparent corners), into `$D/logos/tile-NN.png`; paste with `composite.py --logo C1=$D/logos/tile-01.png@1.07` | a mark is required |
| `cover.html` | The cover type over `fitted/slide-01.png`: kicker, 1–2 line Inter Black wordmark title, Playfair Display italic subtitle, soft shadow, optional bottom shade | full frame, `--w 1080 --h 1350 --scale 1 --min-px 30`, to `$D/final/slide-01.png` | kicker ≤ 3 words; title ≤ 2 lines of ≤ 12 characters; subtitle ≤ 6 words; block top ≥ 55% |

`kit.js` is the shared runtime both cards load. `"ink": "white"` on saturated skies (cobalt, amber, dusk), `"ink"` on
pale ones (overcast, studio grey). Turn `shade` off when the lower half is already dark.

## Deck route

1. Codex cover plate (SYSTEM + COVER + KEYING) → `plates/cover-a.png`; `composite.py … --zones-only` to find `C1`.
2. `tile.html` → `logos/tile-01.png`; `python -I shared/composite.py plates/cover-a.png fitted/slide-01.png --logo C1=logos/tile-01.png@1.07`.
3. `cover.html` → `final/slide-01.png`.
4. Copy `templates/01-graph-paper-cream/slides.html` to `$D/slides.html` and replace `{{BRAND}}` (the CTA handle pill;
   `brand` from `engine/brand.json`, or your handle); `slides[0].coverImg = 'final/slide-01.png'`;
   one `layered` slide per item (captures saved locally in `$D/assets/`, never hotlinked), the keyword CTA
   (`ctaKeyword`, `ctaDeliverable`, optional `ctaHeadline`; see `slides-entries.js`). The counter and slide count
   follow `slides.length`.
5. `node shared/export.mjs --carousel <id>` → `exports/`.

## samples/

From a smoke test on a placeholder topic ("top 3 browser-testing repos"): `plate-cover.png` (the untouched Codex
plate), `slide-01.png` (tile + type), `slide-02.png` (a template 01 item slide with a real README capture and repo
card) and `slide-03.png` (the keyword CTA, with the `{{BRAND}}` pill filled as `YOUR BRAND`), all baked with Template 01.
