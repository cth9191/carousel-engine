# S07 Dark Network Hero: prompt block

Reusable visual-system text for Codex plate prompts. The exemplars are a "meet <NAME>" system-reveal cover
(`engine/styles/exemplars/S07-cover.png`) and a dark interior from a `/<command>` memory-tool deck
(`S07-interior.png`). **Hybrid, plate-first**: Codex paints ONE text-free network plate per slide, and the
kit page `engine/styles/kits/S07/page.html` sets every word, chrome mark, logo tile, brush label, capture
window and card over it. Nothing on an S07 plate is ever read, so the plates carry no key colours.

Refs (attach in this order until a locked cover exists, then the locked cover first and one swatch second):
`engine/styles/refs/s07-ref-teal.png` (a clean 905×333 crop of a network plate: node and hairline rendering,
the default teal ground) and `engine/styles/refs/s07-ref-ember.png` (a text-free warm plate: the `ember`
ground). Never attach finished exports (the exemplars included): they carry words and logos the model would copy.

**Why the interiors are full, not sparse.** Bare black interiors, a headline on an empty field, read as bland.
Every S07 interior plate paints a **network figure** that acts out the slide's lesson (two clusters for a
before/after, four named communities for a model, a thread running into the terminal), and the page lays a
glass capture window, a stat strip or a rail on top of it, so each slide has a lit picture, a real proof and
big type. No interior is a headline on an empty black field.

Brand: the footer's left word is the `brand` in `engine/brand.json` (`{{BRAND}}`), set in each page's `footer`.

## Production split

| Element | Made by |
|---|---|
| Network plate (ground, glow, the slide's network figure, calm space for type) | Codex, one per slide: SYSTEM + COVER or one INTERIOR figure; no text, no logos, no frames |
| Fit to 1080×1350 | `python -I shared/composite.py $D/plates/slide-NN.png $D/fitted/slide-NN.png` (no zones: it only fits) |
| Every word: kicker, giant name, headline, body, section label, counter, footer, tag, footnote | `cards/slide-NN.html` from the kit (Inter Black / Inter / JetBrains Mono) |
| Brush label and dashed hand arrow | Drawn by the kit (SVG dry-brush stroke, dashed curve), never painted |
| App / logo tiles (cover column, icon cover, CTA row) | Real marks in `$D/logos/` (your own logo files, or simple-icons SVGs rendered to PNG with `render-card.mjs`), placed by the kit; never painted |
| Captures (glass windows in define, stage, versus, receipts) | Real shots in `$D/shots/` (`shots.py`, Browser pane), placed by the kit with a `focus` position |
| Prompts, commands, configs (terminal, steps) | Exact text in the kit's terminal and rail, copied from the source and run once |
| Numbers (versus, receipts) | Verified figures from the dossier, in the kit's stat cells; vendor numbers labelled as the vendor's |

Render each slide: `node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22`.
Exit 2 = overflow, text under 22 px or a broken copy rule (`LIMIT-<rule>`): cut the copy, never the floor.

Copy (enforced by the kit): headline ≤ 7 words with one `*accent*` phrase; body ≤ 35 words on define, ≤ 30 on
stage, ≤ 25 on versus/terminal/receipts, ≤ 20 on parts/steps. Giant name ≤ 12 characters (the `name` cover) or
≤ 14 (`/command` on the `icon` cover); brush label ≤ 22 characters, ending in `*` only when a footnote answers it;
footnote ≤ 8 words. The section label is the storyboard's own (`02 — why it works`), lowercase, numbered from the
first interior. The cover tag is the deck's own mono line (your mantra or the system's name), never a handle.

## Layouts by role

| Role (spine A) | Role (spine D) | `layout` | Plate figure (INTERIOR) | Page content |
|---|---|---|---|---|
| cover | cover | `name` (default) or `icon` | name cover / icon cover | kicker + giant name + brush label + tile column + footnote + tag; or /command + big app tile + subline |
| what | what | `define` | define | definition body + 2–4 plain-word chips + capture |
| why | why | `versus` | versus | old vs new: two stat columns, optional capture each (PROVE) |
| model | parts | `parts` | parts | 3–4 named parts, ≤ 8 words each, at the clusters (set `pos` if the plate moved them) |
| how | step | `stage` | stage | one capture with up to 3 numbered pins (PROVE) |
| peak | step (prompt) | `terminal` | terminal | the exact prompt or command |
| use | day | `receipts` | receipts | 2–3 verified numbers + capture |
| start | step (setup) | `steps` | steps ({N} = the step count) | 3–4 rail steps with exact commands |
| cta | cta | `cta` | cta | sign-off + Comment KEYWORD pill + deliverable (+ tiles) |

Spine D's N steps use `stage`, `terminal` or `steps` per step; its cover is `name` with the system's parts as the tile
column. Not for listicles (no per-item tile layout) or head-to-heads (S03).

## SYSTEM

