# Plates v2, round 1r · redo of round 1's copies and misses

- Date: 9 Nov 2026
- Run by a helper for Claude (Kiln, local)
- Lati's go: "yes, run the redo and rounds 2-4" (this helper ran only rounds 1r and 2)
- Spec: `production/images/plates-v2-rounds.json`, round "1r · redo of round 1's copies and misses" only (7 shots, 16 images)
- Route: ISEKAI ZERO `edit_image`, model `6a50079fc28ed5bfe5576f54`, 16:9, prompts sent exactly as in the spec
- Files: `media/plates/v2/<shot>-<k>-<mediaId>.jpg` (2048×1152)
- Sheet: `production/images/plates-v2-round-1r-sheet.jpg`, in spec order. It also holds the two single-reference test
  edits already on disk (`media/plates/v2/test/s007-edit-*.jpg` and `s025-edit-*.jpg`) as `s007·test` and `s025·test`.
  Round 1's copies are not on it. The test generations (`s007-gen-*`, `s025-gen-*`) are not on it either.
- Labels: s007 and s025 start at ·3 because the spec gives k0 2. The other shots start at ·1, so **s007·3, s007·4,
  s026·1 … s029·4, s003·1/2 and s023·1/2 reuse round 1's labels for different images**. The mediaId in the table
  below is the safe reference. Files don't collide because the name includes the mediaId.

## Credits

