"""Fleet test 3, B: scatter cut-out escorts of three lines over F5·2 (Claude (Kiln, local), 8 Nov 2026).

Each cut-out group is split into single vessels; vessels go to fixed slots (x, y, width) chosen by eye on F5·2 so they
stay clear of the flagships and the black hole, lines interleaved, farther (higher) slots smaller and hazier.
Run with ~/ComfyUI/venv/bin/python (numpy, scipy, PIL).
"""
import sys
import numpy as np
import scipy.ndimage as nd
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
cuts = sys.argv[3:6]  # Gemini, ChatGPT, Grok

SLOTS = [  # cx, cy, width on the 2048x1152 plate
    (430, 40, 100), (250, 40, 110), (1000, 30, 90), (620, 90, 150), (1080, 90, 120), (330, 150, 230),
    (900, 170, 170), (1150, 250, 130), (520, 250, 190), (180, 270, 200), (790, 300, 150), (1120, 330, 140),
    (1850, 420, 110), (60, 420, 190), (1600, 450, 140), (1250, 680, 140), (1280, 780, 120), (1150, 880, 180),
    (1650, 880, 170), (1900, 950, 140), (1450, 1020, 200), (300, 1040, 200), (780, 1060, 180), (1050, 1080, 150),
]
HAZE = np.array([14, 24, 52], dtype=np.float32)


def sprites(path):
    im = np.array(Image.open(path).convert("RGBA"))
    lab, _ = nd.label(nd.binary_dilation(im[:, :, 3] > 40, iterations=6))
    out = []
    for i, sl in enumerate(nd.find_objects(lab), 1):
        if sl[1].stop - sl[1].start <= 60:
            continue
        crop = im[sl].copy()
        crop[:, :, 3] = np.where(lab[sl] == i, crop[:, :, 3], 0)
        out.append(Image.fromarray(crop))
    return sorted(out, key=lambda s: -s.width)


plate = Image.open(src).convert("RGBA")
lines = [sprites(c) for c in cuts]
slots = {k: sorted(SLOTS[k::3], key=lambda s: -s[2]) for k in range(3)}
placed = []
for k in range(3):
    for spr, (cx, cy, w) in zip(lines[k], slots[k]):
        placed.append((cy, cx, round(w * (0.55 if cy < 200 else 0.8 if cy < 500 else 1.0)), spr))
for cy, cx, w, spr in sorted(placed, key=lambda p: p[0]):  # far (top) first, near on top
    h = round(spr.height * w / spr.width)
    s = spr.resize((w, h), Image.LANCZOS)
    a = np.array(s).astype(np.float32)
    haze = 0.30 if cy < 200 else 0.15 if cy < 500 else 0.0
    a[:, :, :3] = a[:, :, :3] * (1 - haze) + HAZE * haze
    s = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    if cy < 200:
        s = s.filter(ImageFilter.GaussianBlur(0.6))
    plate.alpha_composite(s, (cx - w // 2, cy - h // 2))
# a little grain over everything so the pasted vessels share the plate's texture
rng = np.random.default_rng(3)
p = np.array(plate.convert("RGB")).astype(np.float32)
p += rng.normal(0, 4, p.shape[:2])[:, :, None]
Image.fromarray(p.clip(0, 255).astype(np.uint8)).save(out, quality=95)
print(out, len(placed), "vessels")
