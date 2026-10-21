# Citation Formats by Output Type

`sources.py render --style ...` produces the block; this says where it goes.

- **Markdown/chat** — inline `[n]`; end block `## Sources` / `[1] url — title`.
  `--style plain` → bare `Sources:` for chat.
- **PDF/LaTeX** — `--style footnotes` → `\footnote{}` at first use, or
  numeric + endnotes. Bibliography: `--style bibtex` → `@misc{source<N>,...}`.
  Never mix `[n]` with `\cite{}`+BibTeX.
- **Word (.docx)** — real footnotes, not inline brackets. Ledger ids = footnote
  numbers, so `verify` still runs on the markdown source.
- **Slides (.pptx)** — inline `[n]` in bullets, one "Sources" slide
  (`--style plain`). No raw URLs in body bullets.
- **Spreadsheets (.xlsx)** — `source` column with the id + a `Sources` sheet
  (`--style plain`). No URLs in data cells.
- **Wiki/multi-page** — one shared ledger, per-page Sources block. `[7]` =
  same page everywhere; don't reset mid-build.
- **Code/config** — no citations in code; provenance goes in the commit
  message, PR body, or doc header.
