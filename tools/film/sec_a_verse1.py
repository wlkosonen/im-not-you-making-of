#!/usr/bin/env python3
"""Section A, verse 1 and the pre-chorus (song 0-44.69): a terminal printing film 3's first nine days.

Agent A (verse1) for Claude (Kiln, local), 12 Nov 2026. notes/agents/verse1.md has the design and the record behind
every entry. One scrollback in the centre prints, on the beat nearest its moment in the record: Lati's notes (a few
that turned the film, verbatim, cut only with an ellipsis), a few Kiln replies in clay, a line per day with that day's
calls and commits, and the work as a terminal would show images: framed, dithered to the main film's palette,
scanlined, printed row by row, captioned with their real paths; Lati's picks frame in amber, the rest dim, rejections
in red. At board v2 the scrollback scrolls away and the board takes the centre, filling from film 3's board.json as it
stood at each commit of 9 Nov (read with `git show`, read-only). From 44.30 the centre goes quiet for the drop.

Every frame is a pure function of t and the record; the caches below (media/verse1/cache) only hold decoded pixels.
"""
import hashlib
import json
import re
import subprocess
import textwrap
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

RANGES = [(0.0, 44.69)]

FILM = Path("/home/shegs/Im not you")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = ROOT / "media/verse1/cache"

VX0, VX1, VY0, VY1 = 300, 1140, 160, 785  # the viewport (the summary line's spot at y ~810 stays clear)
VW, VH = VX1 - VX0, VY1 - VY0
T_BOARD = 37.50   # board v2 (6c19350, 9 Nov 14:34:42Z, song 37.31) on the next beat
T_QUIET = 44.30   # the centre fades out by 44.55: the compaction (44.47) and the drop (44.69) land on an empty centre
PANE_Y = 655      # under the board: Lati's last notes of the stretch

QPX, QROWS, QLH = 2, 11, 30   # quote letters (px, rows, line height)
SPX, SROWS, SLH = 2, 9, 26    # small letters: headers, captions, day lines
QCHARS = 49                   # quote line width in characters (16 units each at rows 11; the indent is extra)

B = None  # the base module, set by draw()


# ---------- small helpers
def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def col(rgb, a=1.0):
    return skia.Color(rgb >> 16 & 255, rgb >> 8 & 255, rgb & 255, int(255 * max(0.0, min(1.0, a))))


