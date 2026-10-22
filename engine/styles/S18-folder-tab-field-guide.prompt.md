# S18 Folder-Tab Field Guide: prompt block

Reusable visual-system text for Codex image prompts. A friendly illustrated field guide: a cover map
of an invented island pinned to round medallions, then folder-tab interiors with three painted scene
bands, one entry per band. The layout vocabulary was studied from a high-performing carousel; never
copy any reference deck's characters, art, words, hook, CTA phrasing, item set or signature palette.
Only the layout vocabulary carries over.

**Hybrid.** Per job paste SYSTEM, the one EMBLEM SHEET, COVER or INTERIOR sub-block, and KEYING
(emblem sheet: KEYING's last paragraph only). Delete unused *(optional)* lines: every painted zone
needs an asset or `composite.py` exits 3. One face type per deck, never mixed: an emblem deck takes
every face from one Codex emblem sheet (real marks go in the band cards), a logo deck from HTML face
cards. Order: face set, cover, first three-band page, the rest.

**References.** This style ships no reference images. Until the user approves a first plate, every
Codex job is **text-only**: SYSTEM, the layout sub-block and KEYING carry the whole look, with no
image attached. Once the cover is locked, attach it as Image 1 for the cover and CTA; once the first
three-band page is locked, attach it as Image 1 for every other interior. Codex never receives an
unmasked or partially masked third-party slide. The emblem sheet takes no references: drop SYSTEM's
References paragraph.

## Production split

Codex paints every plate; the table lists the rest. The card kit is `engine/styles/kits/S18/` (copy
the files into `$D/cards/`, edit each file's JSON; its README has every command); kit specs (fonts,
sizes, word caps) are in `requires` in `styles.json` and the cards enforce them.

| Element | Made by |
|---|---|
| Emblem deck faces | Codex sheet, locked before the cover (the only painted faces), disc-cropped into `emblems/NN.png` by `shared/shots.py` (spec entry `{"name": "{nn}", "image": "<deck>/emblems/sheet.png", "discs": "auto", "count": N, "size": 512}`). Never crop the cover: its 135-185 px faces upscale soft |
| Logo deck faces | kit `face-NN.html` as `cards/face-NN.html` via `render-card.mjs` at 300 x 300, 2x, no `--bg`, into `faces/NN.png` |
| Every medallion face | cyan disc, `composite.py --logo N=emblems/NN.png@1.0` (or `faces/NN.png`) after `--zones-only` maps C numbers to entries; never repainted |
| Tab row and `NN / TT` counter | kit `tabs-NN.html` as `cards/tabs-NN.html` (EXTRA lit on the EXTRA page) at the strip's `--zones-only` out bbox (2x), `--bg` = plate cream beside it; `--card` |
| Band text | kit `band-NN.html` as `cards/band-NN-B.html` at the well's out bbox, `--bg` = pool ink sampled just outside the well (never exactly #0E0E0E); `--card` |
| Subject mark | cyan rounded square, `--logo N=logos/x.png@0.8` |
| Proof (deep-dive, D steps) | magenta, `--shot N=shots/x.png@focus` (`--letterbox edge` if dark) |
| EXTRA prompt, D step command | HTML ink terminal card, `--card` |
| *(optional)* Your own mascot as an explorer with a map, cover only, for finding-your-way hooks | your own mascot (optional; transparent PNG poses you made, never a licensed character) via the cyan slot, `--logo`; never drawn. With no mascot, leave the slot out |

Cover copy caps: kicker 1-2 words; title 6 words, line 2 the count and outcome in 13 characters (spine
D: line 1 the system's name, line 2 "{N}-STEP BUILD" or the outcome); labels 12 characters; CTA line 8
words. Cover and CTA plates (about 4:5, 1122 x 1402) composite with `--fit pad`, so an aspect fix
extends the orange ground. Text QA reads interior text from the cards. Patch a failed cover label,
numeral or stamp with a cream `render-card.mjs` card at its bbox, pasted with
`composite.py final/slide-01.png final/slide-01.png --paste cards/fix.png@x,y,w,h,erase`; never
regenerate the cover. Every well keeps its pool: the cream band text needs the flat ink behind it,
whether the band card goes in opaque (`--bg` pool ink) or transparent with `--ground fill`.

## SYSTEM

Visual system: a friendly illustrated software field guide, flat and print-like as a printed brochure.
Palette: cream #F5EBE0, Claude orange #D9551F, ink #0E0E0E, cobalt #3D7DC8 (violet-leaning, never
teal), sage #7DAA5A (district edges #5C8A40), ochre #E3A33B, pale sand #D4C0A1.

Cover and CTA: a full-bleed orange ground with one cream panel inset about 2.5% of the width all
round, so the orange reads as a thin frame; panel corners rounded about 2%, no grain. Title in a
chunky rounded heavy display sans (like Nunito Black or Fredoka Bold), cobalt, with a hard pale sand
offset down and right like a sticker. Labels in cobalt bold grotesk caps (like Inter Bold). The kicker
is cream heavy caps in an ink rounded pill.

Interiors: under a plain cream top strip, three equal full-width bands run to the bottom edge, split
by thin cream hairlines. Each is a moody painted scene of that entry's job (say, a workbench under a
lamp) at about 55% brightness, deepening on its text side under a heavy dark gradient into a
soft-edged pool of flat, untextured ink #0E0E0E behind the text well; only the pool is flat. Scenes
use warm ambers, ochres, deep greens, slate #4A5560 and navy #2A3A55; water, glass and sky are slate
or navy. No screens, UI, people's faces or logos in any scene.

