# How it works

This is the method behind `/carousel` ([skill](../.claude/skills/carousel/SKILL.md)): a topic plus
sources in, a deck of 1080 × 1350 PNGs out, with a human touching it twice. Claude decides; Codex
makes the pixels and also plays the context-free cold reader. The worked example is
[`carousels/2026-10-14-claude-video-free/`](../carousels/2026-10-14-claude-video-free/). Every rule
here is a default we're testing, not a law, and the samples behind them are small. When you break one
on purpose, log it in `storyboard.json` → `deviations[]`.

## Text before pixels

Almost all the wasted effort in the decks this came from had one cause: a choice made after images
existed. Decks stalled at a pile of cover plates, dozens of generations went into swapping a character
mid-deck, and a finished deck was re-rendered because the story changed. So topic, hook, storyboard,
CTA keyword and style are all decided in text first, and no image job runs until you approve that
text. A story rewrite after rendering goes back to the text, never into another image round. That
leaves two human touches:

| Touch | You see | You reply |
|---|---|---|
| 1. **Brief card** (no pixels yet) | 3 ranked hooks (one starred), the storyboard, gate results, the cold reader's answers, a recommended style plus an alternative | `go`, or `hook 2, S03`, or copy edits by slide number |
| 2. **Contact sheet** | All slides at phone size, the alternate cover, the caption, a ship checklist | approve, or name the fixes |

## The stages

```
 YOU: topic + sources ─▶ CLAUDE: dossier ▶ hooks ▶ storyboard ▶ gates + cold reader ▶ style pick
                                                                                         │
                         ┌───────────────── BRIEF CARD (touch 1) ◀───────────────────────┘
                         ▼
       CODEX WORKERS: cover ×2 (Claude picks) ▶ slide 2 ▶ the rest in parallel
                         ▼
       CLAUDE: composite ▶ independent QA ▶ fixes ▶ contact sheet + caption ─▶ YOU (touch 2)
```

| Stage | What happens | Output |
|---|---|---|
| 0. Intake | Pull the sources and build a **dossier**: definition, pain, outcome, mechanism, first step, and a verified-facts table. Every number on a slide cites a fact id. Ask only for what's missing: the angle, and whether the CTA deliverable exists. | `dossier.md` ([template](../engine/templates/dossier.md)) |
| 1. Hooks | About 10 hooks across at least 5 formulas, ranked by the rubric. The CTA keyword is locked with the hook. | `hooks.md` |
| 2. Storyboard | Fill the spine's roles with every visible string, then run gates G1–G8. Rewrite at most twice on a failure, then report it. | `storyboard.json`, `cold-reader.json` |
| 3. Brief card | Touch 1. Claude sends the card and a crop of the two style tiles, then stops and waits. | `brief-card.md` ([template](../engine/templates/brief-card.md)) |
| 4. Make | Real captures and cards are prepared, Codex renders the plates, and the compositor drops the real things into keyed zones. | `plates/`, `final/` |
| 5. QA + ship | Independent agents check every slide. Fixes are routed by kind. Exports, contact sheet and caption go to touch 2. | `exports/slide-NN-YYYY-MM-DD.png` |
| 6. Learn | One line per post in your own post log: style, spine, hook formula, result. Review it monthly. Never rewrite an engine rule from one post. | your log |

**Batch mode** is how a steady cadence happens. Once a week, run stages 0–3 for about 5 topics in
parallel (one subagent per deck) and approve all the brief cards in one sitting. On other days,
`/carousel make <deck>` runs stages 4–5 for one approved deck. Treat "daily" as a capacity, not a
quota: ship what passes the gates.

**Sources.** Your own video gives the transcript (what / why / how), frames for proof panels (with the
webcam bubble scrubbed by [`shots.py`](../shared/shots.py)) and your on-camera verdict. A repo gives the
definition, install command and stars (re-verified on posting day). Docs give the definition and
verified numbers. "Go research it" builds the same dossier from web search, on the slower path. A
video runs setup → build → reveal; a carousel leads with the reveal, puts the mental model before the
steps, and follows the viewer's questions, never the source's timeline.

## Story spines

The format picks the spine. A spine is a fixed list of slide **roles**, and each role decides what the
slide has to do, what evidence it needs and how many words it gets. Full tables:
[`engine/spines.md`](../engine/spines.md).

