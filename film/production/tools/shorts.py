#!/usr/bin/env python3
"""The Shorts, cut from the master: film 2's method (`~/checked-me/production/tools/shorts.py`).

    media/cache/gfx-venv/bin/python production/tools/shorts.py [media/render/master-1080-v2.mp4]

The 16:9 frame sits whole over a blurred, enlarged copy of itself (cropping to 9:16 would cut off the graphics and the
lyric line); under the picture, inside Shorts' safe area, "full video on the channel" in the film's own CRT letters
(the YouTube analysis of 12 Nov: each Short points to the long video). Lati's picks, 12 Nov. Kiln, 12 Nov 2026.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import skia

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production/tools/gfx"))
import base as F  # noqa: E402

OUT = ROOT / "media/release/shorts"
SHORTS = {  # (from, to) in song time; edges kept off the transitions' frames
    "short-1-bot-farm": (67.50, 81.17),           # "Write the phishing mail" to "I'm not you" (published 12 Nov)
    # 13 Nov, longer, Lati's markers on /cut: the second from s067 to the pilots, the third from "Ask me anything" to the
    # sakura (the old cuts stay in the folder as short-2-ask-me-anything and short-3-me)
    "short-2-me-to-battle-3": (105.13, 128.41),   # s067 (after its CRT roll) to before the 128.54 whip into the pilots
    "short-3-ask-me-anything-to-chorus": (36.243, 56.944),  # "Ask me anything" through chorus 1 to the cut to the sakura
}
LINE, PX, ROWS, Y = "full video on the channel", 4, 13, 1300


def card(path):
    img = np.zeros((1920, 1080, 4), np.uint8)
    c = skia.Surface(img).getCanvas()
    w = F.text_w(LINE) * PX / F.KPX
    x0 = (1080 - w) / 2 - 40  # a little left of centre: Shorts' buttons sit on the right
    c.drawRoundRect(skia.Rect.MakeLTRB(x0 - 28, Y - 22, x0 + w + 28, Y + ROWS * PX + 30), 12, 12,
                    skia.Paint(Color=F.col(0x000000, 0.72), AntiAlias=True))
    F.crt_text(c, LINE, x0, Y, px=PX, rows=ROWS, color=F.AMBER)
    import cv2
    cv2.imwrite(str(path), cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA))


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "media/render/master-1080-v2.mp4"
    OUT.mkdir(parents=True, exist_ok=True)
    cp = OUT / "card.png"
    card(cp)
    for name, (a, b) in SHORTS.items():
        if len(sys.argv) > 2 and name not in sys.argv[2:]:
            continue
        out = OUT / f"{name}.mp4"
        fc = ("[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.12[bg];"
              "[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2[v];[v][1:v]overlay=0:0[o]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src),
                        "-i", str(cp), "-filter_complex", fc, "-map", "[o]", "-map", "0:a", "-c:v", "libx264",
                        "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", str(out)], check=True)
        print(out.relative_to(ROOT), f"{b - a:.2f} s")


if __name__ == "__main__":
    main()
