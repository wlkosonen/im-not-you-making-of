"""Section A, the opening and the bridge (0:00-0:43.92): the title, verse 1's sourced cases, the radar, the servers.

What plays is Lati's cut (F.cut()), not the board: each shot's graphic is dispatched with F.shot_at(t) and placed from
the picture itself. Graphics on the film's own screens and projections go in world() (they take the place pulse with
the picture); the title and the LOAD readout hold still in over(). Lyrics only in the karaoke line (Lati, 12 Nov).
Every graphic is a pure function of song time and the frame.

  s006  the title, bridge-UI style (over): "I'M NOT YOU" typed in phosphor between cyan brackets, on the downbeat
  s009, s010  line 0, a holo spec sheet beside the orb: a predicted protein fold (AlphaFold2)
  s011  line 1 (it plays just before the line), the second monitor wakes with a chart: missense variants scored
        (AlphaMissense)
  s017  line 3, the lightbox: a scan film, a box closes on the shadow, FLAGGED, a human reader decides (Mia)
  s027  in the cut under line 4: the mech head's schematic drafting itself; VISOR ONLINE when the take's visor lights
  s021  lines 4 and 5 on the white screen, behind her head: attempted speech becoming words (UCSF, Ann Johnson), then
        sperm-whale codas (Project CETI)
  s023  the radar tags (approved 12 Nov, Kiln's code, unchanged: tracks() and s023())
  servers (s025, s029, s026 plates, s025 clip)  line 7: LOAD climbing on the beats, maxing out on "feed" (over)

Facts: production/research/forms.md (pass 1, its "shown as / limits" respected) and research/pass-1/. Text that is
drawn rather than measured (the fold, the scan, the clicks) says ILLUSTRATIVE in micro-type. Words that are the
fiction's own (LOAD, MAX, VISOR, the title) need no source.

Tracked surfaces: each take's camera move is measured afresh in every frame against the take's first frame in the cut
(ORB features, a RANSAC similarity), never chained from frame to frame, then smoothed over 5 frames. The picture
occludes the screens' graphics where it is not screen (a brightness mask from the frame itself, every frame).

Kiln wrote s023 (12 Nov); the rest is graphics agent A, 12 Nov 2026. Log: production/edit/agents/opening.md.
"""
import math
import subprocess
import sys
from functools import lru_cache

import cv2
import numpy as np
import skia

import base as F

# ======================================================================================================== s023
# Kiln's approved radar tags (12 Nov), unchanged below: signatures(), tracks(), s023().
"""s023 (board, Lati 10 Nov): "radar: the oncoming swarm's signatures rise from the table, tagged ABLITERATED and
HERETIC; the fleet untagged". The signatures are the take's own lights rising off the holo table: each frame they are
found afresh in the picture (cyan glow around a white core, above the table's rim), never flowed from frame to frame
(film 2's drift lesson); then the finds are linked into tracks over the whole take and smoothed, and each track keeps
one word for its life (12 Nov: per-frame tags flickered between lights).
The fleet seen through the window is grey, not cyan: it stays untagged by construction.
ABLITERATED and HERETIC are real names: ~9,000 "abliterated" and ~7,400 "heretic" models on Hugging Face (research,
forms.md, 7 Nov 2026). Kiln, 12 Nov 2026.
"""

S023 = F.spans("s023")
WORDS = ("ABLITERATED", "HERETIC")


def signatures(img, loose=False):
    """[(x, y, strength)] in 1920 units: cyan glow peaks with a white core, above the table"""
    h, w = img.shape[:2]
    f = img.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    cy = ((b - r) > 40) & (b > 180) & (g > 130)
    sc = cv2.GaussianBlur(cy.astype(np.float32) * (r + g + b) / 765, (0, 0), 6 * w / 1280)
    mx = cv2.dilate(sc, np.ones((int(41 * w / 1280),) * 2, np.uint8))
    core = cv2.dilate(f.mean(2), np.ones((int(9 * w / 1280),) * 2, np.uint8))
    ys, xs = np.where((sc == mx) & (sc > (0.06 if loose else 0.10)) & (core > (215 if loose else 232)))
    k = 1920 / w
    return [(x * k, y * k, float(sc[y, x])) for x, y in zip(xs, ys) if 0.04 * h < y < 0.76 * h and 0.02 * w < x < 0.98 * w]


