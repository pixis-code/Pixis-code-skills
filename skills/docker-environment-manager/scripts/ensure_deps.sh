#!/usr/bin/env bash
# Check Docker Engine + Compose. Does NOT auto-install Docker (requires admin / OS installer).
# Usage: ensure_deps.sh [--check-only]
# Exit: 0 ok, 1 missing, 2 bad args
set -euo pipefail

for arg in "$@"; do
  case "$arg" in
    --check-only) ;; # always check-only for Docker
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only]
  Required: docker CLI + running Docker Engine + Compose v2 (docker compose)
  This script never auto-installs Docker — follow https://docs.docker.com/get-docker/
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  echo "MISSING: docker CLI"
  echo "Install Docker Desktop / Engine: https://docs.docker.com/get-docker/"
  exit 1
fi
echo "OK: docker ($(docker --version 2>/dev/null | head -1))"

if ! docker info >/dev/null 2>&1; then
  echo "FAIL: docker CLI found but Engine not reachable (daemon not running or permission denied)"
  echo "Start Docker Desktop / dockerd, or add user to the docker group and re-login."
  exit 1
fi
echo "OK: Docker Engine reachable"

if docker compose version >/dev/null 2>&1; then
  echo "OK: docker compose ($(docker compose version 2>/dev/null | head -1))"
  exit 0
fi

if command -v docker-compose >/dev/null 2>&1; then
  echo "OK: docker-compose (legacy) ($(docker-compose --version 2>/dev/null | head -1))"
  echo "WARN: prefer Compose v2: docker compose"
  exit 0
fi

echo "MISSING: Docker Compose v2 (docker compose)"
echo "Install Compose plugin: https://docs.docker.com/compose/install/"
exit 1
