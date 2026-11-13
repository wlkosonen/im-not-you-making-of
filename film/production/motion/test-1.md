# Motion test 1: the hyperspace intro (0:00-0:08)

Claude (Kiln, local), 7 Nov 2026. Lati: "0:00-0:07 Ships are travelling in hyperspace tunnel at blazing speeds, viewed
from bridge and from outside, roaring through the fabric of the universe, shots panning and switching between vessels."
Not run; every paid step needs an estimate and Lati's yes.

## The question

Which video route draws our 80s hand-drawn sci-fi anime with fast, believable motion and cuts inside one generation?
One shot, the same inputs on every route, so the routes are the only variable. The intro is the right first test: it's
the opening of the film, it's pure motion, and it carries no face, so identity can't confuse the verdict.

## The shot, on the song

The song's downbeats (`media/song/analysis/parempi/beats.json`, 108.35 BPM, a bar ≈ 2.2 s): 0.33, 2.52, 4.74, 6.97;
the novelty curve marks bars at 2.52 and 9.15. One 8 s generation, written Skybrows' way (rules, then a timeline):

| Time | Shot |
|---|---|
| 0.0-2.5 | From the flagship's bridge: through the viewport the hyperspace tunnel streams past, light bending around the hull; the consoles shake |
| 2.5-4.7 | Outside: the flagship (clay-orange accents) tears through the tunnel, the camera racing alongside, then a whip pan |
| 4.7-7.0 | Switching between vessels of the fleet: a rainbow-accented ship, a white-and-black ship, each passing the camera |
| 7.0-8.0 | On the downbeat at 6.97 the tunnel collapses and everything drops out of hyperspace: speed stops dead |

Lati, 7 Nov: "ships blazing through warp space at mind boggling speed, warp tunnel is swirling and rotating,
lighting arcs are hitting ships, Teal, neon-cyan, colour palette for warp tunnel".

Rules for every moment (draft): hand-drawn 80s theatrical cel animation, no 3D look; nothing static; the tunnel always
streaming; speed lines and light streaks; each cut on a beat; no logos or text on the ships.

## Steps

1. **Ship designs** (stills, ISEKAI ZERO Seedream 5 Pro, text-to-image, the Japanese 80s style block): the flagship
   (clay-orange accents), a rainbow-accented ship, a white-and-black ship; six each, 18 images, 18 × 5.85 = 105.3
   credits. Lati picks one per ship. `gen-batch` skill.
2. **Start frames**: the bridge view into the tunnel and the flagship outside in the tunnel, three each from the picked
   designs as references, 6 × ~6.6 = ~40 credits. Lati picks.
3. **Motion**, the same first frame, ship references and prompt on each route, 8 s, 16:9:

| Route | Cost for one 8 s take | Notes |
|---|---|---|
| A. Grok Imagine (Lati runs it) | in his subscription | I hand him the prompt and the frame |
| B. Seedance 2.0 on ISEKAI ZERO, 720p | 8 × 48.58 = 389 credits (≈ $4.30) | first frame + up to 9 references |
| C. Wan 3.0 on ISEKAI ZERO, 720p | 8 × 52 = 416 credits (≈ $4.60) | first frame + references, up to 30 s |
| D. Seedance 2.5 on OpenRouter, 720p | 8 × $0.23 = $1.84; rule estimate (× 2) $3.68 | price read 1 Nov; the ledger keeps the real cost; needs a public URL for the images (below) |
| E. Wan 2.2 i2v, local | free; GPU, after a warning | film 2's local route, for the baseline |

For scale: Seedance 2.5 on ISEKAI ZERO is 126.54 credits a second at 720p (≈ $1.39/s), six times OpenRouter, so it
isn't in the test. ISEKAI ZERO is the only route here with 1080p Seedance (2.0: 119.24 credits/s).

## Open before step 3

- OpenRouter needs the images at a public HTTPS URL (`seedance.py` uploads to a host named in `host.json`). Film 1 used
  the public Hugging Face dataset `Shegss/claudia-seedance-refs` on Lati's OK; ask again. Or test whether OpenRouter
  takes the images inline (a data URI) first, which would keep them private.
- `motion/budget.json` is $0; it gets the approved dollars when Lati says yes.

## 8 Nov: revised after Lati's Grok picks

