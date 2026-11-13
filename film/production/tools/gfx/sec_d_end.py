"""Section D, the end: the bridge's launch (1:45-1:56.79) and the calm, the missile, the zoom and the end (2:21-the end).

What each shot carries (dispatch by F.shot_at / F.spans, so Lati's trims move the graphics with the shots):
- s067 the terminal faces, s075 "Me": locked pictures, nothing drawn. s095q the calm cockpit, s109 sakura, s108 the
  nuclear end: quiet, the base's karaoke line only.
- s068-s073, the launch (end, 12 Nov): one launch-control readout in the top-left, over the film (the takes have no
  screen that can carry it: s068's console is switches, a key and a button; the silos are outdoors). Red and amber, the
  real 8x8 console font of the zoom, scaled x3, scanlines inside the letters only (as the karaoke line). It follows the
  take's own events, measured in s068's frames: KEY 1 ARMED as the key turns (take 0.50 s), ENABLE ON as the switch
  lamps light (0.79 s), a countdown to the button's red glow (2.58 s), then LAUNCH and a T+ clock. Each silo shot adds
  a row on its cut (SILO 01 DESERT, ... in the order they play), s073 ALL SILOS. Every word is the fiction's own.
- s101 the missile: a track box on the battle ahead (in the picture, so world()), found afresh in every frame of the
  take (the fireball's warm mass, or before it the brightest spark above the missile), smoothed over the whole take;
  it closes on the beats from the shot's first, then rides the fireball and fades as it fills the frame.
- The cuts into and out of the zoom: the base's crt_roll, CUTS below.

The cosmic zoom (Kiln's step 1 test, Lati's eye pending on its last changes) is unchanged: zoom_picture() and all
above it; picture() only hands the zoom's gap to it.

Lati, 12 Nov: the stretch 2:31.83-2:43.71 is "wholly for universe scale zoom-out and zoom in on beat, in code", and
"aestethically late 80s, pixel, crt graphics, (no monitor)". So: a 320x180 picture in a 32-colour palette with an
ordered dither, scaled up hard, scanlines inside every pixel row and phosphor glow (base: quantize, crt), the type a
real 8x8 console font (40 columns, as on the home computers of the time).

The camera steps out on each beat from Earth (the battle glittering in orbit) past the Moon's orbit, the planets, the
Oort cloud and the nearest stars to the Milky Way, which it reaches on the accent at 157.76, on to the Local Group and
Laniakea, holds there two beats, then steps back in to Earth's night side for the cut to s109 at 163.71. Every scale and distance is real: Earth 12,742 km across, the Moon
384,400 km, the planets' orbits in AU, the Oort cloud 2,000-100,000 AU, the nearest stars at their distances and
galactic longitudes (projected onto the plane), the Sun 26,000 ly from the galaxy's centre. The planets' places on
their orbits and the galaxy's arms are drawn, not measured. A small clay cross keeps Earth's place at every scale.
Kiln, 12 Nov 2026.
"""
import math
from functools import lru_cache

import numpy as np

import base as F

GAP = next(p for p in F.cut() if p["kind"] not in ("video", "image") and p["t0"] <= 157.0 < p["t1"])
LAUNCH_SHOTS = ("s068", "s069", "s070", "s071", "s072", "s073")
RANGES = [(a, b) for s in LAUNCH_SHOTS + ("s101",) for a, b, _ in F.spans(s)] + [(GAP["t0"], GAP["t1"])]
CUTS = {GAP["t0"]: ("crt_roll", 4), GAP["t1"]: ("crt_roll", 4)}  # into and out of the zoom (end, 12 Nov)
IMPACTS = []  # "Me" (116.08) is on s075, locked and quiet: no starburst (log, 12 Nov)
W, H = 320, 180
KM_AU, KM_LY = 1.496e8, 9.461e12
KM_MLY = KM_LY * 1e6

# ---------- the camera: log10 of the field's width in km, one step on each beat (out, then back in)
# out: the Milky Way lands on the 157.76 accent; two steps more to the clusters (Lati, 12 Nov: "add couple more steps to
# galactic clutsters"), the widest view held two beats ("hold at maximum zoom out for a beat longer"), a quicker way in
OUT = [(151.83, 4.6), (152.09, 5.15), (152.64, 6.15), (153.19, 7.0), (153.72, 8.55), (154.26, 9.1), (154.81, 9.75),
       (155.34, 10.4), (155.89, 13.0), (156.46, 14.25), (157.03, 15.9), (157.58, 18.25), (158.13, 20.15),
       (158.69, 22.1)]
TURN = 159.79  # the widest view holds 158.69-159.79
IN = [(159.79, 18.25), (160.34, 14.25), (160.89, 10.4), (161.44, 8.55), (161.99, 6.15), (162.54, 5.15), (163.16, 4.6),
      (163.68, 3.85)]
KEYS = OUT + IN
STEP = 0.16  # each step snaps in over 0.16 s, then the view drifts on slowly


