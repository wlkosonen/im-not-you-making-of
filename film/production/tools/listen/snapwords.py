#!/usr/bin/env python3
"""Each sung word moved onto its own onset in the vocal stem (the aligner's times run late: median 0.05 s, a quarter
0.17 s or more; Lati, 11 Nov: "when I time to sound waveform peaks, it alings better with words").

    media/cache/listen-venv/bin/python production/tools/listen/snapwords.py
    -> media/song/analysis/parempi/words-snapped.json   (words.json's shape, t0 snapped, "t0_aligner" kept)

Onsets: librosa's onset detector on the vocal stem, backtracked to the energy minimum before each attack. A word takes
the strongest onset within 0.25 s before to 0.10 s after its aligned start (the aligner runs late, so earlier is
likelier); with none there it keeps its time, flagged "unsnapped". Kiln, 12 Nov 2026.
"""
import json
from pathlib import Path

import librosa
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
A = ROOT / "media/song/analysis/parempi"
BEFORE, AFTER = 0.25, 0.10


def main():
    y, sr = librosa.load(A / "stems/vocals.wav", sr=22050, mono=True)
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
    idx = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=256, backtrack=True, units="frames")
    times = librosa.frames_to_time(idx, sr=sr, hop_length=256)
    peak_idx = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=256, backtrack=False, units="frames")
    strength = {round(float(t), 4): float(env[p]) for t, p in zip(times, peak_idx[:len(times)])}
    w = json.loads((A / "words.json").read_text())
    moved, kept = [], 0
    for x in w["words"]:
        if x.get("t0") is None:
            continue
        near = [t for t in times if x["t0"] - BEFORE <= t <= x["t0"] + AFTER]
        if not near:
            x["unsnapped"] = True
            kept += 1
            continue
        best = max(near, key=lambda t: strength.get(round(float(t), 4), 0))
        x["t0_aligner"] = x["t0"]
        x["t0"] = round(float(best), 3)
        moved.append(x["t0"] - x["t0_aligner"])
    # words the aligner never timed (12 Nov: line 17 lost "same thread, same line", Lati caught it): each run of untimed
    # words takes the strongest vocal onsets in the gap between its timed neighbours, in order; even spacing if too few
    MARKS = {"Me": 116.083}  # Lati's marker, 10 Nov (the aligner missed it)
    filled = 0
    by_line = {}
    for x in w["words"]:
        by_line.setdefault(x["line"], []).append(x)
    lines = {ln["line"]: ln for ln in w["lines"]}
    for li, ws in by_line.items():
        ln = lines.get(li, {})
        if ln.get("t0") is None and ln.get("text") in MARKS:
            ln["t0"] = MARKS[ln["text"]]
            ln["t1"] = ln["t0"] + 0.38
        nxt = min([l["t0"] for l in w["lines"] if l.get("t0") and ln.get("t0") and l["t0"] > ln["t0"] + 0.1], default=None)
        i = 0
        while i < len(ws):
            if ws[i].get("t0") is not None:
                i += 1
                continue
            j = i
            while j < len(ws) and ws[j].get("t0") is None:
                j += 1
            run = ws[i:j]
            prev = ws[i - 1] if i else None
            lo = (prev.get("t1") or prev["t0"] + 0.25) if prev else (ln.get("t0") or 0) - 0.3
            hi = ws[j]["t0"] if j < len(ws) else min(nxt - 0.15 if nxt else lo + 3, lo + 0.65 * len(run) + 0.6)
            if ln.get("text") in MARKS and len(ws) == 1:
                cand = [ln["t0"]]
            else:
                c = sorted((t for t in times if lo + 0.02 <= t < hi), key=lambda t: -strength.get(round(float(t), 4), 0))
                cand = sorted(c[:len(run)]) if len(c) >= len(run) else list(np.linspace(lo + 0.05, hi - 0.1, len(run)))
            for x, t in zip(run, cand):
                x["t0"] = round(float(t), 3)
                x["estimated"] = True
                filled += 1
            for k, x in enumerate(run):
                x["t1"] = round(run[k + 1]["t0"] if k + 1 < len(run) else min(hi, x["t0"] + 0.45), 3)
            i = j
        tt = [x["t1"] or x["t0"] for x in ws if x.get("t0") is not None]
        if tt and ln:
            ln["t1"] = round(max(tt + [ln.get("t1") or 0]), 3)
    w["snapped"] = {"filled": filled, "by": "snapwords.py", "onsets": len(times), "moved": len(moved), "kept": kept,
                    "median_shift": round(float(np.median(moved)), 3) if moved else 0}
    (A / "words-snapped.json").write_text(json.dumps(w, indent=1) + "\n")
    print(f"words-snapped.json: {len(moved)} words moved (median {w['snapped']['median_shift']:+.3f} s), "
          f"{kept} kept, {w['snapped']['filled']} untimed words placed on onsets, {len(times)} onsets in the vocal stem")


if __name__ == "__main__":
    main()
