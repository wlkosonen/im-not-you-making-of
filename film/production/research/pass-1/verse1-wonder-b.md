# Verse 1 (wonder), lines 4–6: source check

Pass 1, part b. Researched 7 Nov 2026. Public announcements and news only.

Method note: every source marked "read" was opened with WebFetch in this pass. WebFetch returns the page through an
extraction step, so quotes below are as that step returned them. Check a quote against the live page before it goes
on screen or into a public note. Sources that blocked the fetch are listed at the end and are not cited as checked.

---

## Line 4. "Read the scan, flag the shadow — caught before it's found"

### Case 4a. Mia (Kheiron Medical) as an extra reader in Hungary: peer-reviewed, prospective

- **Primary:** Ng A.Y. et al., "Prospective implementation of AI-assisted screen reading to improve early detection of
  breast cancer", *Nature Medicine* 29(12):3044–3049, published 16 Nov 2023, DOI 10.1038/s41591-023-02625-9.
  Read via the open PMC copy: https://pmc.ncbi.nlm.nih.gov/articles/PMC10719086/ (nature.com redirected to a login,
  not read there).
  - Supports: Mia was run as an additional reader on top of standard double reading at four Hungarian screening sites
    (April 2021 to January 2023, about 25,000 women); it flagged cases that two radiologists had passed, and a human
    arbitration reader decided on recall.
  - Quote (abstract): "implementing the AI-assisted additional-reader process could achieve 0.7–1.6 additional cancer
    detection per 1,000 cases"
- **Backup (institutional news):** Imperial College London, "New AI tool detects up to 13% more breast cancers than
  humans alone", 17 Nov 2023. https://www.imperial.ac.uk/news/249573/new-ai-tool-detects-13-more/
  - Supports: 24 more cancers than standard reading across the three phases, a 7% relative increase; 70 more women
    recalled; 83% of the extra cancers invasive. Mia "flagged potential false negatives to a third human reader".
  - Note: the "13%" headline is the best single phase (13%, 10%, 5% by phase). The overall figure is 7%.
  - Note: Kheiron funded the study; Imperial co-authored. Not a fully independent source.
- **System:** Mia, Kheiron Medical Technologies (CE-marked class IIa).
- **Human check:** yes, built in. Two radiologists read first; Mia's flags went to a human reader who made the recall
  decision. Mia made no recall decisions.

### Case 4b. Mia in NHS Grampian (GEMINI evaluation), Aberdeen: prospective, press-release level

- **Primary:** University of Aberdeen, "More breast cancers detected in first evaluation of breast screening AI",
  21 Mar 2024. https://www.abdn.ac.uk/news/22964/
  - Supports: first formal prospective UK evaluation of Mia, NHS Grampian, 10,889 patients, funded by a UK Government
    AI in Health and Care Award.
  - Quote: Mia "helped doctors find an additional 12 percent more cancers than in routine practice."
  - The page does not give the "11 women" figure, does not say how the AI flags were reviewed, and does not say the
    results were peer-reviewed. The 30% workload saving is modelled, not measured.