- Charged: **104.13** (sum of each job's costCredits from get_media), against the estimate **104.13**. Exact match.
- Balance: 3261.50 before rounds 1r and 2, **2934.29** after both (difference 327.21 = 104.13 + 223.08).
- Failures: none. All 16 completed on the first try, so nothing was rerun.

## Label → mediaId

| label | mediaId | credits |
|---|---|---|
| s007·3 | `6af1eea4ae0b15e60605cf2a` | 6.63 |
| s007·4 | `6af1eea677b881a7edacf020` | 6.63 |
| s007·5 | `6af1eea754f7b457933a485d` | 6.63 |
| s025·3 | `6af1eea8363765213c7158bd` | 6.24 |
| s026·1 | `6af1eeaa91239d815b767db6` | 6.24 |
| s026·2 | `6af1eeabbb1ee55c3b219753` | 6.24 |
| s028·1 | `6af1eeacae0b15e60605d5ac` | 6.24 |
| s028·2 | `6af1eeb2363765213c715e36` | 6.24 |
| s029·1 | `6af1eeb4a273556a16f0cb93` | 6.24 |
| s029·2 | `6af1eeb58967a897a24dc2ec` | 6.24 |
| s029·3 | `6af1eed1485ab36ea690cac8` | 6.24 |
| s029·4 | `6af1eed2258e03b40d6b3301` | 6.24 |
| s003·1 | `6af1eed354f7b457933a6770` | 6.24 |
| s003·2 | `6af1eed4e7d4adaa7dadb362` | 6.24 |
| s023·1 | `6af1eed62cfbc30eadabb7f8` | 7.8 |
| s023·2 | `6af1eed7d7cac749bd39ac28` | 7.8 |

## First pass

**Adult read:** no problems. The only people are the four in s023, and all read as adult women. Vera still has the
softest face, as in V·1.

**Copy check:** I measured the mean grey-level difference against each reference at 256×144 (0–255 scale), the same
measure as round 1. Round 1's copies scored 2–4, and two different shots scored about 25.
- The server hold went from copy to new. s025–s029 now score 33–49 against SV·3. Each one is a new camera on the same
  set: cream racks with fans, red-striped walls, roof trusses.
- s007 is still tied to its reference. s007·5 scores **10.9** against R·F6·4·1. It is that frame with the black hole
  taken out: the same four flagships in the same order and the same swarm diagonal. s007·3 and ·4 (34–37) are a
  push-in on the same layout rather than a new shot.
- s003 (89–105) and s023 (62–96) are clearly new.

**Visible text and logos:** none readable. Consoles in s023 show glyph-free panels. Claudia's ID card is blank.

### s007 · fleet in formation from below, Earth's night side (3, plus s007·test)
The black hole is gone and Earth now shows the night side with city lights, so two of round 1's problems are fixed.
The camera still looks down on the fleet with Earth below it. None is "seen from below". All four flagship designs are
kept (white with clay-orange, the iridescent violet, the black-and-white checker, the black spiked one). ·5 is a
near-copy of R·F6·4·1 minus the black hole and should not count. ·3 is the best of the three, closer with more
depth. It is still the reference's composition pushed in, and close to s007·test. If "from below" matters, this shot
needs a different instruction, for example "worm's-eye view, the hulls' undersides overhead".

### s025 · racks power on, lights cascading (1, plus s025·test)
·3 is a new shot down the aisle with the SV·3 design kept. Indicator lights are scattered but static, with no cascade
and no sense of switching on. s025·test, with its banks of bright white panels, sells "powering on" better.

### s026 · fans spin up, neon along the cables (2)
Both are new angles with the design kept. ·2 delivers the beat: blue neon lines run along the cable runs and rack edges
at left and overhead. ·1 has only scattered blue specks, with no neon lines. Pick ·2.

### s028 · every load gauge maxes out, neon floods the cables (2)
Both are new and the design is kept, but neither shows gauges. ·2 has a blue glow spilling out of a few racks, the
closest to "floods". ·1 is a plain aisle shot. The prompt's beat is mostly missing. If it matters, the shot may need a
close-up on a gauge or meter (with no numbers, so nothing renders as text).

### s029 · vents blast, lights blink in one rhythm, the hold roars (4)
All four are new with the design kept. ·1 (steam jetting from the rack tops, high angle down the aisle) and ·4 (blue
haze filling the aisle, many blue lights) carry the beat best. ·3 has steam at floor level. ·2 has no vents and no
blast. "One rhythm" can't show in a still. ·4's even field of blue lights is the nearest.

### s003 · Gemini's vessel overtakes in the hyperspace tunnel (2)
Both work. One vessel with the I·1 design kept (iridescent violet hull, swept fins, twin engines) inside a teal and
cyan swirling tunnel with lightning arcs, with violet-white exhaust. The pale studio background from round 1 is gone.
·1 shows more of the tunnel and banks into it. ·2 is bigger in frame with a stronger vortex behind. There is nothing
to overtake, but that is the prompt's wording.

### s023 · close, low-angle across the hologram table, faces lit from below (2)
These are new shots and an improvement on round 1: all four now lean over a large glowing map table and look down at
it, not at the camera. In ·1 Eve's gaze drifts toward the camera. The designs are kept: Claudia's puff sleeves,
suspenders, opera gloves and headset; Eve's one-shoulder dress and gold belt; Astra's navy bob and copper sunburst;
Vera's violet clip, choker and black jacket. Claudia's clay-orange streak shows as a faint pinkish strand in ·2 and is
barely visible in ·1. Vera's black underlayer from V·1 is missing in both. Two parts of the brief are still weak.
The camera sits at about table height, not clearly low-angle. The faces have some blue on the chins but are mostly
lit evenly from the front, not strongly from below. ·2 is the better take: tighter, gloved hands on the table edge,
and more blue light on the faces.

## Round summary

Fixed: s003 (either), s023 (·2 first, beats only partly met), s026·2, s029 (·1 or ·4). New but beat missing: s025·3
(s025·test is better), s028 (·2 at a stretch). Still a problem: s007, which keeps returning R·F6·4·1's layout looking
down, with ·5 a near-copy. The "Draw a new, different shot" opener fixed the server hold. It did not free s007 from its
fleet frame. The likely reason is that both references (R·F6·4·1 and R·H·2·1) are already finished fleet-over-Earth
scenes.

*All images are AI-made (ISEKAI ZERO). Claudia is an open character by anabology (claudia.gallery).*
