# S05 Phone-Photo Monitor: prompt block

Every slide is a phone photo of your monitor showing the real thing (a README, the tool, a title screen), with white
TikTok-style caption stickers on top. The exemplars are the cover of a "3 GitHub repos" deck
(`engine/styles/exemplars/S05-cover.jpg`, browser tabs and taskbar blurred) and an item slide of a "5 repos" deck in a
red-lit room (`S05-interior.jpg`, tabs and tray blurred). It works because it looks unproduced. Keep that: no chrome
beyond the stickers and a tiny counter, no layout grid, no brand colour on the page.

**Hybrid.** The screen is always real (a capture or an exact HTML title screen), and every word is an HTML sticker. Only
the room and the monitor can be painted, and only when you have no photo. Source order, best first:

1. **Your photo of the real screen** (the original method): open each capture full screen and shoot it on your phone.
   No Codex, no keying. `composite.py` fits it to 1080 × 1350 and the caption card goes on top.
2. **Your photo of a magenta screen**: open a full-screen `#FF00FF` page and shoot the monitor once per angle (a
   10-second job; reusable until the desk changes). Each shot then goes through `--shot …,warp` (Compositing, below)
   like a Codex plate. Check the composite report: camera magenta is not pure, so a leftover count above 0 means
   re-shoot with the room lights on and no screen glare.
3. **Codex plate** (SYSTEM + COVER or INTERIOR + KEYING): a painted phone photo of a monitor in a real-looking room with
   a flat magenta screen. The capture is perspective-warped onto it.

Attach the sanitized refs, never raw exports (their stickers and screens would be copied):
`engine/styles/refs/s05-ref-desk.png` (whole monitor, webcam, desk; near-frontal), `s05-ref-canted.png` (monitor turned
about 20°, red-lit room) and `s05-ref-close.png` (camera close, webcam and top bezel at the top, screen fills the rest).
They were cut from real desk photos with the screen quad filled magenta and the stickers and the stand logo inpainted;
`engine/styles/refs/src/s05-make-refs.py` does the same to your own photos (edit its quads, see its header).
Once a cover plate is locked, attach it first.

## Production split

| Element | Made by |
|---|---|
| Room, desk, monitor, webcam | Your photo (modes 1–2), else one Codex plate per view (mode 3) |
| Screen content | Real capture (`shots.py` frames, Browser pane / playwright web shots, faces scrubbed) or `kits/S05/screen-title.html` (pixel title wordmark, optional real mark on a white panel, optional mascot PNG: your own mascot, if you have one; never a licensed character) |
| Screen onto the plate | `composite.py --shot 1=shots/x.png@x,y,w,h,warp`: perspective-warps the capture onto the magenta quad with a photographed-screen look and the loose key (see Compositing). Use it on every view, the near-frontal desk view included (a plain `--shot` pastes a crisp flat screen that reads as pasted) |
| Caption stickers + counter | `kits/S05/caption.html`, one per slide, rendered full frame over the fitted photo |

Plates per deck: 1 cover plate + 2 interior plates (one canted, one close). The interiors alternate the two views and
only the capture changes, which is how the real decks read (a handheld phone, the same desk, a new screen). Make one
plate per slide only if you ask for it; it adds jobs, not story.

