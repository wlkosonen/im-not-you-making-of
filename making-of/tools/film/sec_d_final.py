#!/usr/bin/env python3
"""Section D, the final chorus and the end (song 128.59-176.2): the night, the review, the master, the numbers.

Agent D for Claude (Kiln, local), 12 Nov 2026. notes/agents/final.md has the design and every source.

- the night (129.43-157.03): gfx-pass1-full.mp4 is written (01:38:57Z) and sits as a contact sheet of the cut, one
  cell per shot, while nothing happens: Kiln's calls stop at 01:39:30Z and start again at 06:32:24Z.
- the morning (157.03-168.17): the sheet folds into a strip of the cut along the top; Lati's notes of 12 Nov type into
  a terminal log at the times he sent them, each followed by what was done (the commits, the review files), with red
  ticks on the strip where a note names a shot; three short inserts from the master, each where its fix landed.
- the master (168.17): the strip turns to the master's frames; its numbers; the headline numbers (data/summary.json).
- 171.2: the making-of's first commit line, then black.
Every frame is a pure function of t; the frames from the main film are decoded once into media/final/cache/.
"""
import subprocess
import textwrap
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

RANGES = [(128.59, 176.2)]

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "media/final/cache"
FILM = Path("/home/shegs/Im not you")
PASS1 = FILM / "media/review/gfx-pass1-full.mp4"     # 1280x720, 4229 frames, written 12 Nov 03:38:57 EET
MASTER = FILM / "media/render/master-1080-v1.mp4"    # 1920x1080, 24 fps, 4229 frames, 176.21 s, written 10:29:42 EET
CUT_END = 173.46  # the last piece of Lati's cut ends here (s108, 168.17-173.46)

T_WRITTEN = "2026-11-12T01:38:57Z"   # gfx-pass1-full.mp4 written (the file's mtime)
T_LASTCALL = "2026-11-12T01:39:30Z"   # Kiln's last call before the night (calls.json)
T_NEXTCALL = "2026-11-12T06:32:24Z"   # and the first after it
T_MORNING = 130.78  # the fold: the downbeat that ends the night (Kiln's pin, 06:30Z); Lati's first note at ~131.48
T_MASTER = 168.17   # the pin: the master rendered
T_END = 171.2       # the making-of's first commit
FIRST_COMMIT = ("10:50:52", "b667f51", "start (Kiln): the making-of: README, decisions")  # git log of this repo

# the review files Lati watched (main film, media/review/, file mtimes, EET), each after the note that asked for it
FILES = [("2026-11-12T08:32:45+02:00", "media/review/gfx-pass1-phone-1.mp4"),
         ("2026-11-12T08:33:00+02:00", "media/review/gfx-pass1-phone-2.mp4"),
         ("2026-11-12T09:31:39+02:00", "media/review/gfx-pass2-phone-1.mp4"),
         ("2026-11-12T09:31:55+02:00", "media/review/gfx-pass2-phone-2.mp4"),
         ("2026-11-12T09:50:12+02:00", "media/review/s017-pass3.mp4"),
         ("2026-11-12T10:06:52+02:00", "media/review/gfx-pass3-phone-1.mp4"),
         ("2026-11-12T10:07:08+02:00", "media/review/gfx-pass3-phone-2.mp4")]
# the fixes: the gfx commits made on these notes (commits.json), plus the decisions commits that record a "keep"
FIXES = ["5bbd11af", "851187e0", "e887045d", "86185d99", "cc21aaa9", "5f6faa48", "6ff0bbbd", "9bf870a2", "f0c633d9",
         "88c2e3b8", "b2ca1622", "6ef4a926", "31fc64fa"]
# shots a note names (its context in decisions.md: the screenshots it was written on), and what became of them
TICKS = [  # (production time, shots, state)
    ("2026-11-12T06:54:00Z", ["s009", "s017", "s021", "s025", "s029", "s026", "s048", "s047", "s050"], "flag"),
    ("2026-11-12T07:20:36Z", ["s064", "s067", "s083"], "flag"),
    ("2026-11-12T07:22:02Z", ["s017"], "flag"),
    ("2026-11-12T07:51:26Z", ["s017"], "kept"),   # "Reads much better, we will keep that."
    ("2026-11-12T07:53:30Z", ["s083"], "kept"),   # "Hud lines, keep."
    ("2026-11-12T07:56:45Z", ["s060"], "kept"),   # "s060 totally fine"
]
# fixes the commits name by shot (commit subjects): a flagged tick turns clay when its fix is committed
FIXED_BY = {"e887045d": ["s017", "s025", "s029", "s026"], "851187e0": ["s048", "s047", "s050"],
            "5bbd11af": ["s021"], "86185d99": ["s067"], "5f6faa48": ["s083"], "6ff0bbbd": ["s064"],
            "9bf870a2": ["s017"]}
