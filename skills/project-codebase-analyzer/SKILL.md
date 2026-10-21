---
name: project-codebase-analyzer
description: "Analyze project size, languages, and composition (pygount + structure scan). Use when inspecting an existing repo's makeup or LOC. Not for explaining how code works (code-explainer), generating a wiki (codebase-documentation-generator), or fixing bugs (debugging-assistant)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [LOC, codebase, metrics, pygount, languages, structure]
    related_skills: [code-explainer, codebase-documentation-generator]
---

# Project codebase analyzer

Measure and summarize an existing project: languages, LOC, file counts, code-vs-comment ratios, and high-level layout. Prefer evidence from tools and manifests — do not invent frameworks or modules.

Adapted from Hermes `codebase-inspection` for Pixis, expanded with a light structure/framework discovery pass.

## When to use

- "How big is this repo?" / LOC / language breakdown
- "What languages and frameworks does this project use?"
- Onboarding scan before deeper explanation or documentation
- Code-vs-comment ratios or composition questions

## Do not use

| Request | Hand off to |
|---------|-------------|
| Explain how a feature/flow works | `code-explainer` |
| Generate durable wiki/architecture docs | `codebase-documentation-generator` |
| Fix bugs or tracebacks | `debugging-assistant` |
| Structural find/replace by AST | `structural-code-search` |
| Feasibility experiment before build | `technical-feasibility-investigator` |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** (metrics) | `pygount` | LOC/language summary |
| **Required** (always) | shell + `find`/`ls` | Structure scan works without pygount |
| **Optional** | project manifests | Read for stack detection |

**Production:** do not assume pip install is allowed. Prefer `--check-only` first.

```bash
# From this skill directory — skip install when already present
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes          # install pygount only if missing
```

If pygount stays unavailable, still run the structure/manifest scan and report the metrics blocker.

## Steps

### 1. Resolve the target

Use the given path or the current workspace root. Confirm it is a project (has source or a VCS root).

### 2. Structure and framework discovery

Scan shallow layout (skip noise dirs). Identify stack from real manifests:

| Signal | Likely stack |
|--------|----------------|
| `pyproject.toml` / `requirements.txt` / `manage.py` | Python / Django / etc. |
| `package.json` / `pnpm-lock.yaml` | Node |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | JVM |
| `docker-compose.yml` | Multi-service |

Read README and top-level configs. State only what files prove.

```bash
find . -type d \
  -not -path '*/\.*' \
  -not -path '*/node_modules*' \
  -not -path '*/venv*' \
  -not -path '*/.venv*' \
  -not -path '*/__pycache__*' \
  -not -path '*/dist*' \
  -not -path '*/build*' \
  -maxdepth 3 | sort
```

### 3. Metrics with pygount

**Always** pass `--folders-to-skip` or large dependency trees hang.

```bash
# Catch-all
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info,vendor,third_party,target,coverage" \
  .

# Language filter
pygount --suffix=py --format=summary .
pygount --suffix=py,yaml,yml --format=summary .

# JSON for scripting
pygount --format=json --folders-to-skip=".git,node_modules,venv,.venv" .
```

Project-type skips:

- Python: `.git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache`
- JS/TS: `.git,node_modules,dist,build,.next,.cache,.turbo,coverage`

### 4. Interpret

Summary columns: Language, Files, Code, Comment, %.

Pseudo-languages: `__empty__`, `__binary__`, `__generated__`, `__duplicate__`, `__unknown__`.

Notes:

- Markdown often shows 0 "code" lines (classified as comments) — expected.
- JSON line counts may be conservative; use `wc -l` if exact JSON LOC matters.
- Large monorepos: prefer `--suffix` per language.

## Report format

1. Project path and detected stack (with file evidence).
2. Top-level layout (key dirs only).
3. pygount summary table (or blocker).
4. Notable composition facts (dominant language, generated/vendor share).
5. Suggested next skill if the user wants depth (`code-explainer` or `codebase-documentation-generator`).

## Completion criteria

- Structure and stack claims cite real files.
- Metrics command and output reported (or explicit install/env blocker).
- No invented modules; no production code changes.
