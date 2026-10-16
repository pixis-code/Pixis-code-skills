#!/bin/bash
# Pixis github skill — gh-only preflight.
# Exit codes: 0 ok, 1 gh missing, 2 auth failed, 3 not a git repo, 4 no GitHub remote
set -euo pipefail

NEED_REMOTE=0
for arg in "$@"; do
  case "$arg" in
    --need-remote) NEED_REMOTE=1 ;;
    -h|--help)
      echo "Usage: preflight.sh [--need-remote]"
      exit 0
      ;;
  esac
done

if ! command -v gh >/dev/null 2>&1; then
  echo "FAIL: gh is not installed."
  echo "Install the GitHub CLI from https://cli.github.com then run: gh auth login"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "FAIL: gh is installed but not authenticated."
  echo "Run: gh auth login"
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "FAIL: not inside a Git repository."
  echo "cd into the project repo and retry."
  exit 3
fi

if [ "$NEED_REMOTE" -eq 1 ]; then
  if ! git remote -v 2>/dev/null | grep -qi 'github\.com'; then
    echo "FAIL: no GitHub remote found."
    echo "Add one, for example: git remote add origin <github-repo-url>"
    exit 4
  fi
fi

echo "OK: gh installed, authenticated, git repo$([ "$NEED_REMOTE" -eq 1 ] && echo ', GitHub remote present')."
exit 0
