#!/usr/bin/env bash
# Ensure pygount for project-codebase-analyzer.
# Usage: ensure_deps.sh [--check-only] [--yes]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    -h|--help)
      echo "Usage: ensure_deps.sh [--check-only] [--yes]"
      echo "  Checks for pygount; installs via pip only if missing (not in --check-only)."
      echo "  Production note: auto-install may be disabled; use --check-only then install manually."
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

have_pygount() {
  command -v pygount >/dev/null 2>&1 && return 0
  # Common --user script locations (may be off PATH)
  for d in "$HOME/Library/Python/"*/bin "$HOME/.local/bin"; do
    [ -x "$d/pygount" ] 2>/dev/null && return 0
  done
  python3 -c "import pygount" >/dev/null 2>&1 && return 0
  return 1
}

if have_pygount; then
  if command -v pygount >/dev/null 2>&1; then
    echo "OK: pygount present ($(command -v pygount))"
  else
    echo "OK: pygount importable via python3"
  fi
  exit 0
fi

echo "MISSING: pygount (required for LOC/language metrics)"
if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install: python3 -m pip install --user pygount"
  echo "Or: pipx install pygount"
  exit 1
fi

if [ "$ASSUME_YES" -ne 1 ] && [ ! -t 0 ]; then
  echo "FAIL: pygount missing and non-interactive shell without --yes."
  echo "Re-run with --yes to install, or: python3 -m pip install --user pygount"
  exit 1
fi

echo "Installing pygount via python3 -m pip --user ..."
if python3 -m pip install --user pygount; then
  if have_pygount; then
    echo "OK: pygount installed"
    exit 0
  fi
  echo "FAIL: pip reported success but pygount still not found on PATH/import."
  echo "Try: python3 -m pip show pygount && export PATH=\"\$HOME/.local/bin:\$PATH\""
  exit 1
fi

echo "FAIL: could not install pygount (pip may be blocked in this environment)."
echo "Manual: python3 -m pip install --user pygount"
exit 1