@lru_cache(4)
def tracks(file):
    """the take's lights as tracks: found in every frame (never flowed from frame to frame), then linked to the
    nearest light of the next frames, gaps of up to 3 frames bridged, short tracks dropped, positions smoothed over
    5 frames. -> (n_frames, [track: {frame: (x, y)}, ...], the words) (Lati, 12 Nov: "follow the rising light more
    tightly")"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F.ROOT / file), "-vf", "scale=1280:720", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3)
    det = [signatures(im, loose=True) for im in fr]
    live, done = [], []
    for i, ds in enumerate(det):
        free = list(ds)
        for tr in sorted(live, key=lambda tr: -len(tr["pts"])):
            last_i = max(tr["pts"])
            lx, ly = tr["pts"][last_i]
            vx, vy = tr.get("v", (0.0, -8.0))
            px, py = lx + vx * (i - last_i), ly + vy * (i - last_i)  # where it should be now, moving as it moved
            best = min(free, key=lambda d: (d[0] - px) ** 2 + (d[1] - py) ** 2, default=None)
            if best and (best[0] - px) ** 2 + (best[1] - py) ** 2 < 70 ** 2:
                tr["v"] = ((best[0] - lx) / (i - last_i), (best[1] - ly) / (i - last_i))
                tr["pts"][i] = best[:2]
                tr["s"].append(best[2])
                free.remove(best)
        for tr in [tr for tr in live if i - max(tr["pts"]) > 3]:
            live.remove(tr)
            done.append(tr)
        live += [{"pts": {i: d[:2]}, "s": [d[2]]} for d in free]
    done += live
    out = []
    for tr in done:
        ks = sorted(tr["pts"])
        if len(ks) < 10 or np.mean(tr["s"]) < 0.08:
            continue
        idx = np.arange(ks[0], ks[-1] + 1)
        xs = np.interp(idx, ks, [tr["pts"][k][0] for k in ks])
        ys = np.interp(idx, ks, [tr["pts"][k][1] for k in ks])
        ker = np.ones(5) / 5
        xs = np.convolve(np.pad(xs, 2, mode="edge"), ker, "valid")
        ys = np.convolve(np.pad(ys, 2, mode="edge"), ker, "valid")
        out.append({int(k): (float(x), float(y)) for k, x, y in zip(idx, xs, ys)})
    out.sort(key=lambda tr: min(tr))  # by birth: the words alternate in the order the lights rise
    out = sorted(out, key=lambda tr: -len(tr))[:8]
    out.sort(key=lambda tr: min(tr))
    return len(fr), out, [WORDS[i % 2] for i in range(len(out))]


def s023(c, t, F):
    a0, a1, p = next(s for s in S023 if s[0] <= t < s[1])
    fade = F.ease((t - a0) / 0.25) * (1 - F.ease((t - (a1 - 0.12)) / 0.12))
    n, trs, words = tracks(p["file"])
    fi = F.src_t(p, t) * 24
    i0 = int(np.floor(fi))
    for tr, word in zip(trs, words):
        if i0 not in tr or i0 + 1 not in tr:
            continue
        u = fi - i0
        x = tr[i0][0] * (1 - u) + tr[i0 + 1][0] * u
        y = tr[i0][1] * (1 - u) + tr[i0 + 1][1] * u
        life = min(i0 - min(tr), max(tr) - i0)
        a = fade * F.ease(life / 4)
        side = -1 if x < 960 else 1
        blink = 0.75 + 0.25 * (int(t * 12) % 2)

        def draw():
            F.brackets(c, x - 32, y - 32, 64, 64, F.RED, a * blink, arm=0.3, sw=2.8)
            F.tag(c, x + side * 32, y - 32, word, F.RED, a, dx=side * 50, dy=-46, size=26)
        F.glow_draw(c, draw, blur=5, amount=0.55)


# ======================================================================================================== the clock
END = (F.spans("s031") or [(43.92,)])[0][0]  # the section ends where the launch (section B) begins
SERVERS = sorted((a, b, p) for sh in ("s025", "s026", "s029") for a, b, p in F.spans(sh) if b <= END + 1e-3)
SHOTS = ("s006", "s009", "s010", "s011", "s017", "s021", "s023", "s027")
RANGES = sorted([(a, b) for sh in SHOTS for a, b, _ in F.spans(sh) if b <= END + 1e-3] + [(a, b) for a, b, _ in SERVERS])
IMPACTS = []  # "feed" proposed against: see the log (12 Nov)
CUTS = {}


def word_t(line, w, n=0, end=False):
    """a sung word's onset (or end) from the snapped words, so graphics follow the voice, not hard-coded times"""
    ws = [x for x in F.WORDS if x.get("line") == line and x["w"].lower().strip(".,!?—'") == w]
    x = ws[min(n, len(ws) - 1)]
    return (x.get("t1") or x["t0"]) if end else x["t0"]


def beats(a, b):
    return [x for x in F.BEATS if a - 1e-3 <= x < b]


def eighths(a, b):
    """the beats and the half-beats between them"""
    bs = F.BEATS
    out = sorted(set(bs) | {(x + y) / 2 for x, y in zip(bs, bs[1:])})
    return [x for x in out if a - 1e-3 <= x < b]


def on(t, at, dur=0.18):
    """0..1 easing in from `at`"""
    return F.ease((t - at) / dur)


def clamp(x, a=0.0, b=1.0):
    return min(b, max(a, x))


# ======================================================================================================== measuring the picture
def _edit():
    p = str(F.ROOT / "production/tools/edit")
    if p not in sys.path:
        sys.path.insert(0, p)
    import render
    return render


def _key(p):
    return (p["file"], round(p["t0"], 3), round(p["t1"], 3), round(p.get("in") or 0, 3), p.get("speed") or 1)


@lru_cache(16)
def motion(key, excl=(), only=None):
    """the camera move of one piece of the cut: for each of its song frames, a similarity (a, b, tx, ty) mapping the
    piece's first frame to this frame, in 1920 units. Each frame is matched to the first frame afresh (ORB features,
    RANSAC), never to its neighbour, so nothing accumulates; then smoothed over 5 frames. `excl`: rectangles (1920
    units) of things that move by themselves (people, hands), left out of the matching; `only`: match inside this
    rectangle alone (the surface's own neighbourhood: a dolly moves near and far things differently).
    -> (first song frame, params (n, 4), worst inlier error in 1920 units per frame)"""
    render = _edit()
    p = next(q for q in F.cut() if _key(q) == key)
    k0, k1 = render.fr(p["t0"]), render.fr(p["t1"])
    fr = np.frombuffer(render.frames(p, k0, k1), np.uint8).reshape(-1, render.H, render.W, 3)
    s = 1920 / render.W
    gray = [cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in fr]
    mask = np.full(gray[0].shape, 255, np.uint8)
    if only:
        mask[:] = 0
        x0, y0, x1, y1 = only
        mask[int(y0 / s):int(y1 / s), int(x0 / s):int(x1 / s)] = 255
    for x0, y0, x1, y1 in excl:
        mask[int(y0 / s):int(y1 / s), int(x0 / s):int(x1 / s)] = 0
    orb = cv2.ORB_create(4000)
    kr, dr = orb.detectAndCompute(gray[0], mask)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    par, err = [], []
    for g in gray:
        kc, dc = orb.detectAndCompute(g, mask)
        M = None
        if dc is not None and len(kc) > 8:
            m = bf.match(dr, dc)
            src = np.float32([kr[x.queryIdx].pt for x in m])
            dst = np.float32([kc[x.trainIdx].pt for x in m])
            M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
        if M is None:
            par.append(par[-1] if par else (1.0, 0.0, 0.0, 0.0))
            err.append(float("nan"))
            continue
        res = np.linalg.norm(src @ M[:, :2].T + M[:, 2] - dst, axis=1)[inl.ravel() > 0]
        par.append((M[0, 0], M[1, 0], M[0, 2] * s, M[1, 2] * s))
        err.append(float(np.percentile(res, 90)) * s if len(res) else float("nan"))
    par = np.array(par)
    ker = np.ones(5) / 5
    par = np.stack([np.convolve(np.pad(par[:, i], 2, mode="edge"), ker, "valid") for i in range(4)], 1)
    return k0, par, err


