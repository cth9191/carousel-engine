# S04 Brutalist Mascot Poster: prompt block

Reusable visual-system text for Codex image prompts. A brutalist printed poster: cream spec-sheet paper, a two-tier
condensed headline (an ink line, then a cream line knocked out of a flat orange block), a big cut-out hero in the
middle of the cover with four tilted tag chips around it, and ruled cards, framed captures and prompt cards on the
interiors.

**Hybrid.** Codex paints every plate: paper, chrome, the two-tier headline, body lines, the takeaway pill, and the
empty frames. The cover hero is your own mascot (optional; transparent PNG poses you made, never a licensed
character) or, with no mascot, the subject's real logo tile, always pasted through a cyan slot, never painted.
Captures go through magenta screen zones; tables, prompts, commands and steps are cards from
`engine/styles/kits/S04/` through magenta card zones. Per slide, paste SYSTEM, then COVER or one INTERIOR paragraph,
then KEYING, filling each `{placeholder}` from `storyboard.json`.

Cooldown: the cover is in group `brutalist-poster-cover` (S04, S22, S23; 30 days), one cover a month across the
group: this cover look wears out fast when it repeats. The interiors alone (under another cover) only follow the
usual 14 days.

## References

Attach the sanitized refs, copied to the deck's `refs/`: `engine/styles/refs/s04-{cover,table,capture,prompt}.png`,
built from the author's own S04 slides with every word as a grey bar, the orange blocks flat, the hero replaced by
one cyan slot over a soft contact shadow, the tag chips blank, and every card or capture a magenta block.

Cover, until a locked cover exists: `s04-cover` + `s04-table`. Interiors: the locked cover (Image 1), then the
layout's ref (Image 2): table → `s04-table`, capture → `s04-capture`, prompt and steps → `s04-prompt`, CTA →
`s04-table`. After your first approved deck, your locked plates replace these refs.

## Production split

