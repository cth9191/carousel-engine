# S05 card kit

Cards for S05 Phone-Photo Monitor (`engine/styles/S05-phone-photo-monitor.prompt.md`). Two cards, both exact HTML:

| Card | What it is | Render | Copy limits (enforced) |
|---|---|---|---|
| `caption.html` | Every word on the slide: up to 3 white TikTok-style stickers (each line its own box, black Inter 600) plus a small `N/T` counter, over the finished photo | full frame, `--w 1080 --h 1350 --scale 1 --min-px 30`, straight to `$D/final/slide-NN.png` | ≤ 3 stickers; title ≤ 12 words, body ≤ 34 words, link ≤ 48 characters |
| `screen-title.html` | The cover's screen when no capture says it better: a pixel-font wordmark (Silkscreen) on a dark screen, optional real mark on a white panel, optional mascot PNG (your own mascot, if you have one; never a licensed character) | at the screen's aspect (the zone's `out bbox`), `--scale 2 --bg "#0B0B0F"`, into `$D/shots/` (it is a screen, so it is warped like a capture) | 1–2 lines, ≤ 12 characters a line |

`kit.js` is the shared runtime both cards load (JSON in, fit pass, `window.cardReady` for `shared/render-card.mjs`).

Sticker roles and default boxes (top % / height %): `title` 12.5 / 19 (text at the top of its box), `body` 40 / 36 (centred),
`link` 82 / 9 (bottom). Override per sticker with `y`, `h` and `align` (`top`, `mid`, `bottom`) to keep a sticker off the
part of the screen that carries the proof. Fonts shrink to fit (title down to 54 px, body 40, link 34), never below.

## Fill one slide

1. Copy `kit.js`, `caption.html` and (cover) `screen-title.html` into `$D/cards/`; name each caption copy `slide-NN.html`.
2. Screen: a real capture in `$D/shots/` (faces scrubbed), or render `screen-title.html` there.
3. Photo: your own photo, or the Codex plate with the screen warped on:
   `python -I shared/composite.py $D/plates/slide-NN.png $D/fitted/slide-NN.png --shot 1=$D/shots/x.png@x,y,w,h,warp[,extend=left|right][,aspect=W:H]`
   (the block's Compositing section has the options); leftover must be 0.
4. Edit only the JSON in `slide-NN.html` (`plate` defaults to `../fitted/slide-NN.png`), from `strings[]` verbatim.
5. `node shared/render-card.mjs $D/cards/slide-NN.html $D/final/slide-NN.png --w 1080 --h 1350 --scale 1 --min-px 30`.
   Exit 0 is required; exit 2 names the broken rule (`LIMIT-<rule>`) or the overflowing sticker.

## samples/

`slide-01.png` (cover: desk-view plate, `screen-title` with the GitHub mark, two stickers) and `slide-03.png` (item:
canted plate, a real README capture warped on with `extend=left`, three stickers), from a smoke test on a placeholder
topic ("3 browser-testing repos"); `plate-cover.png` and `plate-canted.png` are the untouched Codex plates.
