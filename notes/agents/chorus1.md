# Agent log: chorus1

Section B, chorus 1, verse 2 and the break. Song time 44.69-82.31. Agent B for Claude (Kiln, local), 12 Nov 2026.
File: `tools/film/sec_b_chorus1.py`. Cache: `media/chorus1/cache/` (thumbnails, master inserts). Checks:
`media/chorus1/check/`. Render: `media/chorus1/pass1.mp4`.

## Read

notes/agents.md, treatment, decisions.md, base.py, film3_gfx.py, data/README.md; takes.json, spend.json, notes.json
(the window 9 Nov 17:28Z to 11 Nov 05:53Z); film 3's decisions.md (for verse 2), motion/opening-results.md,
motion/mid-2-run.md, edit/timeline.json (where takes play in the cut); master frames at the insert times.

## What's on screen

**Chorus 1, 44.69-66.81: the wall of takes.** 72 cells (12 x 6, each 66x37 units): every row of takes.json made by
11 Nov 05:53Z except `rough-1` (an edit, not a take, as summary.json counts). A cell appears at `song_at(made)`,
never earlier; a burst is spread 0.06 s apart so it stays countable (the battle-2-3 burst runs 46.26-47.22). The
picture is the take's first frame, 32x18, dithered to the main film's palette (`G.quantize`), wiping in; a white flash
on arrival. In the final cut: full brightness and an amber frame; not: 30%. Failed jobs: red cells marked FAILED.
Below the wall: `TAKES n  IN FINAL CUT n  FAILED n`; Lati's verdict of the moment; a log of the last 7 takes
(time EET, the ledger's clip id or the take name, the model).

Made times:
- ledger takes: the ledger's completion/failure time (takes.json `ts`).
- ISEKAI ZERO takes (the opening batch, s078/s080 `sd20-isk0`): the media id in the file name; its first 4 bytes are
  the id's creation time (6af2a3e3 = 10 Nov 04:56:03Z, batch 1; 6af2ed27 = 10:08:39Z, batch 5; matches Flint's
  commits). That's the job's creation, not completion. Model shown as `seedance-2.0/isk0` (opening-results.md:
  "Seedance 2.0 on ISEKAI ZERO").
- Lati's two test-1 Grok takes (s001, s003; in the cut): no time in the record; they are there at the drop and their
  log time reads `test1`. Model `grok imagine`.
- T1-D and Q1 (7-8 Nov) also there at the drop.

Verdicts (typed in verbatim, on the beat at or after the time he sent it; each asserted against notes.json):
- 45.81 decisions 502 (9 Nov 20:19 EET): "Overall wan reads as more 3d animated and seedance as 80s cinematic anime."
- 47.46 decisions 581 (22:16): "both are good. seedance 2.0 holds up quite well."
- 55.23 decisions 592, to Flint (10 Nov 06:55): "Run opening plates with alternates, but in batch of 4, then stop for my review for them."
- 56.87 decisions 598, to Flint (08:52): "S005: both have same problem, fleet is stationary, then starts moving."
- 64.06 decisions 696 (17:04): "yeah, for lipsync, 2.5. 2.0 invents second mic boom, and lipsync is weaker. clear result."

Inserts (a window that opens out of the take's cell, title `take @ m:ss.ss` of the master, scanlines, his words
about it as the caption; master cropped to 1600x900 from the top so its burned-in lyric line is out):
- 46.35-46.91 s033-6, "very good." (528, 9 Nov 19:07Z). Master at the same time, 46.35: s033 plays there in the cut.
- 46.91-49.12 s054-2, "awsome, entirely." (551, 19:38Z). Master 1:31.33 (one bar). Back to back with s033: the
  window stays open.
- 56.87-58.98 s006-r-h2-1, "pretty cool." (598, to Flint, 10 Nov 06:52Z). Master 0:08.79.
- 64.62-66.81 s050 (the red lens, locked render; opens from the `s050-claudia` cell, the lip-synced face it carries:
  decisions 731), "works, hal is done." (738, 15:47Z). Master 1:18.62.

