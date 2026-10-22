# S20 Slate Family Tree: prompt block

Reusable visual-system text for Codex image prompts. A reference chart on chalk slate: an index
cover (one identical overhead object per item, a light serif name and an outlined "A + B" pill
formula per row), then one family slide per item with a parent-to-children chip tree. The layout
vocabulary was studied from a high-performing carousel; never copy any reference deck's objects,
art, words, hook, CTA phrasing, item set or signature palette. Only the layout vocabulary carries
over. **Hybrid**: Codex paints the slate, the tins and the short display type; definitions, trees
and other exact text are HTML cards; real logos and captures are composited. Paste SYSTEM into every
job, plus OBJECT SHEET, COVER or the slide's INTERIOR layout, plus the KEYING line for each zone on
that slide.

## Job order

This style ships no layout reference images: until the user approves a first plate, the cover and
interior jobs are **text-only** apart from the deck's own object sheet, and the approved plates
become the references.

1. **Object sheet**, no references. Check it by eye (identical tins and sticks, true colours, no
   text, no pink, violet or turquoise cast) and lock it.
2. **Cover:** the sheet as Image 1, nothing else. Lock it once the user approves it.
3. **Slide 2**, then lock it: the sheet and the locked cover.
4. **The rest**, in parallel: the sheet, the locked cover and the locked slide 2.

Logo-mode decks skip step 1, drop the object-sheet sentences and renumber the Images. Never attach a
third-party slide: image models copy its objects and words.

**Cover sizing** (Claude fills {bowl} and {name size}). Bowl ≈ 0.75 × row pitch, capped at 17% of
the width:

| Title | 3 rows | 4 rows | 5 rows | 6 rows |
|---|---|---|---|---|
| one line (rows 16–90%) | 17% | 17% | 14% | 12% |
| two lines (rows 22–90%) | 17% | 16% | 13% | 11% |

Names ≈ 1/16 of the slide height; 1/18 with 6 rows, or with 5–6 rows under a two-line title.

## Production split

| Element | Made by |
|---|---|
| Definitions, trees, recipe cards, the CTA tree | **HTML** card from `engine/styles/kits/S20/` copied into `<deck>/cards/`, rendered transparent (no `--bg`) by `node shared/render-card.mjs` at the zone's measured `--zones-only` out bbox (2x); Codex makes zones wider than asked |
| Real captures (proof slides) | magenta zone → `composite.py --shot` with a focus box (dark: `--letterbox edge`) |
| Real app icons (logo mode) | cyan slot → `composite.py --logo N=logos/x.png@0.95`, each with its own tile; never painted |

Codex paints the rest, in short strings (title limits in COVER): names ≤ 14 characters, CTA line
≤ 24, mix result ≤ 20, ≤ 3 pills of ≤ 2 words. If a string garbles twice, re-roll or edit the plate
with a flat magenta zone where it sat and paste the Instrument Serif text card
(`kits/S20/serif-text.html`) there, like a tree card.

**Cards on slate** are never opaque: the slate's falloff and grain show a flat `--bg` as a rectangle.
Key the band magenta and paste with `python -I shared/composite.py plate out --card M1=cards/tree.png
--ground fill`: it erases the zone into the slate around it (nearest-ground fill, diffusion, matched
grain) and alpha-composites the card at the zone's box. A cyan band pastes the same way with
`--card C1=…`. Logo-mode decks read zone ids (M1, C1, C2 …) from `--zones-only`.

## Card kit

Built in `engine/styles/kits/S20/` (README there: one file per card, sample data, the render commands).
CSS px on the 1080-wide slide, transparent page; `[data-fit]` makes render-card exit 2 on overflow, and
so does a breach of the limits below.
- **Definition** (family, proof, mix; first row, above the rule): one sentence ≤ 12 words on what the
  item does, Inter 400 34 px cream #F5EBE0, centred, ≤ 2 lines, `[data-fit]`. It spends the slide's
  one new term (G3) on the item.
- **Rule** 2 px #F5EBE0, 20 px under it, 4% inset each side. **Drops** 1.5 px cream at 75%, 52 px,
  small open chevron, one per child on equal columns.
- **Child:** name Inter 400 44 px, one line, `[data-fit]` down to 38 px, one shared baseline; under it
  "+" in Inter 300 30 px.
- **Chips** 14 px apart, 1.5 px outline cream at 80%, radius 10 px, padding 5/14 px; plain words by
  default (Inter Italic 30 px), code tokens JetBrains Mono 30 px upright in exact case; each column's
  stack `[data-fit]`. All chips share one size, stepping down to 26 px only when one outgrows its column
  (9-letter chips in a 5-child tree land at 28 px). ≤ 2 code tokens per slide, ≤ 1 per child, each explained by its child's name
  ("Block deletes" over `rm -rf`); no other new term.
