#!/usr/bin/env python3
"""Section B (chorus1): chorus 1, verse 2 and the break. Song time 44.69-82.31.

- Chorus 1 (44.69-66.81): the wall of takes. Every take in data/takes.json made by the end of this stretch (11 Nov
  05:53 UTC) is a cell that appears when it was made, its first frame as a small dithered thumbnail; cells in the
  final cut lit, the rest dim, failed jobs red. A log names each take's model as it lands. Lati's verdicts that turned
  something type in verbatim. Three inserts from the main film's master, each where Lati approved that shot.
- Verse 2 (66.81-80.06): the wall shrinks to a strip; the production's mistakes and dead ends print in red from the
  record, each with its own date.
- The break (80.06-82.31): the centre empties to a cursor; the base does the compaction.

Agent B for Kiln, 12 Nov 2026. Every line shown is checked against its source at load (assert): notes.json quotes,
the ledger's errors (spend.json), and two files of film 3 read at load (decisions.md, motion/mid-2-run.md).
"""
import json
import re
import subprocess
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

RANGES = [(44.69, 82.31)]
T_IN, T_V2, T_BRK, T_END = 44.69, 66.81, 80.06, 82.31

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
F3 = Path("/home/shegs/Im not you")
CACHE = ROOT / "media/chorus1/cache"
MASTER = F3 / "media/render/master-1080-v1.mp4"
EET = timezone(timedelta(hours=2))

# the centre
CX0, CX1 = 300, 1140


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def _eet(u, fmt="%d %b %H:%M"):
    return datetime.fromtimestamp(u, EET).strftime(fmt).upper()


# ---------- the takes
MODEL_ISK = "seedance-2.0/isk0"  # opening-results.md / decisions 9 Nov: Seedance 2.0 on ISEKAI ZERO


@lru_cache(1)
def takes(B):
    """the takes made by the end of this section, oldest first: dicts with u (made, UTC epoch), app (song time the
    cell appears), name (as the log prints it), model, in_cut, failed, file"""
    end = B.clock(T_END)
    clip = {r["job"]: r["clip"] for r in B.rows("spend")}
    clip.update({r["file"]: r["clip"] for r in B.rows("spend") if r["file"]})
    out = []
    for r in B.rows("takes"):
        if r["take"] == "rough-1":  # an edit, not a take (data/README)
            continue
        u = _ts(r["ts"]) if r["ts"] else None
        m = re.search(r"-([0-9a-f]{8})$", r["take"])
        known = u is not None
        if u is None and m and ("opening" in (r["batch"] or "") or "isk0" in r["take"]):
            u = float(int(m.group(1), 16))  # an ISEKAI ZERO media id: its first 4 bytes are its creation time
            known = True
        model = r["model"]
        if model:
            model = model.split("/")[-1]
        elif "grok" in r["take"]:
            model = "grok imagine"
            u = u or B.T0  # Lati's test-1 Grok takes, 7-8 Nov: made before this stretch
        elif m:
            model = MODEL_ISK
        if u is None or u > end:
            continue
        failed = r["ledger_status"] == "failed"
        name = r["take"]
        if r["ledger_status"]:  # the ledger's clip id (s054-2-sd25, T1-D), matched by the job id
            job = re.search(r"job ([A-Za-z0-9]{8})", name).group(1) if failed else name[-8:]
            name = clip.get(r["file"]) or clip[job]
        elif m:
            name = name[: m.start()]
        out.append(dict(u=u, known=known, batch=r["batch"], name=name, take=r["take"], model=model, in_cut=bool(r["in_cut"]), failed=failed,
                        file=r["file"], cost=r.get("cost_usd"), shot=r["shot"]))
    out.sort(key=lambda d: d["u"])
    prev = -1e9
    for d in out:  # a take appears at its own time, never sooner; a burst is spread 0.06 s apart to stay countable
        a = max(B.song_at(d["u"]), T_IN, prev + 0.06)
        d["app"] = prev = a
    return out


