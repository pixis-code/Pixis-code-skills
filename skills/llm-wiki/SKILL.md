---
name: llm-wiki
description: "Build and query an interlinked markdown LLM wiki (Karpathy pattern). Use when creating/ingesting/querying/linting a knowledge wiki. Not for a plain Obsidian vault without wiki schema (obsidian), citation ledgers alone (grounded-citations), or arXiv search (arxiv)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [wiki, knowledge-base, research, notes, markdown]
    category: research
    related_skills: [obsidian, grounded-citations, arxiv, pdf]
    attribution: Adapted from hermes-agent llm-wiki (MIT); pattern by Andrej Karpathy
---

# LLM Wiki

Persistent, compounding knowledge base as interlinked markdown files
([Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)).
Human curates sources; agent summarizes, cross-references, and maintains consistency.

**When to use:** create/start a wiki · ingest a source · query an existing wiki ·
lint/audit the wiki · research notes that should compound.

**Do not use:** casual Obsidian note edits without schema/index/log → `obsidian`;
inline citation ledger only → `grounded-citations`; paper search → `arxiv`.

## Wiki location

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

Set `WIKI_PATH` in the environment or `$PIXIS_HOME/.env`. Default: `~/wiki`.

## Architecture

```
wiki/
├── SCHEMA.md      # conventions, taxonomy, domain
├── index.md       # catalog with one-line summaries
├── log.md         # append-only action log
├── raw/           # immutable sources (articles, papers, transcripts, assets)
├── entities/      # people, orgs, products, models
├── concepts/      # topics
├── comparisons/   # side-by-side analyses
└── queries/       # filed query results worth keeping
```

Layer 1 `raw/` is immutable. Layer 2 wiki pages are agent-owned. Layer 3 is `SCHEMA.md`.

## Orient every session (required)

Before ingest/query/lint on an existing wiki:

1. Read `SCHEMA.md`
2. Read `index.md`
3. Scan the last ~20–30 lines of `log.md`

Prevents duplicates, missed links, and schema violations.

## Initialize a new wiki

1. Resolve `$WIKI_PATH` (or ask; default `~/wiki`)
2. Create the directory tree above
3. Ask the domain; write domain-specific `SCHEMA.md` (frontmatter rules, tag taxonomy,
   page thresholds, update policy)
4. Write initial `index.md` and `log.md`
5. Confirm ready; suggest first sources

Frontmatter on wiki pages: `title`, `created`, `updated`, `type`
(`entity|concept|comparison|query|summary`), `tags`, `sources`. Optional:
`confidence`, `contested`, `contradictions`. Use `[[wikilinks]]` (≥2 outbound
per page). Filenames: lowercase-hyphens.

Raw sources get `source_url`, `ingested`, `sha256` (body only) for drift detection.

## Core operations

### Ingest

1. Capture to `raw/` (URL/PDF/paste); set raw frontmatter; on re-ingest compare sha256
2. Discuss takeaways (skip in automated contexts)
3. Search `index.md` + wiki for existing entities/concepts
4. Create/update pages per SCHEMA thresholds; cross-link; provenance markers on
   multi-source pages; bump `updated`
5. Update `index.md` + append `log.md`
6. Report every file created/updated. Confirm before mass-updating 10+ pages.

### Query

1. Use `index.md` (and content search on large wikis)
2. Read relevant pages; synthesize with `[[page]]` citations
3. File substantial answers under `queries/` or `comparisons/`
4. Log the query

### Lint

Report: orphans, broken `[[links]]`, index gaps, bad frontmatter/tags, stale pages,
`contested`/`confidence: low`, raw sha256 drift, pages >200 lines, log rotation
(>500 entries). Append lint summary to `log.md`.

## Pitfalls

- Never modify `raw/`
- Always orient first
- Always update `index.md` and `log.md`
- No pages for passing mentions; no isolated pages without cross-links
- Tags only from SCHEMA taxonomy
- Handle contradictions explicitly — do not silently overwrite

## Completion criteria

- Oriented (or newly initialized) before writes
- Pages have valid frontmatter and ≥2 wikilinks
- Index + log updated for every ingest/create
- User confirmed before bulk mutations
