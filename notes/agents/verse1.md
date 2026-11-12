# Agent log: verse1

Section A, verse 1 and the pre-chorus. Song time 0-44.69.


## 12 Nov, agent A (verse1)

**Read:** notes/agents.md, treatment.md, decisions.md, base.py, film3_gfx.py, data/README.md; notes.json, commits.json,
compactions.json for 1 Nov-9 Nov 17:28; film 3's board.json and its git history (read-only `git show`), picks.json,
look-test-1.md; looked at the images (contact sheets in `media/verse1/look/`: look tests, face sheets, ships, fleet
side views, designs, dataset, looktest-2, Lati's handwritten 9 Nov notes, rough-1).

**What the record holds for 0-44.69** (song times from `song_at`): 1-6 Nov quiet (Lati's opening message, the 4 Nov
compaction at 2.58); 7 Nov evening is dense (38 of his notes between 6.2 and 18.8; compactions at 11.14, 18.60);
8 Nov has a sleep gap (18.8-23.9) and an afternoon gap (24.8-29.1); 9 Nov: Flint's note 34.62, the draft-2 pages 36.21,
board v2 37.3, plates in rounds, picks 42.05 / 42.54 / 44.12, compaction 44.47.

**Design:** one terminal scrollback in the centre (x 300-1140, y 160-785; the summary line's spot at y ~810 stays
clear always). It prints, in order and on the beat nearest the record's time (later beat when two collide):
Lati's notes as `DAY DD MON HH:MM  LATI` + his words typing in (white while typed, then amber), a few Kiln replies in
clay, day lines for 2-9 Nov with that day's calls and commits counting live (the quiet days read 0), and the work as
images the way a terminal shows them: framed, dithered to the main film's 32-colour palette (film3_gfx.quantize),
scanlined, printed row by row, captioned with their real path. Batches print as grids; when Lati's picks land the
picked cells get an amber frame and the rest dim; rejections in red. At board v2 (37.50) the scrollback scrolls away
and the board fills the centre: 111 cells in time order, filled from board.json as it stood at each of film 3's
commits that day (git), plates bright, references dim; a small pane under it carries his last notes. From 44.30 the
centre fades out by 44.55, so the compaction (44.47) and the drop (44.69) land on an empty centre.
