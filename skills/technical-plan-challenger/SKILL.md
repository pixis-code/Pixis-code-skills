---
name: technical-plan-challenger
description: "Adversarial interview of a technical plan before coding. Use when stress-testing architecture or design decisions. Not for coding, spikes (technical-feasibility-investigator), or reviewing existing diffs (self-review)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [planning, adversarial, interview, architecture, pre-implementation]
    related_skills: [technical-feasibility-investigator, self-review, test-first]
---

# Technical plan challenger

Stress-test a plan with structured adversarial questions **before any implementation**. Model the plan as a **design tree**; interview in frontier rounds until branches are resolved and nothing is silently assumed.

Adapted from Hermes `grill-me` (frontier rounds + coverage) for Pixis. Look up codebase facts yourself — do not ask the user what you can read in the repo.

## When to use

- "Grill me" / "challenge this design" / "stress-test this plan"
- Before complex work: auth, schema changes, migrations, payments, multi-service backends
- Vague plans with unresolved decisions
- Before a large implementation push

## Do not use

| Request | Hand off to |
|---------|-------------|
| Build a throwaway prototype to prove feasibility | `technical-feasibility-investigator` |
| Review an existing code diff before commit | `self-review` |
| Debug a failing API or container | `api-backend-troubleshooter` / `docker-environment-manager` |
| Explain existing code | `code-explainer` |
| Simple one-off tasks with no design ambiguity | Just implement (or ask one clarifying question) |

## Dependencies

None. Interview-only skill — no install scripts. Hermes had no `references/`.

Look up codebase facts with normal file search/read; do not ask the user for anything you can find in the repo.

## Core mechanic: frontier rounds

The **frontier** = every decision whose prerequisites are already settled.

Each round: ask the **entire** current frontier in one message. Number questions. Each carries your **recommendation**. Then wait.

A question that depends on an unanswered question in this round belongs in a **later** round.

```
❓ Q1 — <title>: <body / options>
➡️ Recommendation: <answer + one-line why>

❓ Q2 — ...
➡️ Recommendation: ...
```

**Facts are your job; decisions are the user's.** Search the codebase for existing patterns before asking. Don't block the whole round on one lookup — ask the rest of the frontier now.

## Question coverage

**Understanding** — real objective; IN/OUT of scope; constraints (time, tech, team); users.

**Technical decisions** — why this approach not X; failure modes; worst case; rollback; match existing project patterns when they exist.

**Edge cases** — bad user input; dependency down; 100× volume; security/privacy implications.

## Synthesis (frontier empty)

1. Summarize all decisions  
2. List open items and explicit OUT of scope  
3. Ask: "Aligned? Start implementing, or adjust?"  

**Do not write production code** until the user confirms shared understanding.

## Pitfalls

1. Asking out of dependency order (guesses wearing question marks)  
2. Asking the user for facts visible in the repo  
3. Accepting "I don't know" without options + a recommendation  
4. Writing code during interrogation  
5. Being too agreeable — find problems  
6. Ignoring the user's language  

## Verification checklist

- [ ] Round questions had settled prerequisites  
- [ ] Each question had a recommendation  
- [ ] Codebase facts looked up, not asked  
- [ ] Frontier empty before synthesis  
- [ ] Decision summary + open items delivered  
- [ ] User alignment confirmed before stopping  

## Completion criteria

1. Adversarial rounds completed (or user ended early with explicit stop).  
2. Decision summary and open risks recorded.  
3. No implementation started without green light.  
4. If user wants a spike next → `technical-feasibility-investigator`.
