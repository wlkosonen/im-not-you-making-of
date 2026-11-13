"""Section B, the battles and the pilots (0:44-0:57, 1:21-1:34, 1:56-2:21).

What plays is Lati's cut (F.cut()); every shot is found with F.spans()/F.shot_at(), never by hard-coded song times.

s089 (Kiln, 12 Nov, approved by Lati: "cockpit hud good"): "ChatGPT's pilot; a lock tone; the HUD closes on a target."
The take's visor already carries a reticle that turns from blue to red: the HUD follows it. Each frame the visor's
glowing reticle is found afresh in the picture; lock rings close on it while it is blue, and the moment it is red the
HUD says LOCK, on a swarm mech (HERETIC, the radar's word from s023). Over the film, holding still (the over layer),
cyan like the fleet's HUDs, red for the lock. Its code below is unchanged (over_s089, visor, frame_hud).

The rest (battles agent, 12 Nov), from the board and the picture:
- Locks on swarm mechs, in the world layer (they ride the picture through the kick): the swarm's glow (the green
  eyes and cores of the skeletal mechs, the violet eyes of the spiked colossus) is found afresh in every frame of the
  take, linked into tracks over the whole take, gaps bridged, smoothed (sec_a's method, film 2's drift lesson). Red,
  with the swarm's words from s023; the fleet is never tagged.
    s033 "the lock holds" (line 8): ring closes, LOCK · ABLITERATED holds on a swarm mech in the melee.
    s036 a light touch: a thin red ring on the swarm mech's core as the frontier mech fires (no tag).
    s052 the missiles' target: the colossus's eyes locked on the beat (LOCK · ABLITERATED).
    s080 ChatGPT's fighter: TRACK on the far swarm mech, LOCK · HERETIC on the beat before the hit.
- s051 (line 16) "missile-lock brackets multiplying across the frame": the HUD's lock brackets double on every
  half-beat (1, 2, 4 ... 32), set where the take's first frame is open sky (measured), never on the fleet mech.
- The pilots (s083-s092, line 23-24, board: "cockpit HUDs, one per model, each in its colours, no logos"): a family
  of HUDs built like s089's (thin cyan vector frame, glow, one instrument each), a frame shape per machine:
    Claude's (s083, s084, s090): chamfered corners, side tapes, clay index marks (clay is Claude's side only).
    ChatGPT's (s089, s092): s089's corner brackets and heading tape; on s092 it breaks up as the screen shatters.
    Grok's (s085, s086, s091): notched bars and a white chevron (its black and white).
    Gemini's (s088): an arc scale shading cyan to violet (its iridescent helmet).
  Instruments: s083 none, the frame only (Lati, 12 Nov: "drop the graphics insert ... too busy"; its lock window,
  lock_window(), is kept unused), s086 throttle to MAX, s088 comms trace and s085 comms levels (both drawn from the vocal stem: the voice itself),
  s084 the horizon banking as he wrenches the sticks, s090 caution lights going red one after another, s091 pressure
  falling.  Values that are not measured (the horizon, throttle, pressure, the heading) are the fiction's own HUD,
  shaped to the take's action; no number on screen claims a real-world fact.
- Quiet: s094 (karaoke only). Left alone (the motion carries them): s031, s034, s035, s037, s038, s032, s053, s059,
  s056, s057, s058, s054, s076, s078, s079, s081, s082, s087. See production/edit/agents/battles.md.
The bottom ~170 units stay clear for the lyric line: nothing here is drawn below y = 880.
"""
import math
import subprocess
from functools import lru_cache

import cv2
import numpy as np
import skia

import base as F

S089 = F.spans("s089")

TRACKED = {  # shot: (glow kind, word or None, style)
    "s033": ("green", "ABLITERATED", "hold"),
    "s036": ("green", None, "light"),
    "s052": ("violet", "ABLITERATED", "beat"),
    "s080": ("green", "HERETIC", "beat"),
}
PILOTS = ("s083", "s084", "s085", "s086", "s088", "s090", "s091", "s092")
OVER_SHOTS = ("s089", "s051") + PILOTS
RANGES = sorted((a, b) for s in tuple(TRACKED) + OVER_SHOTS for a, b, _ in F.spans(s))
CUTS = {}
IMPACTS = []  # none proposed in this section: the hooks ("feed", "Me", "I'm not you") are outside it

VIOLET = 0xa98bff  # Gemini's iridescence, only as the far end of its cyan arc
BOTTOM = 880  # nothing below: the karaoke line's band


# ====================================================================== s089 (approved, unchanged)
def visor(img):
    """(x, y, red?) of the visor's reticle glow in 1920 units, or None"""
    h, w = img.shape[:2]
    f = img.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    red = np.clip((r - np.maximum(g, b)) / 255, 0, 1) * (r > 170)
    blue = np.clip((b - r) / 255, 0, 1) * (b > 170)
    y0, y1, x0, x1 = int(0.12 * h), int(0.62 * h), int(0.2 * w), int(0.8 * w)
    best = None
    for m, is_red in ((red, True), (blue, False)):
        s = cv2.GaussianBlur(m[y0:y1, x0:x1], (0, 0), 5 * w / 1280)
        yx = np.unravel_index(s.argmax(), s.shape)
        if best is None or s[yx] > best[2]:
            best = ((yx[1] + x0) * 1920 / w, (yx[0] + y0) * 1920 / w, float(s[yx]), is_red)
    return None if best[2] < 0.08 else (best[0], best[1], best[3])


