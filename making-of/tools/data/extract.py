#!/usr/bin/env python3
"""Extract film 3's record (*I'm Not You*) into privacy-filtered JSON for the making-of.

Rebuilds everything in data/ from the read-only sources:
  - film 3's repo ("/home/shegs/Im not you"): git log, decisions.md, the ledger, takes.json, timeline.json,
    the run files, the graphics agents' logs
  - Kiln's session transcript and its subagent transcripts (~/.claude/projects/-home-shegs-Claudia/)

Usage:  python3 tools/data/extract.py [--end ISO|now]
Default window: film 3's first commit to the making-of's first commit (see data/README.md).
Stdlib only. Never writes outside this repo's data/.
"""
import argparse
import bisect
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))           # the making-of repo
OUT = os.path.join(REPO, "data")
FILM = "/home/shegs/Im not you"
PROJ = "/home/shegs/.claude/projects/-home-shegs-Claudia"
KILN_ID = "85bff6f8-ec89-4d67-bd26-a10e71acc6c2"
KILN = os.path.join(PROJ, KILN_ID + ".jsonl")
SUBS = os.path.join(PROJ, KILN_ID, "subagents")
LOCAL_TZ = dt.timezone(dt.timedelta(hours=2))  # Europe/Helsinki, EET (+02:00) for the whole window (DST ended 25 Oct)
ENV_FILES = ["/home/shegs/Im not you/.env", "/home/shegs/Claudia/.env", "/home/shegs/checked-me/.env"]

UTC = dt.timezone.utc


# ---------------------------------------------------------------- time helpers

def parse_iso(s):
    """ISO string (Z, offset, or naive) -> aware UTC datetime. Naive strings are taken as UTC."""
    s = s.strip().replace("Z", "+00:00")
    d = dt.datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=UTC)
    return d.astimezone(UTC)


def parse_local(s):
    """Naive local (Helsinki) time string -> aware UTC datetime."""
    d = dt.datetime.fromisoformat(s.strip().replace(" ", "T"))
    return d.replace(tzinfo=LOCAL_TZ).astimezone(UTC)


def iso(d):
    return d.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


# ---------------------------------------------------------------- privacy

# Every e-mail address is removed (the 'email' pattern), Lati's included; his address is not written here.
SECRET_PATTERNS = [
    ("share-tracking", re.compile(r"[?&]si=[A-Za-z0-9_-]+")),  # YouTube share ids identify the sharer (Kiln, 12 Nov)
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")),
    ("sk-key", re.compile(r"\bsk-[A-Za-z0-9_-]{10,}")),
    ("or-key", re.compile(r"(?<![\w-])or-[A-Za-z0-9_-]{20,}")),
    ("bearer", re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{12,}", re.I)),
    ("long-hex", re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{32,}(?![0-9a-fA-F])")),
    ("long-token", re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9]*[0-9])(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])"
                               r"[A-Za-z0-9]{32,}(?![A-Za-z0-9])")),
    ("base64-padded", re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{30,}={1,2}")),
]
# Lati's health stays out (decisions.md of the making-of, 12 Nov). Words that would flag a note for a manual look.
HEALTH_WORDS = re.compile(
    r"\b(health|healthy|sick|illness|doctor|hospital|clinic|medic(?:al|ine|ation)?|pills?|blood|"
    r"pain|ache|injur(?:y|ed)|surgery|fever|flu|covid|migraine|diagnos\w*|symptom\w*|therapy|anxiety|"
    r"depress\w*|burn(?:ed|t)? ?out|exhausted|exhaustion|insomnia|tired|fatigue\w*|sleep\w*|asleep)\b", re.I)


