# Motion test 2: battle plates with Skyebrows' skeleton (plan, 9 Nov 2026)

Claude (Kiln, local). Plan only; nothing spent. Lati, 9 Nov: "lets spend for proper plates and motion shots would come
through openrouter and grok then." Method: `research/motion-direction-9-nov.md` (the skeleton: style block with
"deliberate 12fps limited animation", 1-2 time-coded beats starting in motion at 0 s, camera pinned to something
physical with a roll direction, one "Throughout" line; positive wording only). One generation per shot, from its own
plate as the first frame.

## Plates

| Shot | Plate | Board |
|---|---|---|
| s034 | `s034-1` | A swarm mech lunges blade first, foreshortened at the camera. Dutch, handheld. |
| s036 | `s036-5` | The knight and the rifle mech, the tracer line between them. Orbit. |
| s058 | `s058-1` | Both sides collide in one flash. Fast pull out. |
| s082 | `s082-1` | An explosion passes the camera. Shake. |

## Routes and cost (prices read from OpenRouter's video models list, 9 Nov)

| Route | Take | Price | 4 plates |
|---|---|---|---|
| Seedance 2.5, 720p, audio off (OpenRouter) | 4 s (its minimum) | $0.231/s (video tokens) | $3.70 |
| Wan 3.0, 720p, audio off (OpenRouter) | 3 s | $0.10/s | $1.20 |
| Grok Imagine (Lati, subscription) | 3 s | in the subscription | $0 |
| Total on OpenRouter | | | **$4.90; ×2 rule $9.80** |

Optional: Grok Imagine 1.5 through OpenRouter instead of by hand, 720p, 3 s: $0.43 a take, $1.72 for four ($3.44 ×2).

## Prompts

Style block, the same in every take:

> 1980s theatrical sci-fi anime film, hand-drawn cel animation, dense detailed linework, two-tone cel shading, soft
> film grain, deliberate 12fps limited animation, ink smear frames and speed lines on the fastest moves, extreme
> foreshortening, wide-angle perspective.

Beats as written for 3 s (Wan, Grok); for Seedance's 4 s the times stretch to 0-2s and 2-4s.

**s034**
> 0-1.5s: the stripped swarm mech thrusts its blade straight at the camera, arm and blade huge with foreshortening,
> sparks streaming off the edge; the camera jerks back and rolls left as the point reaches for the lens.
> 1.5-3s: the mech's green core flares as it drives forward again, armour fragments spinning past. Handheld camera,
> shaking, rolling left.
> Throughout: constant motion, backlit by the blue glow of Earth below, sparks and debris drawn in detail, perfect
> character, lighting and style consistency.

**s036**
> 0-1.5s: the iridescent knight mech dives forward under a burst of rifle fire, body twisting, sword sweeping up; the
> stripped mech fires again, a bright tracer line streaking past the knight's shoulder. The camera orbits the two on a
> tilted axis, rolling right.
> 1.5-3s: the knight's sword cuts across the rifle, a one-frame white impact flash and a ring of sparks; the stripped
> mech recoils, spinning backward. The camera keeps orbiting.
> Throughout: constant motion, backlit by the blue glow of Earth below, thruster flame and sparks drawn in detail,
> perfect character, lighting and style consistency.

**s058**
> 0-1s: the white flash at the centre blooms outward, a ring of light racing through the fleet and the swarm, hulls
> and mechs lit white on one side.
> 1-3s: the shockwave throws debris outward, mechs tumble, the space vessels rock on their axes; the camera pulls back
> fast and wide, rolling right, the black hole's bent light glowing in the corner.
> Throughout: constant motion, lit by the flash and Earth's blue limb, debris and thruster trails drawn in detail,
> perfect character, lighting and style consistency.

