# S19 Window-Chrome Build Diary: prompt block

A build diary told inside an app window. The layout was studied from a high-performing carousel;
only its layout vocabulary carries over: an app window as the frame, bleeding off the right and
bottom; artboards on a grey canvas with pieces breaking out over their edges and the chrome; a raw →
refined process row; flat tinted caption pages between. Never copy any reference deck's characters,
art, words, hook, CTA phrasing, item set or signature palette, and never its app's UI: no third-party
design-app toolbars or invented product chrome. Palette rules for this style: caption pages are
apricot #F5C9A0 or cream #F5EBE0 with rust #7A2C14 type, never pink or maroon.

**Hybrid, mostly HTML.** Chrome slides and all type are HTML. Codex paints only cut-outs and
result-page scenes. **The template is `templates/08-window-chrome/`** (`recipe.md` has every field): a
deck copies its `slides.html` to `$D/slides.html`, fills `DECK` and `slides[]`, and bakes with
`node shared/export.mjs --carousel <id>` (exit 3 lists the template's `qa()` warnings: fix them and
bake again). No deck forks its own copy of the template's engine.
COVER and INTERIOR are template layouts, never pasted. Each Codex job
(`shared/codex-img.mjs`) gets SYSTEM, then CUT-OUT or SCENE (never both), then KEYING. Cover hooks
come from `engine/hooks.md`: F1 or F3 for spine D, F10 for spine A, never a reference deck's line.

## Production split

| Element | Made by |
|---|---|
| Window frame | For a deck about one app: a real 4:5 capture of its window (VS Code or Terminal for Claude Code; the real Cursor or n8n window), side panels closed, right and bottom cropped off, scrubbed (`shared/shots.py`); the canvas covers its editor rect. Otherwise the HTML kit below |
| Stage label, counter | HTML: in the kit's control bar, or two pills 16 px below a real frame's chrome (stage #2F2F2F with white text, top-left; counter top-right) |
| Canvas, all type | HTML: flat graphite, Instrument Serif + Inter (Google Fonts). Exact, so only the layout budgets limit length |
| Artboards | Real captures (`shared/shots.py`) cover-fit around a focus box, square corners, no border or shadow. Exact text (prompt, command, config, file tree, table): an HTML card, cream #F5EBE0, JetBrains Mono in ink. The orange selection box with square handles is HTML, never painted |
| Break-out layer | Real UI pieces cropped from that slide's own capture (scaled only), or exact-text pieces from `render-card.mjs` (transparent outside the card). Spot illustrations: Codex CUT-OUT, background removed (any background-removal tool, or a flood fill of the flat ground). Process-row result pieces are these cut-outs with a CSS contact shadow |
| Result-page scene | Codex SCENE plate, `composite.py --shot` / `--card` into its faces, full-bleed under HTML type |
| Logos | Real files only: inside a real frame or capture, on the canvas (simple-icons SVG), or in a SCENE cyan slot (`composite.py --logo`). Never in kit chrome |
| Your own mascot (optional) | Transparent PNG poses you made (never a licensed character) in the break-out layer, only when its pose comments on the slide. Never painted. With no mascot, leave it out |

**Z-order:** frame → canvas → type, artboards, cards, selection boxes → break-out layer. A break-out
piece may cover one outer corner or edge of an artboard (never its focus box), reach over the rail by
up to a quarter of its own width, and run to within 3% of the right and bottom edges. It never covers
type, the stage label, the counter or the active tab. Break-outs are on by default on the cover and
at least every other chrome slide. Each piece is an element visibly inside its artboard or a painted
object standing for that artboard's artifact, never a generic sticker.

**The frame is chrome, not proof.** It carries the stage, counter and real file names, never a claim:
no model pills, fake status or fake run results. PROVE lives in the artboards and real-UI cut-outs.

**Frame kit** (HTML, px at 1080 x 1350): your own window in generic IDE vocabulary, with no
third-party name, logo or setting anywhere in it.
- **Title bar, y 0–66,** #4A4A4A: traffic lights #FF5F57 / #FEBC2E / #28C840, 24 px, from x 24;
  right-aligned "{real repo or folder} — {{BRAND}}", Inter Medium 26 px #E6E6E6. No home glyph.
- **Control bar, y 66–127,** #4A4A4A, 1 px #393939 line above: left, the stage label or breadcrumb
  (at most 3 words), Inter Medium 30 px #F2F2F2; right, a #ECECEC pill (ink, Inter Medium 30 px)
  with an orange dot and "{NN} / {TT}". Nothing else.
- **Tab row, y 127–177,** #3F3F3F, Inter Medium 24 px: the active tab in canvas graphite with a 3 px
  #D9551F top line, an "×" and a real repo file name; one or two #A6A6A6 inactive tabs, the last cut
  off by the right edge.
- **Activity rail, x 0–96, y 270–1312,** #474747, 1 px #353535 outline, 8 px right-corner radius:
  40 px line icons #D6D6D6 at a 76 px pitch (files, search, branch, terminal, chat, run; at the foot,
  account, settings). The step's icon sits in a #2F2F2F cell with a 3 px #D9551F left bar. No
  collapse header, grip, fill/stroke squares, swatches or action button.
