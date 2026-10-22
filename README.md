# Carousel Engine

Instagram carousels that a cold viewer can follow, made by Claude Code with Codex painting the pixels.

You give it a topic and a source (your YouTube video, a GitHub repo, docs, or "go research it"). It
hands back 7–10 finished 1080 × 1350 slides. You touch it twice: once to approve a one-page **brief
card** (text only, no images yet), and once to check the final contact sheet.

![The worked example: 10 slides made with this pipeline](carousels/2026-10-14-claude-video-free/contact-sheet.jpg)

*The worked example, [`carousels/2026-10-14-claude-video-free`](carousels/2026-10-14-claude-video-free/):
16 Codex image jobs, real screen captures composited in, independent QA on every slide.*

## Why it's built this way

Most wasted effort in AI carousels comes from deciding things after the images exist: a weak hook
discovered on render 30, a story that only makes sense if you watched the video, a logo the model
misspelled. So this pipeline locks every word first, and only then makes pixels.

- **Text before pixels.** Hook, storyboard, CTA keyword and style are decided in text and checked
  by a "cold reader" (a model with no context) before any image is generated.
- **Story spines.** Every deck follows one of four fixed slide sequences (explainer, head-to-head,
  listicle, system build), so the thing is defined before any of its parts, and the payoff isn't
  buried.
- **Real things are pasted in, never drawn.** The model paints flat magenta zones. Real screenshots,
  video frames, logos and exact text (prompts, commands, tables) are composited into them afterwards.
- **Independent QA.** Separate agents check every slide's text, crops and truthfulness against the
  storyboard. A story problem goes back to the brief card, never into another round of renders.

The full method is in [docs/how-it-works.md](docs/how-it-works.md).

## How a deck gets made

