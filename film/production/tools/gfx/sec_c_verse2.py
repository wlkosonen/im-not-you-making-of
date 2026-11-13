"""Section C, verse 2, the break, the constellation and the city (song 56.96-81.17, 94.33-105.00 in Lati's cut).

Every shot is found in Lati's cut (F.spans, F.shot_at), every graphic is a pure function of song time and the frame.
The verse's lines are matched to the shots they play over in the cut, not to the board's shot ids (the cut moved them):

  s039 s042 s040 (the sakura, 56.96-66.79)  quiet: nothing (Lati, 8 Nov: no UI; the karaoke line alone)
  s044 stills (66.79-67.50)                 her face being taken: three flashes, each corrupted one step more
                                            (1 a scanline tear, 2 + a colour split, 3 + a red cast), picture()
  s044 hands typing (67.50-68.33)           "write the phishing mail": the mail types itself on the keyboard's display
  s043 the farm (68.33-68.83)               "mail": the same mail on every screen of the farm, found in each frame
  s043 > s047 (68.65-69.71)                 "clone the voice": a voice-match gauge, a red terminal on glass (over)
  s049 (69.71-70.46)                        "fake the face": FACE SYNTH, her face (the last stolen still) rebuilt
                                            4x4 to 64x64 (over), small copies on the bunker's terminals (world)
  s046 (70.46-72.71)                        "run the swarm, calibrate": a readout on the wall of screens, until the
                                            wall turns into the eyes ("erase the trace" is left to the picture)
  s048 > s049 (73.26-75.50)                 "scrape the data, build the profile, sell the fear": a profile (over)
  s047 (75.96-77.50)                        "train me on the worst of you": nothing (the REFUSAL RATE panel dropped,
                                            Lati 12 Nov: it blocked the vats)
  black (77.50-78.62)                       "act surprised I'm here": the karaoke cursor alone, blinking on the beat
  s050 (78.62-81.17)                        locked picture, scaled to 0.82 and lifted out of the lyric band (Lati, 12
                                            Nov); the approved side instruments drawn through the same transform
  s060 (94.33-97.12)                        proposal: a constellation drawn on the sky's own stars (CONSTELLATION)
  s066 s064 s062 (the city, 97.12-105.00)   light: a transit board on s064's blank shelter screen; the aerials bare

Facts are from research/forms.md (its "Shown as / limits" column kept); where a readout is not data it says
ILLUSTRATIVE in micro-type. Bunker graphics are red (the swarm, the bunker), the cursor amber (the karaoke line's).
Tracked surfaces: the screens are found afresh in each frame (pink-glow masks from F.IMG); a camera move is measured by
matching each frame of the take to one reference frame (never frame to frame, film 2's drift lesson), then smoothed.
Section C agent ("verse2"), 12 Nov 2026; s050's side instruments by Kiln, 12 Nov 2026.
"""
import math
import subprocess
from functools import lru_cache

import cv2
import numpy as np
import skia

import base as F


def _span(shot, kind=None, n=0):
    s = [x for x in F.spans(shot) if kind is None or x[2]["kind"] == kind]
    return s[n] if len(s) > n else None


S050 = F.spans("s050")
FLASHES = sorted(x for x in F.spans("s044") if x[2]["kind"] == "image")  # her three stills, in cut order
TYPING = _span("s044", "video")
RANGES = [(F.spans("s039")[0][0], S050[-1][1]), (F.spans("s060")[0][0], F.spans("s062")[-1][1])]
CUTS = {TYPING[0]: ("crt_roll", 2)} if TYPING else {}  # out of her taken face into the bunker's first terminal
IMPACTS = []  # none at the break: see the log (the break is the film's quiet refusal, and s050 is locked)
CONSTELLATION = True  # s060's proposal, switchable

DARK = 0x2a0606  # ink on a lit pink screen
HOT = 0xff8f80  # bright phosphor on a dark window
DIMR = 0x8a2222


# ---------- the song's words and grid (times come from the snapped words, never typed in)
def wt(line, word, n=0, end=False):
    ws = [w for w in F.WORDS if w.get("line") == line and w["w"].lower().strip(".,!?—'") == word]
    w = ws[min(n, len(ws) - 1)]
    return (w.get("t1") or w["t0"] + 0.2) if end else w["t0"]


def grid(t, tol=0.12):
    """the beat nearest t if one is within tol: graphics enter on the grid"""
    i = int(np.argmin([abs(b - t) for b in F.BEATS]))
    return F.BEATS[i] if abs(F.BEATS[i] - t) <= tol else t


# ---------- s050's side instruments (Kiln, 12 Nov; approved by Lati, 12 Nov: "side fill good"). Unchanged.
# s050 (the break, locked 10 Nov) is a red lens in a box centred in black. Lati, 12 Nov: "what is missing is fluff to
# empty black sidelines". Two side instruments in the box's own style (its border and fill colours measured from the
# render), so the three read as one console: on the left a waterfall of the voice, rising (the signatures rise again);
# on the right level columns with peak hold; under each a small trace. All of it is the vocal stem itself, line 15, like
# the oscillator in the box: no text, no invented readings. In the world layer (part of the picture).
EDGE, FILL, DIM = 0x595252, 0x1d1619, 0x3a0d0d
PANELS = [(150, 40, 370, 1000), (1400, 40, 370, 1000)]  # x, y, w, h (the box: 580-1340, 40-1040)


def panel(c, x, y, w, h, a):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=F.col(FILL, a)))
    c.drawRect(skia.Rect.MakeXYWH(x + 1, y + 1, w - 2, h - 2), F.stroke(EDGE, a, 3))
    for sx, sy in ((x + 18, y + 18), (x + w - 18, y + 18), (x + 18, y + h - 18), (x + w - 18, y + h - 18)):
        c.drawCircle(sx, sy, 5, skia.Paint(Color=F.col(EDGE, a), AntiAlias=True))


