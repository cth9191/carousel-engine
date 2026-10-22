# S18 Folder-Tab Field Guide: card kit

HTML cards for the exact text and the logo faces on S18 slides. Codex paints the plates (cover, tab
pages, EXTRA, CTA) with flat key zones; these cards go into those zones through
`shared/composite.py`. Spec: `styles.json` S18 `requires[]` and `engine/styles/S18-folder-tab-field-guide.prompt.md`.

A deck copies the files it needs into `$D/cards/` and edits only the JSON in each file's
`<script id="data">` block. Every card prints `card: {...}` from render-card. A broken rule (too many
characters or words, a wrong tab count) adds an overflowing `.LIMIT` element, so render-card exits 2
and prints the rule in the class name, e.g. `LIMIT body-is-21-words-max-20-for-three-band`.

| File | Goes into | Fill | Rules the card enforces |
|---|---|---|---|
| `tabs-NN.html` → `cards/tabs-NN.png` | the tab-row magenta zone (3-9% of the height, 3-97% of the width) on every page but the CTA | `tabs` (3-5 labels), `extra` (EXTRA tab), `lit` (1-based tab, or `"EXTRA"` on the EXTRA page), `counter` (`"NN / TT"`) | 3-5 tabs; with 3 tabs a label is 8 characters or fewer (`"02 BUILD"`), with 4-5 the number alone; Nunito 900 cream labels fitted 40 → 34 px (one size for all); cobalt `#3D7DC8` tabs, lit tab orange `#D9551F`, rounded tops, 6 px gaps; counter Inter 700 ink 32 px at the right end |
| `band-NN.html` → `cards/band-NN-B.png` | one band's magenta text well (B = band 1-3) | `layout`, `name`, `where`, `body`, `mark` (emblem decks), `markTone` | `layout` `three-band` (body ≤ 20 words: "does X; replaces Y"), `deep-dive` (≤ 22: the concrete use), `d-step` (≤ 18: what you build); name ≤ 14 characters, Inter 900 caps fitted 48 → 40 px; orange pin + Inter 700 'where it lives' line and Inter 400 body, both fitted 32 → 30 px; all text cream `#F5EBE0`. In an emblem deck `mark` is the entry's real mark (PNG/SVG), shown beside the name, flattened to cream by default |
| `face-NN.html` → `faces/NN.png` | every medallion's cyan face, logo decks only | `mark`, `disc` (`cobalt` / `ochre` / `sage` / `orange`), `tone` (`cream` / `ink` / `original`), `scale` (0.45-0.65, default 0.55) | the real mark at about 55% of the disc on a flat disc; transparent outside the disc. Neighbours on one tab page take different discs; never an orange mark on the orange disc |

Paths in `mark` are relative to the card file: in a deck use `../logos/<name>.png` (real marks only:
your logo folder, simple-icons, or official files; trim them to their alpha first). The kit's own
sample data borrows the marks shipped in `engine/styles/kits/S25/logos/` (`../S25/logos/`), so the
cards render as they are from the kit folder.

## Render commands (from the repo root)

Read each zone's `out bbox` first:

```
python -I shared/composite.py $D/plates/slide-04.png --zones-only --report $D/plates/slide-04.zones.json
```

On a three-band page the magenta zones come out in reading order: M1 the tab row, M2-M4 the three
wells; the cyan medallion faces are C1-C3.

```
# tab row: --bg = the plate cream sampled just beside the strip
node shared/render-card.mjs $D/cards/tabs-04.html $D/cards/tabs-04.png --w <bw> --h <bh> --scale 2 --bg "<cream>" --min-px 30
# each band: --bg = the pool ink sampled just outside that well (never exactly #0E0E0E)
node shared/render-card.mjs $D/cards/band-04-1.html $D/cards/band-04-1.png --w <bw> --h <bh> --scale 2 --bg "<pool ink>" --min-px 30
# logo-deck faces: once per deck, before the cover, NO --bg
node shared/render-card.mjs $D/cards/face-01.html $D/faces/01.png --w 300 --h 300 --scale 2
```

Emblem decks take their faces from the locked Codex emblem sheet instead, disc-cropped by
`shared/shots.py` from a spec entry (with `"out_dir": "carousels/<id>/emblems"`):
`{ "slide": 0, "name": "{nn}", "image": "carousels/<id>/emblems/sheet.png", "discs": "auto", "count": N, "size": 512 }`
→ `emblems/01.png` … in reading order.

Composite (every zone needs an asset or composite.py exits 3):

```
python -I shared/composite.py $D/plates/slide-04.png $D/final/slide-04.png \
    --card M1=$D/cards/tabs-04.png --card M2=$D/cards/band-04-1.png --card M3=$D/cards/band-04-2.png \
    --card M4=$D/cards/band-04-3.png --logo C1=$D/faces/04.png@1.0 --logo C2=$D/faces/05.png@1.0 \
    --logo C3=$D/faces/06.png@1.0
```

Render tabs and bands with `--bg`: plain `--card` flattens transparency onto white. (A band rendered
without `--bg` can instead go in with `--ground fill`, which erases the well into the pool ink around
it first; `--ground` then applies to every `--card` on the slide.) A cover label, numeral or stamp
that fails text QA is patched in place, never regenerated: render a cream label card at its box and
`python -I shared/composite.py $D/final/slide-01.png $D/final/slide-01.png --paste $D/cards/label-fix.png@x,y,w,h,erase`.

The kit ships no character. The optional cover explorer is your own mascot (optional; transparent PNG
poses you made, never a licensed character), pasted through its cyan slot with `--logo`; with no
mascot, the prompt asks for no slot.

## Samples (`samples/`, rendered at realistic zone sizes, 2x)

| PNG | Zone (CSS px) | What it shows |
|---|---|---|
| `tabs-3-extra-lit2.png` | 1015 x 81 | 3 named tabs + EXTRA, tab 02 lit, `04 / 08` |
| `tabs-3-longest-8ch.png` | 1015 x 81 | three 8-character labels (the limit): fits at 36.5 px |
| `tabs-5-extra-lit-extra.png` | 1015 x 81 | 5 numbered tabs + EXTRA lit (the EXTRA page): 34 px |
| `tabs-4-no-extra-lit1.png` | 1015 x 81 | 4 tabs, no EXTRA |
| `band-three-band.png` | 616 x 287 | the default sample (band well at 38-95% x 14-84% of a 409 px band) |
| `band-three-band-longest.png` | 616 x 287 | 14-character name + a 20-word body (the limits): fits at 48 / 32 px |
| `band-deep-dive-emblem.png` | 616 x 340 | deep-dive (22 words) with a real mark beside the name (emblem deck) |
| `band-d-step.png` | 616 x 293 | D step page (18 words) |
| `face-*.png` | 300 x 300 | Claude on cobalt (cream), Claude on orange (ink), Anthropic on sage (cream), OpenAI on ochre (ink) |

Sample star counts read `NNK stars` on purpose: every 'where it lives' figure is verified on posting
day. The style ships no reference images: Codex jobs run text-only until your first approved plate
becomes the reference (see the prompt block).
