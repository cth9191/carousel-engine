# Style library

Every visual style a deck can use. A style is three things: two exemplar images, a prompt block, and
an entry in `styles.json`. Picking a style takes **zero image generations**: the pick sheet is built
from the exemplars.

| File | What it is |
|---|---|
| `styles.json` | The catalog: one entry per style id. Name, one-liner, status, production type, spine fit, attributes, cooldown, exemplar paths, requirements, template. |
| `<id>-<slug>.prompt.md` | The style's prompt block: the SYSTEM text pasted into every Codex image prompt, the COVER / INTERIOR layouts, and the KEYING rules for magenta (capture) and cyan (logo) zones. |
| `exemplars/` | One cover and one interior per style (`<id>-cover`, `<id>-interior`), 4:5. They're the art on the pick sheet and the style references attached to a deck's first prompts. |
| `refs/` | Text-free or keyed layout references that a style's Codex jobs attach (S04, S05, S07–S09, S12–S14, S17, S19, S26), drawn from the author's own slides or HTML mocks. `refs/src/` holds the builders that ship. Styles without refs run text-only prompts until your first approved plate becomes the reference. |
| `kits/<id>/` | Per-style HTML card kits (S04–S14, S18, S20, S23–S28; S15–S17, S19, S21 and S22 work from their HTML template): the cards, a README with the render commands, and rendered `samples/`. A deck copies the kit's cards into `$D/cards/`. |
| `gallery.jpg` | The pick sheet: one tile per style. Built by `shared/build-gallery.mjs` (see below). |
| `library/` | A browsable HTML page of every style (cards, filters, attributes, requirements, the prompt block). Built by `shared/build-style-library.mjs`; a build output, git-ignored. |

Two placeholders appear in prompt blocks, in `styles.json` and in a deck's copy of an HTML template.
`{{BRAND}}` is the `brand` in `engine/brand.json`; the skill asks for it before your first deck if
it's still `YOUR BRAND`. `{{MONTH_YEAR}}` is the month and year of the deck folder's date, e.g.
`OCTOBER ©2026`. The skill fills both in when it writes prompts and when it copies a template into a
deck.

## The styles

