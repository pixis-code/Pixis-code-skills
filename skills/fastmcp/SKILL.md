---
name: fastmcp
description: "Build, test, and install Python MCP servers with FastMCP. Use when creating or scaffolding an MCP server, wrapping an API/DB/files as tools, or validating with the FastMCP CLI. Not for calling an existing remote MCP ad hoc (use a client/CLI), debugging unrelated app APIs (api-backend-troubleshooter), or Docker-only issues (docker-environment-manager)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [MCP, FastMCP, Python, tools, resources, prompts]
    related_skills: [api-backend-troubleshooter, run, test-first]
---

# FastMCP

Build MCP servers in Python with FastMCP, validate them locally, install them into MCP clients (Cursor, Claude Desktop, etc.), and prepare HTTP deployment.

Adapted from Hermes `fastmcp` (MIT; homepage https://gofastmcp.com) for Pixis code beta. Scripts and templates live under this skill directory.

## When to use

- Create a new Python MCP server
- Wrap an API, database, CLI, or file workflow as MCP tools
- Add resources/prompts when the client needs them
- Smoke-test with `fastmcp` CLI before wiring into a client
- Install into Cursor / Claude Code / Claude Desktop

## Do not use

| Request | Hand off to |
|---------|-------------|
| Debug your own REST/GraphQL app API | `api-backend-troubleshooter` |
| Run an unrelated project command | `run` |
| Container/Compose failures | `docker-environment-manager` |
| Ad-hoc calls to an already-running MCP without building one | Client/CLI for that server — not this scaffold skill |

## Prerequisites

```bash
pip install fastmcp   # or uv add / poetry add in the project env
fastmcp version
# API template also needs: pip install httpx
```

## Included files

| Path | Role |
|------|------|
| `templates/api_wrapper.py` | REST wrapper + auth headers |
| `templates/database_server.py` | Read-only SQLite query server |
| `templates/file_processor.py` | Text-file inspect/search |
| `scripts/scaffold_fastmcp.py` | Copy a template; replace `__SERVER_NAME__` |
| `references/fastmcp-cli.md` | CLI install/deploy detail |

## Steps

1. Pick the **smallest** useful surface: API (1–3 endpoints), DB (`list_tables` / `describe_table` / constrained SELECT), or file ops. Prefer thin tools with clear names over a large vague surface.
2. Scaffold from this skill:
   ```bash
   python3 scripts/scaffold_fastmcp.py --list
   python3 scripts/scaffold_fastmcp.py --template api_wrapper --name "Acme API" --output ./acme_server.py
   ```
   Or copy a template and replace `__SERVER_NAME__`.
3. Implement `@mcp.tool` first: verb names, typed params, JSON-safe returns, validate unsafe input, read-only by default. Add `@mcp.resource` / `@mcp.prompt` only when they help.
4. Validate before any client install:
   ```bash
   fastmcp inspect acme_server.py:mcp
   fastmcp list acme_server.py --json
   fastmcp call acme_server.py <tool> <args> --json
   ```
   At least one real `fastmcp call` per new tool. Optional HTTP: `fastmcp run … --transport http --host 127.0.0.1 --port 8000`.
5. Install when local checks pass: `fastmcp install cursor acme_server.py` (or `claude-code` / `claude-desktop`). Use `fastmcp discover` to inspect configured servers.
6. Deploy only after the local contract is stable: `requirements.txt` or `pyproject.toml`, env vars documented, `fastmcp inspect` clean.

## Quality bar

- Server imports cleanly
- `inspect` + `list` succeed
- Every new tool has a real `fastmcp call`
- Env vars documented; surface small enough to understand

## Completion criteria

Done when you can state:

1. Server file and object name (`file.py:mcp`).
2. Commands run (`inspect` / `list` / `call`) and results.
3. Client install status (or explicit “local-only”).
4. Env vars and next deploy step if any.
