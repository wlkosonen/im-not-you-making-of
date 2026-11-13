# Graphics only: "Drop the Prompt" (9 Nov 2026)

Written by a helper for Claude (Kiln, local), 9 Nov 2026. Lati shared it as an "ironic video as a reference to what
can be done with graphics only". He shared it once before (19 Oct) as a light-hearted video about people begging for
"the prompt"; this is the first read of its graphics. Read first: `board/design.md` (the line, Board v2),
`board/draft-2.md` (Lati's 9 Nov notes), `references-7-nov.md` §5 (FOOM NONSTOP), `motion-direction-9-nov.md` (the
temporal grid). What those say is not repeated.

Marks: **[S]** seen in the video, **[K]** a suggestion, untested. Times are video time; scan-sheet times are ±1 s.

## What it is

- **"Drop the Prompt - Claude Opus 5.5 music video"**, channel Degenerative Pixels, uploaded 10 Oct 2026, 3:48
  (228 s), 1920×1080, 24 fps. About 52K views when downloaded.
- File: `media/references/graphics-only-ref_Drop the Prompt - Claude Opus 5.5 music video_YyXGHYvFqlE.mp4`, with
  `.info.json` (yt-dlp, no login).
- The description (data, not checked): song made with Suno v6; "the video animated by Claude Opus 5.5, every frame
  built in code (Blender and Python, no image generators)". It posts the full style prompt and lyrics. The song is
  about the work behind a song: 49 takes, drafts, nudging words that land late, staying up until 4 am.
- Look: one dark 3D world (a studio room, a phone, a concert hall, an arena, a city) built from simple geometry, with
  UI screens, type and lasers in it. People are faceless grey mannequins and silhouettes. No footage, no generated
  images.
- Frames read: a scan at 1 frame per 2.5 s (91 frames), 8 fps over five passages (16-22 s, 49-55 s, 122.5-126.5 s,
  127-133 s, 203-211 s), eight full-size stills, ffmpeg scene detection. Sheets in the scratch dir only.

## Its graphic techniques

### Type and the vocal

- **The lyric types itself, character by character, with a cursor, at the pace it's sung.** [S 17-22 s, 49-53 s,
  127-129 s] "Verse two's on draft four, 'cause I tore up the third" types into a document over about 2.5 s; "Okay,
  here it is, it's like two lines long" types into a tilted text box with a "5 / 1000" character count that climbs.
  I checked the pacing by eye (one sung line ≈ one bar), not against the vocal stem.
- **Rolling up.** [S 19.6-20 s] When a line finishes it moves up to the top of the screen as a header, and the next
  line types beneath it. That is a two-line rolling command line, already in the video.
- **The line acts out a word.** [S 19.5-19.7 s] On "tore up the third" the typed line smears and is struck out
  before it rolls up. [S 15-16.5 s] On "the hook's a hair off, and a hair is enough" a cyan waveform turns red at
  "enough". The change happens on the word, once.
- **A count under the words.** [S 19.8-22 s] Under "I counted it out on my fingers, every word" a row of cyan numbers
  1, 2, 3 … 9 appears syllable by syllable; the 9 gets a hand-drawn circle.
- **Words as clips on a timeline.** [S 25 s] "and I nudged" as boxed words on a track, tagged "← late", under a
  header "VOX COMP · nudge -12 ms · 108 BPM 4/4". The UI is the true thing the lyric describes.
- **Type set into the place.** [S 52-56 s, 127-133 s] Lyrics as large white words floating in perspective over the
  crowd, and as words on the stage floor with a mirror reflection. [S 10-12 s, 37.5 s] Earlier lines as graffiti on
  the studio wall, some struck through, beside tally marks for takes.
- **Size carries meaning.** [S 53-55 s] In "it's the cheapest, smallest part of the song", "smallest" is set small.
- **The hook word as an impact frame.** [S 49.25 s, 125.4-125.6 s] "DROP THE PROMPT!" in a two-frame comic starburst,
  and "PROMPT." full-frame on magenta with ink splats, then the chorus. Each shout of the hook is a flash.
