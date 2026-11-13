# Verse 1 (wonder): sources, pass 1

Research subagent for the "I'm Not You" source pass, 7 Nov 2026. One section per line, then a summary table.

**How these were read.** Every source marked "read" was opened with WebFetch on 7 Nov 2026. WebFetch passes the page
through a small summarising model, so the quotes below are what that tool returned as verbatim. They should be
spot-checked against the page before they go on screen. For paywalled journals (Nature, Science, Cell, Lancet, NEJM)
the abstract was read through the Europe PMC REST API (`ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:...`),
which returns the publisher's abstract and metadata. Europe PMC's "first publication date" is sometimes the issue date,
not the online date; where they differ that is noted. nobelprize.org, nature.com, science.org, bbc.co.uk/bbc.com and
pmc.ncbi.nlm.nih.gov all refused the fetch (403, login redirect, or a bot check that was not bypassed).

---

## Line 1: "Fold the protein, find the shape nobody saw"

### Case 1a: AlphaFold2 and the 2024 Nobel Prize in Chemistry

- **Primary (prize):** Royal Swedish Academy of Sciences press release, "The Nobel Prize in Chemistry 2024",
  https://www.kva.se/en/news/the-nobel-prize-in-chemistry-2024/, dated 2024-10-09. Read.
  - Supports: half the prize to David Baker "for computational protein design"; the other half jointly to Demis Hassabis
    and John Jumper "for protein structure prediction".
  - Quote: "In 2020, Demis Hassabis and John Jumper presented an AI model called AlphaFold2."
  - Also on the page: AlphaFold2 can "predict the structure of virtually all the 200 million proteins that researchers
    have identified", and "has been used by more than two million people from 190 countries."
  - nobelprize.org itself returned 403 and was not read. KVA is the awarding body, so its release is a primary source.
- **Primary (paper):** Jumper, Evans, Pritzel et al., "Highly accurate protein structure prediction with AlphaFold",
  *Nature* 596:583-589, published 2021-07-15 (received 2021-05-11). Read on PubMed Central:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/ (nature.com redirected to login). DOI 10.1038/s41586-021-03819-2.
  - Supports: only a small fraction of known proteins had an experimentally solved shape.
  - Quote: "the structures of around 100,000 unique proteins have been determined", and that this "represents a small
    fraction of the billions of known protein sequences."
  - On CASP14: "demonstrating accuracy competitive with experimental structures in a majority of cases".
- **Primary (database):** Google DeepMind, "AlphaFold reveals the structure of the protein universe",
  https://deepmind.google/discover/blog/alphafold-reveals-the-structure-of-the-protein-universe/, dated 2022-07-28. Read.
  - Supports: the AlphaFold Protein Structure Database, with EMBL-EBI, expanded "from nearly 1 million structures to
    over 200 million structures", covering "nearly all catalogued proteins known to science."
  - The page calls them "predicted structures" and gives no accuracy caveat in its own text.
- **System:** AlphaFold2 (Google DeepMind).
- **Did a person check it?** Yes, in two ways. CASP14 is a blind assessment: predictions are scored against experimental
  structures that were unpublished at the time. And the Nobel committee judged it. The DeepMind 2022 post also gives an
  example of researchers using experimental methods alongside AlphaFold "to complete and interpret any areas that were
  unclear", meaning people still checked the predictions experimentally.
- **Against the line:** "Fold the protein" is right in spirit, though strictly AlphaFold *predicts* the folded structure;
  it doesn't fold anything. "Find the shape nobody saw" is supported: for most of the 200 million proteins nobody had
  an experimental structure. But the shapes are predictions, not observations, and accuracy varies (the paper says
  "competitive with experimental structures in a majority of cases", not all). The honest image is a predicted shape
  that people then check, not a revelation.
- **Confidence: high.** Awarding body's release, the peer-reviewed paper and the company's own database announcement
  all read and consistent.

### Case 1b (optional): David Baker's designed proteins