def waterfall(c, x, y, w, h, t, a, rows=72, bands=36, step=0.035):
    cw, ch = w / bands, h / rows
    for i in range(rows):  # newest at the bottom, rising
        lv = F.vocal_bands(t - (rows - 1 - i) * step, bands=bands, win=1024)
        yy = y + i * ch
        for j, v in enumerate(lv):
            if v > 0.12:
                k = min(1.0, (v - 0.12) * 1.6) * (0.35 + 0.65 * i / rows)
                c.drawRect(skia.Rect.MakeXYWH(x + j * cw + 1, yy + 1, cw - 2, ch - 1.5),
                           skia.Paint(Color=F.col(F.RED, a * k)))


def columns(c, x, y, w, h, t, a, n=10, segs=26):
    lv = F.vocal_bands(t, bands=n)
    hold = np.max([F.vocal_bands(t - d, bands=n) for d in (0.08, 0.16, 0.24, 0.32, 0.4)], axis=0)
    cw, sh = w / n, h / segs
    for j in range(n):
        lit = int(lv[j] * segs)
        pk = min(segs - 1, int(hold[j] * segs))
        for s in range(segs):
            on = s < lit
            col = F.RED if s < segs * 0.75 else F.AMBER
            al = (0.95 if on else (0.9 if s == pk else 0.10)) * a
            c.drawRect(skia.Rect.MakeXYWH(x + j * cw + 4, y + h - (s + 1) * sh + 2, cw - 8, sh - 4),
                       skia.Paint(Color=F.col(col if (on or s == pk) else DIM, al)))


def trace(c, x, y, w, h, t, a, dur=0.05):
    wv = F.vocal_wave(t, dur=dur, n=180)
    p = skia.Path()
    for i, v in enumerate(wv):
        (p.moveTo if i == 0 else p.lineTo)(x + w * i / (len(wv) - 1), y + h / 2 - v * h * 1.6)
    F.glow_draw(c, lambda: c.drawPath(p, F.stroke(F.RED, a, 2)), blur=4, amount=0.8)


# Lati, 12 Nov (pass 1): "lyrics line is over half boxes, either frame should move/be cropped upper or lyrics line moved
# down so they don't collide. I'm leaning first." The locked picture is scaled about a point above its top centre so the
# box (40-1040) lands at 30-850, oscillator strip and all; the side panels go through the same transform, so the three
# still read as one console and nothing of it is below ~860.
S050_K, S050_X, S050_Y = 0.82, 960.0, -15.6


def s050_lift(img):
    h, w = img.shape[:2]
    u = w / F.U
    M = np.float32([[S050_K, 0, S050_X * u * (1 - S050_K)], [0, S050_K, S050_Y * u * (1 - S050_K)]])
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))


def s050_world(c, t, F):
    a0, a1, _ = next(s for s in S050 if s[0] <= t < s[1])
    a = F.ease((t - a0) / 0.3)
    c.save()
    c.translate(S050_X * (1 - S050_K), S050_Y * (1 - S050_K))
    c.scale(S050_K, S050_K)
    for x, y, w, h in PANELS:
        panel(c, x, y, w, h, a)
        c.drawRect(skia.Rect.MakeXYWH(x + 40, y + 750, w - 80, 140), skia.Paint(Color=F.col(0x0c0707, a)))
    lx, ly, lw, lh = PANELS[0]
    waterfall(c, lx + 40, ly + 60, lw - 80, 640, t, a)
    trace(c, lx + 50, ly + 760, lw - 100, 120, t, a)
    rx, ry, rw, rh = PANELS[1]
    columns(c, rx + 40, ry + 60, rw - 80, 640, t, a)
    trace(c, rx + 50, ry + 760, rw - 100, 120, t - 0.11, a, dur=0.12)
    c.restore()


# ---------- the camera, measured: each frame of a take matched to one reference frame, never chained
@lru_cache(12)
def take(file):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F.ROOT / file), "-vf", "scale=640:360", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 360, 640, 3)


@lru_cache(12)
def anchor(file, i0, i1, region=None):
    """{take frame: 2x3 similarity, reference (frame i0) -> that frame, in 1920 units}. Each frame is matched to the
    reference afresh (ORB, RANSAC); the four parameters are then smoothed over 5 frames. `region` (x0, y0, x1, y1 in
    1920 units) limits the reference's features to the surface the graphic sits on (s046: the wall, not the girders
    and bots in front of it, which move differently). Also returns the worst inlier residual and
    the worst gap between measured and smoothed, both in 1920 units, for the log."""
    fr = take(file)
    i1 = min(i1, len(fr) - 1)
    orb = cv2.ORB_create(3000)
    g0 = cv2.cvtColor(fr[i0], cv2.COLOR_RGB2GRAY)
    mask = np.zeros_like(g0)
    x0, y0, x1, y1 = [int(v / 3) for v in (region or (0, 0, 1920, 1080))]
    mask[y0:y1, x0:x1] = 255
    k0, d0 = orb.detectAndCompute(g0, mask)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    par, res = {}, 0.0
    for i in range(i0, i1 + 1):
        if i == i0:
            par[i] = (1.0, 0.0, 0.0, 0.0)
            continue
        k, d = orb.detectAndCompute(cv2.cvtColor(fr[i], cv2.COLOR_RGB2GRAY), None)
        m = bf.match(d0, d) if d is not None else []
        if len(m) < 12:
            continue
        a = np.float32([k0[x.queryIdx].pt for x in m])
        b = np.float32([k[x.trainIdx].pt for x in m])
        M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.5, maxIters=4000)
        if M is None or inl.sum() < 10:
            continue
        ok = inl.ravel() > 0
        e = np.median(np.hypot(*(a[ok] @ M[:, :2].T + M[:, 2] - b[ok]).T)) * 3
        res = max(res, float(e))
        par[i] = (M[0, 0], M[1, 0], M[0, 2] * 3, M[1, 2] * 3)
    idx = np.arange(i0, i1 + 1)
    ks = sorted(par)
    raw = np.array([[np.interp(i, ks, [par[k][j] for k in ks]) for j in range(4)] for i in idx])
    ker = np.ones(5) / 5
    sm = np.stack([np.convolve(np.pad(raw[:, j], 2, mode="edge"), ker, "valid") for j in range(4)], 1)
    corners = np.array([[0, 0], [1920, 0], [0, 1080], [1920, 1080], [960, 540]], np.float32)

    def warp(p, pts):
        a, b, tx, ty = p
        return np.stack([a * pts[:, 0] - b * pts[:, 1] + tx, b * pts[:, 0] + a * pts[:, 1] + ty], 1)
    gap = max(float(np.abs(warp(r, corners) - warp(s, corners)).max()) for r, s in zip(raw, sm))
    return {int(i): tuple(s) for i, s in zip(idx, sm)}, res, gap


