# Battle motion prompts: the rules (film 3)

Claude (Kiln, local), 9 Nov 2026, from motion test 2, Battle 1 and Battles 2-3 part 1 and Lati's verdicts on them
(decisions.md, 9 Nov). Lati: "incorporate lessons learned also into future motion heavy battle scenes that are yet to
come, so this wont go unnoticed after this batch." Every battle or action motion prompt is built from this file, and
`tools/seedance.py` refuses one that is missing the two sentences marked **lint** (`MOTION_RULES` in the tool).

## Route

Seedance 2.5 through OpenRouter, 720p, 4 s (its minimum), silent, the picked plate as the first frame. Wan 3.0 "reads as
more 3d animated", Grok Imagine "way too 'modern'" (Lati, test 2). $0.934 a take.

## The prompt, in order

1. **Style block, word for word** (it gave the look Lati picked; don't change it untested):
   > 1980s theatrical sci-fi anime film, hand-drawn cel animation, dense detailed linework, two-tone cel shading, soft
   > film grain, deliberate 12fps limited animation, ink smear frames and speed lines on the fastest moves, extreme
   > foreshortening, wide-angle perspective.
2. **Camera and action sentence** (Skyebrows' references; Lati asked for "heat", Battles 2-3):
   > Extreme wide-angle lens, ultra-wide three-point perspective, asymmetric diagonal framing, extreme motion arcs and
   > motion smears; a fast camera that rolls left and right and swoops beside, over, under and between the mechs, space
   > vessels and debris, with near misses at the lens. Every mech move starts with a thruster burst and ends in a recoil
   > of its armour.
3. **lint: everything acts** (s051's targets and s052's mech stood still):
   > Every mech, fighter, drone and space vessel in the frame is always in action, dodging, firing, turning or breaking
   > apart, from the first frame to the last.
4. **lint: hits do damage** (s053's sword passed through):
   > Every hit does visible damage: armour cracks and bursts, parts tear off and spin away.
5. **Two time-coded beats, 0-2s and 2-4s,** starting in motion at 0 s. Beat 1 is the board's moment (shots are 1-2 s on
   screen); beat 2 its consequence, a spare piece when Seedance cuts inside the take.
6. **Throughout line:** "Throughout: constant motion, shaky camera, explosions blooming regularly in the background,
   <one light rule>, <what to draw in detail> drawn in detail, powerful impacts, perfect character, lighting and style
   consistency."

## In the beats

- **Every figure named gets its own verbs.** A target is never just "a mech": it charges, fires back, scatters too late.
  Anything mentioned without an action stands still (s051, s052).
- **Fire has a direction and one named target** (s032, mid-1): "the two leading mechs raise their rifles up and to the
  right and fire at the big white space vessel in the upper right", never "fire toward the space vessels". Without one,
  the mechs shot at a mech between them and one exploded for no reason; the space vessels, given a group verb ("the
  fleet answers") in the last beat, did nothing.
- **The action starts on frame one when the shot is short on screen.** s032 plays 1.11 s: its beat 1 is the whole shot.
  Check the on-screen time in the plan before writing the beats.
- **Late arrivals get their action where they first appear,** and again where they're hit: targets that only enter in
  the last beat still stood in a line, waiting (s059, Battles 2-3 part 2).
- **Explosions near a mech write its damage** like any hit (s082-4's last part: the blast didn't touch it).
- **Every hit writes its consequence:** what cracks, what tears off, where it spins. "Cuts", "strikes", "hits" alone pass
  through (s053).
- **Gunfire** (Lati, Battle 1): each round leaves the muzzle in a bright trail; where it hits, sparks and armour burst off.
  Fire is named as visible events: muzzle flash, tracer trail.
- **A target that isn't in the plate is described by its look** ("a stripped grey skeletal mech with a glowing green
  core"); otherwise the model clones the shooter (s037).
- **Camera pinned to something physical,** with a roll direction per beat: "skims low beneath the mech's legs", "races
  alongside", "bolted to the cockpit frame". Near misses at the lens; something crossing the lens near the end gives a
  cut point.
- **Hits as "a brief hit-stop on contact" and "a one-frame white flash",** never "slow motion" (it freezes ~0.9 s).
- **Camera verbs, never "cut to":** a written cut invites the model to change shot.
- **Positive words only** (Lati): no "no", "not", "without", "never". The tool flags them.
- **"Space vessel", never the other word.** Designs named as the plate shows them; Gemini's are iridescent, never the
  other word for many colours.

## Expect

- Seedance 2.5 draws no held frames from "12fps"; held drawings, if wanted, are done in the cut.
- Takes often lose energy or reframe after ~2 s; Lati cuts at the point it stops working ("usable until ...").
- Watch the API key's own spending limit on OpenRouter (separate from the balance; it stopped Battles 2-3 at $20).

## Lati, 11 Nov (before the pilots and the cosmic zoom)

- **Cockpit damage spreads and gets worse,** never only flickering sparks: sparks become a burst panel, then fire, smoke,
  more lights going red, a crack across the canopy. Beat 1 is the first damage, beat 2 its cascade.
- **The battle outside a canopy is alive and progressing:** fighters swerving through tracer, a space vessel burning and
  breaking apart, explosions flashing into the cockpit; never a still backdrop (s092).
- **An enemy mech chasing something flies aerobatics while it shoots:** corkscrews, flips, evasive rolls, with the wildest
  camera and the most extreme angles (s087).
- **Beats:** "0-1s: from the first frame …", then "1-4s" (shots run ~1 s in Lati's cut; s032).