| Stage | What happens | You |
|---|---|---|
| 0. Intake | Pull sources (transcript, frames, README, stars) and write a dossier ending in a verified-facts table | name the topic and source |
| 1. Hooks | About 10 hooks from a formula bank, ranked by a six-criterion rubric (max 12); CTA keyword locked with the hook | |
| 2. Storyboard | Fill a story spine into `storyboard.json` with every visible string; run text gates G1–G8, including the cold reader | |
| 3. Brief card | One message: 3 hooks, all slide text, the cold-reader result, 2 style picks | **touch 1:** reply `go`, or `hook 2, S03` |
| 4. Make | Codex paints the plates (covers first, then slide 2 as a check, then the rest 4 at a time); captures, logos and text cards get composited in | |
| 5. QA + export | Independent QA, targeted edit jobs, exports and a contact sheet | **touch 2:** approve and post |

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [Codex CLI](https://github.com/openai/codex), signed in with a ChatGPT account that can use
  `gpt-6.1-sol` with image generation. Check it with `codex --version`. If `codex` isn't on your PATH,
  set `CODEX_BIN` to the binary.
- Node.js 20+ (Playwright and sharp)
- Python 3.11+ with Pillow>=10.1, NumPy and SciPy
- Optional: `yt-dlp` and `ffmpeg` for video sources (ffmpeg makes the frames and merges 1080p
  downloads), and `gh` for repo stats

## Install

```bash
git clone https://github.com/cth9191/carousel-engine.git
cd carousel-engine

# Codex CLI, then sign in
npm i -g @openai/codex
codex login
codex --version

# Node tools and the headless browser
npm install
npx playwright install chromium

# Python tools, in a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Optional: video sources and repo stats
#   yt-dlp and ffmpeg from your package manager (brew, winget, apt)
#   gh, then: gh auth login
```

Use `python3` and `pip3` where those are your system's names. The skill runs its Python tools with
`python -I`, which ignores user site-packages, so activate the venv before you start Claude Code (or
install the requirements system-wide).

The first time you run `/carousel`, the skill asks for your brand name if
[`engine/brand.json`](engine/brand.json) still says `YOUR BRAND`, and writes it there. It's printed in
every style's header and footer.

## Use

Open Claude Code in the repo folder:

```
/carousel https://www.youtube.com/watch?v=<your video>
/carousel github.com/<owner>/<repo>  "angle: why it beats X"
/carousel batch            # about 5 brief cards in one sitting
/carousel make <deck>      # build an approved deck
```

Each deck lives in its own folder, `carousels/YYYY-MM-DD-slug/`, and ends with
`exports/slide-NN-YYYY-MM-DD.png`.

## Changing models

- **Image jobs** take `model`, `effort` and `tier` from each deck's `jobs-*.json`. The skill writes
  `gpt-6.1-sol`, `high` and `priority` (the Fast tier). Edit a deck's jobs files to change one deck,
  or the "One image engine" rule in [`SKILL.md`](.claude/skills/carousel/SKILL.md) to change the
  default.
- **The cold reader** reads `CODEX_MODEL`, `CODEX_EFFORT` and `CODEX_TIER` from the environment.
- **`CODEX_HOME`** (default `~/.codex`) is where Codex keeps its login, generated images and session
  rollouts. The tools read images from it, and the skill offers to prune a deck's rollouts there after
  you approve it.

## Styles

28 styles ship with prompt blocks, kits or HTML templates, and exemplars. Eleven are proven in
posted decks; the other 17 (`test-wave`) are ready to make but show sample renders until you post one. Add your own in [`engine/styles/`](engine/styles/); a style rests 14 days after each use
(look-alike styles can share a cooldown group).

| ID | Style | Best for | Made as |
|---|---|---|---|
| S01 | Terracotta Zine | system builds, N-step tutorials | Codex cover + HTML interiors |
| S02 | Logo Equation | tool combos, integrations | hybrid: Codex plates, real logos composited in |
| S03 | Newsprint Benchmark | head-to-heads, model launch tests | Codex, every slide |
| S04 | Brutalist Mascot Poster | urgency listicles, use cases | Codex plates, your mascot or a logo tile composited, exact text as HTML cards |
| S05 | Phone-Photo Monitor | repo listicles, quick tips | your monitor photo (or a Codex desk plate) with the real capture warped onto the screen, HTML stickers |
| S06 | Statue Cover + Graph-Paper Cards | top-N lists, tool roundups | Codex statue cover + HTML type and logo tile, HTML interiors |
| S07 | Dark Network Hero | single-tool and system reveals | text-free Codex network plates, every word HTML |
| S08 | Bone Editorial | system reveals, explainers | Codex paper ground and doodles, every word HTML |
| S09 | Charcoal Studio | tutorials, step-by-step builds | Codex plates, exact text as HTML cards |
| S10 | Command-Press Blueprint | skill and command roundups, N levels | HTML sheets from Template 03, word-free Codex FIG plates |
| S11 | Sketchnote | what-is / how-it-works explainers | Codex, every slide (diagram kit for exact-text diagrams) |
| S12 | Voxel Costume Explainer | one tool or feature explained end to end | HTML pages, your own costume poses or logo tiles composited |
| S13 | Oversized-Serif Photo Editorial | frameworks, 'N rules' decks | Codex photo plates, every word HTML, sky-tone pass |
| S14 | Scenic Painterly | big collections grouped by job | Codex painted plates, HTML list cards, sky-tone pass |
| S15 | Landscape Specimen | top-N tools and pairings | Codex landscape plates under Template 06's HTML overlay, sky-tone pass |
| S16 | Neon Node Pipeline | how pipelines and agent patterns run | HTML from Template 05, graphs from storyboard JSON |
| S17 | Split-Band Before/After | before/after habit flips | HTML from Template 07 |
| S18 | Folder-Tab Field Guide | entries grouped into 3 chapters | Codex plates, HTML tab and band cards, logo or emblem medallions |
| S19 | Window-Chrome Build Diary | build diaries | HTML from Template 08 over real app captures |
| S20 | Slate Family Tree | taxonomies: N base parts and what's built on each | Codex slate plates, transparent HTML tree cards |
| S21 | Circled-Count Tip Stack | 'I went through N' findings | HTML from Template 09 |
| S22 | Layered Parts Atlas | 20-36 items in 4-6 layers | Codex cover plate, atlas sheets from Template 03 |
| S23 | Crop-Mark Proof Sheet | slash-command roundups with proof | Codex plates, proof cards from the kit |
| S24 | Spotlight Dossier | repo, tool and skill roundups | Codex plates, numbers / install / verdict cards, real logo tiles |
| S25 | Soft-UI Step Guide | setup guides for a tool or repo | one Codex cover plate, every page HTML |
| S26 | Whiteboard Doodle Showcase | repo and tool showcases | Codex doodle plates, every word an HTML card |
| S27 | Icon-Grid Cheat Sheet | one-page repo cheat sheets | HTML only, no Codex job |
| S28 | Alpine Product Window | tools that each have a real UI | three Codex plates per deck, every page HTML |

![Every style, with an example cover and interior for each](engine/styles/gallery.jpg)

`node shared/build-style-library.mjs` builds a browsable page of the library (cards, filters, the
spec and prompt block per style) at `engine/styles/library/index.html`.

## What's in the repo

| Path | What |
|---|---|
| [`.claude/skills/carousel/SKILL.md`](.claude/skills/carousel/SKILL.md) | The orchestrator skill: every stage, rule and command |
| [`engine/`](engine/) | Story spines and gates, hook bank and rubric, storyboard schema, cold-reader prompts, templates, `brand.json` |
| [`engine/styles/`](engine/styles/) | Style library: `styles.json`, prompt blocks, exemplars, Codex refs (`refs/`), HTML card kits (`kits/`) |
| [`shared/`](shared/) | Tools: Codex image worker, cold reader, compositor (captures, logos, cards, perspective warp, patching), card renderer, frame grabber, brief-card, gallery and style-library builders, Lucide icon inliner, an optional mascot pose checker, and `export.mjs` (HTML-template bakes) |
| [`templates/02-terracotta-zine/`](templates/02-terracotta-zine/) | HTML interiors for style S01 |
| [`templates/01-graph-paper-cream/`](templates/01-graph-paper-cream/) | HTML interiors for style S06 |
| [`carousels/2026-10-14-claude-video-free/`](carousels/2026-10-14-claude-video-free/) | The worked example, with its own README |

## Cost and time

On the worked example, each Codex image job took about 46 seconds and about 50K tokens. A 10-slide
deck is roughly 11 plates plus a handful of edit jobs, run 4 at a time. The text stages (dossier,
hooks, storyboard, cold reader) take most of the thinking and none of the image budget.

## Limits

- The style library is a starting set. New styles are a separate design session, not part of a deck.
- No mascot ships. Styles that suit a character take your own (composited as a PNG, never painted);
  never use a licensed one.
- You supply the real material: screenshots, screen recordings, logos. The pipeline won't invent them.
- Codex draws key zones a little wider than asked, and sometimes adds a margin note nobody asked for.
  The compositor's focus boxes and the QA pass exist for exactly this.
- It replaces the older ref-deck skill (github.com/cth9191/ref-deck), which built decks a different
  way.

## License

MIT. See [LICENSE](LICENSE).
