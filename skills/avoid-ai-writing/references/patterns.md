# Pattern catalog

Apply the editing contract in `../SKILL.md` first. Entries are candidate matches, not automatic edits: check context, pass conditions, protected status, and surrounding meaning before calling something a finding, and edit only if the mode and scope allow it. Replacement wording never supplies new facts. Decision rule for each finding: **edit**, **keep**, or **flag a gap**. A gap means the fix would need a fact, name, number, mechanism, or experience the source lacks; report it, do not invent it, and still deliver any bounded edit.

## Formatting

- **Em dashes (— and --):** replace with commas, periods, parentheses, or two sentences. Target zero, hard max 1 per 1,000 words, headings included. Carve-out: a dash separating a bolded or linked lead term from its description in a list item (`- **Term** — text`) is typography, not a splice.
- **Bold overuse:** at most one bolded phrase per major section, or none. Lead with the important thing instead.
- **Emoji in headers:** remove. Social posts may use one or two at line end, never mid-sentence.
- **Excessive bullets:** flag bullet-heavy sections that are not list-shaped; convert to prose only if restructuring is in scope. Comparisons, steps, and API parameters stay lists.
- **Curly quotes and apostrophes:** judge by destination style, not authorship (Word, Google Docs, macOS, and iOS curl them by default). Do not flag curly apostrophes alone. Preserve finished-publication and locale-correct marks (French « », German „ “).
- **Immaculate typography in casual text:** a style choice, not authorship evidence. Keep the source's contractions, odd capitalization, and rough edges; do not add mistakes.

## Sentence structure

- **"It's not X, it's Y" / "This isn't about X, it's about Y"** (also the split form "The headline isn't the speed. The real story is Y." and stacked negations "It's not the price. It's not the features. It's the trust."): rewrite as a direct positive. Max one per piece, only if it serves the argument. Keep a literal correction or a contrast that carries the argument ("It is not a timeout, it is a refused connection"). When simplifying, keep both propositions, including a stated value judgment. If the positive claim is missing, flag the empty contrast.
- **Hollow intensifiers:** genuine/genuinely, real, truly, quite frankly, to be honest, let's be clear, it's worth noting that, and emphasis-only "actually". Default fix is deletion. Keep "actually" when it marks an expectation gap named nearby ("we expected a cache hit; it was actually a miss").
- **Vague endorsement ("worth [verb]ing"):** worth reading, worth a look, worth your time, and similar, when they replace a reason. Give a reason only if the source has one.
- **Hedging:** cut padding like "it's important to note that" and redundant stacks like "could potentially". Keep a modal or qualifier that carries uncertainty, a condition, or a technical limit.
- **Missing bridge sentences:** if paragraphs could be reordered unnoticed, report the missing through-line; add connective tissue only if the relationship exists in the source and structure is in scope.
- **Compulsive rule of three:** keep a triad if the source has three real items or the repetition is deliberate; never add or drop an item for rhythm.

## Words and phrases

Match inflected forms (genuine/genuinely, leverage/leveraging, delve/delving) unless a form has a distinct honest sense (e.g. "real" meaning factual).

- **Tier 1: review every match.** Two bands, reported separately in detect mode:
  - **1A, AI frequency markers.** Evidence about how a passage was produced when clustered. The claim that these appear far more often in model text is inherited, not measured here: treat it as a well-supported convention, not a verified statistic.
  - **1B, clarity edits.** Wordiness and inflated formality. A fix is good writing regardless of authorship, and a 1B hit is **not** evidence of machine authorship (ordinary formal human writing uses these). Never present a wordiness fix as authorship evidence.
- **Tier 2: flag when 2+ appear in the same paragraph.** A single occurrence is not a finding.
- **Tier 3 words: flag by density.** One word (each listed form counted separately) at least `max(3, floor(wordCount x 0.03))` times. Several different Tier 3 words that together pass 3% do not trigger.
- **Tier 3 phrases:** flag the same phrase used twice, or three or more distinct phrases from the list in one piece.