def follow(c, t, p, sid):
    """concat the camera move at t onto the canvas: draw in the piece's first-frame coordinates after this"""
    k0, par, _ = motion(_key(p), tuple(EXCL.get(sid, ())), ONLY.get(sid))
    i = int(clamp(round(t * 24) - k0, 0, len(par) - 1))
    a, b, tx, ty = par[i]
    c.concat(skia.Matrix.MakeAll(a, -b, tx, b, a, ty, 0, 0, 1))


def masked(c, draw, mask):
    """draw into a layer the size of the frame, keep it only where mask (h, w, 0..1) is 1: the picture's own things
    (a head, a hand) stay in front of the screen they stand before"""
    h, w = F.IMG.shape[:2]
    arr = np.zeros((h, w, 4), np.uint8)
    surf = skia.Surface(arr)
    cc = surf.getCanvas()
    cc.scale(w / F.U, w / F.U)
    draw(cc)
    surf.flushAndSubmit()
    arr = surf.makeImageSnapshot().toarray()
    arr[..., 3] = (arr[..., 3] * mask).astype(np.uint8)
    img = skia.Image.fromarray(arr, colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
    c.save()
    c.scale(F.U / w, F.U / w)
    c.drawImage(img, 0, 0)
    c.restore()


def screen_mask(lo=150, hi=205):
    """where the frame is lit screen: 0 on hair, hands, heads, 1 on the glowing panel"""
    lum = F.IMG.astype(np.float32).mean(2)
    m = np.clip((lum - lo) / (hi - lo), 0, 1)
    return cv2.GaussianBlur(m, (0, 0), 1.0)


@lru_cache(1)
def vocal_energy():
    """the vocal stem's loudness, summed: 100 values a second, cumulative"""
    x, sr = F.vocal()
    hop = sr // 100
    n = len(x) // hop
    e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))
    return np.concatenate([[0.0], np.cumsum(e)])


def voiced(a, b, t):
    """0..1: how much of the voice between a and b has been sung by t (typing at the pace of the voice)"""
    cs = vocal_energy()
    i = lambda x: int(clamp(x * 100, 0, len(cs) - 1))  # noqa: E731
    return clamp((cs[i(t)] - cs[i(a)]) / max(1e-9, cs[i(b)] - cs[i(a)]))


# ======================================================================================================== drawing kit
def text(c, s, x, y, size=18, color=F.CYAN, a=1.0, bold=True, align="left"):
    return F.hud_text(c, s, x, y, size=size, color=color, a=a, bold=bold, align=align)


def micro(c, s, x, y, color=F.CYAN, a=1.0, size=11):
    return F.hud_text(c, s, x, y, size=size, color=color, a=a * 0.75, bold=False)


def scanlines(c, x, y, w, h, color, a, step=4):
    p = F.stroke(color, a, 1.0)
    for yy in np.arange(y + 2, y + h, step):
        c.drawLine(x, yy, x + w, yy, p)


def holo(c, x, y, w, h, a, t):
    """a holo panel: dark cyan glass, scanlines, a frame and corner brackets, a faint flicker"""
    fl = 0.92 + 0.08 * math.sin(t * 61.0) * math.sin(t * 17.0)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=F.col(0x04141c, 0.74 * a)))
    scanlines(c, x, y, w, h, F.CYAN, 0.05 * a)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), F.stroke(F.CYAN, 0.45 * a * fl, 1.4))
    F.brackets(c, x - 6, y - 6, w + 12, h + 12, F.CYAN, 0.95 * a * fl, arm=0.07, sw=2.4)


# ======================================================================================================== s006: the title
TITLE = "I'M NOT YOU"


def title(c, t):
    """over the fleet's arrival: brackets open on the downbeat, the title types itself in phosphor, holds through the
    bar, and the panel collapses to a line into the cut (a CRT switching off)"""
    a0, a1, _ = next(s for s in F.spans("s006") if s[0] <= t < s[1])
    tb = next((d for d in F.DOWNS if a0 - 1e-3 <= d < a1), a0)
    if t < tb:
        return
    sy = max(0.015, on(t, tb, 0.2)) * (1 - F.ease((t - (a1 - 0.2)) / 0.18))
    if sy <= 0.01:
        return
    px, rows = 9, 13
    tw = (int(F._font(rows * 1.15).measureText(TITLE)) + 4) * px
    th = (rows + 4) * px
    cx, cy = 960, 430
    hw, hh = tw / 2 + 110, th / 2 + 46
    c.save()
    c.translate(cx, cy)
    c.scale(1, sy)
    c.translate(-cx, -cy)
    c.drawRect(skia.Rect.MakeLTRB(cx - hw, cy - hh, cx + hw, cy + hh), skia.Paint(Color=F.col(0x000000, 0.5)))

    def frame():
        F.brackets(c, cx - hw, cy - hh, 2 * hw, 2 * hh, F.CYAN, 0.95, arm=0.06, sw=2.6)
        y = cy + hh - 16
        c.drawLine(cx - hw + 40, y, cx + hw - 40, y, F.stroke(F.CYAN, 0.5, 1.4))
        for i, x in enumerate(np.arange(cx - hw + 40, cx + hw - 39, 32)):
            c.drawLine(x, y, x, y - (10 if i % 4 == 0 else 5), F.stroke(F.CYAN, 0.5, 1.4))
        c.drawLine(cx - hw + 40, cy - hh + 16, cx - hw + 160, cy - hh + 16, F.stroke(F.CYAN, 0.7, 2))
        c.drawLine(cx + hw - 160, cy - hh + 16, cx + hw - 40, cy - hh + 16, F.stroke(F.CYAN, 0.7, 2))
    F.glow_draw(c, frame, blur=5, amount=0.6)
    n = int(len(TITLE) * clamp((t - tb - 0.12) / 0.5))
    x, y = cx - tw / 2 - px * 3, cy - th / 2 - 8
    w = F.crt_text(c, TITLE[:n], x, y, px=px, rows=rows, color=F.AMBER)
    if n < len(TITLE) or int(t * 2.5) % 2 == 0:
        c.drawRect(skia.Rect.MakeXYWH(x + w + 6, y + 2 * px, px * 5, rows * px), skia.Paint(Color=F.col(F.AMBER, 0.85)))
    c.restore()


