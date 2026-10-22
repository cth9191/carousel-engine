# S23 proof-card kit

Opaque HTML cards for the magenta card zones of S23 Crop-Mark Proof Sheet plates (`engine/styles/S23-crop-mark-proof-sheet.prompt.md`).
Anton, Inter and JetBrains Mono at the S23 tokens: cream `#F5EBE0`, ink `#0E0E0E`, orange `#D9551F`, sheet white `#FBF8F3`,
warm grey `#8A847C`. The `.card`, `.audit` and `.chart` rules in `kit.css` are lifted from `templates/03-command-press/slides.html`
(CSS only; none of its sample copy).

| Card | Zone it fills | Sample size (CSS px) | Copy limits (enforced) |
|---|---|---|---|
| `before-NN.html` | before/after: the ink stack's front face. Faint halftone stipple lower-left | 364x331 (1.1:1); 364x291 under a two-line headline | title ≤ 14 chars; prose ≤ 28 words, or code ≤ 8 lines (6 in the 1.25:1 zone), ~30 chars a line |
| `after-NN.html` | before/after: the sheet-white stack's front face. The tag line carries the exact lowercase command | same | command ≤ 22 chars, lowercase; title and lines as above |
| `audit-NN.html` | chart + audit: the tall right column. Ink-header audit card with the command, then BEFORE / AFTER tab cards | 346x460 (0.75:1) | command ≤ 22; 2-4 rows ≤ 26 chars; tab text ≤ 64 chars; verdict ≤ 10 |
| `chart-NN.html` | chart + audit: the sheet on the left. Two-tone lines (orange = with the skill, ink = without), pill labels at the line ends | 484x400 | pill ≤ 14 chars; x title ≤ 18. The plate paints the chart title |
| `file-NN.html` | triptych: the output-file face. Command title row, the file it wrote, icon + label rows, orange folded corner | 262x374 (0.7:1) | command ≤ 18; file ≤ 24; 3-5 rows, label ≤ 14, value ≤ 22. Icons from `icons.js` |
| `typeline-NN.html` | split: the slim caption under the body; capture: the optional caption under the frame. `> /command` on ink + one short line | split 464x93 (5:1); capture 432x62 (7:1) | command ≤ 22; line ≤ 40; one-row zones (< 80 px tall): command + line ≤ 36 |

## Fill one

1. Copy the whole kit into the deck: `cp engine/styles/kits/S23/{kit.css,kit.js,icons.js} $D/cards/` and each card you need as
   `$D/cards/<card>-NN.html` (NN = slide number).
2. Edit only the JSON in `<script id="data">`. Every string comes from the real run saved in the slide's `evidence.source`
   (README or SKILL.md, a terminal run, the source page). Chart points come from that run, never an illustrative curve.
   The sample strings in this folder are placeholders.
3. Find the zone size: `python -I shared/composite.py $D/plates/slide-NN.png --zones-only` and read the zone's `out bbox`.
4. Render at that size, 2x:

   ```
   node shared/render-card.mjs $D/cards/before-04.html $D/cards/before-04.png --w 364 --h 331 --scale 2
   ```

   Exit 0 is required. Exit 2 means text overflowed, fell under 14 px, or broke a copy rule: the printed
   `LIMIT-<rule>` names it. Fix the copy, never the floor.
5. Paste with `composite.py … --card N=$D/cards/before-04.png --dilate 3`.

Faces are opaque and fill the zone edge to edge; the plate paints the stacked back sheets, arrows and labels around them.
Text renders with ligatures off, so `===` and `=>` stay exact.

## samples/

`<card>.png` is each card with its sample data at the sample size. `<card>-longest*.png` (where present) is the same
card at the longest strings its limits allow, at the tighter zone (before/after at 364x291). All passed render-card
with exit 0. The sample strings are placeholders, not a real run.
