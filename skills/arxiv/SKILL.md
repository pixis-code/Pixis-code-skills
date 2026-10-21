---
name: arxiv
description: "Search arXiv papers by keyword, author, category, or ID."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Research, Arxiv, Papers, Academic, Science, API]
    related_skills: [pdf, grounded-citations]
---

# arXiv Research

Search/fetch papers via arXiv's free REST API — no key, no deps. Returns
Atom XML; use `scripts/search_arxiv.py` for clean parsed output.

```bash
python scripts/search_arxiv.py "GRPO reinforcement learning" --max 10 --sort date
python scripts/search_arxiv.py --author "Yann LeCun" --max 5
python scripts/search_arxiv.py --category cs.AI --sort date
python scripts/search_arxiv.py --id 2402.03300,2401.12345
```

Raw API: `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"`
or `?id_list=2402.03300,2401.12345` for specific papers. Read a paper with
`web_extract(urls=["https://arxiv.org/abs/ID"])` (abstract) or `.../pdf/ID`
(full text, via `pdf` skill for local processing).

## Query Syntax

`all:` all fields · `ti:` title · `au:` author · `abs:` abstract ·
`cat:` category · `co:` comment. Example: `all:transformer+attention`.

Boolean: `+`=AND (default) · `all:GPT+OR+all:BERT` ·
`all:language+model+ANDNOT+all:vision` · phrase `ti:"chain+of+thought"` ·
combined `au:hinton+AND+cat:cs.LG`.

**Params:** `sortBy` = relevance/lastUpdatedDate/submittedDate ·
`sortOrder` = ascending/descending · `start` = offset (0-based) ·
`max_results` = default 10, max 30000.

**Categories:** cs.AI (AI) · cs.CL (NLP) · cs.CV (vision) · cs.LG (ML) ·
cs.CR (crypto/security) · stat.ML (ML stats) · math.OC (optimization) ·
physics.comp-ph. Full list: arxiv.org/category_taxonomy

## Semantic Scholar (citations, related work, authors)

arXiv has no citation data — Semantic Scholar fills that gap (free, 1
req/sec, no key; JSON via `python -m json.tool`).

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,referenceCount,influentialCitationCount,year,abstract"
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10"
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10"
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,citationCount,externalIds"
curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" -H "Content-Type: application/json" -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}'
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,citationCount,paperCount"
```

Useful fields: `title, authors, year, abstract, citationCount,
referenceCount, influentialCitationCount, isOpenAccess, openAccessPdf,
fieldsOfStudy, publicationVenue, externalIds`.

## Workflow

1. Discover (`search_arxiv.py` + `--sort date`) → 2. Check impact
(citationCount/influentialCitationCount) → 3. Read abstract then full text
→ 4. Related work (`/references`) → 5. Recommendations
(`/recommendations`) → 6. Track authors (`/author/search`).

## Rate Limits

arXiv: ~1 req/3s, no auth. Semantic Scholar: 1 req/s, no auth (100/s with key).

## Notes

- IDs: old (`hep-th/0601001`) vs new (`2402.03300`). PDF `.../pdf/{id}` ·
  Abstract `.../abs/{id}` · HTML (when available) `.../html/{id}`.
- **Versioning** — `abs/1706.03762` resolves to latest; `...v1` pins a
  version. Cite the version you actually read (later versions can differ
  materially); the API's `<id>` field returns the versioned URL.
- **Withdrawn papers** — check `<summary>` for "withdrawn"/"retracted"
  before trusting a result; metadata may be incomplete.