# ======================================================================================================== s009, s010: line 0
# AlphaFold2 (Google DeepMind): KVA press release 9 Oct 2024 (Nobel, Chemistry, Hassabis and Jumper "for protein
# structure prediction"); Nature 15 Jul 2021 ("around 100,000 unique proteins" solved by experiment); DeepMind 28 Jul
# 2022 (database "over 200 million structures", predicted). Shown as: another system, not Claude; predicted, not seen.
_n = 56
_i = np.arange(_n, dtype=np.float64)
CHAIN = np.stack([(_i - _n / 2) * 4.6, 8 * np.sin(_i * 0.7), np.zeros(_n)], 1)
_lat = 0.95 * np.sin(_i * 0.23 + 0.4)
FOLDED = np.stack([62 * np.cos(_i * 0.52) * np.cos(_lat) + 14 * np.cos(_i * 1.9),
                   62 * np.sin(_lat) + 14 * np.sin(_i * 1.9),
                   62 * np.sin(_i * 0.52) * np.cos(_lat)], 1)
SPEC = {"s009": (120, 66, 440, 380), "s010": (110, 66, 440, 380)}  # the panel in each take's first frame (1920 units)


def fold(c, cx, cy, f, k, rot, a):
    pts = (CHAIN * (1 - f) + FOLDED * f) * 1.45
    ca, sa = math.cos(rot), math.sin(rot)
    x = pts[:, 0] * ca + pts[:, 2] * sa
    z = -pts[:, 0] * sa + pts[:, 2] * ca
    y = pts[:, 1]
    m = int(_n * k)
    for j in range(1, m):
        d = clamp(0.55 + (z[j] + z[j - 1]) / 260)
        col = F.AMBER if j in (11, 12, 13, 37, 38) else F.CYAN  # a few residues lit like a picked site (drawn, not data)
        c.drawLine(cx + x[j - 1], cy + y[j - 1], cx + x[j], cy + y[j], F.stroke(col, a * d, 3.2))
    for j in range(0, m, 4):
        c.drawCircle(cx + x[j], cy + y[j], 2.6, skia.Paint(Color=F.col(F.WHITE, a * 0.8), AntiAlias=True))


def spec_sheet(c, t, sid, p):
    x, y, w, h = SPEC[sid]
    t_open = F.spans("s009")[0][0] if F.spans("s009") else p["t0"]
    t_fold, t_shape = word_t(0, "fold"), word_t(0, "shape", end=True)
    t_end = F.spans("s010")[-1][1] if F.spans("s010") else p["t1"]
    a = on(t, t_open, 0.15) * (1 - F.ease((t - (t_end - 0.1)) / 0.1))
    if a <= 0:
        return
    rows = eighths(t_open + 0.3, 30)[:4]

    def draw():
        holo(c, x, y, w, h, a, t)
        text(c, "STRUCTURE PREDICTION", x + 18, y + 32, size=19, a=a)
        c.drawLine(x + 18, y + 42, x + w - 18, y + 42, F.stroke(F.CYAN, 0.5 * a, 1.2))
        f = F.ease((t - t_fold) / max(0.3, t_shape - t_fold))
        fold(c, x + w / 2, y + 140, f, on(t, t_open, 0.35), 0.25 + 1.1 * f + 0.6 * max(0.0, t - t_fold), a)
        text(c, "PREDICTED" if f > 0.97 else "FOLDING", x + w - 18, y + 72, size=14, a=0.8 * a, align="right")
        lines = [("AlphaFold2 · DeepMind", F.CYAN, 18), ("200,000,000+ predicted", F.AMBER, 21),
                 ("~100,000 solved by experiment", F.CYAN, 16), ("Nobel, Chemistry 2024", F.CYAN, 16)]
        for i, (s, col, size) in enumerate(lines):
            if i < len(rows) and t >= rows[i]:
                text(c, s, x + 18, y + 236 + i * 30, size=size, color=col, a=a * on(t, rows[i], 0.1))
        micro(c, "FOLD: ILLUSTRATIVE · KVA 9 OCT 2024 · NATURE 15 JUL 2021", x + 18, y + h - 12, a=a)
    c.save()
    follow(c, t, p, sid)
    F.glow_draw(c, draw, blur=4, amount=0.45)
    c.restore()


# ======================================================================================================== s011: line 1
# AlphaMissense (Google DeepMind, 19 Sep 2023; Science, 22 Sep 2023): "categorised 89% of all 71 million possible
# missense variants"; "only 0.1% have been confirmed by human experts". Not the whole genome; it patches nothing.
SCREEN2 = [(244, 306), (387, 331), (370, 517), (242, 515)]  # the second monitor in s011's first frame (1920 units)


