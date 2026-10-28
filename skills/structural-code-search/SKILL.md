---
name: structural-code-search
description: "AST-aware search and safe rewrites via ast-grep. Use for structural find/codemod across a codebase. Not for text/regex search alone, behavior-preserving cleanup without AST (code-refactoring), or explaining code (code-explainer)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [ast-grep, codemod, structural-search, refactor, tree-sitter]
    related_skills: [code-refactoring, debugging-assistant]
---

# Structural code search

Use **ast-grep** (`sg` / `ast-grep`) when the question depends on **code shape** (AST), not raw text. Prefer the helper at `scripts/ast_grep_helper.py`. Always dry-run rewrites before `--apply`.

Adapted from Hermes `ast-grep` (upstream: code-yeongyu/ast-grep-skill, MIT). Supporting files live in this skill directory.

## When to use

- Find every function/call/import matching a structural pattern
- Codemod: rewrite `console.log($MSG)` → `logger.info($MSG)`, strip `as any`, migrate `Optional[X]` → `X | None`, etc.
- Empty catch blocks, require→import migrations, YAML lint rules via `sg scan`
- Bulk pattern edits across many files

## Do not use

| Request | Hand off to |
|---------|-------------|
| Text/regex/string/content/file-name search | Plain `rg` / editor search |
| Small manual readability cleanup | `code-refactoring` |
| Explain what code does | `code-explainer` |
| Fix a bug (not a structural rewrite) | `debugging-assistant` |

Ask: does the answer depend on the **syntax tree** or on **bytes**? Tree → this skill. Bytes → `rg`.

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | `python3` | Runs `scripts/ast_grep_helper.py` |
| **Required** | `ast-grep` / `sg` binary | Search & rewrite engine |
| **Bundled** | `references/`, `install.sh`, `install.ps1` | From Hermes; keep as-is |

**Production:** binary download may be blocked; check first, install only if missing.

```bash
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes          # prefers install.sh --method=github if missing
# Equivalents: bash install.sh --method=github
#              python3 scripts/ast_grep_helper.py doctor|install
```

On Linux prefer `ast-grep` if `sg` collides with util-linux `sg`. The helper resolves this.

## Three invariants

1. **Not regex** — wildcards are `$VAR` (one node) and `$$$` (zero+ nodes). `\w`, `.*`, `|` are wrong; validate first.
2. **Patterns must parse** as code for that language (`def $FN($$$)` not `def $FN($$$):`).
3. **`--json` and `--update-all` are mutually exclusive** — preview then apply in two passes (helper `replace --apply` does this).

## Helper (default entry point)

Paths are relative to this skill directory (`skills/structural-code-search/`).

```bash
# Search
python scripts/ast_grep_helper.py search 'console.log($MSG)' --lang ts src/

# Rewrite dry-run (default)
python scripts/ast_grep_helper.py replace 'console.log($MSG)' 'logger.info($MSG)' --lang ts src/

# Apply after inspecting preview
python scripts/ast_grep_helper.py replace 'console.log($MSG)' 'logger.info($MSG)' --lang ts src/ --apply

# Validate pattern offline
python scripts/ast_grep_helper.py validate 'console.log($MSG)' --lang ts

# YAML rules
python scripts/ast_grep_helper.py scan src/
python scripts/ast_grep_helper.py scan -r rules/no-console.yml src/
```

Always **single-quote** patterns in shell so `$VAR` is not expanded.

## Direct `sg` (when needed)

```bash
sg run -p 'console.log($MSG)' --lang ts src/
sg run -p 'console.log($MSG)' -r 'logger.info($MSG)' --lang ts --json=compact src/
sg run -p 'console.log($MSG)' -r 'logger.info($MSG)' --lang ts --update-all src/
sg run -p '<pattern>' --lang <lang> --debug-query=ast --stdin <<< '<sample>'
```

## Safe rewrite workflow

1. `helper search` — confirm matches  
2. `helper replace` without `--apply` — inspect blast radius (files + matches)  
3. Refine if wrong  
4. `helper replace ... --apply`  
5. `git diff --stat` before commit  

Never apply a rewrite you have not dry-run.

## Zero matches checklist

1. `helper validate`  
2. Correct `--lang` (`tsx` vs `ts`)  
3. `--debug-query=ast` on pattern and sample  
4. Inspect target CST; playground: https://ast-grep.github.io/playground.html  

## References (read as needed)

| File | Topic |
|------|--------|
| `references/recipes.md` | Copy-paste patterns by language |
| `references/patterns.md` | Meta-variables, strictness |
| `references/pitfalls.md` | Failure modes |
| `references/cli.md` | Full CLI |
| `references/yaml-rules.md` | Rule schema |
| `references/sgconfig.md` | Project config |
| `references/install.md` | Install fallbacks |

## Completion criteria

1. Tool choice justified (AST vs text).  
2. Patterns validated; search/replace commands and counts reported.  
3. Rewrites dry-run before apply; diff reviewed.  
4. Tests run when behavior might change (`test-first` / project suite).
