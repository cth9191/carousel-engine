# S10 Command-Press Blueprint: prompt block

A blueprint spec sheet: bone paper with a faint ink grid, an Anton `/SLASH-COMMAND` headline that bleeds right,
dimension lines, FIG and SHEET labels and orange corner crosshairs. Template 03 (`templates/03-command-press/`)
already renders the whole look; this block adds the cover kit, an exact-text card, and the one thing HTML can't draw
well: an engineering drawing.

**HTML-native, with Codex FIG plates.** Every slide is HTML. Interiors are Template 03 command sheets (the default
`hero.type` layout, not `layout:'atlas'`, which is S22), baked by `node shared/export.mjs --carousel <id>`. The cover is
`engine/styles/kits/S10/cover.html` rendered to `$D/cover.png`. Codex paints only **FIG plates**: word-free
isometric line drawings on white, with numbered balloons, shown as FIG.0 on the cover and as the `image` hero of a
model or parts sheet. Nothing a reader must read or trust is painted. Paste FIG SYSTEM, then FIG COVER or FIG
INTERIOR, then KEYING into each FIG job.

Spines A, C and D. S10 and S23 take the same storyboard field for field (chip, /COMMAND, body, one hero); pick S10
when exact text matters more than texture (code-heavy decks), and keep S10 and S23 interiors 14 days apart (a hand
check: build-gallery counts covers only). The S10 cover is not in the brutalist-poster-cover group.

## References

