# S08 Bone Editorial: prompt block

An editorial notebook page: grained kraft-cream paper, a two-line Didone headline with one accent
colour, a taped handwritten sticky top-right, ruled tables, dark app panes and loose ink doodles.
Refs: `engine/styles/refs/s08-ref-what.png` (a "what" page) and `s08-ref-parts.png` (a "model"
table page); the exemplars are the same two pages. **Hybrid**: Codex paints only text-free paper,
once per deck (the fitted ground in the kit is reusable across decks); every word, table, sticky line
and mantra is HTML; captures, logos and an optional mascot are composited. That keeps small type and
the handwritten sticky crisp: a fully painted page blurs the one and garbles the other.

Kit: `engine/styles/kits/S08/` (its README has the commands). Sample pages with placeholder copy:
`kits/S08/cards/page-01.html` (what), `page-02.html` (model), `page-03.html` (why), rendered to
`kits/S08/samples/`.

## Production split

| Element | Made by |
|---|---|
| Ground: kraft paper, header rule, top-left star, BLANK taped sticky top-right, footer lightning + crown | **Codex**, one plate per deck or reuse `kits/S08/fitted/ground.png` (prompt `kits/S08/prompts/ground.txt`). Plates come back 3:4: fit to 1080x1350 by scaling to the height and mirroring 28 px of plain paper on each side (kit README) |
| Doodles (bulb, arrows, stars, checkbox, loop, gear, folder, clock, magnifier, bubble) | **Codex** doodle sheet once (`prompts/doodles.txt`), cut into `kits/S08/doodles/*.png`, placed as `<img class="dd">` |
| Headline, sticky text, body, tables, rows, notes, mantra, header, counter | **HTML**: `cards/page-NN.html` + `cards/s08.css`, rendered with `node shared/render-card.mjs … --w 1080 --h 1350 --scale 1 --min-px 20` |
| Real captures | `shared/shots.py` crops in a dark `.pane` (app window) or a taped `.card` (light pages) |
| Icons in tables, rows and strips | Lucide via `node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards` |
| Mascot (optional) | your own mascot, if you have one (never a licensed character): a transparent PNG pose as `<img class="mascot">`, on the CTA or on one slide where the pose comments on that slide's content; never painted. Leave it out entirely if you have none |
| Logos | real files as `<img>`; never painted |

## Tokens (`s08.css`)

Paper #EEE4D2 (sticky #F5ECDA), ink #1A1A1A, secondary ink #3A3631, accent = one colour taken from
the subject (the kit default is orange #D9551F; cobalt #3D7DC8 also works well), dark pane #15171A.
Fonts: Playfair Display 800 (Didone headline, 112 px, fitted down to a 76 px floor, one line per
line), Inter 400/700 (statements, table names), IBM Plex Mono 500–700 (body, tables, header, mantra),
Kalam 700 (sticky and margin notes, uppercase). Header: deck label left (e.g. `{{BRAND}} · topic`)
and `NN / TT` right, above the painted rule. Mantra footer: three short phrases with the
middle-to-last word hand-circled, between the painted bolt and crown (the samples use
"ONE INBOX. EVERY TASK. (ZERO) TABS."); keep the same mantra on every page of a deck.

## Plate prompts (paste to Codex)

### GROUND

Use `kits/S08/prompts/ground.txt` verbatim (attach the two s08 refs). It asks for grained kraft cream
with fibre, a thin header rule at 4.6% of the height, a small outline star top-left, one blank cream
sticky (about 25% x 14%, centred near x 81% y 15%, rotated +5°, masking-tape strip, torn bottom edge),
a lightning bolt bottom-left and a crown bottom-right at 96%, and nothing else: no text, letters,
numbers, icons, colour or characters. After fitting, measure the marks (kit README) and align
`.hdr`, `.sticky` and `.mantra` if a new plate drifts.

### DOODLES

Use `kits/S08/prompts/doodles.txt` verbatim: twelve outline ink doodles in a 4 x 3 grid on the same
paper, generous spacing, no text or colour. Cut each one out onto a transparent PNG.

## INTERIOR layouts (HTML)

Every interior: header, the two-line headline (`.head`: line 1 ink + line 2 accent with a hand
underline; `.head.step` flips the colours for step and action slides), sticky (≤ 4 short handwritten
lines, ≤ 8 words), one body block in `.zone`, optional margin note and 1–3 doodles, mantra.

- **what**: 3–4 `.say` statements (44 px) with one hand-circled word (`.loop`), one underline (`.u`) and
  one highlight (`.hi`), then a 4-box `.strip` of icon + verb previewing the flow. No component names
  yet. Sample: `page-01.html`.
- **why**: `.rows` old way / new way (circle icon + mono line, dashed separators), then a `.pane`
  capture. Sample: `page-03.html` (an HTML stand-in sits in the pane; use a real capture on a deck).
- **model**: a ruled `.tbl` "Part | What it does", ≤ 4 rows, icon tiles, plus one margin note.
  Sample: `page-02.html`.
- **how / compare**: a 3-column `.tbl` (blank | A | B), then a small `.pane` with a handwritten note.
- **use (proof)**: a mono 2-line summary with accent words, then a large `.pane` capture with a tag.
- **peak / settings**: a ruled `.tbl` "Setting | Set it to", key value in accent bold, a note that
  defines any jargon (e.g. "Opus = Claude's top model").
- **start**: `.rows` steps with the URL or command, then a taped `.card` capture.
- **cta**: headline "Comment / KEYWORD" (keyword in accent), one `.say` deliverable line, a `.composer`
  showing the keyword, a 3-box `.strip` of what they get, optionally your own mascot pose.

Budgets: headline lines ≤ 14 characters each at 112 px (the fit pass shrinks to 76 px, never below);
`.say` ≤ 45 words total; tables ≤ 4 rows, ≤ 12 words per cell; `.zone` overflow exits 2 (cut copy,
never shrink the floor).

## Pitfalls

- The cover is not part of this block: decks may keep their own cover (an HTML cover or a cover from
  another style). If S08 covers are wanted, add a COVER section after a test.
- It is an easy look to lean on: respect the 14-day cooldown so the feed does not go monotone.
- Keep doodles off text: place them in margins (x < 110 or x > 900), in the gap between the headline
  and the sticky, or in the empty band above the footer, and let QA check collisions.
- Captures never crop: size the `.pane` or `.card` box to the capture's aspect (`object-fit: contain`).
