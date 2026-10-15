# Style library

Every visual style a deck can use. A style is three things: two exemplar images, a prompt block, and
an entry in `styles.json`. Picking a style takes **zero image generations**: the pick sheet is built
from the exemplars.

| File | What it is |
|---|---|
| `styles.json` | The catalog: one entry per style id. Name, one-liner, status, production type, spine fit, attributes, cooldown, exemplar paths, requirements, template. |
| `<id>-<slug>.prompt.md` | The style's prompt block: the SYSTEM text pasted into every Codex image prompt, the COVER / INTERIOR layouts, and the KEYING rules for magenta (capture) and cyan (logo) zones. |
| `exemplars/` | One cover and one interior per style (`<id>-cover`, `<id>-interior`), 4:5. They're the art on the pick sheet and the style references attached to a deck's first prompts. |
| `gallery.jpg` | The pick sheet: one tile per style. Built by `shared/build-gallery.mjs` (see below). |

Two placeholders appear in prompt blocks, in `styles.json` and in a deck's copy of an HTML template.
`{{BRAND}}` is the `brand` in `engine/brand.json`; the skill asks for it before your first deck if
it's still `YOUR BRAND`. `{{MONTH_YEAR}}` is the month and year of the deck folder's date, e.g.
`OCTOBER ©2026`. The skill fills both in when it writes prompts and when it copies a template into a
deck.

## The four styles

| Id | Name | Looks like | Spines | Production |
|---|---|---|---|---|
| S01 | Terracotta Zine | Terracotta texture, massive lowercase headline with a period, taped dark app windows | D system build, A explainer | html-native |
| S02 | Logo Equation | Terracotta, giant white "Tool A + Tool B", two big app-icon tiles joined by a plus | A explainer: tool combos, integrations, set-up tutorials | hybrid |
| S03 | Newsprint Benchmark | Warm newsprint, Didone italic, diagonal VS split with huge percentages, ruled tables, green verdict bar | B head-to-head / launch test | image-native |
| S11 | Sketchnote Diagram Explainer | Cream, heavy grotesk with a yellow highlighter pill, pastel flow-diagram boxes, hand-drawn arrows | A explainer for cold viewers | image-native |

How each one gets made:

- **S01**: Codex paints only the cover plate. Interiors come from the deck's copy of
  `templates/02-terracotta-zine/slides.html` (`{{BRAND}}` and `{{MONTH_YEAR}}` filled in, the
  template's `assets/` copied to the deck's `assets/`), baked with
  `node shared/export.mjs --carousel <id>`. Needs real terminal or dashboard captures for its windows.
- **S02**: a hybrid. Codex paints the plate and short type; real logos go in through cyan zones,
  captures through magenta, exact text as HTML cards. There is no HTML template for it yet. Needs
  real logos (your logo folder, or simple-icons), never generated marks.
- **S03**: Codex paints every slide. Captures and logos are composited in. Every number is verified,
  and long tables, charts and code are HTML cards.
- **S11**: Codex paints every slide, diagrams included. Real captures go into magenta zones, and exact
  text (a prompt, a command) is an HTML card from `shared/render-card.mjs`. Its exemplars are the
  cover and slide 4 of this repo's worked example, `carousels/2026-10-14-claude-video-free`.

## Reading a tile

```
S01  Terracotta Zine                          <- id + name (id colour = status)
spine D System build · A Explainer            <- or, once you sync a post log: N uses · median Mx · best Bx · last MM-DD
[CARD v1]  html-native   no posts logged      <- status, production, availability
COVER                        INTERIOR · slide 2
[ cover art ]                [ interior art ]
```

- **Status**: `card-v1` means the style has a prompt block and can go to Make. All four styles here
  are `card-v1`. The script also accepts `next-wave` (worked for you, no prompt block yet),
  `test-wave` (seen only on other accounts) and `retired` (hidden unless `--include-retired`).
- **Production**: `html-native` means Playwright renders the exact text and AI paints at most the
  illustration plates. `image-native` means AI paints the slide and real assets get composited in.
  `hybrid` means Codex paints the plate and short type; real logos go in through cyan zones,
  captures through magenta, exact text as HTML cards.
- **Availability**: `no posts logged`, `rested Nd`, or `cooling until MM-DD` in orange (see Cooldown).

## How to pick

Reply with the number: **"S03"**. The brief card (`engine/templates/brief-card.md`) offers one
recommended style and one alternative, based on:

1. **Spine fit.** Each style lists the spines it suits (`formats.spines`: A explainer, B head-to-head,
   C listicle, D system build). S03 fits head-to-heads, S02 fits tool combos, S01 fits system builds
   and S11 fits explainers for viewers who've never heard of the tool.
2. **Cooldown.** See the next section.
3. **Requirements.** Check `requires` before picking. S01 needs real captures for its windows, S02
   needs real logos, and S03 needs verified numbers for its tables.

### Why median, not best

If you log your own posts, the tiles show uses, a median and a best. Showing only the best post is
selection on outcome. In the author's feed, most styles scored highest the first time and decayed
with repeats, so a style's best post mostly measures novelty and topic. Trust the median. With only
one or two uses, the median and the best are nearly the same number and tell you little: read those
as "barely tested".

## Cooldown

