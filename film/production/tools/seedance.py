#!/usr/bin/env python3
"""Seedance 2.5 through OpenRouter: submit clips from a clip book, poll, download, and log every paid call.

    python3 production/tools/seedance.py production/motion/pilot.json [--only C1B] [--dry-run]

The clip book is a JSON list of clips: {"id", "kind": "sung"|"motion"|"reference", "duration", "resolution", "prompt",
"image": local PNG, or "images": several (sung, reference), "last_image": an end frame (motion), "audio": local WAV (sung only)}. Per the gallery
(wiki/seedance, "Providers and filters"):
  - sung clips go in reference mode: the plate or sheets as image references, the vocal window as an audio reference
    (on OpenRouter a first frame silently drops the audio);
  - motion clips use the plate as the first frame and are silent;
  - reference clips are silent and take their images as references, with no first frame: a character sheet, a set;
  - audio must be a public HTTPS URL (no data: URIs), so references are uploaded to a public host first
    (production/motion/host.json says which; every upload is listed in the ledger and deleted after the batch).

Spending gate: production/motion/budget.json holds the approved dollars. A submission is refused if the money already
spent (ledger) plus this clip's estimate (seconds x price x 2, the CLAUDE.md rule) would go over it. Ledger:
production/motion/ledger.jsonl, one line per paid call, with OpenRouter's reported cost.
"""

import argparse
import subprocess
import json
import re
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "https://openrouter.ai/api/v1/videos"
MODEL = "bytedance/seedance-2.5"  # default; a clip may name its own "model"
# $/s, from OpenRouter's /api/v1/videos/models (Seedance 2.5 read 1 Nov, re-read 9 Nov as video tokens: 0.231 at 720p;
# Wan 3.0 read 9 Nov); the ledger keeps each job's real cost
PRICE = {"bytedance/seedance-2.5": {"720p": 0.231, "480p": 0.1028},
         "bytedance/seedance-2.0": {"720p": 0.1512, "480p": 0.0672},  # video tokens 0.000007 x 21,600/s at 720p, read 9 Nov
         "alibaba/wan-3.0": {"720p": 0.142, "480p": 0.071, "1080p": 0.284}}  # Wan charged 0.142 at 720p on 9 Nov (lists 0.10); 480p/1080p scaled, unverified
LEDGER = ROOT / "production/motion/ledger.jsonl"
BUDGET = ROOT / "production/motion/budget.json"
HOST = ROOT / "production/motion/host.json"
OUT = ROOT / "media/clips"


def env():
    for line in (ROOT / ".env").read_text().splitlines():
        k, _, v = line.partition("=")
        if k and v and k not in os.environ:
            os.environ[k.strip()] = v.strip()


def spent():
    if not LEDGER.exists():
        return 0.0
    # per job: the real cost once OpenRouter reports it, the estimate until then (the submitted line and the
    # completed line are the same job; 8 Nov the sum counted both, $5.54 for a $1.86 take)
    jobs = {}
    for line in LEDGER.read_text().splitlines():
        r = json.loads(line)
        key = r.get("job") or r.get("clip")
        if r.get("cost_usd") is not None:
            jobs[key] = r["cost_usd"]
        elif r.get("status") in ("failed", "cancelled", "expired"):
            jobs[key] = 0  # refused or failed jobs report no cost (9 Nov: two copyright refusals)
        elif key not in jobs:
            jobs[key] = r.get("estimate_usd", 0)
    return sum(jobs.values())


def log(rec):
    rec["at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def req(method, url, body=None, auth=True):
    h = {"Content-Type": "application/json"}
    if auth:
        h["Authorization"] = "Bearer " + os.environ["OPENROUTER_API_KEY"]
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} from {url}: {e.read().decode()[:1500]}")


def host_upload(path, batch):
    """Upload one reference file to the public host named in host.json; return its HTTPS URL."""
    cfg = json.loads(HOST.read_text())
    if cfg["kind"] == "hf-dataset":
        from huggingface_hub import HfApi
        api = HfApi(token=os.environ["HF_TOKEN"])
        dest = f"{batch}/{Path(path).name}"
        api.upload_file(path_or_fileobj=str(path), path_in_repo=dest, repo_id=cfg["repo"], repo_type="dataset")
        return f"https://huggingface.co/datasets/{cfg['repo']}/resolve/main/{dest}"
    raise SystemExit(f"unknown host kind {cfg['kind']}")


# Battle motion rules (production/motion/battle-prompt-rules.md, Lati 9 Nov: "so this wont go unnoticed after this
# batch"). A motion prompt with mechs, fighters, drones or fire in it must carry both sentences; any prompt is refused
# for negative words (they leak into the output) or the other word for space vessel. A clip may set "lint_skip": reason.
MOTION_RULES = ["is always in action", "Every hit does visible damage"]
BATTLE_WORDS = ("mech", "fighter", "drone", "missile", "tracer", "torpedo")
BANNED = (" no ", " not ", "n't ", " without ", " never ", " ship", "rainbow")


def lint(clip):
    # quoted text is the lyric being sung or spoken, not an instruction: it isn't checked
    p = " " + re.sub(r'"[^"]*"', " ", clip["prompt"]) + " "
    errs = [f"banned word {w.strip()!r}" for w in BANNED if w in p.lower()]
    if clip.get("kind") == "motion" and any(w in p.lower() for w in BATTLE_WORDS):
        errs += [f"missing battle rule {r!r}" for r in MOTION_RULES if r not in p]
    if errs and not clip.get("lint_skip"):
        raise SystemExit(f"REFUSED {clip['id']} by the prompt rules: {'; '.join(errs)}")


