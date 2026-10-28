---
name: debugging-assistant
description: "Root-cause debugging of errors, logs, and failed tests before fixing. Use when investigating a traceback, bug, or unexpected behavior. Not for read-only explanation (code-explainer), behavior-preserving cleanup (code-refactoring), or browser QA (app-qa)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [debugging, root-cause, traceback, investigation, fix]
    related_skills: [test-first, code-explainer, self-review]
---

# Debugging assistant

Diagnose software defects and apply the **smallest** fix once the root cause is known. No fixes without investigation. Never claim reproduction or a successful fix without evidence.

Adapted from Hermes `systematic-debugging` for Pixis (no Hermes-only tools or subagent fan-out).

## When to use

- Tracebacks, exceptions, stack traces
- Failed tests or unexpected runtime behavior
- "Why does this endpoint return 500?" / "Investigate this failing API request"
- Logs that point at a defect you need to isolate and fix

## Do not use

| Request | Hand off to |
|---------|-------------|
| Explain code without changing it | `code-explainer` |
| Improve structure / readability with same behavior | `code-refactoring` |
| Only write the failing regression test first (RED before any production edit) | `test-first` — use it when Phase 4 needs a new regression test |
| Live browser QA of an app flow | `app-qa` |
| Pre-commit review of your own diff (no active bug) | `self-review` |

## Iron law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Do not propose or apply production fixes until Phase 1 is done.

## Feedback loop rule

Before theorizing from code alone, identify or create a **tight** command that goes red on the user's symptom and green when fixed. Prefer the project's own test runner and pinned environment (same discovery rules as `test-first`). Guessing without a red-capable loop is failure.

## Phase 1 — Root cause investigation

1. Read the full error, traceback, log, or failing assertion (paths, line numbers, codes).
2. Build or identify a tight repro loop (in order of preference): focused failing test → scripted CLI/HTTP repro → minimal harness. Run it at least once. If not reproducible, gather more data — do not guess.
3. Check recent changes: `git log`, `git diff`, relevant commits.
4. For multi-layer systems, gather evidence at boundaries (input/output per layer) before blaming one component.
5. Trace bad values upstream to the source; plan to fix at the source, not only the symptom.

**Stop** until you can state what fails and why (hypotheses allowed only after evidence).

## Phase 2 — Pattern analysis

1. Minimize the repro (cut inputs/steps one at a time while the loop stays red).
2. Find working siblings in the same codebase; list concrete differences.
3. Note config, env, and dependency assumptions.

## Phase 3 — Hypothesis and testing

1. Rank 3–5 falsifiable hypotheses with a predicted observation for each.
2. Test one variable at a time (smallest probe). Prefer inspection over shotgun patches.
3. If the probe fails, form a new hypothesis — do not stack unrelated fixes.
4. If you do not know, say so and ask or gather more evidence.

## Phase 4 — Implementation

1. Prefer a failing regression test before the production fix. When writing that test is the immediate job, follow `test-first` (project test command, RED then GREEN). Do not invent a runner.
2. Apply **one** root-cause fix. No drive-by refactors or feature work.
3. Re-run the focused loop (must pass), then a relevant broader suite when available. Report **actual** commands and results.
4. **Rule of three:** after three failed fix attempts, stop and discuss architecture with the user — do not silently attempt a fourth.

## Evidence rules

- Do not claim you reproduced, fixed, or verified unless you ran the commands and saw the output.
- If tools or the environment block repro, state the blocker and what remains unverified.
- Remove temporary debug logging you added once the fix is verified (or leave it only if the user wants it kept).

## Completion criteria

Done only when you can state:

1. Root cause (with file references).
2. What changed (and what you deliberately did not change).
3. Commands run and their results (repro red → fix green, plus broader checks if run).
4. Remaining risks or unverified areas.
