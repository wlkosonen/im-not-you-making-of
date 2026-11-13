#!/usr/bin/env python3
# Vendored from the main film (im-not-you-internal, production/tools/gfx/base.py) on 12 Nov 2026, so this repo stands
# alone: the palette, the song clock, the CRT letters, the pixel module and the lyric line are the main film's own.
"""The graphics base for I'm Not You. Kiln owns this file; the section agents build on it (notes/graphics-plan.md).

render.py --gfx calls frame(rgb, t) for every frame of Lati's cut (song time t, the only clock). The order of a frame:

    the picture -> sections' world() (things in the picture: screens, HUDs on glass) -> beat kick and place pulse
    -> grade and grain -> sections' over() (on top of the film, holding still) -> transitions at cuts (SEAMS and
    sections' CUTS: they take the panels with the picture) -> the karaoke line -> impact frames

So a graphic in the world takes the kick with the picture; the lyric line and the HUD readouts in over() hold still.
Sections: production/tools/gfx/sec_<name>.py, each with RANGES = [(t0, t1), ...] and any of picture(img, t, F) -> img
(makes the whole picture, e.g. the pixel zoom), world(c, t, F), over(c, t, F), where c is a Skia canvas in 1920x1080
units at any output size and F this module. F.IMG is the frame's picture while world() runs; F.spans(shot) and
F.src_t() say where a shot plays in Lati's cut and the take's own time, so sections follow his edits.

MODULES switches each finishing part on or off (Lati, 12 Nov: impact frames "with option to switch that off"; "the
line" out unless wanted). Drawing is Skia (media/cache/gfx-venv, shared with film 2): subpixel text and paths.
Lyrics only in the bottom line (Lati, 12 Nov). Text on screen is real: the song's words, sourced facts, this repo.
"""
import importlib
import importlib.util
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

ROOT = Path("/home/shegs/Im not you")  # the main film: its song analysis and media
A = ROOT / "media/song/analysis/parempi"
U = 1920.0  # drawing units: 1920 x 1080 at any output size

MODULES = {"world": True, "kick": True, "pulse": True, "grade": True, "grain": True, "over": True,
           "karaoke": True, "impact": True, "line": False}

# the 80s anime UI palette: phosphor amber for text, cyan for HUDs, clay for Claude's side, red for the bunker and warnings
AMBER, CYAN, CLAY, RED, GREEN, WHITE = (0xffb347, 0x5fe8ff, 0xd97757, 0xff4040, 0x8dff9a, 0xf2f2f2)
MONO = "DejaVu Sans Mono"


def col(rgb, a=1.0):
    return skia.Color(rgb >> 16 & 255, rgb >> 8 & 255, rgb & 255, int(255 * a))


# ---------- the song's clock
_b = json.loads((A / "beats.json").read_text())
BEATS, DOWNS = _b["beats"], _b.get("downbeats", [])
SECTIONS = _b.get("sections", [])
_w = json.loads(((A / "words-snapped.json") if (A / "words-snapped.json").exists() else (A / "words.json")).read_text())
WORDS = [x for x in _w["words"] if x.get("t0") is not None]
LINES = [ln for ln in _w["lines"] if ln.get("t0") is not None]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def pulse(t, times, up=0.07, down=0.07):
    """0..1..0 around the nearest time in times: rises over `up`, falls over `down` (film 2's place pulse)"""
    best = 0.0
    for c in times:
        d = t - c
        if -up <= d <= down:
            best = max(best, 1 - (-d / up if d < 0 else d / down))
    return best


def beat_no(t):
    """(index of the beat at or before t, its 1-4 position in the bar, counted from the last downbeat)"""
    i = max(0, int(np.searchsorted(BEATS, t, side="right")) - 1)
    d = max(0, int(np.searchsorted(DOWNS, BEATS[i] + 1e-3, side="right")) - 1) if DOWNS else 0
    n = int(np.searchsorted(BEATS, BEATS[i] + 1e-3)) - int(np.searchsorted(BEATS, DOWNS[d] - 1e-3)) if DOWNS else 1
    return i, (n - 1) % 4 + 1


# ---------- the finishing (numbers from film 2; places from Lati's cut, notes/graphics-plan.md)
PLACES = [18.04, 35.96, 39.54, 43.92, 56.96, 66.79, 81.17, 94.33, 97.12, 105.00, 109.88, 115.33, 116.79, 128.54,
          141.05, 146.08, 151.83, 163.71, 168.17]