def frame_hud(c, t, a, F):
    """the HUD's fixed furniture: corner frame, a heading tape, a pitch line"""
    F.brackets(c, 150, 110, 1620, 760, F.CYAN, 0.55 * a, arm=0.06, sw=2)
    hd = (t * 37.0) % 360  # the heading turns as the mech banks (illustrative)
    for i in range(-10, 11):
        deg = math.floor(hd / 5) * 5 + i * 5
        x = 960 + (deg - hd) * 14
        if 640 < x < 1280:
            tall = deg % 15 == 0
            c.drawLine(x, 140, x, 140 + (22 if tall else 11), F.stroke(F.CYAN, 0.6 * a, 2))
            if tall:
                F.hud_text(c, f"{int(deg) % 360:03d}", x, 196, size=22, color=F.CYAN, a=0.6 * a, align="center")
    c.drawLine(960, 118, 960, 134, F.stroke(F.CYAN, 0.9 * a, 2.5))


def over_s089(c, t, F):
    a0, a1, p = next(s for s in S089 if s[0] <= t < s[1])
    a = F.ease((t - a0) / 0.08)
    v = visor(F.IMG)
    F.glow_draw(c, lambda: frame_hud(c, t, a, F), blur=4, amount=0.5)
    if not v:
        return
    x, y, locked = v
    if not locked:
        k = F.ease((t - a0) / max(0.2, (a1 - a0) * 0.7))
        r = 300 - 230 * k

        def draw():
            F.reticle(c, x, y, r, F.CYAN, 0.85 * a, rot=t * 2.2, ticks=4, sw=2.2)
            F.reticle(c, x, y, r * 0.62, F.CYAN, 0.5 * a, rot=-t * 3.1, ticks=3, sw=1.6)
            F.hud_text(c, "TRACK", x + r + 18, y - 8, size=28, color=F.CYAN, a=0.8 * a)
        F.glow_draw(c, draw, blur=5, amount=0.6)
    else:
        blink = 1.0 if int(t * 16) % 2 == 0 else 0.55

        def draw():
            F.brackets(c, x - 90, y - 90, 180, 180, F.RED, blink, arm=0.32, sw=3)
            c.drawCircle(x, y, 64, F.stroke(F.RED, 0.9, 2.5))
            F.tag(c, x + 90, y - 90, "LOCK · HERETIC", F.RED, 1.0, dx=60, dy=-50, size=34)
        F.glow_draw(c, draw, blur=7, amount=0.8)


# ====================================================================== helpers (Kiln may lift these into the base)
def piece_at(shot, t):
    return next(((a, b, p) for a, b, p in F.spans(shot) if a <= t < b), None)


def beat_after(t, half=False):
    """the first beat (or half-beat) at or after t"""
    grid = list(F.BEATS)
    if half:
        grid = sorted(grid + [(x + y) / 2 for x, y in zip(F.BEATS, F.BEATS[1:])])
    i = int(np.searchsorted(grid, t - 1e-4))
    return grid[min(i, len(grid) - 1)]


def grid_steps(t0, t, half=True):
    """how many (half-)beats have struck since t0 (0 before the first)"""
    grid = list(F.BEATS)
    if half:
        grid = sorted(grid + [(x + y) / 2 for x, y in zip(F.BEATS, F.BEATS[1:])])
    return int(np.searchsorted(grid, t + 1e-4)) - int(np.searchsorted(grid, t0 - 1e-4))


def noise(i, salt=0):
    """a pure hash of an integer: 0..1 (glitches that are the same every render)"""
    x = (i * 374761393 + salt * 668265263) & 0xFFFFFFFF
    x = ((x ^ (x >> 13)) * 1274126177) & 0xFFFFFFFF
    return (x & 0xFFFF) / 65535.0


def halo(c, draw, a=0.55, blur=5):
    """a dark blurred copy under a HUD drawn on a bright picture (fire, a white flash), as the karaoke line has"""
    c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Blend(F.col(0x000000, a), skia.BlendMode.kSrcIn),
                                 ImageFilter=skia.ImageFilters.Blur(blur, blur)))
    draw()
    c.restore()


def take(file, size=(1280, 720)):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F.ROOT / file), "-vf", f"scale={size[0]}:{size[1]}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0], 3)