def view(t):
    """(L, velocity) at song time t"""
    i = max(0, int(np.searchsorted([k[0] for k in KEYS], t, side="right")) - 1)
    t0, L = KEYS[i]
    prev = KEYS[i - 1][1] if i else L
    nxt = KEYS[i + 1] if i + 1 < len(KEYS) else (t0 + 0.55, L)
    drift = (0.07 if t < 158.6 else 0.05 if t < TURN else -0.07)
    u = t - t0
    if i and u < STEP:
        pt = KEYS[i - 1][0]
        start = prev + (0.07 if pt < 158.6 else 0.05 if pt < TURN else -0.07)
        return start + (L - start) * F.ease(u / STEP), (L - start) / STEP
    return L + drift * min(1.0, (u - STEP) / max(0.05, nxt[0] - t0 - STEP)), 0.0


def smooth(x, a, b):
    return F.ease((x - a) / (b - a))


# ---------- the places (km, Earth at the origin; x right, y down; the Sun to the left, so Earth is lit from the left)
SUN = np.array([-KM_AU, 0.0])
GC_DIR = np.array([0.62, -0.78])  # the galactic centre, up and to the right of the Sun
GC = SUN + GC_DIR * 26000 * KM_LY
# beyond the Milky Way (distances real, directions drawn): the Local Group (~10 Mly across; Andromeda 2.5 Mly, Triangulum
# 2.7 Mly), and Laniakea, the supercluster we are part of (~520 Mly across), the Virgo cluster 54 Mly away, its
# Great Attractor about 220 Mly away (Tully et al., Nature 2014)
M31 = GC + np.array([0.80, 0.60]) * 2.5 * KM_MLY
M33 = GC + np.array([0.62, 0.86]) * 2.73 * KM_MLY
VIRGO = GC + np.array([-0.55, -0.83]) * 54 * KM_MLY
GA = GC + np.array([-0.98, 0.20]) * 220 * KM_MLY
PLANETS = [("MERCURY", 0.387, 0xc2c3c7, 2.1), ("VENUS", 0.723, 0xfff1a8, 4.0), ("MARS", 1.524, 0xef7d57, 5.2),
           ("JUPITER", 5.203, 0xffcd75, 0.9), ("SATURN", 9.537, 0xffb347, 2.6), ("URANUS", 19.19, 0x9fe4ff, 3.7),
           ("NEPTUNE", 30.07, 0x5fb8f0, 1.4)]  # name, AU, colour, angle on the orbit (drawn, not the date's)
STARS = [("ALPHA CEN", 4.37, 315.7, -0.7), ("BARNARD'S", 5.96, 31.0, 14.1), ("WOLF 359", 7.86, 244.1, 56.1),
         ("SIRIUS", 8.6, 227.2, -8.9), ("EPS ERIDANI", 10.5, 195.8, -48.1), ("PROCYON", 11.4, 213.7, 13.0),
         ("61 CYGNI", 11.4, 82.3, -5.8), ("TAU CETI", 11.9, 173.1, -73.4), ("ROSS 128", 11.0, 270.4, 59.6),
         ("EPS INDI", 11.9, 336.2, -48.0), ("ROSS 154", 9.7, 11.3, -10.3), ("LALANDE 21185", 8.3, 185.1, 65.4)]
LABELLED = {"ALPHA CEN", "SIRIUS", "BARNARD'S"}


def gal_dir(l_deg):
    """a direction on the galactic plane: longitude 0 points at the centre, counter-clockwise on screen"""
    ang = math.atan2(GC_DIR[1], GC_DIR[0]) - math.radians(l_deg)
    return np.array([math.cos(ang), math.sin(ang)])


@lru_cache(1)
def galaxy():
    """the Milky Way from above: a bar, two major and two minor arms, the disc; positions in km from Earth, colours"""
    rng = np.random.default_rng(7)
    pts, cols = [], []
    n = 70000
    for arm, (phase, weight) in enumerate(((0, 1.0), (math.pi, 1.0), (math.pi / 2, 0.45), (3 * math.pi / 2, 0.45))):
        m = int(n * 0.2 * weight)
        th = rng.uniform(0.0, 7.4, m)
        r = 6500 * np.exp(0.26 * th) + rng.normal(0, 900, m)
        a = th + phase + rng.normal(0, 0.12, m)
        pts.append(np.stack([r * np.cos(a), r * np.sin(a)], 1))
        cols.append(np.where(rng.random(m) < 0.75, 1, 2))
    m = int(n * 0.18)
    r = np.abs(rng.normal(0, 3200, m))
    a = rng.uniform(0, 2 * math.pi, m)
    bar = np.stack([r * np.cos(a) * 1.0, r * np.sin(a) * 0.45], 1)
    pts.append(bar)
    cols.append(np.full(m, 3))
    m = int(n * 0.2)
    r = np.sqrt(rng.uniform(0, 1, m)) * 50000
    a = rng.uniform(0, 2 * math.pi, m)
    pts.append(np.stack([r * np.cos(a), r * np.sin(a)], 1))
    cols.append(np.full(m, 0))
    p = np.concatenate(pts) * KM_LY  # ly -> km, centred on the galactic centre
    # turn the disc so an arm passes near the Sun (26,000 ly from the centre, opposite GC_DIR)
    ang = math.atan2(-GC_DIR[1], -GC_DIR[0]) - (math.log(26000 / 6500) / 0.26 + 0.25)
    c, s = math.cos(ang), math.sin(ang)
    p = p @ np.array([[c, s], [-s, c]])
    return p + GC, np.concatenate(cols)