| Spine | Use it for | Path |
|---|---|---|
| **A. Explainer** | A tool, repo, feature or workflow someone should be able to use | cover → what → why → model → how ×2 → value peak → use → start here → CTA |
| **B. Head-to-head** | Two tools tested against each other, or a launch put to a real test | "I tested" → on paper → context → one slide per test → verdict → CTA |
| **C. Listicle** | N repos, skills, plugins or prompts | count hook → optional why → one item per slide, each a mini what-and-why → CTA |
| **D. System build** | A named personal system built in N steps | named system → optional what / why / parts → N step slides → optional real day → CTA |

Defaults across all four: 10 slides or fewer, headlines of 7 words or fewer, about 45 body words,
one proof artifact per slide. **PROVE** means a real capture, verified number or real run; **EXPLAIN**
means a diagram or mock, clearly illustrative. A mock is never shown as proof.

## Text gates (G1–G8)

All eight run on the storyboard text, before any image exists. G1–G7 are Claude's self-check; G8 is
independent.

| Gate | Fails when… |
|---|---|
| G1 Cover contract | The hook names no outcome or artifact; a count on the cover doesn't match the slides that pay it off; a superlative or number the deck never proves; a bare "X is live" with no claim |
| G2 Slide 2 defines the whole | A sub-component (a model name, tier, internal tool) shows up before the whole thing is defined, or before slide 4 |
| G3 Glossary | A term is used before it's defined; more than one new term on a slide; any new term on the verdict or CTA |
| G4 Budget | Headline over 7 words, body over the role's budget, or stacked blocks |
| G5 Spine test | The headlines alone, joined by "so / but / then", don't read as one story; step numbering drifts |
| G6 Re-sequence | Slides follow the source's order instead of the viewer's questions |
| G7 CTA match | The keyword doesn't name this deck's deliverable, differs between slide and caption, or the deliverable doesn't exist |
| G8 Cold reader | A context-free model can't recover what it is, why to care and the first step |

**The cold reader** ([`shared/cold-reader.mjs`](../shared/cold-reader.mjs), prompts in
[`engine/cold-reader-prompt.md`](../engine/cold-reader-prompt.md)) is two Codex calls with no repo, no
tools and no web. The **reader** sees only the slide text (headlines, every visible string, a
one-line description of each panel) and answers what / why / first step, plus any undefined terms.
The **judge** compares those answers with the storyboard's `intent`. Pass means no "no", at most one
"partial", and no blocking undefined terms. Exit 0 is a pass, 2 a fail, 1 an error. Its model,
effort and tier come from `CODEX_MODEL`, `CODEX_EFFORT` and `CODEX_TIER` (defaults in the script
header). Two rules it taught us: give every line of a headline `place: "headline"`, or the lead-in
reads as a fragment; and a slide that shows a command must say where to type it. Write `intent.why`
as one claim, because the judge grades every clause as core.

**What the gates protect: comprehension, not reach.** A deck can fail the cold reader and still do
well because its topic carries it, and a perfectly coherent deck can still stall on a weak hook. The
gates protect understanding, trust and saves. Topic and hook drive reach.

## Hooks

**Topic first** (full rubric and formula bank: [`engine/hooks.md`](../engine/hooks.md)). A hook can
only be as good as its topic. A launch post needs a claim the announcement doesn't make for you (a
verdict, a benchmark surprise, a build). A trending repo only works when it fixes a pain people
already feel, and the pain leads, not the repo name.

**Writing.** Each hook is a set: the main line, an optional kicker, and a visual promise (what the
cover image shows). Write about 10 across at least 5 formulas, score them, show the top 3.

| # | Criterion | 2 points looks like |
|---|---|---|
| R1 | Anchor | A felt pain, wanted outcome or familiar reference, not a name they've never heard |
| R2 | Specific | An artifact or result **and** one number or bound ("4-step build", "3 repos") |
| R3 | Instant visual | One focal image a cold viewer gets at a glance |
| R4 | Timing fit | A claim, verdict or build on something people are talking about now |
| R5 | Payable | The deck pays off every word one-to-one |
| R6 | Glanceable | 10 words or fewer in the main line, readable in under 2 s at phone size |