def env_values():
    vals = []
    for p in ENV_FILES:
        try:
            for line in open(p, encoding="utf-8", errors="replace"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                v = line.split("=", 1)[1].strip().strip("'\"")
                if len(v) >= 8:
                    vals.append(v)
        except OSError:
            pass
    return vals


ENV_VALUES = env_values()
SCRUB_LOG = []   # (file, path, pattern, count)


def scrub_str(s, where):
    out = s
    for v in ENV_VALUES:
        if v in out:
            SCRUB_LOG.append((where, "env-value", out.count(v)))
            out = out.replace(v, "[removed: key]")
    for name, rx in SECRET_PATTERNS:
        hits = rx.findall(out)
        if hits:
            SCRUB_LOG.append((where, name, len(hits)))
            out = rx.sub("[removed: %s]" % name, out)
    return out


def scrub(obj, where):
    if isinstance(obj, str):
        return scrub_str(obj, where)
    if isinstance(obj, list):
        return [scrub(x, where) for x in obj]
    if isinstance(obj, dict):
        return {k: scrub(v, where + "." + k) for k, v in obj.items()}
    return obj


def write(name, obj):
    obj = scrub(obj, name)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    return path


# ---------------------------------------------------------------- window

def window(end_arg):
    first = git(FILM, "log", "--reverse", "--format=%aI").splitlines()[0]
    w0 = parse_iso(first)
    if end_arg == "now":
        w1 = dt.datetime.now(UTC)
        end_src = "the time extract.py ran"
    elif end_arg:
        w1 = parse_iso(end_arg)
        end_src = "--end " + end_arg
    else:
        w1 = parse_iso(git(REPO, "log", "--reverse", "--format=%aI").splitlines()[0])
        end_src = "the making-of's first commit (b667f51 'start (Kiln): the making-of')"
    return w0, w1, end_src


# ---------------------------------------------------------------- transcripts

def usage_ctx(u):
    return (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)


def read_transcript(path, w0, w1, want_users=False, want_compactions=False):
    """Stream a transcript. Dedupe records by uuid and calls by message.id (one API call is written as one record
    per content block, each with the same usage; a stretch of the Kiln file is also written twice, see README)."""
    seen_uuid = set()
    calls = {}           # message id -> call
    users = []
    compactions = []
    first_any = last_any = None
    with open(path, "rb") as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            u = r.get("uuid")
            if u:
                if u in seen_uuid:
                    continue
                seen_uuid.add(u)
            ts = r.get("timestamp")
            if not ts:
                continue
            d = parse_iso(ts)
            first_any = d if first_any is None or d < first_any else first_any
            last_any = d if last_any is None or d > last_any else last_any
            typ = r.get("type")
            if want_compactions and typ == "system" and r.get("subtype") == "compact_boundary":
                compactions.append((d, r.get("compactMetadata") or {}, u))
                continue
            if want_users and typ == "user":
                users.append((d, r))
                continue
            if want_users and typ == "attachment" and (r.get("attachment") or {}).get("type") == "queued_command":
                users.append((d, r))
                continue
            if not (w0 <= d <= w1):
                continue
            if typ == "assistant":
                m = r.get("message") or {}
                mid = m.get("id") or r.get("requestId") or u
                model = m.get("model")
                if model == "<synthetic>" or not m.get("usage"):
                    continue
                if mid in calls:
                    continue
                us = m["usage"]
                calls[mid] = {
                    "d": d, "model": model,
                    "in": us.get("input_tokens") or 0,
                    "cr": us.get("cache_read_input_tokens") or 0,
                    "cc": us.get("cache_creation_input_tokens") or 0,
                    "out": us.get("output_tokens") or 0,
                }
    cl = sorted(calls.values(), key=lambda c: c["d"])
    for c in cl:
        c["ctx"] = c["in"] + c["cr"] + c["cc"]
    return cl, users, compactions, first_any, last_any


def user_text(r):
    c = (r.get("message") or {}).get("content")
    if isinstance(c, str):
        return c, 0
    if isinstance(c, list):
        txt = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        imgs = sum(1 for b in c if isinstance(b, dict) and b.get("type") == "image")
        return txt, imgs
    return "", 0


def lati_turns(users):
    """Lati's own messages: user records with origin.kind == 'human', and messages he sent while Kiln was working
    (attachment records of type queued_command, humanTurn true); plus his /compact commands and interrupts."""
    turns = []
    normal = defaultdict(list)
    for d, r in users:
        if r.get("type") == "user" and (r.get("origin") or {}).get("kind") == "human":
            normal[user_text(r)[0].strip()].append(d)
    for d, r in users:
        if r.get("type") == "attachment":
            a = r["attachment"]
            if not (a.get("humanTurn") or (a.get("origin") or {}).get("kind") == "human"):
                continue
            p = a.get("prompt")
            txt = p if isinstance(p, str) else " ".join(b.get("text", "") for b in (p or []) if isinstance(b, dict))
            imgs = sum(1 for b in (p or []) if isinstance(b, dict) and b.get("type") == "image") if isinstance(p, list) else 0
            if any(abs((d - x).total_seconds()) < 1800 for x in normal.get(txt.strip(), [])):
                continue   # the same message also arrived as an ordinary turn
            turns.append({"d": d, "kind": "message", "mid_turn": True, "chars": len(txt), "images": imgs, "text": txt})
            continue
        o = r.get("origin") or {}
        txt, imgs = user_text(r)
        c = (r.get("message") or {}).get("content")
        if isinstance(c, list) and c and all(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            continue
        if o.get("kind") == "human":
            turns.append({"d": d, "kind": "message", "mid_turn": False, "chars": len(txt), "images": imgs, "text": txt})
        elif not o and not r.get("isMeta") and not r.get("isCompactSummary"):
            if txt.lstrip().startswith("<command-name>/compact"):
                turns.append({"d": d, "kind": "compact-command", "mid_turn": False, "chars": len(txt), "images": 0, "text": None})
            elif txt.startswith("[Request interrupted by user"):
                turns.append({"d": d, "kind": "interrupt", "mid_turn": False, "chars": 0, "images": 0, "text": None})
    turns.sort(key=lambda t: t["d"])
    return turns


# ---------------------------------------------------------------- decisions.md

DEC = "production/decisions.md"
H2 = re.compile(r"^## (\d{4}-\d{2}-\d{2}) · (.+?)\s*$")
BOLD = re.compile(r"^\*\*(\d{4}-\d{2}-\d{2}) · (.+?)\*\*\s*(\(.*\))?\s*$")
MONTHS = {"Oct": 10, "Nov": 11}


def first_seen_times(keys_of):
    """For each key (a string found in decisions.md), the author time of the first commit whose decisions.md
    contains it. keys_of(text) -> iterable of keys."""
    commits = [l.split(" ", 1) for l in git(FILM, "log", "--reverse", "--format=%H %aI", "--", DEC).splitlines()]
    seen = {}
    for h, t in commits:
        try:
            text = git(FILM, "show", "%s:%s" % (h, DEC))
        except subprocess.CalledProcessError:
            continue
        for k in keys_of(text):
            if k not in seen:
                seen[k] = parse_iso(t)
    return seen


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def match_paren(s, i):
    """s[i] == '(' -> index of its matching ')' (or len(s)-1)."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "(":
            depth += 1
        elif s[j] == ")":
            depth -= 1
            if depth == 0:
                return j
    return len(s) - 1


def first_sentence(s):
    s = re.sub(r"\s+", " ", s).strip()
    m = re.search(r"(?<!\d)(?<!\be\.g)(?<!\bi\.e)[.!?](?=\s+[A-Z(\"`'*]|\s*$)", s)
    return s[: m.end()] if m else s


def parse_decisions():
    lines = open(os.path.join(FILM, DEC), encoding="utf-8").read().split("\n")
    entries = []
    cur = None
    for i, line in enumerate(lines):
        m = H2.match(line)
        b = BOLD.match(line)
        if m or b:
            mm = m or b
            cur = {"date": mm.group(1), "title": mm.group(2), "line": i + 1,
                   "heading": line.strip(), "kind": "h2" if m else "bold",
                   "by": (b.group(3) or "") if b else "", "body": []}
            entries.append(cur)
        elif cur is not None:
            cur["body"].append((i + 1, line))
    return entries


def split_blocks(body):
    """Paragraph blocks: ('quote', firstline, text) for runs of '>' lines, ('para', firstline, text) otherwise."""
    blocks = []
    kind = None
    buf = []
    start = None

    def flush():
        if buf:
            if kind == "quote":
                # join wrapped lines with a space; an empty '>' line is a paragraph break
                paras, p = [], []
                for x in buf:
                    x = x[1:].lstrip() if x.startswith(">") else x
                    x = x[1:] if x.startswith(" ") else x
                    if x.strip() == "":
                        if p:
                            paras.append(" ".join(p))
                            p = []
                    else:
                        p.append(x.rstrip())
                if p:
                    paras.append(" ".join(p))
                blocks.append(("quote", start, "\n\n".join(paras)))
            else:
                blocks.append(("para", start, " ".join(x.strip() for x in buf)))

    for ln, line in body:
        k = "quote" if line.startswith(">") else ("blank" if not line.strip() else "para")
        if k == "blank":
            flush()
            buf, kind, start = [], None, None
            continue
        if k != kind:
            flush()
            buf, kind, start = [], k, ln
        buf.append(line)
    flush()
    return blocks


RESP = re.compile(r"^Claude \(([A-Za-z]+), (local|cloud)\)[^:]*:\s*(.*)$", re.S)


def parse_quote_block(text):
    """A '>' block -> (quote text, attribution inner text, remainder after the attribution) or None if it has no
    '(Lati' attribution after a closing quote."""
    idx = text.rfind('" (Lati')
    if idx < 0:
        return None
    a0 = idx + 2
    a1 = match_paren(text, a0)
    attrib = text[a0 + 1:a1]
    rest = text[a1 + 1:]
    q = text[:idx + 1].strip()
    return q, attrib, rest


def strip_outer(q):
    q = q.strip()
    if q.startswith('"') and q.endswith('"'):
        return q[1:-1]
    return q


def candidate_splits(q):
    """Kiln sometimes records two of Lati's messages in one line: "a" and "b", or "a" (on X) and "b"."""
    rx = re.compile(r'"(\s+\([^)]*\))?\s+and\s+"')
    out = []
    for m in rx.finditer(q):
        out.append((m.start(), m.end(), m.group(1)))
    return out


def notes_from_decisions(w0, w1, human_msgs):
    entries = parse_decisions()
    hmsgs = [(d, norm(t)) for d, t in human_msgs]

    def find_in_transcript(qtext, date_str, after):
        key = norm(qtext)
        if len(key) > 80:
            key = key[:80]
        day = dt.date.fromisoformat(date_str)
        cands = []
        for d, t in hmsgs:
            if key and key in t:
                ld = d.astimezone(LOCAL_TZ)
                # the written date is Lati's local day; allow the small hours of the next day ("late")
                if ld.date() == day or (ld.date() == day + dt.timedelta(days=1) and ld.hour < 7) or \
                        (ld.date() == day - dt.timedelta(days=1) and ld.hour >= 20):
                    cands.append(d)
        if not cands:
            return None, 0
        later = [c for c in cands if after is None or c >= after]
        return (min(later) if later else min(cands)), len(cands)

    # first-seen commit times of headings and quote lines
    raw_quotes = []
    for e in entries:
        for kind, ln, text in split_blocks(e["body"]):
            if kind == "quote":
                raw_quotes.append(norm(text)[:100])
    keyset_h = set(e["heading"] for e in entries)
    keyset_q = set(raw_quotes)

    def keys_of(text):
        ks = []
        t_lines = text.split("\n")
        for l in t_lines:
            if l.strip() in keyset_h:
                ks.append(("h", l.strip()))
        nt = norm(text)
        for q in keyset_q:
            if q in nt:
                ks.append(("q", q))
        return ks

    seen = first_seen_times(keys_of)

    headings = []
    for e in entries:
        headings.append({"date": e["date"], "title": e["title"], "line": e["line"],
                         "committed": seen.get(("h", e["heading"]))})

    notes = []
    last_t = None
    for e in entries:
        if e["date"] < w0.astimezone(LOCAL_TZ).strftime("%Y-%m-%d"):
            continue
        blocks = split_blocks(e["body"])
        for bi, (kind, ln, text) in enumerate(blocks):
            if kind != "quote":
                continue
            parsed = parse_quote_block(text)
            if parsed:
                q, attrib, rest = parsed
                date_m = re.match(r"Lati,\s*(\d{1,2}) (Oct|Nov) (\d{4})", attrib)
                date = "%s-%02d-%02d" % (date_m.group(3), MONTHS[date_m.group(2)], int(date_m.group(1))) \
                    if date_m else e["date"]
                context = re.sub(r"^Lati,\s*\d{1,2} (Oct|Nov) \d{4}[,;]?\s*", "", attrib) if date_m else attrib
            elif e["kind"] == "bold" and "(Lati" in e["by"] and bi == 0:
                q, attrib, rest, date, context = text.strip(), e["by"].strip("()"), "", e["date"], ""
            else:
                continue
            addressee = "Flint" if re.search(r"\bto Flint\b", attrib) else "Kiln"
            # split two recorded messages only when the pieces match Lati's messages and the whole doesn't
            pieces = [strip_outer(q)]
            whole_t, _ = find_in_transcript(strip_outer(q), date, last_t)
            if whole_t is None:
                for s0, s1, between in candidate_splits(q):
                    a, b = strip_outer(q[:s0 + 1]), strip_outer(q[s1 - 1:])
                    ta, _ = find_in_transcript(a, date, last_t)
                    tb, _ = find_in_transcript(b, date, last_t)
                    if ta is not None and tb is not None:
                        pieces = [a, b]
                        break
            # the response: inline after "):", or the first Claude paragraph after this quote in the entry
            responder, response, direct = None, None, None
            inline = re.match(r"^\s*:\s*(.+)$", rest, re.S)
            if inline:
                responder, response, direct = "Kiln", first_sentence(inline.group(1)), True
            else:
                direct = True
                for kind2, ln2, text2 in blocks[bi + 1:]:
                    m = RESP.match(text2) if kind2 == "para" else None
                    if m:
                        responder, response = m.group(1), first_sentence(m.group(3))
                        break
                    if kind2 == "quote":
                        direct = False
            commit_t = seen.get(("q", norm(text)[:100]))
            for pi, piece in enumerate(pieces):
                t_tr, n_c = find_in_transcript(piece, date, last_t)
                if t_tr is not None:
                    t_note, src = t_tr, "transcript"
                    last_t = t_tr
                else:
                    t_note, src = commit_t, "commit"
                notes.append({
                    "d": t_note, "time_source": src, "transcript_matches": n_c,
                    "date": date, "heading": e["title"], "heading_date": e["date"], "decisions_line": ln,
                    "to": addressee, "quote": piece, "context": context or None,
                    "part": (pi + 1) if len(pieces) > 1 else None,
                    "responder": responder, "response_first_sentence": response,
                    "response_directly_after": direct,
                })
    return notes, headings


# ---------------------------------------------------------------- commits

def commits(w0, w1):
    out = git(FILM, "log", "--reverse", "--numstat", "--format=@@%H %aI%n%s")
    res = []
    cur = None
    for line in out.split("\n"):
        if line.startswith("@@"):
            h, t = line[2:].split(" ", 1)
            cur = {"hash": h[:8], "d": parse_iso(t), "subject": None, "files": 0, "added": 0, "removed": 0,
                   "binary_files": 0}
            res.append(cur)
        elif cur is not None and cur["subject"] is None:
            cur["subject"] = line
        elif cur is not None and line.strip():
            a, r, _ = line.split("\t", 2)
            cur["files"] += 1
            if a == "-":
                cur["binary_files"] += 1
            else:
                cur["added"] += int(a)
                cur["removed"] += int(r)
    rows = []
    for c in res:
        if not (w0 <= c["d"] <= w1):
            continue
        m = re.match(r"^([^:]{1,60}):\s", c["subject"])
        tag = m.group(1) if m else None
        stage = re.sub(r"\s*\(.*?\)\s*$", "", tag) if tag else None
        who = re.search(r"\(([^)]*)\)", tag) if tag else None
        rows.append({**c, "tag": tag, "tag_word": stage, "signed": who.group(1) if who else None})
    return rows


# ---------------------------------------------------------------- ledger, takes

def ledger():
    recs = [json.loads(l) for l in open(os.path.join(FILM, "production/motion/ledger.jsonl")) if l.strip()]
    sub = {}
    for r in recs:
        if r.get("status") == "submitted":
            sub[r["job"]] = r
    return recs, sub


def shot_of(clip):
    m = re.match(r"(s\d{3})", clip or "")
    return m.group(1) if m else None


def infer_model_from_file(clip_id):
    """Two early jobs (T1-D, Q1) have no model in the ledger; their files in media/motion name it."""
    for p in glob.glob(os.path.join(FILM, "media/motion/**/*.mp4"), recursive=True):
        b = os.path.basename(p)
        if clip_id == "T1-D" and b.startswith("D-seedance25"):
            return "bytedance/seedance-2.5", os.path.relpath(p, FILM)
        if clip_id == "Q1" and b.startswith("Q1-seedance25"):
            return "bytedance/seedance-2.5", os.path.relpath(p, FILM)
    return None, None


def spend(w0, w1):
    recs, sub = ledger()
    rows = []
    total = 0.0
    for r in recs:
        d = parse_local(r["at"])
        s = sub.get(r["job"], {})
        model = r.get("model") or s.get("model")
        model_src = "ledger"
        if not model:
            model, f = infer_model_from_file(r.get("clip"))
            model_src = ("file name " + f) if model else None
        cost = r.get("cost_usd")
        if cost:
            total += cost
        err = r.get("error")
        if err:
            err = re.sub(r"\s*Request id:.*$", "", err)
        rows.append({
            "d": d, "job": r["job"][-8:], "batch": r.get("batch"), "clip": r.get("clip"), "shot": shot_of(r.get("clip")),
            "status": r.get("status"), "model": model, "model_source": model_src,
            "kind": r.get("kind") or s.get("kind"),
            "seconds": r.get("duration") or s.get("duration"),
            "resolution": r.get("resolution") or s.get("resolution"),
            "estimate_usd": r.get("estimate_usd"), "cost_usd": cost, "total_usd": round(total, 5),
            "error": err, "file": r.get("file"),
        })
    return rows


RUN_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]+?)\s*\|(.*)\|\s*$")


