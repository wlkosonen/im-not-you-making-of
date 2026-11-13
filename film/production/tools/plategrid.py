#!/usr/bin/env python3
"""Plate choices as 2x2 grids for Lati's phone (Lati, 11 Nov 2026: "2x2 grid per plate selection").

    ~/ComfyUI/venv/bin/python production/tools/plategrid.py s077 s083 s084 ... [--out media/review/plates-next]

One image per shot: its v2 plates (media/plates/v2/<shot>-N-*.jpg), else the design plates its board refs name
(media/images/designs-*/, by design-ids.json, with that design's siblings), labelled A-D in order; ★ marks the 9 Nov picks (board/picks.json). Header: shot,
song time, length, the board's action. Shots with two or fewer candidates are paired two to a grid, one row each.
"""
import argparse
import glob
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
W, H, HD = 640, 360, 56
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = lambda n: ImageFont.truetype(FONT, n)


IDS = json.loads((ROOT / "production/images/design-ids.json").read_text())
PICKS = json.loads((ROOT / "production/board/picks.json").read_text())


def candidates(sid, shot):
    """v2 plates; else the design its first board ref names (by id) and that design's siblings (p2i-a-1 → p2i-*)"""
    files = sorted(glob.glob(str(ROOT / f"media/plates/v2/{sid}-*.jpg")))
    p = PICKS.get("p-" + sid) or {}
    first = [str(ROOT / f) for f in [p.get("file"), *p.get("also", [])] if f and (ROOT / f).exists()]
    files = first + [f for f in files if f not in first]  # the 9 Nov picks always among the four shown
    if not files:
        for r in shot.get("refs") or []:
            hit = glob.glob(str(ROOT / f"media/images/designs-*/*-{IDS.get(r, 'none')}.jpg"))
            if hit:
                fam = Path(hit[0]).name.split("-")[0]
                sib = sorted(glob.glob(str(ROOT / f"media/images/designs-*/{fam}-*.jpg")))
                files = hit + [f for f in sib if f != hit[0]]
                break
    return files[:4]


def tile(f):
    im = Image.open(f).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def star(picks, sid, f):
    p = picks.get("p-" + sid) or {}
    rel = str(Path(f).relative_to(ROOT))
    if rel == p.get("file"):
        return "★ picked"
    if rel in p.get("also", []):
        return "★ also picked"
    return ""


def mark(picks, sid, f, i):
    return star(picks, sid, f) or ("★ the board's design" if i == 0 and "/designs-" in f else "")


def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def draw(out, title, cells):
    """cells: [(label, file, star, col, row)]"""
    rows = max(c[4] for c in cells) + 1
    img = Image.new("RGB", (2 * W, HD + rows * H), (12, 12, 14))
    d = ImageDraw.Draw(img)
    d.text((10, 14), title[:110], fill=(255, 210, 120), font=F(20))
    for lab, f, st, cx, cy in cells:
        img.paste(tile(f), (cx * W, HD + cy * H))
        d.text((cx * W + 10, HD + cy * H + 8), lab, fill="yellow", font=F(30), stroke_width=3, stroke_fill="black")
        if st:
            d.text((cx * W + 10, HD + cy * H + H - 40), st, fill=(120, 255, 140), font=F(24), stroke_width=3,
                   stroke_fill="black")
    img.save(out, quality=82)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots", nargs="+")
    ap.add_argument("--out", default="media/review/plates-next")
    a = ap.parse_args()
    board = {s["id"]: s for s in json.loads((ROOT / "production/board/board.json").read_text())["shots"]}
    picks = json.loads((ROOT / "production/board/picks.json").read_text())
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    pending = []  # shots with 1-2 candidates, paired two to a grid

    def head(sid):
        s = board[sid]
        return f"{sid} · {fmt(s['t0'])} · {s['t1'] - s['t0']:.1f} s · {s['action']}"

    def flush():
        if not pending:
            return
        cells = [(f"{sid} {'AB'[i]}", f, mark(picks, sid, f, i), i, r) for r, (sid, fs) in enumerate(pending)
                 for i, f in enumerate(fs)]
        name = "-".join(sid for sid, _ in pending)
        title = "  |  ".join(f"{'Top' if r == 0 else 'Bottom'}: {head(sid)[:52]}" for r, (sid, _) in enumerate(pending))
        draw(out / f"{name}.jpg", title, cells)
        print(out / f"{name}.jpg")
        pending.clear()

    for sid in a.shots:
        fs = candidates(sid, board[sid])
        if not fs:
            print(f"{sid}: no plates")
            continue
        if len(fs) <= 2:
            pending.append((sid, fs))
            if len(pending) == 2:
                flush()
            continue
        cells = [(f"{sid} {'ABCD'[i]}", f, mark(picks, sid, f, i), i % 2, i // 2) for i, f in enumerate(fs)]
        draw(out / f"{sid}.jpg", head(sid), cells)
        print(out / f"{sid}.jpg")
    flush()


if __name__ == "__main__":
    main()