# the song's strong accents (hits.json) that don't already have a change of place: a harder, brighter punch (polish, 12 Nov)
ACCENTS = [5.61, 29.13, 44.69, 69.05, 81.37, 130.78, 135.16]
KICK_SPANS = [(44.69, 57.0), (81.17, 94.3), (116.76, 141.0)]  # choruses and battles only
GRADE = [  # (from, lift, gain (r, g, b), saturation): gentle, one per chapter, to sit the routes together
    (0.0, 0.0, (1.00, 1.00, 1.02), 1.00), (18.0, 0.01, (1.02, 1.00, 0.98), 1.00), (66.8, 0.0, (1.03, 0.98, 0.97), 0.97),
    (128.5, 0.0, (1.00, 0.99, 1.00), 0.96), (163.7, 0.01, (1.00, 1.00, 1.03), 0.98)]


def zoom(img, k):
    if k <= 1e-4:
        return img
    import cv2
    h, w = img.shape[:2]
    m = cv2.getRotationMatrix2D((w / 2, h / 2), 0, 1 + k)
    return cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def finish(img, t):
    k = 0.0
    lift = 0.0
    if MODULES["pulse"]:
        k += 0.04 * ease(pulse(t, PLACES))
        a = ease(pulse(t, ACCENTS, up=0.001, down=0.16))
        k += 0.025 * a
        lift = 0.07 * a
    if MODULES["kick"] and any(a <= t < b for a, b in KICK_SPANS):
        i, pos = beat_no(t)
        if pos in (1, 3):
            k += 0.012 * ease(pulse(t, [BEATS[i]], up=0.001, down=0.12))
    img = zoom(img, k)
    if lift > 0.002:
        img = np.clip(img.astype(np.float32) * (1 + lift) + 255 * lift * 0.3, 0, 255).astype(np.uint8)
    if MODULES["grade"]:
        g = [x for x in GRADE if x[0] <= t][-1]
        f = img.astype(np.float32) / 255
        f = f * np.array(g[2], np.float32) + g[1]
        if g[3] != 1.0:
            y = f.mean(axis=2, keepdims=True)
            f = y + (f - y) * g[3]
        img = (np.clip(f, 0, 1) * 255).astype(np.uint8)
    if MODULES["grain"]:
        rng = np.random.default_rng(int(t * 24))  # a pure function of t: the same frame always gets the same grain
        n = rng.normal(0, 3.2, img.shape[:2]).astype(np.float32)[..., None]
        img = np.clip(img.astype(np.float32) + n, 0, 255).astype(np.uint8)
    return img


# ---------- pixel / CRT voice (the karaoke line, the zoom, terminals): a mono font drawn small, scaled up hard
@lru_cache(64)
def _font(size, bold=False):
    return skia.Font(skia.Typeface(MONO, skia.FontStyle.Bold() if bold else skia.FontStyle.Normal()), size)


def crt_text(c, text, x, y, px=6, rows=9, color=AMBER, alpha=1.0, glow=True):
    """text as blocky phosphor: drawn at `rows` px tall on a tiny surface, scaled by `px` with no smoothing. The
    scanlines are inside the letters only (Lati, 12 Nov: "only crt letters, not scanlines making a lyric line a
    rectangle"): each pixel block's last row is dimmed, so nothing between the letters is touched."""
    if not text:
        return 0
    f = _font(rows * 1.15)
    w = int(f.measureText(text)) + 4
    small = skia.Surface(w, rows + 4)
    sc = small.getCanvas()
    sc.clear(skia.ColorTRANSPARENT)
    sc.drawString(text, 1, rows, f, skia.Paint(Color=skia.ColorWHITE, AntiAlias=False))
    a = small.makeImageSnapshot().toarray()[..., 3] > 0
    m = np.kron(a, np.ones((px, px), np.float32))
    m[px - 1::px, :] *= 0.35  # the scanline gap inside each glyph row
    r, g, b = color >> 16 & 255, color >> 8 & 255, color & 255
    rgba = np.zeros(m.shape + (4,), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = r, g, b
    rgba[..., 3] = (m * 255 * alpha).astype(np.uint8)
    img = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)
    # a dark halo first, so phosphor reads on white smoke as well as on space (12 Nov)
    c.drawImage(img, x, y, skia.SamplingOptions(), skia.Paint(
        ColorFilter=skia.ColorFilters.Blend(col(0x000000, 0.8 * alpha), skia.BlendMode.kSrcIn),
        ImageFilter=skia.ImageFilters.Blur(px * 2.2, px * 2.2)))
    if glow:
        c.drawImage(img, x, y, skia.SamplingOptions(), skia.Paint(Alphaf=0.6, ImageFilter=skia.ImageFilters.Blur(px * 1.4, px * 1.4)))
    c.drawImage(img, x, y)
    return w * px


