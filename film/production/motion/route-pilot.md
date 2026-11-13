# Route pilot: is Seedance the step up?

Claude (Kiln, local), 1 Nov 2026. **Not run. Nothing is approved** (`budget.json` is $0, so `seedance.py` refuses every
job). It runs after the anime design exists, and needs an estimate and Lati's yes on the day.

Why: Lati, 1 Nov, on Grok takes alone not reaching the next step in quality. Film 2's limits were Grok's short phrases and
its own music; Seedance takes the real vocal and holds longer shots (gallery: up to 16 s).

Prices on OpenRouter, read 1 Nov 2026: Seedance 2.5 $0.23/s at 720p, $0.1028/s at 480p, 4-30 s, **720p at most**. Grok
Imagine 1.5 $0.14/s at 720p, $0.25/s at 1080p, up to 15 s. So Seedance takes on OpenRouter would need upscaling to match
film 2's 1080p; Higgsfield's 1080p was $1.14/s in October, five times the price.

## Questions, in order

Each estimate is seconds × price × 2, the film's rule.

| # | Question | Clip | Estimate |
|---|---|---|---|
| 1 | Does OpenRouter accept the anime face sheet? A decline is free | 4 s silent, 480p, `reference` | $0.82 |
| 2 | Does a hard subject pass the content filter? A drone swarm or lab scene, the plainest true staging | 4 s silent, 480p, `reference` | $0.82 |
| 3 | Does she hold lip sync from a lead stem, on an anime face? Film 2's vocal is free to use for this | 8 s, 720p, `sung`, short prompt | $3.68 |
| 4 | Does a 15-cut burst work, and does it keep the lips? | 15 s, 720p, `sung` | $6.90 |
| 5 | Positive words or exclusions? Same shot, two prompts | 2 × 4 s, 480p, `reference` | $1.64 |

Total **$13.86** at the rule's doubled estimate, about half that in real cost. OpenRouter credit left: $18.49, read 1 Nov.

Only if question 3 fails: a black MP4 in place of the audio (`dan-kieft-lessons.md` point 2). I don't know how OpenRouter
bills it, so the first job reads the real cost.

## Reading the answers

- **Refused at 1:** final for that reference on OpenRouter. Don't alter it. Ask Lati about Higgsfield, or local and Grok.
- **Blocked at 2:** this shapes the board. Re-stage it as a genuinely different shot, or show the subject by type and
  graphics. Ask Lati. Never route around a block.
- **Holds at 3:** the budget talk starts. A 3-minute film at three seconds shot per second kept is about 540 s, or about
  $125 in real cost at 720p. The gallery's THE CAKE IS NOT A LIE ran 1,353 s for $435.
- **Fails at 3:** Grok for stage, as film 2. InfiniteTalk on anime faces is also untested, and free.

## Before it runs

- **Audio goes by public HTTPS URL.** Film 1's route was the public Hugging Face dataset `Shegss/claudia-seedance-refs`,
  which is empty. That was Lati's OK for film 1: ask again. `host.json` doesn't exist yet, so a real run stops there too.
- Suno's lead stem for question 3 if he has it from film 2; htdemucs's otherwise.
- Stills downscaled to the output size, PNG, in their own colour (gallery, "Inputs").
- Read the gallery's wiki/seedance page, "Lip sync from the song's own vocal" and its template, and write the prompts from it.