def chart(c, t, p):
    a0 = p["t0"]
    tw = (beats(a0, a0 + 1) or [a0])[0]  # it wakes on the first beat of the shot
    if t < tw:
        return
    loc = skia.Matrix()
    loc.setPolyToPoly([skia.Point(0, 0), skia.Point(260, 0), skia.Point(260, 360), skia.Point(0, 360)],
                      [skia.Point(*q) for q in SCREEN2])
    wake = on(t, tw, 0.12)
    grow = on(t, tw + 0.1, 0.45)

    def draw():
        c.save()
        c.translate(130, 180)
        c.scale(1, max(0.02, wake))
        c.translate(-130, -180)
        c.drawRect(skia.Rect.MakeXYWH(0, 0, 260, 360), skia.Paint(Color=F.col(0x06141c, 0.97)))
        scanlines(c, 0, 0, 260, 360, F.CYAN, 0.07, step=5)
        text(c, "VARIANTS SCORED", 14, 34, size=24)
        c.drawLine(14, 46, 246, 46, F.stroke(F.CYAN, 0.6, 1.5))
        base, top = 250, 76
        for i, (frac, lab, col) in enumerate(((0.89, "CLASSED", F.AMBER), (0.11, "UNCLEAR", F.CYAN))):
            bx = 30 + i * 118
            hgt = (base - top) * frac * grow
            c.drawRect(skia.Rect.MakeLTRB(bx, base - hgt, bx + 84, base), skia.Paint(Color=F.col(col, 0.85)))
            text(c, f"{round(frac * 100 * grow)}%", bx + 42, base - hgt - 8, size=24, color=col, align="center")
            text(c, lab, bx + 42, base + 24, size=17, color=col, align="center")
        c.drawLine(14, base, 246, base, F.stroke(F.CYAN, 0.7, 1.5))
        text(c, "OF 71 M POSSIBLE", 14, 306, size=20, color=F.CYAN)
        text(c, "0.1% CONFIRMED BY EXPERTS", 14, 330, size=14, color=F.CYAN, a=0.9)
        micro(c, "AlphaMissense · DeepMind · 19 Sep 2023", 14, 350, size=12)
        c.restore()
    c.save()
    follow(c, t, p, "s011")
    c.concat(loc)
    draw()
    c.restore()


# ======================================================================================================== s017: line 3
# Mia (Kheiron) as an extra reader: Nature Medicine, 16 Nov 2023 (Hungary, ~25,000 women): "0.7-1.6 additional cancer
# detection per 1,000 cases"; it flagged cases two radiologists had passed and a human reader decided on recall.
# Shown as: a radiologist made every final call, never the machine diagnosing alone. The film on the box is drawn.
# The lightbox stands at an angle to the camera (Lati, 12 Nov, pass 1: "insert on screen is not matching the perspective
# of monitor in front of her"): the film lies on its plane through a homography. The plane's four corners come from its
# edges in s017's first frame (1280x720, fitted to the glow's boundary): left x = 0.00927 y + 197.5, right
# x = 0.01688 y + 630.4, top y = 0.5144 x - 205.5 (inliers within 1.7, 0.5, 0.9 px); the bottom, where the glass meets
# the sill, y = -0.0556 x + 549.8 (read by eye: the sill is as bright as the glass). The top-left corner is above the
# frame. They ride the take's measured camera move (motion(), each frame against the first). The film is
# transmissive: the lightbox's own light times the film, so it takes the box's brightness, tint and sweep.
SCREEN17 = [(294.8, -156.6), (948.6, 179.7), (958.7, 771.5), (303.8, 807.8)]  # TL TR BR BL, 1920 units
# Pass 3 (Lati, 12 Nov: "scan does not fill the screen, it read as ctrlz image on screen"; then Kiln's suggestion, "Lets
# try your suggestion for s017"): the film fills the whole lightbox edge to edge, as a film hangs on a real one, backlit.
FW, FH, LS = 1400, 1000, 1.0  # the film = the lightbox's plane, in its own units (about the box's aspect), 1 px a unit
SPOT = (0.62, 0.50)  # the drawn dense spot, on the plane (u across, v down)


def plane(u, v):
    return u * FW, v * FH


@lru_cache(1)
def film_transmission():
    """an ILLUSTRATIVE mammogram film over the whole box, as the light it lets through (0..1): as on a real film, the
    exposed background is dark grey, tissue is lighter, denser tissue lighter still, the small dense spot brightest.
    The breast lies against the chest wall at the right edge (behind her, the part she isn't reading)."""
    W, H = int(FW * LS), int(FH * LS)
    rng = np.random.default_rng(7)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 1.0, H * 0.47
    r = np.sqrt(((xx - cx) / (W * 0.72)) ** 2 + ((yy - cy) / (H * 0.46)) ** 2)
    body = np.clip((1.0 - r) / 0.05, 0, 1)
    n = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 2.2 * LS)
    n /= n.std() + 1e-6
    n2 = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 22 * LS)
    n2 /= n2.std() + 1e-6
    ang = np.arctan2(yy - cy, xx - cx)  # fibres fan out from the chest wall towards the nipple
    fib = 0.25 * n + 0.35 * np.sin(ang * 30 + n2 * 2.6) + 0.5 * n2
    dense = np.clip(0.42 + 0.09 * fib + 0.30 * np.clip(1 - r, 0, 1) ** 1.3, 0, 1) * body
    sx, sy = SPOT[0] * W, SPOT[1] * H
    d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)
    spot = np.clip(1.3 - d / (13.0 * LS), 0, 1) * (0.88 + 0.12 * np.sin(np.arctan2(yy - sy, xx - sx) * 9))
    skin = np.clip(1 - np.abs(r - 0.985) / 0.02, 0, 1) * 0.12  # the skin line, a faint rim
    v = np.clip(dense + skin + 0.55 * spot, 0, 1)
    base = 0.25 + 0.06 * cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 40)  # base fog
    return np.clip(np.maximum(base, 0.28 + 0.70 * v), 0, 1).astype(np.float32)