Same KVA release: Baker "succeeded with the almost impossible feat of building entirely new kinds of proteins." This is
"a shape nobody saw" in the strongest sense (proteins that never existed), but it is computational design (Rosetta,
later deep-learning tools), and the release text read here does not name a specific AI system for it. Not researched
further. **Confidence: medium** as an alternative for the line; it would need the Baker lab's own papers.

---

## Line 2: "Map the genome, patch the flaw, rewrite the law"

No single case does all three verbs. Two cases cover it between them: one reads the genome for flaws, one designs a tool
that rewrites it.

### Case 2a: AlphaMissense (reading the genome for flaws)

- **Primary (paper):** Cheng, Novati, Pan ... Hassabis, Kohli, Avsec, "Accurate proteome-wide missense variant effect
  prediction with AlphaMissense", *Science*, DOI 10.1126/science.adg7492. Europe PMC lists first publication
  2023-09-22. science.org returned 403; abstract read through Europe PMC.
  - Quote: "We present AlphaMissense, an adaptation of AlphaFold fine-tuned on human and primate variant population
    frequency databases."
  - The abstract says it classifies 89% of missense variants as likely benign or likely pathogenic.
- **Primary (company):** Google DeepMind, "AlphaMissense: catalogue of genetic mutations to help pinpoint the cause of
  diseases",
  https://deepmind.google/blog/alphamissense-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/,
  dated 2023-09-19. Read.
  - Quote: "we show it categorised 89% of all 71 million possible missense variants"; of those, "only 0.1% have been
    confirmed by human experts."
  - Its own caveat: "our predictions are not designed to be used in the clinic directly" and "should be interpreted with
    other sources of evidence."
- **System:** AlphaMissense (Google DeepMind), built on AlphaFold.
- **Did a person check it?** The model was benchmarked against expert-annotated variants (ClinVar etc. per the abstract's
  "benchmarks"), but the point of the catalogue is that 99.9% of the variants have no expert verdict. DeepMind itself
  says a clinician must weigh it with other evidence. A search snippet (not read in full) reports Heidi Rehm (Broad
  Institute) saying the engineers overstated the certainty of the predictions; that is not cited as checked.
- **Against the line:** "Map the genome" overstates: AlphaMissense scores one class of variant (single amino-acid
  changes, 71 million possible ones) in protein-coding genes, not the genome. It flags a likely flaw; it doesn't patch
  anything.
- **Confidence: high** for the facts; **medium** as a fit for the line.

### Case 2b: OpenCRISPR-1, an AI-designed gene editor (rewriting)

- **Primary (paper):** Ruffolo, Nayfach, Gallagher ... Cameron, Madani, "Design of highly functional genome editors by
  modelling CRISPR-Cas sequences", *Nature* 645:518-525, DOI 10.1038/s41586-025-09298-z. Europe PMC lists first
  publication 2025-07-30. nature.com redirected to login; abstract read through Europe PMC.
  - Quote: the AI-generated editor, "denoted as OpenCRISPR-1, exhibits compatibility with base editing."
  - The generated editors show comparable or improved activity and specificity "relative to SpCas9, the prototypical
    gene editing effector", "while being 400 mutations away in sequence."
  - Tested "when ported into non-native environments, such as human cells".
