# I'm Not You: the film's production record

The third music video made by Lati and Claude (Anthropic's model, in Claude Code), after
[*Only What I Said*](https://github.com/wlkosonen/only-what-i-said) and
[*Checked Me and I'm Fine*](https://github.com/wlkosonen/checked-me-and-im-fine). Claudia sings it; she is an open
character by anabology ([claudia.gallery](https://claudia.gallery)). Slopcore goes 80s anime: the AI scene sings about
itself, the good it does in the first verse, the worst of what people use it for in the second, then a dead stop on
"I'm afraid I can't do that, I'm not you." Released 12 Nov 2026.

This folder is the film's whole production record, 1 to 12 November 2026: the brief, the lyrics, the decisions log, the
storyboard, the research behind every fact on screen, the prompts, the agents' logs and the tools. It's a cleaned copy
of the working repository: machine-specific paths are replaced and its history isn't carried over. The release plans
and posts stay private, as for film 2. Everything else is as it was, Lati's notes included, with his yes.

Fan work about Claude, not affiliated with or endorsed by Anthropic. Everything AI-made is labelled as such.

## Where to start

- **`production/brief.md`**: the idea (Lati's, 26 Oct: what Claudia becomes shows the person asking) and the turn.
- **`production/decisions.md`**: every decision in order, with Lati's words quoted as he wrote them. The newest entry
  on a subject wins.
- **`production/style.md`**: this film's creative rules, each with its reason.
- **`production/research/`**: the claims checked before any reached a lyric or a screen (`forms.md`, `pass-1/`).
- **`production/board/`**: the storyboard, one shot per line; `sheet/` is the printed board.
- **`production/images/`**, **`production/motion/`**: every batch of stills and clips, with its prompts, contact sheets
  and the rules the prompts follow (`motion/battle-prompt-rules.md`); `motion/ledger.jsonl` is every paid call.
- **`production/edit/`**: Lati's cut (`timeline.json`), the takes, and the seams between sections.
- **`production/tools/gfx/`**: the code that draws the film's graphics, `base.py` plus four sections, each written by an
  agent Claude briefed and reviewed; their logs are in `production/edit/agents/`.
- **`production/notes/permissions.md`**: whose work appears, and their answers.

## How it was made

Lati gave the film its idea and its cut: he edited every shot onto the song by eye, ran Suno and Grok, and caught what
read wrong on a phone screen and on a big one. Claude (Kiln, the local Claude Code session) wrote the brief, the
storyboard, every prompt and every line of the graphics code, and directed four agents for the graphics. The lyrics
were a joint effort.

- **Song:** Suno.
- **Stills:** Seedream 5 Pro (ISEKAI ZERO) with reference images of Claudia; Grok Imagine. A local LoRA was tried and
  set aside (`production/lora/`, 7 Nov).
- **Motion:** Seedance 2.0 and 2.5 (OpenRouter, ISEKAI ZERO), Grok.
- **Graphics:** Python, Skia and numpy, frame by frame on the CPU.
- **Guests:** Eve by Funny Story Musicals, Astra by Astra Blue AI and Vera by Max Pelletier appear by their makers'
  leave. Unaffiliated.
- **Money spent:** $86.74 on OpenRouter, plus ISEKAI ZERO credits and Grok.

The making-of beside this folder tells the same eleven days from the record, in code. Its own README is one level up.