Each criterion scores 0–2, max 12. Automatic zeros: R4 for a bare "X is live" main line, R5 for any
superlative or number the deck can't show. **The rubric ranks hooks; it doesn't gate shipping**
until a blind back-test against your own results shows it separates winners from losers.

The formula bank, with a template and an example for each, is in
[`engine/hooks.md`](../engine/hooks.md) §4: F1 fantasy build, F1b franchise sequel, F2 known + known,
F3 new-model build, F4 hype + real deadline, F5 count + 10X outcome, F6 enemy → identity, F7 "I
tested", F7b launch + surprising claim, F8 ranked top-N, F9 value twist, F10 first-person capability
("my Claude Code can … now", the formula the worked example uses), F11 problem first / fix second and
F12 outcome playbook. A risk-lowering kicker often helps: "(for free)", "(exact setup inside)".
Avoid bare announcements, "biggest upgrade" superlatives, an unknown name as the headline, "learn X
in 48 hours", generic system names, "which one are you" self-diagnosis, a generic CTA gate, and two
same-format decks within 72 hours.

**CTA keyword.** Lock it with the hook, never later. It names this deck's deliverable and is identical
on the slide, in the caption and in any comment-to-DM automation you use. Prefer a few standing
keywords tied to evergreen deliverables over a new lead magnet per deck.

## The storyboard

[`storyboard.json`](../engine/storyboard.schema.json) is the single record of the deck. Every visible
string lives in `strings[]` before any prompt is written; prompts quote them verbatim with counts,
and QA checks the slides against them.

```jsonc
{ "spine": "A", "style": "S11", "keyword": "ANIMATE", "hook": { "main": "...", "formula": "F10", "score": {...} },
  "intent": { "what": "...", "why": "...", "first_step": "..." },   // what the cold reader must recover
  "glossary": [...], "gates": { "G1": { "pass": true, "note": "..." } }, "deviations": [...],
  "slides": [ { "n": 1, "headline": "...", "strings": [ { "text": "...", "place": "headline", "count": 1 } ],
                "evidence": { "kind": "prove", "describe": "one plain line", "source": "..." } } ] }
```

Three `place` values are reserved: `"headline"` (every line of the headline), `"counter"` (the
`NN / TT` slide counter) and `"chrome"` (the brand header and footer). The cold reader skips headline
and counter strings and shows a chrome string only once; the brief card leaves all three out of the
slide text. Any other `place` (`eyebrow`, `body`, `panel-label`, …) is free-form.

## Style library

