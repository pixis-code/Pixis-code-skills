---
name: airtable
description: "Airtable REST API via curl: list bases, read/create/update records. Use when working with Airtable bases, tables, or records. Not for Notion (notion), Google Sheets (google-workspace), or meeting extraction (meeting-action-items)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [AIRTABLE_API_KEY]
  commands: [curl]
metadata:
  pixis:
    tags: [Airtable, Productivity, Database, API]
    category: Productivity
    related_skills: [notion, google-workspace, meeting-action-items]
    attribution: Adapted from hermes-agent airtable skill (MIT / community)
---

# Airtable

Airtable REST API via `curl` + a personal access token. No MCP/OAuth/SDK required.

**When to use:** inspect bases/tables · list/filter records · create/update/upsert/delete
rows where API access exists.

**Do not use:** Notion databases → `notion`; Google Sheets → `google-workspace`;
meeting notes → tickets without Airtable → `meeting-action-items`.

## Setup

1. Create a PAT at https://airtable.com/create/tokens (`pat…`)
2. Scopes (minimum): `data.records:read`, `data.records:write`, `schema.bases:read`
3. Add each target base to the token **Access** list (wrong base → `403`)
4. Store (never print the full token):
   ```
   AIRTABLE_API_KEY=pat_your_token_here
   ```
   in the environment or `$PIXIS_HOME/.env`

Legacy `key…` API keys are deprecated — PATs only.

If `AIRTABLE_API_KEY` is missing, stop and give setup steps — do not invent records.

## API basics

- Base: `https://api.airtable.com/v0`
- Auth: `Authorization: Bearer $AIRTABLE_API_KEY`
- IDs: bases `app…`, tables `tbl…`, records `rec…`
- Rate limit: 5 req/sec/base (`429` → back off)
- Batch create/delete: max **10** records/request; list pages: max **100** + `offset`

```bash
# Auth check — expect 200
curl -s -o /dev/null -w "%{http_code}\n" \
  https://api.airtable.com/v0/meta/bases \
  -H "Authorization: Bearer $AIRTABLE_API_KEY"
```

## Common reads

```bash
curl -s "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool

curl -s "https://api.airtable.com/v0/meta/bases/$BASE_ID/tables" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool

curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=10" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool

FORMULA="{Status}='Todo'"
ENC=$(python -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$FORMULA")
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?filterByFormula=$ENC&maxRecords=20" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

Always URL-encode `filterByFormula` via Python — never hand-escape.

## Common writes

Confirm before create/update/delete. Prefer `PATCH` (merge) over `PUT` (replace/clear).

```bash
curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Name":"New task","Status":"Todo"}}' | python -m json.tool

curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Status":"Done"}}' | python -m json.tool

# Upsert by merge field
curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"performUpsert":{"fieldsToMergeOn":["Email"]},"records":[{"fields":{"Email":"a@b.com","Status":"Active"}}]}' \
  | python -m json.tool
```

Pass `"typecast": true` to auto-coerce / create select options. Inspect schema
before mutating. For bulk deletes, echo filter + count and get approval first.

## Workflow

1. Auth check → 2. List bases / get `app…` → 3. Inspect tables/schema →
4. Filter to resolve `rec…` before PATCH → 5. Batch writes (≤10) → 6. Confirm deletes

## Pitfalls

- Empty fields omitted from responses ≠ field missing from schema
- Single-select option must exist unless `typecast: true`
- `403` often means base not on token Access list
- Do not log or paste full API keys

## Completion criteria

- Credential present or setup instructions given
- Schema inspected before writes
- Mutations approved when destructive/consequential
- Responses checked for Airtable error codes
