---
name: code-explainer
description: "Explain existing code, flows, and design with file references. Use when the user asks how code works or to trace a path. Not for fixes (debugging-assistant), structure changes (code-refactoring), or browser QA (app-qa)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [explain, codebase, tracing, onboarding, read-only]
    related_skills: [debugging-assistant, code-refactoring]
---

# Code explainer

Explain **existing** code so the user understands it. Do not modify source, add features, fix bugs, or refactor. Read and cite real files.

## When to use

- "Explain this function / class / module"
- "How does authentication / X work in this project?"
- "Trace the request / data flow through …"
- Unfamiliar code, dependencies, or design decisions in the current repo

## Do not use

| Request | Hand off to |
|---------|-------------|
| Fix a traceback, bug, or failing test | `debugging-assistant` (then `test-first` when a regression test is needed) |
| Refactor, dedupe, or restructure without changing behavior | `code-refactoring` |
| Browser walkthrough / screenshots of a running app | `app-qa` |
| Pre-commit review of your own diff | `self-review` |
| Full wiki / permanent docs dump | Answer briefly here; only write docs if the user explicitly asks for a document |

## Steps

1. Clarify the target: symbol, file, feature, or flow. If ambiguous, ask once; otherwise infer from selection / open files / the question.
2. Locate real sources (search and open files). Prefer project entrypoints, routers, and call sites over guesses.
3. Trace only what the question needs:
   - **Local:** inputs → steps → outputs / side effects of one function or class.
   - **Flow:** entry → key hops → exit (e.g. HTTP handler → service → DB).
   - **Design:** why this shape exists, using evidence from code, tests, and nearby patterns.
4. Explain in clear steps matched to the user's depth (brief for "what does this do?", deeper for "how does X work across the app?").
5. Cite concrete locations (`path` and symbol or line range) for every important claim. Do not invent files, APIs, or behavior.
6. Call out uncertainty: missing context, dynamic dispatch, generated code, or unread branches. Do not bluff.
7. Stop without editing. If the user then wants a fix or refactor, point them to `debugging-assistant` or `code-refactoring`.

## Completion criteria

Done only when you can state:

1. What was explained (symbol / flow / question).
2. A correct, evidence-based explanation with file references.
3. Open questions or unread areas (if any).
4. You did not modify the codebase.
