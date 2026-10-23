#!/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
record() {
  local n="$1" ok="$2" d="$3"
  if [ "$ok" = "1" ]; then echo "PASS: $n — $d"; PASS=$((PASS+1))
  else echo "FAIL: $n — $d"; FAIL=$((FAIL+1)); fi
}
SKILL="$ROOT/SKILL.md"
DESC=$(grep -E '^description:' "$SKILL" | head -1)
[ -f "$SKILL" ] && record "SKILL.md exists" 1 "ok" || record "SKILL.md exists" 0 "missing"
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: pr-lens$' "$SKILL"; then
  record "frontmatter name is pr-lens" 1 "ok"
else record "frontmatter name" 0 "bad"; fi
grep -q 'author: Pixis' "$SKILL" && record "author Pixis" 1 "ok" || record "author Pixis" 0 "missing"
grep -q 'category: Software Development' "$SKILL" && record "category" 1 "ok" || record "category" 0 "missing"
desc_ok=1
echo "$DESC" | grep -qiE 'use when|not for' || desc_ok=0
record "description WHAT/WHEN/NOT" "$desc_ok" "router"
gate_ok=1
grep -qi 'When to use' "$SKILL" || gate_ok=0
grep -qi 'Do not use' "$SKILL" || gate_ok=0
grep -qi 'Completion criteria' "$SKILL" || gate_ok=0

record "body gates" "$gate_ok" "sections"
if grep -qE 'delegate_task|HERMES_HOME|kanban_show|kanban_complete|`search_files`|`read_file`|`terminal`|~/.hermes' "$SKILL"; then
  record "no Hermes runtime tools" 0 "found"; else record "no Hermes runtime tools" 1 "ok"; fi
echo "$DESC" | grep -qiE 'diagram|SVG|architecture|data-flow|PR Lens' && record "positive cue" 1 "ok" || record "positive cue" 0 "missing"
echo "$DESC" | grep -qiE 'self-review|code-explainer|codebase-documentation' && record "negative cue" 1 "ok" || record "negative cue" 0 "missing"
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
