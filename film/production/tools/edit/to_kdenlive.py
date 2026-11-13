#!/usr/bin/env python3
"""The cut, as an OpenTimelineIO timeline for Kdenlive: what /cut plays now, laid out on tracks, with the song and our
markers, so Lati can edit with the mouse (Lati, 10 Nov 2026: "multiple tracks, stacked, where I can choose each shot
from library and trim and move it to the song with mouse across the timeline").

    ~/ComfyUI/venv/bin/python production/tools/edit/to_kdenlive.py            # -> production/edit/kdenlive/cut-1.otio

Tracks, bottom up: V1 the cut (each shot's pick, take, locked render or plate, as cutplan.plan() resolves it), V2 empty
for overlays, A1 the song. Markers on the timeline: sections, the drop and the break, each lyric line, each sung word,
each board shot's start. 24 fps. Media by absolute path. Kdenlive reads it with File > Import > OpenTimelineIO (it is
built on OTIO 0.18.1, as this is). Reading Lati's edit back: from_kdenlive.py (his OTIO export).
"""
import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import opentimelineio as otio

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "production/tools"))
import cutplan  # noqa: E402

FPS = 24
SONG = ROOT / "media/song/parempi.wav"
ANALYSIS = ROOT / "media/song/analysis/parempi"
OUT = ROOT / "production/edit/kdenlive/cut-1.otio"
M = otio.schema.MarkerColor


def rt(sec):
    return otio.opentime.RationalTime(round(sec * FPS), FPS)


def rng(start, dur):
    return otio.opentime.TimeRange(rt(start), rt(dur))


def url(p):
    # Kdenlive 25.12 reads target_url as a path (a file:// URL got joined onto the .otio's folder and crashed it,
    # 10 Nov); links in media/clips/shot/ are resolved to the take itself
    return str(Path(p).resolve())


@lru_cache(None)
def length(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def media(p, still=False):
    avail = rng(0, 3600) if still else rng(0, length(p))
    return otio.schema.ExternalReference(target_url=url(p), available_range=avail)


def main():
    plan = cutplan.plan()
    tl = otio.schema.Timeline(name="I'm Not You · cut 1", global_start_time=rt(0))
    v1 = otio.schema.Track(name="V1 cut", kind=otio.schema.TrackKind.Video)
    v2 = otio.schema.Track(name="V2 overlays", kind=otio.schema.TrackKind.Video)
    a1 = otio.schema.Track(name="A1 song", kind=otio.schema.TrackKind.Audio)
    # every boundary snapped to its own frame from song time, so nothing drifts along the track
    F = lambda t: round(t * FPS)
    fr = lambda n: otio.opentime.RationalTime(n, FPS)
    def piece(n):
        return otio.schema.Gap(source_range=otio.opentime.TimeRange(fr(0), fr(n)))
    pos = 0
    for s in plan["shots"]:
        f0, f1 = F(s["t0"]), F(s["t1"])
        if f0 > pos:
            v1.append(piece(f0 - pos))
        n = f1 - f0
        f = ROOT / s["file"] if s.get("file") else None
        label = f"{s['id']} · {f.stem if f else 'empty'}"
        if s["kind"] == "video" and f and f.exists():
            start = F(s["t0"] - s["at"])  # the file's frame at the shot's start
            lead = max(0, -start)  # the file starts after the shot does: hold empty first
            start = max(0, start)
            usable = max(0, min(n - lead, int(length(f) * FPS) - start))
            if lead:
                v1.append(piece(lead))
            if usable:
                v1.append(otio.schema.Clip(name=label, media_reference=media(f),
                                           source_range=otio.opentime.TimeRange(fr(start), fr(usable)),
                                           metadata={"kiln": {"shot": s["id"], "src": s["src"]}}))
            if n - lead - usable > 0:
                v1.append(piece(n - lead - usable))
        elif s["kind"] == "image" and f and f.exists():
            v1.append(otio.schema.Clip(name=label, media_reference=media(f, still=True),
                                       source_range=otio.opentime.TimeRange(fr(0), fr(n)),
                                       metadata={"kiln": {"shot": s["id"], "src": "still"}}))
        else:
            v1.append(piece(n))
        pos = f1
    song_len = length(SONG)
    a1.append(otio.schema.Clip(name="parempi (the song)", media_reference=media(SONG), source_range=rng(0, song_len)))
    tl.tracks.extend([v1, v2, a1])

    # markers on the timeline itself: Kdenlive's guides
    def mark(t, name, color, dur=0.0):
        tl.tracks.markers.append(otio.schema.Marker(name=name, marked_range=rng(t, dur), color=color))

    beats = json.loads((ANALYSIS / "beats.json").read_text())
    for sec in beats.get("sections", []):
        mark(sec["t0"], f"§ {sec.get('name') or sec.get('label')}", M.GREEN)
    board = json.loads((ROOT / "production/board/board.json").read_text())
    for h in board.get("hits", []):
        mark(h["t"], f"! {h['name']}", M.RED)
    for s in board["shots"]:
        mark(s["t0"], s["id"], M.YELLOW)
    words = json.loads((ANALYSIS / "words.json").read_text())
    for ln in words["lines"]:
        if ln["t0"] is not None:
            mark(ln["t0"], f"♪ {ln['text']}", M.CYAN)
    for w in words["words"]:
        if w["t0"] is not None:
            mark(w["t0"], w["w"], M.MAGENTA)
    mark(116.083, "♪ Me", M.CYAN)  # Lati's marker, 10 Nov (the aligner missed it)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    otio.adapters.write_to_file(tl, str(OUT))
    n = sum(1 for c in v1 if isinstance(c, otio.schema.Clip))
    print(f"{OUT.relative_to(ROOT)}: {n} clips on V1, {len(tl.tracks.markers)} markers, {tl.duration().to_seconds():.2f} s")


if __name__ == "__main__":
    main()
