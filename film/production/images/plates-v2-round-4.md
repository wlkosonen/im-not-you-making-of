# Plates v2 · round 4 · battle 3 to the end

9 Nov 2026 · run by a helper for Claude (Kiln, local) · Lati's go: "yes, run the redo and rounds 2-4"

Spec: `plates-v2-rounds.json`, round "4 · battle 3 to the end". Model 6a50079fc28ed5bfe5576f54, 16:9, edit_image with
each shot's refs and prompt exactly as written. Files: `media/plates/v2/<shot>-<k>-<mediaId>.jpg`. Sheet:
`plates-v2-round-4-sheet.jpg` (spec shot order; the two missing takes are left out).

## Credits

- Charged: **375.96** (sum of costCredits over all jobs; failed jobs were refunded and charged 0) against the round's
  est **390.00**. The 14.04 difference is the two takes that failed twice (7.80 + 6.24).
- Balance at the end (get_balance): **2215.13** (2934.29 before round 3; rounds 3+4 = 719.16).

## Failures

Five jobs failed on the provider side ("The generation failed on our side", refunded) and were rerun once with the
same inputs:
s076-1, s076-3, s079-4, s080-1, s080-2. The reruns of s076-1, s079-4 and s080-1 completed. **Two failed again and
were not run a third time: s076-3 (6af1f4bb71749553dbe9401c) and s080-2 (6af1f4dc3d598a1685a1d20a).** So s076 has 3
takes and s080 has 1.

## Images

The last column is the mean absolute pixel difference against each reference image at 128x72 (0-255). Under ~15
means a near-copy. Reruns are listed under the same label below the failed first attempt.

