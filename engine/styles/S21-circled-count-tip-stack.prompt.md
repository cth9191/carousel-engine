# S21 Circled-Count Tip Stack: prompt block

A flat cream desktop-notes page: a hand-circled count hook, a folder spilling window cards, and
three captioned app windows per slide. The layout was studied from a high-performing carousel; only
its layout vocabulary carries over. Never copy any reference deck's characters, photo, name, art,
words, hook, CTA phrasing, item set or signature palette. Palette rules for this style: the accent is
Claude orange #D9551F (never red), the folder is ink or kraft (never blue: sky blues pass
composite.py's cyan key test and break a logo slot), and the byline is your own.

**Html-native.** `templates/09-window-stack` renders every word: copy its `slides.html` into the
deck, fill `DECK` and `slides[]` (fields in `templates/09-window-stack/recipe.md`), and bake with
`node shared/export.mjs --carousel <id>`, the normal slides.html route (exit 3 = a FIT/COPY failure:
rewrite the copy).
Codex paints at most a topic-container hero plate. The plate route below is the fallback: Codex
paints one plate per slide (SYSTEM, then COVER or INTERIOR, then KEYING), and every interior window
is a magenta face under an exact-text HTML card. **No style refs ship for this style:** the first
plate prompts run text-only (SYSTEM plus the layout); once the user approves a plate, it becomes
Image 1 (a locked cover first, then a locked interior). Never attach another creator's slides.

## Production split (Codex fallback)

| Element | Made by, on a plate |
|---|---|
| Window: chrome, dots, item number or label, tip | Magenta face; Codex paints only its shadow. One card per window, `cards/window-NN.html`, via `node shared/render-card.mjs --bg "#FFFFFF"` at 2x the zone's measured `--zones-only` out bbox (not the nominal size), pasted with `composite.py --card`. Render edge to edge with square corners; the zone's rounded mask trims them |
| Proof capture | `shared/shots.py` shot as an `<img>` in the card: object-fit cover on the focus box; dark captures letterboxed on their edge colour |
| Terminal body | Exact prompt, command or config in the card: ink #141414, cream JetBrains Mono, fit pass (about 28 px at 840 wide) |
| CTA ellipse, "before" strike | Orange SVG marker paths in their cards |
| Byline avatar | Your square profile photo (or your brand mark): magenta circle → `composite.py --shot`; never painted |
| Subject logo | Folder front: cyan slot → `--logo N=logos/x.png@0.8`; title bar: `<img>` in the card |

Codex paints everything else: ground, headline, item range, captions, counter, arrow, the cover's
byline, hook, payoff and ellipse, and the folder hero. Claude checks each painted string against
`strings[]`, and hook identifiers letter by letter; a wrong one becomes an edit job. On the template
path every word is HTML (the hook auto-fits); captures, logos and the avatar are `<img>`s; the
ellipse and strike are template SVG paths scaled to the word; your own mascot (optional; transparent
PNG poses you made, never a licensed character) is an `<img>` sitting on the card heap or peeking out
of the folder; and
the hero is HTML/SVG, its fanned cards carrying the deck's own tip fragments clipped by the folder
front. A topic container (box, terminal) is a Codex hero plate cut out to alpha first (flood-fill
the cream from the corners, or any background-removal tool).

**Cards.** Stack: one lowercase tip (≤6 words, ≤2 lines) and the item number ("04") at the bar's
right, which checks the cover's count. Proof: the item's exact name in mono after the dots, an
optional small logo at the bar's right end. Before/after: bars labelled "before" / "after"; the
before tip muted #8A8178 under the strike, the after tip full ink. CTA: "comment {KEYWORD}", the
keyword circled.

