# Motion direction in prompts: five references (9 Nov 2026)

Written by a helper for Claude (Kiln, local), 9 Nov 2026. Lati's request, in his words: "Mainly not the content itself
in the prompts, but how it directs motion and camera." Read first: `references-7-nov.md` §2 and
`skybrows-ultimate-showdown-prompt.md` (the 30 s showdown), `lessons-1-2.md`. What those already say is not repeated.

Marks in the toolbag: **[S]** seen in a source here, **[R]** our own record, **[K]** a suggestion, untested.

Files (all under `media/`, gitignored):
- Clips: `media/references/Skyebrows-2118419084433928598.mp4`, `Skyebrows-2119157098307104858.mp4`,
  `danikkk_wqs-2119535297541070962.mp4`, each with its `.info.json`.
- Skybrows' two prompts, full text as posted: `media/references/Skyebrows-2118419084433928598.prompt.txt` and
  `Skyebrows-2119157098307104858.prompt.txt`. Kept out of git because they're his text; only short phrases are quoted here.
- Contact sheets: `media/references/motion-refs-9-nov/` (labels are frame order; 2 fps sheets: O001 = 0.0 s, O002 = 0.5 s ...).

How they were read: `yt-dlp` with no login; the post text and the author's reply prompts from the public
`api.fxtwitter.com/2/thread/<id>` endpoint (no login). Frames at 2 fps for the whole clip, 8 fps and 24 fps bursts, ffmpeg
scene detection, and a frame-difference count for held drawings (script in the scratch dir, `tools/twos.py`).

---

## 1. Skybrows' "semi reliable Wan Formula" (screenshot, X post 7 Nov 2026)

**What it is:** a screenshot Lati took of the post and its reply prompt. Two fighters, 80s/90s OVA look, an 8 s clip.
**Read:** the full prompt (it's in the screenshot). **Not read:** the clip itself (one frame visible: a high kick with
the near leg huge in the foreground, low camera, backlit) and the post URL, so the Wan version and settings are unknown.
The same skeleton reappears an hour later in source 4, run on Seedance 2.0, which we could watch.

**The skeleton, in four parts:**
1. **Style block that sets the frame rate and drawing.** "deliberate 12fps limited animation", "rotoscoped traditional
   Japanese 2D animation", "peak sakuga", "hatch shading and sketchy detail", "CRT quality", one phrase in bold:
   "Realistic proportion Hand-drawn anime". It also names studios; we don't (our rule), and source 4 shows the rest of
   the block still does the work.
2. **A move vocabulary, not a story:** "kicks, blocks, counters, backflips, twists, and near misses". It names the kinds
   of action and leaves the order to the beats.
3. **Four time-coded beats of 2 s each** ("0–2s:", "2–4s:" ...). Each beat is one action, the answer to it, and one
   camera line: "Camera skims the ground beneath their legs", "Camera whips around behind them". Two beats aim the
   action at the camera: a kick "that narrowly misses the lens"; "ending on a dramatic near-miss counterstrike".
4. **A "Throughout:" clause** for what holds in every beat: the camera's standing behaviour ("Constantly orbiting,
   highly shaky close-up camera, swooping low and between fighters, extreme perspective"), the motion quality ("fluid
   rotoscoped motion, elaborate hair and cloth animation, powerful impacts"), the light ("consistently backlit and in
   shadow"), and an accuracy line ("Perfect character, lighting, and style consistency").

**What's new against what we knew:** the showdown prompt was rules + a 5 s timeline over 30 s. This one is the short
form: about 200 words, 8 s, 2 s beats, and the global rules squeezed into one "Throughout" line. That's our shot length.

## 2. "The temporal poster-grid" prompt (pasted by Lati, 9 Nov)

**What it is:** a prompt headed "Opus 5.5 Prompt:", asking for a whole music video as a 20×12 grid of cells over one
continuous image, each cell showing the same footage at a different moment. Read in full (`temporal-grid-prompt.md`).

**What it directs:** time, not camera. Its vocabulary is an edit vocabulary: "staggered time offsets, rapid repetitions,
reversed motion, delayed echoes, speed ramps, micro-loops and impact freezes"; patterns ("diagonal temporal cascades,
radial time ripples, expanding freeze-frame waves, checkerboard reversals"); a structure tied to the music ("restrained
motion during quieter passages", "cascading temporal explosions across the grid, followed by sudden unified resets");
one anchor ("Keep the central 4×4 region anchored to the primary action").