| Label | mediaId | Status | Credits | Mean diff vs refs (0-255) |
|---|---|---|---|---|
| s076-1 | 6af1f2fe958d42a9dcac642d | failed | 0 (refunded) |  |
| s076-2 | 6af1f2ffae0b15e6060935a2 | completed | 7.8 | M1·C·1:125.7 M2·C·2:109.5 M3·C·1:112.6 M4·C·2:113.0 S3·2:120.5 |
| s076-3 | 6af1f300eb6bb3c2db9c980b | failed | 0 (refunded) |  |
| s076-4 | 6af1f30277b881a7edafede7 | completed | 7.8 | M1·C·1:129.6 M2·C·2:111.5 M3·C·1:113.4 M4·C·2:113.2 S3·2:124.1 |
| s077-1 | 6af1f303568df6968f24b884 | completed | 6.63 | M4·C·1:99.5 S3·2:112.7 |
| s077-2 | 6af1f3088b03de9e0c919285 | completed | 6.63 | M4·C·1:95.0 S3·2:106.4 |
| s078-1 | 6af1f30a3d598a1685a0e1ff | completed | 6.63 | M2·C·2:103.7 I·1:106.3 |
| s078-2 | 6af1f30b91239d815b79ed74 | completed | 6.63 | M2·C·2:96.9 I·1:97.4 |
| s079-1 | 6af1f331e7d4adaa7db0d0c5 | completed | 6.63 | M1·C·1:119.0 S3·1:117.8 |
| s079-2 | 6af1f3323d598a1685a100f9 | completed | 6.63 | M1·C·1:125.5 S3·1:123.2 |
| s079-3 | 6af1f333e6d0977a2d38146f | completed | 6.63 | M1·C·1:111.3 S3·1:112.0 |
| s079-4 | 6af1f33778e70d68ce66c8e3 | failed | 0 (refunded) |  |
| s080-1 | 6af1f338f78085fa4d9671df | failed | 0 (refunded) |  |
| s080-2 | 6af1f33c858417a214b7fa8e | failed | 0 (refunded) |  |
| s081-1 | 6af1f33e4dcfb550e5dd7405 | completed | 6.24 | M4·C·2:105.2 |
| s081-2 | 6af1f340d028dedc626ea06b | completed | 6.24 | M4·C·2:119.8 |
| s082-1 | 6af1f341485ab36ea6945752 | completed | 6.24 | S2·1:90.1 |
| s082-2 | 6af1f343858417a214b7ff88 | completed | 6.24 | S2·1:94.1 |
| s082-3 | 6af1f367650e747cd4c6bb7e | completed | 6.24 | S2·1:100.5 |
| s082-4 | 6af1f3687eb8065c825e04f3 | completed | 6.24 | S2·1:94.3 |
| s084-1 | 6af1f36ae6d0977a2d3844b1 | completed | 6.24 | P1·B·2:61.9 |
| s084-2 | 6af1f36bbb1ee55c3b2537a1 | completed | 6.24 | P1·B·2:57.2 |
| s086-1 | 6af1f36c78e70d68ce66efcd | completed | 6.24 | P4·A·1:43.8 |
| s086-2 | 6af1f36d2c1f13f82477dc44 | completed | 6.24 | P4·A·1:45.3 |
| s087-1 | 6af1f37091239d815b7a3a7e | completed | 6.63 | M3·C·1:102.8 S3·1:108.4 |
| s087-2 | 6af1f371568df6968f252fe7 | completed | 6.63 | M3·C·1:102.2 S3·1:109.6 |
| s090-1 | 6af1f373e1ec69208b9e79ec | completed | 6.24 | P1·B·2:59.1 |
| s090-2 | 6af1f374958d42a9dcacbc0c | completed | 6.24 | P1·B·2:49.5 |
| s091-1 | 6af1f399858417a214b8453e | completed | 6.24 | P4·A·1:16.0 |
| s091-2 | 6af1f39a71749553dbe866db | completed | 6.24 | P4·A·1:52.2 |
| s092-1 | 6af1f39c363765213c74e68d | completed | 6.24 | P3·B·2:51.6 |
| s092-2 | 6af1f39da273556a16f49502 | completed | 6.24 | P3·B·2:51.9 |
| s093-1 | 6af1f39ebb1ee55c3b2560a1 | completed | 6.63 | M2·C·2:100.8 M4·C·1:101.0 |
| s093-2 | 6af1f39fd028dedc626ee660 | completed | 6.63 | M2·C·2:109.8 M4·C·1:100.0 |
| s094-1 | 6af1f3a1858417a214b84a23 | completed | 6.63 | S4c·4:50.9 R·H·2·1:56.3 |
| s094-2 | 6af1f3a2eb6bb3c2db9d1837 | completed | 6.63 | S4c·4:39.4 R·H·2·1:44.6 |
| s094-3 | 6af1f3a4bb1ee55c3b25635b | completed | 6.63 | S4c·4:33.9 R·H·2·1:40.7 |
| s094-4 | 6af1f3a57eb8065c825e31c5 | completed | 6.63 | S4c·4:44.0 R·H·2·1:50.9 |
| s095-1 | 6af1f3c8ae0b15e60609c920 | completed | 6.24 | R·F6·4·1:34.4 |
| s095-2 | 6af1f3ca2377e4b17622c58d | completed | 6.24 | R·F6·4·1:22.7 |
| s095-3 | 6af1f3cc7eb8065c825e4d0c | completed | 6.24 | R·F6·4·1:37.3 |
| s095-4 | 6af1f3cd485ab36ea694c10e | completed | 6.24 | R·F6·4·1:40.0 |
| s101-1 | 6af1f3d0f0e43b457fd373b9 | completed | 6.63 | SI·1:52.5 R·H·2·1:43.5 |
| s101-2 | 6af1f3d12c1f13f8247838bc | completed | 6.63 | SI·1:64.6 R·H·2·1:53.2 |
| s102-1 | 6af1f3d2e6d0977a2d38984d | completed | 6.24 | SI·1:40.3 |
| s102-2 | 6af1f3d4363765213c750426 | completed | 6.24 | SI·1:49.5 |
| s103-1 | 6af1f3d5f6b305b32b3749b4 | completed | 6.63 | M1·A·1:80.6 S1·1:77.1 |
| s103-2 | 6af1f3d6113f2d3d3fb23a15 | completed | 6.63 | M1·A·1:91.3 S1·1:87.3 |
| s104-1 | 6af1f3fbf0e43b457fd392a2 | completed | 6.24 | V1·1:129.4 |
| s104-2 | 6af1f3fe568df6968f25d85f | completed | 6.24 | V1·1:126.3 |
| s105-1 | 6af1f40071749553dbe8a979 | completed | 6.24 | R·F6·4·1:38.1 |
| s105-2 | 6af1f4013d598a1685a16cdb | completed | 6.24 | R·F6·4·1:35.8 |
| s106-1 | 6af1f402e1ec69208b9ed802 | completed | 6.24 | SI·1:43.9 |
| s106-2 | 6af1f404d7cac749bd3d9be2 | completed | 6.24 | SI·1:54.5 |
| s107-1 | 6af1f405568df6968f25de5a | completed | 6.24 | R·F6·4·1:31.7 |
| s107-2 | 6af1f4062377e4b17622f062 | completed | 6.24 | R·F6·4·1:34.2 |
| s107-3 | 6af1f4082377e4b17622f31f | completed | 6.24 | R·F6·4·1:17.6 |
| s107-4 | 6af1f409d7cac749bd3da31b | completed | 6.24 | R·F6·4·1:41.5 |
| s109-1 | 6af1f41af6b305b32b377a43 | completed | 7.02 | d74:52.1 d45:98.4 d72:74.4 |
| s109-2 | 6af1f41bd751c6089b77b238 | completed | 7.02 | d74:52.4 d45:99.0 d72:74.8 |
| s076-1 | 6af1f4ba958d42a9dcad9cb5 (rerun of 6af1f2fe958d42a9dcac642d) | completed | 7.8 | M1·C·1:114.6 M2·C·2:105.1 M3·C·1:103.8 M4·C·2:108.3 S3·2:112.6 |
| s076-3 | 6af1f4bb71749553dbe9401c (rerun of 6af1f300eb6bb3c2db9c980b) | failed | 0 (refunded) |  |
| s079-4 | 6af1f4d971749553dbe95a52 (rerun of 6af1f33778e70d68ce66c8e3) | completed | 6.63 | M1·C·1:123.7 S3·1:120.5 |
| s080-1 | 6af1f4da363765213c75add0 (rerun of 6af1f338f78085fa4d9671df) | completed | 6.24 | M3·C·1:112.9 |
| s080-2 | 6af1f4dc3d598a1685a1d20a (rerun of 6af1f33c858417a214b7fa8e) | failed | 0 (refunded) |  |