# ---------- the karaoke line: the sung line typing itself along the bottom, at the pace it's sung
def line_at(t):
    cur = None
    for ln in LINES:
        if ln["t0"] - 0.05 <= t:
            cur = ln
    if not cur:
        return None
    ws = [w for w in WORDS if w.get("line") == cur.get("i", cur.get("line"))] or \
         [w for w in WORDS if cur["t0"] - 0.3 <= w["t0"] <= (cur.get("t1") or cur["t0"] + 6) + 0.3]
    end = max([w.get("t1") or w["t0"] for w in ws] + [cur.get("t1") or cur["t0"]]) + 1.2
    if t > end:
        return None
    return cur, ws, end


KARAOKE_OFF = [(77.5, 78.62), (151.83, 163.71)]  # the black under "act surprised I'm here" (the cursor alone), the pixel zoom


KPX, KROWS = 4, 13  # 13 px letters scaled x4: blocky but readable (9 px made M read as R, 12 Nov)
KY = 1080 - 150  # the bottom row's top
KMAXW = 1920 - 2 * 110  # Lati, 12 Nov: "lyrics get cut off again ... lyrics line needs centering"


def text_w(s):
    """the width crt_text gives s at the lyric size, in 1920 units"""
    return 0 if not s else (int(_font(KROWS * 1.15).measureText(s)) + 4) * KPX


@lru_cache(256)
def k_layout(text):
    """[(start, stop, x, y)] rows of a lyric line: one row centred, or, when too wide, two rows broken where it reads
    best (after a comma or dash, near the middle), each centred, the second on the bottom row"""
    if text_w(text) <= KMAXW:
        return ((0, len(text), (U - text_w(text)) / 2, KY),)
    best = None
    for i, ch in enumerate(text):
        if ch != " ":
            continue
        a, b = text[:i].rstrip(), text[i + 1:]
        wa, wb = text_w(a), text_w(b)
        if max(wa, wb) > KMAXW:
            continue
        score = max(wa, wb) - (260 if a.endswith((",", "—", "-", ";")) else 0) + (120 if b[:1] in "—-" else 0)
        if best is None or score < best[0]:
            best = (score, i, a, b)
    _, i, a, b = best
    up = KY - KROWS * KPX - 18
    return ((0, len(a), (U - text_w(a)) / 2, up), (i + 1, len(text), (U - text_w(b)) / 2, KY))


def k_shown(text, ws, t):
    """how many characters of the line are typed at t: up to the end of each word whose onset has passed, typed across
    the word's own duration"""
    shown, pos = 0, 0
    for w in sorted(ws, key=lambda w: w["t0"]):
        k = text.lower().find(w["w"].lower().strip(".,!?—"), pos)
        if k < 0:
            continue
        if t >= w["t0"]:
            dur = max(0.08, ((w.get("t1") or w["t0"] + 0.3) - w["t0"]))
            shown = max(shown, k + round(len(w["w"]) * min(1.0, (t - w["t0"]) / min(dur, 0.35))))
        pos = k + len(w["w"])
    return shown


def karaoke_cursor(t, text=""):
    """(x, y, w, h) of the cursor after the typed part of `text` (empty: the cursor alone, centred)"""
    rows = k_layout(text) if text else ((0, 0, (U - KPX * 5) / 2, KY),)
    return rows[0][2], rows[0][3] + 2 * KPX, KPX * 5, KROWS * KPX


KARAOKE_OFF_SHOTS = ("s067",)  # Lati, 12 Nov: the terminal faces, "I think the correct way is to drop lurics from this scene"


def _off_shot(t):
    return any(a <= t < b for sh in KARAOKE_OFF_SHOTS for a, b, _ in spans(sh))


