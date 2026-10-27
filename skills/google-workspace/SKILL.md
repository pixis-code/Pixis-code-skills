---
name: google-workspace
description: "Gmail, Calendar, Drive, Docs, and Sheets via gws CLI or Python. Use when the user asks about unread Gmail, Google Calendar, Drive files, Docs, or Sheets. Not for local PDF/PPTX (pdf, powerpoint), Notion pages (notion), or Obsidian vault notes (obsidian)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  pixis:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth]
    category: Productivity
    related_skills: [notion, pdf, powerpoint]
    attribution: Adapted from Nous Research hermes-agent google-workspace (MIT)
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs through Pixis-managed OAuth
and a thin CLI wrapper. Prefers `gws` when installed; otherwise uses the
bundled Python client (`scripts/google_api.py`).

**When to use:** search/send Gmail · list/create Calendar events · Drive
upload/download/share · Sheets read/write · Docs create/append · morning brief
(Gmail + Calendar).

**Do not use:** local `.pdf` / `.pptx` editing → `pdf` / `powerpoint`; Notion
pages → `notion`; Obsidian vault files → `obsidian`; email-only IMAP without
Calendar/Drive (plain App Password IMAP is out of scope here).

## References

- `references/gmail-search-syntax.md` — Gmail operators (`is:unread`, `from:`, …)
- `references/daily-brief.md` — morning brief procedure (schedule + urgent mail)

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once)
- `scripts/google_api.py` — API CLI (prefers `gws`, falls back to Python)

Tokens live under `$PIXIS_HOME` (default `~/.pixis`): `google_token.json`,
`google_client_secret.json`.

## First-time setup

Non-interactive — drive it step by step with the user.

```bash
GSETUP="python <skill-dir>/scripts/setup.py"
```

0. `$GSETUP --check` → `AUTHENTICATED` means skip to Usage.
1. Ask which services they need (`email,calendar` vs `all`, etc.).
2. User creates a Desktop OAuth client in Google Cloud Console, enables Gmail /
   Calendar / Drive / Sheets / Docs / People APIs, adds them as a test user if
   the app is in Testing, and gives you the client-secret JSON path:
   `$GSETUP --client-secret /path/to/client_secret.json`
3. `$GSETUP --auth-url --services all --format json` → send `auth_url` to the
   user. Browser landing on `http://localhost:1` is expected; they paste the
   full redirect URL (or code).
4. `$GSETUP --auth-code "URL_OR_CODE" --format json`
5. `$GSETUP --check` → `AUTHENTICATED`. Token auto-refreshes.

Deps (once): `$GSETUP --install-deps` installs `google-api-python-client`,
`google-auth-oauthlib`, `google-auth-httplib2` via pip.

Revoke: `$GSETUP --revoke`

## Usage

```bash
GAPI="python <skill-dir>/scripts/google_api.py"
```

### Gmail

```bash
$GAPI gmail search "is:unread" --max 10
$GAPI gmail get MESSAGE_ID
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail reply MESSAGE_ID --body "Thanks"
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
```

### Calendar

```bash
$GAPI calendar list
$GAPI calendar create --summary "Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar delete EVENT_ID
```

### Drive / Contacts / Sheets / Docs

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive upload /path/to/report.pdf
$GAPI drive download FILE_ID --output ~/doc.pdf
$GAPI drive share FILE_ID --email alice@example.com --role reader
$GAPI contacts list --max 20
$GAPI sheets create --title "Q4 Budget"
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'
$GAPI docs create --title "Meeting Notes" --body "First paragraph..."
$GAPI docs get DOC_ID
$GAPI docs append DOC_ID --text "Additional content"
```

All commands return JSON.

## Rules

1. **Confirm before send/create/delete/share/write** — show recipients, IDs,
   content, and role; prefer Drive trash over `--permanent`.
2. **Check auth first** — `$GSETUP --check`.
3. **Calendar times need timezone** — ISO 8601 with offset or `Z`.
4. **Rate limits** — avoid rapid-fire sequential calls; batch reads.

## Completion criteria

- Auth checked (or setup completed) before API work.
- Destructive/send actions confirmed with the user.
- Output is parsed JSON; failures report the API/setup error, not a guessed success.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Setup steps 2–5 |
| `REFRESH_FAILED` | Redo auth-url + auth-code |
| `HttpError 403: Insufficient Permission` | `$GSETUP --revoke` then re-auth |
| `ModuleNotFoundError` | `$GSETUP --install-deps` |
| Advanced Protection blocks auth | Admin must allowlist the OAuth client ID |
