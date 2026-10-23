---
name: run
description: "Run the stated task or project command end-to-end. Find the real command, execute it, report the result. Use when the user says run/build/start/lint a script or the app. Not for TDD (test-first), browser QA (app-qa), GitHub CI (github), or explain-only (code-explainer)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Developer Workflow
    tags: [run, execute, build, start, core-loop]
    related_skills: [test-first, github, self-review, code-explainer, docker-environment-manager]
---

# Run

Take the user's goal, find the project's real command, run it, report what happened. Prefer action over planning.

## When to use

- "Run the app" / "start the server"
- "Run the build" / "lint" / "migrate" / a named npm/make/poetry script
- Execute a project command the user named without asking for a full debug campaign

## Do not use

| Request | Hand off to |
|---------|-------------|
| Write a failing test then fix | `test-first` |
| Browser walkthrough of a live UI | `app-qa` |
| PR / review comments / CI via `gh` | `github` |
| Explain how a command or flow works (no execute) | `code-explainer` |
| Container / Compose / Docker logs | `docker-environment-manager` |
| Root-cause a traceback then patch | `debugging-assistant` |

## Steps

1. Restate the goal in one line (start the app, build, lint, migrate, run a script). If the goal is missing, ask once.
2. Find the project's command — do not invent one. Check, in order: `package.json` scripts, `Makefile`, `pyproject.toml` / `poetry` / `uv`, `Cargo.toml`, `go.mod`, `docker-compose.yml`, README “Getting started”, then CI `run:` steps.
3. Use the pinned environment (project `.venv` / `uv` / `poetry`, or the lockfile's package manager). Do not switch to system tools when a project env exists.
4. If no reliable command is found, **stop and ask**. Do not guess.
5. Run the command. Capture exit code and the important stdout/stderr (last errors, not the whole log unless short).
6. Report: command used, exit status, and whether the goal succeeded. If it failed, give the first real error and the next safe step — do not silently switch to another skill unless the user asks.

## Completion criteria

Done when you can state:

1. The goal in one line.
2. The exact command (and interpreter/env) used.
3. Success or failure from the real run.
4. You did not claim success without running the command.