def stroke(rgb, a=1.0, w=1.5):
    return skia.Paint(Color=col(rgb, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w)


def utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def stamp_local(u):
    return datetime.fromtimestamp(u, B.EET).strftime("%a %d %b %H:%M").upper()


@lru_cache(1)
def notes():
    return {r["decisions_line"]: r for r in B.rows("notes")}


def wrap(text, n):
    return textwrap.wrap(text, n, break_on_hyphens=False, break_long_words=False)


def excerpt(line, start=None, end=None):
    """Lati's words exactly as notes.json has them; cut only at the ends, each cut marked with an ellipsis"""
    q = notes()[line]["quote"]
    i = q.index(start) if start else 0
    j = q.index(end, i) + len(end) if end else len(q)
    return ("… " if i > 0 else "") + q[i:j].strip() + (" …" if j < len(q) else "")


# ---------- pictures: the main film's pixel voice (32-colour palette, Bayer dither), scanlines inside the pixels
def _key(*a):
    return hashlib.sha1("|".join(map(str, a)).encode()).hexdigest()[:20]


def _fill(img, gw, gh):
    import cv2
    h, w = img.shape[:2]
    a = gw / gh
    if w / h > a:
        nw = int(h * a)
        img = img[:, (w - nw) // 2:(w - nw) // 2 + nw]
    else:
        nh = int(w / a)
        img = img[(h - nh) // 2:(h - nh) // 2 + nh]
    return cv2.resize(img, (gw, gh), interpolation=cv2.INTER_AREA)


@lru_cache(2048)
def small(path, gw, gh):
    """the picture at gw x gh pixels, filled (centre crop), dithered to the palette; cached on disk"""
    f = CACHE / "pix" / f"{_key(path, gw, gh)}.npy"
    if f.exists():
        return np.load(f)
    import cv2
    img = cv2.imread(str(FILM / path), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    q = B.G.quantize(_fill(img, gw, gh), spread=26.0).astype(np.uint8)
    f.parent.mkdir(parents=True, exist_ok=True)
    np.save(f, q)
    return q


def to_image(sm, px):
    """pixels scaled up by px (in 1920 units), the last row of each pixel dimmed (the scanline)"""
    big = np.kron(sm.astype(np.float32), np.ones((px, px, 1), np.float32))
    if px >= 3:
        big[px - 1::px] *= 0.45
    rgba = np.dstack([big.astype(np.uint8), np.full(big.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)


@lru_cache(2048)
def pic(path, w, h, px):
    return to_image(small(path, w // px, h // px), px)


@lru_cache(4)
def clip_frames(path, src0, dur, gw, gh):
    """an insert's frames (24 fps) from film 3's own take, decoded with ffmpeg, dithered; cached on disk"""
    f = CACHE / "clip" / f"{_key(path, src0, dur, gw, gh)}.npy"
    if not f.exists():
        import cv2
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{src0}", "-t", f"{dur}", "-i", str(FILM / path), "-r", "24",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                             "-of", "csv=p=0", str(FILM / path)], capture_output=True, text=True, check=True).stdout
        w, h = map(int, pr.strip().split(",")[:2])
        fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
        out = np.stack([B.G.quantize(_fill(x.astype(np.float32), gw, gh), spread=26.0).astype(np.uint8) for x in fr])
        f.parent.mkdir(parents=True, exist_ok=True)
        np.save(f, out)
    return np.load(f)


@lru_cache(64)
def clip_image(path, src0, dur, gw, gh, px, k):
    fr = clip_frames(path, src0, dur, gw, gh)
    return to_image(fr[min(k, len(fr) - 1)], px)


def grey_dim(dim=1.0, grey=0.0):
    lr, lg, lb = 0.299, 0.587, 0.114
    m = []
    for i in range(3):
        row = [((1 - grey) * (1.0 if j == i else 0.0) + grey * (lr, lg, lb)[j]) * dim for j in range(3)]
        m += row + [0.0, 0.0]
    m += [0.0, 0.0, 0.0, 1.0, 0.0]
    return skia.ColorFilters.Matrix(m)


def draw_pic(c, img, x, y, w, h, reveal=1.0, dim=1.0, grey=0.0, alpha=1.0):
    """a picture printed row by row (reveal 0..1), as a terminal streams an image"""
    if reveal <= 0 or alpha <= 0:
        return
    ih = img.height()
    rows = max(1, int(round(ih * min(1.0, reveal))))
    p = skia.Paint(Alphaf=alpha, ColorFilter=grey_dim(dim, grey) if (dim < 1 or grey > 0) else None)
    c.drawImageRect(img, skia.Rect(0, 0, img.width(), rows), skia.Rect(x, y, x + w, y + h * rows / ih),
                    skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if reveal < 1:  # the line being printed
        yy = y + h * rows / ih
        c.drawRect(skia.Rect(x, yy - 1.5, x + w, yy + 1), skia.Paint(Color=col(B.WHITE, 0.6 * alpha)))


# ---------- entries: each knows its start (song time), its height at t and how to draw itself at (x, y)
class Entry:
    t0 = 0.0

    def height(self, t):
        return 0.0

    def busy(self, t):  # still typing (the idle cursor waits)
        return False

    def draw(self, c, x, y, t, a):
        pass


class Quote(Entry):
    """Lati's words: a header (when, who), the words typing in, and optionally Kiln's reply in clay"""

    def __init__(self, t0, line, start=None, end=None, kiln=None, cps=150, who=None, note=None):
        self.t0, self.cps = t0, cps
        r = notes()[line]
        self.u = utc(r["ts"])
        self.head = f"{stamp_local(self.u)}  " + (who or ("LATI to FLINT" if r["to"] == "Flint" else "LATI"))
        self.text = excerpt(line, start, end)
        self.lines = wrap(self.text, QCHARS)
        self.kiln = wrap(kiln, QCHARS - 6) if kiln else []
        self.note = note  # a heading line (decisions.md, Kiln's words) in red, for what went wrong
        self.ls = []  # each line's start
        n = 0
        for ln in self.lines:
            self.ls.append(t0 + 0.12 + n / cps)
            n += len(ln) + 1
        self.t_end = t0 + 0.12 + n / cps
        self.ks = [self.t_end + 0.15 + 0.12 * k for k in range(len(self.kiln) + (1 if note else 0))]

    def busy(self, t):
        return t < self.t_end + 0.1

    def height(self, t):
        h = SLH * ease((t - self.t0) / 0.12)
        h += sum(QLH * ease((t - s) / 0.1) for s in self.ls)
        h += sum(SLH * ease((t - s) / 0.1) for s in self.ks)
        return h + 14 * ease((t - self.t0) / 0.12)

    def draw(self, c, x, y, t, a):
        if t < self.t0:
            return
        B.crt(c, self.head, x, y, px=SPX, rows_=SROWS, color=B.CYAN, alpha=0.7 * a, glow=False)
        yy = y + SLH
        typed = (t - self.t0 - 0.12) * self.cps
        n = 0
        settle = ease((t - self.t_end - 0.35) / 0.4)  # white while new, then amber
        for k, ln in enumerate(self.lines):
            if typed <= n:
                break
            part = ln[:max(0, int(typed - n))]
            colr = B.WHITE if settle < 0.5 else B.AMBER
            w = B.crt(c, "  " + part, x, yy, px=QPX, rows_=QROWS, color=colr, alpha=a)
            if typed < n + len(ln):  # the typing cursor
                c.drawRect(skia.Rect.MakeXYWH(x + w + 2, yy + 4, 11, QROWS * QPX + 2), skia.Paint(Color=col(B.AMBER, 0.9 * a)))
            n += len(ln) + 1
            yy += QLH
        for k, ln in enumerate(self.kiln):
            if t < self.ks[k]:
                return
            B.crt(c, ("KILN  " if k == 0 else "      ") + ln, x + 24, yy, px=SPX, rows_=SROWS, color=B.CLAY, alpha=0.95 * a)
            yy += SLH
        if self.note and t >= self.ks[-1]:
            B.crt(c, self.note, x + 24, yy, px=SPX, rows_=SROWS, color=B.RED, alpha=a)


class Day(Entry):
    """a day begins: its date, and its calls and commits counting as they happen (the quiet days stay at 0)"""

    def __init__(self, t0, day):
        self.t0 = t0
        d0 = datetime(2026, 11, day, tzinfo=B.EET).timestamp()
        self.span = (d0, d0 + 86400)
        self.label = datetime.fromtimestamp(d0, B.EET).strftime("%a %d %b").upper()

    def height(self, t):
        return 34 * ease((t - self.t0) / 0.12)

    def draw(self, c, x, y, t, a):
        if t < self.t0:
            return
        u = min(B.clock(t), self.span[1])
        ts, _ = B.calls()
        n = int(np.searchsorted(ts, u, side="right") - np.searchsorted(ts, self.span[0]))
        m = sum(1 for cu, _ in B.commits() if self.span[0] <= cu <= u)
        txt = f"── {self.label} ──  {n} call{'s' if n != 1 else ''} · {m} commit{'s' if m != 1 else ''}"
        B.crt(c, txt, x, y + 4, px=SPX, rows_=SROWS, color=B.CYAN, alpha=0.55 * a, glow=False)


class Grid(Entry):
    """a batch of pictures printed as a grid; picks frame in amber (the rest dim), rejects frame in red"""

    def __init__(self, t0, caption, files, cols, cw, ch, px=2, labels=None, gap=6, pick_t=None, picks=(),
                 rejects=(), reject_t=None, aside_t=None, count=None, flash=None):
        self.t0, self.caption, self.files = t0, caption, files
        self.cols, self.cw, self.ch, self.px, self.gap = cols, cw, ch, px, gap
        self.labels = labels
        self.pick_t, self.picks = pick_t, set(picks)
        self.rejects, self.reject_t = set(rejects), reject_t
        self.aside_t = aside_t   # the whole batch set aside (dims, frames go red)
        self.count = count       # text added to the caption when the picks land
        self.flash = flash or {}  # {index: t}: one cell lit later (a second pick)
        self.rows = (len(files) + cols - 1) // cols
        self.cell_h = ch + (SLH if labels else 0) + gap

    def height(self, t):
        return (SLH + self.rows * self.cell_h + 10) * ease((t - self.t0) / 0.18)

    def state(self, i, t):
        """(dim, grey, frame colour or None, frame alpha)"""
        dim, grey, fr, fa = 0.85, 0.0, None, 0.0
        if self.reject_t is not None and i in self.rejects and t >= self.reject_t:
            return 0.45, 0.6, B.RED, 0.95
        lit_t = self.flash.get(i) if i in self.flash else (self.pick_t if i in self.picks else None)
        if self.pick_t is not None and t >= self.pick_t:
            if lit_t is not None and t >= lit_t:
                dim, fr, fa = 1.0, B.AMBER, 1.0
            else:
                dim, grey = 0.32, 0.7
        if self.aside_t is not None and t >= self.aside_t:
            k = ease((t - self.aside_t) / 0.3)
            dim, grey = dim * (1 - 0.6 * k), grey + (1 - grey) * k
            if fr:
                fr, fa = B.RED, 0.5
        return dim, grey, fr, fa

    def draw(self, c, x, y, t, a):
        if t < self.t0:
            return
        cap = self.caption + (f"   {self.count}" if self.count and self.pick_t is not None and t >= self.pick_t else "")
        B.crt(c, cap, x, y, px=SPX, rows_=SROWS, color=B.CYAN, alpha=0.75 * a, glow=False)
        n = len(self.files)
        span = min(0.45, 0.02 * n + 0.1)
        for i, f in enumerate(self.files):
            r, k = divmod(i, self.cols)
            cx = x + k * (self.cw + self.gap)
            cy = y + SLH + r * self.cell_h
            ts = self.t0 + 0.08 + span * i / max(1, n)
            rev = (t - ts) / 0.12
            if rev <= 0:
                continue
            dim, grey, fr, fa = self.state(i, t)
            draw_pic(c, pic(f, self.cw, self.ch, self.px), cx, cy, self.cw, self.ch, reveal=rev, dim=dim, grey=grey, alpha=a)
            c.drawRect(skia.Rect.MakeXYWH(cx, cy, self.cw, self.ch), stroke(B.CYAN, 0.35 * a, 1.0))
            if fr:
                lit = self.flash.get(i, self.pick_t) if fr == B.AMBER else self.reject_t
                fl = 1 - ease((t - (lit or -9)) / 0.25)
                c.drawRect(skia.Rect.MakeXYWH(cx - 2, cy - 2, self.cw + 4, self.ch + 4), stroke(B.WHITE if fl > 0.5 else fr, fa * a, 2.2))
            if self.labels and self.labels[i]:
                B.crt(c, self.labels[i], cx, cy + self.ch + 4, px=SPX, rows_=SROWS,
                      color=fr if fr else B.CYAN, alpha=(0.9 if fr else 0.55) * a, glow=False)


class ClipQuote(Entry):
    """an insert from one of film 3's takes in a window (a beat to a bar), Lati's words beside it"""

    def __init__(self, t0, path, src0, dur, caption, line, start=None, end=None, kiln=None, w=300, h=168, px=3):
        self.t0, self.path, self.src0, self.dur, self.caption = t0, path, src0, dur, caption
        self.w, self.h, self.px = w, h, px
        self.q = _qlines(Quote(t0 + 0.25, line, start, end, kiln=kiln), 28)

    def busy(self, t):
        return self.q.busy(t)

    def height(self, t):
        return max(SLH + self.h + 14, SLH + self.q.height(t) + 4) * ease((t - self.t0) / 0.15)

    def draw(self, c, x, y, t, a):
        if t < self.t0:
            return
        B.crt(c, self.caption, x, y, px=SPX, rows_=SROWS, color=B.CYAN, alpha=0.75 * a, glow=False)
        d = t - self.t0
        k = int(d * 24)
        playing = d < self.dur
        img = clip_image(self.path, self.src0, self.dur, self.w // self.px, self.h // self.px, self.px, k)
        draw_pic(c, img, x, y + SLH, self.w, self.h, reveal=d / 0.1, dim=1.0 if playing else 0.6,
                 grey=0.0 if playing else 0.3, alpha=a)
        c.drawRect(skia.Rect.MakeXYWH(x, y + SLH, self.w, self.h), stroke(B.CYAN, 0.6 * a, 1.5))
        if playing and int(t * 3) % 2 == 0:
            c.drawCircle(x + self.w - 14, y + SLH + 14, 5, skia.Paint(Color=col(B.RED, 0.9 * a), AntiAlias=True))
        self.q.draw(c, x + self.w + 24, y + SLH, t, a)


def _qlines(q, width):
    """re-wrap a Quote to a narrower column (beside a picture)"""
    q.lines = wrap(q.text, width)
    q.ls, n = [], 0
    for ln in q.lines:
        q.ls.append(q.t0 + 0.12 + n / q.cps)
        n += len(ln) + 1
    q.t_end = q.t0 + 0.12 + n / q.cps
    q.ks = [q.t_end + 0.15 + 0.12 * k for k in range(len(q.kiln) + (1 if q.note else 0))]
    return q


# ---------- the board, as film 3's board.json stood at each commit of 8-9 Nov (git show, read-only)
BOARD_COMMITS = ["4db0458", "6c19350", "b80962a", "ee81c0a", "9e7b5e3", "be8a026", "f174ff9"]


@lru_cache(1)
def board_states():
    f = CACHE / "board-states.json"
    if f.exists():
        return json.loads(f.read_text())
    out = []
    for h in BOARD_COMMITS:
        when = subprocess.run(["git", "-C", str(FILM), "log", "-1", "--format=%aI", h], capture_output=True, text=True,
                              check=True).stdout.strip()
        b = json.loads(subprocess.run(["git", "-C", str(FILM), "show", f"{h}:production/board/board.json"],
                                      capture_output=True, text=True, check=True).stdout)
        shots = [{"id": s["id"], "status": s.get("plate_status") or "", "frame": s.get("frame")} for s in b["shots"]]
        out.append({"commit": h, "ts": when, "shots": shots})
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out))
    return out


def kind(status, frame):
    """plate: the shot's picture is chosen (a pick, a design as plate, a still as it is); ref: a reference for a plate
    still to make; empty: nothing yet (or a shot drawn in code)"""
    if not frame:
        return "empty"
    s = status.lower()
    if s.startswith(("picked", "design as plate", "still ")):
        return "plate"
    return "ref"


class BoardV1(Entry):
    """board v1 with the plate plan (4db0458): 63 shots in time order, each card's picture"""

    def __init__(self, t0):
        self.t0 = t0
        st = board_states()[0]
        self.shots = st["shots"]
        self.cols, self.cw, self.ch, self.gap = 16, 48, 27, 4.5
        self.rows = (len(self.shots) + self.cols - 1) // self.cols
        n = sum(1 for s in self.shots if s["status"].startswith("picked"))
        self.caption = f"production/board/board.json   {len(self.shots)} shots   picked {n}"

    def height(self, t):
        return (SLH + self.rows * (self.ch + self.gap) + 12) * ease((t - self.t0) / 0.18)

    def draw(self, c, x, y, t, a):
        if t < self.t0:
            return
        B.crt(c, self.caption, x, y, px=SPX, rows_=SROWS, color=B.CYAN, alpha=0.75 * a, glow=False)
        for i, s in enumerate(self.shots):
            r, k = divmod(i, self.cols)
            cx, cy = x + k * (self.cw + self.gap), y + SLH + r * (self.ch + self.gap)
            rev = (t - (self.t0 + 0.08 + 0.4 * i / len(self.shots))) / 0.1
            if rev <= 0:
                continue
            kd = kind(s["status"], s["frame"])
            if kd != "empty":
                draw_pic(c, pic(s["frame"], self.cw, self.ch, 2), cx, cy, self.cw, self.ch, reveal=rev,
                         dim=1.0 if kd == "plate" else 0.3, grey=0.0 if kd == "plate" else 0.6, alpha=a)
            c.drawRect(skia.Rect.MakeXYWH(cx, cy, self.cw, self.ch), stroke(B.CYAN, (0.5 if kd == "plate" else 0.25) * a, 1.0))


# ---------- the schedule: (song time on the beat, the entry). Record times and song_at in the log.
@lru_cache(1)
def schedule():
    F = "media/images/"
    ds1 = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "dataset-1").glob("d*.jpg"))
    ds2 = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "dataset-2").glob("d*.jpg"))
    ds3 = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "dataset-3").glob("d*.jpg"))

    def dnum(p):
        return int(re.match(r"d(\d+)", Path(p).name).group(1))

    def picks_of(line, files):
        got = {int(x) for x in re.findall(r"D(\d\d)", notes()[line]["quote"])}
        return [i for i, p in enumerate(files) if dnum(p) in got]

    # dataset 3: "D80." was meant to be D88 (Lati, L149, 20:40); D89 rejected (L143)
    p3 = [i for i in picks_of(143, ds3) if dnum(ds3[i]) != 89]
    i88 = next(i for i, p in enumerate(ds3) if dnum(p) == 88)
    i89 = next(i for i, p in enumerate(ds3) if dnum(p) == 89)
    face = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "face-sheet-1").glob("[A-F]-*"))
    lt2 = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "looktest-2").glob("*s1001*.png"))
    grok = [F + "ships-grok/" + n + ".jpg" for n in ("claude-1", "gemini-1", "chatgpt-1", "grok-1", "grok-2", "grok-3")]
    her = sorted(str(p.relative_to(FILM)) for p in (FILM / "media/plates/her-1").glob("s*.jpg"))
    her_picks = {"s009-1", "s011-4", "s012-4", "s013-2", "s024-1", "s024-2", "s024-3", "s024-4", "s025-1", "s026-2",
                 "s026-3", "s032-4", "s044-1", "s044-2", "s044-3", "s044-4", "s062-1", "s062-3"}  # L247, his list
    d1 = sorted(str(p.relative_to(FILM)) for p in (FILM / F / "designs-1").glob("*.jpg")
                if not re.match(r"(m2i|p2i|i)-", p.name))  # the 01:45 batch; the iridescent redo came at 12:39
    d1_picks = {"m1-a-1", "m1-b-2", "m1-c-1", "m3-a-2", "m3-c-1", "m4-a-1", "m4-a-2", "m4-b-1", "m4-b-2", "m4-c-1",
                "m4-c-2", "p1-b-2", "p3-b-2", "p4-a-1", "v-1", "v-2"}  # Kiln's reading of L305, as recorded

    def stem(p):
        return re.sub(r"-6a[0-9a-f]{20,}$", "", Path(p).stem)

    gem = [next(str(p.relative_to(FILM)) for p in (FILM / F / "designs-1").glob(n + "-6a*.jpg"))
           for n in ("m2i-a-1", "m2i-c-2", "p2i-a-1", "i-1")]
    notes9 = sorted(str(p.relative_to(FILM)) for p in (FILM / "media/board/notes-9-nov").glob("page-*.jpg"))

    E = [
        # 1 Nov: the message that opened film 3 (18:35Z, 8 min before the first commit)
        (0.00, Quote(0.00, 44, end="empty repo.", cps=120)),
        # the quiet days, on the beat nearest each local midnight (song_at: 0.13, 1.08, 2.04, 2.99, 3.94, 4.90)
        (0.33, Day(0.33, 2)), (1.41, Day(1.41, 3)), (2.52, Day(2.52, 4)), (3.08, Day(3.08, 5)), (4.18, Day(4.18, 6)),
        (5.61, Day(5.61, 7)),  # 7 Nov lands on the first accent
        # 7 Nov
        (6.42, Quote(6.42, 59, start="Anyhow, I think")),                                          # 16:23, 6.23
        (6.97, Quote(6.97, 65, start="This song is not", end="as a whole.", kiln="agreed.")),      # 16:34, 6.50
        (8.08, Grid(8.08, F + "look-test-1/", [F + "look-test-1/A-en-seedream5pro.jpg", F + "look-test-1/A-ja-seedream5pro.jpg"],
                    2, 300, 169, px=3, labels=["R1·1", "R1·2"], gap=14, pick_t=8.59, picks=[0, 1])),  # sheet 17:30, 7.92
        (8.59, Quote(8.59, 77, end="80s feel of R1·2.")),                                          # 17:39, 8.20
        (9.15, Grid(9.15, F + "face-sheet-1/", face, 6, 132, 74, px=2, labels=list("ABCDEF"), gap=9.6,
                    pick_t=9.70, picks=[4], rejects=[0, 2, 3], reject_t=9.25)),                    # 17:47-17:56, 8.6-8.9
        (9.70, Quote(9.70, 83, end="much better.")),                                                # 18:26, 9.42
        (10.26, Grid(10.26, F + "dataset-1/  30", ds1, 15, 50, 66, px=2, gap=6, pick_t=10.81, picks=picks_of(101, ds1),
                     aside_t=14.71, count="picked 17")),                                            # 19:09, 10.43
        (10.81, Quote(10.81, 101)),                                                                 # 19:23, 10.89
        (11.36, Grid(11.36, F + "dataset-2/  40", ds2, 20, 36, 48, px=2, gap=6, pick_t=11.95, picks=picks_of(119, ds2),
                     aside_t=14.71, count="picked 15")),                                            # 19:45, 11.46; picks 19:58
        (12.50, Grid(12.50, F + "dataset-3/  20", ds3, 20, 36, 48, px=2, gap=6, pick_t=13.05, picks=p3 + [i88],
                     rejects=[i89], reject_t=13.05, aside_t=14.71, count="picked 13 · D89 out")),   # 20:25, 12.33; picks 20:33-20:40
        (14.16, Grid(14.16, F + "looktest-2/", lt2, 12, 62, 90, px=2, gap=6.2, rejects=range(len(lt2)), reject_t=14.71)),  # 21:20, 13.92
        (14.71, Quote(14.71, 161, end="style and composition.", note="LoRA set aside")),           # 21:28, 14.16; set aside 21:33
        (15.29, Day(15.29, 8)),                                                                     # midnight, 14.96
        (15.85, Grid(15.85, F + "ships-grok/", grok, 6, 132, 74, px=2, labels=[Path(g).stem for g in grok], gap=9.6,
                     pick_t=16.95, picks=[0, 1, 2, 4])),                                            # 22:41, 16.03; Grok2 23:00, 16.52
        (16.40, Quote(16.40, 191, start="its ill-adviced", cps=180)),                               # 22:40, 16.02
        (16.95, ClipQuote(16.95, "media/motion/test-1/rough-1.mp4", 1.9, 1.1, "media/motion/test-1/rough-1.mp4",
                          203, start="1-2 second shot")),                                           # 23:12-23:13, 16.84-16.88
        (17.51, Quote(17.51, 209, start="But. We should", kiln="motion stops until the board exists.")),  # 23:16, 16.94
        # 8 Nov
        (18.08, Grid(18.08, "media/plates/her-1/  40", her, 10, 78, 44, px=2, gap=6, pick_t=18.64,
                     picks=[i for i, p in enumerate(her) if stem(p) in her_picks], count="picked 18")),  # 00:24, 18.27; picks 00:30, 18.32
        (19.18, Quote(19.18, 297, start="multiple options", end="abundance is what works.")),      # 01:30, 18.79
        (19.71, Grid(19.71, F + f"designs-1/  {len(d1)}", d1, 14, 54, 54, px=2, gap=6, pick_t=24.14,
                     picks=[i for i, p in enumerate(d1) if stem(p) in d1_picks], count=f"picked {len(d1_picks)}")),  # 01:45, 18.90; picks 12:27, 23.91
        (24.14, Quote(24.14, 305, start="Maybe", end="more apt.")),                                 # 12:27, 23.91
        (24.70, Grid(24.70, F + "designs-1/", gem, 4, 198, 111, px=3, labels=[stem(g) for g in gem], gap=16,
                     pick_t=24.70, picks=[0, 1, 2, 3])),                                            # redo 12:39, picks 12:52 (24.10)
        (25.25, Quote(25.25, 317, start="I-1 is also")),
        # 9 Nov
        (28.57, Day(28.57, 9)),                                                                     # midnight, 28.37
        (29.13, Quote(29.13, 347, start="could you update", end="chronological order.")),          # 23:28Z, 29.06 (the accent)
        (29.68, BoardV1(29.68)),                                                                    # 4db0458 23:30Z, 29.10
        (34.72, Quote(34.72, 353, start="it was my intention", end="is a great idea.")),            # to Flint 11:22Z, 34.62
        (36.41, Grid(36.41, "media/board/notes-9-nov/", notes9, 4, 150, 200, px=2, gap=12)),         # 14:08Z, 36.21
        (36.95, Quote(36.95, 371, start="Go ahead", end="board v2.")),                              # 14:26Z, 36.96
    ]
    pane = [
        (40.28, Quote(40.28, 411, end="by chapter.")),                                              # 15:44Z, 40.19
        (42.48, Quote(42.48, 449, start="DEFINETELY", end="still profiles.")),                      # 16:29Z, 42.05
    ]
    return E, pane


