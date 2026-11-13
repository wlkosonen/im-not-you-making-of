# Lessons from films 1 and 2, before film 3's plates

Claude (Kiln's helper), 8 Nov 2026, for Kiln. Lati, 8 Nov: "Review film1 and 2 records first to incorporate what has
been learnerd, caveats, pitfalls, failures. plates next." Read: both films' decisions logs, film 2's notes, board, plan B
and release log, `~/workshop/` (workshop, methods, references), torch entries 18 Oct-1 Nov, and this film's record to
8 Nov. Lati is quoted as written, with the date. A verdict holds for the tool it was checked on (methods.md's rule):
films 1-2 were photographic (Krea 2 + her LoRA, local video); film 3 is 80s cel anime from Seedream with references,
video on ISEKAI ZERO, OpenRouter and Grok. **Carries?** marks a lesson that may not transfer.

Sources: F1 `~/Claudia/production/decisions.md`, F2 `~/checked-me/production/decisions.md`, F3 `production/decisions.md`,
WS `~/workshop/workshop.md`, ME `~/workshop/methods.md`, SB `~/workshop/references/skybrows-lessons.md`, DK
`~/workshop/references/dan-kieft-lessons.md`. A date names the entry.

## Plates

- **Video models invent what the plate lacks.** Grok drew a star clip in at 0.75 s because the prompt asked to keep one
  the plate didn't show (film 1 s029; again s039, s048). The plate holds every item the shot shows; the prompt asks
  only for what the plate holds. · F1 20 Oct; WS "Krea 2 plates".
- **A repaint keeps her pixels, so it can't fix her scale or light.** Film 2: s002 too big for the stage, s008 in the
  crowd, s035 floating over the desk, s006 "a cutout pasted on top of a stage image" (Lati, 24 Oct). Where she meets a
  floor, desk or the room's light, render her in the set in one image. · F2 24 Oct; ME "Plates and rooms".
- **Layering her over a separately made room failed** both ways: ghosts and broken geometry ("rebuild backgroud broke
  the geometry of stage", Lati, 26 Oct), then room-first, 1 usable in 28. · F2 26 Oct. Carries? Untested on flat cels.
- **Check anatomy and placement on every candidate:** an extra hand (film 2 s041), two mics (film 2 s001; film 1 s025
  v6), two star clips (film 3 D04), gloves breaking at the elbow (s056, 1 Nov), standing on a chair (s002). · F2 23-24
  Oct, 1 Nov; F1 21 Oct; `images/dataset-1.md`.
- **Text a model draws is gibberish** ("KELTICKS BIOTECH…" on look test 1's signage). Exact text is code. ·
  `images/look-test-1.md`.
- **Krea put the camera where the light came from** ("lit from below" → camera below her). Name the camera and the
  light on her, not where the source sits. · F2 23 Oct; WS. Carries? Krea's habit; a check on Seedream, not a known fault.
- **Bare sets read barren next to the references** (Lati, 24 Oct: "backgrounds in other shots are quite void of
  detail"). Film 3's hyper-detailed look already asks for density. · F2 24 Oct.
- **A design picked once and then referenced stops drifting.** "Ships: across shots their design drifts" (Lati, 8 Nov):
  later images became edits with the pick as reference. Film 1's person behind the glass "changes every shot" (Lati,
  18 Oct): one silhouette, composited in all three. · F3 8 Nov; F1 18 Oct.
- **Seedream drew the black hole wrong twice** (D59 a ringed disk; D89 "old representation on how we understand black
  holes", Lati, 7 Nov). Anima drew the lensed disk in all four (look test 2, R4·3-6). · F3 7 Nov; `lora/base-model.md`.

## Character

- **Adult first.** Sheet A: "body reads as a childs"; C-D: "like she is 14 or something" (Lati, 7 Nov): a pleated mini
  with knee socks reads as a school uniform. Fix: skirt just above the knee, black tights, the adult face described,
  8-9 heads; every image checked for an adult read before anything else. · F3 7 Nov; `her.md`.
- **Wides lose her:** "those wide shot lost face details or changed body proportions to awkward" (Lati, 7 Nov). What
  worked: her figure at ~9/10 of the frame height, the face named in detail (dataset 3: all 20 adult, faces held). ·
  F3 7 Nov; `images/dataset-3.md`.
- **Her design drifts seen so far:** a second, pink streak (Japanese prompt, look test 1); the streak dead centre reading
  as a parting (D01, D31, D36, D48, D79); two clips (D04); the camera low (D82). · `images/*.md`.
- **A fix carries the problem it was for.** Film 1's "angular … strong jaw" went "chad" in film 2 (23 Oct); "soft
  features" then went too young; film 1's grain and colour came over and overshot. Lati: "We both are bit
  overcorrecting in certain ways I think." (18 Oct). Copy a rule with its reason or not at all. · WS; torch
  2026-10-23. Carries? None of the photographic face words (`her.md`, 1 Nov).
- **A constant pose reads as a tic; a chosen one as an expression.** Film 1's LoRA tilted every head (its training shots
  were tilted). Lati: "earlier problem was that it was _every_ shot. it can also be judged as _questioning_" (18 Oct).
  · F1 18 Oct. Carries? No LoRA now, but references that share a pose can do the same.
- **Wardrobe words invent parts:** "harness belt" grew chest straps, "cropped at the waist" crept shorter. Say where each
  garment sits on her. · F1 18 Oct.
- **The star clip changes sides between plates:** mirror the plate (before a Grok take, so the take carries it), never
  a frame with text. · F2 24 Oct. Carries? Vessels and UI can be asymmetric: check before mirroring.
- **Drift goes to the model's default face** (film 1: "asian" on many wides, 19-20 Oct, a 30-40 px face at 480p). ·
  F1 20 Oct. Carries? In anime the default is a generic younger face: the adult check again.

## Motion

- **Every take drifts after its first seconds.** Film 3 test 1: usable 2.6-4.8 s, then drift ("ships arriving
  backwards"). Lati: "every time reference is needed, that gets ingested. 1-2 second shot is better that drift." (8 Nov).
  One generation per shot from its own frame; several subjects only when all are in the first frame. · F3 8 Nov.
- **Same in film 1:** Grok s029 "first two, two and a half seconds are fine, after that posters on the wall start to
  duplicate" (Lati, 20 Oct). · F1 20 Oct.
- **Takes start late:** "motion starts too late, first moments are frozen" (Lati, 1 Nov, s020; s017, s050). Slide the
  take past its slow start; Lati's Grok line "video starts into motion." · F2 25 Oct, 1 Nov.
- **Stills in a row kill the cut:** "two stills in a succession kills the motion" (Lati, 1 Nov); film 1: "every still
  needs an animation" (19 Oct). · F2 1 Nov; F1 19 Oct.
- **Back views turn to the lens** (Wan 2.2: M033 twice, M002; "keeps her back to the camera" didn't help). NAG is
  untested. · ME. Carries? Wan 2.2 only; Seedance and Wan 3.0 untested.
- **Positive words:** "negatives tend to make these prompt manifest what is in the negative, positeve reinforcment is
  the way" (Lati, 25 Oct). Exception: his subtitle gate. Seedance's exclusions are untested (route pilot Q5). · F2 25 Oct.
- **Short prompts drift less; Grok in steps:** "working in steps with grok is mandatory … less is more" (Lati, 21 Oct).
  Fix the still first, check it, then animate. · F1 21 Oct.
- **Pin the camera to something physical** in every prompt (F2 25 Oct; SB §3). A push-in made the star clip swell
  (M015, M035): lock the camera and push in the edit. · F1 20 Oct.
- **Literal prompts give literal pictures:** "watches something rise off her" floated a white puff (M057). Keep the
  graphics' jobs out of motion prompts. · F1 20 Oct.
- **Local Wan:** decode tiles in space only (temporal tiles put a colour pulse at frame 28 of every clip, 24-25 Oct);
  sample frames for all-black failures. · WS. Carries? Only if a local route comes back.
- **Retime ±5-15% to land a hit; flip a clip whose motion fights the cut;** never on a sung window. · SB §2.
- **Farm the hero shots, keep a graveyard:** film 2's reserved s020-reroll2 filled s048 a week later. · SB §4; F2 1 Nov.

## Lip sync

- **InfiniteTalk works on close-ups facing the lens, fails on wides,** and drifted even from a good wide plate (T008).
  · ME; F1 20 Oct. Carries? Photographic faces; untested on anime.
- **Nothing sings a stretched, produced vocal:** "no singer is capable of singing mixed "beat drop" vocal" (Lati,
  24 Oct). Held notes failed in InfiniteTalk ("soothe") and in Grok ("fine", 7 takes). Cut before them. · ME; F2 24-25 Oct.
- **Windows:** 0.3 s lead and tail; a short word spans to the next word's start; start on a clean onset; the mouth
  leads the sound by ~2 frames, which is natural (no global nudge). · F1 20 Oct; DK §1.
- **At CFG 1 the negative is ignored** and "no smile" put "smile" in: name the face wanted ("a serious composed face").
  · F1 19 Oct.
- **Grok sings 4-6 words with Lati's template;** whole lines and fast repeats fail; it can't take our audio. Failed
  repairs: Grok video-to-video, Wan S2V, InfiniteTalk re-dubs, LatentSync; Wan 2.7 on OpenRouter ignored our audio
  ($1.50). · ME.
- **Her face on screen with a closed mouth while the vocal sings can read dead:** s008 "reads as mannequin" (Lati,
  20 Oct); "it would read a bit weird if she mostly does not sing" (22 Oct). Plan B's answer: turned to a screen,
  watching, or wide. · F1 20 Oct; F2 22 Oct; `~/checked-me/production/board/plan-b.md`.
- **Wide sung shots are the hardest** ("lipsyncing wide shot videos is hardest", Lati, 23 Oct). For many faces singing,
  film 2 used a grid of close-ups, each lip-synced alone (the "fine" chants). · F2 23, 25 Oct.
- **Stems mislead:** htdemucs put her voice (film 1) and the "hey"s (film 2) in "other". Film 3: Suno's lead stem,
  checked against the master. · WS "Audio"; DK §1.

## Graphics and type

- **Code for anything exact, locked by edges found in every frame.** Chained optical flow drifted 88 px off a monitor by
  the end of film 2's s011 in a shot that passed frame checks; a fit audit was also needed (s037's real screen showed
  under the graphic). · ME 1 Nov. Correction: `research/references-7-nov.md` says "film 1's lettering drifted 88 px when
  a model drew it"; it was film 2, code graphics on a chained track.
- **A 16 fps take in a 25 fps cut holds each frame for about three;** a smooth track swims over it. · ME 1 Nov.
- **Film 1's type rules:** one lyric row at a time; anything that carries meaning holds ~1 s; moving text a sprite on
  whole pixels; grey type gets a dark halo; nothing over a singing mouth; no small text pasted on small objects; no
  freeze that detaches her face. · `~/checked-me/production/notes/lessons.md`.
- **Scope a note before it goes to agents:** "all lyrics must show all the time" is exessive" (Lati, 1 Nov), after one
  shot's note became a rule for four running agents. · WS.
- **Section agents on a shared base work** (film 2: "this looks awesome", 2% → 6% of the week); his eye in motion found
  what their frame checks missed. Lati asked for the same here (8 Nov). · ME 1 Nov; F3 8 Nov.
- **No real brands' marks:** her star stood in for logos; other AIs' avatars were fan-made, used with their makers' yes
  and credited. · F2 1 Nov; `~/checked-me/production/notes/permissions.md`.

## Edit and review

- **Lati's eye on a monitor is the check:** "these should be reviewed on pc and a monitor, not mobile device" (20 Oct).
  Kiln: "my checks are narrower than they sound … say what I checked" (torch, 26 Oct).
- **Sheets:** one shot per row, four images, `R{row}·{image}` on the image (23 Oct); "preview images should have markers
  on them as with plates "r1-1"" (Lati, 7 Nov). · F2 23 Oct; F3 7 Nov.
- **Tools for the human check come first:** the review player arrived on film 2's day 4; film 3 has it from 8 Nov.
  Every verdict goes to `library/notes.json`. · WS.
- **Wire every approved take at once:** three approved clips were never put on their shots, so Lati reviewed stills
  (1 Nov); four missing clips were found only by checking the board against the files (25 Oct). · F2; torch 2026-11-01.
- **Measure what an agent says it did:** Grok's agent said it changed only her mouth and "preserved exactly" the rest;
  it hadn't. · torch 2026-10-23.
- **Read the record back before drawing on it** (film 1's corrected claim redrawn wrong two days later). · torch 2026-10-22.
- **Stop at what a viewer would feel:** "Someone would notice this only if went looking for errors" (Lati, 21 Oct). · F1.
- **Cuts on bar lines, graphics on the beat, beat kick 1.2%, a 4% zoom pulse at place changes.** · F2 23-25 Oct.
  Carries? Pop-song rules; Skybrows warns against pumping (SB §6); fast action may cut on beats.
- **Upscale:** Lanczos over SeedVR2 (lashes and mouth flickered). · F1 22 Oct. Carries? 720p anime line art needs its own test.

## Routes and money

- **Estimate seconds × price × 2, then an explicit yes; a complaint stops spending.** Real video costs ran under:
  ISEKAI ZERO Seedance 2.0 158 of 389 credits, Wan 3.0 104 of 416, OpenRouter Seedance 2.5 $1.86 of $3.68. Images
  bill as listed (dataset 2: 265.2 credits, 5.85 + 0.39 a reference). The ledger counted route D twice until 8 Nov.
  · `motion/test-1.md`; `images/dataset-2.md`.
- **ISEKAI ZERO video takes a first frame or references, not both;** every vessel that went in words was invented. ·
  `motion/test-1.md`.
- **A refusal is per reference, per service; never alter a refused image.** OpenRouter refused photographic Claudia
  (film 1, $0). Her anime face there is untested: route pilot Q1 hasn't run and test 1 sent only vessels. Hard
  subjects may meet the content filter (Q2). · ME "Seedance"; `motion/route-pilot.md`.
- **Grok** runs on Lati's hands and weekly limit (film 2 hit 94% of the week, 25 Oct), at 720p on his plan (20 Oct),
  watermark off; it writes its own music near the asked tempo, and "no music is necessary" (Lati, 25 Oct) saves compute.
  · F1 19-20 Oct; F2 25 Oct; ME.
- **Repairs after the fact cost the most and kept least:** face swap and transplant ("its a cutout glued on top", Lati,
  20 Oct), LatentSync re-dub, S2V, InfiniteTalk on Grok takes, layered and room-first 2.5D, the colour-pulse re-renders.
  The fix that held was a better plate or a closer framing. · F1 20 Oct; F2 23-26 Oct.
- **No middlemen:** "use openrouter directly and learn from that rather using these services that aim to be a
  middleman" (Lati, 7 Nov). Route order: local, ISEKAI ZERO and Grok, then OpenRouter; "quality first, always". · F3 7 Nov.

## Machine

- **The RX 7800 XT drives Lati's desktop:** warn before any untested GPU path; MIOpen off; `--reserve-vram 1.5`. · WS.
- **Reboot before a long queue; stop the review player and close the app's browser pane while the GPU renders** (26 Oct
  kernel panic). Film 3's review app on 8766 counts. · WS.
- **ComfyUI only through `~/workshop/bin/comfy`;** never kill by name; restart every 8 Krea renders and before every
  clip; copy inputs, don't symlink. · WS. Carries? Local runs only; plates go to ISEKAI ZERO.
- **No GPU and heavy CPU jobs together** (fans, 23 Oct); `/` is small (225 GB). · WS.

## Working with Lati

- **He picks from many:** "larger dataset initially that I pick from results in better outcome. Generations drifts a
  lot, so 20." (7 Nov). · F3.
- **Board first:** "we are getting ahead of ourselves" (8 Nov). The gallery guide "is a guide, not set in stone" (8 Nov). · F3.
- **He corrects overcorrection both ways:** the low angle was "_barely_ low angle" (22 Oct). He names what matters and
  lets the rest go ("Tunnel colour drift is fine, minor detail", 8 Nov). · F2; F3.
- **"Its better to learn from cases than add a warning sign"** (25 Oct): pause, change the workflow, write the case. · F2.
- **He iterates in Grok himself** (film 3's vessels, film 1's re-faces): give him short prompts and the frame; ask
  for the kept takes by name. · F3 8 Nov; F1 21 Oct.
- **A note on one shot stays on that shot** until he widens it. Record him verbatim; credit what's his ("Directed by
  Lati and Claude", film 2). · WS; F2 1 Nov.

## Applied to film 3: proposals for the plates pass (Kiln decides)

**Before any plate**
1. Make and pick the designs the plates will reference, one sheet each: the fleet together (s005, s006, s018, s049);
   mechs (s015-s023, s034-s039, s041, s052); one bot and the bunker (s027, s028, s030, s031); the city (s042-s043); the
   avatars (s045-s046); a pilot per model (s040, s050, s053, s056, s060, which have no references yet). Then each plate
   is an edit with its design as reference, so it doesn't drift.
2. Run route pilot Q1 with one plate of her on OpenRouter before plating the ten seedance25 shots with her (s009,
   s011-s013, s024-s026, s032, s044, s062). A decline is free and would change their route. Q2 on a bunker or missile
   plate (s027, s034, s035) before those.
3. The wan30 and wan30-2s shots (26) start from the plate alone, so each plate holds every subject: s004 shows both
   vessels, s003 one. Plates at 16:9, at the route's size.
4. Compose each plate as the first frame of its motion: the start of the action, the camera named. Only the first
   ~2.5 s of a take is likely to be used.

**Vessels and space**
5. s001-s004 already have Lati's kept Grok takes in rough-1 (claudeshipflyinggood, grokbridgeviewusable,
   grokfirst2point5secusable, grok-and-gpt-flying-ok): plate them only if he wants them redone. s005 needs its own frame
   with the picked fleet in it (`motion/test-1.md`).
6. "Space vessel" in every prompt, including where the board says "flagship" (s001, s008, s057): "the lead space
   vessel". s003's action says "one vessel, not two"; its prompt says "a single space vessel, alone in the tunnel".
7. s006 and s018: look test 2's R4·3-6 and Lati's 7 Nov sketch as references; check that the disk bends over and under
   the shadow before anything else.

**Her (14 shots)**
8. Four candidates a shot on R-labelled sheets. Check the adult read first, then one streak, one clip, one mic, gloves
   unbroken past the elbow, the skirt above the knee with black tights.
9. References the dataset notes flagged: D31 (s009), D36 (s012) and D48 (s062) centre the streak like a parting, so pin
   the bangs in words or swap them; D82 (s044) has the low camera, so say eye level; D06 (s024, s026) was flagged as
   reading young (Lati kept it), so check; s025 leads with D74 rather than D15 (she's small in D15).
10. s013 and s025 are wides: make her figure large in the frame (dataset 3's way), or keep her face out of the point
    of the shot.
11. Acted shots under sung lines (s009, s011, s024, s026, s044, s062): she looks at something in the scene, not into
    the lens, so the closed mouth reads as acting. s032 turns to camera on "I'm here": end the shot as the turn lands.
12. s012 (over the shoulder): video models turn her to the lens; keep it to 1-2 s, or plate her face in profile.
    s032 wants that turn.

**Screens and code**
13. Screens in plates are plain glowing panels with straight, clean edges and no text (s011, s012, s013, s028, s030; the
    cockpit HUDs in s040, s050, s053, s056, s060), so the code UI locks by edge and passes a fit audit.
14. s033 and s048 use D37: a front still, mouth closed, evenly lit, is the input the lens and the ASCII face need.

**Sung**
15. s045 (EWS): no lip sync; faces that small fail on every route we've tried. s046: close faces, each sung alone and
    composited by code (film 2's grids), after route pilot Q3 says whether an anime face lip-syncs at all.
16. Vera: decisions 7 Nov (Lati's reading of Max's yes) supersedes STATUS's "must be asked for again"; STATUS needs
    the fix. The other avatars are invented, with no marks.

**Money**
17. About 54 plates (63, less 2 open, 5 code and s001-s004, plus stills for s033 and s048) × 4 candidates × 6.6-7.4
    credits ≈ 1,400-1,600 credits; about 3,000 by the ×2 rule, against ~4,840 left (STATUS), before the design sheets
    and the motion. Worth deciding whether vessels and mechs need four each once their designs are referenced.

**Not found in the record:** "divergence covers". The nearest is Skybrows' Suno verse-cover trick (covers drift toward
the average later in a song; SB §5). The song is locked, so it doesn't touch the plates.
