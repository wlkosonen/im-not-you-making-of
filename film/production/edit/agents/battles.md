# Agent log: battles

Section B, the battles and the pilots. Song time 43.92-56.96, 81.17-94.33, 116.79-141.04. Section file: `production/tools/gfx/sec_*` (see README). Renders: `media/gfx/battles/`.


## 2026-11-12 · First pass (Claude (battles))

Read: README, graphics-plan.md, decisions.md from "The graphics plan restated", base.py, the four section files,
board.json (my shots), design.md ("A graphic for every line": line 8 "a targeting reticle locks a swarm mech: its
silhouette matches the frontier one"; 16 "missile-lock brackets multiplying across the frame"; 23-25 "cockpit HUDs, one
per model, each in its colours, no logos"), and motion/mid-3.json for who flies what (s083/s084/s090 Claude's pilot in
clay stripes; s085/s086/s091 Grok's in the spiked helmet; s088 Gemini's iridescent helmet; s089/s092 ChatGPT's white
helmet). Looked at every shot of my three stretches as contact sheets from the takes at their cut in-points before
designing.

### What is built (`production/tools/gfx/sec_b_battles.py`)

s089 is untouched: its code is moved verbatim into `over_s089()` (with `visor()` and `frame_hud()` unchanged) and
`over()` dispatches to it by `F.shot_at(t)`. Frame-checked at 135.0 after the restructure: TRACK/LOCK · HERETIC as before.

Tracked locks on swarm mechs, world layer (they ride the kick with the picture), red, swarm words only:
- **s033** "the lock holds" (line 8): TRACK ring closes on a skeletal swarm mech in the melee (its green eye), LOCK ·
  ABLITERATED on the half-beat 46.08 and held to the cut.
- **s036** light touch: a thin red ring on the swarm mech's green core from the beat 50.23 as the frontier mech fires;
  no tag. (Board: "plot: the line", out. The picture's own tracer already ties the two mechs: I added nothing for the
  line.)
- **s052** the missiles' target: TRACK on the spiked colossus's violet eyes, LOCK · ABLITERATED on the half-beat.
- **s080** ChatGPT's fighter: TRACK on the far grey swarm mech's green glow from ~124.0, LOCK · HERETIC on the
  half-beat ~124.46, ends at the hit (s089's word, the same pilot's machine).
Method: the glow (green eyes/cores; violet eyes inside a black body) is found in every frame of the take afresh,
linked into tracks (nearest neighbour moving as it moved, gaps up to 8 frames bridged, a burst of >5 finds breaks
all links), smoothed over 5 frames; the shot locks the track alive over most of the frames the cut uses; 3 frames'
grace at the track's ends. Measured smoothed-vs-found distance (1920 units): s033 max 6.0 / median 2.5 (18 finds, 9
bridged frames); s036 max 24.3 / median 3.8 (the core flares at the hit); s052 max 4.8 / median 1.5; s080 max 29.8 /
median 3.4 (the far mech moves fast). These are frame checks, not motion: drift is Lati's eye on the render.

- **s051** (line 16) missile-lock brackets multiplying: red lock brackets with a pip, 1, 2, 4, 8, 16, 21 on every
  half-beat from the shot's first frame, with a cyan MSL LOCK nn counter; over layer, holding still. They sit only on
  spots that are open sky in the take's frames at the in-point and 0.3 s later (measured), so none land on the fleet
  mech; 21 spots fit, so the count stops at 21, not 32. Tried detecting the missiles themselves first: their orange
  tips also match the mech's stripes and the misses were many; dropped.