## First pass

**Near-copies:** none under 15. The closest are s091-1 (16.0 against P4·A·1) and s107-3 (17.6 against R·F6·4·1).
Both are new shots, but they stay close to their reference's layout and colours.

**Adults:** Claude's pilot (s084, s090) is a young man with a youthful face. He reads as a young adult rather than a
boy, but s084-2 looks the youngest; worth Lati's eye. Grok's pilot (s086, s091) is clearly adult. ChatGPT's pilot
(s092) is helmeted. Claudia in s109 is adult.

- **s076** New (3 takes). A dense dogfight above the night side with the frontier fighters and swarm mechs, tracers
  everywhere. s076-1 shows the most fighter types; s076-4 is so busy that it reads as noise.
- **s077** New. The jagged black fighter streaking through debris with swarm mechs; Earth below in s077-1. Design kept.
- **s078** New. The iridescent delta fighter rolling through a wall of fire, the iridescence kept. Very strong; one
  of the best images of the round.
- **s079** New (4 takes). The off-white clay-orange fighter racing through wreckage, swarm mechs close behind; all
  four takes are close to one another.
- **s080** New (1 take). The black-and-white fighter firing white beams forward, a ring of six engines blazing,
  Earth below. Matches.
- **s081** New. The jagged black fighter banking away from missile trails, angular debris, violet glow. Matches.
- **s082** New. A swarm mech blowing apart in a fireball with debris flying at the lens. s082-1/2 are the cleanest.
- **s084** New. Claude's pilot (white and orange helmet) gripping two flight sticks; matches. Cockpit screens show
  only abstract marks.
- **s086** New. Grok's pilot in spiked black armour, grinning; s086-2 pushes a fist at the lens. The throttle reads
  only in s086-1 (hand on a lever), and even there it is not clearly slammed.
- **s087** New. The black-and-white fighter and a swarm mech facing each other above Earth's curve, a thin line of
  light joining them. Matches; strong and clear.
- **s090** New. Claude's pilot close-up with sparks and red warning lights, damaged panels. Matches.
- **s091** New, but s091-1 is close to its reference (16.0). Grok's pilot with steam venting behind the seat; matches.
- **s092** New. ChatGPT's pilot (white helmet, blue visor); a cracked screen in s092-1, glass shards in s092-2.
- **s093** New. The iridescent and jagged black fighters spiralling with contrails twisting into a helix over Earth.
  Strong; s093-2 has the cleaner helix.
- **s094** New. A wide battle panorama of fleet and swarm over Earth. s094-1/4 bring in the black hole from S4c·4,
  which the prompt doesn't ask for (it may suit continuity with s058).
- **s095** New, though all four keep R·F6·4·1's fleet layout (22.7 to 40.0). Fast pass over the fleet; there is
  little sense of pulling up and away.
- **s101** New. Missiles rising from Earth toward the fleet; s101-2 awkwardly puts a ground silo in the same frame
  as orbit. Black hole in both.
- **s102** New. A wall of missiles passing the camera, but under a red ground-level sky, not in the battle.
- **s103** New, but set on the ground (a mountain desert and a ruined city) with missiles raining down. Claude's mech
  and a swarm mech are kept.
- **s104** New. The flagship with its turrets swinging and firing; design kept, clearly a space vessel. Strong.
- **s105** New. Missile trails arcing over Earth's limb into the fleet; matches, close to the fleet reference's layout.
- **s106** New. One missile filling the frame upright; s106-2 shows it launching. Matches.
- **s107** New (s107-3 close at 17.6). An orbital battle seen from above; s107-4 adds the black hole. Not much
  sense of zooming out compared with s095/s105, so the four shots look alike.
- **s109** New. Claudia under cherry blossom at night, looking up into white light, mouth closed; outfit, clip and
  streak kept. s109-1 is the better take (light on her face).
