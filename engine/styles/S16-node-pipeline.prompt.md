# S16 Neon Node Pipeline: prompt block

Pure black, one glowing colour per concept, numbered icon-node pipelines with beaded connectors, and a
listicle cover that grids the deck's own diagrams. The layout was studied from a high-performing
carousel; only its layout vocabulary carries over. Never copy any reference deck's characters, art,
words, hook, CTA phrasing, topic, node names, node-to-icon pairings, item set or signature palette.
Palette rules for this style: the concept colours are Claude orange, white, amber, lime, green and
cobalt (keying-safe), the cover headline glows white, and the cover hairline is Claude orange.

**Html-native by default** (`templates/05-node-pipeline`). The template renders every layout below
from each slide's `graph` data with the SYSTEM numbers as its tokens: copy
`templates/05-node-pipeline/slides.html` and `assets/` into the deck, put the white logos you need in
the deck's `assets/` as `<name>-white.png` (`claude-white.png` ships with the template; make others
from your logo folder or simple-icons), put real captures in `assets/`, paste each storyboard
`slides[].graph` into `slides[]` (the storyboard form works verbatim), then
`node shared/export.mjs --carousel <id>`. The fit pass throws on any copy cap or overflow, so export
exits 1 with the slide and rule named. Overview-cover thumbnails are the item slides' own graphs at
about 36%, so the cover needs no crops. The recipe is `templates/05-node-pipeline/recipe.md`.
Nothing on an S16 slide is painted on the html-native route; the prompt blocks below are the
image-native fallback, kept for a deck that wants a painted look.

**No style refs ship for this style.** On the fallback, the first prompts run text-only (SYSTEM plus
the layout); once the user approves a plate, that plate becomes the reference (see Notes).

On the fallback the cover comes last: brief card → interiors (plates → QA → composite) → thumbnail
crops → cover plate → cover composite. Paste SYSTEM into every slide prompt, plus that slide's COVER or
INTERIOR layout, plus KEYING when it has a slot. The rest is for Claude.

## Production split

Codex paints one plate per slide (7 nodes or fewer, labels of 2 words or fewer, sub-labels only on a
parts diagram), titles, node labels, badges and captions included, so QA reads every one against
`strings[]`. These parts are not painted:

