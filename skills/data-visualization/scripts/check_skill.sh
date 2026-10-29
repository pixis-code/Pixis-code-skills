#!/bin/bash
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
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: data-visualization$' "$SKILL"; then
  record "frontmatter name" 1 "ok"; else record "frontmatter name" 0 "bad"; fi
grep -q 'author: Pixis' "$SKILL" && record "author Pixis" 1 "ok" || record "author Pixis" 0 "missing"
grep -q 'pixis:' "$SKILL" && record "metadata.pixis" 1 "ok" || record "metadata.pixis" 0 "missing"
desc_ok=1
echo "$DESC" | grep -qiE 'chart|graph|plot|visual' || desc_ok=0
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
echo "$DESC" | grep -qiE 'jupyter-notebook|xlsx|excalidraw|model-deployment' && record "negative cue" 1 "ok" || record "negative cue" 0 "missing"
[ -f "$ROOT/scripts/plot_data.py" ] && record "plot_data.py" 1 "ok" || record "plot_data.py" 0 "missing"
[ -f "$ROOT/scripts/ensure_deps.sh" ] && record "ensure_deps.sh" 1 "ok" || record "ensure_deps.sh" 0 "missing"
grep -qi 'Do not overwrite the source' "$SKILL" && record "no source mutate" 1 "ok" || record "no source mutate" 0 "missing"
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
