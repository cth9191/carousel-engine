---
name: carousel
description: Carousel Engine orchestrator for Instagram carousels. Takes a topic plus sources (a YouTube video, a repo, docs, or "go research it") to final 1080x1350 PNGs with two human touches, a text-only brief card (dossier, ranked hooks, gated storyboard, cold-reader result, style pick) and a final contact-sheet check. Between them it drives headless Codex CLI image workers (gpt-6.1-sol), composites real captures, logos and exact-text cards, and runs independent QA. Needs the Codex CLI installed and signed in. Also runs batch mode (about 5 brief cards in one sitting). Use for any new carousel, "/carousel", "make a carousel about X", "brief card for X", "batch the week's brief cards" ("/carousel batch"), or making an approved deck ("/carousel make <deck>").
---

# carousel: the Carousel Engine orchestrator

Topic + sources → `exports/slide-NN-YYYY-MM-DD.png`, with the user touching it twice: **touch 1** is the
brief card (no pixels exist yet), **touch 2** is the contact sheet. The method lives in `engine/`
(spines, hooks, schemas, styles). The worked example is
`carousels/2026-10-14-claude-video-free/`: when unsure of a file's shape, copy the worked example's.

Run every command from the repo root, with `D=carousels/<YYYY-MM-DD-slug>`. The tools need:

- the Codex CLI, signed in (`codex` on PATH, or `CODEX_BIN`). `CODEX_HOME` (default `~/.codex`) is
  where Codex keeps its login, its generated images and its session rollouts; the tools read it.
- Node 20+ with the repo's Playwright and sharp (`npm install`, `npx playwright install chromium`).
- Python 3.11+ with Pillow>=10.1, numpy and scipy. Commands use `python -I`, which ignores user
  site-packages, so install `requirements.txt` into a venv and activate it first (or install
  system-wide). Where the system's name is `python3`, use that.
- For video sources, yt-dlp plus ffmpeg (ffmpeg makes the frames and merges 1080p downloads). For repo
  stats, `gh`, signed in with `gh auth login`.

Where this file says SendUserFile, use it if your Claude Code has it; otherwise give the user the file
path.

## Rules (do not relax)

