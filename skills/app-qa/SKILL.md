---
name: app-qa
description: "Browser QA of an app flow. Report page, repro steps, observed result, and screenshot status."
version: 2.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: UX
    tags: [qa, browser, ux, bug-report]
---

# App QA

Manually test a running app in the browser. Do not write unit tests or invent results from source code. The browser toolset is off by default.

Report only with `templates/qa-report.md`. `references/issue-taxonomy.md` is optional — use it only when evidence clearly supports a severity label.

## Steps

1. Check which tools are available **this turn**. You need all of:
   - navigate (open a URL)
   - page inspect / snapshot (see the page structure)
   - click (and type/submit if the flow needs them)
   - screenshot (or an equivalent capture tool)
2. If any of those are missing, **stop**. Do not pretend you tested. Do not QA from source, curl, or a guessed walkthrough. Tell the user:

   Browser tools are not available in this chat (needed: navigate, page inspect, click, screenshot).
   The Pixis browser toolset is off by default.
   Enable it: open the session tools and turn on Browser, then send the QA request again so the tools load.

3. Get the target URL and the flow to cover. Navigate to that URL.
4. On each screen in the flow: inspect/snapshot the page, then click/type through the requested steps.
5. Console: record console errors **only** if an available tool actually returns them. If no console tool is available, omit console notes — never invent them.
6. Screenshots: for each bug, capture the broken state when a screenshot tool is available. If screenshot/capture is unavailable, set Screenshot to `unavailable — no capture tool in this session` and still fill the other fields.
7. Write one report using `templates/qa-report.md`. One entry per bug. Sort by how badly it blocks the flow. Deduplicate the same bug on multiple pages (list extra pages on the first entry).

## Completion criteria

Done only when you can state all of the following:

1. What was actually tested (URL + flows/steps you ran in the browser).
2. Confirmed issues, each with page, reproduction steps, observed result, expected result when known, and screenshot path or `unavailable`.
3. Blocked or untested steps (and why — e.g. missing auth, tool failure, out of scope).
4. You did not claim a test, console finding, or screenshot you did not perform.
