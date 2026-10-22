# S26 Whiteboard Doodle Showcase: card kit

Every word on an S26 slide is one of these HTML cards, rendered by `shared/render-card.mjs` and pasted into a
magenta zone of the Codex plate. Spec: `engine/styles/S26-whiteboard-doodle-showcase.prompt.md` ("Cards",
"Measurements"). Sizes are CSS px on the 1080 x 1350 slide. Shantell Sans 800/500 from Google Fonts.

## Use in a deck

1. `cp engine/styles/kits/S26/{kit.css,kit.js} $D/cards/`, then one copy per slide: `head-NN.html` ->
   `cards/head-03.html`, `cap-NN.html` -> `cards/cap-03.html`, plus `cover.html`, `cta.html`, `ink-card.html`.
2. Replace the JSON in `<script id="data">` (the `<pre id="text">` and label for the ink card). Change nothing else.
3. Read the zones: `python -I shared/composite.py plates/slide-03.png --zones-only` -> each `out bbox` W x H.
4. Render at that size, `--bg` = the plate ground sampled beside the zone (`#FBF8F3` on a clean plate):
   `node shared/render-card.mjs $D/cards/head-03.html $D/cards/head-03.png --w W --h H --scale 2 --bg "#FBF8F3"`
   (the ink card takes no `--bg`: it paints its own #141414). Exit 0 required.
5. Paste: `python -I shared/composite.py plates/slide-03.png final/slide-03.png --card M1=cards/head-03.png --shot M2=shots/x.png@x,y,w,h --card M3=cards/cap-03.png`
   (zone ids from step 3). If a card edge shows on the paper, re-sample `--bg` at that edge and re-render.

About two cards per item slide; 15–17 for an 8-slide deck.

## Cards

| File | What | Zone | Nominal W x H |
|---|---|---|---|
| `head-NN.html` | Counter "NN / TT" (26 px #8A8178, top-right), exact item name (800, real case, 120 -> 64 px; one line, else two), orange SVG marker underline 12 px, 104% of the last line | x 80–1000, y 64–330 | 920 x 266 |
| `cap-NN.html` | Caption, 500, 46 -> 36 px, centred, ≤ 4 lines, ≤ 34 words, a string or two paragraphs | x 100–980, y 906–1104 | 880 x 198 |
| `cover.html` | Hook lines (800, shared size 120 -> 64 px), the `key` line underlined, smaller aside (verified stars or month); counter optional | x 80–1000, y 64–830 | 920 x 766 |
| `cta.html` | CTA lines, `{keyword}` becomes the orange keyword in curly quotes; counter | x 80–1000, y 64–830 | 920 x 766 |
| `ink-card.html` | Prompt / command / config verbatim, cream JetBrains Mono on #141414, optional label, largest size 22–40 px that fits; fills the frame's capture zone edge to edge | inside the frame, x ~84–996, y ~360–880 | 912 x 520 |

Shared: `kit.css` (tokens), `kit.js` (builds head / cover / CTA / caption from the JSON, fit pass, underline,
limit check). A line that cannot fit at 64 px wraps once; past that, or past the caption limits, render-card
exits 2 and `card.violations` says why.

Caption length: 34 words only fit in 4 lines when the words are short. Plan on about 160 characters
(`samples/cap-NN.png` is 27 words / 147 characters at 37.5 px; 33 words / 190 characters failed at 36 px).

## Samples

`samples/*.png` at nominal size, `--scale 2`, `--bg "#FBF8F3"`. `head-NN-long-name.png` is
`awesome-claude-code-subagents`, which wraps to two lines at 81 px. The cover aside and every number in the
samples are placeholders: verify real figures on posting day.