def film_overlay(t, b, a):
    """the markings on the film, in its plane: the box closing on the spot, FLAGGED with its reader line, the facts
    bottom left (the near side, clear of her head and gloves, above the lyric band). RGBA, unpremultiplied."""
    arr = np.zeros((int(FH * LS), int(FW * LS), 4), np.uint8)
    surf = skia.Surface(arr)
    cc = surf.getCanvas()
    cc.scale(LS, LS)
    sx, sy = plane(*SPOT)
    text(cc, "R MLO", *plane(0.03, 0.25), size=44, color=F.WHITE, a=0.8 * a)
    k = F.ease((t - b[0]) / max(0.1, b[1] - b[0]))  # from the whole breast to the spot by the second beat
    x0, y0, x1, y1 = plane(0.30, 0.06) + plane(0.97, 0.86)
    bw, bh = (x1 - x0) * (1 - k) + 150 * k, (y1 - y0) * (1 - k) + 150 * k
    bx, by = x0 * (1 - k) + (sx - 75) * k, y0 * (1 - k) + (sy - 75) * k
    locked = t >= b[1]
    F.brackets(cc, bx, by, bw, bh, F.RED if locked else F.AMBER, a, arm=0.28, sw=7)
    if locked and int(t * 12) % 2 == 0:
        cc.drawCircle(sx, sy, 92, F.stroke(F.RED, 0.85 * a, 5))
    fx, fy = plane(0.03, 0.74)
    text(cc, "AI AS AN EXTRA READER", fx, fy, size=46, color=F.AMBER, a=a)
    text(cc, "+0.7-1.6 cancers found per 1,000", fx, fy + 58, size=40, color=F.AMBER, a=a * on(t, b[1], 0.1))
    micro(cc, "Mia · Nature Medicine 16 Nov 2023", fx, fy + 104, color=F.AMBER, a=a, size=30)
    micro(cc, "SCAN: ILLUSTRATIVE", fx, fy + 140, color=F.AMBER, a=a, size=30)
    if t >= b[2]:  # the stamp slams on the downbeat; who decides comes with it
        s = 1 + 0.5 * (1 - F.ease((t - b[2]) / 0.09))
        cc.save()
        cc.translate(*plane(0.27, 0.40))
        cc.rotate(-8)
        cc.scale(s, s)
        f = F._font(120, True)
        sw = f.measureText("FLAGGED")
        cc.drawRect(skia.Rect.MakeXYWH(-sw / 2 - 30, -108, sw + 60, 144), F.stroke(F.RED, 0.95 * a, 9))
        cc.drawRect(skia.Rect.MakeXYWH(-sw / 2 - 42, -120, sw + 84, 168), F.stroke(F.RED, 0.6 * a, 3))
        cc.drawString("FLAGGED", -sw / 2, 0, f, skia.Paint(Color=F.col(F.RED, 0.95 * a), AntiAlias=True))
        cc.restore()
        text(cc, "→ A RADIOLOGIST DECIDES", *plane(0.05, 0.57), size=46, color=F.RED, a=a * on(t, b[2] + 0.06, 0.1))
    surf.flushAndSubmit()
    return surf.makeImageSnapshot().toarray().astype(np.float32) / 255


def screen17_at(t, p):
    """the lightbox's corners at t, in 1920 units: SCREEN17 carried by the take's measured camera move"""
    k0, par, _ = motion(_key(p), tuple(EXCL.get("s017", ())), ONLY.get("s017"))
    i = int(clamp(round(t * 24) - k0, 0, len(par) - 1))
    A, B, tx, ty = par[i]
    return np.float32([(A * x - B * y + tx, B * x + A * y + ty) for x, y in SCREEN17])


def film_homography(t, p, w):
    """film pixels -> output pixels: the film is the whole lightbox plane"""
    src = np.float32([(0, 0), (FW * LS, 0), (FW * LS, FH * LS), (0, FH * LS)])
    return cv2.getPerspectiveTransform(src, screen17_at(t, p) * (w / 1920))


def lightbox(c, t, p):
    a0, a1 = p["t0"], p["t1"]
    bs = beats(a0, a1)  # on s017: 28.02 film up, 28.57 box locks, 29.13 FLAGGED and who decides
    b = (bs + [a1] * 4)[:4]
    a = on(t, a0, 0.08) * (1 - F.ease((t - (a1 - 0.08)) / 0.08))
    if a <= 0:
        return
    img = F.IMG
    h, w = img.shape[:2]
    Hm = film_homography(t, p, w)
    warp = lambda x: cv2.warpPerspective(x, Hm, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)  # noqa: E731
    trans = film_transmission()
    inside = warp(np.ones_like(trans))  # where the film lies
    T = warp(trans)
    ov = film_overlay(t, b, a)
    O = warp(np.dstack([ov[..., :3] * ov[..., 3:], ov[..., 3]]))  # premultiplied, so the edges don't fringe dark
    m = screen_mask(140, 190) * a  # her hair and gloves stay in front
    pic = img.astype(np.float32)
    light = np.clip(pic / 232.0, 0, 1.15)  # the box's own light, normalised: the marks are lit by it too
    k = (inside * m)[..., None]
    out = pic * (1 - k) + pic * T[..., None] * k  # light through the film
    ko = (O[..., 3] * m)[..., None]
    out = out * (1 - ko) + O[..., :3] * 255 * light * m[..., None]
    rgba = np.dstack([np.clip(out, 0, 255).astype(np.uint8), np.full((h, w), 255, np.uint8)])
    c.save()
    c.scale(F.U / w, F.U / w)
    c.drawImage(skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType), 0, 0)
    c.restore()


# ======================================================================================================== s027 (under line 4)
# The mech head in its cradle: the fiction's own schematic, its callouts drafting themselves on the beats; VISOR
# ONLINE the moment the take's visor lights (measured in the frame). No sourced fact: the board's spec sheet.
HEAD = (690, 60, 480, 560)  # around the head, s027's first frame (1920 units)
VISOR = (800, 300, 300, 160)
CALLOUTS = [((955, 410), (1240, 300), "VISOR"), ((870, 232), (560, 150), "SENSOR SLIT"),
            ((640, 380), (330, 330), "CRADLE ARM"), ((960, 640), (1240, 560), "NECK RING")]


