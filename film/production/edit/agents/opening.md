# Agent log: opening

Section A, the opening and the bridge. Song time 0:00-0:43.92 (s001-s025). Section file: `production/tools/gfx/sec_*` (see README). Renders: `media/gfx/opening/`.


## 2026-11-12 · Pass 1 (graphics agent A, opening)

Graphics agent A ("opening"), for Kiln. Section file `production/tools/gfx/sec_a_opening.py`; render
`media/gfx/opening/opening-pass1.mp4` (0-43.92, 1054 frames, timeline saved 02:15:18). Frame checks in
`media/gfx/opening/check/`.

**What plays (F.cut()) and what each shot got.** I looked at every shot first (contact sheets, 4 frames a shot, and full
frames of each shot I drew on).

| Song | Shot | Line | Graphic | Layer |
|---|---|---|---|---|
| 0-8.83 | s001-s005 | intro | none: no board graphic, nothing in the picture asks | |
| 8.83-11.42 | s006 | intro | the title: "I'M NOT YOU" types itself in phosphor amber between cyan brackets on the 9.15 downbeat, holds the bar, collapses to a line into the cut. No credit, no AI label (Lati, 12 Nov) | over |
| 11.42-18.04 | s007, s008 | | none | |
| 18.04-20.21 | s009, s010 | 0 | a holo spec sheet beside the orb (left wall), carried over both shots of the line: STRUCTURE PREDICTION, a chain folding from "fold" to the end of "shape", FOLDING → PREDICTED, rows on the half-beats: AlphaFold2 · DeepMind; 200,000,000+ predicted; ~100,000 solved by experiment; Nobel, Chemistry 2024 | world |
| 20.21-21.29 | s011 | (1) | the second monitor on the left wakes on the 20.27 beat with a chart instead of its own text: VARIANTS SCORED, bars to 89% CLASSED / 11% UNCLEAR, OF 71 M POSSIBLE, 0.1% CONFIRMED BY EXPERTS | world |
| 21.29-28.0 | s012, s013, s014, s016 | 1, 2 | none (see "Left" below) | |
| 28.0-29.96 | s017 | 3 | the lightbox: a scan film (drawn), a box closes on the dense spot by the 28.57 beat, FLAGGED stamps on the 29.13 downbeat, "→ A RADIOLOGIST DECIDES" on 29.68; AI AS AN EXTRA READER, +0.7-1.6 cancers found per 1,000 | world, behind her head and hands |
| 29.96-31.75 | s027 | 4 | the head unit's schematic drafting itself: brackets and centrelines on 30.25, callouts on 30.82 and 31.41; VISOR · ONLINE in amber the frame the take's visor lights (measured in the picture) | world |
| 31.75-35.96 | s021 | 4, 5 | on the white screen, in its own dark-blue ink, behind her head: line 4 at top left, SPEECH NEUROPROSTHESIS, typing at the pace of the vocal stem (the voice becoming words): ATTEMPTED SPEECH → WORDS / MEDIAN 78 WORDS / MIN / MEDIAN WORD ERROR 25%. Line 5 at top right from the 33.06 beat: SPERM WHALE CODAS, nearly 9,000 recorded, three click rows on the beats (CODA, RUBATO, ORNAMENT with its extra click in red), MEANING: UNKNOWN on 35.29 | world, masked |
| 35.96-37.29 | s020 | 6 | none (see "Left") | |
| 37.29-39.54 | s023 | 6 | Kiln's approved tags, unchanged | world |
| 39.54-43.92 | s025, s029, s026, s029, s025 | 7 | LOAD: a 24-segment gauge in the dark aisle, holding still across the five server shots, a step up on each beat (34 → 46 → 58 → 71 %), to 100 % on "feed" (41.36), then red, MAX blinking on eighths to the cut | over |

**Sources** (forms.md pass 1, "shown as" respected; every drawn picture says ILLUSTRATIVE in micro-type):
- Line 0: KVA press release 9 Oct 2024 (Nobel, "protein structure prediction"); Nature 15 Jul 2021 ("around 100,000"
  solved); DeepMind 28 Jul 2022 ("over 200 million", predicted). Shown as another system, and as PREDICTED. The fold is
  drawn.
