# Template 05 — Node Pipeline

The html-native kit for style **S16 Neon Node Pipeline** (`engine/styles/S16-node-pipeline.prompt.md`). Pure black,
one glowing colour per concept, numbered icon-node pipelines with beaded connectors. Every diagram is drawn from
the slide's `graph` data: you never place a node by hand, and nothing is AI-painted.

## When to use

- **Spine C** listicles ("N ways X is built"): `cover-overview` (a grid of every item's own diagram), then one
  `pipeline` proof slide per item in its own colour, an optional combo, then `cta`.
- **Spine D** system builds: `cover-system`, then `inspector` slides with the same rail in build-up states.
- **Spine A** explainers: `cover-system`, `pipeline` explain (what) and parts (model), `compare` (why),
  `inspector` with a capture (how) or an exact-text card (peak, start), `cta`.
- Not for head-to-heads: a pipeline explains, it doesn't prove.

## Workflow

1. Copy `slides.html` and `assets/` into `carousels/<id>/`.
2. Put the white logos you need in the deck's `assets/` as `<name>-white.png` (`claude-white.png` ships in this
   template's `assets/`; make others from your logo folder or a simple-icons SVG filled #F5F5F5, rendered to a
   transparent PNG with `node shared/render-card.mjs <svg> <png> --w 512 --h 512 --scale 2`). A tool node's
   `logo: 'claude'` means `assets/claude-white.png`; any other path (`'assets/x.png'`) is used as written. Never a
   dark mark (it vanishes on #111111) or a teal, cyan or purple one (banned hues).
3. Put real captures in `assets/` (`shared/shots.py` for video frames, Playwright for web pages). Delete the
   sample `docs-*.png` captures.
4. Edit `DECK.label` and `slides[]` at the bottom of `slides.html`. The sample deck is a worked example of every
   layout but `cover-overview` (shown below).
5. `Invoke-Item carousels/<id>/slides.html`. A red **FIT FAILED** box lists every rule a slide breaks. Fix the copy
   or the graph; the type never shrinks.
6. Tweak (⚙): haze, connector opacity, bead spacing, titles, captions, capture src/focus, row-gap cap.
   📋 Export → paste the JSON in chat → copy the values into each slide's fields / `defaults`.
7. `node shared/export.mjs --carousel <id>` → `exports/slide-NN-YYYY-MM-DD.png`. Exit 1 = a slide failed its fit
   pass (the message names the slide and rule); exit 2 = a capture or logo `<img>` didn't load.

## Slide data

`DECK = { label, counterOffset?, counterTotal? }`: set `counterOffset: 1, counterTotal: N` when the cover is made
outside this file (an HTML-composed cover rendered with render-card as slide 01); give each slide an
`exportName: 'slide-02'` … so the exports line up.

```js
{ name:'Router', layout:'pipeline', variant:'proof', color:'amber',   // proof | explain; parts:true = sub-labels
  title:'Router', gloss:'one triage step, many specialists',           // title ≤3 words; title+gloss ≤7 words
  graph:{
    rows:[ [ {label:'Support ticket', icon:'chat'} ],
           [ {label:'Haiku sorts', kind:'tool', logo:'claude'} ],
           [ {label:'Refunds', icon:'scale'}, {label:'Bugs', icon:'wrench'}, {label:'Sales', icon:'person', state:'ghost'} ],
           [ {label:'Reply sent', kind:'decision', icon:'check'} ] ],
    edges:['1>2','2>3','2>4','2~5','3>6','4>6','5~6'],   // optional; omitted = auto (fan out / merge / straight)
    loop:{ from:6, to:2, tag:'until it passes' } },     // optional, one per slide; ids or badge numbers
  proof:{ img:'assets/x.png', focus:'50% 0%', fit:'cover', tag:'THE LOGS' },   // fit 'contain' letterboxes
  caption:'One phrase in <b>the accent</b>, ≤20 words.',
  defaults:{ gapMax:120 } }
```

- **Node:** `label`, `kind` (`step` circle · `decision` diamond · `tool` #111 disc with a white logo), `icon`
  (Lucide name or alias: magnifier, chat, checklist, terminal, wrench, branch, merge, layers, database, eye, repeat,
  scale, person, bolt, check, file…), `state` (`ghost` for a path not taken; `done`/`live` on rails — leave unset
  on pipelines), `sub` (parts diagrams), `color` (combo slides), `id`. Badges number 1..N in reading order
  automatically. The first and last single-node steps get the deep fill.
- **storyboard.json form** works verbatim: `graph:{rows:[['a'],['b','c']], nodes:[{id:'a',…}], edges:[{from,to,kind}], loop}`.
- **Layouts:**
  - `cover-system`: `title` (≤7 words, `<em>` = orange phrase), `gloss` (subline ≤9 words), `stamp`, `graph`
    (≤3 nodes a row) + `output:'Label'` (the larger unnumbered bolt node; counts toward the 4 rows).
  - `cover-overview`: `cells:[{of:'<item slide name>', name:'Router', hero:true}, …]` (1–6 cells, names ≤8
    characters). Each thumbnail is that slide's own layout, cropped to its diagram and contain-fitted (about
    36%), so cover and interiors always match.
  - `pipeline`: proof = ≤4 rows, ≤8 nodes in 16–66%, chip + tag + caption at 70–92%; explain = ≤5 rows, ≤9
    nodes in 16–82% (4 rows once any label wraps or has a sub-label), caption at 85–92%; parts = 2 a row.
  - `compare`: `left:{head, graph}` (always neutral grey; use `icon:'person'` on hand steps), `right:{head,
    graph}`, `proof`, `caption` (state the node-count difference). ≤4 nodes a side.
  - `inspector`: rail `graph` (one row, ≤5 nodes, labels ≤8 characters a line, 2 lines), `inspect` (badge or id;
    earlier nodes default to done, later to ghost), `panel:{title, img | text, focus}`. `text` is the exact-text
    card (≤14 lines, `<b>` = accent tokens). `tall:true` puts the rail down the left 30%.
    `uses:[{node, img, title}, …]` (2–3 live nodes) splits the panel into one zone per use.
    Payoff variant: set every rail node `state:'live'`.
  - `cta`: `keyword`, `caption` (the deliverable line), optional `colors` (default: every deck colour; three
    orange connectors on a one-colour deck) and `mascot:{src,w,h}` beside the output node.

## Colours

`orange` (Claude, hero item; the whole deck on spines A and D), `white`, `amber`, `lime`, `green`, `cobalt` — one
per item on spine C. No two touching overview cells may be orange-amber, lime-green or green-cobalt (set the cell
order). `grey` is reserved for the compare slide's old way. No purple, pink, teal or cyan anywhere.

## Fit pass (what throws)

Labels over 3 words or over 12 / 16 / 22 characters in a 4- / 3- / other row; label wraps where not allowed;
neighbouring labels colliding; rows or nodes over the layout's cap; rows not fitting their band (gap < 40 px);
loop tag with no room right of the loop; title over one line or 3 words; title + gloss over 7 words; caption over
20 words or its band; exact-text card over 14 lines or wider than its panel; cover headline over 2 lines or 7
words; hairline below 24%; unknown icon, colour, layout or node id; a tool node without a logo.

## Pitfalls

- **Captures are real.** Every proof chip, compare chip and inspector panel holds a real screenshot. Never an
  AI image, never an HTML mock passed off as a capture (exact text goes in `panel.text`).
- **Check the pipeline against the docs.** Node names, order and branches must match the real system.
- **Never reuse a reference deck's topic, node names or node-to-icon pairings.** Only the layout vocabulary carries over.
- **Logos are real white marks** (your logo folder or simple-icons); never draw a product mark or use a letter.
- **localStorage tweaks don't reach the bake.** Copy the 📋 Export values into `slides[]` first.