Medallions: perfect circles with a thick ink rim (about 7% of the diameter, one small rounded notch at
the bottom), a thin cream inner ring and a cyan face (see KEYING); never paint a face. Same-size
medallions share one rim; all sit on a soft shadow. No 3D, no glow, no gradients outside the scenes
and pools, no grain on flat areas.

Framing, in percentages of the 4:5 slide. Cover and CTA: everything inside the panel, 5% of the panel
width clear on every side. Interiors: scenes full-bleed; medallions at least 3% and text wells 5% from
the sides; only cream within 3% of the top, only scene or cream within 4.5% of the bottom. If content
does not fit, make it smaller. Minimum sizes: cover labels, numerals, counter and stamp text 1/45 of
the slide height; each title line 1/16.

References: with no image attached, follow this text alone. Once a locked page is attached as Image 1,
match its rims, band heights, pools and proportions exactly. Never draw a real country's outline,
lettering on a medallion rim, or any character, creature or mascot outside a cyan slot.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. Interiors
carry no text at all. No extra captions, labels, place names, lorem ipsum, watermarks, handles or
logos. Never render these instructions or section names as text.

## EMBLEM SHEET

Emblem decks only. A plain cream page holds a 3 x 3 grid of {N} faces, each a perfect circle about 26%
of the page width, evenly spaced, with clear cream between them and at least 5% at every edge. No
rims, shadows, labels or numbers. Each row is one tab page; in reading order, face 1 is
{emblem 1, e.g. "a magnifier over a page"} ... face {N} is {emblem N}. Each face is a flat, bold,
sticker-like emblem of one entry's job: thick ink outlines, a flat circular ground in cobalt, ochre,
sage or orange, 3-4 flat colours, neighbours in a row on different grounds. No letters, numbers, logos
or characters. With fewer than 9 entries, leave the remaining cells plain cream.

## COVER

Inside the cream panel, top to bottom:
- A small cobalt "01 / {TT}" top-right; the ink kicker pill "{KICKER}" centred near the top.
- Centred title: "{Title line 1}" in sentence case, as wide as the margins allow, over
  "{TITLE LINE 2}" in caps; at line 2's right, a round ochre compass-dial stamp about 12% of the panel
  width (thin double ring, four ticks) with "{STAMP}" in ink caps on one or two lines.