@lru_cache(1)
def clusters():
    """galaxies beyond our own: the Local Group's dwarfs, then the cosmic web: knots of galaxy clusters joined by
    filaments, Laniakea's knots (the Great Attractor, Virgo) among them. The places are drawn; the sizes and the
    distances named on screen are the real ones."""
    rng = np.random.default_rng(13)
    pts, br = [], []
    m = 90  # the Local Group's dwarf galaxies, within a few Mly of the middle between us and Andromeda
    mid = (GC + M31) / 2
    r = np.abs(rng.normal(0, 1.7, m)) * KM_MLY
    a = rng.uniform(0, 2 * math.pi, m)
    pts.append(mid + np.stack([r * np.cos(a), r * np.sin(a)], 1))
    br.append(rng.uniform(0.6, 1.0, m))
    # the web: knots (Laniakea's own placed at their distances, the rest scattered), each joined to its nearest few
    nodes = [GA, VIRGO, GA + np.array([70, -60]) * KM_MLY, GA + np.array([-40, 90]) * KM_MLY]
    sizes = [16, 7, 9, 8]
    while len(nodes) < 34:
        q = GA + rng.uniform(-700, 700, 2) * KM_MLY
        if min(np.hypot(*(q - n)) for n in nodes) > 90 * KM_MLY:
            nodes.append(q)
            sizes.append(rng.uniform(3, 9))
    nodes = np.array(nodes)
    for i, n in enumerate(nodes):
        k = int(80 * sizes[i])
        pts.append(n + rng.normal(0, sizes[i] * 0.6 * KM_MLY, (k, 2)))
        br.append(rng.uniform(0.3, 0.8, k))
        d = np.hypot(*(nodes - n).T)
        for j in np.argsort(d)[1:4]:
            if j < i and d[j] > 0:
                continue
            s_ = rng.uniform(0, 1, int(d[j] / KM_MLY * 1.4))
            seg = n[None] + (nodes[j] - n)[None] * s_[:, None]
            perp = np.array([-(nodes[j] - n)[1], (nodes[j] - n)[0]])
            seg += perp[None] * (np.sin(s_ * math.pi) * rng.normal(0, 0.18))[:, None]
            seg += rng.normal(0, 5 * KM_MLY, seg.shape)
            pts.append(seg)
            br.append(rng.uniform(0.15, 0.45, len(s_)))
    m = 2500  # field galaxies between the filaments
    pts.append(GA + rng.uniform(-750, 750, (m, 2)) * KM_MLY)
    br.append(rng.uniform(0.08, 0.25, m))
    return np.concatenate(pts), np.concatenate(br)


@lru_cache(1)
def local_stars():
    """stars around the Sun out to 3,000 ly (a field, for the scales between the nearest stars and the galaxy)"""
    rng = np.random.default_rng(11)
    m = 30000
    r = np.sqrt(rng.uniform(0, 1, m)) * 3000 * KM_LY
    a = rng.uniform(0, 2 * math.pi, m)
    return SUN + np.stack([r * np.cos(a), r * np.sin(a)], 1), rng.uniform(0.3, 1.0, m)


@lru_cache(1)
def oort():
    rng = np.random.default_rng(5)
    m = 5000
    r = np.exp(rng.uniform(math.log(2000), math.log(100000), m)) * KM_AU
    a = rng.uniform(0, 2 * math.pi, m)
    return SUN + np.stack([r * np.cos(a), r * np.sin(a)], 1)


@lru_cache(1)
def bg_stars():
    rng = np.random.default_rng(3)
    return rng.uniform(0, 1, (160, 2)) * [W, H], rng.uniform(0.25, 1.0, 160)


# ---------- drawing into the 320x180 float picture
def plot(img, xy, rgb, k=1.0, add=True):
    xy = np.round(xy).astype(int)
    ok = (xy[:, 0] >= 0) & (xy[:, 0] < W) & (xy[:, 1] >= 0) & (xy[:, 1] < H)
    xy = xy[ok]
    k = (k[ok] if np.ndim(k) else np.full(len(xy), k))[:, None]
    col = np.array(rgb, np.float32)[None] * k
    if add:
        np.add.at(img, (xy[:, 1], xy[:, 0]), col)
    else:
        img[xy[:, 1], xy[:, 0]] = col


def rgb(c):
    return np.array([(c >> 16) & 255, (c >> 8) & 255, c & 255], np.float32)


def ring(img, centre, r, colour, k, dots=3):
    n = max(24, int(2 * math.pi * r / dots))
    if r < 1.5 or r > 4 * W:
        return
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    plot(img, np.stack([centre[0] + r * np.cos(a), centre[1] + r * np.sin(a)], 1), rgb(colour), k, add=False)


