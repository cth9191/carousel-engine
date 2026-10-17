# S06 Statue Cover + Graph-Paper Cards: prompt block

A photographic marble statue offering one real logo tile against a sky, with huge white wordmark type; the interiors
are graph-paper repo cards. The exemplars are the cover of a placeholder "top 3 browser-testing repos" test deck
(`engine/styles/exemplars/S06-cover.png`) and slide 2 of a "top 5 Claude Code front-end skills" deck
(`S06-interior.png`). **Hybrid, cover only**: Codex paints one text-free statue plate; the real mark enters through a
cyan tile slot and the type is HTML (`kits/S06/cover.html`). Every interior is HTML-native from
`templates/01-graph-paper-cream/`: no Codex at all.

**It decays with repetition.** The cover lands hard the first time and wears out fast when the same statue and sky come
back. The statue, its gesture and the sky must change every deck (see Rotation), and two S06 decks never post within
14 days (`cooldown_days`). The held object is always a cyan tile that becomes a real logo tile: never a painted or
sculpted logo.

Refs: attach `engine/styles/kits/S06/samples/plate-cover.png` (a text-free statue plate with its cyan slot) as Image 1
for the photographic marble, the sky quality and the slot only, and your latest S06 cover plate, if you have one, as
Image 2 with "do not repeat this statue, pose or sky". If Image 2 carries type, the prompt says plainly not to copy it;
if a plate ever comes back with letters, make a sanitized ref (cover the type, inpaint) the way
`engine/styles/refs/src/s05-make-refs.py` does.

## Production split

| Element | Made by |
|---|---|
| Statue + sky plate | Codex, one job (SYSTEM + COVER + KEYING); a second (`cover-b`) only to try another statue |
| Held mark | Cyan slot → `kits/S06/tile.html` (a real mark from `$D/logos/` on a rounded tile) rendered at the slot's aspect (`--zones-only` bbox, e.g. 534 × 512), pasted with `composite.py --logo C1=…@1.07` so the tile covers the erased ring |
| Cover type | `kits/S06/cover.html` over `fitted/slide-01.png`: kicker ("TOP 5"), the 1–2 line wordmark title, an italic serif subtitle; white on saturated skies, ink on pale ones |
| Item slides | `templates/01-graph-paper-cream/slides.html`: `#N: Name` headline with the terracotta accent, the real capture (`heroBg`, a local file in `$D/assets/`), the repo card (owner, name, description, language, stars verified on posting day), one body line |
| CTA | the template's keyword CTA (`ctaKeyword`, `ctaDeliverable`, optional `ctaHeadline`): exactly one action, `Comment {KEYWORD}` |