- **Brand.** `engine/brand.json` ships as `{"brand": "YOUR BRAND", ...}`. If `brand` is missing or
  still `YOUR BRAND`, stop and ask the user for their brand name, write it into `brand.json`, and only
  then go on. Do this at intake, before any storyboard string, prompt or card is written. Two
  placeholders are replaced wherever they appear, in a style prompt block and in a deck's copy of an
  HTML template: `{{BRAND}}` (the `brand` value) and `{{MONTH_YEAR}}` (the month and year of the deck
  folder's date, upper case, for example `OCTOBER ©2026`).
- **Text before pixels.** No image job runs before the user approves the brief card. A story or copy
  change after rendering goes back to stage 2/3 (fix the storyboard, rerun the gates, show the changed
  rows), never into another image round.
- **One image engine:** `node shared/codex-img.mjs` with `gpt-6.1-sol`, effort `high`, tier `priority`
  (Fast). Never switch to another image generator without asking the user. These are the values the
  jobs files get; to change the default, change it here. The cold reader takes its model from
  `CODEX_MODEL`, `CODEX_EFFORT` and `CODEX_TIER` instead.
- **Real things are composited, never painted:** logos (the user's own logo files or simple-icons
  SVGs, as PNGs in `$D/logos/`, through cyan zones), screenshots and video frames (through magenta
  zones), and exact text such as prompts, commands and long tables (HTML cards). Every number resolves
  to a verified fact.
- **Every visible string lives in `storyboard.json` → `strings[]`** before any prompt is written.
  Prompts quote them verbatim with counts; QA checks the slides against them.
- **No per-deck scripts.** No `.mjs` or `.py` files in a deck folder. Card HTML in `$D/cards/` and the
  JSON specs are content, so they're fine. If a shared tool can't do a job, extend the shared tool
  (and say so), or stop and report.
- **Styles come from the library** (`engine/styles/`). Only styles with a prompt block can go to Make:
  S01, S02, S03, S05, S06, S07, S08, S09 and S11 (routes in Stage 4). A new style is a separate R&D
  session, never part of a deck.
- **Mascots are optional and never licensed.** No style needs a character. If the user has their own
  mascot, it is composited as a PNG cutout (never painted by Codex); `shared/pose-check.py --sprite`
  checks generated poses against it.
- **Spacing:** a 14-day style cooldown, and no two same-format decks within 72 hours.
- **Folders:** `$D` is dated today, or the planned posting day in batch mode. It's never a past date.
  Check `carousels/` for a parallel session's folder on the same topic before creating one.
- **The worked example doesn't count.** `carousels/2026-10-14-claude-video-free` ships with the repo.
  Ignore it in every cooldown, 72-hour spacing and folder-collision check.

## Deck folder

```
dossier.md  hooks.md  storyboard.json  cold-reader.json  brief-card.md  style-pick.jpg   stages 0-3
deliverable.md (only when the CTA deliverable doesn't exist yet)
refs/ shots/ (shots.spec.json) cards/ logos/ prompts/ jobs-*.json plates/                stage 4
slides.html  assets/  (S01 only)                                                         stage 4
runs/ (runs.jsonl, logs/, zones/, composite/, qa-vN.json, boards)                        stages 4-5
final/  exports/  contact-sheet.jpg  caption.md                                          stage 5
```

## Stage 0: Intake

Input: `/carousel <YouTube URL | repo | docs URL | topic> [angle]`. Ask the user only for what's
missing: the angle, whether the CTA deliverable exists, and the brand name if `engine/brand.json` still
says `YOUR BRAND` (see Rules).

1. Pull the sources into `research/<YYYY-MM-DD-slug>-source/` (created here):

   | Source | Pull with | Fills (`engine/spines.md` → "Source → spine") |
   |---|---|---|
   | A YouTube video (the user's own, or one the deck cites) | `yt-dlp --skip-download --write-auto-subs --sub-langs en-orig --sub-format vtt --write-info-json` (on HTTP 429, add `--sleep-subtitles 5`). Views: the public count, or the user's own channel data if they have it (optional) | transcript → what/why/how; chapters; frames at chosen timestamps → proof panels (scrub the webcam bubble); the creator's take → verdict or peak; tangents → caption |
   | GitHub repo | `gh api repos/<o>/<r>` (stars, forks, license, pushed) and `gh api repos/<o>/<r>/readme` | README definition → `what`; install → `start`; verified stars → proof; examples → `use` |
   | Docs / announcement | WebFetch | definition + examples → `what`, `use`; verified numbers → `why`/`paper`. Ignore its section order |
   | "Go research it" | WebSearch and WebFetch, plus any research skills the user has (for example `/last30days` or `/github-trending`, if you have them) | the same dossier, on the slower path |

2. Write `$D/dossier.md` from `engine/templates/dossier.md`. End it with a `## verified-facts` table
   (`id | claim | source | verified`), as in the worked example. Every number and claim on a slide
   cites an id. Stars and views get re-checked on posting day. Name only the official repo or package;
   lookalike repos exist.
3. Re-sequence by the viewer's questions. A video runs setup → build → reveal, and a carousel leads
   with the reveal.
4. Note the timing in §10: launch day N, the same-topic video's 48-hour views (if the user has that
   data), and any same-format deck in the last 72 h (the user's own post log, if they keep one, plus
   recent `carousels/` other than the worked example).

## Stage 1: Hooks

1. Pick the spine with the table in `engine/spines.md`.
2. Write about 10 hooks across at least 5 formulas (`engine/hooks.md` §4). Each hook is a set: main
   line, kicker, and visual promise. Score each one R1–R6 (0–2 each, max 12) with the automatic zeros
   and §5's anti-patterns. The rubric **ranks**; it doesn't gate.
3. Lock the CTA keyword together with the hook. Prefer a standing keyword: one the user already runs,
   with an evergreen deliverable (they keep the list in the standing-keyword table of
   `engine/templates/brief-card.md`). A new keyword means drafting `$D/deliverable.md` and flagging it.
4. Save all ten, ranked, to `$D/hooks.md`. The top hook goes to `storyboard.hook`, with `score` as
   `{R1..R6, total, note}` (`note` = why it's starred), and the next two to `alt_hooks`.

## Stage 2: Storyboard

1. Fill the spine's roles into `$D/storyboard.json` (schema `engine/storyboard.schema.json`; the
   worked example's `storyboard.json` is a complete example). For each slide:
   - `lesson`, `headline`, and `strings[]` with `place` and `count`. Include the chrome, the counter
     `NN / TT`, and the candidate style's furniture (S11 eyebrows, the S03 header label).
   - Three `place` values are reserved: `"headline"` (every line of the headline), `"counter"` (the
     `NN / TT` counter) and `"chrome"` (the brand header and footer). The cold reader skips headline
     and counter strings and shows a chrome string only once; the brief card leaves all three out of
     the slide text. Any other `place` is free-form (`eyebrow`, `body`, `panel-label`, …).
   - `evidence {kind: prove|explain|none, describe, source}`. `describe` is one plain line, because the
     cold reader reads it.
   - Optional per slide: `layout` (a layout name from the style's prompt block; the role still sets the
     job), `cards[]` (`{zone, html, size}` for HTML cards pasted into zones) and `star: true` on the one
     item the cover payoff leans on (at most one per deck). The brief card shows layout and ★.
   - `format: "single"` makes a one-image post (exactly one slide); its gates are in `engine/spines.md`
     → "Format single". Leave it out for a normal carousel.

   Also fill `intent` (`why` is one claim), `glossary`, `keyword`, `deliverable`, `caption` (the keyword
   plus a pointer to the source video when there is one), `sources`, and `style` (the recommendation).

   Two rules the cold reader enforces (learned on an early dry run):
   - Give every line of the headline `place: "headline"`. The headline is printed once and those
     strings are skipped, so a lead-in under any other place name reads as an unfinished fragment.
   - A slide that shows a command must say where it goes. The cold reader blocks bare commands and
     words like "terminal". Prefer the path a viewer already knows, such as asking Claude Code to
     install it.
2. Self-check gates G1–G7 (`engine/spines.md` → Text gates), and write `gates.Gn = {pass, note}`. The G5
   note is the spine-test sentence. Log every deliberate deviation in `deviations[]`.
3. G8: `node shared/cold-reader.mjs $D/storyboard.json`. `--dry` prints the reader input. Exit 0 is a
   pass, 2 a fail, 1 an error. It writes `cold-reader.json` and fills `gates.G8` / `cold_reader`.
4. On any failure, rewrite and rerun, at most 2 rewrites. After that, carry the failure into the brief
   card. Optional, when the angle is unclear: draft 2–3 competing storyboards in
   `$D/drafts/<angle>.storyboard.json`, cold-read each one, and keep the best (the worked example did
   this).

## Stage 3: Brief card (touch 1)

1. Pick a style from `engine/styles/styles.json`: spine fit (`formats.spines`), cooldown (`stats.last_used`
   + unposted `drafts`, the user's own post log if they keep one, and recent `carousels/` folders other
   than the worked example), and `requires[]`. Recommend one style plus an alternative, both with
   prompt blocks. Look-alike styles can share a `cooldown_group` (see `engine/styles/README.md`):
   `node shared/build-gallery.mjs --check` prints each style's availability, group cooldowns included.
2. `node shared/build-gallery.mjs --only <REC>,<ALT> --out $D/style-pick.jpg`. It only renders: it
   never writes `styles.json` unless you pass `--sync`, which re-reads the usage stats from the user's
   post log (`--deck-map FILE`; the log's shape is in the script header). Never pass `--sync` from
   parallel batch agents. Without `--only` it renders the full sheet (default
   `engine/styles/gallery.jpg`), and phone-sized parts only with `--parts`.
3. `node shared/brief-card.mjs $D/storyboard.json --style <REC> --alt <ALT>` writes `$D/brief-card.md`.
4. Append `### Timing` and `### Needs from you` to `brief-card.md`. The script doesn't write them, and
   rerunning it overwrites the file. Needs from you covers captures only the user can take, the
   deliverable and its comment-keyword automation (for example ManyChat, if they use one), and facts
   only they know.
5. Send the card's text in chat and `style-pick.jpg` with SendUserFile. Then **stop and wait**.
6. Replies:
   - `go`: approves the starred hook, the storyboard and the recommended style.
   - `hook 2, S03`: swaps the hook and/or the style.
   - Copy edits by slide number.

   Apply them to `storyboard.json`. If any string changed, rerun the affected gates and the cold reader.
   Set `style`.

## Stage 4: Make

Production depends on the style. Read the style's prompt block first:
`engine/styles/<id>-*.prompt.md`.
- **S03, S11** are image-native: Codex paints every slide.
- **S01** is HTML-native: Codex paints only the cover plate. Interiors come from
  `templates/02-terracotta-zine/slides.html`, baked with `node shared/export.mjs --carousel <id>`
  (step 9).
- **S02** is a hybrid, per its block.
- **S05–S09** each have a route below. The style's kit `README.md` (`engine/styles/kits/<id>/`) or
  template `recipe.md` has the exact commands and limits. Refs live in `engine/styles/refs/` (copy the
  ones a block names into `$D/refs/`). Exact text is always HTML. A template bake that exits 1 (fit pass
  threw), 2 (missing image) or 3 (fit/copy or `qa()` failure) means rewrite the copy or fix the data,
  never shrink the type floor.

  | Style | Route |
  |---|---|
  | S05 | The user's own photos of their monitor first. Otherwise 3 Codex plates (a desk cover with `s05-ref-desk` + `s05-ref-canted`; canted and close interiors with the locked cover first, then `s05-ref-canted` / `s05-ref-close`), reused across items. Screens: real captures (faces scrubbed) or `kits/S05/screen-title.html` at the zone aspect. `composite.py --shot 1=…@x,y,w,h,warp` (`,extend=left\|right` when the screen runs off a side; the desk cover takes `,aspect=` its zone aspect) → `fitted/`, leftover 0. Stickers: `kits/S05/caption.html` → `cards/slide-NN.html`, render-card 1080x1350 `--scale 1 --min-px 30` → `final/`. |
  | S06 | One Codex statue plate (refs: the S06 exemplar cover + the user's last S06 cover, if any; a new statue and sky per the block's Rotation). `kits/S06/tile.html` (a real mark) at the slot aspect → `--logo C1=…@1.07`; `kits/S06/cover.html` → `final/slide-01.png`. Interiors: copy `templates/01-graph-paper-cream/slides.html`, set `coverImg` to that cover, one `layered` slide per item (local captures, a verified repo card), the keyword CTA (`ctaKeyword`, `ctaDeliverable`); `export.mjs` (exit 3 = the keyword or deliverable doesn't fit: cut copy). |
  | S07 | One Codex plate per slide (SYSTEM + COVER or the layout's INTERIOR figure; refs `s07-ref-teal` + `s07-ref-ember`; no text, no keys); `composite.py plates/slide-NN.png fitted/slide-NN.png`; copy `kits/S07/page.html` to `cards/slide-NN.html` and fill its JSON (layout per role; `parts` sets `pos` from the plate); render-card 1080x1350 `--scale 1 --min-px 22` to `exports/`. |
  | S08 | Copy `kits/S08/cards/s08.css`, the fitted ground (or paint a fresh one with `kits/S08/jobs-setup.json --only ground`, then fit it per the kit README) and `doodles/`; write `cards/page-NN.html` per slide (layouts in the prompt block, `kits/S08/samples/` as the example); icons with `node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards`; render-card 1080x1350 `--scale 1 --min-px 20` to `exports/`. |
  | S09 | Codex plates with `s09-ref-cover` + `s09-ref-step`; cards from `kits/S09/` at each magenta bbox (`--bg "#151515"`, bar `"#F5F400"`, terminal `"#0E0E0F"`); `--shot`, `--card`; logo tiles via `--logo`; a mascot only if the user has one (cyan slot on charcoal, `--logo C1=…@1.0,bottom`); headline and sticky QA letter by letter. |
  | S11 | Codex plate with one magenta zone; the diagram from `engine/styles/kits/S11/` rendered at the zone bbox (2x, `--bg` paper, `--min-px 22`), `--card M1=`. |

1. **Real assets.**
   - Video frames, stills and tile re-layouts: write `$D/shots/shots.spec.json` (the worked example's
     shape), then run `python -I shared/shots.py $D/shots/shots.spec.json --sheet $D/runs/shots.jpg`
     (it creates the sheet's folder). It crops or scrubs the webcam bubble. Frames need the video file
     itself in the source folder (yt-dlp without `--skip-download`; ffmpeg merges the 1080p streams).
   - `bubble_prior` in the worked example's spec is its author's webcam position (cx, cy, r in a
     1920 × 1080 frame). For another video, set `"bubble": "none"` on each shot when there's no webcam
     bubble, or measure the user's own bubble and put it in `bubble_prior`.
   - Web pages: screenshot them into `shots/` with whatever browser tool you have (the Browser pane,
     or the playwright-cli skill if you have it), or a short Playwright call.
   - Logos: the user's own logo file, or a simple-icons SVG. `composite.py --logo` needs a PNG, so
     turn an SVG into a transparent PNG with
     `node shared/render-card.mjs $D/logos/<name>.svg $D/logos/<name>.png --w 512 --h 512 --scale 2`.
     A PNG the user supplies is copied into `$D/logos/` as is.
   - Copy the style's exemplars (`engine/styles/exemplars/`), or the user's own `refs/` files, into
     `$D/refs/`.
2. **Prompts.** Write one file per plate in `$D/prompts/` (`cover-a.txt`, `cover-b.txt`,
   `slide-NN.txt`), in the worked example's order:
   - opening line: slide N of T, 4:5, 1080 × 1350
   - "one lesson: …"
   - references, in attachment order
   - the SYSTEM block, verbatim (with `{{BRAND}}` and `{{MONTH_YEAR}}` resolved)
   - framing
   - the KEYING block, filled per zone with the aspect of the shot's focus box
   - the composition, top to bottom
   - "Visible copy, verbatim, with intended occurrence counts": exactly `strings[]`, minus what a
     capture or card supplies
   - the hygiene and key-colour negatives

   Interiors open with the locked cover as Image 1 ("match its visual system; its magenta is only a
   placeholder"). `cover-b` changes the composition only, staying inside the style.
3. **Jobs.** Write `$D/jobs-cover.json` and `$D/jobs-interiors.json` in the worked example's shape:
   - `deck`
   - `model` `gpt-6.1-sol`, `effort` `high`, `tier` `priority`, `concurrency`
   - `jobs[{id, prompt_file, refs, out}]`

   Cover refs are the 2 style references. Interior refs are `[final/cover-anchor.png, interior style ref]`.
4. **Cover.** Run `node shared/codex-img.mjs gen $D/jobs-cover.json` (2 variants in parallel). Composite
   both (steps 6–8).
   - Build a board: `node shared/codex-img.mjs board $D/runs/covers.jpg $D/final/slide-01-a.png=A $D/final/slide-01-b.png=B`
     (it creates the output folder).
   - **Claude picks** on phone legibility, focal image, verbatim text and clean zones. Copy the
     winner's **plate** to `final/cover-anchor.png` and its composite to `final/slide-01.png`, and log
     the reason.
   - Send the board with SendUserFile (proactive). Don't wait: the user can swap the cover at touch 2.
5. **Interiors.**
   - Run slide 2 alone first: `gen $D/jobs-interiors.json --only slide-02`. Inspect its style match,
     text and zones. Fix the shared prompt wording before the batch.
   - Then run the rest at concurrency 4: `gen $D/jobs-interiors.json --only slide-03,slide-04,…`.
   - A failed job reruns with `--only <id>`. If read-only blocks image generation, set
     `CODEX_IMG_SANDBOX=workspace-write`.
   - Plates are never overwritten; reruns land as `.v2`, `.v3`.
6. **Zones.** For each plate, run
   `python -I shared/composite.py $D/plates/slide-NN.png $D/runs/zones/slide-NN.zones.png --zones-only --report $D/runs/zones/slide-NN.json`
   and read each zone's id, aspect, fill and `out bbox`. A fill under 0.97 means something overlaps
   the zone: check the debug PNG.
7. **Cards** (exact text that must not be painted):
   - Put the HTML in `$D/cards/<name>.html`, starting from the worked example's
     `cards/prompt-card.html` (it fills the viewport and runs a fit pass).
   - Render at the zone's `out bbox`, ×2: `node shared/render-card.mjs $D/cards/<name>.html $D/cards/<name>-zone.png --w W --h H --scale 2 [--bg "#hex"] [--min-px N]`.
   - Exit 2 means the text overflows, or its measured size is below `--min-px` (default 14) and it
     prints `TOO SMALL`. Either way, cut copy; never lower `--min-px` to make a card pass.
   - Cards must be opaque, because `composite.py` flattens alpha onto white.
8. **Composite.** Run:
   ```
   python -I shared/composite.py $D/plates/slide-NN.png $D/final/slide-NN.png \
     --shot 1=$D/shots/<x>.png@x,y,w,h --card 2=$D/cards/<name>-zone.png --logo 1=$D/logos/<l>.png@0.9 \
     --dilate 3 [--letterbox paper] --report $D/runs/composite/NN.json
   ```
   - **Always pass a focus box.** Codex makes zones wider than asked (16:9 comes back about 2.1:1).
   - Use `--letterbox paper` for cream or light assets. The default `edge` suits dark captures.
   - `--logo` takes a PNG only (see step 1 for SVGs).
   - Exit 3 means leftover key colour or a zone with no asset. Assign the asset, or fix the plate
     with an edit job.
   - Plates with no zones still go through it, to fit 1080 × 1350.
9. **S01 only:**
   - Copy `templates/02-terracotta-zine/slides.html` to `$D/slides.html`, and the template's
     `assets/` folder to `$D/assets/` (the page loads `assets/bg-zine.png`).
   - In the copy, replace `{{BRAND}}` with `engine/brand.json` → `brand`, and `{{MONTH_YEAR}}` with
     the month and year of the folder's date (`OCTOBER ©2026`).
   - Set `slides[0].coverImg` to the composited cover, and fill each slide's `eyebrow`, `headlineHTML`,
     `body` and hero (`heroImg`: a capture or a rendered card PNG, with paths relative to `$D`) from
     `strings[]`. Only when the deck has its own `$D/heroes/*.html`, render them to
     `$D/assets/hero-<name>.png` with `node shared/render-heroes.mjs --carousel <id>` (without that
     folder the script renders the template's sample mocks, which never belong in a deck).
   - Optionally, the user tweaks in the browser first. If so, they copy the overrides with the tweak
     panel's Export button and paste the JSON in chat; write it into each slide's `defaults` before
     the bake, because the headless bake never sees the browser's localStorage.
   - Bake: `node shared/export.mjs --carousel <id>`. `--carousel` is required, and it bakes
     `carousels/<id>/slides.html`; if that file is missing it stops with an error (it falls back to a
     template only when you pass `--template <id>` yourself). It renders at 2× and writes 1080 × 1350
     PNGs to `$D/exports/slide-NN-YYYY-MM-DD.png`; `--native` keeps 2160 × 2700. Exit 2 means a
     visible image failed to load; the message names the slide and the `src`.

## Stage 5: QA and ship (touch 2)

1. **Independent QA.** Spawn parallel general-purpose subagents in one message. The worked example
   used 5 agents with 2 slides each. The author never QAs their own slides.
   - Each agent gets the final PNG, its plate, its composite report, the slide's `storyboard.json`
     entry (strings, lesson, evidence) and the style block.
   - Each returns `{n, verdict: ok|minor|fail, phone_readable, notes, defects[{severity: minor|major, kind, where, detail, fix}]}`.
   - They check:
     - every string verbatim, with the right count
     - no invented text, marks or duplicate labels (Codex habit)
     - leftover key colour, fringe and seams (zoom in)
     - the capture matches `describe` (truth)
     - margins of at least 5%
     - readable at 360 px wide
     - consistent with the anchor
     - no faces or webcam bubble
     - no drift from the storyboard

   Merge the results into `$D/runs/qa-v1.json`. There's no OCR: reading the images is the text check.
2. **Fix by kind:**
   - **Plate defects** (text, invented mark, layout) get an edit job: `prompts/edit-slide-NN.txt`.
     Write "Edit Image 1 … The only change: … Keep everything else exactly as it is:", then list every
     string and zone, then "Do not add any new text or elements." Refs are `[plates/slide-NN.png]`, the
     plate as ref #1, and `out` is the same path (it auto-versions). Batch them in `jobs-edits-N.json`.
     Keep one change per edit where possible. Then re-zone and re-composite.
   - **Composite defects** (crop, fringe, letterbox): change the focus box, `--dilate` or `--letterbox`
     and re-composite. No generation needed.
   - **Story or copy defects** go back to stage 2/3. Never fix them with a new render round.

   Re-QA only the changed slides (`qa-v2.json`). If any string changed, rerun
   `node shared/cold-reader.mjs $D/storyboard.json`.
3. **Export.**
   - Image-native: copy `final/slide-NN.png` to `exports/slide-NN-YYYY-MM-DD.png`, with the date from
     the folder name. S01 already exported at 1080 × 1350 in step 9.
   - Verify every export is 1080 × 1350.
   - Build the contact sheet:
     `node shared/codex-img.mjs board $D/contact-sheet.jpg $D/exports/slide-01-<date>.png=01 … --cols 5 --w 360 --title "<topic>"`.
4. **Caption.** Write `$D/caption.md` from `storyboard.caption`. It includes the source-video pointer
   when there is one and ends on `Comment KEYWORD`, the same keyword as the CTA slide.
5. **Touch 2.**
   - SendUserFile the contact sheet and the alternate cover composite.
   - Paste the caption.
   - Give the ship checklist: comment keyword wired in the user's DM automation (ManyChat or similar,
     if they use one), deliverable link live, facts re-verified today, the source video's description
     link correct (if there is one).
   - Report the run stats from `runs/runs.jsonl`: jobs, edits, wall time and tokens.
   - After the user approves, offer to prune the deck's Codex rollouts, which keep each image inline
     (about 13 MB per image). The thread ids are in `runs/runs.jsonl`. For each thread id the files
     are `$CODEX_HOME/sessions/**/rollout-*-<thread_id>.jsonl` and
     `$CODEX_HOME/generated_images/<thread_id>/` (`CODEX_HOME` defaults to `~/.codex`). Delete only
     those paths, and only with the user's OK.
6. **Learn.** After posting, log the deck in the user's own tracker: folder, cover and interior style,
   spine, hook formula, and the result once it settles. Never rewrite engine rules from one post (n=1).

## Batch mode

Use `/carousel batch`.

1. Take about 5 topics the user names, or from their own content plan if they keep one. Check
   `engine/brand.json` here, in the main session, and ask for the brand once if it's still
   `YOUR BRAND`, before any subagent starts.
2. Give each topic a posting day so that no two same-format decks land within 72 h and no style repeats
   inside its cooldown (the worked example doesn't count). Date each `$D` by its posting day.
3. Run stages 0–3 for each deck: one general-purpose subagent per deck, in parallel, each pointed at
   this file and its `$D`. Each one stops after writing `brief-card.md`.
4. Check the set together: formats, styles and keywords spread out, and every deliverable exists or is
   flagged.
5. Send one message with the 5 brief cards in posting order, plus their style crops. The user approves
   the whole batch in one sitting.
6. On later days, `/carousel make <deck>` runs stages 4–5 for one approved deck.

## Where things live

| What | Path |
|---|---|
| Data contract | `engine/storyboard.schema.json`; the worked example's `storyboard.json` as a full example |
| Codex worker notes | the header comment of `shared/codex-img.mjs` |
| Spines + gates, hooks, templates | `engine/spines.md`, `engine/hooks.md`, `engine/templates/{dossier,brief-card}.md` |
| Cold reader | `engine/cold-reader-prompt.md`, `engine/cold-reader.schema.json`, `engine/cold-reader-judge.schema.json` |
| Brand name | `engine/brand.json` (`{{BRAND}}` in the style blocks and the S01 template; `{{MONTH_YEAR}}` comes from the deck folder's date) |
| Styles | `engine/styles/styles.json`, `README.md`, `exemplars/`, the `<id>-*.prompt.md` blocks (S01–S03, S05–S09, S11), refs in `engine/styles/refs/`, card kits in `engine/styles/kits/<id>/` |
| Tools | `shared/codex-img.mjs`, `cold-reader.mjs`, `brief-card.mjs`, `build-gallery.mjs`, `build-style-library.mjs` (a browsable HTML page of the library), `shots.py`, `composite.py`, `render-card.mjs`, `lucide-icons.mjs` (+ `vendor/lucide/`), `pose-check.py` (optional, your own mascot), `export.mjs` and `render-heroes.mjs` (HTML-template decks) |
| Interior renderers | `templates/02-terracotta-zine/` (S01), `templates/01-graph-paper-cream/` (S06) |
| Worked example | `carousels/2026-10-14-claude-video-free/` |
| Logos | the user's own logo files or simple-icons SVGs, as PNGs in `$D/logos/` |

This skill replaces the older `ref-deck` skill (github.com/cth9191/ref-deck), which built decks a
different way. Notes that say "ref-deck vN" mean decks made with that older method, not this one.
