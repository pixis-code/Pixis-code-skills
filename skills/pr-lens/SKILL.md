---
name: pr-lens
description: "Draw code changes as animated architecture/data-flow SVGs with PR Lens. Use when diagramming a diff, PR, or system for comprehension. Not a review bot (self-review / github), not Mermaid wiki docs (codebase-documentation-generator), not explain-only prose (code-explainer)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos]
metadata:
  pixis:
    category: Software Development
    tags: [diagrams, pull-requests, architecture, data-flow, svg]
    related_skills: [github, code-explainer, codebase-documentation-generator, self-review]
---

# PR Lens

Author a graph JSON document (lanes, nodes, edges, flows) and render **animated SVGs** of diffs, architecture, and data flows. Comprehension layer only — no bug/risk fields; invented “findings” fields are rejected.

Adapted from Hermes `pr-lens` / [coldteadotai/pr-lens](https://github.com/coldteadotai/pr-lens) (MIT © Coldtea AI; see `LICENSE.txt`) for Pixis code beta.

## When to use

- Diagram / visualise a code change or system
- Attach an architecture or data-flow diagram to a PR
- Keywords: PR Lens, architecture diagram, data flow, visualise diff

## Do not use

| Request | Hand off to |
|---------|-------------|
| Review own diff for defects | `self-review` |
| Open PR / CI / review comments only | `github` |
| Prose explain without diagrams | `code-explainer` |
| Wiki + Mermaid from whole repo | `codebase-documentation-generator` |

## Prerequisites

- Node.js with `npx` (`npx @coldtea/pr-lens-cli@latest` — no install step)
- `gh` optional (attach diagrams to PRs; `--attach` needs gh ≥ 2.99)
- Canvas publish to prlens.dev only when the user explicitly asks

## Steps

1. Read the change: `git diff --find-renames <base>...<head>` (merge base, not tip of base branch), or read the code if not a diff.
2. Write `.pr-lens/graph.json` per `references/graph-document.md`. Read `references/example.graph.json` before the first document.
3. Validate and fix every failure (do not delete elements to “work around”):
   ```bash
   npx @coldtea/pr-lens-cli@latest validate .pr-lens/graph.json
   ```
4. Render (light theme unless asked otherwise):
   ```bash
   npx @coldtea/pr-lens-cli@latest render .pr-lens/graph.json --theme light
   ```
   Outputs land in `.pr-lens/` (gitignored by the CLI). **Do not commit** them.
5. **Canvas push — opt-in only** when the user wants a shareable link: `npx @coldtea/pr-lens-cli@latest canvas push`. Share the **view** link; treat `#w=…` edit links as secrets.
6. Attach to a PR when relevant (`gh` ≥ 2.99 `--attach`, or gist / canvas URL). Prefer the top architecture view + one data-flow. Use `comment` with `--graph .pr-lens/drawn.graph.json` and a durable `--asset-base-url`.

## Document quality (short)

- Include `unchanged` neighbours the change touches
- Lanes = mental model (runtime/tier/boundary), not folder tree
- One hero edge; add a flow only when a sequence is worth animating
- File refs for permalinks; walkthroughs for non-trivial changes (CLI ≥ 0.4.0)
- Corrections go in `.github/pr-lens.yml` (`references/config.md`), not by editing generated SVGs

## Completion criteria

Done when you can state:

1. Graph path validated successfully.
2. Render produced SVGs + `manifest.json` under `.pr-lens/`.
3. How the user can open them (local path, PR attach, or canvas view link).
4. No secrets (canvas edit links) posted unprompted.

## Smoke test

```bash
cp references/example.graph.json /tmp/prlens-smoke/ && cd /tmp/prlens-smoke
npx -y @coldtea/pr-lens-cli@latest validate example.graph.json
npx -y @coldtea/pr-lens-cli@latest render example.graph.json --theme light
```