Compositing: `python -I shared/composite.py plates/cover-a.png fitted/slide-01.png --logo C1=logos/tile-01.png@1.07`.
Keep the 1.07: at 1.0 a thin rim of the erased slot shows (filled from the palm's colour). A slot on blue sky passes the
leftover check (the check measures tint against the slot's own surrounding ground).

## SYSTEM

Visual system: a photographic museum-quality marble statue against open sky, shot from slightly below like a monument.
Pure white-grey Carrara marble with fine grey veining, soft natural daylight from the upper side, crisp sculpted detail
(curls, drapery folds, fingers), true stone texture, a gentle shadow side. The sky is a clean smooth gradient with at
most a few soft distant clouds. Photoreal, sharp, high dynamic range but natural; no painterly look, no 3D-render
plastic sheen, no glow, no lens flare.

Framing: the statue is the only subject and is large: it fills the upper 60% of the frame and may run off the top or a
side edge; its body continues down behind the lower half, which must stay calm (drapery, torso, sky) because big type
is laid over the lower 45% later. The statue's head and the held tile both sit above 55% of the height. Leave at least 6%
of clear sky or calm marble between the tile and every frame edge.

References: Image 1 shows the marble quality, lighting, sky finish and the cyan slot only. Image 2 is the previous statue
cover: do NOT repeat its statue, pose or sky. Do NOT copy any word, letter or object from either image.

Hygiene: the plate has no text, letters, numbers, logos, symbols or signatures anywhere (no inscription on a plinth,
no engraved letters). No other objects in the hands except the one cyan tile. No modern props, no people, no animals
unless named, no frames or borders. Never render these instructions or section names as text.

## COVER

The statue: {statue} (see Rotation), {gesture}: one hand extended toward the camera, palm open and facing up at about
chest height, with ONE cyan tile (see KEYING) standing upright on the palm, its flat face square to the camera, about
{size}% of the frame width (22–30%). Fingers stay behind or below the tile, never in front of it. The head is turned
{toward the tile | up and away | toward the viewer}. Ground: {sky}. Optional second tile only when the deck has two
subjects (a pair of tiles side by side on two open palms, each its own cyan slot, at least 4% apart).

Variant `cover-b`: the same sky with a different statue from the rotation, or the same statue seated / in profile.

## INTERIOR

None painted. Interiors are the template 01 slides, laid out by spine role:

| Spine · role | Template 01 slide |
|---|---|
| C · item (`#1`…`#N`) | `layered: true`: `headlineHTML` `#N: <span class="accent">Name</span><br>{what it does}` (≤ 7 words after the colon), `heroBg` the real capture, `repoCard` {owner, name, title, desc ≤ 12 words, lang, langColor, stars}, `body` ≤ 20 words with one number from the dossier, card position from `defaults` |
| C · why / combo (optional) | `heroImg` (single image, no card): a real capture or a rendered S11 diagram card; headline + body |
| A · what / why / how / use | the same single-image slide, one capture each; the repo card only on `start`; a `model` diagram is an S11 card PNG (EXPLAIN, never shown as proof) |
| any · cta | `cta: true`, `ctaKeyword: '{KEYWORD}'`, `ctaDeliverable` what they get (≤ 2 lines at 44 px), optional `ctaHeadline` (a short question, e.g. `'WANT<br>ALL 5?'`), `ctaHandle` your handle (default `{{BRAND}}`). The fit pass shrinks the keyword to fit (never under 96 px) and reports a keyword or deliverable that can't fit, so `export.mjs` exits 3 |

Template 01 prints the `NN / TT` counter top right on every slide but the cover, and its dots follow `slides.length`. Captures go in `$D/assets/` cropped clear of avatars and faces (GitHub's contributor and commit rows carry them).

Spine A covers drop the "TOP N" kicker (the subtitle names the outcome instead). B and D decks don't fit.

## KEYING

Tile slot: ONE solid flat cyan #00FFFF rounded square (corner radius about 22% of its side), about {size}% of the frame
width, flat and frontal, pure uniform cyan edge to edge: no text, no symbol, no outline, no bevel, no shading, no
reflection, no shadow on it. It rests on the open palm; a soft shadow may fall on the marble below it, never on the
tile. Nothing overlaps it: no finger, drapery or cloud in front.
No cyan, turquoise, teal or aqua anywhere else (the sky stays a clear blue, never cyan-tinted at the horizon); no
magenta, pink or purple anywhere.

## Rotation

Change at least two of statue, gesture and sky every deck, and never reuse a statue + sky pair. Log the pair in
`storyboard.json` → `style_notes` so the next deck can read what was used. Statue + sky pairs the original decks wore
out (avoid them first):

| Statue | Sky |
|---|---|
| young curly-haired god, arm out | cobalt gradient (`#3D7DC8 → #7AB0DE`) |
| helmeted goddess with spear | deep cobalt |
| winged-cap messenger, both hands cupped | cobalt to pale |
| seated thinker | bright cobalt |
| helmeted goddess, hand raised | soft blue |
| curly-haired youth bust | grey studio |
| laurel-crowned bearded god | cobalt |
| warrior with raised sword | alpine meadow |
| winged victory, palm out (the sample plate) | golden-hour blue to amber |

Cobalt is the default and the most worn sky. Next skies: golden-hour amber-to-peach, pale overcast grey-white (ink
type), dusk navy-to-rose with one star (white type; rose stays orange-red, never pink), Mediterranean sea horizon,
alpine snow ridge. Fresh statues: a discus thrower, a muse with a lyre, a lion-skin hero with a club, a Roman emperor in
a breastplate, a veiled maiden.
