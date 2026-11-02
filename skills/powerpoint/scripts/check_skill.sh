#!/bin/bash
# Local hygiene + routing fixtures for powerpoint
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
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: powerpoint$' "$SKILL"; then
  record "frontmatter name is powerpoint" 1 "ok"
else record "frontmatter name" 0 "bad"; fi
grep -q 'author: Pixis' "$SKILL" && record "author Pixis" 1 "ok" || record "author Pixis" 0 "missing"
grep -q 'metadata:' "$SKILL" && grep -q 'pixis:' "$SKILL" && record "metadata.pixis" 1 "ok" || record "metadata.pixis" 0 "missing"
desc_ok=1
echo "$DESC" | grep -qiE 'pptx|PowerPoint|python-pptx|slides|deck' || desc_ok=0
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
echo "$DESC" | grep -qiE 'pptx|PowerPoint|python-pptx|slides|deck' && record "positive cue" 1 "ok" || record "positive cue" 0 "missing"
echo "$DESC" | grep -qiE 'pdf|google-workspace|notion' && record "negative cue" 1 "ok" || record "negative cue" 0 "missing"
for f in scripts/pptx_create.py scripts/pptx_read.py scripts/pptx_edit.py references/design.md LICENSE; do
  [ -f "$ROOT/$f" ] && record "asset $f" 1 "ok" || record "asset $f" 0 "missing"
done
grep -qi 'professional' "$SKILL" && record "theme guidance" 1 "ok" || record "theme guidance" 0 "missing"
grep -q 'THEMES' "$ROOT/scripts/pptx_create.py" && record "create themes" 1 "ok" || record "create themes" 0 "missing"
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