- **Company announcement:** Profluent / Business Wire, 2025-07-30
  (https://www.businesswire.com/news/home/20250730820469/en). Seen only in search results, **not read**.
- **System:** Profluent's protein language models trained on its CRISPR-Cas Atlas; the editor is OpenCRISPR-1. The exact
  model name was not confirmed in what was read.
- **Did a person check it?** Yes: the designed editors were made and tested in the lab, in human cells, against SpCas9.
- **Against the line:** "Rewrite" is right in kind: an AI designed a working genome editor not found in nature. "Patch
  the flaw" overstates: nothing read says OpenCRISPR-1 has treated a patient or corrected a disease mutation in a person.
  It is a lab-validated research tool.
- **Confidence: high** for the facts (peer-reviewed abstract); **medium** as a fit.

### "Rewrite the law"

Nothing read supports a literal law being rewritten. Read as "the rule of the code" it works as a figure for gene
editing. If it means a legal law, there is no verse-1 source for it; flag for the writer.

---

## Line 3: "Screen a million molecules before the morning round"

The earlier table's date was wrong. Halicin is 2020 (Cell). The 2023 MIT/McMaster paper is abaucin. A third, stronger case
on the "million" is the December 2023 MRSA paper.

### Case 3a: Halicin (MIT, 2020)

- **Primary (paper):** Stokes, Yang, Swanson ... Barzilay, Collins, "A Deep Learning Approach to Antibiotic Discovery",
  *Cell*, DOI 10.1016/j.cell.2020.01.021. Europe PMC lists 2020-02-01 (issue); MIT News dates the release 2020-02-20.
  Abstract read through Europe PMC.
  - Quote on the large screen: "from a discrete set of 23 empirically tested predictions from >107 million molecules
    curated from the ZINC15 database", which "identified eight antibacterial compounds that are structurally distant
    from known antibiotics."
  - Halicin "also effectively treated Clostridioides difficile and pan-resistant Acinetobacter baumannii" in mice.
- **Institution:** MIT News, "Artificial intelligence yields new antibiotic",
  https://news.mit.edu/2020/artificial-intelligence-identifies-new-antibiotic-0220, 2020-02-20. Read.
  - Halicin came from the Drug Repurposing Hub, "a library of about 6,000 compounds", not from the 100-million screen.
  - The ZINC15 screen of "more than 100 million molecules" "took only three days" and yielded 23 candidates.
  - Halicin "has been previously investigated as possible diabetes drug." Named after HAL from *2001*.
- **System:** a deep neural network (a graph neural network; the paper says "deep learning"). No product name.
- **Did a person check it?** Yes. The researchers tested candidates against bacterial strains from patients and in mice.
  MIT News names no independent lab.
- **Against the line:** "a million" understates the big screen (>107 million) but halicin itself came from about 6,000.
  "Before the morning round" overstates the speed: the 107-million screen took three days. There was no hospital round;
  this is lab work, and halicin is not an approved drug.

### Case 3b: Abaucin (McMaster and MIT, 2023)

- **Primary (paper):** Liu, Catacutan, Rathod ... Collins, Stokes, "Deep learning-guided discovery of an antibiotic
  targeting Acinetobacter baumannii", *Nature Chemical Biology*, DOI 10.1038/s41589-023-01349-8, first published
  2023-05-25 (Europe PMC). Abstract read.
  - Quote: "Here we screened ~7,500 molecules for those that inhibited the growth of A. baumannii in vitro."
  - "abaucin could control an A. baumannii infection in a mouse wound model."
  - The abstract does not say how many molecules the model then predicted on. Thousands, not millions.
- **Confidence for the line: low** on "a million"; it's included only to correct the earlier table.

### Case 3c (best fit for "a million"): a new structural class of antibiotics (MIT/Broad, 2023)

- **Primary (paper):** Wong, Zheng, Valeri ... Stokes, Renner, Collins, "Discovery of a structural class of antibiotics
  with explainable deep learning", *Nature* 626:177-185, DOI 10.1038/s41586-023-06887-8, first published 2023-12-20.
  Abstract read through Europe PMC.
  - Quote: the team "applied ensembles of graph neural networks to predict antibiotic activity and cytotoxicity for
    12,076,365 compounds."
  - Trained on lab results for 39,312 compounds; 283 tested; one class "selective against methicillin-resistant S.
    aureus (MRSA)"; "reduces bacterial titres in mouse models of MRSA skin and systemic thigh infection."
- **Institution:** Broad Institute, "With AI, researchers identify a new class of antibiotic candidates",
  https://www.broadinstitute.org/news/researchers-use-ai-identify-new-class-antibiotic-candidates, 2023-12-20. Read.
  "the researchers screened about 12 million compounds"; "purchased about 280 compounds and t