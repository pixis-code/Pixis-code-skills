---
name: sdlc-review
description: "Read-only review of an implementation against its requirements: correctness, code quality, edge cases, test coverage, and regressions. Produce a severity-ranked review report with file references and recommended fixes — do not modify files. Use when the user asks to review a feature/login/register/flow against requirements or acceptance criteria, or to independently verify a handoff. Not for fixing bugs yourself (debugging-assistant), your own pre-commit diff that you will edit (self-review), explaining how code works (code-explainer), or opening/triaging PRs via gh (github)."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Developer Workflow
    tags: [review, requirements, quality, correctness, handoff, report]
    related_skills: [self-review, github, code-explainer, debugging-assistant, test-first, app-qa]
---

# SDLC review

Independently review an implementation **against its requirements** (or a handoff’s acceptance criteria). Deliver a clear, severity-ranked report with file references and recommended fixes. **Do not modify any files** unless the user explicitly asks you to apply fixes after the report.

Adapted from Hermes `sdlc-review` (MIT) for Pixis code beta.

## When to use

- “Review the login/register (or any feature) implementation against its requirements”
- Check code quality, correctness, edge cases, test coverage, potential regressions
- Produce a review report with prioritized issues and recommended fixes (no edits)
- Independently verify a finished handoff before it can close (approve / request changes / escalate)

## Do not use

| Request | Hand off to |
|---------|-------------|
| Review **your** uncommitted diff and **fix** it before commit | `self-review` |
| Explain how the feature works (no quality verdict) | `code-explainer` |
| Open/triage PRs and CI as the author | `github` |
| Challenge a plan before any code exists | `technical-plan-challenger` |
| “Fix the bugs you found” as the next ask | `debugging-assistant` / `test-first` after the report |
| Browser-only UX walkthrough | `app-qa` (may feed this review) |

## Steps

1. **Gather the contract.** Find requirements / acceptance criteria from the user message, ticket, PR, README, or tests. If none are stated, infer a short checklist from the feature name and existing tests — then state those assumptions in the report.
2. **Locate the implementation.** Search and read the real login/register (or named feature) paths: handlers, UI, validation, auth, persistence, and related tests. Cite concrete files.
3. **Review against the contract** (read-only):
   - Correctness vs each requirement
   - Code quality and project conventions
   - Edge cases and error handling
   - Test coverage gaps (missing cases, weak assertions)
   - Likely regressions / blast radius on callers
4. If a handoff record exists, also apply a **lens** by round:
   - Round 1 — Artifact: read the deliverable cold before the summary
   - Round 2 — Execution: run focused tests/build when practical
   - Round 3+ — Contract: strict audit + prior requested changes landed
5. **Write the report** (do not edit source):
   - Summary (scope + overall verdict)
   - Issues ranked by severity (`critical` / `important` / `minor`)
   - Each issue: what / where (file + symbol or line range) / why it matters / recommended fix
   - What looked solid (brief)
   - Optional handoff verdict when applicable: approve | request changes | escalate
6. Stop without modifying files. If the user then wants fixes applied, point to `debugging-assistant` / `test-first`.

## Report shape

```text
## Review: <feature>
Verdict: <approve | request changes | escalate | n/a — report only>
Assumptions: <if requirements were inferred>

### Critical
1. <title> — `path` (`symbol` or lines)
   Problem: …
   Recommend: …

### Important
…

### Minor
…

### Coverage / regressions
…

### What looks good
…
```

## Pitfalls

- Rubber-stamping without reading the real code
- Editing files during a “do not modify” review
- Vague “needs work” without file refs or a fix direction
- Blocking on style nits when behavior and repo standards pass
- Turning the review into a full rewrite plan

## Completion criteria

Done when you can state:

1. What was reviewed (feature + requirement source).
2. Every major requirement mapped to evidence or an explicit gap.
3. A severity-ranked issue list with file references and recommended fixes.
4. No source files were modified.
5. If it was a handoff close-out: exactly one verdict with concrete evidence.
