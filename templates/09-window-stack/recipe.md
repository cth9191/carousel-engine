# Template 09 — Window Stack

The html-native build of style **S21 Circled-Count Tip Stack** (`engine/styles/S21-circled-count-tip-stack.prompt.md`).
A flat cream desktop-notes page. The cover is a lowercase count hook with the number hand-circled in Claude orange,
an ink folder spilling window cards, and a payoff line. Interiors are white app windows (fixed height per layout)
with a mono counter and a marker arrow. Every word is HTML; captures, logos and the avatar are `<img>`s; the ellipse,
strike and arrow are SVG paths. Codex paints nothing unless a topic container replaces the folder (see Hero).

## When to use

- "I read / ran / tested N" findings listicles from a corpus you actually went through (the declared Spine C
  variant: three numbered windows per stack slide, at most 3 stack slides, M counts windows 01–M, not slides).
- One tool, repo or skill per slide in a proof window; an exact prompt or config in a terminal window.
- Not for diagrams or head-to-heads.

## Layouts (`layout` in each `slides[]` entry)

| layout | fields | what renders |
|---|---|---|
| `cover` | `hook:[line1, line2]`, `circle`, `hero`, `payoff` | byline (avatar circle, `DECK.name`, role) · hook auto-fit to 840 px (max 128) with `circle` ringed · hero 840×490 at y 520 · payoff 54 px · counter + arrow on y 1276 |
| `stack` | `headline`, `range`, `items:[{n, tip, caption}] ×3` | headline 48 px with one `*accent*`, item range right-aligned · windows 840×252 at y 200/556/912, item number in the bar · a caption under each |
| `proof` | `tip`, `label`, `logo`, `shot:{src, focus, fit, bg}`, `caption:[1–2]` | 56 px tip line · one 840×742 window, the item's exact name in mono after the dots, optional logo at the bar's right · capture cropped to the focus box (dark captures: `fit:'contain'`, `bg` = edge colour) |
| `terminal` | `tip`, `label`, `code`, `caption:[1–2]` | same window with an ink body; `code` in cream JetBrains Mono (28 px, shrinks to fit); lines starting `$ ` or `> ` get an orange prompt |
| `beforeAfter` | `tip`, `before:{tip, caption}`, `after:{tip, caption}` | two 840×330 windows labelled `before` / `after`; the before tip muted #8A8178 under an orange marker strike |
| `cta` | `tip` (optional), `keyword`, `caption` | one 840×420 window: "comment" / KEYWORD ringed; the caption is the deliverable. No arrow on the last slide |

- **Markup:** `|` is a hard line break; without it the browser wraps (balanced). `*word*` is the slide's one orange accent. Identifiers keep their real case (CLAUDE.md, /compact).
- **Byline:** `DECK = { name:'{{BRAND}}', role:'…', avatar:'assets/avatar.png' }`. Your square profile photo or your brand mark, never painted. `avatar:null` shows a neutral warm-grey circle (samples only).
- **Sample copy:** the shipped `slides[]` is placeholder copy; its corpus and counts are not a real study.
- **Counter:** `NN / TT` from the slide order: top-left on interiors, bottom-left on the cover.

## Hero

- `{ type:'folder', tone:'ink' | 'kraft', logo:'assets/x.png', fragments:[…] }`: HTML/SVG folder (back + tab, six fanned
  window cards, front panel). The cards carry the deck's own tip fragments, taken from the stack slides when
  `fragments` is omitted; the front panel clips them. `logo` sits centred on the front (real logo files only).
- `{ type:'image', src:'assets/hero.png' }`: a topic container (box, terminal) from a Codex hero plate cut out to alpha
  first (flood-fill the cream from the corners, or remove_background), contain-fitted in 840×490.
- Mascot (optional): your own mascot (transparent PNG poses you made, never a licensed character) can be added as
  an `<img>` sitting on the card heap or peeking out of the folder. Never painted. With no mascot, the folder stands alone.

## Fit pass (the card's limits are enforced)

Tips 64 px (≤ 2 lines in 746 px, floor 60) · stack headline 48 px on one line beside the range (floor 45) · tip lines
56 px (floor 46) · captions 34 px on one line in 840 px (34 is the floor) · hook max 128 (floor 64) · payoff 54 (floor 48)
· terminal 28 (floor 22) · CTA keyword 96 (floor 64, ellipse inside the body). Copy limits checked on every render:
headline and tip lines ≤ 7 words, window tips ≤ 6 words, captions ≤ 46 characters, ≤ 3 windows per stack, ≤ 3 stack
slides. A broken limit puts a **red FIT/COPY banner across the top of the slide**, in the browser and in the export,
plus `console.error` and `window.fitReport`. `export.mjs` writes every slide and then exits 3, naming each failure: a
banner means rewrite, never ship.

## Workflow

1. `mkdir carousels/<id>/assets`; copy `templates/09-window-stack/slides.html` into `carousels/<id>/`.
2. Put the avatar (optional), logos and captures (`shared/shots.py`, focus boxes from `shots.json`) in `assets/`.
3. Edit `DECK` and `slides[]` from `storyboard.json` (`strings[]`). Captions: "{why} · in {k} of {N}".
4. `Invoke-Item carousels/<id>/slides.html` → tweak (⚙) → 📋 Export → paste JSON → update `slides[]`.
5. `node shared/export.mjs --carousel <id>` → `exports/slide-NN-YYYY-MM-DD.png` (exit 2 = an image didn't load,
   exit 3 = a FIT/COPY failure). Look at every slide.

## Pitfalls

- No blue folder (its blues pass composite.py's cyan key test), no red accent, no creator photo; orange only on the
  arrow, the ellipse, the strike and one accent per slide.
- Proof captures are real (shots.py), verified on posting day; an empty proof window shows "capture slot · 826 × 683".
- Re-sync localStorage tweaks into `slides[]` before baking, as in every template.