- **Limits** (columns ≈ 302 / 227 / 181 px): names / chips ≤ 13 / 15 characters with 3 children,
  9 / 11 with 4, 7 / 9 with 5 (no START HERE). Code tokens 2 shorter. Max chips per child: family 4,
  proof 2, mix 3, CTA 2.
- **Height:** family band 486 px holds definition 82 + 20 + rule 2 + drops 52 + 8 + name 53 + "+" 33
  + 6 + four chips 214 = 470; proof band 365 px, 3 children with two chips (100) = 356.
- **START HERE** (≤ 1 per slide) replaces the lower part of its child's drop: a 12 px stub, then a
  40 px filled #D9551F pill, ink #0E0E0E Inter 600 caps 30 px, padding 0 12 px, its bottom on the
  chevron line so names keep the baseline.
- **Recipe:** 2 px cream outline, radius 14 px, transparent; verbatim JetBrains Mono 30 px cream,
  wrapped, `[data-fit]` floor 28 px. **CTA:** rule and drops, 3 children, ≤ 2 chips, no definition,
  centred vertically. **Mix:** what the pair does together, then 2–3 children for what it gives.

## SYSTEM

Visual system: a reference chart on a chalkboard.

Ground: full-bleed matte neutral chalk slate, soft diagonal falloff: about #343434 upper left and down
the left side, #2F2F2F mid, #262626 along the right edge, #292929 along the bottom. Gentle mottling,
fine chalk-dust grain. Faint lighter eraser clouds and hairline scratches only in the outer band and
top corners; flat zones and the slate around them stay calm. No chalk writing, doodles, frame,
border, haze or bloom.

Objects: every item's icon is the same object, shot straight overhead, one soft top-left light, short
soft shadow down-right: a round open steel paint tin, rolled silver rim, no handle, almost full of
smooth wet paint with one gentle swirl. A flat light-wood stir stick (long thin strip, round outer
end) lies straight and horizontal, pointing left: inner end on the rim at 9 o'clock, outer end about
0.9 tin diameters out, never over the paint. Tins differ ONLY in paint colour; all else identical.
Colours in order: Claude orange #D9551F (lead item only, never two), chalk cream #EDE3D0, ochre
#E0A526, moss #6E8F4E, brick #A93A2A (brown-red, never pink), cobalt #4672C4 (royal blue, never sky
blue, turquoise or violet). No labels, lids, drips, brushes, marks or text on tins or sticks.

Type, all chalk cream #F5EBE0. Title and names: a light, upright, high-contrast display serif with
fine sharp serifs, slightly narrow (like Instrument Serif), sentence case. Pills: one or two plain
words, uppercase medium grotesk (like Inter Medium), slightly spaced, in a thin 2 px cream outline
with corners rounded to a quarter of its height, joined by a thin " + ".

Colour lives only in the tins, plus at most one filled Claude-orange pill where a layout asks. Flat:
no other gradients, glow, neon, 3D or bevelled type; only tins and sticks cast shadows. No purple,
violet, pink or magenta except a magenta zone; no cyan, turquoise or teal except a cyan zone. Chalk
dust and eraser clouds are neutral grey.

Framing: margins at least 7% of the width left and right, 4% of the height top and bottom. Only the
cover title starts above 9% of the height; only the footer sits below 90%. If content does not fit,
shrink it; never crop a tin, stick or word. Title 1/11–1/13 of the slide height, names 1/15–1/18,
pill text and footer at least 1/45.