@lru_cache(256)
def thumb(take, file):
    """the take's first frame, 32x18, dithered to the main film's palette (G.quantize): RGBA uint8"""
    import cv2
    import film3_gfx as G
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"thumb-{take.replace(' ', '_')}.png"
    if not p.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(F3 / file), "-frames:v", "1", "-vf",
                        "scale=128:72:flags=area", str(p)], check=True)
    im = cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2RGB).astype(np.float32)
    small = cv2.resize(im, (32, 18), interpolation=cv2.INTER_AREA)
    q = G.quantize(small, spread=24.0).astype(np.uint8)
    rgba = np.dstack([q, np.full(q.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)


# ---------- the inserts: (opens, closes, master start, take name for the cell it opens from, note line, caption: his
# words about that take, an excerpt; the take's name is in the window's title)
# each opens on the beat at or after Lati's approval of that shot (notes.json time), from the master where it plays
INSERTS = [
    (46.35, 46.91, 46.35, "s033-6-sd25", 528, "very good."),   # 9 Nov 19:07Z; in the cut at 0:45.79 (the same moment)
    (46.91, 49.12, 91.33, "s054-2-sd25", 551, "awsome, entirely."),  # 9 Nov 19:38Z; in the cut at 1:31.33
    (56.87, 58.98, 8.79, "s006-r-h2-1", 598, "pretty cool."),    # 10 Nov 06:52Z (to Flint); in the cut at 0:08.79
    (64.62, 66.81, 80.33, "s050-claudia", 738, "works, hal is done."),   # 10 Nov 15:47Z; s050 (locked render), 1:18.62-1:21.16
]
# Kiln, 12 Nov: "a moving mouth on no vocal reads wrong": s050 is held on one frame of the master, the one with her mouth
# closest to closed in 78.6-81.1 (80.33, read from face crops at 12 fps and then frame by frame)
HOLD = {"s050-claudia"}
VW, VH = 288, 162  # the insert's picture, in 1920 units


@lru_cache(8)
def insert_frames(m0, dur):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"master-{m0:.2f}-{dur:.2f}-crop.npy"  # cropped above the main film's lyric line (y < 900)
    if not p.exists():
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{m0:.3f}", "-i", str(MASTER), "-t", f"{dur + 0.1:.3f}",
                              "-vf", f"fps=24,crop=1600:900:160:0,scale={VW * 2}:{VH * 2}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, VH * 2, VW * 2, 3)
        np.save(p, a)
    return np.load(p)


# ---------- the words, each checked against its source
@lru_cache(1)
def notes(B):
    return {r["decisions_line"]: r for r in B.rows("notes")}


def _note(B, line, excerpt):
    r = notes(B)[line]
    assert excerpt in r["quote"], (line, excerpt)
    return _ts(r["ts"]), r


@lru_cache(1)
def f3_text(rel):
    return (F3 / "production" / rel).read_text()


KILN_JSONL = Path.home() / ".claude/projects/-home-shegs-Claudia/85bff6f8-ec89-4d67-bd26-a10e71acc6c2.jsonl"


@lru_cache(4)
def kiln_line(excerpt):
    """a line of Kiln's own, checked against his session transcript: the jsonl (600+ MB) is streamed once and the
    paragraph holding the excerpt cached with its record's uuid and time (media/chorus1/cache/kiln-lines.json).
    Returns the record's time (UTC epoch s)."""
    p = CACHE / "kiln-lines.json"
    found = json.loads(p.read_text()) if p.exists() else {}
    if excerpt not in found:
        key = excerpt.split(" was ")[0].encode()  # an ASCII part, as it is in the raw jsonl
        with open(KILN_JSONL, "rb") as f:
            for raw in f:
                if key not in raw:
                    continue
                r = json.loads(raw)
                if r.get("type") != "assistant":
                    continue
                for part in r.get("message", {}).get("content", []):
                    txt = part.get("text", "") if isinstance(part, dict) else ""
                    if excerpt in txt:
                        para = next(x for x in txt.split("\n") if excerpt in x)
                        found[excerpt] = dict(uuid=r["uuid"], ts=r["timestamp"], text=para)
                        break
                if excerpt in found:
                    break
        assert excerpt in found, f"not in Kiln's session: {excerpt}"
        CACHE.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(found, ensure_ascii=False, indent=1))
    rec = found[excerpt]
    assert excerpt in rec["text"]
    return _ts(rec["ts"])


def _f3(rel, excerpt):
    assert excerpt in f3_text(rel), (rel, excerpt)
    return excerpt


# the chorus's verdicts: (decisions.md line, excerpt); shown on the beat at or after the time he sent it
VERDICTS = [
    (502, "Overall wan reads as more 3d animated and seedance as 80s cinematic anime."),
    (581, "both are good. seedance 2.0 holds up quite well."),
    (592, "Run opening plates with alternates, but in batch of 4, then stop for my review for them."),
    (598, "S005: both have same problem, fleet is stationary, then starts moving."),
    (696, "yeah, for lipsync, 2.5. 2.0 invents second mic boom, and lipsync is weaker. clear result."),
]


def _next_beat(t):
    import film3_gfx as G
    i = int(np.searchsorted(G.BEATS, t - 1e-3))
    return float(G.BEATS[min(i, len(G.BEATS) - 1)])


@lru_cache(1)
def verdicts(B):
    out = []
    for line, ex in VERDICTS:
        u, r = _note(B, line, ex)
        who = "LATI" if r["to"] == "Kiln" else f"LATI TO {r['to'].upper()}"
        out.append(dict(t=_next_beat(B.song_at(u)), head=f"{who} · {_eet(u)} EET", text=ex))
    return out


# verse 2: what went wrong. Each item: (song time, header, [(voice, text)]); voices: LATI (amber), KILN (clay),
# LEDGER (red). Built at load from the sources, each excerpt asserted.
V2_BEATS = [66.81, 67.92, 69.05, 70.08, 71.18, 72.26, 73.38, 74.49, 75.59, 76.72, 77.83]


@lru_cache(1)
def wrongs(B):
    sp = {r["job"]: r for r in B.rows("spend")}
    fails = [r for r in B.rows("spend") if r["status"] == "failed"]
    it = []
    # 1. the LoRA set aside (7 Nov)
    u, _ = _note(B, 167, "yes, set it aside")
    it.append((u, "LoRA set aside", [("LATI", "yes, set it aside"),
              ("KILN", _f3("decisions.md", "her LoRA is set aside (dataset, captions and look tests kept)"))], ()))
    # 2. Grok too modern (9 Nov)
    u, _ = _note(B, 511, "looks very 3d and not 80s anime.")
    it.append((u, "Grok Imagine on the battle plates: too modern",
               [("LATI", "looks very 3d and not 80s anime."), ("LATI", "but is way too \"modern\".")], ("grok",)))
    _note(B, 511, "but is way too \"modern\".")
    # 3. s037-1 shoots its own (9 Nov)
    u, _ = _note(B, 528, "s037-1 error in here, claude mech ends up shooting at identical one too.")
    it.append((u, "Battle 1 takes", [("LATI", "s037-1 error in here, claude mech ends up shooting at identical one too.")],
               ("s037-1-sd25",)))
    # 4. the copyright filter on our own designs (9 Nov): four failed jobs
    f9 = [r for r in fails if r["ts"].startswith("2026-11-09")]
    assert len(f9) == 4 and all("output video may be related to copyright" in r["error"] for r in f9)
    _note(B, 563, "we know they are original designs, we made them.")
    it.append((_ts(f9[0]["ts"]), f"{', '.join(sorted({r['clip'] for r in f9}))}: {len(f9)} jobs FAILED",
               [("LEDGER", f9[0]["error"]), ("LATI", "we know they are original designs, we made them.")], ("failed",)))
    # 5. the library's best fits (10 Nov)
    ex = "I have \"warp\" selected for example, but there are fight and hangar clips. something is wrong."
    u, _ = _note(B, 791, ex)
    it.append((u, "The library's \"best fits\" ignored the filters", [("LATI", ex)], ()))
    # 6. Kdenlive's import (10 Nov)
    u, r = _note(B, 820, "a: nothing happens. b: nothing happens.")
    assert "Kdenlive's OpenTimelineIO import" in r["context"]
    it.append((u, "Kdenlive's OpenTimelineIO import", [("LATI", "a: nothing happens. b: nothing happens.")], ()))
    # 7. B2-2, mechs firing at their own (11 Nov)
    ex = ("B2-2 is weakest: ships in view do nothing and mechs are shooting somewhere that appears one of their own, "
          "then explode seemingly for no reason.")
    u, _ = _note(B, 889, ex)
    it.append((u, "Mid-1 batch 2: s032 retake", [("LATI", ex)], ()))
    # 8. the copyright filter on our own vocal (11 Nov)
    f11 = [r for r in fails if r["ts"].startswith("2026-11-11")]
    assert len(f11) == 1 and "output audio may be related to copyright" in f11[0]["error"]
    it.append((_ts(f11[0]["ts"]), f"{f11[0]['clip']}: FAILED",
               [("LEDGER", f11[0]["error"]), ("KILN", _f3("motion/mid-2-run.md", "our own vocal; failed jobs cost 0"))],
               ()))
    # 9-10. motion before the plates were seen; the "too realistic" end (11 Nov)
    ex = "plates to review first, then genning motion after approval. just now you went ahead without confirmation."
    u, _ = _note(B, 1016, ex)
    it.append((u, "The nuclear end, again: plates first",
               [("LATI", ex), ("KILN", _f3("decisions.md",
                                           "I ran motion before he had seen the plates ($2.79 on two takes neither of which works)."))],
               ()))
    ex = "realistic is too realistic in terms of style and explosions are equally spaced."
    _note(B, 1016, ex)
    it.append((u + 1, "s108-anime, s108-real", [("LATI", ex)], ()))
    # 11. Lati's held s069 still, overwritten: Kiln's reply in his session (decisions.md line 1032 records only
    # "Kept: Lati's s069 edits on V3"); checked against the transcript (kiln_line)
    ex = "the V3 s069 still at 1:52.08 was your edit, a held frame after your ×3 launch, not a placeholder."
    u = kiln_line(ex)
    it.append((u, "edit/timeline.json: the V3 s069 still",
               [("KILN", ex), ("SOURCE", "Kiln's session, " + datetime.fromtimestamp(u, timezone.utc).strftime("%d %b %H:%MZ"))],
               ()))
    it.sort(key=lambda x: x[0])
    assert len(it) == len(V2_BEATS)
    return [dict(t=V2_BEATS[k], u=u, head=h, lines=ls, cells=cells) for k, (u, h, ls, cells) in enumerate(it)]


# ---------- drawing helpers
def _cw(px, rows_=9):
    import film3_gfx as G
    return G._font(rows_ * 1.15).measureText("M") * px


def wrap(text, width, px=2):
    n = max(8, int(width / _cw(px)))
    out, cur = [], ""
    for w in text.split(" "):
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return out + ([cur] if cur else [])


def typed(text, t, t0, cps=90.0):
    if t < t0:
        return ""
    return text[: int((t - t0) * cps) + 1]


def rect(c, x, y, w, h, color, a, fill=True, sw=1.5):
    import film3_gfx as G
    p = skia.Paint(Color=G.col(color, a), AntiAlias=True)
    if not fill:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(sw)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)


