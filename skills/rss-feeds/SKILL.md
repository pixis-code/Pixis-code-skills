---
name: rss-feeds
description: "Read RSS, Atom, JSON feeds; discover feeds behind a page."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [RSS, Atom, Feeds, Monitoring, Research, Blogs, Releases]
    related_skills: [reddit-reading, competitor-news-monitor, grounded-citations, youtube-content, blogwatcher]
---

# RSS Feeds

Reads RSS 2.0/1.0 (RDF), Atom, or JSON Feed URLs into a clean, date-sorted
list, and discovers the feed behind an ordinary page (`<link
rel="alternate">` or common `/feed`, `/rss.xml`, `/atom.xml` paths). Stdlib
only. Doesn't fetch full article bodies — pass an entry's `link` to
`web_extract` for that.

**Use for:** "what's new on X" · latest GitHub releases · recent subreddit
posts · "read this feed" · "does this site have RSS". A recurring digest
(feeds are cheaper/more stable than scraping a front page each run — for
persistent read/unread tracking across many feeds, use `blogwatcher`; this
is the zero-install read). Anywhere a structured `title/link/date/
author/summary` list beats a rendered page: podcasts, changelogs, YouTube
channels, newsrooms, forum categories.

## Setup

None. Python 3.10+, network access to the feed host.

## Commands

```bash
python3 scripts/feed.py read https://hnrss.org/frontpage --limit 10
python3 scripts/feed.py read https://example.com/              # page URL → auto-discovers feed
python3 scripts/feed.py read URL --since 2026-09-01 --json     # only newer entries, machine-readable
python3 scripts/feed.py discover https://example.com/          # list candidate feed URLs
```

## Common Feed URLs

GitHub: `github.com/OWNER/REPO/releases.atom` (also `/commits/BRANCH.atom`,
`/tags.atom`) · Reddit: `reddit.com/r/NAME/.rss`,
`reddit.com/search.rss?q=…` (1 req/min anon — see `reddit-reading`) ·
YouTube: `youtube.com/feeds/videos.xml?channel_id=UC…` · Hacker News:
`hnrss.org/frontpage`, `hnrss.org/newest?q=TERM` · arXiv:
`rss.arxiv.org/rss/cs.CL` · Substack/Medium/WordPress/Ghost:
`SITE/feed`, `medium.com/feed/@user`, `SITE/rss/` · podcasts: use
`discover` on the show's page.

Output per entry: `title`, `link`, `published` (UTC ISO 8601), `author`,
`summary` (HTML stripped, ≤2000 chars). Sorted newest-first.

## Procedure

1. Have only a site URL? Run `read` on it directly — the script discovers
   the feed and reports `discovered_from`. Use `discover` to pick between
   several advertised feeds (comments vs posts, per-category).
2. Bound the request: `--limit` for "latest N", `--since YYYY-MM-DD` for
   "since last check". For a recurring digest, persist the last-seen
   `published` value and pass it as `--since` next run.
3. For full text, hand the entry `link` to `web_extract` — summaries are
   often truncated or first-paragraph-only.
4. Cite the entry `link`, not the feed URL, in a report
   (`grounded-citations`).

## Pitfalls

- A 200 with HTML means it's a page, not a feed — the script auto-falls
  through to discovery, but a site with no `<link rel="alternate">` and
  none of the common paths reports "no feed found." Check the site's
  footer or `/sitemap.xml` before concluding there's none.
- Reddit feeds share Reddit's anonymous throttle (~1 req/min/IP) — chain
  through `reddit-reading` for more than one Reddit call.
- RSS `pubDate` is RFC 822, Atom is ISO 8601 — the script normalizes both
  to UTC. Feeds that omit dates sort last and drop from `--since`.
- Some feeds are Cloudflare-fronted and 403 non-browser clients.

## Verification

`read https://github.com/OWNER/REPO/releases.atom --limit 1` prints one
entry with a `releases/tag/` link and `[atom]` format tag.
`discover https://example.com/` prints a feed URL.