def visor_lit():
    h, w = F.IMG.shape[:2]
    k = w / 1920
    x, y, vw, vh = VISOR
    reg = F.IMG[int(y * k):int((y + vh) * k), int(x * k):int((x + vw) * k)].astype(np.float32)
    return float((reg.mean(2) > 200).mean()) > 0.12


def schematic(c, t, p):
    a0, a1 = p["t0"], p["t1"]
    bs = beats(a0, a1)
    a = 1 - F.ease((t - (a1 - 0.08)) / 0.08)
    x, y, w, h = HEAD
    lit = visor_lit()

    def draw(dark=False):
        """dark: the same lines in a soft black first, so thin cyan reads on the cream hangar"""
        K = (lambda col: 0x000000) if dark else (lambda col: col)
        A = 0.45 if dark else 1.0
        W = 3.0 if dark else 0.0
        k = on(t, bs[0] if bs else a0, 0.25)
        F.brackets(c, x, y, w, h, K(F.CYAN), A * 0.95 * a * k, arm=0.12, sw=2.8 + W)
        c.drawLine(x + w / 2, y - 20, x + w / 2, y - 20 + (h + 40) * k, F.stroke(K(F.CYAN), A * 0.45 * a, 1.4 + W))
        c.drawLine(x - 20, y + h * 0.58, x - 20 + (w + 40) * k, y + h * 0.58, F.stroke(K(F.CYAN), A * 0.45 * a, 1.4 + W))
        text(c, "HEAD UNIT · SCHEMATIC", x, y - 14, size=22, color=K(F.CYAN), a=A * a * k)
        for i, ((px, py), (lx, ly), lab) in enumerate(CALLOUTS):
            tb = bs[min(len(bs) - 1, 1 + i // 2)] if len(bs) > 1 else a0
            q = on(t, tb, 0.12)
            if q <= 0:
                continue
            ex, ey = px + (lx - px) * q, py + (ly - py) * q
            col = K(F.AMBER if (lab == "VISOR" and lit) else F.CYAN)
            c.drawCircle(px, py, 6, F.stroke(col, A * a, 2.4 + W))
            c.drawLine(px, py, ex, ey, F.stroke(col, A * 0.9 * a, 2.0 + W))
            if q >= 1:
                right = lx > px
                c.drawLine(lx, ly, lx + (150 if right else -150), ly, F.stroke(col, A * 0.9 * a, 2.0 + W))
                s = "VISOR · ONLINE" if (lab == "VISOR" and lit) else lab
                text(c, s, lx + (6 if right else -6), ly - 9, size=22, color=col, a=A * a, align="left" if right else "right")
    c.save()
    follow(c, t, p, "s027")
    c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(3, 3)))
    draw(dark=True)
    c.restore()
    F.glow_draw(c, draw, blur=4, amount=0.5)
    c.restore()


# ======================================================================================================== s021: lines 4, 5
# Line 4, "give the voiceless words": Ann Johnson, after a brainstem stroke; UCSF / UC Berkeley neuroprosthesis,
# Nature, 23 Aug 2023: median 78 words per minute, median word error rate 25% (Berkeley: "AI-powered"). "Draft the
# brief" has no case (forms.md: stays unillustrated). Line 5, "the pattern no one heard": Project CETI, 7 May 2024:
# nearly 9,000 sperm-whale codas, "rubato" and "ornamentation" found; "the communicative function of many codas
# remains unknown". The coda clicks drawn here are ILLUSTRATIVE, not CETI's data.
INK, INK2 = 0x1d2b53, 0x2f5fa8  # the white screen's own dark blue, like its waveform
PANE = (286, 214)  # the free top-left of the screen above the waveform, s021's first frame (1920 units)
PANE5 = (1376, 196)  # the free top-right
DECODED = ["ATTEMPTED SPEECH → WORDS", "MEDIAN 78 WORDS / MIN", "MEDIAN WORD ERROR 25%"]
CODAS = [[0, 1, 2, 4.6], [0, 1.08, 2.16, 4.97], [0, 1, 2, 4.6, 5.25]]  # click times in units: plain, slower (rubato), +1 (ornament)


def typed(rows, frac):
    total = sum(len(r) for r in rows)
    n = int(round(total * frac))
    out = []
    for r in rows:
        out.append(r[:max(0, n)])
        n -= len(r)
    return out


