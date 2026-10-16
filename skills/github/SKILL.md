---
name: github
description: "GitHub via gh: PRs, review comments, CI failures, issues. Starts after commit — not for commit messages (pixis:commit)."
version: 3.1.1
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Developer Workflow
    tags: [github, gh, pull-requests, ci, issues]
    related_skills: [self-review]
---

# GitHub

This `SKILL.md` is the only workflow. Use the `gh` CLI only. Never use curl, raw REST with a token, or `GITHUB_TOKEN` fallbacks.

Starts **after** the commit. Do not write commit messages — that is `pixis:commit`.

Optional helpers: `scripts/preflight.sh`, PR bodies in `templates/`.

## Preflight (every job)

Run before any GitHub operation. Or: `bash <skill-dir>/scripts/preflight.sh` (add `--need-remote` before push/PR).

1. Confirm `gh` is installed: `command -v gh`.  
   If missing → stop: install from https://cli.github.com, then `gh auth login`, retry.
2. Confirm auth: `gh auth status`.  
   If it fails → stop: run `gh auth login`, retry.
3. Confirm a Git repo: `git rev-parse --is-inside-work-tree`.  
   If it fails → stop: `cd` into the project repo (or `git init` only if the user asked).
4. Before **push** or **open a PR**, confirm a GitHub remote:  
   `git remote -v` must list a `github.com` URL (usually `origin`).  
   If none → stop: `git remote add origin <github-repo-url>` (user must provide the URL), retry.
5. If any check fails, stop. Do not continue with curl, tokens, or unofficial API clients.

## Job 1 — Open a pull request

1. Pass preflight with remote (`bash <skill-dir>/scripts/preflight.sh --need-remote`).
2. Read `git status`, `git diff`, and `git log` so the PR matches the branch.
3. Push: `git push -u origin HEAD`.
4. Create: `gh pr create --title "..." --body "..."`.  
   Include a short summary and a test plan. Use `templates/pr-body-feature.md` or `templates/pr-body-bugfix.md` when they fit (fill in the project’s real test command).
5. Confirm: `gh pr view --json url,state,title`.

## Job 2 — Address review comments

1. Pass preflight.
2. List conversation comments: `gh pr view <number> --comments`.
3. List inline review comments:  
   `gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/pulls/<number>/comments`
4. For **each** comment:
   - Read it fully.
   - If you accept it: make the code change.
   - Reply with `gh` (do not skip the reply):
     - Conversation: `gh pr comment <number> --body "..."`  
     - Inline: `gh api repos/<owner>/<repo>/pulls/comments/<comment-id>/replies -f body="..."`  
   - If you decline: reply with the reason; do not change code for that item.
5. When a review thread is resolved and `gh` supports it, resolve via GraphQL:  
   `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id="<thread-node-id>"`  
   Skip resolve if you cannot get a thread id; still leave the reply.
6. Push commits, then confirm: `gh pr view <number> --json commits,url`.

## Job 3 — Find why CI failed

1. Pass preflight.
2. Inspect checks: `gh pr checks <number>`.  
   Or by branch: `gh run list --branch <branch> --limit 10`.
3. Identify the failed run id (`gh pr checks` / `gh run list`). Then:  
   `gh run view <run-id> --json conclusion,status,name,url`  
   `gh run view <run-id> --log-failed`
4. Report: failing check name, first real error (not a cascade), and file/command it points at.
5. Never claim CI passed unless a fresh `gh pr checks <number>` (or equivalent `gh run` read) shows success.

## Job 4 — Triage an issue

1. Pass preflight.
2. Read: `gh issue view <number> --comments`.
3. Duplicates: `gh issue list --search "<keywords>" --state all`.
4. Act with one outcome:
   - Label: `gh issue edit <number> --add-label "..."`  
   - Ask for missing repro: `gh issue comment <number> --body "..."`  
   - Close **only** if it is a duplicate, or the user authorized closure:  
     `gh issue close <number> --comment "..." --reason <completed|not planned|duplicate>`  
   - Otherwise leave open.
5. Confirm: `gh issue view <number> --json state,labels,title`.
