---
name: reddit-reading
description: "Read Reddit: subreddits, search, threads, users. No browser."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Reddit, Social Media, Research, Discussions, Community]
    related_skills: [rss-feeds, grounded-citations]
---

# Reddit Reading

Reads Reddit — subreddit listings, search, full threads with comments, user
activity — from a server where normal routes are dead. Never posts, votes,
or logs in.

**Use for:** "what's r/X saying about Y" · summarize a thread · a shared
reddit.com URL (web_extract/browser_navigate/.json all 403 from server IPs
— this is the working path).
**Not for:** posting, voting, messaging, anything needing login.

## Setup

**None required.** Default backend is Reddit's public `.rss` feeds — the
only unauthenticated route server IPs still get. ~1 req/min/IP, thinner
data (no scores, top-level comments only).

**Optional upgrade** (still no login): register a free "script" app at
reddit.com/prefs/apps, set in `~/.pixis/.env`:
```
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
```
App-only `client_credentials` grant — never a password or cookie, never
acts as a user. Switches to OAuth automatically (~100 req/min, scores,
nested comments); falls back to anonymous feeds if missing/rejected.

| | Anonymous (default) | OAuth |
|---|---|---|
| Setup | none | 1-min app registration |
| Rate limit | ~1/min/IP | ~100/min |
| Data | post + top-level comments, no scores | nested comments, scores, counts |

## Commands

```bash
python3 scripts/reddit.py doctor                                  # active backend, rate-limit window
python3 scripts/reddit.py sub LocalLLaMA --sort hot --limit 15
python3 scripts/reddit.py search "query" --sub LocalLLaMA --sort new
python3 scripts/reddit.py thread https://www.reddit.com/r/x/comments/abc123/slug/ --limit 40
python3 scripts/reddit.py user spez --limit 10
python3 scripts/reddit.py --json search "topic"                   # machine-readable
```

The script picks the backend automatically — no flag needed. `sub` sorts:
hot/new/top/rising. `search` sorts: relevance/new/top/comments.

## Procedure

1. Run `doctor` once per session — shows active backend + remaining
   rate-limit window.
2. Plan calls first: anonymous is ~1 req/min/IP (a 429 sleeps out the
   window and retries once — 5 calls ≈ 5 min). Prefer one `search --sub`
   over several `sub` listings; read one thread, not a whole listing.
3. For "what's the community saying," read `thread` bodies, not just
   listing titles (listings truncate to ~300 chars).
4. Cite the `url` (permalink), not the listing page — `grounded-citations`
   registers it like any other source.
5. Need sustained access (monitoring, 10+ calls)? Ask the user to register
   app credentials rather than grinding the throttle — it's a free app
   registration, not a login. Never ask for a password or cookies.

## Pitfalls

- `.json`, `api.reddit.com`, `old.reddit.com` → 403/empty shell from
  server IPs. Don't retry them, don't spoof a browser User-Agent (also 403).
- Anonymous thread feeds cap at a handful of entries, top-level only —
  scores/nesting are OAuth-only.
- Reddit's `limit` is advisory — expect 5–25 entries regardless of ask.
- Never put `REDDIT_CLIENT_SECRET` in chat or logs — env var only.
- A 429 means wait once (the script already does); repeated 429s mean the
  task needs app credentials, not a retry loop.

## Verification

`doctor` → `anonymous_feed: ok` + an `x-ratelimit-reset` value.
`sub announcements --limit 1` → one entry with a
`reddit.com/r/announcements/comments/` URL. With credentials, `doctor` →
`active_backend: oauth` and `thread` shows numeric scores.
