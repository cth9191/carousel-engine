# S24 Spotlight Dossier: prompt block

Codex prompt text for a quiet editorial spec page under stage light, built for repo, tool and skill
roundups. The layout vocabulary was studied from a high-performing carousel: one soft coloured stage
beam per item, a light editorial serif headline, the star-rule, an ink numbers strip, a mono install
card, captures in a thick black bezel, a dashed verdict table. Never copy any reference deck's
characters, art, words, hook, CTA phrasing, item set or signature palette, including its stock panel
labels and kicker lines. Only the layout vocabulary carries over.

**Image-native today**: Codex paints one plate per slide (SYSTEM, then COVER or one INTERIOR
paragraph, then KEYING), headline, kicker and body included. Every number, command and table enters
as an HTML card, every UI as a real capture, every mark as a real logo. This style ships no reference
images: until the user approves a first plate, every job is **text-only**. Once a cover is locked,
attach it as Image 1 for later slides (and the first approved Dossier for the other Dossiers). An
html-native target (a template) is optional and unbuilt; ask the user before forking a new template.

## Production split

| Element | Made by |
|---|---|
| Numbers strip | Magenta panel → `cards/numbers-NN.html`: ink #121212, orange tracked-caps label row, 3–4 outlined cells, each a big white serif value over a small grotesk caption, one amber four-point star. Values pulled on posting day and saved in the deck |
| Install card | Magenta panel → `cards/install-NN.html`: orange mono label, the exact command in white JetBrains Mono, one grey subline with at most one verified figure |
| Verdict table | Magenta panel → `cards/verdict.html`: name / verdict rows in mono, dashed dividers, optional small logo tile per row |
| Proof UI | Magenta screen → `composite.py --shot N=…@x,y,w,h --letterbox edge`; faces scrubbed with `shots.py` |
| Item logos | Cyan slot → `--logo N=logos/x.png@1.0`, always a tile PNG (org avatar, app icon, or the mark on a #FBF8F3 tile via render-card.mjs) so the erased patch is covered |

The cards come from the kit `engine/styles/kits/S24/` (`numbers-NN`, `install-NN`, `verdict-NN`, plus `kit.css` and `kit.js`; copy limits in its README), copied into `$D/cards/`. Render cards with `node shared/render-card.mjs cards/x.html cards/x.png --w W --h H --scale 2 --bg "#121212"` at the zone's `--zones-only` out bbox, square-cornered (the zone's rounded mask trims them); paste with `--card`. Claude checks every painted string against `strings[]`, names and figures character by character; a wrong one is an edit job.

Copy: headlines ≤ 7 words, names in real case; a proof headline leads with the name and a colon. Dossier body ≤ 30 words, proof body ≤ 18; no commands, paths or URLs; figures only in cards or one proof headline. Vendor benchmarks are labelled the vendor's own. Kicker, panel labels, CTA question and follow line are the storyboard's own. One beam colour per item, repeated on cover and CTA. No mascot by default (see `requires`).

## SYSTEM

