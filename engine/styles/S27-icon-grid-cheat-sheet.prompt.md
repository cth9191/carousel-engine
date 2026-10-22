# S27 Icon-Grid Cheat Sheet: prompt block

A save-and-zoom cheat sheet, from a layout studied from a high-performing post. Keep its
system: a small two-logo equation crowning a heavy count hook, over a numbered grid of N identical
tiles (icon, name, one line, repo chip). Never copy any reference post's characters, art, words, hook,
CTA phrasing, item set, order or blurbs, or signature palette; only the layout vocabulary carries over.

One system, two formats. The **one-pager** is the whole post, the grid is the payoff, and saves are
the mechanic. In the **carousel** the same page is the cover, each tile opens into an item slide, and
a CTA closes it.

**HTML-native, no template.** Every page is a per-deck HTML card. Codex paints nothing: the look is
flat vector UI with no texture or illustration, and everything on it that matters is exact text or a
real mark. A painted variant needs the user's OK (see KEYING).

## Production split

| Element | Made by |
|---|---|
| Every page: ground, crown "+", hook, pill, tiles, badges, names, lines, chips, byline, counter | **HTML** `$D/cards/page-NN.html` filled from `strings[]`, rendered with `node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-<date>.png --w 1080 --h 1350 --scale 1 --bg "#FBF8F3" --min-px 15`. Add a `[data-fit]` pass so any overflow fails the render, and render once at `--scale 2` into `drafts/` for zoom QA |
| Crown tiles, tile icons, GitHub mark | Real files in `$D/logos/` as `<img>` (contain). Use the host mark from your logo folder, the project's own README logo or its owner's GitHub avatar, or a simple-icons SVG via render-card's SVG mode. With no mark, use an ink monogram tile (cream initial). Never painted or generated |
| Item proof | A real README, UI or terminal capture (a browser screenshot tool, playwright-cli or `shots.py`) as an `<img>`, focus-cropped |
| Byline avatar | Your square profile photo (`$D/logos/avatar.png`), or your logo mark; the kit ships a neutral placeholder circle |