def disc(img, centre, r, lit, t, kind):
    """a shaded sphere: Earth (seas, land, ice, clouds, the night side's cities, the atmosphere's rim) or the Moon"""
    cx, cy = centre
    if r < 1.2:  # a dot, with a cross of dimmer pixels so it survives the dither
        c0 = rgb(0x9fe4ff if kind == "earth" else 0xffffff)
        plot(img, np.array([[cx, cy]]), c0, 1.0, add=False)
        plot(img, np.array([[cx - 1, cy], [cx + 1, cy], [cx, cy - 1], [cx, cy + 1]]), c0, 0.45, add=False)
        return
    x0, x1 = max(0, int(cx - r - 3)), min(W, int(cx + r + 4))
    y0, y1 = max(0, int(cy - r - 3)), min(H, int(cy + r + 4))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    nx, ny = (xx + 0.5 - cx) / r, (yy + 0.5 - cy) / r
    d2 = nx * nx + ny * ny
    inside = d2 <= 1
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    light = np.clip(nx * lit[0] + ny * lit[1] + nz * 0.35, 0, 1)
    reg = img[y0:y1, x0:x1]
    if kind == "moon":
        col = rgb(0x94b0c2)[None, None] * (0.12 + 0.95 * light[..., None])
        reg[inside] = col[inside]
        return
    spin = t * 0.08
    px, pz = nx * math.cos(spin) + nz * math.sin(spin), -nx * math.sin(spin) + nz * math.cos(spin)
    py = ny
    n = (np.sin(px * 3.1 + 1.3) * np.sin(py * 2.7 - 0.4) * np.sin(pz * 2.3 + 2.1)
         + 0.55 * np.sin(px * 6.3 - pz * 4.1 + 0.7) * np.sin(py * 5.2 + px * 2.0)
         + 0.25 * np.sin(px * 13.0 + py * 9.0) * np.sin(pz * 11.0 - py * 7.0))
    land = n > 0.12
    ice = np.abs(py) > 0.86
    cloud = (np.sin(px * 7.0 + py * 4.0 + t * 0.15) * np.sin(pz * 6.0 - py * 5.0) + 0.4 * np.sin(px * 15 + pz * 12)) > 0.75
    base = np.where(land[..., None], np.where((n > 0.45)[..., None], rgb(0x257179), rgb(0x38b764)), rgb(0x26407a))
    base = np.where(ice[..., None], rgb(0xc2c3c7), base)
    base = np.where(cloud[..., None], rgb(0xc2c3c7) * 0.95, base)
    day = base * (0.08 + 1.0 * light[..., None])
    night = (light < 0.05) & land & ~ice & (np.sin(px * 91 + py * 57) * np.sin(pz * 77 - px * 43) > 0.8)
    day = np.where(night[..., None], rgb(0xffcd75) * 0.9, day)
    reg[inside] = day[inside]
    rim = (d2 > 1) & (d2 < (1 + 2.2 / r) ** 2)
    reg[rim] = np.maximum(reg[rim], rgb(0x3c8ad8) * 0.8 * np.clip(0.4 + light[rim][..., None] * 2, 0, 1))


def text(img, s, x, y, colour=F.AMBER, a=1.0):
    return F.stamp(img, s, x, y, colour, a)


def scale_bar(img, L, a):
    """a round length near a quarter of the width, in km, AU or light years"""
    width_km = 10 ** L
    target = width_km / 4
    if target < 2e6:
        unit, u = "KM", 1.0
    elif target < 3e12:
        unit, u = "AU", KM_AU
    elif target < 3e6 * KM_LY:
        unit, u = "LY", KM_LY
    else:
        unit, u = "MLY", KM_MLY
    v = target / u
    e = 10 ** math.floor(math.log10(v))
    nice = max([m * e for m in (1, 2, 5) if m * e <= v] or [e])
    px = nice * u / width_km * W
    x0, y0 = 10, H - 14
    img[y0:y0 + 1, x0:x0 + int(px)] = rgb(F.CYAN)
    img[y0 - 3:y0 + 4, x0:x0 + 1] = rgb(F.CYAN)
    img[y0 - 3:y0 + 4, x0 + int(px) - 1:x0 + int(px)] = rgb(F.CYAN)
    label = f"{nice:,.0f} {unit}" if nice >= 1 else f"{nice:g} {unit}"
    text(img, label, x0 + int(px) + 6, y0 - 4, F.CYAN, a)


