#!/bin/bash
# Local hygiene + routing fixtures for code-explainer — no live agent session required.
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

if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: code-explainer$' "$SKILL"; then
  record "frontmatter name is code-explainer" 1 "ok"
else
  record "frontmatter name is code-explainer" 0 "bad frontmatter"
fi

grep -q 'category: Software Development' "$SKILL" \
  && record "category Software Development" 1 "ok" \
  || record "category Software Development" 0 "missing"

# WHAT + WHEN + NOT in description
desc_ok=1
echo "$DESC" | grep -qi 'explain' || desc_ok=0
echo "$DESC" | grep -qiE 'use when|when the user' || desc_ok=0
echo "$DESC" | grep -qiE 'not for|debugging-assistant|code-refactoring' || desc_ok=0
record "description has WHAT/WHEN/NOT" "$desc_ok" "router blurb"

# Body gates
gate_ok=1
grep -qi 'Do not use' "$SKILL" || gate_ok=0
grep -qi 'Completion criteria' "$SKILL" || gate_ok=0
grep -qi 'Do not modify' "$SKILL" || gate_ok=0
grep -qi 'debugging-assistant' "$SKILL" || gate_ok=0
grep -qi 'code-refactoring' "$SKILL" || gate_ok=0
record "body has exclusions, completion, no-modify, handoffs" "$gate_ok" "gates"

# No Hermes-specific surface
if grep -qE 'delegate_task|search_files|HERMES_HOME|read_file`|`terminal`|hermes' "$SKILL"; then
  record "no Hermes tool assumptions" 0 "found hermes-specific names"
else
  record "no Hermes tool assumptions" 1 "ok"
fi

# Positive / negative routing fixtures (description must match positive cues, not negative-only jobs)
pos_ok=1
echo "$DESC" | grep -qiE 'explain|trace|how .* works|file reference' || pos_ok=0
record "positive cue: explain/trace in description" "$pos_ok" "Explain what this function does"

neg_ok=1
# Negative: refactor request should not be the primary job of this description
echo "$DESC" | grep -qi 'refactor' && echo "$DESC" | grep -qiE 'not for|code-refactoring' || neg_ok=0
record "negative cue: refactor excluded" "$neg_ok" "Refactor this function → not this skill"

echo ""
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
