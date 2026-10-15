# Template 02 — Terracotta Zine

The HTML renderer for style S01 (`engine/styles/S01-terracotta-zine.prompt.md`). Codex paints only
the cover plate; every interior slide bakes from a deck's copy of this `slides.html`. This file is
template-specific.

## Using it in a deck

The /carousel skill does this at Make (S01 only). Do the same by hand for a deck made without it.

1. **Copy.** `slides.html` goes to `carousels/<id>/slides.html`, and this folder's `assets/` files go
   to `carousels/<id>/assets/`. The page loads `assets/bg-zine.png` relative to itself, so a deck
   with no `assets/` folder bakes with no ground.
2. **Placeholders.** The meta strip holds the only two:
   - `{{BRAND}}`: `brand` from `engine/brand.json`
   - `{{MONTH_YEAR}}`: the month and year of the deck folder's date, e.g. `2026-10-14-…` →
     `OCTOBER ©2026`
3. **Slides.** Replace the sample `slides[]` with the deck, one entry per slide, filled from
   `storyboard.json` → `strings[]`:
   - Cover: `cover: true` and `coverImg: 'final/slide-01.png'` (the composited cover). While
     `coverImg` is empty, the cover renders as a typographic slide from its own fields. That is a
     preview, not a cover.
   - Body slides: `eyebrow`, `headlineHTML` (the accent phrase in `<span class="accent">`), `body`
     (1-3 `<strong>` accents) and `heroImg`.
   - `heroImg`: a real capture (`shots/…png`) or a card PNG rendered with `shared/render-card.mjs`,
     relative to the deck folder. `assets/hero-placeholder.png` only marks where a capture goes:
     replace every one before the bake. An empty `heroImg`, or `noHero: true`, hides the hero.
   - `defaults`: the sizes and positions the bake uses (see the tweak loop).
4. **Bake.** Run `node shared/export.mjs --carousel <id>`. It renders at 2x and writes 1080×1350 PNGs
   to `carousels/<id>/exports/slide-NN-YYYY-MM-DD.png`; `--native` keeps 2160×2700. If any visible
   image failed to load, it exits 2 and names the slide and the src.

## Tweak loop (optional)

Open the deck's `slides.html` in a browser. Arrow keys or the bottom buttons move between slides,
and `F` toggles fullscreen. The **Tweaks** button (top right) opens the panel:

- **Global:** accent color
- **Per-slide:** eyebrow text, headline HTML, body HTML, headline size, body size, body top
  position, hero image src, hero bottom, hero width, hero tilt

Tweaks save to localStorage under keys namespaced by the page's path, so two decks open in the same
browser keep separate tweaks. The bake runs a fresh browser and never sees localStorage. Before
baking, click **Export tweaks (copy JSON)**, paste the JSON in chat, and write each value into that
slide's entry: sizes into `defaults`, text into `eyebrow` / `headlineHTML` / `body` / `heroImg`,
and a changed accent color into `GLOBAL_DEFAULTS.accent`.

Tweak chrome CSS comes from `shared/tweak-panel.css`. Don't redefine `.tw-*` rules in the template.

## What this is for

Step-by-step explainers and process carousels. Body slides carry more text than a data-card list
layout, so the layout favors sticker-collage composition over dense data cards.

**Fits:**
- System builds: "Build X in 3 steps" (spine D)
- "How [system] works" walkthroughs (spine A)
- "Stage 1 / Stage 2 / Stage 3" frameworks
- A concept slide followed by a concrete example slide

**Doesn't fit:**
- Pure top-N tool roundups (use a list-first style instead)
- Visual-light essays (no hero asset looks empty)
- Quote roundups

## Visual DNA

- **Ground:** terracotta texture (`assets/bg-zine.png`), full-bleed on every body slide. Owning the
  color across the swipe is the brand move.
- **Cover:** a Codex plate painted from the SYSTEM and COVER blocks of the S01 prompt: terracotta
  ground, massive white headline, black brush band, dark app windows as stickers. The windows are
  magenta zones and the sticker's logo slot is a cyan zone; `shared/composite.py` fills them with
  real captures and a real logo file. Logos are composited, never painted.
- **Meta strip:** mono `{{MONTH_YEAR}} · {{BRAND}} · NN / TT` at the top.
- **Eyebrow:** small white caps inside a slightly rotated black brush badge
  (e.g. `STEP 1 / SOURCES`).
- **Headline:** lowercase Inter Black 84-160px, line-height ~.92, with the accent color (ink
  `#0E0E0E` by default) on the key phrase. Seven words or fewer.
- **Body:** Inter 600 ~43px, cream `#F5EBE0`, with 1-3 `<strong>` words in the accent color.
- **Hero:** a capture styled as a sticker: 4px cream border, rounded corners, drop shadow, slight
  tilt, cream tape at top-left and bottom-right.
- **Footer:** `NN / TT` bottom-left, `SWIPE →` bottom-right. The counter is computed from the real
  slide count.

## CTA slide

One action: `Comment KEYWORD` plus the deliverable. The sample body is
`Comment <strong>KEYWORD</strong> and I'll send you <strong>the full setup</strong>.`: put in the
deck's keyword, the same one as in the caption and your comment-to-DM automation, and name what they
get. Save, follow and share asks, and any link, go in the caption, never on the slide.

Set `noHero: true` and `heroImg: ''`. A big stacked headline (`headSize` ~150) with the body under it
(`bodyTop` ~760) makes the slide read like a poster.

## Sizing rules of thumb

- Slide count follows the spine; 9 (cover + 7 body + CTA) fits a 3-step system build.
- Body font 32px is too sparse. **43px is the sweet spot** for an IG carousel.
- Body top **340-450** reads well under a two-line headline. Check that the body ends above the hero.
- Hero width: **880px** gives a full-bleed feel for wide screenshots; **600-700px** suits 4:3
  captures like the placeholder; **400-600px** floats square or portrait art as a sticker.
- Hero tilt: **-1.5°** is subtle, **-12°** is playful. Vary it per slide for rhythm.
- Bold accent words in the body: 2-3 per slide at most, in the same color as the headline accent.

## heroes/ (optional sample mocks)

`heroes/` holds standalone HTML mocks (an intro and seven steps of a design-to-deploy walkthrough).
They are illustrative reference compositions, not real product UI. The /carousel skill runs
`shared/render-heroes.mjs` only for a deck's own `heroes/` folder and never uses these samples. To
render them into a deck as a starting point:

```bash
node shared/render-heroes.mjs --carousel <id> --template 02-terracotta-zine
```

It reads `carousels/<id>/heroes/*.html` if the deck has that folder, otherwise this template's, and
writes `carousels/<id>/assets/hero-<name>.png` at 3200×2000. Edit the HTML for the deck's content
first. A mock explains; it never stands in as proof.