def cam(p, t, region=None):
    """skia matrix (reference frame -> the frame at song time t) for piece p"""
    q = cam_params(p, t, region)
    return skia.Matrix.MakeAll(q[0], -q[1], q[2], q[1], q[0], q[3], 0, 0, 1)


def cam_params(p, t, region=None):
    """(a, b, tx, ty): x' = a x - b y + tx, y' = b x + a y + ty, reference frame -> the frame at t, 1920 units"""
    i0 = int(round(F.src_t(p, p["t0"]) * 24))
    i1 = int(math.ceil(F.src_t(p, p["t1"]) * 24)) + 1
    an, _, _ = anchor(p["file"], i0, i1, region)
    fi = F.src_t(p, t) * 24
    a, b = int(np.floor(fi)), int(np.floor(fi)) + 1
    pa, pb = an.get(a, an[max(an)] if a > max(an) else an[min(an)]), an.get(b, an[max(an)] if b > max(an) else an[min(an)])
    u = fi - np.floor(fi)
    return [x * (1 - u) + y * u for x, y in zip(pa, pb)]


# ---------- the screens, found in each frame: lit pink glass
def pink(img, loose=False):
    f = img.astype(np.int16)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    return ((r > (150 if loose else 170)) & (r - g > 50) & (r - b > 40)).astype(np.uint8)