**s082**
> 0-1.5s: the explosion behind the swarm mech bursts toward the camera, fire and armour plates flying past the lens,
> the mech hurled forward out of the flames, arms flung wide; the camera shakes hard and rolls left.
> 1.5-3s: the fireball races past the edges of the frame and thins into smoke and glowing fragments, the mech tumbling
> past the camera.
> Throughout: constant motion, lit orange by the fire against black space, flame and fragments drawn in detail,
> perfect character, lighting and style consistency.

## What it tests

Which route holds the designs and the 80s cel look under fast motion, whether the 12fps words give held drawings
(measured by frame differences, as in the research), and whether the time-coded beats land. Lati judges the motion.

## For Grok Imagine (Lati runs it)

Plates in `media/plates/v2/`: `s034-1-…`, `s036-5-…`, `s058-1-…`, `s082-1-…`. Prompts: the 3 s ones in
`motion/test-2.json` (ids ending `-wan30`), the same words as above with the style block first. Grok liked short
prompts in test 1; if a take ignores the beats, try the beats and "Throughout" line without the style block.

## Results (9 Nov, evening)

Eight takes in `media/clips/test-2/`; side by side (Seedance left, Wan right, Wan's last frame held 1 s):
`media/clips/test-2/test-2-side-by-side.mp4`; six frames a take: `motion/test-2-strips.jpg`.

**Cost:** $5.44 in all (ledger). Seedance 2.5: $0.934 a 4 s take ($0.234/s, as listed). Wan 3.0: $0.425 a 3 s take,
**$0.142/s, not the $0.10 the models list shows**; the tool's price table should take the charged rate.

**Run note:** the eighth take was refused at first by the budget gate (the ledger and the estimate summed to the cap
with float noise) and the refusal ended the script before it fetched the seven submitted jobs. Fixed in
`tools/seedance.py`: the sum is rounded to cents, and `--collect` fetches a book's submitted-but-unfetched jobs.

**Measured** (frame differences at 160×90; held = under 1.0 of 255 between frames):

| Take | fps | held frames | mean change/frame | first → last frame |
|---|---|---|---|---|
| s034 Seedance | 24 | 0 % | 21.2 | 46.8 |
| s034 Wan | 30 | 6 % | 14.3 | 95.8 |
| s036 Seedance | 24 | 0 % | 9.4 | 62.9 |
| s036 Wan | 30 | 4 % | 13.5 | 69.9 |
| s058 Seedance | 24 | 10 % | 9.6 | 53.2 |
| s058 Wan | 30 | 0 % | 8.1 | 52.3 |
| s082 Seedance | 24 | 0 % | 23.5 | 85.9 |
| s082 Wan | 30 | 18 % | 13.2 | 88.6 |

"Deliberate 12fps limited animation" gave no held drawings on Seedance 2.5 (Skyebrows measured 29 % on Seedance 2.0);
Wan holds a few. If the on-twos look is wanted, it can be done in the cut (every second frame held) rather than asked
of the model.

**Kiln's read of the frames (Lati judges motion):** Seedance cuts inside a take in s034 and s082 (a new framing midway,
s082 ending on a different scene); Wan stays one shot in all four. s034 Wan: the blade comes at the lens, then the
camera swings out to Earth with the mech small. s036 Wan: the two close in and trade places, a sword clash with sparks,
but the knight drifts toward purple; Seedance's s036 stays near the plate's composition with one flash. s058: both
bloom; Seedance gets the pull-out and shockwave better. s082 Wan: the mech is hurled out of the fireball and flies
off, the board's shot.

## Grok Imagine (Lati, 9 Nov)

Same plates and prompts (`media/motion/test-2-grok/`). s034 three takes (image-to-video and Grok's agent), s036 one
(agent, with style guardrails). Lati: crisp detail and good motion, but "very 3d and not 80s anime ... way too
'modern'". s034 take 3 (`generated_video.mp4`) might fill a second or two; s036-2 maybe for a sword hit. Route not
tried further. Strips: `test-2-grok-strips.jpg`.
