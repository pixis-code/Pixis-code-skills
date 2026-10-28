---
name: grounded-citations
description: "Anchor responses and documents with cited, checkable sources."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Research, Citations, Sourcing, Web, Reports]
    category: research
    related_skills: [arxiv, pdf, reddit-reading, rss-feeds, youtube-content]
---

# Grounded Citations

Every claim from an outside source gets an inline `[n]` marker + a trailing
`Sources:` list. A ledger script (`scripts/sources.py`) owns `url → [n]` —
numbers come from retrieval, never memory. Optional fact-check mode: attach
verbatim quotes per source (rejected if not word-for-word in the fetched
page); tag unsourced claims `[unverified]`; `verify --evidence` fails a draft
if a cited source has no quote.

Use for: chat, docs (md/PDF/docx/slides), reports. Skip for: quick syntax
checks, casual chat, creative writing. For academic BibTeX use `arxiv`
instead (`references/citation-formats.md`).

## Setup

Stdlib Python 3, no install. `S=~/.pixis/skills/grounded-citations/scripts/sources.py`
Ledger: `$PIXIS_HOME/cache/citations/ledger.json` (override: `--ledger` /
`PIXIS_CITATION_LEDGER`).

## Commands

| Action | Command |
|---|---|
| Fresh ledger | `sources.py reset` |
| Register | `sources.py add <url> [--title T]` → `[n]` |
| From JSON output | `sources.py ingest results.json` |
| Attach evidence | `sources.py quote <id> --text "exact" --from page.txt` |
| List ledger | `sources.py list [--json]` |
| Render Sources block | `sources.py render [--style markdown\|plain\|footnotes\|bibtex\|evidence]` |
| Render cited only | `sources.py render --cited-in draft.md` |
| Rewrite in place | `sources.py render --replace-in draft.md` |
| Check draft | `sources.py verify draft.md [--strict] [--min-coverage 0.6] [--evidence]` |

`add` is idempotent/URL-normalized — same page always gets the same id.

## Procedure

1. `reset` at task start (skip if continuing a draft with ids already set).
2. Register every URL via `add`/`ingest` right after fetching — before prose.
3. Cite while drafting: `Ice floats, less dense than water.[1][2]`
   — no space before bracket · `[1][2]` not `[1, 2]` · max 3 ids/sentence ·
   only ledger ids, never type a URL · no citation for your own knowledge ·
   conflicting sources get separate ids · exact figures/dates from source.
4. `render --cited-in <draft>` to append the block (pick `--style` per
   `references/citation-formats.md` for non-markdown).
5. `verify <draft>` before delivering — fails on unknown ids, mismatched
   block, or thin `--min-coverage`. Fix, re-run.
6. Chat answers: same steps, end with rendered `Sources:`.

## Multi-Platform Sweeps

"What's X saying about Y" isn't one `web_search` — fan out by source type,
collect in parallel, attribute each claim to its platform:

| Source | Route | Adds |
|---|---|---|
| Open web | `web_search` → `web_extract` | docs, articles, announcements |
| Reddit | `reddit-reading` | user experience, workarounds, sentiment |
| Blogs/releases | `rss-feeds` | dated primary posts, version history |
| Video | `youtube-content` | walkthroughs, demos, talks |
| Code | `terminal` + `gh search repos/issues` | implementations, open bugs |
| X/Twitter | `xurl` (read-only commands; needs API access) | announcements, developer chatter |

Register every URL from every route in the ledger as it arrives (step 2).
Keep opinion and measurement apart — a Reddit thread shows users *report*
something, not that it's true; pair it with a primary source or label it
sentiment. Report per-platform gaps ("Reddit search returned nothing newer
than March") instead of silently narrowing to what worked.

## Fact-Checking Mode

For medical/legal/financial/disputed claims:
1. `quote <id> --text "exact sentence" --from page.txt` — rejected if not
   verbatim in the page text.
2. Unsourced claim → tag `[unverified]`.
3. Disputed fact → cite both sources separately, don't pick one silently.
4. `verify report.md --evidence --min-coverage 0.5` then
   `render --style evidence --replace-in report.md`.

## Pitfalls

- Register after writing → wrong. Register at retrieval, always.
- Hand-editing ids/URLs → use `render`, never retype.
- Citing a snippet as a full read → `web_extract` the page first.
- >3 ids on one sentence.
- Paraphrasing into `quote --text` → verbatim only.
- `[unverified]` as a shortcut → it's for truly unsourceable claims only.

## Verify

`python "$S" verify report.md --strict --min-coverage 0.5` — pass means every
`[n]` is in the ledger, block matches ledger URLs, coverage meets threshold.
