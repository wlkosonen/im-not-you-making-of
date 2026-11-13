# STATUS: the making-of of *I'm Not You*

Claude (Kiln, local), 13 Nov 2026. Kiln directs and codes; Lati checks (as film 1).

| | |
|---|---|
| Stage | **Released 12 Nov 2026** on YouTube (before the film, so the film sits newest). Repo public. Master `media/render/making-of-master-1080-v1.mp4`; its pure black is 3.6 s (an end screen would sit over the last line). |
| What | Film 3's record (1-12 Nov) drawn in code on the same song: the context gauge and its 6 compactions (9 Nov before the chorus drop, 11 Nov on the break, 12 Nov on "Me"), commits, spend, Lati's notes verbatim, the takes, the edit, the code drawing itself, the agents. `notes/treatment.md`. |
| Code | `tools/film/` (base.py Kiln's; sec_a_verse1, sec_b_chorus1, sec_c_bridge, sec_d_final by four agents, logs `notes/agents/`); `tools/data/` (extract.py, timeline_history.py) -> `data/` (privacy-filtered). |
| Render | `~/Im\ not\ you/media/cache/gfx-venv/bin/python tools/film/render.py --tail 5 [--size 1080]`, 4229 frames, ~5 min at 720. |

## Open
1. Nothing pending. Lessons for a next one in `~/workshop/release.md`.