**Tier 1A (replace with plain words, or cut):** delve (explore, look at); landscape (metaphor; field, space, industry); tapestry; realm (area, field); paradigm (model, approach); embark (start); beacon (metaphor); testament to (shows, proves); robust (strong, reliable); comprehensive (thorough, full); cutting-edge (latest, advanced); leverage (verb; use); pivotal (important, key); underscores (highlights, shows); meticulous(ly) (careful, precise); seamless(ly) (smooth, without friction); game-changer / game-changing (say what changed); hit(s) different; watershed moment; marking a pivotal moment (state what happened); "the future looks bright" and "only time will tell" (cut); nestled (is located, sits); vibrant (lively, or describe); thriving (growing, or cite a number); "despite challenges... continues to thrive" (name the challenge and response, or cut); showcasing (showing, or cut the clause); deep dive / dive into (look at); unpack (explain, break down); bustling; intricate / intricacies (complex, or name the complexity); complexities; ever-evolving; enduring; daunting (hard); holistic(ally); actionable (practical); impactful (effective, or describe the impact); learnings (lessons, findings); thought leader / leadership; best practices (what works, proven methods); "at its core" (cut); synergy; interplay (relationship); keen (as intensifier); genuinely/genuine (as intensifier; cut); symphony (metaphor); embrace (metaphor; adopt, use); load-bearing (metaphor). For **load-bearing**, only the hyphenated form counts, and only directly modifying an abstract noun (assumption, claim, invariant, premise, constraint, dependency, argument, abstraction); literal building uses and predicative uses ("that claim is load-bearing") pass.

**Tier 1B:** utilize (use); in order to (to); due to the fact that (because); serves as (is); features (verb; has, includes); boasts (has); presents (inflated; is, shows); commence (start); ascertain (find out); endeavor (effort, try).

**Tier 2:** harness (use); navigate/navigating (work through, handle); foster (encourage, support); elevate (improve); unleash (release, enable); streamline (simplify); empower (enable, let); bolster (support); spearhead (lead); resonate with (connect with); revolutionize (change, or describe what changed); facilitate (enable, help); underpin(ning/nings) (support, basis); nuanced (specific, subtle, or name the nuance); crucial (important, key); multifaceted; ecosystem (metaphor; system, community, market); myriad (many, or a number); plethora; encompass (include, cover); catalyze (start, trigger); reimagine (rethink, redesign); galvanize (motivate, rally); augment (add to); cultivate (build, develop); illuminate (clarify, explain); elucidate (explain); juxtapose (compare, contrast); paradigm-shifting; transformative / transformation (describe what changed); cornerstone (foundation, key part); paramount (most important); poised (to) (ready, about to); burgeoning (growing, or cite a number); nascent (new, early-stage); quintessential (typical, classic); overarching (main, central); quietly (cut, or name the contrast); deeply, only in significance collocations like "deeply integrated / committed / rooted" (literal "deeply nested", "cares deeply" never count).

**Tier 3 words:** significant(ly), innovative / innovation, effective(ly), dynamic / dynamics, scalable / scalability, compelling, unprecedented, exceptional(ly), remarkable / remarkably, sophisticated, instrumental, world-class / state-of-the-art / best-in-class, verbatim. Fix by replacing some with specifics (numbers, comparisons, how, why, what role). "Verbatim" is usually redundant ("copies X verbatim" = "copies X"); weigh density in legal, research, and QA registers where it is a term of art.

**Tier 3 phrases:** emerging sector / space / category; the integration of (X with Y); the intersection of (X and Y); community-driven; long-term sustainability; user engagement; decentralized compute; (sustainable) reward emissions; tokenized incentive structures; "designed for long-term [X]" (cut "designed for", state the property). Name the actual thing instead of the label.

