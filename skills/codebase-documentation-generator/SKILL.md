---
name: codebase-documentation-generator
description: "Generate wiki docs and Mermaid diagrams from a real codebase. Use when documenting architecture or producing onboarding docs. Not for Q&A explain (code-explainer), LOC metrics only (project-codebase-analyzer), or inventing components."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [documentation, wiki, mermaid, architecture, onboarding]
    related_skills: [code-explainer, project-codebase-analyzer]
---

# Codebase documentation generator

Produce **reference documentation** (what/how) from the actual repository: overview, architecture, module pages, Mermaid diagrams. Every claimed component and call must exist in source — never fabricate.

Adapted from Hermes `code-wiki` for Pixis. Templates live in `templates/`. Default output is outside the repo unless the user asks to write into `docs/wiki/`.

## When to use

- "Document this codebase" / "generate a wiki" / "architecture diagrams"
- Onboarding reference for an unfamiliar repo
- Stable markdown + Mermaid artifact for GitHub rendering

## Do not use

| Request | Hand off to |
|---------|-------------|
| Explain one function/flow interactively | `code-explainer` |
| LOC / language metrics only | `project-codebase-analyzer` |
| Strategic product "why" narrative | Ask user; not this skill's job |
| Active debugging session Q&A | `debugging-assistant` / answer briefly |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | `git` | SHA tracking / shallow clone |
| **Bundled** | `templates/` | From Hermes code-wiki |
| **Optional** | `pygount` | Language stats; see `project-codebase-analyzer` |

**Production:** git is not auto-installed; pygount install may be blocked.

```bash
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes --with-pygount   # only if you want metrics
```

## Output location

```bash
REPO_NAME=$(basename "$PWD")
OUTPUT_DIR="${PIXIS_WIKI_DIR:-$HOME/.pixis/wikis}/$REPO_NAME"
mkdir -p "$OUTPUT_DIR/modules" "$OUTPUT_DIR/diagrams"
```

Only write into the project (`docs/wiki/`) when the user explicitly requests it.

## Procedure

### 1. Resolve target

Local path/cwd, or `git clone --depth 50 <url>` to a temp dir. Record `REPO_SHA=$(git rev-parse HEAD 2>/dev/null || echo uncommitted)`.

### 2. Scan structure

Shallow tree (max depth 3), skip `node_modules`, venvs, `dist`, `build`, `.git`. Read manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) and README. Optional pygount summary.

### 3. Pick modules (cap 8–10)

Heuristics: Python packages; `src/` subdirs; crates; Go packages; otherwise source-bearing top-level dirs. Prioritize by import centrality, LOC, README mentions. On large repos, confirm the list with the user first.

### 4–10. Write artifacts

Use templates in `templates/` as skeletons. Fill only from evidence:

| File | Content |
|------|---------|
| `README.md` | Overview, concepts, entry points, module map |
| `architecture.md` | Shape, components, Mermaid `flowchart`, data flow |
| `modules/<name>.md` | Responsibilities, key files, public API, deps, gotchas |
| `diagrams/class-diagram.md` | Mermaid `classDiagram` (or skip for non-OOP) |
| `diagrams/sequences.md` | 2–4 real workflows as `sequenceDiagram` |
| `getting-started.md` | Prereqs, install, first run from README/manifests |
| `api.md` | Only if library/API server with a clear public surface |
| `.codewiki-state.json` | repo name, path, SHA, timestamp, modules list |

Generator field in state file: `pixis codebase-documentation-generator v1.0.0`.

**Mermaid rules:** ≤ ~20 nodes per diagram; quote labels with `/`; no fabricated participants; class generics as `List~T~`.

### 11. Report paths

List every file written and remind the user if a temp clone can be deleted.

## Scope control

- Max depth 3 on first scan; ≤ 10 modules unless user expands  
- Skip vendor/generated/minified/test-as-product  
- For huge repos, estimate cost and confirm before exhaustive coverage  

## Re-run

If `.codewiki-state.json` exists: same SHA → ask regenerate or skip; different SHA → offer full regen (incremental optional).

## Pitfalls

- Fabricating components (largest failure mode)  
- Generic AI prose / restating code as empty paraphrase  
- Mermaid > 50 nodes; documenting vendored code  
- Writing into the repo without permission  

## Verification

1. Mermaid fences balanced in architecture + diagrams  
2. Expected files exist under `$OUTPUT_DIR`  
3. Module count matches the committed list  
4. Spot-check 2–3 source links resolve to real files  

## Completion criteria

1. Wiki written from inspected source only.  
2. Output path reported; state file written.  
3. No invented modules/APIs.  
4. Metrics-only requests redirected to `project-codebase-analyzer`; Q&A to `code-explainer`.
