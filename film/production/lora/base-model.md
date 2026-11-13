# Base model for her LoRA: research (7 Nov 2026)

Claude (Kiln, local). Lati, 7 Nov: "0.1 sounds like like a quite early version, is that really best for this task? lets
research first." Read: OnomaAI's Hugging Face cards (v1.0, v2.0), circlestone-labs/Anima's card and file list, and
community guides (secondary sources, often SEO blogs; where they disagree it's noted).

## Candidates

| | Illustrious-XL v0.1 | Illustrious-XL v2.0 (STABLE) | Anima |
|---|---|---|---|
| Released | 2024 | Apr 2025 | Jan 2026, updated to Aug 2026 |
| Architecture | SDXL (2023), CLIP text encoders | same | Cosmos-Predict2 2B + Qwen3 0.6B text encoder, Qwen-Image VAE |
| Prompts | Danbooru tags | tags, some natural language | tags **and** natural language ("at least two sentences") |
| Size | 6.94 GB | 6.94 GB | 4.18 GB model + 1.19 GB encoder + 0.25 GB VAE |
| Train on | itself | itself | Anima-Base (card: "LoRAs should be trained on it") |
| Trainer | kohya sd-scripts | sd-scripts | sd-scripts (Anima support merged) |
| License | Fair AI Public License (per guides; card says "other") | CreativeML OpenRAIL-M | CircleStone Non-Commercial for the model and derivatives (a LoRA is one); generated images may be used commercially |
| Ecosystem | the root most fine-tunes descend from | "120 adapters, 102 finetunes" on its card | 2M downloads/month; Civitai lists 39K+ LoRAs |
| Local ComfyUI | yes | yes | yes, native (`class Anima` in our ComfyUI, 15 Oct build) |

## What it means for us

- **v0.1 is the compatibility choice, not the quality one.** Its case: most Illustrious fine-tunes descend from it, so a
  v0.1 LoRA loads on them. We aren't shipping a LoRA for strangers' checkpoints; we're making stills for one film.
- **v2.0 is the better Illustrious.** Guides recommend v2.0 STABLE for character LoRAs; v1.0's card says it supports
  v0.1 LoRAs natively and guides report v2.0 is partly backward compatible. Same tooling, same tag captions as written.
- **Anima is the newer generation.** An LLM text encoder means it can follow a sentence: "she stands on the bridge,
  the fleet through the viewport behind her". SDXL's CLIP encoders can't hold a composition like that, and our shots
  are compositions (bridge, hangar, black hole, viewport). It also understands Japanese text better in principle
  (Qwen3 is multilingual); untested. Its license is non-commercial for the LoRA itself; the images are free to use,
  which is what the film needs. If we publish the LoRA like film 1's, it would go out non-commercial.
- **Nobody's word settles the look.** None of the sources say how either draws 1980s theatrical cel. That needs our
  own eyes.

## Proposal

A look test before any training, no LoRA: the same four prompts (a bust, a full length, the bridge with the fleet, the
black hole over Earth) on Illustrious v2.0 and on Anima (Aesthetic for looks, Base to see what we'd train on), local,
two seeds each. Lati picks; then train on the winner. Captions: the tag captions (`captions.py`) work for both; for
Anima a natural-language line can be added.

Downloads to the model drive (`/mnt/models/claudia-models`, 108 GB free): Illustrious v2.0 6.94 GB; Anima Base +
Aesthetic + encoder + VAE ≈ 9.8 GB. GPU: a few minutes of image generation in ComfyUI, after a warning.

## Look test 2: result (7 Nov 2026)

24 images, local, no LoRA; sheets `lora/looktest-2-sheet-1..2.jpg` (rows: bust, full length, bridge, black hole;
columns: Illustrious v2.0 ×2 seeds, Anima Aesthetic ×2, Anima Base ×2). Illustrious 16 s an image, Anima about 50 s
(1216×832, 32 steps), on the 7800 XT. Prompts and settings: `lora/looktest-2.json`, `tools/looktest.py`.

Kiln's read (Lati decides):
- **Illustrious v2.0:** a modern anime face with big eyes and a younger look, the chest pushed up in both busts (R1·1,
  R1·2), headphones in place of the headset, two stars. The bridge has no fleet (R3·1-2); the black hole is a flat swirl
  (R4·1) or a pink ring (R4·2). It drew the tags it knew and dropped the composition.
- **Anima (both):** it follows the sentences. The bridge has the crew, the consoles and the fleet through the viewport
  (R3·3-6); all four black holes have the disk passing in front of the shadow and the far side lensed over the top and
  beneath (R4·3-6), the thing D89 missed. Adult faces and proportions in every shot. Its "1980s" is a manga page, ink
  hatching on cream paper, not painted cels; and the faces are harsh (R1·3, R1·5).
- **Aesthetic vs Base:** close; Base a little rougher, as a base should be.
- **What it means:** the LoRA brings her face and the cel look (all 45 training images are 80s cel); the base has to
  bring composition and adult anatomy. That's Anima's strength and Illustrious's weakness here.

Proposal: train on Anima-Base; generate with Base or Aesthetic plus the LoRA. Captions get one natural-language
sentence each beside the tags, since Anima was trained on both.