def lerp(a, b, k):
    return a + (b - a) * k


# ---------- the wall's two layouts: the chorus wall and verse 2's strip
WALL = dict(x=300, y=176, cols=12, px=70, py=42, w=66, h=37)
STRIP = dict(x=300, y=168, cols=24, px=35, py=21, w=33, h=18.5)


def cell_rect(i, t):
    k = 0.0 if t < T_V2 else min(1.0, (t - T_V2) / 0.25)
    k = k * k * (3 - 2 * k)
    out = []
    for L in (WALL, STRIP):
        out.append((L["x"] + (i % L["cols"]) * L["px"], L["y"] + (i // L["cols"]) * L["py"], L["w"], L["h"]))
    a, b = out
    return tuple(lerp(a[j], b[j], k) for j in range(4))


def draw_wall(c, t, B, hot=()):
    ts = takes(B)
    shown = [d for d in ts if d["app"] <= t]
    hot_t = None
    for i, d in enumerate(ts):
        if d["app"] > t:
            continue
        x, y, w, h = cell_rect(i, t)
        age = t - d["app"]
        k = min(1.0, age / 0.12)  # the picture wipes in top to bottom
        is_hot = ("failed" in hot and d["failed"]) or ("grok" in hot and d["model"] == "grok imagine") or d["name"] in hot
        if d["failed"]:
            rect(c, x, y, w, h * k, B.RED, 0.55)
            rect(c, x, y, w, h, B.RED, 0.9, fill=False, sw=1.5)
            if w > 50:
                B.crt(c, "FAILED", x + 4, y + h / 2 - 9, px=1, rows_=9, color=B.WHITE, alpha=0.9, glow=False)
        else:
            img = thumb(d["take"], d["file"])
            dim = 1.0 if d["in_cut"] else 0.30
            if is_hot:
                dim = 1.0
            c.save()
            c.clipRect(skia.Rect.MakeXYWH(x, y, w, h * k))
            c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kNearest),
                            skia.Paint(Alphaf=dim))
            c.restore()
            if d["in_cut"]:
                rect(c, x - 1, y - 1, w + 2, h + 2, B.AMBER, 0.75, fill=False, sw=1.2)
        if age < 0.25:  # arrival flash
            rect(c, x - 2, y - 2, w + 4, h + 4, B.WHITE, 0.9 * (1 - age / 0.25), fill=False, sw=2.5)
        if is_hot:
            rect(c, x - 2, y - 2, w + 4, h + 4, B.RED, 0.95, fill=False, sw=2.5)
    return shown


def draw_counts(c, t, B, shown, y=440, a=1.0):
    made = sum(1 for d in shown if not d["failed"])
    cut = sum(1 for d in shown if d["in_cut"])
    fail = sum(1 for d in shown if d["failed"])
    x = CX0
    for lab, v, colr in (("TAKES", made, B.AMBER), ("IN FINAL CUT", cut, B.AMBER), ("FAILED", fail, B.RED)):
        x += B.crt(c, lab + " ", x, y, px=2, rows_=9, color=B.CYAN, alpha=0.85 * a, glow=False)
        x += B.crt(c, f"{v:<4}", x, y, px=2, rows_=9, color=colr, alpha=a) + 14


def draw_log(c, t, B, shown, x=CX0, y0=576, n=7):
    rows_ = shown[-n:]
    for k, d in enumerate(rows_):
        y = y0 + k * 30
        new = t - d["app"] < 0.35
        hm = _eet(d["u"], "%H:%M") if d["known"] else "test1"  # Lati's test-1 Grok takes: no time in the record
        x1 = x + B.crt(c, hm + " ", x, y, px=2, rows_=9, color=B.CYAN, alpha=0.55, glow=False)
        x1 += B.crt(c, f"{d['name'][:18]:<18}", x1, y, px=2, rows_=9,
                    color=B.WHITE if new else (B.RED if d["failed"] else B.AMBER), alpha=0.95, glow=False)
        tail = "FAILED" if d["failed"] else d["model"]
        B.crt(c, tail[:17], x1, y, px=2, rows_=9, color=B.RED if d["failed"] else B.CYAN, alpha=0.8, glow=False)


def draw_verdict(c, t, B):
    vs = verdicts(B)
    cur = [v for v in vs if v["t"] <= t]
    if not cur or t >= T_V2:
        return
    v = cur[-1]
    d = t - v["t"]
    B.crt(c, typed(v["head"], t, v["t"], 160), CX0, 478, px=2, rows_=9, color=B.CYAN, alpha=0.75, glow=False)
    txt = "“" + v["text"] + "”"
    lines = wrap(txt, CX1 - CX0, 2)
    pos = 0
    for k, ln in enumerate(lines):
        s = typed(ln, t, v["t"] + 0.12 + pos / 110.0, 110)
        pos += len(ln)
        B.crt(c, s, CX0, 506 + k * 27, px=2, rows_=9, color=B.WHITE if d < 0.55 else B.AMBER, alpha=1.0)


def draw_insert(c, t, B):
    ts = {d["name"]: (i, d) for i, d in enumerate(takes(B))}
    for t0, t1, m0, name, line, cap in INSERTS:
        if not (t0 <= t < t1):
            continue
        _note(B, line, cap)
        hold = name in HOLD
        frames = insert_frames(m0, 0.05 if hold else t1 - t0)
        fi = 0 if hold else min(len(frames) - 1, int((t - t0) * 24))
        W, H = VW + 20, 24 + VH + 38
        WX, WY = CX1 - W, 790 - H
        # opens out of its cell, closes back into it
        joined_in = any(abs(b - t0) < 1e-6 for a, b, *_ in INSERTS)  # back to back: the window stays open
        joined_out = any(abs(a - t1) < 1e-6 for a, b, *_ in INSERTS)
        k = min(1.0, 1.0 if joined_in else (t - t0) / 0.12, 1.0 if joined_out else (t1 - t) / 0.08)
        k = k * k * (3 - 2 * k)
        i, d = ts[name]
        cx, cy, cw, ch = cell_rect(i, t)
        x, y, w, h = lerp(cx, WX, k), lerp(cy, WY, k), lerp(cw, W, k), lerp(ch, H, k)
        rect(c, x, y, w, h, 0x05060a, 0.92)
        rect(c, x, y, w, h, B.CYAN, 0.9, fill=False, sw=1.5)
        if k < 0.98:
            continue
        rect(c, x, y, w, 24, B.CYAN, 0.18)
        mt = m0 if hold else m0 + (t - t0)
        B.crt(c, f"{d['name']} @ {int(mt // 60)}:{mt % 60:05.2f}", x + 8, y + 3, px=2, rows_=9, color=B.CYAN,
              alpha=0.9, glow=False)
        f = frames[fi]
        rgba = np.dstack([f, np.full(f.shape[:2], 255, np.uint8)])
        img = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)
        vx, vy = x + 10, y + 28
        c.drawImageRect(img, skia.Rect.MakeXYWH(vx, vy, VW, VH), skia.SamplingOptions(skia.FilterMode.kLinear))
        p = skia.Paint(Color=B.col(0x000000, 0.32))
        for yy in range(0, VH, 3):  # scanlines, as a terminal shows it
            c.drawRect(skia.Rect.MakeXYWH(vx, vy + yy + 2, VW, 1), p)
        B.crt(c, typed("“" + cap + "”", t, t0 + 0.1, 60), x + 10, y + 28 + VH + 8, px=2, rows_=9, color=B.AMBER, alpha=1.0, glow=False)