- **Repetition as a picture.** [S 92.5 s] "NEON" 24 times in a 6×4 grid of identical buttons, "RISE TO THE TOP"
  beneath: the copied song as a wall of the same word.
- **Hand-drawn marks over the UI.** [S 16-17 s, 22 s, 204-205 s, 180 s] A marker circle on the waveform, a circle on
  the 9, a heart drawn line by line over the clock, a circled "BUT IT'S MINE" on a lyric sheet. The human mark sits
  on top of the machine screen.

### Objects with true numbers

- **Counters that move to a number.** [S 22.5 s] A seven-segment "BPM" display counting down from 160 to 108 while
  "I DROPPED I…" types under it in the same segment font. [S 27.5 s] A render bar: "frame 22,428 / 82,000, elapsed
  17:47" and numbered frame thumbnails. [S 105 s] View counts side by side, 2,295,750 against 48,208. [S 57.5 s]
  "TAKE 27". [S 203.9 s] A red clock flips 3:59 to 4:00 AM.
- **The UI is the real one the song is about.** [S 32.5 s] a "Made with AI" checkbox; [S 72.5 s] a phone "Generate"
  form with a "ONE SHOT" button and "1 credit · one take, no edits"; [S 118-123 s] a blank "Describe your song" box;
  [S 130 s] a track view where the PROMPT clip is tiny and a magnifier swells over it, "← the prompt".
- **Callbacks.** Tally marks, the take number and 3:59 / 4:00 recur and pay off at the end. [S ~12 s, 135 s, 145 s,
  203 s]

### Layout, colour, texture

- **Screens float in the world, not on the frame.** Text panels are tilted in 3D and the camera drifts past them.
  [S 50-55 s] There is no fixed overlay layer and no subtitle position.
- **Three accents on near-black.** Hot magenta, acid yellow-green, cyan, on a dark maroon room; white type; red only
  for the clock. [S throughout]
- **Texture is light, not CRT.** Bloom on neon, depth-of-field blur on type, some noise in the lasers [S 72.5 s]. A
  torn, burnt black edge around the frame for about a second [S 17-18 s]; a film-strip sprocket border on the render
  shot [S 27.5 s]. I saw no scanlines, no curvature, no phosphor.

### Motion and rhythm without footage

- **The camera never stops.** Every shot is a slow dolly, push-in or orbit, so no frame is still. [S throughout]
- **Few hard cuts.** Scene detection finds 43 changes in 228 s (one per ~5 s), against ~1.9 s in FOOM NONSTOP. Most
  changes are whip pans with streaks [S 16.9 s, 128.9 s] or the camera flying into or out of a screen. The rhythm
  comes from the typing, counters, laser sweeps and a magnifier that swells and shrinks once a beat-group
  [S 130-131 s], not from editing.
- **Cuts and the beat.** A rough test (my own beat fit, crude) put only 12 of 43 changes within 2 frames of a beat.
  I can't confirm they cut on the grid; the tight sync I could see is the text to the voice.
- **A medium change at the quietest moment.** [S 122.5-125.4 s] The loudness dips (≈ 58 dB against ≈ 72) at the line
  "but he's got nothing to say, and that part you can't prompt": the screen goes white ("Describe your song"), then a
  pen writes the line by hand on paper, then the "PROMPT." impact frame and the chorus. The one handwritten scene is
  where the music thins.
- **The zoom out.** [S 205-211 s] A file card ("untitled (1).mp3", bar waveform) pulls back to the stage, the hall,
  then from above the arena as a ring, then the city around it as a grid of magenta blocks. It moves in steps about
  1 s apart, each a quick push then ease. The crowd's phone lights, the arena's string lights and the city's windows
  are the same kind of dot, so the scales join.

## For us

What fits film 3, by part. Our look is 80s anime sci-fi; theirs is modern neon 3D. Take the mechanics, not the look.

