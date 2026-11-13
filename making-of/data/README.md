# data/: film 3's record as JSON

Extracted by `tools/data/extract.py` (Python 3, stdlib only; `python3 tools/data/extract.py` rebuilds every file here
in a few seconds). Written 12 Nov 2026 by the data agent for Claude (Kiln, local). Read-only on every source; nothing
outside this folder is touched.

## Conventions

- **Window:** film 3's first commit, `ea3d802d` at 2026-11-01 20:43:50 +02:00 (**2026-11-01T18:43:50Z**), to the
  making-of's first commit, `b667f51` at 2026-11-12 10:50:52 +02:00 (**2026-11-12T08:50:52Z**). After that moment
  Kiln's session is working on this making-of, so ending there keeps the record fixed: a rebuild gives the same
  numbers. `--end now` (or `--end <ISO>`) moves the end.
- **Times:** every `ts` is UTC ISO 8601 with `Z`. Every `t` is seconds since the window start (18:43:50Z), and is
  negative for the few things just before it. Lati's local time is Europe/Helsinki, **EET, +02:00 for the whole
  window** (summer time ended 25 Oct). Dates written in decisions.md (`date`, `heading_date`) are his local dates.
- **Sources:** film 3 = `/home/shegs/Im not you`; Kiln = `~/.claude/projects/-home-shegs-Claudia/85bff6f8-….jsonl`
  (the main session, 614 MB) and its `subagents/` folder.
- **Files are compact JSON** (one line). Each has an `about` string; row arrays are under `rows`.

## How the transcript is read (applies to calls, compactions, turns, agents, sessions)

- One API call is written as several `assistant` records (one per content block: thinking, text, each tool use),
  all with the same `message.id` and the same `usage`. Calls are **deduped by `message.id`**; the call's time is
  its first record's `timestamp`. The one `<synthetic>` (harness-made) record is dropped.
- A stretch of the Kiln file is **written twice**: records 38070-39443 repeat the records from the 4 Nov compaction
  onward up to 7 Nov 19:27Z (same `uuid`s); the copy sits just before the 8 Nov compaction's boundary. Why the
  harness wrote it again isn't recorded. An earlier repeat
  (lines 20180-21973, October) is outside the window. Records are **deduped by `uuid`**, so nothing is counted twice.
