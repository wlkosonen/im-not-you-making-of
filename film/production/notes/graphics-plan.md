# Graphics: the plan for film 3 (proposal for Lati)

Claude (Kiln, local), 12 Nov 2026. Restates everything decided about the graphics layer, how it gets built (the agent
method of film 2, `~/checked-me/production/notes/graphics-split.md`), and what I'd add. Lati's answers of 12 Nov are
folded in below (decisions.md); step 1 is on. Sources: `board/design.md`, each shot's `graphic` in `board/board.json`, decisions.md (7-12 Nov),
`research/references-7-nov.md` §5, `research/graphics-only-9-nov.md`, film 2's seams and agent rules.

## What the graphics are for

The motion carries the spectacle; the graphics carry the meaning (Lati, 10 Nov: "while high-speed, eye-candy,
exhilarating battleshots are for audience, I was also thinking how to highlight the message and the meaning").

Decided:
1. **Each lyric line gets one graphic, and it is a real object of the film's world** in the 80s anime UI style: bridge
   consoles, vector CRTs, dot-matrix readouts, cockpit HUDs, punched-tape, with the **sourced facts** as its numbers
   (research pass 1). Lati, 8 Nov: yes.
2. **Lyrics only in the bottom line** (Lati, 12 Nov, superseding 8 Nov's single words in objects): "when it comes to
   lyrics, that should stay as bottom line only". The film's own monitors, consoles and HUDs carry the insert graphics.
3. **The break is an interface refusing,** true to how refusals work (8 Nov: yes; built: s050 red lens).
4. **No persistent counter** across the film (Lati, 8 Nov). A counter inside one line's graphic is fine.
5. **The karaoke line:** the sung line typing itself along the bottom as a CRT text line, at the pace it's sung.
6. **The line** (the design's through-line) is **out, kept as an optional module** (Lati, 12 Nov: "lets leave that
   out, with an option to add it"). What it would be: one trace drawn from the vocal stem, clay orange in verse 1, the launch
   signal on "feed", the targeting line that ties two mechs in the choruses, red on the bunker terminals, the
   oscillator at the break, the constellation lines, her face in ASCII. Exact to the voice because it is the voice.
7. **Radar tags on the swarm only:** ABLITERATED and HERETIC on s023, the fleet untagged (Lati, 10 Nov).
8. **Quiet shots carry no UI:** s039 (sakura), the calm cockpit at 2:21, the end. The karaoke line alone, if anything.
9. **The cosmic zoom, 2:31.83-2:43.71, in code, in a late-80s pixel and CRT look, no monitor frame** (Lati, 12 Nov):
   320x180 rendered hard, 16-32 colours, Bayer dither on the atmosphere and the galaxy's glow, scanlines and phosphor
   glow over the whole frame; out from Earth to the solar system to the galaxy, then back in, in steps on the beat.
10. **Already locked:** s050 the red lens, s067 the terminal faces, s075 "Me". s050 still needs fill for its empty black
   side areas (Lati, 12 Nov).

## The line graphics, by chapter (from the board, to update against Lati's cut)

| Chapter | Song | Graphics |
|---|---|---|
| Hyperspace, arrival | 0:00-0:18 | s006 the title in the bridge UI style |
| The bridge, verse 1 | 0:18-0:36 | a sourced case per line: spec sheet (protein folding, s009), chart (variants scored, s011), counter (molecules screened, s015), stamp FLAGGED (s017), the brief drafting itself (s020), a voice becoming words (s021), the vocal as soundwaves (s022) |
| Command centre | 0:36-0:40 | s023 radar: the swarm's signatures rise, tagged; s024 "ask me anything" in a prompt field |
| Hangar, servers | 0:40-0:44 | s027 mech schematics; s028 LOAD maxing out on "feed" |
| Battle 1 | 0:44-0:57 | HUD lock, silhouettes match (s030/s033); the line between them (s034, s036) |
| Verse 2, the bunker | 1:07-1:18 | a phishing mail typing itself (s043), voice match gauge (s044), agents active / calibrating (s045, the face rebuilt pixel by pixel), a profile (s046), a training curve (s049) |
| The break | 1:17-1:21 | the cursor in the black under "act surprised I'm here"; s050 locked |
| Chorus 2 | 1:21-1:34 | HUD brackets multiplying (s051); the line (s055) |
| Constellation | 1:34-1:37 | the line draws the constellation (s060) |
| Bridge, "Me" | 1:45-1:58 | s067, s075 locked; launch keys and silos |
| Final chorus, pilots | 2:08-2:21 | cockpit HUDs: lock, damage warnings, comms (s083-s092); the line (s087) |
| Calm, missile, zoom | 2:21-2:44 | the karaoke line only; the missile; the pixel zoom |
| The end | 2:44-2:53 | none: the blast, the aurora, Earth alone; then 5 s black for the end screens |

## The finishing (from film 2, with its numbers)

- **Zoom pulse at each change of place:** ~4 % peak, ~0.07 s each way, through the cut; cuts to black stay plain. The
  candidates in Lati's cut: into the pit (0:18.04), the command centre (0:35.96), the servers (0:39.54), the launch
  (0:43.92), the sakura (0:56.96), the bunker (1:06.79), the chorus battle (1:21.17), the constellation (1:34.33), the
  city (1:37.12), the terminal (1:45.00), the keys (1:49.88), "Me" (1:55.33), battle 3 (1:56.79), the pilots (2:08.54),
  the calm cockpit (2:21.05), the missile (2:26.08), the zoom (2:31.83), the sakura (2:43.71), the end (2:48.17).
  Not between the quick cuts inside a chapter.
- **The beat kick:** 1.2 % on beats 1 and 3, in the choruses and battles only.
- **Graphic transitions at a few seams:** flash, whip, slide, mosaic peel, and new for this film a **CRT roll** (the
  picture rolls and tears like a vertical-hold slip) into and out of the terminal and pixel moments. A seams note per
  boundary (`edit/seams.md`), as in film 2.
- **Words on their onsets:** the aligner's word times run late (median 0.05 s, a quarter 0.17 s+); each word is snapped
  to its measured onset in the vocal stem before the karaoke line or any lyric word uses it.

## What I'd add (Kiln)

1. **A light unifying grade and grain pass** (Lati: yes) over the whole cut: the takes come from Grok, Seedance 2.0 and 2.5, and
   2.5's brightest flashes wash cockpits gold. One gentle grade per chapter, a shared film grain and a touch of gate
   weave make them one film. Small, global, last.
2. **Impact frames, used three or four times, as a module that switches off** (Lati, 12 Nov: yes, "with option to
   switch that off"): a two-frame starburst behind a single hook word, the way "Drop the
   Prompt" uses its hook. Candidates: "Me" (1:55.6), "feed" (0:41.36), "I'm not you" at the break's end. Rare, so it
   lands.
3. **Her face being taken, verse 2** (Lati: yes): the three balcony flashes at 1:06.79-1:07.50 corrupt one step more each
   (scanline tear, colour shift, red cast), paying off on "fake the face" and the wall of faces (s046). Agreed in
   review on 11 Nov; listed here so it isn't lost.
4. ~~The credit and the AI label in the end black~~: **out of the picture** (Lati, 12 Nov: "I wouldnt want it to be in
   the video itself"). They go in the description and, if needed, a pinned comment, as for films 1 and 2.
5. **The render from Lati's timeline:** a compositor that builds the cut from `edit/timeline.json` (tracks, in-points,
   speeds, stills) at 24 fps, so the graphics sit on exactly what he edited, and the master is one command: cut +
   graphics + finishing + the song + 5 s of black.

## How it gets built (film 2's method)

1. **The base, Kiln alone:** `production/tools/gfx.py` for film 3 from film 2's: the palette (the 80s UI: amber,
   cyan, clay for the line, red for the bunker), the type voices (dot-matrix, vector CRT, stencil), the beat grid
   (`snap`, `on`, `pulse`), motion primitives, the karaoke line, a **HUD kit** (reticles, brackets, lock tones drawn
   as rings, warning tags), the transition library plus the CRT roll, the **pixel/CRT module** (downscale, palette,
   dither, scanlines, glow) for the zoom and the terminal moments, and the compositor from (5) above.
2. **One test, for Lati's eye:** s023's radar with its tags, one cockpit HUD (s089), the karaoke line over one chorus,
   and ten seconds of the pixel zoom. His yes starts the agents.
3. **Four agents, a section each,** in the same checkout, each owning only `production/tools/gfx_<section>.py`,
   `media/gfx/<section>/` and its log `production/edit/agents/<section>.md`:
   - **A, Opening and the bridge** (0:00-0:44): the title, verse 1's sourced cases, the radar, the hangar's gauges.
   - **B, Battles and pilots** (0:44-0:57, 1:21-1:34, 1:56-2:21): HUD locks, brackets, the line between mechs, the
     cockpit HUDs, the beat kick.
   - **C, Verse 2 to "Me"** (1:06-1:56): the bunker terminals, her corrupted flashes, the cursor in the black, the
     constellation line, the keys and silos.
   - **D, The zoom and the end** (2:21-2:58): the calm cockpit (karaoke only), the missile, the pixel zoom, the end.
   The karaoke line and the finishing (pulses, kick, grade) stay in the base, one system for the whole film.
4. **Rules carried over from film 2** (`~/checked-me/production/edit/agents/README.md`): no git for agents (Kiln
   commits); no GPU, no paid services; one CPU render at a time through a lock file; every graphic a pure function of
   song time; text on screen is real (the song's words, sourced facts, this repo) or marked illustrative; no real
   brands' marks; **tracked surfaces never chain optical flow** (film 2's drift lesson), each frame measured afresh; a
   frame check is reported as a frame check, and motion and timing are Lati's to judge on `/cut`.
5. **Reviews:** Lati marks with M on `/cut` or `/edit`; Kiln triages and sends each note to the section's agent.

## Estimate

No money: CPU and the Max plan. Film 2's anchor: the base and test ~5-10 % of a 5-hour window, each agent's first pass
5-10 %, review rounds 10-20 %; total roughly 40-70 % of a window spread over sessions, 7-10 % of a week. Film 3 has
more HUD work and the pixel zoom, so I'd expect the top of that range.
