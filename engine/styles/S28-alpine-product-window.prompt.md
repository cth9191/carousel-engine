# S28 Alpine Product Window: prompt block

A product-page listicle, from a layout studied from a high-performing carousel. Keep its system: one
bright alpine wallpaper behind every interior; an app-icon tile over a heavy product name, a two-line
subtitle and a chip row; one dark window floating over the scenery; a three-cell icon footer; solid
studio bookends. Never copy any reference deck's characters, art, words, hook, CTA phrasing, item set
or signature palette; only the layout vocabulary carries over. Every window holds a real capture,
never a painted imitation of a product's UI.

**Hybrid, on per-deck cards.** Codex paints three text-free plates per deck (scene, cover, CTA);
Playwright renders every word, chip, window and icon over them. The starter kit is
`engine/styles/kits/S28/`: `cards/s28.css`, one page per layout (cover, before/after, item, combo,
CTA), `cards/tile-NN.html` for the cover-slot tiles, rendered samples and a README; copy `cards/*` into
`$D/cards/` and replace every string. SYSTEM, one **Plate (paste)** paragraph and, for the cover only,
KEYING go to Codex; every **Card** paragraph is Claude's HTML spec and never goes to Codex. No
reference image goes to Codex until you approve a plate. A template fork would save the per-deck
cards; ask the user before forking a new template.

## Production split

