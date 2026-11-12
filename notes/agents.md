# Section agents for the making-of: how you work

Claude (Kiln, local), 12 Nov 2026, from the main film's agent rules. You're one of four agents building the centre of
the making-of of *I'm Not You*, a section each. Kiln directs and reviews; Lati (he/him) is the eyes and ears, and his
word decides. He approved the base test on 12 Nov: "reads as a terminal, and not ui overlay, which i think is cool",
the sizes included. Your section must read the same way: a terminal printing the production's record, not a dashboard.

## Read first
1. `notes/treatment.md` (the idea, the parts, the clock) and `decisions.md`.
2. `tools/film/base.py`, all of it: the clock (`clock(t)`, `song_at(u)`, PINS), the record (`rows(name)`, `calls()`,
   `commits()`, `spend()`, `compactions()`, `context_at()`), the furniture, `crt()` for text, the palette, `frame()`.
   `tools/film/film3_gfx.py` is the main film's base (vendored): `BEATS`, `DOWNS`, `beat_no`, `pulse`, `ease`, `LINES`,
   `WORDS`, `psf`/`stamp` (the 8x8 console font), `quantize`/`crt` (the pixel module).
3. `data/README.md`: every dataset and its fields and caveats. The data is the record, already privacy-filtered.
4. The main film, for inserts and context: `/home/shegs/Im not you` (quote: spaces). Its master:
   `media/render/master-1080-v1.mp4`; the takes: `media/clips/`, the plates: `media/plates/`; its decisions.md.

## The frame
- The base draws the furniture: clock and date (top left), OPENROUTER spend (top right), the context gauge (left,
  x 80-230), the commit log (right, x 1180-1860), the lyric line (bottom), and at each compaction a white-out of the
  gauge and the summary's first line typed at x 270, y ~810.
- **Yours is the centre:** about x 300-1140, y 150-860, in 1920x1080 units. Your `draw(c, t, B)` paints there with
  Skia; it runs before the furniture. Keep out of the bottom band (the lyric) and clear the summary line's spot for
  2.4 s after a compaction.
- Text: `B.crt(c, text, x, y, px=2..4, rows_=9..13, color=...)`, the same letters as the base. Amber for text, cyan for
  the work's instruments, red for what went wrong, white for the newest line, clay for Claude's side. Dark ground.

## The rules
- **Your files only:** `tools/film/sec_<yours>.py` (with `RANGES = [(t0, t1)]` and `draw(c, t, B)`), `media/<section>/`,
  your log `notes/agents/<section>.md`. Not yours: base.py, render.py, check.py, film3_gfx.py, data/, tools/data/, the
  main film's repo (read only). Helpers go in your file; note them in your log.
- **No git** (Kiln commits). No GPU, no network, no paid services, no downloads.
- **Everything shown is the record:** numbers, times, commit lines and Lati's words exactly as in data/ (his typos
  included). Never invent, round silently or paraphrase a quote. If you summarise, it's labelled as yours. Images and
  clips are the production's own files. Nothing about keys, Lati's email address or his health.
- **Time:** song time is the only clock; every frame a pure function of t and the data, no state between frames. An
  event at production time u appears at song time `B.song_at(u)`. Things enter on the beat grid where they can.
- **Inserts** from the main film: short (a beat to a bar), decoded with ffmpeg from the master or a take, placed where
  the record says that shot was made or approved, framed as a terminal would show them (a window, scanlines), not
  full-frame. Cache decoded frames under `media/<section>/cache/`.
- **Rendering**, one at a time (both tools wait for `media/render.lock`), from `/home/shegs/im-not-you-making-of`:
  - frames: `"/home/shegs/Im not you/media/cache/gfx-venv/bin/python" tools/film/check.py --at 50,51 --out media/<section>/check --only sec_<yours>`
  - a stretch: `"/home/shegs/Im not you/media/cache/gfx-venv/bin/python" tools/film/render.py --only sec_<yours> --from 44.7 --to 82.3 --out media/<section>/pass1.mp4`
  No trailing `&`, no `pkill`.
- **What you can claim:** a frame check is a frame check; motion and timing are Lati's to judge. Read your JPEGs.

If a hook asks you to call `mcp__ccd_session_mgmt__get_usage`, load it with ToolSearch and call it, then carry on.
End with a short report: what's on screen and when, what you checked and how, renders, questions for Kiln.