**Technical-vocabulary check:** read the listed sense and context before replacing. "The robust estimator tolerates outliers" stays. In technical-blog and docs context these have legitimate meaning and are not flagged: robust, comprehensive, seamless, ecosystem, leverage (actual platform leverage or APIs), facilitate, underpin, streamline, and the noun "harness" ("test harness"). Still flag ornamental uses and the listed senses of delve, tapestry, beacon, embark, testament to, and game-changer. Never substitute a mechanism or performance property the source does not state.

**Domain-term collision (judgment only, P2):** in cryptography writing, flag generic "proof" or "proof point" only when a reader could mistake supporting evidence for a cryptographic proof. Preserve literal proofs, "proof of purchase", and clear strategy uses.

## Template and transition phrases

- **Template phrases:** slot-fill shapes like "a [adjective] step towards [adjective] AI infrastructure" or "a [adjective] step forward for [noun]" (a vague-praise adjective such as major, crucial, significant before "step"; neutral uses like "a first step towards the full API" pass); "Whether you're [X] or [Y]" (false breadth; pick the real audience); "I recently had the pleasure of [verb]-ing" (say what happened).
- **Transitions:** Moreover / Furthermore / Additionally (restructure, or "and", "also"); "In today's [X]" / "In an era where" (cut or give the real context); "It's worth noting that" / "Notably" (state the fact); "Here's what's interesting / what stood out" (reader-steering; lead with the reason only if the source gives one); In conclusion / In summary (the conclusion should be obvious); "When it comes to" (talk about the thing); "At the end of the day" (cut); "That said" / "That being said" (cut or "but", "yet"; do not overuse).

## Structural and meaning patterns

