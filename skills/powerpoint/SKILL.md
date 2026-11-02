---
name: powerpoint
description: "Create styled .pptx decks and read or edit them with python-pptx. Use for pitch decks and slide presentations. Fit the palette and layout to the content, and use colors the user names. Not for PDF files (pdf), Google Slides (google-workspace), or Notion (notion)."
version: 1.5.0
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

## Design quality bar (create)

Build a deck for this request. A sample file is an example of quality, not a
look to copy and not a theme every deck must use.

Decide the palette from the content and from any colors the user names. Named
themes (`professional`, `business`, `midnight`, `forest`, `blush`, `sage`,
`sand`, `charcoal`) are starting points. Set `"theme"` when one fits. When the
user names colors, set `palette` or `colors` and those replace the starting
point. `palette` order is cover, secondary, eyebrow. `plain` is only for an
unstyled Office look. In the reply, say which colors you used and why.

Match the layout to the content:

1. **Title slide** — short title, subtitle, and a brand line when there is one.
2. **One idea per content slide.** Use a header, then the content.
3. **Numbers** go in `kpis` (value + label). The script draws them as cards.
4. **Parallel groups** (options, steps, compare) go in `cards`, each with a
   title and a few lines. Set `"tone": "dark"` only on a card that should be
   filled. A list of four or more lines becomes cards. Two or three short lines
   stay `bullets`, and those bullets show a real dot.
5. **Comparisons** use a `table` or a `chart`. Leave table size unset. The
   script makes it wide, under the title, with a header row. A chart is placed
   below cards so they do not overlap.
6. **One font for the whole deck**, heading and body. Set
   `"fonts": {"font": "Calibri"}` when the user names a face. Otherwise the
   theme supplies one face. Do not mix two faces in one deck.
7. Set `brand`, `report`, and `footer` from the user's words.

Illustration only. Do not reuse this copy or these colors unless the request
is this request:

```json
{
  "theme": "professional",
  "fonts": {"font": "Calibri"},
  "brand": "Example",
  "footer": "Example",
  "slide_size": "16:9",
  "slides": [
    {"layout": "title", "title": "Quarterly review", "subtitle": "What changed"},
    {"layout": "title_content", "title": "Results",
     "kpis": [
       {"value": "12%", "label": "Growth"},
       {"value": "3", "label": "Regions ahead"}
     ],
     "bullets": ["North led volume", "Hold spend where return is weakest"]},
    {"layout": "title_content", "title": "Options",
     "cards": [
       {"title": "Keep", "items": ["Current plan"]},
       {"title": "Change", "items": ["Shift budget"]}
     ]}
  ]
}
```

## Spec syntax

Set these on the deck. Slide fields override the deck for that slide. Sizes are points. Colors are `#RRGGBB`, `RRGGBB`, or a name (`red`, `navy`, `teal`).

| Field | What it sets |
|-------|----------------|
| `theme` | Starting palette: `professional`, `business`, `midnight`, `forest`, `blush`, `sage`, `sand`, `charcoal`, or `plain` |
| `palette` | `["cover", "secondary", "eyebrow"]` — replaces the theme colors |
| `colors` | One role: `accent`, `gold`, `eyebrow`, `cover`, `header` |
| `fonts` | `{"font": "Calibri"}` — one face for the whole deck |
| `sizes` | `{"title": 36, "heading": 28, "subtitle": 16, "body": 16, "kpi": 26, "table": 15}` |
| `brand`, `report`, `footer` | Running text, from the request |

Slide content:

| Field | Syntax |
|-------|--------|
| `bullets` | `"Line"` or `{"text": "Line", "level": 1, "size": 18, "bold": true, "color": "1F4E79", "font": "Calibri"}` |
| `kpis` | `{"value": "12%", "label": "Growth", "color": "teal"}` |
| `cards` | `{"title": "Option", "items": ["One line"], "tone": "dark"}` — omit `tone` for a light card |
| `tables` | `{"header": true, "font_size": 15, "rows": [["A", "B"], ["1", "2"]]}` — leave `left`, `top`, `width`, and `height` unset |
| `charts` | `{"type": "bar", "categories": ["Q1"], "series": {"North": [10]}}` — types: `bar`, `bar_h`, `line`, `pie` |

See `references/design.md`.

## Procedure

1. **Create** — JSON with `theme` plus slides (`layout`, `title`, `bullets`,
   `tables`, `charts`, `images`, `shapes`, `notes`). Prefer the design bar above.
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
- Colors and layout follow this request. User-named colors are in `palette` or `colors`.
- The reply says which colors were used.
- Title slide plus content that fits the material: cards, numbers, a wide table, or a short bullet list. Not one copied sample and not a wall of lines.
- Edits confirmed via `--outline` (and render when visuals matter).
- Missing optional tools reported honestly (`rendered: false`), not as success.
