# S11 Sketchnote Diagram Explainer: prompt block

Reusable visual-system text for Codex image prompts. A common sketchnote-explainer look. Its
exemplars are this repo's worked example (cover and slide 4). **Image-native**: Codex paints every
slide, and real captures and exact-text cards are composited in. Paste the SYSTEM block into every
slide prompt, plus KEYING when a slide carries a real capture, and write each slide's composition top
to bottom (`carousels/2026-10-14-claude-video-free/prompts/` shows the shape). Attach
`engine/styles/exemplars/S11-cover.png` and `engine/styles/exemplars/S11-interior.png` as style
references until a locked cover exists. After that, attach the locked cover first.

## SYSTEM

Visual system: a hand-made "sketchnote" explainer page. Warm off-white cream paper ground (#FBF7EE)
with a very faint paper grain, no grid. Headline in a heavy, tightly spaced black grotesk sans
(like Inter Black or Neue Haas Grotesk Display Black), sentence case. Its second line, or one key
phrase, is in Claude orange (#D9551F). Body text in a clean regular grotesk, near-black (#1B1B1B).
Margin notes are in a small, neat handwritten marker script in dark grey, each with a short
scribbled underline. Diagrams use rounded pastel boxes with thin dark ink outlines (pastel green
#DDEEDB, pastel blue #DCE8F7, pastel pink #F8E1E4, pastel lavender #E9E3F5), connected by thin
hand-drawn ink arrows with slightly wobbly lines. The single most important line on a slide sits
in a soft yellow highlighter pill (#FBE38E). Small square tag box top-left holding the slide
counter, with a short uppercase spaced-out eyebrow label beside it. Thin rule near the bottom with
the footer "{{BRAND}}" centred under it. Generous whitespace; flat, crisp, print-like; no gradients, no
3D, no photo textures, no shadows except a very faint one under cards.

Framing: every element sits inside a uniform empty margin of at least 8% of the width on the left
and right and 9% of the height at top and bottom. If content does not fit, make it smaller.
Readable at phone-feed size: body text no smaller than about 1/45 of the slide height; the footer
as large as the body text.

References: Image 1 and Image 2 show the layout vocabulary only: tag box + eyebrow, the heavy
two-tone headline, pastel diagram boxes, wobbly arrows, handwritten margin notes and the yellow
highlighter pill. Do NOT copy their words, their video frame, their diagram or their icons. No
cartoon characters or mascots unless the prompt names one and attaches its sprite (your own mascot,
if you have one); never a licensed character.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. No
extra captions, labels, lorem ipsum, watermarks, handles or logos. Never render these
instructions or section names as text.

## KEYING (when a real capture goes on the slide)

The screen area of {the frame} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}: pure
uniform magenta edge to edge, perfectly flat and frontal, no gradient, no texture, no glow, no
text, no UI inside it, no tilt, square corners inside a thin ink outline. Every other element
stands clear of it with a visible gap. No purple, violet, pink or magenta anywhere else on the
slide (the pastel pink boxes must read as soft pink, not magenta).
