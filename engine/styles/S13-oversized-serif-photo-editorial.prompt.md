# S13 Oversized-Serif Photo Editorial: prompt block

A calm photo editorial: one dominant oversized serif word over a cinematic grainy photo, a small grotesk kicker
and trailing line, the deck's own interiors fanned below it, a three-item mono masthead, a numeral badge on every
rule, and photo pages that alternate with quiet grainy text pages. A layout studied from a high-performing
carousel; only its layout vocabulary carries over. Never copy any reference deck's subjects, art, handle, role
line, words, hook, CTA phrasing, item set or signature palette, and the cover fan only ever shows your own slides.

**Hybrid.** Codex paints a text-free photo plate for the cover and for each photo page; quiet pages have no
plate. Every word, the masthead, the numeral badges, the fan and the grain are an HTML overlay from
`engine/styles/kits/S13/`. **The cover renders last**: its fan shows the deck's own rendered interiors.

**To Codex:** SYSTEM plus one layout's **Plate (paste)** with its braces filled. Refs: none for the first plate
of your first deck (text-only prompt). After that, `engine/styles/refs/s13-ref-photo.png` (a sample photo plate
made with this block; swap in your deck's first approved photo plate once you have one) as Image 1 for every
later photo page, "match its grain, softness and grade; not its subject, water or horizon". Never attach anyone
else's slide (they all carry type).

## Production split

| Element | Made by |
|---|---|
| Fit to 4:5 | Every plate: `python -I shared/composite.py plates/slide-NN.png fitted/slide-NN.png` (Codex returns about 1122 x 1402). An exit 3 means stray key colour: edit job |
| Type colour, scrim | `node shared/sky-tone.mjs $D` reads each card's slide-data `box`, picks ink or white by WCAG contrast and stamps `<body>`; exit 4 = a busy calm zone: edit the plate. Quiet pages are skipped (no fitted plate) |
| Every word, masthead, badges, grain | `kits/S13/cards/slide-NN.html` copies in `$D/cards/` (`{{BRAND}}` filled), slide-data JSON filled → `node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22` |
| Cover fan | Three `<img>` of the deck's own exports (the strongest rule page in front), rendered after every interior |
| Real UI | Only when a rule needs proof: one capture card on a quiet page (the kit's `.fan .card` shell, unrotated). Never on a photo page |

Order: photo plates → fit → interiors (tone pass, render) → cover (tone pass, render) → exports.
Copy budgets: a rule headline ≤ 7 words, 2 lines; body ≤ 3 short paragraphs, ≤ 40 words, one bold phrase;
cover kicker ≤ 4 words, giant word one word (it grows to span 872 px; under 220 px the page fails: pick a
shorter word), trailing line ≤ 4 words; the cover's three-phrase row ≤ 2 words each.

## SYSTEM

Visual system: an editorial film photograph, full bleed, 4:5 portrait, made for a magazine spread.
Medium-format film look: a quiet, slightly desaturated natural grade, soft contrast, lifted blacks, heavy
visible film grain over the whole frame (even in flat sky and still water), a very soft lens and a little
atmospheric haze. One subject in a vast, calm, empty environment: open sea, a still lake, tall grass, a
salt flat, fog, a dune. Calm and spacious, nothing staged or glossy.

Composition: the layout names a calm zone where type is set later. It holds only even sky, water, mist or
grass in soft gradients: no subject, no horizon detail, no birds, boats, hard-edged clouds, sun discs or
flares. The subject stays where the layout puts it, whole and uncropped, sharp, with only the shadow or
reflection the scene gives it. Keep it below the stated line even if that leaves the frame mostly empty.
The left and right 8% hold only continuous environment.

Colour: photo-native: slate and grey-blue water, pale overcast skies, wheat, sage and straw grass, warm
sand. One warm accent only where the layout names it: an orange (#D9551F) touch on the subject, or a soft
warm orange haze. No purple, violet, lavender, pink or magenta; no cyan, turquoise, teal or aqua: water is
grey-blue or slate, never tropical.

No famous people, faces, characters, mascots or recognisable film stills. A person, only when the layout
asks for one, is anonymous and seen from behind or far away.

Hygiene: no text of any kind: no letters, numbers, signs, labels, logos, watermarks, captions, UI, frames,
borders or split-screens. Never render these instructions or section names as text.

## COVER

**Plate (paste).** Layout, cover: a wide {field of tall pale straw grass | calm grey sea | salt flat} under
a soft overcast sky that warms to a pale peach near the horizon. Calm zone: the whole top 50% of the frame
is sky only; the horizon is a soft, low line or nothing at all, at 54-58% of the height. The lower 42% is
the foreground, evenly textured and softly out of focus, with nothing in its centre 70% (cards are placed
there later). One small anonymous subject, {subject, e.g. a walker seen from behind in an orange jacket},
stands at the horizon in the {left | right} outer fifth, 4-7% of the frame width. The bottom 12% warms into a
faint orange light leak (#E8743A at low strength) rising from the lower edge.

**Overlay (`slide-01.html`).** Masthead `{Mon} ©{YYYY} · {{BRAND}} · {role}` in 22 px mono caps. In the
stack (8-46%): the kicker (Inter 800, 72 px, indented 70 px), the giant word in Instrument Serif (grows to
872 px wide, 220-460 px), the trailing line right-aligned under it (dropped 0.14 em below a descender). The
fan from y 660: three of the deck's own exports at about 300 x 375, rotated -11 / -2 / +10 degrees, the
strongest rule page in front and larger. A warm soft-light gradient over the bottom 300 px; the three-phrase
row at the foot ("5 rules." / "Any model." / "No fluff."), its tone from sky-tone's nav band. Spine C's count
lives in the kicker; the month in the masthead is the cover stamp.

## INTERIOR

**Photo page** (spine C `item`: one rule; also `why`). Plate (paste): Layout, photo page: {calm open sea |
still lake | tall grass | fog over a salt flat} under a {pale grey-blue overcast | soft white} sky. Calm
zone: from 10% to 64% of the height, the full width: only smooth sky and {water | grass | mist}. The subject:
{one small everyday object, the rule's metaphor, e.g. an empty wooden rowing boat}, centred or in the right
third, 24-34% of the frame width, its top at 66% of the height or lower and its base between 80% and 88%.
{One orange touch on the subject | No orange anywhere on this slide}. Overlay (`slide-02.html`): masthead;
the stack at 11-60% (slide-data box `[0.10, 0.61]`): a 128 px numeral badge beside the headline (Inter 700,
66→56 px, tracking -0.055em), then the body (40→34 px, 2-3 short paragraphs, one bold phrase).

**Quiet page** (alternates with photo pages; also the `combo` or a proof page). No plate: a photocopy-grey
ground (#CFCDC8) with toner grain and vertical streaks drawn by the kit. Overlay (`slide-03.html`): masthead,
the badge above an 80→66 px headline, a 42→36 px body. One unrotated capture card may sit under the body
when the rule needs proof.

**CTA** (`slide-04.html`, quiet ground). Kicker "comment" over the keyword as the giant serif word in orange
(the keyword exactly once), then one line naming the deliverable.

**Deck rules (Claude; never paste).**
- Rhythm: cover, then photo / quiet alternating, photo first; never two photo pages in a row, so each photo
  costs one Codex job and a 7-slide deck needs about 4 plates.
- Subjects: one per photo page, the rule's metaphor, never the same kind twice (boat, chair, ladder, kite,
  lantern, lone tree, door frame in a field). Environments rotate: sea, lake, grass, salt flat, fog, dune.
- The cover subject stays at the horizon edge: the fan covers the centre.
- Cooldown group `photo-editorial` with S15 (14 days): never back to back with a landscape-specimen deck.

## KEYING

None. Plates are text-free and zone-free; real UI never enters a photo, it sits on a quiet page as an HTML
capture card. `composite.py` exiting 3 on a plate means stray magenta: edit job.

## Notes from the sample plates

The two sample plates (`kits/S13/fitted/`) came back usable on the first try: the grain, the grade, the calm
zones and the lone subjects held. Drift seen: the photo page's horizon came back at 48% and the boat at 62-70%
instead of 30% and 78-84%; the overlay still cleared it (the body ends at 60%), and SYSTEM now says "keep it
below the stated line even if that leaves the frame mostly empty". A cover walker in the right third was
half-hidden by the fan, so the cover subject now stands in the outer fifth at 4-7% of the width. sky-tone chose
ink on both plates with no scrim.
