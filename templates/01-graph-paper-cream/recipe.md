# Template 01 — Graph Paper Cream

The HTML renderer for style S06's interiors (`engine/styles/S06-statue-graph-paper.prompt.md`): Codex paints only
the statue cover plate, and every other slide bakes from a deck's copy of this `slides.html`.

## Using it in a deck

1. **Copy.** `slides.html` goes to `carousels/<id>/slides.html`. Copy `assets/hero-placeholder.png` too only while
   you still have placeholder slides; `assets/cover.png` is the template's own sample cover, never a deck's.
2. **Placeholder.** `{{BRAND}}` is the only one: the CTA's handle pill (`ctaHandle` and its fallback). Replace it with
   your handle or the `brand` in `engine/brand.json`. `export.mjs` warns if a slide still shows it.
3. **Slides.** Replace the sample `slides[]` with the deck, one entry per slide, from `storyboard.json` → `strings[]`
   (schema below). Cover: `coverImg: 'final/slide-01.png'`, the composited S06 cover.
4. **Bake.** `node shared/export.mjs --carousel <id>` renders at 2x and writes 1080×1350 PNGs to
   `carousels/<id>/exports/slide-NN-YYYY-MM-DD.png` (`--native` keeps 2160×2700). It exits 2 if a visible image failed
   to load and 3 if the keyword CTA can't fit (the fit pass names the slide).

`node shared/export.mjs --carousel <id> --template 01-graph-paper-cream` bakes the template's own sample slides into
a deck folder that has no `slides.html` (a preview, nothing more).

## What this is for

Editorial list carousels where each slide shows one tool, skill or framework with its real GitHub repo or product
screenshot.

Fits:
- "Top 5 Claude Code skills"
- "5 frameworks I'd build with this year"
- "5 MCP servers that changed my workflow"

Doesn't fit:
- Personal essay / story carousels (too text-heavy)
- Process tutorials (they need step diagrams; see Template 02 / S01)
- Quote roundups (no hero images)

## Visual DNA

- **Ground:** cream `#F5EBE0` + 60 px graph-paper grid (ink at 14% opacity)
- **Mark:** terracotta `#D97757` bookmark ribbon, top-left
- **Headline:** Inter 800, ~80 px, ink, terracotta accent on the item name
- **Hero block:** full-bleed capture inside a rounded card, layered with a white repo-card overlay
- **Body line:** Inter 800 40 px, ink, with a terracotta `→`
- **Counter:** `NN / TT` top right on every slide but the cover (from `slides.length`)
- **CTA:** keyword mode (`→ COMMENT` / `KEYWORD` / what they get) and a black handle pill

## Production rule

Cover = the S06 Codex statue plate + `kits/S06/tile.html` + `kits/S06/cover.html`. Value heroes = real captures or
HTML compositions, never AI-generated: AI heroes look generic, mangle typography, drift on re-renders and can't be
iterated cleanly. If someone proposes an AI hero for a value slide, push back.

### Value heroes, in priority order

**Path A, real product assets** (preferred when the item has a real UI)
- The maintainer's banner or screenshot in the README, then `https://opengraph.githubassets.com/1/owner/repo`, then the
  product site. Save it locally as `carousels/<id>/assets/hero-<item>.png` (never hotlink: the bake must not depend on
  the network).
- For a local tool with no public repo, a real screenshot of what it operates on.

**Path B, an HTML hero composition** (for abstract or multi-source items)
- A standalone HTML page in the deck's own `heroes/` folder, real logos only (simple-icons marks), the template's
  palette, JetBrains Mono for code, Inter for labels.
- Render with `node shared/render-heroes.mjs --carousel <id>` (it reads the deck's `heroes/*.html`) →
  `carousels/<id>/assets/hero-<name>.png`. This template ships no sample heroes.

Pitfalls: GitHub OG cards bake in the owner's avatar; use the template's repo card instead, or hide the card
(`cardOn: false`). Crop captures tight and clear of avatars and faces (contributor and commit rows carry them).

## Tweak loop (optional)

Open the deck's `slides.html` in a browser. Arrow keys or the bottom buttons move between slides, `F` toggles
fullscreen. **⚙ Tweaks** (top right) opens the panel:

- **Global:** background pattern, density, opacity, accent colour, headline size
- **Per-slide:** show repo card, card X / Y / width / tilt, headline, body line, repo description; drag the card to move it

Tweaks save to localStorage under keys namespaced by the page's path. The bake runs a fresh browser and never sees
them: click **📋 Export tweaks**, paste the JSON in chat, and write each slide's values into its `defaults`
(`cardOn`, `cardX`, `cardY`, `cardW`, `tilt`) and its text fields, and the global values into `GLOBAL_DEFAULTS`.

## Lessons specific to this template

- **Per-slide `cardOn: false`** hides the repo card where it adds noise (a text-heavy hero).
- **Headline accent:** when the slide's `name` appears in a headline edited in the panel, it is wrapped in `.accent`.
- **Card drag uses `--card-x` / `--card-y`** (left + bottom anchored), so the Y math is inverted for drag.
- **Pagination dots are hidden**: Instagram and TikTok add their own.
- **Showcase images can carry someone else's brand.** Prefer an infographic or a product screen over a cover that
  reads as another company's branding.

## Known pitfalls

- **`let i` block scoping:** the export calls `window.goSlide(idx)`; calling `render(idx)` directly doesn't update
  the script's own `i`, so per-slide tweaks load for the wrong slide.
- **GIF heroes don't export cleanly:** use static images or a first frame.
- **Font:** Inter stands in for Söhne; license Söhne (or use General Sans) for an exact match.

## Slot reference (slides[] schema)

### Cover
```js
{ name: 'Cover', cover: true, coverImg: 'final/slide-01.png', slideIndex: 0 }
```

### Value (layered)
```js
{
  name: 'ItemName',
  headlineHTML: '#1: <span class="accent">ItemName</span><br>does the thing<br>everyone wants',
  layered: true,
  heroBg: 'assets/hero-item.png',
  repoCard: {
    owner: 'github-owner',
    name: 'repo-name',
    title: 'repo-name',
    desc: 'One-line description.',
    lang: 'TypeScript',
    langColor: '#3178c6',
    stars: '1.2k', // verified on posting day
  },
  body: 'Body line that ends with the terracotta arrow',
  slideIndex: 1,
  defaults: { cardX: 24, cardY: 40, cardW: 44, tilt: 0, cardOn: true },
}
```

### Single image (no repo card)
```js
{ name: 'Why', headlineHTML: '…', heroImg: 'assets/proof.png', body: '…', slideIndex: 2 }
```

### CTA (keyword mode)
```js
{
  name: 'CTA',
  cta: true,
  ctaHeadline: 'WANT<br>ALL 5?',   // optional
  ctaKeyword: 'KEYWORD',
  ctaDeliverable: 'I’ll send you all 5 with install links.',
  ctaHandle: '{{BRAND}}',
  slideIndex: 6,
}
```
Without `ctaKeyword`, the legacy `ctaActions` list (`[{ marker: '→', text: 'Save' }, …]`) renders instead.

## File map

```
01-graph-paper-cream/
├── slides.html        # the editable template (sample slides with placeholder copy)
├── assets/
│   ├── cover.png              # sample statue cover (the S06 smoke test), for the preview only
│   └── hero-placeholder.png   # marks where a capture goes
├── manifest.json      # machine-readable metadata
├── recipe.md          # this file
└── preview.png        # for the picker grid
```
