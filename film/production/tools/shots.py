#!/usr/bin/env python3
"""Build the shots the review player's /cut plays: each shot's default take linked to media/clips/shot/<shot>.mp4 (it
plays from the shot's start), and the locked graphics renders copied to media/gfx/locked/<shot>.mp4 with a sidecar
<shot>.json giving the song time of their first frame.

    python3 production/tools/shots.py

Kiln, 10 Nov 2026 (Lati: "do a proper cut preview for it. In that player I can make notes and choose between alternate
shots"). Defaults: production/edit/takes.json and gfx.json. Lati's picks in the player (Use for) come first in cutplan.
"""
import glob
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHOT = ROOT / "media/clips/shot"
LOCKED = ROOT / "media/gfx/locked"


def main():
    takes = json.loads((ROOT / "production/edit/takes.json").read_text())["takes"]
    gfx = json.loads((ROOT / "production/edit/gfx.json").read_text())["gfx"]
    SHOT.mkdir(parents=True, exist_ok=True)
    LOCKED.mkdir(parents=True, exist_ok=True)
    for f in SHOT.glob("*.mp4"):
        if f.is_symlink():
            f.unlink()
    made, missing = [], []
    for sid, pat in sorted(takes.items()):
        hits = sorted(glob.glob(str(ROOT / "media/clips" / pat) + ".mp4"))
        if not hits:
            missing.append(sid)
            continue
        os.symlink(os.path.relpath(hits[0], SHOT), SHOT / f"{sid}.mp4")
        made.append(sid)
    for sid, g in gfx.items():
        shutil.copy2(ROOT / g["file"], LOCKED / f"{sid}.mp4")
        (LOCKED / f"{sid}.json").write_text(json.dumps({"t0": g["t0"], "from": g["file"]}) + "\n")
    print(f"{len(made)} shots linked, {len(gfx)} renders locked; no take found: {missing}")


if __name__ == "__main__":
    main()