**Verse 2, 66.81-80.06: what went wrong.** The wall shrinks to a strip (24 x 3) in 0.25 s; then `WHAT WENT WRONG`
in red and the sources line. Eleven items, one per half bar (66.81 ... 77.83), in date order; each a red header
(its own date and time EET, outside the clock's window where it is) and the record's words: Lati amber (newest
white), Kiln clay, the ledger red. The list scrolls like a terminal; older items at 55%. Cells on the strip go red
when their item prints (Grok cells; s037-1; the four failed jobs).

1. 7 Nov 23:33 LoRA set aside: Lati "yes, set it aside" (167); Kiln "her LoRA is set aside (dataset, captions and look tests kept)" (decisions.md).
2. 9 Nov 20:40 Grok Imagine on the battle plates: too modern: "looks very 3d and not 80s anime." / "but is way too "modern"." (511).
3. 9 Nov 21:07 Battle 1 takes: "s037-1 error in here, claude mech ends up shooting at identical one too." (528).
4. 9 Nov 21:46 s078-1-sd25, s080-2-sd25: 4 jobs FAILED: the ledger's error ("...output video may be related to copyright restrictions.") and Lati "we know they are original designs, we made them." (563).
5. 10 Nov 18:48 The library's "best fits" ignored the filters: "I have "warp" selected ... something is wrong." (791).
6. 10 Nov 19:22 Kdenlive's OpenTimelineIO import (the entry's context): "a: nothing happens. b: nothing happens." (820).
7. 11 Nov 08:09 Mid-1 batch 2: s032 retake: "B2-2 is weakest: ... for no reason." (889).
8. 11 Nov 21:41 s060-c: FAILED: the ledger's error ("...output audio may be related to copyright restrictions.") and mid-2-run.md "our own vocal; failed jobs cost 0".
9. 11 Nov 23:29 The nuclear end, again: plates first: "plates to review first, ... without confirmation." (1016) and Kiln "I ran motion before he had seen the plates ($2.79 on two takes neither of which works)."
10. 11 Nov 23:29 s108-anime, s108-real: "realistic is too realistic in terms of style and explosions are equally spaced." (1016).
11. 11 Nov 23:45 edit/timeline.json: the V3 s069 still: Kiln "the V3 s069 still at 1:52.08 was your edit, a held frame after your ×3 launch, not a placeholder." Source: Kiln's session, his reply of 11 Nov 21:45Z (records 49395-49432, found with the memory search). decisions.md only says "Kept: Lati's s069 edits on V3"; data/ doesn't hold this line. Hardcoded, checked by eye against the transcript.

Every other excerpt is asserted at load against notes.json, spend.json or the film-3 file it comes from; a change in
the record stops the render rather than showing a wrong line.

**The break, 80.06-82.31:** the centre clears; a cursor block at the list's top blinks on each beat. The base whites
out the gauge and types the summary line.

## Helpers in the file
`takes(B)` (the cells and their times), `thumb()` (ffmpeg first frame -> cache -> dithered 32x18), `insert_frames()`
(ffmpeg master span -> cropped, 576x324 -> .npy cache), `_note()`/`_f3()` (excerpt asserts), `wrap()`, `typed()`,
`cell_rect()` (wall to strip), `draw_wall/counts/log/verdict/insert/wrongs/cursor`.

## Checks
Frames at 44.75, 46.2, 46.6, 46.95, 47.0, 47.5, 48.0, 54.9, 57.5, 59.0, 65.5, 66.5, 66.95, 67.15, 67.3, 67.5, 70.5,
74.0, 77.0, 79.5, 80.1, 80.5, 82.2, read as JPEGs. Fixed from them: the counts collided with the clock (moved under
the wall); the log ran under the insert window (shorter model label, narrower window); captions overflowed the window
(take id moved to the title, captions are his words only); the sources line ran into the commit log (own line); the
verse-2 list drew over the shrinking wall (now after it settles); back-to-back inserts flickered (window stays open);
the log printed an invented time for the Grok takes (now `test1`). The summary line's spot (y ~810) stays clear: the
window ends at y 790, the list at 790.

## Open
- s050's insert at 64.62-66.81 plays a lip-synced face where the song has no vocal. In the master it's in sync at
  78.62 ("I'm afraid I can't do that"), which falls in verse 2; I kept the rule (where it was approved). Lati to judge.
- The wall stops at 72 cells (11 Nov 05:53Z). If chorus 2 continues it, `takes()` and `cell_rect()` are reusable.
