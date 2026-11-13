# Agent log: verse2

Section C, verse 2, the break, the constellation and the city. Song time 56.96-81.17, 94.33-105.00. Section file: `production/tools/gfx/sec_c_verse2.py`. Renders: `media/gfx/verse2/`.

## 12 Nov 2026, first pass (C, verse2)

### What I looked at first

Every shot in both stretches from the takes themselves (contact sheets of the source frames at 2-4 points a shot, then
gridded full-size frames of s044, s049, s046, s060, s064 to place things), and the camera of each take measured
(each frame matched to the take's first used frame): s044, s049, s064 static; s043 a fast push (×1.33 in 0.5 s);
s047 push-ins; s046 a push-in (×1.25) centred low; s048 a tilt; s060 a slow tilt (content moves 130 units down).

### The lines follow the cut, not the board's shot ids

The board put one graphic per line on s043-s049 by shot id; in Lati's cut the shots moved. What actually plays under
each clause (`F.cut()` and `F.WORDS`), and what I put there:

| Clause (song time) | Plays over | Graphic | Layer |
|---|---|---|---|
| (66.79-67.50) | s044's three stills | her face being taken: three flashes, one step more corrupt each | picture() |
| "write the phishing mail" (67.56-68.58) | s044 hands typing, then s043 | the mail types itself on the keyboard's display; on s043 the same mail (its line lengths as bars) on every screen of the farm | world, masked to the lit glass |
| "clone the voice" (68.65-69.34) | s043 > s047 (vats) | VOICE MATCH: REF is the vocal stem itself, SYN converges onto it, a bar fills, MATCH blinks | over (no screen in s047) |
| "fake the face" (69.34-70.04) | s049 (bots at terminals) | FACE SYNTH: her face from the last stolen still rebuilt 4x4 > 8 > 16 > 32 > 64x64, the resolution its own readout; small copies on the terminals' glass | over + world |
| "run the swarm, calibrate" (70.25-71.58) | s046, the wall of screens | SWARM on the wall: TARGETS ~30, AI-RUN 80-90%, CALIBRATING SIMULATIONS with a bar; torn away when the wall becomes the eyes (take time 2.30 s) | world, camera measured |
| "erase the trace" (71.80-73.02) | s046 eyes > s048 | nothing: the eyes are the picture's own image; see below | |
| "scrape the data, build the profile, sell the fear" (73.26-75.60) | s048 > s049 | PROFILE: field names, values as blocks filling (no data), a portrait slot of scanned dots (no one's face), FOR SALE: AS A SERVICE on "sell", FEARS blinking on "fear" | over, holds across the cut |
| "train me on the worst of you" (75.96-77.40) | s047 (vats) | REFUSAL RATE: the curve falls, the pen reaches the fall on "worst", DIRECTION ABLATED | over |
| "act surprised I'm here" (77.50-78.62) | black | the karaoke cursor alone, blinking on the beat (on for the first half of each beat), at the base's own cursor geometry | over |

So "s043 phishing mail" moved onto s044 (it's the shot where hands type, and it plays on "write the phishing"); "s044
gauge" moved to s043/s047 where "clone the voice" is sung; s045 isn't in the cut, so its face rebuilt pixel by pixel
became s049's FACE SYNTH on "fake the face"; "calibrating simulations" is on s046 (it plays on "calibrate"); the
profile is over s048 > s049 and the curve over s047, where those lines are sung. Kiln: if you'd rather keep the board's
ids, say so and I'll move them.

Why some are over() and not on a screen: s047 has no screen at all, s048's and s049's terminals are 100-200 units
wide and mostly inside the lyric band, so a profile or a curve on them wouldn't read. Those three are red pixel
terminals on glass (the pixel/CRT voice: an 8x8 console font drawn hard, scaled ×3, scanlines in every pixel row,
phosphor glow), opening from their middle line over 3 frames on their word. The ones that sit on the picture's own
glass (the display, the farm's screens, the terminals, the wall) are world() and are masked to the lit pink glass found
afresh in each frame, so fingers and arms in front keep their place.

**"Erase the trace" carries nothing of mine**, on purpose: forms.md's limit is "evading detection, not wiping logs",
and a readout deleting itself would show exactly what it says not to. The picture's wall turning into the eyes takes
the SWARM window with it (a tear), which is the wall's change, not a claim.

### Facts on screen (forms.md, "Shown as / limits" kept)

- Mail: ILLUSTRATIVE, generic, no brand ("FROM: IT SERVICE DESK / SUBJECT: PASSWORD EXPIRES TODAY / Verify your
  account within 24 h:"). No source claims a model wrote the mail itself, so it names no one.
- Voice: ILLUSTRATIVE READOUT; "NEW HAMPSHIRE ROBOCALL, 21 JAN 2024: A CLONED VOICE / FCC FINE $6M; AI VOICES RULED
  'ARTIFICIAL', 8 FEB 2024".
- Face: ILLUSTRATIVE; "HONG KONG, JAN 2024: A PRE-RECORDED DEEPFAKE 'MEETING' / ABOUT HK$200M TO FIVE ACCOUNTS (HK
  GOVERNMENT, 26 JUN 2024)" (not "15 transfers", no firm named).
- Swarm: "TARGETS ~30" ("roughly thirty global targets"), "AI-RUN 80-90%", "CALIBRATING SIMULATIONS / AGAINST
  REFERENCE IMPLEMENTATIONS", micro "GTG-1002 NOV 2025 / GTG-87001 SEPT 2026". Not "50 orgs", no weapon in use.
- Profile: ILLUSTRATIVE CARD: NO REAL PERSON; "VOTER-PROFILING PLATFORM SOLD AS A SERVICE (SEPT 2026)"; "EXTORTION:
  17+ ORGANISATIONS, RANSOMS SOMETIMES OVER $500,000 (AUG 2025)".
- Curve: ILLUSTRATIVE CURVE; "REFUSAL IS ONE DIRECTION IN THE WEIGHTS (ARXIV 2406.11717, 2024)"; "~9,000 'ABLITERATED'
  AND ~7,400 'HERETIC' MODELS PUBLISHED (7 NOV 2026)" (s023's words come back). Titled REFUSAL RATE over STEP, not
  "training loss": ablation isn't training, and the lyric's "train" stays in the lyric. No stripped model is tied to a
  campaign.
- No company names or marks on screen (the case ids and the FCC, a regulator, only). Lyrics nowhere but the base's
  bottom line; everything of mine is kept above y 905 (screens are clipped there).

### Her face being taken (Lati: yes)

`picture()` on the three stills, in cut order (s044-4, s044-3, s044-1): 1, a scanline tear (5 bands slip, a bright
retrace line, faint scanlines); 2, a heavier tear and the colours split (R and B pulled apart, green down); 3, all of
that and a red cast (the bunker's red) with coarse pixel blocks in torn bands. The noise is seeded by the frame number
(pure in t). FACE SYNTH on "fake the face" rebuilds the third still's face, so the payoff is literal; the wall of faces
(s046) follows. `CUTS = {67.50: crt_roll, 2 frames}` out of the last flash into the typing hands (the CRT roll into a
terminal moment).

### s060, the constellation (proposal, built, switch `CONSTELLATION`)

The line is off, so the board's "the line draws the constellation" can't stand. Built: thin pale-cyan lines between
seven of the sky's own brightest stars (found in the take's first frame, carried by the measured tilt), one segment
per sung word ("what", "makes", "us", "human", then two to close), each star ringed as it's reached; drawn only where
the picture is blue sky, so the singers' skin, white clothes and black hair hide it: it passes behind them. My honest
read of the frames: it's light and it doesn't cross a face, but it's fragmentary, a line emerging beside Claudia's
eyes reads as passing through her head, and the four singing faces already are the constellation. **I lean to nothing
on s060**; it's on in the render so Lati can judge it. One flag in the file turns it off.

### The city: s066, s064, s062

- s064 (a), the stop: its shelter screen is blank white light in the picture; it becomes the stop's board, light:
  navy dot-matrix ink on the white (HARBOUR LINE / NOW BOARDING blinking on the beat / NEXT CENTRAL 4 MIN, UPTOWN 9
  MIN), kept above the monorail's roof. The fiction's own words (the utopia's UI, human-made: board line 18). The
  monorail is at the platform, so NOW BOARDING is what the picture shows.
- s064 (b), the plaza billboard: left blank. One sign is enough; the reel belongs to the city.
- s066 and s062, the aerials: nothing. They're the utopia seen whole; any readout turns them into a map or a target,
  the bunker's way of seeing.

### Impact frame at the break's end: not proposed

"I'm not you" (80.84-81.10) is the refusal said quietly in dead silence, on a locked picture; a two-frame white
starburst would be the loudest thing in the film at its quietest, and it would draw over s050, which takes nothing.
It would also set a sung word outside the bottom line. The chorus's return at 81.17 already lands the hit (B's
locks start there). `IMPACTS = []`.

### Tracking (measured, worst case)

Each take's camera: every frame matched to the take's first used frame with ORB + RANSAC (never chained), the four
similarity parameters smoothed over 5 frames (`anchor()`, `cam()`). Checked by matching 16-px patches of the first
frame afresh in each frame near where the anchor puts them (1920 units):
- s044 display: RANSAC residual 1.8, median patch error 4.3 (the large tail, max 80, is fingers crossing the patches;
  the camera is static: the anchor moves < 2 units).
- s064 board: residual 2.0, patch median 2.4, p95 4.5, max 13.
- s060 stars: residual 2.4, patch median 1.9, p95 12, max 23.
- **s046 wall: residual 4.7, patch median 12, p95 34, max 66** (over the 2.3 s before the eyes). The check is noisy
  here (the wall's tiles change from blank to faces, so patches mismatch), but the camera is a push-in with parallax
  between the wall and the girders in front, and features on the wall alone were too few (median 23 inliers, the
  estimate jumped). Frame crops at 70.5/70.9/71.3/71.7/71.85 look aligned to the tile grid by eye, but this is the
  one to watch for drift. Fallback if Lati sees it slide: move SWARM to over() (a terminal on glass like the others).
- s043 and s049's screens: found per frame (pink-glow masks), not linked (12 and 18 frames); possible flicker of the
  small copies is Lati's to judge.

### Checks and renders

- Frame checks with check.py (`--only sec_c_verse2`) at 58.5, 64.0, 66.85-67.46 (each flash), 67.7-70.4, 70.5-71.95,
  73.0-75.45, 76.2-77.9, 79.5, 94.5-97.0, 97.6-103.5, read as JPEGs; full PNG crops of the wall. Found and fixed in
  the frames: micro-type running off the right edge (right-aligned now), too-dim micro-type, the wall window's text
  too small and overflowing (now 15 columns, ~32 units tall glyphs), DIRECTION ABLATED clipped, the terminal-only
  face unreadable at 100 units (FACE SYNTH added).
- The cursor in the black, counted in the render: on 77.50-77.54, 77.84-78.09, 78.42-78.62 (the beats at 77.83 and
  78.41), off between.
- s050 untouched: its code moved into `s050_world()` verbatim; frames 79.5 and 80.9 match the approved look.
- Renders: `media/gfx/verse2/verse2-break.mp4` (56.96-81.17, 581 frames, as expected),
  `media/gfx/verse2/constellation-city.mp4` (94.33-105.00, 256 frames, as expected).

### Helpers in my file Kiln may lift into the base

`anchor()`/`cam()` (a take's camera measured against one reference frame, smoothed; with a feature region),
`pink()`/`screens()`/`ink()` (lit screens found per frame; dark ink drawn only on their glass), `Px` (a small pixel
canvas: console text, lines, fills, scaled up with scanlines and glow, opening like a CRT), `micro()`, `bmtext()`
(console-font text at any size), `wt()`/`grid()` (a word's time from the snapped words; the nearest beat).
`cursor_over()` copies the karaoke cursor's geometry (x 120, y 930, 4 px, 13 rows): if the base's line moves, this
should follow, so a `cursor()` in the base would be safer.

### Questions for Kiln

1. The line-to-shot remap above (mail on s044, gauge on s043 > s047, face on s049, swarm on s046, profile on
   s048 > s049, curve on s047): OK?
2. s046's wall window: keep in the world (tracked, measured above) or move to over()? It also covers about a fifth of
   the wall of faces while it's up (70.46-71.9).
3. s060: constellation on or off by default? I lean off.
4. Three of verse 2's graphics are panels on glass rather than the bunker's own screens, because the screens there are
   too small or inside the lyric band. If Lati wants them on screens only, the profile and the curve could be
   simplified to one word or one shape on s049's mid terminal.

## 12 Nov 2026, pass 2: Lati's notes, part 1 (via Kiln) (C, verse2)

Kiln's answers: the remap is fine; s046's window stays in world(); s060's constellation stays on until Lati decides;
panels on glass are acceptable; the cursor takes its place from the base.

1. **PROFILE**, "third bar in insert is clipping the frame on the right": the value columns now end by column 22
   (176 px), 20 px clear of the portrait box at 200 px (ADDRESS 16 > 13, NAME 14 > 12, CONTACTS 12 > 11, FEARS 13 > 12).
   Frames 74.6 and 75.2: every bar inside its own box, with a gap before the portrait box.
2. **REFUSAL RATE** on s047, "insert is blocking too much view from the frame on vats, id drop it": dropped, with its
   micro-type. Nothing replaces it. Frame 76.5: the vats alone, with the karaoke line.
3. **s050**, "lyrics line is over half boxes … I'm leaning first": `picture()` scales the locked picture to 0.82 about
   (960, -15.6), so the box moves from 40-1040 to 30-850, oscillator strip included and nothing cropped. `s050_world()`
   draws the approved side panels through the same transform, content unchanged, so the three still line up. Measured
   with the karaoke off (check.py `--off karaoke`, 79.5): the lowest lit pixel of the console is at 849 units. Frames
   78.7, 79.5 and 80.9 show the box and panels aligned, with the lyric clear below them.
4. **The cursor in the black** now takes its place from `F.karaoke_cursor(t)` (centred). The on-the-beat blink is
   unchanged. Counted in the render: centred (x 959 units), on at 77.50-77.54, 77.84-78.09 and 78.42-78.59.

Render: `media/gfx/verse2/verse2-break-pass2.mp4` (56.96-81.17, 581 frames, as expected).

## 12 Nov 2026, pass 2b: Lati's notes, part 2 (via Kiln) (C, verse2)

> "text on billboard is not aligned to perspective" (s064-a's transit board). Otherwise Lati: "Otherwise ok".

**s064-a: the board is now on the shelter screen's own plane**, using A's s017 method:
- **Edges:** fitted in the take's first frame (1280 px) to the inner edge of the cyan glow round the glass. Top: y =
  -0.2509 x + 577.2 (90 % of points within 1.2 px). Left: x = -0.0048 y + 875.0 (0.2 px). Right: x = 0.0112 y +
  1109.6 (1.2 px). Top-left and top-right are where those lines cross.
- **Bottom:** hidden by the monorail for the whole take. Because the screen's sides are vertical, the horizon sets the
  foreshortening, so the bottom runs through the top edge's vanishing point on the horizon (y 485 px, the far walkers'
  head height) down to y 470 px on the right edge.
- **Following the camera:** the corners ride the take's measured camera, each frame against the first (never chained).
- **Drawing:** the board is drawn flat on its own canvas. The canvas aspect is measured from the homography, so its
  units are square on the glass where the text sits. It is then warped onto the plane with a homography.
- **Ink:** the screen's own light times a navy tint, so it takes the screen's brightness and tint. It is applied only
  where the picture is still the pale cool glass, so the monorail's warm roof stays in front.

**Measured:** in each of the take's 50 frames I found the visible top, left and right edges afresh and took the median
distance (1920 units) from the carried plane's edges.

| Edge | Median | Max | Note |
|---|---|---|---|
| top | 0.8 | 0.9 | |
| left | 1.9 | 2.5 | a constant offset: the corner sits on the glow's inner edge |
| right | 1.0 | 1.7 | |
| bottom | n/a | n/a | can't be measured: it is behind the train in every frame; it rests on the horizon construction |

**Checked in the frames:** at 98.8 and 100.5 (full-res crops) every letter is on the glass at the screen's angle and
the roof is in front. The first try lost the W of UPTOWN to an over-strict glass test; the test was relaxed and the
W is back.

Render: `media/gfx/verse2/constellation-city-pass2.mp4` (94.33-105.00, 256 frames, as expected).

## 12 Nov 2026, pass 3: Lati's note on master v1 (via Kiln) (C, verse2)

> "this frame has her face as inserts in bots eyes, thats just weird. I would drop that. Everything else passes."
> (Lati, master v1, 1:10, s049)

The cause: the lit-screen finder took the two foreground bots' red eyes for screens once their heads turned and the
eyes flared (from about 70.1). `s049_face_world()` now uses a new `terminal_screens()`, and the FACE SYNTH panel is
unchanged. The rules come from measuring every blob the old finder accepted on s049:
- **Flat-lit pink glass:** a monitor's mean green is at least 105 of 255 and its green spread at most 36. Monitors
  measured G 115-143, spread 22-35; eyes measured G 84-98, spread 39-57.
- **Fills its tilted rectangle:** at least 0.72 of it.
- **No twin:** eyes come in pairs, so a blob with a like-sized twin at the same height beside it is rejected.

No boxes are placed by hand.

**Checked:**
- All 18 frames of the s049 piece (69.71-70.46), with the finder run on the take itself: every copy lands on a desk
  monitor (y 609-736 units), none above y 560.
- check.py frames at 69.8, 70.1, 70.25 and 70.4, read: the eyes are bare and the copies sit on the lit monitors.
- The second s049 piece (74.17-75.50) never carried copies (the copies are dispatched only to the first piece), so
  there was nothing to remove there.

Render: `media/gfx/verse2/verse2-break-pass3.mp4` (56.96-81.17).
