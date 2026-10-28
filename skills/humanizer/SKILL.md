---
name: humanizer
description: "Rewrite text so it stops sounding AI-generated and has a real voice (strips AI-isms, filler, inflated claims, chatbot residue; optionally matches a writing sample). Use when the user asks to humanize, de-AI, or de-slop text, edit a draft (blog, essay, PR description, docs, email, resume) to sound natural, match their voice, or check prose for AI tells before publishing; also for your own user-facing prose. Not for fact-checking, translation, or generating new content from scratch."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Creative
    tags: [writing, editing, humanize, anti-ai-slop, voice, prose, text]
    related_skills: [grounded-citations, docx]
---

# Humanizer

Find and remove the marks of machine-written text, then give the prose a human voice. Language models drift toward the statistically safest phrasing, which is where the patterns below come from.

## When to use

- "Humanize", "de-AI", "de-slop" a text, or make it not read like an LLM wrote it.
- Edit a blog post, essay, PR description, docs, memo, email, tweet, or resume bullet to sound natural.
- Match the user's own voice from a sample.
- Audit prose for AI tells before publishing.
- Run a quick pass over your own release notes, PR text, docs, and summaries.

Input arrives inline (rewrite in the reply), as a file (read it, apply targeted edits per section, show the diff or changed text, never overwrite silently), or with a voice sample (see below).

## Task

1. Scan for the 34 patterns below.
2. Rewrite offending parts with plain alternatives.
3. Keep the meaning intact. Never add a claim, number, name, feature, or source that is not in the original. If the source is mostly filler, the rewrite should be short: keep the one real point, drop the rest, and ask the user for concrete details instead of inventing them.
4. Keep the intended tone (formal, casual, technical); if a sample exists, match it.
5. Add personality; stripping patterns is only half the job.
6. Final audit: ask "What makes this still obviously AI-written?", list the remaining tells briefly, revise once more.
7. Pre-send check on the whole reply (rewrite and your own commentary), fixing each hit: any em dash; clipped fragments or kickers ("no fuss.", "Every time."); adverb or filler openers (Honestly, Interestingly, So,); "I think"/"I believe" before a plain fact; leftover chatbot closers ("happy to help", "let me know"); any detail not present in the source. A problem flagged in the audit must not reappear in the final.

## Voice calibration (optional)

If the user supplies their own writing, study it first: sentence length, word level (casual vs academic), how paragraphs open, punctuation habits (dashes, parentheses, semicolons), recurring phrases, and how transitions work. Then mimic those traits: short sentences stay short, and "stuff"/"things" must not become "elements"/"components". With no sample, use the natural, varied, opinionated voice described next.

## Personality

Sterile writing is as obvious as slop. Signs: uniform sentence length and structure, no opinions, no uncertainty, no first person where it fits, no humor, press-release tone. To add voice:

- **Have opinions.** React to the facts instead of listing pros and cons.
- **Vary rhythm.** Short sentences, then longer ones that take their time.
- **Admit complexity.** "Impressive but also unsettling" beats "impressive."
- **Use "I" when it fits.** "I keep coming back to..." signals a person thinking.
- **Allow some mess.** Asides and half-formed thoughts are human; perfect structure feels algorithmic.
- **Be specific about feelings** rather than saying "concerning."

Soulless: "The experiment produced interesting results. Some developers were impressed while others were skeptical." Alive: "I don't know how to feel about this one. 3 million lines of code, written while the humans slept. Half the community is thrilled, half are explaining why it doesn't count."

## Patterns

### Content

1. **Inflated significance/legacy.** Watch: stands as, testament, pivotal, crucial role, underscores, reflects broader, evolving landscape, marks a shift, indelible mark. Say what happened. "Established in 1989, marking a pivotal moment in regional statistics" -> "Established in 1989 to publish regional statistics independently of the national office."
2. **Notability name-dropping.** Watch: cited in major outlets, leading expert, active social media presence. Give one concrete cited fact: "In a 2024 NYT interview, she argued regulation should focus on outcomes."
3. **Tacked-on -ing phrases.** Watch: highlighting, ensuring, reflecting, symbolizing, fostering, showcasing. Cut the participle or make it a real sentence with a source: "The temple uses blue, green, and gold; the architect said they reference local bluebonnets and the Gulf coast."
4. **Promotional tone.** Watch: boasts, vibrant, rich, nestled, breathtaking, groundbreaking, must-visit, stunning. "Nestled in the breathtaking Gonder region..." -> "A town in the Gonder region, known for its weekly market and 18th-century church."
5. **Vague attribution.** Watch: experts argue, industry reports, observers note, several sources. Name the source: "...according to a 2019 survey by the Chinese Academy of Sciences."
6. **Formulaic "Challenges and future" sections.** Watch: Despite its..., faces challenges..., continues to thrive. Replace with dated, specific facts: "Congestion rose after three IT parks opened in 2015; a drainage project began in 2022."

### Language and grammar