Start from `engine/styles/kits/S27/cards/` (one-pagers at 10 and 12 tiles, the carousel cover, item,
combo and CTA pages, `s27.css`) or the last S27 deck's cards, and replace every string. The chip may
borrow the `.repo-card .top` layout from `templates/01-graph-paper-cream`, recoloured to the chip greys
(no #0969DA blue). An independent QA agent reads each export against `strings[]` and the live repo,
checking names, owner/repo and stars letter by letter, and confirms each icon file belongs to its repo.

**Budgets.** Hook: 9 words or fewer on 3 lines or fewer, with one pill phrase holding the count. Tile:
a name of 3 words or fewer (16 characters or fewer), one line of 7 words or fewer in your own words
(never the README tagline or a reference's blurb), and `owner/repo` verbatim, wrapping after the
slash. At 5 columns each half must fit 16 characters; if one doesn't, use 4×2 or 3 rows. A hosted
product with no repo shows a plain ink link glyph and its docs domain instead of the GitHub mark.
Grid: 6 = 3×2, 8 = 4×2, 10 = 5×2; 9 and 12 use 3 rows with the icon left of the name. Carousel: N is 8
or fewer, so the deck stays at 10 slides or fewer.

**Measurements** (1080 × 1350): margins 60 px at the sides, 48 at the top. Crown: two 160 px tiles
around a 56 px "+", y 48–208. Hook: max 92 px, auto-fit, y 236–520. Grid: x 60–1020, 16 px gaps, y
556–1248 (a 5×2 tile is 179 × 338). In each tile: a 34 px badge, an 80 px icon (88 px at 4 columns or
fewer), a 24 px name, 18 px lines, and a 15 px mono chip. Byline: y 1270–1318.

## SYSTEM

Visual system: a clean one-page cheat sheet, like a printed app-store shelf. Flat warm-white ground
(#FBF8F3) with no grain, grid, gradient or texture.

Type: a heavy geometric grotesk (like Inter Black) for the hook, names and item headlines, ink
#0E0E0E, title case, tracking -0.03em, the hook centred. One phrase per page, the count phrase, sits
in a solid Claude-orange (#D9551F) capsule pill with white type, the pill about 1.2 times the cap
height. Tile lines use a regular grotesk in warm grey (#5E574F). Owner/repo, the month stamp and the
counter use a monospace (like JetBrains Mono, #6E675E).

Tile: the repeating unit, a white (#FFFFFF) card with corners rounded about 2% of the width, a 1 px
warm-grey border (#E6DED3) and a short soft shadow (6% ink, 18 px blur). Every tile on a page is the
same size, on one grid. Inside, left-aligned from the top:
- an orange circle badge with cream two-digit numerals ("01")
- a rounded-square app icon, always a real mark
- the name in the heavy grotesk
- one to three warm-grey lines
- a pale inset chip (#F4EEE6) holding the GitHub mark, "GitHub" in semibold, and the owner/repo in
  mono, broken after the slash

Crown: two app-icon tiles of equal size side by side, joined by a heavy ink "+", centred above the
hook. Brand colour comes only from the real logos; nothing around them is tinted to match.

Foot: a small circle avatar, "{{BRAND}}" in bold grotesk and a mono month stamp ("Oct 2026"), centred.
On carousel slides, add "NN / TT" in small warm-grey mono at the bottom right.

Orange appears only on the pill, the badges, the item rule, the mini-map cell and one optional accent
word. No gradients, glow, 3D, illustration, mascot, handwriting, stickers or tape.

Framing: a uniform margin of at least 5.5% of the width at the sides and 3.5% of the height top and
bottom, and tiles 1.5% apart. Shrink before crowding. Text floors: tile lines 18 px, chips 15 px,
names 24 px. That is save-and-zoom size, below the usual 1/40 floor, which a one-page cheat sheet
needs. Carousel interiors, where each item is actually read, keep body text at least 1/40 of the
height (34 px).

Hygiene: render only `strings[]`, verbatim and exactly as often as specified. Identifiers keep their
real case (owner/repo, CLAUDE.md, /command). No URLs beyond owner/repo or a docs domain, no star count
without a posting-day check, no "Follow … for more", and no handles, watermarks or lorem ipsum.

## COVER

The one-pager and the carousel cover are the same page, centred, top to bottom:

1. **Crown** (12% of the height): "{host}" tile + "+" + "{source}" tile, for example Claude Code +
   GitHub, Claude Code + MCP or Codex + skills. It names the ecosystem the list lives in, not two tools
   being wired together (that is S02).
2. **Hook**: two or three lines as wide as the margins allow, "{hook}", with "{count phrase}" in the
   pill. Use a count formula from `engine/hooks.md` (F5, F8, F9), never a reference post's hook line.
3. **Grid** (about 51% of the height): N tiles numbered 01–N in deck order. That order is the
   storyboard's sort (newest stars, setup order, most used), stated in the caption or in `why`.
4. **Foot**: the byline. Its month stamp is spine C's cover stamp. On the carousel cover, also add
   "01 / {TT}".

There is no comment ask on the cover (spines.md). On a one-pager, the caption carries "Comment
{KEYWORD}" for the links.

## INTERIOR

Carousel only. Paste the one layout the slide uses.

**Item (default: the tile, opened).** The top row has the item's badge ("03") at the left and a mini
map at the right: the cover's grid as N small rounded cells, the current one orange and the rest
#E6DED3. The hero row has the real icon (168 px) at the left. To its right, "{name}" in the heavy
grotesk (one line, 88 px max, auto-fit) sits over the chip, which holds owner/repo and "★ {stars}",
checked on posting day. Then "{what}" in ink, 18 words or fewer. Then a white tile about 960 × 500 px
holding one real capture. Then two rows, each a short orange rule plus a semibold label: "Replaces"
with "{8 words or fewer}", and "Use it for" with "{10 words or fewer}". Foot.

**Combo (optional, when N is 7 or fewer).** At the top, "{headline}", 7 words or fewer. Below it, the
two items' tiles half-opened (badge, icon, name), side by side and joined by the crown's heavy "+".
Then one ink card (#141414, cream JetBrains Mono, 28 px or larger) holding the exact prompt or command
that combines them, and one caption line naming the result. Foot.

**CTA.** At the top, the cover's grid at 70% scale, each tile icon and name only. Below it, "Want all
{N} links?" in the heavy grotesk, then "Comment" with "{KEYWORD}" in the orange pill, then
"{deliverable}" in 10 words or fewer. Foot. This is the deck's one action: no "save", no
"follow".

## KEYING

None by default. Nothing is painted, so pages carry no key colours and `composite.py` never runs.

If the user approves a painted variant, the plate keeps this layout with two kinds of zone:
- each tile face is ONE flat magenta #FF00FF rounded rectangle at the tile's aspect, filled by an
  HTML tile card through `--card`
- each crown tile is ONE flat cyan #00FFFF rounded square, filled through `--logo`

Every zone has clear warm white around it. Codex paints only the ground, hook, pill and "+", and
Claude checks them against `strings[]`.

Either way, no purple, violet, pink or magenta appears outside a zone. The pill is solid #D9551F, a
warm red-orange, never pink and never a gradient. No cyan or turquoise appears outside a zone. Real
logos are exempt: a pink or teal app icon is placed as an `<img>` and never sits in a plate.
