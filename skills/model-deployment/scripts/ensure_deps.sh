#!/usr/bin/env bash
# Detect ML frameworks / serving libs for model-deployment (check-only by default).
# Usage: ensure_deps.sh [--check-only] [--yes] [--with-fastapi]
# Does NOT auto-install torch/tensorflow (too heavy). --yes only installs fastapi/uvicorn if requested.
set -euo pipefail

CHECK_ONLY=1
ASSUME_YES=0
WITH_FASTAPI=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) ASSUME_YES=1; CHECK_ONLY=0 ;;
    --with-fastapi) WITH_FASTAPI=1 ;;
    -h|--help)
      cat <<EOF
Usage: ensure_deps.sh [--check-only] [--yes] [--with-fastapi]
  Reports presence of sklearn / torch / tensorflow / joblib / onnxruntime.
  Never auto-installs torch/tensorflow. With --yes --with-fastapi, may pip install
  fastapi uvicorn if missing.
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "MISSING: python3"
  exit 1
fi

found_framework=0
for mod in sklearn torch tensorflow keras joblib onnxruntime; do
  if python3 -c "import $mod" >/dev/null 2>&1; then
    echo "OK: $mod"
    found_framework=1
  else
    echo "ABSENT: $mod"
  fi
done

if command -v docker >/dev/null 2>&1; then
  echo "OK: docker CLI ($(command -v docker))"
else
  echo "ABSENT: docker CLI (optional; use docker-environment-manager if needed)"
fi

if [ "$WITH_FASTAPI" -eq 1 ] || python3 -c "import fastapi" >/dev/null 2>&1; then
  if python3 -c "import fastapi, uvicorn" >/dev/null 2>&1; then
    echo "OK: fastapi + uvicorn"
  else
    echo "MISSING: fastapi/uvicorn"
    if [ "$ASSUME_YES" -eq 1 ] && [ "$WITH_FASTAPI" -eq 1 ]; then
      python3 -m pip install fastapi uvicorn
      python3 -c "import fastapi, uvicorn" && echo "OK: fastapi + uvicorn installed"
    elif [ "$CHECK_ONLY" -eq 1 ]; then
      echo "Install (optional): python3 -m pip install fastapi uvicorn"
    fi
  fi
fi

if [ "$found_framework" -eq 0 ]; then
  echo "WARN: no common ML framework importable in this Python."
  echo "Install into the project venv as appropriate (sklearn/torch/tensorflow)."
  # Not a hard failure — skill can still inspect project files
fi

exit 0