Composite every plate with `--dilate 3`; cards with `--ground fill` (they're rendered without `--bg`, so their
rounded corners land on the plate's own paper).

| Element | Made by |
|---|---|
| Headline tiers, body lines, example chip, takeaway pill, CTA keyword, header and footer chrome | **Codex**, quoted verbatim from `strings[]`. Claude checks every headline and the keyword letter by letter; a misspelling is an edit job, never a pass |
| Cover tag chips (4 tokens, 6 characters or fewer each, e.g. `/goal`, `.md`, `MCP`) | **Codex**, letter-checked; a garbled chip is patched with `kits/S04/chip-NN.html` and `composite.py --paste …,erase`, never regenerated |
| Cover hero, with a mascot | cyan slot → one of your own mascot poses (a transparent PNG with its prop), `--logo C1=$D/assets/mascot/<pose>.png@1.0,bottom`; never painted |
| Cover hero, without a mascot | cyan rounded-square slot → the subject's real logo tile via `--logo` (see KEYING, logo slot); never a generated mark |
| Interior mascot cameo (optional, at most 2 interiors a deck, mascot decks only) | small cyan slot → a different pose of your mascot whose prop comments on that slide (a padlock on a permissions slide, a magnifier on a research slide); never the cover pose |
| Comparison table, prompt, command, config, steps | magenta card zone → `kits/S04/{table,prompt,steps}-NN.html`, `node shared/render-card.mjs … --min-px 22` without `--bg`, at the zone's `--zones-only` out bbox ×2, `--card N=… --ground fill` |
| Real proof (app UI, terminal run, README, page) | magenta screen zone in a painted white frame → `--shot N=…@x,y,w,h` with a focus box; `--letterbox paper` for light pages, `edge` for dark terminals; faces cropped or scrubbed first (`shared/shots.py`) |

String caps (checked before touch 1): tier-1 line ≤ 4 words (≤ 22 characters); block line 1–3 words ending in a
period (≤ 16 characters a line, at most 2 lines); kicker ≤ 8 words (≤ 40 characters); deck label ≤ 24 characters;
example chip ≤ 28 characters; body ≤ 2 sentences (≤ 30 words); closing line ≤ 14 words. Codex never paints a command
a reader would type, a number they must trust (outside the headline or chip strings), a mascot or a logo.

## Layout picks (Claude only)

Spines A, C and D (B head-to-heads belong to S03). One layout per slide:

| Role | Layout | Proof |
|---|---|---|
| A `what`, A `model`, D `parts`, C `why` | **Table**: 2–4 ruled rows, one accent row | EXPLAIN (the card) |
| A `why`, A `how`, A `use`, C `item`, D `step`, D `day` | **Capture**: example chip + one framed capture | PROVE (the capture) |
| A `peak`, A `start`, D `step` with a command | **Prompt** (prompt card) or **Steps** (2–4 numbered rows) | the real text |
| `cta` | **CTA** | — |

- Headline grammar on every slide: an ink line, then a cream-on-orange block line ending in a period. A question
  plus answer ("FINISHED A TASK? / PICK WHAT'S NEXT.") is the strongest interior form; 7 words or fewer in all.
- C item slides: the chip carries "{ITEM n/N · NAME}"; the name in the chip is the item's exact name in caps.
- Spine D cover: the kicker names the N steps ("{System} in {N} steps") and the four chips name the parts, so the
  cover shows the build's shape without a parts illustration.

## SYSTEM

Visual system: a brutalist printed poster. Warm cream paper (#F1EBE0) with a very fine even grain and the faintest
soft relief, no grid. Thin ink L-shaped corner brackets (#0E0E0E, 3 px) sit in all four corners, inset about 4% of
the width and 5% of the height. Header, at 5.5–8% of the height: "{deck label}" in small ink monospace caps (like
JetBrains Mono) at the left margin, a thin ink hairline running across to "{NN} / {TT}" in the same monospace at the
right margin. Footer, centred at 91–93% of the height: "{{BRAND}} · Swipe →" in small ink monospace.

Headline: two tiers in an ultra-condensed heavy grotesque in all caps (like Anton), flush left at the margin. Tier 1,
"{tier 1}", solid ink, sized so its longest line spans most of the content width. Tier 2, "{tier 2}", cream
(#F5EBE0) letters knocked out of ONE flat, square-cornered orange block (#D9551F) that runs from the left margin to
about the right margin, with a hard flat warm-grey offset shadow down and right (about 1% of the width); the letters
fill the block's height. Tier 2 ends with its period. Never a gradient, bevel or 3D on type.

Body: ink (#0E0E0E) in a WIDE, normal-width heavy sans in sentence case (like Inter ExtraBold), at least 1/40 of the
slide height, left-aligned at the margin, no orange words; never the condensed headline face. The takeaway, when the
prompt gives one: a small solid orange right-pointing triangle, then the line in the same wide heavy sans.

Colour: orange only on the block, the triangles, the example chip and one accent; everything else ink on cream.
Panels are flat and frontal: white capture frames with a soft grey shadow, no tilt, no tape.

Framing: every element inside an even margin of at least 7% of the width left and right and 5% of the height top and
bottom (the plate comes back about 0.76 wide-to-tall and is centre-cropped to 4:5, losing about 2.6% at the top and
bottom); content between 10% and 89% of the height. If content does not fit, make it smaller.

References: the attached images show layout only; grey bars are text this prompt supplies, magenta and cyan blocks
are key zones. Do NOT copy any of their words. No creature, mascot, character, face, photo or logo anywhere; a cyan
slot marks where one belongs.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. No spec-sheet metadata
(grid system, unit, snap, version, dates, technical specs, layout notes), coordinates, dimension labels, captions,
lorem ipsum, watermarks or handles. No lowercase commands, file paths or code unless quoted here as a chip. Never
render these instructions or section names as text.

## COVER

Header: "{deck label}" left, "01 / {TT}" right.

Top 6–45%: the headline. Tier 1, "{tier 1}", one ink line, glyphs about 9–13% of the slide height. Under it the
orange block with "{tier 2}" (one line, or two when the prompt says so), at least 18% of the height, its letters
filling the block.

Middle 46–80%: the hero. With a mascot: ONE flat cyan character slot (see KEYING) centred on plain paper, about
{slot width}% of the width and {slot height}% of the height, its bottom edge at about 78% of the height, with one
soft grey oval contact shadow painted just below its bottom edge, outside the cyan. Without one: ONE flat cyan logo
slot (see KEYING), a rounded square about 34% of the width, centred at about 62% of the height, with the same soft
contact shadow below it. Around the slot, four small tag chips, rounded rectangles with a hard flat shadow, each
tilted 4–7°, two orange with cream monospace text and two ink with cream monospace text: "{chip 1}" upper left and
"{chip 2}" upper right, beside the slot's top corners; "{chip 3}" lower left and "{chip 4}" lower right, beside its
shadow. Every chip at least 3% of the width clear of the slot and of each other; each word appears once.

Bottom 80–88%: a wide rounded pill with a 3 px ink outline and a hard flat ink offset shadow, cream inside, holding a
small solid orange right-pointing triangle and "{kicker}" in the wide heavy sans (like Inter Black, not the
condensed headline face), sentence case, one or two lines, centred.

## INTERIOR

Paste the slide's paragraph. Header "{deck label}" left, "{NN} / {TT}" right; footer as in SYSTEM.

**Table.** Headline 10–34% of the height. 2.5% below it, "{lead}" in the body grotesque, one or two lines. From about
44% to 82% of the height: ONE magenta card zone (see KEYING) at the aspect this prompt gives, spanning the margins.
Below it, "{closing line}" in the body grotesque, then the takeaway line "{takeaway}" led by the orange triangle.

**Capture.** Headline 10–32%. Under it, one small orange chip tilted about 3°, "{chip}" in cream monospace caps. Then
"{body}" in the body grotesque, one or two lines. A small ink monospace source label, "{source label}", sits left-
aligned just above the frame. The frame: a white rounded panel with a soft grey shadow, spanning the margins, from
about 50% of the height to at most 80%, its screen ONE magenta screen zone at the aspect this prompt gives, an even
white border of about 1.3% of the width. Below it, "{closing line}" in the body grotesque, one or two lines.

**Prompt / Steps.** Headline 10–48% (two block lines allowed). 2.5% below it, "{lead}" in the body grotesque, one
line. Then ONE magenta card zone (see KEYING) spanning the margins at the aspect this prompt gives, its bottom edge at
or above 85% of the height. Below it, "{closing line}" in the body grotesque, one or two lines.

**CTA.** Header "{deck label}" left, "{TT} / {TT}" right; footer "{{BRAND}}" only. Headline 10–36%: tier 1
"{statement}" (≤ 4 words) in ink, then the orange block holding "{KEYWORD}" in cream, no period. Under it, "Comment
{KEYWORD} and I'll send you {deliverable}." in the body grotesque, two lines at most. Then a wide rounded pill with a
3 px ink outline holding the orange triangle and "{deliverable name}". The keyword appears exactly twice. Nothing
else: no URL, no "save", no "follow".

**Mascot cameo** (optional, mascot decks only; add to Table, Capture or Prompt): ONE small flat cyan slot (see
KEYING), about 22–28% of the width, standing on the paper at the right margin beside the closing line, its bottom
edge on a soft contact shadow; the closing line wraps short of it. Never on a card, frame or the orange block.

## KEYING

Screen zone: the screen of the white frame is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}, frontal,
square corners, no gradient, texture, glow, text, UI or tilt, with an even white border around it.
Card zone: ONE solid flat magenta #FF00FF rectangle of aspect {W:H} on plain paper, frontal, square corners, empty,
no outline or shadow of its own; the card supplies both. At least 2% of the height of clear paper above and below.
Character slot (mascot decks): ONE solid flat cyan #00FFFF rectangle of aspect {W:H}, frontal, empty, no outline; at
least 3% of the width of clean paper on every side (no chip, line, shadow or text in that ring); one soft grey
contact shadow just below its bottom edge, outside the cyan.
Logo slot (no mascot, or a second mark): ONE solid flat cyan #00FFFF rounded square about {size}% of the width,
flat, no text or outline, with clear paper around it.
No purple, violet, pink or magenta anywhere else; no cyan, teal, turquoise or blue except these slots. The orange
stays a warm red-orange, never pink or salmon.

## Compositing (Claude only)

With a mascot: slot aspect = the pose's trimmed aspect × 1.04 (W : H), so the pose fills the slot's height and its
feet land on the shadow. Measure the aspect with `python -I shared/pose-check.py check <pose.png> --sprite <your
sprite>` (it prints `aspect` and `feet_y`; keep them in your pose set's `index.json`). Cover slot: {slot height}
27–30% of the height, {slot width} = that × the aspect × 1.25 (about 55–65% of the width); cameo: 22–28% of the
width. Codex returns slots and card zones about 15–25% wider than asked; the pose is fitted by height with
`,bottom`, so a wide slot only widens the erased paper around it, and cards are rendered at the measured bbox, never
the asked aspect. A deck uses each pose once; the cover pose never repeats inside. Without a mascot, the logo tile
goes in with `--logo C1=$D/logos/<subject>-tile.png@0.9` (render a simple-icons mark onto a tile with
`shared/render-card.mjs`, or use the subject's own logo file).

1. `python -I shared/composite.py $D/plates/slide-NN.png $D/runs/zones/slide-NN.zones.png --zones-only --report $D/runs/zones/slide-NN.json`;
   read each zone's id, aspect, fill (≥ 0.97) and `out bbox`. A slot narrower than the pose's aspect, or a zone
   overlapped by a chip, is an edit job ("make the cyan slot {x}% wider, keep everything else").
2. Cards: copy `engine/styles/kits/S04/{kit.css,kit.js}` and each `<card>-NN.html` into `$D/cards/`, fill the JSON
   from `strings[]` and the real source, render at the zone's out bbox ×2 without `--bg`, `--min-px 22`. Exit 2 is a
   copy problem: cut the copy, never the floor (limits in `kits/S04/README.md`).
3. `python -I shared/composite.py $D/plates/slide-NN.png $D/final/slide-NN.png --logo C1=$D/assets/mascot/<pose>.png@1.0,bottom --card M1=$D/cards/<card>-NN.png --shot M2=$D/shots/<x>.png@x,y,w,h --ground fill --dilate 3 --report $D/runs/composite/NN.json`
   (the `--logo C1=…` part is the mascot pose or the logo tile, whichever the deck uses).
4. Check the report: a pose's placed bottom sits within 4 px of the slot's bottom; no leftover key. QA the
   headline, chips and keyword letter by letter against `strings[]`.