VOICE = {"LATI": "AMBER", "KILN": "CLAY", "LEDGER": "RED", "SOURCE": "CYAN"}


def draw_wrongs(c, t, B):
    items = [it for it in wrongs(B) if it["t"] <= t]
    B.crt(c, "WHAT WENT WRONG", CX0, 262, px=3, rows_=9, color=B.RED, alpha=1.0)
    B.crt(c, "from decisions.md, the ledger, a run file and Kiln's session", CX0, 300, px=2, rows_=9, color=B.CYAN,
          alpha=0.6, glow=False)
    LH, GAP, TOP, BOT = 27, 12, 342, 790
    gut = _cw(2) * 7
    # lay out every item, then scroll so the newest sits above the bottom
    blocks = []
    y = 0
    for it in items:
        lines = [("HEAD", f"{_eet(it['u'], '%d %b %H:%M')}  {it['head']}", 0)]
        for voice, txt in it["lines"]:
            q = txt if voice in ("LEDGER", "SOURCE") else "“" + txt + "”"
            for j, ln in enumerate(wrap(q, CX1 - CX0 - gut, 2)):
                lines.append((voice, ln, j))
        blocks.append((it, y, lines))
        y += len(lines) * LH + GAP
    if not blocks:
        return
    # scroll: eased to each new item's offset over 0.25 s
    def off_for(n):
        it, yb, lines = blocks[n]
        return max(0.0, yb + len(lines) * LH - (BOT - TOP))
    n = len(blocks) - 1
    k = min(1.0, (t - blocks[n][0]["t"]) / 0.25)
    k = k * k * (3 - 2 * k)
    off = lerp(off_for(n - 1) if n > 0 else 0.0, off_for(n), k)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(CX0 - 10, TOP - 4, CX1 + 10, BOT + 6))
    for bi, (it, yb, lines) in enumerate(blocks):
        newest = bi == len(blocks) - 1
        a = 1.0 if newest else 0.55
        t0 = it["t"]
        pos = 0
        for li, (voice, ln, j) in enumerate(lines):
            yy = TOP + yb + li * LH - off
            if yy < TOP - LH or yy > BOT:
                pos += len(ln)
                continue
            start = t0 + pos / 140.0
            pos += len(ln)
            s = typed(ln, t, start, 140) if newest else ln
            if voice == "HEAD":
                B.crt(c, s, CX0, yy, px=2, rows_=9, color=B.RED, alpha=a)
                continue
            if j == 0 and s and voice != "SOURCE":
                B.crt(c, voice, CX0, yy, px=2, rows_=9, color=B.CYAN, alpha=0.6 * a, glow=False)
            colr = getattr(B, VOICE[voice])
            if newest and voice == "LATI" and t - t0 < 0.9:
                colr = B.WHITE
            B.crt(c, s, CX0 + gut, yy, px=2, rows_=9, color=colr, alpha=a, glow=newest)
    c.restore()
    return items[-1]["cells"] if items else ()


def draw_cursor(c, t, B):
    i, pos = B.G.beat_no(t)
    on = (t - B.G.BEATS[i]) < 0.28
    if on:
        rect(c, CX0, 320, 14, 24, B.AMBER, 0.9)


def draw(c, t, B):
    if t >= T_BRK:  # the break: silence; the base whites out the gauge and types the summary
        draw_cursor(c, t, B)
        return
    hot = ()
    if t >= T_V2 + 0.25:  # once the wall has shrunk to its strip
        hot = draw_wrongs(c, t, B) or ()
    shown = draw_wall(c, t, B, hot)
    if t < T_V2:
        a = min(1.0, (t - T_IN) / 0.2)
        draw_counts(c, t, B, shown, a=a)
        draw_verdict(c, t, B)
        draw_log(c, t, B, shown)
        draw_insert(c, t, B)
    else:
        a = max(0.0, 1 - (t - T_V2) / 0.3)
        if a > 0:
            draw_counts(c, t, B, shown, a=a)
