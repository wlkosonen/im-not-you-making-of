#!/usr/bin/env python3
"""The clip library: one index of every clip, for finding and swapping takes (Lati, 26 Oct: "If I wanted to change one
dance clip to another, I'd have to go through folders by hand … We need a system.").

    media/cache/listen-venv/bin/python production/tools/library.py        # (CPU; cached, so re-runs are quick)

Film 3: copied from ~/checked-me by Kiln's helper, 8 Nov 2026. Scans every take under media/motion/ and media/clips/
(a "superseded" folder anywhere marks old takes). Per clip: source (grok, from its folder or name; else the model token
in names like "B-seedance20-isko-<job>.mp4"; "rough cut" for rough-N), kind (sung / motion / rough cut), the batch (its
folder, e.g. test-1), the shot it was made for (an sNNN in its name that the board has) and that shot's framing and
place, length, Grok's own tempo, how much it moves (mean frame difference), the words Whisper hears in sung takes,
Lati's verdict and its status (production/library/notes.json), and which shots use it now (Lati's picks, the clip
book). The board, the picks and the clip book are optional. Writes production/library/clips.json and an
8-frame filmstrip per clip to media/library/strips/. The review player's library page reads both.
"""
import json
import re
import subprocess
from pathlib import Path

import av
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "production/library/clips.json"
STRIPS = ROOT / "media/library/strips"
CACHE = ROOT / "media/library/cache.json"
# Film 3's places, from board/draft-1.md's scenes (keep in step with PLACES in review/library.html); first match wins
PLACES = [("warp", ("hyperspace", "warp")), ("lair", ("lair", "bunker", "bot swarm", "swarm of bots")),
          ("hangar", ("hangar", "docking")), ("break", ("red lens", "voice-interface", "oscillator")),
          ("avatars", ("avatar",)), ("city", ("utopia", "spires", "flying cars")),
          ("battle", ("battlefield", "battle", "dogfight", "cockpit", "mech")), ("earth", ("sakura", "on earth")),
          ("bridge", ("bridge", "viewport", "terminal", "flagship"))]


def place(shot):
    st = shot["set"].lower()
    return next((p for p, keys in PLACES if any(k in st for k in keys)), st)


def probe(path):
    c = av.open(str(path))
    s = c.streams.video[0]
    fps = float(s.average_rate)
    frames = [f.to_ndarray(format="rgb24") for f in c.decode(video=0)]
    return fps, frames


def strip(frames, out):
    idx = np.linspace(0, len(frames) - 1, 8).round().astype(int)
    tiles = []
    for i in idx:
        f = frames[i]
        h, w = f.shape[:2]
        s = 108 / h
        t = cv2.resize(f, (round(w * s), 108), interpolation=cv2.INTER_AREA)
        if t.shape[1] > 192:  # centre-crop to 16:9 tiles
            x = (t.shape[1] - 192) // 2
            t = t[:, x:x + 192]
        else:
            t = cv2.copyMakeBorder(t, 0, 0, 0, 192 - t.shape[1], cv2.BORDER_CONSTANT)
        tiles.append(t)
    cv2.imwrite(str(out), cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])


def energy(frames):
    g = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), (64, 36)).astype(np.float32) for f in frames]
    d = [float(np.mean(np.abs(g[i] - g[i - 1]))) for i in range(1, len(g))]
    return round(float(np.median(d)) if d else 0.0, 2)


def bpm(path):
    import librosa
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "22050", "-f", "f32le",
                          "-"], capture_output=True).stdout
    if len(raw) < 22050 * 4:
        return None
    y = np.frombuffer(raw, dtype=np.float32)
    if float(np.abs(y).max()) < 1e-3:
        return None
    t, _ = librosa.beat.beat_track(y=y, sr=22050)
    return round(float(np.atleast_1d(t)[0]), 1)


_whisper = None


def heard(path):
    global _whisper
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = os.environ["HIP_VISIBLE_DEVICES"] = ""
    import whisper
    if _whisper is None:
        _whisper = whisper.load_model("turbo", device="cpu", download_root=str(ROOT / "media/cache/listen-models/whisper"))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le",
                          "-"], capture_output=True).stdout
    if not raw:
        return ""
    r = _whisper.transcribe(np.frombuffer(raw, np.float32).copy(), language="en", fp16=False)
    return r["text"].strip()


