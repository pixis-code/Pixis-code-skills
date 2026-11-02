# PDF create styling guide

Use with `scripts/pdf_create.py`. Performance reports use theme **business**
(widescreen, navy cover, gold rules). Omitting `theme` stays on **professional**.

## Why specs looked B&W before

Older specs used only `heading` + `paragraph` + grey tables with ReportLab’s
stock stylesheet. Always set a color theme and use lists/callouts/tables.

## Minimal good report

```json
{
  "title": "Weekly Ops Report",
  "subtitle": "Week of 2026-03-01",
  "theme": "business",
  "page_size": "widescreen",
  "brand": "Growlio Demo",
  "footer": "Growlio Demo • Quarterly Business Performance Report",
  "elements": [
    {"type": "heading", "text": "Status", "level": 1},
    {"type": "callout", "text": "All SLAs met. One Sev-3 open.", "style": "success"},
    {"type": "bullet_list", "items": ["API latency p95: 180ms", "Error rate: 0.12%"]},
    {"type": "heading", "text": "Metrics", "level": 2},
    {"type": "table", "header": true, "rows": [
      ["Service", "Uptime", "Tickets"],
      ["API", "99.95%", "3"],
      ["Web", "99.99%", "1"]
    ]}
  ]
}
```

## Theme cheat sheet

- `business` — navy `#0E1F38`, gold `#E89B3C`, teal eyebrow — board / performance reports
- `professional` — blue (#1F4E79) — shorter documents when theme is omitted
- `midnight` — indigo — product/eng reviews
- `forest` — green — sustainability / finance positive
- `plain` — greyscale — only when explicitly requested

Override accent: `"accent": "#B45309"`.

## Inline markup in paragraphs

ReportLab Paragraph subset: `<b>bold</b>`, `<i>italic</i>`, `<br/>`,
`<font color="red">…</font>` (use sparingly).