# inserts from the master, each from its fix commit for one bar: (commit, master in, seconds, title)
INSERTS = [("5bbd11af", 33.75, 2.2, "s021"),    # the lyric line centred (Lati's "thirds")
           ("6ff0bbbd", 98.70, 2.0, "s064"),    # the board on the shelter screen's plane
           ("9bf870a2", 28.00, 1.96, "s017")]   # the scan filling the lightbox
IW, IH = 640, 360  # insert size in 1920 units

# layout (1920 units): the centre is x 300-1140, y 150-860
CX0, CX1 = 300, 1140
GRID_COLS, CW_, CH_, GAP = 10, 80, 45, 4
GRID_X = CX0 + (CX1 - CX0 - (GRID_COLS * (CW_ + GAP) - GAP)) / 2
GRID_Y = 200
STRIP_Y, STRIP_H = 188, 30
HEAD_Y = 158
LOG_TOP, LOG_BOT, LOG_LH = 236, 852, 25.5
LOG_CHARS = 66


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def _song(s):
    import base as B
    return B.song_at(_ts(s))


T_NIGHT = _song(T_WRITTEN)  # the sheet appears when its file is written (128.66 on the clock of 12 Nov, Kiln's pins)


def _eet(u):
    from base import EET
    return datetime.fromtimestamp(u, EET).strftime("%H:%M:%S")


# ---------- the main film's frames, decoded once
def _grab(path, t, w, h):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", "-s", f"{w}x{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8)
    return a.reshape(h, w, 3) if a.size == w * h * 3 else np.zeros((h, w, 3), np.uint8)


@lru_cache(1)
def cells():
    """the cut as cells: consecutive pieces of the same shot merged; (t0, t1, shot id)"""
    import film3_gfx as G
    out = []
    for p in G.cut():
        sid = G.shot_of(p)
        if out and out[-1][2] == sid and abs(out[-1][1] - p["t0"]) < 1e-3:
            out[-1][1] = p["t1"]
        else:
            out.append([p["t0"], p["t1"], sid])
    return [tuple(x) for x in out]


@lru_cache(2)
def thumbs(kind):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"thumbs-{kind}.npy"
    if f.exists():
        a = np.load(f)
        if len(a) == len(cells()):
            return a
    src = PASS1 if kind == "pass1" else MASTER
    a = np.stack([_grab(src, (t0 + t1) / 2, 160, 90) for t0, t1, _ in cells()])
    np.save(f, a)
    return a


@lru_cache(4)
def insert_frames(i):
    CACHE.mkdir(parents=True, exist_ok=True)
    _, t_in, dur, _ = INSERTS[i]
    f = CACHE / f"insert-{i}.npy"
    n = int(round(dur * 24))
    if f.exists():
        a = np.load(f)
        if len(a) == n:
            return a
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t_in:.3f}", "-i", str(MASTER), "-frames:v", str(n),
                          "-s", f"{IW}x{IH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, IH, IW, 3)
    np.save(f, a)
    return a


