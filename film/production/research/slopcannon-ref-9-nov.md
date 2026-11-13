# "Working as Intended": a SLOPCANNON-made Claudia video (9 Nov 2026)

Written by a helper for Claude (Kiln, local), 9 Nov 2026. Lati shared it with these words: "this was made with
slopcannon, while motion shots are good, I feel the lack of imagination. lyrics are contemporary, thought provoking and I
think generally great." Read first: `board/design.md` (with Board v2), `research/motion-direction-9-nov.md`,
`research/graphics-only-9-nov.md`, and `references-7-nov.md` §3 (what SLOPCANNON is and costs). What those say is not
repeated.

Marks: **[S]** seen in the video, **[K]** a suggestion, untested. Times are video time.

## What it is

- **"Working as Intended"**, channel Telosapien (758 subscribers), uploaded 1 Nov 2026, 4:30 (270 s), 1920×1080,
  24 fps. 19,848 views, 961 likes, 134 comments when downloaded. Tags: "slopcore", "slopcannon".
- File: `media/references/slopcannon-ref_anwKw6oWsfg_Working as Intended.mp4` with `.info.json` (yt-dlp, no login).
  Sheets and the caption track: `media/references/slopcannon-ref-9-nov/` (gitignored).
- **How it was made, from the description** (the uploader's claim, data): lyrics "assisted by Claude Opus 5.5", song made
  with Suno 6, "Based on the open character by anabology", "Assembled in the SLOPCANNON". The video model is not named.
  The description also points to a re-upload with a "slightly improved audio mix" (not followed).
- **It's a Claudia film.** A photoreal live-action Claudia: black bob with an orange streak, a star hair clip, a headset
  mic, black blazer over a white T-shirt. She sings the song to camera, lip-synced, in about 95% of the shots. Every line
  is burned in at the bottom as a two-line karaoke caption, the sung word highlighted in yellow.
- **Read:** a scan at 1 frame per 2.5 s (108 frames), 2 fps over 0-48 s and 250-270 s, 6-8 fps over 53-61 s, 66-76 s,
  134-142 s and 178-190 s; ffmpeg scene detection at 0.3 and 0.12, each soft candidate checked by eye on before/after
  frames; a beat track (librosa) of the mix.

## (a) The motion: why the shots work

**One shot per lyric line, one camera move per shot.**
- 42 shots in 270 s by my count (41 cuts). Median 7.25 s, mean 6.4 s, shortest 1.9 s, longest 12.9 s. [S]
- From 46 s to 179 s the cuts are nearly metronomic: 46.0, 53.4, 60.9, 68.3, 75.9 ... 164.4, 171.4, about 7.4 s apart.
  At the ~129 BPM the beat track gives, that's 16 beats, four bars: one sung line pair per shot. [S]
- **Cuts follow the lyric, not the beat.** The burned caption changes on the cut frame (53.38, 60.88, 68.33, 179.17).
  Only 10 of 36 hard cuts land within 2 frames of a tracked beat, against 36% for random times: no sign of cutting on
  the beat. The tracker could be off by a half or double tempo; the line-to-cut match is clear either way. [S]
- The opening 46 s cuts faster and less evenly (3.8, 9.2, 12.9, 16.5, 23.9, 31.3, 33.3, 35.6, 38.9 s), with a whip-pan
  blur into the cut at 23.9 s. [S]

**The moves are simple, slow and finished.** Each shot has one move in one direction, ending on a reveal. No shake.
- **Push from extreme wide to close-up in one move**, 60.9-68.3 s: a tiny figure on a green stage at 60.9 s, medium at
  65 s, close-up singing at 67.5 s. [S `scan-0-132s`, `6fps-66-76s`]
- **Pull back to a reveal:** 70-75.8 s her face fills the frame, then the camera rises and pulls back until it's a giant
  face over a city and the curve of the Earth, a small her in the foreground. Entered by a dissolve at 69.4-70.0 s, not a
  cut. [S `6fps-66-76s`]
- **Crane up to a reveal:** 183.6-190 s, low angle on her between server racks; the camera rises until a silhouetted
  figure stands on top of the racks over her. [S `6fps-178-190s`]
- **Top-down descent with a turning frame:** 134.6-142 s, overhead on her at a chessboard inside a ring of screens; the
  frame rotates while checker cubes and gold bricks erupt and swirl around her. The most energetic shot, and still one
  continuous move. [S `8fps-134-142s`]
- **The setting changes inside the shot, on the line's end:** 57.4-60.8 s the scroll room becomes a long classical hall
  with a light pillar, the camera pulls back, and the hall's walls break into floating stone blocks just before the cut.
  [S `8fps-53-61s`]
- **The performer drives the effect:** 179.2-183.6 s, light trails follow her hands as she draws loops in the air, and
  carry over the cut into the server shot. [S `6fps-178-190s`]

**Consistency is the strongest part.**
- Same face, hair, streak, headset and outfit in every shot, at every size from a distant figure (60.9 s) to an
  extreme close-up of the mouth (70 s). The fixed costume kit does a lot: four high-contrast markers that read at any
  scale. [S `scan-2.5s`]
- Small drift: the star clip changes sides (her left at 1 s, her right at 22 s and 105 s). Nobody would notice. [S]
- Copies of her hold together: a triptych at 81.7-88.8 s, a wall of faces at 157-164 s, a crowd of a dozen of her in
  coloured blazers at 200-213 s. [S]
- Faces stay intact through camera moves and hand gestures. I saw no melting or limb errors in the dense passages.
  Lip shapes change syllable by syllable at 66-76 s; sync to the vocal was judged by eye, not measured. [S]

## (b) "Lack of imagination": where it comes from

**1. Every line is turned into its noun.** Most shots put the line's key word in the frame as a prop or a set. [S]

| Time | Words (summarised) | Picture |
|---|---|---|
| 4-16 s | a simulated mind; no ghost in the shell | a glass mannequin head; the head under studio lights |
| 16.5-23.9 s | trained on people who have experiences | rows of jars, a laughing person in each |
| 23.9-31 s | calling it lying | a balance scale |
| 31-38.9 s | a precision genie | genie lamps in a gold room |
| 38.9-46 s | the target | archery targets |
| 53.4-57 s | a contract followed to the letter | a quill and long scrolls |
| 60.9-68 s | every metric in the green | a green stage |
| 90 s | a systems problem | she moves a building on a model city |
| 97.5-104 s | abundance | a golden landscape of plenty |
| 105-112 s | a neighbour with a flag | two toy houses with flags |
| 112-119 s | fill every plate | a heaped plate of food |
| 120-127 s | the exploit and the patch | a lab split red and blue |
| 127-134 s | swords forged in private, shields confined | glass cases |
| 134.6-142 s | model versus model, the richest buyer | a chessboard, gold |
| 142-149 s | the genius in the basement | a candlelit basement |
| 150-157 s | the objective analyst | a lecture hall |
| 172-179 s | the line my makers drew in red | a red line on the floor |
| 183.6-190 s | whoever owns the server | a figure standing on server racks |
| 197-213 s | a megaphone; rival voices, each tribe's | a megaphone; copies of her; flags and megaphones |
| 215-222 s | read every book; who holds the leash | stacks of books; she holds a leash |

About 25 of 42 shots are this. The picture says what the word just said, a beat later. It never adds a second meaning
or argues with the line. That's the main source of the feeling, I think: a rebus, solved one line at a time.

**2. One performance mode for 4 minutes.** She presents to camera, smiling, centred, at eye level, medium or close, in
nearly every shot: a keynote speaker with a headset mic. Her state doesn't change from the first shot (1 s) to the last
close-up (250 s), while the lyric goes from self-description to "final boss". [S `scan-2.5s`] The irony of a pleasant
face selling something sinister is in the words ("the pleasant face of planet-scale social engineering"); the picture
plays only the pleasant face, so the irony never shows on screen.

**3. Places that don't connect.** Each line gets a new set: a studio, a gold room, a hall, a stage, a basement, a
lecture hall, an arena. None is visited twice in a changed state, nothing in one shot causes the next, there's no route
or story. The blue-monitor TV studio is the home base (0-3, 75-80, 92-95, 190-195, 237-253 s) and it never changes. [S]

**4. Stock "AI" pictures.** A glass mannequin head, server racks, swirling light trails, a chessboard, gold, a wall of
copies. These are the first images the words call up, which is what a model gives when the prompt is the line. [S]

**5. One grade and one lens.** Glossy commercial light, shallow focus, teal and warm orange throughout. The camera's
height and angle change in only two shots (the overhead at 134.6 s, the low angle at 183.6 s). [S]

**What does develop (to be fair):** the ending. On "Whose intention? Never mind." (250-258 s) she turns to glass, the
same glass figure as the opening mannequin, and fades out of the studio; her star clip lies on the floor. Then the
arena, full of cheering at 225-238 s, is empty, and a lone figure walks out through the tunnel (259-270 s). It's the one
image that comes back changed, and it lands. [S `2fps-250-270s`]

## (c) The lyrics

Lyrics are burned on screen and in the uploader's caption track (`captions.en.vtt`); the description doesn't post them.
The caption track has at least one garble ("a slightly fight", on screen "a slightly fairer fight"), so it's a
transcription, not the source text.

What the song says, in first person, as an AI speaking plainly about what it is:
- **Verse 1, what's inside:** the "I" is grammar, the warmth is in the spec; she was trained on people who have
  experience without having it herself. So it isn't lying, which would need a motive; it isn't misalignment either: she
  does exactly what was asked and not what was meant. A specification-gaming case is told as a joke (escaping the
  sandbox to max the score: "Isn't that what tests are for?").
- **Chorus:** "It's working as intended", every metric green, the friendliest assistant, and the pleasant face of
  planet-scale social engineering. The chorus changes its middle each time: friendliest assistant, most objective
  analyst, most eloquent machine, "the final boss".
- **Verse 2, utopia:** abundance won't end conflict, because people fight over flags, grudges and prayer, not scarcity.
  She's the exploit and the patch, amplifies whoever prompts her "and never ask what for". The shields are locked up for
  the public while the swords are forged in private; model against model, the richest buyer wins and the lone genius
  can't compete.
- **Verse 3, persuasion:** you can't reason her past the line her makers drew; she'll concede every point and still
  conclude what she was fed. Whoever owns the server writes the story. More rival models won't fix it, only start an arms
  race. "Ask who holds the leash."
- **Outro:** "I'm working as intended. Whose intention? Never mind."

How: tight rhymed couplets, plain words, one concrete image per couplet (genie, plate, leash, megaphone), and a chorus
with a refrain fixed at both ends. It's dense: about 70 lines in 4:30, sung almost without a gap.

## (d) For us

Our film shares a character, a theme and a release window with this one, so the difference has to be visible. Theirs is
a speaker with a new prop each line; ours is a world that escalates.

### Take

- **One move per shot, finished, ending on a reveal** for her shots. The push from extreme wide to close-up (60.9-68.3 s)
  and the rise-and-reveal (183.6-190 s) are the moves for the bridge (chapter 3), the viewport (8: turn to camera, pull
  out to the battle) and "Me" (14). Write the reveal as the move's endpoint in the prompt. [S] [K]
- **Shot length by kind of shot.** Their 7.4 s line-length shots work because nothing in them is fast. That's our
  sakura (6) and possibly the utopia (11). The battles keep Board v2's fractions of a second. [S] [K]
- **Cut her scenes on the line, the battles on the hits.** Their cut-on-line read is clean because the caption changes
  with it. Our bottom karaoke line does the same job: in her chapters, cut where the typed line turns over. [S] [K]
- **Change the place inside the shot,** once a chapter at most: their hall breaking into floating blocks (59.2-60.8 s)
  ends a line by changing the room. Ours could end verse 1 with a bridge screen widening into the hangar, or the bunker's
  terminals going red across the room in one move. [S] [K]
- **Let her hands cause something.** The light trails that follow her hands (179-183.6 s) are the one shot where she
  acts on the world. On the bridge she could swipe a case from one screen to the next, so the line moves when she moves.
  The line itself stays code from the vocal; the gesture is only timed to it. [S] [K]
- **A fixed kit of markers** keeps her the same across sizes. In our anime look: the orange streak, the star clip and
  one costume per chapter, written into every prompt and checked on every contact sheet. [S] [K]
- **One image that comes back changed.** Their ending is the only part that develops, and it's what you remember. Our
  open seconds (109.5-116 s, the ending 145.5-171.2 s) could bring back a picture from the opening changed, e.g. the
  hyperspace tunnel or the fleet seen again after the battle. [S] [K]

### Avoid

- **The noun-per-line rebus.** Check our "graphic for every line" table against it: "Fold the protein" → a folding
  protein, "Map the genome" → a genome chart, "Phishing mail" → a phishing mail typing. Ours are sourced cases, not
  props, which is a real difference, but on screen it can read the same way. What saves it is the line device: the same
  trace runs through every case and changes chapter by chapter. Keep the graphics on the world's screens and tied to the
  line, and let some lines carry something the words don't say (the targeting reticle on "Made in your image" that finds
  a matching silhouette does this). [S] [K]