7. **AI vocabulary.** Watch: additionally, align with, crucial, delve, enduring, enhance, foster, garner, highlight (verb), interplay, intricate, key (adj.), landscape (abstract), pivotal, showcase, tapestry, testament, underscore, valuable, vibrant. Also business clichés: at the end of the day, when it comes to, moving forward, deep dive, game-changer, double down, make no mistake, it turns out, let me be clear, navigate (challenges), lean into, unpack, straightforward. Swap for plain words.
8. **Copula avoidance.** serves as / stands as / boasts / features / offers -> is / are / has. "The gallery boasts over 3,000 sq ft" -> "The gallery has 3,000 sq ft."
9. **Negative parallelism and tailing negations.** "Not only... but...", "It's not just X, it's Y", and clipped tails like "no guessing". Say the point directly: "The heavy beat adds to the aggressive tone." / "...without forcing the user to guess."
10. **Rule of three.** Don't force triplets: "keynotes, panels, and networking" -> "talks and panels, plus time to mingle."
11. **Synonym cycling.** protagonist / main character / central figure / hero for one subject. Repeat the noun or use a pronoun.
12. **False ranges.** "From the Big Bang to the cosmic web, from stars to dark matter" where X and Y aren't a real scale. List the topics.
13. **Passive voice and subjectless fragments.** "No configuration file needed. Results are preserved automatically." -> "You don't need a configuration file. The system preserves results automatically."

### Style

14. **Em dash overuse.** Do not use em dashes (—) or spaced dashes in the rewrite; use commas, periods, colons, or parentheses.
15. **Mechanical boldface.** Drop bold on every term ("**OKRs**, **KPIs**...").
16. **Inline-header lists.** Bullets starting "**Performance:** Performance has been enhanced..." -> fold into one sentence.
17. **Title Case headings.** Use sentence case.
18. **Emoji decoration** on headings and bullets. Remove.
19. **Curly quotes** (“ ” ’). Use straight quotes.

### Communication

20. **Chatbot residue.** Watch: I hope this helps, Certainly!, Of course!, Let me know, Here is a... Delete; start with the content.
21. **Knowledge-cutoff disclaimers.** Watch: as of [date], based on available information, specific details are limited. State the fact with its source, or say it is unknown.
22. **Sycophancy.** "Great question! You're absolutely right..." -> go straight to the substance.

### Filler and hedging

23. **Filler phrases.** "In order to" -> "To"; "Due to the fact that" -> "Because"; "At this point in time" -> "Now"; "In the event that" -> "If"; "has the ability to" -> "can"; "It is important to note that" -> drop.
24. **Over-hedging.** "could potentially possibly be argued... might have some effect" -> "may affect."
25. **Generic upbeat endings.** "The future looks bright... exciting times ahead" -> a concrete fact, e.g. "The company plans two more locations next year."
26. **Uniform hyphenation** of common pairs (cross-functional, high-quality, data-driven, decision-making, client-facing, well-known, real-time, long-term, end-to-end). Humans hyphenate these inconsistently; rare technical compounds are fine to hyphenate.
27. **Authority tropes.** Watch: the real question is, at its core, what really matters, fundamentally, the heart of the matter. The next sentence usually restates something ordinary. "The real question is whether teams can adapt" -> "The question is whether teams can adapt."
28. **Signposting.** Watch: let's dive in, let's break this down, here's what you need to know, without further ado. Skip the announcement and state the content.
29. **Echo headers.** A heading followed by a one-line paragraph restating it ("## Performance / Speed matters."). Remove the warm-up line.

### Rhythm and rhetoric

30. **Forced metaphors.** Decorative or mixed metaphors, often explained right after ("The codebase is a garden... In other words, delete unused code"). Say the literal thing.
31. **Dramatic fragments and punchy kickers.** "Pay for what it does. Not promises. It just works. Every time." and a quotable closing line on every section. Merge into a normal sentence with a subject. This is about rhythm and showmanship, distinct from #13 (hidden actors).
32. **Self-answered rhetorical questions.** "What makes an API good? Predictability. Think about it." -> "A good API is predictable."
33. **Opener tics.** So..., Look,, habitual And/But starts, "I think" before a fact, and adverb openers (Interestingly, Importantly, Notably, Crucially, Essentially, Ultimately). Drop the opener and lead with substance.
34. **Reassurance kickers.** "And that's okay.", "There's nothing wrong with that.", "you're not alone", "it's completely normal." Trust the reader; make the point and stop.

## Process

1. Read the full input (load the file if one is given).
2. Mark every instance of the patterns.
3. Rewrite each: natural when read aloud, varied structure, specific details over vague claims, tone suited to context, simple is/are/has where fitting.
4. Present a draft.
5. Ask "What makes this still obviously AI-generated?" and list remaining tells briefly.
6. Revise to remove them, run the pre-send check (task step 7), and present the final version.
7. For file input, apply targeted edits and show what changed.

## Output format

1. Draft rewrite.
2. Brief bullets answering "What makes this still obviously AI-generated?"
3. Final rewrite.
4. Optional short summary of the changes.

## Completion criteria

- Meaning, facts, and intended tone are unchanged; no new claims, names, numbers, or sources were invented.
- None of the 34 patterns remain unintentionally, and the final text contains no em dashes or kicker fragments.
- Voice matches the sample if one was given.
- File edits were shown, not silently applied.