def _skimg(rgb):
    rgba = np.dstack([rgb, np.full(rgb.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)


@lru_cache(512)
def thumb_img(kind, k):
    return _skimg(thumbs(kind)[k])


@lru_cache(160)
def insert_img(i, k):
    return _skimg(insert_frames(i)[k])


# ---------- the record, as log lines
@lru_cache(1)
def commit_by_hash():
    import base as B
    return {r["hash"]: r for r in B.rows("commits")}


@lru_cache(1)
def events():
    """the morning log: [(song time, kind, payload)], oldest first"""
    import base as B
    ev = []
    for r in B.rows("notes"):
        if "2026-11-12T06:30" <= r["ts"] <= "2026-11-12T08:20":
            ev.append((r["ts"], "note", r["quote"]))
    for h in FIXES:
        r = commit_by_hash()[h]
        ev.append((r["ts"], "commit", (h, r["subject"])))
    for ts, path in FILES:
        ev.append((datetime.fromisoformat(ts).astimezone(timezone.utc).isoformat(), "file", path))
    ev.sort(key=lambda e: _ts(e[0]))
    return [(B.song_at(_ts(ts)), _ts(ts), kind, x) for ts, kind, x in ev]


@lru_cache(1)
def log_lines():
    """every line of the morning log: (appears at, [(column, text, colour)], kind)"""
    import base as B
    out = []
    for st, u, kind, x in events():
        hm = _eet(u)
        if kind == "note":
            body = '"' + " ".join(x.split()) + '"'
            ws = textwrap.wrap(body, LOG_CHARS - 15)
            for i, w in enumerate(ws):
                segs = [(15, w, B.AMBER)]
                if i == 0:
                    segs = [(0, hm, B.CYAN), (9, "lati", B.WHITE)] + segs
                out.append((st + i * 0.02, segs, "note"))
        elif kind == "commit":
            h, subj = x
            ws = textwrap.wrap(subj, LOG_CHARS - 18)
            for i, w in enumerate(ws):
                segs = [(18, w, B.CLAY)]
                if i == 0:
                    segs = [(0, hm, B.CYAN), (9, h, B.CYAN)] + segs
                out.append((st + 0.03 + i * 0.02, segs, "commit"))
        else:
            out.append((st, [(0, hm, B.CYAN), (9, x, B.CYAN)], "file"))
    return out


def _cw(px):
    import film3_gfx as G
    return G._font(9 * 1.15).measureText("0") * px


# ---------- drawing
def _stroke(color, a, w=1.5):
    from base import col
    return skia.Paint(Color=col(color, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w)


def _fill(color, a):
    from base import col
    return skia.Paint(Color=col(color, a))


def _lerp(a, b, k):
    return a + (b - a) * k


def _grid_rect(k):
    r, cc = divmod(k, GRID_COLS)
    return (GRID_X + cc * (CW_ + GAP), GRID_Y + r * (CH_ + GAP), CW_, CH_)


def _strip_rect(k):
    t0, t1, _ = cells()[k]
    x0 = CX0 + t0 / CUT_END * (CX1 - CX0)
    x1 = CX0 + t1 / CUT_END * (CX1 - CX0)
    return (x0, STRIP_Y, max(1.0, x1 - x0 - 0.6), STRIP_H)


def _scanlines(c, x, y, w, h, a=0.22, step=3.0):
    p = _fill(0x000000, a)
    yy = y
    while yy < y + h:
        c.drawRect(skia.Rect.MakeXYWH(x, yy + step - 1, w, 1), p)
        yy += step


def tick_state(sid, u):
    """the shot's mark at production time u: None, flag, fixed, kept (the newest wins)"""
    st, when = None, -1
    for ts, shots, s in TICKS:
        if sid in shots and _ts(ts) <= u and _ts(ts) > when:
            st, when = s, _ts(ts)
    for h, shots in FIXED_BY.items():
        cu = _ts(commit_by_hash()[h]["ts"])
        if sid in shots and cu <= u and cu > when and st == "flag":
            st, when = "fixed", cu
    return st


def draw_sheet(c, t, B):
    """the contact sheet (night) folding into the strip (morning), then turning to the master"""
    G = B.G
    n = len(cells())
    fold = B.ease((t - T_MORNING) / 0.55)
    u = B.clock(t)
    for k, (t0, t1, sid) in enumerate(cells()):
        # the sheet fills in reading order over half a second once the file is written (a display cascade)
        appear = T_NIGHT + 0.5 * k / n
        if t < appear:
            continue
        a_in = B.ease((t - appear) / 0.12)
        gx, gy, gw, gh = _grid_rect(k)
        sx, sy, sw, sh = _strip_rect(k)
        x, y, w, h = _lerp(gx, sx, fold), _lerp(gy, sy, fold), _lerp(gw, sw, fold), _lerp(gh, sh, fold)
        # the master's frames sweep in left to right over a beat after the pin
        kind = "master" if t >= T_MASTER + 0.45 * t0 / CUT_END else "pass1"
        img = thumb_img(kind, k)
        # source: the whole frame on the sheet, a centre slice of it on the strip
        sw_src = min(160.0, 90.0 * w / max(h, 1e-3))
        src = skia.Rect.MakeXYWH((160 - sw_src) / 2, 0, sw_src, 90)
        c.drawImageRect(img, src, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear),
                        skia.Paint(Alphaf=0.92 * a_in))
        if fold < 1:
            _scanlines(c, x, y, w, h, a=0.25 * a_in)
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), _stroke(B.CYAN, 0.25 * a_in * (1 - fold), 1.0))
            if sid and fold < 0.5:
                B.crt(c, sid, x + 3, y + h - 20, px=2, rows_=9, color=B.AMBER, alpha=0.8 * a_in * (1 - 2 * fold), glow=False)
        # the marks, from the first note on, cleared by the master
        if fold >= 1 and t < T_MASTER:
            s = tick_state(sid, u)
            if s:
                colr = {"flag": B.RED, "fixed": B.CLAY, "kept": B.WHITE}[s]
                c.drawRect(skia.Rect.MakeXYWH(x - 0.5, y - 0.5, w + 1, h + 1), _stroke(colr, 0.95, 1.6))
                mx = x + w / 2
                c.drawRect(skia.Rect.MakeXYWH(mx - 3, y + h + 4, 6, 9), _fill(colr, 0.95))
    # the file the sheet is
    if t >= T_NIGHT:
        a = B.ease((t - T_NIGHT) / 0.15)
        name = "master-1080-v1.mp4  1920x1080" if t >= T_MASTER else "gfx-pass1-full.mp4  1280x720"
        B.crt(c, name, CX0, HEAD_Y, px=2, rows_=9, color=B.CYAN, alpha=0.85 * a)
        if t < T_MASTER:
            B.crt(c, "4229 frames  written 03:38:57", CX0 + 31 * _cw(2), HEAD_Y, px=2, rows_=9, color=B.CYAN,
                  alpha=0.55 * a, glow=False)