- **Uniform paragraph length / formulaic openings / suspiciously clean grammar:** review same-size paragraphs when boundaries ignore the argument; cut local throat-clearing like "In the rapidly evolving world of..." but move or rebuild context only with structural scope; do not sand away deliberate fragments, starting with "And" or "But", or comma splices the voice uses.
- **Significance inflation:** "marking a pivotal moment in the evolution of...", "a watershed moment". State what happened. If the sentence survives deleting the clause, delete it. Bare "in the evolution of" is ordinary English and passes; flag it only after an inflating word like chapter, milestone, role, or turning point.
- **Aphorism formulas:** slot-fill profundity ("X is the language of Y", "the architecture of trust", "X is not a tool but a mirror"). Replace with the source-supported claim it gestures at. Distinct from significance inflation and authority tropes: it manufactures a general law from one observation. Quotations and set idioms ("time is money") pass.
- **Generic future-narrative closers:** "may become one of the most important narratives of the next cycle", "is poised to become the next major chapter in [X]" (modal + become + one of the most [adjective] + narrative/story/trend/chapter/force). Cut, or use a falsifiable claim only if the source supplies its details.
- **Hedge-stacked predictions:** "could potentially create", "may eventually unlock", "might ultimately transform". Keep the one qualifier that carries the source's uncertainty; if unclear and it matters, leave it and ask. "The cache might reduce latency if the working set fits in memory" keeps both uncertainty and condition.
- **"Real/actual" adjective inflation:** "real on-chain tokenomics", "genuine utility", "true product-market fit" imply an unnamed fake. Drop the adjective unless the contrast is named ("real settlement, not bridged IOUs").
- **Moral-adjective category errors:** honest, faithful, truthful on non-agents ("an honest shape", "flagged honestly"). State a concrete property the source supports, or cut. Related: "the assumption stops being true" (write "no longer holds"); gratuitous universal quantifiers ("taught in every first-year course", use the real scope).
- **Transformation crutch (P2):** repeated unexplained relabeling ("the concern turns into panic", "the risk becomes real"). Ask what changed. Keep literal changes (water turns into ice), supported metaphors, and changes explained anywhere in the passage. Never invent a mechanism or actor.
- **Hashtag stuffing:** 6+ hashtags on a short post is a context-dependent flag, not authorship evidence (6 is an operational threshold; 5+ is a soft tell on linkedin and investor-email). Not hashtags: issue refs (`#88`), CSS hex colors, `#include`, URL fragments, Markdown headings, code. Fix: 2 to 3 specific tags or none.
- **Bullet lists of bare noun phrases:** 5+ consecutive short adjective-plus-noun bullets with no verb ("Stable mining efficiency / Reliable pool connectivity"). State checkable claims using supplied details, or leave a genuine list (changelog, parameters, ingredients) alone.
- **Copula avoidance:** "serves as", "features", "boasts", "presents", "represents" for "is" or "has". Default to is/has. Keep a real role ("Mina serves as chair during the hearing") and product nouns ("three features").
- **Subjectless fragments and agentless passives:** "No configuration file needed." Name the actor only if the source identifies it; never invent "you" or a team. Terse registers (README feature lists, changelogs, parameter docs, commit subjects) are the correct form; one deliberate fragment is rhythm.
- **False agency:** an obscured accountable decision-maker ("The decision emerged after the offsite") when naming them matters. Name the actor only if the source does. Conventional personification ("the data shows") and emergent change ("the culture shifted") pass.
- **Synonym cycling:** one referent rotated through developers, engineers, practitioners, builders. Use the clearest term consistently if the source says they are the same; keep distinct terms for distinct things; a repeated right word stays.
- **Vague attributions:** "Experts believe", "Studies show", "Research suggests". Cite the specific source if supplied; otherwise flag the gap or cut. Do not turn an attributed claim into the writer's own assertion by dropping the attribution.
- **Filler phrases:** "It is important to note that", "In terms of", "The reality is that".
- **Generic conclusions (P2):** "The future looks bright", "Only time will tell", "One thing is certain", "As we move forward". Cut; add a closing thought only if the source has one.
- **Chatbot artifacts:** "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel free to reach out", "Let me know if you need anything else", "In this article, we will explore...", "Let's dive in!". Remove.
- **"Let's" constructions:** "Let's explore / break this down / take a look" used as a transition rather than a real invitation to act.
- **Notability name-dropping and historical analogy stacking:** stacked prestige citations or "like the printing press, the telegraph, and the internet". Keep one relevant, supported reference; invent no date, venue, or argument.
- **Vague third-party validation:** unnamed authority plus superlative ("independent testing confirms", "analysts agree"). Name the source, test, and result only if supplied; named, checkable validation (a dated audit, a linked report) is fine.
- **Superficial -ing analyses and meaning-telling:** participle chains ("symbolizing..., reflecting..., showcasing...") and glosses like "this represents a broader shift". Replace with supplied facts or cut.
- **Promotional language:** "nestled within breathtaking foothills", "a vibrant hub of innovation". Use plain source-grounded description or cut.
- **Formulaic challenges:** "Despite challenges, [subject] continues to thrive". Name challenge and response only if supplied; otherwise cut or flag.
- **Speculative scenario openers:** "Imagine a world where...", "Picture a future in which...". Keep the claim at its confidence ("Every deploy would be instant"). Fiction, thought experiments with a payoff, and teaching "imagine a sorted array" pass.
- **False ranges:** "from the Big Bang to dark matter". List the actual topics.
- **Inline-header lists:** "**Performance:** Performance improved by...". Strip the redundant label; converting to prose needs structural scope.
- **List-label periods:** a period after a short bold label before the explanation continues; the colon form is clearer.
- **Title case headings** where the document uses sentence case.
- **Hyphenated modifier stacking:** "a high-quality, well-architected, future-proof solution"; the tell is density. Keep the modifier that matters.
- **Unnecessary hyphenation (P2 copyediting):** open noun phrases ("research-impact aggregator" to "research impact aggregator"); one-word compounds ("code-base", "data-set", "time-frame", "road-map"); adverbial or noun use ("in real-time", "out-of-the-box" after a verb) while the same compounds before a noun stay ("real-time analytics"). Keep established compounds (high-quality, open-access, third-party, machine-readable, server-side). Not authorship evidence.
- **Cutoff disclaimers:** "While specific details are limited", "As of my last update", "I don't have access to real-time data". Remove or flag; never turn missing information into a confident claim.
- **Speculative gap-filling:** hedged speculation dressed as background ("maintains a relatively low public profile", "is believed to have", "likely began his career in"). Worse than a cutoff disclaimer because it hides the gap. Cut, or use a supplied fact; keep a hypothesis the writer actually makes.
- **Unfilled placeholders:** `[Your Name]`, `[INSERT SOURCE URL]`, `2025-XX-XX`, `<!-- Add citation -->`. Fill only with supplied content or flag; keep placeholders intentional in templates and drafts.
- **Chatbot citation markup leaks:** `citeturn0search0`, `contentReference[oaicite:0]`, `oai_citation`, `[attached_file:1]`, `grok_card`. Strip the tokens; supply a reference only if given, else flag the citation gap.
- **AI-tool URL parameters:** `utm_source=chatgpt.com`, `copilot.com`, `openai`, `claude.ai`, `perplexity.ai`, `referrer=grok.com`. Strip only that parameter and keep the rest of the URL and any functional params.
- **Novelty inflation:** "He introduced a term", "a failure mode nobody talks about", "what nobody tells you". Remove the unsupported novelty claim, keep any supported action. Also invented labels coined mid-sentence and never defined ("the supervision paradox", "a coordination tax"): define on first use or describe the mechanism.
- **Infomercial engagement hooks:** "The catch?", "The kicker?", "Here's the thing.", "The best part?", "Plot twist:". Delete the hook and state the thing. Also fake-candid standalone openers ("Honestly?", "Look,", "Real talk:"); the word mid-sentence in casual prose is fine.
- **Launch-copy dramatic introductions:** "Enter Flowdesk.", "Meet Flowdesk, your new favorite treasury dashboard", "Think Notion meets Figma". State what the product is. "Meet Sarah, your new account manager", UI instructions ("Enter Password."), and stage directions pass.
- **Fake-casual register:** one-word verdict closers ("wild.", "unhinged."), stage directions ("*checks notes*", "*chef's kiss*", "*mic drop*"), wink asides ("(yes, really)"), label openers ("hot take", "fun fact", "pro tip", "PSA", "unpopular opinion"), "because of course it does", and self-QA volleys ("Is it fast? Yes. Is it cheap? Also yes."). Delete the prop, keep the observation; invent no reaction. A writer whose real voice runs on these keeps them.
- **Social endorsement closers:** "This one is worth your time:", "must-read", "Do yourself a favor", "Save this for later", "Thank me later". Use a supplied reason, else drop the generic call to action.
- **Stock reaction framing (style heuristic, zero authorship weight):** "What surprised me most", "I was fascinated to discover", "What struck me was", "The most interesting part" as empty frames, plus "hit(s) different". Keep authentic reactions, judgments, and rankings; a bare fact does not preserve "most surprising". Add expectations or reasons only if supplied.
- **Lingering-attention claims:** "the line I keep coming back to", "I can't stop thinking about this", "rattling around in my head all week". Keep it when a reason is attached ("I keep coming back to X because...").
- **False concession structure:** "While X is impressive, Y remains a challenge". Cut the empty frame while keeping both claims and their uncertainty; do not pick a side. A factual or temporal "while" ("While the worker restarted, the queue kept accepting jobs") stays.
- **Invented contrast-pair mirroring:** one half of a contrast is a real term and the other a fabricated mirror ("false precision rather than genuine accuracy"). Use a real opposite or state the positive claim directly.
- **Rhetorical question openers:** "But what does this mean for developers?", "So why should you care?". Answer only if the source does; otherwise cut or leave open.
- **Parenthetical hedging:** "(and, increasingly, Z)", "(or, more precisely, Y)". Give the aside its own sentence or cut it.
- **Numbered list inflation:** "Three key takeaways", "Five things to know". Justified only if the source has that many parallel items.
- **Reasoning chain artifacts:** "Let me think step by step", "Breaking this down", "Here's my thought process", "Step 1:" leaking from chain of thought. Cut scaffolding, keep the supplied reasoning.
- **Sycophantic tone:** "Great question!", "Excellent point!", "You're absolutely right!". Remove. Also cold-outreach flattery asks ("I'd value your take on this") as the whole ask; state the question. A colleague asking feedback on a named draft is fine.
- **Narrated candor:** "Two caveats I would rather flag than let you discover later:", "I want to be upfront:", "To be fully transparent:". Deletion test: if cutting the frame loses nothing, cut it. Substantive admissions ("I haven't tested this on Windows") and conflict-of-interest disclosures ("I own shares in the company discussed") stay. Judgment-only.
- **Acknowledgment loops:** "You're asking about...", "To answer your question...". Fine in replies that orient the reader ("To answer your question from Tuesday: ..."). Judgment-only.
- **Confidence calibration phrases:** "It's worth noting that", "Interestingly", "Surprisingly", "Importantly", "Notably", "Certainly", "Undoubtedly". Flag by density (one "notably" in 2,000 words is fine; three in 500 is not). Related authority tropes: "the real question is", "at its core", "fundamentally", "make no mistake", "the truth is". Consequence-free explanation: "This matters because..." flags only when it restates importance; keep a concrete consequence.
- **Self-labeling significance:** "That last move is the contrarian one", "This is the interesting part". Cut the label; let the explanation work.
- **Dramatized contrast against the crowd:** "shipped it in 2022, while everyone else was still debating timelines"; teaser form "the call most leaders won't make". State the fact; name a competitor only if supplied. Literal simultaneity ("she read while everyone else watched the movie") passes.
- **Wall-of-text replies:** in conversational registers (issue and PR comments, chat, DMs, email), a reply under about 150 words with 4+ sentences and no line break. Report it; break at existing thought boundaries only if restructuring is in scope. Never flag continuous long-form prose.
- **Recap-flattery opener:** summarizing the other person's own work back at them with praise before the point. Cut the recap, keep real thanks.
- **Excessive structure:** more than 3 headings in under 300 words; 8+ bullets in under 200 words when not list-shaped; empty section labels (Overview, Key Points, Summary, Conclusion, Introduction); fragmented headers (a heading plus a one-line restatement). During wording-only cleanup keep headings and order and report the issue.
- **Diff-anchored writing:** docs or comments narrating a change ("This function was added to replace...") instead of describing the thing. Describe current behavior from source-present facts. Changelogs, release notes, migration guides, and decision records are fine.
- **Performed-insight phrases:** "sit with that for a moment", "that's not nothing", "the punchline is", "worth naming", "that's the whole point", "the only metric that matters", "X is dead; long live X", sentence-initial "Turns out", staged discoveries ("the real story was"). One hit may be a choice; several is a tell. Keep quoted speech and genuinely comedic writing.
- **Negation chains:** "No fluff, no filler, no jargon.", "It didn't ask. It didn't wait.", "Don't call it a pivot. Call it a correction." Say what the thing is. Mid-sentence factual inventories ("takes no arguments, no headers, and no body") pass.
- **Dev-blog boilerplate:** "batteries included", "it just works", "zero config", "sane defaults", "small enough to fit in your head". Name a concrete behavior only if supplied. Quoting a product's own tagline passes.
- **Stacked rhetorical questions:** two or more in a row. Keep at most one; interviews, FAQs, and dialogue are fine.
- **Same-opener sentence runs:** three or more consecutive sentences opening on the same word or skeleton ("Maybe... Maybe... Maybe..."). Keep the first, vary or merge the rest; deliberate anaphora and pronoun narration ("He... He... He...") pass.
- **Stranded auxiliary contrast:** "The tool died; the data didn't." One is fine; ration it, and write the next contrast out in full.
- **Colon into a triple:** a colon opening onto exactly three comma-separated items. Audit the list; judge by genre (noisy in technical writing).
- **Manufactured punchlines and staccato drama:** three or more same-shape fragments in a row ("No aesthetic prior. No nostalgia. The old rules were gone."). Keep a fragment that earns emphasis, fold the rest into sentences using only supplied claims. Repeated empty concessions ("Not always. Not perfectly.") flag only when repeated and unexplained; keep meaningful ones ("Not during failover. Not for expired tokens.").
- **Repeated setup/reversal punchlines (P2, judgment-only):** two or more reversals that replace explanations ("We planned for every failure mode. Except the one that happened."). Keep supported, voice-appropriate reversals and comedy. Fix by merging into one sentence; if the failure is unnamed, ask.