Choosing a style by generating images was the biggest time sink, so now picking one takes **zero
generations**. Each style in [`engine/styles/`](../engine/styles/README.md) is a tile made from
existing exemplars (one cover, one interior) plus a prompt block.
[`shared/build-gallery.mjs`](../shared/build-gallery.mjs) renders the sheet, and `--only REC,ALT`
renders the two-tile crop the brief card sends. Claude recommends one style and an alternative from
spine fit, the cooldown, and the style's requirements. Brand text in a style's chrome (header and
footer) is `{{BRAND}}` in the prompt blocks and the S01 template, and the date there is
`{{MONTH_YEAR}}` (`OCTOBER ©2026`, from the deck folder's date). The skill fills both, the brand from
[`engine/brand.json`](../engine/brand.json); that file ships as `YOUR BRAND`, and the skill asks for
yours on the first deck. `build-gallery.mjs` only renders: it never writes `styles.json` unless you
pass `--sync`, which re-reads usage stats from your post log.

| Card | Look | How it's made | Spines |
|---|---|---|---|
| [S01 Terracotta Zine](../engine/styles/S01-terracotta-zine.prompt.md) | Terracotta texture, massive lowercase headline, taped app windows | HTML-native: Codex paints only the cover plate; interiors come from [`templates/02-terracotta-zine`](../templates/02-terracotta-zine/), baked to 1080 × 1350 by [`shared/export.mjs`](../shared/export.mjs) | D, A |
| [S02 Logo Equation](../engine/styles/S02-logo-equation.prompt.md) | Flat terracotta, giant "A + B" equation of real app icons | Hybrid: Codex paints the ground and short type; real logos go in through cyan zones | A |
| [S03 Newsprint Benchmark](../engine/styles/S03-newsprint-benchmark.prompt.md) | Ivory newsprint, grotesk + Didone italic, ruled tables, green verdict bar | Image-native: Codex paints the slide; captures and logos are composited | B |
| [S04 Brutalist Mascot Poster](../engine/styles/S04-brutalist-mascot-poster.prompt.md) | Cream spec-sheet poster, Anton white-on-orange block line, one big cut-out hero (your mascot or the subject's logo tile) ringed by tag chips | Hybrid: Codex plates, your mascot or a logo tile composited, exact text as HTML cards | A, C, D |
| [S05 Phone-Photo Monitor](../engine/styles/S05-phone-photo-monitor.prompt.md) | A phone photo of a monitor showing the real thing, white caption stickers | Hybrid: your photo, or a Codex desk plate with the real capture perspective-warped onto its screen; every word a sticker card | C, A |
| [S06 Statue + Graph Paper](../engine/styles/S06-statue-graph-paper.prompt.md) | Marble statue offering a real logo tile against a changing sky; graph-paper repo cards | Hybrid: one Codex statue plate, HTML cover type and logo tile; interiors from [`templates/01-graph-paper-cream`](../templates/01-graph-paper-cream/) | C, A |
| [S07 Dark Network Hero](../engine/styles/S07-dark-network-hero.prompt.md) | Near-black glowing network, giant white sans, app tile, brush label | Hybrid: text-free Codex network plates, every word HTML from the kit | A, D |
| [S08 Bone Editorial](../engine/styles/S08-bone-editorial.prompt.md) | Kraft-cream, Didone with one accent, dark app pane, ink doodles, taped sticky | Hybrid: Codex paints only paper and doodles, every word HTML from the kit | D, A |
| [S09 Charcoal Studio](../engine/styles/S09-charcoal-studio.prompt.md) | Charcoal, off-white serif, acid-yellow highlights and stickies | Image-native: Codex plates, exact text as kit cards in magenta zones | A, D |
| [S10 Command-Press Blueprint](../engine/styles/S10-command-press-blueprint.prompt.md) | Bone and ink grid, Anton /SLASH-COMMAND bleeding right, dimension lines, two-tone audit charts | HTML-native: HTML sheets from Template 03, word-free Codex FIG plates ([`templates/03-command-press`](../templates/03-command-press/)) | A, C, D |
| [S11 Sketchnote](../engine/styles/S11-sketchnote.prompt.md) | Cream paper, highlighter pill, pastel diagram boxes, hand-drawn arrows | Image-native in the worked example; captures and exact-text cards are composited; a diagram kit for exact-text diagrams | A |
| [S12 Voxel Costume Explainer](../engine/styles/S12-voxel-costume-explainer.prompt.md) | Near-white, bold sans with line 2 in orange, your mascot in one costume per slide (or a logo tile), side-by-side screenshots | Hybrid: HTML pages, your own costume poses or logo tiles composited | A, D |
| [S13 Oversized-Serif Photo Editorial](../engine/styles/S13-oversized-serif-photo-editorial.prompt.md) | One dominant oversized serif word over a cinematic photo, fanned preview cards, giant numerals inside | Hybrid: Codex photo plates, every word HTML, sky-tone pass | C |
| [S14 Scenic Painterly](../engine/styles/S14-scenic-painterly.prompt.md) | A painted landscape per slide, cream Didone, paper list card, optionally your mascot doing something different on each slide | Hybrid: Codex painted plates, HTML list cards, sky-tone pass | C |
| [S15 Landscape Specimen](../engine/styles/S15-landscape-specimen.prompt.md) | A cinematic landscape per item, the item's name set giant in the sky as a two-font specimen, masthead row, BACK/NEXT nav | Hybrid: Codex landscape plates under Template 06's HTML overlay, sky-tone pass ([`templates/06-landscape-specimen`](../templates/06-landscape-specimen/)) | C |
| [S16 Neon Node Pipeline](../engine/styles/S16-node-pipeline.prompt.md) | Pure black, glowing numbered icon-node pipelines, one colour per concept; the cover is a grid of every diagram | HTML-native: HTML from Template 05, graphs from storyboard JSON ([`templates/05-node-pipeline`](../templates/05-node-pipeline/)) | C, D, A |
| [S17 Split-Band Before/After](../engine/styles/S17-split-band-before-after.prompt.md) | Cream-over-white split on every slide, mono Before: / After: labels, huge grotesk statements, one orange text-selection highlight | HTML-native: HTML from Template 07 ([`templates/07-split-band`](../templates/07-split-band/)) | C |
| [S18 Folder-Tab Field Guide](../engine/styles/S18-folder-tab-field-guide.prompt.md) | Orange-framed map cover pinned to round medallions; folder-tab interiors with three scene bands | Hybrid: Codex plates, HTML tab and band cards, logo or emblem medallions | C, D |
| [S19 Window-Chrome Build Diary](../engine/styles/S19-window-chrome-diary.prompt.md) | An app window as the frame, condensed white serif over real artboards, cut-outs breaking out over the chrome; apricot caption pages between | Hybrid: HTML from Template 08 over real app captures ([`templates/08-window-chrome`](../templates/08-window-chrome/)) | D, A |
| [S20 Slate Family Tree](../engine/styles/S20-slate-family-tree.prompt.md) | Chalk slate, index cover of overhead paint-tin icons, light serif names, 'A + B' pill formulas, branching chip trees | Hybrid: Codex slate plates, transparent HTML tree cards | C |
| [S21 Circled-Count Tip Stack](../engine/styles/S21-circled-count-tip-stack.prompt.md) | Cream, lowercase count hook with a hand-circled orange number; three white app-window cards per slide, one finding each | HTML-native: HTML from Template 09 ([`templates/09-window-stack`](../templates/09-window-stack/)) | C |
| [S22 Layered Parts Atlas](../engine/styles/S22-layered-parts-atlas.prompt.md) | Bone blueprint sheet: Anton LAYER n/N over an orange count banner, a detail box with your mascot (or a logo tile), parts numbered across the deck | HTML-native: Codex cover plate, atlas sheets from Template 03 ([`templates/03-command-press`](../templates/03-command-press/)) | C |
| [S23 Crop-Mark Proof Sheet](../engine/styles/S23-crop-mark-proof-sheet.prompt.md) | Cream crop-mark proof sheet: orange mono chip, a giant width-fitted Anton /COMMAND, one stacked-paper proof module per slide | Image-native: Codex plates, proof cards from the kit | C |
| [S24 Spotlight Dossier](../engine/styles/S24-spotlight-dossier.prompt.md) | Grained cream, a soft coloured stage beam lighting each item's real logo, a serif name headline, an ink numbers strip and a mono install card | Image-native: Codex plates, numbers / install / verdict cards, real logo tiles | C, A |
| [S25 Soft-UI Step Guide](../engine/styles/S25-soft-ui-step-guide.prompt.md) | Paper-white product-page tutorial: caps kicker and orange step pill, big sentence-case headline, one soft white UI module per slide, dashed margin traces | HTML-native: one Codex cover plate, every page HTML | A, D |
| [S26 Whiteboard Doodle Showcase](../engine/styles/S26-whiteboard-doodle-showcase.prompt.md) | Warm paper-white page: a handwritten item name over one orange marker underline, a real capture in a sketched ink frame, a small ink doodle acting out the item | Hybrid: Codex doodle plates, every word an HTML card | C, A |
| [S27 Icon-Grid Cheat Sheet](../engine/styles/S27-icon-grid-cheat-sheet.prompt.md) | Warm-white cheat sheet: two real logo tiles joined by '+', a heavy count hook with one orange pill, a numbered grid of repo tiles | HTML-native: HTML only, no Codex job | C |
| [S28 Alpine Product Window](../engine/styles/S28-alpine-product-window.prompt.md) | One bright alpine wallpaper behind every interior: a real app-icon tile over a heavy product name, feature chips, one dark window holding a real capture; orange studio cover | Hybrid: three Codex plates per deck, every page HTML | C, A |

Styles that are more than a prompt block carry a **kit** (`engine/styles/kits/<id>/`: HTML cards with a
fit pass, CSS, needed assets, a README with the render commands, and rendered samples) and **refs**
(`engine/styles/refs/`: text-free or keyed layout references the Codex jobs attach instead of finished
slides, so the model copies the look and not old text). The skill's Stage 4 table gives each style's
route. [`shared/build-style-library.mjs`](../shared/build-style-library.mjs) turns the whole library
into one browsable HTML page.

**Cooldown.** A style posted in the last 14 days is cooling: don't pick it unless you mean to.
Unposted drafts don't start the clock, but count them, because three drafts in one style in a row is
overuse in the making. Most styles score best the first time and decay with repeats, so when you log
results, judge a style by its **median** across uses, not its best post: showing only the best is
selection on outcome. Look-alike styles can share a **cooldown group** (`cooldown_group` in
`styles.json`): a member cools while any member's cover is inside the group's cap, and the tile says
`via S0N`. The shipped worked example doesn't count toward the cooldown, the 72-hour format
spacing or the folder-collision check. A new style is designed in a separate R&D session, never
inside a deck.

## The Codex worker

[`shared/codex-img.mjs`](../shared/codex-img.mjs) runs each job as one headless `codex exec` session.
Claude writes the prompt; the worker tells Codex to call its image tool once with the given references
and do nothing else.

```
codex exec --ignore-user-config -m gpt-6.1-sol -c model_reasoning_effort="high" -c service_tier="priority" \
  -c web_search="disabled" --disable apps -s read-only --skip-git-repo-check --json -C <empty dir> \
  -i <ref 1> -i <ref 2> -  < prompt
```

The model, effort and tier come from the deck's `jobs-*.json`; the skill writes the values above. Each
reference image is attached with its own `-i`, in order, before the trailing `-` that reads the prompt
from stdin.

| Rule | Why |
|---|---|
| `gpt-6.1-sol`, effort `high`, tier `priority` (Fast) | The standing default. Never switch to another image generator without asking the user. |
| `--ignore-user-config`, `--disable apps` | Keeps your own MCP servers, connectors and tokens out of the worker; a lean config also costs far fewer tokens per job |
| Read-only sandbox in an empty dir | Set `CODEX_IMG_SANDBOX=workspace-write` only if read-only blocks generation |
| Prompt on stdin, stdin closed | `codex exec` hangs otherwise |
| **One session per job** | Image calls inside one session run one at a time, so parallelism means separate sessions |
| **2 s stagger, 4 in parallel** | Simultaneous starts race on Codex's own skill install |
| Output via `thread_id` | `--json` has no image event. The worker reads `thread.started`, then takes the PNG from `$CODEX_HOME/generated_images/<thread_id>/` (`CODEX_HOME` defaults to `~/.codex`) |
| Plates never overwritten | Reruns land as `.v2`, `.v3`; every run is logged to `runs/runs.jsonl` with the CLI version, wall time and tokens |
| **Edits are new jobs** | The plate is reference #1, and the prompt says "the only change: …", lists everything to keep, and ends "do not add any new text or elements". Never `resume`: it drops the lean config and puts two images in one thread |

**Order:** two cover variants in parallel, Claude picks one (you can swap it at touch 2), the cover
plate becomes the anchor, slide 2 runs alone and gets inspected, then the rest run in parallel with the
anchor as reference #1. In the worked example, 16 of 16 jobs succeeded (2 covers, 9 interiors, 5
edits) at 29–57 s each, about 46 s on average and about 50K tokens per job, and every edit changed
only its target.

**Known habits:**
- **Keyed zones come out wider than asked** (16:9 requested, about 2.1:1 delivered). Always pass a focus box.
- It occasionally **invents a margin note or a duplicate label**. QA catches it; one edit fixes it.
- **Output size drifts** around 4:5. The compositor fits every plate to 1080 × 1350.
- Each rollout keeps the image inline (about 13 MB per image). After approval, prune the deck's
  threads (their ids are in `runs/runs.jsonl`): `$CODEX_HOME/sessions/**/rollout-*-<thread_id>.jsonl`
  and `$CODEX_HOME/generated_images/<thread_id>/`. The skill offers this and deletes only with your OK.
- An older Codex CLI can reject the model. Pin the binary and check the logged version.

## Compositing

Real things are composited, never painted: screenshots, video frames, logos, prompts, commands and long
tables. The plate leaves flat key-colour zones for them, and
[`shared/composite.py`](../shared/composite.py) fills them.

| Key | Holds | Fit |
|---|---|---|
| Magenta `#FF00FF` | Real captures (`--shot N=path@x,y,w,h`) or exact-text cards (`--card N=path`) | Shots cover-fit around the **focus box**, which always stays fully visible; cards contain-fit and never crop |
| Cyan `#00FFFF` | Real logos (`--logo N=path@scale`) | The zone is erased into the surrounding ground, then the logo is fitted on top |

More modes, for the hybrid styles:

| Mode | What it does |
|---|---|
| `--shot N=path@x,y,w,h,warp` | Perspective-warps a capture onto a screen photographed at an angle (S05), with a photographed-screen look; `,extend=left\|right` when the screen runs off the frame, `,aspect=W:H` for the real screen aspect. Needs opencv |
| `--card N=path --ground fill` | Erases the zone into the ground first, then lays a transparent card on top (cards rendered without `--bg` on textured grounds) |
| `--logo …,bottom` / `,top` / `,tight` / `,fill=#hex` | Sits a cutout on the slot's bottom or top edge, quilts the erased slot from nearby ground, or erases it to one colour |
| `--paste …,erase` | Patches a garbled piece of a plate with a rendered card (fix a bad label without a new generation) |

Template bakes (`shared/export.mjs`) also exit 3 when a template's own fit check (`window.fitReport`)
or `window.qa()` reports a failure, so copy that doesn't fit stops the bake instead of shipping small.

1. **Learn the zones:** `--zones-only` prints each zone's id (M1…, C1… in reading order), aspect, fill
   and `out bbox`, with a debug PNG. A fill under 0.97 means something overlaps the zone.
2. **Render cards** for exact text with [`shared/render-card.mjs`](../shared/render-card.mjs) at the
   zone's `out bbox`, ×2. Exit 2 means the text overflows, or its measured size is below `--min-px`
   (default 14 px): cut copy, never shrink below phone size. Cards must be opaque. The same tool turns
   a logo SVG (simple-icons, or your own) into the transparent PNG that `--logo` needs:
   `node shared/render-card.mjs logo.svg logo.png --w 512 --h 512 --scale 2`.
3. **Composite.** `--dilate` widens the mask to swallow the anti-aliased fringe (in the worked
   example, 3 cleared a faint fringe QA flagged at the default 2). `--letterbox paper` fills bars
   with the plate ground for cream assets; the default `edge` suits dark captures. Exit 3 means
   leftover key colour or a zone with no asset: assign it, or fix the plate with an edit job. The
   final fit never stretches: it crops the minimum, then Lanczos-resizes to 1080 × 1350.

## QA by independent agents

The author never QAs its own slides. Claude spawns parallel subagents (the worked example used 5
agents with 2 slides each). Each gets the final PNG, its plate, the composite report, the slide's
storyboard entry and the style block, and returns `ok | minor | fail` with defects: strings verbatim
with the right count, invented text or marks, leftover key colour and seams, a capture that doesn't
match its description, margins, readability at 360 px wide. There's no OCR (it throws false alarms on
display fonts), so reading the image is the text check. After fixes, re-QA only the changed slides,
and rerun the cold reader if any string changed.

