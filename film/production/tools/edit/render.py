#!/usr/bin/env python3
"""Render Lati's cut from production/edit/timeline.json: the picture /cut and /edit play, frame for frame, with the song.

    python3 production/tools/edit/render.py                       # -> media/render/cut-<saved>.mp4, 1280x720, 24 fps
    python3 production/tools/edit/render.py --from 60 --to 75     # a stretch, for checks
    python3 production/tools/edit/render.py --tail 5              # the master's 5 s of black after the song (end screens)

Kiln, 12 Nov 2026 (the graphics plan, step 1: "the render from Lati's timeline"). timeline.flatten() gives what plays:
the upper track where clips overlap, the clip's start, in-point and speed; black where a take has no frames. Each piece
is decoded with ffmpeg to raw frames on the 24 fps grid (boundaries rounded to whole frames) and streamed into one
encoder with the song, so the count is exact by construction (joining encoded pieces dropped and reordered frames at
the seams, 12 Nov). Graphics come later as layers over this picture (gfx.py), on the same song clock.
"""
import argparse
import subprocess
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:  # only --gfx needs it
    np = None

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import timeline  # noqa: E402

FPS, W, H = 24, 1280, 720
SONG = ROOT / "media/song/parempi.wav"
VF = ""


def set_size(w, h):
    """the output size: 1280x720 for checks, 1920x1080 for the master (Lanczos: film 1's upscale decision, 22 Oct)"""
    global W, H, VF, FRAME
    W, H = w, h
    VF = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
    FRAME = W * H * 3
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p"]


def fr(t):
    return round(t * FPS)


FRAME = W * H * 3
set_size(W, H)


def frames(p, a, b):
    """raw RGB frames a..b (song frames) of one flattened piece: exactly b - a of them"""
    n = b - a
    if p["kind"] == "image":
        cmd = ["ffmpeg", "-v", "error", "-loop", "1", "-i", str(ROOT / p["file"]), "-vf", f"{VF},fps={FPS}"]
    elif p["kind"] == "video":
        sp = p.get("speed") or 1
        t_in = p["in"] + (a / FPS - p["start"]) * sp  # the file's time at this piece's first frame
        lead = max(0, round(-t_in / sp * FPS))  # frames before the take's first frame: black
        t_in = max(0.0, t_in)
        # setpts stretches the take by its speed; tpad adds black before its first and past its last frame
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{t_in:.4f}", "-i", str(ROOT / p["file"]), "-an", "-vf",
               f"setpts=(PTS-STARTPTS)/{sp},fps={FPS},{VF},tpad=start_duration={lead / FPS:.4f}:start_mode=add:"
               f"stop_duration=60:stop_mode=add"]
    else:
        return bytes(FRAME * n)
    raw = subprocess.run(cmd + ["-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    if len(raw) < FRAME * n:  # never expected; pad with black so the song stays in sync, and say so
        print(f"  short by {n - len(raw) // FRAME} frames: {p.get('label') or p.get('file')}", file=sys.stderr)
        raw += bytes(FRAME * n - len(raw))
    return raw[:FRAME * n]


def render_lock():
    """one render at a time across sessions and agents (the CPU is shared): waits for media/gfx/render.lock"""
    import fcntl
    (ROOT / "media/gfx").mkdir(parents=True, exist_ok=True)
    f = open(ROOT / "media/gfx/render.lock", "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("waiting for another render (media/gfx/render.lock)", file=sys.stderr)
        fcntl.flock(f, fcntl.LOCK_EX)
    return f  # held until the process ends


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=None)
    ap.add_argument("--tail", type=float, default=0.0, help="seconds of black after the song (a master: 8, measured; 13 Nov: 5.000 s was too tight for YouTube end screens)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--gfx", action="store_true", help="the graphics layer over the cut (run with media/cache/gfx-venv)")
    ap.add_argument("--off", default="", help="graphics modules to switch off, e.g. impact,grain")
    ap.add_argument("--size", type=int, default=720, choices=(720, 1080), help="output height (1080: the master)")
    ap.add_argument("--only", default="", help="load only these sections, e.g. sec_b_battles (default: all)")
    a = ap.parse_args()
    set_size(a.size * 16 // 9, a.size)
    gfx = None
    if a.gfx:
        sys.path.insert(0, str(ROOT / "production/tools/gfx"))
        import base as gfx  # noqa: E402
        gfx.load_sections([x for x in a.only.split(",") if x] or None)
        for m in filter(None, a.off.split(",")):
            gfx.MODULES[m] = False
    lock = render_lock()
    tl = timeline.load()
    flat = timeline.flatten(tl)
    end = a.t1 if a.t1 is not None else flat["duration"]
    f0, f1 = fr(a.t0), fr(end)
    tail = round(a.tail * FPS)
    stamp = (tl.get("saved") or "").replace(" ", "-").replace(":", "")[:15]
    out = ROOT / (a.out or f"media/render/{'gfx' if a.gfx else 'cut'}-{stamp}{'' if (a.t0, a.t1) == (0.0, None) else f'-{a.t0:g}-{end:g}'}.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = (f1 - f0 + tail) / FPS
    # one encoder, fed raw frames in order: the frame count is exact by construction, and graphics can draw on them
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-ss", f"{f0 / FPS:.4f}", "-t", f"{dur:.4f}", "-i", str(SONG),
                            "-map", "0:v", "-map", "1:a", *ENC, "-c:a", "aac", "-b:a", "256k",
                            "-af", f"apad=whole_dur={dur:.4f}", "-t", f"{dur:.4f}", str(out)], stdin=subprocess.PIPE)
    n_pieces = 0
    for p in flat["shots"]:
        a_, b_ = max(fr(p["t0"]), f0), min(fr(p["t1"]), f1)
        if b_ > a_:
            raw = frames(p, a_, b_)
            if gfx:
                arr = np.frombuffer(raw, np.uint8).reshape(b_ - a_, H, W, 3)
                raw = b"".join(gfx.frame(arr[k].copy(), (a_ + k) / FPS).tobytes() for k in range(b_ - a_))
            enc.stdin.write(raw)
            n_pieces += 1
    enc.stdin.write(bytes(FRAME * tail))
    enc.stdin.close()
    enc.wait()
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout or 0)
    print(f"{out.relative_to(ROOT)}: {n_pieces} pieces, {n} frames (expected {f1 - f0 + tail}), "
          f"timeline saved {tl.get('saved')}")


if __name__ == "__main__":
    main()
