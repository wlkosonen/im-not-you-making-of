#!/usr/bin/env python3
"""Is this stem really the locked take? Cross-correlate it with the master before any lip sync is built on it.

    ~/checked-me/media/cache/listen-venv/bin/python production/tools/stemcheck.py media/song/take.wav media/song/stems/lead.wav

Prints the lag and the correlation peak. The gallery's first stems came from the wrong takes, one of them matched by its
length (wiki/song, "Take a singing shot's vocal from Suno's own stem split"): check by the sound, not by title or length.
"""

import argparse

import numpy as np
import soundfile as sf

RATE = 4000  # lag resolution 0.25 ms, and a whole song stays cheap
MIN_PEAK = 0.2  # measured 1 Nov on both films' demucs vocals: right song 0.44 and 0.47, wrong songs 0.007 and under
MAX_LAG_MS = 5


def load(path):
    x, sr = sf.read(path, always_2d=True)
    x = x.mean(axis=1)
    n = max(1, int(sr // RATE))
    x = x[:len(x) // n * n].reshape(-1, n).mean(axis=1)
    x = np.interp(np.arange(0, len(x) * RATE * n / sr) * sr / n / RATE, np.arange(len(x)), x)  # masters and stems differ: 44.1 and 48 kHz
    return x - x.mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master")
    ap.add_argument("stem")
    a = ap.parse_args()
    m, s = load(a.master), load(a.stem)
    n = len(m) + len(s)
    c = np.fft.irfft(np.fft.rfft(m, n) * np.conj(np.fft.rfft(s, n)), n)
    i = int(np.argmax(np.abs(c)))
    lag = (i if i < n / 2 else i - n) / RATE
    peak = abs(c[i]) / (np.linalg.norm(m) * np.linalg.norm(s))
    print(f"length: master {len(m) / RATE:.3f} s, stem {len(s) / RATE:.3f} s")
    print(f"lag: {lag * 1000:+.2f} ms (positive: the stem runs early), peak: {peak:.3f}")
    ok = peak >= MIN_PEAK and abs(lag) * 1000 <= MAX_LAG_MS
    print("OK: this stem is this take" if ok else "CHECK: this is not this take, or it isn't aligned")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
