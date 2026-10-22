# S15 Landscape Specimen: prompt block

Reusable visual-system text for Codex plate prompts: one cinematic landscape per item, the item's name set giant
in the sky as a two-font specimen, one small subject on a low horizon, a two-column masthead and a BACK/NEXT nav.
A layout studied from a high-performing carousel; only its layout vocabulary carries over. Never copy any
reference deck's subjects, people, cover device, art, words, hook, CTA phrasing, item set or signature palette
(no turquoise seas, no violet dusks). **Hybrid**: Codex paints a text-free plate per slide; an HTML overlay
(`templates/06-landscape-specimen/overlay.html`) sets every word and all chrome.

**To Codex:** SYSTEM, one layout's **Plate (paste)** with its braces filled, and KEYING only when the plate
has a zone. Nothing else: Codex paints quoted words and font names.

**References:** none to start. The first plates run on the text prompt alone. Once you approve a plate, lock it
as the reference for its time of day (golden, day, dusk, night): a lock carries grain, lens and haze, not the
grade, and the nearest locked time of day is attached first. Never attach anyone else's slide. The cover goes
first.

## Production split

| Element | Made by |
|---|---|
| Fit to 4:5 | **Every** plate: `python -I shared/composite.py plates/slide-NN.png fitted/slide-NN.png` (centre crop + Lanczos to 1080x1350); keyed plates run `--zones-only` first, then add `--shot` / `--logo`. An unkeyed plate exiting 3 has stray magenta: edit job |
| Type colour, scrim | `node shared/sky-tone.mjs <deck>` → `runs/tone/slide-NN.json`, stamped onto each card's `<body>` as data attributes |
| Every word, all chrome | Overlay `cards/slide-NN.html`, a copy of `templates/06-landscape-specimen/overlay.html` with its slide-data JSON filled, on the fitted plate (`center / 1080px 1350px no-repeat`): `node shared/render-card.mjs cards/slide-NN.html final/slide-NN.png --w 1080 --h 1350 --scale 1`. Recipe: `templates/06-landscape-specimen/recipe.md` |
| Real UI | A capture card in the overlay, pre-cropped with `shared/shots.py` around its focus box. Cover monitor and in-scene variant: the magenta zone, via `composite.py --shot N=shots/x.png@x,y,w,h` |
| Real logos | Combo: icon PNGs (your logo folder, or simple-icons) in the overlay. Sign-board: a cyan slot via `composite.py --logo`, which erases into the sampled colour around it, so only on flat board |

Order per slide: plate → fit → card copy → tone pass → overlay render → copy to `exports/slide-NN-YYYY-MM-DD.png`
(date from the folder name), verified at 1080x1350.

## SYSTEM

Visual system: a cinematic landscape photograph, full bleed, 4:5 portrait. Natural grade, slightly
saturated, lifted blacks, fine 35mm film grain, soft haze toward the horizon. Calm and spacious: one
horizon, wide negative space, no crowds, no clutter.

Composition: everything above 44% of the height is open sky: a clean gradient, soft cloud banks or fine
stars. No sun disc, birds, kites, flares, poles, wires, tree tops or peaks reach into it. The horizon or
hill crest sits at 56-72% of the height. The layout's subjects stand on or just below it, whole and
uncropped, at the size and position the layout gives. The bottom 12% holds no small detail: even field,
grass, sand or dark meadow, or the plain lower part of a near subject. The left and right 10% hold only
continuous landscape. Keep the top and bottom 5% free of anything that matters.

Colour: orange #D9551F appears only on the touch the layout names, on a subject, never in sky or
ground. Every other colour is the landscape's own for the layout's time of day. Day: #8FB6D9 at the
horizon to #3F78B8 at the top. Deep afternoon: #1F5FA8. Golden hour: cream-peach #F3E3C8 to grey-blue
#C9D6E2. Dusk: navy #1E2F52 over an amber horizon band #E9A15A. Night: navy #0F1B33 to #050A16. Grounds:
canola #E8D320, wheat #D8B45A, meadow #5E8F2E, dry sand #C9874A, night ground #0B0F14. No purple, violet,
lavender, pink or magenta anywhere: glows are amber, peach or grey-navy, flowers yellow, white or orange,
roofs and doors orange-red, never crimson. No cyan, turquoise, teal or aqua anywhere: water is slate or
deep navy #2E4A6B, skies mid-blue, never green-blue. The only exceptions are KEYING's flat zones, when
attached.

References: the attached images show only the photographic treatment: grain, lens softness, haze, open sky
over a low horizon. Do NOT copy their time of day, colours, terrain or subject, any person or figure, or
any text, numbers or chrome.

No famous people, actors, characters, costumes, props or recognizable film or TV stills. A person is
anonymous and seen from the side or back, unless the layout attaches photos of one specific person.

Hygiene: no text of any kind: no letters, numbers, signs, labels, logos, watermarks, captions, UI or
handles. Screens, boards and signs are blank or are KEYING's flat zones. No border, frame, vignette or
split-screen. Never render these instructions or section names as text.

## COVER

