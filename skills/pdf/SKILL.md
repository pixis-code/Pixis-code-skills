---
name: pdf
description: "Create styled PDFs and read/merge/fill/OCR local PDF files. Use when building a professional PDF report/invoice, or merging/extracting/filling PDFs. Board reports use theme business (widescreen, navy cover, gold rules). Not for PowerPoint (powerpoint), Google Docs (google-workspace), or Notion (notion)."
version: 1.2.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [pdf, documents, forms, ocr, text-extraction, reportlab, pypdf, pdfplumber, styling]
    category: Productivity
    related_skills: [powerpoint, grounded-citations, arxiv, data-visualization]
    attribution: Adapted from Nous Research hermes-agent pdf skill (MIT) — see LICENSE; Pixis adds professional themes
---

# PDF

Create **professionally styled** PDFs from JSON specs, plus read/merge/split/
watermark/fill/OCR helpers via `pypdf`, `reportlab`, and `pdfplumber`.

**Create quality bar (mandatory):** board and performance reports use theme
`business` with `page_size: "widescreen"`, plus `brand`, `report`, and `footer`.
That theme paints a navy cover (`#0E1F38`), gold bars (`#E89B3C`), a teal
eyebrow, and a navy header band on later pages. `professional`, `midnight`, and
`forest` remain for shorter documents. Do **not** emit bare black-and-white
platypus defaults unless the user asks for `theme: "plain"`.

**When to use:** reports/invoices as PDF · fillable forms · extract text/tables ·
merge/split/stamp/secure · page PNGs for review/OCR.

**Do not use:** Google Docs → `google-workspace`; slide decks → `powerpoint`;
Notion → `notion`; pixel-perfect HTML-to-PDF (use a headless browser).

## Prerequisites

```bash
python -m pip install pypdf reportlab pdfplumber
# optional rasterization:
python -m pip install pypdfium2   # or install poppler (pdftoppm)
```

## How to run

```bash
python scripts/pdf_create.py spec.json -o out.pdf
python scripts/pdf_read.py doc.pdf --text
python scripts/pdf_read.py doc.pdf --meta
python scripts/pdf_merge.py a.pdf b.pdf -o merged.pdf
python scripts/pdf_split.py doc.pdf --pages 1-3,7 -o part.pdf
python scripts/pdf_fill_form.py form.pdf --fields-json values.json -o filled.pdf
python scripts/pdf_page_image.py doc.pdf --pages 1 --dpi 150 --out-dir imgs/
```

Forms/OCR/edit playbooks: `references/forms.md`, `references/ocr-extraction.md`,
`references/nano-pdf-editing.md`. Styling examples: `references/styling.md`.

## Creating a professional PDF

### 1. Write a rich JSON spec (default)

For a performance report, set `theme` to **business** (widescreen is the default
for that theme). Also set `title`, `brand`, `footer`, and a mix of structured
elements — not only bare paragraphs. Omitting `theme` stays on `professional`
(A4) for short notes.

```json
{
  "title": "Q1 2026 Business Performance",
  "subtitle": "Reporting period · Q1 2026",
  "brand": "Growlio Demo",
  "report": "Q1 2026 Business Performance",
  "footer": "Growlio Demo • Quarterly Business Performance Report",
  "author": "Analytics",
  "theme": "business",
  "page_size": "widescreen",
  "page_numbers": true,
  "elements": [
    {"type": "heading", "text": "Executive summary", "level": 1},
    {"type": "paragraph", "text": "Revenue grew <b>45.8%</b> versus last quarter."},
    {"type": "callout", "text": "Key risk: April demand dip (−12%).", "style": "warn"},
    {"type": "heading", "text": "Highlights", "level": 2},
    {"type": "bullet_list", "items": [
      "North region led volume (+18%)",
      "Marketing efficiency highest in Services"
    ]},
    {"type": "heading", "text": "Results by region", "level": 2},
    {"type": "table", "header": true, "rows": [
      ["Region", "Units", "Revenue"],
      ["North", "1,250", "$420k"],
      ["South", "980", "$310k"]
    ]},
    {"type": "spacer", "height": 8},
    {"type": "hrule"},
    {"type": "paragraph", "text": "See appendix for methodology."}
  ]
}
```

```bash
python scripts/pdf_create.py spec.json -o report.pdf
```

### 2. Element types

| Type | Purpose |
|------|---------|
| `heading` | `level` 1–3 (accent-colored) |
| `paragraph` | Body; supports `<b>`, `<i>`, `<br/>` |
| `bullet_list` / `numbered_list` | `items: [...]` |
| `table` | `rows` + `header: true` (accent header + zebra rows) |
| `callout` | Highlight box; `style`: `info` \| `warn` \| `success` |
| `image` | `path`, optional `width` |
| `spacer` | `height` in points |
| `hrule` | Accent divider |
| `pagebreak` | New page |

### 3. Themes

| Theme | Look |
|-------|------|
| `business` | Widescreen board report: navy cover, gold bars, header band on later pages |
| `professional` (**default if theme omitted**) | Corporate blue accent, white header text on tables |
| `midnight` | Indigo accent |
| `forest` | Green accent |
| `plain` | Greyscale — **only if user asks for minimal/B&W** |

Optional: `"accent": "#C45C26"` overrides the theme accent.

### 4. Layout rules for agents

1. Prefer **short sections** with H1/H2, not one wall of paragraphs.  
2. Put KPIs in a **callout** or **table**, not buried in prose.  
3. Use **bullet_list** for 3+ parallel points.  
4. After create, run `pdf_read.py out.pdf --meta` (and optionally
   `pdf_page_image.py` for a visual check).  
5. Never claim “professional styling” while using `theme: "plain"` or only
   unstyled paragraphs.

## Other workflows

1. **Inspect** — `pdf_read.py file.pdf --meta`. Decrypt / OCR scanned pages as needed.  
2. **Extract** — `--text` / `--tables`; parse JSON.  
3. **Manipulate** — merge/split/rotate/watermark/stamp.  
4. **Forms** — lint → `pdf_make_form.py` → fill.  

## Pitfalls

- Omitting `theme` stays on professional A4. Performance reports must set
  `"theme": "business"`. `plain` without being asked yields the weak B&W look.
- Scanned PDFs need OCR — empty extract ≠ empty document.
- Helper CLIs use **1-based** pages.
- PDF/A is out of scope.

## Completion criteria (create)

- [ ] Performance reports set `theme` to `business` and `page_size` to `widescreen`
- [ ] Title + at least one heading, and tables/lists/callouts where content fits
- [ ] Output PDF exists; `--meta` page_count makes sense
- [ ] Source files not overwritten unless requested
