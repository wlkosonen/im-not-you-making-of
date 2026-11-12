#!/usr/bin/env python3
"""The making-of's base: Kiln's. The clock that maps the song onto the production, the data, and the furniture that runs
through the whole video (the production clock, the context gauge, the commit log, the spend counter, the lyric line).

Every frame is a pure function of song time t and the record in data/ (notes/treatment.md). Drawing is Skia in
1920x1080 units at any output size, the main film's interface voice (film3_gfx: palette, CRT letters, lyric line).
Sections (tools/film/sec_*.py, by agent) draw the centre area with RANGES and draw(c, t, B), B this module.
Kiln, 12 Nov 2026.
"""
import importlib.util
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(HERE))
import film3_gfx as G  # noqa: E402  (the main film's base, vendored)

U = 1920.0
AMBER, CYAN, CLAY, RED, GREEN, WHITE = G.AMBER, G.CYAN, G.CLAY, G.RED, G.GREEN, G.WHITE
BG = 0x07080d
col, ease, pulse = G.col, G.ease, G.pulse
EET = timezone(timedelta(hours=2))  # Lati's time for the whole window

# the lyric line as in the main film, without the main film's cut-specific switches
G.KARAOKE_OFF = []
G.KARAOKE_OFF_SHOTS = ()


def rows(name):
    d = json.loads((DATA / f"{name}.json").read_text())
    return d["rows"] if isinstance(d, dict) and "rows" in d else d


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


# ---------- the clock: song time -> production time (UTC epoch s). Pinned so each turn of the song lands on a turn of
# the work (treatment, "The clock"); linear between pins.
PINS = [
    (0.0, "2026-11-01T18:43:50Z"),    # film 3's first commit
    (5.61, "2026-11-07T16:00:00Z"),   # the first accent: the song is picked (1-6 Nov were quiet days)
    (18.08, "2026-11-08T00:00:00Z"),  # the 7 Nov evening: the look, her dataset, the fleet
    (35.85, "2026-11-09T14:00:00Z"),  # 8-9 Nov: designs, plates, board v2 (pre-chorus)
    (44.50, "2026-11-09T17:28:40Z"),  # the 9 Nov compaction lands just before the chorus drop (44.69)
    (66.81, "2026-11-10T18:30:00Z"),  # chorus 1: the battles, the opening batch, s067, the red lens, the editor
    (80.06, "2026-11-11T05:50:50Z"),  # verse 2, then the break: the 11 Nov compaction on the silence
    (82.31, "2026-11-11T05:53:00Z"),
    (104.38, "2026-11-11T23:30:00Z"),  # chorus 2: the mid batches, the cut, the end, the review
    (116.08, "2026-11-12T00:33:57Z"),  # "Me": the 12 Nov compaction
    (128.59, "2026-11-12T01:30:00Z"),  # the bridge's battle: the four graphics agents' first pass
    (168.17, "2026-11-12T08:29:00Z"),  # the final chorus: Lati's notes, the fixes, the polish, the master
    (171.2, "2026-11-12T08:50:52Z"),   # the making-of begins
]
_PT = np.array([p[0] for p in PINS])
_PU = np.array([_ts(p[1]) for p in PINS])
T0 = _PU[0]


def clock(t):
    """production time (UTC epoch seconds) at song time t"""
    return float(np.interp(t, _PT, _PU))


def song_at(u):
    """song time at production time u (the inverse, for placing events)"""
    return float(np.interp(u, _PU, _PT))


# ---------- the record
@lru_cache(1)
def calls():
    r = np.array([[x[0], x[2]] for x in rows("calls")], np.float64)  # t (s from window start), context tokens
    return r[:, 0] + T0, r[:, 1]


@lru_cache(1)
def compactions():
    return [(_ts(r["ts"]), r["pre_tokens"], r["post_tokens"]) for r in rows("compactions")]


@lru_cache(1)
def commits():
    return [(_ts(r["ts"]), r) for r in rows("commits")]


@lru_cache(1)
def spend():
    out, tot = [], 0.0
    for r in rows("spend"):
        tot += r.get("cost_usd") or 0
        out.append((_ts(r["ts"]), tot, r))
    return out


def context_at(u):
    """Kiln's context (tokens) at production time u: the last call's, and drops at a compaction"""
    ts, ctx = calls()
    i = int(np.searchsorted(ts, u, side="right")) - 1
    v = float(ctx[i]) if i >= 0 else 0.0
    for cu, pre, post in compactions():  # between a compaction and the next call, the summary's size
        if (i < 0 or ts[i] < cu) and cu <= u:
            v = post
    return v


# ---------- furniture
def crt(c, text, x, y, px=3, rows_=9, color=AMBER, alpha=1.0, glow=True):
    return G.crt_text(c, text, x, y, px=px, rows=rows_, color=color, alpha=alpha, glow=glow)