| Element | Made by |
|---|---|
| Plates | `shared/codex-img.mjs`, 2 variants each, text-only prompt. Scene, CTA: `python -I shared/composite.py plates/x.png fitted/x.png` (fit to 1080x1350; exit 3 = stray magenta, usually a pink flower: edit job). Cover: `--zones-only` must find exactly N cyan zones, each fill ≈ 0.95 (the 22% corner radius; under 0.93 something overlaps: edit job), then `--logo i=logos/x.png@1.0` per slot, tiles at the same corner radius |
| Every word, chip, window, footer | `$D/cards/page-NN.html` + `$D/cards/s28.css`, plate as CSS background (`center / 1080px 1350px`): `node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 20`. `data-fit` + `window.cardReady`; exit 2 = shorter copy |
| Window body | One real capture (`shared/shots.py`, focus box, key text ≥ 30 px) as `<img>`, contain-fit, letterboxed on its edge colour. Spine A only: `peak` / `start` hold the exact prompt or command as mono text (#E8E6E3, 28–32 px); `what` / `model` may hold an HTML mock or diagram tagged `evidence.kind: explain`, never shown as proof |
| Tiles, cover icons | Real app icon, org avatar or simple-icons mark on a #111111 or #FFFFFF rounded tile (render-card); no mark: a cream Lucide glyph on #111111 |

**Tokens** (`s28.css`): Inter 300–900, JetBrains Mono 500, Anton, Caveat Brush. Ink #0E0E0E, subtitle
#2B2F36. Window #121418, 1 px rgba(255,255,255,.08), radius 26, shadow `0 30px 60px rgba(14,14,14,.35)`,
44 px bar, dots #FF5F57 #FEBC2E #28C840. Chip tints in order: apricot #FBE3D6, butter #FFF1CC, sage
#E2EDD9, sand #EFE5D8, stone #E9E7E3; icon strokes a deeper shade of each (#D9551F on apricot). Lucide
inline SVG, 2 px stroke. Interior veils: white radial at .6 over y 20–390, white band at .5 over y
1100–1300 (raise to .75 if a word reads under 4.5:1). Background `url(../fitted/scene.png)`. Margins
64 px.

## SYSTEM

Visual system: a bright, soft-focus photoreal scene, 4:5 portrait, like a premium app-launch wallpaper. Clean and luminous: gentle bloom, shallow depth of field, no grain. Two grounds; the layout names one.

Alpine ground: a sunny alpine valley in late spring. Snow-capped granite peaks rise in the left and right thirds, tops at 14–30% of the height. Between them the centre top is open sky, mid-blue #4A84C2 at the top edge fading to hazy near-white #EEF3F8 behind the centre from 12% to 36%, with a few soft white cloud banks. Dark pine forest (#2F4A2E) runs down both sides from 30% to 62%. A calm lake lies across the middle (42–72%): slate blue-grey water #5E7B91 with pale grey reflections. The bottom 22% is a soft-focus wildflower meadow with a few grey boulders: white daisies, buttercup yellow #F2C230, cream and soft orange blooms in fresh green grass; a pale morning mist over the far shore keeps 80–90% light. One out-of-focus leafy branch enters from the top-left corner. No people, animals, buildings, roads or boats.

Studio ground: a seamless studio backdrop in Claude orange #D9551F, lit from the upper right, deepening to burnt sienna #8F3414 toward the left and bottom edges, smooth, faint vignette. Light pools softly behind the hero only; the left 55% and all four corners stay clean, even and deeper (#9A3816 to #7E2C10). One hero object, named by the layout, as a clean softly lit 3D product render: matte materials, one soft contact shadow.

Colour: no purple, violet, lavender, pink, magenta or crimson anywhere: flowers are white, yellow, cream or orange, and the studio stays orange to burnt sienna, never red-wine. No cyan, turquoise, teal or aqua anywhere: water is slate, the sky mid-blue, never green-blue. The only exceptions are KEYING's flat zones.

Framing: on the alpine ground, 4–38% of the height behind the centre 70% of the width and the band 82–96% stay bright, calm and soft; nothing sharp or high-contrast there.

References: none until a plate is approved; then the approved plate is Image 1: match its light, lens and palette, add nothing.

Hygiene: apart from KEYING's flat slots, no text, letters, numbers, logos, icons, UI, screens, windows, cards, frames, borders, watermarks, people, animals, characters or mascots. Never render these instructions or section names as text.

## COVER

**Plate (paste).** The studio ground. Hero in the right 50%, base at 74–90% of the height: an open matte cream toolbox (#F2E9DE) with a hinged lid and no handles or labels, about 40% of the slide width, seen slightly from above and three-quarters on, the lid swung open behind it, a warm amber glow (#F4B06A) rising from inside. Rising out of it in a loose staggered cluster, {N} flat cyan logo slots (see KEYING), each about 12% of the width, between 34% and 66% of the height, with clean backdrop between them.

**Card** (page-01.html over fitted/cover.png). Cream #F5EBE0 type from x 72, at most 560 px wide. Corner micro-labels (Inter 600, 22 px caps, tracking .3em, under 3 short lines, a 40 × 3 px cream rule): top-left "{{BRAND}}", top-right the deck label and month, bottom-left "01 / {TT}". Hook stack, y 300–1040: the count as a giant numeral (Inter 900, 300–380 px, line-height .8); the list's noun in caps (Inter 800, fitted to 520 px, 64–80 px); one script word (Caveat Brush, 120–150 px) over a hand-drawn cream underline; a closing line (Inter 300, 72–90 px). Your own hook (bank F5, F8 or F9 in `engine/hooks.md`), count = item slides (G1), no comment ask. The slots carry the items' tiles in deck order.

## INTERIOR

**Scene plate (paste, once per deck).** The alpine ground, full frame, nothing else. Every interior card uses fitted/scene.png; once approved it may be reused as-is on later S28 decks.

**Item** (spine C `item`; spine A pages with the subject's tile repeated). Card: tile y 34–184, 150 px, radius 34, shadow. Name y 196–300, exact case, Inter 800 104 px (floor 76, two lines at most), tracking -0.045em, ink, centred. What it does y 308–388, ≤ 14 words, Inter 500 34/40, ≤ 2 lines. Chips y 410–462: 3–5 pills, 52 px, radius 16, 24 px icon + Inter 500 26 px, ≤ 2 words each, real README features; the row fits 952 px or drops a chip. Window x 70–1010, y 500–1080, its bar carrying the capture's source in JetBrains Mono 20 px #8B9096 ("github.com/owner/repo"). Footer y 1118–1212: three cells split by 1 px rules, each a 48 px ink icon + two lines of Inter 500 26 px, ≤ 5 words: what it replaces, one concrete use, proof (★ stars · licence, or price; verified on posting day). Counter y 1250: "{{BRAND}} · {NN} / {TT} →", Inter 600 26 px caps, tracking .35em, centred over a 140 × 2 px ink rule.

**Before / after** (C's optional `why`, A's `why`). No tile; the title moves to y 60–260: the stake, ≤ 7 words, one Claude-orange word. Subtitle as Item, no chips. The window body splits into two cells by a 1 px divider, each topped by a label row ("✕ without" #E5534B, "✓ with" #3FB950, Inter 600 24 px) and holding a real capture of the same task, or one sample text rendered twice in HTML (tagged explain). Footer: old cost, new cost, source.

**Combo** (C's `combo`, slide n-1). Two 130 px tiles joined by an ink "+" (Inter 800, 80 px) in the tile row. Title: the pair's job, ≤ 7 words. Subtitle: what the pair does. Chips: none or 3. Window: one real capture of both at work (a Claude Code session calling both). Footer: setup order, one use, proof.

**CTA.** Plate (paste): the studio ground; the same cream toolbox, now shut and latched, a blank cream tag tied to the lid, right 50%, base at 72–90%; no slots. Card: the cover's micro-labels with "{TT} / {TT}"; "COMMENT" in Anton 150 px cream; "{KEYWORD}" in Anton up to 190 px, ink, on a cream block (radius 10), exactly once; a 96 px cream Lucide message-square glyph; the deliverable in Inter 500 40 px cream, ≤ 10 words.

**Deck (Claude; never paste).** Order: cover, optional why, items, optional combo, CTA; 10 slides at most, so 6 items at most. Chip tints restart on every slide. Every item and combo window holds a real capture. No mascot by default: the cover's actor is the toolbox. Your own mascot (optional; transparent PNG poses you made, never a licensed character) fits only where a pose comments on the slide, composited as an `<img>`, never painted.

## KEYING

Cover only. Each logo slot is ONE solid flat cyan #00FFFF rounded square, corner radius about 22% of its side, about {size}% of the slide width, frontal and untilted: pure uniform cyan edge to edge, with no icon, text, outline, gloss, gradient, glow or shadow on it. Clean backdrop or glow shows all round each slot; no slot touches another, the toolbox or its lid, and the amber glow never tints a slot. These are the only cyan pixels; there is no magenta on the slide. No purple, violet, pink, magenta, turquoise, teal or blue anywhere on the cover.
