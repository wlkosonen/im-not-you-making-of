#!/usr/bin/env python3
"""Every committed version of Lati's cut (film 3's production/edit/timeline.json) as one privacy-filtered JSON, so the
making-of can draw the cut as it grew without reading film 3's git at render time.

Usage:  python3 tools/data/timeline_history.py [--out data/timeline-history.json]
Stdlib only; read-only on film 3's repo (git log / git show). Written 12 Nov 2026 by section agent C (bridge) for
Claude (Kiln, local). Not wired into base.py or extract.py: sec_c_bridge.versions() still reads git; switching it to
this file is a few lines (rows -> the same fields).

Output: {"about", "source", "rows": [...]} oldest first, one row per commit that touched the file:
  hash (8), commit_ts (author time, UTC Z), saved (the editor's own "saved" field, local EET, as written),
  saved_ts (that field as UTC Z, or the commit time when the field is missing), made (the file's "made" note),
  clips: [[track, start, in, dur, speed, kind, file, shot], ...]  (track 0 = V1; speed null = 1; kind as written,
  "video" or "image"; shot as written, may be null).
"""
import argparse
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as X  # noqa: E402  (git, time helpers, the privacy filter)

PATH = "production/edit/timeline.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(X.OUT, "timeline-history.json"))
    a = ap.parse_args()
    rows = []
    for line in X.git(X.FILM, "log", "--reverse", "--format=%H %aI", "--", PATH).splitlines():
        if not line.strip():
            continue
        h, when = line.split()
        d = json.loads(X.git(X.FILM, "show", f"{h}:{PATH}"))
        saved = d.get("saved")
        saved_ts = X.iso(X.parse_local(saved)) if saved else X.iso(X.parse_iso(when))
        clips = []
        for ti, tr in enumerate(d.get("tracks", [])):
            for c in tr.get("clips", []):
                clips.append([ti, c.get("start"), c.get("in"), c.get("dur"), c.get("speed"), c.get("kind"),
                              c.get("file"), c.get("shot")])
        clips.sort(key=lambda c: (c[1] or 0, c[0]))
        rows.append({"hash": h[:8], "commit_ts": X.iso(X.parse_iso(when)), "saved": saved, "saved_ts": saved_ts,
                     "made": d.get("made"), "tracks": [t.get("name") for t in d.get("tracks", [])], "clips": clips})
    obj = X.scrub({"about": "Every committed version of film 3's production/edit/timeline.json (Lati's cut), oldest "
                            "first. saved = the editor's own save time, local EET as written; saved_ts its UTC. "
                            "clips: [track, start, in, dur, speed, kind, file, shot], track 0 = V1.",
                   "source": f"{X.FILM} git, {PATH}", "rows": rows}, "timeline-history")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print(f"{a.out}: {len(rows)} versions, {sum(len(r['clips']) for r in rows)} clip rows; "
          f"privacy hits: {len(X.SCRUB_LOG)}")


if __name__ == "__main__":
    main()