# ====================================================================== the swarm's glow, tracked
def glows(img, kind):
    """[(x, y, strength)] in 1920 units: the swarm's glow peaks in one frame (green eyes and cores of the skeletal
    mechs; the violet eyes of the spiked colossus, which sit in its black body)"""
    h, w = img.shape[:2]
    f = img.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    if kind == "green":
        m = np.clip((g - np.maximum(r, b)) / 255, 0, 1) * (g > 150)
    else:
        m = np.clip((np.minimum(r, b) - g) / 255, 0, 1) * (b > 170) * (r > 120)
        dark = cv2.blur((f.mean(2) < 60).astype(np.float32), (int(41 * w / 1280),) * 2)
        m = m * (dark > 0.25)  # eyes in a black body, not the lilac shading of the smoke
    s = cv2.GaussianBlur(m, (0, 0), 3 * w / 1280)
    mx = cv2.dilate(s, np.ones((int(31 * w / 1280),) * 2, np.uint8))
    ys, xs = np.where((s == mx) & (s > 0.04))
    k = 1920 / w
    return [(x * k, y * k, float(s[y, x])) for x, y in zip(xs, ys) if y * k < BOTTOM]


@lru_cache(8)
def glow_tracks(file, kind):
    """every glow of the take, found in each frame afresh (never flowed from frame to frame), linked to the nearest
    glow of the next frames (moving as it moved), gaps up to 8 frames bridged, smoothed over 5 frames.
    -> (detections per frame, [track: {frame: (x, y)}], [track: {frame: raw (x, y, s)}])"""
    det = [glows(im, kind) for im in take(file)]
    live, done = [], []
    for i, ds in enumerate(det):
        busy = len(ds) > 5  # a burst (the hit): nothing links through it
        free = [] if busy else list(ds)
        for tr in sorted(live, key=lambda tr: -len(tr["pts"])):
            last = max(tr["pts"])
            lx, ly, _ = tr["pts"][last]
            vx, vy = tr.get("v", (0.0, 0.0))
            px, py = lx + vx * (i - last), ly + vy * (i - last)
            best = min(free, key=lambda d: (d[0] - px) ** 2 + (d[1] - py) ** 2, default=None)
            if best and (best[0] - px) ** 2 + (best[1] - py) ** 2 < 90 ** 2:
                tr["v"] = ((best[0] - lx) / (i - last), (best[1] - ly) / (i - last))
                tr["pts"][i] = best
                free.remove(best)
        for tr in [tr for tr in live if i - max(tr["pts"]) > 8 or busy]:
            live.remove(tr)
            done.append(tr)
        live += [{"pts": {i: d}} for d in free]
    done += live
    out, raw = [], []
    for tr in done:
        ks = sorted(tr["pts"])
        if len(ks) < 5:
            continue
        idx = np.arange(ks[0], ks[-1] + 1)
        xs = np.interp(idx, ks, [tr["pts"][k][0] for k in ks])
        ys = np.interp(idx, ks, [tr["pts"][k][1] for k in ks])
        ker = np.ones(5) / 5
        xs = np.convolve(np.pad(xs, 2, mode="edge"), ker, "valid")
        ys = np.convolve(np.pad(ys, 2, mode="edge"), ker, "valid")
        out.append({int(k): (float(x), float(y)) for k, x, y in zip(idx, xs, ys)})
        raw.append(tr["pts"])
    return det, out, raw


def target(shot, piece):
    """the track this piece locks: the one alive over most of the frames the cut uses, the strongest on a tie"""
    kind = TRACKED[shot][0]
    det, trs, raw = glow_tracks(piece["file"], kind)
    f0 = int(piece["in"] * 24)
    f1 = int((piece["in"] + (piece["t1"] - piece["t0"]) * (piece.get("speed") or 1)) * 24)
    best, score = None, 0.0
    for tr, rw in zip(trs, raw):
        n = sum(1 for k in tr if f0 <= k <= f1)
        s = n + 0.01 * sum(v[2] for v in rw.values())
        if n >= 4 and s > score:
            best, score = (tr, rw), s
    return best


def at(tr, fi):
    i0 = int(np.floor(fi))
    if i0 not in tr or i0 + 1 not in tr:
        return (tr[i0] if i0 in tr else None)
    u = fi - i0
    return (tr[i0][0] * (1 - u) + tr[i0 + 1][0] * u, tr[i0][1] * (1 - u) + tr[i0 + 1][1] * u)


