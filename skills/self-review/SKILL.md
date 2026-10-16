---
name: self-review
description: "Review your own change before commit: read the diff, fix in-scope defects, run project tests. Not for a colleague's PR."
version: 3.1.1
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Agentic Work
    tags: [review, diff, tests]
    related_skills: [test-first, github]
---

# Self-review

Deliberate pre-handoff review of **your** change before commit. Do not use this for a colleague's pull request (use `github` for that). Do not spawn parallel agents. This is not the engine's automatic verification gate — you must read the diff and decide.

## Steps

1. Collect the complete change: run `git status`, then read **both** `git diff` (unstaged) and `git diff --cached` (staged). If both diffs are empty, stop — nothing to review.
2. For every changed hunk, open the file and read the surrounding code (not only the diff lines).
3. Inspect relevant sibling files and nearby patterns (same kind of function, error handling, or test). Match how the project already does it.
4. Fix **every in-scope** defect you find (bugs in the current change, clear copy-paste of the same bug in code this task owns, accidental edits). Apply the fixes before handoff.
5. Report **out-of-scope** issues separately (other modules, pre-existing debt, follow-ups). Do not silently expand the task to fix them.
6. If the diff changes what an existing test expects: keep the change only when the requested behavior itself changed. Otherwise restore the old expectation. Revert only that inappropriate assertion edit — do not discard unrelated user edits.
7. Run relevant tests with the project's documented command and pinned interpreter/environment (`package.json` scripts, `pyproject.toml` / `pytest.ini` / `Makefile` / `Cargo.toml` / `go.mod` / CI `run:` steps; `.venv` / `uv` / `poetry` / lockfile package manager). Do not invent a runner.
8. Do **not** declare the review complete if tests were not run. State the exact blocker and which checks remain unverified.

## Done (only after step 7 succeeded)

Report:

1. What the full diff does (staged + unstaged).
2. In-scope defects fixed.
3. Out-of-scope issues (if any).
4. Any test expectation restored.
5. Test command(s) run and their results.
