---
name: xurl
description: "X/Twitter via xurl CLI: raw post search, posting, DM, media."
version: 1.1.3
author: Pixis (wraps xdevplatform/xurl)
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [xurl]
metadata:
  pixis:
    tags: [twitter, x, social-media, xurl, official-api]
    homepage: https://github.com/xdevplatform/xurl
---

# xurl — X (Twitter) API via the Official CLI

X's official developer-platform CLI: shortcut commands for common actions
plus raw curl-style access to any v2 endpoint. All commands return JSON.

**Covers:** post/reply/quote/delete · search raw posts (with IDs you can
act on), read timelines/mentions · like/repost/bookmark · follow/unfollow/
block/mute · DMs · media upload (image/video) · raw v2 endpoint access ·
multi-app/multi-account.

OAuth 2.0 PKCE with auto-refresh; maintained by the X dev platform team.

## Secret Safety (MANDATORY)

- **Never** read, print, parse, summarize, upload, or send `~/.xurl` to
  LLM context.
- **Never** ask the user to paste credentials/tokens into chat.
- The user fills `~/.xurl` with secrets manually, on their own machine —
  not through this skill.
- **Never** recommend or execute auth commands with inline secrets in an
  agent session.
- **Never** use `--verbose`/`-v` here — it can expose auth headers/tokens.
- To check credentials exist, only use: `xurl auth status`.

**Forbidden flags in agent commands** (accept inline secrets):
`--bearer-token`, `--consumer-key`, `--consumer-secret`, `--access-token`,
`--token-secret`, `--client-id`, `--client-secret`.

App registration and credential rotation happen outside the agent
session; so does `xurl auth oauth2`. Tokens persist to `~/.xurl` (YAML),
isolated per app, auto-refreshing.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash   # shell script, no sudo
brew install --cask xdevplatform/tap/xurl                                               # macOS
npm install -g @xdevplatform/xurl
go install github.com/xdevplatform/xurl@latest
```
Verify: `xurl --help` · `xurl auth status`

## One-Time User Setup (user runs these, not the agent — pastes secrets)

1. Create/open an app at developer.x.com/en/portal/dashboard; set redirect
   URI to `http://localhost:8080/callback`; copy Client ID + Secret.
2. `xurl auth apps add my-app --client-id ID --client-secret SECRET`
3. `xurl auth oauth2 --app my-app` (opens browser for PKCE flow). If X
   returns `UsernameNotFound`/403 on the post-OAuth lookup, append your
   handle: `xurl auth oauth2 --app my-app YOUR_USERNAME` (v1.1.0+).
4. `xurl auth default my-app` — binds all commands to this app.
5. Verify: `xurl auth status` · `xurl whoami`

Agent can use any command below once this is done; tokens auto-refresh.

**Pitfall:** omitting `--app my-app` from `auth oauth2` saves the token to
the built-in `default` profile (no client-id/secret) — commands then fail
auth even though OAuth looked successful. Fix: re-run
`xurl auth oauth2 --app my-app` then `xurl auth default my-app`.