**Our read:** no video model we use takes a full song and keeps a 240-cell grid coherent. Every term in it is a
compositing operation on footage that already exists. It's a spec for code. See "The temporal grid for us" below.

## 3. Skybrows, "Not Rogue Vs Not Juggernaut" (x.com/Skyebrows/status/2118419084433928598, 5 Nov)

**What it is:** a 15 s "cutting room floor test" on Seedance 2.0, 720p (container 60 fps, 24 new frames a second).
Post: "I'm convinced this level of dynamism is only possible in seedance 2.0". **Read:** the clip and the full prompt
(Japanese, about 2,900 characters, in his reply). The prompt is written for 30 s and 20 beats; the posted clip is 15 s.

**How the prompt is built (translated in summary):**
- **Priority first:** it opens with "speed and motion first" and a density target: about 20 continuous actions.
- **A locomotion rule per character:** she moves only by flight, never walks; he moves only on the ground and by huge
  leaps that "follow gravity" in parabolas, never floating. Each fighter's way of moving is fixed before any beat.
- **Standing camera rules:** ultra-wide, three-point perspective, extreme foreshortening, asymmetric diagonal framing,
  a fast-moving camera rolling left and right, the dutch angle flipping often; the camera "always passes fast beside,
  over, under and through gaps" in figures and structures; scale goes "ultra close-up → extreme wide → ultra close-up".
- **One light rule for every cut:** backlit, the fire behind or behind-diagonal is the key light "even as the camera
  moves, turns and rolls"; rim light, deep black shadows, faces dark but readable.
- **A route through places:** loading yard → container alley → pipe racks → elevated walkway → furnace, "distinct
  landmarks, persistent damage". The camera travels; the places change; the damage stays.
- **20 numbered beats, each in the same order:** action, then a camera verb with a roll direction ("the camera dives
  under the fist, rolls left"), then the same suffix every time (ultra-wide three-point perspective, extreme
  foreshortening, backlit), then a list of what to animate in detail: "shoulder rotation, hair lag, wind pressure";
  "landing compression and ground shatter"; "weight shift, armour, cubic destruction".
- **A written ending:** a shockwave shatters the ground into cubes, the camera retreats ahead of it, then thick black
  smoke and debris cross the lens, cover the frame and wipe to full black. "No long explosion wide, no aftermath."
- It uses a negatives list too ("no pauses, held drawings, fixed camera, frontal framing, symmetry").

**What the clip shows** (`jp-prompt-2118419-*.jpg`):
- The camera is almost never at eye level: worm's-eye under the giant (O001, O019), high and rolled over the alley
  (O005, O006), down the pipe walkway with every line converging (O014-O016). Foreground structure (containers, pipes,
  girders) frames nearly every shot, so the camera's speed reads against something near.
- Only about 4 hard cuts in 15 s (scene detection at 0.5, 8.1, 9.5, 11.8 s). The rest is one moving camera. The beat
  list wrote "fast cuts mid-action"; the model mostly gave camera moves instead.
- **Start and end held, middle dropped.** Beat 1 (the dodge under the fist, 0-1 s), the low-altitude flight down the
  container alley (beat 4, 2-3 s), the pipe walkway (beat 11 or 16), then the finale as written: a full-frame white
  starburst impact frame at 11.8 s (`8fps-11.5-15s` B003), cubic debris (B015-B023), smoke across the lens (B024-B026),
  black by about 14.7 s. Most of the 20 beats are not there. One clip, so a hint, not a rule.
- Drawn on ones: about 7% of frame steps are holds (the showdown clip: 3%). This prompt has no frame-rate words.

## 4. Skybrows, "Good Ol Seedance 2.0 (480p)" (x.com/Skyebrows/status/2119157098307104858, 7 Nov)

**What it is:** a 10 s, 480p (864×496), 24 fps clip of two sword fighters on a rampart, Seedance 2.0 on Dreamina. Post:
"still has some crazy moves (if sometimes totally beyond comprehension)". **Read:** the clip and the full prompt.

**The prompt** is source 1's formula with a sword fight swapped in, posted about an hour after it (by the screenshot's
timestamp). Additions worth noting:
- **Lens and motion words in the style block:** "extreme wide angle lens. extreme motion arcs and motion smears.
  extreme foreshortening and perspective distortion".
- **An event that moves the camera:** swords collide "with massive clangs and sparks and shockwave that shatter the
  ground into [cubes] as the camera snaps to a wide angle to show the whole ground shatter". The cut is caused by the hit.
- **A setting that keeps the background moving:** "explosions regularly exploding in the background", "extremely windy".

