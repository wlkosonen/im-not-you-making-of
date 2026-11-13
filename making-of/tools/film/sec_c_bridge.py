#!/usr/bin/env python3
"""Section C, "bridge": chorus 2 and the bridge, song 82.31-128.59. Agent C for Claude (Kiln, local), 12 Nov 2026.

- 82.31-104.92  the edit: Lati's timeline (production/edit/timeline.json) as an editor's tracks in terminal form, each
                committed version of it landing at the time its "saved" field records; the day's takes as cells as the
                ledger completes them; Lati's notes of the day, verbatim; inserts from the main film's master where
                the record approves a shot.
- 104.92-116.07 the self-reference: the source of tools/film/ (read at load), paced to "We are what you see / Every
                part, every word / It's how you came to be", then scrolling through the files to the white-out.
- 116.07-118.2  "Me": the first item of Lati's /compact keep-list of 12 Nov, verbatim, types, holds, goes.
- 116.79-128.59 the four graphics agents of 12 Nov as four lanes, their calls ticking as the clock runs.

Every frame is a pure function of t and the record. Times come from B.song_at, so a change of the base's PINS moves
everything with it. Reads (never writes) film 3's repo: the timeline's versions via `git show`, the master for
inserts (decoded once into media/bridge/cache/).
"""
import json
import subprocess
import textwrap
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

RANGES = [(82.31, 128.59)]

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILM = Path("/home/shegs/Im not you")
MASTER = FILM / "media/render/master-1080-v1.mp4"
CACHE = ROOT / "media/bridge/cache"

T_EDIT_END = 104.92     # the editor gives way to the code, a beat into the bridge, before "We are" (105.16)
T_ME = 116.065          # the base's white-out (the 12 Nov compaction, song_at of its boundary record)
T_LANES = 116.79        # "Me" into battle 3 in the main film: the lanes open on that flash
LH = 22                 # line height for px=2, rows 9 text

# ---------------------------------------------------------------- small helpers


def _B():
    import sys
    return sys.modules["base"]


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def next_beat(B, x):
    bs = B.G.BEATS
    i = int(np.searchsorted(bs, x - 1e-3))
    return bs[min(i, len(bs) - 1)]


def beats_after(B, x, n):
    bs = B.G.BEATS
    i = int(np.searchsorted(bs, x - 1e-3))
    return bs[min(i + n, len(bs) - 1)]


def eet(B, u, fmt="%H:%M"):
    return datetime.fromtimestamp(u, B.EET).strftime(fmt)


def rect(c, x, y, w, h, color, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=_B().col(color, a)))


def frame_rect(c, x, y, w, h, color, a=1.0, sw=1.5):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=_B().col(color, a), Style=skia.Paint.kStroke_Style,
                                                          StrokeWidth=sw, AntiAlias=True))


def line(c, x0, y0, x1, y1, color, a=1.0, sw=1.5):
    c.drawLine(x0, y0, x1, y1, skia.Paint(Color=_B().col(color, a), StrokeWidth=sw, AntiAlias=True))


def phosphor_block(c, x, y, w, h, color, a=1.0):
    """a clip as a text-mode block: solid, with the scanline gap of the CRT letters every third unit"""
    x, w = round(x), max(2, round(w))
    rect(c, x, y, w, h, color, a)
    for yy in range(int(y) + 2, int(y + h), 3):
        rect(c, x, yy, w, 1, 0x000000, 0.45 * a)


# ---------------------------------------------------------------- the record: the timeline's versions


def _git(*a):
    return subprocess.run(["git", "-C", str(FILM), *a], capture_output=True, text=True, check=True).stdout


