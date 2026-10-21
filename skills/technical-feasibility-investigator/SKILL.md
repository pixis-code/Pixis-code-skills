---
name: technical-feasibility-investigator
description: "Throwaway spikes to validate feasibility before a real build. Use when checking if an approach works or comparing options. Not for production implementation, plan grilling (technical-plan-challenger), or explaining existing code (code-explainer)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [spike, feasibility, prototype, experiment, proof-of-concept]
    related_skills: [technical-plan-challenger, test-first, debugging-assistant]
---

# Technical feasibility investigator

Run **disposable** experiments to answer feasibility questions before committing to a production build. Spikes are throwaway by design — delete or leave under `spikes/` once they paid their debt.

Adapted from Hermes `spike` (GSD-inspired) for Pixis. No parallel subagent fan-out; build sequentially unless the user asks otherwise.

## When to use

- "Is this even possible?" / "spike this" / "quick prototype"
- Compare approach A vs B with observable output
- Validate an unknown (library, protocol, perf bound) that docs alone cannot settle
- Before a large backend/feature build when risk is high

## Do not use

| Request | Hand off to |
|---------|-------------|
| Stress-test a written plan with questions only | `technical-plan-challenger` |
| Answer knowable from docs/code — research, don't build | `code-explainer` / read docs |
| Production feature implementation | Stop — implement after verdict; use `test-first` |
| Debug a production defect | `debugging-assistant` |
| Generate project wiki | `codebase-documentation-generator` |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | None beyond normal agent tools | Language/runtime only if the spike needs them |
| **Optional** | Project package managers | Install only inside `spikes/` scratch dirs |

No Hermes `references/` or install scripts. Do **not** add global deps for a spike — keep experiments self-contained.

## Iron rules

1. **No production path edits** for the spike itself. Work under `spikes/` (or a user-named scratch dir).
2. **Observable output** — CLI, minimal page, one endpoint, or a failing/passing assertion the user can feel. "It works" from a log line alone is a failed spike.
3. **Depth over speed** — test edges; an honest INVALIDATED is success.
4. **Hardcode** — avoid Docker, env systems, and bundlers unless the question requires them.

## Method

```
decompose → align → research → build → verdict
```

### 1. Decompose

Break the idea into **2–5** independent feasibility questions. Present a table:

| # | Spike | Validates (Given/When/Then) | Risk |
|---|-------|----------------------------|------|
| 001 | websocket-streaming | Given WS, when tokens stream, then client gets chunks &lt; 100ms | High |
| 002a | pdf-pdfjs | … | Medium |
| 002b | pdf-camelot | … | Medium |

- **standard** — one approach, one question  
- **comparison** — same number, letter suffix `a`/`b`

Order by risk (kill the idea early). Skip decompose only if the user already named one exact spike.

### 2. Align

Ask: build all in this order, or adjust? Do not write code until the user confirms scope.

### 3. Research (brief)

Per spike: 2–3 sentence brief, competing approaches table if needed, pick one with why. Check installed versions in the project env. Skip research for pure logic with no deps.

### 4. Build

```
spikes/
├── 001-websocket-streaming/
│   ├── README.md
│   └── main.py
└── 002a-pdf-parse-pdfjs/
    ├── README.md
    └── parse.js
```

Prefer: runnable CLI → minimal HTML → tiny HTTP endpoint → focused test assertions.

### 5. Verdict (in each README)

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked
### What didn't
### Surprises
### Recommendation for the real build
```

- **VALIDATED** — question answered yes, with evidence  
- **PARTIAL** — works under constraints X/Y/Z  
- **INVALIDATED** — does not work; document why (still a successful spike)

For comparison spikes, add a head-to-head table and a winner for *this* use case.

## Frontier mode

If spikes already exist and the user asks what next: look for integration risks, unproven data handoffs, vision gaps, and alternatives for PARTIAL/INVALIDATED. Propose 2–4 Given/When/Then candidates.

## Completion criteria

1. Spike table aligned with the user (unless single named spike).
2. Code lives under throwaway dirs; production tree untouched for the experiment.
3. Each spike has a verdict with evidence (commands/output).
4. Clear recommendation: proceed / constrain / abandon — no silent production merge of spike code.
