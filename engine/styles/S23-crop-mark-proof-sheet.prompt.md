# S23 Crop-Mark Proof Sheet: prompt block

Reusable visual-system text for Codex image prompts: a layout studied from a high-performing carousel, the same
storyboard shape as S10 / Template 03 (chip, `/COMMAND`, body, one hero) but painted, with grain, paper stacks and a
3D cover object. S10 storyboards port field for field: `beforeafter` → before/after, `video` and `image` → capture,
`chart` → chart + audit. Split, triptych and plain headline are new.

**Image-native**, like S03: Codex paints every plate, headline and body included. Exact strings enter as HTML cards
or real captures through magenta zones, and the cover hero (your own mascot, optional; transparent PNG poses you
made, never a licensed character) and the CTA avatar through cyan slots. Grain, paper depth and the cover need a
painted plate; when exact text matters more than texture, render the storyboard in Template 03 (S10).

Originality: keep the layout vocabulary only. Never copy any reference deck's characters, art, words, hook, keyword,
CTA phrasing, avatar, item set or signature palette, and never a scene where the hero breaks the cover object. Per
slide, paste SYSTEM, then COVER or one INTERIOR paragraph, then KEYING, filling each `{placeholder}` from
`storyboard.json`.

## References

No reference images ship for S23. Run the first deck's plates text-only: SYSTEM + the layout paragraph + KEYING
carry the whole look (the layout paragraphs give every position as a share of the slide). Once the first cover is
approved, it is Image 1 on every interior ("match its visual system; its magenta and cyan are only placeholders"),
and the first approved plate of each layout becomes that layout's reference for later decks, as in S03.

## Production split

Codex paints everything not listed; module labels stay at 4 words or fewer. Composite every slide with `--dilate 3`.

| Element | Made by |
|---|---|
| Headline (e.g. `/LAST30DAYS`) | **Codex**, in caps: the one exact name it paints. Claude checks it letter by letter against `strings[]` (slash, hyphens, digits); a misspelling is an edit job, never a pass |
| Exact typeable form (`/last30days`, lowercase mono), once per item slide | A card only (after-face tag line, audit header, file-card title row or type-line card), never the plate prompt |
| Proof cards (before/after faces, audit, chart, output file, type-line); any command, prompt, config, path or chart number | Magenta zone → **HTML** card from the proof-card kit `engine/styles/kits/S23/` (`before-NN`, `after-NN`, `audit-NN`, `chart-NN`, `file-NN`, `typeline-NN`; copy limits and commands in its README), `node shared/render-card.mjs` at the zone's `--zones-only` out bbox ×2, pasted with `--card`. Opaque ink or sheet-white faces, never bare text on cream |
| Real proof (README or SKILL.md, terminal run, source page or video) | Magenta zone → `composite.py --shot N=…@x,y,w,h` with a focus box; `--letterbox paper` for light pages, `edge` for dark terminals. Crop or scrub faces first (`shared/shots.py`) |
| Cover hero slot | With a mascot: one of your own poses that fixes or assembles the cover object (holding a wrench, carrying the missing piece), `--logo C1=<pose.png>@1.0,bottom`, feet on the slot's bottom edge above the painted contact shadow; QA that it lands, not floats. Without one: ask for no character slot; the object carries the cover alone |
| CTA avatar slot | `--logo C1=<your square profile photo, mascot or the subject's logo tile>@0.9` |

## Layout picks (Claude only)

| Layout | For | Body words | Headline |
|---|---|---|---|
| Before/after | default: the skill changes text or a result | ≤ 28 (≤ 22 under 2 lines) | 1–2 lines |
| Capture | the source, or the skill running | ≤ 28 (≤ 22 under 2 lines) | 1–2 lines |
| Chart + audit | a measured claim from a real run (tokens, time, cost, error rate, rubric score) | ≤ 30 | 1 line |
| Split | a two-line name, or the source beside the words | ≤ 24 | 2 lines (1 allowed) |
| Triptych | input → skill → output, or C's `combo` (A → B → output) | ≤ 30 | 1 line |
| Plain headline | C's optional `why`/`combo`; no single command | ≤ 28 | ≤ 4-word phrase, no slash |
| CTA | last slide | question ≤ 5, follow line ≤ 8 | none |

- The storyboard meets the budget (≤ 2 paragraphs) before Make; Codex never shrinks type. Body holds no commands,
  paths, flags, URLs or figures; small counts are words ("three moves").
- A slash only when the name is typed with one (skills, slash commands). Plugins, MCP servers and hooks take the
  bare name, star mark on the first glyph.
