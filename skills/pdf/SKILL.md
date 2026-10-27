---
name: pdf
description: "Create, read, merge, fill, OCR, and edit local PDF files. Use when the user asks to merge PDFs, extract PDF tables/text, fill PDF forms, or build a PDF report. Not for PowerPoint decks (powerpoint), Google Docs (google-workspace), or Notion (notion)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [pdf, documents, forms, ocr, text-extraction, reportlab, pypdf, pdfplumber]
    category: Productivity
    related_skills: [powerpoint, grounded-citations, arxiv]
    attribution: Adapted from Nous Research hermes-agent pdf skill (MIT) — see LICENSE
---

# PDF

Create PDFs from JSON specs, build/fill AcroForm forms, extract text/tables/
metadata, merge/split/rotate/watermark/stamp, export page images, manage
metadata/attachments, and encrypt/decrypt — via `pypdf`, `reportlab`, and
`pdfplumber`. Extra playbooks:

- Scanned/OCR: `references/ocr-extraction.md` (+ `scripts/extract_pymupdf.py`,
  `scripts/extract_marker.py`)
- NL text edits inside an existing PDF: `references/nano-pdf-editing.md`
- Form field layout: `references/forms.md`

**When to use:** reports/invoices as PDF · fillable forms · extract text/tables ·
merge/split/stamp/secure PDFs · page PNGs for review/OCR.

**Do not use:** Google Drive Docs → `google-workspace`; slide decks →
`powerpoint`; Notion → `notion`; HTML-to-PDF pixel perfection (use a headless
browser instead).

## Prerequisites

```bash
python -m pip install pypdf reportlab pdfplumber
# optional rasterization:
python -m pip install pypdfium2   # or install poppler (pdftoppm)
```

Helpers print an install hint if an import is missing.

## How to run

Scripts are argparse CLIs under `scripts/` — UTF-8 JSON in/out, `--help` on each.

```bash
python scripts/pdf_create.py spec.json -o out.pdf
python scripts/pdf_make_form.py formspec.json -o form.pdf
python scripts/pdf_form_layout.py formspec.json
python scripts/pdf_read.py doc.pdf --text
python scripts/pdf_read.py doc.pdf --tables --csv-dir t/
python scripts/pdf_read.py doc.pdf --meta
python scripts/pdf_read.py form.pdf --fields
python scripts/pdf_merge.py a.pdf b.pdf -o merged.pdf
python scripts/pdf_split.py doc.pdf --pages 1-3,7 -o part.pdf
python scripts/pdf_fill_form.py form.pdf --fields-json values.json -o filled.pdf
python scripts/pdf_secure.py doc.pdf --encrypt -o enc.pdf --user-password SECRET
python scripts/pdf_watermark.py doc.pdf --stamp mark.pdf -o stamped.pdf
python scripts/pdf_stamp.py doc.pdf -o out.pdf --text "DRAFT" --x 150 --y 400
python scripts/pdf_page_image.py doc.pdf --pages 1-3 --dpi 150 --out-dir imgs/
python scripts/pdf_meta.py doc.pdf --set-meta --title "T" --author "A" -o out.pdf
```

## Procedure

1. **Inspect** — `pdf_read.py file.pdf --meta`. If encrypted, decrypt first. If
   `likely_scanned_pages`, render with `pdf_page_image.py` and follow
   `references/ocr-extraction.md` (do not report empty text as "no content").
2. **Create** — write a JSON spec (`heading`, `paragraph`, `table`, `image`,
   `pagebreak`), run `pdf_create.py`, optionally render a page PNG to verify.
3. **Extract** — `--text` / `--tables`; parse JSON (never eyeball binary PDF).
4. **Manipulate** — merge/split/rotate/watermark/stamp as needed.
5. **Forms** — lint with `pdf_form_layout.py`, build with `pdf_make_form.py`,
   fill with `pdf_fill_form.py` after listing `--fields`.
6. **Verify** before claiming success (see below).

## Pitfalls

- Scanned PDFs need OCR — empty extract ≠ empty document.
- Flattened exotic widgets may misrender — verify visually.
- `--compress` only deflates content streams (often 0–20% savings).
- Permission flags are not real security; only user-password encryption is.
- Helper CLIs use **1-based** pages; do not double-convert with 0-based APIs.
- PDF/A is out of scope for these scripts (use Ghostscript + veraPDF externally).

## Verification

- After create/merge/split: `pdf_read.py out.pdf --meta` (page_count / rotation).
- After fill: `pdf_read.py filled.pdf --fields` and compare values.
- Visual checks: `pdf_page_image.py` then open the PNGs.

## Completion criteria

- Right tool path chosen (create vs extract vs form vs OCR).
- Dependencies present or install hint shown.
- Output files exist; meta/fields/text checks match the user request.