**What the clip shows** (`formula-seedance-2119157-*.jpg`):
- **The time codes landed.** The 4-6 s beat ("colliding midair in a dramatic slow-motion impact"): a one-frame white
  flash at 3.9 s (`8fps-3.5-6.5s` A004), then the crossed blades held near-still for about 0.9 s (A005-A011), then at
  5.0 s the snap wide to the shattered rampart (A013), then freefall against open sky by 6 s (A017-A024). The 6-8 s
  "separate ... midair clash" beat follows on time.
- **The 12 fps words did something.** The first second is drawn on twos: frame differences alternate low and high
  (7, 23, 7, 23 ...), 12 new drawings in 24 frames; later it mixes ones, twos and threes. Across the clip about 29% of
  frame steps are holds, against 7% and 3% in his two prompts without the words (`24fps-0-2s` sheet: F001=F002,
  F003=F004 ...).
- **Smears and near misses are real frames.** At ~1.1 s a body crossing the lens becomes two frames of pure streak
  (`24fps-0-2s` F027-F029); at ~0.6 s a cape fills the frame for two frames (F015-F016). Blade trails show as white arcs
  (`2fps` O004, O009-O010).
- **"Camera skims the ground beneath their legs"** gave a camera at ankle height with a tilted horizon for the first 2 s.
- **Where it broke:** bodies and swords mangle in the fastest frames (his own "beyond comprehension"). In the slow-motion
  beat, the model's answer was a near-freeze: for our 1-4 s shots a 0.9 s hold is a quarter of the shot.

## 5. danikkk_wqs, "AI configs on GitHub" (x.com/danikkk_wqs/status/2119535297541070962, 8 Nov)

Lati: "Generally useful, maybe". **Read:** the post text and the 21 s clip. Not a motion-prompt reference.

