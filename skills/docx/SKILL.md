---
name: docx
description: "Create, read, edit, fill templates in, and review Word .docx files (text, tables, images, headers/footers, tracked changes, comments, TOC, page numbers). Use when the user wants a .docx made or changed, a {{token}} template filled, revisions accepted/rejected, comments read or added, or a corrupt .docx triaged. Not for PDFs (pdf), spreadsheets (xlsx), slides (powerpoint), legacy .doc/.odt, or pixel-exact layout."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Productivity
    tags: [word, docx, documents, office, templates, revisions, comments]
    related_skills: [pdf, xlsx, powerpoint]
---

# Docx

Python-docx CLIs in `scripts/` (all print JSON, support `--help`). Setup: Python 3.10+, `pip install python-docx`. Cannot render pages (PDF needs LibreOffice) or edit legacy `.doc`.

## When to use

Generate Word reports/letters/contracts; extract text, outline, styles, or images; edit an existing file; fill `{{placeholder}}` templates; review tracked changes and comments; triage a broken `.docx`. Not for `.doc`, `.odt`, PDFs, or visual layout.

## Commands

| Task | Command |
| --- | --- |
| Create from JSON spec | `python scripts/docx_create.py spec.json out.docx` |
| Text (body, tables, headers/footers) | `docx_read.py f.docx --text` |
| Outline / styles / revisions | `docx_read.py f.docx --structure` / `--styles` / `--revisions` |
| Extract images | `docx_read.py f.docx --images outdir/` |
| Find/replace (keeps formatting) | `docx_edit.py replace f.docx --find A --replace B -o out.docx` |
| Table cell | `docx_edit.py set-cell f.docx --table 0 --row 1 --col 2 --text X` |
| Insert / delete / style paragraph | `docx_edit.py insert\|delete\|style f.docx --index N [--text X] [--style S]` |
| Merge same-format runs | `docx_edit.py normalize f.docx -o out.docx` |
| TOC / "Page X of Y" | `docx_edit.py toc f.docx --index N` / `page-numbers f.docx` |
| Fill tokens | `docx_template.py tpl.docx values.json out.docx --strict` |
| Revisions | `docx_revisions.py list\|accept-all\|reject-all f.docx`, or `accept\|reject --id N` |
| Comments | `docx_comments.py list f.docx`, `add --target "phrase" --text "note" --author You`, `delete --id 0` |
| Health check | `docx_validate.py f.docx` (exit 1 on errors) |

## Notes

- **Spec** keys: `page` (mm sizes/margins), `header`, `footer`, `footer_page_numbers`, `styles` (font, size, bold/italic, hex `color`), `blocks`: `heading` (1-9), `paragraph` (`text` or `runs` with bold/italic/underline), `bullet_list`, `numbered_list`, `table` (`header`, `rows`, `style`), `image` (`path`, `width_mm`), `toc`, `page_break`. Full format is in the `docx_create.py` docstring.
- **Read:** one mode flag per call.
- **Edit:** indices follow `--structure`/`--text` body order; `-o` keeps the original, otherwise edits in place; `--body-only` skips headers/footers. Run `normalize` first on heavily Word-edited files.
- **Revisions:** accept keeps insertions and drops deletions; reject does the reverse. XML details: `references/revisions-and-comments.md`.
- **Comments:** `add` anchors to the first occurrence of the phrase; `delete` leaves document text intact.
- **Templates:** output lists `filled` and `unfilled_tokens`; `--strict` fails if any remain.
- **PDF:** if `command -v soffice || command -v libreoffice` works, run `soffice --headless --convert-to pdf --outdir outdir/ file.docx`; otherwise tell the user conversion is unavailable.

## Pitfalls

- Split runs: a multi-run match collapses and takes the first run's formatting; `normalize` first.
- Only run-level insertions/deletions are auto-resolved; paragraph-mark, table-row, format-change, and move revisions are detected but need Word.
- Comment replies/resolved state are ignored; added comments are top-level.
- TOC and page numbers are field codes; placeholders show until Word/LibreOffice updates fields.
- `docx_validate.py` is a health check (zip, parts, relationships, image bytes, styles), not XSD validation.
- Unknown style names raise `KeyError`; built-ins (`Heading 1`, `List Bullet`, `List Number`, `Table Grid`) exist, custom ones must be declared in the spec.
- Separate `List Number` lists may not restart numbering.
- `set-cell` resets that cell's run formatting.
- Use explicit UTF-8 for JSON files. Never unzip-and-sed `document.xml`; edit through the scripts only.

## Completion criteria

- Re-read output (`--text`) shows new strings and no old ones; `--structure`/`--styles` match intent.
- After accept/reject, `docx_revisions.py list` is `[]` (or only intended ids); after comment changes, text is unchanged.
- `docx_validate.py` exits 0 with `"ok": true`; templates have `unfilled_tokens == []`.
