# I'm Not You: the making-of

A second video for the song "I'm Not You": how the main film (repo `im-not-you-internal`) was made, drawn entirely in
code from the production's own record (commits, the spend ledger, Lati's notes, the sessions' model calls and
compactions, the agents' work), timed to the same song, with brief inserts from the main film.

Roles, as in film 1: Claude (Kiln, the local Claude Code session) directs and writes the code; Lati is the eyes and
ears, and his word decides. Started 12 Nov 2026 (decisions.md).

- `notes/treatment.md`: what the video is and how it's built.
- `data/`: the record, extracted (tools/data), privacy-filtered (keys and the email address out).
- `tools/film/`: the renderer and its sections.
- `media/`: renders and inserts (not in git).

## Rebuilding it

`python3 tools/data/extract.py` rebuilt `data/` from the production's sources (film 3's repo and Claude's session
transcript, neither public); `data/` is committed, so the video rebuilds from it alone, except for the pictures: the
inserts, plates and takes come from the main film's media (not in git). With them in place:

    python tools/film/render.py --tail 5 --size 1080     # Python 3, skia-python, numpy, opencv; ffmpeg

`data/session-lines.json` holds the two lines the video quotes from Claude's session transcript, so the quotes are
checked without it. Privacy: no keys, no email addresses (`data/privacy-scan.json`); everything else is the record
as it is, Lati's words included, with his yes (decisions.md, 12 Nov 2026).