def scene(t):
    L, vel = view(t)
    width = 10 ** L
    k = W / width  # px per km
    w_sun = smooth(L, 7.9, 9.4)
    w_gal = smooth(L, 16.2, 17.9)
    w_lan = smooth(L, 20.6, 21.9)
    cam = SUN * w_sun + (GC - SUN) * w_gal + (GA - GC) * 0.45 * w_lan
    cam = cam + np.array([6371 * 0.55, 0]) * smooth(t, 163.1, 163.7)  # Earth's night side for the cut to s109

    def scr(p):
        return np.stack([W / 2 + (p[..., 0] - cam[0]) * k, H / 2 + (p[..., 1] - cam[1]) * k], -1)

    img = np.zeros((H, W, 3), np.float32)
    img[:] = rgb(0x0b0b1e) * 0.6
    # the far stars hold still; a step stretches them into streaks from the centre (the zoom's motion)
    bs, bk = bg_stars()
    fade_bg = 1 - smooth(L, 15.0, 16.5)
    if fade_bg > 0:
        plot(img, bs, rgb(0x94b0c2), bk * 0.8 * fade_bg)
        if abs(vel) > 0.5:
            d = bs - [W / 2, H / 2]
            for s in np.linspace(0, 0.12 * np.sign(vel), 5):
                plot(img, [W / 2, H / 2] + d * (1 + s), rgb(0x5fb8f0), bk * 0.35 * fade_bg)
    # the Milky Way and the stars around the Sun
    g_w = smooth(L, 15.2, 16.6) * (1 - 0.97 * smooth(L, 18.7, 19.6))
    if g_w > 0:
        gp, gc = galaxy()
        cols = np.array([rgb(0x26407a), rgb(0x9fe4ff), rgb(0x5fb8f0), rgb(0xffcd75)])
        s = scr(gp)
        dens = 0.35 * g_w * min(1.0, 10 ** (18.3 - L) * 0.6)
        for ci in range(4):
            m = gc == ci
            plot(img, s[m], cols[ci], dens * (2.2 if ci == 3 else 1.0))
    labels = []
    c_w = smooth(L, 18.6, 19.6)
    if c_w > 0:
        cp, cb = clusters()
        plot(img, scr(cp), rgb(0xc2c3c7), cb * c_w * 0.8)
        g_l = c_w * (1 - smooth(L, 20.9, 21.5))
        for pos, rad, tilt, colour in ((M31, 4.0, 0.45, 0xfff1a8), (M33, 2.0, 0.7, 0x9fe4ff), (GC, 3.0, 1.0, 0xfff1a8)):
            if g_l > 0:  # the big three as small tilted discs, bright in the middle (drawn bigger than life to be seen)
                q = scr(pos)
                yy, xx = np.mgrid[-6:7, -6:7].astype(np.float32)
                ca, sa = math.cos(0.6), math.sin(0.6)
                u, v = xx * ca + yy * sa, -xx * sa + yy * ca
                sm = np.exp(-(u ** 2 / rad ** 2 + v ** 2 / (rad * tilt) ** 2) * 2.2)
                plot(img, np.stack([q[0] + xx.ravel(), q[1] + yy.ravel()], 1), rgb(colour), sm.ravel() * g_l * 1.3)
        if 19.7 < L < 20.9:
            labels += [("LOCAL GROUP", np.array([W / 2, 14.0]), F.CYAN),
                       ("ANDROMEDA 2.5 MLY", scr(M31) + [0, 6], F.AMBER), ("MILKY WAY", scr(GC) + [0, 6], F.AMBER)]
        if L > 21.5:
            labels += [("LANIAKEA 520 MLY", np.array([W / 2, 14.0]), F.CYAN),
                       ("VIRGO CLUSTER", scr(VIRGO) + [0, 6], F.AMBER)]
    l_w = smooth(L, 12.8, 13.8) * (1 - smooth(L, 16.6, 17.4))
    if l_w > 0:
        lp, lb = local_stars()
        plot(img, scr(lp), rgb(0xe0e4f0), lb * l_w * 1.3)
    # the nearest stars, at their distances
    n_w = smooth(L, 13.2, 13.9) * (1 - smooth(L, 15.2, 15.9))
    if n_w > 0:
        for name, d, l_deg, b_deg in STARS:
            p = scr(SUN + gal_dir(l_deg) * d * math.cos(math.radians(b_deg)) * KM_LY)
            plot(img, p[None], rgb(0xffffff), n_w, add=False)
            if name in LABELLED and n_w > 0.6 and 14.0 < L < 14.6:
                labels.append((f"{name} {d:g} LY", p, F.AMBER))
    # the Oort cloud
    o_w = smooth(L, 11.4, 12.4) * (1 - smooth(L, 13.9, 14.5))
    if o_w > 0:
        plot(img, scr(oort()), rgb(0x566c86), 0.6 * o_w)
        if 12.6 < L < 13.5:
            labels.append(("OORT CLOUD", scr(SUN + np.array([0, -60000 * KM_AU])), F.CYAN))
    # the planets' orbits and the Sun
    sun = scr(SUN)
    p_w = smooth(L, 7.6, 8.3) * (1 - smooth(L, 11.6, 12.4))
    if p_w > 0:
        for name, au, colour, ang in PLANETS + [("EARTH", 1.0, 0x5fb8f0, math.pi)]:
            r = au * KM_AU * k
            ring(img, sun, r, 0x1d2b53 if name != "EARTH" else 0x26407a, p_w)
            if name != "EARTH":
                plot(img, (sun + r * np.array([math.cos(ang), math.sin(ang)]))[None], rgb(colour), p_w, add=False)
    s_w = smooth(L, 7.2, 8.0) * (1 - smooth(L, 15.4, 16.2))
    if s_w > 0 and -40 < sun[0] < W + 40 and -40 < sun[1] < H + 40:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r_sun = max(1.2, 696000 * k)
        d = np.hypot(xx + 0.5 - sun[0], yy + 0.5 - sun[1])
        glow = np.clip((r_sun * 2.5 / np.maximum(d, 0.5)) ** 1.6, 0, 1) * s_w
        img += rgb(0xfff1a8)[None, None] * glow[..., None]
        if 8.2 < L < 10.9:
            labels.append(("SUN", sun + [0, r_sun + 6], F.AMBER))
    # the Moon and its orbit
    m_w = smooth(L, 5.3, 5.9) * (1 - smooth(L, 8.4, 9.0))
    moon = np.array([math.cos(3.6), math.sin(3.6)]) * 384400
    if m_w > 0:
        ring(img, scr(np.zeros(2)), 384400 * k, 0x26407a, m_w)
        disc(img, scr(moon), 1737 * k, (-1, 0), t, "moon")
        if 5.9 < L < 7.4:
            labels.append(("MOON", scr(moon) + [0, max(4, 1737 * k) + 4], F.AMBER))
    # Earth, and the battle glittering in orbit around it
    e = scr(np.zeros(2))
    R = 6371 * k
    disc(img, e, R, (-0.95, -0.15), t, "earth")
    if L < 6.0:
        rng = np.random.default_rng(int(t * 24))
        m = 140
        a = rng.uniform(0, 2 * math.pi, m)
        rr = R * rng.uniform(1.08, 1.7, m)
        sp = np.stack([e[0] + rr * np.cos(a), e[1] + rr * np.sin(a)], 1)
        on = rng.random(m) < 0.45
        plot(img, sp[on], rgb(0xffffff), 1.0 - smooth(L, 5.2, 6.0), add=False)
        plot(img, sp[~on][: m // 5], rgb(0xffb347), 1.0 - smooth(L, 5.2, 6.0), add=False)
    if L < 5.6 and t < 163.5:
        labels.append(("EARTH", e + [0, R + 7], F.AMBER))
    elif L > 7.4 and not (L < 8.6 and p_w < 0.3):
        mk = 1.0 if int(t * 4) % 2 == 0 else 0.6  # Earth's place, kept at every scale
        x, y = int(round(e[0])), int(round(e[1]))
        for dx, dy in ((-2, 0), (-1, 0), (1, 0), (2, 0), (0, -2), (0, -1), (0, 1), (0, 2)):
            if 0 <= x + dx < W and 0 <= y + dy < H:
                img[y + dy, x + dx] = rgb(F.CLAY) * mk
        if 16.5 < L < 19.0:
            labels.append(("EARTH", e + [0, 5], F.CLAY))
    if 17.2 < L < 19.0:
        labels.append(("MILKY WAY", scr(GC) + [0, -int(56000 * KM_LY * k)], F.CYAN))
    return img, labels, L


def zoom_picture(img_in, t, F):
    small, labels, L = scene(t)
    q = F.quantize(small)
    for s, p, colour in labels:  # type after the dither, in the palette's own colours
        x = int(np.clip(p[0] - len(s) * 4, 2, W - len(s) * 8 - 2))
        y = int(np.clip(p[1], 2, H - 22))
        text(q, s, x, y, colour)
    scale_bar(q, L, 1.0)
    if abs(t - 157.76) < 0.05:  # the accent at the galaxy: one frame of phosphor flare
        q = np.clip(q * 1.6 + 30, 0, 255)
    return F.crt(q, img_in.shape[0], img_in.shape[1])


# ================= the rest of the section (end, 12 Nov) =================
import subprocess  # noqa: E402

import cv2  # noqa: E402
import skia  # noqa: E402


def picture(img_in, t, F):
    """only the zoom's gap makes its own picture; the shots in RANGES keep theirs"""
    if GAP["t0"] <= t < GAP["t1"]:
        return zoom_picture(img_in, t, F)
    return img_in


def take_time(p, src):
    """song time at which a take's own time `src` plays in this piece (inverse of F.src_t)"""
    return p["start"] + (src - p["in"]) / (p.get("speed") or 1)


# ---------- s068-s073: the launch-control readout
# the events in s068's take (s068-b-a), measured in its frames (log): the key turns by 0.50 s, the six switch lamps
# light at 0.79 s (no lit lamp before frame 19, a dozen from frame 20), the button glows red at 2.58 s (frame 62)
KEY_SRC, LAMPS_SRC, PRESS_SRC = 0.50, 0.79, 2.58
SITE = {"s069": "DESERT", "s070": "TUNDRA", "s071": "MOUNTAIN", "s072": "ISLAND"}  # the board's places for the takes
PX, COLS = 3, 21  # 8x8 glyphs scaled x3: 24 units a character, 21 columns
PANEL_X, PANEL_Y = 56, 56
DARK = 0x0b0b1e


def launch_window():
    """(start, end, s068's piece, [(t0, t1, shot) of each silo shot, in cut order], s073's start) or None"""
    ps = [(a, b, p, F.shot_of(p)) for s in LAUNCH_SHOTS for a, b, p in F.spans(s)]
    if not ps:
        return None
    ps.sort(key=lambda x: x[0])
    key = next((x for x in ps if x[3] == "s068"), None)
    silos = [(a, b, s) for a, b, _, s in ps if s in SITE]
    earth = next((a for a, b, _, s in ps if s == "s073"), None)
    return ps[0][0], ps[-1][1], key, silos, earth


def typed(s, t, t0, cps=60.0):
    """s typed in from t0 at cps characters a second"""
    return s[:max(0, min(len(s), int((t - t0) * cps)))]


def lr(label, status=""):
    """a row: the label left, the status right-aligned to the panel's width"""
    return label + status.rjust(COLS - len(label)) if status else label


def panel_rows(t):
    """[(text, colour, inverse?)] of the readout at song time t; typed in as each event happens"""
    a0, a1, key, silos, earth = launch_window()
    if key:
        p = key[2]
        k_t, l_t, b_t = take_time(p, KEY_SRC), take_time(p, LAMPS_SRC), take_time(p, PRESS_SRC)
    else:  # s068 trimmed out: the sequence starts launched
        k_t = l_t = b_t = a0
    rows = [(typed(lr("LAUNCH CONTROL"), t, a0, 120), F.RED, True)]
    rows.append((typed(lr("KEY 1", "ARMED" if t >= k_t else "SAFE"), t, a0 + 0.04, 120), F.RED if t >= k_t else F.AMBER, False))
    rows.append((typed(lr("ENABLE", "ON" if t >= l_t else "OFF"), t, a0 + 0.08, 120), F.AMBER, False))
    if t < b_t:
        d = b_t - t
        rows.append((typed(lr("LAUNCH", f"T-00:{d:04.1f}"), t, a0 + 0.12, 120), F.AMBER, False))
    else:
        d = t - b_t
        on = int(d * 6) % 2 == 0 and d < 0.6
        rows.append((lr("LAUNCH", f"T+{int(d // 60):02d}:{d % 60:04.1f}"), F.RED, on))
    rows.append(("", F.AMBER, False))
    for n, (s0, s1, shot) in enumerate(silos):
        if t >= s0:
            rows.append((typed(lr(f"SILO {n + 1:02d} {SITE[shot]}", "AWAY" if t >= s0 + 0.2 else "OPEN"), t, s0, 140),
                         F.AMBER, False))
    if earth is not None and t >= earth:
        rows.append((typed(lr("ALL SILOS", "AWAY"), t, earth, 140), F.RED, int((t - earth) * 4) % 2 == 0))
    n_rows = 5 + len(silos) + (earth is not None)  # the box keeps its size: empty rows wait for their silo
    return rows + [("", F.AMBER, False)] * (n_rows - len(rows))


def text_layer(rows, rgb_dim=1.0):
    """the rows as an RGBA pixel image (glyph pixels only, 8x8 font), each pixel row's last line dimmed (scanlines in
    the letters only, Lati 12 Nov) after scaling x PX"""
    h = len(rows) * 11 + 6
    w = COLS * 8 + 8
    rgbi = np.zeros((h, w, 3), np.float32)
    mask = np.zeros((h, w, 3), np.float32)
    for i, (s, colour, inv) in enumerate(rows):
        y = 4 + i * 11
        if inv and s:  # inverse video: a block of the colour, the letters cut out of it
            bar = np.array([(colour >> 16) & 255, (colour >> 8) & 255, colour & 255], np.float32)
            bw = min(w - 4, len(s) * 8 + 4)
            rgbi[y - 1:y + 9, 2:2 + bw] = bar
            mask[y - 1:y + 9, 2:2 + bw] = 255
            F.stamp(rgbi, s, 4, y, DARK, shadow=False)
        else:
            F.stamp(rgbi, s, 4, y, colour, shadow=False)
            F.stamp(mask, s, 4, y, 0xffffff, shadow=False)
    a = mask[..., 0] / 255
    big = np.kron(rgbi, np.ones((PX, PX, 1), np.float32))
    ab = np.kron(a, np.ones((PX, PX), np.float32))
    ab[PX - 1::PX] *= 0.35
    rgba = np.dstack([big * rgb_dim, ab * 255]).clip(0, 255).astype(np.uint8)
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)


def launch_panel(c, t):
    lw = launch_window()
    if not lw or not (lw[0] <= t < lw[1]):
        return
    a0, a1 = lw[0], lw[1]
    rows = panel_rows(t)
    img = text_layer(rows)
    w, h = img.width(), img.height()
    x, y = PANEL_X, PANEL_Y
    # the CRT switching on (a line opening to the box) on the first beat, and off at the cut to s075 (3 frames each)
    k = min(F.ease((t - a0) / (3 / 24)), F.ease((a1 - t) / (3 / 24)))
    cy = y + h / 2
    c.save()
    c.translate(0, cy)
    c.scale(1, max(0.03, k))
    c.translate(0, -cy)
    c.drawRect(skia.Rect.MakeXYWH(x - 10, y - 10, w + 20, h + 20), skia.Paint(Color=F.col(DARK, 0.62)))

    def frame_():
        F.brackets(c, x - 10, y - 10, w + 20, h + 20, F.RED, 0.9, arm=0.08, sw=2.2)
        c.drawLine(x - 10, y + 11 * PX * 1 + 2, x + w + 10, y + 11 * PX * 1 + 2, F.stroke(F.RED, 0.45, 1.4))
    F.glow_draw(c, frame_, blur=4, amount=0.5)
    c.drawImage(img, x, y, skia.SamplingOptions(), skia.Paint(Alphaf=0.6, ImageFilter=skia.ImageFilters.Blur(PX * 1.4, PX * 1.4)))
    c.drawImage(img, x, y)
    c.restore()


# ---------- s101: the track box on the battle ahead
@lru_cache(2)
def s101_track(file):
    """per frame of the take: (x, y, d) in 1920 units, the target found afresh in each frame (the fireball's warm
    mass, else the brightest spark above and right of the missile), then smoothed over the whole take: x, y over 5
    frames, the size (equivalent diameter of the warm mass) by a 7-frame median, then 5. -> (smoothed, raw)"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F.ROOT / file), "-vf", "scale=640:360", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 360, 640, 3)
    hh, ww = 360, 640
    det = []
    for im in fr:
        f = im.astype(np.float32)
        r, b = f[..., 0], f[..., 2]
        warm = ((r > 180) & (r - b > 50)).astype(np.uint8)
        warm[int(0.62 * hh):, :int(0.55 * ww)] = 0  # the missile's plume, lower left
        n, lab, st, cen = cv2.connectedComponentsWithStats(warm)
        j = 1 + int(np.argmax(st[1:, 4])) if n > 1 else 0
        if j and st[j, 4] >= 150:
            det.append((cen[j][0], cen[j][1], 2 * math.sqrt(st[j, 4] / math.pi)))
        else:
            br = f.mean(2)
            br[int(0.55 * hh):] = 0
            br[:, :int(0.4 * ww)] = 0
            s = cv2.GaussianBlur(br, (0, 0), 4)
            yy, xx = np.unravel_index(s.argmax(), s.shape)
            det.append((float(xx), float(yy), 0.0))
    d = np.array(det, np.float64) * 3  # 640 -> 1920 units
    sm = d.copy()
    k5 = np.ones(5) / 5
    for i in (0, 1):
        sm[:, i] = np.convolve(np.pad(d[:, i], 2, mode="edge"), k5, "valid")
    med = np.array([np.median(d[max(0, i - 3):i + 4, 2]) for i in range(len(d))])
    sm[:, 2] = np.convolve(np.pad(med, 2, mode="edge"), k5, "valid")
    return sm, d


def missile_hud(c, t):
    sp = [s for s in F.spans("s101") if s[0] <= t < s[1]]
    if not sp:
        return
    a0, a1, p = sp[0]
    sm, _ = s101_track(p["file"])
    fi = F.src_t(p, t) * 24
    i0 = int(np.clip(np.floor(fi), 0, len(sm) - 1))
    i1 = min(i0 + 1, len(sm) - 1)
    u = float(np.clip(fi - i0, 0, 1))
    x, y, d = sm[i0] * (1 - u) + sm[i1] * u
    # closing on the beats: from the shot's first beat, four steps down to the target's own size
    bts = [b for b in F.BEATS if a0 - 0.06 <= b < a1][:4]
    n_in = sum(1 for b in bts if t >= b)
    if n_in == 0:
        return
    steps = [520, 360, 220, 0]
    i = n_in - 1
    prev = steps[i - 1] if i else 700
    close = prev + (steps[i] - prev) * F.ease((t - bts[i]) / 0.14)
    side = max(110.0, d * 1.1 + 40, close)
    a = 1 - smooth(d, 400, 470)  # fades as the fireball fills the frame, before the ships cross it
    if a <= 0.01:
        return
    entry = F.ease((t - bts[0]) / 0.1)
    a *= entry
    blink = 1.0 if (close > 1 or int(t * 10) % 2 == 0) else 0.7
    rng = 1 - (t - a0) / max(0.1, a1 - a0)  # the range closing over the shot: the fiction's own, no figure

    def draw():
        h2 = side / 2
        F.brackets(c, x - h2, y - h2, side, side, F.RED, a * blink, arm=0.22, sw=2.6)
        c.drawLine(x - 14, y, x - 5, y, F.stroke(F.RED, a, 2))
        c.drawLine(x + 5, y, x + 14, y, F.stroke(F.RED, a, 2))
        c.drawLine(x, y - 14, x, y - 5, F.stroke(F.RED, a, 2))
        c.drawLine(x, y + 5, x, y + 14, F.stroke(F.RED, a, 2))
        F.hud_text(c, "TRACK", x - h2 + (0 if y - h2 - 12 >= 30 else 10), max(y - h2 - 12, y - h2 + 30, 30), size=24, color=F.RED, a=a)
        # a range tape under the box: ticks, and a bar that shortens as the missile closes
        bx, by, bw = x - h2, y + h2 + 16, side
        c.drawRect(skia.Rect.MakeXYWH(bx, by, bw * max(0.0, rng), 6), skia.Paint(Color=F.col(F.AMBER, 0.85 * a)))
        for k in range(11):
            c.drawLine(bx + bw * k / 10, by + 9, bx + bw * k / 10, by + (16 if k % 5 == 0 else 12), F.stroke(F.AMBER, 0.7 * a, 1.6))
        F.hud_text(c, "RNG", bx + bw + 10, by + 12, size=18, color=F.AMBER, a=0.85 * a)
    F.glow_draw(c, draw, blur=5, amount=0.6)


def world(c, t, F):
    shot, _ = F.shot_at(t)
    if shot == "s101":
        missile_hud(c, t)


def over(c, t, F):
    shot, _ = F.shot_at(t)
    if shot in LAUNCH_SHOTS:
        launch_panel(c, t)