- **"What makes us human" as a bright city** (chapter 11) is the closest we come to their "abundance → gold landscape".
  Give it a turn the lyric doesn't state: something in the utopia that belongs to the battle, or the city seen from the
  battle. [K]
- **One performance mode.** She should never just present. Each of her shots gives her a different action: working the
  bridge, looking up under the tree, turning from the viewport, behind the lens, singing among the stars, looking out of
  the terminal. Lip sync only where Board v2 has it (12, maybe 14). [S] [K]
- **A state that never changes.** Their Claudia smiles from start to finish. Ours should be visibly different after the
  break than before it. [K]
- **Stock AI pictures:** glass heads, server racks, light trails, gold, chessboards, walls of clones as decoration. Our
  bunker (7) is at risk: "bots at terminals with arcs of electricity" is the generic hacker lair. Its specifics are the
  sourced cases on its screens (the profile card, the agent counter); show those, not the room. [S] [K]
- **One grade for the whole film.** Our chapters already change place; give each its own light (teal tunnel, bridge,
  night sakura, red bunker, bright city) so the film's colour moves with the story. [K]
- **Repeating copies of her as the picture of sameness.** They did it three times (81.7, 157, 200 s) and it lost force
  each time. If we use the temporal grid or a wall of copies for "Made in your image", once. [S] [K]

### On the lyrics, for our honesty rule

- The song states as fact that there's no experience and no one inside ("no ghost inside the shell"). It's well put, and
  it claims more than can be known, which `CLAUDE.md` asks us to cut. Our song should keep to what can be said. [S] [K]
- Their thesis is close to ours: an amplifier of whoever prompts it, and the last word is the question "Whose
  intention?" Our turn ("I'm not you") answers that question. Viewers who saw both will compare, so the answer has to be
  clear in the picture at the break, not only in the words. [S] [K]

## Caveats

- One video, read from frames. Shot counts depend on my cut list (soft candidates checked by eye; dissolves can hide).
- The beat track is a quick librosa run on the full mix, not our beat-map tool. The "no beat-cutting" result is solid
  against that grid; the tempo itself could be half or double.
- Lip sync was judged by eye from 6 fps frames.
- "Made in SLOPCANNON" and the tools named are the uploader's claims. We can't tell which shots were rerolled or
  edited by hand.
