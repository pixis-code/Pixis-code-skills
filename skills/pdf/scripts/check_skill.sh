#!/bin/bash
# Local hygiene + routing fixtures for pdf
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
record() {
  local n="$1" ok="$2" detail="$3"
  if [ "$ok" = "1" ]; then echo "PASS: $n — $detail"; PASS=$((PASS+1))
  else echo "FAIL: $n — $detail"; FAIL=$((FAIL+1)); fi
}
SKILL="$ROOT/SKILL.md"
DESC=$(grep -E '^description:' "$SKILL" | head -1)
[ -f "$SKILL" ] && record "SKILL.md exists" 1 "ok" || record "SKILL.md exists" 0 "missing"
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: pdf$' "$SKILL"; then
  record "frontmatter name is pdf" 1 "ok"
else record "frontmatter name" 0 "bad"; fi
grep -q 'author: Pixis' "$SKILL" && record "author Pixis" 1 "ok" || record "author Pixis" 0 "missing"
grep -q 'metadata:' "$SKILL" && grep -q 'pixis:' "$SKILL" && record "metadata.pixis" 1 "ok" || record "metadata.pixis" 0 "missing"
desc_ok=1
echo "$DESC" | grep -qiE 'PDF|create|merge|OCR|forms' || desc_ok=0
echo "$DESC" | grep -qiE 'use when|not for' || desc_ok=0
record "description WHAT/WHEN/NOT" "$desc_ok" "router"
body_ok=1
grep -qiE 'When to use' "$SKILL" || body_ok=0
grep -qiE 'Do not use' "$SKILL" || body_ok=0
grep -qiE 'Completion criteria' "$SKILL" || body_ok=0
record "body gates" "$body_ok" "sections"
if grep -qiE 'HERMES_HOME|delegate_task|skill_view|hermes setup|`search_files`|`read_file`|`terminal`|vision_analyze|browser_navigate' "$SKILL"; then
  record "no Hermes runtime tools" 0 "found"
else record "no Hermes runtime tools" 1 "ok"; fi
echo "$DESC" | grep -qiE 'PDF|create|merge|OCR|forms' && record "positive cue" 1 "ok" || record "positive cue" 0 "missing"
echo "$DESC" | grep -qiE 'google-workspace|powerpoint|notion' && record "negative cue" 1 "ok" || record "negative cue" 0 "missing"
for f in scripts/pdf_create.py scripts/pdf_read.py scripts/pdf_merge.py references/forms.md references/styling.md LICENSE; do
  [ -f "$ROOT/$f" ] && record "asset $f" 1 "ok" || record "asset $f" 0 "missing"
done
grep -qi 'professional' "$SKILL" && record "professional theme guidance" 1 "ok" || record "professional theme guidance" 0 "missing"
grep -qi 'callout\|bullet_list' "$SKILL" && record "rich elements documented" 1 "ok" || record "rich elements" 0 "missing"
if grep -q 'professional' "$ROOT/scripts/pdf_create.py" && grep -q 'THEMES' "$ROOT/scripts/pdf_create.py"; then
  record "pdf_create themes" 1 "ok"
else
  record "pdf_create themes" 0 "missing"
fi
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