- **The post** lists five open agent-skill repos. All five exist (GitHub API, 9 Nov, stars at that time):
  `mattpocock/skills` (319K), `addyosmani/agent-skills` (114K), `cloudflare/security-audit-skill` (68K, "one team of
  agents hunts for bugs, another tries to prove them wrong"), `kepano/obsidian-skills` (51K),
  `google/elephant-goldfish-model` (16K, design review: "fresh AI sessions that never saw it try to tear it apart").
  The last two ideas are close to how Lati already uses fresh-eyed checks; whether to look at them is Kiln's call.
  Nothing was installed.
- **The clip** is a code-rendered dashboard (`danikkk-2119535-2fps.jpg`): a 3D point-cloud graph whose virtual camera
  orbits and flies to each matched node ("hunters / MATCHED", with an "AZ 248.9°" readout), while twelve panels below
  update: typed command lines, bar charts, a token-rate meter, a git diff. Exact, legible, no cuts, 30 fps.
- **For us [K]:** it's the kind of code graphic `references-7-nov.md` already proposes for the screens. The orbit-and-
  fly-to-node camera through a point cloud is one way to draw Lati's 9 Nov "research ... technological space" for the
  verses, rendered in our 80s vector-CRT style instead of a modern dashboard.

---

## The toolbag for our 1-4 s shots

### The skeleton

One generation per shot, from its own still. With a first frame, the prompt says what moves, not what's there.

```
[STYLE, identical in every shot]
1980s theatrical sci-fi anime film, hand-drawn cel animation, dense detailed linework, two-tone cel shading,
soft film grain, deliberate 12fps limited animation, ink smear frames and speed lines on the fastest moves,
extreme foreshortening, wide-angle perspective.

[BEATS: 1 or 2, time-coded, starting in motion at 0 s]
0-1.5s: <subject> <one strong action>, <the answer: contact, parry, dodge, recoil>. Camera <verb> <physical anchor>,
rolling <left/right>.
1.5-3s: <the consequence>. Camera <verb>.

[THROUGHOUT, one line]
Throughout: constant motion, <one light rule>, <secondary motion to draw in detail>, perfect character, lighting and
style consistency.
```

What each part rests on:
- Style block first, identical across shots, frame rate inside it. [S 1, 4] [R `skybrows-lessons.md` §3]
- "deliberate 12fps limited animation" raised held frames from 3-7% to 29% on Seedance 2.0. [S 4] Untested on Wan 3.0,
  Seedance 2.5 and Grok. [K]
- Time-coded beats land within ~0.2 s on Seedance 2.0 [S 4] and within ~0.5 s on Seedance 2.5 and Wan 3.0 in our test 1
  [R `motion/test-1.md`]. So a hit can be written at the second it should land, then retimed ±5-15%. [R]
- Beats as action + answer + camera line. [S 1, 3, 4] Every action has a cause and a target. [S showdown]
- Camera pinned to something physical: "skims the ground beneath", "dives under the fist", "beside the boot". [S 1, 3, 4]
  [R `lessons-1-2.md` Motion]
- A roll direction named per beat. [S 3]
- "Throughout" for what must not change: camera habit, light, consistency. [S 1, 4]
- One light rule for all shots ("backlit by ..."). [S 1, 3, 4] It hides drift in faces and hulls by putting them in
  shadow with a rim; good for vessels and mechs whose designs drift. [K]
- Start in motion at 0 s; the first moments of takes were frozen before. [R]
- Positive words: write "asymmetric diagonal framing, rolling dutch angle" rather than his "no symmetry, no fixed
  camera". [R Lati 25 Oct] Untested against his negatives on Seedance. [K]
- In one-shot prompts, no "cut to": a beat that implies a new framing invites a cut (test 1 route B cut early;
  source 3 turned written cuts into camera moves). Use camera verbs. [R] [S 3] [K]
- "Slow motion" gave a near-freeze of 0.9 s. In 1-4 s shots ask for "a brief hit-stop on contact" instead. [S 4] [K]
- 1-2 beats only. Source 3 dropped most of 20 beats and kept the first and last. [S 3, one sample]

### Our example lines

Style block as above in each. "Space vessel", never "ship". Designs come from the plate and its references.

**Beam sword clash, mechs (2.5 s)**
> 0-1s: the white mech drives its beam sword down in a two-handed overhead cut; the black mech catches it on its own
> beam blade, a one-frame white impact flash and a ring of sparks. Camera low beneath the crossed blades, the blades
> huge in the foreground, rolling right.
> 1-2.5s: the blades grind, the white mech's back thrusters flare as it pushes, the black mech's arm buckles and its
> shoulder plates shudder. The camera circles under them on a tilted axis.
> Throughout: constant motion, backlit by the blue glow of the planet below, thruster flame and sparks drawn in detail,
> perfect character, lighting and style consistency.

[S 1, 3, 4: contact, flash, camera under the action, roll; showdown: "blades lock ... huge in the foreground as the
viewer circles on a tilted axis"] Mech weight [K]: give mechs a locomotion rule as source 3 did for its fighters, e.g.
"every mech move starts with a thruster burst and ends in a recoil of its armour".

**Missile swarm (2-3 s)**
> 0-2s: dozens of missiles burst from the launch pods along the hull and fan out toward the camera, their white smoke
> trails curling and crossing in tight spirals; the nearest warhead passes inches from the lens. Camera fixed to the
> hull of the launching space vessel, looking back along the trails, shaking with each launch.
> Throughout: constant motion, backlit by the sun behind the swarm, smoke trails drawn in detail.

[S 1, 4: near miss at the lens] [S showdown: tied shake on launches] [K: the hull as the camera's anchor] Ends on the
warhead crossing the lens: a ready cut point (below).

**Dogfight pass (1-2 s)**
> 0-1.5s: two space fighters scream past the camera from left to right, the nearer one rolling inverted, its wing filling
> the frame for a moment, exhaust smearing into streaks; the camera whips to follow them, rolling with their turn.
> Throughout: tracer fire crossing the frame, backlit by an explosion behind them.

[S 1, 4: "whips around", smear frames when something crosses the lens] [S showdown: whip pans between targets]

**Fast camera across the battlefield (3-4 s)**
> 0-2s: the camera races low over the hull of the lead space vessel, threading between its gun turrets as they fire,
> rolling left.
> 2-3.5s: it rises past the bridge tower into the wide battle: explosions blooming across a field of space vessels,
> tracer lines everywhere, debris tumbling toward the camera.
> Throughout: constant motion, three-point perspective, every line converging.

[S 3: camera passing through gaps in structure; route through places; "ultra close-up → extreme wide"] [R test 1:
models invent vessels once the shot reveals new ones] So: make the plate the wide, or let the reveal hold only things
without a design (explosions, tracers, debris). [K]

**Cockpit (1-3 s)**
> 0-1s: the pilot slams the throttle forward; the whole cockpit jolts, red warning lights strobe across her visor, the
> starfield outside stretches into streaks. Camera fixed to the cockpit frame beside her helmet, shaking hard.
> 1-2.5s: a hit rocks the fighter; sparks burst from a side panel, the pilot's head snaps with the impact.
> Throughout: the glowing screens stay plain and clean-edged, lit from the panels in front of her.

[R lesson 13: plain screens for code UI] [S 1, 4: camera habit in one line] [K: inside a cockpit, shake is the motion
that's free; the camera stays bolted to the frame so the panels can be tracked]

### Two edit devices from the clips [K]

- **The occluder cut.** Both of his finished clips end with something crossing the lens (smoke, a severed head) and a cut
  to black. Write a shot's last half-second as a hull, a warhead, a wing or smoke filling the frame: it gives a cut
  point the model draws itself, and hides the drift that starts after ~2.6 s. [S 3, showdown] [K for our use]
- **The impact frame.** A one-frame white or inverted flash at the hit came out in both Skybrows clips when asked for
  ("impact flash", "impact frame"). It can also be done in code on the beat, exact to the frame, if the model misses it. [S 3, 4] [K]

---

## The temporal grid for us (a suggestion)

**What it is in code:** take one finished take, cut the frame into a grid, and show in each cell the same crop of
the same take at a different time: output frame t, cell (x, y) shows source frame t − offset(x, y, t). Offsets make the
patterns: a diagonal cascade is offset = k·(x + y); a ripple is k·distance from the centre; a checkerboard reverses
alternate cells; a "unified reset" sets every offset to 0 on a downbeat. The centre cells stay at offset 0 so the action
still reads. Python and Pillow or ffmpeg on the CPU, no generation, no spend.

**Why it could fit this film:**
- The title. One source, many copies of it out of step with each other, is a picture of "made in your image" and "I'm
  not you": the same thing, diverging. It earns its place on those lines, not as decoration.
- **It stretches short good takes.** Only the first ~2.5 s of a take are usable. A grid can fill a 4-6 s bar from a
  2 s clean take by looping and offsetting it, and never show the drift.
- **It's exact to the music** because it's ours: resets on downbeats, cascades on hits.

**Where, as candidates:** "Made in your image" at 1:21 (space battle mayhem) or 2:08 (the pilot and cockpit reel, one
pilot's take, many moments of it); the 2:31-2:37 zoom back in "in steps, on beat", where each step could be a grid
resolving into one image. Not the sung close-ups (lip sync across offset cells won't read).

**What to keep out:** most of its effects list is 2010s motion design: pixel sorting, datamosh, RGB split. Our period
has its own: scanlines, halftone, negative flashes, speed lines, monochrome flashes. A grid of thin grey lines is closer
to a CRT bank or a bridge wall of monitors. Framing it as a wall of monitors on the bridge would keep it inside the world. [K]

---

## Caveats

- **One sample each.** Every observation from sources 3 and 4 is one clip, which he chose as a best or a near-best.
  "Best of 4" was his rate on the showdown; expect retries.
- **The Wan formula was not seen on Wan.** We have its prompt and one frame. What we measured (time codes, twos, smears)
  is Seedance 2.0. Wan 3.0, Seedance 2.5 and Grok each need their own check. Grok's takes looked closest to the stills in test 1; it
  likes short prompts, so the style block may need trimming there.
- **The held-frame count is a measurement of frame differences,** not of drawings. A camera move over a held drawing
  still differs a little, so the counts are approximate; the pattern in the first second of source 4 is clear.
- **A 24 fps take on twos in a 25 fps cut** will judder unevenly. Cut at 24 fps or conform the takes, before trusting
  the look. [R `lessons-1-2.md`: a 16 fps take in a 25 fps cut]
- **Names:** his prompts name studios and a real animator to get the look. Ours don't; the descriptive words carry it,
  and source 4 shows that block works with the names among many other words, so we can't tell what the names add.
  His "cubes" destruction has a name we won't use; "large angular cubic debris" says it.
- **Japanese prompting** is what he used for source 3. We have no A/B; it's still on style.md's test list.
- **Cost of testing:** each A/B (12 fps words on and off, Japanese and English) is at least two takes. At OpenRouter's
  Seedance 2.5 $0.23/s for 720p, two 3 s takes are $1.38, $2.76 by the ×2 rule; ISEKAI ZERO Wan 3.0 lists 52 credits
  a second (test 1 was charged 104 for 8 s). Nothing here has been spent; any test needs Lati's yes first.
- **Fast frames mangle bodies.** Source 4's fastest frames break anatomy. For mechs that may pass as smear; for her
  and the pilots, the adult and anatomy checks still come first.
- **The danikkk repos** were checked to exist, not read. Star counts are a snapshot.
