#!/usr/bin/env bash
# Check Node.js for inspector debugging. Optional CDP driver package.
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-cdp]
# Exit: 0 ok, 1 missing/failed, 2 bad args
set -euo pipefail

CHECK_ONLY=0
ASSUME_YES=0
WITH_CDP=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --with-cdp) WITH_CDP=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-cdp]
  Required: node (includes \`node inspect\`)
  Optional: chrome-remote-interface for scripted CDP (--with-cdp)
  This script does not auto-install Node.js (use nvm/fnm/OS packages).
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if ! command -v node >/dev/null 2>&1; then
  echo "MISSING: node"
  echo "Install: https://nodejs.org/ or nvm/fnm. This script will not auto-install Node."
  exit 1
fi
echo "OK: node ($(node --version))"

if node --help 2>&1 | grep -q inspect || node -e 'process.exit(0)'; then
  echo "OK: node binary usable (use: node inspect <script>)"
fi

if [ "$WITH_CDP" -eq 0 ]; then
  exit 0
fi

# Prefer project-local, then global
if node -e "require('chrome-remote-interface')" >/dev/null 2>&1; then
  echo "OK: chrome-remote-interface resolvable from cwd"
  exit 0
fi

echo "MISSING: chrome-remote-interface (optional CDP automation)"
if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "Install (project): npm i chrome-remote-interface"
  echo "Or throwaway: mkdir -p /tmp/cdp-tools && cd /tmp/cdp-tools && npm i chrome-remote-interface"
  exit 1
fi

if [ "$ASSUME_YES" -ne 1 ] && [ ! -t 0 ]; then
  echo "FAIL: CDP package missing and non-interactive without --yes"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "FAIL: npm not found; cannot install chrome-remote-interface"
  exit 1
fi

TMP="${TMPDIR:-/tmp}/pixis-cdp-tools"
mkdir -p "$TMP"
echo "Installing chrome-remote-interface into $TMP ..."
(cd "$TMP" && npm i --silent chrome-remote-interface) || {
  echo "FAIL: npm install failed"
  exit 1
}
if NODE_PATH="$TMP/node_modules${NODE_PATH:+:$NODE_PATH}" node -e "require('chrome-remote-interface')"; then
  echo "OK: chrome-remote-interface at $TMP"
  echo "Use: NODE_PATH=$TMP/node_modules node your-cdp-driver.js"
  exit 0
fi
echo "FAIL: package installed but not importable"
exit 1
