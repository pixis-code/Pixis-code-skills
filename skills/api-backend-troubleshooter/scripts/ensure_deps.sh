#!/usr/bin/env bash
# Check HTTP tooling for api-backend-troubleshooter.
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-requests]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
WITH_REQUESTS=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --with-requests) WITH_REQUESTS=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-requests]
  Required: curl (or python3 urllib as fallback)
  Optional: python3 + requests/httpx for richer scripts (--with-requests)
  Production note: package installs may be blocked; --check-only first.
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

ok=1
if command -v curl >/dev/null 2>&1; then
  echo "OK: curl ($(curl --version | head -1))"
else
  echo "MISSING: curl (primary HTTP probe tool)"
  ok=0
fi

if command -v python3 >/dev/null 2>&1; then
  echo "OK: python3"
else
  echo "WARN: python3 not found (JWT decode / requests recipes unavailable)"
fi

if [ "$WITH_REQUESTS" -eq 1 ]; then
  if python3 -c "import requests" >/dev/null 2>&1 || python3 -c "import httpx" >/dev/null 2>&1; then
    echo "OK: requests or httpx"
  else
    echo "MISSING: requests/httpx"
    ok=0
  fi
fi

if [ "$ok" -eq 1 ]; then
  exit 0
fi

if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install curl via your OS package manager (apt/brew/choco)."
  [ "$WITH_REQUESTS" -eq 1 ] && echo "  python3 -m pip install --user requests"
  exit 1
fi

# curl cannot be reliably auto-installed without admin; only try requests
if [ "$WITH_REQUESTS" -eq 1 ] && command -v python3 >/dev/null 2>&1; then
  if [ "$ASSUME_YES" -ne 1 ] && [ ! -t 0 ]; then
    echo "FAIL: requests missing and non-interactive without --yes"
    exit 1
  fi
  echo "Installing requests ..."
  python3 -m pip install --user requests || {
    echo "FAIL: pip install requests failed"
    exit 1
  }
fi

if command -v curl >/dev/null 2>&1; then
  echo "OK: curl present (requests may still be optional)"
  exit 0
fi

echo "FAIL: curl still missing — install manually (this script does not auto-install curl)"
exit 1
