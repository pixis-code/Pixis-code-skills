# Revisions and comments: XML notes

Background for `docx_revisions.py` and `docx_comments.py`. Read when extending the scripts or debugging an odd file; normal use needs only SKILL.md.

## Tracked changes (`w:ins` / `w:del`)

Run-level changes are wrapper elements inside a `w:p` (namespace `http://schemas.openxmlformats.org/wordprocessingml/2006/main`):

```xml
<w:p>
  <w:r><w:t>Base </w:t></w:r>
  <w:ins w:id="1" w:author="Editor" w:date="2026-01-02T03:04:05Z">
    <w:r><w:t>inserted text</w:t></w:r>
  </w:ins>
  <w:del w:id="2" w:author="Editor" w:date="2026-01-02T03:04:05Z">
    <w:r><w:delText>deleted text</w:delText></w:r>
  </w:del>
</w:p>
```

- Deleted text sits in `w:delText`, not `w:t`, so plain extraction shows the "accepted" view.
- Resolution:
  - accept `w:ins`: unwrap (keep child runs)
  - reject `w:ins`: drop wrapper and contents
  - accept `w:del`: drop wrapper and contents
  - reject `w:del`: rename `w:delText` to `w:t`, then unwrap
- Revisions may appear in the body, table cells (nested too), headers, footers, and text boxes. The script scans the body root and each header/footer root with `root.iter(W+"ins", W+"del")`.
- `w:id` is unique per element, but one edit can yield several elements; `--id` acts on every element carrying that id.

Detected (via `docx_read.py --revisions`) but not resolved: paragraph-mark revisions (`w:rPr/w:ins` in `w:pPr`), table-row revisions (`w:trPr/w:ins`), format changes (`w:rPrChange`, `w:pPrChange`), and moves (`w:moveFrom`/`w:moveTo`). Open such files in Word instead of guessing.

## Comments

Three parts work together:

1. `word/comments.xml`: one `w:comment` per comment (`w:id`, `w:author`, `w:initials`, `w:date`, body paragraphs), linked by a `.../comments` relationship and a `[Content_Types].xml` override (python-docx adds the override when the part is registered).
2. Range markers: `w:commentRangeStart` / `w:commentRangeEnd` with matching `w:id` around the anchored runs.
3. A reference run containing `w:commentReference w:id="N"` right after the range end.

Script behavior:

- **list / delete** work on raw XML, so any producer's files are fine. `anchored_text` is the `w:t` text between the markers, in document order.
- **add** first isolates the target into whole runs, splitting at boundaries (copying `w:rPr` to keep formatting). On python-docx >= 1.2 it calls `document.add_comment(runs, ...)`; on older versions, or with `--xml`, it builds `comments.xml`, registers the part and relationship, and inserts markers and the reference run itself.
- **delete** removes the `w:comment` and all three marker kinds for that id, leaving document text alone.

Modern Word also writes `commentsExtended.xml` (threads, resolved state). The scripts neither read nor write it.