| Id | Name | Looks like | Spines | Production |
|---|---|---|---|---|
| S01 | Terracotta Zine | Terracotta texture, massive lowercase headline with a period, taped dark app windows | D system build, A explainer | html-native |
| S02 | Logo Equation | Terracotta, giant white "Tool A + Tool B", two big app-icon tiles joined by a plus | A explainer: tool combos, integrations, set-up tutorials | hybrid |
| S03 | Newsprint Benchmark | Warm newsprint, Didone italic, diagonal VS split with huge percentages, ruled tables, green verdict bar | B head-to-head / launch test | image-native |
| S04 | Brutalist Mascot Poster | Cream spec-sheet poster, Anton white-on-orange block line, one big cut-out hero (your mascot or the subject's logo tile) ringed by tag chips | C listicle / use cases, A explainer, D system build | hybrid |
| S05 | Phone-Photo Monitor | A phone photo of a monitor showing the real thing (README, tool, title screen), with white caption stickers | C repo listicle / quick tips, A explainer | hybrid |
| S06 | Statue Cover + Graph-Paper Cards | A marble statue offering one real logo tile against a changing sky, huge white wordmark; graph-paper repo-card interiors | C top-N / roundups, A explainer | hybrid |
| S07 | Dark Network Hero | Near-black glowing network or teal starfield, giant white sans, app tile and brush label | A single-tool reveal, D system reveal | hybrid |
| S08 | Bone Editorial | Grained kraft-cream, Didone with one cobalt accent, rounded dark app pane, ink doodles, taped sticky | D system reveal, A explainer | hybrid |
| S09 | Charcoal Studio | Charcoal ground, off-white serif, acid-yellow highlights and stickies, browser windows | A tutorial, D step-by-step build | image-native |
| S10 | Command-Press Blueprint | Bone and ink grid, Anton /SLASH-COMMAND bleeding right, dimension lines, two-tone audit charts | C skill and command roundups, D levels and builds, A code-heavy explainer | html-native |
| S11 | Sketchnote Diagram Explainer | Cream, heavy grotesk with a yellow highlighter pill, pastel flow-diagram boxes, hand-drawn arrows | A explainer for cold viewers | image-native |
| S12 | Voxel Costume Explainer | Near-white, bold sans with line 2 in orange, your mascot in one costume per slide (or a logo tile), side-by-side screenshots | A explainer, D system build | hybrid |
| S13 | Oversized-Serif Photo Editorial | One dominant oversized serif word over a cinematic photo, fanned preview cards, giant numerals inside | C frameworks / 'N rules' | hybrid |
| S14 | Scenic Painterly | A painted landscape per slide, cream Didone, paper list card, optionally your mascot doing something different on each slide | C big lists grouped by job | hybrid |
| S15 | Landscape Specimen | A cinematic landscape per item, the item's name set giant in the sky as a two-font specimen, masthead row, BACK/NEXT nav | C top-N listicle | hybrid |
| S16 | Neon Node Pipeline | Pure black, glowing numbered icon-node pipelines, one colour per concept; the cover is a grid of every diagram | C 'N patterns', D system build, A explainer | html-native |
| S17 | Split-Band Before/After | Cream-over-white split on every slide, mono Before: / After: labels, huge grotesk statements, one orange text-selection highlight | C before/after flips | html-native |
| S18 | Folder-Tab Field Guide | Orange-framed map cover pinned to round medallions; folder-tab interiors with three scene bands | C entries in chapters, D steps | hybrid |
| S19 | Window-Chrome Build Diary | An app window as the frame, condensed white serif over real artboards, cut-outs breaking out over the chrome; apricot caption pages between | D build diary, A explainer | hybrid |
| S20 | Slate Family Tree | Chalk slate, index cover of overhead paint-tin icons, light serif names, 'A + B' pill formulas, branching chip trees | C taxonomies | hybrid |
| S21 | Circled-Count Tip Stack | Cream, lowercase count hook with a hand-circled orange number; three white app-window cards per slide, one finding each | C findings listicle | html-native |
| S22 | Layered Parts Atlas | Bone blueprint sheet: Anton LAYER n/N over an orange count banner, a detail box with your mascot (or a logo tile), parts numbered across the deck | C big grouped lists | html-native |
| S23 | Crop-Mark Proof Sheet | Cream crop-mark proof sheet: orange mono chip, a giant width-fitted Anton /COMMAND, one stacked-paper proof module per slide | C skill and command roundups | image-native |
| S24 | Spotlight Dossier | Grained cream, a soft coloured stage beam lighting each item's real logo, a serif name headline, an ink numbers strip and a mono install card | C repo and tool roundups, A explainer | image-native |
| S25 | Soft-UI Step Guide | Paper-white product-page tutorial: caps kicker and orange step pill, big sentence-case headline, one soft white UI module per slide, dashed margin traces | A setup guide, D steps | html-native |
| S26 | Whiteboard Doodle Showcase | Warm paper-white page: a handwritten item name over one orange marker underline, a real capture in a sketched ink frame, a small ink doodle acting out the item | C showcase, A explainer | hybrid |
| S27 | Icon-Grid Cheat Sheet | Warm-white cheat sheet: two real logo tiles joined by '+', a heavy count hook with one orange pill, a numbered grid of repo tiles | C one-pager or carousel | html-native |
| S28 | Alpine Product Window | One bright alpine wallpaper behind every interior: a real app-icon tile over a heavy product name, feature chips, one dark window holding a real capture; orange studio cover | C product roundup, A explainer | hybrid |

How each one gets made:

- **S04, S10, S12–S28**: the route is in the skill's Stage 4 table, with the exact commands in the
  style's kit README (`kits/<id>/`) or template `recipe.md`. Most have no posted deck yet, so their
  tiles show sample renders from the kit or template; S10 and S24 show real decks.
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
  cover and slide 4 of this repo's worked example, `carousels/2026-10-14-claude-video-free`. Its
  diagram kit (`kits/S11/`: flow, compare and parts) renders a diagram as an exact-text card when a
  painted one would garble.
- **S05**: your own photos of your monitor are best. Without them, three Codex plates of a desk (a
  cover view, a canted and a close view, refs `refs/s05-ref-*`) get the real capture
  perspective-warped onto their magenta screen (`composite.py --shot …,warp`). Every word is a caption
  sticker from `kits/S05/`.
- **S06**: one Codex statue plate per deck (rotate statue, gesture and sky every time), a real logo
  tile on the statue's palm (`kits/S06/tile.html` through a cyan slot), HTML cover type
  (`kits/S06/cover.html`). Interiors come from `templates/01-graph-paper-cream/slides.html`.
- **S07**: one text-free Codex network plate per slide (refs `refs/s07-ref-*`); every word, tile,
  capture window and rail is HTML from `kits/S07/page.html` over the fitted plate.
- **S08**: Codex paints only text-free paper (a reusable kraft ground) and ink doodles; every word is
  HTML from `kits/S08/`, so small type and stickies stay sharp.
- **S09**: Codex paints charcoal plates (refs `refs/s09-ref-*`); exact text is cards from `kits/S09/`
  (list, grid, terminal, stats, footer bar) pasted into magenta zones.

## Reading a tile

```
S01  Terracotta Zine                          <- id + name (id colour = status)
spine D System build · A Explainer            <- or, once you sync a post log: N uses · median Mx · best Bx · last MM-DD
[CARD v1]  html-native   no posts logged      <- status, production, availability
COVER                        INTERIOR · slide 2
[ cover art ]                [ interior art ]
```

- **Status**: `card-v1` means the style has a prompt block, can go to Make and has been proven in a
  posted deck. `test-wave` means it has a prompt block and kit and can go to Make, but no posted
  deck has proven it yet: its tile shows sample renders. The script also accepts `next-wave`
  (worked for you, no prompt block yet) and `retired` (hidden unless `--include-retired`).
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

**Cooldown groups.** Styles that look alike in the feed can share a `cooldown_group` (one object or an
array): `{id, members, applies_to: cover|any, cap_days}`. Every member carries an identical copy. A
member cools while any member's cover (or, with `any`, any use) is younger than `cap_days`, and the
tile names the cause, e.g. `cooling until 11-02 · via S08`. `--check` prints a table of the groups and
fails on a malformed or mismatched one. None ship by default; add one when two of your styles start
reading as the same look.

The clock reads `stats.last_used` on each style. No style has stats yet. When you post a deck, add
`"stats": { "last_used": "YYYY-MM-DD" }` to its style, or keep a post log and let
`build-gallery.mjs --sync` fill it in.

## Build the pick sheet

```
node shared/build-gallery.mjs                          # every style -> engine/styles/gallery.jpg
node shared/build-gallery.mjs --only S03,S11 --out carousels/<deck>/style-pick.jpg
node shared/build-gallery.mjs --check                  # validate + print the table, render nothing
node shared/build-style-library.mjs                    # the browsable page -> engine/styles/library/index.html
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
2. **Prompt block.** `<ID>-<slug>.prompt.md`, with the sections the existing blocks use:
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
