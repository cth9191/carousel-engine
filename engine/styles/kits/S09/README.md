# S09 card kit

HTML cards for the magenta zones of S09 Charcoal Studio plates (`engine/styles/S09-charcoal-studio.prompt.md`). Inter
and JetBrains Mono at the S09 tokens (`kit.css`): ground #151515, off-white #F2F0EA, acid yellow #F5F400, grey #8E8A82.
Cards are square-cornered faces; the plate paints the outlines and its rounded magenta mask trims the corners.

| Card | Zone | Sample size (CSS px) | Copy limits (enforced) |
|---|---|---|---|
| `list-NN.html` | outlined panel: checklist (`check`, `warn` rows), numbered list (`num`), arrow table (`arrow`) | 936×330 | title ≤ 34 chars; 3–6 rows; name ≤ 26; text ≤ 56 |
| `grid-NN.html` | outlined panel: roadmap strip or tells / truth columns | 936×300 | label ≤ 30; 2–4 cols; head ≤ 18; 1–4 cells ≤ 40 chars; `✓ ` cells get a check box |
| `terminal-NN.html` | terminal zone (the card is the whole window) | 936×420 | title ≤ 40; text ≤ 110 words; ≤ 3 highlights, each in the text |
| `stats-NN.html` | outlined panel: 2–4 measured values joined by yellow arrows (`down` or `right`) | 300×440 | label ≤ 32; value ≤ 10; caption ≤ 24 |
| `bar-NN.html` | the yellow footer bar | 936×74 | lead ≤ 4 words; ≤ 14 words in all; ≤ 1 figure |

The kit ships no character. The cyan character slot is for your own mascot, if you have one: a cut-out PNG with alpha
(trimmed, its aspect written into the prompt's `{mascot W:H}`), pasted with
`--logo C1=$D/assets/mascot.png@1.0,bottom`. Never a licensed character, and never drawn by the model. With no mascot,
the prompts ask for no character slot. Give each appearance a different painted prop, since the prop carries the
slide's meaning.

## Fill one

1. Copy `kit.css`, `kit.js` and each card into `$D/cards/` (`list-03.html`, `bar-03.html` …). Edit only the JSON in
   `<script id="data">`. Words come from `strings[]`; every figure, command and prompt from the dossier, copied from the
   source and run once.
2. Find each zone: `python -I shared/composite.py $D/plates/slide-NN.png --zones-only` and read its `out bbox`.
3. Render at that size, 2x:

   ```
   node shared/render-card.mjs $D/cards/list-03.html $D/cards/list-03.png --w 936 --h 330 --scale 2 --bg "#151515" --min-px 20
   node shared/render-card.mjs $D/cards/bar-03.html $D/cards/bar-03.png --w 936 --h 74 --scale 2 --bg "#F5F400" --min-px 20
   node shared/render-card.mjs $D/cards/terminal-08.html $D/cards/terminal-08.png --w 936 --h 420 --scale 2 --bg "#0E0E0F" --min-px 18
   ```

   Exit 0 is required. Exit 2: overflow, text under the floor, or a `LIMIT-<rule>`. Cut the copy.
4. Composite (zones are numbered in reading order; check the `--zones-only` debug PNG). The `--logo C1=…` line is only
   for a deck with a mascot:

   ```
   python -I shared/composite.py $D/plates/slide-03.png $D/final/slide-03.png \
     --shot 1=$D/shots/x.png@x,y,w,h --card 2=$D/cards/list-03.png --card 3=$D/cards/bar-03.png \
     --logo C1=$D/assets/mascot.png@1.0,bottom --dilate 3 --report $D/runs/composite/03.json
   ```

## samples/

`list.png`, `grid.png`, `terminal.png`, `stats.png`, `bar.png`: each card rendered at its sample size, 2x, with the
placeholder data in its `<script id="data">` (exit 0).
