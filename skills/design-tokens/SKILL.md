---
name: design-tokens
description: "Extract app colors/spacing into one theme file; author, lint, diff, and export DESIGN.md. Not for page redesign — that is pixis:site-redesign-ui-ux."
version: 2.2.0
author: Hermes Agent (adapted for Pixis)
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Frontend
    tags: [design-tokens, design-md, css-variables, tailwind, theme]
---

# Design tokens

Token and theme work only. Do not redesign pages, layouts, or components. That is `pixis:site-redesign-ui-ux`.

Supports: (1) extract named colours/spacing into one theme file, then integrate into CSS variables / Tailwind; (2) author, validate, compare, and export Google DESIGN.md via `@google/design.md`.

## Completion criteria

Done only when all are true:

1. One theme file holds **named** colour/spacing variables taken from the app (no invented values or invented token names).
2. Every `var(--…)` you added resolves to a variable defined in that theme file (or you explicitly document an existing external dependency).
3. Existing theme files, CSS, and Tailwind config were inspected first and not silently overwritten or stripped.
4. Incomplete extraction (truncation, unreadable files, unnamed literals) was reported honestly.
5. You stopped without restyling pages or components.

## Job A — extract, then integrate (default for “pull the colours and spacing…”)

Extraction and Tailwind integration are **separate**. The script only extracts. You integrate.

### A1 — Extract (once)

1. Inspect existing token/theme files before writing. Look for `DESIGN.md`, `theme*.css`, `tokens*.css`, `tokens.json`, `tailwind.theme.json`, `:root` / `@theme`, and `tailwind.config.*`. Prefer the file the project already loads.
2. Detect the real Tailwind major version from `package.json` (`tailwindcss` / `@tailwindcss/*`). v4 signals: `@import "tailwindcss"`, `@theme`. v3 signals: `tailwind.config.*`, `@tailwind base`. Do not guess.
3. Run the extractor from the app root (resolve `<skill-dir>` to this skill’s folder):

   ```bash
   python3 <skill-dir>/scripts/extract-tokens.py --root . --out <theme-path> --json-out <summary.json>
   ```

   Put `<summary.json>` in the project or the process temp dir (Python: `tempfile.gettempdir()`, not a hard-coded `/tmp`).  
   Prefer an existing theme path from step 1 for `--out` only if you intend to replace it after inspection. Otherwise use `theme.tokens.css`.  
   The script **refuses to overwrite** an existing `--out` unless you pass `--force` after reading that file. It never modifies `tailwind.config.*`.
4. Read the JSON summary once. Do **not** run extraction again to “finish” the theme.
   - `success: false` / no `theme_file` → stop; report the error. Do not invent tokens.
   - `unnamed_colors` / `unnamed_spacing` → list for review only. Do not promote them to tokens unless the user names them.
   - `complete: false` / `incomplete_files` → report truncation or read errors; keep any theme that was written from named tokens found so far.
   - Tailwind `theme.extend` / CSS-in-JS colour maps in `tailwind.config.*` are **not** auto-parsed as named tokens — review those files manually.
5. Optional check: `python3 <skill-dir>/scripts/extract-tokens.py --self-test`

### A2 — Integrate (only after a successful extract)

6. Wire the extracted variables into the app **without** rewriting the whole config:
   - **CSS:** Import or register the theme file where global CSS already loads. Do not paste a second copy of the same tokens into another file.
   - **Tailwind v3:** Merge into existing `theme.extend` keys (e.g. `colors`, `spacing`). Add only entries that point at `var(--existing-name)`. Do not delete unrelated `theme.extend` keys or replace the whole `theme` object.
   - **Tailwind v4:** Merge into the project’s existing `@theme` / `@theme inline` block, or add one only if none exists. Map utilities to `var(--…)` using the **same** names written in the theme file. Do not append a duplicate `@theme` block.
7. Confirm every new `var(--…)` resolves to a name in the theme file (or document an external dependency). Confirm you did not invent colours, spacing scales, or semantic names.
8. Stop. Hand page/component redesign to `pixis:site-redesign-ui-ux`.

## Job B — DESIGN.md (when asked for DESIGN.md / lint / diff / export)

DESIGN.md is Google’s token spec (`google-labs-code/design.md`). CLI: `npx -y @google/design.md` (Windows: `npx -y -p @google/design.md designmd …`).

1. Author or update `DESIGN.md` from **existing** brand/style sources when present. Include at least `name:` and `colors:`. Prefer `{colors.primary}` in `components:`. Quote hex and negative dimensions.
2. Validate: `npx -y @google/design.md lint DESIGN.md`
3. Compare: `npx -y @google/design.md diff DESIGN.md DESIGN-v2.md`
4. Export as needed:
   - Tailwind v3 JSON: `npx -y @google/design.md export --format json-tailwind DESIGN.md`
   - Tailwind v4 CSS `@theme`: `npx -y @google/design.md export --format css-tailwind DESIGN.md`
   - DTCG JSON: `npx -y @google/design.md export --format dtcg DESIGN.md`
5. If the user also wants the live app theme updated, follow Job A. Exports must not invent values the app does not use.

## Script notes

`scripts/extract-tokens.py`:

- Writes **named** CSS variables only (`--color-*`, `--bg-*`, `--space-*`, etc. found in sources).
- Puts unnamed literals in the JSON summary for review — never as fake tokens (`--swatch-*`, `--space-14px`).
- Does **not** append `@theme` or edit Tailwind config (integration is Job A2).
- Skips its own output / `*.tokens.css` / generated marker files on discovery.
- Streams large files, caps bytes per file, continues on other sources, reports `incomplete_files`.
- Exit codes: `0` success, `1` no sources/tokens, `2` bad root, `3` refused overwrite, `4` unresolved `var()` in generated CSS.
