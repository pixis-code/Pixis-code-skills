---
name: code-refactoring
description: "Improve structure and readability without changing behavior. Use when the user asks to refactor, dedupe, or simplify working code. Not for explaining code (code-explainer), fixing bugs (debugging-assistant), or pre-commit review (self-review)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [refactor, cleanup, readability, duplication, maintainability]
    related_skills: [test-first, self-review, debugging-assistant, code-explainer]
---

# Code refactoring

Improve existing code structure **without changing intended behavior**. Cleanup and clarity only — not a bug hunt and not a rewrite.

Adapted from Hermes `simplify-code` ideas (reuse, quality, risk tiers) for a single-agent Pixis workflow — no parallel subagent fan-out and no Hermes-only tools.

## When to use

- "Refactor this large function into smaller functions"
- "Remove duplicated logic from these modules"
- "Improve readability without changing behavior"
- Simplify naming, modularity, or nesting in code that already works

## Do not use

| Request | Hand off to |
|---------|-------------|
| Explain what code does (no edits) | `code-explainer` |
| Diagnose / fix a defect or traceback | `debugging-assistant` |
| Write a failing test before any production change for a bug | `test-first` |
| Review your own diff before commit | `self-review` |
| Browser QA of a running app | `app-qa` |
| Add features or change business rules | Stop — that is not refactoring; confirm intent with the user |

## Rules

1. **Preserve behavior** — same inputs → same outputs and side effects for in-scope paths.
2. **Preserve interfaces** — public APIs, routes, DB schemas, and config keys are contracts; treat renames as high risk and do not auto-apply without explicit approval.
3. **Scope tightly** — touch only what the request requires; no unrelated module rewrites or new dependencies.
4. **Chesterton's fence** — before removing code, understand why it exists (`git blame`, tests, comments). If unclear, keep it and mark low confidence.
5. **Tests verify safety** — discover the project test command (same rules as `test-first` / `self-review`). Prefer existing tests; add or update tests only when needed to lock behavior. Do not weaken assertions to make a refactor "pass".

## Steps

1. Identify scope: named files/symbols, or the relevant diff (`git diff` / staged / user paths). If nothing is in scope, stop and ask.
2. Inspect surrounding code and existing tests for the behavior that must stay.
3. List concrete smells (duplication, long functions, deep nesting, poor names, dead locals) with file references. Skip pure style nits unless the user asked for style.
4. Plan small steps. Classify each change:
   - **SAFE** — unused imports, dead commented code, pure renames of locals; apply freely, then verify.
   - **CAREFUL** — extract helpers, flatten conditionals, dedupe with shared helpers; apply with tests after each chunk.
   - **RISKY** — public API renames, concurrency, error-handling semantics, deeper architectural moves; present and wait for approval — do not auto-apply.
5. Apply SAFE → CAREFUL. One coherent chunk at a time. Revert any chunk that breaks tests.
6. Run relevant tests (and linter/typecheck if the project has them). Report actual commands and results.
7. Summarize: what changed, what stayed the same, RISKY items skipped, remaining risks.

## If a bug appears

Stop refactoring that path. Report the defect and hand off to `debugging-assistant` (and `test-first` for a regression test). Do not fold a correctness fix into a "cleanup" silently.

## Completion criteria

Done only when you can state:

1. Scope refactored (files / symbols).
2. Behavior preserved (and how you verified — tests or explicit blocker).
3. Changes made, grouped by SAFE / CAREFUL; RISKY items left for the user.
4. No unrelated features or dependency churn.