FIG plates run with no reference image (the smoke test came back on-system without one). After a deck's first
approved FIG plate, attach it as Image 1 to every later FIG job in that deck ("match its line weight, hatching and
balloons; draw a new object"). Never attach a slide: the plate is a drawing, not a layout.

## Production split

| Element | Made by |
|---|---|
| Every word, number, chip, FIG line, sheet counter, headline | **HTML**: Template 03 `slides[]` (`chip`, `headlineHTML`, `fig`, `body`, `hero`) and `kits/S10/cover.html` JSON, filled from `strings[]` |
| Cover | `kits/S10/cover.html` → `node shared/render-card.mjs $D/cover.html $D/cover.png --w 1080 --h 1350 --scale 2 --bg "#ECE3D4" --min-px 16`; `slides[0] = {cover:true, coverImg:'cover.png'}` |
| FIG.0 on the cover; FIG on A `model` / D `parts` / C `why` sheets (at most 2 interior FIGs a deck) | **Codex** FIG plate (this block), 3:2, white ground. Cover: the kit multiplies it onto the grid. Interior: `hero:{type:'image', src:'assets/fig-NN.png', maxH:470, focus:'center'}` (a white drawing sheet in the orange frame) |
| Prompt, command or config (A `peak` / `start`); the CTA's deliverable stub | `kits/S10/prompt-NN.html` → render-card at 920 × (360–460) ×2, `--min-px 22`, into `$D/assets/`, shown as an `image` hero |
| Real proof (README, terminal run, app UI, source video) | `image` hero with a real capture, or `video` hero with the real thumbnail (faces cropped or scrubbed with `shared/shots.py`) |
| Before/after text | `beforeafter` hero, text from a real run (spines.md: a mock is never proof) |
| Chart + audit | `chart` hero; the `good`/`bad` points come from a real run saved in `evidence.source` (orange = with it, ink dashed = without). The template's sample curves are illustrative and never ship |

String caps (checked before touch 1): headline one name, 14 characters or fewer (a leading `/` only when it is typed
with one; plugins, MCP servers and hooks take the bare name); chip 12; FIG line 46, a plain fact; body ≤ 45 words in
2 short paragraphs with one `accent` phrase; cover lines per the kit (12 characters a line). Template 03's own chrome
(chip, REV, 1080 PX, SHEET, FIG) is 13–17 px mono ornament; only the FIG line carries a fact, so keep it short.

## Layout picks (Claude only)

| Role | Sheet | Hero |
|---|---|---|
| cover | kit `cover.html`: **fig** (default for A and D; required for D: FIG.0 draws the N parts as balloons 1..N and the eyebrow names "{N}-PART" or "{N}-STEP") or **stack** (type only, 3–4 lines; a C list with a verified star figure in the command box) | FIG.0 plate |
| A `what` | `/NAME` + one-sentence definition | real capture of the thing (`image`) |
| A `why`, C `why` | the pain in the headline word | `beforeafter` from a real run |
| A `model`, D `parts` | `PART 02` chip, headline the system's name | FIG plate, balloons 1..N, the body names them ("1 note · 2 link · 3 note" also in the FIG line) |
| A `how`, C `item`, D `step` | `SKILL 0n` / `STEP 0n` chip, `/COMMAND` headline | real capture (`image`) or source video (`video`) |
| A `peak`, A `start` | `PROMPT 0n` chip | prompt card, verbatim |
| A `use`, D `day` | the result word | `chart` from real numbers, or a capture |
| `cta` | `OUTRO` chip; headline = the KEYWORD (no slash, `headSize` ≤ 240 so it clears the FIG rule); body "Comment KEYWORD and I'll send you {deliverable}." | ink prompt card as the deliverable stub: tag `IN YOUR DMS`, its first 3 real lines, "+ N more" |

Write apostrophes in `slides[]` strings as ’ (or escape them): a bare `'` inside a single-quoted JS string breaks the page.

## FIG SYSTEM

Drawing system: a precise engineering drawing in 30° isometric projection on pure flat white paper (#FFFFFF): no
grain, no grid, no paper texture, no vignette, no shading, no gradients, no drop shadows. Line art only. Outlines in
ink (#0E0E0E), one even stroke weight (about 0.4% of the image width); hidden edges and alignment lines as thinner
dashed ink hairlines. Exactly one part is the highlight: its outline in orange (#D9551F) with light 45° orange
hatching; every other part is ink outline with white faces. Numbered balloons: small circles with a thin ink outline
and ONE digit inside in a bold monospace, each joined to its part by one straight thin ink leader line ending in a
small dot on the part. The balloons are the only marks that are not drawing.

Objects: simple solid stand-ins for the deck's parts (a stack of blank cards, a tray, a chain link, a box, a gear, a
funnel, a key), never screens with UI, logos, letters, people or creatures. The highlight is the part the slide is
about (the cover: the part the hook leans on).

Hygiene: no words, letters, labels, captions, titles, dimensions, measurements, logos, signatures, handles or
watermarks anywhere; no text on any part; no colour other than ink, orange and white. Render only the balloon digits
quoted, each exactly once. Never render these instructions as text.

## FIG COVER

One landscape image, 3:2 (1536 × 1024). An exploded view of the deck's {N} parts (N ≤ 5), floating apart along one
dashed alignment line with equal gaps, drawn large so the whole drawing fills the frame with about 5% white margin:
{part 1} … {part N}, one of them the highlight. Balloons "1" … "{N}" in one tidy column beside the parts (or one row
above them), numbered in build order. The kit contain-fits the whole plate into a 920 × 474 box, so the drawing may
use the full height; a vertical stack is fine.

## FIG INTERIOR

One landscape image, 3:2 (1536 × 1024). One mechanism, left to right on one dashed alignment line: {part 1} → {part 2}
→ {part 3} (2–4 parts), {highlight part} the highlight. Balloons "1" … "{N}" in one row ABOVE the parts, each leader
dropping straight down. The whole drawing, balloons included, sits inside a centred horizontal band 2.2 times as
wide as it is tall (the full width, the middle 66% of the height), the top and bottom 17% pure white: the template
shows it at 920 px wide with `maxH:470`, cropping that white.

## KEYING

FIG plates carry no key colours and are never composited: no magenta, purple, violet or pink anywhere; no cyan,
teal, turquoise or blue anywhere. If a deck needs a real logo beside a drawing, it goes into the HTML (an `<img>` in
the sheet or a capture in another hero), never into the plate.

## Make (Claude only)

1. Copy `templates/03-command-press/slides.html` to `$D/slides.html`, replace `slides[]` (delete the command and atlas
   samples; `engine/styles/kits/S10/slides-sample.js` is a filled example), fill from `strings[]`.
2. FIG plates: `$D/prompts/fig-NN.txt` = FIG SYSTEM + FIG COVER or FIG INTERIOR + KEYING, filled; one jobs file
   (`refs: []`, or `[plates/fig-0.png]` once FIG.0 is approved); `node shared/codex-img.mjs gen $D/jobs-figs.json`.
   QA each plate: digits 1..N once each, no stray letters, one orange part, white ground. A stray letter is an edit
   job ("remove the letters, keep everything else"), never a pass.
3. Cover: copy `engine/styles/kits/S10/{cover.html,kit.css,kit.js}` into `$D/`, set the JSON (`fig.src` →
   `plates/fig-00.png`), render to `$D/cover.png` (exit 2 names the broken copy limit).
4. Cards: `kits/S10/prompt-NN.html` per peak / start / CTA sheet, rendered into `$D/assets/`.
5. `node shared/export.mjs --carousel <id>` (exit 2: an image failed to load).
