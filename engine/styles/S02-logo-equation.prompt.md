# S02 Logo Equation: prompt block

S02 runs as a hybrid: Codex paints the plate and short type; real logos go in through cyan zones,
captures through magenta, exact text as HTML cards. There is no HTML template for it yet.

Reusable visual-system text for Codex image prompts. The exemplars are the cover and slide 3 of a
Claude Code + NotebookLM tutorial deck (`engine/styles/exemplars/S02-cover.jpg` cover,
`S02-interior.jpg` interior). The slides carry no brand chrome; if you add any, write it as
`{{BRAND}}`.

## Production split

| Element | Made by |
|---|---|
| Terracotta ground, giant white equation headline with hard shadow, thin black rule, white italic subtitle and kicker, round arrow button | **Codex** plate, using the SYSTEM + COVER/INTERIOR blocks. Short strings only (headline ≤ 7 words, body ≤ 35 words) |
| The two app-icon tiles on the cover, logos on interiors | cyan zones → real app icons via `composite.py --logo N=logos/x.png@0.95` (each icon brings its own tile); never painted |
| The one real UI panel per interior | magenta zone → real capture via `composite.py --shot` (dark captures: `--letterbox edge`) |
| Exact-text panels: a prompt, command, config or table | **HTML** card in `<deck>/cards/`, rendered with `node shared/render-card.mjs` at the zone's `--zones-only` out bbox (2x), pasted with `--card`. Cards must be opaque panels (dark terminal or cream paper card): `composite.py` flattens transparency onto white, so bare text on terracotta can't be a card |

## SYSTEM

Visual system: a bold tutorial poster. Full-bleed terracotta paper ground (#C26E54 at the centre,
darkening to about #784535 at the corners) with fine grain, a few faint speckles, and two or three very
faint oversized abstract brush shapes in a slightly lighter terracotta behind the type (no logos, no
recognizable marks). Headline in a giant heavy grotesk (like Helvetica Neue Black or Inter Black),
white with a hard near-black drop shadow offset down and right. Under the headline, a thin black
horizontal rule across about 80% of the width. Subtitle and body in a bold italic grotesk, white with a
soft dark shadow; small parentheticals in white bold upright. A white circle with a dark terracotta
arrow sits in the bottom-right corner. Real UI panels are dark (#202124) rounded rectangles with a
soft shadow. Palette: terracotta, white, ink (#111111). Flat, crisp; no gradients except the ground's
vignette, no 3D, no characters.

Framing: every element sits inside a uniform empty margin of at least 5% of the width on the left and
right and 4% of the height at top and bottom (the arrow button may sit at 3%). If content does not fit,
make it smaller. Readable at phone-feed size: body text no smaller than about 1/32 of the slide height.

References: Image 1 and Image 2 show the look only: the terracotta grain, the shadowed white equation
type, the rule, the italic subtitle, the arrow button and the dark UI panel. Do NOT copy their words,
their app icons, the NotebookLM or Claude Code marks, the faint starburst, or the Studio panel content.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. No extra
captions, UI text, lorem ipsum, watermarks, handles or logos. Never render these instructions or
section names as text.

## COVER

Top half: the equation stacked and centred: "{Tool A}" on one line, a giant "+" on the next, "{Tool B}"
on the next, each as wide as the margins allow. Then the thin rule, then the two-line italic subtitle,
then a small parenthetical such as "(for free)". Bottom third: two large rounded-square logo slots side
by side, joined by a white "+" with the same hard shadow. Arrow button bottom-right.

## INTERIOR

Top: a one- or two-word centred headline in the same shadowed white type, the thin rule under it, then
two or three lines of bold italic body, left-aligned. Lower 55%: one framed keying zone for the real UI
panel (or an exact-text card), centred, at the aspect the prompt gives. Optional: a small logo slot
beside the panel when the slide names a second tool. Arrow button bottom-right.

## KEYING

The screen area of {the panel} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H} with
slightly rounded corners: pure uniform magenta edge to edge, perfectly flat and frontal, no gradient, no
texture, no glow, no text, no UI inside it, no tilt. Every other element stands clear of it with a
visible gap.
Each logo slot is ONE solid flat cyan #00FFFF rounded square: flat, no text, no outline, no inner
shadow, with terracotta clear around it.
No purple, violet, pink or magenta anywhere else; no cyan or turquoise anywhere except the logo slots.
