---
name: test-first
description: "Failing test before the fix, using the project's own test command and interpreter."
version: 2.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Engineering
    tags: [testing, tdd, regression]
    related_skills: [self-review]
---

# Test first

Prove the bug with a failing test, then fix production code. This skill is only the test-first loop — not full root-cause debugging (`pixis:systematic-debugging`).

## Find the project's test command

1. Discover the runner from the repo (do not invent one). Check, in order: `package.json` `scripts.test` (and related scripts), `pyproject.toml`, `pytest.ini`, `tox.ini`, `Makefile`, `Cargo.toml`, `go.mod`, then `run:` steps in `.github/workflows`.
2. Use the pinned environment:
   - Python: project `.venv/bin/python -m pytest`, `uv run`, or `poetry run` when present — not system Python if a project env exists.
   - Node: lockfile picks the runner (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` / `bun.lock` → bun, else npm).
3. If you cannot identify a reliable test command and interpreter, **stop and ask the user**. Do not guess.

## Steps

1. Inspect the bug and nearby code (failing behavior, sibling functions, other call sites). Note where a focused test should live. Do not change production code yet.
2. If production code was already changed for this fix before a failing test existed: revert **only those premature production edits**. Keep unrelated user changes. Then continue from step 1.
3. Write one focused test for the missing or broken behavior. Do not change production code yet. Do not change what an existing test expects unless the requested behavior itself is changing — if an old assertion must move, stop and ask.
4. Run **only that test** with the project command from above. Capture the command and output.
5. Confirm it fails for the **expected** reason (missing/wrong behavior).  
   - Passes immediately → test is wrong; rewrite and rerun.  
   - Errors from typos/imports/setup → fix the test only; rerun until the failure is the behavior gap.  
   Do not edit production code until this evidence exists.
6. If siblings/call sites share the same defect, add a failing test for each before fixing.
7. Apply the smallest production change that makes the new test(s) pass. No unrelated refactors.
8. Verify:
   - Re-run the focused test — it must pass.
   - Run the relevant broader suite (project test script or the closest targeted suite).
   - Report the **actual commands** and results. Confirm the focused test failed for the expected reason earlier, then passed after the fix.