| Element | Made by |
|---|---|
| Overview cover thumbnails | magenta cell zones → crops of the composited interior finals, pasted with `--card` (Notes) |
| Logos in tool nodes | cyan disc → `composite.py --logo N=logos/claude-white.png@0.9` (white `#F5F5F5` marks from your logo folder or simple-icons). An orange mark only on a non-orange slide; never a dark mark (it vanishes on #111111) or a teal, cyan or purple one (banned hues) |
| Captures (proof chip, compare chip, inspector panel, use zone) | magenta zone → `composite.py --shot N=shots/x.png@x,y,w,h` from `shared/shots.py`, cropped to a focus box (dark: `--letterbox edge`) |
| Exact text in an inspector panel (prompt, command, config) | HTML card in `<deck>/cards/`: JetBrains Mono 28-30 px, #E6E6E6 on #0B0B0B, caret and key tokens in the accent, 14 lines or fewer; `node shared/render-card.mjs` at the zone's `--zones-only` out bbox (2x), `--bg "#0B0B0B"`, pasted with `--card`. Opaque only: composite flattens transparency onto white |
| Your own mascot (optional, CTA only) | cyan slot → `composite.py --logo` (alpha-aware): transparent PNG poses you made, never a licensed character, never painted. With no mascot, ask for no mascot slot |

## Layouts by role

- **C:** `cover` overview cover · `why` (optional) compare · `item` proof pipeline in the item's
  colour · `combo` (optional) proof pipeline, each node in its own item's colour.
- **A and D:** `cover` system cover · `what` explain pipeline, 3 plain-word nodes, no component
  names, caption "X is a ___ that ___" · `why` compare · A `model`, D `parts` parts diagram, each
  part (4 or fewer for `model`) with a defining sub-label (on D, its body-role analogy).
- **A only:** `how` inspector with a capture · `peak` inspector with the exact-text card · `use` uses
  variant · `start` inspector with the install and first-command card. **D only:** `step` inspector,
  one rail repeated in build-up states · `day` payoff variant. Every `cta`: CTA slide.

**Colours.** Colours follow items; the story sets the order (G6). On spine C the hero item (the one
the deck recommends, or the Claude one) is Claude orange; the rest take white, amber, lime, green and
cobalt so no two touching cover cells (side by side, or overlapping across rows) clash: orange-amber,
lime-green or green-cobalt. White pairs with anything. Six items always solve; with fewer, drop a
clashing hue. Spines A and D are Claude orange throughout. The cover and CTA show every deck colour;
the compare slide's old way is neutral grey, never concept white.

## SYSTEM

Visual system: glowing node-pipeline diagrams on flat #000000; no grid, stars, noise, vignette or
gradient, only a faint radial haze in the slide's colour (about 10%, radius about 28% of the width)
behind the branching section. Each concept owns one colour (title, nodes, connectors, glow); the
prompt names this slide's, and no other appears unless the layout says so. Accent / glow / deep
fill / badge:
- Claude orange #D9551F / #FF8A4C / #4A1D0B / cream #F5EBE0
- White #F2F2F2 / #FFFFFF / #262626 / #F2F2F2; working nodes #3A3A3A, #F2F2F2 rim, never solid white
- Amber #F5A524 / #FFC766 / #4D3208 / #FFE3A3
- Lime #A3E635 / #C8F27A / #2C410E / #E2F5BD
- Green #2FD27A / #6EE89B / #0C3B22 / #C9EFD6, never mint or teal
- Cobalt #4F8EF7 / #8DB8FF / #0F2647 / #F2F2F2

Type: title Inter ExtraBold 60 px in the accent, tight same-colour glow plus a wide faint halo;
gloss under it Inter Medium 34 px #D6D6D6. Node labels Inter SemiBold 30 px #F5F5F5 under the node,
in a tight black halo no connector crosses. Tags, sub-labels and footer JetBrains Mono 28 px.
Footer: deck label in caps bottom-left, counter bottom-right, #5E5E5E.

Nodes: 76 px, each with a 36 px tinted badge (22 px bold ink #0E0E0E number) at 9 to 10 o'clock.
Step: circle, 3 px glow-tone rim, accent fill (grey on white); first input and final output in deep
fill. Decision: 58 px rounded square at 45 degrees, solid accent, only at a split, route or merge.
Tool: #111111 disc, accent rim, one logo slot; may be the split. Step and decision nodes hold one
upright generic line icon (34 px, 3 px stroke): white on orange, cobalt, grey and deep fills; ink on
amber, lime and green. Never a product mark or a letter as a logo.

Connectors: 3 px accent lines at about 45%, straight on diagonals, gently curved on verticals,
beaded in the glow tone about every 40 px (6 px beads, every third 9 px and glowing). No arrowheads.
Ghost paths (not taken): 2 px dashed white at about 18%, no beads. Glow only on titles, rims, beads
and haze. No 3D, bevels, glass, lens flare, bokeh, scanlines or drop shadows.

Framing: margins of at least 6% of the width at the sides, 4% of the height top and bottom; footer
baseline at 96%. At most 4 nodes a row; never shrink type. Badges run 1 to N top to bottom, then
left to right, none skipped or repeated.

References show layout vocabulary only. Do NOT copy their words, topic, node names, numbers, icon
pairings, handles, logos, off-palette colours, or flat #111111 placeholder panels and discs. No
characters unless the prompt names one and its slot.

Hygiene: render only the slide's Visible copy list (badge numbers and counter included), each string
verbatim, exactly as many times as listed. Never invent a node, branch, number or label; no UI text,
lorem ipsum, watermarks, handles or extra logos, and never these instructions or section names.

## COVER

**Overview cover.** Top: the headline, centred, 84 px, one or two lines, white with a soft white glow
(never pink), one accent phrase in Claude orange with its glow. Under it the subline in Inter Medium
36 px #BDBDBD, then on the same line the stamp in JetBrains Mono #BDBDBD. Then a 2 px Claude-orange
hairline (#D9551F at about 55%) across the margin width, above 24% of the height. From 25% to 92%,
the grid: one cell per item slide in slide order, no boxes or borders, gutters of at least 4% of the
width. Each cell is the item's short name (56 px) in its accent with glow, centred over one thumbnail
area; the prompt gives each cell's colour. The hero cell is Claude orange, about 1.25 times the
others, its name 64 px with a brighter glow. 3 cells in one row, 4 as 2 x 2, 5 as 3 + 2, 6 as 3 x 2,
every row centred. Thumbnails are added later: paint nothing inside the thumbnail areas. Footer as
on the interiors.

**System cover.** Headline, subline and hairline as above. From 25% to 90%, the finished system as
one large centred Claude-orange pipeline, 4 rows or fewer of 1 to 3 nodes: one numbered 100 px node
per step or part, 1 to N matching the cover's count, all lit, labels 34 px, ending in one larger
unnumbered output node with a bolt icon. Tool nodes hold logo slots and are the focal point. One haze
behind the widest row. No caption.

## INTERIOR

**Pipeline slide.** Title at top centre. The pipeline runs top to bottom, centred, from 16% of the
height, in rows of 1 to 4 nodes. A split leaves a decision diamond (or the deciding tool node) and
fans out on straight diagonals; a merge converges on a diamond. The route taken is beaded, the rest
are ghost paths. At most one loop: a beaded arc on the right back to an earlier node, with a short
mono tag. On a combo slide each node keeps its own item's colour. Caption: Inter Medium 30 px,
#D6D6D6, one phrase in the accent.
- **Proof:** 4 rows and 8 nodes or fewer inside 16-66% of the height. A proof band fills 70-92%. On
  its left (6-52% of the width), the proof chip: a 16 px-radius rectangle, 2 px accent rim at 60%,
  holding one capture; a short ghost connector with one elbow runs from the last node to its top
  edge. On its right (56-94%), a mono tag in the accent naming what the chip shows, the caption
  left-aligned under it.
- **Explain:** no capture. 5 rows and 9 nodes or fewer inside 16-82% (4 rows if any label wraps or
  has a sub-label); caption centred at 85-92%, one or two lines. Parts diagram: a sub-label under
  each label (JetBrains Mono 28 px, #BDBDBD, up to 2 lines), 2 nodes a row at most.

**Compare slide.** Title as above. Two pipelines side by side under column heads (Inter SemiBold 32
px), split by a thin dashed ghost line, inside 20-66% of the height, 4 nodes or fewer each. Left, the
old way in neutral grey: #8A8A8A rims, labels and icons, #2A2A2A fills, no glow, a person icon on
every step a human does by hand. Right, the new way in its accent with full glow. Proof band at
70-92%: on the left the caption, stating the difference in node count; on the right a proof chip as
above, holding a capture of the new way running.

**Inspector slide.** Title line 1 (on a system build "Step {k}: {what you build}"), optional line 2.
Below, a left-to-right rail of 5 nodes or fewer at 16-33% of the height: 64 px nodes, 28 px labels of
up to 2 lines. An inspector panel fills 38-89%: #0B0B0B, 22 px corners, 2 px accent rim at 60%, a 56
px #141414 title bar holding the inspected node's badge and its label in mono. A beaded connector
drops from that node, with one elbow, into the bar. The panel holds one capture or exact-text card.
For a tall capture, the rail runs down the left 30% and the panel takes the right. Rail states: Done
(earlier) deep fill, no glow; Live (current) full glow, a thin accent ring 12 px outside, label in
the accent; Ghost (later) #161616 fill, #333333 rim, #555555 icon and label. Uses variant: 2 or 3
Live nodes, the panel split into one capture zone per use under its node, 24 px apart. Payoff
variant: every node Live, one capture of the system running.

**CTA slide.** Each deck colour enters from the top edge as its own beaded connector (three
Claude-orange ones on a one-colour deck), converging into one Claude-orange output node (about 180
px, bolt icon) at about 40% of the height. Under it "Comment {KEYWORD}" in Inter ExtraBold 88 px,
white, the keyword in Claude orange with its glow; then one deliverable line in Inter Medium 36 px
#CFCFCF. Counter only, no deck label. A mascot slot beside the output node only when the prompt names
a mascot.

## KEYING

Each {proof chip | inspector panel | use zone} screen and each cover thumbnail area is ONE solid flat
magenta #FF00FF rectangle of aspect {W:H}: frontal, no gradient, texture, glow, text, UI or tilt.
Capture zones have slightly rounded corners inside the accent rim; cover zones have square corners,
no rim, on black. No haze, bead, glow or hairline touches a zone; connectors stop with a visible gap.
Logo slot: ONE flat cyan #00FFFF disc, about 62% of its tool node, centred, a #111111 ring between it
and the rim; no icon, text, outline, shadow or glow.
Mascot slot: ONE flat cyan #00FFFF rectangle of aspect {W:H} on black beside the output node, 24 px
or more clear on every side.
No purple, violet, lavender, pink, rose or magenta outside the magenta zones, in glows, haze, beads
and badges too; no cyan, turquoise, teal or aqua outside the cyan slots. Cobalt never pales toward
cyan; orange and amber never drift to rose.

## Notes for Claude (not pasted)

- **Attach.** No refs ship. The first interior runs text-only; once the user approves one, it is
  Image 1 for every later prompt, attached as a composited final with its capture and logo areas
  flooded #111111 (`$D/refs/s16-locked-interior.png`): raw plates teach magenta and cyan, unflooded
  finals teach logos. Never attach another creator's slides: an image pulls palette harder than a
  sentence, and off-palette glows (violet, teal, pink) spread hue into key-like halos. Cover: attach
  two flooded locked interiors; a grid image only as a greyscale copy of your own
  (`$D/refs/s16-cover-grid-gray.png`).
- **Thumbnails.** Crop each item's composited final to its diagram (every node, label, ghost path and
  loop, padded 24 px; within 15-67% of the height on the proof variant) as an opaque PNG on #000000
  at native size; it keeps tiny labels and real logos.
  `python -I shared/composite.py plates/cover.png --zones-only` numbers the cell zones (M1..,
  reading order); paste each with `--card N=thumbs/slide-NN.png`. Contain-fit letterboxes in the
  crop's black border, so aspect warnings are harmless.
- **Zones.** Codex makes them wider than asked: keep a focus box on every shot, run `--zones-only`
  first, `--dilate 3` if a fringe shows. Tool nodes stay 64 px or more so each cyan disc clears
  `--min-logo-zone`.
- **Copy caps** (maximums). Codex can't fix copy, and every string goes in the slide's Visible copy
  list, never in a pasted block. Labels name one concrete run ("Support ticket", "Haiku sorts",
  "Refunds"), never "Input", "Output" or "Process": 3 words; 12 characters in a 4-node row, 16 in a
  3-node row, 22 otherwise (an explain diagram may wrap to 2 lines); if it doesn't fit, cut nodes.
  Title: a 1-3 word name ("Router") and a gloss ("one triage step, many specialists"), 26 characters
  a line, 7 words in all. Caption: 20 words, what it does, then when to use it. Tag: 4 words; loop
  tag: 3 ("until it passes"); sub-label and inspector line 2: 8 words; rail label: 8 characters a
  line; "Step {k}" matches the cover's count. Cover: headline 7 words ("6 AI Agent Patterns,
  Mapped"), subline 9, cell name 8 characters, stamp the month or a verified figure; a system cover
  names the system, step count and outcome. A compare caption has a number only if verified.
- **Icons** (one per step or decision node, named in the prompt): magnifier, chat bubble, file,
  checklist, terminal, wrench, branch, merge, layers, database, eye, repeat, scale, person, bolt,
  check.
- **QA.** Read every label, badge number, tag and caption against `strings[]`; count nodes,
  diamonds, branches and the loop against `slides[].graph`. Badges run 1 to N in reading order
  (a painted branch numbered 4, 6, 5 is a common miss).
