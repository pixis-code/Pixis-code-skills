---
name: api-backend-troubleshooter
description: "Troubleshoot failing REST and GraphQL APIs and backend HTTP requests, including HTTP 400, 401, 403, 404, 422, 429, and 500 errors. Inspect endpoints, request payloads, headers, server logs, tracebacks, response bodies, and exception handling to identify API root causes and recommend fixes. Use when an API endpoint fails, returns an unexpected status, or produces incorrect data. Do not use for general Python errors unrelated to HTTP APIs (debugging-assistant), code explanations (code-explainer), or browser UI testing (app-qa)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Backend
    tags: [api, rest, graphql, http, auth, debugging, curl]
    related_skills: [debugging-assistant, test-first, browser-traffic-api-client]
---

# API / backend troubleshooter

Isolate the failing HTTP/API layer before guessing at a fix. Drive diagnosis with `curl`, Python `requests`/`httpx`, or the project's HTTP client. Redact tokens in all logs and reports.

Adapted from Hermes `rest-graphql-debug` for Pixis (no Hermes-only tools).

## When to use

- Unexpected status or body from a REST or GraphQL endpoint
- Auth failures (401/403, expired token, wrong scheme)
- Works in Postman/Insomnia but fails in app code
- Webhook/callback integration issues
- Rate limiting, pagination, or schema/contract drift
- Building or reviewing API smoke/integration tests

## Do not use

| Request | Hand off to |
|---------|-------------|
| Live browser UI walkthrough | `app-qa` |
| General traceback / non-API root cause | `debugging-assistant` |
| Derive a client from captured browser HAR | `browser-traffic-api-client` |
| Explain code without probing the API | `code-explainer` |
| Failing unit test with no HTTP layer | `debugging-assistant` / `test-first` |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | `curl` | Primary HTTP probe |
| **Optional** | `python3` | JWT decode / multi-step scripts |
| **Optional** | `requests` / `httpx` | Richer Python clients (`--with-requests`) |

Hermes had no `references/` or install scripts — recipes are in this file.

```bash
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes --with-requests   # pip only if requests missing; curl is manual
```

**Production:** curl/OS packages are not auto-installed by this skill.

## Core principle

Walk the chain in order; never skip a step:

```
1. Connectivity   → can we reach the host?
1.5 Timeouts      → connect-slow vs read-slow?
2. TLS/SSL        → cert valid and trusted?
3. Auth           → credentials correct and unexpired?
4. Request format → payload/method/headers match expectations?
5. Response parse → does our code accept what came back?
6. Semantics      → is the data correct for the request?
```

A 200 can hide bad data. A 500 can mask a one-character auth typo.

## Quickstart

```bash
# Verbose REST
curl -v "https://api.example.com/users/1"

# POST JSON
curl -v -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"test","email":"test@example.com"}'

# Headers only / health
curl -sI "https://api.example.com/health"

# Timing breakdown
curl -w "dns:%{time_namelookup}s connect:%{time_connect}s tls:%{time_appconnect}s ttfb:%{time_starttransfer}s total:%{time_total}s\n" \
  -o /dev/null -s "https://api.example.com/endpoint"
```

GraphQL (always inspect `errors` even when HTTP is 200):

```bash
curl -s -X POST "https://api.example.com/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"{ user(id: 1) { name email } }"}' | python -m json.tool
```

Python with explicit timeouts (never hang forever):

```python
import requests
resp = requests.get(url, headers=headers, timeout=(3.05, 30))
print(resp.status_code, dict(resp.headers))
ct = resp.headers.get("Content-Type", "")
print(resp.json() if "application/json" in ct else resp.text[:500])
```

## Layered debug flow

### 1–1.5 Connectivity and timeouts

```bash
nslookup api.example.com
curl -v --connect-timeout 5 "https://api.example.com/health"
```

High `time_connect` → network/firewall/VPN. High `time_starttransfer` with low connect → slow server. Distinguish `ConnectTimeout` vs `ReadTimeout` in Python.

### 2 TLS

```bash
curl -vI "https://api.example.com" 2>&1 | grep -Ei "SSL|subject|expire|issuer"
```

Use `-k` only for ad-hoc debug, never in committed code.

### 3 Auth

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $TOKEN" "https://api.example.com/me"
```

Checklist: token present? expired (`exp` in JWT)? scheme (Bearer / Basic / Token / `X-Api-Key`)? staging key on prod? header vs query param?

Decode JWT payload (no verify — debug only):

```python
import json, base64, os
tok = os.environ["TOKEN"].split(".")[1]
tok += "=" * (-len(tok) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(tok)), indent=2))
```

### 4 Request format

Prefer `requests.post(url, json=payload)` over `data=` with a lying `Content-Type`. Common failures: form vs JSON, missing fields, wrong method, unencoded query params, multipart boundary mistakes.

### 5–6 Parse and semantics

Inspect `Content-Type` before `.json()`. Then check IDs, enums, timezones, and pagination (`next_cursor` / `offset` / `total_count`).

## HTTP status playbook

| Code | Meaning | First checks |
|------|---------|--------------|
| 401 | Missing/invalid credentials | Header present? scheme? expiry? |
| 403 | Authenticated, not authorized | Scopes, ownership, IP allowlist, CORS |
| 404 | Missing resource or bad URL | Path, ID, API version, base URL env |
| 409 | Conflict | Duplicate create, stale ETag, concurrency |
| 422 | Valid JSON, invalid data | Field types, required, enums in body |
| 429 | Rate limited | `Retry-After`, backoff with jitter |
| 5xx | Server-side | Capture correlation ID; backoff; reduce payload |

## Pagination, idempotency, contracts

- Prefer cursor pagination for live data; verify you consume *all* pages.
- For non-idempotent POST (payments/orders), send `Idempotency-Key: <uuid>` on retries.
- Validate required fields/types after upgrades or third-party changes.

Always capture provider request IDs: `X-Request-Id`, `X-Trace-Id`, or `CF-Ray`.

## Security

- Never log full tokens. Redact: `Bearer <REDACTED>`.
- Read secrets from env, not hardcoded scripts.
- Prefer auth headers over query-string API keys.
- Treat HAR files and verbose curl logs as sensitive.

## Report format

```
## Finding
Endpoint: POST /api/v1/users
Status:   422
Req ID:   req_abc123

## Repro
curl ... (auth redacted)

## Root cause
Missing required field `email`.

## Fix / next step
...
```

## Completion criteria

1. Failing layer identified (connectivity → semantics).
2. Repro command run with redacted credentials and real status/body observed.
3. Root cause stated with evidence (or explicit blocker if env/network blocked repro).
4. If code fix needed, hand off to `debugging-assistant` / `test-first` after the API layer is clear.