# ---------- the board v2 screen
BCOLS, BCW, BCH, BGAP = 12, 64, 36, 6


@lru_cache(1)
def board_timeline():
    """[(song time on the beat, shots)] for board v2's states; the first is v2 itself"""
    sts = board_states()[1:]
    beats = {"6c19350": T_BOARD, "b80962a": 38.06, "ee81c0a": 40.28, "9e7b5e3": 42.48, "be8a026": 43.03, "f174ff9": 44.14}
    return [(beats[s["commit"]], s["shots"]) for s in sts]


def board_cell(i, t):
    """(kind, frame, when it last changed) of card i at t; a new state lands across the cards within 0.08 s"""
    cur, since = None, None
    for ts, shots in board_timeline():
        when = ts + 0.08 * i / len(shots)
        if when > t:
            break
        s = shots[i]
        v = (kind(s["status"], s["frame"]), s["frame"])
        if cur is not None and v != cur:
            since = when
        cur = v
    return (cur[0], cur[1], since) if cur else ("empty", None, None)


def draw_board(c, t, a):
    tl = board_timeline()
    shots = [s for ts, s in tl if ts <= t][-1]
    n_pick = sum(1 for s in shots if s["status"].startswith("picked"))
    B.crt(c, f"production/board/board.json   v2   {len(shots)} shots   picked {n_pick}", VX0, VY0, px=SPX,
          rows_=SROWS, color=B.CYAN, alpha=0.8 * a, glow=False)
    y0 = VY0 + SLH + 8
    hi = 42.48 <= t  # Lati's "DEFINETELY s034-1 and s034-2": the shot framed
    for i, s in enumerate(shots):
        r, k = divmod(i, BCOLS)
        cx, cy = VX0 + k * (BCW + BGAP), y0 + r * (BCH + BGAP)
        rev = (t - (T_BOARD + 0.04 + 0.03 * r + 0.004 * k)) / 0.1
        if rev <= 0:
            continue
        kd, fr, since = board_cell(i, t)
        if kd != "empty":
            draw_pic(c, pic(fr, BCW, BCH, 2), cx, cy, BCW, BCH, reveal=rev, dim=1.0 if kd == "plate" else 0.28,
                     grey=0.0 if kd == "plate" else 0.65, alpha=a)
        c.drawRect(skia.Rect.MakeXYWH(cx, cy, BCW, BCH), stroke(B.CYAN, (0.55 if kd == "plate" else 0.22) * a, 1.0))
        if since is not None and 0 <= t - since < 0.3:  # a new plate lands: a white flash on its card
            c.drawRect(skia.Rect.MakeXYWH(cx, cy, BCW, BCH), skia.Paint(Color=col(B.WHITE, 0.8 * (1 - (t - since) / 0.3) * a)))
        if hi and s["id"] == "s034":
            c.drawRect(skia.Rect.MakeXYWH(cx - 3, cy - 3, BCW + 6, BCH + 6), stroke(B.AMBER, a, 2.4))


