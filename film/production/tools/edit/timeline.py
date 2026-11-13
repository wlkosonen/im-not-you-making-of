#!/usr/bin/env python3
"""The edit: Lati's multi-track timeline, production/edit/timeline.json (Lati, 10 Nov 2026: "multiple tracks, stacked,
where I can choose each shot from library and trim and move it to the song with mouse across the timeline").

    python3 production/tools/edit/timeline.py --init      # start it from the current cut (cutplan), if none exists

A clip: {"file", "kind" ("video" | "image"), "start" (song s), "in" (file s), "dur" (s), "len" (file s; null for
stills), "label", "shot", optional "speed" (playback rate; the file's time at song time t is in + (t - start) × speed,
and dur stays the length on the timeline; Lati, 11 Nov)}. Tracks bottom up: V1, V2, V3; where clips overlap the upper track plays. The review player's
/edit page edits it (server.py: GET/POST /api/timeline); each save keeps the previous one as timeline.prev.json.
Kiln reads Lati's cut from it for the graphics and the render.
"""
import argparse
import json
import subprocess
import sys
import time
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TL = ROOT / "production/edit/timeline.json"
sys.path.insert(0, str(ROOT / "production/tools"))


@lru_cache(None)
def length(rel):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(ROOT / rel)], capture_output=True, text=True).stdout.strip()
    return round(float(out or 0), 3)


def from_plan():
    import cutplan
    clips = []
    for s in cutplan.plan()["shots"]:
        f = s.get("file")
        if not f or not (ROOT / f).exists():
            continue
        if s["kind"] == "video":
            n = length(f)
            start = max(s["t0"], s["at"])
            inp = start - s["at"]
            end = min(s["t1"], s["at"] + n)
            if end - start > 0.02:
                clips.append({"file": f, "kind": "video", "start": round(start, 3), "in": round(inp, 3),
                              "dur": round(end - start, 3), "len": n, "label": f"{s['id']} · {Path(f).stem}",
                              "shot": s["id"]})
        elif s["kind"] == "image":
            clips.append({"file": f, "kind": "image", "start": s["t0"], "in": 0, "dur": round(s["t1"] - s["t0"], 3),
                          "len": None, "label": f"{s['id']} · {Path(f).stem}", "shot": s["id"]})
    return {"fps": 24, "tracks": [{"name": "V1", "clips": clips}, {"name": "V2", "clips": []},
                                  {"name": "V3", "clips": []}],
            "made": f"from the cut plan, {time.strftime('%Y-%m-%d %H:%M')}", "saved": None}


def flatten(tl, dur=171.2):
    """What plays, as one track (for /cut and the render): where clips overlap the upper track plays, on one track the
    later clip; where a video has no frames there, black. Each piece: song t0-t1, the clip's file, start, in, speed."""
    clips = [(ti, c) for ti, tr in enumerate(tl["tracks"]) for c in tr["clips"]]
    fr = lambda t: round(round(t * 24) / 24, 4)  # every boundary on the frame grid: no slivers
    cuts = sorted({0.0, fr(dur)} | {fr(c["start"]) for _, c in clips} | {fr(c["start"] + c["dur"]) for _, c in clips})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 1e-4:
            continue
        m = (a + b) / 2
        top = None
        for ti, c in clips:
            if fr(c["start"]) <= m < fr(c["start"] + c["dur"]) and (top is None or (ti, c["start"]) > (top[0], top[1]["start"])):
                top = (ti, c)
        piece = {"t0": round(a, 4), "t1": round(b, 4), "kind": "none", "src": "empty", "id": "-"}
        if top:
            c, sp = top[1], top[1].get("speed", 1) or 1
            piece.update({"id": c.get("shot") or "-", "kind": c["kind"], "file": c["file"], "start": c["start"], "in": c["in"],
                          "speed": sp, "len": c.get("len"), "src": f"V{top[0] + 1}", "label": c.get("label", "")})
        if out and out[-1].get("file") == piece.get("file") and out[-1].get("start") == piece.get("start") \
                and out[-1]["src"] == piece["src"] and abs(out[-1]["t1"] - piece["t0"]) < 1e-4:
            out[-1]["t1"] = piece["t1"]
        else:
            out.append(piece)
    return {"duration": dur, "shots": out, "saved": tl.get("saved"), "source": "timeline"}


def load():
    if not TL.exists():
        save(from_plan())
    return json.loads(TL.read_text())


def save(tl):
    TL.parent.mkdir(parents=True, exist_ok=True)
    if TL.exists():
        TL.replace(TL.with_name("timeline.prev.json"))
    tl["saved"] = time.strftime("%Y-%m-%d %H:%M:%S")
    TL.write_text(json.dumps(tl, indent=1) + "\n")
    return tl["saved"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true")
    if ap.parse_args().init:
        t = load()
        print(f"{TL.relative_to(ROOT)}: {sum(len(x['clips']) for x in t['tracks'])} clips")