def world(c, t, F):
    shot, p = F.shot_at(t)
    if shot not in TRACKED or not p:
        return
    kind, word, style = TRACKED[shot]
    got = target(shot, p)
    if not got:
        return
    tr, _ = got
    fi = F.src_t(p, t) * 24
    GRACE = 3  # frames a lock holds its last found place when the glow drops out at the ends of the track
    if not min(tr) - GRACE <= fi <= max(tr) + GRACE:
        return
    pos = at(tr, min(max(fi, min(tr)), max(tr)))
    if not pos:
        return
    x, y = pos
    a0, a1 = p["t0"], p["t1"]
    life = min(fi - min(tr), max(tr) - fi) + GRACE
    a = F.ease(life / 3) * F.ease((t - a0) / 0.08) * (1 - F.ease((t - (a1 - 0.06)) / 0.06))
    if style == "light":  # s036: a thin ring, no words
        t_in = beat_after(a0)
        k = F.ease((t - t_in + 0.12) / 0.2)
        if k <= 0:
            return
        F.glow_draw(c, lambda: F.reticle(c, x, y, 70 - 22 * k, F.RED, 0.8 * a * k, rot=t * 1.4, ticks=4, sw=1.8),
                    blur=4, amount=0.55)
        return
    if style == "hold":  # s033: the lock closes on the first half-beat and holds the whole shot
        t_lock = beat_after(a0 + 0.2, half=True)
    else:  # s052, s080: tracked, then LOCK on the first half-beat after the ring has had time to close
        born = a0 + (min(tr) / 24 - p["in"]) / (p.get("speed") or 1)  # song time the glow is first found
        t_lock = beat_after(max(a0, born) + 0.25, half=True)
    if t < t_lock:
        k = F.ease((t - a0) / max(0.1, t_lock - a0)) if style == "hold" else F.ease((t - max(a0, born)) / max(0.1, t_lock - max(a0, born)))
        r = 170 - 110 * k

        def draw():
            F.reticle(c, x, y, r, F.RED, 0.75 * a, rot=t * 2.6, ticks=4, sw=2.0)
            F.reticle(c, x, y, r * 0.6, F.RED, 0.45 * a, rot=-t * 3.3, ticks=3, sw=1.4)
            F.hud_text(c, "TRACK", x + r + 14, y - 6, size=22, color=F.RED, a=0.75 * a)
        F.glow_draw(c, draw, blur=5, amount=0.55)
    else:
        blink = 1.0 if int(t * 16) % 2 == 0 else 0.6
        snap = 1 + 0.35 * (1 - F.ease((t - t_lock) / 0.1))  # the brackets snap shut on the lock
        h = 62 * snap
        f0 = int(p["in"] * 24)
        side = -1 if np.mean([v[0] for k, v in tr.items() if k >= f0]) > 1400 else 1  # one side for the piece

        def draw():
            F.brackets(c, x - h, y - h, 2 * h, 2 * h, F.RED, a * blink, arm=0.32, sw=2.8)
            c.drawCircle(x, y, 40, F.stroke(F.RED, 0.85 * a, 2.2))
            F.tag(c, x + side * h, y - h, f"LOCK · {word}", F.RED, a, dx=side * 46, dy=-40, size=26)
        F.glow_draw(c, draw, blur=6, amount=0.7)


# ====================================================================== s051: missile-lock brackets multiplying
@lru_cache(4)
def open_sky(file, t_in, speed):
    """up to 32 spots of open dark sky (1920 units), spread out, in a fixed shuffled order: where the HUD's lock
    brackets appear. A spot must be sky in the take's frames over the first ~0.25 s the cut uses (measured), so no
    bracket sits on the fleet mech as the camera drifts; later the smoke covers everything and that is fine."""
    masks = []
    for dt in (0.0, 0.3):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t_in + dt * speed / 1.25:.3f}", "-i", str(F.ROOT / file),
                              "-frames:v", "1", "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        im = np.frombuffer(raw, np.uint8).reshape(270, 480, 3).astype(np.float32)
        masks.append(cv2.blur((im.mean(2) < 50).astype(np.float32), (21, 21)))  # ~85 units of sky round each spot
    dark = np.min(masks, axis=0)
    k = 1920 / 480
    cand = [(x * k, y * k) for y in range(10, 270, 6) for x in range(10, 480, 6)
            if dark[y, x] > 0.85 and 150 < x * k < 1770 and 130 < y * k < BOTTOM - 40
            and not (x * k < 560 and y * k < 230)]  # clear of the counter
    cand.sort(key=lambda q: noise(int(q[0]) * 7919 + int(q[1]), 51))
    out = []
    for q in cand:
        if all((q[0] - o[0]) ** 2 + (q[1] - o[1]) ** 2 > 84 ** 2 for o in out):
            out.append(q)
        if len(out) == 32:
            break
    return out


def over_s051(c, t, a0, a1, p):
    spots = open_sky(p["file"], p["in"], p.get("speed") or 1)
    n = min(len(spots), 2 ** grid_steps(a0, t))  # 1, 2, 4, ... doubling on every half-beat
    if not n:
        return
    fade = F.ease((t - a0) / 0.06) * (1 - F.ease((t - (a1 - 0.1)) / 0.1))
    grid = sorted(list(F.BEATS) + [(x + y) / 2 for x, y in zip(F.BEATS, F.BEATS[1:])])

    def draw():
        for i, (x, y) in enumerate(spots[:n]):
            born = a0 if i == 0 else grid[int(np.searchsorted(grid, a0 - 1e-4)) + int(math.log2(i))]
            k = F.ease((t - born) / 0.08)
            h = 30 * (2.2 - 1.2 * k)
            bl = 1.0 if int(t * 14 + i) % 3 else 0.6
            F.brackets(c, x - h, y - h, 2 * h, 2 * h, F.RED, fade * bl * (0.5 + 0.5 * k), arm=0.3, sw=2.8)
            c.drawCircle(x, y, 4.5, skia.Paint(Color=F.col(F.RED, fade * k), AntiAlias=True))
        F.hud_text(c, f"MSL LOCK {n:02d}", 200, 172, size=30, color=F.CYAN, a=0.95 * fade)
        c.drawLine(200, 186, 200 + 9 * n, 186, F.stroke(F.CYAN, 0.7 * fade, 3))
    F.glow_draw(c, draw, blur=5, amount=0.6)


