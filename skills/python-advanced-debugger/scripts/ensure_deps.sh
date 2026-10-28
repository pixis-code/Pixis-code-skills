#!/usr/bin/env bash
# Check Python debugger deps. pdb is stdlib (always available with python3).
# Optional: debugpy (DAP/attach), remote-pdb (nc-friendly).
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-debugpy] [--with-remote-pdb]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
WITH_DEBUGPY=0
WITH_REMOTE=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --with-debugpy) WITH_DEBUGPY=1 ;;
    --with-remote-pdb) WITH_REMOTE=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-debugpy] [--with-remote-pdb]
  Required: python3 (pdb is stdlib — no install)
  Optional: debugpy, remote-pdb — only installed when flags request them and missing
  Prefer project/dev env: .venv/bin/pip install debugpy
  Production note: do not inject debugpy into production runtimes.
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "FAIL: python3 not found (required)"
  exit 1
fi
echo "OK: $PY ($("$PY" -c 'import sys; print(sys.version.split()[0])'))"
"$PY" -c "import pdb" >/dev/null 2>&1 && echo "OK: pdb (stdlib)" || {
  echo "FAIL: pdb missing (broken Python install)"
  exit 1
}

need_install=()
if [ "$WITH_DEBUGPY" -eq 1 ]; then
  if "$PY" -c "import debugpy" >/dev/null 2>&1; then
    echo "OK: debugpy ($("$PY" -c 'import debugpy; print(debugpy.__version__)'))"
  else
    echo "MISSING: debugpy (optional DAP/attach)"
    need_install+=(debugpy)
  fi
fi

if [ "$WITH_REMOTE" -eq 1 ]; then
  if "$PY" -c "import remote_pdb" >/dev/null 2>&1; then
    echo "OK: remote_pdb"
  else
    echo "MISSING: remote-pdb (optional TCP pdb)"
    need_install+=(remote-pdb)
  fi
fi

if [ "${#need_install[@]}" -eq 0 ]; then
  exit 0
fi

if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install into the project/dev interpreter (preferred):"
  echo "  $PY -m pip install ${need_install[*]}"
  exit 1
fi

if [ "$ASSUME_YES" -ne 1 ] && [ ! -t 0 ]; then
  echo "FAIL: optional packages missing and non-interactive without --yes"
  exit 1
fi

echo "Installing ${need_install[*]} via $PY -m pip --user ..."
if "$PY" -m pip install --user "${need_install[@]}"; then
  for pkg in "${need_install[@]}"; do
    mod=${pkg//-/_}
    "$PY" -c "import $mod" >/dev/null 2>&1 || {
      echo "FAIL: installed $pkg but import failed"
      exit 1
    }
  done
  echo "OK: optional debugger packages installed"
  exit 0
fi

echo "FAIL: pip install blocked or failed. Use project venv: .venv/bin/pip install ${need_install[*]}"
exit 1