def submit(clip, batch, dry):
    lint(clip)
    res = clip.get("resolution", "720p")
    model = clip.get("model", MODEL)
    est = round(clip["duration"] * PRICE[model][res] * 2, 2)
    budget = json.loads(BUDGET.read_text())["approved_usd"]
    if round(spent() + est, 2) > budget + 1e-9:
        raise SystemExit(f"REFUSED {clip['id']}: spent {spent():.2f} + estimate {est:.2f} > approved {budget:.2f}")
    body = {"model": model, "prompt": clip["prompt"], "duration": clip["duration"], "resolution": res,
            "aspect_ratio": "16:9"}
    if dry:
        print(f"[dry] {clip['id']} {clip['kind']} {clip['duration']} s {res}, estimate ${est}")
        return None
    imgs = [host_upload(ROOT / p, batch) for p in clip.get("images") or [clip["image"]]]
    refs = [{"type": "image_url", "image_url": {"url": u}} for u in imgs]
    if clip["kind"] == "sung":
        aud = host_upload(ROOT / clip["audio"], batch)
        body["input_references"] = refs + [{"type": "audio_url", "audio_url": {"url": aud}}]
    elif clip["kind"] == "reference":
        body["generate_audio"] = False
        body["input_references"] = refs
    else:
        body["generate_audio"] = False
        body["frame_images"] = [{"type": "image_url", "image_url": {"url": imgs[0]}, "frame_type": "first_frame"}]
        if clip.get("last_image"):  # the shot ends on this plate (s068: the key, then the red button)
            body["frame_images"].append({"type": "image_url", "image_url": {"url": host_upload(ROOT / clip["last_image"], batch)},
                                         "frame_type": "last_frame"})
    job = req("POST", API, body)
    log({"clip": clip["id"], "job": job.get("id"), "model": model, "kind": clip["kind"], "duration": clip["duration"],
         "resolution": res, "estimate_usd": est, "cost_usd": None, "status": "submitted", "batch": batch})
    print(f"submitted {clip['id']} -> job {job.get('id')} (estimate ${est})")
    return job


def wait(job, clip, batch):
    cur = job
    for _ in range(120):
        st = cur.get("status")
        if st == "completed":
            break
        if st in ("failed", "cancelled", "expired"):
            log({"clip": clip["id"], "job": job["id"], "status": st, "error": cur.get("error"), "estimate_usd": 0,
                 "cost_usd": (cur.get("usage") or {}).get("cost"), "batch": batch})
            print(f"{clip['id']}: {st}: {cur.get('error')}")
            return None
        time.sleep(20)
        url = cur.get("polling_url") or f"{API}/{job['id']}"
        cur = req("GET", url if url.startswith("http") else "https://openrouter.ai" + url)
    else:
        print(f"{clip['id']}: still not done; poll later: {job['id']}")
        return None
    dest = OUT / batch / f"{clip['id']}-{job['id'][-8:]}.mp4"
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = (cur.get("unsigned_urls") or [None])[0] or f"{API}/{job['id']}/content?index=0"
    h = {"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]} if url.startswith(API) else {}
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300) as r:
        dest.write_bytes(r.read())
    cost = (cur.get("usage") or {}).get("cost")
    log({"clip": clip["id"], "job": job["id"], "status": "completed", "estimate_usd": 0, "cost_usd": cost,
         "file": str(dest.relative_to(ROOT)), "batch": batch, "usage": cur.get("usage")})
    print(f"{clip['id']}: saved {dest.relative_to(ROOT)}, cost {cost}")
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--collect", action="store_true",
                    help="poll and download this book's jobs that were submitted but never fetched; submit nothing")
    a = ap.parse_args()
    env()
    clips = json.loads(Path(a.book).read_text())
    only = set(filter(None, a.only.split(",")))
    batch = Path(a.book).stem
    if a.collect:
        recs = [json.loads(l) for l in LEDGER.read_text().splitlines()]
        done = {r["job"] for r in recs if r.get("status") != "submitted"}
        byid = {c["id"]: c for c in clips}
        for r in recs:
            if r.get("batch") == batch and r.get("status") == "submitted" and r["job"] not in done:
                wait({"id": r["job"], "status": "submitted"}, byid[r["clip"]], batch)
        print(f"spent so far (ledger): ${spent():.2f}")
        reindex()
        return
    jobs = []
    for c in clips:
        if only and c["id"] not in only:
            continue
        try:
            jobs.append((c, submit(c, batch, a.dry_run)))
        except SystemExit as e:  # a refusal or an HTTP error stops submitting; jobs already out still get fetched
            print(f"stopped submitting at {c['id']}: {e}")
            break
    for c, j in jobs:
        if j:
            wait(j, c, batch)
    print(f"spent so far (ledger): ${spent():.2f}")
    if any(j for _, j in jobs):
        reindex()


def reindex():
    """New takes go straight into the library /edit's drawer reads (Lati, 11 Nov: "edit tool does not parse fresh takes")"""
    py = ROOT / "media/cache/listen-venv/bin/python"
    r = subprocess.run([str(py if py.exists() else sys.executable), str(ROOT / "production/tools/library.py")],
                       capture_output=True, text=True, cwd=ROOT)
    print("library:", (r.stdout.strip().splitlines() or [r.stderr.strip()[-200:]])[-1])


if __name__ == "__main__":
    main()
