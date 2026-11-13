#!/usr/bin/env python3
"""s050, the break: a red lens set in a box, Claudia inside it as red ASCII, an oscillator speaking the line.

    ~/ComfyUI/venv/bin/python production/tools/gfx/red_lens.py --out media/gfx/s050-red-lens.mp4

Kiln, 10 Nov 2026, from Lati's sketch on draft 2 (a box, an oval lens in it, her face inside the lens) and the board's
s050: "The music stops. A red lens set in a box; inside it Claudia drawn as ASCII code; the oscillator speaks the
line." The whole frame is code over still D37 (her face); the trace is the vocal stem itself, line 15, "I'm afraid I
can't do that, I'm not you" (78.66-81.10 s). CPU only.
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

import terminal_faces as tf

ROOT = Path(__file__).resolve().parents[3]
FACE = ROOT / "media/images/dataset-2/d37-6aef7e1e4793ed8f8e5d3590.jpg"
VOCAL = ROOT / "media/song/analysis/parempi/stems/vocals.wav"
SONG = ROOT / "media/song/parempi.wav"
W, H, FPS, SR = 1920, 1080, 24, 48000


def vocal(t0, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", str(VOCAL), "-ac", "1", "-ar",
                          str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)


def radial(h, w, cx, cy):
    y, x = np.mgrid[0:h, 0:w]
    return np.hypot(x - cx, y - cy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=float, default=78.62)
    ap.add_argument("--end", type=float, default=81.168)
    ap.add_argument("--cell", type=int, default=4)
    ap.add_argument("--clip", default="media/clips/quiet-1/s050-claudia-L9xRlzTT.mp4",
                    help="her lip-synced face (Lati: the still \"reads as a still\"); '' for D37")
    ap.add_argument("--clip-start", type=float, default=78.55, help="song time of the clip's first frame")
    ap.add_argument("--clip-crop", default="340,120,940,720", help="brow-to-chin square in the clip's pixels")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    dur = a.end - a.start
    n = int(round(dur * FPS))
    voc = vocal(a.start, dur + 0.2)
    peak = np.abs(voc).max() + 1e-6

    # the box: a dark panel with a bevel, centred, taller than wide like the sketch
    bw, bh = 760, 1000
    bx, by = (W - bw) // 2, (H - bh) // 2
    yy, xx = np.mgrid[0:H, 0:W]
    inbox = (xx >= bx) & (xx < bx + bw) & (yy >= by) & (yy < by + bh)
    panel = np.zeros((H, W, 3))
    grad = 0.05 + 0.04 * (1 - (yy - by) / bh)
    panel[inbox] = grad[inbox][:, None] * np.array([1.0, 1.0, 1.08])
    edge = inbox & ((xx < bx + 6) | (xx >= bx + bw - 6) | (yy < by + 6) | (yy >= by + bh - 6))
    panel[edge] = 0.32

    # the lens: rings, then the glass
    cx, cy, R = W // 2, by + 400, 300
    r = radial(H, W, cx, cy)
    ring = (r < R + 40) & (r >= R)
    panel[ring] = 0.06
    panel[(r < R + 46) & (r >= R + 40)] = 0.35
    glass = r < R

    # her face, cropped square around the face in D37, fitted to the lens
    face = Image.open(FACE).convert("RGB")
    # tight on the face, brow to chin (D37 is 1536 square: eyes ~y 750, mouth ~y 1135)
    face = face.crop((324, 495, 1246, 1417))
    D = 2 * R
    clip = None
    if a.clip:
        x0, y0, x1, y1 = map(int, a.clip_crop.split(","))
        skip = max(0, round((a.start - a.clip_start) * FPS))
        clip = (Image.fromarray(f).crop((x0, y0, x1, y1)) for j, f in enumerate(tf.frames(ROOT / a.clip)) if j >= skip)
    glyphs = tf.atlas(a.cell, a.cell * 2, 24)

    # the oscillator slot under the lens
    sx0, sx1, sy = bx + 90, bx + bw - 90, by + 820
    slot = (xx >= sx0) & (xx < sx1) & (np.abs(yy - sy) < 70)
    panel[slot] = 0.03

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r",
                            str(FPS), "-i", "-", "-ss", str(a.start), "-t", f"{dur:.3f}", "-i", str(SONG), "-map", "0:v",
                            "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
                            "-b:a", "192k", "-shortest", str(ROOT / a.out)], stdin=subprocess.PIPE)
    eq = None
    rng = np.random.default_rng(50)
    for i in range(n):
        t = i / FPS
        seg = voc[int(t * SR): int((t + 1 / FPS) * SR)]
        amp = float(np.sqrt((seg ** 2).mean()) / peak) if len(seg) else 0.0
        img = panel.copy()

        # a slow push into the lens over the shot
        zoom = 1.0 + 0.05 * t / dur
        src = next(clip, None) if clip is not None else None
        fz = (src or face).resize((int(D * zoom), int(D * zoom)), Image.LANCZOS)
        off = (fz.width - D) // 2
        f = np.asarray(fz.crop((off, off, off + D, off + D))).astype(float) / 255
        small, lum = tf.cells(f, a.cell, a.cell * 2)
        # plain brightness: her black hair, brows and eyes are the drawing, equalising would flatten them
        # and local contrast, so brows, eyes and the moving mouth stand out as sparse characters on the skin
        from scipy import ndimage
        lum = lum + 1.6 * (lum - ndimage.gaussian_filter(lum, 3))
        rank = np.clip((lum - 0.12) / 0.8, 0, 1) ** 1.6
        idx = np.clip(rank * (len(glyphs) - 1), 0, len(glyphs) - 1).round().astype(int)
        rows, cols = idx.shape
        ink = glyphs[idx].transpose(0, 2, 1, 3).reshape(rows * a.cell * 2, cols * a.cell)
        asc = np.zeros((D, D))
        asc[: ink.shape[0], : ink.shape[1]] = ink

        # the glass: a red core that breathes with the voice, her face in red characters on it
        rr = r[cy - R: cy + R, cx - R: cx + R]
        core = np.clip(1 - rr / R, 0, 1) ** 1.6
        bright = 0.55 + 0.45 * amp + 0.02 * rng.standard_normal()
        red = np.stack([0.16 * core + 1.25 * asc * (0.55 + 0.45 * bright), 0.02 * core + 0.16 * asc * bright,
                        0.02 * core + 0.10 * asc * bright], -1) * (0.85 + 0.15 * bright)
        m = (rr < R)[..., None]
        win = img[cy - R: cy + R, cx - R: cx + R]
        img[cy - R: cy + R, cx - R: cx + R] = np.where(m, red, win)

        # the oscillator: the vocal under the frame's few ms, drawn as a red trace
        trace = np.zeros((H, W))
        if len(seg):
            xs = np.arange(sx0, sx1)
            ys = sy - (np.interp(np.linspace(0, len(seg) - 1, len(xs)), np.arange(len(seg)), seg) / peak) * 110
            for dx in (0, 1):
                trace[np.clip(ys.astype(int) + dx, 0, H - 1), xs] = 1.0
        else:
            trace[sy, sx0:sx1] = 1.0
        img += trace[..., None] * np.array([1.0, 0.15, 0.08])

        # glow over the red parts, a highlight on the glass, grain
        lit = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
        glow = np.asarray(lit.filter(ImageFilter.GaussianBlur(18))).astype(float) / 255
        img = img + 0.45 * glow * np.array([1.0, 0.25, 0.25])
        hl = np.exp(-((xx - (cx - 120)) ** 2 + (yy - (cy - 150)) ** 2) / (2 * 55 ** 2)) * glass
        img += hl[..., None] * 0.12
        img += rng.normal(0, 0.012, img.shape)
        enc.stdin.write((np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    print(f"{a.out}: {n} frames, {n / FPS:.2f} s")


if __name__ == "__main__":
    main()
