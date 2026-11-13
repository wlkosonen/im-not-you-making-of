#!/usr/bin/env python3
"""Render the making-of: every frame drawn from song time and the record (data/), with the song.

    ~/Im\\ not\\ you/media/cache/gfx-venv/bin/python tools/film/render.py                 # 1280x720
    ... render.py --from 80 --to 83 --size 1080 --out media/x.mp4                          # a stretch, the master size

Kiln, 12 Nov 2026. Same rules as the main film's render.py: raw frames into one encoder, so the frame count is exact.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import base  # noqa: E402

FPS = 24
SONG = Path("/home/shegs/Im not you/media/song/parempi.wav")
DUR = 171.2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=DUR)
    ap.add_argument("--tail", type=float, default=0.0)
    ap.add_argument("--size", type=int, default=720, choices=(720, 1080))
    ap.add_argument("--out", default=None)
    ap.add_argument("--only", default="", help="load only these sections, e.g. sec_b_motion")
    a = ap.parse_args()
    import fcntl
    (ROOT / "media").mkdir(exist_ok=True)
    lock = open(ROOT / "media/render.lock", "w")  # one render at a time (agents share the CPU)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("waiting for another render (media/render.lock)", file=sys.stderr)
        fcntl.flock(lock, fcntl.LOCK_EX)
    H = a.size
    W = H * 16 // 9
    base.load_sections([x for x in a.only.split(",") if x] or None)
    f0, f1 = round(a.t0 * FPS), round(a.t1 * FPS)
    tail = round(a.tail * FPS)
    out = ROOT / (a.out or f"media/render/making-of-{a.t0:g}-{a.t1:g}.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = (f1 - f0 + tail) / FPS
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-ss", f"{f0 / FPS:.4f}", "-t", f"{dur:.4f}", "-i", str(SONG),
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-af", f"apad=whole_dur={dur:.4f}",
                            "-t", f"{dur:.4f}", str(out)], stdin=subprocess.PIPE)
    for k in range(f0, f1 + tail):
        enc.stdin.write(base.frame(k / FPS, W, H).tobytes())
    enc.stdin.close()
    enc.wait()
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout or 0)
    print(f"{out.relative_to(ROOT)}: {n} frames (expected {f1 - f0 + tail})")


if __name__ == "__main__":
    main()