def draw_night(c, t, B):
    """below the sheet: no calls since the render; the gap counts up until the morning"""
    t_next = _song(T_NEXTCALL)
    if not (T_NIGHT <= t < t_next):
        return
    # in after the sheet, out as the first call of the morning comes (Lati's note lands 0.02 s before it)
    a = B.ease((t - (T_NIGHT + 0.25)) / 0.2) * (1 - B.ease((t - (t_next - 0.08)) / 0.08))
    last, nxt = _ts(T_LASTCALL), _ts(T_NEXTCALL)
    u = min(B.clock(t), nxt)
    y = GRID_Y + 9 * (CH_ + GAP) + 26
    if u < last:
        return
    gap = int(u - last)
    B.crt(c, f"no calls since {_eet(last)}", CX0 + 2, y, px=3, rows_=9, color=B.AMBER, alpha=a)
    B.crt(c, f"+{gap // 3600}:{gap // 60 % 60:02d}:{gap % 60:02d}", CX0 + 2 + 26 * _cw(3), y, px=3, rows_=9,
          color=B.WHITE, alpha=a)


def draw_log(c, t, B):
    if not (T_MORNING <= t < T_MASTER):
        return
    lines = [ln for ln in log_lines() if ln[0] <= t]
    nmax = int((LOG_BOT - LOG_TOP) / LOG_LH)
    lines = lines[-nmax:]
    cw = _cw(2)
    for j, (at, segs, kind) in enumerate(lines):
        y = LOG_BOT - (len(lines) - j) * LOG_LH
        new = t - at < 0.3
        age_a = 0.45 + 0.55 * (j + 1) / len(lines)
        for colm, txt, colr in segs:
            cc = B.WHITE if new and colr in (B.AMBER, B.CLAY) else colr
            B.crt(c, txt, CX0 + colm * cw, y, px=2, rows_=9, color=cc, alpha=min(1.0, age_a * (1.0 if colr != B.CYAN else 0.8)),
                  glow=False)


def draw_inserts(c, t, B):
    for i, (h, t_in, dur, sid) in enumerate(INSERTS):
        t0 = B.song_at(_ts(commit_by_hash()[h]["ts"]))
        if not (t0 <= t < t0 + dur):
            continue
        k = min(len(insert_frames(i)) - 1, int((t - t0) * 24))
        grow = B.ease((t - t0) / 0.15) * (1 - B.ease((t - (t0 + dur - 0.12)) / 0.12))
        # the window opens out of its shot's slot on the strip
        ks = [j for j, x in enumerate(cells()) if x[2] == sid]
        sx, sy, sw, sh = _strip_rect(ks[0]) if ks else (720, STRIP_Y, 1, STRIP_H)
        wx, wy = CX0 + (CX1 - CX0 - IW) / 2, 272
        x, y = _lerp(sx, wx, grow), _lerp(sy + sh, wy, grow)
        w, hh = _lerp(sw, IW, grow), _lerp(2, IH, grow)
        tb = 26 * grow
        # the log's older lines go dark behind the window
        c.drawRect(skia.Rect.MakeLTRB(CX0 - 4, wy - 40, CX1 + 4, wy + IH + 14), _fill(B.BG, 0.97 * grow))
        c.drawRect(skia.Rect.MakeXYWH(x - 6, y - tb - 6, w + 12, hh + tb + 12), _fill(B.BG, 0.96))
        c.drawImageRect(insert_img(i, k), skia.Rect.MakeXYWH(x, y, w, hh), skia.SamplingOptions(skia.FilterMode.kLinear))
        _scanlines(c, x, y, w, hh, a=0.18)
        c.drawRect(skia.Rect.MakeXYWH(x - 6, y - tb - 6, w + 12, hh + tb + 12), _stroke(B.CYAN, 0.8, 1.5))
        c.drawLine(x - 6, y - 4, x + w + 6, y - 4, _stroke(B.CYAN, 0.5 * grow, 1.0))
        if grow > 0.9:
            m, s = divmod(t_in + (t - t0), 60)
            B.crt(c, f"master-1080-v1.mp4  {int(m)}:{s:05.2f}  {sid}", x, y - tb - 2, px=2, rows_=9, color=B.CYAN, alpha=0.9, glow=False)


