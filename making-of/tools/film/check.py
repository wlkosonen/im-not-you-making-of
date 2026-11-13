#!/usr/bin/env python3
"""Single frames for frame checks: ~/Im\\ not\\ you/media/cache/gfx-venv/bin/python tools/film/check.py --at 50,51.5 --out media/x/check [--only sec_x]
Writes <out>/<t>.jpg at 1280x720 (--size 1080 for the master size). Takes the render lock. Kiln, 12 Nov 2026."""
import argparse
import fcntl
import sys
from pathlib import Path

import cv2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import base  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--at", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--only", default="")
ap.add_argument("--size", type=int, default=720, choices=(720, 1080))
a = ap.parse_args()
(ROOT / "media").mkdir(exist_ok=True)
lock = open(ROOT / "media/render.lock", "w")
fcntl.flock(lock, fcntl.LOCK_EX)
base.load_sections([x for x in a.only.split(",") if x] or None)
out = ROOT / a.out
out.mkdir(parents=True, exist_ok=True)
for t in [float(x) for x in a.at.split(",")]:
    img = base.frame(t, a.size * 16 // 9, a.size)
    f = out / f"{t:.3f}.jpg"
    cv2.imwrite(str(f), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(f.relative_to(ROOT))
