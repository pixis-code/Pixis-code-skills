#!/usr/bin/env bash
# Check git (required) and optional pygount for wiki generation.
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-pygount]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
WITH_PYGOUNT=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --with-pygount) WITH_PYGOUNT=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-pygount]
  Required: git
  Optional: pygount (LOC stats in wiki scan) — same as project-codebase-analyzer
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if ! command -v git >/dev/null 2>&1; then
  echo "MISSING: git (required for SHA tracking / clone)"
  echo "Install via OS package manager. This script does not auto-install git."
  exit 1
fi
echo "OK: git ($(git --version))"

if [ "$WITH_PYGOUNT" -eq 0 ]; then
  exit 0
fi

ANALYZER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../project-codebase-analyzer/scripts" && pwd)/ensure_deps.sh"
if [ -x "$ANALYZER" ] || [ -f "$ANALYZER" ]; then
  bash "$ANALYZER" $([ "$CHECK_ONLY" -eq 1 ] && echo --check-only) $([ "$ASSUME_YES" -eq 1 ] && echo --yes)
  exit $?
fi

# Fallback inline
if command -v pygount >/dev/null 2>&1 || python3 -c "import pygount" >/dev/null 2>&1; then
  echo "OK: pygount"
  exit 0
fi
echo "MISSING: pygount"
[ "$CHECK_ONLY" -eq 1 ] && exit 1
[ "$ASSUME_YES" -eq 1 ] || [ -t 0 ] || { echo "FAIL: need --yes"; exit 1; }
python3 -m pip install --user pygount && echo "OK: pygount installed" && exit 0
exit 1
