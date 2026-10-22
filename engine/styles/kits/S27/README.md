# S27 Icon-Grid Cheat Sheet: card kit

Starter pages for both S27 formats (spec: `engine/styles/S27-icon-grid-cheat-sheet.prompt.md`). Every page
is HTML; Codex paints nothing and `composite.py` never runs. The kit mirrors a deck folder, so the
relative paths (`../logos/`, `../shots/`) work unchanged once copied.

| Path | What it is |
|---|---|
| `cards/s27.css` | Tokens and components: crown, hook + count pill, grid (5x2, 4x2, 3x2, and 3-row 3x3 / 4x3 with the icon left of the name), tile (badge, icon, ink monogram, name, lines, GitHub chip or docs chip), byline foot, counter, item page, combo, CTA |
| `cards/onepager-10.html` | **One-pager**, 10 tiles at 5x2 (the single-image format) |
| `cards/onepager-12.html` | **One-pager**, 12 tiles at 4x3, icon left of the name; tile 12 shows the docs-domain chip for a hosted product with no repo |
| `cards/page-01.html` | **Carousel cover**: the one-pager layout with 6 tiles (3x2) and "01 / TT" |
| `cards/page-02.html` | **Item** (the tile, opened), an item with no mark: ink monogram icon |
| `cards/page-03.html` | **Item**, an item with a real mark |
| `cards/page-08.html` | **Combo** (N ≤ 7): two half-opened tiles + "+", the ink prompt card, one caption |
| `cards/page-09.html` | **CTA**: the cover grid at 70% (icon + name), "Want all N links?", Comment + keyword pill, deliverable |
| `logos/` | Sample marks (Claude, Anthropic, OpenAI, GitHub as SVG + PNG); `github.svg` is GitHub's simple-icons path and `github-ink.png` its render (`node shared/render-card.mjs engine/styles/kits/S27/logos/github.svg engine/styles/kits/S27/logos/github-ink.png --w 512 --h 512 --scale 1`). Your own marks come from your logo folder or simple-icons |
| `shots/` | Placeholder captures: replace with each item's real README / UI / terminal capture |
| `samples/` | Every page rendered (exit 0 each), with `{{BRAND}}` filled as `YOUR BRAND` |

The byline foot is `<span class="avatar"></span><b>{{BRAND}}</b>` plus a month stamp. The avatar span is a
neutral dashed circle; on a deck, replace it with your square profile photo
(`<img src="../logos/avatar.png" alt="">`, styled by `.foot img`) and replace `{{BRAND}}` with the `brand` in
`engine/brand.json`.

Sample repos are real; their stars were read with `gh api repos/<owner>/<repo>` when the kit was built
(item pages only). Re-check every name, owner/repo and star count on posting day.

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/logos $D/shots $D/exports
cp engine/styles/kits/S27/cards/* $D/cards/
cp engine/styles/kits/S27/logos/{claude-orange.png,github-ink.png} $D/logos/   # + your avatar.png and each item's mark
# carousel: page-01 (cover), one item page per tile in cover order (copy page-02/03 to page-02..NN),
# optional combo at n-1, CTA last; renumber badges, mini-map cell and "NN / TT"; replace every string
node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --bg "#FBF8F3" --min-px 15
node shared/render-card.mjs $D/cards/page-NN.html $D/drafts/slide-NN@2x.png --w 1080 --h 1350 --scale 2 --bg "#FBF8F3" --min-px 15   # zoom QA
```

Grid class by N: 6 → `grid c3`, 8 → `grid c4`, 10 → `grid c5`, 9 → `grid r3 c3`, 12 → `grid r3 c4`.
Item icon: `<div class="icon"><img src="../logos/x.png"></div>` (add `class="fill"` on the img for an
avatar or full-bleed app icon); no mark: `<div class="icon mono">X</div>`. Hosted product with no repo:
the chip shows the link glyph and its docs domain (see tile 12 in `onepager-12.html`).

## Fit and limits (measured on the kit)

Every tile is `[data-fit]`, so a tile that overflows fails the render (exit 2). At 5 columns:
- a tile holds a 1-line name plus 3 lines of description, or a 2-line name plus 2 lines;
- a single heavy word wider than about 155 px fails ("Superpowers" just fits);
- each owner/repo half fits 16 mono characters.
At 4x3 (icon left) a single word beside the icon fits about 9 heavy characters ("Superpowers" fails
there; pick another layout or a shorter display name) and owner/repo halves fit about 20 characters
("modelcontextprotocol/" fails). The hook fits 9 words on 3 lines at 92 px; it shrinks to 64 px before
failing. Item pages: name one line (88 → 56 px), what ≤ 18 words (2 lines at 36 px), Replaces ≤ 8 words,
Use it for ≤ 10 words (2 lines each). Combo prompt: mono 34 px, about 4 lines.
