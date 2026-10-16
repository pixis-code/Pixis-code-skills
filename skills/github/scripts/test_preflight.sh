#!/bin/bash
# Local fixture tests for preflight.sh — no real GitHub credentials required.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PREFLIGHT="$ROOT/scripts/preflight.sh"
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

# --- missing gh ---
TMP=$(mktemp -d)
empty_bin="$TMP/bin"
mkdir -p "$empty_bin"
# PATH with no gh binary (git still available via /bin:/usr/bin)
set +e
PATH="$empty_bin:/bin:/usr/bin" /bin/bash "$PREFLIGHT" >/dev/null 2>"$TMP/err1"
EC=$?
set -e
record "missing gh" "$([ "$EC" = "1" ] && echo 1 || echo 0)" "exit=$EC"

# --- gh present, auth fails ---
TMP2=$(mktemp -d)
bin2="$TMP2/bin"
mkdir -p "$bin2"
# Keep /bin:/usr/bin so shebangs and real git work; only override gh via front of PATH.
cat >"$bin2/gh" <<'EOF'
#!/bin/bash
if [ "${1:-}" = "auth" ] && [ "${2:-}" = "status" ]; then
  echo "not logged in" >&2
  exit 1
fi
exit 0
EOF
chmod +x "$bin2/gh"
set +e
PATH="$bin2:/bin:/usr/bin" /bin/bash "$PREFLIGHT" >/dev/null 2>"$TMP2/err"
EC=$?
set -e
record "gh present, auth fails" "$([ "$EC" = "2" ] && echo 1 || echo 0)" "exit=$EC"

# --- auth ok, not a git repo ---
TMP3=$(mktemp -d)
bin3="$TMP3/bin"
mkdir -p "$bin3"
cat >"$bin3/gh" <<'EOF'
#!/bin/bash
if [ "${1:-}" = "auth" ] && [ "${2:-}" = "status" ]; then
  exit 0
fi
exit 0
EOF
chmod +x "$bin3/gh"
# git that always fails rev-parse
cat >"$bin3/git" <<'EOF'
#!/bin/bash
if [ "${1:-}" = "rev-parse" ]; then
  exit 128
fi
# Allow other git calls if any
exec /usr/bin/git "$@"
EOF
chmod +x "$bin3/git"
set +e
PATH="$bin3:/bin:/usr/bin" /bin/bash "$PREFLIGHT" >/dev/null 2>"$TMP3/err"
EC=$?
set -e
record "not a git repo" "$([ "$EC" = "3" ] && echo 1 || echo 0)" "exit=$EC err=$(head -1 "$TMP3/err")"

# --- auth ok, git repo, no GitHub remote (need-remote) ---
TMP4=$(mktemp -d)
repo4="$TMP4/repo"
mkdir -p "$repo4"
git -C "$repo4" init -q
git -C "$repo4" remote add origin "https://example.com/not-github/app.git" 2>/dev/null || true
bin4="$TMP4/bin"
mkdir -p "$bin4"
cat >"$bin4/gh" <<'EOF'
#!/bin/bash
[ "${1:-}" = "auth" ] && [ "${2:-}" = "status" ] && exit 0
exit 0
EOF
chmod +x "$bin4/gh"
set +e
(
  cd "$repo4"
  PATH="$bin4:/bin:/usr/bin" /bin/bash "$PREFLIGHT" --need-remote >/dev/null 2>"$TMP4/err"
)
EC=$?
set -e
record "no GitHub remote with --need-remote" "$([ "$EC" = "4" ] && echo 1 || echo 0)" "exit=$EC"

# --- successful preflight with GitHub remote ---
TMP5=$(mktemp -d)
repo5="$TMP5/repo"
mkdir -p "$repo5"
git -C "$repo5" init -q
git -C "$repo5" remote add origin "https://github.com/example/app.git"
bin5="$TMP5/bin"
mkdir -p "$bin5"
cat >"$bin5/gh" <<'EOF'
#!/bin/bash
[ "${1:-}" = "auth" ] && [ "${2:-}" = "status" ] && exit 0
exit 0
EOF
chmod +x "$bin5/gh"
set +e
(
  cd "$repo5"
  PATH="$bin5:/bin:/usr/bin" /bin/bash "$PREFLIGHT" --need-remote
) >"$TMP5/out" 2>"$TMP5/err"
EC=$?
set -e
record "successful preflight" "$([ "$EC" = "0" ] && echo 1 || echo 0)" "exit=$EC out=$(head -1 "$TMP5/out" 2>/dev/null)"

# --- skill package hygiene (ignore this test file) ---
HYGIENE_HITS=$(
  grep -RInE 'curl |GITHUB_TOKEN|HERMES_HOME|github-auth|pytest' \
    "$ROOT/SKILL.md" "$ROOT/scripts/preflight.sh" "$ROOT/templates" 2>/dev/null \
    | grep -v 'Never use curl' \
    | grep -v 'GITHUB_TOKEN fallbacks' \
    | grep -v 'Do not continue with curl' \
    || true
)
if [ -z "$HYGIENE_HITS" ]; then
  record "no curl/token/Hermes/pytest assumptions in skill surfaces" 1 "clean"
else
  record "no curl/token/Hermes/pytest assumptions in skill surfaces" 0 "$(echo "$HYGIENE_HITS" | head -5)"
fi

# referenced templates exist
ok_paths=1
for p in \
  "$ROOT/templates/pr-body-feature.md" \
  "$ROOT/templates/pr-body-bugfix.md" \
  "$ROOT/templates/bug-report.md" \
  "$ROOT/templates/feature-request.md" \
  "$ROOT/scripts/preflight.sh"
do
  [ -f "$p" ] || ok_paths=0
done
# references/ and old Hermes scripts must be gone
[ ! -e "$ROOT/scripts/gh-env.sh" ] || ok_paths=0
[ ! -e "$ROOT/scripts/git-credential-token.py" ] || ok_paths=0
if [ -d "$ROOT/references" ] && [ -n "$(find "$ROOT/references" -type f 2>/dev/null | head -1)" ]; then
  ok_paths=0
fi
record "referenced paths exist; curl refs removed" "$ok_paths" "layout ok=$ok_paths"

# SKILL must not point at references/
if grep -q 'references/' "$ROOT/SKILL.md"; then
  record "SKILL.md does not route to references/" 0 "still mentions references/"
else
  record "SKILL.md does not route to references/" 1 "ok"
fi

echo ""
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