def clock_readout(c, t):
    d = datetime.fromtimestamp(clock(t), EET)
    crt(c, d.strftime("%a %d %b %Y").upper(), 80, 56, px=3, rows_=9, color=CYAN, alpha=0.85)
    crt(c, d.strftime("%H:%M:%S") + " EET", 80, 100, px=4, rows_=11, color=AMBER)


GX, GY, GW, GH = 80, 250, 150, 600  # the context gauge
LIMIT = 1_000_000


def gauge(c, t):
    u = clock(t)
    v = context_at(u)
    segs = 40
    lit = v / LIMIT * segs
    # a compaction: white-out of the gauge, fading over half a second of song
    flash = 0.0
    for cu, pre, post in compactions():
        st = song_at(cu)
        if st - 0.02 <= t < st + 0.6:
            flash = max(flash, 1 - (t - st) / 0.6)
    sh = GH / segs
    for s in range(segs):
        on = s < lit
        part = min(1.0, max(0.0, lit - s))
        colr = RED if s >= segs * 0.8 else AMBER if s >= segs * 0.5 else CYAN
        a = 0.95 * part if on else 0.10
        c.drawRect(skia.Rect.MakeXYWH(GX, GY + GH - (s + 1) * sh + 2, GW, sh - 5),
                   skia.Paint(Color=col(colr if on else 0x2a3040, a)))
    if flash > 0:
        c.drawRect(skia.Rect.MakeXYWH(GX - 20, GY - 20, GW + 40, GH + 40), skia.Paint(Color=col(WHITE, 0.9 * flash)))
    crt(c, "CONTEXT", GX, GY - 44, px=3, rows_=9, color=CYAN, alpha=0.85)
    crt(c, f"{int(v):,}", GX, GY + GH + 18, px=3, rows_=9, color=AMBER)
    crt(c, "/ 1,000,000", GX, GY + GH + 52, px=2, rows_=9, color=CYAN, alpha=0.6, glow=False)


def summary_line(c, t):
    """after a compaction, the summary's first words type back in beside the gauge"""
    line = "This session is being continued from a previous conversation that ran out of context."
    for cu, pre, post in compactions():
        st = song_at(cu)
        d = t - st
        if 0.15 <= d < 2.4:
            n = int(len(line) * min(1.0, (d - 0.15) / 1.2))
            a = 1 - ease((d - 1.9) / 0.5)
            crt(c, line[:n], GX + GW + 40, GY + GH - 40, px=2, rows_=9, color=WHITE, alpha=a)


LX, LY, LW, LN = 1180, 250, 680, 16  # the commit log


def commit_log(c, t):
    u = clock(t)
    cs = [x for x in commits() if x[0] <= u][-LN:]
    crt(c, f"COMMITS {sum(1 for x in commits() if x[0] <= u):>3}", LX, LY - 44, px=3, rows_=9, color=CYAN, alpha=0.85)
    for k, (cu, r) in enumerate(cs):
        age = song_at(u) - song_at(cu)  # how long ago in song time
        a = (0.35 + 0.65 * (k + 1) / len(cs)) * (1.0 if age > 0.25 else 1.6)
        txt = r.get("first_line") or r.get("subject") or ""
        crt(c, txt[:52], LX, LY + k * 36, px=2, rows_=9, color=AMBER if age > 0.25 else WHITE, alpha=min(1, a), glow=False)


def spend_readout(c, t):
    u = clock(t)
    s = [x for x in spend() if x[0] <= u]
    tot = s[-1][1] if s else 0.0
    crt(c, "OPENROUTER", LX, 56, px=3, rows_=9, color=CYAN, alpha=0.85)
    crt(c, f"${tot:,.2f}", LX, 100, px=4, rows_=11, color=AMBER)


# ---------- sections
SECS = []


def load_sections(only=None):
    import traceback
    SECS.clear()
    for f in sorted(HERE.glob("sec_*.py")):
        if only and f.stem not in only:
            continue
        try:
            spec = importlib.util.spec_from_file_location(f.stem, f)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            SECS.append(m)
        except Exception:
            print(f"section {f.stem} skipped:\n{traceback.format_exc(limit=3)}", file=sys.stderr)


def frame(t, W, H):
    img = np.zeros((H, W, 4), np.uint8)
    surf = skia.Surface(img)
    c = surf.getCanvas()
    c.scale(W / U, W / U)
    c.clear(col(BG))
    for m in SECS:
        if any(a <= t < b for a, b in getattr(m, "RANGES", [(0, 1e9)])):
            m.draw(c, t, sys.modules[__name__])
    clock_readout(c, t)
    spend_readout(c, t)
    gauge(c, t)
    summary_line(c, t)
    commit_log(c, t)
    G.karaoke(c, t)
    rgb = img[..., :3].copy()
    rng = np.random.default_rng(int(t * 24))  # the main film's grain, a pure function of t
    rgb = np.clip(rgb.astype(np.float32) + rng.normal(0, 3.0, rgb.shape[:2])[..., None], 0, 255).astype(np.uint8)
    return rgb
