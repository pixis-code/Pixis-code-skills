#!/usr/bin/env bash
# Check / optionally install pandas + matplotlib for data-visualization.
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-seaborn] [--with-excel]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
WITH_SEABORN=0
WITH_EXCEL=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --with-seaborn) WITH_SEABORN=1 ;;
    --with-excel) WITH_EXCEL=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-seaborn] [--with-excel]
  Required: pandas, matplotlib
  Optional: seaborn, openpyxl
  Prefer project venv. Auto-install only with --yes (not in --check-only).
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

ok=1
if ! command -v python3 >/dev/null 2>&1; then
  echo "MISSING: python3"
  exit 1
fi

check_mod() {
  local mod="$1"
  if python3 -c "import $mod" >/dev/null 2>&1; then
    echo "OK: $mod"
    return 0
  fi
  echo "MISSING: $mod"
  return 1
}

check_mod pandas || ok=0
check_mod matplotlib || ok=0
if [ "$WITH_SEABORN" -eq 1 ]; then
  check_mod seaborn || ok=0
fi
if [ "$WITH_EXCEL" -eq 1 ]; then
  check_mod openpyxl || ok=0
fi

if [ "$ok" -eq 1 ]; then
  exit 0
fi

if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install: python3 -m pip install pandas matplotlib"
  [ "$WITH_SEABORN" -eq 1 ] && echo "  python3 -m pip install seaborn"
  [ "$WITH_EXCEL" -eq 1 ] && echo "  python3 -m pip install openpyxl"
  exit 1
fi

if [ "$ASSUME_YES" -ne 1 ]; then
  echo "FAIL: deps missing; re-run with --yes to install, or install manually."
  exit 1
fi

pkgs=(pandas matplotlib)
[ "$WITH_SEABORN" -eq 1 ] && pkgs+=(seaborn)
[ "$WITH_EXCEL" -eq 1 ] && pkgs+=(openpyxl)
echo "Installing: ${pkgs[*]}"
python3 -m pip install "${pkgs[@]}"
check_mod pandas && check_mod matplotlib
exit $?
