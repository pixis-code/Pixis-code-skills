#!/bin/bash
# Local checks for app-qa skill package — no browser / Pixis session required.
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
REPORT="$ROOT/templates/qa-report.md"
TAX="$ROOT/references/issue-taxonomy.md"

# --- paths ---
[ -f "$SKILL" ] && record "SKILL.md exists" 1 "ok" || record "SKILL.md exists" 0 "missing"
[ -f "$REPORT" ] && record "templates/qa-report.md exists" 1 "ok" || record "templates/qa-report.md exists" 0 "missing"
[ -f "$TAX" ] && record "references/issue-taxonomy.md exists" 1 "ok" || record "references/issue-taxonomy.md exists" 0 "missing"

# --- frontmatter ---
if head -1 "$SKILL" | grep -q '^---' && grep -q '^name: app-qa$' "$SKILL"; then
  record "frontmatter name is app-qa" 1 "ok"
else
  record "frontmatter name is app-qa" 0 "bad frontmatter"
fi

# --- skill references only existing paths ---
missing_ref=0
while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  if [ ! -e "$ROOT/$rel" ]; then
    echo "  missing: $rel"
    missing_ref=1
  fi
done < <(grep -oE '(templates|references|scripts)/[A-Za-z0-9._/-]+' "$SKILL" | sort -u)
record "all SKILL.md relative paths exist" "$([ "$missing_ref" = "0" ] && echo 1 || echo 0)" "scanned"

# --- required report fields in template ---
need_ok=1
for needle in \
  'Page:' \
  'Steps to reproduce:' \
  'Observed:' \
  'Expected:' \
  'Screenshot:' \
  'Blocked / not tested' \
  'Scope tested:'
do
  grep -qF "$needle" "$REPORT" || need_ok=0
done
record "qa-report.md has required sections" "$need_ok" "page/repro/observed/expected/screenshot/blocked"

# --- skill gates ---
gate_ok=1
grep -qi 'stop' "$SKILL" || gate_ok=0
grep -qi 'enable' "$SKILL" || gate_ok=0
grep -qi 'screenshot' "$SKILL" || gate_ok=0
grep -qi 'console' "$SKILL" || gate_ok=0
grep -qi 'Completion criteria' "$SKILL" || gate_ok=0
grep -qi 'unit test' "$SKILL" || gate_ok=0
record "SKILL has stop/enable, screenshot, console, completion, no-unit-tests" "$gate_ok" "gates present"

# --- must not claim unsupported Hermes browser_* as required ---
if grep -qE 'browser_navigate|browser_console|browser_vision|dogfood' "$SKILL"; then
  record "no Hermes dogfood tool names required" 0 "found hermes-specific names"
else
  record "no Hermes dogfood tool names required" 1 "ok"
fi

# --- taxonomy stays optional ---
if grep -qi 'optional' "$TAX" && grep -qi 'optional' "$SKILL"; then
  record "taxonomy marked optional in SKILL and reference" 1 "ok"
else
  record "taxonomy marked optional in SKILL and reference" 0 "optional wording missing"
fi

# --- forbid forcing severity ---
if grep -qiE 'must (assign|set|add) severity|always (assign|set) severity|severity required' "$SKILL"; then
  record "SKILL does not force severity" 0 "forces severity"
else
  record "SKILL does not force severity" 1 "ok"
fi

echo ""
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