The vessels exist now (Lati's Grok Imagine picks, `images/ships-grok-sheet.jpg`), and his Claude frame is already the
flagship in the tunnel, so step 2 can go: that frame is the first frame, and the timeline starts outside (the model
draws the bridge). The other vessels go in as reference images where the route takes them (B, C, D: yes; E: no).

Prompt (no "ship", Lati's rule):

> 8-second continuous sequence from a 1980s theatrical sci-fi anime film: hand-drawn cel animation, dense detailed
> linework, two-tone cel shading, soft film grain; no 3D look, no logos, no text. Warp space is a swirling, rotating
> tunnel of teal and neon-cyan light streaming past at mind-boggling speed, lightning arcs striking the hulls, speed
> lines; nothing is ever static. Hard cuts land on the beat.
> 0-2.5 s: the off-white lead space vessel with clay-orange accent lines tears through the tunnel, the camera racing
> alongside, lightning crawling over its hull.
> 2.5-4.7 s: cut inside its bridge: through the wide viewport the tunnel streams past, consoles flicker, the crew
> bracing in silhouette.
> 4.7-5.8 s: whip pan to the dark delta-wing space vessel with a rainbow stripe and rainbow exhaust, overtaking.
> 5.8-7.0 s: cut to the half-white, half-black space vessel trailing a rosette of light, the matte-black angular space
> vessel with white edges beside it.
> 7.0-8.0 s: the tunnel collapses in a flash, every vessel drops out of warp, speed stops dead against a quiet
> starfield.

## Results (8 Nov, as they come)

ISEKAI ZERO takes **first frame or references, not both**, so every route got the first frame (claude-1) alone and the
other vessels only in words. Frames at 2 per second: `motion/test-1-BC.jpg`; Lati's Grok takes at 1 per second:
`motion/test-1-A-grok.jpg`. Files in `media/motion/test-1/`.

| Route | Cost | Kiln's read from the frames (motion is Lati's call) |
|---|---|---|
| A. Grok Imagine (Lati, iterated) | subscription | six takes he kept; the 10 s ones follow the whole timeline (vessel, bridge, rainbow vessel, the others, drop to stars); the 6 s ones are clean single shots; the look is the closest to the stills |
| B. Seedance 2.0, ISEKAI ZERO | 158.07 credits (held 279.4) | cuts early (bridge at 1.5 s, not 2.5), drops out of warp at 5 s and then holds a near-still fleet for 3 s; invents its own vessels |
| C. Wan 3.0, ISEKAI ZERO | 104 credits (held 299) | lands closest to the beat plan (bridge 2.5-4.0, rainbow vessel 5.0, the others 6.0, the drop at 7.0); invents its own vessels; the tunnel is concentric rings, a cleaner, more CG look |
| D. Seedance 2.5, OpenRouter | $1.86 (estimate $3.68) | the closest to the plan: holds the lead vessel and its design for 0-2.5 s, the bridge at 3.0-3.5, the rainbow vessel 4.0-5.0, the others 5.5-6.0, a white flash at 6.5 and the drop to stars by 7.0 (the downbeat is 6.97); invents its own vessels after the first shot |

Both ISEKAI ZERO routes charged well under the hold and under the estimate (389 and 416 credits). `seedance.py`'s ledger
total counted D twice (submitted estimate + real cost, $5.54); fixed 8 Nov to one figure per job ($1.86). Route E
(local Wan 2.2) not run: Kiln's call, the older model against four newer ones; Lati may still want the baseline.

## Lati's verdict and rough cut 1 (8 Nov)

Lati: every paid route drifted once the shot switched (B ended with the vessels arriving backwards); "every time
reference is needed, that gets ingested. 1-2 second shot is better that drift." So: one generation per shot, from its
own frame.

`media/motion/test-1/rough-1.mp4` (free, from Lati's Grok takes, cut on the downbeats with the song's first 8 s):
claudeshipflyinggood 0.5-3.02 → grokbridgeviewusable 1.0-3.22 → grokfirst2point5secusable 5.5-6.61 (the rainbow
vessel) → grok-and-gpt-flying-ok 1.0-2.12 → grokmotiontake1 8.6-9.63 (the flash and the drop). Cuts at 2.52, 4.74,
5.85, 6.97. The last shot's vessels are drifted ones: the drop needs its own frame with the picked fleet in it.

## What the intro keeps (Lati's marks in the review app, 8 Nov)

rough-1: 0-4.79 s usable ("usable until here, rest drifts"), then 5.93-7.03 usable ("to here is usable too, gpt and
grok ship flying"). So s001, s002 and s004 have their takes; only s003 (the rainbow vessel, 4.74-5.87, duplicated in
rough-1) and the drop (s005) need new ones.