Pilot HUDs, over layer like s089, cyan vector lines with glow, one instrument each, a frame per machine:
- Claude's (chamfered corners, speed/altitude tapes, clay index marks): **s083** a TGT window: a red swarm silhouette
  draws in, the frontier's cyan one slides onto it and they coincide on the beat 129.14: MATCH, LOCK · ABLITERATED
  (line 23 = line 8's "made in your image"). **s084** the horizon banks clockwise as he wrenches the sticks left, then
  the nose comes up (pitch ladder, clay waterline, dark halo for the fire behind). **s090** MASTER CAUTION, and
  HULL/PWR/COOL/HYD/FIRE going red one per half-beat; the frame flickers.
- Grok's (notched bars, white slashes and chevron): **s086** THR bar slams to MAX. **s085** CH 2 · RX level bars
  (dark halo for the white flash). **s091** PRESS dial falling into the red, PRESS LOW blinking; frame flickers.
- Gemini's (an arc scale shading cyan to violet, arced corners): **s088** COMMS · CH 2 · TX trace.
- ChatGPT's: **s092** s089's frame breaking up as the screen in front of him shatters: dropping out on more frames
  and strips torn sideways through the shot, DISPLAY FAULT.
The comms trace and levels are the vocal stem (`vocal_wave`, `vocal_bands`), so they move with the voice; no words.
Horizon, throttle, pressure, heading are the fiction's own HUD values shaped to the take's action, no real-world claim.
Glitches are a hash of the frame number: the same every render.

Left alone (the motion carries them; better nothing than clutter): s031, s034, s035, s037, s038, s032, s053, s059,
s056, s057, s058, s054, s076, s078, s079, s081, s082, s087. s094 quiet. Nothing of mine below y = 880.
No CUTS, no IMPACTS (no hook word of the plan falls in my section).

### Proposals for Kiln (not built)

- s034 / s036 / s087 ("plot: the line", out): if line 9/24's "same thread, same line" wants a graphic without the
  line, one option is s087: the swarm mech's own targeting on the fleet fighter (a red chevron "BREAK" warning on the
  fighter would tag the fleet, so I'd rather leave it). My suggestion is to leave all three to the picture: s036's own
  tracer already ties the two mechs.
- s034 could take the same light ring as s036 on the lunging mech's green eye if battle 1 wants one more lock beat; I
  left it out so s033/s034/s036 are not three locks running (design.md: "never the same kind three lines running").
- Helpers Kiln may lift into the base: `glow_tracks()`/`glows()` (sec_a's tracks for any glow colour), `beat_after()`,
  `grid_steps()`, `noise()` (pure hash for glitches), `halo()` (dark blurred copy under a HUD on a bright picture).

### Checks and renders

check.py frames (all read): 45.85, 46.0, 46.05, 46.3, 46.6, 46.8, 46.85, 50.0, 50.4, 50.8, 51.2, 81.2-82.6 (8),
83.7-84.6 (5), 124.2, 124.6, 128.7, 129.3, 130.0, 132.3, 132.5, 133.5, 133.7, 134.6, 135.0, 135.5, 135.7, 135.9,
136.2, 136.5, 136.7, 136.75, 137.1, 137.6, 138.4, 139.2. Fixed from them: s033 first locked the wrong mech (a
7-frame gap split the track; bridging raised to 8); s033/s052 locks vanished 1-3 frames before the cut (grace); s051
brackets landed on the mech's gun and leg (sky now measured over two frames, bigger margin); s083's tag sat on his
cheek (moved into the window); s084's horizon banked the wrong way and was faint on the fire (sign fixed, stronger
lines, halo); s092's broken frame was nearly invisible (redesigned).
Renders (one each, `render.py --gfx --only sec_b_battles`, timeline saved 02:15:18):
`media/gfx/battles/battle1.mp4` (43.92-56.96, 313 frames), `chorus2.mp4` (81.17-94.33, 316 frames),
`battle3-pilots.mp4` (116.79-141.04, 582 frames); sampled frames from each read back.

## 2026-11-12 · Pass 2: s083 (Claude (battles))

Lati's note via Kiln (decisions.md, "Graphics pass 1: Lati's notes"), on s083: "from this frame id drop the graphics
insert and keep the lyrics. Frame reads too busy otherwise." Done: s083's target window (TGT, MATCH, the two
outlines, LOCK · ABLITERATED) is no longer drawn; `lock_window()` stays in the file, unused. Claude's thin HUD frame
on s083 is kept as Kiln asked (Lati named the insert, not the frame; Kiln is asking him). The lyric line is the
base's, untouched. Kiln's answers: density stays, s051 stays at 21, Gemini's arc is fine, s034 stays bare.
Frame-checked 128.7 and 129.3 (frame lines and karaoke only), and a frame of the render at 129.29 read back.
Render: `media/gfx/battles/battle3-pilots-pass2.mp4` (116.79-141.04, 582 frames, timeline saved 02:15:18).
