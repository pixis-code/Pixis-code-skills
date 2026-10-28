# Pixis skills

Short decision table for skill selection. The agent routes primarily from each skill’s `description`; this table helps humans and collision checks keep boundaries clear.

| Skill | Job | Use when | Do not use / hand off |
|-------|-----|----------|------------------------|
| `code-explainer` | Explain existing code and flows | How does X work? Explain / trace this | Fixes → `debugging-assistant`; structure cleanup → `code-refactoring`; browser QA → `app-qa` |
| `debugging-assistant` | Root-cause then smallest fix | Traceback, bug, failed test, unexpected behavior | Read-only explain → `code-explainer`; pure refactor → `code-refactoring`; new failing test loop → `test-first`; browser QA → `app-qa` |
| `code-refactoring` | Improve structure, same behavior | Refactor, dedupe, simplify working code | Explain-only → `code-explainer`; bugs → `debugging-assistant`; pre-commit review → `self-review` |
| `test-first` | Failing test before production fix | Bug fix needs a regression test first | Full root-cause campaign → `debugging-assistant` |
| `self-review` | Review **your** diff before commit | Pre-handoff check of own changes | Colleague PR → `github` |
| `github` | `gh` PRs, issues, CI | After commit: PR / review comments / CI | Commit messages; own pre-commit review → `self-review` |
| `app-qa` | Browser QA of a live flow | Manual UI walkthrough with evidence | Unit tests from source; code-only QA |
| `design-tokens` | Theme tokens / DESIGN.md | Extract colors/spacing into theme | Page redesign → site redesign skill |
| `google-workspace` | Gmail/Calendar/Drive/Docs/Sheets | Google Workspace API tasks | Local PDF/PPTX → `pdf`/`powerpoint`; Notion → `notion`; Obsidian → `obsidian` |
| `notion` | Notion pages/databases | Notion API / ntn CLI | Obsidian vault → `obsidian`; Google Docs → `google-workspace` |
| `obsidian` | Local Obsidian vault notes | Read/search/edit vault markdown | Notion → `notion`; Google Docs → `google-workspace` |
| `pdf` | Local PDF create/read/edit | PDF reports, forms, merge, OCR | PPTX → `powerpoint`; Google Docs → `google-workspace` |
| `powerpoint` | Local .pptx decks | Create/edit PowerPoint | PDF → `pdf`; Google Slides → `google-workspace` |
| `meeting-action-items` | Decisions/owners/tickets from notes | Meeting notes or transcript follow-through | Calendar/Gmail fetch → `google-workspace`; inbox triage → `email-inbox-triage` |
| `email-inbox-triage` | Prioritize inbox + draft replies | What needs attention / triage / draft replies | Raw Gmail API → `google-workspace`; SMS → `telephony` |
| `llm-wiki` | Interlinked markdown knowledge wiki | Create/ingest/query/lint a wiki KB | Plain Obsidian notes → `obsidian`; citations-only → `grounded-citations` |
| `airtable` | Airtable bases/tables/records via API | Airtable CRUD / filters / upserts | Notion → `notion`; Sheets → `google-workspace` |
| `telephony` | Twilio SMS/calls + AI outbound calls | Texts, phone numbers, outbound AI calls | Email → `email-inbox-triage` / `google-workspace` |

## Routing fixtures (positive → expected)

| Prompt | Expected skill |
|--------|----------------|
| Explain what this function does. | `code-explainer` |
| Investigate and fix this traceback. | `debugging-assistant` |
| Refactor this function to improve readability without changing its behavior. | `code-refactoring` |
| Write a failing test then fix the bug. | `test-first` |
| Review my changes before I commit. | `self-review` |
| Open a PR for this branch. | `github` |
| QA the signup flow in the browser. | `app-qa` |
| Pull colors into CSS variables / DESIGN.md. | `design-tokens` |
| List unread Gmail and today's calendar. | `google-workspace` |
| Create a Notion page from these meeting notes. | `notion` |
| Add a daily note in my Obsidian vault. | `obsidian` |
| Merge these PDFs and extract the tables. | `pdf` |
| Build a 5-slide pitch deck as pptx. | `powerpoint` |
| Extract action items and owners from these meeting notes. | `meeting-action-items` |
| Triage today's inbox and draft replies to anything urgent. | `email-inbox-triage` |
| Ingest this article into my LLM wiki and update the index. | `llm-wiki` |
| List records in my Airtable Tasks table with Status=Todo. | `airtable` |
| Send an SMS from my Twilio number after I confirm. | `telephony` |

## Routing fixtures (negative — must not steal)

| Prompt | Must not activate first | Prefer |
|--------|-------------------------|--------|
| Refactor this function to remove duplicated logic. | `code-explainer` | `code-refactoring` |
| Explain this function without changing the code. | `debugging-assistant` / `code-refactoring` | `code-explainer` |
| Explain this function without modifying it. | `code-refactoring` | `code-explainer` |
| Merge these PDFs into one file. | `powerpoint` / `notion` | `pdf` |
| Create a Notion database for tasks. | `obsidian` / `google-workspace` | `notion` |
| Build a PowerPoint pitch deck. | `pdf` | `powerpoint` |
| Triage my Gmail inbox for urgent replies. | `meeting-action-items` / `telephony` | `email-inbox-triage` |
| Extract owners and deadlines from this transcript. | `email-inbox-triage` | `meeting-action-items` |
| Buy a Twilio number and text me a status update. | `email-inbox-triage` | `telephony` |
| Create a wiki page for this research topic with cross-links. | `obsidian` (alone) | `llm-wiki` |

Run per-skill checks:

```bash
bash skills/code-explainer/scripts/check_skill.sh
bash skills/debugging-assistant/scripts/check_skill.sh
bash skills/code-refactoring/scripts/check_skill.sh
bash skills/google-workspace/scripts/check_skill.sh
bash skills/notion/scripts/check_skill.sh
bash skills/obsidian/scripts/check_skill.sh
bash skills/pdf/scripts/check_skill.sh
bash skills/powerpoint/scripts/check_skill.sh
bash skills/meeting-action-items/scripts/check_skill.sh
bash skills/email-inbox-triage/scripts/check_skill.sh
bash skills/llm-wiki/scripts/check_skill.sh
bash skills/airtable/scripts/check_skill.sh
bash skills/telephony/scripts/check_skill.sh
```