**Containerized runtime pitfall:** if the agent's subprocess `HOME`
differs from the shell's interactive `HOME` (common in Docker), `~/.xurl`
resolves against the subprocess one. Run setup with that same `HOME`
explicitly, e.g. `HOME=/path/used/by/subprocess xurl auth status`, and
confirm it (not the interactive shell's `HOME`) shows the registered app.

## Quick Reference

| Action | Command |
|---|---|
| Post / Reply / Quote / Delete | `post "text"` / `reply ID "text"` / `quote ID "text"` / `delete ID` |
| Read / Search | `read ID` / `search "QUERY" -n 10` |
| Who am I / Look up user | `whoami` / `user @handle` |
| Timeline / Mentions | `timeline -n 20` / `mentions -n 10` |
| Like / Unlike | `like ID` / `unlike ID` |
| Repost / Undo | `repost ID` / `unrepost ID` |
| Bookmark / Remove / List | `bookmark ID` / `unbookmark ID` / `bookmarks -n 10` |
| List likes | `likes -n 10` |
| Follow / Unfollow | `follow @handle` / `unfollow @handle` |
| Following / Followers | `following -n 20` / `followers -n 20` |
| Block / Mute (+ undo) | `block`/`unblock` / `mute`/`unmute @handle` |
| DM send / list | `dm @handle "msg"` / `dms -n 10` |
| Media upload / status | `media upload FILE` / `media status ID` |
| Apps: list / remove / set default | `auth apps list` / `auth apps remove NAME` / `auth default APP [USER]` |
| Per-request app / Auth status | `--app NAME /2/users/me` / `auth status` |

`POST_ID` accepts full URLs (ID is extracted). Usernames work with or
without `@`.

## Command Notes

- **Media on a post:** `post "text" --media-id ID` (repeat `--media-id`
  for multiple). Upload first (`media upload file.mp4`), check processing
  on video (`media status --wait ID`).
- **Search** returns raw post objects (IDs, authors, full text) as your
  authenticated account — use it when you need actual posts, not a
  summary. `search "from:user"`, `search "#tag lang:en" -n 15`.
- **X Articles**: use raw API, not `read` (which expects a post ID/URL).
  Request the `article` field and read `data.article.plain_text`:
  `xurl --app APP '/2/tweets/ID?tweet.fields=...,article'`
- **Graph for another user**: `following --of handle -n 20`.
- **Multiple apps**: `auth default prod alice` then
  `xurl --app staging /2/users/me` for a one-off against staging.

## Raw API Access

```bash
xurl /2/users/me                                        # GET
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'     # POST + JSON body
xurl -X DELETE /2/tweets/ID                              # DELETE/PUT/PATCH
xurl -H "Content-Type: application/json" /2/some/endpoint
xurl -s /2/tweets/search/stream                          # force streaming
```
Known streaming endpoints (auto-detected): `/2/tweets/search/stream`,
`/2/tweets/sample/stream`, `/2/tweets/sample10/stream`. Force with `-s`.

## Global Flags

| Flag | Short | What |
|---|---|---|
| `--app` | | use a specific registered app (overrides default) |
| `--auth` | | force auth type: `oauth1`/`oauth2`/`app` |
| `--username` | `-u` | which OAuth2 account, if multiple |
| `--verbose` | `-v` | **forbidden in agent sessions** — leaks auth headers |
| `--trace` | `-t` | add `X-B3-Flags: 1` trace header |

JSON to stdout, mirroring X API v2: `{ "data": { "id": "...", "text": "..." } }`.
Errors too: `{ "errors": [ { "message": "Not authorized", "code": 403 } ] }`.
Non-zero exit on any error; API errors still print as parseable JSON. Write
actions needing the caller's user ID (like/repost/bookmark/follow)
auto-fetch it via `/2/users/me` — an auth failure there surfaces as an
auth error.

## Agent Workflow

1. Verify prerequisites: `xurl --help`, `xurl auth status`.
2. Reach for `search` when the task needs actual post objects or
   authenticated context — not for a topic summary.
3. Check the default app has credentials: the `▸` marks it in `auth
   status`. If it shows `oauth2: (none)` while another app has a valid
   user, tell the user to `xurl auth default <that-app>` — the most
   common setup mistake.
4. Auth missing entirely → stop, point the user to One-Time User Setup.
   Never register apps or pass secrets yourself.
5. Start with a cheap read (`whoami`, `user @handle`, `search ... -n 3`)
   to confirm reachability.
6. Confirm target post/user and intent before any write action.
7. Only the `xurl` output (or raw X API response) proves a write
   happened — never report one done from search results or prior context.
8. Use JSON output directly; it's already structured.
9. Never paste `~/.xurl` contents into the conversation.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Auth errors after OAuth succeeded | Token saved to `default` app, not your named one | `xurl auth oauth2 --app my-app` then `auth default my-app` |
| `unauthorized_client` during OAuth | App type = "Native App" | Change to "Web app, automated app or bot" |
| `UsernameNotFound`/403 on `/2/users/me` post-OAuth | X not returning username reliably | `xurl auth oauth2 --app my-app YOUR_USERNAME` |
| 401 on every request | Expired token / wrong default | `auth status` — check `▸` points to an app with oauth2 tokens |
| `client-forbidden`/`client-not-enrolled` | Platform enrollment issue | Dashboard → Apps → Manage → "Pay-per-use" → Production |
| `CreditsDepleted` | $0 API balance | Buy credits (min $5) → Billing |
| `media processing failed` on image | Default category is `amplify_video` | Add `--category tweet_image --media-type image/png` |
| Two "Client Secret" values shown | UI bug — first is actually Client ID | Confirm on "Keys and tokens" page; ID ends `MTpjaQ` |

## Notes

- **Rate limits**: per-endpoint; 429 = wait and retry. Writes are tighter than reads.
- **Scopes**: broad OAuth2 scopes; a 403 on one action usually means a
  missing scope — re-run `auth oauth2`.
- **Token refresh**: automatic, nothing to do.
- **Multiple apps/accounts**: isolated per app; switch with `auth
  default`/`--app`; pick account with `-u`/`--username`.
- **Token storage**: `~/.xurl` (YAML) — resolve against the agent
  runtime's actual subprocess `HOME`. Never read or send it to LLM context.
- **Cost**: meaningful usage is typically paid; many failures are
  plan/permission issues, not code bugs.

## Attribution

Upstream CLI: github.com/xdevplatform/xurl (X developer platform team).