def karaoke(c, t):
    if any(a <= t < b for a, b in KARAOKE_OFF):
        return
    got = line_at(t)
    if not got:
        return
    ln, ws, end = got
    if _off_shot(t) or _off_shot(ln["t0"]):  # a line sung over such a shot stays off after its cut too
        return
    text = ln["text"]
    shown = k_shown(text, ws, t)
    fade = 1 - ease((t - (end - 0.4)) / 0.4)
    rows = k_layout(text)
    top = rows[0][3]
    band = skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, top - 60), (0, 1080)], [col(0x000000, 0.0), col(0x000000, 0.35 * fade)]))
    c.drawRect(skia.Rect.MakeXYWH(0, top - 60, U, 1080 - top + 60), band)
    cur = None
    for a, b, x, y in rows:
        if shown <= a and cur is not None:
            break
        part = text[a:min(b, shown)] if shown > a else ""
        wpx = crt_text(c, part, x, y, px=KPX, rows=KROWS, alpha=fade)
        cur = (x + wpx + 4 if part else x, y)
    if cur and (int(t * 2.5) % 2 == 0 or shown < len(text)):  # the cursor
        c.drawRect(skia.Rect.MakeXYWH(cur[0], cur[1] + 2 * KPX, KPX * 5, KROWS * KPX), skia.Paint(Color=col(AMBER, 0.9 * fade)))


# ---------- impact frames (switchable): a two-frame starburst behind a hook word
IMPACTS = []  # (song time, word): each section lists its own in IMPACTS = [...], e.g. (115.6, "ME"); rare, so it lands


def impact(c, t):
    for t0, word in IMPACTS + [x for m in SECS for x in getattr(m, "IMPACTS", [])]:
        if 0 <= t - t0 < 2 / 24:
            p = skia.Path()
            cx, cy, n = 960, 540, 18
            for i in range(n * 2):
                r = 900 if i % 2 == 0 else 380
                a = math.pi * i / n
                (p.moveTo if i == 0 else p.lineTo)(cx + r * math.cos(a), cy + r * math.sin(a))
            p.close()
            c.drawPath(p, skia.Paint(Color=col(WHITE, 0.92), AntiAlias=True))
            f = _font(260, True)
            c.drawString(word, cx - f.measureText(word) / 2, cy + 90, f, skia.Paint(Color=col(0x000000), AntiAlias=True))


# ---------- what plays when: Lati's cut (sections follow his edits instead of hard-coded times)
IMG = None  # the frame's picture while world() runs (RGB, output size): measured afresh each frame, never chained


@lru_cache(1)
def cut():
    import sys
    sys.path.insert(0, str(ROOT / "production/tools/edit"))
    import timeline
    return timeline.flatten(timeline.load())["shots"]


def shot_of(p):
    """the board's shot id of a flattened piece ("s044", "s095q"), from its label or its file name"""
    import re
    m = re.match(r"(s\d{3}q?)", (p.get("label") or "") + " " + Path(p.get("file") or "x").name)
    return m.group(1) if m else ""


def shot_at(t):
    """(shot id, piece) playing at song time t; ("", piece) where the cut is black"""
    for p in cut():
        if p["t0"] <= t < p["t1"]:
            return shot_of(p), p
    return "", None


def spans(shot):
    """[(t0, t1, piece)] where this shot plays in Lati's cut"""
    return [(p["t0"], p["t1"], p) for p in cut() if shot_of(p) == shot]


def src_t(p, t):
    """the take's own time at song time t"""
    return p["in"] + (t - p["start"]) * (p.get("speed") or 1)


# ---------- the vocal stem (oscillators, meters: the voice itself)
@lru_cache(1)
def vocal(sr=22050):
    import subprocess
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(A / "stems/vocals.wav"), "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32), sr


def vocal_wave(t, dur=0.05, n=400):
    x, sr = vocal()
    a = int(t * sr)
    seg = x[max(0, a):max(0, a) + int(dur * sr)]
    return np.interp(np.linspace(0, len(seg) - 1, n), np.arange(len(seg)), seg) if len(seg) > 1 else np.zeros(n)


def vocal_bands(t, bands=16, win=2048):
    """log-spaced band levels 0..1 of the vocal at t (80 Hz-8 kHz)"""
    x, sr = vocal()
    a = int(t * sr) - win // 2
    seg = x[max(0, a):max(0, a) + win]
    if len(seg) < win:
        seg = np.pad(seg, (0, win - len(seg)))
    mag = np.abs(np.fft.rfft(seg * np.hanning(win)))
    f = np.fft.rfftfreq(win, 1 / sr)
    edges = np.geomspace(80, 8000, bands + 1)
    out = np.array([mag[(f >= lo) & (f < hi)].mean() if ((f >= lo) & (f < hi)).any() else 0 for lo, hi in zip(edges, edges[1:])])
    return np.clip(np.log10(1 + out * 4) / 1.6, 0, 1)


