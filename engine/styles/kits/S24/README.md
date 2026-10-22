# S24 card kit

HTML cards for the magenta panels of S24 Spotlight Dossier plates (`engine/styles/S24-spotlight-dossier.prompt.md`).
Newsreader (values), Inter (captions) and JetBrains Mono (labels, commands, table) at the S24 tokens: panel ink `#121212`,
cream `#F3EBDF`, Claude orange `#D9551F` (labels), amber `#E8A33D` (the four-point star), warm grey `#8A847C`.
Cards are square-cornered; the plate's rounded magenta mask trims them.

| Card | Panel it fills | Sample size (CSS px) | Copy limits (enforced) |
|---|---|---|---|
| `numbers-NN.html` | Dossier: the numbers strip. Orange tracked label row, 3-4 outlined cells (big serif value over a grotesk caption), one amber star | 928x250 (3.7:1); a 4:1 zone is 928x232 | label ≤ 40; value ≤ 7; caption ≤ 14 |
| `install-NN.html` | Proof: the install card. Orange label, the exact command in white mono after an orange `$`, one grey subline | 800x222 (3.6:1) | label ≤ 40; command ≤ 52; subline ≤ 48 with at most one figure |
| `verdict-NN.html` | Verdict: the table. Name / verdict rows in mono, dashed dividers, optional logo tile per row | 864x560 | 3-6 rows; name ≤ 18; verdict ≤ 24; logos on every row or none |

## Fill one

1. Copy `engine/styles/kits/S24/{kit.css,kit.js}` into `$D/cards/`, and each card as `$D/cards/numbers-NN.html`,
   `install-NN.html`, `verdict.html`.
2. Edit only the JSON in `<script id="data">`. Labels are the storyboard's own words (never a reference deck's panel
   labels). Numbers are pulled on posting day and saved in the deck (stars, the weekly delta from the GitHub API,
   language, licence). The install command is copied from the README and run once. Verdicts are the user's own, from
   real use. Logo tiles are real (`$D/logos/`, paths relative to the card). The sample strings here are placeholders,
   and the sample figures are illustrative, not checked.
3. Find the panel size: `python -I shared/composite.py $D/plates/slide-NN.png --zones-only` and read the zone's `out bbox`.
4. Render at that size, 2x, on the panel ink:

   ```
   node shared/render-card.mjs $D/cards/numbers-02.html $D/cards/numbers-02.png --w 928 --h 250 --scale 2 --bg "#121212"
   ```

   Exit 0 is required. Exit 2 means overflow, text under 14 px, or a broken copy rule (`LIMIT-<rule>` names it).
5. Paste with `composite.py … --card N=$D/cards/numbers-02.png`.

## samples/

`<card>.png` is each card with its sample data. `<card>-longest.png` is the card at the longest strings its limits allow
(numbers at the 4:1 size; verdict with six rows and real logo tiles, the marks in `engine/styles/kits/S25/logos/`). All
passed render-card with exit 0.

The style ships no reference images: Codex jobs run text-only until your first approved plate becomes the reference
(see the prompt block).
