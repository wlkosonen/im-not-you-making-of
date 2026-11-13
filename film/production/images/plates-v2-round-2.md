# Plates v2, round 2 · launch, battle 1, sakura, bot farm

- Date: 9 Nov 2026
- Run by a helper for Claude (Kiln, local)
- Lati's go: "yes, run the redo and rounds 2-4" (this helper ran only rounds 1r and 2)
- Spec: `production/images/plates-v2-rounds.json`, round "2 · launch, battle 1, sakura, bot farm" only (14 shots, 34 images)
- Route: ISEKAI ZERO `edit_image`, model `6a50079fc28ed5bfe5576f54`, 16:9, prompts sent exactly as in the spec
  (s042's Japanese prompt included)
- Files: `media/plates/v2/<shot>-<k>-<mediaId>.jpg` (2048×1152)
- Sheet: `production/images/plates-v2-round-2-sheet.jpg` (labels s031·1 …, in spec order)

## Credits

- Charged: **223.08** (sum of each job's costCredits from get_media), against the estimate **223.08**. Exact match.
- Balance: 3261.50 before rounds 1r and 2, **2934.29** after both (difference 327.21 = 104.13 + 223.08).
- Failures: none. All 34 completed on the first try, so nothing was rerun.

## Label → mediaId

| label | mediaId | credits |
|---|---|---|
| s031·1 | `6af1eefe363765213c7189c0` | 7.02 |
| s031·2 | `6af1eeff8967a897a24df10a` | 7.02 |
| s032·1 | `6af1ef00e4ffef00e9b44931` | 6.63 |
| s032·2 | `6af1ef02958d42a9dca96f2b` | 6.63 |
| s033·1 | `6af1ef03eb6bb3c2db9998b2` | 6.63 |
| s033·2 | `6af1ef06258e03b40d6b5dc1` | 6.63 |
| s033·3 | `6af1ef07a963791a5c7a9e68` | 6.63 |
| s033·4 | `6af1ef092cfbc30eadabe0b9` | 6.63 |
| s034·1 | `6af1ef0a485ab36ea690f727` | 6.24 |
| s034·2 | `6af1ef0bde4f3abdafaf754d` | 6.24 |
| s035·1 | `6af1ef32485ab36ea6911c3e` | 6.63 |
| s035·2 | `6af1ef36a963791a5c7ac0a3` | 6.63 |
| s036·1 | `6af1ef38258e03b40d6b8454` | 6.63 |
| s036·2 | `6af1ef3a8b03de9e0c8ef14c` | 6.63 |
| s037·1 | `6af1ef3be1ec69208b9af3f0` | 6.24 |
| s037·2 | `6af1ef3c54f7b457933acdf1` | 6.24 |
| s038·1 | `6af1ef3fb7e269c633320476` | 6.63 |
| s038·2 | `6af1ef408b03de9e0c8ef40c` | 6.63 |
| s038·3 | `6af1ef4277b881a7edad6410` | 6.63 |
| s038·4 | `6af1ef434004962801030129` | 6.63 |
| s041·1 | `6af1ef7277b881a7edad7eb0` | 6.24 |
| s041·2 | `6af1ef73e1ec69208b9b23eb` | 6.24 |
| s042·1 | `6af1ef75460b53f4c28e03eb` | 7.02 |
| s042·2 | `6af1ef76460b53f4c28e04a6` | 7.02 |
| s044·1 | `6af1ef777eb8065c825b30ee` | 6.63 |
| s044·2 | `6af1ef79f0e43b457fd0b07f` | 6.63 |
| s046·1 | `6af1ef7aeb6bb3c2db99e86d` | 6.24 |
| s046·2 | `6af1ef7ce7d4adaa7dae2708` | 6.24 |
| s047·1 | `6af1ef7de6d0977a2d351c29` | 6.24 |
| s047·2 | `6af1ef7e650e747cd4c39b53` | 6.24 |
| s049·1 | `6af1ef9254f7b457933b0a0d` | 6.63 |
| s049·2 | `6af1ef94e1ec69208b9b3532` | 6.63 |
| s049·3 | `6af1ef96e1ec69208b9b37de` | 6.63 |
| s049·4 | `6af1ef988967a897a24e69c6` | 6.63 |

## First pass

**Adult read:** no problems. The only person is Claudia in s042. She reads as an adult woman in both takes: tall,
long neck, long legs, an adult face. In ·2 her face is a little rounder and softer than in ·1, but she still reads as
an adult.

**Copy check** (mean grey-level difference at 256×144, 0–255; round 1's copies scored 2–4, distinct shots about 25):
- **s041·2 scores 11.6 against U1·1, a near-copy of the city plate.** It has the same towers, dome and flyers in the
  same places, plus a railing and debris streaks. s041·1 (41.9) recomposes with sakura framing, but it is still U1·1's
  city from nearly the same viewpoint.
- s047·2 (19.1) and s047·1 (26.5) keep VT·3's layout: a brain vat in the left foreground and a row going back to the
  right. They are redrawn, not copied, but they are the reference's composition.
- s044, s046 and s049 against the bunker plates K1·1 and K2·2 score 25–34. All are new shots on the same set.
- Every mech shot (s031, s034–s038) scores 87–127 against its design sheets. They are clearly new.
- s032 and s033 against S4c·4 and the fleet frames score 34–50. They are new, though s033 reuses R·F6·4·1's black hole
  at top centre.

**Visible text and logos:** none readable. Keyboards in s044 have blank keys. Panels and terminals in s044, s046 and
s049 are plain glowing red. The small lit sign in s042·2's park is blank.

### s031 · frontier mechs streak away from the flagship's hull (2)
New shots. The mechs fly off a big grey-white hull on exhaust trails with beam swords out. Claude's off-white
clay-orange mech, ChatGPT's black-and-white mech with the white halo rings, and Gemini's iridescent knight are all
recognisable. ·1 adds a fourth, dark spiky mech, so it reads as "all four makers". ·2 has three, with bigger, cleaner
figures. The hull is grey and lacks the flagship's clay-orange lines, so it may not read as the flagship.

### s032 · wide from orbit, swarm lifting off far below as tiny points (2)
Night-side Earth with city lights and the blue rim, as asked. But the swarm is not "tiny points far below". In ·2
large S4c-style mechs fill the foreground on exhaust trails, and in ·1 they are mid-size. Both also add the frontier
fleet (flagships, R·H·2·1) across the top, which the prompt doesn't ask for, probably from the second reference.
·1 is closer to the brief.

### s033 · extreme wide battlefield, swarm rising toward the fleet, black hole far off (4)
All four have the swarm rising from Earth's night side toward the fleet, with tracer streaks between them and a black
hole with its accretion disk bent over and under the shadow. The black hole sits top centre, large rather than "far
off", in the same place as in R·F6·4·1. ·3 has the clearest two-sided read (fleet above, swarm below). ·1 has the
most dynamic swarm.

### s034 · swarm mech lunges blade first at the camera, dutch angle (2)
These work. The S1 swarm mech (white and dark frame, green eye and core) lunges with its blade arm forward, with sparks
and debris and Earth below. ·2 has the stronger foreshortening and dutch tilt, but Earth is on its day side. ·1 is
darker, with the blade swinging across rather than straight at the lens.

### s035 · Claude's mech parries the swarm mech's blade, sparks (2)
These work. The off-white mech with clay-orange lines blocks with a beam sword against the S1·2 mech's blade, with a
burst of sparks at the contact point and Earth and space behind. Both designs are kept. ·1 has the bigger spark burst
and the clearer blade contact.

### s036 · Gemini's knight and the insect swarm mech face off, one tracer line between (2)
The designs are kept (M2's iridescent knight with its beam sword, S3's insect-like mech with blade arms) above Earth.
·2 has the long single tracer line across the gap, as asked. In ·1 the tracer is a short streak in the middle. In both
the two stand in design-sheet poses side by side, which reads a little like a lineup rather than a standoff.

### s037 · Claude's heavy mech, missile swarm across the battle, explosions (2)
The M1·B heavy mech's design is kept (cannon, shoulder pods, clay-orange stripes), with missiles and explosions behind
it. ·1 is in space and matches the battle. **·2 is set over a burning ruined city under clouds**, so it is not in
space and would break continuity.

### s038 · huge explosion between a black-and-white mech and a swarm mech, angular debris (4)
All four deliver it: M3's black-and-white mech with its sword on one side, an S2 swarm mech on the other, a big
explosion between them, and Earth below. ·1 has the "white-hot core" (a white flash). ·2–·4 are orange fireballs with
sharp angular chunks flying out, ·2 most clearly. ·4 has a purple sky that differs from the rest of the battle.

### s041 · her view: debris falling across the sky, sakura branches in frame (2)
**·2 is a near-copy of U1·1 (11.6).** ·1 adds sakura framing but keeps U1·1's view. Both have streaks falling across
the sky. **Both are bright daytime, while s042, the reverse shot of the same moment, is at night.** That is a
continuity break whichever take is picked. The prompt doesn't say night, so a re-run would need "at night" added.

### s042 · Claudia under the sakura at night, rising from the bench and looking up (2)
These are new shots and the scene is right: a night park, full sakura framing the frame, glowing debris streaks
crossing the sky, and city lights behind. Her design is kept: puff-sleeve white shirt, black pleated skirt, suspenders,
black opera gloves, tights, the star clip and the thin headset. The clay-orange streak is not visible in either take.
Her bangs are straight in ·1 but slightly parted in ·2. She is already standing beside the bench, not rising from it.
Her mouth is closed, as asked. ·1 looks up at the sky with her head tilted back, which is the stronger read. In ·2
she looks up more mildly.

### s044 · ECU of the bot's thin metal hands typing, lit red from below (2)
These work. The thin, jointed dark-metal hands type on a keyboard over a plain glowing red panel, with cables and
machinery behind. The B1 design is kept. ·2 is closer and redder, with keys lit from below. ·1 is wider and shows
more of the arms.

### s046 · wide: a wall of plain red panels, bots in silhouette at terminals, steam, tesla arc (2)
These work. A tall red grid wall with no text, rows of silhouetted bots with red eyes at terminals, steam, a gantry,
and violet-white tesla arcs overhead. It is clearly the K2·2 bunker, seen from a new angle. ·1 has more steam and a
cleaner wall.

### s047 · vats of cyborg brains wired to the farm, arcs between them (2)
The VT·3 design is kept: green tanks, a wired brain with implants, red glow at the base, arcs crackling between tanks.
**Both keep VT·3's composition, ·2 more closely (19.1).** They are usable only if repeating the set plate's framing
is acceptable.

### s049 · row of gaunt bots at red terminals turn their heads to camera, red slits, arcs (4)
All four are new shots in the K1·1 bunker with the B1 bot design (faceless domed heads, red sensor slits, skeletal
bodies) at plain red terminals, with blue tesla arcs behind. In ·2 and ·4 the foreground bots face the camera
directly, the clearest "all turn at once". ·1 has a mix of facing and turning. ·3 is the widest row, with most heads
toward the camera.

## Round summary

Strong: s034, s035, s038, s044, s046, s049, s042·1. Usable with a note: s031 (hull lacks flagship colours), s033
(black hole large, not far off), s036·2, s037·1. Problems: s041 (·2 is a near-copy of U1·1, and both are daytime
against s042's night), s032 (the swarm is large and close, not tiny far below, and an extra fleet is added), s037·2 (a
city, not space), s047 (VT·3's framing). The copy problem now shows up only where the single reference is a finished
scene plate (U1·1, VT·3). The opening line reduced it, but U1·1 still came back almost unchanged.

*All images are AI-made (ISEKAI ZERO). Claudia is an open character by anabology (claudia.gallery).*
