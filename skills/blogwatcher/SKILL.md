---
name: blogwatcher
description: "Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool."
version: 2.0.0
author: Pixis (wraps JulienTant/blogwatcher-cli)
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [RSS, Blogs, Feed-Reader, Monitoring]
    homepage: https://github.com/JulienTant/blogwatcher-cli
prerequisites:
  commands: [blogwatcher-cli]
---

# Blogwatcher

Tracks blog/RSS/Atom updates via the external `blogwatcher-cli` tool —
auto feed discovery, HTML-scrape fallback, OPML import, read/unread state.

**When to reach for this vs. alternatives:**
- **Recurring watch** — schedule a tick that runs
  `blogwatcher-cli scan >/dev/null 2>&1 && blogwatcher-cli articles`
  (deterministic: unchanged output = no new articles = skip the LLM call;
  changed output = new articles, act on the diff).
- **Reading an article the user asks about** — `web_extract([url])` on the
  article URL from `blogwatcher-cli articles`; don't re-scrape by hand.
- **One-off "watch this page for changes," no feed semantics** — skip
  this skill; point your scheduler straight at the URL.
- **One-off read, nothing to install** — use `rss-feeds`
  (`scripts/feed.py read URL`); blogwatcher earns its install once you're
  tracking many feeds with read/unread state.
- **Competitor tracking with analysis + citations** — prefer
  `competitor-news-monitor`; blogwatcher is the lighter raw-feed layer
  under it.

## Install

- Go: `go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`
- Docker: `docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli`
- Binary (Linux amd64/arm64, macOS Apple Silicon/Intel):
  `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_<platform>.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
  (platform = `linux_amd64`, `linux_arm64`, `darwin_arm64`, `darwin_amd64`)

All releases: github.com/JulienTant/blogwatcher-cli/releases

**Docker persistence** — the DB defaults to
`~/.blogwatcher-cli/blogwatcher-cli.db`, lost on container restart unless
mounted:
```bash
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

**Migrating from the original `Hyaxia/blogwatcher`:**
`mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db`
(binary renamed `blogwatcher` → `blogwatcher-cli`).

## Commands

**Managing blogs:** `add "Name" URL` · `add "Name" URL --feed-url FEED` ·
`add "Name" URL --scrape-selector "article h2 a"` · `blogs` (list) ·
`remove "Name" --yes` · `import subscriptions.opml`

**Scanning/reading:** `scan` (all) · `scan "Name"` (one) · `articles`
(unread) · `articles --all` · `articles --blog "Name"` ·
`articles --category "Cat"` · `read N` · `unread N` · `read-all` ·
`read-all --blog "Name" --yes`

## Environment Variables (`BLOGWATCHER_` prefix on any flag)

`BLOGWATCHER_DB` (SQLite path) · `BLOGWATCHER_WORKERS` (default 8) ·
`BLOGWATCHER_SILENT` (quiet scans) · `BLOGWATCHER_YES` (skip confirms) ·
`BLOGWATCHER_CATEGORY` (default category filter).

## Example Output

```
$ blogwatcher-cli blogs
Tracked blogs (1):
  xkcd
    URL: https://xkcd.com
    Feed: https://xkcd.com/atom.xml
    Last scanned: 2026-04-03 10:30

$ blogwatcher-cli scan
Scanning 1 blog(s)...
  xkcd
    Source: RSS | Found: 4 | New: 4
Found 4 new article(s) total!

$ blogwatcher-cli articles
Unread articles (2):
  [1] [new] Barrel - Part 13
       Blog: xkcd | URL: https://xkcd.com/3095/
       Published: 2026-04-02 | Categories: Comics, Science
```

## Notes

- Auto-discovers RSS/Atom from a blog homepage when no `--feed-url` given.
- Falls back to HTML scraping if RSS fails and `--scrape-selector` is set.
- Categories from feeds are stored and filterable.
- Bulk-import OPML from Feedly, Inoreader, NewsBlur, etc.
- DB at `~/.blogwatcher-cli/blogwatcher-cli.db` by default (`--db` or
  `BLOGWATCHER_DB` to override).
- `blogwatcher-cli <command> --help` for full flag list.
