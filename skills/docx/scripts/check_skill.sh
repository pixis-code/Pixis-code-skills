#!/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
record() { if [ "$2" = "1" ]; then echo "PASS: $1 — $3"; PASS=$((PASS+1)); else echo "FAIL: $1 — $3"; FAIL=$((FAIL+1)); fi; }
SKILL="$ROOT/SKILL.md"
DESC=$(grep -E '^description:' "$SKILL" | head -1)
grep -q '^name: docx$' "$SKILL" && record "name" 1 "ok" || record "name" 0 "bad"
grep -q 'author: Pixis' "$SKILL" && record "author" 1 "ok" || record "author" 0 "missing"
echo "$DESC" | grep -qiE 'use when' && echo "$DESC" | grep -qiE 'not for' && record "description router" 1 "ok" || record "description router" 0 "missing use when/not for"
grep -qi 'Completion criteria' "$SKILL" && grep -qi 'When to use' "$SKILL" && record "body gates" 1 "ok" || record "body gates" 0 "missing"
for f in create read edit template revisions comments validate common; do
  [ -f "$ROOT/scripts/docx_$f.py" ] || record "script $f" 0 "missing"
done
if grep -rqiE 'hermes|nous research' "$ROOT" --include='*.py' --include='*.md'; then
  record "no source branding" 0 "found"; else record "no source branding" 1 "ok"; fi
echo ""; echo "$PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
