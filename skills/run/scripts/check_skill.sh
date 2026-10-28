#!/bin/bash
# Local hygiene + routing fixtures for run — no live agent session required.
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

if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: run$' "$SKILL"; then
  record "frontmatter name is run" 1 "ok"
else
  record "frontmatter name is run" 0 "bad frontmatter"
fi

grep -q 'category: Developer Workflow' "$SKILL" \
  && record "category Developer Workflow" 1 "ok" \
  || record "category Developer Workflow" 0 "missing"

desc_ok=1
echo "$DESC" | grep -qiE 'run|execute|command' || desc_ok=0
echo "$DESC" | grep -qiE 'use when|when the user' || desc_ok=0
echo "$DESC" | grep -qiE 'not for|test-first|app-qa|code-explainer' || desc_ok=0
record "description has WHAT/WHEN/NOT" "$desc_ok" "router blurb"

gate_ok=1
grep -qi 'Do not use' "$SKILL" || gate_ok=0
grep -qi 'Completion criteria' "$SKILL" || gate_ok=0
grep -qi 'stop and ask' "$SKILL" || gate_ok=0
grep -qi 'test-first' "$SKILL" || gate_ok=0
grep -qi 'code-explainer' "$SKILL" || gate_ok=0
record "body has exclusions, completion, stop-ask, handoffs" "$gate_ok" "gates"

if grep -qE 'delegate_task|search_files|HERMES_HOME|read_file`|`terminal`|hermes' "$SKILL"; then
  record "no Hermes tool assumptions" 0 "found hermes-specific names"
else
  record "no Hermes tool assumptions" 1 "ok"
fi

pos_ok=1
echo "$DESC" | grep -qiE 'run|build|start|execute' || pos_ok=0
record "positive cue: run/build/start in description" "$pos_ok" "run the app"

neg_ok=1
echo "$DESC" | grep -qi 'test-first' || neg_ok=0
echo "$DESC" | grep -qiE 'not for|code-explainer' || neg_ok=0
record "negative cue: TDD/explain excluded" "$neg_ok" "fix with TDD / explain → not this skill"

echo ""
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
