# Plates v2, round 1 · intro to pre-chorus

- Date: 9 Nov 2026
- Run by a helper for Claude (Kiln, local)
- Lati's go: "B, run it in rounds by chapter."
- Spec: `production/images/plates-v2-rounds.json`, round "1 · intro to pre-chorus" only (14 shots, 36 images)
- Route: ISEKAI ZERO `edit_image`, model `6a50079fc28ed5bfe5576f54`, 16:9, prompts sent exactly as in the spec
- Files: `media/plates/v2/<shot>-<k>-<mediaId>.jpg` (2048×1152)
- Sheet: `production/images/plates-v2-round-1-sheet.jpg` (labels s003·1 …, in board order)

## Credits

- Charged: **242.58** (sum of each job's costCredits from get_media), against the estimate **242.58**. Exact match.
- Balance: 3528.26 before, **3285.68** after (difference 242.58).
- Failures: none. All 36 completed on the first try, so nothing was rerun.

## Label → mediaId

| label | mediaId | credits |
|---|---|---|
| s003·1 | `6af1eab9ae0b15e606030241` | 6.24 |
| s003·2 | `6af1eabaf78085fa4d8ff681` | 6.24 |
| s007·1 | `6af1eabbeb6bb3c2db968b45` | 6.63 |
| s007·2 | `6af1eabdf6b305b32b3437f5` | 6.63 |
| s007·3 | `6af1eabec3487999668fd7fa` | 6.63 |
| s007·4 | `6af1eac0b7e269c6332ed721` | 6.63 |
| s008·1 | `6af1eac4e7d4adaa7daac958` | 6.24 |
| s008·2 | `6af1eac5d7cac749bd36dfce` | 6.24 |
| s008·3 | `6af1eac854f7b457933735f5` | 6.24 |
| s008·4 | `6af1eaca78e70d68ce606426` | 6.24 |
| s009·1 | `6af1eaeca273556a16edf450` | 7.41 |
| s009·2 | `6af1eaeebb1ee55c3b1f0519` | 7.41 |
| s010·1 | `6af1eaef485ab36ea68dcbc2` | 6.63 |
| s010·2 | `6af1eaf18b03de9e0c8bdf93` | 6.63 |
| s013·1 | `6af1eaf2fe9e4046ce149158` | 6.63 |
| s013·2 | `6af1eaf47eb8065c8257f27d` | 6.63 |
| s016·1 | `6af1eaf598b7e40dbabe9b0c` | 6.63 |
| s016·2 | `6af1eaf74dcfb550e5da5581` | 6.63 |
| s018·1 | `6af1eaf8e7d4adaa7daae92b` | 7.41 |
| s018·2 | `6af1eaf978e70d68ce608d5a` | 7.41 |
| s020·1 | `6af1eb1e363765213c6e9fc1` | 7.8 |
| s020·2 | `6af1eb1f5969f6e2c2849698` | 7.8 |
| s020·3 | `6af1eb215969f6e2c2849a16` | 7.8 |
| s020·4 | `6af1eb23e7d4adaa7dab1358` | 7.8 |
| s023·1 | `6af1eb25858417a214b1755e` | 7.8 |
| s023·2 | `6af1eb28f0e43b457fcd0b90` | 7.8 |
| s025·1 | `6af1eb29f6b305b32b348c02` | 6.24 |
| s025·2 | `6af1eb2b8967a897a24b2da0` | 6.24 |
| s026·1 | `6af1eb2c5969f6e2c284a21d` | 6.24 |
| s026·2 | `6af1eb2d8967a897a24b2fd4` | 6.24 |
| s028·1 | `6af1eb42858417a214b1849f` | 6.24 |
| s028·2 | `6af1eb448612c62a321c4bad` | 6.24 |
| s029·1 | `6af1eb45c3487999669034d6` | 6.24 |
| s029·2 | `6af1eb4777b881a7edaab97b` | 6.24 |
| s029·3 | `6af1eb48568df6968f1e76bc` | 6.24 |
| s029·4 | `6af1eb49f1df4d362a2ccf1f` | 6.24 |

## First pass

**Adult read:** no problems. Every person in s009–s023 reads as an adult woman. Vera has the softest, roundest face of the four, as in her reference V·1, but she still reads as a young adult. The personnel in s020 are small background figures and read as adult crew.

**Biggest problem: some shots copy their reference.** A shot whose only reference is a full scene or composition comes back as almost exactly that reference. Across that shot's takes the prompt's action is ignored. I measured the mean grey-level difference against the reference at 256×144 (0–255 scale). Two different shots (s010·1 against s013·1) differ by 24.8.
- s025, s026, s028 and s029 (10 images) against SV·3: 2.0–3.9, and s029·1 at 7.3. These are effectively ten copies of the set plate.
- s007 (4 images) against R·F6·4·1: 3.2–3.8. These are four copies of the design frame.
- s003 against I·1: 28–31. The ship is redrawn in a new pose, but it keeps the reference's pale studio background.
That is 14 of 36 images (88.92 credits) with little or nothing new. With this model, a single scene reference plus an action line behaves like "return the reference". These shots need a different approach, such as a text-only generate, a crop or angle instruction, or a character or prop added so the model has to recompose. That is Kiln's call.

**Visible text and logos:** no readable text or logos anywhere. Monitors and pads show pseudo-UI glyphs only. Claudia's white ID card at her hip comes from D31 and is blank at this size. The flagship hull has orange stripes and no markings.

### s003 · Gemini's vessel overtakes (2)
Both takes show one vessel with the iridescent exhaust, and the design matches I·1 (purple-iridescent hull, forward swept fins, twin engines). Both keep the reference's flat pale-grey background, though, so there is no space: no stars, nothing for it to overtake. Neither can be used as a plate as it stands. ·2 is the better pose for "overtakes" (banking, nose forward).

### s007 · fleet in formation from below, Earth's night side (4)
All four are near-copies of R·F6·4·1, including its black hole at the top. The camera looks down on the fleet with Earth's lit blue day side below, which is the opposite of the "seen from below, night side behind" in the prompt. The black spiky craft from the reference are still there; Kiln should check whether those count as the "mechs" the prompt says not to show yet. The design is kept only because the frame is the reference. The prompt is not met.

### s008 · flagship bow passing over camera (4)
The off-white hull with clay-orange lines, the panel lines and the turrets are all kept well. None is the shot asked for: each is a three-quarter view of most of the ship, not the bow passing directly overhead and filling the frame. ·1 comes closest, with a low angle on the belly and the hull filling most of the frame. ·2 sits against clouds and sky, so it looks like it's in atmosphere, not space. ·3 and ·4 have stars, but the whole ship sits in frame like a profile shot.

### s009 · Eve, Astra, Vera around the orb (2)
This shot works. All three are correct: Eve has the one-shoulder dress, gold belt and parted bob with no bangs; Astra has the navy bob with bangs and the copper sunburst halter; Vera has the platinum bob with the black underlayer, violet clip, choker and black jacket over a white tee. They have pads, pipes, monitors and the orb. ·2 is the only image in the round where the orb clearly has a brain inside, and it's the wider, more readable frame. ·1 is the closer group, with pads in hand.

### s010 · Eve at the orb, working a pad (2)
Eve's design is kept and she is working a console pad in both. The orb lights her only weakly, since the orb's light isn't really falling on her face. The background is the same RP·3 framing used in s013 and s016 (same column, same camera), so these three singles will cut as one locked-off angle. ·1 is the closer, stronger frame.

### s013 · Astra at the orb, data streams in her eyes (2)
Astra's design is kept and both frames are good portraits. The "data streams in her eyes" beat is missing: her eyes are ordinary green or blue with no reflected data. ·2 has her hand on the orb, which gives a gesture to animate.

### s016 · Vera at the orb, violet choker light (2)
Vera's design is kept (clip, black underlayer, jacket, choker). The choker has a small violet stone but no visible glow, so "the violet light of her choker" doesn't come through. She is standing near the orb rather than at it, and nothing in the frame connects her to it.

### s018 · orb lights up, streams climb the walls, avatars lean in (2)
This shot works best of the people shots. All three lean in, the designs are kept, and electric-blue streams crawl up the walls and pipes. The orb shows network lines, not a clear brain. ·1 has a stronger "lean in" with the faces close to camera. In ·2 the orb is more central.

### s020 · command centre, four around the map hologram, personnel on the sidelines (4)
All four take the prompt correctly: a map hologram table, crew at consoles on the sidelines, and Claudia, Eve, Astra and Vera together. Claudia's look comes from D31 (puffed sleeves, suspenders, black opera gloves, star clip, headset). The clay-orange streak is faint, a thin warm strand in the fringe at most. Kiln should check whether that's enough. ·1 is the most "working": Claudia's gloved hands are on the hologram and the others lean in. ·2, ·3 and ·4 are more of a lineup, and in ·4 everyone faces camera.

### s023 · faces lit from below by the hologram (2)
The designs are kept, but neither take is lit from below. The faces are evenly front-lit and the four stand in a line looking at camera, like a cast photo. In ·1 the hologram is barely in frame. The prompt's lighting beat is not met, and these read as posed, not caught.

### s025 · racks power on, lights cascading (2)
These are near-copies of SV·3: the same dim hold with a few indicator lights. There is no cascade and no "powering on". Not usable as a distinct shot.

### s026 · fans spin up, neon along the cables (2)
These are near-copies of SV·3. ·1 adds a few thin red and blue lines on cables at upper left, which is the only nod to "neon". Not usable as a distinct shot.

### s028 · every load gauge maxes out, neon floods the cables (2)
These are near-copies of SV·3. There are no gauges and no flood of neon.

### s029 · vents blast, lights blink in one rhythm (4)
These are near-copies of SV·3. ·1 differs most (7.3), but the difference is subtle, and there are no vents or blast visible.

## Round summary

Usable now: s009 (·2 or ·1), s010·1, s013 (either), s018 (either), s020 (·1 first). s016 and s023 can be used with the beat missing (no choker glow; no underlighting). s003, s007, s008 and the whole server-hold run (s025–s029) don't show what the prompt asks. s007 and s025–s029 come back as the reference itself. Before rounds 2–4 are sent, check which of their shots have a single scene or design-frame reference, because they will probably behave the same way. A count from the spec: 5 of 14 shots in round 2, 13 of 19 in round 3 and 14 of 24 in round 4 have a single reference. Four shots (s095, s105, s107, s073) use the same R·F6·4·1 or R·H·2·1 fleet frames that s007 copied. Not every single-reference shot copied: s008 (V1·1) and s003 (I·1) were redrawn. The copying showed up where the reference is already a finished 16:9 scene.

*All images are AI-made (ISEKAI ZERO). Claudia is an open character by anabology (claudia.gallery).*

## Single-reference test (9 Nov, Kiln)

Lati: "yes, run the test." 4 images, 24.18 credits; sheet `plates-v2-test-sheet.jpg`, files `media/plates/v2/test/`.
s025 and s007 as edits that open with "Draw a new, different shot ... the reference only shows what it looks like" and
as plain generations. The edits made new shots and kept the designs (SV·3's racks; all four flagships, no black hole,
Earth's night side); the generations made new shots but lost the designs (other racks; a different flagship lineup).
So: edits stay, and every world prompt now opens with that line (`plates-v2-rounds.json`, `plates-world.json`,
`plates-v2.json`).