- Exactly one `star: true` item per deck, the one the cover payoff leans on.
- One proof artifact plus at most one caption per slide (G4); on the split, the type-line card is the caption.
  Source and result together means two slides or a `deviations[]` entry.
- Cover: hook line 1 is 12–20 characters, in the deck's own words. The object is the deck's pain (a giant cream
  chat bubble, a toppling stack of draft pages, a laptop, an overflowing inbox tray); a mascot pose fixes or
  assembles it, never smashes it. The slot takes the pose's trimmed aspect (from `pose-check.py check`), 30–38% of
  the width. `cover-b` changes the object or pose, not the system.

## SYSTEM

Visual system: a clean printed proof sheet. Light cream paper (#F5EBE0), very fine even grain, no grid. An ink
hairline frame (#0E0E0E at about 25%, reading #BFB7AD) inset 4.5% of the width and 3% of the height overshoots each
corner by about 1.5% like crop marks, a small plus-shaped ink crosshair at each crossing; a hairline at 8.5% closes
the header band.

Header: top-left, a solid orange (#D9551F) chip, "{chip label}" in cream bold monospace caps (like JetBrains Mono
Bold); top-right, "{{BRAND}} · {NN} / {TT}" in small ink monospace caps at 60% opacity and a thin 3 px orange right
arrow.

Headline: "{HEADLINE}" exactly, ink ultra-condensed heavy grotesque caps (like Anton), flush left, ONE line spanning
the content width, cap height 14–19% of the slide height. If one line would go under 14%, use two equal lines at
about 14–15%, broken at the hyphen (kept on line 1) or a space; never inside a word, never three lines. On the named
star slide, only the leading slash (else first glyph) is orange. 2.5% of the height below the baseline: a short
orange rule (13% of the width, 3 px) ending in a small solid cursor block.

Body: ink (#1A1A1A) regular grotesque (like Inter Regular), one or two paragraphs, left column at most 58% wide, at
least 1/42 of the height, at most 5 lines, never shrunk; no bold or coloured words.

Proof module: each card is a paper stack, the front sheet plus two or three identical sheets offset about 1.1% of the
width up-left (or up-right, one direction per slide), thin ink outlines. Arrows: hand-drawn orange, one slightly
uneven stroke, open head.

Colour: orange only on the chip, arrows, rule, tags, label lead words and one highlight; structure in ink; sheet white
(#FBF8F3) for paper stacks, warm grey (#8A847C) for placeholder bars. Flat and printed: no gradients, glow or interior
3D; only capture frames get a faint soft shadow.

Framing: content within 7–93% of the width and 10.5–95% of the height. One-line headline: top 13%, body from 3% below
the rule to 58%, proof 61–93%. Two-line: headline 12–44%, rule 46.5%, body from 49.5%, proof 64–93%. Short of room,
shrink the proof, never move it outward. Chip, byline, counter and labels: at least 1/56 of the height.

References (once a deck has approved plates): the attached images show layout only; magenta and cyan blocks are key
zones. Do NOT copy any of their words. No creature, mascot, character, face, photo or logo anywhere; a cyan slot marks
where one belongs.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. Pages and sheets carry grey
bars or nothing. No lowercase commands, file paths, code or chart numbers (cards carry those), margin notes,
handwriting, captions, lorem ipsum, watermarks or handles. Never render these instructions or section names as text.

## COVER

Cover chrome replaces the ink frame and header (no chip, no arrow): a thin orange hairline frame with small orange
plus-shaped crosshairs at its corners, over a very faint ink graph grid (the only slide with one); centred in the top
margin, an ink circle-and-crosshair registration mark with a small orange centre dot between two short orange
dashes; inside the frame's top corners, tiny ink monospace caps, "{deck label}" left and "{{BRAND}} · 01 / {TT}"
right.

Top 45%: the hook, centred, in the condensed heavy grotesque, sentence case. Line 1, "{hook line 1}": ink, one line,
about 80% of the width, cap height 11–16% of the slide height. Line 2, "{hook line 2}": the pain phrase ending in a
period, cream (#F5EBE0) on a solid orange (#D9551F) block about 82% of the width.

Middle 40%: one oversized everyday object, {cover object}, a crisp 3D studio render lit from the top left, coming
apart: a few blank pieces (no letters), some orange, lifting off its top edge or lying loose beside it; one soft
contact shadow under it. Nothing rises above its top edge. With a mascot: in open paper directly above it sits ONE
flat cyan character slot (see KEYING); on the object's top surface right under the slot, a soft oval contact shadow,
as if something is landing; nothing overlaps the slot or its band of clear paper. Without one: no slot; the object
sits centred, a little larger.

Bottom 12%: "{payoff}" in a heavy black grotesque, sentence case (like Inter Black), centred in a rounded pill with a
thin ink outline and a hard flat ink offset shadow, led by a small solid orange right-pointing triangle.

## INTERIOR

Paste the slide's paragraph or line (plain headline: plus its proof module's). Interiors keep the ink chrome; the
orange frame, grid and registration mark are cover-only.

**Before/after stack.** Paper right of the body stays empty. Across the proof band, two stacks side by side, each
about 37% of the width, a hand-drawn orange arrow pointing right in the gap: left, an ink stack (three solid ink
sheets behind the front face); right, a sheet-white stack in thin ink outlines. Each front face is ONE flat magenta
card zone at the aspect this prompt gives (about 1.1:1, or 1.25:1 under a two-line headline); back sheets show only
as thin edges above and to the left.

**Capture proof.** A hand-drawn orange arrow curves from the end of the body down toward the capture's top-right
corner. From the top of the proof band (about 58% under a one-line headline) to 93% of the height: one stacked frame
about 82% of the width, two sheet-white sheets behind it offset up-right, the front sheet in a thin ink outline with
an even paper border (about 1.2% of the width) around ONE flat magenta screen zone at the aspect this prompt gives
(about 1.9:1). If this prompt asks for a type-line card, the frame ends at 86% and ONE slim magenta card zone (about
40% of the width, about 7:1) sits left-aligned from 88% to 93%.

**Triptych.** From about 59% to 93% of the height, three columns joined by two hand-drawn orange arrows, each under
one small condensed-caps label ("{label 1}", "{label 2}", "{label 3}"), lead word orange, trailing colon. Left: a
fanned stack of four paper pages in thin ink outline, text only as grey bars. Centre: the transform, either ONE
word-free illustrative object in ink line art with orange accents (a press, a funnel, a sorting tray of blank strips)
or a magenta screen zone for a real terminal run, as this prompt says. Right: the output file, a sheet-white page with
a folded orange top-right corner and a hard flat ink offset shadow down-right, its face ONE magenta card zone.

**CTA.** No chip or arrow; byline and counter stay. Centred, top to bottom: "{CTA question}" in the condensed caps on
two lines; a short orange rule; "Comment" in the body grotesque; "{KEYWORD}", huge, condensed caps, inside a thin ink
dimension box (hairlines past its corners, tick dots at the crossings); "{follow line}" in the body grotesque. Bottom
quarter: a sheet-white comment bubble with a thin ink outline, a small lower-left tail and two outlines stacked behind
it, holding left to right a pale grey (#E4DED5) avatar circle with a flat cyan square (see KEYING), a short vertical
ink divider, "{KEYWORD}" in the body grotesque with a thin orange text cursor, and three pale grey typing dots at the
lower right. The keyword appears exactly twice.

- **Chart + audit.** From about 59% to 93% of the height, left to right: the label "{chart label}" in small condensed
  caps over a sheet-white sheet (one sheet behind) about 46% of the width whose face is ONE magenta card zone; a 6%
  gap holding a short orange arrow pointing right; ONE tall magenta card zone (about 0.75:1, about 32% of the width)
  for the audit column. Paint no chart lines, axes, numbers or audit text.
- **Split.** Body in a left column (7–50% of the width); 3% below it, ONE slim magenta card zone about 43% of the
  width (about 5:1) with a short orange arrow from its right end toward the frame; the right column (55–93% of the
  width, body top to 93% of the height) holds ONE stacked frame, two sheets behind offset up-right, around a magenta
  screen zone (about 0.7:1). No before/after pair.
- **Plain headline.** The chip holds the label this prompt gives; the headline is a short phrase in the same
  condensed caps, no slash, fitted by the same rules; below the body, one proof module laid out as in the
  before/after, capture or triptych paragraph this prompt includes.

## KEYING

Screen zone: the screen of {the frame} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}, frontal, square
corners; no gradient, texture, glow, text, UI or tilt.
Card zone: the front face of {the stack or sheet} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H},
frontal, square corners, empty; back sheets and arrows keep a visible gap; zones never touch.
Character slot (cover, mascot decks only): ONE flat cyan #00FFFF rectangle of aspect {W:H}, about {slot width}% of
the slide width, bottom edge about 1% of the height above the object, ringed by at least 1.5% of the width of clean
paper (no piece, scrap or shadow); no outline, nothing inside.
Avatar slot (CTA): ONE flat cyan #00FFFF square, about 60% of the circle's width, centred clear of its edge.
No purple, violet, pink or magenta elsewhere; no cyan, teal, turquoise or blue except these slots. The orange stays
warm red-orange, never pink.