def run_verdicts():
    """Lati's column of the take tables in motion/*-run.md and motion/opening-results.md."""
    out = {}
    files = sorted(glob.glob(os.path.join(FILM, "production/motion/*-run.md"))) + \
        [os.path.join(FILM, "production/motion/opening-results.md")]
    for p in files:
        rel = os.path.relpath(p, FILM)
        header = None
        for line in open(p, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.startswith("|"):
                header = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if "Lati" in cells and "Take" in cells:
                header = cells
                continue
            if header is None or set("".join(cells)) <= set("-: "):
                continue
            ti, li = header.index("Take"), header.index("Lati")
            # opening-results has a doubled '||' in some rows: the verdict is the last non-empty cell
            verdict = cells[li] if li < len(cells) else ""
            if not verdict:
                tail = [c for c in cells[li:] if c]
                verdict = tail[-1] if tail else ""
            take = cells[ti]
            name = re.sub(r"\s*\(.*$", "", take).strip().strip("`")
            label = cells[0] if header[0] in ("", "Batch") else None
            out[name] = {"verdict": verdict or None, "source": rel, "row_label": label or None, "as_written": take}
    return out


def takes(w0, w1):
    film_clips = os.path.join(FILM, "media/clips")
    disk = {}
    for p in glob.glob(os.path.join(film_clips, "*", "*.mp4")):
        b = os.path.basename(os.path.dirname(p))
        if b == "shot":
            continue
        stem = os.path.splitext(os.path.basename(p))[0]
        disk[stem] = os.path.relpath(p, FILM)
    for p in glob.glob(os.path.join(FILM, "media/motion/**/*.mp4"), recursive=True):
        stem = os.path.splitext(os.path.basename(p))[0]
        disk.setdefault(stem, os.path.relpath(p, FILM))

    T = {}

    def get(stem, file=None):
        t = T.get(stem)
        if t is None:
            t = T[stem] = {"take": stem, "file": file, "shot": shot_of(stem), "batch": None, "sources": [],
                           "ledger_status": None, "model": None, "seconds": None, "cost_usd": None, "d": None,
                           "default_take": False, "in_cut": False, "cut_clips": 0, "cut_note": None,
                           "verdict": None, "verdict_source": None}
        if file and not t["file"]:
            t["file"] = file
        return t

    # 1. ledger jobs
    sp = spend(w0, w1)
    recs_all, _ = ledger()
    by_job = defaultdict(list)
    for r in sp:
        by_job[(r["job"], r["clip"])].append(r)
    for (job, clip), rs in by_job.items():
        done = [r for r in rs if r["status"] == "completed"]
        fail = [r for r in rs if r["status"] == "failed"]
        sub = [r for r in rs if r["status"] == "submitted"]
        if done:
            f = done[-1]["file"]
            stem = os.path.splitext(os.path.basename(f))[0]
            ondisk = os.path.exists(os.path.join(FILM, f))
            if not ondisk:
                # two early jobs were saved under media/motion with the job's token in the name
                full_job = next(r0["job"] for r0 in recs_all if r0["job"].endswith(job))
                tok = full_job.split("-")[-1]
                alt = [s0 for s0 in disk if tok in s0]
                if alt:
                    f2 = disk[alt[0]]
                    stem = alt[0]
                    t = get(stem, f2)
                    t["cut_note"] = "the ledger's path %s is not on disk; the file is %s (same job id)" % (f, f2)
                else:
                    t = get(stem, f)
                    t["cut_note"] = "the ledger's file path is not on disk"
            else:
                t = get(stem, f)
            t["ledger_status"] = "completed"
            t["cost_usd"] = done[-1]["cost_usd"]
            t["d"] = done[-1]["d"]
        else:
            stem = "%s (job %s)" % (clip, job)
            t = get(stem)
            t["ledger_status"] = "failed" if fail else "submitted"
            t["d"] = (fail or sub)[-1]["d"]
            t["cut_note"] = fail[-1]["error"] if fail else None
        s0 = sub[0] if sub else rs[0]
        t["batch"] = rs[0]["batch"]
        t["model"] = s0["model"]
        t["seconds"] = s0["seconds"]
        t["shot"] = shot_of(clip) or t["shot"] or clip
        t["sources"].append("ledger")

    # 2. takes.json defaults
    tj = json.load(open(os.path.join(FILM, "production/edit/takes.json")))["takes"]
    for shot, pat in tj.items():
        hits = sorted(glob.glob(os.path.join(film_clips, pat if pat.endswith(".mp4") else pat + ".mp4"))) or \
            sorted(glob.glob(os.path.join(film_clips, pat)))
        hits = [h for h in hits if h.endswith(".mp4")]
        if not hits:
            t = get("%s (takes.json: %s)" % (shot, pat))
            t["shot"] = shot
            t["cut_note"] = "takes.json pattern matched no file"
        for h in hits:
            stem = os.path.splitext(os.path.basename(h))[0]
            t = get(stem, os.path.relpath(h, FILM))
            t["shot"] = shot
            t["default_take"] = True
            if "takes.json" not in t["sources"]:
                t["sources"].append("takes.json")
            t["batch"] = t["batch"] or os.path.basename(os.path.dirname(h))

    # 3. run-md verdicts (match a written take name to a file stem: equal, or the stem starts with name + '-')
    rv = run_verdicts()
    stems = sorted(set(list(disk) + list(T)))
    for name, v in rv.items():
        matched = [s for s in stems if s == name or s.startswith(name + "-")]
        if len(matched) > 1:
            exact = [s for s in matched if s == name]
            matched = exact or matched
        if not matched:
            t = get(name)
            t["cut_note"] = "named in %s; no file found" % v["source"]
            matched = [name]
        for s in matched:
            t = get(s, disk.get(s))
            t["verdict"], t["verdict_source"] = v["verdict"], v["source"]
            if "run-md" not in t["sources"]:
                t["sources"].append("run-md")
            if not t["batch"] and disk.get(s):
                t["batch"] = os.path.basename(os.path.dirname(disk[s]))

    # 4. the final cut
    tl = json.load(open(os.path.join(FILM, "production/edit/timeline.json")))
    gfx_shots = []
    for tr in tl["tracks"]:
        for c in tr["clips"]:
            if c.get("kind") != "video":
                continue
            f = c["file"]
            real = os.path.realpath(os.path.join(FILM, f))
            rel = os.path.relpath(real, FILM)
            if rel.startswith("media/gfx/"):
                gfx_shots.append(c.get("shot"))
                continue
            stem = os.path.splitext(os.path.basename(rel))[0]
            t = get(stem, rel)
            if stem.startswith("rough-"):
                t["cut_note"] = "a rough cut assembled from motion test 1's takes (an edit, not one generation)"
                t["not_a_generation"] = True
            t["in_cut"] = True
            t["cut_clips"] += 1
            if "timeline" not in t["sources"]:
                t["sources"].append("timeline")
            if not t["shot"]:
                t["shot"] = c.get("shot")
            if not t["batch"]:
                t["batch"] = rel.split("/")[2] if rel.startswith("media/clips/") else os.path.dirname(rel)
    for s in gfx_shots:
        for t in T.values():
            if t["shot"] == s and t["default_take"]:
                t["cut_note"] = ("shot %s plays in the cut as a locked graphics render (media/gfx/locked); "
                                 "this is takes.json's default take for the shot, not resolved further" % s)
    for t in T.values():
        if t["file"] and not t["file"].startswith("media/"):
            t["file"] = os.path.relpath(t["file"], FILM)
        t["on_disk"] = bool(t["file"]) and os.path.exists(os.path.join(FILM, t["file"]))
    unref = sorted(s for s in disk if s not in T and not re.search(r"reel|side-by-side|rough", s))
    return sorted(T.values(), key=lambda t: (t["shot"] or "~", t["take"])), unref, sorted(set(gfx_shots)), tl


# ---------------------------------------------------------------- agents, other sessions

def agents(w0, w1):
    rows = []
    for meta in sorted(glob.glob(os.path.join(SUBS, "*.meta.json"))):
        aid = os.path.basename(meta)[: -len(".meta.json")]
        path = os.path.join(SUBS, aid + ".jsonl")
        if not os.path.exists(path):
            continue
        m = json.load(open(meta))
        far = dt.datetime(2100, 1, 1, tzinfo=UTC)
        cl, _, _, first, last = read_transcript(path, dt.datetime(2000, 1, 1, tzinfo=UTC), far)
        if first is None or not (w0 <= first <= w1):
            continue
        desc = m.get("description")
        section = None
        g = re.match(r"Graphics agent ([A-D]): (\w+)", desc or "")
        if g:
            section = g.group(2)
            for cand in (section, {"opening": "opening", "battles": "battles", "verse": "verse2", "end": "end"}.get(section)):
                if cand and os.path.exists(os.path.join(FILM, "production/edit/agents/%s.md" % cand)):
                    section = cand
                    break
        rows.append({
            "id": aid.replace("agent-", ""), "description": desc, "agent_type": m.get("agentType"),
            "start": first, "end": last, "calls": len(cl),
            "output_tokens": sum(c["out"] for c in cl),
            "peak_context": max((c["ctx"] for c in cl), default=0),
            "models": sorted(set(c["model"] for c in cl)),
            "log": ("production/edit/agents/%s.md" % section) if section else None,
            "series": cl,
        })
    rows.sort(key=lambda r: r["start"])
    return rows


def other_sessions(w0, w1):
    rows = []
    for p in sorted(glob.glob(os.path.join(PROJ, "*.jsonl"))):
        sid = os.path.basename(p)[:-6]
        if sid == KILN_ID:
            continue
        cl, _, _, first, last = read_transcript(p, w0, w1)
        if first is None or last < w0 or first > w1:
            continue
        rows.append({"session": sid[:8], "first": first, "last": last, "calls_in_window": len(cl),
                     "output_tokens_in_window": sum(c["out"] for c in cl)})
    return rows


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", default=None, help="window end: ISO time, or 'now' (default: the making-of's first commit)")
    a = ap.parse_args()
    w0, w1, end_src = window(a.end)
    os.makedirs(OUT, exist_ok=True)

    def T(d):
        return round((d - w0).total_seconds(), 3)

    print("window", iso(w0), "->", iso(w1), "(%s)" % end_src)

    # Kiln's main transcript
    calls, users, comps, k_first, k_last = read_transcript(KILN, w0, w1, want_users=True, want_compactions=True)
    all_turns = lati_turns(users)
    turns = [t for t in all_turns if w0 <= t["d"] <= w1]
    print("calls", len(calls), "turns", len(turns))

    # decisions: notes and headings (quotes are matched against all of Lati's messages, before the window too)
    human = [(t["d"], t["text"]) for t in all_turns if t["kind"] == "message"]
    notes, headings = notes_from_decisions(w0, w1, human)
    hd = sorted([h for h in headings if h["committed"]], key=lambda h: h["committed"])
    hd_t = [h["committed"] for h in hd]

    # calls.json
    models = sorted(set(c["model"] for c in calls))
    write("calls.json", {
        "about": "Kiln's model calls in the window, one row per API call (deduped by message id). ctx = input + "
                 "cache_read + cache_creation tokens. See README.",
        "window_start": iso(w0), "window_end": iso(w1),
        "fields": ["t", "ts", "ctx", "out", "in", "cache_read", "cache_creation", "model"],
        "models": models,
        "rows": [[T(c["d"]), iso(c["d"]), c["ctx"], c["out"], c["in"], c["cr"], c["cc"], models.index(c["model"])]
                 for c in calls],
    })

    # compactions.json
    ct = [c["d"] for c in calls]
    crow = []
    seen_c = set()
    for d, meta, u in sorted(comps, key=lambda x: x[0]):
        if u in seen_c or not (w0 <= d <= w1):
            continue
        seen_c.add(u)
        i = bisect.bisect_left(ct, d)
        before = calls[i - 1] if i > 0 else None
        after = calls[i] if i < len(calls) else None
        j = bisect.bisect_right(hd_t, d) - 1
        st = hd[j] if j >= 0 else None
        crow.append({
            "t": T(d), "ts": iso(d), "trigger": meta.get("trigger"),
            "pre_tokens": meta.get("preTokens"), "post_tokens": meta.get("postTokens"),
            "duration_ms": meta.get("durationMs"),
            "ctx_last_call_before": before["ctx"] if before else None,
            "last_call_before_ts": iso(before["d"]) if before else None,
            "ctx_first_call_after": after["ctx"] if after else None,
            "first_call_after_ts": iso(after["d"]) if after else None,
            "stage_heading": st["title"] if st else None, "stage_date": st["date"] if st else None,
            "stage_heading_committed": iso(st["committed"]) if st else None,
        })
    outside = [(iso(d), m.get("trigger"), m.get("preTokens")) for d, m, u in comps if not (w0 <= d <= w1)]
    near = [o for o in outside if abs((parse_iso(o[0]) - w0).total_seconds()) < 86400]
    write("compactions.json", {"about": "Compactions of Kiln's session in the window. See README.",
                               "rows": crow,
                               "just_outside_window": [{"ts": a, "trigger": b, "pre_tokens": c} for a, b, c in near]})

    # commits.json
    cm = commits(w0, w1)
    write("commits.json", {"about": "Film 3's commits (git log --numstat), oldest first. See README.",
                           "rows": [{"t": T(c["d"]), "ts": iso(c["d"]), "hash": c["hash"], "subject": c["subject"],
                                     "tag": c["tag"], "tag_word": c["tag_word"], "signed": c["signed"],
                                     "files": c["files"], "added": c["added"], "removed": c["removed"],
                                     "binary_files": c["binary_files"]} for c in cm]})

    # spend.json
    sp = spend(w0, w1)
    write("spend.json", {"about": "production/motion/ledger.jsonl, every line, oldest first; OpenRouter USD only. "
                                  "See README.",
                         "rows": [{"t": T(r["d"]), "ts": iso(r["d"]), **{k: v for k, v in r.items() if k != "d"}}
                                  for r in sp]})

    # notes.json
    nrows = []
    health_flags = []
    for n in notes:
        row = {"t": T(n["d"]) if n["d"] else None, "ts": iso(n["d"]) if n["d"] else None,
               "in_window": bool(n["d"] and w0 <= n["d"] <= w1),
               **{k: v for k, v in n.items() if k != "d"}}
        if HEALTH_WORDS.search(n["quote"]):
            health_flags.append((n["date"], n["decisions_line"], len(HEALTH_WORDS.findall(n["quote"]))))
        nrows.append(row)
    write("notes.json", {"about": "Every Lati quote in film 3's decisions.md dated 1 Nov 2026 or later, verbatim. "
                                  "See README.", "rows": nrows})

    # agents.json
    ag = agents(w0, w1)
    write("agents.json", {"about": "Kiln's subagent runs that started in the window. series rows: [t, ctx, out]. "
                                   "See README.",
                          "rows": [{"id": r["id"], "description": r["description"], "agent_type": r["agent_type"],
                                    "start_t": T(r["start"]), "start": iso(r["start"]),
                                    "end_t": T(r["end"]), "end": iso(r["end"]),
                                    "calls": r["calls"], "output_tokens": r["output_tokens"],
                                    "peak_context": r["peak_context"], "models": r["models"], "log": r["log"],
                                    "series": [[T(c["d"]), c["ctx"], c["out"]] for c in r["series"]]}
                                   for r in ag]})

    # takes.json
    tk, unref, gfx_shots, tl = takes(w0, w1)
    write("takes.json", {"about": "Every generated take named in the ledger, edit/takes.json, a run file's take "
                                  "table, or the final cut. See README.",
                         "timeline_saved": tl.get("saved"), "gfx_locked_shots_in_cut": gfx_shots,
                         "clips_on_disk_not_referenced": unref,
                         "rows": [{"t": T(t["d"]) if t["d"] else None, "ts": iso(t["d"]) if t["d"] else None,
                                   **{k: v for k, v in t.items() if k != "d"}} for t in tk]})

    # turns.json
    write("turns.json", {"about": "Lati's messages to Kiln in the window: time and length only. See README.",
                         "rows": [{"t": T(t["d"]), "ts": iso(t["d"]), "kind": t["kind"], "mid_turn": t["mid_turn"],
                                   "chars": t["chars"], "images": t["images"]} for t in turns]})

    # sessions.json (other local sessions; no content)
    os_rows = other_sessions(w0, w1)
    write("sessions.json", {"about": "Other local Claude Code sessions in ~/.claude/projects/-home-shegs-Claudia "
                                     "with records in the window: time span and call count only. See README.",
                            "kiln": {"session": KILN_ID[:8], "first": iso(k_first), "last": iso(k_last)},
                            "rows": [{"session": r["session"], "first": iso(r["first"]), "last": iso(r["last"]),
                                      "first_t": T(r["first"]), "last_t": T(r["last"]),
                                      "calls_in_window": r["calls_in_window"],
                                      "output_tokens_in_window": r["output_tokens_in_window"]} for r in os_rows]})

    # summary.json
    made = [t for t in tk if t["ledger_status"] in (None, "completed") and t["on_disk"]
            and not t.get("not_a_generation")]
    used = [t for t in tk if t["in_cut"]]
    days_active = sorted(set(c["d"].astimezone(LOCAL_TZ).date().isoformat() for c in calls))
    summary = {
        "window_start": iso(w0), "window_end": iso(w1), "window_end_is": end_src,
        "days": round((w1 - w0).total_seconds() / 86400, 2),
        "calendar_days_local": (w1.astimezone(LOCAL_TZ).date() - w0.astimezone(LOCAL_TZ).date()).days + 1,
        "days_with_kiln_calls_local": len(days_active), "dates_with_kiln_calls_local": days_active,
        "commits": len(cm),
        "lines_added": sum(c["added"] for c in cm), "lines_removed": sum(c["removed"] for c in cm),
        "calls": len(calls),
        "output_tokens": sum(c["out"] for c in calls),
        "peak_context": max(c["ctx"] for c in calls), "peak_context_ts": iso(max(calls, key=lambda c: c["ctx"])["d"]),
        "compactions": len(crow),
        "lati_messages": sum(1 for t in turns if t["kind"] == "message"),
        "takes_made": len(made), "takes_in_cut": len(used),
        "takes_in_cut_note": "clips placed in timeline.json resolved to a take file; plus %d shots (%s) that play as "
                             "locked graphics renders" % (len(gfx_shots), ", ".join(gfx_shots)),
        "paid_jobs_completed": sum(1 for r in sp if r["status"] == "completed"),
        "paid_jobs_failed": sum(1 for r in sp if r["status"] == "failed"),
        "spend_usd": round(sum(r["cost_usd"] or 0 for r in sp), 2),
        "spend_note": "OpenRouter only (the ledger). ISEKAI ZERO credits and Lati's Grok subscription are not in it.",
        "paid_seconds": sum((r["seconds"] or 0) for r in sp if r["status"] == "submitted"),
        "agents": len(ag), "agent_calls": sum(r["calls"] for r in ag),
        "agent_output_tokens": sum(r["output_tokens"] for r in ag),
        "notes": len([n for n in nrows]), "notes_in_window": sum(1 for n in nrows if n["in_window"]),
        "other_sessions_in_window": len(os_rows),
    }
    write("summary.json", summary)

    # final privacy scan of data/ (re-read every file as text)
    found = []
    for p in sorted(glob.glob(os.path.join(OUT, "*.json"))):
        s = open(p, encoding="utf-8").read()
        for v in ENV_VALUES:
            if v in s:
                found.append((os.path.basename(p), "env-value"))
        for name, rx in SECRET_PATTERNS:
            for h in rx.findall(s):
                found.append((os.path.basename(p), name))
    scan = {
        "removed_while_writing": [{"where": w, "pattern": n, "count": c} for w, n, c in SCRUB_LOG],
        "found_in_final_scan": [{"file": f, "pattern": n} for f, n in found],
        "health_word_hits_in_notes": [{"date": d, "decisions_line": l, "hits": k} for d, l, k in health_flags],
        "env_values_checked": len(ENV_VALUES),
    }
    with open(os.path.join(OUT, "privacy-scan.json"), "w", encoding="utf-8") as f:
        json.dump(scan, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps(summary, indent=1))
    print("privacy:", json.dumps(scan, indent=1)[:3000])


if __name__ == "__main__":
    main()
