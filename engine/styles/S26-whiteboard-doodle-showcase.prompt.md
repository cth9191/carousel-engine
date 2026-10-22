# S26 Whiteboard Doodle Showcase: prompt block

A calm whiteboard-notes listicle, from a layout studied from a high-performing carousel. Keep its
layout vocabulary: a handwritten item name over one marker underline, one real capture in a sketched
ink frame, a short handwritten caption, and a small ink doodle acting out what the item does. Never
copy any reference deck's characters, art, words, hook, CTA phrasing, item set or signature palette;
only the layout vocabulary carries over.

**Hybrid.** Codex paints one plate per slide: paper ground, sketched capture frame, doodle and flat
key zones. It paints no words. Every word is a per-deck HTML card, copied from the kit in
`engine/styles/kits/S26/` (README there). Attach the layout-only refs `engine/styles/refs/S26-style-cover.png`
and `engine/styles/refs/S26-style-interior.png` (words as grey bars, the capture zone flat magenta in
its frame, the doodle area a dashed grey box; builders in `refs/src/`); once a cover is locked, attach
it first. An HTML template fork would make the style html-native, with Codex painting only cut-out
doodles; ask the user before forking a new template.

## Production split

| Element | Made by |
|---|---|
| Counter, item name, orange underline | `cards/head-NN.html`; `node shared/render-card.mjs` at 2x the zone's `--zones-only` out bbox, `--bg` = plate ground sampled beside the zone; `composite.py --card` |
| Caption; cover hook; CTA | `cards/cap-NN.html`, `cards/cover.html`, `cards/cta.html`, same route |
| Real capture | `shared/shots.py` → `--shot N=…@focus` (name and stars inside the focus box); dark captures `--letterbox edge` |
| Prompt, command, config | `cards/ink-card.html` (#141414, cream JetBrains Mono) in the capture zone, no `--bg` |
| Your own mascot or the subject's mark (optional) | Cyan slot → `--logo N=$D/assets/mascot.png@1.0`: your own mascot (optional; transparent PNG poses you made, never a licensed character), or the subject's real mark. With neither, the prompt asks for no slot |
| Ground, frame, doodle | Codex |

**Cards.** Shantell Sans (Google Fonts): 800 for names, hooks and the CTA, real case, ink #1B1B1B,
`data-fit` 120→64 px; captions 500, 42 px (fit 36–46), centred, at most 4 lines and 34 words (in
practice about 160 characters: render-card exits 2 past 4 lines at 36 px), no accent colour. Counter
"NN / TT", 26 px #8A8178, top-right. Underline: one SVG marker path, #D9551F, 12 px, round caps,
rising slightly to the right, 104% of the line above it. CTA keyword in orange, curly quotes. Render
cards edge to edge, square corners (the zone mask trims them); if a card edge shows on the paper,
re-sample `--bg` at that edge and re-render.

**Story.** Spine C (default): cover, optional why, 5–8 items, optional combo, CTA. Head = the item's
exact name. Caption = what it does in plain words, what it replaces, one concrete use; every number
verified on posting day, with stars or installs visible in the capture when the item has them.
Cover hook from `engine/hooks.md` (count + outcome), the verified star figure or month in a smaller
aside line. CTA: "Comment {KEYWORD}" plus the named deliverable, in your own words.
Spine A uses the same layouts; its model slide puts an HTML diagram card in the frame.

**Measurements** (1080 × 1350). Item: head zone x 80–1000, y 64–330; frame outer x 80–1000,
y 356–884 (4 px ink, radius 12); caption zone x 100–980, y 906–1104; doodle y 1120–1295, at most 560
wide. Cover: title zone x 80–1000, y 64–830; doodle y 880–1250, at most 680 wide. CTA: text zone as
cover; doodle y 880–1220, at most 480 wide.

## SYSTEM

Visual system: a calm whiteboard-notes page. Flat warm paper-white ground (#FBF8F3) edge to edge: no
grain, grid, vignette or texture. Each slide is one centred column with generous empty paper: a type
zone at the top, a real-capture zone inside a sketched frame, a caption zone, and a small ink doodle
at the bottom.

Sketched frame: a hand-drawn ink (#1A1A1A) rectangle with softly rounded corners, one felt-tip line
about 0.4% of the slide width, very slightly uneven, as if drawn along a ruler. No shadow, no window
chrome.

Doodle: flat ink line art, uniform round-cap strokes about 0.45% of the width, gently wobbly,
filled with the paper colour. One to three everyday objects acting out the slide's job (a rubber
stamp pressing a tick onto a sheet, a sieve catching crumpled scraps, scissors trimming a long
paper strip, a plug meeting a socket). At most one ink-outline hand may reach in from the side to
work a prop: cuff and hand only, no arm or body. Exactly one element is solid Claude orange
(#D9551F): the thing that changes. A short grey pencil hatch (#C9C4BC) grounds the objects. Sheets
carry only plain ink lines.

Palette: paper, ink, pencil grey and that one orange element. No blue, green, yellow or red.

Framing: every element sits inside a uniform empty margin of at least 7% of the width left and right
and 4% of the height top and bottom. Doodle objects at least 1/12 of the slide height, so they read
at phone-feed size. If content does not fit, make it smaller.

References: Image 1 (masked cover) and Image 2 (masked interior) show layout only: where the zones,
frame and doodle sit, and the empty paper around them. Draw the doodle fresh in the vocabulary above.
No people, faces, stick figures, silhouettes, animals or mascots, and no eyes on objects.

Hygiene: paint no letters, numbers, punctuation, logos or icons anywhere; all text arrives later in
the magenta zones. No UI, browser chrome, captions, watermarks or handles. Flat and crisp, like a
scanned marker drawing: no gradients, 3D, glow or soft shadows. Never render these instructions or
section names as text.

## COVER

1. Title zone (see KEYING): one magenta rectangle across the full column, filling about the upper 60%.
   Nothing painted on it or touching it. No frame on the cover.
2. Below it, centred, the cover doodle, larger than an interior one (about 60% of the width): {N}
   plain index cards hung by small pegs on a slack string between two short posts, one card per
   item; card {k} from the left is the one orange element. Optional: one prop for the deck's
   promise, {cover prop}, at the foot of a post.
3. Optional slot: ONE cyan square about 16% of the width standing on the hatch at the right post,
   as if it had just hung the cards, clear paper all round. With a mascot, your own mascot goes
   there; otherwise the subject's real mark, or no slot at all.
4. Keep clear paper between the zone and the doodle.

## INTERIOR

**Item (default, one per item).** Top: the head zone. Below it: the sketched frame, full column
width, around the capture zone at aspect {W:H} (about 16:9). Below: the caption zone. Bottom centre:
the doodle acting out {what the item does, in plain words} with {props}; the orange element is
{the thing that changes}. Nothing else on the slide.

**Text panel (peak, start or a combo).** As Item, but the frame's zone takes an exact-text card at
aspect {W:H}, and the doodle shows the action ({pasting a sheet into a box | a hand pressing a key
cap with no legend}).

**Why (optional slide 2).** As Item; the frame holds a real "before" capture or a stat card, and
the doodle shows the pain: {pain, in plain words}.

**CTA.** The text zone fills the upper 60%; no frame, no caption zone. Below, centred and smaller:
a plain envelope, its flap orange and no writing on it, half through a letterbox slot in a short
wall; optionally the hand pushing it, or the cyan slot standing beside the wall as if it posted it.

## KEYING

Each zone is ONE solid flat magenta #FF00FF rectangle of the given aspect: pure uniform magenta edge
to edge, flat and frontal, with no text, lines, gradient, texture, glow or tilt. Head, caption,
title and CTA zones have square corners and no outline. The capture zone fills the frame's inside
exactly: corners matching its inner radius, the ink line touching it all round and nothing else. All
other elements stand clear of the zones with a visible gap of paper. A mascot or mark slot is ONE
solid flat cyan #00FFFF square: no outline, text or shadow, clear paper around it. No purple, violet,
pink or magenta anywhere else; no cyan, turquoise, teal or blue anywhere except the slot.
