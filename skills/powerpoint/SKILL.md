---
name: powerpoint
description: "Create, read, and edit .pptx PowerPoint decks with python-pptx. Use when the user asks for a pitch deck, slides, or a pptx presentation. Not for PDF files (pdf), Google Slides/Docs (google-workspace), or Notion (notion)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [pptx, powerpoint, presentations, slides, office, python-pptx]
    category: Productivity
    related_skills: [pdf, google-workspace]
    attribution: Adapted from Nous Research hermes-agent powerpoint skill (MIT) — see LICENSE
---

# PowerPoint

Create, inspect, and edit `.pptx` decks with `python-pptx`. Five helpers cover
JSON-spec creation, structured read-back, in-place edits, template fills, and
optional slide PNG rendering — offline, no PowerPoint install required.

**When to use:** build a deck · extract text/notes/tables/charts · replace text
or chart data · template-driven brand decks · render slides to PNG.

**Do not use:** PDF files → `pdf`; Google Slides/Drive → `google-workspace`;
Notion → `notion`; legacy `.ppt` (convert first with
`soffice --convert-to pptx` if LibreOffice is available).

## Prerequisites

```bash
python -m pip install python-pptx
python -c "import pptx; print(pptx.__version__)"
# optional render/PDF export:
# LibreOffice (soffice) + poppler (pdftoppm)
```

`pptx_render.py` exits 0 with `{"rendered": false, "missing": [...]}` when
render tools are absent — create/read/edit still work.

## How to run

```bash
python scripts/pptx_create.py deck.json out.pptx
python scripts/pptx_read.py deck.pptx --outline
python scripts/pptx_read.py deck.pptx --notes
python scripts/pptx_read.py deck.pptx --images ./img
python scripts/pptx_edit.py deck.pptx --replace-text "Old Corp" "New Corp"
python scripts/pptx_edit.py deck.pptx --chart-data update.json
python scripts/pptx_edit.py deck.pptx --duplicate-slide 2
python scripts/pptx_from_template.py brand.pptx out.pptx --values vals.json
python scripts/pptx_render.py deck.pptx --outdir ./render
```

Author JSON specs as UTF-8; parse script JSON from stdout.

## Quick reference

| Task | Command |
|------|---------|
| New deck | `pptx_create.py spec.json out.pptx` |
| 16:9 / 4:3 | `"slide_size": "16:9"` or `"4:3"` in spec |
| Outline JSON | `pptx_read.py deck.pptx --outline` |
| Replace text | `pptx_edit.py … --replace-text OLD NEW` |
| Chart data | `pptx_edit.py … --chart-data spec.json` |
| Template fill | `pptx_from_template.py tpl.pptx out.pptx --values v.json` |
| Slide PNGs | `pptx_render.py deck.pptx --outdir DIR` |
| Export PDF | `soffice --headless --convert-to pdf --outdir ./out deck.pptx` |

## Procedure

1. **Create** — JSON slides with `layout`, `title`, `bullets`, `tables`,
   `charts`, `images`, `shapes`, `notes`, optional `background` / `footer`.
2. **Read** — `--outline` for structure; `--images DIR` to dump pictures.
3. **Edit** — combine flags in one `pptx_edit.py` pass; use `--output` to keep
   the original. Chart `"ops"` round-trip via full `replace_data`.
4. **Template** — replace `{{token}}` values; append slides using template layouts.
5. **Verify** — re-read outline; optionally render PNGs and inspect visually.

## Pitfalls

- Run-splitting: `--replace-text` merges identically formatted runs first.
- Chart slides cannot be duplicated — rebuild the chart instead.
- Reorder/remove are XML-level; re-read the deck afterward.
- Cross-deck slide copy is unsupported.
- Default create size is 16:9 unless the spec says otherwise.

## Verification

1. `pptx_read.py OUT.pptx --outline` — slide count, texts, charts, notes.
2. Optional: `pptx_render.py` + visual PNG review.
3. Unit contract (needs python-pptx + pytest):
   `python -m pytest tests/ -q`

## Completion criteria

- Output `.pptx` exists and outline matches the request.
- Edits confirmed via `--outline` (and render when visuals matter).
- Missing optional tools reported honestly (`rendered: false`), not as success.
