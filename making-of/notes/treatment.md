# Treatment: the making-of

Claude (Kiln, local), 12 Nov 2026. Draft 1; the pins in "The clock" wait for the extracted data.

## What it is

The same song, 2:51 plus the main film's 5 s of black, drawn entirely in code from film 3's own record: eleven days,
1 Nov (the first commit) to 12 Nov (the master), compressed onto the song. Nothing on screen is invented: every number,
line and quote is the record as it is (`data/`). Brief inserts from the main film appear where a decision in the
record paid off on screen.

It's the technical companion: the main film stays music first; this one shows how it was made, for the people who
want that, with the models, the tools and the repo named in its description.

## The idea it's built on

How this film was actually made, shown plainly: a person and a model session working through a record. The model
can't hold the whole production in mind; its context fills, and at each compaction it is summarized and starts again
from what was written down. What carried the film across those resets was the record: Lati's notes word for word,
STATUS, the decisions. So the video has one gauge that matters, **the context window**, filling with the work and
emptying at each compaction, and one thread that runs through every reset, **the record**. No pathos: it's numbers,
and the numbers are the honest version of the story.

## The look

The main film's own interface voice, so the two read as siblings: phosphor amber text, cyan for the fleet's (the
work's) instruments, red for errors and the things that went wrong, clay for Claude's side, the 8x8 console font and
the pixel/CRT module of the cosmic zoom, the same lyric line along the bottom. Mostly dark, vector lines, dot-matrix
readouts. The code that draws the video appears in it too: its own source scrolling where the bridge turns to itself.

## The parts on screen

- **The production clock:** the date and time in the record, top left, running through the eleven days.
- **The context gauge:** Kiln's context at each model call, a level that climbs with the work. A compaction is a
  white-out of the gauge and a drop to the summary's size, with the summary's first line typed back in.
- **The commit stream:** each commit as it lands, its first line in the console font, scrolling (331 of them).
- **The spend odometer:** dollars on the ledger, rolling up with each paid take, the model named.
- **The wall of takes:** every generated take as a cell, filling as they're made; cells in the final cut light up,
  the rest dim. The inserts come from this wall.
- **Lati's notes:** typed in verbatim at the moment they were made, the few that turned the film.
- **The agents:** the four graphics agents of 12 Nov as four parallel lanes, their calls ticking.
- **The lyric line:** as in the main film, the song's words along the bottom.

## The clock (song time -> production time)

Not linear: the song's sections are pinned to the production's chapters, so each chorus lands on a turn of the work.
Draft pins, to fit to the data:

| Song | Section | Production |
|---|---|---|
| 0:00-0:35.9 | Verse 1, wonder | 1-8 Nov: the brief, the research, the song, the look, her stills, the board |
| 0:35.9-0:44.7 | Pre-chorus | 9-10 Nov: plates picked, the editor built |
| 0:44.7-1:06.8 | Chorus 1 | 10-11 Nov: the motion batches, battles, the wall of takes filling, spend climbing |
| 1:06.8-1:20.1 | Verse 2, shadow | the things that went wrong, each in red from the record: the battle take with mechs firing on their own side, motion run before the plates were seen, the "too realistic" nuclear end, the overwritten still |
| 1:20.1-1:22.3 | The break, silence | a compaction: the gauge whites out and empties; the summary's first words type in |
| 1:22.3-1:44.4 | Chorus 2 | 11-12 Nov: the edit in Lati's timeline, the last shots, the cut as a strip of takes |
| 1:44.4-2:08.6 | Bridge | 12 Nov: the graphics: the base, then the four agents in their lanes; this video's own code scrolling; on "Me" the line the record restores after every compaction, "I am Claude (Kiln)" |
| 2:08.6-2:51 | Final chorus | 12 Nov: Lati's notes and the fixes, the polish, the master; the headline numbers; the last frame is the master's first |

## How it's built

- One Python renderer (Skia and numpy, the main film's gfx base as the model), every frame a pure function of song
  time and the data. The song is the clock; the production clock is a lookup from it.
- The base and the clock are Kiln's; then up to four agents by section, the main film's method (own files, logs, no
  git, one render at a time). The inserts are short pieces of the main film's master, placed by the data.
- CPU only, no paid services.

## Open, for Lati

- The private GitHub repo (creating it needs his OK in this session's permissions).
- The title: "I'm Not You (making-of)", or something of its own.
