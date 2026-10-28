# Reference-aware restructuring (`xlsx_restructure.py`)

Performs one row/column insert or delete and rewrites everything that points at the moved cells. This file lists the exact rules and the limits.

## What gets rewritten

| Artifact | Scope | Behavior |
|---|---|---|
| Formula references | all sheets | A1 refs into the edited sheet shift; refs into a fully deleted region become `#REF!` |
| Merged ranges | edited sheet | shifted; grown if they span the insertion point; dropped (`to: null` in the report) if fully deleted |
| Autofilter | edited sheet | shifted/grown like a range |
| Freeze panes | edited sheet | anchor cell shifted, never past the pane's own minimum row/col |
| Data validations | edited sheet | each sqref range shifted; deleted ranges removed |
| Conditional formats | edited sheet | applied range (sqref) shifted |
| Native tables | edited sheet | table `ref` shifted/grown |
| Defined names | workbook scope | refs into the edited sheet rewritten |
| Row heights / column widths | edited sheet | dimension keys re-indexed |

## Reference syntax handled

- Relative/absolute mixes (`B2`, `$B2`, `B$2`, `$B$2`); `$` flags survive the shift.
- Ranges like `B2:D9`, including partly absolute endpoints.
- Cross-sheet refs: `Data!B2`, `'My Sheet'!$A$1:$C$9` (quoted names may contain doubled `''`). Only refs qualified with the edited sheet are touched; unqualified refs belong to the formula's own sheet.
- String literals in formulas (`"See B2"`) are never rewritten.
- Function names that look like cells (`LOG10(...)`) are skipped, since a reference is never followed by `(`.
- Whole-row/column refs (`B:B`, `2:2`) are left alone; they stay valid across inserts within the span.

## Shift rules

**Insert N at index i:** every coordinate >= i moves +N. Range endpoints move independently, so a range spanning i grows by N.

**Delete N at index i:** coordinates before i stay; those after the block move -N; a single cell inside the block becomes `#REF!`; a range partly in the block is clamped (as Excel does); a range wholly inside becomes `#REF!` in formulas, or is removed for merges/validations.

## Not shifted

- **Chart anchors and plotted ranges.** openpyxl doesn't reliably round-trip charts. Recreate them if their data moved.
- **Images/drawings**, same reason.
- **Conditional-format rule formulas.** Only the applied range moves; formulas inside `cell_is`/`expression` rules (e.g. `$B1>100`) are untouched, so review them.
- **Sheet-local defined names**, and names in R1C1 or using union/intersection operators, are rewritten only if they parse as plain A1 refs.
- **Structured table refs** (`Table1[Sales]`) follow the table and are left alone.

Each run prints a JSON report of changed formulas, merges, tables, names, and ranges, plus a fixed `not_shifted` list covering the items above. Read it after every structural edit.

## One operation per run

Pass exactly one of `--insert-rows`, `--delete-rows`, `--insert-cols`, `--delete-cols`, as `IDX[:N]` (columns accept letters). For several changes, run the script repeatedly; combining shifts in one pass is where spreadsheet tools tend to corrupt references.
