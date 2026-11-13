# Tools

Claude (Kiln, local), 1 Nov 2026. Only what film 3 needs first lives here. The rest stays in `~/checked-me/production/tools/`
until a stage calls for it: copy it then, and read its hard-coded film 2 paths and rules before trusting it.

Here now:

| Tool | Job | State |
|---|---|---|
| `listen/` | Song analysis: stems, word times, beat map, sections | Copied unchanged; imports checked from this path |
| `stemcheck.py` | Is this Suno stem really the locked take? | New; tested on both films' stems |
| `seedance.py` | Seedance 2.5 on OpenRouter, with the spending gate and ledger | Film 1's runner, plus `reference` clips and several images; never yet run past a refusal |
| `contact.py` | Contact sheets | Copied unchanged |

Bring when the stage starts:

| Stage | From `~/checked-me/production/tools/` |
|---|---|
| Design | `plate.py`, `repaint.py`, `grokkit.py` |
| Song | `clipaudio.py` (point `STEMS` at the locked take; prefer Suno's stem) |
| Board | `board/` (audit, sheet) |
| Clips | `video.py`, `nightclips.py`, `orvideo.py`, `beatfit.py`, `retime.py`, `lipsync_lag.py` |
| Edit | `shots.py`, `cutplan.py`, `roughcut.py`, `library.py`, `review/` (the player, `/library` and `/cut` with M notes are built: copy them, and start them before the first review) |
| Graphics | `gfx.py` and sections, `gfxrender.py`, `gfx_matte.py`, `gfx_wall.py` |
| Release | `export_public.py`, `shorts.py` |

Venvs are shared to save the small disk: `media/cache/listen-venv` and `listen-models` are symlinks (gitignored), and the
others are used in place, such as `~/checked-me/media/cache/gfx-venv`.

**This folder's path has spaces.** Quote it in every shell command, and in any tool that builds a command as a string.
Python's `Path` and argument lists are fine.