# ---------- the HUD kit (vector lines on glass, 80s anime cockpit): Skia, 1920 units
def stroke(color, a=1.0, w=2.0):
    return skia.Paint(Color=col(color, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w)


def glow_draw(c, draw, blur=6, amount=0.7):
    """draw twice: once blurred (phosphor glow), once sharp"""
    c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(blur, blur), Alphaf=amount))
    draw()
    c.restore()
    draw()


def brackets(c, x, y, w, h, color=CYAN, a=1.0, arm=0.22, sw=2.5):
    p = skia.Path()
    ax, ay = w * arm, h * arm
    for (px, py, dx, dy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        p.moveTo(px + dx * ax, py)
        p.lineTo(px, py)
        p.lineTo(px, py + dy * ay)
    c.drawPath(p, stroke(color, a, sw))


def reticle(c, x, y, r, color=CYAN, a=1.0, rot=0.0, ticks=4, sw=2.0):
    c.drawCircle(x, y, r, stroke(color, a, sw))
    for i in range(ticks):
        ang = rot + 2 * math.pi * i / ticks
        c.drawLine(x + math.cos(ang) * r * 0.75, y + math.sin(ang) * r * 0.75,
                   x + math.cos(ang) * r * 1.25, y + math.sin(ang) * r * 1.25, stroke(color, a, sw))


def hud_text(c, text, x, y, size=22, color=CYAN, a=1.0, bold=True, align="left"):
    f = _font(size, bold)
    if align != "left":
        x -= f.measureText(text) * (0.5 if align == "center" else 1.0)
    c.drawString(text, x, y, f, skia.Paint(Color=col(color, a), AntiAlias=True))
    return f.measureText(text)


def tag(c, x, y, text, color=RED, a=1.0, dx=70, dy=-60, size=20):
    """a leader from the point (x, y) to a boxed label"""
    f = _font(size, True)
    tw = f.measureText(text)
    lx, ly = x + dx, y + dy
    c.drawLine(x, y, lx, ly, stroke(color, a * 0.9, 1.6))
    bx = lx if dx >= 0 else lx - tw - 16
    c.drawLine(lx, ly, bx + (tw + 16 if dx < 0 else 0), ly, stroke(color, a * 0.9, 1.6))
    c.drawRect(skia.Rect.MakeXYWH(bx, ly - size - 6, tw + 16, size + 10), skia.Paint(Color=col(0x000000, 0.45 * a)))
    c.drawRect(skia.Rect.MakeXYWH(bx, ly - size - 6, tw + 16, size + 10), stroke(color, a, 1.6))
    c.drawString(text, bx + 8, ly - 3, f, skia.Paint(Color=col(color, a), AntiAlias=True))


# ---------- the pixel / CRT module (the cosmic zoom, terminal moments): late-80s, no monitor frame (Lati, 12 Nov)
PAL = np.array([  # 32 colours: a late-80s home-computer palette (deep space blues, phosphor, earth, fire)
    0x000000, 0x0b0b1e, 0x141432, 0x1d2b53, 0x26407a, 0x2f5fa8, 0x3c8ad8, 0x5fb8f0, 0x9fe4ff, 0xffffff,
    0x7e2553, 0xb13e53, 0xef7d57, 0xffcd75, 0xfff1a8, 0xa7f070, 0x38b764, 0x257179, 0x1a3c3a, 0x29366f,
    0x5d275d, 0x8b4a8b, 0xc46cc4, 0x566c86, 0x94b0c2, 0xc2c3c7, 0x333c57, 0xffb347, 0xd97757, 0xff4040,
    0x8dff9a, 0x5fe8ff], np.float32)
PAL_RGB = np.stack([(PAL.astype(np.int64) >> 16) & 255, (PAL.astype(np.int64) >> 8) & 255, PAL.astype(np.int64) & 255], 1).astype(np.float32)
BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16 - 0.5


def quantize(small, spread=28.0):
    """float RGB 0..255 (h, w, 3) -> nearest palette colour after an ordered (Bayer) dither"""
    h, w = small.shape[:2]
    d = np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w, None] * spread
    x = np.clip(small + d, 0, 255).reshape(-1, 1, 3)
    i = ((x - PAL_RGB[None]) ** 2).sum(2).argmin(1)
    return PAL_RGB[i].reshape(h, w, 3)