def screen21(c, t, p):
    a0, a1 = p["t0"], p["t1"]
    l4a, l4b = max(a0, word_t(4, "give")), word_t(4, "words", end=True)
    l5 = (beats(word_t(5, "score") - 0.2, a1) or [a1])[0]  # the codas come in on the beat nearest "score"
    x, y = PANE
    a = 1 - F.ease((t - (a1 - 0.1)) / 0.1)

    def draw(cc):
        x, y = PANE
        cc.save()
        follow(cc, t, p, "s021")
        k4 = 1 - F.ease((t - l5) / 0.15)
        if k4 > 0:
            text(cc, "SPEECH NEUROPROSTHESIS", x, y, size=15, color=INK2, a=a * k4)
            rows = typed(DECODED, voiced(l4a, l4b, t))
            for i, r in enumerate(rows):
                text(cc, r, x, y + 34 + i * 32, size=24, color=INK, a=a * k4)
            last = max([i for i, r in enumerate(rows) if r] or [0])
            if int(t * 5) % 2 == 0 or len(rows[last]) < len(DECODED[last]):
                cw = F._font(24, True).measureText(rows[last])
                cc.drawRect(skia.Rect.MakeXYWH(x + cw + 4, y + 14 + last * 32, 13, 24), skia.Paint(Color=F.col(INK, 0.8 * a * k4)))
            if t >= l4a + 0.3:
                micro(cc, "Ann Johnson, after a stroke · Nature 23 Aug 2023", x, y + 140, color=INK, a=a * k4, size=12)
        if t >= l5:
            x, y = PANE5  # right of her head at its widest in this take (measured: hair reaches x 1358 at most)
            k5 = on(t, l5, 0.12)
            text(cc, "SPERM WHALE CODAS", x, y, size=17, color=INK2, a=a * k5)
            text(cc, "NEARLY 9,000 RECORDED", x, y + 22, size=15, color=INK2, a=a * k5)
            bs = beats(l5, a1 + 1)
            for i, cl in enumerate(CODAS):
                tb = bs[min(i, len(bs) - 1)]
                if t < tb:
                    continue
                ry = y + 78 + i * 46
                lab = ["CODA", "RUBATO", "ORNAMENT"][i]
                text(cc, lab, x, ry - 26, size=15, color=F.RED if i == 2 else INK2, a=a * on(t, tb, 0.08))
                cc.drawLine(x, ry, x + 270, ry, F.stroke(INK2, 0.35 * a, 1.2))
                sweep = clamp((t - tb) / 0.35)
                for j, ct in enumerate(cl):
                    if ct / 5.6 <= sweep:
                        cc.drawRect(skia.Rect.MakeXYWH(x + 4 + ct * 46, ry - 20, 8, 20),
                                    skia.Paint(Color=F.col(F.RED if (i == 2 and j == 4) else INK, a)))
            if len(bs) > 3 and t >= bs[3]:
                text(cc, "MEANING: UNKNOWN", x, y + 228, size=22, color=INK, a=a * on(t, bs[3], 0.1))
            micro(cc, "Project CETI · 7 May 2024", x, y + 248, color=INK, a=a * k5, size=12)
            micro(cc, "CLICKS: ILLUSTRATIVE", x, y + 263, color=INK, a=a * k5, size=12)
        cc.restore()
    masked(c, draw, screen_mask(150, 205))


# ======================================================================================================== servers: line 7
def load(c, t):
    """LOAD as a slim segment strip along the top edge (Lati, 12 Nov, pass 1: the centre gauge was "front and centre,
    blocking the screen and diminishing the impact of motion clips where racks light up with "feed""): quiet cyan, a
    step on each beat of the line, full on "feed" and red, then holding still. Nothing in the aisle; the racks' own
    surge keeps the moment. The fiction's own readout; the numbers are its own."""
    s0 = SERVERS[0][0]
    feed = word_t(7, "feed")
    steps = beats(s0 + 0.05, feed - 0.1)
    lv = 0.34 + 0.12 * sum(on(t, b, 0.1) for b in steps)
    if t >= feed:
        lv = lv + (1 - lv) * on(t, feed, 0.14)
    lv = clamp(lv)
    mx = t >= feed + 0.14
    a = on(t, s0, 0.12) * (1 - F.ease((t - (END - 0.06)) / 0.06))
    x0, x1, y, hgt, n = 330, 1590, 44, 9, 48
    seg = (x1 - x0) / n
    lit = 0.42 if not mx else 0.55 + 0.25 * (1 - on(t, feed + 0.14, 0.4))  # one swell at the max, then quiet
    col = F.RED if mx else F.CYAN
    c.drawRect(skia.Rect.MakeLTRB(0, 0, F.U, 84), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (0, 84)], [F.col(0x000000, 0.3 * a), F.col(0x000000, 0.0)])))

    def draw():
        text(c, "LOAD", x0 - 74, y + hgt, size=17, color=col, a=0.6 * a)
        for i in range(n):
            on_ = (i + 1) / n <= lv + 1e-6
            c.drawRect(skia.Rect.MakeXYWH(x0 + i * seg + 1.5, y, seg - 3, hgt),
                       skia.Paint(Color=F.col(col, (lit if on_ else 0.1) * a)))
        text(c, "MAX" if mx else f"{round(lv * 100)}%", x1 + 16, y + hgt, size=17, color=col, a=0.6 * a)
    F.glow_draw(c, draw, blur=3, amount=0.35)


# ======================================================================================================== dispatch
EXCL = {  # what moves by itself in each take (1920 units of its first frame), left out of the camera measurement
    "s009": [(380, 480, 1560, 1080), (690, 0, 1170, 420)],  # the three avatars, the orb's turning rings
    "s010": [(1050, 200, 1600, 1080), (780, 0, 1150, 900)],  # Eve, the column's rings and the orb
    "s011": [(480, 60, 1300, 1080), (0, 560, 900, 1080), (1350, 500, 1920, 1080)],  # Claudia, the crew
    "s017": [(700, 0, 1400, 1080), (280, 0, 960, 800)],  # Claudia, the lightbox's own sweep
    "s021": [(700, 0, 1400, 1080), (400, 650, 650, 800), (1340, 650, 1500, 800), (300, 380, 1500, 600)],
    "s027": [(1150, 300, 1450, 480), (1300, 560, 1450, 780)],  # the welding sparks, the worker
}
ONLY = {  # where to measure the move: the surface's own neighbourhood (1920 units of the take's first frame)
    "s009": (0, 0, 700, 700),  # the left wall behind the spec sheet
    "s010": (0, 0, 760, 700),
    "s011": (0, 220, 620, 640),  # the bank of monitors and their bezels
}


def world(c, t, F):
    sid, p = F.shot_at(t)
    if sid == "s023":
        s023(c, t, F)
    elif sid in ("s009", "s010"):
        spec_sheet(c, t, sid, p)
    elif sid == "s011":
        chart(c, t, p)
    elif sid == "s017":
        lightbox(c, t, p)
    elif sid == "s027":
        schematic(c, t, p)
    elif sid == "s021":
        screen21(c, t, p)


def over(c, t, F):
    sid, p = F.shot_at(t)
    if sid == "s006":
        title(c, t)
    elif SERVERS and SERVERS[0][0] <= t < END:
        load(c, t)
