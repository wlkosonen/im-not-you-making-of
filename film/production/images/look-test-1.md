# Look test 1: Claudia as an 80s hand-drawn sci-fi anime character (7 Nov 2026)

Lati: "yes, run the look test. Claudia as an 80s anime character across different models. Lets see what we get."
Route: ISEKAI ZERO (Lati's earned credits). Estimate 42.5 credits, 85 at most; 1 credit ≈ $0.011 at top-up prices.
Text only, no reference images: this finds the look, not her consistency. Design points from `production/her.md`.
The style is described by the era's traits, never by a named film or artist.

## Prompts

**A, close-up**

```text
1980s hand-drawn cel anime illustration, hyper-detailed science fiction. Close-up portrait of an adult woman with slim adult proportions and a calm, focused expression. Glossy black blunt bob with heavy straight bangs, one clay-orange streak through the bangs, a small eight-pointed star hair clip, a thin headset microphone curving toward her mouth. Hand-painted cel shading, fine dense linework, soft film grain, gentle halation on highlights. Deep blue and teal palette with warm orange and neon reflections from banks of glowing monitors behind her.
```

**B, wide**

```text
1980s hand-drawn cel anime illustration, hyper-detailed science fiction. Wide shot of a vast research laboratory built from machines: towering cable-bundled computers, gantries, pipes, rows of glowing amber monitors showing protein structures and star charts. An adult woman with a black blunt bob, one clay-orange streak in her bangs and a thin headset microphone stands small at the centre, looking up at it all. Hand-painted background art, cel shading, intricate mechanical detail, soft film grain, deep blues with warm orange and neon highlights.
```

## Models (16:9)

| Model | modelId | Credits |
|---|---|---|
| Tsubaki.3 (pro) | 6ad69c5e0fffc58c8d1ac7c8 | 13.4 |
| Animagine XL 4.0 | 6aca7c422b5d48cc9379762a | 2 |
| Seedream 5 Pro (medium) | 6a50079fc28ed5bfe5576f54 | 5.85 |

## Results

Spent 29.4 credits (balance 5,880.36 → 5,850.96, read back); Tsubaki.3 failed on ISEKAI ZERO's side three times,
each refunded. Originals in `media/images/look-test-1/` (gitignored); also in Lati's ISEKAI ZERO gallery.

**Round 2, Japanese** (Lati, mid-run: "how about skyebrows lessons? Those were exactly for this usecase, prompting in
japanese?"). Skybrows, from the Zuckerwars breakdown transcript in Flint's session (19 Oct): Seedance prompted in Japanese
leans anime, in English it drifts toward a 3D game-studio look; a Japanese style header with English beats also works;
the reference art still has to be in the right style. His test was video; this round tries it on stills. The Japanese
prompts are the same subjects translated, with 作画, 原画, 二値のセル塗り, 劇場用 in the header (as recorded in the
ISEKAI ZERO gallery entries).

| Image | Model | Language | Kiln's read (Lati's eye decides) |
|---|---|---|---|
| A-en-seedream5pro | Seedream 5 Pro | English | Every design point lands: one orange streak, the star clip, the headset mic, a grown face; CRT walls. 80s cel look, slightly glossy-modern |
| A-ja-seedream5pro | Seedream 5 Pro | Japanese | The most 80s theatrical: softer palette, cel highlights, hand on a CRT. Drift: a second, pink streak beside the orange |
| B-en-seedream5pro | Seedream 5 Pro | English | Dense lab, readable; invented signage text ("KELTICKS BIOTECH…") that would need removing |
| B-ja-seedream5pro | Seedream 5 Pro | Japanese | Hand-painted, cable-heavy, closest to the era; she's small at the centre as asked; screen text is gibberish but reads as texture |
| A-en-animagine | Animagine XL 4.0 | English | 90s pop rather than 80s; no streak, no mic; an unasked "shh" gesture; reads younger than she should |
| B-en-animagine | Animagine XL 4.0 | English | Stylised and airy, not hyper-detailed; she's a tiny figure in a red suit |
| A-ja-animagine | Animagine XL 4.0 | Japanese | Ignored the prompt: a generic group of long-haired girls, sexualised framing. Tag-based SDXL doesn't read Japanese prose: out |

So far: Seedream 5 Pro, and Japanese pushes it toward the 80s theatrical look on stills too. Next would be the same
prompt with her face sheet as a reference image (Seedream takes up to 10), once there is one.