- **Context size** of a call = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` of its
  `usage`. Peaks above 800k mean Kiln ran with a context window larger than 800k tokens.
- The transcript also logs each request it sends (`type: "api-request"`, since 23 Oct): **2,286** in the window
  against **2,175** calls with a recorded response. The ~111 difference is requests without a response record
  (retries, interrupted turns, the compaction summaries and the like); they are not in calls.json. Uncertain which
  is which; the 2,175 are the calls whose size is known.

### How compactions are marked

A compaction writes two records, both with the same timestamp:

1. `{"type": "system", "subtype": "compact_boundary", "compactMetadata": {...}}` with `trigger` (`manual` = Lati's
   `/compact`; `auto` = the harness), `preTokens` (the harness's count of the context just before), `postTokens`
   (the count after: the summary), `durationMs` (how long the summary took), plus the preserved-segment uuids.
2. A `user` record with `"isCompactSummary": true` (and `isVisibleInTranscriptOnly`) whose text begins "This session
   is being continued from a previous conversation that ran out of context…": the summary itself.

A manual one is preceded by Lati's `/compact` command (a `user` record `<command-name>/compact</command-name>` with
Kiln's keep-list in `<command-args>`) and the PreCompact hook's backup message (`<local-command-stdout>Compacted
PreCompact ["$HOME/workshop/bin/backupsessions" --hook] …`). The boundary record is the time used here.

## Files

### calls.json (Kiln's main-session model calls)

`fields` names the columns of each row in `rows` (arrays, to keep the file small; 2,175 rows, ~145 KB):

| field | meaning |
|---|---|
| `t` | seconds since the window start |
| `ts` | UTC time of the call's first record |
| `ctx` | context tokens at the call: input + cache_read + cache_creation |
| `out` | output tokens |
| `in`, `cache_read`, `cache_creation` | the three parts of `ctx`, as reported |
| `model` | index into `models` (all calls are `claude-opus-5-5`) |

Subagent calls are not here; they are in agents.json.

### compactions.json

`rows`: the 6 compactions of Kiln's session in the window (all manual: 4, 7, 8, 9, 11 and 12 Nov).

| field | meaning |
|---|---|
| `t`, `ts` | the `compact_boundary` record's time |
| `trigger` | `manual` or `auto` |
| `pre_tokens`, `post_tokens`, `duration_ms` | from `compactMetadata` (the harness's own counts) |
| `ctx_last_call_before`, `last_call_before_ts` | the context of Kiln's last call before the boundary (measured, from usage) |
| `ctx_first_call_after`, `first_call_after_ts` | the context of the first call after it. It is ~60-70k above `post_tokens` because a call also carries the system prompt and tool definitions |
| `stage_heading`, `stage_date` | the film-3 stage: the newest decisions.md heading committed before the compaction |
| `stage_heading_committed` | when that heading first appeared in a commit of decisions.md |

`just_outside_window`: compactions within a day of the start but before it. One matters to the story: an **auto
(idle) compaction at 2026-11-01T18:35:26Z**, 8 minutes before film 3's first commit (preTokens 716,568, postTokens
22,232). Lati's message at 18:49Z (turns.json) is about it (the text is not in this data).

Uncertain: the stage is by commit time. A heading written but committed later would place a compaction one stage
early; Kiln committed decisions as he went, so the error is at most minutes.

### commits.json

Film 3's 331 commits, oldest first (`git log --numstat`, author time).

| field | meaning |
|---|---|
| `t`, `ts` | author time (one commit has a committer time 17 s later; author time is used) |
| `hash` | first 8 characters |
| `subject` | the first line, as written |
| `tag` | the prefix before the first `: ` (e.g. `gfx (Kiln)`, `decisions, status (Kiln)`); every commit has one. Two of Flint's commits use `Claude (Flint, cloud)` as the whole prefix, so their `tag_word` is `Claude` |
| `tag_word` | the tag without the parenthesis (`gfx`, `decisions, status`) |
| `signed` | the parenthesis (`Kiln`, `Flint, cloud`, `Kiln's helper`, `agent A, Kiln`, …) |
| `files` | files changed |
| `added`, `removed` | lines, text files only |
| `binary_files` | files git counts as binary (their lines are not counted) |

### spend.json

Every line of `production/motion/ledger.jsonl` (214), oldest first. The ledger records each paid job twice: a
`submitted` line and a `completed` (or `failed`) line.

| field | meaning |
|---|---|
| `t`, `ts` | the ledger's `at`, which is **local time without a zone** (`time.strftime` in `tools/seedance.py`): converted from +02:00 |
| `job` | the last 8 characters of the job id |
| `batch`, `clip` | as in the ledger |
| `shot` | `sNNN` from the clip id, or null (`T1-D`, `Q1`) |
| `status` | `submitted`, `completed`, `failed` |
| `model`, `kind`, `seconds`, `resolution` | from the job's `submitted` line (the `completed` line doesn't repeat them) |
| `model_source` | `ledger`, or for T1-D and Q1 (no model in the ledger) `file name …`: inferred as Seedance 2.5 from their files' names in `media/motion` |
| `estimate_usd` | as written: the estimate on `submitted` lines; the ledger writes 0 on `completed` and `failed` lines |
| `cost_usd` | OpenRouter's reported cost, on `completed` lines only; failed jobs cost nothing |
| `total_usd` | running total of `cost_usd` through this line |
| `error` | the refusal reason on `failed` lines, with the provider's request id removed |
| `file` | the ledger's path for the take |

Total **$86.74** over 102 completed jobs; 5 failed (copyright filter, free). **Only OpenRouter is in the ledger.**
ISEKAI ZERO credits (plates, the opening batch, the s078/s080 takes, etc.: in credits, recorded per batch in the
motion and images docs, e.g. `motion/opening-results.md`) and Lati's Grok subscription are not; no USD figure for
them is given here.

