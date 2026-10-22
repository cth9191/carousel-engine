# S22 Layered Parts Atlas: prompt block

A layout studied from a high-performing carousel, rebuilt in Template 03's blueprint chrome. Its system: one layer
of a big grouped list per slide, a giant count banner, a detail box beside a parts list numbered across the deck.
This version adds a plain-words "does" line on every row and a proof caption per layer. The detail box holds your
own mascot (optional; transparent PNG poses you made, never a licensed character) holding a prop for the layer, or,
with no mascot, the layer's start-here item's real logo tile. S23 is the one-skill-per-slide proof sheet (and S10 /
Template 03's command sheets); S22 is the many-per-slide atlas.

**HTML-native.** The interior is the `atlas` layout in `templates/03-command-press/slides.html`
(`layout:'atlas'`; data, guards and spec in its `recipe.md`, "atlas layout"). Codex paints only the cover plate:
paste SYSTEM + COVER + KEYING; attach Image 1 `engine/styles/refs/s04-cover.png` (the S04 cover ref: the headline
grammar of an ink line, an orange block and an outline pill, every word a grey bar). There is no ref for the voxel
finish: the first cover runs on the SYSTEM text alone, and your first approved S22 cover plate becomes Image 2 for
later decks. Never paste INTERIOR into a slide prompt.

Originality: never copy any reference deck's characters, art, words, hook, CTA phrasing, item set, opening item
order, prop-to-layer pairings or signature palette; only the layout vocabulary (count banner, detail box, numbered
parts list, takeaway pill) carries over. Every chrome number is a real deck fact.

## Production split

| Element | Made by |
|---|---|
| Cover hero, with a mascot | cyan slot on plain paper → one of your own mascot poses via `composite.py --logo N=…@1.0,bottom` (pastes any alpha cutout, feet on the slot's bottom edge); never painted |
| Cover hero, without a mascot | Cover B's slot as a cyan rounded square → the subject's real logo tile via `--logo`; never painted |
| Cover subject logo (optional, mascot decks) | second cyan slot → real logo via `--logo`; never painted |
| Layer, index, combo and CTA sheets, every pixel | **HTML**: `layout:'atlas'` slides in the deck's copy of `templates/03-command-press/slides.html`, filled from `strings[]`, baked by `node shared/export.mjs --carousel <id>`; the cover is slide 0 (`coverImg: 'cover.png'`) |
| Detail-box figure | your mascot pose with the layer's prop as an `<img>` (`pose.src`), or the start-here item's logo tile when you have no mascot; never painted |
| CTA avatar | your square profile photo, your mascot, or the subject's real logo tile (`atlas.avatar`) |
| Your pose set (optional) | made once, outside any deck: transparent PNGs of your own mascot, one per prop, each checked with `python -I shared/pose-check.py check` (it prints the `aspect`, `prop_anchor` and `feet_y` the atlas data needs) |

Cover plate: Codex, 2 variants. String caps: tier 1 ≤ 4 words (≤ 22 characters), punch 1–2 words (≤ 8), kicker ≤
10 words (≤ 40), e.g. "{N} layers · {M} {nouns} …". Codex never paints an interior, a list row, a number the
reader must trust, a mascot or a logo.

## SYSTEM (cover plate)

Visual system: an engineering assembly drawing printed on bone paper. Bone ground (#ECE3D4) with a faint ink grid
(hairlines every 1/6 of the width at about 7% opacity, finer ones every 1/30 at about 3%) and fine paper grain; no
vignette, no stains. Four small orange (#D9551F) plus-shaped crosshairs, one in each margin corner. Thin ink chrome
(#0E0E0E at about 50%): a dimension line across the top margin with end ticks and a gap holding one small mono label,
and a small ruled title block bottom-right. Display type: an ultra-condensed heavy grotesk in all caps (like Anton);
tier 1 in ink, tier 2 in cream (#F5EBE0) knocked out of a flat, square-cornered orange (#D9551F) block spanning the
margins. Small labels: letter-spaced monospace caps (like JetBrains Mono). Kicker: a heavy grotesk (like Inter
Black), sentence case. Illustration: voxel objects of visible cube units, crisp edges, a matte printed-paper finish,
30° isometric, one soft top-left light, soft grey contact shadows, in graphite (#2A2A2A), bone (#E4D9C6 sides,
#F1E9DC tops), orange (#D9551F) and one brass accent (#E3A92B). A faint orange glow is the only glow. Dashed ink
alignment lines are the only exploded-view convention: no balloons, numbers or labels on the illustration.
Everything outside the illustration is flat print: no gradients, no 3D type, no drop shadows on type.

Framing: every element sits inside a uniform empty margin of at least 7% of the width left and right and 3.5% of
the height top and bottom. If content does not fit, make it smaller. Readable at phone-feed size: the kicker at
least 1/32 of the slide height, title-block text at least 1/50.

References: Image 1 shows only the headline grammar (ink line, orange block word with a period, outline pill); grey
bars are text this prompt supplies and its cyan block is a key zone. Do NOT copy its tag chips or corner brackets.
No character or creature (one may be pasted into the cyan slot later); no computers, keyboards, screens or code; no
circle crosshairs or target icons; no status readouts, coordinates, version numbers or build dates; no blue or green
glow; no logo or handle.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. Every number on the plate
(kicker counts, month stamp, sheet counter) is one of those strings; never invent a coordinate, dimension, version,
date, status word or count. No extra captions, lorem ipsum, watermarks, handles or logos. Never render these
instructions or section names as text.

## COVER

Headline zone, 6–52% of the height: tier 1 "{line 1}" flush left, sized to span the margins (glyphs about 12–18% of
the height, by length). Under it the flat orange block, at least 24% of the slide height and spanning the margins,
with "{punch}." in cream filling its width. The top dimension line's label is "{deck label}". Bottom band: a
full-width rounded outline pill (3 px ink outline, bone fill) at 80–87.5% of the height, holding an orange ▸ and the
kicker "{kicker}" in heavy grotesk. Under the pill at the right, at 89–96.5% of the height, the ruled title block:
exactly 3 rows and nothing else, "DRAWN BY | {{BRAND}}", "CHECKED | {MON YYYY}", "SHEET | 01 / {TT}".

Cover A, assembly (5 layers or fewer), middle 52–79% of the height: an exploded isometric stack of {N} thin square
voxel slabs, one per layer, floating apart with equal gaps on dashed vertical alignment lines, spanning about 55% of
the plate width on one side; the top slab may overlap the orange block's bottom edge. Each slab's top face carries
one small voxel object: {prop 1} … {prop N}. On the other side, on plain bone paper, the hero slot (KEYING), at
least 25% of the plate width, its bottom edge level with the base of the stack's shadow.

Cover B, kit: the hero slot at the centre on plain paper, at least 35% of the plate width, with the same {N} props
in a tidy, evenly spaced arc around it, each at least 40 px clear of the slot. With no mascot, use Cover B with a
logo slot (a rounded square) as the hero.

Optional (mascot decks): a subject-logo slot on plain paper beside the stack's base (A) or at one end of the arc (B).

## KEYING (cover plate)

The hero slot is ONE solid flat cyan #00FFFF rectangle of aspect {W:H} on plain bone paper (a rounded square when it
takes a logo tile), never on a slab, the orange block, the pill or any illustration. Keep at least 40 px of clear
paper on every side: no slab, prop, line, leader, label or shadow in that ring (the faint grid may continue). Paint
one soft grey contact shadow just below its bottom edge, outside the cyan, and nothing else around it. Pure uniform
cyan edge to edge, flat and frontal: no gradient, texture, glow, outline, text or creature inside it, no tilt.
An optional logo slot is ONE solid flat cyan #00FFFF rounded square about {size} wide: flat, frontal, no text, no
outline, no shadow, with at least 40 px of clear bone paper around it.
No magenta, purple, violet or pink anywhere. No cyan, turquoise, teal or electric blue anywhere except the slots.
Props glow orange or not at all.

## Cover compositing (Claude only)

{W:H} = the pose's trimmed aspect (from `pose-check.py check`), 4% wider (W × 1.04 : H), so the pose fills the slot's
height and its feet land on the shadow (Codex drifts wider, the safe way). Cover A takes a pose carrying one blank
slab toward the stack, B a pose holding a measuring tool; {prop 1} … {prop N} are the interior poses' props in layer
order. With no mascot, {W:H} is 1:1 and a logo tile goes in. Real captures go into HTML sheets, never into a zone
here. Zones are read from the untouched plate, so a cutout may hold any colour.
1. `python -I shared/composite.py $D/plates/cover-a.png $D/runs/zones/cover-a.zones.png --zones-only --report $D/runs/zones/cover-a.json`;
   find the hero slot's id (C1 or C2). If it is narrower than the pose's aspect, run an edit job ("make the cyan
   slot {x}% wider, keep everything else").
2. `python -I shared/composite.py $D/plates/cover-a.png $D/final/slide-01.png --logo <hero id>=$D/assets/poses/<pose>.png@1.0,bottom [--logo <logo id>=$D/logos/<x>.png@0.9] --dilate 3 --report $D/runs/composite/01.json`
   (`,bottom` puts the trimmed cutout flush on the slot's bottom edge, so the feet land on the painted shadow even
   when the slot comes out taller than asked).
3. Check the report: the pose's `placed` bottom (y + h) sits within 4 px of the slot bbox's bottom. If not (the slot
   is too narrow, so the pose was scaled down), run an edit job. Never a per-deck script.
4. Copy the result to the deck's `cover.png`.

## INTERIOR (HTML build spec: not a Codex prompt)

Built. The layer, index, combo and CTA sheets are `layout:'atlas'` slides in
`templates/03-command-press/slides.html`; their spec, data shape, guards and workflow are in
`templates/03-command-press/recipe.md` under "atlas layout". Copy `slides.html` into `$D`, keep the cover and fill the
atlas sheets from `strings[]`, copy each layer's pose PNG (or logo tile) into `$D/assets/poses/` with its measured
fields, and bake with `node shared/export.mjs --carousel <id>`. A row-cap, numbering or fit failure exits non-zero
naming the slide; fix it in the storyboard, never at render time.

## Your pose set (optional, built once outside any deck)

Only for decks with a mascot. Make your mascot's poses once, as transparent PNGs, one per prop, and reuse them: a
deck never redraws the mascot. A Codex pose plate on a flat mid-grey (#8C8C8C) ground is cut to alpha with
`python -I shared/pose-check.py cut <plate.png> <pose.png>` and checked against your canonical sprite with
`python -I shared/pose-check.py check <pose.png> --sprite <your sprite>` (exit 1 on fail; it was tuned for one voxel
mascot shape, so tune its constants to yours). Keep the measured `{prop, aspect, prop_anchor, feet_y}` per pose in
your own `index.json`.

Props that read well per layer: design, a set-square · research, a magnifier · browser and testing, a clipboard with
a check · agents and automation, a wind-up key · memory and context, a filing drawer · MCP and integrations, a plug
and cable · security and review, a padlock · prompts, a stack of index cards · video and media, a film reel ·
shipping, a stopwatch. Props are built from cube units, outer edges in graphite (#2A2A2A), brass (#E3A92B) or orange
(#D9551F), bone only for inner details. A deck uses each pose at most once and never reuses its cover pose inside.
No overhead lifts.