- An invented flat sage island, long and narrow with a soft irregular coast, running lower-left to
  upper-right: bounding box about 40% of the panel, land only 14-18% of the panel width across,
  leaving open cream triangles upper-left and lower-right. Thin cream roads cut it into districts with
  large cream numerals "01", "02", "03". Exactly {N} orange teardrop pins, each on its entry's
  district.
- {N} medallions in the triangles (with 9: five on one side, four on the other), the 3 chapter leads
  ({lead labels}) about 22% of the panel width, the rest 16%; as close as 1-2% to the coast but never
  over land, a pin or a numeral, and never touching another medallion or label. Each joins its pin by
  one thin straight orange leader line (no arrowhead) and has a cobalt caps label above or below:
  "{label 1}" ... "{label N}".
- Bottom-left, the cyan subject slot with clear cream around it. Bottom-right, a cobalt rounded pill
  with cream "{Start at tab 01}" and three solid cream triangles.

*(optional)* 6 entries: six medallions at about 20%, three per triangle, two pins per district.
*(optional, spine D)* One district, pin and 22% medallion per step (3-5), numbered "01" to "0{N}".
*(optional)* Tool-insides deck: the island is a flat rounded sage app window, three empty panes, pins
on them.
*(optional, only with your own mascot)* A cyan mascot slot about 12% of the panel width on the shore.

## INTERIOR

Every page but the CTA: the cream top strip (to 9% of the height) holds the tab-row zone at 3-9% of
the height and 3-97% of the width, its bottom edge on band 1 (on cream on the EXTRA page).

**Three-band page** (one chapter, three entries, three different scenes).
- Band 1: the medallion on the left, 3% from the edge, vertically centred, about 70% of the band
  height across, the scene brightest around it. The text well, centred in a pool reaching about 2%
  beyond it, spans 38-95% of the width and 14-84% of the band height.
- Band 2 mirrors it: medallion and brightest scene on the right, well at 5-62% of the width.
- Band 3 repeats band 1, medallion and well raised slightly to clear the bottom margin.

**Deep-dive page** (the strongest entry, a why page, or a one-entry chapter). One band laid out like
band 1, from 9% to about 45% of the height. Below it on plain cream, one capture zone at {W:H} inside
a thin ink frame with a 2% cream mat, from about 48% of the height to at least 5% above the bottom, 5%
cream clear on each side.
*(optional, spine D step page)* The band ends at 40%, the capture zone runs 43-76%, and a command-card
zone at {W:H} runs 79-95%, 5% cream clear on each side.

**EXTRA page** (the combo or copy-paste payoff). Upper half, plain cream: a small cover island about
55% of the width with only two pins joined by a dashed orange route line, and those two entries'
medallions beside their pins at about 18% of the width. Lower half: one prompt-card zone at {W:H},
centred, 5% cream clear on each side.

**CTA page** (the cover frame; "{TT} / {TT}" top-right). A large ink pill with cream caps "Comment
{KEYWORD}", one cobalt line under it, "{what they get}", then the island at about half the panel width
with every pin and no medallions or labels. Nothing else.

## KEYING

Every magenta zone is ONE solid flat #FF00FF rectangle at its aspect: pure uniform magenta edge to
edge, flat and frontal, no gradient, texture, glow, text, UI or tilt. Corners are square, but slightly
rounded on the prompt- and command-card zones. Everything else keeps a visible gap from each zone;
only band 1's top edge touches the tab-row zone.

Every cyan slot is ONE flat #00FFFF shape with no text, art, outline or shadow: each medallion face, a
disc filling everything inside the cream ring; the subject slot, a rounded square about 11% of the
panel width; *(optional, only with your own mascot)* the mascot slot, a rounded rectangle at {W:H}.

No purple, violet, pink or magenta anywhere else: no pink or purple skies, neon, blossom, or pink or
red flowers. No cyan, turquoise or teal except the cyan slots; the sage stays yellow-green, and
painted cobalt stays at least 2% of the width from any cyan slot.
