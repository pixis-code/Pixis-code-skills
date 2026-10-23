#!/bin/bash
# Local hygiene + routing fixtures for technical-plan-challenger
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
record() {
  local name="$1" ok="$2" detail="$3"
  if [ "$ok" = "1" ]; then echo "PASS: $name — $detail"; PASS=$((PASS+1))
  else echo "FAIL: $name — $detail"; FAIL=$((FAIL+1)); fi
}
SKILL="$ROOT/SKILL.md"
DESC=$(grep -E "^description:" "$SKILL" | head -1)
[ -f "$SKILL" ] && record "SKILL.md exists" 1 "ok" || record "SKILL.md exists" 0 "missing"
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: technical-plan-challenger$' "$SKILL"; then
  record "frontmatter name is technical-plan-challenger" 1 "ok"
else record "frontmatter name" 0 "bad"; fi
grep -q "author: Pixis" "$SKILL" && record "author Pixis" 1 "ok" || record "author Pixis" 0 "missing"
desc_ok=1
echo "$DESC" | grep -qiE 'plan|adversarial|challenge|interview' || desc_ok=0
echo "$DESC" | grep -qiE "use when|not for" || desc_ok=0
record "description WHAT/WHEN/NOT" "$desc_ok" "router"
body_ok=1
grep -qiE 'When to use' "$SKILL" || body_ok=0
grep -qiE 'Do not use' "$SKILL" || body_ok=0
grep -qiE 'frontier' "$SKILL" || body_ok=0
grep -qiE 'Completion criteria' "$SKILL" || body_ok=0
record "body gates" "$body_ok" "sections"
if grep -qE "delegate_task|HERMES_HOME|\`search_files\`|\`read_file\`|\`terminal\`|browser_navigate|execute_code\(" "$SKILL"; then
  record "no Hermes runtime tools" 0 "found"; else record "no Hermes runtime tools" 1 "ok"; fi
echo "$DESC" | grep -qiE 'plan|adversarial|challenge|interview' && record "positive cue" 1 "ok" || record "positive cue" 0 "missing"
echo "$DESC" | grep -qiE 'feasibility|self-review|implement' && record "negative cue" 1 "ok" || record "negative cue" 0 "missing"
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