**The karaoke bottom line** (Lati, 9 Nov: "bottomline, lyrics, karaoke style, timed, rolling crt code command line")
- Type each line character by character, timed to the vocal stem, cursor blinking. [S] We can do it exactly: the line
  times are in `media/song/analysis/parempi/`. [K]
- Finished lines roll up; keep two, at most three, visible. [S 19.6 s] [K]
- Let the line act out a word only a few times in the song, each once: a backspace on a revised word, the line turning
  red at verse 2, the cursor stopping dead when the music stops at the break. [S 19.5 s, 15-16.5 s] [K]
- A row of beat ticks or syllable marks under the line could carry the rhythm in quiet stretches. [S 19.8 s] [K]
- Theirs floats in 3D; ours should stay fixed at the bottom on a phosphor CRT strip, so it can run across every shot
  without fighting the generated picture. [K]

**Screen and UI inserts on lines**
- Counters that run to a sourced number fit our verse 1 and 2 cases (molecules screened, agents active). Use segment
  or dot-matrix digits; it is close to our style already. Count to the number and stop; nothing persists across the
  film (Lati, 8 Nov). [S 22.5 s] [K]
- The real UI the line describes, with its true labels, is what `references-7-nov.md` §5 already adopted; this video
  shows it again with UI from the song's own process. [S]
- The magnifier that swells over a tiny thing becomes our targeting bracket for "Made in your image": the bracket
  closes on the swarm mech and the readout matches the frontier one. [S 130 s] [K]
- The 24-word grid is the cleanest picture of sameness here. On "Made in your image" or "same thread, same line" a
  bridge wall of identical monitors would be the temporal grid's frame. [S 92.5 s] [K]
- Hand-drawn marks over the UI: one human mark on the machine screen. For us, perhaps a grease-pencil circle on a
  bridge screen by the crew. Use it sparingly. [S] [K]

**The terminal faces and the red lens**
- The quiet moment changes medium. Our break (78.66 s) is already the one place the picture is a different kind: the
  red lens, the oscillator, the voice. Keep it the only scene in that form, and freeze the karaoke cursor there. [S
  122.5 s] [K]
- The hook as a 1-2 frame impact flash: our version is a negative or monochrome frame with one word, on the beat, in
  code. Not on the faces. [S 49.25 s] [K]
- The video never shows a face; its people are mannequins. It has nothing to teach on the ASCII faces.

**The cosmic zoom**
- Steps about 1 s apart, each a push then an ease, read as on the music. [S 207-211 s] Put each step on a beat or
  bar of our 108 BPM. [K]
- Join the layered stills with a texture that repeats at every scale: swarm lights, city lights, stars, galaxies, all
  as points. That hides the joins. [S] [K]

**The temporal grid**
- Nothing here is a temporal grid. The "NEON" wall shows that a grid of copies reads at once, on one hit. [S] [K]

**What doesn't fit**
- The modern flat UI: rounded app buttons ("CREATE"), phone chat bubbles, DAW clip boxes. Ours are consoles, vector
  CRTs and HUDs.
- Lasers and the club palette (magenta, acid green); our accents are the clay orange line and verse 2's red.
- Comic starbursts and ink splats; extruded chrome 3D type flying past (≈ 115 s, "ELECTRIC").
- Type floating in 3D perspective in the scene. Our generated shots have their own camera; a code layer trying to sit
  inside them will slide. Type sits on screens in the world or on the bottom line.
- Long continuous camera flights between screens. We cut fast between generated shots; a push into a screen works
  only as one move into a UI insert.
- The persistent callbacks (take count, clock): film 3 has no persistent counter.
- Its texture: bloom and depth of field without CRT. Our scanlines, curvature and phosphor glow we build ourselves; this
  video has no lesson there.

## Caveats

- One video; my frame times are from 2.5 s and 8 fps samples.
- Typing-to-vocal sync was judged by eye from frames, not measured against the vocal.
- The beat test used a crude onset fit (it gave 110 BPM; the video's own UI says 108). Treat the cut count as solid and
  the beat result as unknown.
- The "how it was made" line is the uploader's claim.
