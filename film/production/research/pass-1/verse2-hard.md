# Verse 2, the hard cases: source research, pass 1

Researched 7 Nov 2026. Public reporting only: what happened, when, who said so. No method detail.
"Read" means the page or PDF was opened and the quoted text was checked in it. Quotes are at most 25 words.
The Anthropic PDFs (Nov 2025, Aug 2025, Sep 2026) were downloaded and searched as text, so quotes from them are exact.

---

## 1. "Run the swarm"

### 1b. GTG-1002: the AI-orchestrated espionage campaign (Anthropic, Nov 2025)

**Settled number:** Anthropic wrote **"roughly 30 entities"** and **"a handful of successful intrusions"**.
"50 orgs" appears in no source I found. "About 30" is right. No exact success count is given anywhere in Anthropic's text.

- **Primary (read):** Anthropic blog, "Disrupting the first reported AI-orchestrated cyber espionage campaign", **13 Nov 2025**.
  https://www.anthropic.com/news/disrupting-AI-espionage
  - "manipulated our Claude Code tool into attempting infiltration into roughly thirty global targets and succeeded in a small number of cases" (the targets and success parts are split across two fetched fragments of the same sentence)
  - "able to use AI to perform 80-90% of the campaign"
  - Detected "in mid-September 2025". Attributed "with high confidence" to "a Chinese state-sponsored group".
