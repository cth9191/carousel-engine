# S14 Scenic Painterly: prompt block

A storybook listicle: a new painted landscape per slide, a Didone headline in the sky with one orange accent, a
paper list card floating over the middle distance, a small mono header row and a footer mantra, and, if you have
one, your own mascot doing a different activity in the foreground of each slide. Bare name lists read as filler,
so every row carries what the item does and a verified figure (spine C's item contract).

**Hybrid.** Codex paints one text-free landscape plate per slide. `shared/sky-tone.mjs` picks the type tone.
The header, headline, list card, capture, optional pose and footer are an HTML overlay from
`engine/styles/kits/S14/`. Same route as S15, with a painting instead of a photo.

The mascot is optional and always yours: transparent PNG poses you made, never a licensed character, never
painted into the plate. With no mascot, ask the plate for no Spot (drop the Spot sentence) and let its one small
orange object stand alone in the foreground.

**To Codex:** SYSTEM plus one layout's **Plate (paste)** with its braces filled. Image 1 is always
`engine/styles/refs/s14-ref-item.png`, an approved text-free morning plate made with this block: brushwork and
light only, never its scene. Once the deck's first plate is approved, attach it as Image 2, "match its
painting style and light; not its scene".

## Production split

| Element | Made by |
|---|---|
| Fit to 4:5 | Every plate: `python -I shared/composite.py plates/slide-NN.png fitted/slide-NN.png` (Codex returns 1092 x 1440; about 5% is trimmed top and bottom) |
| Type tone, scrims | `node shared/sky-tone.mjs $D` with each card's slide-data `box` (the headline stack): "white" sets cream #F5EBE0, "ink" sets warm ink #2A1E16; exit 4 = busy sky: edit the plate |
| Every word, list card, capture | `kits/S14/cards/slide-NN.html` copies in `$D/cards/` → `node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22` |
| Your mascot (optional) | One activity pose per slide from your own pose folder, copied to `$D/mascot/`, placed on the plate's clear spot with `<img class="pose" data-x data-feet data-w data-feet-y>`; Claude reads the spot off the fitted plate. Cut new poses with `shared/pose-check.py cut` (and `check --sprite` if your mascot fits its shape) |
| Captures | Real (README, the full list's own page), pre-cropped with `shots.py`, in the cover's `.win` frame |
| Proof figures | Stars or another verified figure per row, pulled on posting day and saved in the deck |

Order per slide: plate → fit → card copy (spot, optional pose, rows) → `sky-tone.mjs` → render → `exports/`.
Copy budgets: headline ≤ 5 words on 2 lines (one line may be the orange accent); list label ≤ 6 words;
**at most 6 rows per card**, each a real name (one line, never cut), a what-it-does line ≤ 8 words and one
figure; footer mantra ≤ 6 words, the same on every slide.

## SYSTEM

Visual system: a hand-painted landscape, full bleed, 4:5 portrait: a storybook background painting in
gouache and oil, broad soft brush strokes with visible texture, simplified shapes, warm glowing light and
gentle atmospheric depth. Not a photograph, not 3D, no outlines, no cel shading, no film grain.

Composition, three bands. Sky band, 0-34% of the height: open sky only, a smooth painted gradient with a
few soft cloud masses, its upper two thirds a deep, calm value (darker than the clouds, never pale or
washed out) so pale cream lettering reads on it: no glare, no sun disc, no bright white cloud behind the
middle 70% of the width, no birds, kites or balloons, and no tree tops, peaks or cliffs reaching into it
except within the outer 12% at the left or right. Middle band, 34-64%: distant, low-detail scenery only
(rolling hills, a far tree line, soft mountains, a calm sea): a card covers most of this band later, so
keep it soft and plain. Foreground, 64-100%: a meadow, river bank, path or clearing with grass texture and
a few small wildflowers. [With a mascot only:] The layout names one spot in the foreground: a clear, level
patch of short grass about 24% of the frame width with nothing on it and nothing in front of it (a small
character is placed there later). The bottom 6% is even grass or path.

Colour: painted greens (#5E8F2E, #8DB04A, #3F6B2A in shade), warm earth paths (#C9A46A), the layout's
sky. Orange (#D9551F) only as a few small wildflowers or the one small object the layout names. No
purple, violet, lavender, pink or magenta; no cyan, turquoise, teal or aqua: water is deep slate blue
(#3E5C7A) with warm highlights.

References: Image 1 (and Image 2, when attached) is an earlier plate in this style: copy only its
brushwork, softness and warm light. Do NOT copy its scene: its river, mountains, clouds, stump, mushroom or
layout.

No characters, creatures, people, animals, mascots or figures: any character is added later. Hygiene: no
text of any kind: no letters, numbers, signs, labels, logos, watermarks, captions, UI, panels, cards, frames
or borders. Never render these instructions or section names as text.

## COVER

**Plate (paste).** Layout, cover: the golden-hour version: a sky of deep honey-amber (#B8742E) at the top
easing to warm gold (#E0A85A) at the horizon, a few dusky peach cloud masses, never a bright orange glow.
Middle band: gentle rolling hills and a far tree line, low and soft; on the right half, from 38% to 72% of
the height, the scenery stays especially plain (a card is placed there later). Foreground: a sunlit meadow
with a few small orange and cream wildflowers. [With a mascot only:] Spot: a clear, level patch of short
grass centred at {28 | 72}% of the width, its ground line at 86% of the height.

**Overlay (`slide-01.html`).** Header row `{DECK LABEL}` + `1 / TT`. Stack at 7-40%: the count as a giant
orange Playfair Display 900 numeral (180-250 px, with an ink drop shadow) over a two-line Didone hook (92→76
px): the count, then the noun and audience ("research skills" / "for Claude Code"). A real capture of the
full list in a tilted cream-bordered window on the side away from the spot. With a mascot, the cover pose on
the spot (the deck's own job: a magnifier for research, a wrench for tooling, a book for learning), never
reused inside. The footer mantra.

## INTERIOR

**Item group** (spine C `item`, grouped: one slide per job, up to 6 items each). Plate (paste): Layout,
item: the {morning | afternoon | sunset | dusk} version: a sky from {pale clear blue (#CFE3EE) at the horizon
to deep mid blue (#4F80B5) at the top | warm apricot at the horizon to dusty rose-brown at the top | amber at
the horizon to deep navy at the top}, a few cloud masses with warm undersides. Middle band: {terrain far
away: soft mountains and a long lake | rolling farmland | a sea cliff | a forest edge}. Foreground: {a river
bank meadow | a dirt path | a clearing at a forest edge | a hilltop}. [With a mascot only:] Spot: a clear,
level patch of short grass centred at {x}% of the width, its ground line at {86-88}% of the height. {One small
object in the foreground (beside the spot, with a mascot), at most 7% of the frame width, the one orange
touch: a mossy stump with an orange mushroom | a small orange-roofed birdhouse on a post | a fence post with
an orange ribbon}.

Overlay (`slide-02.html`): header row with `NN / TT`; the job as the headline (line 2 or one word in
orange); the paper list card from y 420 (label: count and what it's sorted by; up to 6 rows: number, exact
name, figure, then the what-it-does line); the activity pose on the spot, with a mascot; the footer mantra.

**Proof** (optional, the 1-2 strongest items): the item plate with the spot (if any) moved to one side; the
list card replaced by the cover's capture window with the item's real README or output, plus one row card
under it for that item alone.

**CTA**. Plate (paste): the dusk version: amber at the horizon to deep navy at the top, a first star or two,
a meadow going dark with a warm-lit cabin window far away as the one orange touch. Overlay (`slide-03.html`):
headline ("Want the" / "whole list?"), a paper keyword card `Comment KEYWORD` (the keyword exactly once)
with one line naming the deliverable, a last pose (with a mascot), the footer mantra.

**Deck rules (Claude; never paste).**
- Light arc: cover golden hour, items morning → afternoon → sunset, CTA dusk. Never the same terrain twice in
  a row.
- With a mascot: one pose per slide, never repeated, each the group's job (magnifier: research; plug: MCP;
  book: docs; wind-up key: agents; padlock: security; set square: design; stopwatch: speed; clipboard:
  testing; wrench: tooling). The pose stands on the plate's clear spot, never in the list card's band.
- Grouping is a deliberate spine C deviation: log `item slides group up to 6 items by job` in
  `deviations[]`. Every row still carries its own what-it-does line and verified figure; a card of names
  alone fails G4.
- Cooldown groups `landscape-grounds` (S15, S28) and `grouped-list-mascot` (S22), 14 days each.

## KEYING

None. Plates are text-free and zone-free; captures and cards are HTML over the fitted plate, and any pose is
an HTML cutout, so nothing is keyed. `composite.py` exiting 3 on a plate means stray magenta: edit job.

## Notes from the sample plates

The two sample plates (`kits/S14/fitted/`) held the painting style, the three bands, the clear spots and the
item's orange-mushroom stump on the first try, and the morning plate is now `refs/s14-ref-item.png`. Drift: both skies came back lighter than asked (the cover a
saturated orange glow, the item a bright clear blue), so sky-tone chose warm ink instead of cream, and the
orange cover numeral needed an ink shadow to read. SYSTEM now asks for a deep upper sky and no bright cloud
behind the headline, and the cover sky is honey-amber, not cream-gold. Ink type on a bright sky stays in
style when sky-tone picks it.