### notes.json

Every Lati quote in film 3's `production/decisions.md` dated 1 Nov 2026 or later: 167 rows, 166 in the window.

| field | meaning |
|---|---|
| `t`, `ts` | when Lati sent it (see `time_source`) |
| `in_window` | false for one: "In preparation for the 3rd film…" (the message that opened film 3) was sent at 18:35:26Z, 8 min before the first commit |
| `time_source` | `transcript`: matched to his message in Kiln's transcript (164); `commit`: the time the quote first appeared in a commit of decisions.md (3, all said **to Flint**, the cloud session, so not in Kiln's transcript) |
| `transcript_matches` | how many of his messages contained the quote (1 for every matched note) |
| `date` | the date written in the attribution `(Lati, 11 Nov 2026, …)`, or the entry's date |
| `heading`, `heading_date` | the entry (`## date · heading`, or a bold `**date · heading**` entry in the file's preamble) |
| `decisions_line` | line number of the quote in decisions.md |
| `to` | `Kiln`, or `Flint` when the attribution says "to Flint" |
| `quote` | his words **verbatim** as decisions.md records them, typos included; the outer quotation marks removed. A quote wrapped over several `>` lines is joined with spaces; an empty `>` line is kept as a paragraph break (`\n\n`) |
| `context` | the rest of the attribution after the date (what he was looking at), or null |
| `part` | 1 or 2 when Kiln recorded two of Lati's messages in one line (`"a" and "b" (Lati, …)`); each is its own row with its own time. Split only where both halves match separate messages |
| `responder` | who answered in the log: `Kiln` or `Flint` |
| `response_first_sentence` | the first sentence of that answer: the `Claude (Kiln, local): …` paragraph after the quote, or the text after `(Lati, …):` on the same line |
| `response_directly_after` | false when another Lati quote stands between this one and the answer (the answer covers both) |

How quotes are found: blockquotes ending in `" (Lati…)`, plus the preamble's bold entries attributed `(Lati)`.
Left out: Lati's words quoted inline inside Kiln's paragraphs (one in the window's dates, 1 Nov: `Lati: "save this
permission…"`, and paraphrases such as `(Lati: usable)`), and the run files' quotes (their verdicts are in
takes.json).

Times: decisions.md dates are local days. A quote matched in the transcript is checked against its written date
(allowing his small hours after midnight and late evening of the day before); a few "late" quotes therefore have a
UTC date one day off their written date.

### agents.json

Kiln's subagent runs that started in the window: 22 (from `subagents/agent-*.jsonl` and `.meta.json`). This data
agent's own run (it started after the window end) is not included.

| field | meaning |
|---|---|
| `id` | the agent id |
| `description`, `agent_type` | from the run's `.meta.json` (the label Kiln gave it) |
| `start`, `end` (+ `start_t`, `end_t`) | first and last record of the run. Graphics agents A, B and C of 12 Nov were resumed after their first pass (Kiln sent them notes), so their spans run from 00:59Z to 07:22-07:50Z with idle gaps; D ran 00:59-01:09Z |
| `calls`, `output_tokens`, `peak_context` | deduped by message id, as for Kiln |
| `models` | model ids used (one agent, the claude-code-guide, ran on `claude-haiku-5-5`) |
| `log` | the graphics agents' own log in film 3 (`production/edit/agents/<section>.md`), else null |
| `series` | every call: `[t, ctx, out]` |

### takes.json

Every generated take named in the ledger, `production/edit/takes.json`, a run file's take table
(`motion/*-run.md`, `motion/opening-results.md`) or the final cut: 134 rows.

| field | meaning |
|---|---|
| `t`, `ts` | the ledger's completion (or failure) time; null for takes not in the ledger (ISEKAI ZERO, Grok) |
| `take` | the file name without `.mp4`; for a failed job, `<clip> (job <id>)` |
| `file` | path in film 3's repo (media is local, not in git) |
| `shot`, `batch` | the shot (`sNNN`), the batch (ledger batch, or the clip folder) |
| `sources` | which of `ledger`, `takes.json`, `run-md`, `timeline` name it |
| `ledger_status` | `completed`, `failed`, or null (not a paid OpenRouter job) |
| `model`, `seconds`, `cost_usd` | from the ledger |
| `default_take` | takes.json makes it the shot's default |
| `in_cut` | it plays in `production/edit/timeline.json` (Lati's cut, saved 2026-11-12 02:15:18 local) |
| `cut_clips` | how many timeline clips use it |
| `cut_note` | anything odd: a ledger path not on disk, a refusal reason, a shot played as a graphics render |
| `verdict`, `verdict_source` | the Lati column of the run file's table, as written (sometimes his words in quotes, mostly Kiln's summary of his verdict); null where the table has none |
| `on_disk` | the file exists |

Resolving the cut: timeline clips that point at `media/clips/shot/<shot>.mp4` are symlinks (set by `tools/shots.py`)
and are followed to the take; they were last set 11 Nov 23:53 local, before the cut was saved, and are read as they
are now. Three shots (s050, s067, s075) play as **locked graphics renders** (`media/gfx/locked/`), so their source
takes are not resolved; those takes carry a `cut_note` and `in_cut` false. `rough-1` (s002 in the cut) is motion
test 1's rough cut, an edit, not counted as a take made. Lati's three Grok takes in the cut are included; his other
Grok takes and ISEKAI ZERO test takes on disk are listed by name only in `clips_on_disk_not_referenced` (18 files:
some are reels or comparisons, not takes).

### turns.json

Lati's messages to Kiln in the window: time and length only, no text. 279 rows.

| field | meaning |
|---|---|
| `t`, `ts` | when it arrived |
| `kind` | `message` (271), `compact-command` (his `/compact`, 6; its length is the keep-list Kiln drafted for it), `interrupt` (2) |
| `mid_turn` | true for the 23 messages he sent while Kiln was working: those are not `user` records but `attachment` records of type `queued_command` (`humanTurn: true`), folded into Kiln's running turn |
| `chars` | characters of text |
| `images` | images attached |

A `user` record counts as his message when `origin.kind == "human"`. Tool results, subagent hand-backs
(`origin.kind == "peer"`), task notifications, image placeholders (`isMeta`) and the compaction summaries are not.

### sessions.json

The other local sessions in `~/.claude/projects/-home-shegs-Claudia/` with records in the window: 10, each with its
first 8 id characters, its overall `first`/`last` record, and `calls_in_window`, `output_tokens_in_window`. No content
was read beyond timestamps and usage. They are short (2-10 calls each in the window). `kiln` gives the main session's span.

### summary.json

Headline numbers, each computed from the files above: `days` (window length), `calendar_days_local` (1-12 Nov),
`days_with_kiln_calls_local` (9: no calls on 2, 3 and 5 Nov), `commits`, `lines_added`/`removed`, `calls`,
`output_tokens`, `peak_context` (+ when), `compactions`, `lati_messages` (kind `message`), `takes_made` (rows of
takes.json with a file on disk that are not failed jobs and not rough-1), `takes_in_cut`, `paid_jobs_completed`/
`failed`, `spend_usd` (OpenRouter only), `paid_seconds` (seconds requested in paid jobs), `agents`, `agent_calls`,
`agent_output_tokens`, `notes`, `notes_in_window`, `other_sessions_in_window`.

### privacy-scan.json

The filter's report. Every string written passes through it: the values in film 3's, Claudia's and checked-me's
`.env` files (read in memory, never written), every e-mail address (Lati's included; it is not named in the
script), `sk-…` and `or-…` keys, `Bearer …`, hex runs of
32+, mixed-case alphanumeric runs of 32+, padded base64. After writing, every file in data/ is read back and scanned
again. Lati's health: notes are scanned for health words; hits are listed by decisions.md line for a person to look
at, not removed (the quotes stay verbatim).