Visual system: a dark network field, like a live knowledge graph seen at night. Ground near-black (#06090B) with a
faint cold teal cast, deepest at the corners and edges. On it, a network of small glowing nodes joined by straight
hairline edges: nodes are soft round points in three sizes (most tiny, some medium, a few large with a gentle
bloom), edges are thin single-pixel lines at low opacity, crossing freely, with no arrows. Colour (teal ground):
nodes in luminous teal (#39C6BF) with white-hot centres on the largest, edges in deep teal (#1E6F6B) at 30–50%
opacity, a soft teal bloom only around the densest clusters. Colour (ember ground, when the prompt says ember):
nodes in warm terracotta (#D97757), amber (#E8A35A) and a few cream-white, edges in dim warm brown, the same
restraint. Density varies on purpose: the figure the prompt asks for is dense and bright, the rest of the field is
sparse, and the areas reserved for type are almost empty (a few dim far nodes, no bright ones, no edges crossing
bright). Depth: far nodes are smaller and dimmer; a few near nodes are larger and slightly out of focus.

Contrast: true dark blacks. No haze, no fog, no milky or grey veil over the frame, no lifted blacks, no smoke, no
vignette glow; the glow belongs to the nodes and the densest clusters only. Flat digital render, crisp; no
lens flares, no light rays, no stars with spikes, no particles that read as dust, no 3D objects, no planets, no
brains, no circuit boards, no city lights.

Framing: the plate is 4:5, 1080 × 1350, full bleed (the network may run off every edge). Reserved type areas named
in the composition stay calm: darker and sparser than the rest, with no node brighter than mid-grey there.

References: Image 1 (and Image 2) show how the nodes, edges and glow are rendered and the ground colour. Match that
rendering. Do NOT copy their exact layout, and never add anything they don't have.

Hygiene: this is a background plate. NO text of any kind: no letters, numbers, labels, captions, UI, code, logos,
icons, symbols, watermarks or signatures. No frames, windows, panels, cards, buttons or rectangles; no brush
strokes, arrows or hand-drawn marks (they are added later). No purple, violet, pink, magenta or blue-violet; keep
to the ground's palette. Never render these instructions or section names as text.

## COVER

**Name cover** (`layout: "name"`, the "meet <NAME>" shape). The top 34% of the frame is calm and dark: the giant
name and its kicker are set there later. Below it, the network fills the frame as one huge loose cloud from about
35% down to the bottom edge, densest and brightest in a wide core centred near 48% across and 62% down, thinning
toward the edges. Along the bottom 14%, a faint perspective floor grid: thin dim horizontal lines, closer together
toward the horizon at about 86%, under the network. Calm patches, darker and sparser, at: the right side from 50% to
61% down (a brush label goes there), the bottom-right corner from 82% to 94% down (a footnote), and a narrow left
column from 6% to 16% across, 60% to 97% down (logo tiles). The core never sits under those patches.

**Icon cover** (`layout: "icon"`, the "/<command> over one app tile" shape; ember or teal). The top 18% calm and
dark (a giant /command). The network radiates from a centre at 50% across, 39% down: a dense bright ring of nodes
around an empty dark square about 44% of the width wide at that centre (an app tile covers it later), with long
edges reaching out to every side. From 59% to 78% down, the field is darker and sparser (three lines of type). The
lower 20% is a dim continuation of the network.

## INTERIOR

Every interior plate: the top 36% is a calm, dark, sparse stretch of the same network (section label, headline and
body go there), then the slide's **figure** below it. Name the figure in the composition with its positions:

**define** (what): the network gathers from the sides into the edges of a calm, dark, empty rectangle from 9% to 91%
across and 53% to 91% down (a capture window covers it later), as if feeding it; a bright thread of nodes runs along
42% to 47% down from edge to edge, under the strip of chips.

**versus** (why): the field splits at the vertical centre line. Left half (old way): scattered dim grey-teal nodes
with almost no edges, isolated and cold. Right half (new way): one dense, connected, bright cluster centred at 73%
across, 66% down, with a warm terracotta tint at its core. A faint seam of empty dark at 50% across.

**parts** (model): three or four distinct glowing clusters ("communities"), each about 22% of the width across, centred
at 27%/47% and 73%/47%, then 27%/73% and 73%/73% (four) or 50%/73% (three). The top two centres sit at 47% down,
clearly below the calm top 36%, never higher (a test plate put them at 41%). The first cluster is tinted warm
terracotta, the others teal. A few long faint edges link the clusters to each other. Under each cluster, from 3% to
13% of the height below its centre, the field is dark and sparse (a name and a short line go there).

**stage** (how / step): a calm, dark, empty rectangle from 6% to 94% across and 40% to 92% down (the capture window),
with the network's edges running into its four sides from the surrounding field and a band of brighter nodes along
its top edge.

**terminal** (peak): one bright braided thread of nodes descends from a dense cluster in the upper-right (around
80% across, 30% down) and runs into the top edge of a calm, dark, empty rectangle from 6% to 94% across and 39% to
89% down.

**receipts** (use): two or three bright nodes in a row at 37% down (above the stat cells), each with a small halo,
linked by a glowing edge; below, a calm, dark, empty rectangle from 6% to 94% across and 53% to 92% down with edges
running into its sides.

**steps** (start): a vertical chain of {N} (3–4) large bright nodes at 9% across, evenly spaced from 44% to 86% down,
linked by a glowing line; the field right of 18% across is calm and sparse from 37% to 92% down (step text).

**cta**: the whole network converges toward one bright core at 50% across, 62% down, behind a calm horizontal band
from 56% to 66% down (the keyword pill covers it); above 45% the field is dark and sparse (the sign-off).

## KEYING

None. S07 plates carry no magenta or cyan zones: every real asset (captures, logo tiles, cards) is placed by the kit
page, and the plate only has to keep the named rectangles calm and empty. If a deck ever needs a capture set into
the art itself (a screen inside the network), use S03's magenta screen sentence for that one zone and composite it
before the page renders; on the teal ground never key cyan (the glow would read as key).