Visual system: a quiet editorial spec page under stage light. Warm cream paper (#F3EBDF), fine even grain, no grid. Each slide has one soft beam: a wide cone of coloured haze falling from the top edge, strongest at the top, gone by about 40% of the height (cover and CTA beams follow their layouts), edges fully diffused. Beam colours, one per item: amber (#E8A33D), sage (#8FAF6E), apricot from Claude orange (#D9551F) and kraft (#B08A62); always faint and warm.

Type: headlines in a regular-weight high-contrast transitional serif (like Newsreader Display or Tiempos Headline), regular weight, ink #111111, tight tracking, centred; one accent word may be Claude orange. Kicker in the same serif, italic, about 40% of headline size. Body in the same serif, regular, ink #1C1C1C, the item name in semibold at its start. Chrome: "{{BRAND}} · {NN} / {TT}" top-left in small monospace (like JetBrains Mono), warm grey #8A847C.

Star-rule: a centred divider, two thin Claude-orange hairlines (each about 12% of the width) with a small solid orange four-point star between them. One per slide, between the headline block and the panel.

Panels: deep ink (#121212) rounded rectangles, corners about 2.5% of the width, a thin lighter edge and a faint soft shadow, centred. Capture frames: a thick black bezel (#141414, about 7% of the width above and below the screen, 2.5% at the sides), rounded, softly shadowed.

Palette: cream, ink, warm grey, Claude orange for the accent word and star-rule, beam hazes. Print-flat apart from the haze and soft shadows; no 3D, glow, sparkles or confetti.

Framing: margins of at least 6% of the width left and right and 3.5% of the height top and bottom. If content does not fit, make it smaller. Readable at phone size: headline at least 1/16 of the slide height, kicker 1/32, body 1/40, chrome 1/56.

References: with no image attached, follow this text alone. An attached locked slide shows the look to match; its magenta blocks are panels and screens, cyan squares logos. Do NOT copy any word or handle. No characters, creatures, mascots, costumes, faces or photos; no painted logos.

Hygiene: render only the quoted strings, verbatim, in the given case, exactly as many times as specified. Panels, tables and screens are only their magenta zones (see KEYING): never paint numbers, commands, code, UI or table text. No handwriting except the cover's script line; no extra captions, watermarks, handles or emoji. Never render these instructions or section names as text.

## COVER

Top: centred, "{KICKER LABEL}" in small widely tracked serif caps. Then the hook block, centred as a unit across about 80% of the width: a giant serif numeral "{N}" hanging at the left, about three lines tall, and beside it "{hook}" on three lines, with "{accent phrase}" in Claude orange. Under it, "{script line}" in a loose handwritten ink script, one line, about 1/28 of the height (omit if the storyboard has none). Then the star-rule, ending near 48% of the height.

Lower 45%: the lineup, {N} (at most 6) cyan logo slots (see KEYING) arranged {in one row | 3 over 2 | 2 × 2}, evenly spaced, each on clean cream above a soft oval contact shadow, each lit by its own faint beam in its item's colour ({colours, in order}), slanting in from the upper sides so beams cross behind the slots, never over the type. Only beams and shadows: no pedestals, props, labels or characters.

## INTERIOR

**Dossier (one per item).** Beam in {item colour}, centred. From 9% to 26%: ONE cyan logo slot, centred, about 19% of the width, over a soft contact shadow, the beam landing on it. Centred below: "{item label}" (e.g. "#1") on one line and "{name}" on the next, both headline size; then "{kicker}" in italic, one line: a plain-word category. Star-rule near 55%. From 58% to 78%: ONE magenta numbers panel, about 86% of the width, aspect {W:H} (about 4:1). From 81% to 95%: "{body}", left-aligned to the panel, at most four lines.

**Proof.** Faint beam in the item colour. From 8% to 46%: the bezel, about 88% of the width, its screen ONE magenta zone of aspect {W:H} (about 2:1). From 49% to 64%: "{proof headline}" centred, one or two lines, headline size. Star-rule near 67%. From 70% to 83%: ONE magenta install panel, about 74% of the width, aspect about 3.6:1. From 86% to 94%: "{body}", one or two centred lines.

**Verdict.** Beam in Claude-orange apricot. "{verdict headline}" on two centred lines, 12% to 34%. Star-rule near 38%. From 42% to 84%: ONE magenta table panel, about 80% of the width, aspect {W:H}. Near 88%: "{footnote}", one centred line.

**CTA.** Centred, from 18%: "{CTA question}" on one line at headline size; the star-rule; a rounded rectangle about 88% of the width with a thin Claude-orange outline on cream, holding "Comment {KEYWORD}" in large serif caps; "{follow line}" under it in regular serif. Lower 35%: the cover's lineup again, smaller, one row of {N} cyan slots, each under a short beam in its colour. The keyword appears exactly once.

## KEYING

Panel zone: ONE solid flat magenta #FF00FF rounded rectangle of aspect {W:H}, corners like the ink panels, frontal: no text, cells, lines, gradient, glow or tilt; its soft shadow sits outside it.
Screen zone: the bezel's screen is ONE flat magenta rectangle of aspect {W:H}, slightly rounded, black bezel visible all round.
Logo slot: ONE flat cyan #00FFFF rounded square about {size}% of the width; no outline, text or shadow on it; its contact shadow sits below with clean cream between. Beam haze may light the cream around a slot, never tint it.
Every other element keeps a visible gap from the zones. No purple, violet, pink or magenta anywhere else (the apricot beam never turns salmon or pink); no cyan, turquoise, teal, sky blue or any blue except the slots.