**Plate (paste).** The golden-hour version of the system, horizon at 64-70% over a wheat field, dry
meadow or low grassy hill. The focal subject is near and large: a plain wooden desk seen from a low angle
close to the camera, one monitor on it facing the camera square-on. Desk and monitor span 55-80% of the
frame width and fill most of the lower half; the monitor's top edge sits at 44-48% of the height and its
screen is at least 45% of the frame width. A plain orange folding chair stands beside the desk,
clear of the screen: the orange touch. The screen is the magenta zone, 16:10 (see KEYING). {Pairing deck:
one long desk with two monitors side by side, both square to the camera, each screen its own magenta zone
at least 30% of the frame width, with desk between them.} {You, opt-in, from your own attached photos: on
the orange chair, turned three-quarters toward the screen, back and shoulder to us, head no higher than
the monitor's top, never overlapping the screen.}

**Overlay (kit).** The cover set, centred in 12-43%. Kicker: the count and audience ("7 claude code").
Hero: the list's noun, the biggest thing on the slide. Outcome line, mandatory, 8 words at most ("that do
the boring work"): one line up to 30 characters, else two lines with the hero capped at 200 px. The
count is a plain numeral in the kicker: no tile, boxed letters, superscript or corner number, and no
unproven superlative ("best"). The masthead's month is spine C's cover stamp; nav 01 is current.

## INTERIOR

**Item** (spine C's `item`, one per list item).

**Plate (paste).** The {day | deep afternoon | dusk} version of the system, over {terrain}. One lone
subject: {subject description}, 8-22% of the frame width, on the horizon in the centre third or on a
third line, its top no higher than 54% of the height, carrying the one orange touch the
description names.

**Overlay (kit).** The stack in 12-52%: kicker (the job, "for memory"), giant line (the name, exact),
caption (what it does and what it replaces), use line ("→ " + one concrete use), proof line (verified on
posting day, "★ 18.4k stars · free · MIT").

**Stake** (optional slide 2, spine C's `why`). Plate (paste): the {time of day} version of the system,
one road or track running straight to a horizon at 60-68%, no subject or one under 6% of the frame width
carrying the orange touch. Overlay: a verified number or two-word stake as a P3 giant line ("3 HOURS"),
the kicker for context, a caption sentence; no use or proof line.

**Proof** (an item whose real UI or README must show).

**Plate (paste).** The {day | deep afternoon | dusk} version of the system, over {terrain}. One lone
subject: {subject description}, at most 12% of the frame width, on the horizon in the left or right
third, carrying the one orange touch. The middle of the horizon is empty, even ground. {In-scene
variant: in the middle stands a blank easel, a monitor on a camp table or a sign-board, square to the
camera; its face is the magenta zone, at least 45% of the frame width, top at 46% of the height or lower
(see KEYING).}

**Overlay (kit).** The full stack in 11-44%, giant line and caption one line each (giant 160 px at most).
One capture card on the horizon, top no higher than 46%, bottom no lower than 88%; none in the in-scene
variant.

**Combo** (slide n-1, or every slide of a pairings deck).

**Plate (paste).** The {time of day} version of the system, over {terrain}. Two lone subjects on one
horizon, each 8-18% of the frame width, side by side with a gap of at least 20% of the width, not facing
each other: two cabins, two tents, or two walkers heading the same way, seen from the side or back. One
carries the orange touch; the other's matching touch is cream or white.

**Overlay (kit).** Kicker: tool A in the quiet face. Giant line: tool B. One-line caption "A + B: what the
pair does", the "+" in the caption's colour, flanked by the two real app icons. Use line: what you'd do
with the pair.

**CTA** (last slide).

**Plate (paste).** The night version of the system: fine stars, and a horizon at 62-70% with grey-navy
mist along it, never violet. One canvas tent with an orange fly glows warm amber (#F2A23A)
from inside, seen three-quarters on from a low angle, 18-28% of the frame width, in the left or right
third. {Alternative: a small observatory dome with an orange-lit slit, same size and place.}

**Overlay (kit).** In the tone pass's colour (white on night). Kicker "comment" in P1's face. Giant
line: the comment keyword, exact, P3 caps up to 6 characters, else P2 caps. Caption names the
deliverable ("for all 7, with install commands"). Nav: the last number is current.

**Deck rules (Claude; never paste).**
- Arc: cover golden hour; items through day into deep afternoon and dusk; CTA night.
- Terrain, never twice in a row: canola, wheat, grassy hill, dune, salt flat, alpine meadow, coastal bluff
  over slate water, straight country road.
- Subject: the item's metaphor, pasted as the description only (never the job word or name), never the
  same kind (two buildings, two figures) on adjacent slides. Memory: a small cabin, orange door, windows
  lit only at dusk or night. Browser automation: a small boxy orange rover on a dirt track. Speed: a
  cyclist in an orange jacket on a straight road. Security: a gate with an orange bar in a long dry-stone
  wall. Research: a walker with an orange lantern on a dune. Deploys: one orange shipping container alone
  in a field. Testing: an orange windsock on a short pole. Else: one low object or small figure at ground
  level with one orange touch.
- Mascot: off by default. If you have your own (a transparent PNG you made, never a licensed character), an
  overlay sprite (slide-data `sprite`, never painted) on the ground line replaces the cover chair or the CTA
  tent, in a pose that comments on the slide.

## KEYING (only when the plate has a zone)

The face of {the monitor | the easel | the sign-board} is ONE solid flat magenta #FF00FF rectangle of
aspect {W:H}, square to the camera: pure uniform magenta edge to edge, no gradient, texture, glow,
reflection, text or UI, no perspective tilt. It sits in its own thin dark bezel or plain wooden frame and
is at least {min}% of the frame width. Grass, people, the chair and props stand clear of it with a
visible gap.
A logo slot goes only on a flat cream sign-board face, never on sky or ground: ONE solid flat cyan
#00FFFF rounded square about {size} wide, no text, outline or shadow, with clear board around it.
These are the only magenta and cyan on the slide; the SYSTEM colour bans hold everywhere else.

## OVERLAY KIT (never paste; built as `templates/06-landscape-specimen/overlay.html`)

**Every slide.** Inside 104 px side margins and 3-98% of the height; no shadows on type; nothing under
46 px (caption), 30 px (use, proof) or 24 px (masthead, nav). Masthead, baseline at 6%: "{{BRAND}}" left
(Inter Black 26 px caps, +0.04em); the deck label (3 words at most) · month ("OCT 2026") right (JetBrains
Mono Medium 24 px caps); never three tracked columns. Nav: a 2 px rule at 93%, x 104-976,
open chevrons at both ends; at 95.8%, "BACK" and "NEXT" (Inter Medium 24 px caps) with 01…TT evenly
between (JetBrains Mono 26 px; TT is the real total). The current number is ink bold in an orange
pill (4.8:1; orange type alone is under 2:1 on day skies). Cover: rule and labels at 70% only if still
4.5:1. Last slide: NEXT at 40%.

**Tone pass** (`shared/sky-tone.mjs`, Node + `sharp`, outside the browser, before rendering). Regions across x 104-976:
masthead (3-9%), the stack box, nav (91-98%). Ink #0E0E0E or white, whichever has the higher WCAG
contrast against the p10 / p90 luminance (crossover L ≈ 0.19). Targets: 4.5:1 for caption, use, proof,
masthead and nav, each in its own band; 3:1 for kicker and giant line. Short of that, the first scrim
step that passes, 20%, 35%, 50%: multiply-darken behind white, screen-lighten behind ink; radial on the
stack box with an 80 px feather, a band fading over 60 px on the strips. Still short: edit job for a
calmer sky. Output `runs/tone/slide-NN.json` → `<body data-mast data-stack data-nav data-scrim data-scrim-mast data-scrim-nav [data-nav-dim]>` (data-scrim is the stack's; exit 4 = still short at 50%).

**Stack**, centred in the layout's box. Kicker: quiet face, 64-96 px, 1-4 words; in P1 it overlaps the
giant line's cap height by about 10%, in P2/P3 it sits 12-24 px above. Giant: loud face, line-height
0.86, fitted by `window.cardReady` to 872 px; cap 260 px (160 px on two lines or a proof slide), floor
140 px. Caption: Inter SemiBold 46 px, -0.03em, line-height 1.12, 20-28 px below; 2 lines / about 68
characters. Use: JetBrains Mono Medium 32 px, 16-20 px below; 8 words / 40 characters. Proof: JetBrains
Mono Medium 30 px, 8 px below; 6 tokens, star as inline SVG. Giant, caption, use and proof are `data-fit`;
before failing, the giant drops to its floor, the kicker to 64 px, then the long-name rule applies. An
overflowing caption or use line is a storyboard rewrite.

**Pairings** (longest name at the 140 px floor):
- P1: Playfair Display Italic 400 over Inter Black, -0.05em, the name's own case. 10 characters.
- P2: Instrument Serif 400 over Archivo wdth 62, wght 900, italic. 12 characters.
- P3: Inter Medium over Archivo wdth 125, wght 900. 6 characters, or two short words on two lines.
- Cover set: Inter Black lowercase kicker, 64-80 px; Playfair Display Black Italic lowercase hero, 240 px
  at most, a 14 px bloom of its own colour at 35%; Inter Bold 56 px outcome line.
- P2/P3 use caps only for a capitalised-word name (Playwright); own casing (claude-mem, n8n, shadcn/ui,
  GitHub) keeps `text-transform: none`. Adjacent slides never share a pairing unless the length rule
  leaves one. Past 12 characters, break at a hyphen, slash or space, each line within its pairing's limit
  at 160 px; else the giant line is the README's own short name (never invented) and the exact name goes
  in the caption.

**Capture card:** key text at least 30 px rendered; 62-70% of the width, 10 px cream #F5EBE0 border,
18 px radius, shadow `0 24px 48px rgba(0,0,0,.35)`, centred on the horizon. **Combo icons:** 72 px,
16 px radius, either side of the caption.
