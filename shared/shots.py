"""
Build the real-capture "shots" for a deck: frames pulled from a source video (webcam bubble
cropped out or scrubbed), still images, and tile re-layouts. Writes PNGs + shots.json.

Usage (from the repo root; -I keeps the deck folder out of sys.path; python3 where that is the name):
  python -I shared/shots.py carousels/<id>/shots/shots.spec.json [--only name1,name2] [--sheet out.jpg]

--sheet writes a contact sheet of the shots built in this run, focus boxes in green. Its folder is
created if needed. The spec path and --sheet are relative to the repo root unless absolute, like
every path in the spec. Video frames need ffmpeg on PATH; image and tile shots don't.

Spec (paths are relative to the repo root unless absolute):
{
  "video": "sources/<video>.mp4",           # your own copy of the source video (not part of the repo);
                                             #   only needed by shots that use "t"
  "out_dir": "carousels/<id>/shots",
  "bubble_prior": [1697, 834, 201],          # cx, cy, r of the webcam bubble in the 1920x1080 frame
  "shots": [
    { "slide": 2, "name": "s02-x", "t": "1:08.85",          # video frame (ffmpeg -ss t -frames:v 1)
      "crop": [x, y, w, h],                                  # in frame pixels (omit = full frame)
      "bubble": "scrub" | "cropped" | "none",
      "fill": "laplace" | "flat" | "mirror_x" | "shift",     # scrub method (default laplace)
      "mirror_x": 960,                                       # axis for mirror_x
      "shift": [0, -300],                                    # source offset for shift
      "color": [r, g, b],                                    # for flat (default: median of the ring)
      "pad": 8,                                              # px added to the fitted radius
      "pad_max": 36,                                         # mirror_x/shift: pick the pad in
                                                             #   [pad, pad_max] with the best seam
      "protect": 40,                                         # keep content in the pad band whose
                                                             #   colour differs from the bg by > N
      "square_corners": {"rect": [x0, y0, x1, y1], "r": 19, "color": [r, g, b]},
      "focus": [x, y, w, h],                                 # in OUTPUT pixels: must stay visible
      "note": "..." },
    { "slide": 9, "name": "s09-a", "image": "path.png", "crop": [...], "bubble": "none", ... },
    { "slide": 9, "name": "s09-row", "image": "path.png", "tiles": [[x, y, w, h], ...],
      "layout": "row" | "grid:ROWSxCOLS", "gap": 16, "margin": 16, "bg": [r, g, b] }
  ]
}

Scrub methods (they fill only the part of the disc inside the crop; the crop edge is a free
boundary, while mirror/shift may copy from anywhere in the frame outside the bubble):
  laplace   harmonic fill from the ring around the disc. Smooth, graded backgrounds with
            nothing touching the bubble (content on the ring bleeds in: use flat + protect).
  flat      one colour. Flat UI cards and flat dark grounds.
  mirror_x  copy the mirror image about a vertical axis, then a harmonic correction so the
            seam disappears (seamless clone). Symmetric layouts: rings, perspective floors.
  shift     same, but copy from a translated position: a repeated element (an identical
            label or page edge elsewhere in the frame).
The bubble is located per frame by fitting a circle near bubble_prior. Every scrubbed shot is
re-checked: the bubble's edge score inside the crop must fall to background level, or the
shot fails.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rp(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def rel(p):
    """Repo-relative, forward slashes (for messages)."""
    try:
        return os.path.relpath(p, ROOT).replace(os.sep, '/')
    except ValueError:  # another drive on Windows
        return p


def parse_t(t):
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(x) for x in str(t).split(':')]
    s = 0.0
    for x in parts:
        s = s * 60 + x
    return s


def fmt_t(s):
    m = int(s // 60)
    return f'{m}:{s - 60 * m:05.2f}'


def need_file(p, name, what, hint):
    if not p or not os.path.isfile(rp(p)):
        raise SystemExit(f'{name}: {what} not found: {p!r}. {hint}')
    return rp(p)


def extract(video, t, out):
    try:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', video,
                        '-frames:v', '1', out], check=True)
    except FileNotFoundError:
        raise SystemExit('ffmpeg not found on PATH: install ffmpeg to pull video frames '
                         '(image and tile shots work without it)')
    return np.asarray(Image.open(out).convert('RGB')).astype(np.float64)


# ---------- bubble detection ----------

def _grad(img):
    g = img.mean(2)
    gy, gx = np.gradient(g)
    return np.hypot(gx, gy)


def ring_score(mag, cx, cy, r, n=720, rect=None):
    """Mean gradient along a circle (optionally only the part inside rect x, y, w, h)."""
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    xs = np.round(cx + r * np.cos(th)).astype(int)
    ys = np.round(cy + r * np.sin(th)).astype(int)
    x0, y0, w, h = rect or (0, 0, mag.shape[1], mag.shape[0])
    # stay 1 px inside the rect: the crop edge itself is not part of the shot's content
    ok = ((xs >= max(x0, 0) + 1) & (xs < min(x0 + w, mag.shape[1]) - 1) &
          (ys >= max(y0, 0) + 1) & (ys < min(y0 + h, mag.shape[0]) - 1))
    if not ok.any():
        return 0.0
    return float(mag[ys[ok], xs[ok]].mean())


def fit_bubble(img, prior, search=24, rsearch=16):
    mag = _grad(img)
    c0x, c0y, r0 = prior
    best = (-1, c0x, c0y, r0)
    for cx in range(c0x - search, c0x + search + 1, 2):
        for cy in range(c0y - search, c0y + search + 1, 2):
            for r in range(r0 - rsearch, r0 + rsearch + 1, 2):
                s = ring_score(mag, cx, cy, r)
                if s > best[0]:
                    best = (s, cx, cy, r)
    _, bx, by, br = best
    for cx in range(bx - 2, bx + 3):
        for cy in range(by - 2, by + 3):
            for r in range(br - 2, br + 3):
                s = ring_score(mag, cx, cy, r)
                if s > best[0]:
                    best = (s, cx, cy, r)
    return best  # score, cx, cy, r


# ---------- fills ----------

def harmonic(img, mask, domain=None):
    """Solve Laplace(u)=0 inside mask with Dirichlet values from img outside (Neumann at the
    image border and outside `domain`, e.g. the crop). img HxWxC float, mask HxW bool.
    Returns a copy with the mask filled."""
    out = img.copy()
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return out
    H, W = mask.shape
    y0, y1 = max(ys.min() - 1, 0), min(ys.max() + 2, H)
    x0, x1 = max(xs.min() - 1, 0), min(xs.max() + 2, W)
    m = mask[y0:y1, x0:x1]
    sub = img[y0:y1, x0:x1]
    dom = None if domain is None else domain[y0:y1, x0:x1]
    h, w = m.shape
    idx = -np.ones((h, w), dtype=np.int64)
    n = int(m.sum())
    idx[m] = np.arange(n)
    py, px = np.nonzero(m)
    pid = idx[py, px]
    rows, cols, vals = [], [], []
    diag = np.zeros(n)
    b = np.zeros((n, img.shape[2]))
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        qy, qx = py + dy, px + dx
        inb = (qy >= 0) & (qy < h) & (qx >= 0) & (qx < w)
        if dom is not None:
            inb[inb] = dom[qy[inb], qx[inb]]
        diag[inb] += 1
        qy, qx, p_in = qy[inb], qx[inb], pid[inb]
        unk = m[qy, qx]
        rows.append(p_in[unk]); cols.append(idx[qy[unk], qx[unk]]); vals.append(-np.ones(unk.sum()))
        kn = ~unk
        np.add.at(b, p_in[kn], sub[qy[kn], qx[kn]])
    rows.append(np.arange(n)); cols.append(np.arange(n)); vals.append(diag)
    A = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                   shape=(n, n)).tocsc()
    lu = splu(A)
    sol = np.stack([lu.solve(b[:, c]) for c in range(b.shape[1])], 1)
    region = out[y0:y1, x0:x1]
    region[m] = sol
    return out


def guided(img, mask, guide, domain=None):
    """Seamless clone: guide inside the mask, plus a harmonic correction so it meets img."""
    diff = img - guide
    corr = harmonic(diff, mask, domain)
    out = img.copy()
    out[mask] = guide[mask] + corr[mask]
    return out


def disc_mask(shape, cx, cy, r):
    H, W = shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    return (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r


def ring_median(img, cx, cy, r0, r1):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    m = (d2 > r0 * r0) & (d2 <= r1 * r1)
    return np.median(img[m], axis=0)


def scrub(img, spec, cx, cy, r, crop):
    """Fill the bubble disc. Only the part inside the crop is filled and matched (the crop
    edge is a free boundary), so content outside the shot never constrains the fill."""
    H, W = img.shape[:2]
    x, y, w, h = crop
    domain = np.zeros((H, W), bool)
    domain[y:y + h, x:x + w] = True
    out, R = _fill(img, spec, cx, cy, r, domain)
    if 'protect' in spec:
        # keep real content that sits in the pad band just outside the bubble edge (e.g. an
        # arrow running alongside it): restore band pixels that differ from the background
        H, W = img.shape[:2]
        yy, xx = np.mgrid[0:H, 0:W]
        d2 = (xx - cx) ** 2 + (yy - cy) ** 2
        band = (d2 > (r + 2) ** 2) & (d2 <= R * R) & domain
        bgc = ring_median(img, cx, cy, R + 2, R + 12)
        keep = band & (np.abs(img - bgc).sum(2) > spec['protect'])
        out[keep] = img[keep]
        spec['_protected_px'] = int(keep.sum())
    return out, R


def _fill(img, spec, cx, cy, r, domain):
    pad = spec.get('pad', 8)
    R = r + pad
    mask = disc_mask(img.shape, cx, cy, R) & domain
    mode = spec.get('fill', 'laplace')
    if mode == 'laplace':
        return harmonic(img, mask, domain), R
    if mode == 'flat':
        col = spec.get('color') or ring_median(img, cx, cy, R + 2, R + 12).tolist()
        out = img.copy()
        out[mask] = np.array(col, dtype=np.float64)
        return out, R
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    if mode == 'mirror_x':
        ax = float(spec['mirror_x'])
        sx = np.clip(np.round(2 * ax - xx).astype(int), 0, W - 1)
        sy = yy
    elif mode == 'shift':
        dx, dy = spec['shift']
        sx = np.clip(xx + int(dx), 0, W - 1)
        sy = np.clip(yy + int(dy), 0, H - 1)
    else:
        raise SystemExit(f'unknown fill {mode}')
    guide = img[sy, sx]
    if 'pad_max' in spec:
        # put the seam where the copied content already matches the original best
        # (e.g. between tick marks instead of through one)
        d2 = (xx - cx) ** 2 + (yy - cy) ** 2
        err = np.abs(guide - img).sum(2)
        best = None
        for p in range(pad, spec['pad_max'] + 1):
            ring = (d2 > (r + p) ** 2) & (d2 <= (r + p + 3) ** 2) & domain
            e = float(err[ring].mean())
            if best is None or e < best[0]:
                best = (e, p)
        pad = best[1]
        R = r + pad
        mask = disc_mask(img.shape, cx, cy, R) & domain
        spec['_pad_used'] = pad
    # the copied source must not contain bubble pixels
    if (mask & disc_mask(img.shape, cx, cy, r + 3)[sy, sx]).any():
        raise SystemExit(f'{spec["name"]}: {mode} source overlaps the bubble')
    return guided(img, mask, guide, domain), R


def square_corners(img, sc):
    """Fill pixels outside a rounded rect (frame coords) with a colour: square card corners."""
    x0, y0, x1, y1 = sc['rect']
    r = sc['r']
    col = np.array(sc['color'], dtype=np.float64)
    H, W = img.shape[:2]
    ss = 4  # supersampled coverage for antialiasing
    m = Image.new('L', (W * ss, H * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([x0 * ss, y0 * ss, (x1 + 1) * ss - 1, (y1 + 1) * ss - 1],
                                        radius=r * ss, fill=255)
    cov = np.asarray(m.resize((W, H), Image.BOX)).astype(np.float64)[..., None] / 255.0
    inside_box = np.zeros((H, W, 1))
    inside_box[y0:y1 + 1, x0:x1 + 1] = 1
    out = img.copy()
    # only touch pixels inside the card's bounding box (the corner wedges)
    blend = inside_box * (1 - cov)
    return out * (1 - blend) + col * blend


# ---------- tiles ----------

def relayout(spec):
    src = Image.open(need_file(spec['image'], spec['name'], 'image', 'Fix "image" in the spec.')).convert('RGB')
    tiles = [src.crop((x, y, x + w, y + h)) for x, y, w, h in spec['tiles']]
    tw, th = tiles[0].size
    gap, mar = spec.get('gap', 16), spec.get('margin', 16)
    lay = spec.get('layout', 'row')
    if lay == 'row':
        rows, cols = 1, len(tiles)
    else:
        rows, cols = [int(v) for v in lay.split(':')[1].split('x')]
    W = cols * tw + (cols - 1) * gap + 2 * mar
    H = rows * th + (rows - 1) * gap + 2 * mar
    out = Image.new('RGB', (W, H), tuple(spec.get('bg', [30, 27, 25])))
    for i, t in enumerate(tiles):
        rr, cc = divmod(i, cols)
        out.paste(t, (mar + cc * (tw + gap), mar + rr * (th + gap)))
    return out


# ---------- main ----------

def build(spec, cfg, tmp):
    name = spec['name']
    entry = {'slide': spec['slide'], 'name': name, 'file': f'{name}.png'}
    if 'tiles' in spec:
        im = relayout(spec)
        entry.update(source_time=None, source=spec['image'], bubble='none')
        focus = spec.get('focus') or [0, 0, im.width, im.height]
        return im, entry, focus, {}
    if 'image' in spec:
        src = need_file(spec['image'], name, 'image', 'Fix "image" in the spec.')
        img = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
        entry.update(source_time=None, source=spec['image'])
        tsec = None
    else:
        tsec = parse_t(spec['t'])
        video = need_file(cfg.get('video'), name, 'source video',
                          'Put your own copy of the video there (it is not part of the repo), '
                          'or point "video" in the spec at it.')
        img = extract(video, tsec, os.path.join(tmp, f'{name}.png'))
        entry.update(source_time=fmt_t(tsec), source=cfg['video'])
    mode = spec.get('bubble', 'none')
    info = {}
    H, W = img.shape[:2]
    x, y, w, h = spec.get('crop') or [0, 0, W, H]
    if mode in ('scrub', 'cropped'):
        s, cx, cy, r = fit_bubble(img, cfg['bubble_prior'])
        mag = _grad(img)
        bg = np.median([ring_score(mag, cx, cy, rr) for rr in (r + 15, r + 25, r + 35)])
        info = {'bubble_fit': [cx, cy, r], 'edge_before': round(s, 1), 'edge_bg': round(float(bg), 1)}
        if s < 3 * bg + 5:
            raise SystemExit(f'{name}: no clear bubble edge found (score {s:.1f} vs bg {bg:.1f})')
        if mode == 'cropped':
            R = r + spec.get('pad', 8)
            # nearest point of the crop rect to the bubble centre
            nx, ny = min(max(cx, x), x + w - 1), min(max(cy, y), y + h - 1)
            if (nx - cx) ** 2 + (ny - cy) ** 2 <= R * R:
                raise SystemExit(f'{name}: crop {spec["crop"]} intersects the bubble (+{R - r}px)')
            info['clearance_px'] = round(float(np.hypot(nx - cx, ny - cy) - r), 1)
        else:
            rect = (x, y, w, h)
            before_c = ring_score(mag, cx, cy, r, rect=rect)
            bg_c = np.median([ring_score(mag, cx, cy, rr, rect=rect) for rr in (r + 15, r + 25, r + 35)])
            img, R = scrub(img, spec, cx, cy, r, rect)
            after = ring_score(_grad(img), cx, cy, r, rect=rect)
            info.update(edge_in_crop_before=round(before_c, 1), edge_in_crop_bg=round(float(bg_c), 1))
            info['edge_after'] = round(after, 1)
            info['fill'] = spec.get('fill', 'laplace')
            info['pad'] = spec.get('_pad_used', spec.get('pad', 8))
            if 'protect' in spec:
                info['protected_px'] = spec['_protected_px']
            if after > 2 * bg_c + 4:
                raise SystemExit(f'{name}: bubble edge still visible after scrub ({after:.1f} vs bg {bg_c:.1f})')
    if 'square_corners' in spec:
        img = square_corners(img, spec['square_corners'])
    img = np.clip(np.round(img), 0, 255).astype(np.uint8)
    im = Image.fromarray(img).crop((x, y, x + w, y + h))
    entry['crop_in_source'] = [x, y, w, h]
    entry['bubble'] = mode
    focus = spec.get('focus') or [0, 0, im.width, im.height]
    return im, entry, focus, info


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    def opt(name):
        i = args.index(name)
        if i + 1 >= len(args) or args[i + 1].startswith('--'):
            raise SystemExit(f'{name} needs a value')
        return args[i + 1]

    spec_path = rp(args[0])
    only = None
    sheet = None
    if '--only' in args:
        only = set(opt('--only').split(','))
    if '--sheet' in args:
        sheet = rp(opt('--sheet'))
        os.makedirs(os.path.dirname(sheet) or '.', exist_ok=True)
    if not os.path.isfile(spec_path):
        raise SystemExit(f'spec not found: {args[0]}')
    cfg = json.load(open(spec_path, encoding='utf-8'))
    out_dir = rp(cfg['out_dir'])
    os.makedirs(out_dir, exist_ok=True)
    man_path = os.path.join(out_dir, 'shots.json')
    manifest = []
    if os.path.exists(man_path):
        manifest = json.load(open(man_path, encoding='utf-8'))
    by_name = {e['name']: e for e in manifest}
    built = []
    with tempfile.TemporaryDirectory() as tmp:
        for spec in cfg['shots']:
            if only and spec['name'] not in only:
                continue
            im, entry, focus, info = build(spec, cfg, tmp)
            fx, fy, fw, fh = focus
            if fx < 0 or fy < 0 or fx + fw > im.width or fy + fh > im.height:
                raise SystemExit(f'{spec["name"]}: focus {focus} outside {im.size}')
            im.save(os.path.join(out_dir, entry['file']), optimize=True)
            entry['size'] = [im.width, im.height]
            entry['focus'] = focus
            entry['note'] = spec.get('note', '')
            if info:
                entry['check'] = info
            by_name[entry['name']] = entry
            built.append((entry, im))
            print(f'ok  {entry["file"]:34s} {im.width}x{im.height}  bubble={entry["bubble"]}  {info}')
    order = [s['name'] for s in cfg['shots']]
    manifest = sorted(by_name.values(), key=lambda e: order.index(e['name']) if e['name'] in order else 999)
    with open(man_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'wrote {rel(man_path)} ({len(manifest)} shots)')
    if sheet and built:
        tw = 640
        cells = []
        for e, im in built:
            th = int(tw * im.height / im.width)
            t = im.resize((tw, th), Image.LANCZOS).convert('RGB')
            d = ImageDraw.Draw(t)
            fx, fy, fw, fh = [v * tw / im.width for v in e['focus']]
            d.rectangle([fx, fy, fx + fw, fy + fh], outline=(0, 255, 0), width=2)
            d.text((6, 4), e['name'], fill=(255, 0, 255))
            cells.append(t)
        cols = 2
        rows_h = []
        for i in range(0, len(cells), cols):
            rows_h.append(max(c.height for c in cells[i:i + cols]))
        S = Image.new('RGB', (cols * (tw + 8), sum(h + 8 for h in rows_h)), 'white')
        yy = 0
        for ri, i in enumerate(range(0, len(cells), cols)):
            for ci, c in enumerate(cells[i:i + cols]):
                S.paste(c, (ci * (tw + 8), yy))
            yy += rows_h[ri] + 8
        S.save(sheet, quality=88)
        print(f'sheet {rel(sheet)}')


if __name__ == '__main__':
    main()
