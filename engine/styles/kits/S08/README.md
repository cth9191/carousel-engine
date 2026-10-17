# S08 Bone Editorial: kit

Spec: `engine/styles/S08-bone-editorial.prompt.md`. Hybrid: Codex paints only the paper ground and a
doodle sheet (text-free); every word is HTML.

| Path | What |
|---|---|
| `cards/s08.css` | Tokens, chrome (header, mantra), headline + fit pass hooks, sticky, statements, rows, tables, panes, taped card, strip, notes, composer, optional `.mascot` |
| `cards/page-01.html`, `page-02.html`, `page-03.html` | Sample pages with placeholder copy: what (statements + strip), model (ruled table), why (old/new rows + dark pane) |
| `cards/icons.js` | Lucide glyphs for the sample pages (regenerate per deck with `shared/lucide-icons.mjs`) |
| `fitted/ground.png` | The fitted 1080x1350 ground (paper, rule, star, blank taped sticky, bolt, crown). Reusable across decks |
| `plates/ground.png`, `plates/doodles.png` | The raw Codex plates |
| `doodles/*.png` | Twelve transparent doodle crops: bulb, arrow-dl, arrow-r, star5, twinkle, checkbox, oval, gear, folder, clock, magnifier, bubble |
| `prompts/ground.txt`, `prompts/doodles.txt`, `jobs-setup.json` | The Codex prompts and job file (refs: `engine/styles/refs/s08-ref-*.png`) |
| `samples/page-01.png` … `page-03.png` | The three sample pages rendered |

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/fitted $D/doodles $D/exports
cp engine/styles/kits/S08/cards/s08.css $D/cards/
cp engine/styles/kits/S08/fitted/ground.png $D/fitted/      # or paint a fresh ground (below)
cp engine/styles/kits/S08/doodles/*.png $D/doodles/
# write $D/cards/page-NN.html per slide (start from a sample page in engine/styles/kits/S08/cards/)
node shared/lucide-icons.mjs $D/cards/icons.js --from $D/cards
node shared/render-card.mjs $D/cards/page-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 20
```

Exit 2 = the `.zone` overflows or text is under 20 px: cut copy.

Re-render the kit samples the same way from the repo root:

```bash
K=engine/styles/kits/S08
node shared/lucide-icons.mjs $K/cards/icons.js --from $K/cards
node shared/render-card.mjs $K/cards/page-01.html $K/samples/page-01.png --w 1080 --h 1350 --scale 1 --min-px 20
```

Optional mascot: if you have your own mascot (never a licensed character), drop a transparent PNG
pose into `$D/mascot/` and add `<img class="mascot" src="../mascot/pose.png" style="left:…; top:…; width:…">`
(page-01 has the commented-out line). Leave it out if you have none.

## A fresh ground

`node shared/codex-img.mjs gen engine/styles/kits/S08/jobs-setup.json --only ground` (the job's
`deck` is this kit folder, so the plate lands in `plates/`; copy the job file into a deck and fix
the ref paths to paint there). Codex returns 1092x1440 (3:4). Fit it: scale to height 1350 (1024
wide) and mirror 28 px of plain paper onto each side; then measure the header rule, sticky, bolt and
crown and adjust `.hdr`, `.sticky`, `.mantra` in `s08.css` if they moved (on the shipped plate: rule
y≈49, sticky x 719–1022 y 117–412, bolt and crown y 1257–1315).