## Rhythm and structure tests

- **Sentence and paragraph uniformity:** review runs of similar shape when the rhythm sounds accidental. Vary by clarifying the source, never by imposing word-count bands, adding questions, or chopping into fragments. Regularity alone neither authorizes a rewrite nor shows authorship.
- **Read-aloud test:** if a text-to-speech engine would sound natural reading it, it is probably too uniform.
- **Speaker and stance:** keep first person, opinions, and reactions the source has; their absence is not a finding.
- **Over-polishing:** removing every irregularity can push human writing toward machine-like profiles. Keep natural disfluency and idiosyncratic word choices.
- **Vocabulary diversity (stylometric):** over 200-word stretches, human English prose usually has a type-token ratio of about 0.50 to 0.65; below 0.40 on general prose is worth a second look, but narrow topics, technical reference, and second-language writing compress vocabulary legitimately. Do not thesaurus the text; repeat an accurate technical term.
- **Paragraph-reshuffle test:** if two body paragraphs can swap without notice, the piece is a list of points, not an argument. Report it; build a through-line only if structure is in scope.
- **Treadmill test:** for each paragraph ask what is new; if 40 to 60% could go with no loss, say so. Remove local throat-clearing; substantial condensing needs structural scope.
- **Rewrite from scratch vs patch:** five or more justified vocabulary findings across categories, three or more pattern categories, and uniform structure can support a structural diagnosis. Report it and patch only authorized spans; rebuild only if the user explicitly permits broad restructuring. Density does not grant that permission.

