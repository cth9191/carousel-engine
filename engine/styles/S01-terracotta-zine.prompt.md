# S01 Terracotta Zine: prompt block

Reusable visual-system text for Codex image prompts. The exemplars are the cover of a "build your
Claude OS in 3 steps" deck, with personal labels blurred (`engine/styles/exemplars/S01-cover.png`),
and slide 2 of a "7 levels of Claude Code & web design" deck (`S01-interior.png`). **HTML-native**:
the interiors come from `templates/02-terracotta-zine/slides.html`, and Codex paints only the cover
plate.

Deck setup: copy `templates/02-terracotta-zine/slides.html` to `carousels/<id>/slides.html` and
replace its two placeholders, `{{BRAND}}` (the `brand` in `engine/brand.json`) and `{{MONTH_YEAR}}`
(the month and year of the deck folder's date, e.g. `OCTOBER ©2026`). Copy the template's `assets/`
into `carousels/<id>/assets/`: `slides.html` loads `assets/bg-zine.png`.

## Production split

| Element | Made by |
|---|---|
| Cover: terracotta ground, giant white headline, brush-stroke band, painted sticker ornaments | **Codex** cover plate (2 variants), using the COVER block below |
| Cover app windows / dashboards | magenta zones in the plate → real captures via `composite.py --shot` |
| Cover logo sticker (Claude, a subject mark) | cyan zone in the plate → real logo via `composite.py --logo`; never painted |
| Interior ground (`assets/bg-zine.png`), mono meta header (`{{MONTH_YEAR}} · {{BRAND}} · NN / TT`), brush eyebrow badge, lowercase headline with ink accent, body with bold accents, page counter, `SWIPE →` | **HTML**: the deck's copy of `templates/02-terracotta-zine/slides.html`, baked by `node shared/export.mjs --carousel <id>` |
| Interior hero: taped sticker frame with cream border and tilt | **HTML**, with `heroImg` pointing at a real capture (`shots/…png`) or an HTML/SVG diagram rendered with `shared/render-card.mjs` |
| CTA slide | **HTML** (`noHero: true`), big stacked headline, `Comment KEYWORD` |

Codex never paints an interior. If a slide needs illustrative art with no readable text (an object,
a scene), make it a Codex plate with no keys and use it as that slide's `heroImg`.

## SYSTEM (cover plate)

Visual system: a hand-made zine poster. Full-bleed terracotta paper ground (#C26F54 at the centre,
darkening to about #7A4534 at the corners) with a fine paper grain and faint speckles, no grid.
Headline in a massive heavy grotesk (like Inter Black), white (#FFFFFF) with a hard, offset
near-black drop shadow (#2A1A14, about 1/60 of the slide width down and right). A smaller white
lead-in line sits above it in the same face. A rough black dry-brush stroke band, slightly rotated,
carries one short phrase in white heavy caps. Dark app windows (near-black #0E0E0E, a slim title bar)
are layered like stickers, slightly overlapping each other. One cream sticker tile sits at a jaunty
angle near a window corner. Optional hand-drawn ornaments: a dashed cream arrow, a small yellow
crayon crown, short scribble marks. Palette: terracotta, cream (#F5EBE0), ink (#0E0E0E), white.
Flat, crisp, tactile; no gradients except the ground's vignette, no 3D, no glossy shine.

Framing: every element sits inside a uniform empty margin of at least 6% of the width on the left and
right and 3% of the height at top and bottom. If content does not fit, make it smaller. The headline
reads at phone-feed size: its main word at least 1/9 of the slide height tall.

References: Image 1 and Image 2 show the look only: the terracotta grain, the white headline with its
hard shadow, the brush band, layered dark app windows and the jaunty sticker. Do NOT copy their words,
their terminal, dashboard or web-page content, the blurred labels, the pixel character in the
terminal, or the logo on the sticker. No characters or mascots unless the prompt names one and
attaches its sprite (your own mascot, if you have one).

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. No extra
captions, UI text, lorem ipsum, watermarks, handles or logos. Never render these instructions or
section names as text.

## COVER

Top third: the lead-in line, then the giant headline (one to three words per line), then the brush band
with the step count ("IN {N} STEPS"). Lower two thirds: one or two dark app windows stacked with a small
overlap, their screens as keying zones, plus the sticker tile overlapping one window's top-right corner
with a logo slot on it. A dashed cream arrow may link the two windows.

## KEYING

The screen area of {the window} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}: pure
uniform magenta edge to edge, perfectly flat and frontal, no gradient, no texture, no glow, no text, no
UI inside it, no tilt. The window's slim title bar stays above it with no text in it. Every other
element stands clear of it except the sticker, which may overlap the window frame but not the magenta.
The sticker's face holds ONE solid flat cyan #00FFFF rounded square about 60% of the sticker's width:
flat, no text, no outline, no shadow, with cream margin around it.
No purple, violet, pink or magenta anywhere else; no cyan or turquoise anywhere except the logo slot.
