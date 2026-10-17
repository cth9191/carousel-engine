r"""composite.py - the ONE general plate compositor for Carousel Engine.

A Codex plate is a ~4:5 slide image with flat key-colour zones:
  magenta #FF00FF -> real captures (--shot, cover-fit) or exact-size rendered cards (--card, contain-fit)
  cyan    #00FFFF -> real logos (--logo: the zone is erased into the ground sampled around it, then the
                     logo is contain-fitted on top)
Zone masks are always read from the untouched plate, so pasted content can never be mistaken for a key.
Writing a per-deck compositing script is a bug: if this file can't do a job, extend it.

USAGE (run from the repo root; -I keeps the deck folder out of sys.path)
  1) Learn the zones first (prints id, bbox, aspect, fill; writes a numbered debug PNG with the final
     crop shaded red):
       python -I shared/composite.py plates/slide-03.png [debug.png] --zones-only [--report zones.json]
     Default debug path: <plate>.zones.png. `out bbox` is the zone in final --size pixels: render cards
     at the zone aspect, at least that size (2x is better; contain-fit downsamples once).
  2) Composite (every detected zone must get an asset, or the run exits 3):
       python -I shared/composite.py plates/slide-03.png final/slide-03.png \
           --shot 1=shots/hud.png@120,80,1400,900 --card 2=cards/steps.png --logo 1=logos/claude.png@0.8 \
           [--size 1080x1350] [--fit crop|pad] [--report report.json]
     --shot N=path[@x,y,w,h]  cover-fit (fill, crop overflow). The focus box (shot px) stays fully visible
                              and centred; it zooms in to the focus grown to the zone aspect.
     --shot N=path@[x,y,w,h,]warp[,aspect=W:H][,look=photo|none][,extend=left|right]
                              a screen photographed at an angle (S05 monitor plates, canted panels):
                              the zone's 4 corners (convex hull -> 4-point polygon, grown 1.5%) take the
                              shot cropped to its focus box grown to the screen's REAL aspect (aspect=,
                              default 16:9; a desk view whose screen runs off both sides passes the zone's
                              own aspect, e.g. aspect=1080:818), perspective-warped (Lanczos). look=photo
                              (default) blurs 0.6 px, lifts blacks to 14 and eases whites to 232, adds one
                              soft glare blob, a light screen vignette and the plate's own grain. Pasted
                              through the loose canted-panel key (r>140, b>140, g<130, r+b-2g>120) dilated
                              --dilate+1 px and feathered 1.2 px. extend=left|right: that side of the
                              screen runs off the frame; the share still in frame is estimated from the
                              two edge heights (pinhole, yaw only, f ~ 1.1 x plate width) and only that
                              part of the shot is shown, so the capture is not squeezed. Needs opencv
                              (cv2), imported only for warp. E.g. --shot 1=shots/readme.png@60,330,1060,560,warp,extend=left
     --card N=path            contain-fit (never crops). Warns if the aspect is >2% off the zone.
                              Default: transparency is flattened onto white, letterbox bars per --letterbox.
     --card N=path --ground fill
                              the zone is first erased into the ground around it (the --logo routine:
                              nearest-ground fill, diffusion, matched grain), then the card is
                              alpha-composited on top, transparency kept, contain-fitted and centred in
                              the zone bbox (no alpha trim, so a card's transparent margins keep their
                              place). For cards rendered WITHOUT --bg onto textured grounds.
                              --ground applies to every --card on magenta zones.
     --card CN=path           a card into cyan zone N: always the --ground fill path (cyan zones are
                              erased, never edge-matted). Unlike --logo it is not trimmed to its alpha.
     --logo N=path[@scale][,bottom|top]
                              cyan zone N; logo trimmed to its alpha, fitted to scale x zone (0.9),
                              centred. ,bottom puts the trimmed cutout flush on the zone's bottom edge
                              (a pose's feet on its painted shadow when the slot is taller than the
                              pose), ,top on its top edge; horizontal stays centred. @bottom alone
                              keeps scale 0.9. E.g. --logo C1=poses/assembler.png@1.0,bottom
                              ,tight: the erased slot carries relief quilted from clean ground tiles
                              near the zone (high-pass, overlap-added, random flips) instead of flat
                              diffusion + noise, so a slot much wider than its pose leaves no flat
                              rectangle (wide pose slots on covers). ,fill=#rrggbb: erase the slot to that one
                              colour (plus the surround's grain) instead of sampling the ground, for a slot
                              that touches a lighter surface (a mascot slot on a title bar); match the plate's
                              own ground colour (the report prints it). Pick one of the two.
                              E.g. --logo C1=poses/plug.png@1.0,bottom,tight
     --paste path@x,y,w,h[,erase]
                              after compositing, contain-fit an RGBA card (transparency kept, centred)
                              into the box x,y,w,h in FINAL --size pixels. ,erase first erases exactly
                              that box into the ground around it (same routine as --ground fill).
                              Works on any plate, with or without key zones, e.g. to patch a garbled
                              cover label on a finished slide in place:
       python -I shared/composite.py final/slide-01.png final/slide-01.png \
           --paste cards/label-fix.png@212,860,420,64,erase
                              Render the card at w x h (2x is better) with render-card.mjs; give a
                              transparent card ,erase, or an opaque card that covers the box.
                              Repeatable; applied in order, each on the result of the last.

ZONES   Connected components of key pixels (R>200,G<80,B>200 or HSV near #FF00FF; cyan likewise).
        Magenta zones are M1.., cyan zones C1.., in reading order (rows by vertical overlap, then left).
        Components under --min-zone (0.3% of the plate; cyan --min-logo-zone 0.05%) are ignored.
        N may be written 2 or M2 (--shot/--card) and 2 or C2 (--logo); --card C2 targets cyan. fill < 0.97 = not a clean
        rectangle (rounded corners, or something overlaps the panel); the mask respects that shape.
MASK    The zone's own component pixels (+ specks < 0.05% filled), dilated --dilate px (2) to swallow the
        anti-aliased fringe. Shots are sampled past the bbox into that margin; cards are edge-extended.
        --edge matte (default) un-mixes each fringe pixel against its nearest untinted neighbour, so thin
        ink outlines survive and rounded corners stay anti-aliased; --edge hard = plain binary paste.
CHECK   Pixels with a visible key tint (~20%+ key blended into ink/paper) left in each zone bbox +6 px
        outside the fully replaced area. > --max-leftover (50) -> that zone is redone once at
        --dilate-retry (5); still over -> exit 3, naming the zone, the edges and the bbox.
        When the plate's own ground 8-20 px outside a zone already leans toward the key (blue sky beside a
        cyan slot reads min(G,B)-R ~ 50-60), a pixel counts only if it leans more than that ground's 95th
        percentile + 25, so clean sky passes and a ~20% key blend over it is still caught.
        Stray key specks under the zone size are warned about, not touched.
        Cyan is processed and checked only when --logo (or a --card CN) is used (otherwise it is
        treated as artwork). Erased zones (--logo, --card CN, --ground fill) replace the whole mask
        dilated 2 px more than --dilate, so an ink outline hugging the zone is erased with it (a
        faint 1 px fringe can stay): key those zones flat on the ground, with no outline.
LETTERBOX --letterbox edge|paper|#rrggbb: fill for bars when the focus/card needs more than the
        asset (edge = asset border colour, default; paper = plate ground).
FINAL   Never stretches: centre-crops the minimal amount of the long axis to the --size aspect
        (--fit pad pads the short axis with grain-matched ground instead), then Lanczos-resizes.
        Warns when the crop cuts a zone or visible artwork.
KEEP    --keep C3 leaves a detected zone untouched as artwork (e.g. a cyan design element).
EXIT    0 ok | 2 bad input / unknown zone / --paste box outside the final size | 3 key colour left
        over or a zone without an asset (output + report are still written so you can look)
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

KEY_NAME = {'M': 'magenta', 'C': 'cyan'}
KEY_HUE = {'M': 300.0, 'C': 180.0}
FILL_WARN = 0.97
ASPECT_WARN = 0.02
CHECK_PAD = 6
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print(f'  WARN {msg}')


def die(msg, code=2):
    print(f'ERROR: {msg}', file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------- key colours

def hsv(a):
    f = a.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx, mn = f.max(-1), f.min(-1)
    d = mx - mn
    dd = np.maximum(d, 1e-6)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) * 60
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx / 255


def strict_key(a, k):
    """Pixels that ARE the key colour (zone detection)."""
    r, g, b = a[..., 0].astype(np.int16), a[..., 1].astype(np.int16), a[..., 2].astype(np.int16)
    h, s, v = hsv(a)
    near = (np.abs(h - KEY_HUE[k]) <= 12) & (s >= 0.75) & (v >= 0.75)
    rgb = (r > 200) & (g < 80) & (b > 200) if k == 'M' else (r < 80) & (g > 200) & (b > 200)
    return rgb | near


def key_tint(a, k):
    """Key colour or any visible blend of it with ink/paper (~20%+ key): the leftover check."""
    a = a.astype(np.int16)
    p, q, o = (a[..., 0], a[..., 2], a[..., 1]) if k == 'M' else (a[..., 1], a[..., 2], a[..., 0])
    return (np.minimum(p, q) - o > 40) & (np.abs(p - q) < 70)


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r + r


# ---------------------------------------------------------------- zones

def find_zones(a, k, min_frac):
    key = strict_key(a, k)
    lab, n = ndimage.label(key)
    H, W = key.shape
    zones, small = [], []
    if n == 0:
        return zones, small
    areas = ndimage.sum_labels(key, lab, index=np.arange(1, n + 1))
    for i, (sl, area) in enumerate(zip(ndimage.find_objects(lab), areas), start=1):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        z = dict(key=KEY_NAME[k], kind=k, x=int(x0), y=int(y0), w=int(x1 - x0), h=int(y1 - y0), area=int(area))
        if area < min_frac * H * W:
            if area >= 50:
                small.append(z)
            continue
        comp = lab[sl] == i
        z['K'] = np.median(a[sl][comp], axis=0).astype(np.float32)   # this zone's actual key colour
        holes, nh = ndimage.label(ndimage.binary_fill_holes(comp) & ~comp)
        z['holes_filled'] = z['holes_kept'] = 0
        if nh:
            hs = ndimage.sum_labels(holes > 0, holes, index=np.arange(1, nh + 1))
            tiny = np.where(hs <= max(25, 0.0005 * area))[0] + 1
            comp = comp | np.isin(holes, tiny)
            z['holes_filled'], z['holes_kept'] = int(len(tiny)), int(nh - len(tiny))
        z['core'] = comp
        z['aspect'] = round(z['w'] / z['h'], 4)
        z['fill'] = round(area / (z['w'] * z['h']), 4)
        zones.append(z)
    # reading order: rows of zones that overlap vertically by >= half the smaller height, then left->right
    rows = []
    for z in sorted(zones, key=lambda z: (z['y'], z['x'])):
        for row in rows:
            ref = row[0]
            ov = min(z['y'] + z['h'], ref['y'] + ref['h']) - max(z['y'], ref['y'])
            if ov >= 0.5 * min(z['h'], ref['h']):
                row.append(z)
                break
        else:
            rows.append([z])
    rows.sort(key=lambda r: min(z['y'] for z in r))
    zones = [z for r in rows for z in sorted(r, key=lambda z: z['x'])]
    for i, z in enumerate(zones, 1):
        z['id'] = f'{k}{i}'
    return zones, small


def zone_mask(z, d, W, H, margin=None):
    """Component (+tiny holes) and its d-px dilation, in the window bbox +- margin (clamped).
    Returns mask, core, window."""
    mg = d if margin is None else margin
    x0, y0 = max(0, z['x'] - mg), max(0, z['y'] - mg)
    x1, y1 = min(W, z['x'] + z['w'] + mg), min(H, z['y'] + z['h'] + mg)
    core = np.zeros((y1 - y0, x1 - x0), bool)
    core[z['y'] - y0:z['y'] - y0 + z['h'], z['x'] - x0:z['x'] - x0 + z['w']] = z['core']
    m = ndimage.binary_dilation(core, structure=disk(d)) if d > 0 else core
    return m, core, (x0, y0, x1, y1)


def keyness(P, k):
    """How far a pixel leans toward the key: min(R,B)-G for magenta, min(G,B)-R for cyan."""
    return (np.minimum(P[..., 0], P[..., 2]) - P[..., 1] if k == 'M'
            else np.minimum(P[..., 1], P[..., 2]) - P[..., 0])


def edge_matte(P, z, mask, core):
    """Alpha for one zone window: 1 on the component, 0 outside the dilated mask, and in the d-px ring
    the key's share of each anti-aliased pixel, un-mixed against its local background B (the nearest
    plate pixel with no key tint: ink outline, paper, an overlapping sticker...). Compositing
    a*S + (1-a)*B keeps thin outlines intact and gives soft edges on rounded corners with no tint."""
    alpha = core.astype(np.float32)
    B = P
    ring = mask & ~core
    if not ring.any():
        return alpha, B
    bgc = ~core & (keyness(P, z['kind']) <= 8)
    if not bgc.any():
        alpha[ring] = 1
        return alpha, B
    iy, ix = ndimage.distance_transform_edt(~bgc, return_distances=False, return_indices=True)
    B = P[iy, ix]
    KB = z['K'] - B
    den = (KB * KB).sum(-1)
    a = np.clip(((P - B) * KB).sum(-1) / np.maximum(den, 1.0), 0, 1)
    a[den < 2000] = 1
    alpha[ring] = a[ring]
    return alpha, B


def compose(out, plate, z, d, W, H, edge, make_src):
    """Paste make_src(window) into zone z through its mask. Returns (covered, window) where covered is
    the part of the window that is guaranteed asset pixels (excluded from the leftover check)."""
    mask, core, win = zone_mask(z, d, W, H, margin=d + 4)
    x0, y0, x1, y1 = win
    S = make_src(win).astype(np.float32)
    region = out[y0:y1, x0:x1]
    if edge == 'hard':
        region[mask] = np.clip(S[mask] + 0.5, 0, 255).astype(np.uint8)
        return mask, win
    P = plate[y0:y1, x0:x1].astype(np.float32)
    alpha, B = edge_matte(P, z, mask, core)
    a = alpha[..., None]
    comp = a * S + (1 - a) * B
    region[mask] = np.clip(comp[mask] + 0.5, 0, 255).astype(np.uint8)
    return core | (alpha >= 0.999), win


# ---------------------------------------------------------------- assets

def load_rgb(path, what):
    p = Path(path)
    if not p.is_file():
        die(f'{what} not found: {path}')
    if p.suffix.lower() == '.svg':
        die(f'{what} is an SVG; rasterize it to PNG first: {path}')
    im = Image.open(p)
    if im.mode in ('RGBA', 'LA', 'PA') or (im.mode == 'P' and 'transparency' in im.info):
        rgba = im.convert('RGBA')
        if rgba.getchannel('A').getextrema()[0] < 255:
            warn(f'{p.name} has transparency; flattened onto white')
        bg = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, rgba).convert('RGB')
    return im.convert('RGB')


def border_colour(arr):
    edge = np.concatenate([arr[0], arr[-1], arr[:, 0], arr[:, -1]])
    return np.median(edge, axis=0).astype(np.uint8)


def resample_box(img, box, size, edge_allow, fill=None):
    """Lanczos-resample the float box of img to size; the box may overhang the image (padded)."""
    W, H = img.size
    x0, y0, x1, y1 = box
    l, t = max(0, math.ceil(-x0 - 1e-6)), max(0, math.ceil(-y0 - 1e-6))
    r, b = max(0, math.ceil(x1 - W - 1e-6)), max(0, math.ceil(y1 - H - 1e-6))
    letterbox = False
    if l or t or r or b:
        a = np.asarray(img)
        if max(l, t, r, b) <= edge_allow:          # only the dilation margin overhangs: replicate the edge
            a = np.pad(a, ((t, b), (l, r), (0, 0)), mode='edge')
        else:                                       # focus box forces a bigger box than the image: letterbox
            letterbox = True
            big = np.empty((H + t + b, W + l + r, 3), np.uint8)
            big[:] = border_colour(a) if fill is None else fill
            big[t:t + H, l:l + W] = a
            a = big
        img = Image.fromarray(a)
    out = img.resize(size, Image.LANCZOS, box=(x0 + l, y0 + t, x1 + l, y1 + t))
    return np.asarray(out), letterbox


def fit_shot(shot, z, win, focus, fill=None):
    sw, sh = shot.size
    bw, bh = z['w'], z['h']
    t = bw / bh
    if focus:
        fx, fy, fw, fh = focus
        if fx < 0 or fy < 0 or fx + fw > sw or fy + fh > sh or fw <= 0 or fh <= 0:
            die(f'{z["id"]}: focus box {focus} is outside the {sw}x{sh} shot')
        cw, ch = (fh * t, fh) if fw / fh < t else (fw, fw / t)
        cx, cy = fx + fw / 2, fy + fh / 2
    else:
        cw, ch = (sh * t, sh) if sw / sh > t else (sw, sw / t)
        cx, cy = sw / 2, sh / 2
    x0 = min(max(0.0, cx - cw / 2), sw - cw) if cw <= sw else (sw - cw) / 2
    y0 = min(max(0.0, cy - ch / 2), sh - ch) if ch <= sh else (sh - ch) / 2
    k = bw / cw                                    # zone px per shot px
    wx0, wy0, wx1, wy1 = win
    box = (x0 + (wx0 - z['x']) / k, y0 + (wy0 - z['y']) / k, x0 + (wx1 - z['x']) / k, y0 + (wy1 - z['y']) / k)
    arr, letterbox = resample_box(shot, box, (wx1 - wx0, wy1 - wy0), edge_allow=12 / k + 2, fill=fill)
    lost_w = max(0.0, 1 - cw / sw)
    lost_h = max(0.0, 1 - ch / sh)
    info = dict(mode='cover', shot_size=[sw, sh], focus=list(focus) if focus else None,
                crop=[round(x0, 1), round(y0, 1), round(cw, 1), round(ch, 1)], scale=round(k, 4),
                lost_w=round(lost_w, 3), lost_h=round(lost_h, 3), letterbox=letterbox)
    return arr, info


def fit_card(card, z, win, fill=None):
    cw, ch = card.size
    bw, bh = z['w'], z['h']
    diff = (cw / ch) / (bw / bh) - 1
    s = min(bw / cw, bh / ch)
    nw, nh = max(1, round(cw * s)), max(1, round(ch * s))
    c = card if (nw, nh) == (cw, ch) else card.resize((nw, nh), Image.LANCZOS)
    a = np.asarray(c)
    canvas = np.empty((bh, bw, 3), np.uint8)
    canvas[:] = border_colour(a) if fill is None else fill
    ox, oy = (bw - nw) // 2, (bh - nh) // 2
    canvas[oy:oy + nh, ox:ox + nw] = a
    wx0, wy0, wx1, wy1 = win
    pad = ((z['y'] - wy0, wy1 - z['y'] - bh), (z['x'] - wx0, wx1 - z['x'] - bw), (0, 0))
    info = dict(mode='contain', card_size=[cw, ch], aspect_diff=round(diff, 4), scale=round(s, 4),
                placed=[z['x'] + ox, z['y'] + oy, nw, nh], resampled=(nw, nh) != (cw, ch))
    return np.pad(canvas, pad, mode='edge'), info


def ground_texture(plate, z, x0, y0, x1, y1, rng):
    """Borrowed relief for a --logo ...,tight erase. The plate's clean ground (no key tint, no ink or
    edges) is cut into small tiles; the ones nearest the zone are high-passed (sigma 14 px) and
    overlap-added at random with random flips over the window, normalised so the texture keeps its
    strength. The repainted slot then carries the paper's own relief instead of flat diffusion +
    noise. Returns (texture HxWx3 float, tiles used) or (None, 0) when the plate has no clean ground."""
    H, W = plate.shape[:2]
    bw, bh = x1 - x0, y1 - y0
    t = int(max(32, min(64, min(z["w"], z["h"]) // 2)))
    P = plate.astype(np.float32)
    L = P.mean(-1)
    bad = ((keyness(P, 'C') > 8) | (keyness(P, 'M') > 8)
           | (np.abs(L - ndimage.gaussian_filter(L, 8)) > 14)).astype(np.float32)
    bad[max(0, y0 - t):y1 + t, max(0, x0 - t):x1 + t] = 1          # never borrow from the zone itself
    frac = ndimage.uniform_filter(bad, size=t, mode='constant', cval=1.0)
    half = t // 2
    cy, cx = np.mgrid[half:H - half:max(4, t // 4), half:W - half:max(4, t // 4)]
    ok = frac[cy, cx] == 0
    if not ok.any():
        return None, 0
    cy, cx = cy[ok], cx[ok]
    zc = np.array([(y0 + y1) / 2, (x0 + x1) / 2])
    order = np.argsort((cy - zc[0]) ** 2 + (cx - zc[1]) ** 2)[:24]
    tiles = []
    for i in order:
        S = P[cy[i] - half:cy[i] - half + t, cx[i] - half:cx[i] - half + t]
        tiles.append(S - ndimage.gaussian_filter(S, sigma=(14, 14, 0), mode="reflect"))
    w1 = np.hanning(t + 2)[1:-1].astype(np.float32)
    win = np.outer(w1, w1)[..., None]
    acc = np.zeros((bh + t, bw + t, 3), np.float32)
    wsq = np.zeros((bh + t, bw + t, 1), np.float32)
    for yy in range(0, bh + 1, half):
        for xx in range(0, bw + 1, half):
            T = tiles[rng.integers(len(tiles))]
            if rng.random() < 0.5:
                T = T[::-1]
            if rng.random() < 0.5:
                T = T[:, ::-1]
            acc[yy:yy + t, xx:xx + t] += T * win
            wsq[yy:yy + t, xx:xx + t] += win * win
    tex = acc / np.sqrt(np.maximum(wsq, 1e-3))
    return tex[half:half + bh, half:half + bw], len(tiles)


def erase_zone(out, plate, z, dd, W, H, rng, what='zone', fill=None, tight=False):
    """Erase z's core dilated dd px (in place, in out) into the ground around it, read from plate.
    Inpainted from the untinted pixels beyond it: nearest-ground fill, then diffused so tile shading
    and paper gradients carry through, plus grain matched to the surrounding texture. The plate's
    ground is the only colour source. Returns (mask, window, info).
    fill=(r,g,b): erase to that one flat colour instead (plus the surround's grain).
    tight=True: the diffused fill carries relief quilted from clean ground tiles near the zone
    (ground_texture) instead of synthetic grain, so a wide slot leaves no flat rectangle."""
    mask, core, (x0, y0, x1, y1) = zone_mask(z, dd, W, H, margin=dd + 14)
    P = plate[y0:y1, x0:x1].astype(np.float32)
    known = (~ndimage.binary_dilation(core, structure=disk(dd + 2))
             & (keyness(P, 'C') <= 8) & (keyness(P, 'M') <= 8))
    ring = known & ndimage.binary_dilation(core, structure=disk(dd + 12))
    if ring.sum() < 20:
        die(f'{z["id"]}: no ground around the {what} to sample')
    if fill is not None:
        F = np.empty_like(P)
        F[:] = np.asarray(fill, np.float32)
    else:
        iy, ix = ndimage.distance_transform_edt(~known, return_distances=False, return_indices=True)
        F = P[iy, ix]
        s = max(2.0, min(z['w'], z['h']) / 12)
        for _ in range(12):
            F = ndimage.gaussian_filter(F, sigma=(s, s, 0))
            F[known] = P[known]
    px = P[ring]
    ground = np.median(px, axis=0)
    # grain = robust spread of the high-pass luma (minus a 2 px local mean over known pixels), so a
    # ground's falloff, mottling or vignette across the ring does not read as grain
    L = P.mean(-1)
    kn = known.astype(np.float32)
    Ls = ndimage.gaussian_filter(L * kn, 2) / np.maximum(ndimage.gaussian_filter(kn, 2), 1e-3)
    hp = (L - Ls)[ring]
    sigma = float(min(6.0, 1.4826 * np.median(np.abs(hp - np.median(hp))) / 0.98))
    info = dict(ground=[int(v) for v in ground], grain=round(sigma, 2))
    T = None
    if tight and fill is None:
        T, n = ground_texture(plate, z, x0, y0, x1, y1, rng)
        info['texture_tiles'] = n
        if T is None:
            warn(f'{z["id"]}: ,tight found no clean ground on the plate to borrow; plain erase used')
    if T is not None:
        F = F + T
    else:
        F = F + rng.normal(0, sigma, F.shape[:2] + (1,))
    if fill is not None:
        info['fill'] = [int(v) for v in fill]
    region = out[y0:y1, x0:x1]
    region[mask] = np.clip(F[mask] + 0.5, 0, 255).astype(np.uint8)
    return mask, (x0, y0, x1, y1), info


def load_rgba(path, what):
    p = Path(path)
    if not p.is_file():
        die(f'{what} not found: {path}')
    if p.suffix.lower() == '.svg':
        die(f'{what} is an SVG; rasterize it to PNG first: {path}')
    return Image.open(p).convert('RGBA')


def contain_rgba(img, bw, bh, scale=1.0):
    """Resize an RGBA image (premultiplied by PIL) to fit scale x (bw, bh), keeping its aspect."""
    s = min(bw * scale / img.width, bh * scale / img.height)
    nw, nh = max(1, round(img.width * s)), max(1, round(img.height * s))
    return (img if (nw, nh) == img.size else img.resize((nw, nh), Image.LANCZOS)), s


def place_rgba(out, img, x, y):
    """Alpha-composite img over out (in place) at x, y. Returns (x, y, w, h, alpha>0) for the check."""
    pil = Image.fromarray(out)
    pil.paste(img, (x, y), img)
    out[:] = np.asarray(pil)
    return x, y, img.width, img.height, np.asarray(img.getchannel('A')) > 0


def anchor_y(z, h, anchor):
    if anchor == 'bottom':
        return z['y'] + z['h'] - h
    if anchor == 'top':
        return z['y']
    return z['y'] + (z['h'] - h) // 2


def paste_logo(out, plate, z, d, logo_path, scale, W, H, rng, anchor='center', fill=None, tight=False):
    """Erase the cyan zone into the ground around it, then contain-fit the logo on top.
    The zone is dilated d+2 (key tiles carry a soft light rim) before erase_zone inpaints it.
    The logo is trimmed to its alpha (> 8) and centred, or put on the zone's bottom/top edge.
    fill / tight: see erase_zone (one flat colour; borrowed ground relief)."""
    covered, win, ginfo = erase_zone(out, plate, z, d + 2, W, H, rng, 'cyan zone', fill=fill, tight=tight)
    logo = load_rgba(logo_path, 'logo')
    bb = logo.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        logo = logo.crop(bb)
    logo, _ = contain_rgba(logo, z['w'], z['h'], scale)
    lx, ly = z['x'] + (z['w'] - logo.width) // 2, anchor_y(z, logo.height, anchor)
    covered_logo = place_rgba(out, logo, lx, ly)
    info = dict(mode='logo', scale=scale, anchor=anchor, placed=[lx, ly, logo.width, logo.height],
                tight=bool(tight), **ginfo)
    return covered, win, covered_logo, info


def loose_magenta(a):
    """The loose canted-panel key: catches the anti-aliased and lens-softened rim a strict key misses."""
    r, g, b = (a[..., i].astype(np.int32) for i in range(3))
    return (r > 140) & (b > 140) & (g < 130) & (r + b - 2 * g > 120)


def zone_quad(comp):
    """4 corners (TL, TR, BR, BL) of a zone drawn in perspective: convex hull -> 4-point polygon
    (minAreaRect if no epsilon gives 4), grown 1.5% from the centroid to cover soft corners."""
    import cv2
    cnts, _ = cv2.findContours(comp.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(max(cnts, key=cv2.contourArea))
    peri = cv2.arcLength(hull, True)
    quad = None
    for eps in np.linspace(0.005, 0.08, 40):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            quad = ap.reshape(4, 2).astype(np.float32)
            break
    if quad is None:
        quad = cv2.boxPoints(cv2.minAreaRect(hull)).astype(np.float32)
    s, d = quad.sum(1), np.diff(quad, axis=1).ravel()
    q = np.array([quad[np.argmin(s)], quad[np.argmin(d)], quad[np.argmax(s)], quad[np.argmax(d)]], np.float32)
    c = q.mean(0)
    return c + (q - c) * 1.015


def visible_fraction(q, side, W):
    """Share of a screen's true width still in frame when its `side` edge runs off the plate. Pinhole
    model with yaw only: per edge, x/h and 1/h are affine in the true position u, so the in-frame width
    in screen heights is sqrt(d(x/h)^2 + (f d(1/h))^2), f ~ 1.1 x plate width (a phone main camera)."""
    tl, tr, br, bl = q
    cx, f = W / 2, 1.1 * W
    hl, hr = np.linalg.norm(bl - tl), np.linalg.norm(br - tr)
    xl, xr = (tl[0] + bl[0]) / 2 - cx, (tr[0] + br[0]) / 2 - cx
    return float(math.hypot(xr / hr - xl / hl, f * (1 / hr - 1 / hl)))


def paste_warp(out, plate, z, d, shot, focus, opt, W, H, rng):
    """--shot N=path@x,y,w,h,warp: perspective-warp the shot onto the zone's 4-corner quad (a screen
    photographed at an angle), give it a photographed-screen look, paste it through the loose key.
    Returns (covered, window, info)."""
    import cv2
    comp = np.zeros((H, W), bool)
    comp[z['y']:z['y'] + z['h'], z['x']:z['x'] + z['w']] = z['core']
    q = zone_quad(comp)
    aspect = opt['aspect']
    sa = np.asarray(shot)
    sh, sw = sa.shape[:2]
    fx, fy, fw, fh = focus if focus else (0, 0, sw, sh)
    if focus and (fx < 0 or fy < 0 or fx + fw > sw or fy + fh > sh or fw <= 0 or fh <= 0):
        die(f'{z["id"]}: focus box {focus} is outside the {sw}x{sh} shot')
    nw, nh = (fh * aspect, fh) if fw / fh < aspect else (fw, fw / aspect)
    k = min(1.0, sw / nw, sh / nh)                 # never grow past the shot: shrink, keeping the aspect
    nw, nh = nw * k, nh * k
    x0 = int(round(min(max(fx + fw / 2 - nw / 2, 0), sw - nw)))
    y0 = int(round(min(max(fy + fh / 2 - nh / 2, 0), sh - nh)))
    src = sa[y0:y0 + int(round(nh)), x0:x0 + int(round(nw))]
    vis = 1.0
    if opt['extend'] != 'none':                    # the screen runs off the frame on that side
        vis = min(1.0, visible_fraction(q, opt['extend'], W) / aspect)
        cut = int(round(src.shape[1] * (1 - vis)))
        src = src[:, cut:] if opt['extend'] == 'left' else src[:, :src.shape[1] - cut]
    qw = max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3]))
    sc = min(1.0, 1.25 * qw / src.shape[1])
    if sc < 1:
        src = cv2.resize(src, (int(src.shape[1] * sc), int(src.shape[0] * sc)), interpolation=cv2.INTER_AREA)
    h2, w2 = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]), q)
    S = cv2.warpPerspective(np.ascontiguousarray(src), M, (W, H), flags=cv2.INTER_LANCZOS4,
                            borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    key = loose_magenta(plate)
    grain = 0.0
    if opt['look'] == 'photo':
        S = cv2.GaussianBlur(S, (0, 0), 0.6)
        S = 14 + S * (232 - 14) / 255.0             # a photographed LCD never reaches 0 or 255
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        tl, tr, br, bl = q
        gx, gy = (tl * 0.35 + tr * 0.65)[0], (tl * 0.35 + tr * 0.65)[1] + (bl[1] - tl[1]) * 0.25
        span = np.linalg.norm(tr - tl)
        S += np.exp(-((xx - gx) ** 2 + (yy - gy) ** 2) / (2 * (span * 0.32) ** 2))[..., None] * 16
        c = q.mean(0)
        rad = np.sqrt(((xx - c[0]) / (span * 0.62)) ** 2 + ((yy - c[1]) / (np.linalg.norm(bl - tl) * 0.62)) ** 2)
        S *= (1 - 0.12 * np.clip(rad - 0.55, 0, 1))[..., None]
        Lp = plate.astype(np.float32).mean(-1)
        hp = Lp - ndimage.gaussian_filter(Lp, 1.5)
        far = ~ndimage.binary_dilation(key, iterations=12)
        v = hp[far]
        v = v[np.abs(v) < 12]
        grain = float(np.std(v)) if v.size else 2.0
        S += rng.normal(0, max(grain, 1.2), (H, W, 1)).astype(np.float32)
    m = key & ndimage.binary_dilation(comp, iterations=4)
    m = ndimage.binary_dilation(m, structure=disk(d + 1)) | comp
    alpha = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)
    solid = ndimage.binary_erosion(m, iterations=1)
    alpha = np.maximum(alpha, solid.astype(np.float32))
    a = alpha[..., None]
    out[:] = np.clip(out.astype(np.float32) * (1 - a) + S * a + 0.5, 0, 255).astype(np.uint8)
    info = dict(mode='warp', shot_size=[sw, sh], focus=list(focus) if focus else None,
                crop=[x0, y0, int(round(nw)), int(round(nh))], quad=[[round(float(v), 1) for v in p] for p in q],
                aspect=round(aspect, 4), extend=opt['extend'], visible=round(vis, 3), look=opt['look'],
                grain=round(grain, 2))
    return alpha >= 0.999, (0, 0, W, H), info


def paste_card_fill(out, plate, z, d, card, W, H, rng):
    """--card with --ground fill (or into a cyan zone): erase the zone into the ground, then
    alpha-composite the RGBA card contain-fitted and centred in the zone bbox (not trimmed)."""
    covered, win, ginfo = erase_zone(out, plate, z, d + 2, W, H, rng, f'{z["key"]} zone')
    cw, ch = card.size
    fitted, s = contain_rgba(card, z['w'], z['h'])
    cx, cy = z['x'] + (z['w'] - fitted.width) // 2, z['y'] + (z['h'] - fitted.height) // 2
    covered_card = place_rgba(out, fitted, cx, cy)
    info = dict(mode='contain', card_size=[cw, ch], aspect_diff=round((cw / ch) / (z['w'] / z['h']) - 1, 4),
                scale=round(s, 4), placed=[cx, cy, fitted.width, fitted.height],
                resampled=fitted.size != (cw, ch), ground_fill=True, **ginfo)
    return covered, win, covered_card, info


# ---------------------------------------------------------------- final geometry

def final_geometry(w, h, W, H, fit):
    T, A = W / H, w / h
    g = dict(mode='none', axis=None, px=0, crop=[0, 0, w, h], pad=[0, 0, 0, 0])
    if abs(A / T - 1) >= 0.0005:
        if fit == 'crop':
            if A > T:
                nw = round(h * T); x0 = (w - nw) // 2
                g.update(mode='crop', axis='x', px=w - nw, crop=[x0, 0, x0 + nw, h])
            else:
                nh = round(w / T); y0 = (h - nh) // 2
                g.update(mode='crop', axis='y', px=h - nh, crop=[0, y0, w, y0 + nh])
        else:
            if A > T:
                nh = round(w / T); t = (nh - h) // 2
                g.update(mode='pad', axis='y', px=nh - h, pad=[0, t, 0, nh - h - t])
            else:
                nw = round(h * T); l = (nw - w) // 2
                g.update(mode='pad', axis='x', px=nw - w, pad=[l, 0, nw - w - l, 0])
    cx0, cy0, cx1, cy1 = g['crop']
    l, t, r, b = g['pad']
    g['scale'] = W / (cx1 - cx0 + l + r)
    return g


def to_out(g, x, y, w, h):
    s = g['scale']
    ox, oy = g['pad'][0] - g['crop'][0], g['pad'][1] - g['crop'][1]
    return [round((x + ox) * s), round((y + oy) * s), round(w * s), round(h * s)]


def crop_checks(plate, zones, g):
    """Warn when the final crop cuts a zone or removes visible artwork (ink) from the plate edge."""
    if g['mode'] != 'crop':
        return
    h, w = plate.shape[:2]
    cx0, cy0, cx1, cy1 = g['crop']
    for z in zones:
        lost = (max(0, cx0 - z['x']) + max(0, z['x'] + z['w'] - cx1) + max(0, cy0 - z['y'])
                + max(0, z['y'] + z['h'] - cy1))
        if lost:
            warn(f'{z["id"]} loses {lost}px to the final crop')
    bands = ([('left', plate[:, :cx0]), ('right', plate[:, cx1:])] if g['axis'] == 'x'
             else [('top', plate[:cy0]), ('bottom', plate[cy1:])])
    for name, band in bands:
        if band.size == 0:
            continue
        luma = band.astype(np.float32).mean(-1)
        ink = int((np.abs(luma - np.median(luma)) > 48).sum())
        if ink > 0.002 * luma.size:
            warn(f'final crop removes {band.shape[0] if g["axis"] == "y" else band.shape[1]}px at the {name} '
                 f'with {ink} ink px of artwork in it; consider --fit pad')
    frac = g['px'] / (h if g['axis'] == 'y' else w)
    if frac > 0.04:
        warn(f'plate aspect {w / h:.3f} needs a {frac:.1%} crop; consider --fit pad')


def finish(out, g, W, H):
    cx0, cy0, cx1, cy1 = g['crop']
    a = out[cy0:cy1, cx0:cx1]
    l, t, r, b = g['pad']
    if l or t or r or b:
        hh, ww = a.shape[:2]
        rng = np.random.default_rng(7)
        if g['axis'] == 'x':
            strips = [a[:, :24], a[:, -24:]]
        else:
            strips = [a[:24], a[-24:]]
        edge = np.concatenate([s.reshape(-1, 3) for s in strips]).astype(np.float32)
        base = np.median(edge, axis=0)
        sd = float(edge.std(axis=0).mean()) * 0.6
        canvas = np.clip(base + rng.normal(0, sd, (hh + t + b, ww + l + r, 1)), 0, 255).astype(np.uint8)
        canvas[t:t + hh, l:l + ww] = a
        a = canvas
    img = Image.fromarray(np.ascontiguousarray(a))
    return img if img.size == (W, H) else img.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- CLI helpers

ANCHORS = ('bottom', 'top', 'center', 'centre')


def parse_spec(spec, flag, kind, also=None):
    """N=path[@extra] -> (zone id, path, extra). kind = the default key; also = another key the flag
    may target with an explicit prefix (--card C2=...). --logo extra = (scale, anchor)."""
    m = re.match(r'^\s*([MmCc]?)(\d+)\s*=(.+)$', spec)
    if not m:
        die(f'{flag} {spec!r}: expected N=path')
    prefix, n, rest = m.group(1).upper(), int(m.group(2)), m.group(3).strip()
    if prefix and prefix not in (kind, also):
        die(f'{flag} {spec!r}: {flag} targets {KEY_NAME[kind]} zones ({kind}N), not {prefix}{n}')
    extra = None
    if flag == '--logo':
        m2 = re.match(r'^(.*)@([\w.,\s=#]+)$', rest)
        toks = [t.strip().lower() for t in m2.group(2).split(',') if t.strip()] if m2 else []
        nums = [t for t in toks if re.fullmatch(r'\d*\.?\d+', t)]
        fills = [t for t in toks if t.startswith('fill=')]
        words = [t for t in toks if t not in nums and t not in fills and t != 'tight']
        # an '@' followed by anything else (logo@2x.png) is part of the path, as before
        if toks and all(t in nums or t in ANCHORS or t in fills or t == 'tight' for t in toks):
            if len(nums) > 1 or len(words) > 1 or len(fills) > 1:
                die(f'--logo {spec!r}: expected @scale, @scale,bottom|top or @bottom|top, optionally with '
                    f',tight or ,fill=#rrggbb (scale = fraction of the zone, e.g. @0.9,bottom,tight)')
            fill = None
            if fills:
                if not re.fullmatch(r'fill=#[0-9a-f]{6}', fills[0]):
                    die(f'--logo {spec!r}: fill must be fill=#rrggbb')
                fill = tuple(int(fills[0][i:i + 2], 16) for i in (6, 8, 10))
            if fill and 'tight' in toks:
                die(f'--logo {spec!r}: pick one of ,tight and ,fill=')
            anchor = words[0].replace('centre', 'center') if words else 'center'
            rest, extra = m2.group(1), (float(nums[0]) if nums else 0.9, anchor, fill, 'tight' in toks)
    elif flag == '--shot':
        m2 = re.match(r'^(.*)@([\w.,:=\s]+)$', rest)
        toks = [t.strip().lower() for t in m2.group(2).split(',') if t.strip()] if m2 else []
        nums = [t for t in toks if re.fullmatch(r'-?\d*\.?\d+', t)]
        opts = [t for t in toks if t not in nums]
        known = lambda t: t == 'warp' or re.fullmatch(r'(aspect=\d*\.?\d+(:\d*\.?\d+)?|look=(photo|none)|'
                                                      r'extend=(left|right|none))', t)
        # as before, an '@' followed by anything else (shot@2x.png) stays part of the path
        if toks and all(t in nums or known(t) for t in toks):
            rest = m2.group(1)
            focus = [float(v) for v in nums] or None
            if focus is not None and len(focus) != 4:
                die(f'--shot {spec!r}: focus box must be @x,y,w,h')
            if opts and 'warp' not in opts:
                die(f'--shot {spec!r}: aspect=, look= and extend= only go with ,warp')
            warp = None
            if 'warp' in opts:
                warp = dict(aspect=16 / 9, look='photo', extend='none')
                for t in opts:
                    if t.startswith('aspect='):
                        a, _, b = t[7:].partition(':')
                        warp['aspect'] = float(a) / float(b) if b else float(a)
                    elif t.startswith('look='):
                        warp['look'] = t[5:]
                    elif t.startswith('extend='):
                        warp['extend'] = t[7:]
            extra = focus if warp is None else (focus, warp)
    return f'{prefix or kind}{n}', rest, extra


def parse_paste(spec, TW, TH):
    """path@x,y,w,h[,erase] in final --size pixels."""
    m = re.match(r'^(.+?)@\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*((?:,\s*[A-Za-z]+\s*)*)$', spec)
    if not m:
        die(f'--paste {spec!r}: expected path@x,y,w,h[,erase] (final --size pixels)')
    path = m.group(1).strip()
    x, y, w, h = (int(m.group(i)) for i in range(2, 6))
    opts = [o.strip().lower() for o in m.group(6).split(',') if o.strip()]
    bad = [o for o in opts if o != 'erase']
    if bad:
        die(f'--paste {spec!r}: unknown option(s) {", ".join(bad)} (only: erase)')
    if w <= 0 or h <= 0 or x + w > TW or y + h > TH:
        die(f'--paste {spec!r}: box {x},{y} {w}x{h} is outside the {TW}x{TH} final image')
    return path, (x, y, w, h), 'erase' in opts


def zone_row(z, g):
    ob = to_out(g, z['x'], z['y'], z['w'], z['h'])
    return dict(id=z['id'], key=z['key'], bbox=[z['x'], z['y'], z['w'], z['h']], aspect=z['aspect'],
                fill=z['fill'], area=z['area'], holes_filled=z['holes_filled'], holes_kept=z['holes_kept'],
                out_bbox=ob)


def print_table(zones, g, size):
    print(f'{"zone":5} {"key":8} {"bbox x,y wxh":22} {"aspect":>7} {"fill":>7}  out bbox ({size})')
    for z in zones:
        ob = to_out(g, z['x'], z['y'], z['w'], z['h'])
        print(f'{z["id"]:5} {z["key"]:8} {z["x"]:>4},{z["y"]:<4} {z["w"]:>4}x{z["h"]:<6} {z["aspect"]:>7.3f} '
              f'{z["fill"]:>7.1%}  {ob[0]},{ob[1]} {ob[2]}x{ob[3]}'
              + ('' if z['fill'] >= FILL_WARN else '  <- not a clean rectangle'))


def debug_png(plate, zones, g, path):
    img = Image.fromarray(plate).convert('RGBA')
    over = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    W = img.width
    fs = max(14, W // 45)
    try:
        font = ImageFont.truetype('arialbd.ttf', fs)
    except OSError:
        font = ImageFont.load_default(size=fs)
    if g['mode'] == 'crop':
        cx0, cy0, cx1, cy1 = g['crop']
        for box in ([(0, 0, cx0, img.height), (cx1, 0, W, img.height)] if g['axis'] == 'x'
                    else [(0, 0, W, cy0), (0, cy1, W, img.height)]):
            if box[2] > box[0] and box[3] > box[1]:
                d.rectangle(box, fill=(255, 0, 0, 70))
    lw = max(3, W // 300)
    for z in zones:
        col = (255, 214, 0, 255) if z['kind'] == 'M' else (255, 60, 0, 255)
        b = (z['x'], z['y'], z['x'] + z['w'] - 1, z['y'] + z['h'] - 1)
        d.rectangle(b, outline=(0, 0, 0, 255), width=lw + 2)
        d.rectangle(b, outline=col, width=lw)
        label = f'{z["id"]}  {z["w"]}x{z["h"]}  a{z["aspect"]:.3f}  f{z["fill"]:.1%}'
        if z['kind'] == 'C':
            label = z['id']
        tb = d.textbbox((0, 0), label, font=font)
        tx, ty = z['x'] + lw + 4, z['y'] + lw + 4
        d.rectangle((tx - 4, ty - 4, tx + tb[2] + 6, ty + tb[3] + 6), fill=(0, 0, 0, 220))
        d.text((tx, ty), label, font=font, fill=col)
    Image.alpha_composite(img, over).convert('RGB').save(path)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plate')
    ap.add_argument('out', nargs='?')
    ap.add_argument('--shot', action='append', default=[], metavar='N=path[@x,y,w,h][,warp[,aspect=W:H][,look=photo|none][,extend=left|right]]')
    ap.add_argument('--card', action='append', default=[], metavar='N=path')
    ap.add_argument('--logo', action='append', default=[], metavar='N=path[@scale][,bottom|top][,tight|,fill=#rrggbb]')
    ap.add_argument('--ground', choices=['none', 'fill'], default='none',
                    help='fill = erase each --card magenta zone into the surrounding ground and '
                         'alpha-composite the card on top (transparency kept); none = flatten onto white')
    ap.add_argument('--paste', action='append', default=[], metavar='path@x,y,w,h[,erase]',
                    help='after compositing, contain-fit an RGBA card into a box in final --size px; '
                         ',erase first erases the box into the ground around it')
    ap.add_argument('--size', default='1080x1350')
    ap.add_argument('--fit', choices=['crop', 'pad'], default='crop')
    ap.add_argument('--letterbox', default='edge', metavar='edge|paper|#rrggbb',
                    help='fill for letterbox bars when a focus box or card needs more than the asset: '
                         'edge = the border colour of the asset (default; right for dark captures), '
                         'paper = the plate ground (median of the outer 2%% of the plate), or a hex colour')
    ap.add_argument('--report')
    ap.add_argument('--zones-only', action='store_true')
    ap.add_argument('--keep', action='append', default=[], metavar='ZONE',
                    help='leave a detected zone untouched as artwork (e.g. --keep C3); skips its checks')
    ap.add_argument('--edge', choices=['matte', 'hard'], default='matte')
    ap.add_argument('--dilate', type=int, default=2)
    ap.add_argument('--dilate-retry', type=int, default=5)
    ap.add_argument('--max-leftover', type=int, default=50)
    ap.add_argument('--min-zone', type=float, default=0.003)
    ap.add_argument('--min-logo-zone', type=float, default=0.0005)
    args = ap.parse_args()

    m = re.match(r'^(\d+)x(\d+)$', args.size)
    if not m:
        die('--size must look like 1080x1350')
    TW, TH = int(m.group(1)), int(m.group(2))
    pastes = [parse_paste(s, TW, TH) for s in args.paste]
    if not Path(args.plate).is_file():
        die(f'plate not found: {args.plate}')
    plate_img = Image.open(args.plate).convert('RGB')
    plate = np.asarray(plate_img).copy()
    H, W = plate.shape[:2]
    g = final_geometry(W, H, TW, TH, args.fit)

    mzones, msmall = find_zones(plate, 'M', args.min_zone)
    czones, csmall = find_zones(plate, 'C', args.min_logo_zone)
    print(f'plate {Path(args.plate).name} {W}x{H} (aspect {W / H:.3f}) -> {TW}x{TH}: '
          + (f'{g["mode"]} {g["px"]}px on {g["axis"]}' if g['mode'] != 'none' else 'no crop'))
    print_table(mzones + czones, g, args.size)
    for z in mzones + czones:
        if z['fill'] < FILL_WARN:
            warn(f'{z["id"]} fill {z["fill"]:.1%} < 97%: not a clean rectangle (rounded or overlapped); '
                 f'mask follows the drawn shape' + (f', {z["holes_kept"]} occluder hole(s) kept' if z['holes_kept'] else ''))
    for z in msmall:
        warn(f'stray magenta speck {z["w"]}x{z["h"]} at {z["x"]},{z["y"]} ({z["area"]}px) is below '
             f'--min-zone and stays as is')
    report = dict(plate=str(args.plate), plate_size=[W, H], size=[TW, TH], final=g,
                  zones=[zone_row(z, g) for z in mzones + czones],
                  small_components=[dict(key=z['key'], bbox=[z['x'], z['y'], z['w'], z['h']], area=z['area'])
                                    for z in msmall + csmall])

    if args.zones_only:
        crop_checks(plate, mzones + czones, g)
        dbg = args.out or str(Path(args.plate).with_suffix('.zones.png'))
        Path(dbg).parent.mkdir(parents=True, exist_ok=True)
        debug_png(plate, mzones + czones, g, dbg)
        print(f'debug -> {dbg}')
        if args.report:
            report['warnings'] = WARNINGS
            Path(args.report).write_text(json.dumps(report, indent=1), encoding='utf-8')
        return 0
    if not args.out:
        die('missing <out.png> (or pass --zones-only)')

    # ---- assignments
    zmap = {z['id']: z for z in mzones + czones}
    assign = {}
    for flag, specs, kind, also in (('--shot', args.shot, 'M', None), ('--card', args.card, 'M', 'C'),
                                    ('--logo', args.logo, 'C', None)):
        for spec in specs:
            zid, path, extra = parse_spec(spec, flag, kind, also)
            if zid not in zmap:
                have = ', '.join(z['id'] for z in (mzones if zid[0] == 'M' else czones)) or 'none'
                die(f'{flag} {spec!r}: no zone {zid} (zones: {have}); run --zones-only')
            if zid in assign:
                die(f'zone {zid} assigned twice')
            assign[zid] = (flag[2:], path, extra)
    keep = {k.strip().upper() for k in args.keep}
    for k in keep:
        if k not in zmap:
            die(f'--keep {k}: no such zone')
        if k in assign:
            die(f'--keep {k}: zone also has an asset')
    cyan_on = any(zid[0] == 'C' for zid in assign)
    active = [z for z in mzones + (czones if cyan_on else []) if z['id'] not in keep]
    if czones and not cyan_on:
        print(f'  note: {len(czones)} cyan zone(s) left as artwork (no --logo given)')

    out = plate.copy()
    covered = np.zeros((H, W), bool)
    rows = {z['id']: zone_row(z, g) for z in mzones + czones}
    loaded = {}

    lb_fill = None                                  # --letterbox: colour for letterbox bars
    if args.letterbox == 'paper':
        pa = np.asarray(plate)[..., :3]
        bw = max(4, int(min(pa.shape[:2]) * 0.02))
        ring = np.concatenate([pa[:bw].reshape(-1, 3), pa[-bw:].reshape(-1, 3),
                               pa[:, :bw].reshape(-1, 3), pa[:, -bw:].reshape(-1, 3)])
        lb_fill = np.median(ring, axis=0).astype(np.uint8)
    elif args.letterbox.startswith('#') and len(args.letterbox) == 7:
        lb_fill = np.array([int(args.letterbox[i:i + 2], 16) for i in (1, 3, 5)], np.uint8)
    elif args.letterbox != 'edge':
        die(f'--letterbox must be edge, paper or #rrggbb, not {args.letterbox!r}')

    def apply(z, d):
        kind, path, extra = assign[z['id']]
        row = rows[z['id']]
        row['asset'] = dict(type=kind, path=path)
        row['dilate'], row['edge'] = d, args.edge
        fill_card = kind == 'card' and (z['kind'] == 'C' or args.ground == 'fill')
        if kind == 'logo' or fill_card:
            rng = np.random.default_rng(int(z['id'][1:]) + (0 if z['kind'] == 'C' else 100))
            if kind == 'logo':
                scale, anchor, lfill, tight = extra if extra else (0.9, 'center', None, False)
                cov, (x0, y0, x1, y1), (lx, ly, lw, lh, la), info = paste_logo(
                    out, plate, z, d, path, scale, W, H, rng, anchor, lfill, tight)
            else:
                if ('rgba', path) not in loaded:
                    loaded[('rgba', path)] = load_rgba(path, 'card')
                cov, (x0, y0, x1, y1), (lx, ly, lw, lh, la), info = paste_card_fill(
                    out, plate, z, d, loaded[('rgba', path)], W, H, rng)
                row['edge'] = 'erase'
            covered[y0:y1, x0:x1] |= cov
            cx0, cy0 = max(0, lx), max(0, ly)
            cx1, cy1 = min(W, lx + lw), min(H, ly + lh)
            covered[cy0:cy1, cx0:cx1] |= la[cy0 - ly:cy1 - ly, cx0 - lx:cx1 - lx]
            row['fit'] = info
            return
        if path not in loaded:
            loaded[path] = load_rgb(path, kind)
        src, info = loaded[path], {}
        if kind == 'shot' and isinstance(extra, tuple):  # ,warp: perspective onto the zone's quad
            if z['kind'] != 'M':
                die(f'{z["id"]}: ,warp only works on magenta zones')
            cov, _, info = paste_warp(out, plate, z, d, src, extra[0], extra[1], W, H,
                                      np.random.default_rng(int(z['id'][1:]) + 300))
            covered[:] |= cov
            row['fit'] = info
            return

        def make_src(win):
            arr, inf = fit_shot(src, z, win, extra, lb_fill) if kind == 'shot' else fit_card(src, z, win, lb_fill)
            info.update(inf)
            return arr
        cov, (x0, y0, x1, y1) = compose(out, plate, z, d, W, H, args.edge, make_src)
        covered[y0:y1, x0:x1] |= cov
        row['fit'] = info

    def leftover(z):
        x0, y0 = max(0, z['x'] - CHECK_PAD), max(0, z['y'] - CHECK_PAD)
        x1, y1 = min(W, z['x'] + z['w'] + CHECK_PAD), min(H, z['y'] + z['h'] + CHECK_PAD)
        lk = key_tint(out[y0:y1, x0:x1], z['kind']) & ~covered[y0:y1, x0:x1]
        floor = ground_tint(z)
        if floor > 40:                              # the ground itself leans to the key (blue sky by cyan)
            lk &= keyness(out[y0:y1, x0:x1].astype(np.int16), z['kind']) > floor
        n = int(lk.sum())
        if not n:
            return 0, None
        ys, xs = np.nonzero(lk)
        ys, xs = ys + y0, xs + x0
        bx, by = int(xs.min()), int(ys.min())
        bw, bh = int(xs.max()) - bx + 1, int(ys.max()) - by + 1
        # which edge of the zone each leftover pixel hugs (or 'inside' = an interior hole/occluder rim)
        dist = np.stack([xs - z['x'], z['x'] + z['w'] - 1 - xs, ys - z['y'], z['y'] + z['h'] - 1 - ys])
        side = np.where(np.abs(dist).min(0) > CHECK_PAD, 4, np.abs(dist).argmin(0))
        names = ['left', 'right', 'top', 'bottom', 'inside']
        counts = {names[i]: int((side == i).sum()) for i in range(5) if (side == i).any()}
        where = ', '.join(f'{k} {v}' for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
        return n, dict(bbox=[bx, by, bw, bh], where=where, sides=counts)

    tint_floor = {}

    def ground_tint(z):
        """The key-lean a pixel needs before the leftover check counts it: 40 (key_tint's own bar), or,
        when the plate's ground ring 8-20 px outside the zone already leans that way (sky beside a cyan
        slot reads min(G,B)-R ~ 50-60), that ground's 95th percentile + 25, so the sky never counts and
        a 20% key blend over it still does."""
        if z['id'] not in tint_floor:
            mask, core, (wx0, wy0, wx1, wy1) = zone_mask(z, 20, W, H)
            ring = mask & ~ndimage.binary_dilation(core, structure=disk(8))
            P = plate[wy0:wy1, wx0:wx1].astype(np.int16)
            t = keyness(P, z['kind'])[ring & ~strict_key(plate[wy0:wy1, wx0:wx1], z['kind'])]
            tint_floor[z['id']] = float(np.percentile(t, 95)) + 25 if t.size >= 50 else 40.0
        return tint_floor[z['id']]

    failed = []
    unassigned = [z['id'] for z in active if z['id'] not in assign]
    for z in sorted(active, key=lambda z: z['kind'] != 'C'):    # logos first, then magenta panels
        if z['id'] in assign:
            apply(z, args.dilate)
    for z in active:
        row = rows[z['id']]
        if z['id'] in unassigned:
            row['leftover_px'] = z['area']
            continue
        n, where = leftover(z)
        if n > args.max_leftover:
            print(f'  {z["id"]}: {n} key-tinted px left ({where["where"]}) in {where["bbox"]}; '
                  f'retrying with dilation {args.dilate_retry}')
            apply(z, args.dilate_retry)
            n, where = leftover(z)
        row['leftover_px'], row['leftover'] = n, where
        if n > args.max_leftover:
            failed.append(f'{z["id"]}: {n} {z["key"]}-tinted px left ({where["where"]}), '
                          f'bbox {where["bbox"]} x,y,w,h in plate px')

    for zid in rows:
        f = rows[zid].get('fit') or {}
        if f.get('mode') == 'cover':
            eff = f['scale'] * g['scale']
            if eff > 1.25:
                warn(f'{zid}: capture upscaled x{eff:.2f} at final size (soft); capture larger or loosen the focus box')
            if not f['focus'] and max(f['lost_w'], f['lost_h']) > 0.2:
                warn(f'{zid}: cover-fit cut {max(f["lost_w"], f["lost_h"]):.0%} of the shot '
                     f'{"width" if f["lost_w"] > f["lost_h"] else "height"}; '
                     f'pass @x,y,w,h or capture at aspect {zmap[zid]["aspect"]:.3f}')
            if f['letterbox']:
                warn(f'{zid}: focus box needs more than the whole shot at this aspect; padded with its edge colour')
        if f.get('mode') == 'contain' and abs(f['aspect_diff']) > ASPECT_WARN:
            warn(f'{zid}: card aspect is {f["aspect_diff"]:+.1%} off the zone '
                 f'({f["card_size"][0]}x{f["card_size"][1]} vs {zmap[zid]["aspect"]:.3f}); '
                 f'{"ground fill around it" if f.get("ground_fill") else "letterboxed"}. '
                 f'Re-render at the zone aspect')

    crop_checks(plate, mzones + czones, g)
    final = finish(out, g, TW, TH)
    paste_rows = []
    if pastes:                                      # --paste: on the final image, in final px
        fa = np.asarray(final.convert('RGB')).copy()
        for i, (path, (px, py, pw, ph), erase) in enumerate(pastes, 1):
            prow = dict(path=path, box=[px, py, pw, ph], erase=erase)
            if erase:
                pz = dict(id=f'P{i}', key='paste box', kind='P', x=px, y=py, w=pw, h=ph,
                          core=np.ones((ph, pw), bool))
                _, _, ginfo = erase_zone(fa, fa.copy(), pz, 0, TW, TH, np.random.default_rng(200 + i),
                                         'paste box')
                prow.update(ginfo)
            card = load_rgba(path, 'paste card')
            cw, ch = card.size
            fitted, s = contain_rgba(card, pw, ph)
            cx, cy = px + (pw - fitted.width) // 2, py + (ph - fitted.height) // 2
            place_rgba(fa, fitted, cx, cy)
            diff = (cw / ch) / (pw / ph) - 1
            prow.update(card_size=[cw, ch], scale=round(s, 4), placed=[cx, cy, fitted.width, fitted.height],
                        aspect_diff=round(diff, 4))
            if abs(diff) > ASPECT_WARN:
                warn(f'--paste {Path(path).name}: card aspect is {diff:+.1%} off the box {pw}x{ph}; '
                     f'contain-fitted, so part of the box is not covered')
            if s > 1.25:
                warn(f'--paste {Path(path).name}: card upscaled x{s:.2f} (soft); render it at the box size or 2x')
            if not erase and card.getchannel('A').getextrema()[0] < 255:
                warn(f'--paste {Path(path).name}: card has transparency and no ,erase: what is under it shows through')
            print(f'  paste {Path(path).name} -> {cx},{cy} {fitted.width}x{fitted.height}'
                  + (f', erased box on ground {prow["ground"]}' if erase else ''))
            paste_rows.append(prow)
        final = Image.fromarray(fa)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    final.save(args.out)

    for zid, row in rows.items():
        if row.get('asset'):
            f = row['fit']
            desc = (f'warp onto quad {f["quad"]} (aspect {f["aspect"]}, visible {f["visible"]}, look {f["look"]})'
                    if f['mode'] == 'warp' else
                    f'cover crop {f["crop"]} x{f["scale"]:.3f}' if f['mode'] == 'cover'
                    else f'contain {f["placed"][2]}x{f["placed"][3]}'
                    + (f' on ground {f["ground"]}' if f.get('ground_fill') else '') if f['mode'] == 'contain'
                    else f'logo {f["placed"][2]}x{f["placed"][3]} ({f["anchor"]}) on ground {f["ground"]}')
            print(f'  {zid} <- {Path(row["asset"]["path"]).name}: {desc}, dilate {row["dilate"]}, '
                  f'leftover {row["leftover_px"]}px')
    status = 'ok'
    if unassigned:
        failed.insert(0, f'zone(s) with no asset: {", ".join(unassigned)} (assign one, or --keep it)')
    if failed:
        status = 'fail'
        sys.stdout.flush()
        for f in failed:
            print(f'  FAIL {f}', file=sys.stderr)
    report.update(out=str(args.out), zones=list(rows.values()), pastes=paste_rows, warnings=WARNINGS,
                  failures=failed, status=status)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=1), encoding='utf-8')
    print(f'wrote {args.out} ({TW}x{TH}) status {status}')
    return 3 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
