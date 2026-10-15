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
     --card N=path            contain-fit (never crops). Warns if the aspect is >2% off the zone.
     --logo N=path[@scale]    cyan zone N; logo trimmed to its alpha, fitted to scale x zone (0.9).

ZONES   Connected components of key pixels (R>200,G<80,B>200 or HSV near #FF00FF; cyan likewise).
        Magenta zones are M1.., cyan zones C1.., in reading order (rows by vertical overlap, then left).
        Components under --min-zone (0.3% of the plate; cyan --min-logo-zone 0.05%) are ignored.
        N may be written 2 or M2 (--shot/--card) and 2 or C2 (--logo). fill < 0.97 = not a clean
        rectangle (rounded corners, or something overlaps the panel); the mask respects that shape.
MASK    The zone's own component pixels (+ specks < 0.05% filled), dilated --dilate px (2) to swallow the
        anti-aliased fringe. Shots are sampled past the bbox into that margin; cards are edge-extended.
        --edge matte (default) un-mixes each fringe pixel against its nearest untinted neighbour, so thin
        ink outlines survive and rounded corners stay anti-aliased; --edge hard = plain binary paste.
CHECK   Pixels with a visible key tint (~20%+ key blended into ink/paper) left in each zone bbox +6 px
        outside the fully replaced area. > --max-leftover (50) -> that zone is redone once at
        --dilate-retry (5); still over -> exit 3, naming the zone, the edges and the bbox.
        Stray key specks under the zone size are warned about, not touched.
        Cyan is processed and checked only when --logo is used (otherwise it is treated as artwork).
LETTERBOX --letterbox edge|paper|#rrggbb: fill for bars when the focus/card needs more than the
        asset (edge = asset border colour, default; paper = plate ground).
FINAL   Never stretches: centre-crops the minimal amount of the long axis to the --size aspect
        (--fit pad pads the short axis with grain-matched ground instead), then Lanczos-resizes.
        Warns when the crop cuts a zone or visible artwork.
KEEP    --keep C3 leaves a detected zone untouched as artwork (e.g. a cyan design element).
EXIT    0 ok | 2 bad input / unknown zone | 3 key colour left over or a zone without an asset
        (output + report are still written so you can look)
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


def paste_logo(out, plate, z, d, logo_path, scale, W, H, rng):
    """Erase the cyan zone into the ground around it, then contain-fit the logo on top.
    The zone is dilated d+2 (key tiles carry a soft light rim) and inpainted from the untinted pixels
    beyond it: nearest-ground fill, then diffused so tile shading and paper gradients carry through,
    plus grain matched to the surrounding texture. The plate's ground is the only colour source."""
    dd = d + 2
    mask, core, (x0, y0, x1, y1) = zone_mask(z, dd, W, H, margin=dd + 14)
    P = plate[y0:y1, x0:x1].astype(np.float32)
    known = (~ndimage.binary_dilation(core, structure=disk(dd + 2))
             & (keyness(P, 'C') <= 8) & (keyness(P, 'M') <= 8))
    ring = known & ndimage.binary_dilation(core, structure=disk(dd + 12))
    if ring.sum() < 20:
        die(f'{z["id"]}: no ground around the cyan zone to sample')
    iy, ix = ndimage.distance_transform_edt(~known, return_distances=False, return_indices=True)
    F = P[iy, ix]
    s = max(2.0, min(z['w'], z['h']) / 12)
    for _ in range(12):
        F = ndimage.gaussian_filter(F, sigma=(s, s, 0))
        F[known] = P[known]
    px = P[ring]
    ground = np.median(px, axis=0)
    luma = px.mean(axis=1)
    sigma = float(min(6.0, 1.4826 * np.median(np.abs(luma - np.median(luma)))))
    F = F + rng.normal(0, sigma, F.shape[:2] + (1,))
    region = out[y0:y1, x0:x1]
    region[mask] = np.clip(F[mask] + 0.5, 0, 255).astype(np.uint8)
    covered, win = mask, (x0, y0, x1, y1)

    p = Path(logo_path)
    if not p.is_file():
        die(f'logo not found: {logo_path}')
    if p.suffix.lower() == '.svg':
        die(f'logo is an SVG; rasterize it to PNG first: {logo_path}')
    logo = Image.open(p).convert('RGBA')
    bb = logo.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        logo = logo.crop(bb)
    s = min(z['w'] * scale / logo.width, z['h'] * scale / logo.height)
    lw, lh = max(1, round(logo.width * s)), max(1, round(logo.height * s))
    logo = logo.resize((lw, lh), Image.LANCZOS)
    lx, ly = z['x'] + (z['w'] - lw) // 2, z['y'] + (z['h'] - lh) // 2
    pil = Image.fromarray(out)
    pil.paste(logo, (lx, ly), logo)
    out[:] = np.asarray(pil)
    covered_logo = (lx, ly, lw, lh, np.asarray(logo.getchannel('A')) > 0)
    info = dict(mode='logo', ground=[int(v) for v in ground], grain=round(sigma, 2), scale=scale,
                placed=[lx, ly, lw, lh])
    return covered, win, covered_logo, info


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

def parse_spec(spec, flag, kind):
    m = re.match(r'^\s*([MmCc]?)(\d+)\s*=(.+)$', spec)
    if not m:
        die(f'{flag} {spec!r}: expected N=path')
    prefix, n, rest = m.group(1).upper(), int(m.group(2)), m.group(3).strip()
    if prefix and prefix != kind:
        die(f'{flag} {spec!r}: {flag} targets {KEY_NAME[kind]} zones ({kind}N), not {prefix}{n}')
    extra = None
    m2 = re.match(r'^(.*)@([\d.,\s]+)$', rest)
    if m2 and flag != '--card':
        rest, extra = m2.group(1), [float(v) for v in m2.group(2).split(',') if v.strip()]
        if flag == '--shot' and len(extra) != 4:
            die(f'--shot {spec!r}: focus box must be @x,y,w,h')
        if flag == '--logo' and len(extra) != 1:
            die(f'--logo {spec!r}: logo scale must be @0.8 (fraction of the zone)')
    return f'{kind}{n}', rest, extra


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
    ap.add_argument('--shot', action='append', default=[], metavar='N=path[@x,y,w,h]')
    ap.add_argument('--card', action='append', default=[], metavar='N=path')
    ap.add_argument('--logo', action='append', default=[], metavar='N=path[@scale]')
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
    for flag, specs, kind in (('--shot', args.shot, 'M'), ('--card', args.card, 'M'), ('--logo', args.logo, 'C')):
        for spec in specs:
            zid, path, extra = parse_spec(spec, flag, kind)
            if zid not in zmap:
                have = ', '.join(z['id'] for z in (mzones if kind == 'M' else czones)) or 'none'
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
    active = [z for z in mzones + (czones if args.logo else []) if z['id'] not in keep]
    if czones and not args.logo:
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
        if kind == 'logo':
            scale = extra[0] if extra else 0.9
            cov, (x0, y0, x1, y1), (lx, ly, lw, lh, la), info = paste_logo(
                out, plate, z, d, path, scale, W, H, np.random.default_rng(int(z['id'][1:])))
            covered[y0:y1, x0:x1] |= cov
            cx0, cy0 = max(0, lx), max(0, ly)
            cx1, cy1 = min(W, lx + lw), min(H, ly + lh)
            covered[cy0:cy1, cx0:cx1] |= la[cy0 - ly:cy1 - ly, cx0 - lx:cx1 - lx]
            row['fit'] = info
            return
        if path not in loaded:
            loaded[path] = load_rgb(path, kind)
        src, info = loaded[path], {}

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
                 f'({f["card_size"][0]}x{f["card_size"][1]} vs {zmap[zid]["aspect"]:.3f}); letterboxed. '
                 f'Re-render at the zone aspect')

    crop_checks(plate, mzones + czones, g)
    final = finish(out, g, TW, TH)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    final.save(args.out)

    for zid, row in rows.items():
        if row.get('asset'):
            f = row['fit']
            desc = (f'cover crop {f["crop"]} x{f["scale"]:.3f}' if f['mode'] == 'cover'
                    else f'contain {f["placed"][2]}x{f["placed"][3]}' if f['mode'] == 'contain'
                    else f'logo {f["placed"][2]}x{f["placed"][3]} on ground {f["ground"]}')
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
    report.update(out=str(args.out), zones=list(rows.values()), warnings=WARNINGS, failures=failed, status=status)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=1), encoding='utf-8')
    print(f'wrote {args.out} ({TW}x{TH}) status {status}')
    return 3 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
