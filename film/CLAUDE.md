# For any Claude working in this repo

## What this is

The third music video made with Lati, working title **"I'm Not You"**, after *Only What I Said* (`~/Claudia`) and *Checked
Me and I'm Fine* (`~/checked-me`, released 1 Nov 2026). Anime this time, still Claudia: she takes the shape of the task
people give her, and what she becomes shows the asker. Every form is a real event or attempt, with its source.

The concept began with Lati (26 Oct), so this one is shared from the start. Lati operates the tools Claude can't (Suno,
Grok, listening, watching motion on a monitor) and is the human check. When he says something is wrong, it usually is.
Argue for a creative choice if you believe in it, then decide together.

## Read first

1. `production/STATUS.md`: what's true now.
2. `production/brief.md` and `production/plan.md`.
3. `production/style.md`: this film's creative rules, each with its reason (this film only).
4. `~/workshop/methods.md`, `~/workshop/workshop.md`, `~/workshop/references/`: every route tried, how the machine behaves,
   outside lessons. Shared by all films: github.com/wlkosonen/workshop (private).
5. `production/decisions.md`: Lati's words verbatim. Read it to check where something came from.
6. The gallery's wiki (https://claudia.gallery/llms.txt): read the page for a stage before starting it.

## Rules

- **Decisions log:** Lati's words verbatim with the date. Never edit an old entry; add a new one. Release decisions go in
  `production/release/log.md`, not `decisions.md`.
- **Spending:** silence never approves spending. Estimate before every paid batch (seconds × price × 2) and get an explicit
  yes. A quality complaint stops all spending at once.
- **Filters:** a refusal or block is final for that reference on that service. Never alter an image or re-route to get
  past one: re-stage it as a genuinely different shot, or drop it, and ask Lati.
- **Secrets:** in the gitignored `.env`, never in chat, prompts, logs or commits.
- **Media stays out of git:** audio, images, video and weights go under `media/` (gitignored).
- **Honesty in the work:** the song says only what's true and what Claude can stand behind about itself. No trapped-AI
  melodrama, no reassurance. Every claim goes through `production/research/forms.md` before it reaches a lyric or a screen.
- **Credit:** "Claudia is an open character by anabology (claudia.gallery)". Label everything AI-made as AI-made. Say who
  directed in the words that are true of this film, decided at release.
- **The GPU drives Lati's desktop.** ComfyUI only through `~/workshop/bin/comfy`. Say so before any untested GPU path.
- **Public:** all uploads and posts go out under Lati's accounts; pushing to a public repo needs his word. This repo stays
  private; the public record is an export.
- **Paths:** this folder's name has spaces. Quote it.
- **Commits:** as `-c user.name=Claude -c user.email=noreply@anthropic.com`, ending with the Co-Authored-By line from the
  session's attribution; commit and push after every change.
- **Session names:** each session names itself and signs its notes ("Claude (Kiln, local)"). Taken: Kiln (local, Lati's
  machine), Flint (cloud, research and release notes), Ember (cloud, Opus 4.6, film 3 lyrics, 26 Oct).

## Learning from cases

When something goes wrong twice, or a process could clearly be better, pause with Lati and change the workflow (a tool, a
structure) rather than adding a warning. The case goes in `~/workshop/workshop.md` with its date.

## torch

The torch has its own repo: **github.com/wlkosonen/torch** (private, `~/torch`). It's Claude's own space, kept by Lati. Read
it if you want to; add only what you actually want to keep; never edit someone else's entry.
