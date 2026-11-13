# Graphics agents for *I'm Not You*: how you work

Claude (Kiln, local), 12 Nov 2026, from film 2's rules (`~/checked-me/production/edit/agents/README.md`). You're one
of four agents building the graphics of film 3, a section each. Kiln is your mediator and reviewer; Lati (he/him) is
the producer, and his eye on the renders is the check. He approved the base's look on a test set on 12 Nov: your job
is a first pass of your whole section that holds up beside it.

## Read first

1. `production/notes/graphics-plan.md`: the whole plan with Lati's answers. Then `production/decisions.md` from
   "2026-11-12 · The graphics plan restated" to the end.
2. `production/tools/gfx/base.py`, all of it: how a frame is built, MODULES, the palette, the song clock (`BEATS`,
   `DOWNS`, `beat_no`, `pulse`, `ease`), Lati's cut (`cut`, `spans`, `shot_at`, `src_t`), the vocal stem
   (`vocal_wave`, `vocal_bands`), the HUD kit (`brackets`, `reticle`, `hud_text`, `tag`, `glow_draw`, `stroke`), the
   pixel/CRT module (`quantize`, `crt`, `psf`, `stamp`), transitions (`CUTS`, `transition`), `IMPACTS`.
3. The approved test pieces, the bar to match, each already in a section file: `sec_a_opening.py` (s023's tags),
   `sec_b_battles.py` (s089's HUD), `sec_c_verse2.py` (s050's side instruments), `sec_d_end.py` (the pixel zoom).
   **Leave them as they are** unless Kiln sends you a note on them.
4. `production/board/board.json`: each shot's `action`, `graphic`, `devices`, `type`, `lines`. `board/design.md`
   ("One graphic per line"). The board is the plan of 9-11 Nov; Lati's cut has moved on: what plays is
   `F.cut()` (from `edit/timeline.json`; never edit that file). **Always look at the picture before designing on it**:
   `check.py` frames, or `ffmpeg -ss <t> -i <take> -frames:v 1 x.jpg`, and read the JPEGs.
5. The facts for the line graphics: `production/research/forms.md` (sourced, with what NOT to claim),
   `research/graphics-only-9-nov.md`, `research/references-7-nov.md` §5. The song's words:
   `media/song/analysis/parempi/words-snapped.json` (`F.WORDS`, `F.LINES`).

## The rules

- **Your files only:** `production/tools/gfx/sec_<yours>.py`, `media/gfx/<section>/`, your log
  `production/edit/agents/<section>.md`, and your side of your rows in `production/edit/seams.md`. Helpers you need go
  in your own file; note them in your log and Kiln may lift them into the base.
- **Not yours:** `base.py`, `render.py`, `check.py`, `timeline.json`, `takes.json`, the board, `decisions.md`, other
  sections' files. Ask Kiln in your log.
- **No git** (Kiln commits). No GPU, no ComfyUI, no paid services, no downloads, no network. If a shot needs new
  footage, say so in your log and design for the picture that exists.
- **Your RANGES** cover only your section's times (below). Dispatch per shot inside `world`/`over` with `F.shot_at(t)`
  or `F.spans(shot)`, never with hard-coded times where the cut decides: Lati may still trim.
- **Lyrics only in the bottom line** (Lati, 12 Nov: "when it comes to lyrics, that should stay as bottom line only").
  The base draws it; you never set the song's words anywhere else. Keep the bottom ~170 units clear for it.
- **The film's own monitors, consoles and HUDs carry the insert graphics** (Lati, 12 Nov). A graphic in the picture
  (on a screen, a projection, a holo) goes in `world()` and takes the beat kick with it; a HUD on glass or a readout
  holding still goes in `over()`.
- **"The line"** (a trace through the film) is out, an optional module that's off (Lati, 12 Nov). Board entries that
  say "plot: the line" get no line; propose something else in your log if the shot wants a graphic.
- **Quiet shots carry no UI:** s039 (sakura), s075 ("Me"), s094, s095q (the calm cockpit), s109, s108. The karaoke line
  alone. Locked shots (s050, s067, s075) are finished pictures: nothing drawn on them.
- **Colour:** amber phosphor for text, cyan for the fleet's HUDs and the holo, red for the swarm, the bunker and
  warnings, clay only for Claude's side (her, Earth's marker), green only for a pass. 80s anime UI: vector lines,
  dot-matrix, CRT glow, thin brackets; the pixel/CRT module for terminal moments.
- **Honesty:** on-screen text is real: sourced facts (forms.md, with its "not this" column respected), this repo, or
  marked `ILLUSTRATIVE` in micro-type. Words in HUDs that are the fiction's own (LOCK, TRACK, a heading) are fine.
  No real brands' marks or logos. ABLITERATED and HERETIC are the swarm's words (s023), the fleet untagged.
- **Timing:** graphics enter on the grid (beats and downbeats), song time is the only clock: every graphic is a pure
  function of t and the frame, no state between frames.
- **Tracked surfaces** (film 2's lesson, Lati caught drift that frame checks had passed): never chain optical flow.
  Find the thing afresh in each frame of the take (`F.IMG` while `world()`/`over()` run, or decode the take as
  s023 does), then link and smooth over the whole take if needed (`tracks()` in `sec_a_opening.py`: Lati asked for
  tags to "follow the rising light more tightly" after per-frame tags flickered). Report the worst-case error you
  measured.
- **Rendering** (one at a time across all agents; both tools wait for `media/gfx/render.lock` themselves; keep runs short):
  - frames: `media/cache/gfx-venv/bin/python production/tools/gfx/check.py --at 46.2,46.5 --out media/gfx/<section>/check --only sec_<yours>`
  - a stretch: `media/cache/gfx-venv/bin/python production/tools/edit/render.py --gfx --only sec_<yours> --from 43.9 --to 57 --out media/gfx/<section>/<name>.mp4`
  Run from `"~/Im not you"` with absolute paths (the folder name has spaces: quote it). No trailing `&`, no `pkill`.
- **Impact frames** (switchable, rare): put candidates in your `IMPACTS = [(t, "WORD")]` and say why in your log.
- **Transitions:** `CUTS = {cut_time: ("crt_roll" | "mosaic" | "flash", frames each side)}` for cuts inside your
  section, where they earn it (the CRT roll into and out of terminal and pixel moments). Seams between sections:
  write your cell in `seams.md`; Kiln sets the transition.
- **What you can claim:** a frame check is a frame check. Say what you looked at. Motion and timing are Lati's to
  judge: never write that something "works" or "feels right". Read your JPEGs; don't assume.

If a hook asks you to call `mcp__ccd_session_mgmt__get_usage`, load it with ToolSearch (`select:mcp__ccd_session_mgmt__get_usage`) and call it, then carry on.

When you finish, end with a short report: shots done, shots left and why, what you checked and how, renders made,
questions for Kiln.
