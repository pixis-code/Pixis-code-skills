---
name: xlsx
description: "Create, read, edit, and recalculate Excel .xlsx workbooks and convert to/from CSV (styled sheets, formulas, charts, tables, validation, conditional formatting, reference-aware row/column inserts). Use when the user wants a spreadsheet built or changed, data dumped from a workbook, formulas listed or recalculated, or a CSV turned into xlsx. Not for legacy .xls (convert first), Word (docx), PDFs (pdf), or slides (powerpoint)."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Productivity
    tags: [excel, spreadsheet, xlsx, csv, openpyxl, productivity]
    related_skills: [docx, pdf, powerpoint]
---

# Xlsx

openpyxl CLIs in `scripts/` (argparse, `--help`, JSON output, explicit UTF-8). Setup: Python 3.10+, `pip install openpyxl`; LibreOffice (`soffice`) optional for recalculation/PDF. Legacy `.xls`: convert first with `soffice --headless --convert-to xlsx old.xls`.

## When to use

Build styled multi-sheet reports (formats, merges, freeze panes, filters, conditional formatting, charts, dropdowns, native tables, names, hyperlinks, notes, protection); dump or inspect workbooks; edit cells, rows, columns, sheets; recalculate formulas; convert CSV <-> xlsx.

## Commands

Run from `scripts/`:

| Task | Command |
|---|---|
| Create from spec | `python xlsx_create.py spec.json out.xlsx` |
| Inventory / data | `xlsx_read.py f.xlsx --sheets`, `--json --sheet S`, `--csv --out d.csv` |
| Formulas + cached values | `xlsx_read.py f.xlsx --formulas` (also `--notes`, `--names`) |
| Set cell / formula | `xlsx_edit.py f.xlsx --sheet S --set "A1==SUM(B:B)"` |
| Append row | `xlsx_edit.py f.xlsx --append '[1,"x",true]'` |
| Insert rows, refs NOT shifted | `xlsx_edit.py f.xlsx --insert-rows 3:2` |
| Insert/delete, refs shifted | `xlsx_restructure.py f.xlsx --insert-rows 3:2` / `--delete-cols B` |
| Tables | `xlsx_edit.py f.xlsx --add-table Sales:A1:C9`, `--table-append 'Sales=["West",5]'`, `--list-tables` |
| Names | `--define-name "Rates='Data'!$B$2:$B$9"`, `--delete-name Rates` |
| Link / note | `--hyperlink "A1=https://example.com\|Docs"`, `--note "B2=Check this\|Reviewer"` |
| Protect | `--protect pw --unlock B2:B9` (not security) |
| Sheets | `--copy-sheet Src:New`, `--rename-sheet Old:New` |
| Recalc | `--recalc` (flag recompute on open) or `xlsx_recalc.py f.xlsx` (LibreOffice) |
| CSV | `csv_to_xlsx.py in.csv out.xlsx --encoding utf-8` / `xlsx_to_csv.py f.xlsx out.csv --sheet S` |

## Notes

- **Spec** (schema in `xlsx_create.py --help`): per sheet `rows` (scalars or styled cells), `cells`, `column_widths`, `row_heights`, `merges`, `freeze_panes`, `autofilter`, `conditional_formats` (cell_is, color scales), `charts` (bar/line/pie), `validations`, `tables`, `protection`; workbook `defined_names`; cells take `hyperlink`/`note`. Dates: `{"value": "2026-01-31", "type": "date"}`. Formats are Excel strings (`"$#,##0.00"`, `"0.0%"`, `"yyyy-mm-dd"`).
- **Formulas:** `"formula": "SUM(B2:B9)"` in specs. Add `"full_calc_on_load": true` (spec) or `--recalc` (editor) so Excel/LibreOffice recompute on open.
- **Cached values** exist only if a real spreadsheet app last saved the file (else `null`). Run `xlsx_recalc.py` (without `soffice` it prints `{"recalculated": false, ...}` and exits 0), then reload with `--data-only`.
- **Edit order:** renames/copies, then row/column changes, then `--set`/`--append`. Edits in place unless `--out`; copy first to keep the original.
- **Restructure:** use `xlsx_restructure.py` when formulas, merges, tables, or filters exist. It rewrites refs on all sheets and shifts merges, filters, freeze panes, validations, conditional-format ranges, tables, names, and dimensions, then prints a report with `not_shifted`. One operation per run. Details: `references/restructuring.md`.
- **CSV:** infers int/float/bool/ISO date, styles the header; exports ISO dates and blanks. Use `--encoding` (`utf-8-sig`, `cp1252`) and `--delimiter ';'` for European files (decimal commas like `"12,5"` stay strings).
- **LibreOffice:** `soffice --headless --convert-to pdf report.xlsx --outdir out/`. CSV conversion covers the first sheet only; use `xlsx_to_csv.py --sheet` for others.

## Pitfalls

- openpyxl never calculates; formula results need `data_only=True` on a previously app-saved file.
- `xlsx_edit.py` inserts/deletes don't shift refs; even `xlsx_restructure.py` can't move chart anchors, images, or conditional-format rule formulas. Check `not_shifted`.
- Protection is not security: it's a removable hint, not encryption.
- Saving a `data_only=True` workbook permanently replaces formulas with values.
- Load + save drops charts/images; re-add charts or avoid re-saving charted files.
- Dates are `datetime` in openpyxl; dumps emit ISO strings.
- Sheet names: max 31 chars, none of `[ ] : * ? / \`.

## Completion criteria

- Created: `--sheets` matches names, sizes, merges, chart counts; `--json` matches source data.
- Edited: re-dump touched range; formulas appear in `--formulas` and `--recalc` was applied.
- Restructured: read the report, then re-run `--formulas` and `--sheets`.
- Optional: convert to PDF and inspect.