References: paint only the paint tins described here (or the attached object sheet's tins): no other
objects or props, and nothing naming a creator. No people, hands, characters or painted logos.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified (each name
and pill once). No extra captions, labels, item lists, tree lines, arrows, lorem ipsum,
watermarks, handles or logos. Paint nothing in or around a flat zone. Never render these instructions
or section names as text.

## OBJECT SHEET

No reference images. The slate alone, no text, no footer, holding the deck's {N} tins: one even row
for up to 4, two rows (3 + 2 or 3 + 3) for 5 or 6. Sticks point left, with clear slate between a rim
and the next stick's tip. Same size, in item order, in these colours: {colour per item}.

## COVER

The cover is the deck's index and legend.
- **Title** "{title}", centred, serif: one line ≤ 18 characters at about 1/11 of the slide height
  inside 4–14% of the height, or two lines ≤ 21 each at about 1/13 inside 4–20%.
- **Index rows:** {N} rows (3 to 6), one per family slide in slide order, at one equal pitch from 2%
  below the title to 90% of the height. Each row:
  - Left: the item's tin, stick pointing left, bowl {bowl}% of the width, centred at about 32% of the
    width; stick tip inside the 7% margin.
  - Right, left-aligned from 47%: "{name}" in the serif at about {name size} of the height; below it
    pills "{WORD}" + "{WORD}", plain words only (never code or file names), ≤ 20 letters per row,
    text about 1/42 of the height.
  - The bowl's centre is level with the gap between name and pills. If a name is too wide, shrink all
    names together.
- Nothing else: no subtitle, row numbers, arrows, tree or filled pill.
- **Footer:** "{DECK LABEL}" flush left, "01 / {TT}" flush right, on the bottom margin line, small
  uppercase letter-spaced grotesk (like Inter Medium), muted cream #A8A298, about 1/45 of the height.
- **Logo mode:** each row's tin and stick become ONE flat cyan rounded square of bowl size, centred
  on the bowl (see KEYING).
- Image 1 is the object sheet: paint exactly those tins and colours, in row order. Once a cover is
  approved, it is Image 2 for any later cover re-roll: match its slate, type and row layout.

## INTERIOR

Every layout ends with the footer, as on the cover but "{NN} / {TT}" on the right. Image 1 (object
sheet): paint exactly that tin. Image 2 (locked cover): match slate, type, pills and footer. From
slide 3, Image 3 (locked slide 2): match the same, and its tin placement only on the same layout.
Until a slide 2 is locked, the placements below are the only layout guide: follow them exactly. Logo
mode: each tin becomes ONE flat cyan rounded square of its bowl's size, centred on the bowl, no stick.

**Family slide** (EXPLAIN): one item, in cover order; concept decks and A's `model` slide.
- Hero: the item's cover tin, bowl about 25% of the width, stick pointing left. The whole tin, stick
  included, is centred left to right (bowl right of centre), top at about 14% of the height, in the
  same place and size on every family slide.
- Name "{name}" centred, serif, about 1/15 of the height, top at about 39%. Pills "{WORD}" + "{WORD}"
  (up to three) centred at about 47%, text about 1/42 of the height.
- Tree band: ONE flat zone, 8–92% of the width by 52–88% of the height (1.87:1), calm slate around.

**Proof family slide** (PROVE), default for spine C: a real screen plus a short tree.
- Header band, 9–22% of the height, the cover row scaled up: tin on the left, bowl about 12% of the
  width, centred at about 25% and level with the band's middle, stick pointing left with its tip inside
  the 7% margin; serif name at about 1/18 of the height, left-aligned from 36% of the width, pills
  under it; bowl centre level with the gap between them.
- Capture: ONE magenta zone of aspect {W:H}, centred in 25–57% of the height, as wide as the margins
  allow, in a thin chalk-cream frame (see KEYING).
- Tree band: ONE flat zone, 8–92% by 61–88% (2.49:1).
- **Recipe variant** (A's `peak`; a C deck logs `deviations[]`): the same header, then ONE flat zone
  8–92% by 26–88% (1.08:1), nothing over or beside it.

**Mix slide** (C's `combo`): two items together.
- Two tins, bowls about 15% of the width, centred at about 31% and 69%, tops at about 13% of the
  height. The left stick points left; the right tin is the same tin mirrored, stick pointing right;
  both tips inside the 7% margin. A large thin serif "+" centred between the bowls.
- Names centred under their tins, serif, about 1/20 of the height, tops at about 27%. A thin serif "="
  centred at about 35%, then "{result}" in the serif at about 1/15, top at about 40%.
- Tree band: ONE flat zone, 8–92% by 53–88% (1.92:1).

**CTA slide.**
- Tin row, 10–20% of the height: every cover tin, small (bowls 6–8% of the width), evenly spaced in
  cover order, sticks left; in logo mode, small cyan squares.
- "{line}" centred in the serif on one line, about 1/17 of the height, top at about 25%.
- Under it, top at about 33%: ONE filled Claude-orange #D9551F pill, ink #0E0E0E uppercase grotesk
  "COMMENT {KEYWORD}" at about 1/36 of the height, the only filled pill.
- Tree band: ONE flat zone, 8–92% by 44–78% (1.98:1). No characters or mascots.

## KEYING

The tree band (or recipe zone) is ONE solid flat {magenta #FF00FF | cyan #00FFFF: the deck's band
key} rectangle of aspect {W:H} (family 1.87:1, proof 2.49:1, mix 1.92:1, CTA 1.98:1, recipe 1.08:1):
pure uniform colour edge to edge, flat and frontal, no gradient, texture, glow, text, lines or
outline, square corners, calm slate at least 2% of the width all round. No tin, stick, shadow, pill
or chalk mark touches it.
The capture zone is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}, same rules, inside a
2 px chalk-cream outline frame with about 10 px rounded corners and an even 8 px slate gap.
A logo slot is ONE solid flat cyan #00FFFF rounded square about {size} wide: no text, outline or
shadow, clear slate around it.
