# S09 Charcoal Studio: prompt block

Reusable visual-system text for Codex image prompts. A calm dark design-studio look for tutorials and step-by-step
builds. **Image-native**: Codex paints the slide (chrome, eyebrow, serif headline with its yellow underline, sticky
note, browser and panel frames, one painted pixel-art prop), real captures go into magenta screens, exact text into
magenta panels as HTML cards, and logo tiles (plus your own mascot, if you have one) into cyan slots. Nothing with exact
text or a mark on it is ever painted.

Refs (attach in this order until a locked cover exists; after that the locked cover first, then the step ref):
`engine/styles/refs/s09-ref-cover.png` and `engine/styles/refs/s09-ref-step.png`, a cover and a step slide of an
earlier deck in this style with the screens and panels keyed magenta and the character and logo spots keyed cyan.
Their header, headline and sticky words belong to that deck: the prompt says never to copy them.

## Production split

| Element | Made by |
|---|---|
| Chrome, eyebrow, serif headline, accent underline, handwritten subline, sticky note, footer mantra, CTA words | Painted by Codex, verbatim from `strings[]`; Claude checks every letter |
| Browser / phone frames and panel outlines | Painted; their screens and faces are magenta zones |
| Captures (README, app, site, terminal run) | Magenta screen → `composite.py --shot N=…@x,y,w,h` (always a focus box), faces scrubbed with `shots.py` |
| Checklists, numbered lists, arrow tables | Outlined magenta panel → `cards/list-NN.html` |
| Roadmap strip, tells / truth columns | Outlined magenta panel → `cards/grid-NN.html` |
| The exact prompt or command | Magenta terminal → `cards/terminal-NN.html` (the card is the whole window) |
| Measured numbers | Outlined magenta panel → `cards/stats-NN.html` (verified figures only) |
| Yellow footer bar | Magenta bar → `cards/bar-NN.html` |
| Your own mascot (optional) | Cyan slot → `--logo C1=$D/assets/mascot.png@1.0,bottom`: a cut-out PNG with alpha, composited, never drawn, never a licensed character. With no mascot, the prompt asks for no character slot at all |
| Logo tiles (the subject's tool or app) | Cyan squares → `--logo` with a full tile PNG (a simple-icons mark rendered on a #1C1C1C tile with render-card), so the erased patch is covered |
| A prop (boxes, frames, a stopwatch, a clipboard) | Painted by Codex in flat 8-bit pixel art; it carries the slide's meaning (beside the mascot, when there is one) |

Cards come from `engine/styles/kits/S09/` (README there), copied into `$D/cards/`, rendered at each zone's
`--zones-only` out bbox ×2 and pasted with `--card`. Exit 2 from render-card means cut the copy.

Copy: headline ≤ 7 words, Title Case, one accent phrase (the end of the line); eyebrow ≤ 5 words in caps; sticky ≤ 12
words; handwritten cover subline ≤ 12 words; footer mantra ≤ 6 words, the same on every slide; header = subject in bold
caps + a grey "{from} → {to}" or topic phrase, ≤ 4 words in all. Never stack sticky + caption + panel card + bar on one
slide (spines.md): pick the panel card plus at most two of the others. If you use a mascot, it appears on the cover, at
most two interiors and the CTA avatar, each time beside a different painted prop that comments on that slide. Without
one, the props stand alone and the CTA avatar is a logo tile.

## Layouts by role

| Role (spine A / D) | `layout` | Zones |
|---|---|---|
| cover | `cover` | M1 browser screen; C1 mascot (optional), then 1–2 logo tiles above the title bar |
| what | `roadmap` | M1 screen; M2 grid (roadmap strip, one row per column); sticky |
| why | `tells` | M1 screen; M2 grid (2–3 columns: the tells / the truth / what you get) |
| model / parts | `parts` | M1 screen or diagram card; M2 list (`num`) |
| how / step | `step` | M1 screen; C1 mascot (optional) + painted prop; M2 list; M3 bar; sticky |
| peak | `prompt` | M1 terminal card; M2 list (`num`, the prompt's anatomy); sticky |
| use / day | `measured` | M1 screen or phone; M2 list (`arrow`); M3 stats; M4 bar |
| start | `stack` | M1 screen; M2 list (`check`, "You need exactly this:"); M3 bar |
| cta | `cta` | C1 avatar (your mascot or a logo tile); painted profile card, keyword block and lines |

## SYSTEM

Visual system: a calm dark design studio page. Ground: flat matte charcoal (#141414) with a very fine, even paper grain,
the same tone edge to edge. Type: headlines in a high-contrast editorial serif (like Newsreader Display, Tiempos
Headline or GT Super), regular weight, warm off-white (#F2F0EA), Title Case, tight but natural tracking; the accent
phrase in acid yellow (#F5F400) with one loose hand-drawn yellow marker underline beneath it (two quick strokes, the
second shorter). Eyebrows in small monospace caps (like JetBrains Mono), acid yellow, widely tracked. Labels and the
header in a clean grotesk (like Inter): the subject in bold off-white caps, the rest in grey (#8E8A82) caps.
Handwriting (sticky notes, the cover subline, "swipe->") in a casual marker script, off-white on charcoal and black on
the sticky. Chrome on every slide: top-left a rounded pill outlined in acid yellow holding "{NN} / {TT}" in yellow;
top-centre the header; top-right "swipe->" in the script; bottom-centre the footer mantra in small grey monospace caps.

Objects: browser windows with a light grey (#D9D7D2) title bar, three small traffic-light dots and a pale URL pill,
square-cornered screen below, a soft dark drop shadow; panels drawn as a thin off-white (#F2F0EA, 2 px) rounded
outline; sticky notes are pale yellow (#F6EC8C) squares tilted 2–4 degrees with a strip of translucent grey tape on top;
props are flat 8-bit pixel art with hard square edges, warm and simple (kraft boxes, wooden frames, a brass stopwatch),
standing on the charcoal with a small soft contact shadow. A few tiny four-point acid-yellow sparkles may sit near the
cover headline, nowhere else.

Contrast: deep flat charcoal; no haze, no fog, no glow, no vignette, no lifted or milky blacks, no light leaks, no
gradients on the ground. Print-flat, crisp; soft shadows only under windows, panels, stickies and props.

Framing: every element sits inside a margin of at least 6% of the width left and right and 3% of the height top and
bottom. If content does not fit, make it smaller. Readable at phone size: headline at least 1/18 of the slide height,
body and captions at least 1/42, chrome at least 1/56.

References: the attached images show layout and finish only: the chrome row, the serif headline with its yellow
underline, the browser frame, the sticky, the outlined panel and the yellow bar. Magenta areas are screens and panels,
cyan areas are character and logo slots. Do NOT copy their words (the header, headline, sticky and bar text are
another deck's). Never draw a character, mascot, robot or creature, and never draw a logo.

Hygiene: render only the quoted strings, verbatim, in the given case, exactly as many times as specified. Panels,
screens, terminals and bars are only their magenta zones (see KEYING): never paint lists, tables, numbers, code, UI or
bar text. No extra captions, lorem ipsum, watermarks, handles or emoji. Never render these instructions or section
names as text.

## COVER

Chrome row at 4%–8% down. At 15%: "{EYEBROW}" in yellow mono caps, centred. From 18% to 34%: "{headline line 1}" on one
line and "{headline line 2}" on the next, centred, large serif, the accent phrase "{accent}" in acid yellow with the hand
underline; two or three tiny yellow sparkles at the headline's top-right and lower-left corners. At 35%–38%:
"{subline}" in the off-white marker script, one centred line. Hero from 52% to 89% down: a browser window from 15% to
85% across, its screen ONE magenta zone (see KEYING) of aspect {W:H}. Above the right half of the window, on the
charcoal, left to right: [with a mascot: ONE cyan character slot (aspect {mascot W:H}, e.g. 0.88:1, about 9% of the
slide width wide), then] {N} (1–2) cyan logo squares about 8% of the width, their bases level at 49.5% down, 2.5% of
the height ABOVE the title bar, with clear charcoal between them and the bar (they never touch the light bar: see
KEYING) and below the subline. Nothing else on the cover.

## INTERIOR

Every interior: the chrome row; "{STEP N OF M}" or the role's eyebrow in yellow mono caps centred at about 12%; the
headline from 14% to 23%, one centred line (two only if it must), accent phrase yellow and underlined; the footer mantra
at 96.5%. Then the role's composition:

**step** (how / step). Left: a browser window from 6% to 56% across and 26% to 58% down, its screen ONE magenta zone of
aspect {W:H}. Top-right: a sticky note from 62% to 93% across, 26% to 42% down, "{sticky}" in black marker script on 3–4
lines. Below it, its base at 59% down: with a mascot, ONE cyan character slot (aspect {mascot W:H}, about 17% of the
width wide) standing at 60%–78% across and beside it to the right, on the same ground line, {prop} in flat 8-bit pixel
art, about the slot's height; without one, {prop} alone, centred at 62%–92% across, about 16% of the height tall. From
63% to 86% down, 6% to 94% across: ONE outlined magenta panel (see KEYING). From 89% to 94.5%: ONE magenta bar zone, 6%
to 94% across. (Drop the bar when the slide has a caption line instead: a grey grotesk line under the window, at most 2
lines.)

**roadmap** (what). Window from 6% to 64% across, 26% to 62% down (magenta screen). Sticky from 69% to 94% across, 28% to
46% down. From 67% to 92% down: ONE outlined magenta panel, full width (the roadmap strip).

**tells** (why). Window from 6% to 94% across, 26% to 58% down (magenta screen). From 62% to 93% down: ONE outlined
magenta panel, full width (two or three columns go in later).

**parts** (model). Window or diagram panel from 6% to 94% across, 26% to 56% down (magenta). From 60% to 93% down: ONE
outlined magenta panel, full width (a numbered list). Optional sticky overlapping the window's top-right corner.

**prompt** (peak). From 26% to 64% down, 6% to 94% across: ONE magenta terminal zone (no frame of its own; the card is
the window). Sticky from 66% to 92% across, 66% to 80% down, tilted, over nothing. From 67% to 93% down, 6% to 62%
across: ONE outlined magenta panel (the prompt's anatomy). Optional, with a mascot only: a cyan character slot (aspect
{mascot W:H}, 14% wide) under the sticky, with {prop}.

**measured** (use / day). Window or phone frame from 6% to 54% across, 26% to 62% down (magenta screen). From 26% to
62% down, 60% to 94% across: ONE outlined magenta panel (stats). From 66% to 88% down: ONE outlined magenta panel, full
width (arrow rows). From 90% to 95%: ONE magenta bar zone.

**stack** (start). Window from 6% to 94% across, 25% to 52% down (magenta screen). From 55% to 86% down: ONE outlined
magenta panel, full width (the checklist). From 89% to 94.5%: ONE magenta bar zone.

**cta**. Chrome row. From 10% to 30% down, 12% to 88% across: a rounded profile card (thin off-white outline, charcoal
inside) holding at its left ONE cyan circle about 11% of the width (the avatar: your mascot or a logo tile goes in
later), "{{BRAND}}" in bold grotesk, "{bio line}" in grey, and two pill buttons, "Follow" in acid yellow with black text
and "Message" in grey. From 40%: "Comment" in the large serif, centred; under it a rounded acid-yellow block about 70%
of the width holding "{KEYWORD}" in heavy black grotesk caps; then "{deliverable}" on two centred off-white grotesk
lines; then a bookmark mark and "Save for later" in bold grotesk. At 95%: "Follow · {{BRAND}}" in small grey grotesk.
The keyword appears exactly once.

## KEYING

Screen zone: the window's screen is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}, edge to edge under the
title bar, square inner corners, perfectly flat and frontal: no gradient, texture, glow, text or UI in it, no tilt.
Panel zone: a thin off-white rounded outline, and inside it ONE solid flat magenta fill reaching the outline all round,
corners following it; nothing drawn inside.
Bar and terminal zones: ONE solid flat magenta rounded rectangle, no outline, nothing inside.
Character slot (only when the deck has a mascot): ONE solid flat cyan #00FFFF rounded rectangle of aspect {mascot W:H}
(width to height), upright, no outline, no face, no text, with a small soft dark contact shadow under it on the
charcoal, and the prop beside it never touches it.
Every cyan slot sits on plain charcoal with at least 2% of the slide height of charcoal between it and any light surface
(title bar, sticky, panel outline): the compositor erases a slot into the colours around it, so a slot touching the light
title bar leaves a pale patch around whatever is pasted there.
Logo slot: ONE solid flat cyan square with slightly rounded corners, no outline, no text, no shadow on it.
Every other element keeps a visible gap from every zone. No purple, violet, pink or magenta anywhere else; no cyan,
turquoise, teal or sky blue anywhere except the slots; no blue at all (any mascot or logo colour is pasted later).