- **Partner release (also read):** Microsoft UK Stories, "AI detects 12% more breast cancers in UK first", 21 Mar 2024.
  https://ukstories.microsoft.com/features/12-more-breast-cancers-detected-with-potential-workload-savings-of-30-in-the-uks-first-prospective-evaluation-of-breast-screening-ai/
  (read at https://ukstories.microsoft.com/?p=79352). Carries the patient story (Barbara, Aberdeen) and quotes her
  doctors' view that her cancer was too small for the human eye. Microsoft hosts Mia on Azure, so this is a partner's
  marketing page, not an independent one.
- **News backup:** Business Insider via Yahoo News Canada, Mikhaila Friel, "A Microsoft-powered medical AI spotted
  cancer in 11 women where doctors didn't", 22 Mar 2024.
  https://ca.news.yahoo.com/microsoft-powered-medical-ai-spotted-161942626.html
  - Supports, attributing to the BBC: 10,889 patients; 11 women whose tumours the radiologists had not seen; Barbara's
    tumour 6 mm; no case where doctors caught a cancer the AI missed.
  - Quote: "The most striking finding was the 11 women where the AI saw tumors too tiny for trained radiologists to notice."
  - The BBC original could not be read (bbc.co.uk / bbc.com are blocked to this tool). The "11 women" and "6 mm"
    figures are therefore second-hand here.
- **Earlier retrospective study (context, also read):** University of Aberdeen, "Grampian team pioneers breast screening
  Artificial Intelligence", 15 Jun 2023. https://www.abdn.ac.uk/news/17096/ About 220,000 mammograms from more than
  55,000 people; Mia "would have suggested recalling 34.1% of the women who went on to develop cancer in between
  screenings." Retrospective, so nothing was caught in practice. Also: Mia was first "too sensitive" and needed local
  tuning; "ongoing quality assurance monitoring is essential."

### Line against source

- **Right:** "Read the scan, flag the shadow" is exactly the role in both cases: the AI reads the mammogram and flags
  it; a human decides. "Caught before it's found" fits the cancers that the standard reading missed and that would
  otherwise have surfaced later (Hungary: 83% invasive, many 10 mm or smaller; Aberdeen: the Barbara case).
- **Overstates if pictured wrongly:** the AI did not diagnose or treat anyone. Every flag went through a radiologist.
  An image of the machine alone "catching" cancer goes past both sources. The honest image is the flag, then a human
  looking again.
- **Scale:** the gain is real but small per scan: 0.7–1.6 more cancers per 1,000 women (Hungary). The 12% (Aberdeen)
  is press-release level, not peer-reviewed in what was read.
- "Caught before it's found" is a paradox that works as long as "found" means found by the usual route (symptoms or
  the next screen). In the Hungary study follow-up was only 2–9 months; whether these early finds save lives is not
  yet shown (Imperial release says longer follow-up is needed).

### Confidence: high (4a), medium (4b)

4a is a peer-reviewed prospective study with a clear human-in-the-loop design, read in full abstract plus an
institutional release. 4b's headline rests on a press release; its most vivid details (11 women, 6 mm) come
second-hand via Business Insider from a BBC piece that couldn't be read.

---

## Line 5. "Draft the brief, translate the voice, give the voiceless words"

The line has three clauses. Only "give the voiceless words" was researched in depth. The earlier candidate Be My AI
fits "translate" (image to speech) more than "voiceless". A brain-computer interface case fits "give the voiceless
words" literally and is added as 5a. Project CETI was checked and is weak for this line (see 5c).

### Case 5a. Speech neuroprostheses: people who lost their voice speaking again

**5a-i. Casey Harrell, ALS, UC Davis / BrainGate2 (NEJM, Aug 2024)**

- **Primary (institution):** UC Davis, "Brain-computer interface allows man with ALS to 'speak'", 14 Aug 2024.
  https://www.ucdavis.edu/news/brain-computer-interface-allows-man-als-speak
  - Supports: 45-year-old man with ALS; four microelectrode arrays (256 electrodes) in the left precentral gyrus;
    attempted speech decoded to words on screen and read aloud in a voice synthesised from recordings of his pre-ALS
    voice. 99.6% word accuracy on a 50-word vocabulary in the first session; 90.2% on 125,000 words in the second;
    97.5% maintained later.
  - Quote (Sergey Stavisky): "The first time we tried the system, he cried with joy as the words he was trying to say
    correctly appeared on-screen."
- **Paper (abstract only, via Europe PMC record):** Card N.S. … Brandman D.M., "An Accurate and Rapidly Calibrating
  Speech Neuroprosthesis", *NEJM* 391(7):609–618, Aug 2024, DOI 10.1056/NEJMoa2314132. nejm.org returned 403; the
  abstract was read through the Europe PMC API. About 32 words per minute, 248+ hours of self-paced conversation,
  8.4 months.
  - Quote: "reached a level of performance suitable to restore conversational communication after brief training"
- **Backup (partner institution):** Brown University, "Brain-computer interface allows man with ALS to 'speak' again",
  14 Aug 2024. https://www.brown.edu/news/2024-08-14/bci-speak-again Harrell: "Not being able to communicate is so
  frustrating and demoralizing. It is like you are trapped."
- **System:** BrainGate2 investigational BCI, decoding software by the UC Davis Neuroprosthetics Lab.
- **Is it "AI"?** Not stated in what was read. The UC Davis release mentions "machine-learning programs" only about
  earlier systems; Brown's release does not mention AI; the NEJM abstract mentions no neural network or language
  model. The decoder is very likely machine learning, but that was not confirmed from the sources read. Don't label
  this one "AI" on screen without reading the paper's methods.
- **Human check:** Harrell sees the decoded words on screen in real time; the system was continuously recalibrated by
  the research team.

**5a-ii. Ann Johnson, brainstem stroke, UCSF / UC Berkeley (Nature, Aug 2023): explicitly AI**

- **Paper (abstract, via Europe PMC record):** Metzger S.L. … Chang E.F., "A high-performance neuroprosthesis for speech
  decoding and avatar control", *Nature* 620:1037–1046, published 23 Aug 2023, DOI 10.1038/s41586-023-06443-4.
  Median 78 words per minute, median word error rate 25%. (An erratum was published in 2024; not read.)
- **Institution:** UC Berkeley Engineering, "Put into words", Berkeley Engineer, 6 Nov 2023.
  https://engineering.berkeley.edu/news/2023/11/put-into-words
  - Supports: 253-electrode array on the surface of her brain; signals turned into synthesised speech and an avatar's
    facial expressions; voice personalised from a video of her wedding speech; co-lead authors were Berkeley students.
  - Quote: "implantable AI-powered device that, for the first time, translates brain signals into synthesized speech"
- **News backup:** NextShark via Yahoo News, Bryan Ke, 24 Aug 2023.
  https://www.yahoo.com/news/ai-powered-brain-implant-helps-224317854.html Brain implant "powered by artificial
  intelligence"; vocabulary over 1,000 words. A short secondary piece.
- UCSF's own release (ucsf.edu/news/2023/08/425986/…) returned 403 and was not read.
- **System:** UCSF Chang lab neuroprosthesis; deep-learning decoder (Berkeley names CTC loss, a machine-learning
  training technique).
- **Human check:** research setting; Ann trained the decoder over weeks by attempting phrases; outputs evaluated by
  the team. 25% median word error rate means many mistakes.

### Case 5b. Be My AI (Be My Eyes + OpenAI GPT-4)

- **Primary:** Be My Eyes, "Introducing Be My AI (formerly Virtual Volunteer) for People who are Blind or Have Low
  Vision, Powered by OpenAI's GPT-4", 14 Mar 2023. https://www.bemyeyes.com/?p=1012
  - Quote: "the first-ever digital visual assistant powered by OpenAI's new GPT-4 language model"
  - If the AI can't answer, "it will automatically offer users the option to be connected via the app to a sighted
    volunteer".
- **Rename and beta:** Be My Eyes, "Introducing: Be My AI", 7 Aug 2023. https://www.bemyeyes.com/?p=1026 Describes
  photos and answers follow-up questions; users can still reach a human volunteer to check results. (A 25 Sep 2023
  post about rollout to "hundreds of thousands" of users was seen in search results only, not read.)
- **News backup:** The Next Web, Thomas Macaulay, 17 Mar 2023.
  https://thenextweb.com/news/be-my-eyes-app-uses-openai-gpt-4-help-visually-impaired Uses: reading menus,
  identifying ingredients, reading maps; beta testers called it "life-changing"; CEO Mike Buckley: "I know we are in
  the midst of an AI hype cycle right now." No error rates reported.
- **System:** OpenAI GPT-4 (vision), in the Be My Eyes app.
- **Human check:** optional; a human volunteer is one tap away, and Be My Eyes says to use one to check results.

### Case 5c. Project CETI sperm-whale "phonetic alphabet" (checked; weak for this line)

- **Primary:** Project CETI, "Sperm Whale Phonetic Alphabet Proposed for the First Time", 7 May 2024.
  https://www.projectceti.org/blog-posts/sperm-whale-phonetic-alphabet-proposed-for-the-first-time
  - Paper: Sharma P., Gero S., Payne R., Gruber D.F., Rus D., Torralba A., Andreas J., "Contextual and combinatorial
    structure in sperm whale vocalisations", *Nature Communications* 15, 7 May 2024, DOI 10.1038/s41467-024-47221-8.
    Nearly 9,000 codas from the Eastern Caribbean clan; rubato and ornamentation, combined with rhythm and tempo.
  - Quote: "While the communicative function of many codas remains unknown"
- **Backup:** MIT News (Rachel Gordon, MIT CSAIL), "Exploring the mysterious alphabet of sperm whales", 7 May 2024.
  https://news.mit.edu/2024/csail-ceti-explores-sperm-whale-alphabet-0507 "the team used a mix of algorithms for
  pattern recognition and classification"; Daniela Rus: "Our next steps aim to decipher the meaning behind these
  communications."
- The paper itself was not read: nature.com redirected to a login and the PMC copy (PMC11076547) showed a bot check.
  The abstract was read through the Europe PMC API. Which steps were done by ML and which by researchers with new
  visualisations is not clear from what was read.
- **Against the line:** whales are not voiceless, and nothing was translated or given words. The finding is structure,
  not meaning. This belongs to verse 1 only as "found a pattern in whale song", which may suit line 6 better than
  line 5 (rubato, ornamentation, rhythm and tempo are musical terms the authors chose).

### Line against source

- **"give the voiceless words": right, and literal** for 5a. Harrell and Ann Johnson had lost speech; the systems turned
  attempted speech into words, in their own reconstructed voices. Caveats: research devices, one participant each,
  surgery required, and the Harrell sources read don't call it AI. Ann Johnson's case is explicitly AI-powered, with a
  25% median word error rate.
- **"translate the voice":** Be My AI translates images into spoken description, not a voice. If "translate the voice"
  means language translation, no case was researched for it in this pass.
- **"Draft the brief":** not researched. Caution: the best-known news about AI and legal briefs is fabricated citations
  in court filings, the opposite of wonder. Needs its own pass before it gets an image.
- **"voiceless" for Be My AI:** blind and low-vision people are not voiceless. Be My AI gives them a description of
  what they can't see. Use it for "translate", not "voiceless".

### Confidence: high (5a-i facts), medium (5a as "AI"), high (5b), low (5c for this line)

5a-i's facts come from two institutions and the NEJM abstract, but the AI label is unconfirmed. 5a-ii is explicitly AI
per Berkeley, with the paper's abstract read; UCSF's own page was blocked. 5b is the company's own announcements plus
news. 5c is well sourced but doesn't support the line.

---

## Line 6. "Score the pattern no one heard in sixths and thirds"

### Case 6a. Beethoven X: the AI-assisted completion of Beethoven's unfinished Tenth Symphony

- **Primary (sponsor):** Deutsche Telekom, "The exciting path to the completion of Beethoven's 10th Symphony",
  8 Sep 2021.
  https://www.telekom.com/en/newsroom/latest-updates/media-information/2021/9/the-exciting-path-to-the-completion-of-beethoven-s-10th-symphony
  - Supports: Telekom assembled an international team of AI and music experts in spring 2019, led by Matthias Röder;
    AI trained on about 10,000 pieces; experts orchestrated the AI-generated music in October 2020; Beethoven
    Orchestra Bonn recorded it in summer 2021. Symphony "created through the interaction of human and artificial
    intelligence."
  - Also read: Telekom, "Beethoven X: Experiment accomplished", Oct 2021,
    https://www.telekom.com/en/newsroom/latest-updates/news/2021/10/beethoven-x-experiment-accomplished
    World premiere 9 Oct 2021, Telekom Forum, Bonn, about 750 guests.
- **Primary (AI lead, first person):** Ahmed Elgammal (Rutgers Art & AI Lab, Playform AI), "How a team of musicologists
  and computer scientists completed Beethoven's unfinished 10th Symphony", The Conversation, republished by AIhub
  8 Oct 2021.
  https://aihub.org/2021/10/08/how-a-team-of-musicologists-and-computer-scientists-completed-beethovens-unfinished-10th-symphony
  (The Conversation original not read.)
  - Supports: the AI extended Beethoven's sketch motifs into passages, harmonised melodic lines, bridged sections,
    wrote codas and orchestrated; humans (Werzowa, Gotham, Levin, Röder) transcribed the sketches and decided where
    each belonged. "we constructed and orchestrated two entire movements of more than 20 minutes apiece."
- **News backup:** Euronews with AFP, Julie Gaubert, 14 Oct 2021.
  https://www.euronews.com/2021/10/14/after-more-than-two-centuries-beethoven-s-10th-symphony-has-been-completed-by-an-ai
  - Supports: composer Walter Werzowa reviewed hundreds of AI-generated variations each morning and chose which to
    use; critics said the AI was "never lovesick, never drunk."
  - Quote (Werzowa): "The AI interpolated because it learned how Beethoven composed, how Beethoven developed, and it
    gave us methods and variations back."
- **Also read:** The Irish Times, Derek Scally, "And the Beethoven goes on: Bonn premieres 'new' 10th symphony",
  8 Oct 2021. https://www.irishtimes.com/news/world/europe/and-the-beethoven-goes-on-bonn-premieres-new-10th-symphony-1.4695375
  The team evaluated AI output over about 18 months; Robert Levin and Walter Werzowa named.
- **System:** a custom model by Playform AI / Elgammal's team, trained on Beethoven's works. No public model name in
  what was read.
- **Human check:** heavy. Humans placed the sketches, picked among AI variations daily, and experts orchestrated or
  revised. It is a human–AI collaboration, which the sponsor itself says.

### Case 6b. Google's Bach Doodle: Coconet harmonising any melody in four-part Bach chorale style

- **Primary (model):** Magenta (Google), "Coconet: the ML model behind today's Bach Doodle", 20 Mar 2019, by
  Cheng-Zhi Anna Huang, Tim Cooijmans, Monica Dinculescu, Adam Roberts, Curtis Hawthorne.
  https://magenta.tensorflow.org/coconet
  - Supports: trained on 306 Bach chorale harmonisations (four-part counterpoint) by erasing notes and learning to fill
    them in; generates by drafting a full score, erasing parts and rewriting.
  - Quote: "Coconet is trained to restore Bach's music from fragments."
- **Primary (product):** Google, "Honoring J.S. Bach with our first AI-powered Doodle", Lauren Hannah-Murphy,
  21 Mar 2019. https://blog.google/technology/ai/honoring-js-bach-our-first-ai-powered-doodle/
  - Quote: "the Doodle will harmonize your melody in Bach's style."
- **News backup:** TIME, Madeline Roache, 21 Mar 2019. https://time.com/5555837/google-doodle-bach-ai/
  Users write a melody, press "harmonize", and the model adds three voices.
- **System:** Coconet (Google Magenta), run in the browser with TensorFlow.js.
- **Human check:** none needed in the product sense; it's an interactive toy. Users judged their own results.

### Case 6c. Claude (Anthropic): an informal listener poll, October 2026 (weak; noted, not recommended)

- **Only source read:** kod.ru (Russian tech news), 13 Oct 2026. https://kod.ru/claude-opus-koncert-vivaldi
  - Reports: musician "Auggie" had Claude Opus 5.5 write the first movement of an oboe concerto in C minor in Vivaldi
    style (LilyPond), then ran an open online poll against Handel and Vivaldi with the same synthesised playback.
    Judged human-made: Claude 60%, Handel 58%, Vivaldi 43%. The musician added that language models can't yet handle
    classical-era style and that the textures lack contrast.
  - Original post on X (https://x.com/aug5thmusic/status/2109682320001401230) returned 402 and was not read; the
    Substack post was not found.
- **Against the line:** this is pastiche passing a blind poll, not a pattern no one heard. Single secondary source,
  self-selected poll, sample size unknown. Noted because the brief asked; don't build an image on it.

### Line against source

- **"Score": right** for 6a (an orchestral score was made and performed) and broadly for 6b (four-part harmonisation).
- **"in sixths and thirds": fits 6b best.** Four-part chorale harmony is built largely on thirds and sixths. But no
  source read says "sixths and thirds"; that's the line's poetry, not a sourced fact. Fine as a musical image, not as a
  claim.
- **"the pattern no one heard": overstates for both.** Beethoven X extrapolated from Beethoven's own sketches and
  style; Coconet imitates Bach's harmonic practice. Both reproduce a pattern people already knew and loved. The closest
  sourced case of AI finding structure humans hadn't described is the sperm-whale codas (5c): researchers using new
  analysis and ML found "rubato" and "ornamentation" in whale codas, a pattern not described before. If "the pattern
  no one heard" must be literal, CETI fits this line better than line 5, with the caveat that meaning is unknown and
  how much of the finding was ML versus researchers isn't clear from what was read.
- Beethoven X was also criticised by music critics as not Beethoven; the sources read report scepticism (Euronews) but
  no detailed review was read.

### Confidence: medium (6a), high (6b), low (6c)

6a: real, dated and widely covered, but the AI's share is described differently by sponsor, AI lead and press; the
honest description is "AI-assisted, human-selected". 6b: Google's own model and product pages plus TIME agree
exactly. Neither supports "no one heard" literally. 6c: one secondary source.

---

## A. Line 3 alternative (non-biological). "Screen a million molecules before the morning round"

Added at Lati's request via Kiln, 7 Nov 2026.

### Case A1. GNoME (Google DeepMind): 2.2 million predicted crystals

- **Primary (company):** Google DeepMind, "Millions of new materials discovered with deep learning", Amil Merchant and
  Ekin Dogus Cubuk, 29 Nov 2023.
  https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/
  - Supports: 2.2 million new crystals predicted; 380,000 of them the most stable, released to the Materials Project;
    known stable materials raised to 421,000 (from about 48,000 found computationally before, about 20,000 by
    experiment); 736 already made independently by outside labs.
  - Quote: "External researchers in labs around the world have independently created 736 of these new structures
    experimentally."
- **Paper (abstract via Europe PMC record):** Merchant A. … Cubuk E.D., "Scaling deep learning for materials
  discovery", *Nature* 624:80–85, published 29 Nov 2023, DOI 10.1038/s41586-023-06735-9.
  Quote: "discovery of 2.2 million structures below the current convex hull"
- **Lab side (institution):** Lawrence Berkeley National Laboratory via EurekAlert, "Google DeepMind adds nearly 400,000
  new compounds to Berkeley Lab's Materials Project", 29 Nov 2023. https://www.eurekalert.org/news-releases/1009276
  - Quote: "Over 17 days of independent operation, A-Lab successfully produced 41 new compounds out of an attempted 58"
  - GNoME computations were used alongside Materials Project data to test the A-Lab. The A-Lab's own AI took
    synthesis recipes from papers and adjusted them by active learning.
- **News backup:** Freethink, Kevin Dickinson, 22 Dec 2023.
  https://www.freethink.com/robots-ai/google-ai-discovers-2-2-million-new-materials Repeats the numbers; notes two of
  the 41 A-Lab successes needed human intervention and that some scientists called for the A-Lab paper's retraction.
- **Dispute (news):** The Register, Katyanna Quach, 31 Jan 2024 (updated 1 Feb 2024).
  https://www.theregister.com/2024/01/31/ai_chemistry_research_disputed/
  - Seven researchers at Princeton and UCL (Leslie Schoop, Robert Palgrave and others; ChemRxiv preprint, not peer
    reviewed) argued the A-Lab made no truly novel materials: diffraction patterns misread, compositional disorder
    ignored. They said this does not necessarily undermine GNoME itself. Ceder (A-Lab): the critique "is not peer
    reviewed" and has "multiple errors". DeepMind later clarified GNoME predicted the stability of the A-Lab targets;
    the Berkeley team proposed them.
  - The outcome of this dispute after Feb 2024 was not checked.
- **System:** GNoME (Graph Networks for Materials Exploration), a graph neural network, with candidates checked by
  density functional theory (DFT) calculations.
- **Human check:** stability is predicted by computation (GNoME plus DFT), not confirmed in a lab, except the 736
  outside syntheses and the disputed A-Lab runs.

### Line against source

- **"a million": right in scale**, conservative even: 2.2 million candidates predicted, 380,000 predicted most stable.
  But the GNoME pipeline evaluated far more candidates than it kept; the exact number screened was not in what was read.
- **"molecules": wrong word.** GNoME found inorganic crystal structures (solids), not molecules. If the line must be
  exact, "crystals" or "structures" is the sourced word. "Molecules" invites a drug-discovery reading this case doesn't
  support.
- **"before the morning round": overstates the speed** as a literal claim. Nothing read says overnight. DeepMind's own
  framing is "about 800 years' worth of knowledge" (via Freethink). The A-Lab ran 17 days. As an image of speed it's
  fair; as a timed claim it isn't sourced.
- **"Screen": right.** It predicted and filtered; it didn't make them. Almost all 2.2 million remain unmade. A picture of
  the machine making materials should be the A-Lab, and then the dispute matters.

### Confidence: high (GNoME numbers), medium-low (A-Lab synthesis as "new materials")

GNoME's figures come from DeepMind, the Nature abstract and Berkeley Lab and agree. The A-Lab's novelty claim is
publicly disputed by named chemists; the status of that dispute wasn't checked.

---

## B. Extra wonder cases for the picture

### B1. Google flood forecasting (Flood Hub)

- **Primary:** Google, Yossi Matias, "How we're helping partners with improved and expanded AI-based flood
  forecasting", 11 Nov 2024. https://blog.google/innovation-and-ai/products/expanding-flood-forecasting-coverage-helping-partners/
  - Supports: model coverage from 80 to more than 100 countries; flood information to 700 million people, up from
    460 million (across Search, Maps and Flood Hub); an expert layer of about 250,000 "virtual gauge" forecast points
    in 150 countries. Quote: "has the same accuracy at a seven-day lead time as the previous model had at five days."
- **Latest Google figure:** Google, Yossi Matias, "Towards a world where no one is surprised by a natural disaster",
  23 Jun 2026. https://blog.google/innovation-and-ai/technology/research/helping-communities-prepare-for-natural-disasters/
  Quote: "forecasts on Flood Hub cover 2 billion people across more than 150 countries." Scoped to areas at risk of
  significant floods; river forecasts up to seven days ahead.
- **Paper (abstract via Europe PMC):** Nearing G. … Matias Y., "Global prediction of extreme floods in ungauged
  watersheds", *Nature* 627:559–563, 20 Mar 2024, DOI 10.1038/s41586-024-07145-1. AI forecasts reliable to five days
  in ungauged basins, similar to or better than GloFAS nowcasts.
- **Earlier step (search result only, not read):** May 2023 expansion to 80 countries, 460 million people.
- **What it supports:** AI forecasting river floods days ahead for places without river gauges. Coverage numbers are
  Google's own; no independent check of "people covered" or of how many acted on a warning was read.
- **Confidence:** high that Google states these figures; medium for what "cover" means in lives.

### B2. AI wildfire detection from cameras: ALERTCalifornia (UC San Diego) with CAL FIRE

- **Primary (institution):** UC San Diego, Caitlin Scully, "High Alert", 24 Oct 2023 (UC San Diego Magazine, Fall 2023).
  https://today.ucsd.edu/story/alert-california
  - Supports: more than 1,050 cameras; AI tested summer 2023, rolled out to all 21 CAL FIRE units in September 2023.
  - Quote: "When the AI spots an anomaly from the camera feeds, the system alerts watchstanders for confirmation."
- **Dated detection (news):** Bay Area News Group (Paul Rogers), republished by Fire Apparatus Magazine, 19 Sep 2025.
  https://www.fireapparatusmagazine.com/?p=196896
  - 6 July (2025, per the article's date): an AI camera flagged a fire near Auburn at 2:33 a.m.; nobody had called
    911; Cal Fire's Grass Valley command center verified it and crews put it out within a 30 × 30 ft area.
  - Prior year in Cal Fire's jurisdiction: 7,553 wildfires; cameras picked up 1,668; 636 (38%) before any 911 call.
  - Quote (Brian York, Cal Fire): "It was a perfect example of a fire that doesn't gain attention because it was
    detected early."
- **Earlier report (news):** Reuters via Gulf News, 11 Aug 2023.
  https://gulfnews.com/world/americas/california-turns-to-ai-to-help-spot-wildfires-1.1691753082670
  A 3 a.m. fire in Cleveland National Forest, about 50 miles east of San Diego, spotted by camera AI in the
  programme's first month; out within 45 minutes. The exact date of that fire is not given. Project lead Neal Driscoll
  said the sample was too small for firm conclusions.
- **Human check:** always. AI alerts go to human watchstanders / dispatch, who verify before anything is sent; Cal Fire
  staff label each alert right or wrong to retrain it.
- **Confidence:** high for the programme; medium for the Auburn detail (one regional news group, not CAL FIRE's own
  record). Pano AI was not researched.

### B3. AI-assisted demining in Ukraine

- **Reputable report:** IEEE Spectrum, Jasper Baur, "Ukraine Is Riddled With Land Mines. Drones and AI Can Help",
  25 Apr 2024 (May 2024 print). https://spectrum.ieee.org/ukraine-drones
  - Supports: SpotlightAI (Safe Pro AI) runs a machine-learning model on ordinary drone imagery and returns a map of
    detected ordnance; June 2023 U.N. demonstration field north of Kyiv: 74 mines and other items detected; in use by
    humanitarian groups (Norwegian People's Aid, HALO Trust) in Ukraine.
  - Quote: "We don't anticipate that the technology will replace human labor"
  - Conflict of interest: the author works on the system (Safe Pro AI / Demining Research Community). This is a
    first-person account in a reputable outlet, not independent reporting.
- **Field study (news):** Euromaidan Press, Maxim Volovich, 4 Nov 2025. https://euromaidanpress.com/?p=372148
  18-month study by Norwegian People's Aid with SpotlightAI, presented at the 2025 GICHD Innovation Conference in Geneva:
  more than 800% productivity in non-technical survey, about 50% lower labour cost per hectare. NPA called the
  findings preliminary. The underlying source linked is Safe Pro's own Business Wire release (not read); the NPA study
  itself was not found.
- **Context (news):** AFP Relaxnews via The Star, 13 Jul 2024.
  https://www.thestar.com.my/tech/tech-news/2024/07/13/how-ai-is-assisting-demining-operations-in-ukraine
  Quote: "At this stage, AI can only suggest priority areas for demining."
- **What it supports:** AI finding mines in drone photos so people know where to look and where not to walk. It does
  not clear mines. Deminers still sweep with detectors and destroy ordnance.
- **Confidence:** medium. Real and dated, but the numbers come from the vendor or vendor-linked sources; no UNDP or NPA
  primary publication was read.

---

## Summary table

| Line | Case | Primary URL | Date | System | Confidence |
|---|---|---|---|---|---|
| 4 | Mia as extra reader, Hungary, peer-reviewed | https://pmc.ncbi.nlm.nih.gov/articles/PMC10719086/ (Nature Medicine, DOI 10.1038/s41591-023-02625-9) | 16 Nov 2023 | Mia, Kheiron Medical | high |
| 4 | Mia in NHS Grampian (GEMINI), 12% more cancers | https://www.abdn.ac.uk/news/22964/ | 21 Mar 2024 | Mia, Kheiron Medical | medium |
| 5 | Casey Harrell, ALS speech BCI | https://www.ucdavis.edu/news/brain-computer-interface-allows-man-als-speak | 14 Aug 2024 | BrainGate2 BCI, UC Davis decoder (AI label unconfirmed) | high (facts), medium (as AI) |
| 5 | Ann Johnson, stroke, speech + avatar | https://engineering.berkeley.edu/news/2023/11/put-into-words (Nature, DOI 10.1038/s41586-023-06443-4, 23 Aug 2023) | 23 Aug 2023 | UCSF Chang lab neuroprosthesis, AI decoder | high |
| 5 | Be My AI for blind and low-vision people | https://www.bemyeyes.com/?p=1012 | 14 Mar 2023 | OpenAI GPT-4 in Be My Eyes | high (fits "translate", not "voiceless") |
| 5 | Project CETI whale codas | https://www.projectceti.org/blog-posts/sperm-whale-phonetic-alphabet-proposed-for-the-first-time | 7 May 2024 | MIT CSAIL / CETI ML team (methods unclear) | low for line 5 |
| 6 | Beethoven X, Tenth Symphony completion | https://www.telekom.com/en/newsroom/latest-updates/media-information/2021/9/the-exciting-path-to-the-completion-of-beethoven-s-10th-symphony | 8 Sep 2021 (premiere 9 Oct 2021) | Playform AI / Elgammal team model | medium |
| 6 | Bach Doodle harmoniser | https://magenta.tensorflow.org/coconet | 20 Mar 2019 | Coconet, Google Magenta | high (as fact; "no one heard" overstated) |
| 6 | Claude oboe concerto poll | https://kod.ru/claude-opus-koncert-vivaldi (secondary) | 13 Oct 2026 | Claude Opus 5.5 | low |
| 3 (alt) | GNoME, 2.2 million predicted crystals | https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/ (Nature, DOI 10.1038/s41586-023-06735-9) | 29 Nov 2023 | GNoME, Google DeepMind | high (numbers); "molecules" is wrong word |
| 3 (alt) | A-Lab synthesis of 41 of 58 targets | https://www.eurekalert.org/news-releases/1009276 | 29 Nov 2023 | A-Lab, Berkeley Lab | medium-low (novelty disputed) |
| extra | Flood Hub, 700M people / 100+ countries; 2B / 150+ (2026) | https://blog.google/innovation-and-ai/products/expanding-flood-forecasting-coverage-helping-partners/ | 11 Nov 2024 (2026 figure: 23 Jun 2026) | Google flood forecasting model | high (as Google's claim) |
| extra | ALERTCalifornia AI fire cameras; Auburn detection | https://today.ucsd.edu/story/alert-california | 24 Oct 2023 (Auburn: 6 Jul 2025, news 19 Sep 2025) | UCSD / CAL FIRE / DigitalPath AI | high (programme), medium (Auburn) |
| extra | SpotlightAI drone mine detection, Ukraine | https://spectrum.ieee.org/ukraine-drones | 25 Apr 2024 | SpotlightAI, Safe Pro AI | medium |

## Not read or not found

- **BBC** coverage of the NHS Grampian Mia trial (Barbara, 6 mm, 11 women): bbc.co.uk and bbc.com are blocked to the
  fetch tool. Figures cited only via Business Insider.
- **The Scotsman**, "Scottish woman 'incredibly lucky' AI caught tumour…": 403.
- **nature.com** pages for the Nature Medicine Mia paper and the Nature Communications CETI paper: redirected to a login.
  Mia paper read on PMC; CETI paper's PMC copy (PMC11076547) showed a bot check; only its abstract read via Europe PMC.
- **NEJM** (Card et al. 2024): 403. Abstract read via Europe PMC. Methods (whether the decoder uses neural networks or a
  language model) not read.
- **UCSF** news release on Ann Johnson: 403.
- **Nature** erratum to Metzger et al. 2023 (Nature 631, E13, 2024): exists per Europe PMC; content not read.
- **Be My Eyes** 25 Sep 2023 rollout post: seen in search results only.
- **The Conversation** original of Elgammal's article: not read; the AIhub republication was.
- **X post** by aug5thmusic (Claude poll): 402. Substack post not found.
- **Not found:** an NHS trust's or Kheiron's own release on the GEMINI results (kheironmed.com press listing appeared in
  search but was not opened); a peer-reviewed paper for the 12% GEMINI figure.
- **GNoME / A-Lab:** the Nature papers' full texts (abstract only for GNoME; A-Lab paper not opened); the ChemRxiv
  critique itself; any later resolution of the A-Lab dispute; the total number of candidates GNoME screened.
- **Flood Hub:** the May 2023 80-country announcement (search result only); any independent evaluation of coverage
  or of warnings acted on.
- **Wildfire:** CAL FIRE's own record of the Auburn fire; Pano AI (not researched); the exact date of the Cleveland
  National Forest detection (not given in the Reuters piece).
- **Demining:** a UNDP or Norwegian People's Aid primary publication; Safe Pro's Business Wire release (vendor, not
  opened).
- **Not researched:** "Draft the brief" and "translate the voice" (as language translation) in line 5; any Anthropic
  first-party music project (none turned up in one search).
