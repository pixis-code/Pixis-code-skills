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

A sample deck shows finish. It is not a palette or a layout to copy.

### Decide once, before any slide

Write down, then reuse on every slide:

- the outline
- 1–3 fonts
- the hex palette

Do not pick a new palette or a new type scale on the next slide. In the reply, state those choices.

### Palette

- One dark, one light, and 1–2 accents, all hex. A named theme is only a start (`professional`, `business`, `midnight`, `forest`, `blush`, `sage`, `sand`, `charcoal`). User-named colors go in `palette` or `colors` and replace that start.
- No pure `#FFFFFF` or `#000000`. Tone them toward the palette.
- Two light background tones may alternate. One dark slide is the statement slide, not the default for every slide.
- Body text at least 4.5:1 contrast against its background. Text at 44px and up may use 3:1.
- Colors that must be told apart differ in lightness, not only hue.
- Color never carries the meaning alone. The label says it too.
- `plain` only when the user wants unstyled Office slides.

### Type

- One scale, reused: **48 / 36 / 22 / 16 / 12** pt (a 96 / 72 / 44 / 32 / 24 px scale on the 13.333×7.5 in slide). Set it with `sizes`.
- Nothing below 12pt.
- Emphasize with weight or color, not a new size.
- A serif for titles and a clean sans for body. Vary the pairing from deck to deck. Set `fonts.title` and `fonts.body`. Use `fonts.font` only when the user wants a single face.

### Layout

- 16:9 slide. Keep the heading on the same top line on every content slide.
- Slides of the same kind use the same structure.
- Footer is one row: label on the left, page number on the right. Nothing below it.
- Fill about 70% of the column and leave room. If a slide is full, split it.
- Card text is centered. Card height follows the text, not one fixed height.

### Content

- One idea per slide. Turn a list into cards, a table, big numbers, or one statement.
- Cards differ by role. The key card may be `"tone": "dark"`. The others stay light.
- Titles use the same grammar, such as noun phrases.
- Do not invent statistics or quotes. Unknown facts are placeholders like `[Presenter name]`.
- Numbers that are real go in `kpis`. Parallel groups go in `cards`. Two or three short lines stay bullets.

### Process

1. Write the deck index (slide titles only).
2. Build the cover.
3. Build the remaining slides in small batches.
4. Put speaker `notes` on every slide.

## Spec syntax

Set these on the deck. Slide fields override the deck for that slide. Sizes are points. Colors are `#RRGGBB`, `RRGGBB`, or a name (`red`, `navy`, `teal`).

| Field | What it sets |
|-------|----------------|
| `theme` | Starting palette: `professional`, `business`, `midnight`, `forest`, `blush`, `sage`, `sand`, `charcoal`, or `plain` |
| `palette` | `["cover", "secondary", "eyebrow"]` — replaces the theme colors |
| `colors` | One role: `accent`, `gold`, `eyebrow`, `cover`, `header` |
| `fonts` | `{"title": "Georgia", "body": "Calibri"}`. `font` sets both faces |
| `sizes` | `{"title": 48, "heading": 36, "subtitle": 22, "body": 16, "kpi": 36, "table": 16}` — nothing under 12 |
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

1. **Create** — decide palette, fonts, and the outline first, then JSON
   (`layout`, `title`, `bullets`, `cards`, `kpis`, `tables`, `charts`, `notes`).
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