@lru_cache(1)
def summary_lines():
    import base as B
    s = B.rows("summary")
    return [  # (text, px, colour): data/summary.json, as it is
        (f"{s['days']} days, 1-12 Nov 2026", 3, B.AMBER),
        (f"{s['commits']} commits  +{s['lines_added']:,} -{s['lines_removed']:,} lines", 3, B.AMBER),
        (f"{s['calls']:,} calls (Kiln)  {s['output_tokens']:,} tokens out", 3, B.AMBER),
        (f"{s['compactions']} compactions  peak context {s['peak_context']:,}", 3, B.AMBER),
        (f"{s['lati_messages']} messages from Lati", 3, B.AMBER),
        (f"  {s['notes_in_window']} of his notes quoted in decisions.md", 2, B.CYAN),
        (f"{s['takes_made']} takes made  {s['takes_in_cut']} in the cut", 3, B.AMBER),
        ("  and 3 shots as locked graphics renders", 2, B.CYAN),
        (f"${s['spend_usd']:.2f} OpenRouter  {s['paid_jobs_completed']} paid jobs", 3, B.AMBER),
        ("  ISEKAI ZERO credits and Grok not in it", 2, B.CYAN),
        (f"{s['agents']} agents  {s['agent_calls']} calls", 3, B.AMBER),
    ]


def draw_master(c, t, B):
    if not (T_MASTER <= t < T_END):
        return
    y = 240
    a = B.ease((t - T_MASTER) / 0.1)
    B.crt(c, "master-1080-v1.mp4", CX0, y, px=3, rows_=9, color=B.WHITE, alpha=a)
    # the master's numbers: production/STATUS.md of the main film (1.15 GB) and the file itself (4229 frames)
    if t >= T_MASTER + 0.12:
        B.crt(c, "1920x1080  24 fps  4229 frames  176.21 s  1.15 GB", CX0, y + 40, px=2, rows_=9, color=B.AMBER,
              alpha=B.ease((t - T_MASTER - 0.12) / 0.08))
    y0 = y + 104
    t1 = 168.62  # the beat after the pin: the headline numbers print, one line every ~0.1 s
    for j, (txt, px, colr) in enumerate(summary_lines()):
        at = t1 + 0.1 * j
        if t < at:
            break
        B.crt(c, txt, CX0, y0, px=px, rows_=9, color=colr, alpha=B.ease((t - at) / 0.06) * (0.8 if px == 2 else 1.0),
              glow=px > 2)
        y0 += 40 if px == 3 else 30


def draw_end(c, t, B):
    if not (T_END <= t < T_END + 1.5):
        return
    a = B.ease((t - T_END) / 0.06) * (1 - B.ease((t - (T_END + 1.1)) / 0.4))
    hm, h, subj = FIRST_COMMIT
    x = 720 - len(subj) * _cw(3) / 2
    B.crt(c, f"{hm}  {h}", x, 470, px=2, rows_=9, color=B.CYAN, alpha=0.85 * a)
    B.crt(c, subj, x, 504, px=3, rows_=9, color=B.WHITE, alpha=a)


def draw(c, t, B):
    if t >= T_END:
        draw_end(c, t, B)
        return
    if t < T_NIGHT:  # the render running: a cursor where its file will be named
        if int(t * 2.5) % 2 == 0:
            c.drawRect(skia.Rect.MakeXYWH(CX0, HEAD_Y, 10, 18), _fill(B.AMBER, 0.85))
        return
    draw_sheet(c, t, B)
    draw_night(c, t, B)
    draw_log(c, t, B)
    draw_inserts(c, t, B)
    draw_master(c, t, B)
