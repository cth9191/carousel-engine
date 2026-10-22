# S10 kit

The cover and the exact-text card for S10 Command-Press Blueprint (`engine/styles/S10-command-press-blueprint.prompt.md`).
Interiors are `templates/03-command-press/slides.html` command sheets, unchanged; `kit.css` lifts that template's tokens,
grid, grain, frame, crosshairs and chrome so the cover and cards sit beside its sheets without a seam.

| File | What it makes | Size | Copy limits (enforced) |
|---|---|---|---|
| `cover.html` | The cover slide. `layout:"fig"` (2–3 Anton lines over FIG.0, a Codex FIG plate multiplied onto the grid) or `"stack"` (3–4 lines, type only) | 1080x1350, `--bg "#ECE3D4"` | chip ≤ 16; eyebrow ≤ 40 (accent in `*stars*`); lines ≤ 12 chars; FIG caption ≤ 46; cmd ≤ 22; stat ≤ 12 |
| `prompt-NN.html` | A prompt, command or config sheet (`face` sheet or ink), shown through Template 03's `image` hero; also the CTA's deliverable stub | 920 x 360–460 | tag ≤ 24; src ≤ 22; prose ≤ 45 words, or mono ≤ 8 lines × 44 chars |

The Anton stack auto-sizes: the largest size (≤ 300 px stack, ≤ 200 px fig) that fills its height and keeps the
widest line inside 920 px, measured after Anton loads (`window.cardInfo.headlinePx` reports it).

## Use

1. `cp engine/styles/kits/S10/{cover.html,kit.css,kit.js} $D/` and edit the cover JSON. For `fig`, point `fig.src` at
   the approved FIG plate (`plates/fig-00.png`); the plate's white ground disappears into the grid.
2. `node shared/render-card.mjs $D/cover.html $D/cover.png --w 1080 --h 1350 --scale 2 --bg "#ECE3D4" --min-px 16`
3. For each peak / start / CTA sheet: copy `prompt-NN.html` (and `kit.css`, `kit.js`) into `$D/cards/`, fill the JSON
   verbatim from the source, then
   `node shared/render-card.mjs $D/cards/prompt-07.html $D/assets/prompt-07.png --w 920 --h 400 --scale 2 --min-px 22`
   and set that sheet's `hero:{ type:'image', src:'assets/prompt-07.png' }`.
4. Bake the deck: `node shared/export.mjs --carousel <id>`.

Exit 2 from render-card means a copy limit (`LIMIT-<rule>`), an overflow, or text under the floor: cut the copy.

## samples/

- `cover-stack.png`: the stack layout, type only (placeholder topic).
- `prompt.png`, `prompt-ink-stub.png`: the card in both faces (`--min-px 22`, exit 0).
- A smoke test on the placeholder topic "linked notes": two Codex FIG jobs (`gpt-6.1-sol`, high, priority, no refs)
  from the block's FIG SYSTEM + FIG COVER / FIG INTERIOR → `smoke-fig-0-plate.png`, `smoke-fig-model-plate.png`;
  `smoke-cover-fig.png` is `cover.html` with FIG.0; `smoke-bake-01…04-*.png` is a Template 03 bake (cover, model sheet
  with the FIG plate, peak sheet with the prompt card, CTA with the ink stub) from `slides-sample.js`, the filled
  `slides[]` you can start a deck from.
