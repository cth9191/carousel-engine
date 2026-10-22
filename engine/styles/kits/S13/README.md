# S13 Oversized-Serif Photo Editorial: overlay kit

Every word on an S13 slide is one of these HTML overlays (spec: `engine/styles/S13-oversized-serif-photo-editorial.prompt.md`).
Photo pages and the cover sit on a fitted, text-free Codex plate; quiet pages and the CTA have no plate. The
kit mirrors a deck folder (`../fitted/`, `../samples/`), so its paths work unchanged once copied.

| Path | What it is |
|---|---|
| `cards/s13.css` | Tokens and components: mono masthead, numeral badge, rule headline + body, quiet photocopy ground, cover kicker / giant serif / trailing line, fan cards, warm bottom gradient, three-phrase row, CTA |
| `cards/s13.js` | Sets the plate (`slide-data.plate`, else `../fitted/<file>.png`), draws sky-tone's scrims and the grain (film on photo pages; toner + streaks on quiet ones), runs the fit pass and grows `.giant[data-fill]` to its width. Any failure overflows the page (render-card exit 2), never hangs |
| `cards/slide-01.html` | **Cover** (render last): kicker, giant word, trailing line, fan of three of the deck's exports, row of three phrases. slide-data box `[0.08, 0.46]` |
| `cards/slide-02.html` | **Photo page**: badge + headline + body over the plate's calm zone. Box `[0.10, 0.61]` |
| `cards/slide-03.html` | **Quiet page**: badge above headline, body; no plate |
| `cards/slide-04.html` | **CTA** (quiet ground): "comment" + the keyword as the giant orange serif word + deliverable line |
| `fitted/slide-01.png`, `slide-02.png` | Two approved Codex photo plates, fitted (also `engine/styles/refs/s13-ref-cover.png`, `s13-ref-photo.png`) |
| `samples/slide-0N.png` | The four pages rendered, cover last (exit 0 each). Placeholder topic, brand shown as `YOUR BRAND` |

The masthead's middle item is `{{BRAND}}`: the skill fills it in when it copies a card into a deck (rendered
straight from this folder, it shows the placeholder). The cards still carry the `<body>` tone stamps from the
sample plates; sky-tone re-stamps them in every deck.

## Use it for a deck

```bash
D=carousels/YYYY-MM-DD-slug
mkdir -p $D/cards $D/fitted $D/exports
cp engine/styles/kits/S13/cards/{s13.css,s13.js} $D/cards/
# per slide: copy the layout page to cards/slide-NN.html (NN = the slide number, matching fitted/slide-NN.png),
# fill {{BRAND}}, replace every sample string from storyboard strings[], keep the slide-data JSON (layout, box)
python -I shared/composite.py $D/plates/slide-NN.png $D/fitted/slide-NN.png     # every photo plate
node shared/sky-tone.mjs $D                                                     # photo pages + cover; exit 4 = edit the plate
node shared/render-card.mjs $D/cards/slide-NN.html $D/exports/slide-NN-YYYY-MM-DD.png --w 1080 --h 1350 --scale 1 --min-px 22
# last: point the cover's three fan <img> at $D/exports/ (strongest rule page in the middle), then render slide-01
```

## Fit and limits (measured on the kit)

- Masthead: 22 px JetBrains Mono caps, three items, at y 48.
- Photo page: headline 66 → 56 px in 714 x 136 (2 lines, "Say the job before the details." fits at 66);
  body 40 → 34 px in 872 x 450: 3 short paragraphs, about 40 words. Keep the stack inside the plate's calm zone.
- Quiet page: headline 80 → 66 px in 872 x 164; body 42 → 36 px in 872 x 560.
- Cover giant: one word grown to span 872 px, 220-460 px ("prompts" lands near 400 px). A long word that
  stays under 220 px throws: choose a shorter word.
- Fan: three cards about 300 x 375 (the middle one 328 x 410) from y 660; they hide the plate's centre, so the
  cover subject stands at the outer edge.
