#!/bin/bash
# Local hygiene + routing fixtures for debugging-assistant — no live agent session required.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

record() {
  local name="$1" ok="$2" detail="$3"
  if [ "$ok" = "1" ]; then
    echo "PASS: $name — $detail"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $name — $detail"
    FAIL=$((FAIL + 1))
  fi
}

SKILL="$ROOT/SKILL.md"
DESC=$(grep -E '^description:' "$SKILL" | head -1)

[ -f "$SKILL" ] && record "SKILL.md exists" 1 "ok" || record "SKILL.md exists" 0 "missing"

if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: debugging-assistant$' "$SKILL"; then
  record "frontmatter name is debugging-assistant" 1 "ok"
else
  record "frontmatter name is debugging-assistant" 0 "bad frontmatter"
fi

grep -q 'category: Software Development' "$SKILL" \
  && record "category Software Development" 1 "ok" \
  || record "category Software Development" 0 "missing"

desc_ok=1
echo "$DESC" | grep -qiE 'root-cause|debug|traceback|investigat' || desc_ok=0
echo "$DESC" | grep -qiE 'use when|when investigating' || desc_ok=0
echo "$DESC" | grep -qiE 'not for|code-explainer|code-refactoring' || desc_ok=0
record "description has WHAT/WHEN/NOT" "$desc_ok" "router blurb"

gate_ok=1
grep -qi 'Iron law' "$SKILL" || gate_ok=0
grep -qi 'Phase 1' "$SKILL" || gate_ok=0
grep -qi 'test-first' "$SKILL" || gate_ok=0
grep -qi 'Completion criteria' "$SKILL" || gate_ok=0
grep -qi 'Do not claim' "$SKILL" || gate_ok=0
record "body has iron law, phases, test-first, evidence, completion" "$gate_ok" "gates"

# Forbid Hermes runtime tool / path assumptions (attribution in prose is OK)
if grep -qE 'delegate_task|HERMES_HOME|`search_files`|`read_file`|`terminal`|browser_navigate|dogfood' "$SKILL"; then
  record "no Hermes runtime tool assumptions" 0 "found hermes-specific runtime names"
else
  record "no Hermes runtime tool assumptions" 1 "ok"
fi

pos_ok=1
echo "$DESC" | grep -qiE 'traceback|bug|root-cause|investigat|error' || pos_ok=0
record "positive cue: investigate/fix in description" "$pos_ok" "Investigate and fix this traceback"

neg_ok=1
echo "$DESC" | grep -qi 'code-explainer' || neg_ok=0
echo "$DESC" | grep -qiE 'not for|read-only explanation|explain' || neg_ok=0
record "negative cue: explain-only excluded" "$neg_ok" "Explain without changing → not this skill"

echo ""
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
