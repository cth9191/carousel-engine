"""Mascot pose tool: cut a Codex pose plate to a clean alpha PNG, and check that a pose is still your
canonical mascot sprite, by numbers. Never copy it into a deck. Optional: only decks that paste a mascot
need it, and the repo ships no mascot or poses (bring your own; never a licensed character).

  # 1. cut: key a flat-grey plate (#8C8C8C ground) to alpha, unmix the grey from the edge pixels, trim.
  #    Works for any subject on that ground.
  python -I shared/pose-check.py cut <plate.png> <pose.png> [--pad 0]

  # 1b. grade (in place): pull the mascot's body colour onto the sprite's #D97757 (props untouched)
  python -I shared/pose-check.py grade <pose.png> [...] --sprite <mascot.png>

  # 2. check (the acceptance test). Exit 0 only if every pose passes.
  python -I shared/pose-check.py check <pose.png> [<pose2.png> ...] --sprite <mascot.png> [--prop x0,y0,x1,y1]
         [--json out.json] [--index poses/index.json --prop-name "wrench" --note "..."] [--debug dir]

  # 3. sheets from poses/index.json (rendered through shared/render-card.mjs on a bone ground)
  python -I shared/pose-check.py sheet <poses/index.json> <poses/poses-on-bone.png>   # labelled contact sheet
  python -I shared/pose-check.py props <poses/index.json> <poses/props-on-bone.png> [--plate props-plate.png]
       # props alone, no mascot, no text

--sprite (or the MASCOT_SPRITE environment variable) is your mascot's canonical sprite. The check and the
grade were built for one shape of mascot, and you will need to tune the constants below for any other:
a voxel figure on a 14 x 10-unit grid at 96 px a unit, body colour #D97757 (terracotta), dark eyes,
4 legs and 2 arm stubs.

The check:
  - Front-face mask: opaque body-hue pixels within a lightness band around the dominant body lightness
    (the flat front faces), so tops (lighter), sides (darker), eyes and the prop drop out.
  - Prop box: --prop in pixels of the pose PNG (or fractions 0-1); default = the auto box around every
    opaque pixel that is not body colour and not an eye. The box is masked out of the pose and,
    mapped into sprite units, out of the sprite too.
  - The pose mask is scaled to the sprite's 14 x 10-unit bbox (96 px units): body width from the top band
    = sprite columns 1-13, height = body top to feet = 10 units. A small search (scale +-8% x, +-5% y,
    offset +-0.4 x / +-0.2 y units) keeps the best IoU against the sprite's body-colour mask, so a prop or
    raised arm hiding a figure edge can't skew the scale. Prints the fitted IoU and the plain-bbox IoU.
  - Pass = fitted IoU >= 0.85, unit ratio (fitted unit width / height) 0.90-1.10 (a stretched body or long
    legs hide from a bbox-scaled IoU), and as separate parts exactly 2 eyes (dark holes inside the face,
    0.3-3 unit^2 each), 4 legs (front-face components below body row 8.4) and 2 arm stubs (one component
    per side column x < 0.85 / x > 13.15 units that reaches in to the body edge and is >= 0.5 unit wide;
    a stub tilted toward its prop falls back to any body-colour face).
  - Prints the index.json fields measured from the PNG: aspect (w/h), prop_anchor (prop box centre, as
    fractions of the trimmed image), feet_y (lowest leg pixel / height).
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE = os.environ.get('MASCOT_SPRITE')  # set from --sprite in main()
UNIT_PX = 96          # sprite unit
NL = chr(10)
GRID = 24             # normalized px per unit for the IoU
IOU_MIN = 0.85
UNIT_MIN, UNIT_MAX = 0.90, 1.10   # fitted unit width / unit height (catches a stretched body or long legs)


# ---------------------------------------------------------------- colour helpers
def srgb_to_lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)


def hsv(rgb):
    c = rgb / 255.0
    mx, mn = c.max(-1), c.min(-1)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    h = np.zeros_like(mx)
    nz = d > 1e-6
    rm = nz & (mx == r)
    gm = nz & (mx == g) & ~rm
    bm = nz & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    return h * 60, s, mx


def norm_blur(img, w, sigma):
    """Normalized convolution: blur img using only pixels where w > 0."""
    w = w.astype(np.float64)
    num = np.stack([ndi.gaussian_filter(img[..., k] * w, sigma) for k in range(img.shape[-1])], -1)
    den = ndi.gaussian_filter(w, sigma)[..., None]
    return num / np.maximum(den, 1e-6), den[..., 0]


# ---------------------------------------------------------------- cut
def cut(plate, out, pad=0):
    rgb = np.asarray(Image.open(plate).convert('RGB')).astype(np.float64)
    H, W, _ = rgb.shape
    lab = srgb_to_lab(rgb)
    border = np.zeros((H, W), bool)
    border[:12], border[-12:], border[:, :12], border[:, -12:] = True, True, True, True
    b_med = np.median(lab[border], 0)
    d0 = np.linalg.norm(lab - b_med, axis=-1)
    # bg seed: near the border colour and connected to the border
    near = d0 < 10
    lbl, _ = ndi.label(near)
    touch = np.unique(lbl[border & near])
    seed = np.isin(lbl, touch[touch > 0])
    # smooth per-pixel ground estimate (handles a faint gradient or vignette)
    bg = rgb.copy()
    for sig in (40, 120, 400):
        est, den = norm_blur(rgb, seed, sig)
        fill = den > 1e-3
        bg = np.where(fill[..., None], est, bg)
        if fill.all():
            break
    d = np.linalg.norm(lab - srgb_to_lab(bg), axis=-1)
    # background region: low-distance pixels connected to the border, plus large enclosed grey holes
    lo, hi = 6.0, 22.0
    # contact shadows count as ground: neutral grey a little darker than the ground (graphite is far darker)
    _, sat, _ = hsv(rgb)
    bgL = srgb_to_lab(bg)[..., 0]
    shadow = (sat < 0.10) & (lab[..., 0] > bgL - 16) & (lab[..., 0] < bgL + 3)
    bgc = (d < 9) | shadow
    lbl, n = ndi.label(bgc)
    touch = set(np.unique(lbl[border & bgc])) - {0}
    sizes = ndi.sum(np.ones_like(d), lbl, index=np.arange(1, n + 1))
    keep = [i + 1 for i in range(n) if (i + 1) in touch or sizes[i] > 80]
    bgr = np.isin(lbl, keep)
    fg = ~bgr
    fg = ndi.binary_opening(fg, iterations=1)
    lbl, n = ndi.label(fg)                    # drop specks
    if n:
        sizes = ndi.sum(fg, lbl, index=np.arange(1, n + 1))
        fg = np.isin(lbl, [i + 1 for i in range(n) if sizes[i] > 200])
    # alpha: 1 inside, unmixed in a 3 px band at the edge
    inner = ndi.binary_erosion(fg, iterations=3)
    band = fg & ~inner | (ndi.binary_dilation(fg, iterations=1) & ~fg)
    F, _ = norm_blur(rgb, ndi.binary_erosion(fg, iterations=4) | inner, 2.5)
    fb = F - bg
    alpha = np.where(fg, 1.0, 0.0)
    a_est = np.clip(((rgb - bg) * fb).sum(-1) / np.maximum((fb * fb).sum(-1), 1.0), 0, 1)
    a_d = np.clip((d - lo) / (hi - lo), 0, 1)
    a_band = np.maximum(a_est, a_d) if False else np.where((fb * fb).sum(-1) > 400, a_est, a_d)
    alpha = np.where(band, a_band, alpha)
    alpha[alpha < 0.06] = 0
    a3 = np.maximum(alpha, 1e-3)[..., None]
    col = np.clip((rgb - (1 - alpha[..., None]) * bg) / a3, 0, 255)
    col = np.where(band[..., None], col, rgb)
    rgba = np.dstack([col, alpha * 255]).round().astype(np.uint8)
    ys, xs = np.nonzero(alpha > 0.03)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + 1 + pad, H), max(xs.min() - pad, 0), min(xs.max() + 1 + pad, W)
    Image.fromarray(rgba[y0:y1, x0:x1], 'RGBA').save(out)
    print(f'cut {os.path.basename(plate)} -> {out}  {x1 - x0}x{y1 - y0}  ground ~rgb{tuple(int(v) for v in np.median(rgb[border], 0))}')


# ---------------------------------------------------------------- masks
def sprite_mask():
    if not SPRITE or not os.path.isfile(SPRITE):
        sys.exit(f'mascot sprite not found: {SPRITE!r}. Pass --sprite <mascot.png> (or set MASCOT_SPRITE).')
    a = np.asarray(Image.open(SPRITE).convert('RGB')).astype(int)
    terra = (np.abs(a - [217, 119, 87]).sum(-1) < 30)
    eye = a.sum(-1) < 100
    terra = terra[:10 * UNIT_PX, :14 * UNIT_PX]
    eye = eye[:10 * UNIT_PX, :14 * UNIT_PX]
    return terra, eye


def mascot_masks(rgba):
    rgb = rgba[..., :3].astype(np.float64)
    op = rgba[..., 3] > 128
    h, s, v = hsv(rgb)
    lab = srgb_to_lab(rgb)
    fam = op & (h < 32) & (s > 0.28) & (s < 0.80) & (v > 0.30)        # terracotta front/top/side
    L = lab[..., 0][fam]
    hist, edges = np.histogram(L, bins=np.arange(0, 101, 1.5))
    mode = edges[hist.argmax()] + 0.75
    front = fam & (np.abs(lab[..., 0] - mode) <= 6.5)
    front = ndi.binary_closing(front, iterations=2) & op
    front = ndi.binary_opening(front, iterations=2)
    dark = op & (lab[..., 0] < 32) & (s < 0.6)
    return front, fam, dark, mode


def auto_prop_box(rgba, fam, dark, front):
    """Box around the prop: opaque pixels that are clearly not mascot terracotta (brass/yellow hues, greys,
    bone, or a saturated orange), not an eye, grown into one cluster around the largest blob."""
    rgb = rgba[..., :3].astype(np.float64)
    op = rgba[..., 3] > 128
    h, s, v = hsv(rgb)
    H, W = op.shape
    filled = ndi.binary_fill_holes(ndi.binary_closing(front, iterations=6))
    mascot = (h < 30) & (s > 0.22) & (s < 0.84)                     # terracotta fronts, tops, shaded sides
    other = op & ~mascot & ~(dark & filled)
    other = ndi.binary_opening(other, iterations=3)
    lbl, n = ndi.label(other)
    if not n:
        return None
    sizes = ndi.sum(other, lbl, index=np.arange(1, n + 1))
    big = int(np.argmax(sizes)) + 1
    if sizes[big - 1] < 0.002 * H * W:
        return None
    near = ndi.binary_dilation(lbl == big, iterations=40)
    keep_ids = [i + 1 for i in range(n) if sizes[i] > 0.0004 * H * W and (near & (lbl == i + 1)).any()]
    keep = np.isin(lbl, keep_ids)
    ys, xs = np.nonzero(keep)
    return [max(int(xs.min()) - 3, 0), max(int(ys.min()) - 3, 0), min(int(xs.max()) + 4, W), min(int(ys.max()) + 4, H)]


def parse_box(s, w, h):
    v = [float(x) for x in s.split(',')]
    if all(0 <= x <= 1 for x in v):
        v = [v[0] * w, v[1] * h, v[2] * w, v[3] * h]
    return [int(round(x)) for x in v]


# ---------------------------------------------------------------- check
def check(path, prop=None, debug=None):
    rgba = np.asarray(Image.open(path).convert('RGBA'))
    H, W = rgba.shape[:2]
    front, fam, dark, mode = mascot_masks(rgba)
    box = parse_box(prop, W, H) if prop else auto_prop_box(rgba, fam, dark, front)
    pm = np.zeros((H, W), bool)
    if box:
        x0, y0, x1, y1 = max(box[0], 0), max(box[1], 0), min(box[2], W), min(box[3], H)
        pm[y0:y1, x0:x1] = True
    fmask = front & ~pm
    lbl, n = ndi.label(fmask)
    if not n:
        return {'file': path, 'pass': False, 'why': 'no terracotta front face found'}
    # Fit: initial guess = body width from the top band (columns 1-13 of the sprite) and the full height
    # (body top to feet = 10 units), then a small scale/offset search that maximizes the IoU with the
    # prop box masked out of both (so a prop or a raised arm that hides a figure edge can't skew the scale).
    ys, xs = np.nonzero(fmask)
    by0, by1 = ys.min(), ys.max() + 1
    band = fmask[by0:by0 + max(int(0.3 * (by1 - by0)), 1)]
    bxs = np.nonzero(band.any(0))[0]
    L, R = bxs.min(), bxs.max() + 1
    ux0, uy0 = (R - L) / 12.0, (by1 - by0) / 10.0
    bx00 = L - ux0
    terra, _ = sprite_mask()
    sprs = {g: np.asarray(Image.fromarray((terra * 255).astype(np.uint8)).resize((14 * g, 10 * g), Image.BILINEAR)) > 127
            for g in (12, GRID)}
    def iou_at(bx0, by0_, ux, uy, grid):
        gw, gh = 14 * grid, 10 * grid
        spr = sprs[grid]
        gx = bx0 + (np.arange(gw) + 0.5) / grid * ux
        gy = by0_ + (np.arange(gh) + 0.5) / grid * uy
        ix = np.clip(np.round(gx).astype(int), 0, W - 1); iy = np.clip(np.round(gy).astype(int), 0, H - 1)
        inside = ((gx >= 0) & (gx < W))[None, :] & ((gy >= 0) & (gy < H))[:, None]
        pose = fmask[iy][:, ix] & inside
        pmn = pm[iy][:, ix] & inside
        a_, b_ = pose & ~pmn, spr & ~pmn
        return (a_ & b_).sum() / max((a_ | b_).sum(), 1), a_, b_, pmn
    iou_bbox = iou_at(bx00, by0, ux0, uy0, GRID)[0]
    best = (iou_at(bx00, by0, ux0, uy0, 12)[0], bx00, by0, ux0, uy0)
    for sx in np.linspace(0.92, 1.08, 9):
        for sy in np.linspace(0.95, 1.05, 5):
            ux_, uy_ = ux0 * sx, uy0 * sy
            for dx in np.arange(-0.4, 0.41, 0.1):
                for dy in np.arange(-0.2, 0.21, 0.1):
                    v = iou_at(bx00 + dx * ux0, by0 + dy * uy0, ux_, uy_, 12)[0]
                    if v > best[0]:
                        best = (v, bx00 + dx * ux0, by0 + dy * uy0, ux_, uy_)
    _, bx0, by0, ux, uy = best
    iou, a, b, pm_n = iou_at(bx0, by0, ux, uy, GRID)
    gw, gh = 14 * GRID, 10 * GRID
    by1 = by0 + 10 * uy
    # ---- parts (on the original pixels, in unit coordinates)
    U2 = ux * uy
    yy, xx = np.mgrid[0:H, 0:W]
    uxs, uys = (xx - bx0) / ux, (yy - by0) / uy
    filled = ndi.binary_fill_holes(ndi.binary_closing(front, iterations=3))
    eyes_m = filled & ~front & dark & (uys > 0.5) & (uys < 6) & (uxs > 1) & (uxs < 13) & ~pm
    lbl, n = ndi.label(eyes_m)
    sz = ndi.sum(eyes_m, lbl, index=np.arange(1, n + 1)) / U2 if n else []
    eyes = int(sum(1 for s in sz if 0.3 <= s <= 3.0))
    leg_m = front & (uys > 8.4) & (uxs > 0.5) & (uxs < 13.5)
    lbl, n = ndi.label(leg_m)
    sz = ndi.sum(leg_m, lbl, index=np.arange(1, n + 1)) / U2 if n else []
    legs = int(sum(1 for s in sz if s >= 0.4))
    # arms: front-face components in the side columns (x < 0.85 or x > 13.15 units) that reach in to the
    # body edge (within x 0.4-1.1 / 12.9-13.6), so a terracotta-ish prop standing beside the body is not an arm
    arms = 0
    for side, edge in ((uxs < 0.85, (uxs > 0.4) & (uxs < 1.1)), (uxs > 13.15, (uxs > 12.9) & (uxs < 13.6))):
        found = 0
        # flat front faces first; a stub tilted toward the prop is shaded differently, so fall back to any
        # terracotta face (front, top or side) on that side
        for src in (front, fam):
            m = src & (side | edge) & (uys > 1.5) & (uys < 8.5)
            lbl, n = ndi.label(m)
            for i in range(1, n + 1):
                c = lbl == i
                cs = c & side
                area = cs.sum() / U2
                width = (np.ptp(uxs[cs]) if cs.any() else 0)
                if 0.3 <= area <= 4.5 and width >= 0.5 and (c & edge).any():
                    found += 1
            if found:
                break
        arms += found
    # ---- index fields
    leg_rows = np.nonzero(leg_m.any(1))[0]
    feet_y = (leg_rows.max() + 1) / H if len(leg_rows) else by1 / H
    anchor = [round((box[0] + box[2]) / 2 / W, 3), round((box[1] + box[3]) / 2 / H, 3)] if box else None
    prop_area = (pm & filled).sum() / max(filled[int(by0):int(by0 + 8 * uy)].sum(), 1) if box else 0
    unit_ratio = ux / uy                      # cube units must stay square: 1.0 frontal, ~0.94 at a 20 deg turn
    ok = iou >= IOU_MIN and eyes == 2 and legs == 4 and arms == 2 and UNIT_MIN <= unit_ratio <= UNIT_MAX
    res = {'file': os.path.basename(path), 'pass': bool(ok), 'iou': round(float(iou), 3), 'iou_bbox': round(float(iou_bbox), 3), 'unit_ratio': round(float(unit_ratio), 3), 'eyes': eyes, 'legs': legs,
           'arms': arms, 'prop_box': box, 'prop_over_face': round(float(prop_area), 3), 'size': [W, H],
           'aspect': round(W / H, 3), 'prop_anchor': anchor, 'feet_y': round(float(feet_y), 3),
           'face_L': round(float(mode), 1)}
    if debug:
        os.makedirs(debug, exist_ok=True)
        stem = os.path.splitext(os.path.basename(path))[0]
        viz = np.zeros((gh, gw, 3), np.uint8)
        viz[a & b] = (217, 119, 87); viz[a & ~b] = (255, 0, 0); viz[b & ~a] = (0, 120, 255); viz[pm_n] //= 3
        viz[pm_n] += 60
        Image.fromarray(viz).resize((gw * 2, gh * 2), Image.NEAREST).save(os.path.join(debug, f'{stem}.iou.png'))
        dbg = rgba[..., :3].copy() // 3 + 80
        dbg[fmask] = (217, 119, 87); dbg[eyes_m] = (0, 200, 0); dbg[pm] = dbg[pm] // 2 + (0, 0, 120)
        Image.fromarray(dbg.astype(np.uint8)).save(os.path.join(debug, f'{stem}.mask.png'))
    return res


# ---------------------------------------------------------------- sheets (contact sheet, props-on-bone)
GROUND_CSS = """
  html,body{margin:0;background:#ECE3D4;}
  .pg{position:relative;width:%(W)dpx;height:%(H)dpx;background:#ECE3D4;overflow:hidden;font-family:'JetBrains Mono',monospace;}
  .pg::before{content:'';position:absolute;inset:0;background-image:
    linear-gradient(rgba(14,14,14,.07) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba(14,14,14,.07) 1.5px,transparent 1.5px),
    linear-gradient(rgba(14,14,14,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(14,14,14,.035) 1px,transparent 1px);
    background-size:180px 180px,180px 180px,36px 36px,36px 36px;}
  .pg::after{content:'';position:absolute;inset:0;opacity:.5;mix-blend-mode:multiply;
    background-image:radial-gradient(rgba(14,14,14,.05) .6px,transparent .7px);background-size:4px 4px;}
  .frame{position:absolute;inset:34px;border:1.5px solid rgba(14,14,14,.4);}
  .xh{position:absolute;width:30px;height:30px;}
  .xh::before,.xh::after{content:'';position:absolute;background:#D9551F;}
  .xh::before{left:50%%;top:0;width:1.5px;height:100%%;transform:translateX(-50%%);}
  .xh::after{top:50%%;left:0;height:1.5px;width:100%%;transform:translateY(-50%%);}
  .cell{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;z-index:2;}
  .cell img{max-width:100%%;object-fit:contain;display:block;}
  .shadow{width:70%%;height:14px;border-radius:50%%;background:radial-gradient(ellipse at center,rgba(14,14,14,.22),rgba(14,14,14,0) 70%%);margin-top:-8px;}
  .lab{margin-top:10px;font-weight:700;font-size:22px;color:#0E0E0E;letter-spacing:.06em;text-align:center;white-space:nowrap;}
  .sub{font-weight:700;font-size:15px;color:rgba(14,14,14,.55);letter-spacing:.08em;margin-top:4px;text-align:center;white-space:nowrap;}
  .hd{position:absolute;left:80px;top:62px;font-weight:700;font-size:22px;color:rgba(14,14,14,.7);letter-spacing:.14em;z-index:2;}
"""


def _page(W, H, body):
    xh = ''.join(f'<div class="xh" style="{p}"></div>' for p in
                 ('left:19px;top:19px', 'right:19px;top:19px', 'left:19px;bottom:19px', 'right:19px;bottom:19px'))
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">'
            f'<style>{GROUND_CSS % {"W": W, "H": H}}</style></head><body><div class="pg"><div class="frame"></div>{xh}'
            f'{body}</div></body></html>')


def _render(html, out, W, H):
    import subprocess, tempfile
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), '_sheet.tmp.html')
    open(tmp, 'w', encoding='utf-8').write(html)
    r = subprocess.run(['node', os.path.join(ROOT, 'shared', 'render-card.mjs'), tmp, out, '--w', str(W), '--h', str(H),
                        '--scale', '1', '--min-px', '14'], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
    os.remove(tmp)
    if r.returncode:
        sys.exit(r.returncode)


def sheet(index_path, out, cols=3):
    """Labelled contact sheet of every pose in index.json on a bone ground."""
    base = os.path.dirname(os.path.abspath(index_path))
    idx = json.load(open(index_path, encoding='utf-8'))
    W, cw, ch, top = 1080, 300, 300, 120
    rows = -(-len(idx) // cols)
    H = top + rows * (ch + 40) + 40
    x0 = (W - cols * cw) // 2
    cells = []
    for i, e in enumerate(idx):
        r, c = divmod(i, cols)
        uri = 'file:///' + os.path.join(base, e['file']).replace(chr(92), '/')
        k = e.get('check', {})
        cells.append(f'<div class="cell" style="left:{x0 + c * cw + 10}px;top:{top + r * (ch + 40)}px;width:{cw - 20}px;height:{ch}px">'
                     f'<img src="{uri}" style="max-height:{ch - 80}px"><div class="shadow"></div>'
                     f'<div class="lab">{i + 1:02d} {os.path.splitext(e["file"])[0].upper()}</div>'
                     f'<div class="sub">IOU {k.get("iou", "?")} · UNITS {k.get("unit_ratio", "?")}</div></div>')
    body = f'<div class="hd">MASCOT POSE LIBRARY · {len(idx)} POSES</div>' + ''.join(cells)
    _render(_page(W, H, body), out, W, H)


def props(index_path, out, cols=4, plate=None):
    """Props alone (no mascot, no text) knolled on bone, e.g. as a cover plate's second reference. With --plate, a Codex
    knolled-props plate on the flat grey ground is keyed (as `cut`) and centred on the bone ground instead of
    cutting the props out of the poses (cleaner: no arm-shaped holes)."""
    base = os.path.dirname(os.path.abspath(index_path))
    if plate:
        W, H = 1080, 1350
        tmp = os.path.join(base, '_props.tmp.png')
        cut(plate, tmp)
        uri = 'file:///' + tmp.replace(chr(92), '/')
        body = (f'<div class="cell" style="left:110px;top:150px;width:860px;height:1050px;justify-content:center">'
                f'<img src="{uri}" style="max-height:1000px;max-width:860px"></div>')
        _render(_page(W, H, body), out, W, H)
        os.remove(tmp)
        return
    idx = json.load(open(index_path, encoding='utf-8'))
    tmpdir = os.path.join(base, '_props.tmp'); os.makedirs(tmpdir, exist_ok=True)
    files = []
    for e in idx:
        rgba = np.asarray(Image.open(os.path.join(base, e['file'])).convert('RGBA')).copy()
        H0, W0 = rgba.shape[:2]
        x0, y0, x1, y1 = e['check']['prop_box']
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W0), min(y1, H0)
        h, s, v = hsv(rgba[..., :3].astype(np.float64))
        mascot = (h < 30) & (s > 0.22) & (s < 0.84)
        keep = np.zeros((H0, W0), bool); keep[y0:y1, x0:x1] = True
        keep &= ~mascot
        keep = ndi.binary_opening(keep, iterations=1)
        a = rgba[..., 3] * keep
        rgba[..., 3] = a
        ys, xs = np.nonzero(a > 8)
        if not len(ys):
            continue
        f = os.path.join(tmpdir, e['file'])
        Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(f)
        files.append(f)
    W, H = 1080, 1350
    rows = -(-len(files) // cols)
    cw, ch = (W - 200) // cols, min(260, (H - 300) // max(rows, 1))
    y0 = (H - rows * ch) // 2
    cells = []
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        uri = 'file:///' + f.replace(chr(92), '/')
        cells.append(f'<div class="cell" style="left:{100 + c * cw + 15}px;top:{y0 + r * ch}px;width:{cw - 30}px;height:{ch - 30}px">'
                     f'<img src="{uri}" style="max-height:{ch - 50}px"><div class="shadow"></div></div>')
    _render(_page(W, H, ''.join(cells)), out, W, H)
    for f in files:
        os.remove(f)
    os.rmdir(tmpdir)


# ---------------------------------------------------------------- grade
def grade(path, out):
    """Scale the mascot's terracotta faces (front, tops, sides; soft hue/saturation weight) per channel so the
    front-face median lands on the sprite's #D97757. Props (brass, graphite, bone, saturated orange) keep theirs."""
    rgba = np.asarray(Image.open(path).convert('RGBA')).astype(np.float64)
    rgb = rgba[..., :3]
    front, fam, dark, _ = mascot_masks(rgba.astype(np.uint8))
    med = np.median(rgb[front], 0)
    gain = np.array([217.0, 119.0, 87.0]) / np.maximum(med, 1)
    h, s, v = hsv(rgb)
    w = fam.astype(np.float64)
    w = ndi.gaussian_filter(w, 1.2) * ((h < 32) & (s > 0.18) & (s < 0.82))
    graded = np.clip(rgb * (1 + (gain - 1) * w[..., None]), 0, 255)
    rgba[..., :3] = graded
    Image.fromarray(rgba.round().astype(np.uint8), 'RGBA').save(out)
    print(f'grade {os.path.basename(path)}: front median {tuple(int(x) for x in med)} -> gain {tuple(round(float(g), 3) for g in gain)}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['cut', 'grade', 'check', 'sheet', 'props'])
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--prop', help='prop box x0,y0,x1,y1 in px or 0-1 fractions (check, one pose)')
    ap.add_argument('--pad', type=int, default=0)
    ap.add_argument('--plate', help='props: a knolled-props Codex plate on flat grey to key and centre')
    ap.add_argument('--json')
    ap.add_argument('--index', help='poses/index.json to upsert passing poses into')
    ap.add_argument('--prop-name')
    ap.add_argument('--note', default='')
    ap.add_argument('--debug')
    ap.add_argument('--sprite', help="your mascot's canonical sprite PNG (check, grade); default $MASCOT_SPRITE")
    o = ap.parse_args()
    global SPRITE
    if o.sprite:
        SPRITE = o.sprite
    if o.mode in ('sheet', 'props'):
        if len(o.paths) != 2:
            sys.exit(f'{o.mode} needs <index.json> <out.png>')
        if o.mode == 'sheet':
            sheet(o.paths[0], o.paths[1])
        else:
            props(o.paths[0], o.paths[1], plate=o.plate)
        return
    if o.mode == 'cut':
        if len(o.paths) != 2:
            sys.exit('cut needs <plate.png> <pose.png>')
        cut(o.paths[0], o.paths[1], o.pad)
        return
    if o.mode == 'grade':
        for p in o.paths:
            grade(p, p)
        return
    results = []
    for p in o.paths:
        r = check(p, o.prop, o.debug)
        results.append(r)
        flag = 'PASS' if r['pass'] else 'FAIL'
        print(f"{flag}  {r['file']}  IoU {r.get('iou')} (bbox {r.get('iou_bbox')})  units {r.get('unit_ratio')}  eyes {r.get('eyes')}  legs {r.get('legs')}  arms {r.get('arms')}  "
              f"prop_box {r.get('prop_box')}  prop/face {r.get('prop_over_face')}  aspect {r.get('aspect')}  "
              f"prop_anchor {r.get('prop_anchor')}  feet_y {r.get('feet_y')}" + (f"  ({r['why']})" if 'why' in r else ''))
    if o.json:
        json.dump(results, open(o.json, 'w', encoding='utf-8'), indent=1)
    if o.index:
        idx = json.load(open(o.index, encoding='utf-8')) if os.path.exists(o.index) else []
        for r in results:
            if not r['pass']:
                continue
            entry = {'file': r['file'], 'prop': o.prop_name or '', 'aspect': r['aspect'], 'prop_anchor': r['prop_anchor'],
                     'feet_y': r['feet_y'], 'note': o.note,
                     'check': {k: r[k] for k in ('iou', 'iou_bbox', 'unit_ratio', 'eyes', 'legs', 'arms', 'prop_box')}}
            idx = [e for e in idx if e['file'] != r['file']] + [entry]
        with open(o.index, 'w', encoding='utf-8') as fh:
            fh.write("[" + NL + ("," + NL).join(" " + json.dumps(e, ensure_ascii=False) for e in idx) + NL + "]" + NL)
    sys.exit(0 if all(r['pass'] for r in results) else 1)


if __name__ == '__main__':
    main()