## Context profiles

Pass a context hint to adjust applicability and thresholds; with none, infer from cues and treat weak or unfamiliar cues as judgment calls.

- **`linkedin`:** short-form social; punchy fragments and visual formatting matter.
- **`blog`:** default long-form prose; all rules at full strength.
- **`technical-blog`:** code, architecture, APIs; technical terms pass.
- **`investor-email`:** high-trust audience; tighten everything; promotional language is the biggest risk.
- **`docs`:** documentation, READMEs, guides; clarity over voice.
- **`casual`:** Slack, internal notes, quick replies; catch only the worst offenders.

Detector `--context` mapping: linkedin and investor-email to `marketing`; blog to `general`; technical-blog and docs to `technical`; casual to `personal`. The profile tolerances below live in this skill; detector modes only change engine behavior.

**Tolerance matrix** (unlisted rules apply at full strength everywhere). S = strict, R = relaxed, X = skip, ES = extra strict. Columns: linkedin / blog / technical-blog / investor-email / docs / casual.

| Rule | li | blog | tech | inv | docs | cas |
|---|---|---|---|---|---|---|
| Em dashes | R (2 per post) | S | S | S | R | X |
| Bold overuse | R | S | S | S | R | X |
| Emoji in headers | R (1 to 2 at line end) | S | S | S | X | X |
| Excessive bullets | X | S | R | S | X | X |
| Hedging | S | S | R ("may" is accurate) | S | R | X |
| Word table | S | S | partial | S | R | P0 only |
| Promotional language | R | S | S | ES | S | X |
| Significance inflation | S | S | S | ES | R | X |
| Copula avoidance | X | S | R | S | X | X |
| Uniform paragraph length | X | S | S | S | R | X |
| Numbered list inflation | R | S | R | S | X | X |
| Rhetorical questions | R (1 hook) | S | S | S | S | X |
| Transition phrases | X | S | S | S | R | X |
| Generic conclusions | X | S | S | ES | X | X |
| Hashtag stuffing | S | S | S | ES | X | X |
| Bullet noun-phrase lists | S | S | R | S | R | X |
| Tier 3 phrase clustering | S | S | S | ES | R | X |
| Future-narrative closers | S | S | S | ES | X | X |
| Social endorsement closers | S | S | S | S | X | R (1 OK in a DM) |
| Hedge-stacked predictions | S | S | R | ES | R | X |
| Real/actual inflation | S | S | S | ES | R | X |
| Moral-adjective errors | S | S | R | S | R | X |
| Contrast-pair mirroring | S | S | R | S | R | X |
| Subjectless fragments and passives | R | S | R | S | X | X |

