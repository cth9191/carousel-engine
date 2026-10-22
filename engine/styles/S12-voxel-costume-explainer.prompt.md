# S12 Voxel Costume Explainer: prompt block

A bright explainer page: a near-white ground, a step tag, a bold sans headline whose second line is orange, real
captures side by side in browser frames, a speech bubble, icon rows, and one cutout per slide standing on a feet
line: your own mascot in a costume that comments on that slide, or, with no mascot, the subject's real logo on a
tile. A layout studied from a high-performing carousel; only its layout vocabulary carries over. Never copy any
reference deck's characters, art, stickers, words, hook, CTA phrasing, item set or signature palette.

**Hybrid, mostly HTML.** Every word, frame, icon and bubble is an HTML page from `engine/styles/kits/S12/`.
Captures are real. Codex never paints a slide, so slides take no layout refs and no key zones. Codex makes only
cutouts on flat grey, cut with `shared/pose-check.py cut`: optional **set pieces** (one voxel object: a laptop, an
old machine, a microwave) and, if you have a mascot, its **costume poses** (COSTUME below).

The mascot is optional and always yours: transparent PNG poses you made, never a licensed character, never
drawn into a slide by a model. With no mascot, every pose slot takes the subject's real logo on a square tile
(`<img class="pose tile">`), or is deleted; the bubble then speaks for the viewer, or goes.

## Production split

| Element | Made by |
|---|---|
| Every word, tag, counter, bubble, icon row, pill, code card, keyword box | `kits/S12/cards/page-NN.html` copies in `$D/cards/` → `node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22` |
| Captures | Real screenshots (your browser tool, `shots.py` for video frames, faces scrubbed) in `$D/shots/`, shown in `.win` frames: two side by side on a split page, one wide on a single page. A mock is EXPLAIN only, never shown as proof |
| Your mascot (optional) | One costume pose per slide from your own pose folder, copied to `$D/mascot/` and placed with `<img class="pose" data-x data-feet data-w data-feet-y>`. Missing costume → COSTUME below, before any page |
| No mascot | The subject's real logo (your logo folder, or simple-icons rendered to PNG) as `<img class="pose tile">` on the same feet line, or no slot at all |
| Set pieces | Optional, at most one per slide: SET PIECE job → `python -I shared/pose-check.py cut plates/set-x.png $D/sets/x.png` → `<img class="set">` |
| Icons | `node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards` |

