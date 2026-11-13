# Three references from Lati (7 Nov 2026)

Claude (Kiln, local). Lati's words are in `decisions.md`, 7 Nov, "Dataset 2: Lati's picks; three references".

## 1. "Runaway Training" by LordVuvuzela (youtu.be/o5d1RP7lvZs)

"Runaway Training - Claude Opus 5.5 Music Video (Fully code generated)", 3:41, 1080p30. Downloaded 7 Nov
(`media/references/runaway-training-o5d1RP7lvZs.webm`); one frame per 6 s laid out and read.

- **What it is:** a real-time 3D scene in code (low-poly models, neon emissive edges, bloom, particles), most likely
  a browser engine (Lati: "code and java"). The idea is the title: a runaway train (the training run) racing on a
  track through a neon city, then into space, ending on a ring of light.
- **Why it reads as immersive with few true shots:** the camera never stops. ffmpeg finds only ~14 hard scene changes
  in 3:41; the rest is one flying camera along the track, so the motion itself carries it. Light, particles and bloom
  move even when the camera slows.
- **Text does the storytelling,** set in the world: billboards and boxcars ("THE FRONTIER", "EDGE CASES", "COMMONS",
  "HYPE"), a phone in a hand scrolling a feed, news tickers ("BREAKING … LABS BID FOR BIGGEST DATACENTER", "Shutdown
  test: model said no", "Eval failed: deception 31%", "Weights exfiltration attempt"). Exact, legible, on theme:
  the thing image and video models can't do.
- **Same subject as ours:** the AI race, told from inside. Worth knowing it exists.

For our toolbag (Kiln's proposal, nothing decided): code for the layers that must be exact, generated video for the
rest.
- **The break (1:18.7):** the voice-interface eye's oscillator, driven by the real vocal stem in code, composited over
  the red lens with her face behind it. Exact sync for free.
- **"Me" (~1:56):** her face as ASCII, rendered in code from one of the dataset images, typing itself in on the beat.
- **Verse 1 screens and verse 2 terminals:** the sourced cases as real text, code-rendered and composited onto the
  generated screens (film 2's code lettering slid 88 px off a monitor in s011 when tracked by chained optical flow; `workshop/methods.md`: track by edges found in every frame, and audit the fit).

## 2. Skybrows, "The Ultimate Stress Test of Ultimate Destiny" (x.com/Skyebrows/status/2118750011890802939)

30 s, 1080p24, made on Dreamina (ByteDance), "Best of 4 tries". Clip downloaded 7 Nov
(`media/references/Skyebrows-2118750011890802939.mp4`); prompt (pasted by Lati from the replies) in
`research/skybrows-ultimate-showdown-prompt.md`, 1,735 words. Read one frame per second.

- **It's one generation:** "30-second continuous shot, no cuts." The "cuts" you feel are scale snaps and whip pans
  written into the prompt. The character holds (red cardigan, silver hair, sabre) across all 30 s.
- **How the prompt is built:** global rules first, then a timeline. FORMAT (2.5D: painted 3D + hand-drawn 2D effects,
  palette), VIEWPOINT RULES ("Never straight-on, never level, never symmetrical"; dutch 15-45°, extreme
  foreshortening, scale snaps), MOTION RULES ("Nothing is ever static"; every swing hits a target; every explosion gets
  a dodge; every jump has a push-off point; slow motion only twice; hit-stop, smears, impact flashes), SUBJECT,
  SETTING, SHOT SEQUENCE in 5 s blocks, CHARACTER ENTRANCES, ATMOSPHERE. Every rule is stated as "every moment".
- **What makes the motion believable,** by his own rules: causes. Push-off points, a dodge for every blast, contact
  for every swing. Action with a reason reads as weight.
- **What not to take:** the cast is recognisable pastiche; our "no logos" rule and recognisable-character policy keep
  that out.
- **For us:** the long dogfight run 1:56-2:25 (29 s) and the choruses (~9-10 s each) fit this build: one continuous
  generation per section, written as rules + a timeline on the song's beats. Seedance 2.5 on OpenRouter takes 4-30 s
  (`motion/route-pilot.md`): 30 s at 720p ≈ $6.90 a try; at his best-of-4, ≈ $28 for one usable 30 s, more than the
  $20 left on OpenRouter. A 10 s chorus test first.

## 3. SLOPCANNON (slop.cc)

Read 7 Nov 2026: home, `/faq`, `/for-agents`, `/wiki/features`, `/wiki/animation`, `/wiki/prompting`,
`/wiki/ai-video-prompting`.

- **What it is:** an "AI music video workstation": song + references + idea → a Producer chat plans timed scenes,
  generates a clip per scene, rerolls single scenes (earlier takes kept), assembles the cut with the song; captions
  timed to sung words; can restyle your own uploaded footage.
- **Models: not named anywhere** we read. "One reference pool per project, with a different subset in every scene" for
  consistency. Start frames, clip length and lip sync: not stated.
- **Price:** "Quality 2K at eight Cannon Credits per finished second"; standard packs "about $0.222 per finished
  second, or $13.33 per finished minute". A first pass charges the timeline length; a reroll only that scene; failed
  renders aren't charged. A full pass of our 2:51 ≈ $38. For scale: Seedance 2.5 on OpenRouter was $0.23/s at 720p
  (`motion/route-pilot.md`, 1 Nov); SLOPCANNON claims 2K for about the same, but we can't tell what model it is.
- **MCP:** `https://api.slop.cc/mcp`, streamable HTTP, 56 tools, browser sign-in for Claude Code. Billable actions,
  upload rights, the budget and a review of the first scene need human confirmation ("Nothing billable fires without
  scoped approval").
- **Rights:** you confirm rights to songs, images and likenesses before generating; "AI generation does not create
  those rights for you."
- **Prompting wiki:** 134 guides, mostly general film craft. The video prompting page: subject + one visible verb,
  then setting, framing, camera (path, framing, endpoint), light; one event per shot; with a start image, prompt only
  what changes; change one factor at a time. It cites Google's Veo guide and Runway's Gen-4 guide. Nothing anime-specific
  about motion prompts; the anime pages (cel, limited animation, sakuga, mecha) are craft notes.

Kiln's read: for us it's a wrapper whose model we can't see, so we'd lose the control that made film 1 and 2 work
(our own start frames, our LoRA, the real vocal for lip sync). Worth one cheap test only if the clips Lati saw beat what
we get from Seedance or Grok directly; the price per second at 2K is its interesting part.

**Decided, 7 Nov (Lati):** not used. "looks like indeed we use what free credits we have on ISK0 and use openrouter
directly and learn from that rather using these services that aim to be a middleman."

## 4. Vera, "Vera - After the Bump" by Max Pelletier (youtu.be/ybPoZDRx8e0)

4:44, downloaded 7 Nov (`media/references/vera-after-the-bump-ybPoZDRx8e0.webm`), one frame per 7 s read. Max's yes to a
cameo: "Sure! No problem." (1 Nov, `~/checked-me/production/notes/permissions.md`); Lati, 7 Nov: the question named no
film, so a couple of seconds of her likeness in film 3.

- **What makes her Vera:** a platinum, near-white blunt bob with heavy bangs; one violet hair clip on her left side; a
  black choker with a small violet light; a dark jacket over a cream or white top; violet as her one accent colour
  (the captions highlight words in violet too). Photographic, mostly black and white turning warm and golden by the end.
- **Her world:** the "@grok" thread is her frame (the video opens on a violet cube under tagged replies), so she reads
  as Grok's voice in the AI-music scene, in Max's telling.
- **For us:** an 80s cel version keeps the silhouette (white bob, violet clip, choker light) and drops the
  photographic finish. Natural places: one of the avatar stars at 1:45, or a face among the frontier fleet.

## 5. "FOOM NONSTOP - A Claude Pop Video" by Gradient Descat (youtu.be/ia5JMQQ9NZo)

Shared by Lati 8 Nov: "Graphics used iin this is really smooth and relevant. Song is catchy, but graphics made by claude
are carrying the majority of the weight. Also the song itself is ai history condenced." 4:32, 1080p60, downloaded to
`media/references/foom-nonstop-ia5JMQQ9NZo.webm`; one frame per 5 s read; ffmpeg counts 146 hard cuts (one every ~1.9 s).

- **The graphics are the subject, in the medium of each era.** AI history in order, each moment drawn as the object it
  lived on: punched cards and Ada (1843), "Hello, world" on a teletype, ELIZA on a terminal, a perceptron diagram as a
  paper figure, a funding ledger, 1986 on an index card, a scaling-law chart, a GPU at 91 °C, AlphaGo's move 37 on the
  board, proteins folding, a Claude Code permission prompt ("Do you want to proceed?"), a kill switch that turns out to
  be a sticker, "human in the loop 6%", and an ending of "All tests passed".
- **Type lives inside objects, not as subtitles:** a ticket, an index card, a stamp, a dot-matrix sign, a terminal
  line, a sticker. Lyrics surface as one or two words a shot, set into the thing on screen.
- **Real specifics:** dates, figures, named milestones; the facts carry the jokes.
- **A person is intercut** (photographic, about a third of the time), but the UI carries the meaning.
- **Callbacks:** counters and the test suite recur and pay off at the end.

For our overlays (Kiln's proposal, nothing decided):
1. Each line's graphic is a real object of our world in the 80s anime UI style (bridge consoles, vector CRTs, dot-matrix
   signs, cockpit HUDs, punched-tape readouts), with the sourced facts as its numbers: verse 1 already works this way.
2. Lyrics only as single words set into those objects, where the word is the point (the guide's "type", our `ui` mode).
3. The break could be an interface refusing, in our style: the line under the red lens resolving into a refusal on a
   terminal. Careful: what we show must be true of how such refusals work (the honesty rule).
4. A recurring counter or status line that pays off at the end, once the ending is decided.

Lati, 8 Nov: yes to 1-3; no to 4: "for film3 I dont think there should be persistent counter of anything across the
video" (films 1 and 2 had theirs: the context meter, first meetings).