def crt(small, out_h, out_w, line=0.42, glow=0.45):
    """a pixel image scaled up hard to the frame, with scanlines inside every pixel row and phosphor glow"""
    import cv2
    s = out_h // small.shape[0]
    big = np.kron(small, np.ones((s, s, 1), np.float32))
    big = cv2.resize(big, (out_w, out_h), interpolation=cv2.INTER_NEAREST) if big.shape[:2] != (out_h, out_w) else big
    rows = np.ones((out_h, 1, 1), np.float32)
    rows[s - 1::s] = line
    big = big * rows
    g = cv2.GaussianBlur(big, (0, 0), s * 1.6)
    return np.clip(big + g * glow, 0, 255).astype(np.uint8)


@lru_cache(4)
def psf(name="Lat15-VGA8"):
    """a console bitmap font (PSF1) from the system: {char: bool array (h, 8)}; real 80s glyphs, no download"""
    import gzip
    b = gzip.open(f"/usr/share/consolefonts/{name}.psf.gz").read()
    assert b[:2] == bytes([0x36, 0x04])
    mode, h = b[2], b[3]
    n = 512 if mode & 1 else 256
    g = np.unpackbits(np.frombuffer(b[4:4 + n * h], np.uint8)).reshape(n, h, 8).astype(bool)
    out, pos, gi = {}, 4 + n * h, 0
    if mode & 2:
        while gi < n and pos + 1 < len(b):
            u = b[pos] | b[pos + 1] << 8
            pos += 2
            if u == 0xFFFF:
                gi += 1
            elif u != 0xFFFE:
                out.setdefault(chr(u), g[gi])
    else:
        out = {chr(i): g[i] for i in range(n)}
    return out


def bitmap_text(text, name="Lat15-VGA8"):
    f = psf(name)
    blank = np.zeros_like(next(iter(f.values())))
    return np.concatenate([f.get(ch, blank) for ch in text], 1) if text else blank[:, :0]


def stamp(small, text, x, y, color, a=1.0, name="Lat15-VGA8", shadow=True):
    """bitmap text into a pixel image (float RGB) at (x, y), clipped to the image"""
    m = bitmap_text(text, name).astype(np.float32) * a
    h, w = small.shape[:2]
    rgb = np.array([(color >> 16) & 255, (color >> 8) & 255, color & 255], np.float32)
    for ox, oy, k, cc in ([(1, 1, 0.85, np.zeros(3, np.float32))] if shadow else []) + [(0, 0, 1.0, rgb)]:
        x0, y0 = int(x) + ox, int(y) + oy
        sx0, sy0 = max(0, -x0), max(0, -y0)
        x1, y1 = min(w, x0 + m.shape[1]), min(h, y0 + m.shape[0])
        if x1 <= max(0, x0) or y1 <= max(0, y0):
            continue
        mm = m[sy0:sy0 + y1 - max(0, y0), sx0:sx0 + x1 - max(0, x0), None] * k
        reg = small[max(0, y0):y1, max(0, x0):x1]
        reg[:] = reg * (1 - mm) + cc * mm
    return m.shape[1]


# ---------- sections
SECS = []


def load_sections(only=None):
    """every sec_*.py (or only those named, e.g. ["sec_a_opening"]). A section that fails to load is skipped with a
    warning, so one section's half-written file never stops another's render."""
    import sys
    import traceback
    SECS.clear()
    for f in sorted((ROOT / "production/tools/gfx").glob("sec_*.py")):
        if only and f.stem not in only:
            continue
        try:
            spec = importlib.util.spec_from_file_location(f.stem, f)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            SECS.append(m)
        except Exception:
            print(f"gfx: section {f.stem} skipped, it failed to load:\n{traceback.format_exc(limit=3)}", file=sys.stderr)


