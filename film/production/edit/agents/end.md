# Agent log: end

Section D, the bridge's keys and silos, the calm, the missile, the zoom and the end. Song time 105.00-116.79, 141.04-the end. Section file: `production/tools/gfx/sec_*` (see README). Renders: `media/gfx/end/`.


## First pass, 12 Nov 2026 (agent D, "end")

Read: the README, graphics-plan.md, decisions.md from "The graphics plan restated", base.py, the four section files,
the board entries for s067-s075, s095q, s101, s108, s109. Looked at every take in the section first: six frames each
across the part Lati's cut uses (`media/gfx/end/look/*.jpg`, from `F.cut()`, timeline saved 02:15).

What the pictures have:
- s068: a console of toggle switches with amber lamps, a key, a red button, a gauge. No screen that can carry text.
- s069 desert, s070 tundra, s072 island, s071 mountains: outdoor silos, no consoles. s073: Earth with dozens of launch
  streaks, the fleet above.
- s101: the camera rides beside the missile (lower left, nearly still); ahead, upper right, the battle: first a spark,
  from take 0.8 s a fireball that grows until, from ~3.0 s, a beam and ships cross it and it fills the right half.

### Built (`production/tools/gfx/sec_d_end.py`)

Restructured around the zoom: Kiln's zoom code is untouched except `picture()` renamed `zoom_picture()`; the new
`picture()` hands only the zoom's gap to it and returns every other frame as it is. Checked numerically: the old and
new files give identical zoom frames (max pixel difference 0 at 33 times across 151.84-163.70), and a frame outside
the gap passes through unchanged. RANGES now = the spans of s068-s073, s101 (from `F.spans`) + the gap; the gap is
still covered.

**s068-s073, the launch readout** (`over()`, top-left, holding still). No take has a screen for it, so it's an inset
readout: a dark box (62 %), thin red corner brackets, the zoom's 8x8 console font (Lat15-VGA8) scaled x3, scanlines
inside the letters only (as the karaoke line), a little glow. Red header and warnings, amber text. It switches on as a
CRT (a line opening to the box, 3 frames) at s068's cut and collapses at the cut to s075 (3 frames). The box keeps its
size; rows wait empty for their silo. Rows:
- `LAUNCH CONTROL` (inverse), `KEY 1 SAFE -> ARMED`, `ENABLE OFF -> ON`, `LAUNCH T-00:00.x` counting down to the button,
  then `T+00:0x.x` (inverse blinking for 0.6 s at the press).