# ====================================================================== the pilots' machines: frames
def frame_claude(c, t, a, flick=1.0):
    """Claude's machine: chamfered corners, a speed and an altitude tape, clay index marks"""
    st = F.stroke(F.CYAN, 0.55 * a * flick, 2)
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        x0 = 150 if sx > 0 else 1770
        y0 = 110 if sy > 0 else 870
        p = skia.Path()
        p.moveTo(x0, y0 + sy * 150)
        p.lineTo(x0, y0 + sy * 60)
        p.lineTo(x0 + sx * 60, y0)
        p.lineTo(x0 + sx * 190, y0)
        c.drawPath(p, st)
    for x, d in ((236, 1), (1684, -1)):  # the tapes scroll (illustrative), the index holds still
        off = (t * (90 if d > 0 else 55)) % 24
        for i in range(-9, 10):
            y = 630 + i * 24 + off
            if 480 < y < 790:
                ln = 18 if (i % 4 == 0) else 9
                c.drawLine(x, y, x - d * ln, y, F.stroke(F.CYAN, 0.5 * a * flick, 1.6))
        c.drawLine(x, 480, x, 790, F.stroke(F.CYAN, 0.35 * a * flick, 1.4))
        tri = skia.Path()
        tri.moveTo(x + d * 6, 630)
        tri.lineTo(x + d * 24, 620)
        tri.lineTo(x + d * 24, 640)
        tri.close()
        c.drawPath(tri, skia.Paint(Color=F.col(F.CLAY, 0.9 * a), AntiAlias=True))
    c.drawLine(900, 128, 1020, 128, F.stroke(F.CYAN, 0.5 * a * flick, 1.6))
    dm = skia.Path()
    for i, (dx, dy) in enumerate(((0, -9), (9, 0), (0, 9), (-9, 0))):
        (dm.moveTo if i == 0 else dm.lineTo)(960 + dx, 128 + dy)
    dm.close()
    c.drawPath(dm, skia.Paint(Color=F.col(F.CLAY, 0.95 * a), AntiAlias=True))


def frame_grok(c, t, a, flick=1.0):
    """Grok's machine: notched bars top and bottom, a white chevron, slashes (its black and white)"""
    st = F.stroke(F.CYAN, 0.55 * a * flick, 2.2)
    for y0, d in ((112, 1), (868, -1)):
        for sx in (1, -1):
            x0 = 960 - sx * 790
            p = skia.Path()
            p.moveTo(x0, y0 + d * 46)
            p.lineTo(x0 + sx * 40, y0)
            p.lineTo(x0 + sx * 600, y0)
            p.lineTo(x0 + sx * 628, y0 + d * 28)
            c.drawPath(p, st)
            for j in range(3):
                xs = x0 + sx * (470 + j * 26)
                c.drawLine(xs, y0 + d * 8, xs + sx * 14, y0 + d * 22, F.stroke(F.WHITE, 0.6 * a * flick, 2.4))
    ch = skia.Path()
    ch.moveTo(924, 118)
    ch.lineTo(960, 146)
    ch.lineTo(996, 118)
    c.drawPath(ch, F.stroke(F.WHITE, 0.85 * a, 3))


def frame_gemini(c, t, a):
    """Gemini's machine: an arc scale across the top, cyan shading into violet, and arced corners"""
    cx, cy, r = 960, 1520, 1380
    shader = skia.GradientShader.MakeLinear([(420, 0), (1500, 0)], [F.col(F.CYAN, 0.6 * a), F.col(VIOLET, 0.6 * a)])
    arc = skia.Paint(Shader=shader, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2)
    c.drawArc(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), 247, 46, False, arc)
    roll = (t * 6.0) % 2.0  # the scale drifts with the heading (illustrative)
    for i in range(-11, 12):
        ang = math.radians(270 + (i * 2.0 + roll))
        if abs(i * 2.0 + roll) > 22:
            continue
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        ln = 22 if i % 3 == 0 else 11
        x2, y2 = cx + (r + ln) * math.cos(ang), cy + (r + ln) * math.sin(ang)
        c.drawLine(x1, y1, x2, y2, skia.Paint(Shader=shader, AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                              StrokeWidth=2))
    c.drawLine(960, 118, 960, 136, F.stroke(F.WHITE, 0.8 * a, 2.5))
    for (x0, y0, start) in ((150, 110, 180), (1770, 110, 270), (150, 870, 90), (1770, 870, 0)):
        rr = 110
        ox = x0 + (rr if x0 < 960 else -rr)
        oy = y0 + (rr if y0 < 540 else -rr)
        c.drawArc(skia.Rect.MakeLTRB(ox - rr, oy - rr, ox + rr, oy + rr), start, 90, False,
                  skia.Paint(Shader=shader, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2))