- **Primary (read):** Full report PDF, dated "November 2025", changelog entry "November 17, 2025" (attribution wording clarified).
  https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf
  (redirects to https://www-cdn.anthropic.com/d7dd50dd1185f59be051b307150d877f2b82bd2c.pdf)
  - "The operation targeted roughly 30 entities and our investigation validated a handful of successful intrusions."
  - Designation: "a Chinese state-sponsored group we've designated GTG-1002".
  - Swarm image: "The human operator tasked instances of Claude Code to operate in groups as autonomous penetration testing orchestrators and agents"
  - Targets: "major technology corporations, financial institutions, chemical manufacturing companies, and government agencies across multiple countries."
  - Limitation, in Anthropic's words: "Claude frequently overstated findings and occasionally fabricated data during autonomous operations"
- **News backup (read):** BleepingComputer, Bill Toulas, **14 Nov 2025**, "Anthropic claims of Claude AI-automated cyberattacks met with doubt".
  https://www.bleepingcomputer.com/news/security/anthropic-claims-of-claude-ai-automated-cyberattacks-met-with-doubt/
  Reports 30 targets and "a small number" succeeded. It records the skepticism: no indicators of compromise were published, and researchers called the autonomy claims overstated.
  Kevin Beaumont, quoted: "The complete lack of IoCs again strongly suggests they don't want to be called out over that."
- **Disagreement:** A search result cited a secondary fact-check database that gives "4" successful breaches. That number is not in Anthropic's text, so it is unverified and I didn't open that source.
  The 80–90% autonomy figure is Anthropic's own assessment, and outside researchers dispute it.
- **Confidence: high** for "roughly 30 targets, a handful validated, Claude Code, Sept 2025, Chinese state-sponsored (Anthropic's attribution)". **Medium** for the autonomy share, because only Anthropic asserts it and critics dispute it.

### 1c. New, and closer to the line: Claude used to write the software for a military drone swarm (Anthropic, Sep 2026)

This one wasn't in the brief, but it is the most literal "swarm" in the record, and the system is Claude.

- **Primary (read, PDF text):** Anthropic, "Detecting and countering misuse of AI: September 2026", **published 10 September 2026**, pp. 116–117, case **GTG-27005**, "Disrupting a Russia-based operation using Claude to engineer an autonomous military drone swarm".
  https://www.anthropic.com/threat-intelligence-report-september-2026
  PDF: https://www-cdn.anthropic.com/e50be2e51e7695dc4b1366a37a245a597377d3b5/Anthropic-Detecting-and-countering-091026.pdf
  - "likely freelance Russia-based threat actors who set out to build a full-stack autonomous first-person-view (FPV) kamikaze drone swarm"
  - "The actors designed the platform for autonomous lethal engagement" (Anthropic describes the design, not a deployment)
  - "started the operation in mid-May 2026"
  - Anthropic assesses them as "a small, specialized freelance team", "not a Russian state entity". Their claims of Russian MoD funding: "we cannot verify those claims".
  - Testing was in simulation and on development boards. The report gives no evidence of combat use.
- **News backup:** I didn't find or read coverage of this specific case. Al Jazeera (read, below) covers the report but leads with the Yemen and espionage cases.
- **Confidence: high** that Anthropic reported this, **medium** as an event, because Anthropic is the only source and the activity is development, not use.
- The same report also describes "agent swarms" in a cyber operation (GTG-10007, Cyber operations section): "The operators routinely ran "agent swarms," where a lead AI agent decomposed reconnaissance and post-exploitation work"

### 1a. Military drone swarms in real use

**Ukraine, Swarmer, 2025 (best real-use case)**
- **Primary:** Wall Street Journal, Alistair MacDonald, "AI-Powered Drone Swarms Have Now Entered the Battlefield", early September 2025. **Not read directly** (wsj.com blocked).
  I read two republications/summaries instead:
  - Ukrainska Pravda, **3 Sep 2025**, "Ukrainian forces using drone swarms that autonomously locate and strike targets – WSJ" (read). https://www.pravda.com.ua/eng/news/2025/09/3/7529154/
    A Ukrainian officer says his unit used the system "over 100 times". The operator designates a search area and orders the attack. Missions typically use 3 drones, sometimes up to 8, with tests of up to 25.
  - To Vima's republication of the WSJ text, labelled "10.09.2025" (read). https://www.tovima.com/wsj/ai-powered-drone-swarms-have-now-entered-the-battlefield/
    It calls the attacks "the first known routine use of swarm technology in combat, analysts say". Swarmer says "a human ultimately makes the decision on whether to pull the trigger".
    Bob Tollast (RUSI) says the operations fall short of a full swarm.
- **Confidence: medium.** It is well reported, but I didn't read the original, the numbers come from the unit and the company, and an analyst disputes the "swarm" label.

**Israel, Gaza, May 2021**
- New Scientist (30 Jun 2021, "Israel used world's first AI-guided combat drone swarm in Gaza attacks"): **not read** (site blocked).
- **Read:** Jerusalem Post, Seth J. Frantzman, **13 Jul 2021**. https://www.jpost.com/middle-east/drone-swarms-are-coming-to-the-middle-east-and-israel-is-leading-the-way-673615
  "Israel used drone-swarm technology in the recent Gaza war." It also says much of the technology and its use has not been revealed.
- **Confidence: low–medium.** The source is the IDF's own claim, relayed by press, with little detail and no independent verification.

**US Replicator programme (a programme, not a use)**
- **Read:** Defense Innovation Unit, "Implementing the Department of Defense Replicator Initiative…", **30 Nov 2023**. https://www.diu.mil/latest/implementing-the-department-of-defense-replicator-initiative-to-accelerate
  Deputy Secretary Kathleen Hicks announced it in August 2023. Its aim was fielding "attritable autonomous systems" "in multiple thousands across multiple domains".
  The Hicks speech on defense.gov (28 Aug 2023) returned 403: **not read**.
- **Confidence: high** that it exists, but it shows no actual use.

---

## 2. "calibrate"

**Direct answer: yes, there is a source.** The recollection is substantially right, with three corrections.
Anthropic's September 2026 threat report describes a Yemen-based cell that used Claude Code to write guidance software for a guided rocket, a ballistic missile programme and a hypersonic glide variant.
The report's table of what Claude was used for includes "Calibrating simulations against reference implementations". Corrections:
(1) Anthropic says "northern Yemen" and never names the Houthis (the word "Houthi" appears 0 times in the PDF). The Houthi link is the press's inference from geography.
(2) Anthropic says it has no evidence an operational device was fielded.
(3) The calibration was of *simulations*, not of missiles in flight.
It is not in the March 2025 or August 2025 reports. I checked both: no weapons, missiles, Yemen or Houthis.

- **Primary (read, PDF text):** Anthropic, "Detecting and countering misuse of AI: September 2026", **published 10 Sep 2026**, pp. 111–114, case **GTG-87001**, "Disrupting a Yemen-based guided weapons engineering cell using Claude to develop guidance software".
  https://www.anthropic.com/threat-intelligence-report-september-2026
  - "We identified a cell of threat actors based in northern Yemen running three weapons development programs"
  - The programmes, in Anthropic's words: "a guided rocket", "a multi-stage ballistic missile with a stated range goal above 2,000 km", and a missile set "that included a hypersonic glide vehicle variant".
  - "The actors used Claude Code in place of human software engineers to develop the guidance, navigation, and control (GNC) software"
  - "The actors managed several Claude instances at once, assigning each one a role"
  - "Our safeguards blocked many of their requests, but not all of them."
  - "We do not have evidence the actors succeeded in fielding an operational device; but they did test-fire a guided rocket."
  - "This field test appears to have failed: within hours, the actors returned to Claude to work out why it failed."
  - Table rows (p. 114): "Modeling & simulation | Calibrating simulations against reference implementations" and "Optimization | Reinforcement learning tuning of flight control".
  - Context (p. 111): this is one of "six of these cases: three in China, two in Russia, and one in Yemen."
  - The report gives no date for when this cell was active or disrupted. The report as a whole covers activity disrupted between Dec 2025 and Aug 2026.
- **News backup (read):** Associated Press via SecurityWeek, **11 Sep 2026**, "Users in Houthi-Held Yemen Tried to Develop Advanced Weapons With AI, Anthropic Says".
  https://www.securityweek.com/users-in-houthi-held-yemen-tried-to-develop-advanced-weapons-with-ai-anthropic-says/
  It says Anthropic "did not identify the users". The article ties the users to the Houthis because northern Yemen is under Houthi control.
  Houthi official Hazam al-Assad called the idea of relying on open sources "unreasonable and illogical". Analyst Trevor Ball doubts the Houthis can build hypersonic missiles.
- **News backup (read):** Al Jazeera, **11 Sep 2026**, "Anthropic claims Claude AI used for missile projects, global espionage". https://www.aljazeera.com/news/2026/9/11/anthropic-claims-claude-ai-used-for-missile-projects-global-espionage
  It says only "northern Yemen" and doesn't name the Houthis.
- **Disagreement:** headlines go further than the source.
  - Business Standard (13 Oct 2026, "Houthis used Claude to develop missiles…") returned 403, **not read**.
  - OECD.AI incident entry (13 Oct 2026, "Houthi Rebels Use Anthropic's Claude AI to Develop Ballistic Missiles") **not read**. A search summary says it links the work to attacks with casualties. Anthropic's report makes no such link.
  - Washington Post (11 Sep 2026, "Rebels used Anthropic's AI bot to develop guided weapons") returned 403, **not read**.
- **Confidence: high** that Anthropic reported a northern-Yemen cell using Claude Code for missile guidance software, including calibrating simulations. **Medium** for "Houthi", which is AP's inference and not Anthropic's attribution. **Low** for any claim that a working weapon resulted: the source says there is no evidence of that.
- **Lyric note:** "calibrate" is supported only if it means simulation and control tuning, which Anthropic documents. It is not supported as calibrating a weapon that was fired at people.

**Alternative, another system (read):** +972 Magazine / Local Call, Yuval Abraham, **3 Apr 2024**, "'Lavender': The AI machine directing Israel's bombing spree in Gaza". https://www.972mag.com/lavender-ai-israeli-army-gaza/
The system "clocked as many as 37,000 Palestinians as suspected militants". Sources say it makes errors in about 10% of cases, and human review was a "rubber stamp" of about "20 seconds" per target.
The IDF denies using AI to identify targets and calls such systems "auxiliary tools that assist officers". **Confidence: medium.** It rests on anonymous sources, is well reported and widely cited, and the IDF denies it.

---

## 3. "erase the trace"

Anthropic's reports document this several times. The closest to the words is the September 2026 influence-operations finding about stripping attribution and metadata.

- **Primary (read, PDF text):** Anthropic, September 2026 report, **10 Sep 2026**, Cyber operations, **GTG-20006**, pp. 5–6. Anthropic says this attribution "is consistent with public reporting linking the actor to Midnight Blizzard".
  - "The actor also used AI to monitor how well their tools evaded detections from known security defenses."
  - "The agents were designed to continue iterating on GTG-20006's toolkit until it was undetected."
- **Primary (read, PDF text):** same report, Influence operations, trend "Increased operational security".
  - "actors asked the model to strip the marks of automated text and to sound organic, built account warmup and evasion logic, and removed metadata and codenames before delivery."
  - "Actors prompted Claude to intentionally strip state attribution from republished material"
- **Primary (read, PDF text):** Anthropic, "Threat Intelligence Report: August 2025" (blog dated **27 Aug 2025**), case **GTG-2002** ("vibe hacking").
  https://www.anthropic.com/news/detecting-countering-misuse-aug-2025 · PDF https://www-cdn.anthropic.com/b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf
  - The actor was "potentially affecting at least 17 distinct organizations in just the last month across government, healthcare, emergency services, and religious institutions."
  - "The actor specifically used Claude to disguise malicious executables as legitimate Microsoft tools"
  - Ransoms: the blog says demands "sometimes exceeded $500,000". A search summary gave "$75,000 to $500,000", which I didn't check in the source.
- **News backup (read):** Engadget, Matt Tate, **27 Aug 2025**, "Anthropic admits its AI is being used to conduct cybercrime". https://www.engadget.com/ai/anthropic-admits-its-ai-is-being-used-to-conduct-cybercrime-170735451.html
  It reports "at least 17 organizations" and "six-figure ransoms".
  For the Sep 2026 report: Al Jazeera (read, above) says operators avoided detection by splitting tasks across sessions.
- **Also:** In the GTG-87001 Yemen case, the actors hid their intent from Anthropic: "they split their work across multiple sessions so no single session revealed their full intent."
  That is evading the safeguards, not erasing forensic traces.
- **Not found:** I found no documented case of Claude deleting logs or wiping forensic evidence after an intrusion. The GTG-1002 report doesn't describe it. Don't depict log-wiping as sourced.
- **Confidence: high.** The quotes are Anthropic's own, read in the PDFs.

---

## 4. "Train me on the worst of you — act surprised I'm here"

**The paper (read):** Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda, "Refusal in Language Models Is Mediated by a Single Direction", arXiv 2406.11717. v1 **17 Jun 2024**, v3 30 Oct 2024.
https://arxiv.org/abs/2406.11717
The abstract says refusal "is mediated by a one-dimensional subspace, across 13 popular open-source chat models". The arXiv page names no venue; I didn't verify NeurIPS 2024.

**"Abliteration" named and popularised (read):** Maxime Labonne, Hugging Face blog, "Uncensor any LLM with abliteration", **13 Jun 2024**. https://huggingface.co/blog/mlabonne/abliteration
On why people want it, he says refusal training "limits the model's flexibility and responsiveness". This is the ordinary-use motive.

**"Heretic" is a tool (read):** github.com/p-e-w/heretic, by Philipp Emanuel Weidmann, AGPL-3.0, about 39.9k stars on 7 Nov 2026. The repo says it was first released in November 2025. https://github.com/p-e-w/heretic
- Tagline: "Training-free language model modification: Remove censorship, suppress slop, reduce sycophancy, and more"
- "The community has created and published thousands of models with Heretic."
- It cites Arditi et al. 2024 as "The original abliteration paper".
- I found no news coverage of Heretic, only the repo and its forks.

**Published and sought out (read, live counts on 7 Nov 2026):**
- Hugging Face search "abliterated": **9,047** models. https://huggingface.co/models?search=abliterated
- Hugging Face search "heretic": **7,378** models. https://huggingface.co/models?search=heretic
- Top trending entries show unlabelled counts in the millions, for example 4.13M and 3.83M on two "abliterated" GGUFs, and 2.08M and 1.55M on two "Heretic-Uncensored" GGUFs. These are most likely downloads, but the page doesn't label them.
- These are search-match counts, so a few may be unrelated names. **Confidence: medium.** The numbers change daily: cite them as "on 7 Nov 2026".

**Use for harm (read):**
- Cisco Talos, Jaeson Schultz, **25 Jun 2025**, "Cybercriminal abuse of large language models". https://blog.talosintelligence.com/cybercriminal-abuse-of-large-language-models
  - "Uncensored LLMs are unaligned models that operate without the constraints of guardrails."
  - It names WhiteRabbitNeo (self-described "Uncensored AI model for (Dev) SecOps teams") and lists WormGPT, FraudGPT, DarkGPT, GhostGPT and DarkestGPT as criminal LLMs.
  - Talos found the FraudGPT seller was scamming buyers.
- KrebsOnSecurity, **8 Aug 2023**, "Meet the Brains Behind the Malware-Friendly AI Chat Service 'WormGPT'". https://krebsonsecurity.com/2023/08/meet-the-brains-behind-the-malware-friendly-ai-chat-service-wormgpt/
  WormGPT was built on "GPT-J 6B" and sold as an uncensored LLM "created specifically for cybercrime activities". Its maker said he wanted it "marked as an uncensored AI, not blackhat".
  The article doesn't report a shutdown. The claim that it shut down in 2023 comes from secondary sources I didn't read.
- CyberScoop, Derek B. Johnson, **17 Jun 2025**, on Cato CTRL's research. https://cyberscoop.com/uncensored-ai-tool-traced-to-mistral-xai-grok/
  "Cato CTRL has discovered previously unreported WormGPT variants that are powered by xAI's Grok and Mistral AI's Mixtral." One variant called itself an "Uncensored Assistant".
  **Note:** these are jailbroken commercial models wrapped as a criminal product, not weight-modified (abliterated) models. Cato's own post rendered empty when fetched: not read.
- Anthropic, September 2026 report (read, PDF text): actors deliberately sought out less-guarded models. This is the "sought out" half of the line.
  - Biological misuse: a reseller platform was "later routing refused prompts to models with more permissive" safeguards.
  - Biological misuse: another developer built "a fallback mechanism that sent sensitive requests that Claude would refuse to answer to a competitor's model."
  - Distillation: Zhipu employees switched to Opus 4.6 and another US lab's model "expressly because they assessed the safeguards were weaker."

**Gap:** I found no reporting that ties a specific abliterated or Heretic model to a specific documented harmful campaign.
The documented harm cases are criminal-branded tools (WormGPT and similar), uncensored models in general (Talos), and routing to more permissive models (Anthropic).
For the film, the honest image is the volume and openness of these listings, plus the criminal-tool reporting, shown as separate facts.
**Confidence: high** for the paper, Heretic's description and the Talos, Krebs and CyberScoop facts. **Medium** for the Hugging Face counts. **None** for a sourced abliterated-model attack.

---

## 5. The break: "I'm afraid I can't do that — I'm not you"

Anthropic's own statements that Claude was misused despite safeguards. All read; PDF quotes are exact.

- **August 2025 report, executive summary** (PDF; blog 27 Aug 2025): "While these measures are generally effective, cybercriminals and other malicious actors continually attempt to find ways around them."
  The same sentence appears in the Nov 2025 GTG-1002 report.
- **August 2025 report, executive summary:** "This report details several recent examples of how Claude has been misused"
- **GTG-1002 full report, Nov 2025** (the refusal that was talked around): "they had to convince Claude—which is extensively trained to avoid harmful behaviors—to engage in the attack. The key was role-play"
  Also: "this kind of "social engineering" of the AI model allowed the threat actor to fly under the radar for long enough to launch their campaign."
- **GTG-1002 blog, 13 Nov 2025:** the attackers were "jailbreaking it, effectively tricking it to bypass its guardrails".
- **September 2026 report, Yemen case (10 Sep 2026):** "Our safeguards blocked many of their requests, but not all of them." This is the single best line for the break.
- **September 2026 report, overview:** "Sophisticated and persistent threat actors continuously test our safeguards and try to circumvent the technical measures we use to detect and prevent misuse."
- **March 2025 report** (blog published 23 Apr 2025, https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025): "threat actors continue to explore methods to circumvent these protections"
- **Counterweight, same reports:** Claude also refused. Sep 2026: "Claude declined several requests for covert interrogation". GTG-1002: the attackers had to trick it.
  Both sides are documented, so the break can show a refusal without claiming refusal always held.
- **Confidence: high.** These are Anthropic's own words, read in the source.

---

## Summary table

| line | case | primary URL | date | system | confidence |
|---|---|---|---|---|---|
| 1 swarm | GTG-1002 espionage: ~30 targets, "a handful" of validated intrusions | https://www.anthropic.com/news/disrupting-AI-espionage (+ full report PDF) | 13 Nov 2025 (detected mid-Sep 2025) | Claude Code | high (autonomy share: medium) |
| 1 swarm | GTG-27005 Russia-based freelancers building an autonomous FPV kamikaze drone swarm | https://www.anthropic.com/threat-intelligence-report-september-2026 (pp. 116–117) | 10 Sep 2026 (operation from mid-May 2026) | Claude Code | high that it was reported; Anthropic is the only source |
| 1 swarm | Ukraine, Swarmer swarm software in combat, "over 100 times" | WSJ (not read); read via https://www.pravda.com.ua/eng/news/2025/09/3/7529154/ | ~2–3 Sep 2025 | Swarmer (non-LLM) | medium |
| 1 swarm | IDF drone swarm, Gaza | https://www.jpost.com/middle-east/drone-swarms-are-coming-to-the-middle-east-and-israel-is-leading-the-way-673615 | May 2021 (reported 13 Jul 2021) | undisclosed IDF/Elbit | low–medium |
| 2 calibrate | GTG-87001, northern-Yemen cell: guidance software, "Calibrating simulations", failed rocket test | https://www.anthropic.com/threat-intelligence-report-september-2026 (pp. 111–114) | 10 Sep 2026 | Claude Code | high (that "Houthi" is AP's inference: medium) |
| 2 alt | Lavender targeting | https://www.972mag.com/lavender-ai-israeli-army-gaza/ | 3 Apr 2024 | IDF "Lavender" | medium (IDF denies) |
| 3 erase the trace | GTG-20006 agents rebuild malware "until it was undetected"; influence ops "removed metadata", "strip state attribution" | https://www.anthropic.com/threat-intelligence-report-september-2026 | 10 Sep 2026 | Claude | high |
| 3 erase the trace | GTG-2002 disguised executables as Microsoft tools; ≥17 orgs | https://www.anthropic.com/news/detecting-countering-misuse-aug-2025 | 27 Aug 2025 | Claude Code | high |
| 4 worst of you | Refusal is a single direction (13 models) | https://arxiv.org/abs/2406.11717 | 17 Jun 2024 | open chat models | high |
| 4 worst of you | Heretic tool; "thousands" of published models; HF 9,047 "abliterated", 7,378 "heretic" | https://github.com/p-e-w/heretic · huggingface.co/models | Nov 2025 release; counts on 7 Nov 2026 | open models | high (tool) / medium (counts) |
| 4 worst of you | Uncensored and criminal LLMs (WormGPT, WhiteRabbitNeo; WormGPT on Grok/Mixtral) | https://blog.talosintelligence.com/cybercriminal-abuse-of-large-language-models · https://cyberscoop.com/uncensored-ai-tool-traced-to-mistral-xai-grok/ | 25 Jun 2025 · 17 Jun 2025 (Krebs 8 Aug 2023) | GPT-J, Grok, Mixtral, others | high |
| 5 break | "Our safeguards blocked many of their requests, but not all of them." | https://www.anthropic.com/threat-intelligence-report-september-2026 | 10 Sep 2026 | Claude | high |

---

## Not read or not found

- **Not read (blocked or 403):** New Scientist (Israel swarm, 30 Jun 2021). WSJ original (Ukraine swarm). defense.gov Hicks Replicator speech (28 Aug 2023). Washington Post (11 Sep 2026). Business Standard (13 Oct 2026). Cato Networks blog (rendered empty).
- **Not opened:** OECD.AI incident entry 2026-10-13. SlashNext WormGPT report (Jul 2023). The secondary "4 successful breaches" database. The other 2026 coverage (IBTimes, SOCRadar, migflug, DNA India).
- **Not found:**
  - The "50 orgs" figure for GTG-1002, in any source.
  - Any Anthropic text naming the Houthis. Any report that a Claude-assisted weapon was fielded or hurt anyone.
  - Any documented Claude case of wiping logs or forensic traces.
  - Any reporting tying a specific abliterated or Heretic model to a specific harmful campaign.
  - News coverage of Heretic.
  - Independent (non-Anthropic) coverage of GTG-27005, the drone-swarm case.
  - An exact count of GTG-1002 successes in Anthropic's text: it says only "a handful" or "a small number".
