#!/usr/bin/env python3
"""A rough cut of the whole film from the board: each shot's take where one exists, its plate as a still where not,
a black card for code shots; the song under it; the shot id and what fills it in the corner.

    python3 production/tools/rough.py --out media/review/rough-2.mp4

Kiln, 10 Nov 2026 (Lati: "could you put a rough cut up and ill review it in the review player?"). The review player
places files named rough-N at the song's 0:00. Takes are chosen by TAKES (Lati's verdicts in decisions.md and the
motion notes); graphics renders by GFX, with the song time of their first frame.
"""

import argparse
import glob
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FPS, W, H = 24, 1280, 720
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# shot -> take (glob under media/clips), in Lati's order of preference where he gave one
TAKES = {
    "s003": "opening/s003-*", "s005": "opening/s005-ff-1-*", "s006": "opening/s006-r-h2-1-*",
    "s007": "opening/s007-*", "s008": "opening/s008-*", "s009": "opening/s009-*", "s010": "opening/s010-*",
    "s011": "opening-or/s011-*", "s012": "opening/s012-*", "s013": "opening/s013-*", "s014": "opening/s014-h1-2-*",
    "s016": "opening/s016-*", "s017": "opening/s017-*", "s018": "opening/s018-*", "s019": "opening/s019-*",
    "s020": "opening/s020-s020-1-*", "s021": "opening/s021-*", "s023": "opening-or/s023-*",
    "s033": "battle-1/s033-*", "s034": "test-2/s034-sd25-*", "s035": "battle-1/s035-*", "s036": "battle-1/s036-*",
    "s037": "battle-1/s037-*", "s038": "battle-1/s038-*",
    "s051": "battle-2-3/s051-*", "s052": "battle-2-3/s052-*", "s053": "battle-2-3/s053-*", "s054": "battle-2-3/s054-*",
    "s056": "battle-2-3/s056-*", "s057": "battle-2-3/s057-*", "s058": "battle-2-3/s058-*", "s059": "battle-2-3/s059-*",
    "s076": "battle-2-3/s076-*", "s078": "battle-2-3/s078-1-sd20-*", "s079": "battle-2-3/s079-*",
    "s080": "battle-2-3/s080-2-sd20-*", "s081": "battle-2-3/s081-*", "s082": "battle-2-3/s082-1-*",
}
# shot -> (render, song time of its first frame)
GFX = {"s050": ("media/gfx/s050-red-lens-sync.mp4", 78.62), "s067": ("media/gfx/s067-dissolve-c4-fast.mp4", 105.0)}
# her and the world's earlier stills outside the v2 plate folder, by the board's plate status
PLATES = json.loads((ROOT / "production/board/picks.json").read_text())


def seg(shot, n, tmp, i):
    sid = shot["id"]
    out = tmp / f"{i:03d}.mp4"
    vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    kind, src, ss = "card", None, 0.0
    if sid in GFX:
        src, t0 = GFX[sid]
        kind, src = "code", ROOT / src
        ss = shot["t0"] - t0  # negative: hold the first frame until the render starts
    elif sid in TAKES and glob.glob(str(ROOT / "media/clips" / TAKES[sid]) + ".mp4"):
        kind, src = "take", Path(sorted(glob.glob(str(ROOT / "media/clips" / TAKES[sid]) + ".mp4"))[0])
    elif PLATES.get("p-" + sid) and (ROOT / PLATES["p-" + sid]["file"]).exists():
        kind, src = "plate", ROOT / PLATES["p-" + sid]["file"]
    label = f"{sid}  {kind}  {shot['chapter']}".replace(":", "\\:").replace("'", "")
    draw = f"drawtext=fontfile={FONT}:text='{label}':x=12:y=12:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6"
    if kind in ("take", "code"):
        pre = ""
        if ss < 0:
            pre, ss = f"tpad=start_duration={-ss:.3f}:start_mode=clone,", 0.0
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", str(src), "-an",
               "-vf", f"{pre}{vf},tpad=stop_mode=clone:stop_duration=10,{draw}", "-frames:v", str(n)]
    elif kind == "plate":
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(src), "-vf", f"{vf},{draw}", "-frames:v", str(n)]
    else:
        what = shot.get("treatment") or shot.get("plate_status") or ""
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}",
               "-vf", draw, "-frames:v", str(n)]
    subprocess.run(cmd + ["-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out)], check=True)
    return out, kind


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="media/review/rough-2.mp4")
    a = ap.parse_args()
    b = json.loads((ROOT / "production/board/board.json").read_text())
    shots = b["shots"] if isinstance(b, dict) else b
    tmp = Path(tempfile.mkdtemp(prefix="rough-"))
    parts, kinds = [], {}
    for i, s in enumerate(shots):
        n = round(s["t1"] * FPS) - round(s["t0"] * FPS)
        p, k = seg(s, n, tmp, i)
        parts.append(p)
        kinds[k] = kinds.get(k, 0) + 1
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i",
                    str(ROOT / "media/song/parempi.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", str(out)], check=True)
    print(f"{a.out}: {len(shots)} shots, {kinds}")


if __name__ == "__main__":
    main()
