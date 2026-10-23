---
name: subagent-driven-development
description: "Execute an implementation plan with one fresh subagent per task and two-stage review (spec then quality). Use when a multi-task plan should be built task-by-task with independent review between tasks. Not for single-file fixes (debugging-assistant), plan grilling only (technical-plan-challenger), or own-diff pre-commit (self-review)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [subagent, delegation, plan-execution, two-stage-review, workflow]
    related_skills: [test-first, self-review, technical-plan-challenger, debugging-assistant]
---

# Subagent-driven development

Execute an implementation plan by dispatching a **fresh subagent per task**, then running **two-stage review** (spec compliance → code quality) before the next task.

Adapted from Hermes `subagent-driven-development` (MIT; obra/superpowers lineage) for Pixis code beta. Spawn subagents with the host’s Task / subagent tools — not a Hermes-only delegation API.

**Core principle:** Fresh context per task + spec review before quality review = fewer compounded defects.

## When to use

- You have a multi-task implementation plan (from the user or after `technical-plan-challenger`)
- Tasks are mostly independent (different files or clear boundaries)
- Spec compliance and quality matter between tasks

## Do not use

| Request | Hand off to |
|---------|-------------|
| Grill / stress-test a plan before coding | `technical-plan-challenger` |
| One bug / traceback | `debugging-assistant` (then `test-first` if needed) |
| Review only your own unfinished diff | `self-review` |
| Colleague PR / CI via `gh` | `github` |
| Tiny one-step change | Just implement (or `run` / `test-first`) |

## Steps

1. Read the plan **once**. Extract every task with full text. Build a todo list of all tasks. Do not make later subagents re-read the plan file — paste the full task into their context.
2. Size tasks to ~2–5 minutes of focused work (e.g. “Create User model”, not “Implement auth system”). Split oversized tasks before dispatching.
3. For **each** task, in order:
   1. **Implementer subagent** — goal + full task text + project context + TDD instructions (`test-first`: failing test → minimal code → pass → no regressions). Answer any questions before they proceed.
   2. **Spec reviewer subagent** — original spec only; check paths, signatures, behavior, no scope creep. Output PASS or a concrete gap list. If gaps: fix, then re-run spec review until PASS.
   3. **Quality reviewer subagent** — conventions, errors, names, tests, security. Critical/important must be fixed and re-reviewed. Verdict: APPROVED or REQUEST_CHANGES.
   4. Mark the task complete only when both reviews are clean.
4. Do **not** start quality review before spec is PASS. Do **not** start the next task while either review has open issues.
5. Do **not** dispatch multiple implementers that touch the same files in parallel.
6. After all tasks: one **integration** review (consistency, full suite, merge-ready), then run the project’s real test command and report results.

## Red flags — never

- Implement without a plan
- Skip either review stage
- Accept “close enough” on the spec
- Let the implementer self-review replace a real reviewer
- Fix failed tasks only in the controller session when a fresh fix subagent would keep context clean

## Completion criteria

Done when you can state:

1. Every plan task completed with PASS + APPROVED (or an explicit user abort).
2. Integration review ran after the last task.
3. Project tests were run with the real command; results reported.
4. No open critical/important review findings.

## References

Load when relevant:

- `references/context-budget-discipline.md` — context degradation tiers for long multi-subagent runs
- `references/gates-taxonomy.md` — Pre-flight / Revision / Escalation / Abort gate vocabulary

## Attribution

Process adapted from Hermes Agent `subagent-driven-development` (MIT). Gate/context references adapted from gsd-build/get-shit-done (MIT © Lex Christopherson).
