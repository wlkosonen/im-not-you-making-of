#!/usr/bin/env python3
"""s067, the terminal faces: four sung clips composited into the 2x2 CRT plate, as colour ASCII or as video.

    ~/ComfyUI/venv/bin/python production/tools/gfx/terminal_faces.py --mode ascii --out media/gfx/s067-ascii.mp4
    ~/ComfyUI/venv/bin/python production/tools/gfx/terminal_faces.py --mode video --out media/gfx/s067-video.mp4

Kiln, 10 Nov 2026. Lati: "lets go with ascii test, but lets use high resolution in terms of symbols used, since the
motion in that shot is so good", and he weighs it against the clips "as is on crts, with some effects and filters".
Both modes share the plate, the screen masks and the CRT finish (scan lines, glow, flicker), so the comparison is only
ASCII against video. CPU only (numpy, PIL, ffmpeg); nothing touches the GPU.
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[3]
PLATE = ROOT / "media/plates/v2/s067-1-6af32d1ef1ba753dad466024.jpg"
CLIPS = ROOT / "media/clips/quiet-1"
# screen order: top left, top right, bottom left, bottom right (the draft's order: Eve, Claudia, Astra, Vera)
FACES = ["s067-eve-jaWZ5e9U.mp4", "s067-claudia-GjYMGDdQ.mp4", "s067-astra-77fjmNae.mp4", "s067-vera-JeFb1b6f.mp4"]
SONG = ROOT / "media/song/parempi.wav"
W, H, FPS = 1920, 1080, 24
CLIP_W, CLIP_H = 1280, 720
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
CHARS = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def screens(plate):
    """The four glass areas: bounding boxes and soft masks, found by brightness (the bezels are dark)."""
    lum = np.asarray(plate.convert("L")).astype(float)
    m = ndimage.binary_opening(lum > 45, iterations=3)
    lab, _ = ndimage.label(m)
    out = []
    for i, o in enumerate(ndimage.find_objects(lab)):
        if (lab[o] == i + 1).sum() > 50000:
            mask = ndimage.binary_erosion(lab == i + 1, iterations=4).astype(float)
            mask = ndimage.gaussian_filter(mask, 2.0)
            out.append(((o[1].start, o[0].start, o[1].stop, o[0].stop), mask))
    out.sort(key=lambda s: (s[0][1] > H / 2, s[0][0]))
    assert len(out) == 4, f"found {len(out)} screens"
    return out


def atlas(cw, ch, levels):
    """Glyphs rendered into cw x ch cells, ordered by ink, thinned to `levels` evenly spaced steps."""
    font = ImageFont.truetype(FONT, int(ch * 0.95))
    cells = []
    for c in CHARS:
        im = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(im).text((cw / 2, ch / 2), c, fill=255, font=font, anchor="mm")
        cells.append(np.asarray(im).astype(float) / 255)
    ink = np.array([c.mean() for c in cells])
    order = np.argsort(ink)
    pick = [order[int(round(k))] for k in np.linspace(0, len(order) - 1, levels)]
    return np.stack([cells[i] for i in pick])  # (levels, ch, cw)


def frames(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = CLIP_W * CLIP_H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            return
        yield np.frombuffer(b, np.uint8).reshape(CLIP_H, CLIP_W, 3)


def cover(frame, w, h):
    """Scale to fill w x h, centred crop."""
    im = Image.fromarray(frame)
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return np.asarray(im.crop((x, y, x + w, y + h))).astype(float) / 255


def levels(img, lo, hi):
    """Lift the shadows so a hard-lit face (Astra) keeps its dark side in characters."""
    return np.clip((img - lo) / max(hi - lo, 1e-3), 0, 1)


def cells(rgb, cw, ch):
    rows, cols = rgb.shape[0] // ch, rgb.shape[1] // cw
    small = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).resize((cols, rows), Image.BOX)).astype(float) / 255
    return small, small @ np.array([0.299, 0.587, 0.114])


def as_ascii(rgb, glyphs, cw, ch, eq):
    """eq: the face's own luminance quantiles (from its first frame), so the glyph range follows the face, not 0-1:
    skin, eyes and mouth land on different characters instead of all on the densest ones."""
    small, lum = cells(rgb, cw, ch)
    rows, cols = lum.shape
    rank = np.interp(lum, eq, np.linspace(0, 1, len(eq)))
    idx = np.clip(rank * (len(glyphs) - 1), 0, len(glyphs) - 1).round().astype(int)
    ink = glyphs[idx].transpose(0, 2, 1, 3).reshape(rows * ch, cols * cw)
    col = np.repeat(np.repeat(small, ch, 0), cw, 1)
    col = col / np.maximum(col.max(2, keepdims=True), 0.25)  # full-strength hue per cell, the ink carries the light
    out = np.zeros_like(rgb)
    out[: rows * ch, : cols * cw] = ink[..., None] * col
    return out


def crt(layer, t, seed):
    """Scan lines, a glow, a little flicker."""
    h = layer.shape[0]
    scan = np.where(np.arange(h) % 3 == 2, 0.72, 1.0)[:, None, None]
    out = layer * scan
    glow = np.asarray(Image.fromarray((np.clip(layer, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(float) / 255
    flick = 1 + 0.025 * np.sin(t * 2 * np.pi * 9.7 + seed * 1.3)
    return np.clip((out + 0.55 * glow) * flick, 0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["ascii", "video", "dissolve"], default="ascii")
    ap.add_argument("--d0", type=float, default=1.84, help="dissolve: clip time it starts (\"Every part\" at 106.84)")
    ap.add_argument("--d1", type=float, default=2.88, help="dissolve: clip time it ends (\"word\" ends 107.88)")
    ap.add_argument("--band", type=float, default=0.15, help="dissolve: how soft each cell's switch is (0.04 = nearly hard)")
    ap.add_argument("--cell", type=int, default=5, help="character cell width in px at 1080p (height is twice)")
    ap.add_argument("--start", type=float, default=105.0, help="song time of the clips' first frame")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    plate = Image.open(PLATE).convert("RGB").resize((W, H), Image.LANCZOS)
    base = np.asarray(plate).astype(float) / 255
    scr = screens(plate)
    glyphs = atlas(a.cell, a.cell * 2, 24)
    # per-clip levels from its first frame, so each face fills its range
    gens = [frames(CLIPS / f) for f in FACES]

    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-ss", str(a.start), "-i", str(SONG), "-map", "0:v", "-map",
                            "1:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a",
                            "192k", "-shortest", str(out)], stdin=subprocess.PIPE)
    lv = [None] * 4
    eq = [None] * 4
    order = [None] * 4
    n = 0
    for fr in zip(*gens):
        t = n / FPS
        img = base.copy()
        glass = base.copy()
        for k, ((x0, y0, x1, y1), mask) in enumerate(scr):
            w, h = x1 - x0, y1 - y0
            face = cover(fr[k], w, h)
            if lv[k] is None:
                q = np.quantile(face.mean(2), [0.02, 0.995])
                lv[k] = (q[0], q[1])
            face = levels(face, *lv[k])
            if a.mode in ("ascii", "dissolve"):
                if eq[k] is None:
                    _, l0 = cells(face, a.cell, a.cell * 2)
                    eq[k] = np.quantile(l0, np.linspace(0, 1, 33))
                    eq[k] = np.maximum.accumulate(eq[k] + np.arange(33) * 1e-6)
                layer = as_ascii(face, glyphs, a.cell, a.cell * 2, eq[k])
                if a.mode == "dissolve":
                    vid = face.copy()
                    vid[..., 0] = np.roll(vid[..., 0], 1, 1)
                    vid[..., 2] = np.roll(vid[..., 2], -1, 1)
                    # cell by cell: each cell turns to its character at its own moment inside [d0, d1]
                    if order[k] is None:
                        rows, cols = h // (a.cell * 2), w // a.cell
                        order[k] = np.random.default_rng(67 + k).random((rows, cols))
                    prog = np.clip((t - a.d0) / (a.d1 - a.d0), 0, 1)
                    m_cell = np.clip((prog * (1 + a.band) - order[k]) / a.band, 0, 1)
                    mc = np.zeros((h, w))
                    rr, cc = order[k].shape
                    mc[: rr * a.cell * 2, : cc * a.cell] = np.repeat(np.repeat(m_cell, a.cell * 2, 0), a.cell, 1)
                    mc = mc[..., None]
                    layer = vid * (1 - mc) + layer * mc
            else:
                layer = face.copy()
                layer[..., 0] = np.roll(layer[..., 0], 1, 1)   # a hair of colour fringe
                layer[..., 2] = np.roll(layer[..., 2], -1, 1)
            layer = crt(layer, t, k)
            m = mask[y0:y1, x0:x1, None]
            g = glass[y0:y1, x0:x1]
            # the picture on the tube, the plate's glass reflections kept on top
            img[y0:y1, x0:x1] = g * (1 - m) + m * np.clip(layer + 0.18 * g, 0, 1)
        enc.stdin.write((img * 255).astype(np.uint8).tobytes())
        n += 1
    enc.stdin.close()
    enc.wait()
    print(f"{out.relative_to(ROOT)}: {n} frames, {n / FPS:.2f} s, mode {a.mode}, cell {a.cell}x{a.cell * 2}")


if __name__ == "__main__":
    main()
