# S17 Split-Band Before/After: prompt block

Reusable visual-system text for Codex image prompts. The layout was studied from a high-performing carousel; only its layout vocabulary carries over: two flat bands split at half height, a mono label over a big bold statement in each band, one text-selection highlight. Never copy any reference deck's characters, art, words, hook, CTA phrasing, tool row, marks, item set or signature palette. Palette rules for this style: the top band is warm cream #F5EBE0 and the selection is Claude orange on apricot #F8CFA8 with deep brown-black selected text #3A1808.

**Html-native.** `templates/07-split-band` renders every slide: bands, labels, statements (fit pass with the Copy limits below enforced), selection, tiles, byline, proof strip, command chip, counter and CTA. Copy its `slides.html` into the deck (`{{BRAND}}` filled in), fill `DECK` and `slides[]`, and bake with `node shared/export.mjs --carousel <id>` (exit 3 = a FIT/COPY failure: rewrite the copy); `templates/07-split-band/recipe.md` has the fields. Nothing is painted. The Codex route below is the fallback when a slide must be a plate: paste SYSTEM into every slide prompt, plus COVER or the one INTERIOR layout the slide uses, and attach `engine/styles/refs/s17-style-cover.png` and `s17-style-flip.png` (layout mocks in this style's own colours with off-topic placeholder copy, rendered from `engine/styles/refs/src/s17-ref-cover.html` and `s17-ref-flip.html`) until a locked cover exists, then the locked cover first. **Never attach another creator's slides**: they carry a real face, name, marks, tool row and copy.

## Production split (Codex fallback)

On a plate, Codex paints everything except:

| Element | Keyed in, never painted |
|---|---|
| Cover tiles (0–1 before, 1–5 after) | cyan slots → `--logo N=logos/<x>-tile.png@1.0` |
| Byline avatar (optional) | cyan circle → `--logo N=logos/avatar.png@1.0` (your square profile photo, circle-cropped with transparent corners) |
| Proof strip | magenta → `--shot N=shots/<x>.png@x,y,w,h` (focus box from `shared/shots.py`; dark terminals add `--letterbox edge`) |
| Command chip | magenta → `--card N=cards/cmd.png` |

Run `python -I shared/composite.py plates/slide-NN.png --zones-only` to learn the zones, then `python -I shared/composite.py plates/slide-NN.png final/slide-NN.png` with the flags above. Tiles carry their own ground and the avatar has transparent corners, so both paste at `@1.0`. Render a chip card with `node shared/render-card.mjs cards/cmd.html cards/cmd.png --w W --h H --bg "#FFFFFF"` at the zone's out bbox (2x is better): the rounded ink chip, an orange `$`, the exact command in cream mono. A longer command becomes a card at the strip's size.

On the template path every element is HTML (tiles, avatar and strip as `<img>`, the strip cropped to the same shots.py focus box), baked by `node shared/export.mjs --carousel <id>`.

## Template tokens (1080 × 1350)

- **Bands:** cream `#F5EBE0` y 0–668, seam `#EFE4D7` y 668–675, white y 675–1350. Side margins 86 px.
- **Label:** JetBrains Mono 400, 62 px, −0.01em, ink, cap tops y 136 / 778, ≤ 20 characters.
- **Statement:** Inter 650, opsz 32 (else Inter Tight), 126 px on a 115 px line, −0.035em, ink, cap tops y 233 / 875. ≤ 908 px wide, ≤ 3 lines, floor 96 px: ≈ 15 characters per line at 126 px, 19 at 96 px.
- **Selection:** `#F8CFA8` with `mix-blend-mode: multiply`, padding 6 × 28 px, text `#3A1808`, 3 px `#D9551F` full-height bars, 20 px `#D9551F` dots on top of the left bar and under the right.
- **Tiles:** 80 px, radius 18 px, gap 12 px, ground from the asset (white with `0 2px 10px rgba(14,14,14,.08)`, ink, or the brand's own tile); marks on white or ink at 70%.
- **Counter:** JetBrains Mono 400, 30 px, `#6B635B`, right edge x 994, baseline y 1300.
- **Proof strip:** 908 × 220, x 86–994, square corners, 2 px ink outline; after band y 1035–1255, before band (Twin proof) y 392–612. Its top sits ≥ 40 px below a one-line statement's descenders.
- **Command chip:** x 86–994, y 1149–1255, ink, radius 16 px, JetBrains Mono 40 px cream after an orange `$`, ≤ 34 characters.
- **Cover:** headlines Inter 650, 130 px, centred, each line with selection padding inside 908 px. Count line JetBrains Mono 400, 46 px, centred, baseline y 614. Avatar 48 px circle. "{{BRAND}}" Inter 650, 32 px.
- **CTA deliverable:** Inter 650, 74 px on an 84 px line, cap top y 1140, 1–2 lines of ≤ 24 characters.

## Copy (authoring notes for `storyboard.json`; never paste into a prompt)

- **One label pair per deck**, each ≤ 3 words plus the colon: "Old habit:" / "New habit:" or "Prompting:" / "Agents:".
- **Statements:** ≤ 7 words (G4), ≤ 3 lines of ≈ 15 characters (19 at the floor); over 908 px at the floor, rewrite.
- **The mirror is the hook:** the after statement keeps the before's syntax and changes as few words as possible (a role swap, a list that grows, a verified unit that shrinks): "You did the work by hand" → "AI does it, you check it". If the halves don't pair at a glance, rewrite.
- **Proof slides:** the after statement is one line of ≤ 15 characters naming the item ("You read a repo for a week" → "Claude reads it"); Twin proof holds both statements to that. A command that needs two lines takes the chip.
- **Cover:** "{subject}" ≤ 13 characters, verbatim in both bands; selection phrases a mirrored pair of ≤ 13 characters ("by hand" / "delegated"), never "before/after {tool}"; count line ≤ 30 characters plus the arrow, with the count and a month stamp or a verified star figure (G1). Tiles: the deck's tools in item order, none for a manual old way, no rival tool framed as the loser; name each tile's asset and ground in `storyboard.json`.
- **CTA:** a before statement of ≤ 6 words naming the old way, a keyword of ≤ 10 characters, a deliverable naming exactly what they get.
- **G3:** no unfamiliar term except the slide's one item, and none on the CTA.
- **Flips carry no accent phrase** (the mirror replaces it): log it in `storyboard.deviations[]`.

## SYSTEM

Visual system: a quiet typographic before-and-after page, split horizontally at exactly half its height into two full-bleed flat bands: warm cream (#F5EBE0) on top for the old way, pure white (#FFFFFF) below for the new way. Between them is a flat seam about 0.5% of the height tall in a barely darker cream (#EFE4D7): a soft step, not a ruled line.

Each band holds, in the same place, a label in a regular monospace (like JetBrains Mono), sentence case, ending in a colon, capitals about 3.4% of the slide height; under it, a statement in a big bold neo-grotesk (like Inter Display, semibold to bold, not black), sentence case, tightly tracked, line spacing about 0.9 of the size, capitals about 6.8% of the slide height, ragged right, broken by meaning into one to three lines. Both are ink (#0E0E0E). Exactly two weights on every slide: the bold grotesk and the regular mono.

The only accent is an editor-style text-selection box, used only where the prompt places it: a flat apricot fill hugging the selected phrase's line (#F8CFA8 on white, about #EEBF94 on cream), a thin Claude-orange (#D9551F) vertical bar down each edge, and a solid orange handle dot about 2% of the slide width across atop the left bar and another under the right bar. The selected text is deep brown-black (#3A1808). The small slide counter is a regular mono in warm grey (#6B635B) at the bottom-right margin.

Flat, crisp, screen-native: no texture, grain, grid, gradient, 3D or shadows.

Framing: an empty margin of 8% of the width left and right. The top band's label starts 10% of the height below the top edge, the bottom band's 7.6% below the seam; nothing sits within 3.5% of the bottom edge. Interiors align left to the margin; only the cover is centred. If content does not fit, make it smaller down to a floor (statement capitals about 5.2% of the height, label capitals 2.5%, counter type 1/45), then cut words. Everything must read at phone-feed size.

References: Image 1 and Image 2 are layout mocks in this system's own colours, showing the bands, seam, type positions, selection box, the cover's headlines, tile row and byline, and the counter. Do NOT copy their words, placeholder tiles or avatar.

No characters, mascots, photos, illustrations, stickers, tape or handwriting. No arrows unless the prompt quotes one.

Hygiene: render only the quoted strings, verbatim, with the given line breaks, exactly as many times as specified. At most one selection box per band. Never invent a label, caption, number, icon or logo. Every number is verified: reproduce it exactly, with its unit. No lorem ipsum, watermarks, handles or URLs. Never render these instructions or section names as text.

## COVER

Both bands are centred.

Before band, top to bottom:
1. {Only with a before tool:} one tile slot (see KEYING) about 7.4% of the slide width, centred between 12.5% and 18.5% of the height; otherwise empty.
2. A two-line headline between about 21% and 37% of the height: "{subject}" in plain ink, then "{before phrase}" inside the selection box.
3. One centred mono line, capitals about 2.5% of the height, baseline about 4% above the seam: "{count line} ↓".

After band, top to bottom:
1. A centred row of {N} equal tile slots, gaps about 1.1% of the width, between 56% and 62% of the height.
2. The same headline between about 65% and 82% of the height: "{subject}" repeated verbatim, then "{after phrase}" inside the selection box.
3. The byline, centred at about 92% of the height: one avatar slot about 4.5% of the slide width, then "{{BRAND}}" in the grotesk, capitals about 1.7% of the height.

Headline capitals are about 7% of the height; every line, selection box included, stays inside the side margins. Counter: "01 / {TT}". Nothing on the cover asks the viewer to comment.

## INTERIOR

Paste only the layout this slide uses (roles: see `formats.notes`).

**Flip.** Before band: the label "{before label}", then "{before statement}" in one to three lines. After band: the label "{after label}", then "{after statement}". Both statements share one type size. No selection box, tiles or proof; below the statements stays empty. Counter: "{NN} / {TT}".

**Flip + proof.** Before band: the label "{before label}", then "{before statement}" in one to three lines. After band, top to bottom: the label "{after label}"; "{after statement}" on one line; one capture strip (see KEYING) across the side margins from 76.7% to 93% of the height, aspect about 4.1:1, at least 3% of the height below the statement's descenders. For a command, the zone is instead a chip (see KEYING) from 85% to 93%, aspect about 8.6:1, and the after statement may take two lines. Counter: "{NN} / {TT}".

**Twin proof.** Each band, top to bottom: its label ("{before label}" / "{after label}"), its statement ("{before statement}" / "{after statement}") on one line, then one capture strip (see KEYING) across the side margins, aspect about 4.1:1, at least 3% of the height below the statement's descenders: 29% to 45.3% of the height in the before band, 76.7% to 93% in the after band. Counter: "{NN} / {TT}".

**CTA.** Before band: the label "{before label}", then "{cta before statement}". After band, top to bottom: the label "{after label}"; "Comment" in statement type; "{KEYWORD}" in statement type on its own line, inside the selection box; "{deliverable}" in the grotesk, capitals about 4% of the height, on one or two lines starting at about 84.5% of the height. Exactly one action. Counter: "{NN} / {TT}".

## KEYING

Each tile slot is ONE solid flat cyan #00FFFF rounded square (corner radius about 22%) at the tile's full size; the avatar slot is ONE solid flat cyan #00FFFF circle about 4.5% of the slide width. No logo, text, outline or shadow, and the band's colour clear around each.

A capture strip is ONE solid flat magenta #FF00FF rectangle of aspect {W:H} with square corners inside a thin ink outline; a chip zone is the same without the outline. Pure uniform magenta edge to edge, perfectly flat and frontal: no gradient, texture, glow, text, UI or tilt. All type stands clear of every zone with a visible gap.

No purple, violet, lavender, pink or magenta anywhere else: the top band is warm cream, never lavender or grey-blue, and the apricot fill reads as orange, never salmon or pink. No cyan, turquoise or blue except the tile and avatar slots; the selection box, bars and dots are orange.
