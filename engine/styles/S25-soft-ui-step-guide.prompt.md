# S25 Soft-UI Step Guide: prompt block

An airy product-page tutorial: one soft white UI module per slide under a caps kicker, a step pill
and a big sentence-case headline, dashed traces in the margins, chip-row footers, and a cover whose
centred headline stack sits over a hero ringed by floating UI cards. The layout vocabulary was
studied from a high-performing carousel; never copy any reference deck's characters, art, words,
hook, CTA phrasing, item set or signature palette, and never redraw a subject's wordmark (use the
real file). Only the layout vocabulary carries over. Accent: Claude orange #D9551F on tint
#FBE9E1.

**HTML-native, usable today on per-deck cards.** Playwright renders every word, card and trace; Codex
paints only the cover plate, a text-free hero device. The starter kit is `engine/styles/kits/S25/`:
`cards/s25.css`, `cards/s25.js` and one page per layout (cover, definition, step, rows, reasons, cta),
with rendered samples and a README; copy `cards/*` into `$D/cards/` and replace every string. No
template exists: ask the user before forking a new template (`templates/NN-soft-ui-guide`, the next
free number). SYSTEM, the COVER plate paragraph and KEYING are the Codex prompt; the tokens, the cover
overlay and INTERIOR are Claude's HTML spec and never go to Codex. The style ships no reference
images: the cover plate job is text-only until the user approves a cover, which then becomes Image 1.
Never attach a third-party slide to a Codex job.

## Production split

| Element | Made by |
|---|---|
| Every slide's ground, type, cards, chips, traces and terminals | **HTML**: `$D/cards/page-NN.html`, each linking the deck's `$D/cards/s25.css`, rendered with `node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22`. Headline and body carry `data-fit`, with an inline `window.cardReady` fit pass (floors: headline 96 px, body 30 px); an exit 2 (overflow or too small) means shorter copy |
| Cover hero | **Codex** plate (SYSTEM + COVER plate + KEYING; text-only prompt; 2 variants via `shared/codex-img.mjs`). `composite.py --zones-only` first (one magenta zone, fill ≥ 0.97, else an edit job, never a warp), then `--shot 1=$D/shots/<s>.png@x,y,w,h` to `$D/fitted/cover.png` at 1080x1350, the CSS background of page-01 |
| Real UI | `shared/shots.py` crop with a focus box, an `<img>` in a capture card |
| Logos | real files (your logo folder, or simple-icons SVG) as `<img>`; never drawn or imitated in CSS |
| Byline | your square profile photo (or your brand mark) as `$D/logos/avatar.png`, an `<img>` |
| Cover B (opt-in) | the user, cut out from 2–3 photos they supply, as an `<img>`; no plate |

**Tokens** (`s25.css`): ground #F6F5F3, a faint white glow top-left; cards #FFFFFF, 1 px #ECEAE6 border, radius 28, shadow `0 18px 48px rgba(14,14,14,.08), 0 2px 6px rgba(14,14,14,.04)`; ink #111214; body #5F646B; kicker #8C9097; Claude orange #D9551F, tint #FBE9E1; code chip #F2EFEB with #B8461A text; terminal #16181B, text #E8E6E3, `$` #F08A5D, success #3FB950, dots #FF5F57 #FEBC2E #28C840; traces 2 px dashed #D5D3CF (8/8) ending in 10 px orange dots; icons Lucide inline SVG, 2 px stroke. Fonts: Plus Jakarta Sans 500/800, Inter 400–700, JetBrains Mono 500. No blue, cyan, teal, purple or pink in chrome; logos keep their own colours inside white tiles. Every page: a 64 px avatar circle at (64, 52) + "{{BRAND}}" (Inter 600, 28 px); "NN / TT" (Inter 700, 28 px) right-aligned to x 1016. Margins 64 px; nothing below y 1290.

## SYSTEM

