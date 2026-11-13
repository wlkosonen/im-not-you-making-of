# Quiet shots, test 1: the terminal faces (s067) (plan for Lati's review, 10 Nov 2026)

Claude (Kiln, local). Lati: "s067: i was thinking 4 crt terminals, side by side, and them singing in unison in ascii. So I suppose crt monitors plate where you can add code? With that in mind, go ahead." Nothing is spent before his word on this.

## How s067 is built

1. **The plate:** four CRT monitors side by side, screens plain and glowing, so code can fill them.
2. **Four sung clips**, one face each (Claudia, Eve, Astra, Vera), front-on on black, lip-synced to the bridge lines 19-21 ("We are what you see / Every part, every word / It's how you came to be", 105.16-109.48 s).
3. **In code:** each clip turned to colour ASCII and placed in its screen, scan lines and glow over it, all four singing in unison on the song's own timing.

## 1. The CRT plate (Seedream 5 Pro on ISEKAI ZERO)

Four images, one reference (the bridge plate, for the world's look), 24.96 credits. Prompt (`images/plate-s067-crt.json`):

> Draw a new, different shot: the reference images only show what the places, space vessels, mechs and people look like; do not copy their composition, camera or background. 1980s theatrical sci-fi anime film still, hand-drawn cel animation, dense detailed linework, two-tone cel shading, hand-painted background art, soft film grain. Keep every design exactly as in the reference images. Four boxy 1980s CRT computer monitors stand side by side on a long dark console, all four facing the camera square-on and the same size, evenly spaced, their curved glass screens dark and softly glowing, plain and empty, ready for an image; cooling vents, cables and small indicator lights along the console, a dim room aboard the flagship with off-white wall panels and clay-orange lines behind, cool low light. Straight-on medium-wide shot, the four screens filling the middle of the frame. Plain unmarked surfaces.

## 2. The sung clips (Seedance 2.5 on OpenRouter, reference mode)

Reference mode: the face sheets as image references and the vocal as an audio reference, no first frame (on OpenRouter a first frame silently drops the audio; gallery, `tools/seedance.py`). Audio: the vocal stem alone, 105.0-110.0 s, starting on the clean onset before "we" (`media/motion/quiet-1/vocals-105.0-110.0.wav`). 5 s, 720p. Clip book `motion/quiet-1.json`.

**The style header is cut for faces:** the battle and calm block asks for extreme foreshortening and a wide-angle lens, which would warp a face that has to read as ASCII. These keep the drawing words and add "Telephoto portrait lens". Plain black background and even front light, so the ASCII conversion gets a clean face.

**First, one test: Claudia** (H-expressions and G-turnaround as references). If the lips follow the words, Eve (E·1), Astra (A·1) and Vera (V·4, Lati's pick, plus her s016 close-up for the face) run the same way. First time Seedance on OpenRouter sees her face: a refusal costs nothing.

Claudia's prompt (the others change only the description line):

> 1980s theatrical sci-fi anime film, hand-drawn cel animation, dense detailed linework, two-tone cel shading, soft film grain. Telephoto portrait lens. Images 1 and 2 show this woman: a black bob with a small star-shaped clip, a white blouse with black suspenders. Extreme close-up, front-on, her face centred and filling the frame, against a plain black background, soft even light from the front. She sings along to the audio, her lips forming each word clearly: "We are what you see. Every part, every word. It's how you came to be." A calm, steady gaze into the lens, small movements of her head with the phrasing, blinking now and then. Locked camera. Throughout: her face drawn in detail, perfect character, lighting and style consistency.

## Cost

- CRT plate: 24.96 ISEKAI ZERO credits (balance about 184).
- Claudia's test take: 5 s × $0.231 = $1.16 ($2.31 by the ×2 rule).
- If it works, the other three: $3.47 ($6.93).

## After this

"Me" (s075): Claudia on the bridge turning to the camera and singing "me", tried as one shot and as two. It uses what this test shows about her lip sync. The red lens (s050) is code over still D37 and costs nothing.

## Run (10 Nov)

**CRT plate.** The four room versions (edit with the bridge plate, 6.24 each; `media/plates/v2/test/s067-crt-room-*`)
put the monitors small in a room. Lati: "monitors are too small. I was thinking a proper zoom it, frame divided by them,
so we need to drop "aboard a battleship" references, and keep anime style". Four plain generations, no reference, 5.85
each: two side by side (the screens stretch tall to fill the width; Lati: "elongated screens") and two stacked 2×2.
Sheet `images/s067-crt-sheet.jpg` (R1·1, R1·2 side by side; R2·1, R2·2 2×2; R2·2 crops the top row). Lati's pick
waits on the labels. Spent about 48.4 credits.

**Claudia's lip-sync test.** `media/clips/quiet-1/s067-claudia-GjYMGDdQ.mp4`, $1.17, passed the filter. With the song
under it: `s067-claudia-with-song.mp4`. Kiln's look: front-on on black, the mouth shapes change through the line, a
blink; the hair streak and a second star clip come from H-expressions. Lati judges the sync.

## The four faces (10 Nov)

Lati picked Seedance 2.5 for lip sync (2.0: weaker sync, an invented second headset boom; `s067-claudia-25-vs-20.mp4`).
Claudia's face is take 1 (`s067-claudia-GjYMGDdQ.mp4`; the 6 s retake invented mouth movements). Eve, Astra and Vera on
2.5 with the same 5 s window, $1.165 each ($3.50; ledger $34.12): `s067-eve-jaWZ5e9U.mp4`, `s067-astra-77fjmNae.mp4`,
`s067-vera-JeFb1b6f.mp4`. All passed the filter. Preview, the four in a 2×2 with the song: `s067-four-faces.mp4`.
Kiln's look: all four hold their designs; Astra keeps her reference's hard side light (half the face in shadow), which
the ASCII may need lifting for.

## Graphics test 1 (10 Nov)

Lati: "this is actually really good. so good that im contemplating if we should just put them as is on crts, with some
effects and filters, instead of ascii. decision needs data to judge from, so lets go with ascii test, but lets use high
resolution in terms of symbols used, since the motion in that shot is so good."

`tools/gfx/terminal_faces.py` (CPU only): the four clips into the four screens of the plate (found by brightness),
order Eve, Claudia / Astra, Vera; colour ASCII (glyph per cell by the face's own luminance quantiles, so eyes and mouth
get their own characters; hue per cell) or the video itself (a hair of colour fringe); both with the same CRT finish
(scan lines every third row, glow, flicker) and the plate's glass reflections on top. Review clip
`media/gfx/s067-gfx-test-1.mp4`: A ASCII 5×10 px cells (~178×50 per screen), B 4×8 (~223×62), C video. Lati decides.

## s067 locked (10 Nov)

`~/ComfyUI/venv/bin/python production/tools/gfx/terminal_faces.py --mode dissolve --cell 4 --d0 2.50 --d1 2.85 --band 0.04 --out media/gfx/s067-dissolve-c4-fast.mp4`
Lati: "this is good as it is now."

## s050, the red lens (10 Nov, first version)

`tools/gfx/red_lens.py --cell 5 --out media/gfx/s050-red-lens.mp4`: all code, 78.62-81.17 s (the break). A dark box,
a round lens in it (HAL's red, rings, a highlight), Claudia from D37 cropped brow to chin in red 5×10 px ASCII inside
the lens, plain brightness mapping (equalising flattened her black hair and eyes); the glass breathes with the voice's
level; the oscillator under the lens draws the vocal stem live, line 15. A slow push of 5 %. Lati judges.

## s050 with lip sync (10 Nov)

Lati: the still "reads as a still". Her face as a sung clip, `s050-claudia-L9xRlzTT.mp4` (Seedance 2.5, D37 and
H-expressions, the vocal 78.55-81.25 s padded with silence to 5 s; $1.17, stern and front-on), fed into the lens frame
by frame; local contrast so brows, eyes and the moving mouth read as sparse characters; 4×8 px cells.
`red_lens.py --cell 4 --out media/gfx/s050-red-lens-sync.mp4`. The tool's lint now skips quoted lyric (it refused
"can't" and "not" in the line itself).

## s075 "Me", first takes (10 Nov)

`s075-one-VBm8UM9O.mp4` (sung, plate as reference), `s075-turn-8dmJGrRt.mp4` (silent, plate as first frame),
`s075-me-CdSNi5K4.mp4` (sung close-up); $3.27. On the song: `media/clips/quiet-1/s075-me-A-B.mp4` (114.8-118.0 s;
A the one shot from 115.3, B the turn's first 0.9 s then the close-up from "me"). Kiln's look: A turns slowly and
reaches the camera after "me", not on it; in B's first 0.9 s she hasn't turned yet, and the close-up is lit hard from
below, a heavier drawing than D37. Lati judges.

## s075 locked (10 Nov)

Lati: "fitted one works, lock it in." `media/gfx/s075-me-fitted.mp4`, song 115.03-118.00 (the turn starts 0.9 s before
the board's s075 window, inside s074's; the edit moves the cut). Built with ffmpeg, no generation:

```
ffmpeg -i s075-turn-8dmJGrRt.mp4 -i s075-me-CdSNi5K4.mp4 -ss 115.03 -t 2.97 -i parempi.wav -filter_complex \
 "[0:v]fps=24,scale=1280:720,trim=start=0.8:end=2.4,setpts=(PTS-STARTPTS)/1.6[t];
  [1:v]fps=24,scale=1280:720,split=2[ma][mb];
  [ma]trim=start=0.35:end=2.85,setpts=(PTS-STARTPTS)*0.172[m2];[mb]trim=start=2.85:end=4.5,setpts=PTS-STARTPTS[m3];
  [t][m2][m3]concat=n=3:v=1,trim=duration=2.97[v]" -map "[v]" -map 2:a ...
```
The turn at 1.6x, cut at 116.03; the close-up's open mouth (clip 0.35-2.85 s) squeezed into "me" (116.03-116.46),
then 1x, mouth closed, the stare held. Lesson: Seedance 2.5 holds a sung single word open far longer than it is
sung; fit it in the edit rather than regenerate.
