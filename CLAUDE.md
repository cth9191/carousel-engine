# Carousel Engine — notes for Claude

This repo makes Instagram/TikTok carousels (4:5, 1080 × 1350). Everything runs through the project
skill **`/carousel`** (`.claude/skills/carousel/SKILL.md`). Read it before starting any deck.

## How a deck gets made

- **Text first.** Topic, hook, storyboard, CTA keyword and style are decided in text and shown to the
  user as one **brief card**. No image is generated before the user approves it.
- **Two touches from the user:** the brief card, then the final contact sheet.
- **Pixels:** headless Codex workers (`shared/codex-img.mjs`) paint plates with flat magenta/cyan
  zones. Real screenshots, logos and exact text are composited into those zones
  (`shared/composite.py`, `shared/render-card.mjs`). The model never draws a logo or a long string.
- **QA:** independent agents check every slide against `storyboard.json`.

Modes: `/carousel <topic | YouTube URL | repo | docs>`, `/carousel batch` (about 5 brief cards at
once), `/carousel make <deck>` (build an approved deck).

## Layout

| Path | What |
|---|---|
| `engine/` | Story spines + gates, hook bank + rubric, storyboard schema, cold-reader prompts, brief-card and dossier templates, `brand.json` |
| `engine/styles/` | Style library: `styles.json`, one prompt block per style, exemplars, pick-sheet gallery |
| `shared/` | The tools. Extend these; never write one-off scripts into a deck folder |
| `templates/02-terracotta-zine/` | HTML interiors for style S01 |
| `carousels/YYYY-MM-DD-slug/` | One folder per deck. `carousels/2026-10-14-claude-video-free/` is the worked example |
| `docs/how-it-works.md` | The method and the lessons behind it |

## Rules

- **Brand.** `engine/brand.json` ships with `"brand": "YOUR BRAND"`. If it still says that (or the
  value is missing), ask the user for their brand name and write it there before writing any prompt.
  Style prompt blocks and the S01 template use `{{BRAND}}` for it and `{{MONTH_YEAR}}` for the deck
  folder's month and year (`OCTOBER ©2026`); replace both when you write prompts or copy the template
  into a deck.
- Deck folders are dated today (or the planned posting day in batch mode), never a past date.
- The worked example (`carousels/2026-10-14-claude-video-free`) ships with the repo: ignore it for
  style cooldown, 72-hour spacing and folder-collision checks.
- Every visible string lives in `storyboard.json` → `strings[]` before any prompt is written. The
  `place` values `headline`, `counter` and `chrome` are reserved.
- A story or copy change after rendering goes back to the storyboard and brief card, never into
  another image round.
- Never switch to a different image generator without asking the user.
- Exports are 1080 × 1350 PNGs named `exports/slide-NN-YYYY-MM-DD.png`, with the date from the folder
  name. For S01, `node shared/export.mjs --carousel <id>` writes them (`--native` keeps 2160 × 2700).