# ---------- layout and drawing
def layout(entries, t):
    """[(y offset within the content, entry)] and the total height at t"""
    out, y = [], 0.0
    for t0, e in entries:
        if t0 > t:
            break
        out.append((y, e))
        y += e.height(t)
    return out, y


def draw_stack(c, entries, t, top, height, a):
    placed, total = layout(entries, t)
    off = max(0.0, total - height)
    for y, e in placed:
        yy = top + y - off
        if yy > top + height + 10 or yy + 900 < top - 10:
            continue
        e.draw(c, VX0, yy, t, a)
    busy = any(e.busy(t) for _, e in placed)
    if placed and not busy and int(t * 2.5) % 2 == 0:  # the idle cursor
        yy = top + total - off
        if yy < top + height - 20:
            c.drawRect(skia.Rect.MakeXYWH(VX0, yy + 2, 11, SROWS * SPX + 2), skia.Paint(Color=col(B.AMBER, 0.85 * a)))


def draw(c, t, base):
    global B
    B = base
    a = 1.0 - ease((t - T_QUIET) / 0.25)
    if a <= 0.001:
        return
    E, pane = schedule()
    c.save()
    c.clipRect(skia.Rect(VX0 - 12, VY0 - 8, VX1 + 12, VY1))
    if t < T_BOARD:
        draw_stack(c, E, t, VY0, VH, a)
    else:  # a clear, on the beat: the board prints from the top
        draw_board(c, t, a)
        c.save()
        c.clipRect(skia.Rect(VX0 - 12, PANE_Y - 6, VX1 + 12, VY1))
        draw_stack(c, pane, t, PANE_Y, VY1 - PANE_Y, a)
        c.restore()
    c.restore()


def warm(base):
    """decode every picture once (the caches), so a render doesn't pay for it frame by frame"""
    global B
    B = base
    E, pane = schedule()
    for _, e in E:
        for f in getattr(e, "files", []):
            small(f, e.cw // e.px, e.ch // e.px)
    for st in board_states():
        for s in st["shots"]:
            if s["frame"]:
                small(s["frame"], BCW // 2, BCH // 2)
                small(s["frame"], 48 // 2, 27 // 2)