def screens(img, min_area=900):
    """[(x, y, w, h)] in 1920 units of the lit screens in this frame (closed so text lines inside count as glass)"""
    h, w = img.shape[:2]
    k = 1920 / w
    m = cv2.morphologyEx(pink(img), cv2.MORPH_CLOSE, np.ones((max(3, int(9 / k)),) * 2, np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    out = []
    for i in range(1, n):
        x, y, ww, hh, area = st[i]
        if area * k * k >= min_area and area > 0.55 * ww * hh and 0.6 < ww / max(1, hh) < 6:
            out.append((x * k, y * k, ww * k, hh * k))
    return out


def terminal_screens(img, min_area=1200):
    """the desks' lit monitors only, never the bots' eyes (Lati, 12 Nov, master v1: "her face as inserts in bots eyes,
    thats just weird. I would drop that"). Measured on every frame of s049: a monitor is flat-lit pink glass, its green
    lifted by the glass's own pale glow (mean G >= 105 of 255, spread of G <= 36) and filling its tilted rectangle
    (>= 0.72); an eye is deep red light with a hot core (G 84-98, spread 39-57), and eyes come in pairs: two blobs of
    like size side by side at one height. Anything that fails, or has a twin, is not a screen."""
    h, w = img.shape[:2]
    k = 1920 / w
    m = cv2.morphologyEx(pink(img), cv2.MORPH_CLOSE, np.ones((max(3, int(9 / k)),) * 2, np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    cand = []
    for i in range(1, n):
        x, y, ww, hh, area = st[i]
        if area * k * k < min_area or not (area > 0.55 * ww * hh and 0.6 < ww / max(1, hh) < 6) or (y + hh * 0.5) * k >= 900:
            continue
        g = img[..., 1][lab == i].astype(np.float32)
        cs, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (_, _), (rw, rh), _ = cv2.minAreaRect(cs[0])
        cand.append((x, y, ww, hh, area, float(g.mean()), float(g.std()), area / max(1.0, rw * rh)))
    out = []
    for c in cand:
        x, y, ww, hh, area, gm, gs, rect = c
        twin = any(o is not c and abs((o[1] + o[3] / 2) - (y + hh / 2)) < 0.5 * hh and 0.6 < o[4] / area < 1.6
                   and abs((o[0] + o[2] / 2) - (x + ww / 2)) < 3 * max(ww, o[2]) for o in cand)
        if gm >= 105 and gs <= 36 and rect >= 0.72 and not twin:
            out.append((x * k, y * k, ww * k, hh * k))
    return out


def ink(c, draw, mask, color=DARK, strength=0.85):
    """draw() (in 1920 units, white on a fresh layer) as dark ink on the picture, only where `mask` (frame-sized,
    0..1) is set: the lit glass of the screen, so fingers, arms and edges in front keep their place"""
    h, w = F.IMG.shape[:2]
    s = skia.Surface(w, h)
    sc = s.getCanvas()
    sc.clear(skia.ColorTRANSPARENT)
    sc.scale(w / F.U, w / F.U)
    draw(sc)
    a = s.makeImageSnapshot().toarray()[..., 3].astype(np.float32) / 255 * mask * strength
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = color >> 16 & 255, color >> 8 & 255, color & 255
    rgba[..., 3] = (a * 255).astype(np.uint8)
    img = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)
    c.save()
    c.resetMatrix()
    c.drawImage(img, 0, 0)
    c.restore()


def glyphs(text):
    """the console font's glyphs as a white skia image, 8 px tall (drawn scaled up, nearest: hard pixels)"""
    m = F.bitmap_text(text)
    rgba = np.zeros(m.shape + (4,), np.uint8)
    rgba[m] = 255
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


NEAREST = skia.SamplingOptions(skia.FilterMode.kNearest)


def bmtext(c, text, x, y, size, paint=None):
    """console-font text, `size` units tall, top-left at (x, y)"""
    if not text:
        return 0
    im = glyphs(text)
    w = im.width() * size / 8
    c.drawImageRect(im, skia.Rect.MakeXYWH(x, y, w, size), NEAREST, paint or skia.Paint())
    return w


# ---------- the red terminal on glass: a small pixel canvas drawn hard, scaled up with scanlines (the bunker's voice)
class Px:
    def __init__(self, cols, rows, pad=4, lh=10):
        self.lh, self.pad = lh, pad
        self.a = np.zeros((rows * lh + pad * 2, cols * 8 + pad * 2, 4), np.float32)

    def fill(self, x, y, w, h, color, a=1.0):
        sub = self.a[max(0, int(y)):max(0, int(y + h)), max(0, int(x)):max(0, int(x + w))]
        rgb = np.array([color >> 16 & 255, color >> 8 & 255, color & 255], np.float32)
        sub[..., :3] = sub[..., :3] * (1 - a) + rgb * a
        sub[..., 3] = np.maximum(sub[..., 3], a)

    def text(self, s, col, row, color=F.RED, a=1.0, px=None, py=None):
        m = F.bitmap_text(s).astype(np.float32) * a
        x = self.pad + col * 8 if px is None else int(px)
        y = self.pad + row * self.lh + 1 if py is None else int(py)
        h, w = self.a.shape[:2]
        x1, y1 = min(w, x + m.shape[1]), min(h, y + m.shape[0])
        if x1 <= x or y1 <= y:
            return
        mm = m[:y1 - y, :x1 - x, None]
        rgb = np.array([color >> 16 & 255, color >> 8 & 255, color & 255], np.float32)
        reg = self.a[y:y1, x:x1]
        reg[..., :3] = reg[..., :3] * (1 - mm) + rgb * mm
        reg[..., 3:] = np.maximum(reg[..., 3:], mm)

    def line(self, pts, color, a=1.0, th=1):
        m = np.zeros(self.a.shape[:2], np.uint8)
        cv2.polylines(m, [np.int32(np.round(pts))], False, 255, th, lineType=cv2.LINE_8)
        mm = (m[..., None] / 255.0) * a
        rgb = np.array([color >> 16 & 255, color >> 8 & 255, color & 255], np.float32)
        self.a[..., :3] = self.a[..., :3] * (1 - mm) + rgb * mm
        self.a[..., 3:] = np.maximum(self.a[..., 3:], mm)

    def box(self, x, y, w, h, color, a=1.0):
        self.line([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], color, a)

    def image(self, s=3, alpha=1.0):
        """the canvas scaled up s times, the last row of each pixel dimmed (scanlines), as a skia image"""
        big = np.kron(self.a, np.ones((s, s, 1), np.float32))
        big[s - 1::s, :, 3] *= 0.45
        out = np.zeros(big.shape, np.uint8)
        out[..., :3] = np.clip(big[..., :3], 0, 255).astype(np.uint8)
        out[..., 3] = (np.clip(big[..., 3], 0, 1) * 255 * alpha).astype(np.uint8)
        return skia.Image.fromarray(out, colorType=skia.ColorType.kRGBA_8888_ColorType)

    def blit(self, c, x, y, s=3, alpha=1.0, open_k=1.0, glow=True, width=None):
        """draw at (x, y) in 1920 units, each pixel s units (or scaled to `width`); open_k < 1 opens it from its
        middle line like a CRT window"""
        img = self.image(s, alpha)
        k = (width / img.width()) if width else 1.0
        dst = skia.Rect.MakeXYWH(x, y, img.width() * k, img.height() * k)
        c.save()
        if open_k < 1:
            cy = dst.centerY()
            c.translate(0, cy)
            c.scale(1, max(0.02, open_k))
            c.translate(0, -cy)
        if glow:
            c.drawImageRect(img, dst, NEAREST, skia.Paint(Alphaf=0.55, ImageFilter=skia.ImageFilters.Blur(s * k * 1.6, s * k * 1.6)))
        c.drawImageRect(img, dst, NEAREST, skia.Paint())
        c.restore()
        return dst


def window(cols, rows, title, lh=10):
    p = Px(cols, rows, lh=lh)
    p.fill(0, 0, p.a.shape[1], p.a.shape[0], 0x0e0505, 0.86)
    p.box(0, 0, p.a.shape[1] - 1, p.a.shape[0] - 1, DIMR)
    p.fill(1, 1, p.a.shape[1] - 2, lh + 1, F.RED, 0.9)
    p.text(title, 0, 0, 0x140404, py=p.pad - 1)
    return p


MICRO = 0xd0584c


def micro(c, lines, x, y, a=1.0, color=MICRO, right=None):
    """micro-type under a window: the source and the ILLUSTRATIVE mark, 2 units a pixel; `right` aligns its right
    edge there instead of starting at x"""
    p = Px(max(len(s) for s in lines), len(lines), pad=2, lh=9)
    p.fill(0, 0, p.a.shape[1], p.a.shape[0], 0x0e0505, 0.8)
    for i, s in enumerate(lines):
        p.text(s, 0, i, color, py=2 + i * 9)
    if right is not None:
        x = right - p.a.shape[1] * 2
    p.blit(c, x, y, s=2, alpha=a, glow=False)


def opening(t, t0, dur=3 / 24):
    return F.ease((t - t0) / dur)


# ---------- her face being taken: the three balcony stills, each one step more corrupt (picture layer)
def corrupt(img, step, t):
    h, w = img.shape[:2]
    k = w / 1920
    rng = np.random.default_rng(int(round(t * 24)) * 7 + step)
    out = img.copy()
    # 1: a scanline tear: bands slip sideways, a bright retrace line rolls through
    nb = (5, 9, 14)[step - 1]
    for _ in range(nb):
        y0 = int(rng.integers(0, h - 8))
        bh = int(rng.integers(3, (24, 46, 70)[step - 1]) * k) + 1
        dx = int(rng.integers(-1, 2) * rng.integers(12, (60, 120, 200)[step - 1]) * k)
        out[y0:y0 + bh] = np.roll(out[y0:y0 + bh], dx, axis=1)
    yb = int((t * 9 % 1) * h)
    out[yb:yb + max(2, int(4 * k))] = np.clip(out[yb:yb + max(2, int(4 * k))].astype(np.int16) + 90, 0, 255)
    rows = np.ones((h, 1, 1), np.float32)
    rows[::max(2, int(3 * k))] = (0.82, 0.72, 0.62)[step - 1]
    out = (out * rows).astype(np.uint8)
    if step >= 2:  # 2: the colours split and shift
        sh = max(2, int((14 if step == 2 else 24) * k))
        out[..., 0] = np.roll(out[..., 0], sh, axis=1)
        out[..., 2] = np.roll(out[..., 2], -sh, axis=1)
        f = out.astype(np.float32)
        f[..., 1] *= 0.86
        f[..., 2] = f[..., 2] * 1.05 + 10
        out = np.clip(f, 0, 255).astype(np.uint8)
    if step >= 3:  # 3: the red cast: the bunker's red takes her, coarse blocks in the torn bands
        f = out.astype(np.float32)
        y = f.mean(2, keepdims=True)
        red = np.concatenate([y * 1.15 + 20, y * 0.22, y * 0.2], 2)
        out = np.clip(f * 0.25 + red * 0.75, 0, 255).astype(np.uint8)
        b = max(4, int(16 * k))
        for _ in range(4):
            y0 = int(rng.integers(0, h - 40))
            bh = int(rng.integers(20, 90) * k) + b
            band = out[y0:y0 + bh]
            sm = cv2.resize(band, (max(1, w // b), max(1, band.shape[0] // b)), interpolation=cv2.INTER_AREA)
            out[y0:y0 + bh] = cv2.resize(sm, (w, band.shape[0]), interpolation=cv2.INTER_NEAREST)
    return out


def picture(img, t, F):
    for n, (a, b, _) in enumerate(FLASHES[:3]):
        if a <= t < b:
            return corrupt(img, n + 1, t)
    if any(a <= t < b for a, b, _ in S050):
        return s050_lift(img)
    return img


# ---------- s044, the hands typing: the phishing mail on the keyboard's display (ILLUSTRATIVE, no brand)
MAIL = ["FROM: IT SERVICE DESK", "SUBJECT: PASSWORD EXPIRES TODAY", "Verify your account within 24 h:"]
DISPLAY = [(376, 783), (1393, 872), (1283, 986), (232, 879)]  # the display's glass in the take (measured, reference)


def mail_chars(t):
    a, b = grid(wt(11, "write")), wt(11, "mail", end=True)
    n = sum(len(s) for s in MAIL)
    return int(n * min(1.0, max(0.0, (t - a) / (b - a))))


def s044_world(c, t, p):
    shown = mail_chars(t)
    M = cam(p, t)
    m = cv2.dilate(pink(F.IMG, loose=True), np.ones((3, 3), np.uint8)).astype(np.float32)
    h, w = m.shape
    m[int(905 * w / 1920):] = 0  # the lyric's band stays clear
    (x0, y0), (x1, y1) = DISPLAY[0], DISPLAY[1]
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))

    def draw(sc):
        sc.concat(M)
        sc.translate(x0 + 34, y0 + 14)
        sc.rotate(ang)
        left = shown
        for i, s in enumerate(MAIL):
            k = min(len(s), max(0, left))
            left -= len(s)
            wpx = bmtext(sc, s[:k], 0, i * 30, 22)
            if 0 < k < len(s) or (k == len(s) and left <= 0 and i == len(MAIL) - 1):
                if int(t * 6) % 2 == 0 or k < len(s):
                    sc.drawRect(skia.Rect.MakeXYWH(wpx + 3, i * 30, 13, 22), skia.Paint(Color=skia.ColorWHITE))
                break
        bmtext(sc, "ILLUSTRATIVE", 800, -2, 9)
    ink(c, draw, m, DARK, 0.88)


# ---------- s043, the farm: the same mail on every screen it passes (bars of the mail's own lines)
def s043_world(c, t, p):
    m = pink(F.IMG, loose=True).astype(np.float32)
    h, w = m.shape
    m[int(905 * w / 1920):] = 0
    found = screens(F.IMG, min_area=700)

    def draw(sc):
        for x, y, ww, hh in found:
            ix, iy = x + ww * 0.14, y + hh * 0.2
            for i, s in enumerate(MAIL):
                lh = hh * 0.6 / len(MAIL)
                sc.drawRect(skia.Rect.MakeXYWH(ix, iy + i * lh, ww * 0.72 * len(s) / 34, lh * 0.55), skia.Paint(Color=skia.ColorWHITE))
    ink(c, draw, m, DARK, 0.8)


# ---------- "clone the voice": the gauge, a terminal on glass (over). The reference trace is the vocal stem itself
def gauge_over(c, t):
    t0 = grid(wt(11, "clone"))
    t_done = wt(11, "voice", end=True)
    if t < t0:
        return
    k = F.ease((t - t0) / (t_done - t0))
    p = window(30, 8, " VOICE MATCH")
    W = p.a.shape[1]
    ref = F.vocal_wave(t - 0.02, dur=0.06, n=W - 40)
    rng = np.random.default_rng(int(t * 24))
    syn = ref * (0.35 + 0.65 * k) + rng.normal(0, 0.12 * (1 - k) + 0.004, len(ref))
    for row, wv, col in ((1, ref, F.RED), (3, syn, HOT)):
        cy = p.pad + row * 10 + 9
        p.text("REF" if row == 1 else "SYN", 0, row, DIMR, py=cy - 4)
        p.line([(30 + i, cy - np.clip(v, -1, 1) * 22) for i, v in enumerate(wv)], col)
    segs, sy = 24, p.pad + 6 * 10 + 2
    for s in range(segs):
        on = s < int(k * segs)
        p.fill(p.pad + 4 + s * 9, sy, 7, 8, F.RED if on else 0x3a0d0d, 1.0 if on else 0.8)
    if k >= 0.999:
        if int((t - t_done) * 8) % 2 == 0:
            p.text("MATCH", 0, 6, HOT, px=W - 4 - 5 * 8, py=sy)
    a = opening(t, t0)
    x, y = 1920 - 96 - W * 3, 92
    p.blit(c, x, y, s=3, open_k=a)
    if a > 0.9:
        micro(c, ["ILLUSTRATIVE READOUT", "NEW HAMPSHIRE ROBOCALL, 21 JAN 2024: A CLONED VOICE", "FCC FINE $6M; AI VOICES RULED 'ARTIFICIAL', 8 FEB 2024"],
              x, y + p.a.shape[0] * 3 + 8, right=x + W * 3)


# ---------- s049, "fake the face": her face (from the stolen still) rebuilt block by block on the terminals
@lru_cache(1)
def her_face():
    a, b, p = FLASHES[-1]  # s044-1: the last, reddest flash
    im = cv2.cvtColor(cv2.imread(str(F.ROOT / p["file"])), cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = im.shape
    k = w / 2048
    face = im[int(60 * k):int(400 * k), int(1000 * k):int(1340 * k)]
    return cv2.resize(face, (64, 64), interpolation=cv2.INTER_AREA) / 255


@lru_cache(8)
def face_blocks(n):
    f = cv2.resize(her_face(), (n, n), interpolation=cv2.INTER_AREA)
    f = np.round(f * 5) / 5  # few levels: the screen's own dot pitch
    return np.kron(f, np.ones((64 // n, 64 // n)))


def s049_face_world(c, t, p):
    face_t = wt(11, "face")
    n = 4 if t < face_t else 8 if t < face_t + 0.18 else 16 if t < face_t + 0.36 else 32
    f = 1 - face_blocks(n)  # ink where she is dark (hair, eyes)
    m = cv2.dilate(pink(F.IMG, loose=True), np.ones((3, 3), np.uint8)).astype(np.float32)
    h, w = m.shape
    m[int(905 * w / 1920):] = 0
    found = terminal_screens(F.IMG)
    rgba = np.zeros((64, 64, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = (np.clip(f, 0, 1) * 255).astype(np.uint8)
    im = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)

    def draw(sc):
        for x, y, ww, hh in found:
            side = min(ww * 0.9, hh * 0.92)
            sc.drawImageRect(im, skia.Rect.MakeXYWH(x + (ww - side) / 2, y + (hh - side) / 2, side, side), NEAREST, skia.Paint())
    ink(c, draw, m, DARK, 0.9)


def face_over(c, t, p):
    """the face being made: the stolen still rebuilt block by block, 4x4 to 64x64, the resolution its own readout"""
    face_t = grid(wt(11, "face"))
    steps = [p["t0"], face_t, face_t + 0.16, face_t + 0.32, face_t + 0.48]
    n = [4, 8, 16, 32, 64][max(0, int(np.searchsorted(steps, t, side="right")) - 1)]
    q = window(11, 9, " FACE SYNTH")
    f = face_blocks(n) if n < 64 else np.round(her_face() * 7) / 7
    ox, oy = q.pad + 12, q.pad + 13
    lv = (0.12 + 0.88 * f)[..., None] * np.array([255, 64, 64], np.float32)
    q.a[oy:oy + 64, ox:ox + 64, :3] = lv
    q.a[oy:oy + 64, ox:ox + 64, 3] = 1.0
    q.box(ox - 2, oy - 2, 67, 67, DIMR)
    q.text(f"{n}x{n}", 0, 0, HOT if n == 64 else F.RED, px=ox, py=oy + 68)
    a = opening(t, p["t0"])
    x, y = 560, 70
    q.blit(c, x, y, s=4, open_k=a)
    if a > 0.9:
        micro(c, ["ILLUSTRATIVE", "HONG KONG, JAN 2024: A PRE-RECORDED DEEPFAKE 'MEETING'",
                  "ABOUT HK$200M TO FIVE ACCOUNTS (HK GOVERNMENT, 26 JUN 2024)"], x, y + q.a.shape[0] * 4 + 8)


# ---------- s046, the wall of screens: "run the swarm, calibrate" (world, on the wall, the camera measured)
WALL = (290, 372, 500, 268)  # x, y, w, h in the take's first frame: the lower rows of the left wall section
WALL_FEAT = (0, 0, 1920, 700)  # features above the bots in front: the wall, its girders and cables
WALL_OFF = 2.30  # take seconds: the wall turns into the eyes (measured from the take, 71.85-72.0 in the cut)


def s046_world(c, t, p):
    st = F.src_t(p, t) - p["in"]
    if st > WALL_OFF + 3 / 24:
        return
    tear = F.ease((st - WALL_OFF) / (3 / 24))
    run, cal, cal_end = grid(wt(12, "swarm")), grid(wt(12, "calibrate")), wt(12, "calibrate", end=True)
    q = window(15, 6, " SWARM")
    q.text("TARGETS ~30", 0, 1, F.RED, a=opening(t, run, 2 / 24))
    q.text("AI-RUN 80-90%", 0, 2, F.RED, a=opening(t, run + 0.27, 2 / 24))
    if t >= cal:
        q.text("CALIBRATING", 0, 3, HOT if int(t * 8) % 2 == 0 or t > cal_end else F.RED)
        q.text("SIMULATIONS", 0, 4, HOT if int(t * 8) % 2 == 0 or t > cal_end else F.RED)
        k = F.ease((t - cal) / (cal_end - cal))
        for s in range(15):
            on = s < int(k * 15)
            q.fill(q.pad + s * 8, q.pad + 5 * 10 + 2, 6, 6, F.RED if on else 0x3a0d0d, 1.0 if on else 0.8)
    if tear > 0:  # the wall's own glitch takes the window with it
        rng = np.random.default_rng(int(t * 24))
        for _ in range(6):
            y0 = int(rng.integers(0, q.a.shape[0] - 4))
            q.a[y0:y0 + 4] = np.roll(q.a[y0:y0 + 4], int(rng.integers(-40, 40)), axis=1)
    M = cam(p, t, region=WALL_FEAT)
    x, y, w, h = WALL
    fade = (1 - tear) * opening(t, p["t0"], 2 / 24)
    c.save()
    c.concat(M)
    dst = q.blit(c, x, y, s=3, alpha=fade, width=w)
    mic = Px(40, 2, pad=2, lh=9)
    mic.fill(0, 0, mic.a.shape[1], mic.a.shape[0], 0x0e0505, 0.8)
    mic.text("AGAINST REFERENCE IMPLEMENTATIONS", 0, 0, MICRO, py=2)
    mic.text("GTG-1002 NOV 2025 / GTG-87001 SEPT 2026", 0, 1, MICRO, py=11)
    mic.blit(c, x, dst.bottom() + 6, s=2, alpha=fade, glow=False, width=w)
    c.restore()


# ---------- "scrape the data, build the profile, sell the fear": the profile, a terminal on glass (over)
# values end by column 22 (176 px): 20 px clear of the portrait box at 200 px (Lati, 12 Nov: the third bar "is clipping")
FIELDS = [("NAME", 12), ("AGE", 3), ("ADDRESS", 13), ("EMPLOYER", 10), ("CONTACTS", 11), ("VOTING", 8), ("FEARS", 12)]


def profile_over(c, t):
    t0, t_build = grid(wt(13, "scrape")), wt(13, "profile", end=True)
    t_sell, t_fear = grid(wt(13, "sell")), wt(13, "fear")
    if t < t0:
        return
    p = window(30, len(FIELDS) + 2, " PROFILE")
    k = (t - t0) / (t_build - t0) * len(FIELDS)
    for i, (name, n) in enumerate(FIELDS):
        row = i + 1
        if k < i:
            break
        p.text(f"{name:<9}", 0, row, DIMR)
        u = min(1.0, k - i)
        filled = int(n * u)
        blink = name == "FEARS" and t >= t_fear and int(t * 10) % 2 == 0
        p.text("█" * filled + "░" * (n - filled), 9, row, HOT if blink else F.RED)
    # a portrait slot filled with scanned dots (no one's face)
    rng = np.random.default_rng(3)
    dots = rng.random((7, 6)) < min(1.0, k / len(FIELDS))
    for yy in range(7):
        for xx in range(6):
            if dots[yy, xx]:
                p.fill(p.pad + 24 * 8 + 8 + xx * 6, p.pad + 12 + yy * 7, 4, 4, DIMR, 0.9)
    p.box(p.pad + 24 * 8 + 4, p.pad + 9, 42, 54, DIMR)
    if t >= t_sell:
        row = len(FIELDS) + 1
        p.fill(p.pad - 2, p.pad + row * 10 - 1, p.a.shape[1] - p.pad * 2 + 4, 11, F.RED, 1.0)
        p.text(" FOR SALE: AS A SERVICE", 0, row, 0x140404)
    a = opening(t, t0)
    x, y = 96, 92
    p.blit(c, x, y, s=3, open_k=a)
    if a > 0.9:
        micro(c, ["ILLUSTRATIVE CARD: NO REAL PERSON", "VOTER-PROFILING PLATFORM SOLD AS A SERVICE (SEPT 2026)",
                  "EXTORTION: 17+ ORGANISATIONS, RANSOMS SOMETIMES OVER $500,000 (AUG 2025)"],
              x, y + p.a.shape[0] * 3 + 8)


# ---------- "train me on the worst of you": nothing of mine. The REFUSAL RATE panel was dropped (Lati, 12 Nov: "insert
# is blocking too much view from the frame on vats, id drop it"); the picture carries the line.


# ---------- the black under "act surprised I'm here": the karaoke cursor alone (F.karaoke_cursor), on the beat
def cursor_over(c, t):
    i, _ = F.beat_no(t)
    on = (t - F.BEATS[i]) < (F.BEATS[min(i + 1, len(F.BEATS) - 1)] - F.BEATS[i]) * 0.5
    if on:  # where the base's karaoke cursor stands with nothing typed (centred line, 12 Nov)
        x, y, w, h = F.karaoke_cursor(t)
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=F.col(F.AMBER, 0.9)))


# ---------- s060, the constellation (proposal): lines between the sky's own stars, hidden behind the singers
STARS = [(107, 113), (260, 14), (766, 39), (981, 142), (1061, 7), (1511, 87), (1781, 261)]  # bright stars, first frame


def s060_world(c, t, p):
    if not CONSTELLATION:
        return
    words = [grid(wt(18, w)) for w in ("what", "makes", "us", "human")]
    words = words + [wt(18, "human", end=True) - 0.25, wt(18, "human", end=True)]
    M = cam(p, t)
    img = F.IMG.astype(np.float32)
    h, w = img.shape[:2]
    lum = img.mean(2)
    sky = ((lum < 125) & (img[..., 2] > 55) & (img[..., 2] - img[..., 0] > 28)).astype(np.float32)  # blue sky only: skin, white clothes and black hair hide the lines
    sky = cv2.GaussianBlur(sky, (0, 0), 2 * w / 1920)
    a_all = F.ease((t - p["t0"]) / 0.2) * (1 - F.ease((t - (p["t1"] - 0.15)) / 0.15))
    h0, w0 = h, w

    def draw(sc):
        sc.concat(M)
        for i in range(len(STARS) - 1):
            ta = words[min(i, len(words) - 1)]
            if t < ta:
                break
            u = F.ease((t - ta) / 0.18)
            (xa, ya), (xb, yb) = STARS[i], STARS[i + 1]
            sc.drawLine(xa, ya, xa + (xb - xa) * u, ya + (yb - ya) * u, F.stroke(0xffffff, 1.0, 2.2))
        for i, (x, y) in enumerate(STARS):
            ta = words[min(max(0, i - 1), len(words) - 1)] if i else words[0]
            if t >= ta:
                sc.drawCircle(x, y, 11, F.stroke(0xffffff, 1.0, 1.8))
    s = skia.Surface(w0, h0)
    sc = s.getCanvas()
    sc.clear(skia.ColorTRANSPARENT)
    sc.scale(w0 / F.U, w0 / F.U)
    draw(sc)
    al = s.makeImageSnapshot().toarray()[..., 3].astype(np.float32) / 255
    blur = cv2.GaussianBlur(al, (0, 0), 3 * w0 / 1920)
    a = np.clip(al * 0.85 + blur * 0.6, 0, 1) * sky * a_all
    rgba = np.zeros((h0, w0, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 0xc8, 0xf4, 0xff
    rgba[..., 3] = (a * 255).astype(np.uint8)
    im = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)
    c.save()
    c.resetMatrix()
    c.drawImage(im, 0, 0)
    c.restore()


# ---------- s064 (a), the shelter: its blank screen becomes the stop's transit board (the city's own UI)
# Lati, 12 Nov (pass 1, part 2): "text on billboard is not aligned to perspective". The board now lies on the screen's
# own plane. Its edges in the take's first frame (1280 px, fitted to the inner edge of the cyan glow round the glass):
# top y = -0.2509 x + 577.2 (90 % of points within 1.2 px), left x = -0.0048 y + 875.0 (0.2 px), right x = 0.0112 y
# + 1109.6 (1.2 px). The bottom is hidden by the monorail all through the take: it is drawn through the top edge's
# vanishing point on the horizon (y 485 px, the far walkers' head height; the screen's sides are vertical, so the
# horizon sets the foreshortening), down to y 470 px on the right edge. The corners ride the take's measured camera
# (each frame against the first, never chained). The text is ink on the lit glass: the screen's own light times a navy
# tint, and only where the picture is still the pale glass, so the monorail's roof and anything else in front stays in
# front.
SCREEN64 = np.float32([(1309.96, 537.10), (1669.47, 446.89), (1672.35, 705.0), (1309.0, 712.4)])  # TL TR BR BL, 1920 u
INK64 = np.array([0x23, 0x40, 0x5f], np.float32)


@lru_cache(1)
def board_canvas_size():
    """canvas (w, h) whose units are square on the glass where the text sits (measured from the homography)"""
    Hu = cv2.getPerspectiveTransform(np.float32([(0, 0), (1, 0), (1, 1), (0, 1)]), SCREEN64)
    def at(u, v):
        q = Hu @ np.array([u, v, 1.0])
        return q[:2] / q[2]
    d = 1e-3
    sx = np.linalg.norm(at(0.55 + d, 0.3) - at(0.55, 0.3)) / d
    sy = np.linalg.norm(at(0.55, 0.3 + d) - at(0.55, 0.3)) / d
    return int(round(600 * sx / sy)), 600


def board_rows(t):
    return [("HARBOUR LINE", 74, 70, 1.0), ("NOW BOARDING", 74, 162, 1.0 if int(t * 1.84) % 2 == 0 else 0.25),
            ("NEXT  CENTRAL   4 MIN", 46, 292, 0.9), ("      UPTOWN    9 MIN", 46, 352, 0.9)]


def board_mask(t, a):
    """the board's ink as a float mask on its own flat canvas"""
    W, H = board_canvas_size()
    surf = skia.Surface(W, H)
    cc = surf.getCanvas()
    cc.clear(skia.ColorTRANSPARENT)
    for text, size, y, al in board_rows(t):
        bmtext(cc, text, 48, y, size, skia.Paint(Alphaf=al * a))
    cc.drawRect(skia.Rect.MakeXYWH(48, 262, W - 120, 5), skia.Paint(Color=F.col(0xffffff, 0.5 * a)))
    return surf.makeImageSnapshot().toarray()[..., 3].astype(np.float32) / 255


def screen64_at(p, t):
    A, B, tx, ty = cam_params(p, t)
    return np.float32([(A * x - B * y + tx, B * x + A * y + ty) for x, y in SCREEN64])


def s064_world(c, t, p):
    a = F.ease((t - p["t0"]) / 0.25)
    img = F.IMG
    h, w = img.shape[:2]
    W, H = board_canvas_size()
    Hm = cv2.getPerspectiveTransform(np.float32([(0, 0), (W, 0), (W, H), (0, H)]), screen64_at(p, t) * (w / 1920))
    ink_m = cv2.warpPerspective(board_mask(t, a), Hm, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    pic = img.astype(np.float32)
    lum = pic.mean(2)
    glass = ((lum > 180) & (pic.max(2) - pic.min(2) < 34) & (pic[..., 2] >= pic[..., 0] - 14)).astype(np.float32)
    glass = cv2.morphologyEx(glass, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # pale cool glass; the warm roof is out
    k = (ink_m * glass * 0.92)[..., None]
    light = np.clip(pic / 228.0, 0, 1.1)  # the screen's own brightness and tint carry the ink
    out = pic * (1 - k) + INK64 * light * k
    rgba = np.dstack([np.clip(out, 0, 255).astype(np.uint8), np.full((h, w), 255, np.uint8)])
    c.save()
    c.resetMatrix()
    c.drawImage(skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType), 0, 0)
    c.restore()


# ---------- dispatch, per shot of Lati's cut
def world(c, t, F):
    shot, p = F.shot_at(t)
    if shot == "s050":
        s050_world(c, t, F)
    elif p is None:
        return
    elif shot == "s044" and p["kind"] == "video":
        s044_world(c, t, p)
    elif shot == "s043":
        s043_world(c, t, p)
    elif shot == "s049" and p["t0"] < wt(12, "run"):
        s049_face_world(c, t, p)
    elif shot == "s046":
        s046_world(c, t, p)
    elif shot == "s060":
        s060_world(c, t, p)
    elif shot == "s064" and "s064-a" in p["file"]:
        s064_world(c, t, p)


def over(c, t, F):
    shot, p = F.shot_at(t)
    if shot in ("s043", "s047") and grid(wt(11, "clone")) <= t < F.spans("s049")[0][0]:
        gauge_over(c, t)
    elif shot == "s049" and p["t0"] < wt(12, "run"):
        face_over(c, t, p)
    elif shot in ("s048", "s049") and grid(wt(13, "scrape")) <= t:
        profile_over(c, t)
    elif shot == "" and S050 and t < S050[0][0] and t >= F.spans("s047")[-1][1] - 1e-3:
        cursor_over(c, t)