**Story and copy.** A declared Spine C deviation ("C-variant: findings listicle"; conditions in
`formats.notes`): at most 3 stack slides, `deviations[]` logs that M counts windows 01–M, not
slides, and tools, repos and skills stay one per slide in a proof window. A theme headline names the
one lesson its three windows share. Headlines and tip lines ≤7 words. Captions ≤46 characters,
lowercase words and numerals, no identifiers: the why or how plus the corpus count
("{why} · in {k} of {N}"), never restating the tip. A proof caption says how the corpus was picked
and sorted (or what the item replaces plus one use), a terminal caption where to paste it, the CTA
caption the deliverable. The hook is your own claim in your own verb ("i read", "i ran", "i
tested") with a real count; the circle works with any count hook (F4, F5, F8, F13 "I
analyzed N").

**Measurements** (1080 × 1350; the template's values and the plate targets):
- Margins 54 px. Window 840 × 252 at x 120–960: 52 px title bar, 7 px frame on three sides, white
  body 826 × 193, radius 8, hard shadow +10/+10. Dots 13 px, 10 px apart, first 20 px in, centred;
  item number 26 px mono #8A8178, 20 px from the right; proof/terminal labels 26 px mono #3A3A3A,
  20 px after the dots.
- Stack: counter 28 px mono at (120, 54); arrow 72 px wide ending at x 1020 on the counter line;
  headline 48 px, one line, x 120, y 112–164, item range 26 px mono #8A8178 right-aligned to x 960
  on its baseline; windows at y 200 / 556 / 912; captions 34 px centred, 24 px below the shadow, the
  last near y 1238. Tip 64 px, line-height 1.08, tracking -0.02em, centred.
- Proof / terminal: 56 px tip line at y 112; one 840 × 742 window at y 200; captions from y 976.
- Cover: avatar 140 px circle at (120, 60); byline right-aligned to x 960 (name 40 px bold, role
  32 px); hook auto-fit to 840 px, max 128 px, y 225–505; hero 840 × 490 at y 520–1010; payoff 54 px
  centred, y 1040–1230; counter (28 px) and arrow centred on y 1276.

## SYSTEM

Visual system: a clean desktop-notes page. Flat cream ground (#F5EBE0), no grain, grid or texture.
The repeating unit is a white app-window card: a warm-grey title bar (#E9E2D8) about a fifth of its
height, with three traffic-light dots at its left (red #EE4B3F, amber #F5A524, green #2DB84B); a
thin frame in the same grey on the left, right and bottom; a pure white body (#FFFFFF); corners
rounded about 1% of the slide width; a hard flat shadow offset down-right (#B3A99E, about 1% of the
width, no blur). Every window on a slide is the same size.

Type: hooks, headlines and tips in a heavy black grotesk (like Inter ExtraBold), ink #0E0E0E,
lowercase, tight tracking. Captions in a regular grotesk, ink #1B1B1B, centred, about half the tip
size, one line, never wider than the window. Exact identifiers (CLAUDE.md, /compact, MCP, model and
product names) keep their real case.

Chrome: a small mono counter "{NN} / {TT}" (like JetBrains Mono, warm grey #8A8178) at the top-left,
aligned with the windows' left edge, and a hand-drawn Claude-orange (#D9551F) arrow pointing right
at the top-right, a thick marker stroke with a slightly uneven line.

Claude orange appears only on the arrow, the hand-drawn ellipse around the cover number or CTA
keyword, one accent number or word per slide, and the strike line across a "before" tip. Everything
else is ink, white, cream or warm grey; the folder is ink, never orange. Flat and crisp, like a
vector screenshot: no gradients, 3D, glow, soft shadows or paper texture.

Framing: windows about 78% of the slide width, centred. Every element sits inside a uniform empty
margin of at least 5% of the width left and right and 4% of the height top and bottom; the headline
and stack stay between 8% and 92% of the height. If content does not fit, make it smaller. Readable
at phone-feed size: tips at least about 1/22 of the slide height, headlines 1/30, captions 1/40, the
counter, item numbers and labels 1/52.

References, when attached, show the layout vocabulary only: the window card, three captioned
windows, the hand-circled number, the folder spill and the arrow. Do NOT copy any word, number or
photo, and never use a red accent, a blue folder or a glossy gradient. No characters or mascots.

Hygiene: render only the quoted strings, verbatim, in the given case, exactly as many times as
specified. On interiors, paint each window only as its magenta face and hard shadow (see KEYING),
never a title bar, dot, tip, item number or label. No fake UI, menu bars, URL bars or tab strips. No
extra captions, numbering, lorem ipsum, watermarks, handles or logos. Never render these
instructions or section names as text.

## COVER

1. Byline row (top 15%): the avatar zone at the top-left, a circle about 13% of the width (see
   KEYING). Right-aligned to the window margin, "{{BRAND}}" in bold grotesk with "{role line}"
   under it in regular weight, no quotation marks.
2. Hook: the largest, heaviest type, two lines flush left on the window margin, as wide as the
   margins allow: "{hook line 1 with count}" / "{hook line 2}". Circle the number alone with ONE
   loose hand-drawn Claude-orange ellipse: a single marker stroke about 0.6% of the width thick,
   slightly tilted and wider than the number, its end overshooting its start and clipping the next
   letter.
3. Hero (middle 36%): a flat vector ink document folder, frontal (back panel and tab #2A2A2A, front
   #0E0E0E with a thin #3A3A3A top edge; no gloss). Five or six window cards with the same chrome
   fan out from behind it at -35° to +35°, tops and sides poking out; each body holds only two or
   three soft grey text bars (#D6CFC5), no letters. Optional: one cyan logo slot centred on the
   front panel.
4. Payoff: bold grotesk, centred, two or three lines, about 1/25 of the slide height:
   "{payoff with M}". Only "{M}" is Claude orange.
5. Counter "01 / {TT}" bottom-left, arrow bottom-right.

Variants, when the topic earns them: a kraft folder or open archive box (#C9A27A front, #B08A62
back), or a terminal window with an ink body (#141414), overflowing with cards. Hero plate only
(template path, topic container): just the hero on flat cream, at the aspect given (about 12:7).
Never a licensed character, a real person or a painted mascot.

## INTERIOR

**Tip stack (the default):** at the top-left, flush with the windows, the theme headline
"{theme headline}", smaller than a tip, with "{accent word}" in Claude orange and "{01–03}" in small
warm-grey mono right-aligned on its baseline. Below it, three identical window faces at an even
pitch, one caption line under each: "{caption}". Counter top-left above the headline, arrow
top-right. No hero art and no mascot.

**Single window (proof or terminal):** one heavy lowercase tip line above, flush with the window's
left edge: "{tip line}". One large window face, about 55% of the slide height, with one or two
caption lines under it: "{caption}".

**CTA:** one centred window face, larger than a stack window, with one caption line under it:
"{caption}". No arrow on the last slide.

Before / after (the why slide only): one tip line above, two window faces stacked, a caption under
each.

## KEYING

Each interior window is ONE solid flat magenta #FF00FF rectangle of aspect {W:H} (a stack window is
about 10:3), corners rounded about 1% of the slide width: pure uniform magenta edge to edge, flat
and frontal, with no title bar, dots, frame, text, lines, gradient, texture, glow or tilt. Its hard
warm-grey shadow (#B3A99E) sits outside it, down-right, and is the only thing touching it. The
cover's avatar zone is ONE solid flat magenta #FF00FF circle with clear cream around it. A logo slot
is ONE solid flat cyan #00FFFF rounded square about {size} wide on the folder's front panel: no
text, outline or shadow, clear ink around it. Every other element stands clear of the zones with a
visible gap. No purple, violet, pink or magenta anywhere else; the red dot is a warm red, never
pink. No cyan, turquoise or sky blue anywhere except a logo slot: the folder is ink (or kraft),
never blue.
