# Agent log: bridge

Section C, chorus 2 and the bridge. Song time 82.31-128.59. Agent C for Claude (Kiln, local), 12 Nov 2026.
File: `tools/film/sec_c_bridge.py` (RANGES [(82.31, 128.59)]). Media: `media/bridge/` (cache, check frames, pass1).

## What I read
notes/agents.md, treatment.md, decisions.md, base.py, film3_gfx.py, render.py, check.py, data/README.md; data rows
for notes, commits, takes, agents, compactions in my window; film 3's `production/edit/timeline.json` and its git
history; the master (contact sheets of the insert spans, media/bridge/look/).

## Sources and how they're used (all read-only)
- **The timeline as it grew:** every committed version of `production/edit/timeline.json` in film 3's repo
  (`git log` / `git show`, read-only, at load). Each version lands at the time its own `saved` field records (the
  editor writes local time, EET), not the commit time. 23 versions; the ones in my window: 9072e9f (saved 21:18:36
  EET, Lati's cut to 1:21) through dbe2e96 (01:20:41). Between 10 Nov 21:04 and 11 Nov 21:18 nothing was
  committed, so 82.31-99.13 shows the 10 Nov version (the cut plan, 47 stills); the rough cut to 1:05 named in the
  11 Nov stage heading was never committed as a file, so it isn't shown.
- Clip kinds from the file: `kind: image` = a still standing in (cyan outline), `media/gfx/locked/` = a locked
  graphics render (clay), else a take (amber block). A version's additions flash white, its removals go out in red
  (0.5 s). Counts in the header ("N clips: a motion b stills c gfx") are my count of the file.
- The playhead is song time t on the cut (the cut is timed to the song): where the main film is right now.
- **Takes strip:** data/takes.json rows whose ledger time falls 82.31-104.92 (60 takes): amber = in Lati's cut, dim =
  not, red = failed job. Each lands at song_at(its ledger time).
- **Lati's notes:** 14 picks from data/notes.json, at song_at(ts). Each is checked at load to be a substring of his
  quote; an excerpt carries "..." on the side where his quote goes on. Typos kept ("farmnfeel", "Lets"). Red for the
  one that records a mistake ("plates to review first ... just now you went ahead without confirmation.").
- **Inserts** from master-1080-v1.mp4 (crop 1600x900 from the top: the master's own lyric line cut off so it doesn't
  read as this video's), each opening on the first beat after the note that approved the shot, never overlapping:
  s032 retake 83.41-85.61 (master 53.55), s046 redo 87.27-89.48 (70.5), the Grok opening 90.04-91.70 (0.0), the
  pilots s083 101.06-102.16 (128.8), the nuclear end s108-v2c 102.72-104.92 (168.2; about a second of it is the
  shot's white-out). Cached as .npy in media/bridge/cache/.
- **The code (104.92-116.07):** tools/film/*.py read at load (whatever is there at render time, other sections
  included). 104.92 base.py's head; "We are what you see" (words of lyric line 19) steps through base.frame() a word a
  line; "Every part, every word" (line 20) film3_gfx.karaoke(), the `part = text[...]` line on "part" and
  `crt_text(c, part ...)` on "word"; "It's how you came to be" (line 21) base.PINS from the first commit down to the
  `"Me": the 12 Nov compaction` pin on "be". Then render.py's frame loop (highlight on the 110.44 beat), the sec_*.py
  files an equal share of 110.99-113.21 each, film3_gfx.py from the top slowing into crt_text and its Lati comment
  ("only crt letters ...", which ba54655c wrote at 00:28 UTC = song ~115.0), and from 115.39 base.gauge() with
  `if flash > 0:` / the white drawRect highlighted on 115.94, so the code that whites out the gauge is on screen as it
  does. Anchors are found by text, so edits to base.py move them with it.
- **"Me":** verified in Kiln's transcript, line 50614, timestamp 2026-11-12T00:32:08.930Z (the /compact command; the
  boundary record is 00:33:53): the args begin "Keep, verbatim where quoted: (1) I am Claude (Kiln), the local Claude
  Code session on Lati's machine (he/him), Opus 5.5." I type that sentence (without "(1)") from 116.155, 0.7 s, hold,
  out by 118.14, caption "/compact  keep (1)". The command was 00:32 UTC, not 00:33 as the brief said.
- **Agents:** data/agents.json, the four "Graphics agent" rows, lanes from 116.79; x = production time from
  clock(116.19) to clock(128.59) (00:3x-01:30 UTC, labelled in EET every 10 min). Each call a cyan bar at its time,
  height = its context / 360k; newest white; counter "N calls  ctx <that call's context>". By 01:30: A 62 calls,
  B 60, C 50, D 40 (D's last call 01:09:50). Lati's go (00:51:48 UTC, song 120.06) typed above the lanes, excerpt
  "... after these changes, its fine to start the agentic pass, as you as reviewer".

## Helpers in my file
next_beat/beats_after (beat grid), eet(), rect/frame_rect/line/phosphor_block (Skia drawing), versions()/version_at()
(timeline history), day_takes(), notes()/_note() (verbatim check), inserts()/insert_frames() (ffmpeg decode + cache),
sources()/find()/code_plan() (the code view), lanes().

## Checks
Frame checks with check.py --only sec_c_bridge at 82.35, 82.6, 83.8, 84.5, 87.5, 95, 99.6, 100.5, 101.3, 102.5,
103.95, 104.1, 104.6, 104.95-116.0 (12 frames), 116.2-127.6 (10 frames); contact sheets read. Fixed after the first
look: "…" read as "_" in the CRT letters (now "..."); the insert title overlapped its timecode (timecode moved under
the window); the code view's anchors found the first match in the file instead of inside frame().

## For Kiln
- The chorus 2 pin is linear 05:53 -> 23:30 UTC, and the record is silent 09:40-19:18 UTC (Lati at work), so
  ~91.7-99.1 has nothing new in the centre (the clock races, the playhead moves), while the whole evening (mid-2,
  mid-3, the end, the 1:52 fill, Lati's cut) lands in 99.1-104.4. An extra pin, e.g. 09:40Z at ~86.7 and 19:15Z at
  ~89-91, would spread the evening over the chorus. Everything here places by song_at, so it follows a new pin.
- The quiet cockpit (s095q-b) arrives after the bridge starts (take 23:43Z = song ~106.8, placed in 16da28a saved
  01:47 EET = ~107.6), so the editor can't show it landing; it shows the empty calm spot (Lati's 2:21.05-2:26.10,
  red bracket) and his "lets make plates" instead. The base's commit log carries "the quiet cockpit in".

## Render
`media/bridge/pass1.mp4`: 82.31-128.59 at 720, --only sec_c_bridge, 1111 frames (expected 1111), with the song.

## Pass 2 (Kiln's answers, 12 Nov)
- Kiln added two pins to base.py: (88.00, 09:40Z) and (89.60, 19:18Z). New placement, checked by printing the
  schedule: the morning notes land 82.45-88.37, the version saved 21:18:36 at 89.64, and the evening is spread over
  89.6-104.4 (versions 89.64, 90.48, 93.05 ... 103.83; notes about 1 s apart).
- Inserts, each on the first beat after its note, none overlapping: s032 83.41-85.61; s046 87.83-88.93 (shortened
  to 2 beats, because the Grok note follows 0.6 s after s046's); Grok opening 88.93-90.59; pilots 95.01-96.10;
  nuclear end 98.87-101.06.
- The diagonal leader from the insert window to its clip crossed the whole timeline when the clip was far left
  (the Grok opening at 0:00). It's now a cyan box around the clip in the cut, drawn only when the displayed
  version holds the clip at that start time.
- Calm cockpit: kept as the record has it (Kiln).
- Frame checks: 85.3, 87.9, 88.5, 89.8, 92.7, 95.5, 98.4, 99.6, 102.0, 103.5 (media/bridge/check2, sheet2_*.jpg).
  Nothing collides; the notes log scrolls one note at a time.
- `tools/data/timeline_history.py` (asked for by Kiln): every committed version of the timeline as one JSON, through
  extract.py's privacy filter. Not wired in; tested only with --out media/bridge/cache/timeline-history.json:
  23 versions, 2133 clip rows, 0 privacy hits. data/ untouched.
