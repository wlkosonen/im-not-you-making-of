#!/usr/bin/env python3
"""Single frames of the film with its graphics, for frame checks: the picture exactly as render.py makes it.

    media/cache/gfx-venv/bin/python production/tools/gfx/check.py --at 37.5,38.2 --out media/gfx/opening/check
    media/cache/gfx-venv/bin/python production/tools/gfx/check.py --at 37.5 --only sec_a_opening --full

Writes <out>/<t>.jpg (1280x720; --full keeps PNG). Takes the render lock like render.py (one render at a time).
Kiln, 12 Nov 2026, for the graphics agents.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "edit"))
import base as F  # noqa: E402
import render  # noqa: E402
import timeline  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", required=True, help="song times, comma-separated")
    ap.add_argument("--out", required=True, help="folder, relative to the repo")
    ap.add_argument("--only", default="", help="load only these sections (default: all)")
    ap.add_argument("--off", default="", help="modules to switch off, e.g. grain,karaoke")
    ap.add_argument("--full", action="store_true", help="PNG instead of JPEG")
    ap.add_argument("--size", type=int, default=720, choices=(720, 1080))
    a = ap.parse_args()
    render.set_size(a.size * 16 // 9, a.size)
    lock = render.render_lock()  # noqa: F841
    F.load_sections([x for x in a.only.split(",") if x] or None)
    for m in filter(None, a.off.split(",")):
        F.MODULES[m] = False
    flat = timeline.flatten(timeline.load())
    out = F.ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    import cv2
    for t in [float(x) for x in a.at.split(",")]:
        k = render.fr(t)
        p = next((p for p in flat["shots"] if render.fr(p["t0"]) <= k < render.fr(p["t1"])), None)
        raw = render.frames(p, k, k + 1) if p else bytes(render.FRAME)
        img = np.frombuffer(raw, np.uint8).reshape(render.H, render.W, 3).copy()
        img = F.frame(img, k / render.FPS)
        f = out / f"{t:.3f}.{'png' if a.full else 'jpg'}"
        cv2.imwrite(str(f), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(f.relative_to(F.ROOT), F.shot_at(k / render.FPS)[0])


if __name__ == "__main__":
    main()
