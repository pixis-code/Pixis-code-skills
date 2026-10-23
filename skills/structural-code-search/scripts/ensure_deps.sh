#!/usr/bin/env bash
# Ensure ast-grep binary. Skips install when already present.
# Usage: ensure_deps.sh [--check-only] [--yes]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HELPER="$SCRIPT_DIR/ast_grep_helper.py"

CHECK_ONLY=0
ASSUME_YES=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes]
  Required: python3 + ast-grep (sg) binary
  Installer: $SKILL_ROOT/install.sh (or install.ps1 on Windows)
  Production note: auto-download may be blocked; use --check-only then install manually.
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

have_ast_grep() {
  if [ -x "$SKILL_ROOT/bin/sg" ] || [ -x "$SKILL_ROOT/bin/ast-grep" ]; then
    return 0
  fi
  if command -v ast-grep >/dev/null 2>&1; then
    return 0
  fi
  # sg may be util-linux on Linux — only accept if it looks like ast-grep
  if command -v sg >/dev/null 2>&1; then
    if sg --help 2>&1 | grep -qiE 'ast-grep|pattern|rewrite'; then
      return 0
    fi
  fi
  return 1
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "FAIL: python3 required for ast_grep_helper.py"
  exit 1
fi
echo "OK: python3"

if [ ! -f "$HELPER" ]; then
  echo "FAIL: helper missing: $HELPER"
  exit 1
fi

if have_ast_grep; then
  if command -v ast-grep >/dev/null 2>&1; then
    echo "OK: ast-grep ($(ast-grep --version 2>/dev/null | head -1))"
  elif [ -x "$SKILL_ROOT/bin/sg" ]; then
    echo "OK: skill-local $SKILL_ROOT/bin/sg"
  elif [ -x "$SKILL_ROOT/bin/ast-grep" ]; then
    echo "OK: skill-local $SKILL_ROOT/bin/ast-grep"
  else
    echo "OK: sg (ast-grep)"
  fi
  exit 0
fi

echo "MISSING: ast-grep binary"
if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install: bash $SKILL_ROOT/install.sh"
  echo "Or: python3 $HELPER install"
  exit 1
fi

if [ "$ASSUME_YES" -ne 1 ] && [ ! -t 0 ]; then
  echo "FAIL: ast-grep missing and non-interactive without --yes"
  exit 1
fi

INSTALLER="$SKILL_ROOT/install.sh"
if [ -f "$INSTALLER" ]; then
  chmod +x "$INSTALLER" 2>/dev/null || true
  # Prefer GitHub release binary (fast, no brew source builds). Fall back to default installer.
  echo "Installing ast-grep via install.sh --method=github ..."
  if bash "$INSTALLER" --method=github; then
    if have_ast_grep; then
      echo "OK: ast-grep installed (skill-local bin/ may need PATH)"
      echo "Hint: export PATH=\"$SKILL_ROOT/bin:\$PATH\""
      exit 0
    fi
  fi
  echo "GitHub method failed; trying default install.sh ..."
  if bash "$INSTALLER"; then
    if have_ast_grep; then
      echo "OK: ast-grep installed"
      exit 0
    fi
  fi
fi

echo "FAIL: could not install ast-grep. See references/install.md"
exit 1