Visual system: a calm product-launch hero shot. Flat paper-white ground (#F6F5F3) with a very soft white glow toward the top left and the faintest paper grain; no grid, vignette or stains. One hero object as a clean 3D studio product render: matte warm-white and light warm-grey surfaces (#EDEBE7, #D9D6D1) with small graphite details (#2A2B2E), soft diffuse light from the top left, one soft grey contact shadow. Claude orange (#D9551F) appears only as one small detail on the object, such as a status light. Optional, behind everything: a very faint engraved line drawing of {topic object} with a fan of fine sunburst rays, ink at about 8% opacity, bleeding off the top-right edge and kept to the right third of the top half. Everything else is empty ground: the type and UI cards are added later, so leave that space clean.

Framing: the top 52% of the plate holds only ground and the optional engraving. The hero sits centred between 55% and 86% of the height, about 64% of the width at its widest, with at least 18% of the width of clean ground on each side. The bottom 10% is empty ground.

References: none on the first run. Once a cover is approved it is Image 1 for later cover plates: match its light, materials and ground, never its object.

Hygiene: no text, letters, numbers, logos, icons, UI, cards, buttons, people, characters, mascots, hands or statues anywhere, and no reflections of any. Never render these instructions or section names as text.

## COVER

**Plate (paste after SYSTEM):** the hero is {hero object, default: an open matte warm-white laptop seen straight on from slightly above}. Its screen is ONE flat magenta zone (see KEYING) about 50% of the slide width, top edge near 56% of the height. The base ends by 86%, with a soft contact shadow under it.

**Overlay (page-01.html, over the fitted plate):**
1. Optional, y 40–100: the subject's real wordmark or logo, ≤ 300 px wide.
2. Headline stack, centred, y 110–600: 3–5 lines alternating connectives (Plus Jakarta Sans 500, 50–60 px) and giants (800, 110–140 px, tracking -0.035em, fitted to ≤ 940 px). One connective is flanked by 1 px #CFCCC7 hairlines to the margins; the last line (800, about 80 px) carries the deck shape ("in 3 steps").
3. y 610–780: a 100 px white hub circle with the subject's logo and a dashed orange ring, centred; dashed traces join it to 2–4 logo chips (84 px tall, logo + name, tilted ±3°) in the side columns.
4. y 820–1190, side columns: 2–3 cards tilted −6° to +4°: a terminal (the deck's first real command, ≤ 2 mono lines at 22 px); a butter sticky (#FFF4D6, translucent tape) listing the N steps with orange check circles (N = step slides, G1); one small UI fragment using the tool's real option names.
5. y 1210–1290: an 880 px pill banner, the subject's logo in a thin ring plus one payoff line (Inter 500, 32 px) with one phrase in orange 700.

Chips and cards may overlap the device and up to 60 px of the screen's edge, never the capture's focus box. Cover B: the user's cutout, head and shoulders, y 600–1200, cards arranged the same way.

## INTERIOR

**Step** (how, step, start, why, model). At y 190 a caps kicker (Inter 600, 26 px, tracking .14em, #8C9097) and the step pill (white, 1 px #E6E4E0, 48 px tall, an orange dot in a tint ring, "Step 0N" in Inter 500 24 px); why and model pages drop the pill. Headline y 250–480: Plus Jakarta Sans 800, 104–120 px, line-height 1.02, tracking -0.03em, 1–2 lines, ≤ 7 words. Body: Inter 400, 32/43 px, ≤ 640 px wide, ≤ 4 lines (≤ 40 words). Then ONE module in a ~900 px white shell, ending by y 1120: a terminal (dots, copy glyph, mono 26–28 px, ≤ 7 lines copied from a real run, never an invented progress bar); a capture (14 px mat, key text ≥ 30 px); a logo grid (title row, 2×3 tiles of a 120 px logo circle + name); a hub (centre card with the subject's logo, name and two-line sub, ≤ 6 logo tiles on traces); or a command trio (icon tile, mono command 34 px, rule, 24 px grey line). Footer, y 1160–1270, at most one: a chip row (≤ 4 pills, icon circle + 28 px label), a callout pill or an orange-quote card.

**Definition** (what). Kicker, no pill. Headline: a plain question or claim about the whole thing, never a sub-component (G2). Body: the pain, then "X is a ___ that ___". Module, about 840 px wide from y 700 to 1110: a real capture, or an HTML mock tagged `evidence.kind: explain`, with ONE stat card overlapping its top-left corner by about 40 px (an orange glyph circle, a verified number in Plus Jakarta Sans 800 44 px orange, a 30 px label). Footer: a chip row of three plain words previewing the steps.

**Rows** (peak, use, day). Kicker and a two-line headline, no body. From y 520 to 1270 (1180 with a footer), 3–5 white row cards about 880 px wide, ≤ 150 px tall, 18 px apart: an 84 px tint circle holding an orange numeral (Plus Jakarta Sans 800, 44 px), then one or two lines of Inter 500 30 px; commands, prompts and flags sit inline as mono code chips (radius 8). Reasons variant: a filled orange numeral circle, a 72 px tint icon circle, a 700 title and a 26 px grey sub. ≤ 100 words, ≤ 22 per row; a chip-row footer only with ≤ 4 rows.

**CTA**. Kicker; headline "Comment “{KEYWORD}”" with the keyword in orange; "{deliverable line}" in Inter 32 px grey. Below, one white composer card about 860 × 260: a #E4E1DC avatar circle, a field showing "{KEYWORD}" in mono with an orange caret, a small orange send button. Then a chip row naming 2–3 things the deliverable holds. The keyword appears exactly twice.

## KEYING

The screen of {hero object} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H} (16:10 for the laptop): pure uniform magenta edge to edge, frontal and untilted, square corners inside a thin visible bezel, with no gradient, texture, glare, reflection, text or UI. Nothing overlaps it. There are no other key zones and no cyan anywhere. No purple, violet, pink or magenta outside the screen; no cyan, turquoise, teal or blue anywhere on the plate, and the warm-white materials never drift bluish. The orange stays a warm red-orange, never pink.