- Line 1: DeepMind 19 Sep 2023 ("89% of all 71 million possible missense variants"; "only 0.1% have been confirmed by
  human experts"). It only scores; nothing about patching.
- Line 3: Nature Medicine 16 Nov 2023 (0.7-1.6 additional cancers per 1,000; a human reader decided recall). The
  stamp's last word is the radiologist's, per the limits column. The film is drawn.
- Line 4: Ann Johnson, Nature 23 Aug 2023 (median 78 words/min, median word error 25%; Berkeley calls it "AI-powered").
  Not Harrell (his sources don't say AI). "Draft the brief" has no case, so nothing claims it.
- Line 5: Project CETI 7 May 2024 (nearly 9,000 codas; rubato and ornamentation; "the communicative function of many
  codas remains unknown"). The clicks are drawn.

**Tracking (film 2's rule).** `motion()`: each frame of a take is matched to the take's first frame in the cut (ORB,
RANSAC similarity), never to its neighbour, with the people masked out; then smoothed over 5 frames. For s009-s011 the
match is limited to the surface's own neighbourhood (`ONLY`): s011 is a dolly, and a whole-frame fit put the chart
~15 units off the monitor. Measured, 90th-percentile inlier error per frame, worst frame: s009 2.7, s010 2.0, s011 2.4,
s017 2.6, s021 2.9, s027 2.1 units (of 1920). s011 checked against the monitor itself (its white glow's centroid, frames
0-14 before it wakes): a constant ~3-unit offset from my hand-read corners, which I then corrected; drift on top of it
under 2.5 units. The moves are small except s011 (zoom 6 %) and s009 (3 %). Occlusion: the s017 and s021 graphics are
masked each frame by the screen's own brightness, so her hair, head and gloves stay in front. In s021 her head swings
right to x 1358 at most (measured over the take): the codas panel starts at 1376.

**Checked how:** frames from check.py at ~30 times, and 10 frames read back from the render itself
(10.0, 19.0, 21.0, 29.5, 31.6, 33.0, 35.6, 38.2, 40.5, 41.6). That is a frame check: motion, typing pace and how long
anything stays readable are Lati's to judge. Frames are 1280x720; the smallest text (micro-type, the chart on s011's
monitor at ~15 units) is small at that size.

**Left, and why.**
- **Line 2 ("Screen a million molecules", 24.32-26.92)** has no graphic: the board's counter was on s015, which isn't in
  the cut; s014 (hangar) and s016 (Vera at the orb) have no board graphic and no screen that asks for one. If Kiln wants
  the line covered: the GNoME counter (2.2 million predicted crystals, 380,000 most stable, 736 made by outside labs;
  "crystals, not molecules") on the orb holo in s016, the same kind of panel as s009. I didn't build it unasked.
- **s020 (35.96-37.29), the brief drafting itself:** not built. In the cut s020 plays under line 6 ("Ask me anything"),
  not line 4; "Draft the brief" has no sourced case (forms.md: "needs a case or stays unillustrated"); and the map
  projection sits in the bottom band, where the lyric line is. A prompt field there (the board's s024 idea) would set
  the line's own words a second time. The s023 tags follow 1.3 s later.
- **s027's schematic is under line 4, not line 7** in the cut (the board had it for "every shape I wear"). It carries no
  fact; I built it because the board asks and the visor lighting is the take's own beat, as the fiction's spec sheet
  drafting itself (a loose echo of "draft"). It is the first thing to drop if Kiln or Lati wants one graphic per line
  strictly: line 4 is carried by s021.
- **s011's chart plays 0.2 s before line 1** ("Map the genome", 21.42) because that's where the screens wake in the
  cut; the line itself plays over s012/s013, which have no screens for it.
- **Ink colour on the white screen (s021):** the screen's own dark blue (as its waveform), not amber: amber doesn't read
  on white. The ORNAMENT click is red. Kiln to say if the palette rule should win.

**"feed" as an impact frame: proposed against.** IMPACTS stays empty. The racks' own light surges to white at 41.3-42.1
right on "feed" and the LOAD gauge maxes there: a starburst would fight both. It's the pre-chorus, not a hook ("Me" and
"I'm not you" are), so keeping impacts rare argues for leaving it. And an impact sets the sung word large in the
picture, which sits uneasily with Lati's "lyrics … bottom line only" (12 Nov): a question for Kiln on the module itself.

**No CUTS** inside the section: no terminal or pixel moment here that a CRT roll would earn.

**Helpers in my file Kiln may lift into the base:** `motion()`/`follow()` (per-frame camera measurement against the
take's first frame, local region, smoothing), `masked()` + `screen_mask()` (draw on a screen behind the picture's own
foreground), `voiced()` (typing at the pace of the vocal stem), `eighths()`, `word_t()` (a word's snapped onset by line).

**Questions for Kiln.**
1. Line 2: build the GNoME counter on s016's orb, or leave the line with only the karaoke?
2. s027's schematic: keep (board) or drop (one graphic per line; it carries no fact)?
3. s021's dark-blue ink on the white screen instead of amber: OK?
4. Impact frames and "lyrics only in the bottom line": does Lati's rule cover the impact module's word?
5. The title sits at y 330-530 over the fleet with a 50 % black panel; Lati may want it smaller or lower.

## 2026-11-12 · Pass 2: Lati's notes on s017 and the LOAD gauge (graphics agent A, opening)

Lati's notes, relayed by Kiln (verbatim in decisions.md, "Graphics pass 1: Lati's notes, part 1"): s017 "insert on
screen is not matching the perspective of monitor in front of her"; the servers' "load meter is front and centre,
blocking the screen and diminishing the impact of motion clips where racks light up with "feed". It would need to be
either much more subtle on top or bottom bevel, or dropped altogether." Kiln's answers to my questions: line 2 stays
karaoke-only; keep s027's schematic; dark-blue ink on s021 is fine; no impact frames; the title as it is.

**s017, the film on the lightbox's plane.** The lightbox is angled away to the right (its top edge falls 0.51 px per px,
its bottom rises 0.056; they meet at about x 1325, y 476 of 1280x720). Its four corners come from its edges in the
take's first frame, fitted to the glow's boundary: left, right and top by a RANSAC line fit (inliers within 1.7, 0.5 and
0.9 px); the bottom, where the glass meets the sill, by eye, because the sill is as bright as the glass. The top-left
corner is above the frame. The corners ride the take's measured camera move (each frame against the first, never
chained). The film is drawn flat in its own units and warped onto the plane with a homography (`film_homography()`).
It is transmissive: the box's own light times the film, so it takes the box's brightness, its cyan tint and its sweep.
The marks on it (box, facts, FLAGGED) are lit by the same light. Her hair and gloves stay in front (the brightness
mask, as before).
Measured: in each frame I found the visible left, top and right edges of the glow afresh and took the median distance
from the carried plane's edges. Left at most 2.9 units, right at most 1.1, top 0.3-1.2 in 44 of 47 frames. In frames
4-6 (28.17-28.25) the top reads 6-21.5 units: the box's own light beam lights the bevel above the edge there, so the
edge can't be measured (I checked the frame), and the camera move measured over those frames is under 1 unit. The bottom
edge I can't measure per frame (no contrast with the sill); it rests on the same camera fit.

**The LOAD readout, now a slim strip along the top edge** (y 44-53 of 1080, x 330-1590): 48 small segments, a small
LOAD label and percentage, cyan at 42 % opacity, a step on each beat, full and red on "feed" with one swell that fades
in 0.4 s, then MAX, quiet to the cut. No box, nothing in the aisle; only a faint dark gradient behind the strip. I kept
it rather than dropping it: in the frames (39.8, 40.9, 41.5, 42.2, 41.8 from the render) it sits on the dark ceiling and
the racks' surge has the centre. Whether it's quiet enough in motion is Lati's call; dropping it is one line in `over()`.

Render: `media/gfx/opening/opening-pass2.mp4` (0-43.92, 1054 frames). Frame checks: `media/gfx/opening/check2/`.
Seam at 43.92 changes: the strip ends with a 0.06 s fade into the cut, not the centre gauge.

## 2026-11-12 · Pass 3: s017, the film fills the lightbox (graphics agent A, opening)

Lati on pass 2 (verbatim in decisions.md): "scan does not fill the screen, it read as ctrlz image on screen"; then, to
Kiln's suggestion, "Lets try your suggestion for s017": the film fills the whole lightbox, backlit, as a film hangs on
a real one.

What changed (only s017; `film_transmission()`, `film_overlay()`, `film_homography()`):
- The film is the whole plane already fitted in pass 2 (same four corners, same camera move): no card, no border, no
  inset. Where the top-left corner is above the frame, it runs off the top.
- Backlit: the picture is the box's own light times the film, so it keeps the cyan tint and the passing beam. Grey
  range rather than a black card: the exposed background lets ~25-31 % through, tissue 28-98 %. As on a real film,
  denser tissue is lighter and the small dense spot is the brightest thing (Kiln's note had it the other way; I went
  with how film works). The breast lies against the chest wall at the right edge, partly behind her head. Drawn:
  SCAN: ILLUSTRATIVE on it.
- The markings are on the film, in its plane: R MLO top left; the box closing from the breast to the spot (28.02-28.57);
  FLAGGED stamped on 29.13; the facts bottom left on the near side (AI AS AN EXTRA READER, +0.7-1.6 cancers found per
  1,000, Mia · Nature Medicine 16 Nov 2023, SCAN: ILLUSTRATIVE), clear of her head and gloves and above the lyric band.
- "→ A RADIOLOGIST DECIDES" now comes in with the stamp (29.19, fully on by 29.29) under it, instead of on 29.68:
  about 0.65 s on screen before the fade at the cut, against 0.28 s before. Kept, not dropped.
- Her hair and gloves stay in front (the brightness mask, unchanged).

Edge error (same method as pass 2, unchanged plane): visible edges of the glow found afresh in each frame, median
distance to the plane's edges: left at most 2.9 units, right at most 1.1, top 0.3-1.2 in 44 of 47 frames; frames 4-6
unmeasurable (the box's beam lights the bevel above the top edge). The bottom edge has no contrast with the sill and
isn't measured per frame.

Checked: check.py at 28.05, 28.4, 28.8, 29.2, 29.5, 29.9 (PNG, crops of the box at render size), and 28.6, 29.4, 29.8
read back from the render. Render: `media/gfx/opening/opening-pass3.mp4` (0-43.92, 1054 frames). Frame checks:
`media/gfx/opening/check3/`.