Order: costume poses and set pieces (only what's missing) → captures → pages → render → QA.
Copy budgets: headline ≤ 7 words on 1-2 lines (line 2 is the orange one and ends with a period); body ≤ 30
words; a bubble ≤ 4 words, one line (the page throws past that); rows ≤ 3, each ≤ 14 words; one code card
≤ 6 lines. Counter `NN / TT` lives in the step tag.

## SYSTEM

The voxel world every Codex job in this style shares (set pieces and costume poses; never a slide). Paste it
after the job's own first paragraph.

> Matte printed-plastic voxel finish: every shape is built from the same small cube units as Image 1, with
> crisp cube edges, flat front faces, tops a little lighter and sides a little darker. View: from the front,
> turned about 20 degrees to the left, no camera tilt from above. Soft even light from the top left. Ground: one
> pure flat uniform mid-grey (#8C8C8C) from edge to edge: no floor, horizon, gradient, vignette, shadow, contact
> shadow or reflection. Colours: a character keeps exactly its own colours from Image 1; props, costumes and set
> pieces in graphite (#2A2A2A), brass (#E3A92B), bone (#E4D9C6) and orange (#D9551F) as a thin edge or a single
> detail. No purple, pink, magenta, cyan, turquoise, blue or green anywhere (unless they are the character's own
> colours); no text, letters, numbers, logos or UI on anything; no glow.

## COVER

Page `page-01.html` (layout `cover`): the step tag reads `01 / TT` plus a plain topic label; four outline dots
top right with the last one orange; the hook as a 2-3 line headline at 112-150 px, the last line orange; a white
promise card with an ink outline and a soft orange offset (one sentence, ≤ 9 words, one orange phrase); below
it, the cover pose (your mascot, at about 46-50% of the width) or the subject's logo tile (about 30%) on the
right, an optional set piece on the left, both standing on one feet line at y 1262 over soft contact shadows;
one bubble (≤ 4 words, a reaction to the hook, never the hook again); two small four-point sparks. With a
mascot, the cover costume is the deck's most telling one (the job the deck teaches) and is never reused inside.

## INTERIOR

Pages by spine A role (spine D's `step` uses the split page; the kit's four pages are the layouts, its CSS holds
every component). The costume named per role applies only with a mascot; without one, the slot is the logo tile
or nothing.

- **what / why** (`page-02.html`): headline, body (≤ 30 words, one bold phrase), the pose and an optional set
  piece across the lower half, one bubble voicing the viewer's objection ("Wait, what broke?"), and an old-way
  pill at the foot. Costume: the confused or searching one (detective hat + magnifier).
- **model** (`page-03.html` with one capture or an EXPLAIN mock wide across 390-810): headline, ≤ 4 named
  parts as rows. Costume: graduation cap + book.
- **how / step** (`page-03.html`): step tag `Step N: <action>`, headline "Step N:" / "<action>." in orange,
  two real captures side by side (before / after, or input / result) with a 22 px caption chip each, the pose
  lower left with a mono bubble carrying the one command or slash command, 2-3 icon rows on the right. Costume:
  the job of that step (hard hat for setup, chef hat for a recipe, headphones for a video).
- **peak**: the split page with the captures replaced by one `.code` card (the prompt, command or config,
  verbatim, ≤ 6 lines, orange mono label). Costume: a proud one (holding a clipboard with a check mark).
- **use**: 2-3 rows of real results, one capture.
- **start**: one capture of the install or first run plus a `.code` card. Costume: hard hat + wrench.
- **cta** (`page-04.html`): centred headline ("Want my" / "exact X?"), the orange-outlined keyword box
  `Comment KEYWORD` (the keyword exactly once), one line naming the deliverable, a final pose or the logo tile.

With a mascot: one costume per slide, each used once per deck; adjacent slides never share a headwear.

## COSTUME (only with a mascot; one Codex job per missing pose)

Image 1 is your mascot's canonical sprite on the flat grey (your own character, never a licensed one); Image 2,
once you have one, a pose of it you have already approved. Prompt: "Image 1 is the character to keep exactly:
the same shape, proportions, colours, face and finish. Change only the costume piece on its head and, at most,
one held prop and the one arm or limb that holds it." Then SYSTEM, then this paragraph, then one Prop sentence
("Prop: {object}, held in the {left | right} hand, its own colours from SYSTEM." or "No prop: the arms stay as
in Image 1."), then the framing line: "Framing: a square image, the figure, its costume and its prop centred at
about 60% of the width, whole and uncropped, wide empty margins."

> Costume: {headwear}, built in the same finish as the character (the same cube units, for a voxel
> character), resting on top of the head like a lid. It sits entirely above the head's top edge: the
> character's own top edge stays visible between the costume and the eyes, and the body keeps its exact size
> and proportions. It is at most {W} units wide and overhangs the top by at most 1 unit at the front and the
> sides; it covers no part of the face and no eye. Colours: {graphite | brass | bone}, with at most a thin
> orange band; never the character's own main colour.

Headwear lines (say the shape in units, never just the name):
- hard hat: a brass dome stepped from cube units, 8 units wide and 2 tall, with a short 1-unit visor at the
  front only, no brim at the sides or back, one graphite band at its base.
- detective hat: a graphite deerstalker 9 units wide and 2 tall, a bone band, short front and back peaks.
- chef hat: a bone toque 8 units wide and 4 tall, three rounded puffs at the top, a graphite band.
- headphones: a graphite band 1 unit thick arching from one side of the top to the other, a brass cup 2 x 2
  units against each side of the head at eye height, below the top edge and clear of the eyes.
- graduation cap: a graphite mortarboard 10 units square and 1 thick on a 6-unit cap, one brass tassel.

Check: `python -I shared/pose-check.py cut` the plate. If your mascot fits the check's shape (the script's
header names the constants to tune), run `grade` and then `check --sprite <your sprite> --prop <held prop box>`
(pass `--prop` whenever there is a held prop: the automatic box spans hat and prop together and can mask the
eyes); otherwise compare the cutout with the sprite by eye. Look at it on near-white and on ink before you keep
it. At most 3 re-rolls, then simplify the headwear (a cap before a hat with a brim). A brim that sinks over the
top edge makes the body read squat: that is why the paragraph demands the visible top edge.

## SET PIECE (optional; one Codex job each)

Image 1 = `engine/styles/refs/s12-ref-set.png` (an approved voxel laptop on the flat grey, for scale, cube size
and finish). Prompt: "Image 1 shows only the voxel finish, cube size, light, view angle and flat grey ground to
match: ignore the laptop itself and do not draw it. Build ONE object as a voxel model from the same small cube
units: {object, with its colours and a screen or face that is one plain dark panel}. About {N} units wide." +
SYSTEM + "Framing: a square image, the object centred at about 60% of the width, wide empty margins, no
character, creature, mascot or hands." Cut with `pose-check.py cut` (no grade, no check); look at it on
near-white. A screen is never a key zone: real UI goes in a `.win` frame beside it.

## KEYING

No key colours on slides: every page is HTML on a flat near-white #FAF9F7 ground. Cutout jobs key their flat
#8C8C8C ground with `pose-check.py cut`, which is why SYSTEM bans grey-adjacent shadows and floors. A cutout
that keeps a grey halo goes back through `cut` with `--pad 0`, never a hand-paint.

## Notes

- The kit's laptop (`kits/S12/sets/laptop.png`) cut cleanly from its first plate and is reusable.
- The four sample pages show a dashed box where the mascot goes; the layout is proven, and the first deck with a
  mascot builds and checks its first costume before any page.
- Near-white with orange headlines: keep an S12 deck 14 days from another near-white, orange-accent deck by hand.
