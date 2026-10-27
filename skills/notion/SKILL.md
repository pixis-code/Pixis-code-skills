---
name: notion
description: "Notion API + ntn CLI for pages, databases, and markdown. Use when the user asks to create or update a Notion page or Notion database. Not for Google Docs (google-workspace), Obsidian vault notes (obsidian), or local PDF/PPTX (pdf, powerpoint)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [NOTION_API_KEY]
metadata:
  pixis:
    tags: [Notion, Productivity, Notes, Database, API, CLI]
    category: Productivity
    related_skills: [obsidian, google-workspace]
    attribution: Adapted from hermes-agent notion skill (MIT / community)
---

# Notion

Talk to Notion two ways with the same integration token:

- **`ntn` CLI** — preferred on macOS/Linux when installed (shorter syntax, file uploads, Workers).
- **HTTP + curl** — cross-platform fallback (default on Windows).

**When to use:** search/create/update Notion pages · query databases · markdown
in/out · attach files · Notion Workers (advanced).

**Do not use:** Google Docs/Sheets → `google-workspace`; local markdown vault →
`obsidian`; generate a PDF/deck → `pdf` / `powerpoint`.

Block type payloads: `references/block-types.md`.

## Setup

1. Create an integration at https://notion.so/my-integrations and copy the key
   (`ntn_…` or `secret_…`).
2. Store it where the agent can read env vars (e.g. shell profile or
   `$PIXIS_HOME/.env`):
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
3. In Notion: page menu `…` → **Connect to** → your integration (otherwise 404).
4. Optional `ntn` install (macOS/Linux):
   ```bash
   curl -fsSL https://ntn.dev | bash   # or: npm install --global ntn
   export NOTION_API_TOKEN=$NOTION_API_KEY
   export NOTION_KEYRING=0
   ```
   Skip `ntn login` — use the integration token headlessly.

```bash
if command -v ntn >/dev/null 2>&1; then
  # Path A
else
  # Path B (curl)
fi
```

`Notion-Version: 2025-09-03` is required on HTTP. In this API, user-facing
"databases" are **data sources**.

## Path A — `ntn` (preferred)

```bash
ntn api v1/search query="page title"
ntn api v1/pages/{page_id}
ntn api v1/pages/{page_id}/markdown
ntn api v1/blocks/{page_id}/children
ntn api v1/pages parent[page_id]=xxx \
  properties[title][0][text][content]="Notes" \
  markdown="# Agenda\n\n- Item"
ntn api v1/pages/{page_id}/markdown -X PATCH markdown="## Update\n\nShipped."
ntn api v1/data_sources/{data_source_id}/query -X POST \
  filter[property]=Status filter[select][equals]=Active
ntn files create < photo.png
```

`key=value` strings · `key[nested]=value` · `key:=value` typed (bool/num/null).

## Path B — HTTP + curl

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'

curl -s "https://api.notion.com/v1/pages/{page_id}/markdown" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"

curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "properties": {"title": [{"text": {"content": "Notes"}}]},
    "markdown": "# Agenda\n\n- Item"
  }'

curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Status", "select": {"equals": "Active"}}}'
```

### Property shapes

- Title: `{"title": [{"text": {"content": "..."}}]}`
- Select: `{"select": {"name": "Option"}}`
- Date: `{"date": {"start": "2026-01-15"}}`
- Checkbox: `{"checkbox": true}`
- Number: `{"number": 42}`

### Databases vs data sources (2025-09-03)

- Create pages with `parent: {"database_id": "..."}`
- Query with `POST /v1/data_sources/{data_source_id}/query`
- Search may return `"object": "data_source"`

## Rules

1. Confirm before creating/archiving pages or bulk updates.
2. Never print the full API key in logs or chat.
3. Rate limit ~3 req/s — space writes.
4. Prefer `/markdown` endpoints for agent-readable page content.

## Completion criteria

- Target page/database shared with the integration.
- Commands use `NOTION_API_KEY` (and `ntn` token exports when using Path A).
- Mutations confirmed; responses checked for API errors (404 = not shared).