- **Canvas:** the rest, flat #575757, with no right or bottom window edge. Title and tab text are
  decorative (24–26 px); the stage label and counter are the readable chrome (30 px).

**Safe area (chrome slides):** text inside x 18%–82%, y 17%–95%; artboards and cards inside x 14%–86%,
clear of the rail. Only break-outs cross. If content does not fit, make it smaller.

## SYSTEM

Visual system: a flat vector spot illustration for a build diary told inside a desktop app. Soft
rounded forms with flat fills and no outlines; a fine stippled grain on the shaded side, like a
risograph or grain-brush texture; one small white glint inside the silhouette; slightly oversized and
playful, as if it escaped from the work.

Palette: Claude orange (#D9551F), apricot (#F5C9A0), cream (#F5EBE0), muted cornflower blue
(#7E9BD0), sage green (#7FA772), butter yellow (#F0C75E), and ink (#0E0E0E) for small details.
Flat, crisp and screen-native: no 3D render, no glossy shine, no gradients except soft studio light
in a scene.

Never draw people, faces, hands, animals, characters or mascots; letters, numbers, words, logos or
icons of real products; or interfaces. Every screen, window, page face or document is a keying zone
or stays blank.

References: do NOT copy any reference's characters, objects, art, packaging, colours or words.

Hygiene: this image has no text at all. No captions, labels, UI, lorem ipsum, watermarks, handles or
logos. Never render these instructions or section names as text.

## CUT-OUT

One spot illustration of {object}, standing for {its meaning on the slide}. It is alone and centred
and fills about 70% of a square image, on a perfectly flat, plain {graphite #575757 | apricot
#F5C9A0} ground. Nothing else is in the image: no cast shadow, floor, frame, second object or
sparkles. Every edge is crisp against the ground, and the grain stays inside the silhouette.

## SCENE

A quiet studio still life on a full-bleed soft apricot (#F5C9A0) paper sweep, evenly lit from the
upper left, with no texture, grain or colour cast. The top quarter is plain flat apricot with nothing
in it. The hero is {an open laptop | a standing phone | printed pages standing or fanned}, square to
the camera, centred between 25% and 92% of the height. Devices have plain graphite or silver-grey
bodies with no logos, marks or text. Contact shadows are soft, warm amber and grey-brown, never pink
or salmon. Each screen and page face is a keying zone (see KEYING): it emits no light, has no glow or
reflection, and casts no colour onto the backdrop. Empty margins: at least 8% of the width left and
right, 7% at the bottom.

## COVER

Template layout, a chrome slide. Frame: stage label "{stage}", counter "01 / {TT}".
- **Headline:** "{hook}", centred, two lines of Instrument Serif, white, 92 px, line-height 0.98, top
  at about 14.5%. Only the words "{accent}" take the italic cut.
- **Subtitle:** "{subtitle}", one line, white, 46 px (about 1/29), ending by about 33%.
- **Artboards:** a 2 x 2 grid of finished outputs at {W:H}, cell width derived from the aspect,
  inside 34%–92% of the height. 4:5 slides: 300 x 375 cells, 24 px gutter, a 624 x 774 grid at
  x 228–852, y 462–1236. Desktop screens: one 16:10 artboard, 624 wide, over two portrait cells.
- **Break-outs, 3–5:** spine D, the N parts as painted CUT-OUT icons, one job each (the cover
  contract's "N parts as icons"); spine A, real UI cut-outs from the grid's captures. One large piece
  over the top-right artboard's outer corner, toward the right edge; one crossing a lower artboard's
  bottom edge, down to about 3% from the bottom; one reaching over the rail; the rest small, drifting
  on the grey.
- **Mascot (optional):** your own mascot's PNG pose, only when it comments on the cover, e.g.
  dragging a finished slide out of the grid.

Codex jobs: none for spine A; N CUT-OUTs on graphite for spine D.

## INTERIOR

Template slide kinds. "{…}" are slots. Text marked "(example)" is a planning note, never rendered.

**Stage slide** (D `step`; A `how`, `start`), chrome:
- Heading "{heading}", 6 words or fewer, lowercase, Instrument Serif 72 px (about 1/19), centred, top
  at about 18%. Stage label "Step {k} · {name}".
- One artboard at {W:H}, about 62% of the width, centred, ending above 84% of the height; or two side
  by side (the real panel and an exact-text card), together at most 72% of the width, 24 px gutter.
- Caption "{caption}", one line, 12 words or fewer, lowercase, 40 px (about 1/34), under the
  artboards.
- 1–3 break-outs.

**Process row** (D `why`, or a `step` that turns X into Y; A `why`), chrome:
- Top row, 18%–47%: two or three raw-input captures of different heights, bottom-aligned at 47%,
  together at most 72% of the width (example: a rough prompt, a transcript, a whiteboard photo, a
  first draft). Raw label "{raw label}", 4 words or fewer, lowercase serif 40 px, above the left one.
- Heading "{from X to Y}" (example: from transcript to storyboard), 72 px, centred at about 52%.
- Bottom band, 60%–82%: three or four real-result cut-outs, no artboards. Stagger their heights,
  rotate each by at most 4°, give each a soft contact shadow. Optionally two or three tiny painted
  sparks or scraps.
- Caption "{caption}" at about 86%.

**Result page** (D `what`, `day`; A `what`, `use`), apricot:
- Sentence "{sentence}", 30 words or fewer, rust Instrument Serif 48 px, line-height 0.95, centred,
  2–3 lines, top at 9%.
- Hero, 25%–92%: the composited SCENE plate as the full-bleed background, or one large HTML artboard
  with a soft warm shadow.
- Footer.

**Zoom page** (a `step` or `use` detail), cream:
- Sentence, 20 words or fewer, rust, 52 px (about 1/27 per line), centred, top at 9%.
- One 2:3 artboard, 605 x 907 px (56% of the width), centred, 24%–91% of the height, holding a
  cropped real UI panel with its HTML selection box.
- Footer.

**Other kinds, one line each:**
- **Parts row** (D `parts`; A `model`), chrome: "{heading}"; the cover's painted icons (D) or up to 4
  named parts (A) as cut-outs in a loose row at 40%–75%, each labelled "{part}: {8 words or fewer}"
  in lowercase serif 40 px. EXPLAIN only: no captures, no claims.
- **Command slide** (A `peak`; a D `step` whose payload is a prompt or command), chrome: one
  exact-text card at its own aspect, at most 70% of the width inside the 14% margins; one painted
  piece off its top-right corner (a paper plane); one caption line under it.
- **CTA page** (`cta`), apricot: "Comment {KEYWORD}" in rust serif at about 110 px, only the keyword
  italic; "{what they get}" on the next line at sentence size; a hero CUT-OUT of the deliverable on
  apricot (a tied bundle of pages, a folder or a parcel) on an HTML contact shadow, or your own mascot
  (optional) when its pose hands the deliverable over; footer.

**Footer (caption pages):** "{{BRAND}}" left, "{NN} / {TT}" right, 4% from the bottom, Inter Medium
30 px caps, 0.12em letter spacing, rust. Caption-page margins: at least 8% of the width left and
right, 7% of the height top and bottom.

**Readability:** nothing readable is under 30 px (about 1/45) except the decorative title and tab
text. Headlines are at least 1/20 of the slide height.

## KEYING

In a SCENE plate, each screen or page face is ONE solid flat magenta #FF00FF rectangle of aspect
{W:H} with square corners: pure uniform magenta edge to edge, perfectly flat and frontal, no
perspective, gradient, texture, glow, reflection, text, UI or border. Faces keep at least 3% of the
width between them, and nothing overlaps a face.
A logo slot, when asked for, is ONE solid flat cyan #00FFFF rounded square about {size} wide: no
text, outline or shadow, with clear backdrop around it.
No pink, rose, salmon, purple, violet, lavender or magenta anywhere except a key zone. Apricot is a
pale, yellow-leaning orange, never pink, with warm amber or grey-brown shadows. No cyan, turquoise or
teal anywhere except a logo slot; blue stays the muted #7E9BD0, at least 3% of the width from any
cyan slot. No iridescent or rainbow sheen.

## Authoring notes

- **References.** CUT-OUT: none on the first job, then the user's first approved cut-out as Image 1.
  SCENE: `engine/styles/refs/s19-scene-layout.png` as Image 1 (an HTML wireframe from
  `refs/src/s19-scene-layout.html`: apricot page, empty top quarter, plain grey laptop with one flat
  magenta 16:10 screen, 736 x 460 at 172,542) until a result page is locked, then that page. Never attach
  another creator's slides (their palette and art leak) or a rendered frame (it invites painted UI).
- **Before compositing a SCENE,** run `composite.py --zones-only` and check the zone count.
- **CUT-OUT grounds** match the destination, so removal fringe disappears. Objects that fit: a
  magnifier (research), blank index cards (memory, storyboard), a fan of plain colour-swatch cards
  (style pick), a paintbrush (image generation), a film strip (video), a toolbox (skills), a paper
  plane (publishing, sending a prompt), a tied bundle of pages, folder or parcel (a deliverable).
  Sparks and paper scraps are their own small CUT-OUT jobs, reused across the deck.
