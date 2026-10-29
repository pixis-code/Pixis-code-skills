---
name: docker-environment-manager
description: "Troubleshoot Docker Engine, containers, images, networks, volumes, Dockerfiles, and Compose stacks. Use for container crashes/restarts, Docker logs, build failures, connectivity, healthchecks, and environment issues. Not for Python unit-test writing or refactoring without a Docker issue (test-first, code-refactoring), application bugs unrelated to containers (debugging-assistant), API-only failures when the container layer is healthy (api-backend-troubleshooter), or ML model packaging/inference endpoints (model-deployment)."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Backend
    tags: [docker, compose, containers, devops, logs, volumes]
    related_skills: [debugging-assistant, api-backend-troubleshooter, test-first, code-refactoring, model-deployment]
---

# Docker environment manager

Operate and troubleshoot Docker Engine, containers, images, volumes, networks, and Compose stacks with the standard Docker CLI.

Adapted from Hermes `docker-management` for Pixis.

## When to use

- Container crashes, restarts, unhealthy healthchecks
- Compose stack failures; service logs; build failures
- Connectivity between services or host↔container
- Disk pressure / image/volume issues (after diagnosis)
- Dockerfile review for size, cache, or runtime problems

## Do not use

| Request | Hand off to |
|---------|-------------|
| Write/run unit tests with no Docker issue | `test-first` |
| Refactor app code with no container angle | `code-refactoring` |
| Application logic bug with no Docker angle | `debugging-assistant` |
| HTTP API status/auth when container layer is healthy | `api-backend-troubleshooter` |
| Feasibility spike that doesn't need containers | `technical-feasibility-investigator` |
| Browser UI QA | `app-qa` |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | Docker CLI + Engine | Daemon must be running |
| **Required** | Compose v2 (`docker compose`) | Legacy `docker-compose` accepted with warning |

**Production / local:** this skill **never auto-installs** Docker (needs OS installer / admin).

```bash
bash scripts/ensure_deps.sh --check-only
# Manual: https://docs.docker.com/get-docker/
```

Need permission to talk to the daemon (`docker` group or equivalent). Hermes had no `references/`.

## Safety rules

- Start with **read-only** inspection: `docker ps -a`, `docker compose ps`, `docker logs`, `docker inspect`, `docker compose config`, `docker system df`.
- Diagnose from evidence **before** recommending cleanup, rebuilds, or restarts.
- Explain scope and consequences before destructive actions.
- Obtain **explicit user confirmation** before deleting containers, images, volumes, or networks, or before stopping/restarting production services.
- Never delete volumes or persistent data as an assumed fix for a restart loop.
- Do not claim a container is healthy or a fix worked unless command output verifies it.

## Quick reference (read-only first)

| Task | Command |
|------|---------|
| List | `docker ps -a` / `docker compose ps` |
| Logs | `docker logs --tail 50 -f NAME` |
| Inspect | `docker inspect NAME` |
| Compose config | `docker compose config` |
| Disk usage | `docker system df` |
| Shell (after diagnosis) | `docker exec -it NAME /bin/sh` |
| Build | `docker build -t TAG .` |
| Compose up | `docker compose up -d` |

## Procedure

### 1. Check deps, then gather evidence

```bash
bash scripts/ensure_deps.sh --check-only
docker ps -a
docker compose ps          # if compose project
docker logs --tail 100 NAME
docker inspect NAME        # exit code, mounts, health
docker compose config      # resolved compose when relevant
```

State what failed (exit code, restart count, last log lines) before proposing changes.

### 2. Identify the domain

Container lifecycle · logs/inspect · images/build · Compose · volumes/networks · disk pressure.

### 3. Containers (after diagnosis)

```bash
docker run -d --name web -p 8080:80 nginx
docker run -d -e POSTGRES_PASSWORD=secret --name db postgres:16
docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16
docker run -it --rm ubuntu:22.04 /bin/bash

docker exec -it NAME /bin/sh
docker stats --no-stream
```

Key flags: `-d`, `-it`, `--rm`, `-p host:container`, `-e`, `-v`, `--name`, `--restart`, `--memory` / `--cpus`.

Confirm with the user before `stop` / `rm` / `restart` on shared or production containers.

### 4. Images

```bash
docker build -t my-app:latest .
docker build -t my-app:prod -f Dockerfile.prod .
DOCKER_BUILDKIT=1 docker build -t my-app .
docker images
```

`docker image prune` / `docker image prune -a` — confirm first (deletes unused images).

### 5. Compose

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f api
docker compose exec api /bin/sh
docker compose config
docker compose down          # stops/removes containers — confirm if shared env
# docker compose down -v     # ALSO deletes volumes — confirm; destroys data
```

Services reach each other by **service name** as hostname.

### 6. Volumes and networks

```bash
docker volume ls && docker volume inspect NAME
docker network ls && docker network inspect NAME
```

Connect/disconnect and `rm` only after confirmation when data or shared networks are involved.

### 7. Disk cleanup (not routine diagnosis)

1. Read-only: `docker system df -v`
2. Explain what each prune removes
3. Confirm with the user, then run **one** targeted prune at a time:

```bash
docker container prune       # stopped containers only
docker image prune           # dangling images
docker volume prune          # unused volumes — data loss risk
docker network prune         # unused networks
```

**Never** run `docker system prune -a --volumes` without explicit user confirmation.

## Troubleshooting table

| Problem | Likely cause | Next evidence / fix |
|---------|--------------|---------------------|
| Exits immediately | Process crashed/finished | `docker logs`; `docker inspect` ExitCode; optional `docker run -it --entrypoint /bin/sh IMAGE` |
| Port already allocated | Conflict | `docker ps` / `lsof -i :PORT` |
| No space left | Disk full | `docker system df`; confirm before prune |
| Can't reach from host | Bound to 127.0.0.1 inside | Bind `0.0.0.0`; check `-p` |
| Volume permission denied | UID mismatch | `--user $(id -u):$(id -g)` or fix perms |
| Services can't talk | Wrong network/name | `docker compose config` |
| Huge image | No multi-stage / no `.dockerignore` | Multi-stage, pin tags, non-root `USER` |

## Dockerfile tips

1. Multi-stage builds  
2. Deps before source (cache)  
3. Combine `RUN`s thoughtfully  
4. `.dockerignore` (`node_modules`, `.git`, `__pycache__`)  
5. Pin tags (`python:3.12-slim`, not `latest`)  
6. Non-root `USER`

## Verification

- `docker ps` / `docker compose ps` shows Up/healthy  
- `docker logs --tail 20 NAME` free of the prior error  
- Port: `curl -s http://localhost:PORT` or `docker port NAME`  
- After any prune: `docker system df` before/after  

## Completion criteria

1. Evidence gathered before changes (commands + observed output).  
2. Destructive deletes/prunes/restarts confirmed with the user when required.  
3. Healthy state verified with command output, or remaining blocker stated.  
4. App-level bugs handed to `debugging-assistant` once the container layer is healthy.