def main():
    bp, np_ = ROOT / "production/board/board.json", ROOT / "production/library/notes.json"
    board = json.loads(bp.read_text()) if bp.exists() else {"shots": [], "clips": []}
    shots = {s["id"]: s for s in board["shots"]}
    notes = {k: v for k, v in (json.loads(np_.read_text()) if np_.exists() else {}).items() if k[0] != "_"}
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    STRIPS.mkdir(parents=True, exist_ok=True)

    used = {}  # clip id -> shots

    def use(cid, sid):
        used.setdefault(cid, set()).add(sid)
    picks = ROOT / "production/edit/picks-lati.json"
    for p in json.loads(picks.read_text()) if picks.exists() else []:
        name = re.sub(r"-(beat|lips)$", "", Path(p.get("clip") or "").stem)
        if name:
            use(name, p["shot"])
    bk = ROOT / "production/motion/clipbook.json"
    for e in json.loads(bk.read_text()) if bk.exists() else []:
        for sid in e.get("shots", []):
            use(e["id"], sid)

    # the default takes the cut plays (production/edit/takes.json, Kiln from Lati's verdicts)
    tk = ROOT / "production/edit/takes.json"
    import glob as _glob
    for sid, pat in (json.loads(tk.read_text())["takes"] if tk.exists() else {}).items():
        for hit in _glob.glob(str(ROOT / "media/clips" / pat) + ".mp4")[:1]:
            use(Path(hit).stem, sid)

    files = []
    for d in ("media/motion", "media/clips"):
        for f in sorted((ROOT / d).rglob("*.mp4")):
            if ".video." in f.name:
                continue
            # the cut's own links and our review reels aren't takes (Kiln, 10 Nov)
            if "shot" in f.relative_to(ROOT / d).parts[:-1] or any(
                    k in f.stem for k in ("reel", "with-song", "-vs-", "four-faces", "-A-B", "retimed")):
                continue
            parts = [x.lower() for x in f.relative_to(ROOT / d).parts[:-1]]
            n = f.stem.lower()
            if re.match(r"(\d\d-)?rough-?(cut|\d)", n):
                source = "rough cut"
            elif "grok" in parts or n.startswith("grok"):
                source = "grok"
            else:
                m = re.match(r"(?:[a-z]\d?-)?([a-z]+\d*)", n)
                source = m.group(1) if m else "other"
            batch = next((x for x in parts if x not in ("grok", "superseded")), None)
            files.append((f, source, "superseded" in parts, batch))

    out = []
    for f, source, superseded, batch in files:
        rel = str(f.relative_to(ROOT))
        stem = f.stem
        key = f"{rel}:{f.stat().st_mtime:.0f}"
        c = cache.get(key, {})
        m = re.search(r"(?:^|[-_ ])(s\d{3})(?=[-_. ]|$)", stem.lower())
        made_for = m.group(1) if m and m.group(1) in shots else None
        sh = shots.get(made_for) if made_for else None
        if source == "rough cut":
            kind = "rough cut"
        elif re.search(r"(^|[-_])sung([-_]|$)", stem.lower()) or sh and sh.get("motion_tier") == "sung":
            kind = "sung"
        else:
            kind = "motion"
        if "frames" not in c or not (STRIPS / f"{stem}.jpg").exists():
            fps, frames = probe(f)
            strip(frames, STRIPS / f"{stem}.jpg")
            h, w = frames[0].shape[:2]
            c.update(frames=len(frames), fps=fps, w=w, h=h, energy=energy(frames))
        if source.startswith("grok") and "bpm" not in c:
            c["bpm"] = bpm(f)
        if kind == "sung" and "heard" not in c:
            c["heard"] = heard(f)
        cache[key] = c
        nk = max((k for k in notes if stem.startswith(k)), key=len, default=None)
        note = notes.get(nk, {})
        status = note.get("status") or ("reject" if superseded else "spare")  # nothing is kept until Lati says so
        if superseded:  # an old take of a clip that has a newer one; its verdict belongs to the new one
            status, note = "reject", {"note": "superseded by a newer take"}
        cid = re.sub(r"-(fast|hq).*", "", stem)
        users = [] if superseded else sorted(used.get(stem, set()) | used.get(cid, set()))
        out.append({"id": stem, "path": rel, "source": source, "kind": kind, "batch": batch, "made_for": made_for,
                    "framing": sh["framing"] if sh else None, "place": place(sh) if sh else None,
                    "seconds": round(c["frames"] / c["fps"], 2), "fps": round(c["fps"], 2), "size": f"{c['w']}x{c['h']}",
                    "energy": c["energy"], "bpm": c.get("bpm"), "heard": c.get("heard"),
                    "status": status if not users or status == "reject" else "in cut", "verdict": note.get("note"),
                    "reviewed": bool(nk) or superseded,  # Lati has a verdict, a note or a "seen" on it (notes.json)
                    "used_by": users, "strip": f"media/library/strips/{stem}.jpg"})
        print(f"{stem:42} {source:12} {kind:7} {out[-1]['status']:7} {','.join(users)}", flush=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"clips": out}, indent=1) + "\n")
    print(len(out), "clips ->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