# ====================================================================== the pilots' instruments
def mech_wire(c, x, y, s, color, a, sw=2.0):
    """a skeletal mech in vector lines, centred at (x, y), about 2s tall"""
    st = F.stroke(color, a, sw)
    c.drawCircle(x, y - 0.8 * s, 0.14 * s, st)
    c.drawCircle(x, y - 0.8 * s, 0.035 * s, skia.Paint(Color=F.col(color, a), AntiAlias=True))
    body = skia.Path()
    for i, (px, py) in enumerate(((-0.3, -0.6), (0.3, -0.6), (0.2, 0.0), (-0.2, 0.0))):
        (body.moveTo if i == 0 else body.lineTo)(x + px * s, y + py * s)
    body.close()
    c.drawPath(body, st)
    c.drawCircle(x, y - 0.32 * s, 0.07 * s, st)
    for d in (1, -1):
        for pts in (((0.3, -0.58), (0.55, -0.25), (0.62, 0.1)), ((0.12, 0.0), (0.22, 0.45), (0.2, 0.92)),
                    ((0.2, 0.92), (0.32, 0.95))):
            p = skia.Path()
            for i, (px, py) in enumerate(pts):
                (p.moveTo if i == 0 else p.lineTo)(x + d * px * s, y + py * s)
            c.drawPath(p, st)
        c.drawLine(x + d * 0.22 * s, y - 0.68 * s, x + d * 0.42 * s, y - 0.62 * s, st)


def lock_window(c, t, a, a0, a1):
    """s083: a target window; a swarm silhouette draws in (red), the frontier's (cyan) slides onto it and they
    coincide on the beat: LOCK, and the same shape (line 8 and 23: made in your image)"""
    x0, y0, w, h = 1520, 160, 260, 290
    t_lock = beat_after(a0 + 0.35)
    k = F.ease((t - a0) / max(0.1, t_lock - a0))
    locked = t >= t_lock
    cx, cy, s = x0 + w / 2, y0 + 138, 84
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), skia.Paint(Color=F.col(0x000000, 0.5 * a)))

    def draw():
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), F.stroke(F.CYAN, 0.6 * a, 1.6))
        F.hud_text(c, "TGT", x0 + 10, y0 + 26, size=20, color=F.CYAN, a=0.8 * a)
        if locked:
            F.hud_text(c, "MATCH", x0 + w - 10, y0 + 26, size=20, color=F.CYAN, a=0.9 * a, align="right")
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(x0, y0, w, 40 + (h - 40) * F.ease((t - a0) / 0.3)))
        mech_wire(c, cx, cy, s, F.RED, 0.9 * a, 2.2)
        c.restore()
        mech_wire(c, cx + 70 * (1 - k), cy - 10 * (1 - k), s, F.CYAN, (0.35 + 0.4 * k) * a, 1.6)
        bh = 120 - 20 * k if not locked else 100
        bl = 1.0 if (not locked or int(t * 16) % 2 == 0) else 0.6
        F.brackets(c, cx - bh, cy - bh * 1.15, 2 * bh, 2.3 * bh, F.RED if locked else F.CYAN, a * bl, arm=0.18, sw=2.2)
        if locked:
            c.drawRect(skia.Rect.MakeXYWH(x0 + 6, y0 + h - 40, w - 12, 34), skia.Paint(Color=F.col(F.RED, 0.3 * a * bl)))
            F.hud_text(c, "LOCK · ABLITERATED", x0 + w / 2, y0 + h - 15, size=21, color=F.RED, a=a, align="center")
    F.glow_draw(c, draw, blur=5, amount=0.6)


def throttle(c, t, a, a0):
    """s086: the throttle bar slams to MAX"""
    x, y0, y1 = 196, 300, 720
    k = F.ease((t - a0) / 0.22)
    lvl = y1 - (y1 - y0) * k

    def draw():
        c.drawRect(skia.Rect.MakeLTRB(x, y0, x + 26, y1), F.stroke(F.CYAN, 0.6 * a, 1.8))
        c.drawRect(skia.Rect.MakeLTRB(x + 4, lvl, x + 22, y1 - 4), skia.Paint(Color=F.col(F.CYAN, 0.55 * a)))
        for i in range(11):
            yy = y1 - (y1 - y0) * i / 10
            c.drawLine(x + 30, yy, x + (44 if i % 5 == 0 else 36), yy, F.stroke(F.CYAN, 0.55 * a, 1.6))
        F.hud_text(c, "THR", x - 4, y0 - 18, size=22, color=F.CYAN, a=0.8 * a)
        if k > 0.98 and int(t * 10) % 2 == 0:
            F.hud_text(c, "MAX", x + 56, y0 + 10, size=30, color=F.WHITE, a=a)
    F.glow_draw(c, draw, blur=5, amount=0.6)


