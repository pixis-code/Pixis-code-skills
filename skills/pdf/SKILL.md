---
name: pdf
description: "Create styled PDFs and read/merge/fill/OCR local PDF files. Use when building a report or invoice, or merging/extracting/filling PDFs. Choose the theme that fits the topic (business, blush, sage, sand, charcoal, midnight, forest) and use the user's colors when they name them. Not for PowerPoint (powerpoint), Google Docs (google-workspace), or Notion (notion)."
version: 1.4.0
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

**Create quality bar (mandatory):** choose the theme that fits the topic and
audience, set `"theme"`, and say which one you chose. Do not default every
report to `business`.

| Topic | Theme |
|-------|--------|
| Finance, enterprise, board | `business` |
| Beauty, wellness, lifestyle | `blush` or `sage` |
| Tech, startups | `midnight` |
| Sustainability, health | `forest` |
| Hospitality, food, travel | `sand` |
| Fashion, architecture, editorial | `charcoal` |

Those themes use a widescreen cover, bars, an eyebrow, and a header band, in
that theme's colors. Also set `brand`, `report`, and `footer`. When the user
names colors, set `palette` or `colors` and those values replace the cover,
rules, eyebrow, and table header. Hex (`#B91C1C`) and names (`red`, `navy`,
`gold`, `teal`, `blue`, `green`, `black`) both work. Omitting `theme` stays on
`professional` (A4, no cover) for a short note. Do **not** emit bare
black-and-white platypus defaults unless the user asks for `theme: "plain"`.

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

Set `theme` from the topic table above (widescreen is the default for those
themes). Also set `title`, `brand`, `footer`, and a mix of structured elements.
The example below is a finance report, so its theme is `business`. A beauty
report would use `blush` or `sage` instead. Omitting `theme` stays on
`professional` (A4) for short notes.

```json
{
  "title": "Q1 2026 Business Performance",
  "subtitle": "Reporting period · Q1 2026",
  "brand": "Northwind",
  "report": "Q1 Business Performance",
  "footer": "Northwind • Quarterly Business Performance Report",
  "author": "Analytics",
  "theme": "business",
  "palette": ["navy", "gold", "teal"],
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
| `business` | Finance / board. Navy cover, gold bars |
| `blush` | Beauty / lifestyle. Light blush cover, rose type |
| `sage` | Wellness. Light sage cover, brass rule |
| `sand` | Hospitality / food / travel. Warm paper, terracotta |
| `charcoal` | Fashion / architecture. Charcoal cover, terracotta rule |
| `midnight` | Tech / startups. Indigo cover, violet rule |
| `forest` | Sustainability / health. Deep green, brass rule |
| `professional` | Short notes when theme is omitted. Blue accent, A4 |
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

- Omitting `theme` stays on professional A4. A real report sets the topic theme.
  `plain` without being asked yields the weak B&W look.
- Scanned PDFs need OCR — empty extract ≠ empty document.
- Helper CLIs use **1-based** pages.
- PDF/A is out of scope.

## Completion criteria (create)

- [ ] Theme matches the topic, and the reply says which theme was chosen
- [ ] User-named colors are in `palette` or `colors`
- [ ] Title + at least one heading, and tables/lists/callouts where content fits
- [ ] Output PDF exists; `--meta` page_count makes sense
- [ ] Source files not overwritten unless requested