| Defect | Fix |
|---|---|
| Plate (wrong text, invented mark, layout) | An edit job, one change per edit where possible, then re-composite |
| Composite (crop, fringe, letterbox) | Change the focus box, `--dilate` or `--letterbox`. No generation |
| Story or copy | Back to stage 2/3. Never a new render round |

## Lessons learned

- **Topic and hook beat craft.** The winners named an outcome or artifact a cold viewer already wanted. The losers were bare announcements, superlatives, unknown names and self-diagnosis quizzes.
- **A launch needs a claim.** A bare "X is live" did poorly; a launch-day post with a specific, surprising claim and real numbers did well.
- **Coherence is not a reach lever.** Keep the gates for comprehension and trust, and don't expect them to predict views.
- **Comments are not reach,** and slide count inside the usual 7–10 range showed nothing either way.
- **Space out formats and styles.** Both same-format losses we traced went up within about a day of a sibling deck, and styles decay with repetition.
- **Shared tools, not per-deck scripts.** One-off compositing and state scripts piled up into thousands of lines. Now a new per-deck script counts as a bug (extend the shared tool instead), and `storyboard.json` plus the runs log are the whole record.
- **Never let the model paint what must be exact.** Logos, numbers, prompts and long tables go in through keyed zones and cards.
- **If you use a mascot, build a pose library first;** never swap characters mid-deck.