- Each silo shot adds `SILO 0n <PLACE> OPEN -> AWAY` on its own cut, numbered in the order they play (the places are
  the board's: DESERT, TUNDRA, ISLAND, MOUNTAIN); s073 adds `ALL SILOS AWAY` (red, blinking inverse).
- The events follow the take, measured in s068's frames (s068-b-a, 24 fps): key turned by 0.50 s; the switch lamps
  light at 0.79 s (no lit lamp up to frame 19, a dozen from frame 20); the button glows red at 2.58 s (frame 62:
  0 red px at frame 61, 2,752 at frame 62). They're mapped through the piece's start/in/speed (`take_time`), so a trim
  or speed change moves them. In song time today: ARMED 110.07, ON 110.18, press 110.89 (the cut to s069 is 111.00).
- Timing: the box enters on s068's cut (109.875, on the beat at 109.89) and each silo row on its cut (the cuts sit on
  beats 111.00, 112.09, 112.63, 113.21; s073's 114.375 is between beats). The KEY/ENABLE/LAUNCH changes follow the
  picture's events, not the grid: text that lagged the key would read wrong. Say if Lati wants them snapped.
- Words: all the fiction's own (no real-world system, place or number). The T- and T+ clocks are song time from the
  button press in the picture.

**s101, the track box** (`world()`, so it rides the place pulse and the CRT roll with the picture). Red brackets, a
small centre cross, `TRACK`, and an amber range tape under the box that shortens over the shot (no figure: the
fiction's own, nothing to source). The box enters on the shot's first beat (146.13, a downbeat) and closes in four
steps on the beats (146.13, 146.68, 147.23, 147.77) down to the target's own size, then rides the fireball and grows
with it; it fades as the fireball fills (equivalent diameter 400-470 units), which is ~149.5-150.3, before the beam
and the ships cross it.
- Tracking: the take decoded at 640x360; in every frame the target is found afresh (the largest warm mass, r > 180
  and r - b > 50, the missile's plume masked; before the fireball, the brightest blurred spot above and right of the
  missile); then smoothed over the whole take (x, y over 5 frames; size by a 7-frame median then 5). No optical flow.
- Error, smoothed vs each frame's own find, over the frames where the box shows (0-71): median 1.6 units; up to frame
  58 (149.5) at most 12 units; frames 59-71, while it fades, up to 44 units (frames 60-64 the beam splits the warm
  mass and the raw find jumps 30 units up-left, so the smoothed box sits between).

**Cuts into and out of the zoom:** `CUTS = {151.83: ("crt_roll", 4), 163.71: ("crt_roll", 4)}`, 4 frames each side
(0.17 s), the base's roll unchanged. Frame-checked at 151.75, 151.85, 163.65, 163.75: the roll, tear and colour split
are there on both sides; the s101 box is already gone by then. Whether 4 frames is right is Lati's to judge in motion.

**Impact frame on "Me": not proposed.** `IMPACTS = []`. s075 is locked and quiet: her face, side-on to the close-up,
sings "me" plainly, and that plainness is the line. A white starburst with a black word over it would be the loudest
thing in the film on its quietest word, and it would set the song's word outside the bottom line. If the module
wants a "Me", it belongs elsewhere (or nowhere); not on this shot.

**Quiet and locked shots:** s067, s075, s095q, s109, s108 get nothing from this file (dispatch by `F.shot_at`, and
they're outside RANGES). The karaoke line is the base's. The black after s108 (173.46-) is untouched.

### Checked, and how
- Frames with check.py (`media/gfx/end/check/`, read as JPEGs, tiled in `media/gfx/end/sheet_*.jpg`): 109.95,
  110.2, 110.6, 110.92, 111.5, 112.3, 112.9, 113.7, 114.9, 115.31 (the collapse), 143.0 (s095q: karaoke only),
  146.2/146.3, 146.75, 147.0, 147.3, 148.0, 149.0, 149.8, 149.9, 150.4, 151.0, 151.75, 151.85, 163.65, 163.75.
  Seen: the readout reads on the console, red sky, snow, white cloud and space; it stays clear of the karaoke band;
  the box sits on the spark and then the fireball. First try had the box's top and its TRACK label off-frame at entry
  and the box lingering over the crossing ship at 150.4: the steps were made smaller (700 -> 520/360/220), the margin
  tighter, the label kept on-frame, the fade earlier. Re-checked at 146.3, 147.0, 149.0, 149.9.
- The zoom: identical frames, see above.
- Motion and timing (the typing speeds, the CRT on/off, the box's steps, the roll's length) are frame checks only.

### Renders (`media/gfx/end/`, one each, --only sec_d_end)
- `bridge-launch.mp4`: 105.00-116.79, 283 frames.
- `calm-missile-zoom-end.mp4`: 141.04-173.46, 778 frames.

### Questions for Kiln
1. The readout is an inset in `over()`, not on a screen of the film (none of these takes has one). OK under the
   "readout holding still" rule, or would you rather it go?
2. KEY/ENABLE/LAUNCH change on the picture's events, not the beat grid (see above). Keep, or snap?
3. `ALL SILOS` and the silo numbering are the fiction's own; the place names are the board's. Fine?
4. Helpers that could go in the base if wanted: `take_time(p, src)` (inverse of `src_t`), the pixel-font readout
   `text_layer()` (glyph-only scanlines, inverse rows).