def comms_trace(c, t, a):
    """s088: the comms channel's trace, the vocal stem itself"""
    x0, y0, w, h = 180, 170, 420, 180
    shader = skia.GradientShader.MakeLinear([(x0, 0), (x0 + w, 0)], [F.col(F.CYAN, a), F.col(VIOLET, a)])
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), skia.Paint(Color=F.col(0x000000, 0.4 * a)))
    wv = F.vocal_wave(t, dur=0.045, n=220)
    p = skia.Path()
    for i, v in enumerate(wv):
        (p.moveTo if i == 0 else p.lineTo)(x0 + 10 + (w - 20) * i / (len(wv) - 1), y0 + h / 2 + 18 - v * h * 1.4)

    def draw():
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), F.stroke(F.CYAN, 0.55 * a, 1.6))
        c.drawLine(x0 + 10, y0 + h / 2 + 18, x0 + w - 10, y0 + h / 2 + 18, F.stroke(F.CYAN, 0.2 * a, 1))
        c.drawPath(p, skia.Paint(Shader=shader, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        F.hud_text(c, "COMMS · CH 2 · TX", x0 + 10, y0 + 28, size=20, color=F.CYAN, a=0.85 * a)
        if int(t * 4) % 2 == 0:
            c.drawCircle(x0 + w - 20, y0 + 20, 6, skia.Paint(Color=F.col(F.RED, 0.9 * a), AntiAlias=True))
    F.glow_draw(c, draw, blur=4, amount=0.6)


def comms_levels(c, t, a):
    """s085: the same channel received, as level bars from the vocal stem"""
    x0, y0, w, h, n = 180, 720, 340, 140, 16
    lv = F.vocal_bands(t, bands=n)
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), skia.Paint(Color=F.col(0x000000, 0.45 * a)))

    def draw():
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), F.stroke(F.CYAN, 0.55 * a, 1.6))
        F.hud_text(c, "CH 2 · RX", x0 + 10, y0 + 26, size=20, color=F.CYAN, a=0.85 * a)
        bw = (w - 20) / n
        for j, v in enumerate(lv):
            bh = max(3, v * (h - 50))
            c.drawRect(skia.Rect.MakeXYWH(x0 + 10 + j * bw + 2, y0 + h - 10 - bh, bw - 4, bh),
                       skia.Paint(Color=F.col(F.WHITE if v > 0.8 else F.CYAN, 0.8 * a)))
    F.glow_draw(c, draw, blur=4, amount=0.5)


def horizon(c, t, a, a0, a1):
    """s084: the horizon banks as he wrenches the sticks left, then the nose comes up as he hauls them back
    (the fiction's own attitude, shaped to the take's action)"""
    k = (t - a0) / max(0.1, a1 - a0)
    bank = 26 * F.ease(k / 0.45)  # sticks left: the left wing drops, the horizon turns clockwise
    pitch = 14 * F.ease((k - 0.4) / 0.6)
    cx, cy = 960, 470
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(620, 200, 1300, 740))
    c.translate(cx, cy)
    c.rotate(bank)
    c.translate(0, pitch * 9)

    def ladder():
        c.drawLine(-460, 0, -60, 0, F.stroke(F.CYAN, 0.95 * a, 3))
        c.drawLine(60, 0, 460, 0, F.stroke(F.CYAN, 0.95 * a, 3))
        for i in range(-4, 5):
            if i == 0:
                continue
            y = -i * 90
            st = F.stroke(F.CYAN, 0.8 * a, 2.2)
            for d in (1, -1):
                c.drawLine(d * 70, y, d * 170, y, st)
                c.drawLine(d * 170, y, d * 170, y + (12 if i > 0 else -12), st)
            F.hud_text(c, f"{abs(i) * 10}", 186, y + 8, size=22, color=F.CYAN, a=0.8 * a)
    halo(c, ladder, 0.75, blur=4)
    F.glow_draw(c, ladder, blur=4, amount=0.5)
    c.restore()
    w = skia.Path()  # the waterline, Claude's clay
    for i, (px, py) in enumerate(((-70, 0), (-34, 0), (-18, 16), (0, 0), (18, 16), (34, 0), (70, 0))):
        (w.moveTo if i == 0 else w.lineTo)(cx + px, cy + py)
    halo(c, lambda: c.drawPath(w, F.stroke(F.CLAY, 0.95 * a, 3)), 0.5)
    F.glow_draw(c, lambda: c.drawPath(w, F.stroke(F.CLAY, 0.95 * a, 3)), blur=4, amount=0.6)


CAUTIONS = ("HULL", "PWR", "COOL", "HYD", "FIRE")


def cautions(c, t, a, a0):
    """s090: caution lights going red one after another on the half-beats (the damage spreads)"""
    n = 1 + grid_steps(a0, t)
    blink = 1.0 if int(t * 8) % 2 == 0 else 0.45
    x0, y0, w, h = 180, 250, 170, 52

    def draw():
        for i, name in enumerate(CAUTIONS):
            y = y0 + i * (h + 14)
            lit = i < n
            if lit:
                c.drawRect(skia.Rect.MakeXYWH(x0, y, w, h), skia.Paint(Color=F.col(F.RED, 0.32 * a * blink)))
            c.drawRect(skia.Rect.MakeXYWH(x0, y, w, h), F.stroke(F.RED if lit else F.CYAN, (0.95 if lit else 0.4) * a, 2))
            F.hud_text(c, name, x0 + w / 2, y + h / 2 + 9, size=26, color=F.RED if lit else F.CYAN,
                       a=(blink if lit else 0.4) * a, align="center")
        mw = 360
        c.drawRect(skia.Rect.MakeXYWH(960 - mw / 2, 158, mw, 50), F.stroke(F.RED, a * blink, 2.6))
        F.hud_text(c, "MASTER CAUTION", 960, 193, size=28, color=F.RED, a=a * blink, align="center")
    F.glow_draw(c, draw, blur=6, amount=0.7)


