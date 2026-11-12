# STATUS: the making-of of *I'm Not You*

Claude (Kiln, local), 12 Nov 2026, 12:45. Kiln directs and codes; Lati checks (as film 1).

| | |
|---|---|
| Stage | **Public repo; release 12 Nov.** Pass 2 approved ("10/10"). **Master v1:** `media/render/making-of-master-1080-v1.mp4`, 1920x1080, 4229 frames, 1.1 GB (12 Nov, 13:02). |
| What | Film 3's record (1-12 Nov) drawn in code on the same song: the context gauge and its 6 compactions (9 Nov before the chorus drop, 11 Nov on the break, 12 Nov on "Me"), commits, spend, Lati's notes verbatim, the takes, the edit, the code drawing itself, the agents. `notes/treatment.md`. |
| Code | `tools/film/` (base.py Kiln's; sec_a_verse1, sec_b_chorus1, sec_c_bridge, sec_d_final by four agents, logs `notes/agents/`); `tools/data/` (extract.py, timeline_history.py) -> `data/` (privacy-filtered). |
| Render | `~/Im\ not\ you/media/cache/gfx-venv/bin/python tools/film/render.py --tail 5 [--size 1080]`, 4229 frames, ~5 min at 720. |

## Open
1. Release prep with the main film: each description links the other; end screens; shorts. Lati brings film 2's data.
2. Before the repo goes public: the session-derived checks (sec_b's s069 line, sec_c's "Me" line) read the local
   transcript; cache them into data/ so the public repo rebuilds without it. Lati's word for public.
