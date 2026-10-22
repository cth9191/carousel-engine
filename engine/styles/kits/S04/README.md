# S04 card kit

Opaque-faced HTML cards for the magenta card zones of S04 Brutalist Mascot Poster plates
(`engine/styles/S04-brutalist-mascot-poster.prompt.md`), plus a chip patch for the cover. The look: sheet-white face
`#FBF8F3`, 3 px ink outline, 16 px radius, Anton terms, Inter ExtraBold lines, orange `#D9551F` on one accent only.

| Card | Zone it fills | Sample size (CSS px) | Copy limits (enforced) |
|---|---|---|---|
| `table-NN.html` | Table layout (what / model / parts / paper / verdict): ruled rows, Anton term, divider, plain-words line | 928x480 (3 rows); about 928x320 for 2 rows, 928x560 for 4 | 2–4 rows; term ≤ 10 chars; line ≤ 44 chars; exactly one `accent` row |
| `prompt-NN.html` | Prompt layout (peak / start): orange label tab + the exact text. `face` paper for prose, ink for commands | 914x398 | label ≤ 30; prose ≤ 40 words, or mono ≤ 8 lines × 40 chars |
| `steps-NN.html` | Steps layout (start / step): orange numbered squares; backticks set an exact command in mono | 914x300 (3 steps); at least 105 px of height per step | 2–4 steps, ≤ 52 chars each (backticks not counted) |
| `chip-NN.html` | Not a zone: a flat tag tile to patch a cover chip the plate misspelled | the painted chip's box | ≤ 6 chars; colour orange or ink; tilt −8…8° |

The kit ships no mascot. The cover's cyan slot takes your own mascot pose (optional; a transparent PNG you made,
never a licensed character) or, with no mascot, the subject's real logo tile; see the prompt block's Compositing
section.

## Fill one

1. Copy the kit into the deck: `cp engine/styles/kits/S04/{kit.css,kit.js} $D/cards/` and each card you need as
   `$D/cards/<card>-NN.html` (NN = slide number).
2. Edit only the JSON in `<script id="data">`. Commands, prompts and configs come verbatim from the source in the
   slide's `evidence.source` (README, SKILL.md, the run). The sample strings in this folder are placeholders.
3. Find the zone size: `python -I shared/composite.py $D/plates/slide-NN.png --zones-only` and read its `out bbox`.
   Codex returns zones 15–25% wider than asked: always render at the measured bbox.
4. Render without `--bg` (the rounded corners stay transparent), 2x, at a 22 px floor:

   ```
   node shared/render-card.mjs $D/cards/table-02.html $D/cards/table-02.png --w 906 --h 414 --scale 2 --min-px 22
   ```

   Exit 2 means the copy broke a limit (`LIMIT-<rule>`), overflowed, or fell under 22 px. Cut the copy, never the floor.
5. Paste with `composite.py … --card M1=$D/cards/table-02.png --ground fill --dilate 3` (the zone is erased into the
   paper first, so the corners land on the plate's own grain).

Chip patch (only after letter-by-letter QA finds a bad chip): render `chip-NN.html` at the painted chip's box in final
pixels and run `python -I shared/composite.py $D/final/slide-01.png $D/final/slide-01.png --paste $D/cards/chip-2.png@x,y,w,h,erase`.

## samples/

`<card>.png`: each card with its sample data at the sample size. `<card>-longest*.png`: the longest strings its
limits allow. All passed render-card with exit 0 at `--min-px 22`.

The style's exemplars (`engine/styles/exemplars/S04-cover.png`, `S04-interior.png`) come from a smoke test on a
placeholder topic ("linked notes"): two Codex plates from this block, the interior with `table-NN.html` pasted into
its card zone. On the cover, the cyan slot is shown as a dashed "your mascot" placeholder.