# ---------- transitions at cuts (a section's CUTS = {cut time: (kind, frames each side)}; the outgoing side ends on
# its last beat, the incoming starts on its first: edit/seams.md)
def transition(img, t, at, kind, n):
    import cv2
    d = (t - at) * 24  # frames from the cut, negative before it
    if not -n <= d < n:
        return img
    k = 1 - abs(d + 0.5) / n  # 0 at the edges of the window, 1 at the cut
    h, w = img.shape[:2]
    if kind == "flash":
        return np.clip(img.astype(np.float32) + 255 * ease(k) ** 1.5, 0, 255).astype(np.uint8)
    if kind == "whip":  # a whip pan: the outgoing shot flies off to the left, the incoming flies in from the right
        sh = ease(k) * w * 0.22 * (-1 if d < 0 else 1)
        m = np.float32([[1, 0, sh], [0, 1, 0]])
        out = cv2.warpAffine(img, m, (w, h), borderMode=cv2.BORDER_WRAP)
        n_ = max(1, int(ease(k) ** 0.7 * 160 * w / 1920))
        return cv2.blur(out, (n_, 1)) if n_ > 1 else out
    if kind == "mosaic":
        b = max(1, int(2 + ease(k) * 46 * w / 1920))
        small = cv2.resize(img, (max(1, w // b), max(1, h // b)), interpolation=cv2.INTER_AREA)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    if kind == "crt_roll":  # a vertical-hold slip: the picture rolls, tears sideways and splits its colours
        out = np.roll(img, int(ease(k) * h * 0.35 * (1 if d < 0 else -1)), axis=0)
        rows = np.arange(h)
        shift = (np.sin(rows / h * 23 + t * 40) * 40 * k * w / 1920).astype(int)
        out = out[rows[:, None], (np.arange(w)[None] - shift[:, None]) % w]
        sh = max(1, int(10 * k * w / 1920))
        out[..., 0] = np.roll(out[..., 0], sh, axis=1)
        out[..., 2] = np.roll(out[..., 2], -sh, axis=1)
        band = int((t * 7 % 1) * h)
        out[band:band + max(2, h // 60)] = np.clip(out[band:band + max(2, h // 60)].astype(np.int16) + 70, 0, 255)
        return (out * (1 - 0.35 * k)).astype(np.uint8)
    return img


SEAMS = {  # Kiln's transitions at cuts (edit/seams.md); the polish pass of 12 Nov, for Lati's eye
    18.04: ("whip", 3),       # out of space into the research pit, on the 18.08 accent
    35.96: ("flash", 2),      # into the command centre, on the pre-chorus accent (35.85)
    43.92: ("flash", 3),      # the racks white-hot into the launch
    105.00: ("crt_roll", 3),  # into the terminal faces (the plan's CRT roll into terminal moments)
    109.88: ("crt_roll", 3),  # and out of them to the launch keys
    116.79: ("flash", 2),     # "Me" into battle 3, on the 116.76 accent
    128.54: ("whip", 3),      # into the pilots
    146.08: ("flash", 2),     # the missile, on the 146.13 accent
}


def cuts_at(img, t):
    for at, (kind, n) in SEAMS.items():
        img = transition(img, t, at, kind, n)
    for m in SECS:
        for at, (kind, n) in getattr(m, "CUTS", {}).items():
            img = transition(img, t, at, kind, n)
    return img


def _active(m, t):
    return any(a <= t < b for a, b in getattr(m, "RANGES", [(0, 1e9)]))


def _draw(img, t, layer):
    h, w = img.shape[:2]
    rgba = np.dstack([img, np.full((h, w), 255, np.uint8)])
    surf = skia.Surface(rgba)
    c = surf.getCanvas()
    c.scale(w / U, w / U)
    drew = False
    for m in SECS:
        fn = getattr(m, layer, None)
        if fn and _active(m, t):
            fn(c, t, __import__(__name__))
            drew = True
    if layer == "top":  # the lyric line and impact frames: above everything, transitions included
        if MODULES["karaoke"]:
            karaoke(c, t)
            drew = True
        if MODULES["impact"]:
            impact(c, t)
            drew = True
    return rgba[..., :3].copy() if drew else img


def frame(img, t):
    """one frame of the film, picture in, picture with graphics out (both RGB uint8, any size)"""
    global IMG
    for m in SECS:  # a section may make the whole picture (the pixel zoom): picture(img, t, F) -> img
        if getattr(m, "picture", None) and _active(m, t):
            img = m.picture(img, t, __import__(__name__))
    IMG = img
    if MODULES["world"]:
        img = _draw(img, t, "world")
    img = finish(img, t)
    if MODULES["over"]:
        img = _draw(img, t, "over")
    img = cuts_at(img, t)  # a transition takes the picture and its panels with it (12 Nov: the LOAD gauge outlived the flash)
    img = _draw(img, t, "top")
    return img