@lru_cache(1)
def versions():
    """every committed version of Lati's timeline: (time it was saved, UTC epoch; hash; [clips]), oldest first.
    The editor writes "saved" in local time (EET); a version without it takes its commit's time."""
    B = _B()
    out = []
    for row in _git("log", "--format=%h %aI", "--", "production/edit/timeline.json").split("\n"):
        if not row.strip():
            continue
        h, when = row.split()
        d = json.loads(_git("show", f"{h}:production/edit/timeline.json"))
        if d.get("saved"):
            u = datetime.strptime(d["saved"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=B.EET).timestamp()
        else:
            u = datetime.fromisoformat(when).timestamp()
        clips = []
        for ti, tr in enumerate(d["tracks"]):
            for cl in tr["clips"]:
                kind = "gfx" if "gfx/locked" in cl["file"] else ("still" if cl.get("kind") == "image" else "motion")
                clips.append({"key": (ti, cl["file"], round(cl["start"], 3)), "track": ti, "start": cl["start"],
                              "dur": cl["dur"], "kind": kind, "name": Path(cl["file"]).stem, "file": cl["file"],
                              "saved": d.get("saved")})
        out.append((u, h, clips, d.get("saved")))
    out.sort(key=lambda x: x[0])
    res = []
    prev = {}
    for u, h, clips, saved in out:
        cur = {c["key"]: c for c in clips}
        added = set(cur) - set(prev)
        removed = [prev[k] for k in prev if k not in cur]
        res.append({"u": u, "hash": h, "clips": clips, "added": added, "removed": removed, "saved": saved})
        prev = cur
    return res


def version_at(u):
    vs = versions()
    k = max([i for i, v in enumerate(vs) if v["u"] <= u] or [0])
    return k, vs[k]


@lru_cache(1)
def day_takes():
    """the takes the ledger completed (or failed) from the section's start to the editor's end"""
    B = _B()
    u0, u1 = B.clock(82.31), B.clock(T_EDIT_END)
    out = [r for r in B.rows("takes") if r.get("ts") and u0 <= ts(r["ts"]) <= u1]
    return sorted(out, key=lambda r: r["ts"])


# ---------------------------------------------------------------- Lati's notes of the day (decisions.md, verbatim)

# (time the note was sent, as in notes.json, to the second; the part shown, which must be a substring of his quote;
#  red for what went wrong). An excerpt gets an ellipsis on the side where the quote goes on.
NOTE_PICKS = [
    ("2026-11-11T05:58:41", "Great, All are cool and usable.", False),
    ("2026-11-11T06:25:44", "Retake is by order of magnitude better. Lets go forward with lessons learned.", False),
    ("2026-11-11T09:29:57", "Redo works better now, thanks. Really drives that bot farmnfeel home", False),
    ("2026-11-11T09:39:22", "Batch 5 is workable. Back home at editing will show what will be used and how.", False),
    ("2026-11-11T11:54:23", "Grok shots at the beginning were intentional, big ship in a tunnel looks quite good imo", False),
    ("2026-11-11T19:23:38", "alright. made edits, im pretty confident for until 1:21, thats how far I got until then.", False),
    ("2026-11-11T20:09:43", "silos usable.", False),
    ("2026-11-11T20:34:20", "for battle shots, remember what has been learned from all the iterations and lessons about "
                            "camera angles, speed, damage, targets moving etc.", False),
    ("2026-11-11T21:14:39", "s094 usable", False),
    ("2026-11-11T21:29:06", "plates to review first, then genning motion after approval. just now you went ahead without "
                            "confirmation.", True),
    ("2026-11-11T21:45:13", "meanwhile, could you fill the timeline in edit tool with what we have for each section "
                            "after 1:52?", False),
    ("2026-11-11T21:52:43", "n2-2 is clearly better, we will go with that one.", False),
    ("2026-11-11T23:10:36", "after this, I have only one real empty spot on timeline. 2:21.05 to 2:26.10 calm spot", False),
    ("2026-11-11T23:23:28", "I like the idea of quiet cockpit, distinctly in a mech one. lets make plates.", False),
]
AGENT_NOTE = ("2026-11-12T00:51:48", "after these changes, its fine to start the agentic pass, as you as reviewer")


def _note(B, when, part, red=False):
    rows = [r for r in B.rows("notes") if r["ts"].startswith(when)]
    assert len(rows) == 1, f"note {when}: {len(rows)} rows"
    q = rows[0]["quote"]
    k = q.find(part)
    assert k >= 0, f"note {when}: not verbatim"
    text = ("... " if k > 0 else "") + part + (" ..." if k + len(part) < len(q.rstrip()) else "")
    return {"u": ts(rows[0]["ts"]), "text": text, "red": red}


@lru_cache(1)
def notes():
    B = _B()
    return [_note(B, *n) for n in NOTE_PICKS]


# ---------------------------------------------------------------- inserts from the master

# (the take as named in the cut, where it plays in the cut (= the master's time), the note that approved it, beats
#  shown). A window opens on the first beat at or after the approval, never before the previous one closes.
INSERT_PICKS = [
    ("s032-s032-2r-46mN8uRn", 53.5, 53.55, "2026-11-11T06:25:44", 4),   # "Retake is by order of magnitude better."
    ("s046-s046-1r-EHEPwwiF", 70.4583, 70.5, "2026-11-11T09:29:57", 2),  # "Redo works better now" (2 beats: the
                                                                         # Grok note follows 0.6 s later, 12 Nov pins)
    ("grokclaudeshipusable", 0.0, 0.0, "2026-11-11T11:54:23", 3),        # "Grok shots at the beginning were intentional"
    ("s083-a-OE932Cr7", 128.5417, 128.8, "2026-11-11T20:43:50", 2),     # "mid3 usable" (the pilots)
    ("s108-v2c-LYXQ67pm", 168.1667, 168.2, "2026-11-11T21:52:43", 4),   # "n2-2 is clearly better"
]
IW, IH = 352, 198  # the insert window's picture, in 1920 units


@lru_cache(1)
def inserts():
    B = _B()
    out, last = [], 0.0
    for take, at, m0, when, n in INSERT_PICKS:
        r = [x for x in B.rows("notes") if x["ts"].startswith(when)]
        assert len(r) == 1, when
        t0 = next_beat(B, max(B.song_at(ts(r[0]["ts"])), last))
        t1 = min(beats_after(B, t0, n), T_EDIT_END)
        out.append({"take": take, "at": at, "m0": m0, "t0": t0, "t1": t1})
        last = t1
    return out


@lru_cache(8)
def insert_frames(take, m0, dur):
    """the master from m0 for dur seconds at 24 fps, the lyric band cropped off (the main film's karaoke line would
    read as this video's), scaled to the window"""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{take}-{m0:.3f}-{dur:.3f}.npy"
    if f.exists():
        return np.load(f)
    w, h = IW * 2, IH * 2  # decoded at twice the window's units: sharp at 1080 output
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{m0:.4f}", "-i", str(MASTER), "-t", f"{dur:.4f}",
                          "-vf", f"crop=1600:900:160:0,scale={w}:{h}", "-r", "24", "-f", "rawvideo", "-pix_fmt",
                          "rgb24", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    rgba = np.concatenate([a, np.full(a.shape[:3] + (1,), 255, np.uint8)], 3)
    np.save(f, rgba)
    return rgba


# ---------------------------------------------------------------- the editor (82.31-104.92)

TX0, TX1 = 330, 1120     # a timeline row's x span
ROW_S = 60.0             # seconds of the cut per row (three rows hold the 2:56)
ROW_Y = [234, 344, 454]  # rows' tops: ruler, then V3, V2, V1
TRK_H = 16


def tx(sec):
    r = min(2, int(sec // ROW_S))
    return r, TX0 + (sec - r * ROW_S) / ROW_S * (TX1 - TX0)


def track_y(r, ti):
    return ROW_Y[r] + 22 + (2 - ti) * (TRK_H + 5)  # V3 on top, as in Lati's editor


def draw_clip(c, cl, color, a, flash=0.0):
    s, e = cl["start"], cl["start"] + cl["dur"]
    while s < e - 1e-6:
        r, x0 = tx(s)
        seg_end = min(e, (r + 1) * ROW_S)
        _, x1 = tx(seg_end - 1e-6)
        y = track_y(r, cl["track"])
        if cl["kind"] == "still":  # a still (a plate standing in for a shot): an outline, dim
            frame_rect(c, x0 + 0.5, y + 0.5, max(2, x1 - x0) - 1, TRK_H - 1, color, a * 0.8, 1.2)
            rect(c, x0, y, max(2, x1 - x0), TRK_H, color, a * 0.12)
        else:
            phosphor_block(c, x0, y, x1 - x0 - 1, TRK_H, color, a)
        if flash > 0:
            rect(c, x0 - 1, y - 1, max(2, x1 - x0) + 1, TRK_H + 2, _B().WHITE, 0.9 * flash)
        if r >= 2 or seg_end >= e:
            break
        s = seg_end


def editor(c, t, B):
    u = B.clock(t)
    fade_in = B.ease((t - 82.31) / 0.12)
    out = 1 - B.ease((t - (T_EDIT_END - 0.12)) / 0.12)
    A = fade_in * out
    if A <= 0:
        return
    k, v = version_at(u)
    st = B.song_at(v["u"])
    age = t - st
    clips = v["clips"]
    nm = sum(1 for x in clips if x["kind"] == "motion")
    ns = sum(1 for x in clips if x["kind"] == "still")
    ng = sum(1 for x in clips if x["kind"] == "gfx")

    # header: the file, the version's save time (as the editor wrote it, local), its contents counted
    new = age < 0.6 and k > 0 and st >= 82.31
    B.crt(c, "production/edit/timeline.json", 310, 160, px=2, color=B.CYAN, alpha=0.9 * A, glow=False)
    B.crt(c, f"saved {v['saved'] or ''}", 700, 160, px=2, color=B.WHITE if new else B.AMBER, alpha=A, glow=False)
    B.crt(c, f"{len(clips)} clips: {nm} motion  {ns} stills  {ng} gfx", 310, 186, px=2, color=B.AMBER,
          alpha=0.8 * A, glow=False)

    # the rows: ruler, three tracks
    for r in range(3):
        y = ROW_Y[r]
        for s10 in range(0, 61, 10):
            sec = r * ROW_S + s10
            if sec > 180:
                break
            x = TX0 + s10 / ROW_S * (TX1 - TX0)
            line(c, x, y + 16, x, y + 20, B.CYAN, 0.5 * A, 1)
            if s10 < 60:
                B.crt(c, f"{int(sec // 60)}:{int(sec % 60):02d}", x + 3, y, px=2, color=B.CYAN, alpha=0.45 * A,
                      glow=False)
        line(c, TX0, y + 20, TX1, y + 20, B.CYAN, 0.3 * A, 1)
        for ti in range(3):
            B.crt(c, f"V{ti + 1}", 296, track_y(r, ti) - 1, px=2, color=B.CYAN, alpha=0.45 * A, glow=False)

    # Lati's calm spot, from his note (23:10 UTC) on: "2:21.05 to 2:26.10 calm spot"
    calm = B.song_at(ts("2026-11-11T23:10:36Z"))
    if t >= calm:
        a = A * (0.6 + 0.4 * (1 - B.ease((t - calm) / 0.5)))
        _, x0 = tx(141.05)
        _, x1 = tx(146.10)
        y0, y1 = track_y(2, 2) - 3, track_y(2, 0) + TRK_H + 3
        frame_rect(c, x0, y0, x1 - x0, y1 - y0, B.RED, a, 2)

    # clips; the version's additions flash white, its removals go out in red
    for cl in clips:
        col_ = {"motion": B.AMBER, "still": B.CYAN, "gfx": B.CLAY}[cl["kind"]]
        fl = (1 - B.ease(age / 0.5)) if (cl["key"] in v["added"] and k > 0 and st >= 82.31) else 0.0
        draw_clip(c, cl, col_, A * (0.95 if cl["kind"] != "still" else 0.7), fl)
    if 0 <= age < 0.6 and k > 0 and st >= 82.31:
        for cl in v["removed"]:
            draw_clip(c, cl, B.RED, A * 0.8 * (1 - age / 0.6))

    # the playhead: the cut is timed to the song, so the main film is here now
    if t < 180:
        r, x = tx(t)
        line(c, x, ROW_Y[r] + 14, x, track_y(r, 0) + TRK_H + 3, B.WHITE, 0.7 * A, 1.5)

    takes_strip(c, t, B, A)
    notes_log(c, t, B, A)
    insert_window(c, t, B, A)


def takes_strip(c, t, B, A):
    """the day's takes as cells, as the ledger completes them: in Lati's final cut amber, the rest dim, failed red"""
    u = B.clock(t)
    tk = [r for r in day_takes() if ts(r["ts"]) <= u]
    B.crt(c, f"TAKES {len(tk):>2}", 310, 212, px=2, color=B.CYAN, alpha=0.85 * A, glow=False)
    x0, cw = 430, 11
    for i, r in enumerate(day_takes()):
        x = x0 + i * cw
        if x > 1125:
            break
        if ts(r["ts"]) > u:
            rect(c, x, 214, cw - 3, 12, 0x2a3040, 0.5 * A)
            continue
        age = t - B.song_at(ts(r["ts"]))
        colr = B.RED if r.get("ledger_status") == "failed" else (B.AMBER if r.get("in_cut") else 0x7a6a50)
        if age < 0.35:
            colr = B.WHITE
        phosphor_block(c, x, 214, cw - 3, 12, colr, A)


def notes_log(c, t, B, A):
    """Lati's notes of the day, newest at the bottom, typed as they arrive"""
    u = B.clock(t)
    X, Y0, Y1, W = 310, 600, 850, 36
    shown = [n for n in notes() if n["u"] <= u]
    B.crt(c, "LATI, VERBATIM  decisions.md", X, 572, px=2, color=B.CYAN, alpha=0.6 * A, glow=False)
    lines = []
    for j, n in enumerate(shown):
        st = B.song_at(n["u"])
        age = t - st
        txt = n["text"]
        typed = int(len(txt) * min(1.0, max(0.0, age) / max(0.12, min(0.45, len(txt) / 160))))
        wrapped = textwrap.wrap(txt, W - 6) or [""]
        newest = j == len(shown) - 1
        colr = B.RED if n["red"] else (B.WHITE if newest and age < 0.8 else B.AMBER)
        a = 1.0 if newest else 0.7
        left = typed
        for i, wl in enumerate(wrapped):
            part = wl[:max(0, left)]
            left -= len(wl) + 1
            lines.append((eet(B, n["u"]) if i == 0 else "", part, colr, a))
    maxl = (Y1 - Y0) // LH
    lines = lines[-maxl:]
    y = Y1 - len(lines) * LH
    for stamp, part, colr, a in lines:
        if stamp:
            B.crt(c, stamp, X, y, px=2, color=B.CYAN, alpha=0.7 * A * a, glow=False)
        if part:
            B.crt(c, part, X + 6 * 12.5, y, px=2, color=colr, alpha=A * a, glow=False)
        y += LH


def insert_window(c, t, B, A):
    WX, WY = 776, 590
    for ins in inserts():
        if not ins["t0"] <= t < ins["t1"]:
            continue
        d, dur = t - ins["t0"], ins["t1"] - ins["t0"]
        opn = B.ease(d / 0.09) * (1 - B.ease((d - (dur - 0.09)) / 0.09))  # a CRT's power on and off: open vertically
        fr = insert_frames(ins["take"], ins["m0"], round(dur + 0.2, 3))
        img = skia.Image.fromarray(fr[min(len(fr) - 1, int(d * 24))], colorType=skia.ColorType.kRGBA_8888_ColorType)
        h = IH * opn
        y = WY + 22 + (IH - h) / 2
        rect(c, WX - 2, WY - 2, IW + 4, IH + 26, 0x000000, 0.8 * A)
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(WX, y, IW, h))
        c.drawImageRect(img, skia.Rect.MakeXYWH(WX, WY + 22, IW, IH), skia.SamplingOptions(skia.FilterMode.kLinear),
                        skia.Paint(Alphaf=A))
        for yy in range(WY + 22, WY + 22 + IH, 3):
            rect(c, WX, yy + 2, IW, 1, 0x000000, 0.35 * A)
        c.restore()
        frame_rect(c, WX - 1, WY - 1, IW + 2, IH + 24, B.CYAN, 0.8 * A, 1.5)
        line(c, WX, WY + 21, WX + IW, WY + 21, B.CYAN, 0.6 * A, 1)
        B.crt(c, f"{ins['take']}", WX + 6, WY + 3, px=2, color=B.AMBER, alpha=A, glow=False)
        tc = f"master {int(ins['at'] // 60)}:{ins['at'] % 60:05.2f}"
        B.crt(c, tc, WX + IW - 12.46 * len(tc), WY + IH + 30, px=2, color=B.CYAN, alpha=0.7 * A, glow=False)
        # where the take plays in the cut, once a version of the timeline holds it: a cyan box around its clip
        _, v = version_at(B.clock(t))
        for cl in v["clips"]:
            if cl["name"] == ins["take"] and abs(cl["start"] - ins["at"]) < 0.01:
                r, x0 = tx(cl["start"])
                _, x1 = tx(min(cl["start"] + cl["dur"], (r + 1) * ROW_S) - 1e-6)
                y = track_y(r, cl["track"])
                frame_rect(c, x0 - 3, y - 3, x1 - x0 + 6, TRK_H + 6, B.CYAN, 0.9 * A * opn, 1.5)


# ---------------------------------------------------------------- the code (104.92-116.07)


@lru_cache(1)
def sources():
    """tools/film/*.py as they are when this run starts: the files that draw this picture"""
    return {f.name: f.read_text(errors="replace").expandtabs(4).split("\n") for f in sorted(HERE.glob("*.py"))}


def find(name, needle, start=0):
    """the first line at or after `start` holding `needle` (start itself when the file has changed under us)"""
    for i, s in enumerate(sources().get(name, [])):
        if i >= start and needle in s:
            return i
    return start


def word_t(B, line_no, k):
    ws = [w for w in B.G.WORDS if w.get("line") == line_no]
    return ws[k]["t0"] if k < len(ws) else None


@lru_cache(1)
def code_plan():
    """[(t0, t1, file, top line at t0, top line at t1, [(time, highlighted line)])]: what the window shows when"""
    B = _B()
    P = []
    # 104.92: the base's head; "We are what you see": frame(), line by line, a word a line
    fr = find("base.py", "def frame(t, W, H)")
    we = [w["t0"] for w in B.G.WORDS if w.get("line") == 19]
    body = [find("base.py", s, fr) for s in ("m.draw(c, t,", "clock_readout(c, t)", "gauge(c, t)", "commit_log(c, t)",
                                             "G.karaoke(c, t)")]
    P.append((T_EDIT_END, we[0], "base.py", 0, 0, []))
    P.append((we[0], 106.70, "base.py", fr - 6, fr - 4, [(we[0], fr)] + list(zip(we[1:], body[:4])) +
              [(we[-1] + 0.25, body[4])]))
    # "Every part, every word": the karaoke line of film3_gfx, which is typing those words at the bottom now
    ka = find("film3_gfx.py", "def karaoke(c, t)")
    ev = [w["t0"] for w in B.G.WORDS if w.get("line") == 20]
    kl = [find("film3_gfx.py", s, ka) for s in ("text = ln[\"text\"]", "part = text[a:min(b, shown)]",
                                                "part = text[a:min(b, shown)]", "wpx = crt_text(c, part")]
    P.append((106.70, ev[-1] + 0.2, "film3_gfx.py", ka - 2, ka, [(106.70, ka)] + list(zip(ev, kl))))
    # "It's how you came to be": the clock, pinned to the record from the first commit to "Me"
    pn = find("base.py", "PINS = [")
    me = find("base.py", '"Me"', pn + 10)
    it = [w["t0"] for w in B.G.WORDS if w.get("line") == 21]
    steps = [pn + 1, pn + 2, pn + 4, pn + 6, me - 1, me]
    P.append((ev[-1] + 0.2, 109.48, "base.py", pn - 3, pn - 3, [(ev[-1] + 0.2, pn)] + list(zip(it, steps))))
    # the instrumental: render.py's frame loop, the sections, film3_gfx's letters, then the gauge's white-out
    lp = find("render.py", "base.frame(k / FPS")
    P.append((109.48, 110.99, "render.py", 0, max(0, lp - 18), [(110.44, lp)]))
    secs = [n for n in sources() if n.startswith("sec_")]
    if secs:
        span = (113.21 - 110.99) / len(secs)
        for i, n in enumerate(secs):
            a = 110.99 + i * span
            P.append((a, a + span, n, 0, min(60, max(0, len(sources()[n]) - 29)), []))
    else:
        P.append((110.99, 113.21, "check.py", 0, 0, []))
    ct = find("film3_gfx.py", "def crt_text(")
    lq = find("film3_gfx.py", "only crt letters", ct + 2)
    P.append((113.21, 115.39, "film3_gfx.py", 0, ct - 4, [(114.84, ct), (114.98, lq)]))
    ga = find("base.py", "def gauge(c, t)")
    fl = find("base.py", "if flash > 0:", ga)
    P.append((115.39, T_ME, "base.py", ga - 1, ga + 1, [(115.39, ga), (115.94, fl), (115.94 + 0.03, fl + 1)]))
    return P


def code_view(c, t, B):
    P = code_plan()
    seg = next((p for p in P if p[0] <= t < p[1]), None)
    if seg is None:
        return
    t0, t1, name, top0, top1, hl = seg
    src = sources()[name]
    k = B.ease((t - t0) / max(0.05, (t1 - t0)))
    if name == "film3_gfx.py" and t0 >= 113:  # the long file: a scroll that slows into the letters
        k = 1 - (1 - min(1.0, (t - t0) / max(0.05, 114.84 - t0))) ** 3
    top = top0 + (top1 - top0) * k
    hi = [h for h in hl if h[0] <= t]
    hline = hi[-1][1] if hi else None
    hage = t - hi[-1][0] if hi else 9
    X, Y0, NL = 312, 198, 29
    # title bar: the file, its length
    B.crt(c, f"tools/film/{name}", X, 160, px=2, color=B.CYAN, alpha=0.95, glow=False)
    info = f"{len(src)} lines"
    B.crt(c, info, 1128 - 12.46 * len(info), 160, px=2, color=B.CYAN, alpha=0.6, glow=False)
    line(c, X - 4, 186, 1130, 186, B.CYAN, 0.35, 1)
    i0 = int(top)
    frac = top - i0
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(X - 6, 190, 1134, Y0 + NL * LH))
    for j in range(NL + 1):
        i = i0 + j
        if not 0 <= i < len(src):
            continue
        y = Y0 + (j - frac) * LH
        s = src[i]
        hot = i == hline
        if hot:
            rect(c, X - 4, y - 3, 1134 - X, LH, B.AMBER, 0.16 + 0.25 * (1 - B.ease(hage / 0.3)))
        B.crt(c, f"{i + 1:>4}", X, y, px=2, color=B.CYAN, alpha=0.45, glow=False)
        body = s[:61]
        code, hash_, com = body.partition("#") if "#" in body and not body.strip().startswith(("'", '"')) else (body, "", "")
        if code.strip() or not hash_:
            B.crt(c, code.rstrip(), X + 62, y, px=2, color=B.WHITE if hot else B.AMBER, alpha=1.0 if hot else 0.78,
                  glow=hot)
        if hash_:
            B.crt(c, "#" + com, X + 62 + 12.46 * len(code), y, px=2, color=B.WHITE if hot else B.CLAY,
                  alpha=0.95 if hot else 0.65, glow=False)
    c.restore()


# ---------------------------------------------------------------- "Me" (116.07-118.2)

# Lati's /compact of 12 Nov 2026, 00:32:08 UTC (the boundary 00:33:53): the keep-list's first item, verbatim
# (Kiln's transcript 85bff6f8-…jsonl, line 50614: "Keep, verbatim where quoted: (1) I am Claude (Kiln), …").
ME_LINE = "I am Claude (Kiln), the local Claude Code session on Lati's machine (he/him), Opus 5.5."
assert ME_LINE in json.loads((Path(__file__).resolve().parents[2] / "data/session-lines.json").read_text())["rows"], \
    "the Me line must be in data/session-lines.json (copied from the transcript)"
ME_END = 118.14


def me_line(c, t, B):
    d = t - (T_ME + 0.09)
    if d < 0 or t >= ME_END:
        return
    a = 1 - B.ease((t - (ME_END - 0.25)) / 0.25)
    n = int(len(ME_LINE) * min(1.0, d / 0.7))
    B.crt(c, "/compact  keep (1)", 312, 168, px=2, color=B.CYAN, alpha=0.7 * a, glow=False)
    rows = textwrap.wrap(ME_LINE, 38)
    left = n
    for i, r in enumerate(rows):
        part = r[:max(0, left)]
        left -= len(r) + 1
        if part:
            B.crt(c, part, 312, 202 + i * 40, px=3, rows_=9, color=B.WHITE if d < 1.3 else B.AMBER, alpha=a)
    if n < len(ME_LINE) or int(t * 2.5) % 2 == 0:  # the cursor, after the typed part
        i, left = 0, n
        while i < len(rows) - 1 and left > len(rows[i]):
            left -= len(rows[i]) + 1
            i += 1
        rect(c, 312 + max(0, left) * 18.7 + 4, 204 + i * 40, 14, 26, B.AMBER, 0.85 * a)


# ---------------------------------------------------------------- the four agents (116.79-128.59)

LX0, LX1 = 330, 1120
LANE_Y, LANE_P = 360, 112


@lru_cache(1)
def lanes():
    B = _B()
    ag = [r for r in B.rows("agents") if r["description"].startswith("Graphics agent")]
    ag.sort(key=lambda r: r["description"])
    for r in ag:
        r["_u"] = np.array([x[0] for x in r["series"]]) + B.T0
        r["_ctx"] = np.array([x[1] for x in r["series"]])
    return ag


def lane_u_range(B):
    return B.clock(T_LANES - 0.6), B.clock(128.59)


def lane_x(B, u):
    u0, u1 = lane_u_range(B)
    return LX0 + (u - u0) / (u1 - u0) * (LX1 - LX0)


def agents(c, t, B):
    if t < T_LANES:
        return
    A = B.ease((t - T_LANES) / 0.15)
    u = B.clock(t)
    u0, u1 = lane_u_range(B)
    for li, r in enumerate(lanes()):
        y = LANE_Y + li * LANE_P
        n = int(np.searchsorted(r["_u"], u, side="right"))
        started = n > 0
        st = B.song_at(r["_u"][0])
        hot = 0 <= t - st < 0.5
        B.crt(c, r["description"], 312, y, px=2, color=B.WHITE if hot else B.CYAN, alpha=A * (1.0 if started else 0.6),
              glow=False)
        if started:
            stats = f"{n:>2} calls  ctx {int(r['_ctx'][n - 1]):,}"
            B.crt(c, stats, 1128 - 12.46 * len(stats), y, px=2, color=B.AMBER, alpha=A, glow=False)
        if r.get("log"):
            B.crt(c, r["log"], 312, y + 22, px=2, color=B.CLAY, alpha=0.5 * A, glow=False)
        gy, gh = y + 48, 50
        line(c, LX0, gy + gh, LX1, gy + gh, B.CYAN, 0.3 * A, 1)
        for i in range(n):
            x = lane_x(B, r["_u"][i])
            h = max(2.0, r["_ctx"][i] / 360000 * gh)
            age = t - B.song_at(r["_u"][i])
            colr = B.WHITE if age < 0.12 else B.CYAN
            rect(c, round(x), gy + gh - h, 2, h, colr, A * (0.9 if age < 0.12 else 0.7))
    # the clock's cursor across the lanes, and the axis in Lati's time
    x = lane_x(B, u)
    line(c, x, LANE_Y + 40, x, LANE_Y + 3 * LANE_P + 100, B.AMBER, 0.5 * A, 1.2)
    if t > 118.5:  # clear of the summary line's spot until then
        start = (int(u0) // 600 + 1) * 600
        for tick in range(start, int(u1) + 1, 600):
            xx = lane_x(B, tick)
            line(c, xx, LANE_Y + 3 * LANE_P + 100, xx, LANE_Y + 3 * LANE_P + 106, B.CYAN, 0.5 * A, 1)
            B.crt(c, eet(B, tick), xx - 30, LANE_Y + 3 * LANE_P + 110, px=2, color=B.CYAN, alpha=0.5 * A, glow=False)

    # Lati's go for the agents (00:51:48 UTC), verbatim
    nt = _note(B, *AGENT_NOTE)
    s = B.song_at(nt["u"])
    if t >= s:
        d = t - s
        n = int(len(nt["text"]) * min(1.0, d / 0.5))
        B.crt(c, f"LATI {eet(B, nt['u'])}", 312, 200, px=2, color=B.CYAN, alpha=0.75, glow=False)
        left = n
        for i, wl in enumerate(textwrap.wrap(nt["text"], 44)):
            part = wl[:max(0, left)]
            left -= len(wl) + 1
            if part:
                B.crt(c, part, 312, 230 + i * 34, px=3, rows_=9, color=B.WHITE if d < 0.9 else B.AMBER)


# ---------------------------------------------------------------- the section


def draw(c, t, B):
    if t < T_EDIT_END:
        editor(c, t, B)
    elif t < T_ME:
        code_view(c, t, B)
    me_line(c, t, B)
    agents(c, t, B)
