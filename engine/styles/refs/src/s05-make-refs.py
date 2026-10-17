# Builds engine/styles/refs/s05-ref-*.png from your own S05 desk photos (or finished S05 slides): the screen quad
# becomes flat magenta, white caption stickers outside the screen and small hardware marks are inpainted.
#
#   python -I engine/styles/refs/src/s05-make-refs.py <photo-dir> [out-dir]
#
# <photo-dir> holds desk.jpg (near-frontal), close.jpg (camera close, webcam at the top) and canted.jpg (monitor
# turned ~20 degrees). The quads, sticker boxes and mark boxes below were measured on the shipped refs' source
# photos (1080 px wide): re-measure them on yours (4 screen corners clockwise from top-left, boxes as x, y, w, h).
# Run from the repo root. Needs opencv-python and numpy.
import cv2, numpy as np, os, sys

if len(sys.argv) < 2:
    sys.exit("usage: python -I engine/styles/refs/src/s05-make-refs.py <photo-dir> [out-dir]")
SRC = sys.argv[1].rstrip("/\\") + "/"
OUT = (sys.argv[2] if len(sys.argv) > 2 else "engine/styles/refs").rstrip("/\\") + "/"


def white_stickers(img):
    # caption stickers: near-white, low-saturation, large connected blocks
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 225) & (hsv[..., 1] < 30)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if w > 180 and h > 50 and a > 0.45 * w * h:
            keep[lab == i] = 1
    return cv2.dilate(keep, np.ones((9, 9), np.uint8))


def build(name, quad, out, extra_boxes=(), crop=None, sticker_boxes=()):
    path = SRC + name
    if not os.path.exists(path):
        print("skip (missing):", path)
        return
    img = cv2.imread(path)
    H, W = img.shape[:2]
    q = np.array(quad, np.int32)
    scr = np.zeros((H, W), np.uint8); cv2.fillPoly(scr, [q], 1)
    m = white_stickers(img)
    for (x, y, w, h) in sticker_boxes:
        m[y:y + h, x:x + w] = 1
    for (x, y, w, h) in extra_boxes:
        m[y:y + h, x:x + w] = 1
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    m[scr == 1] = 1  # never inpaint from the screen's own pixels
    img = cv2.inpaint(img, m * 255, 9, cv2.INPAINT_TELEA)
    img[scr == 1] = (255, 0, 255)
    if crop:
        x, y, w, h = crop; img = img[y:y + h, x:x + w]
    cv2.imwrite(OUT + out, img)
    print(out, img.shape)


# desk view, near-frontal; the monitor maker's mark on the stand inpainted
build("desk.jpg", [(0, 203), (1080, 193), (1080, 1236), (0, 1226)], "s05-ref-desk.png",
      extra_boxes=[(488, 1248, 90, 48)], sticker_boxes=[(30, 150, 1005, 60)])
# close view, screen fills the frame
build("close.jpg", [(0, 180), (1080, 158), (1080, 1350), (0, 1350)], "s05-ref-close.png")
# canted view in a red-lit room, a 1080x1440 photo cropped to 1080x1350
build("canted.jpg", [(0, 283), (1080, 92), (1080, 1242), (0, 1090)], "s05-ref-canted.png",
      sticker_boxes=[(180, 120, 720, 175), (95, 1045, 890, 305)], crop=(0, 40, 1080, 1350))