Copy (all of it lives in the stickers): cover hook ≤ 12 words with the count ("3 GitHub Repos That Will 10X Your
Claude Code Projects"), plus one optional body sticker. Item slides: title `N) Name` (real case, ≤ 5 words), body
≤ 34 words in one or two plain sentences (what it does, what it replaces or one use), link `github.com/owner/repo` or
the install command (≤ 48 characters). At most 3 stickers a slide. Every number is verified on posting day and sits in
the body or the screen itself. The capture is the proof; a mock on screen is only for a `model` slide and is labelled
as a diagram by its own look.

## SYSTEM

Visual system: an unedited phone photo taken at a home desk. Shot handheld on a phone's main camera from about arm's
length, slightly soft, natural sensor noise, mild lens vignetting, the room a little darker than the screen, true-to-life
colour with no grading, no bokeh tricks, no HDR halo. The subject is one modern widescreen computer monitor (thin black
bezel, about 27 to 32 inches, plain matte black stand) on a light wooden desk. Behind it: a dense green artificial
plant wall, the edge of a white softbox lamp, and a dark round webcam clipped to the top centre of the monitor. The
lighting is warm and practical (the lamp plus the screen's own light); the only coloured light allowed is a deep red
wash on the wall behind (pure red, never pink, purple or magenta).

Framing: the monitor is large in frame and may run off one or both side edges; the camera looks slightly down at it.
Keep the top 9% of the frame free of the webcam's lens centre and the bottom 6% free of the screen's lower edge where
the layout allows, so the overlay stickers have room. No text needs a margin: the plate carries no words.

References: the attached images show camera position, framing and room only. The magenta area in them is the screen. Do
NOT copy their exact objects one for one; keep the same kind of desk, wall, lamp and webcam.

Hygiene: the plate has no text anywhere: no captions, stickers, labels, watermarks, handles, brand names, logos or model
names on the monitor bezel, the stand, the webcam or any object (blank smooth surfaces where a logo would be). No
people, hands, faces, reflections of people, phones or keyboards in the shot. No RGB light strips, no glow in pink,
purple, violet or magenta, no neon. Never render these instructions or section names as text.

## COVER

Desk view, near-frontal: the camera sits slightly above screen centre and square to it, so the screen's top and bottom
edges tilt by no more than about 3° and its sides are near vertical. The monitor fills about 100% to 110% of the frame
width (it may run off both sides) and the screen spans from about 15% to 90% of the frame height. Above the monitor, in
the top 15%: the webcam on its clip at the centre, the plant wall and the lamp's edge. Below the monitor: the top of the
stand and the wooden desk. The screen is ONE magenta quad (see KEYING).

Variant `cover-b` (if a second cover is wanted): the canted view (INTERIOR, canted) with the monitor turned the other way.

## INTERIOR

Two views. Both carry exactly one magenta screen and no other key colour.

**Canted.** The monitor is turned about 15° to 25° away from the camera, its near side on the {left | right}, so the
screen is a clear trapezoid: the near edge about 1.2 to 1.35 times the far edge's height. The screen fills about 70% to
85% of the frame and runs off the near side edge. Room visible behind the far side (plant wall, red wash or lamp) and a
strip of desk below.

**Close.** The camera is close and nearly square to the screen: the webcam on its clip and about 6% to 14% of plant wall
show at the top, the screen's top edge tilts by at most 3°, and the screen fills the frame from its top edge to the
bottom and both sides.

Layouts by spine role (`formats.spines`), all as the stickers in `kits/S05/caption.html`:

| Spine · role | View | Screen | Stickers |
|---|---|---|---|
| C · cover | cover (desk) | `screen-title.html` (the subject's wordmark, optionally with the list's real logo on its white panel) or the strongest item's hero capture | title (hook with count) at 12%; optional body at 76% |
| C · why (optional) | close | the proof page (trending list, stars chart, issue thread), faces scrubbed | title, body |
| C · item | canted / close, alternating | the item's README top or its running UI | `N) Name` title at 12%; body at 40% (or 60% when the screen's centre carries the proof); link at 82% |
| C · combo (optional) | canted | a real screenshot of the two tools side by side on the desktop | title, body |
| A · what / why | close | the tool's page / the before-and-after capture or a page showing the number | title (≤ 7 words), body |
| A · model | canted | an HTML diagram card (S11 kit) shown as a screen; it explains, it does not prove | title, body |
| A · how / use | canted / close | the real run: terminal, UI, output | title, body |
| A · peak / start | close | the prompt, config or install as a real capture at a large font size (zoomed ≥ 150%) | title; link sticker holds the exact command if it is ≤ 48 characters |
| any · cta | cover (desk) or a second desk shot | `screen-title.html` with the keyword ("COMMENT" / "{KEYWORD}") or the real deliverable page | title `Comment {KEYWORD}` + body with what they get. The keyword appears exactly once in stickers |

Spine B and D decks don't fit: a side-by-side test or a part diagram needs a layout, and this style's point is having none.

## KEYING

The screen: ONE solid flat magenta #FF00FF area filling the monitor's whole display, edge to edge inside the thin black
bezel, in correct perspective with the monitor (a trapezoid that follows the view). Pure uniform magenta: no gradient,
no glare, no reflection, no vignette, no moiré, no text, no UI, no taskbar, no cursor. The bezel stays visible all round
the parts of the screen that are in frame. Nothing stands in front of the screen.
No purple, violet, pink or magenta anywhere else in the photo (walls, lights, desk, plants, reflections); no cyan or
turquoise anywhere.

## Compositing (not prompt text)

One command per plate, straight to `fitted/slide-NN.png`:

```
python -I shared/composite.py $D/plates/slide-03.png $D/fitted/slide-03.png   --shot 1=$D/shots/readme.png@60,330,1060,560,warp,extend=left --report $D/runs/composite/03.json
```

- `aspect=W:H` is the screen's real aspect (default 16:9). On the desk cover, whose screen runs off both frame edges,
  pass the zone's own aspect from `--zones-only` (the sample cover used `aspect=1080:818`) and render the title screen
  at that size.
- `extend=left|right` when the screen runs off that side (canted view): the tool estimates how much of the screen is
  still in frame (the sample canted plate: 87%) and shows only that part of the capture, so text is not squeezed.
- `look=photo` is the default (0.6 px blur, blacks lifted to 14, whites eased to 232, one soft glare blob, a light
  screen vignette, the plate's own grain); `look=none` pastes it clean.
- Leftover must be 0 (exit 3 otherwise). The `fill < 97%` warning on a canted zone is its trapezoid shape, not a fault.