`cooldown_days` is 14 for every style. A style **posted** in the last 14 days shows
**"cooling until MM-DD"** in orange, and the skill won't recommend it unless you ask. Styles decay with
repetition: in the author's feed, a cover style that landed well the first time, then ran again and
again over a couple of weeks, ended well below a typical post. Unposted drafts don't start the clock,
but three drafts in a row in one style is overuse in the making (the tile counts drafts when your
synced post log has them). Within one format, the spine rule also applies: never post two
same-format decks within 72 hours. The shipped worked example
(`carousels/2026-10-14-claude-video-free`) doesn't count toward either clock.

The clock reads `stats.last_used` on each style. No style has stats yet. When you post a deck, add
`"stats": { "last_used": "YYYY-MM-DD" }` to its style, or keep a post log and let
`build-gallery.mjs --sync` fill it in.

## Build the pick sheet

```
node shared/build-gallery.mjs                          # every style -> engine/styles/gallery.jpg
node shared/build-gallery.mjs --only S03,S11 --out carousels/<deck>/style-pick.jpg
node shared/build-gallery.mjs --check                  # validate + print the table, render nothing
```

- `--only` renders just those tiles, recommended first. That's the crop the brief card sends. Without
  `--out` it writes `engine/styles/gallery-pick-<ids>.jpg`. The full sheet is left alone.
- Without `--only`, the full sheet goes to `engine/styles/gallery.jpg`, or to `--out FILE`.
- `--parts` also writes phone-sized parts next to the full sheet (`<FILE>-part-N.jpg`, 6 tiles each,
  2 per row). `--part-size` and `--part-cols` change them. Without `--parts`, no parts are written.
- `--sync` recomputes the usage stats in `styles.json` from your post log before rendering (see
  below). Without `--sync` the script never writes `styles.json`.
- Other options: `--today YYYY-MM-DD` sets the cooldown clock, `--include-retired` adds retired
  styles.
- The run fails (exit 1) if an exemplar file is missing, a template folder is missing, or a status,
  production type or spine is unknown. It prints notes when a caption had to shrink to fit, or when
  art is letterboxed because it isn't 4:5.

### Optional: a post log

The stats come from your own post log, if you keep one: a JSON array at
`research/catalog/deck-map.json` (or `--deck-map FILE`), one entry per deck:

```json
{ "code": "<post id>", "folder": "carousels/<id>", "date": "YYYY-MM-DD", "status": "posted",
  "cover_style": "S01", "interior_style": "S01", "mult": 1.0 }
```

`status` is `posted` or `draft`. `mult` is the post's performance ratio. The author uses the post's
views divided by the median views of his carousels posted within ±21 days, which corrects for account
growth. `node shared/build-gallery.mjs --sync` reads the log and recomputes `posts`,
`interior_posts`, `drafts` and `stats` in `styles.json`, grouped by **cover** style. Edit every other
field by hand. Without a log, or without `--sync`, nothing is written and each tile shows the spines
its style fits.

A synced `styles.json` contains your post codes and stats. If your repo is public, don't commit it
after a sync (and keep the post log itself out of the repo).

## Add a style

A new style is its own R&D session, never part of a deck.

1. **Exemplars.** One cover and one interior at 4:5 (1080 × 1350 or 2160 × 2700), saved as
   `exemplars/<ID>-cover.png` and `exemplars/<ID>-interior.png` (`.jpg` is fine). Use your own slides
   when you have them. A third-party reference can seed the prompt block, but keep it out of the
   repo and swap in your own slides once you've made a deck in the style.
2. **Prompt block.** `<ID>-<slug>.prompt.md`, with the sections the four existing blocks use:
   - An intro: where the look came from, the production type, and which images to attach as
     references.
   - Optional: a production split table saying who makes each element (Codex plate, composited
     capture or logo, HTML).
   - `## SYSTEM`: the visual system in one paragraph (ground with hex values, type pairing, panels,
     ornaments, palette, what stays flat), then **Framing** (margins as a share of width and height,
     minimum text size), **References** (the images show the look only; name what not to copy), and
     **Hygiene** (render only the quoted strings, verbatim, with counts).
   - `## COVER` and `## INTERIOR`: the layout, top to bottom.
   - `## KEYING`: flat magenta `#FF00FF` for capture zones, flat cyan `#00FFFF` for logo slots, and no
     magenta or cyan anywhere else.
   - Write any brand text in the chrome as `{{BRAND}}`, and any month and year as `{{MONTH_YEAR}}`.
3. **`styles.json` entry.** `id`, `name`, `one_line`, `status` (`card-v1` once the prompt block
   exists), `production`, `formats` (`spines`, `notes`), `attributes` (`ground`, `type_pairing`,
   `panel`, `character`, `ornament`, `palette`), `cooldown_days`, `exemplars` (`cover`, `interior`,
   `interior_slide`, `note`), `requires`, and `template` (an HTML template folder, or `null`). Paths
   are relative to the repo root.
4. **Skill.** Add the id to the list of styles that can go to Make in
   `.claude/skills/carousel/SKILL.md`.
5. **Check.** `node shared/build-gallery.mjs --check`, then `node shared/build-gallery.mjs`.

To swap an exemplar, replace the file (or change `exemplars.cover` / `interior`) and rebuild the
sheet. Pick a deck that shows the style clearly. When that deck's interiors belong to another style,
take the interior from another deck whose interiors match, and say so in `exemplars.note` (S01's
cover and interior come from two different decks).