"Extra strict" means review every applicable instance instead of waiting for repetition (one unsupported "thriving ecosystem" can sink an investor email); sense and pass conditions still apply. "Skip" means do not audit that rule for that profile.

**Auto-detection cues:** under 300 words with hashtags or mentions: linkedin; code blocks, API references, or architecture: technical-blog; salutation plus investor or fundraising language: investor-email; step-by-step instructions, parameter docs, or README structure: docs; otherwise blog for audit coverage without forcing borderline context-dependent edits. Say which profile you used when it materially affects a finding.

## Voice profiles

Voice is optional and independent of context: context sets strictness, voice sets how the prose sounds. If none is named, infer from the input's register and impose no persona. Every target is bounded by the never-inject rules: bring out what the source has, never manufacture what it lacks.

- **`casual`:** when asked for explicitly, contractions and direct conversational sentences, without forced fragments or length quotas; when inferred, keep the source's existing casual markers. Keep first-person and concrete touches the source has, everyday wording (keep jargon the audience needs), meaningful warm hedges; cut corporate padding. For blogs, social, community.
- **`professional`:** active voice where the actor matters; vary accidental repetition without quotas; concrete claims when supplied (never invent a source behind "experts say"); keep an existing ask explicit; cut empty hedging, keep real uncertainty. For LinkedIn, investor email, sponsor pitches.
- **`technical`:** plain "X is Y" over inflated substitutes; separate ideas for comprehension; imperative for instructions when it matches the source; keep accurate terms and define one only if the source supplies the definition or the user asks; lists and tables where the content is list-shaped. For docs and technical blogs.
- **`warm`:** address the reader directly where the source already does, keeping its acknowledgment instead of adding one; cut empty intensifiers while keeping the degree; avoid performative empathy ("I completely understand how you feel"); unhurried cadence without a sentence-length band. For mentorship, onboarding, thank-yous.
- **`blunt`:** lead with the claim; cut windups like "It's important to note that"; em dashes rare, periods for emphasis when meaning allows; no padding to hit a rule of three; cut redundant hedge stacks but keep modals and qualifiers that carry uncertainty, conditions, or technical limits; direct sentences without manufactured staccato. For decision memos, thought leadership, hard feedback.

**Calibrate to a sample.** If the writer gives a sample of their own writing, analyze sentence length, contraction rate, paragraph openings, and recurring word choices, and match those instead of a named profile. Do not upgrade their vocabulary: if they write "stuff" and "things", keep that register.

**Composition.** Apply context and each rule's pass conditions first. An inferred voice does not reactivate a category the context skips. An explicit voice may authorize its stylistic target in editable prose but does not turn a context-exempt pattern into an AI-ism and cannot override source fidelity or protected content. House-style mechanics control typography after those gates. When voice and context set numeric thresholds for the same feature, use the stricter one; do not apply a global strictness maximum across different dimensions. Sensible pairings: casual with casual, professional with linkedin or investor-email, technical with docs or technical-blog.