def pressure(c, t, a, a0, a1):
    """s091: cabin pressure falling as the pipes burst (the fiction's own gauge, shaped to the take)"""
    k = (t - a0) / max(0.1, a1 - a0)
    v = 0.78 - 0.7 * F.ease(k / 0.9)
    cx, cy, r = 360, 400, 140
    rect = skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r)

    def draw():
        c.drawArc(rect, 180, 180, False, F.stroke(F.CYAN, 0.55 * a, 2))
        c.drawArc(rect, 180, 36, False, F.stroke(F.RED, 0.8 * a, 5))
        for i in range(11):
            ang = math.radians(180 + 18 * i)
            c.drawLine(cx + r * math.cos(ang), cy + r * math.sin(ang), cx + (r - (18 if i % 5 == 0 else 10)) * math.cos(ang),
                       cy + (r - (18 if i % 5 == 0 else 10)) * math.sin(ang), F.stroke(F.CYAN, 0.55 * a, 1.8))
        ang = math.radians(180 + 180 * v)
        low = v < 0.25
        c.drawLine(cx, cy, cx + (r - 24) * math.cos(ang), cy + (r - 24) * math.sin(ang),
                   F.stroke(F.RED if low else F.WHITE, 0.95 * a, 3.2))
        c.drawCircle(cx, cy, 6, skia.Paint(Color=F.col(F.WHITE, 0.9 * a), AntiAlias=True))
        F.hud_text(c, "PRESS", cx, cy + 40, size=24, color=F.CYAN, a=0.8 * a, align="center")
        if low and int(t * 8) % 2 == 0:
            F.hud_text(c, "PRESS LOW", cx, cy + 78, size=30, color=F.RED, a=a, align="center")
    F.glow_draw(c, draw, blur=6, amount=0.65)


def broken_hud(c, t, a, a0, a1):
    """s092: ChatGPT's HUD (s089's frame) breaking up as the screen in front of him shatters: the whole HUD drops out
    on more frames as the shot goes on, and strips of it tear sideways (a hash of the frame number: the same every
    render)"""
    k = (t - a0) / max(0.1, a1 - a0)
    fi = int(round(t * 24))
    if noise(fi, 95) > 0.15 + 0.4 * k:  # whole frame present
        dy = (noise(fi, 96) - 0.5) * 14 * k
        c.save()
        c.translate(0, dy)
        F.glow_draw(c, lambda: frame_hud(c, t, a * (0.75 + 0.25 * noise(fi, 97)), F), blur=4, amount=0.5)
        c.restore()
    for j in range(3 + int(4 * k)):  # torn strips
        y0 = 100 + noise(fi * 13 + j, 98) * 760
        hh = 12 + noise(fi * 7 + j, 99) * 40
        dx = (noise(fi * 17 + j, 93) - 0.5) * 260
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0, y0, 1920, hh))
        c.translate(dx, 0)
        F.glow_draw(c, lambda: frame_hud(c, t, a, F), blur=4, amount=0.6)
        c.restore()
    if int(t * 6) % 2 == 0:
        F.glow_draw(c, lambda: F.hud_text(c, "DISPLAY FAULT", 200, 250, size=28, color=F.RED, a=a), blur=5, amount=0.7)


def over(c, t, F):
    shot, p = F.shot_at(t)
    if shot == "s089":
        return over_s089(c, t, F)
    got = piece_at(shot, t) if shot in OVER_SHOTS else None
    if not got:
        return
    a0, a1, p = got
    a = F.ease((t - a0) / 0.08)
    if shot == "s051":
        return over_s051(c, t, a0, a1, p)
    fi = int(round(t * 24))
    if shot in ("s083", "s084", "s090"):
        flick = (0.35 + 0.65 * noise(fi, 90)) if shot == "s090" else 1.0
        F.glow_draw(c, lambda: frame_claude(c, t, a, flick), blur=4, amount=0.5)
        if shot == "s083":
            pass  # the frame only: Lati, 12 Nov, "from this frame id drop the graphics insert and keep the lyrics.
            # Frame reads too busy otherwise." lock_window() kept below, unused, in case it is wanted elsewhere
        elif shot == "s084":
            horizon(c, t, a, a0, a1)
        else:
            cautions(c, t, a, a0)
    elif shot in ("s085", "s086", "s091"):
        flick = (0.4 + 0.6 * noise(fi, 91)) if shot == "s091" else 1.0
        if shot == "s085":  # the take flashes white: the frame keeps a dark halo
            halo(c, lambda: frame_grok(c, t, a, flick), 0.45)
        F.glow_draw(c, lambda: frame_grok(c, t, a, flick), blur=4, amount=0.5)
        if shot == "s085":
            comms_levels(c, t, a)
        elif shot == "s086":
            throttle(c, t, a, a0)
        else:
            pressure(c, t, a, a0, a1)
    elif shot == "s088":
        F.glow_draw(c, lambda: frame_gemini(c, t, a), blur=4, amount=0.5)
        comms_trace(c, t, a)
    elif shot == "s092":
        broken_hud(c, t, a, a0, a1)
