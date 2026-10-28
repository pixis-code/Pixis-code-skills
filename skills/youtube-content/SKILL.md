---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [YouTube, Video, Transcripts, Media]
    related_skills: [rss-feeds]
---

# YouTube Content

**Use when:** the user shares a YouTube URL, asks to summarize a video,
requests a transcript, or wants video content reformatted (chapters,
summary, thread, blog post).

## Setup

Needs the `youtube-transcript-api` package:

```bash
pip install --break-system-packages youtube-transcript-api
python -c "import youtube_transcript_api; print(youtube_transcript_api.__file__)"
```

Run commands with whichever interpreter's import check succeeded.

## Commands

`SKILL_DIR` = this skill's folder. Accepts any YouTube URL format (full,
`youtu.be`, shorts, embed, live) or a raw 11-char video ID.

```bash
python SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"    # JSON + metadata
python SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only                          # plain text
python SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps                         # with timestamps
python SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en                     # language + fallback chain
```

## Output Formats

Pick based on what the user asked for — **chapters** (timestamped,
grouped by topic shift) · **summary** (5-10 sentences) · **chapter
summaries** (chapters + short paragraph each) · **thread** (numbered
posts, <280 chars each) · **blog post** (title + sections + takeaways) ·
**quotes** (notable lines + timestamps). Examples and templates in
`references/output-formats.md`.

## Workflow

1. Fetch with `--text-only --timestamps`.
2. Validate: non-empty, expected language. Empty → retry without
   `--language` for any available transcript; still empty → tell the user
   transcripts are likely disabled.
3. Chunk if >~50K chars: overlapping ~40K chunks with 2K overlap,
   summarize each, then merge.
4. Transform into the requested format (default: summary if unspecified).
5. Re-read the output for coherence, correct timestamps, completeness
   before presenting.

## Error Handling

- **Transcripts disabled** — tell the user, suggest checking if subtitles
  exist on the video page.
- **Private/unavailable video** — relay the error, ask them to verify the URL.
- **No matching language** — retry without `--language`, note the actual
  language returned.
- **Dependency missing** — re-run the pip install above and re-check the import.
