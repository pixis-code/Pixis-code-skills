---
name: nodejs-advanced-debugger
description: "Debug Node.js with node inspect, --inspect, and CDP breakpoints. Use when stepping through Node/TS or attaching to a running process. Not for Python (python-advanced-debugger) or general bugs without a debugger (debugging-assistant)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Software Development
    tags: [debugging, nodejs, inspect, cdp, breakpoints]
    related_skills: [debugging-assistant, python-advanced-debugger, test-first]
---

# Node.js advanced debugger

Drive Node's V8 inspector for real breakpoints, stepping, stacks, and expression eval. Prefer **`node inspect`** first; use CDP (`chrome-remote-interface`) when you need automation.

Adapted from Hermes `node-inspect-debugger` for Pixis (Hermes TUI-specific recipes generalized to any Node app).

## When to use

- Node/TS test fails and intermediate state is unclear
- Inspect closures that `console.log` cannot reach cleanly
- Attach to a running Node server/dev process
- Capture CPU profile or heap snapshot via CDP

## Do not use

| Request | Hand off to |
|---------|-------------|
| Python pdb/debugpy | `python-advanced-debugger` |
| General root-cause without inspector | `debugging-assistant` |
| HTTP API layer only | `api-backend-troubleshooter` |
| Solved by a quick `console.log` | Skip this skill |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | Node.js (`node`) | Includes `node inspect` |
| **Optional** | `chrome-remote-interface` | Scripted CDP (`--with-cdp`) |

**Production:** Node is **not** auto-installed (use nvm/fnm/OS packages).

```bash
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes --with-cdp   # throwaway npm install only if missing
```

Hermes had no `references/` — recipes in this SKILL.md.

## Quick start: `node inspect`

```bash
node inspect path/to/script.js
node --inspect-brk $(which tsx) path/to/script.ts
# or:
node --inspect-brk --import tsx script.ts
```

| Command | Action |
|---------|--------|
| `c` / `n` / `s` / `o` | continue / next / step in / step out |
| `pause` | pause running code |
| `sb('file.js', 42)` / `sb(42)` / `sb('fn')` | set breakpoint |
| `cb(...)` / `breakpoints` | clear / list |
| `bt` / `list(5)` | backtrace / source |
| `watch('expr')` / `repl` / `exec expr` | watch / REPL / once |
| `restart` / `kill` / `.exit` | restart / kill / quit |

In `repl`, evaluate locals/closures; `Ctrl+C` returns to `debug>`.

## Attach to a running process

```bash
# Enable inspector on existing process
kill -SIGUSR1 <pid>
# Node prints: Debugger listening on ws://127.0.0.1:9229/<uuid>

node inspect -p <pid>
# or
node inspect ws://127.0.0.1:9229/<uuid>
```

Start with inspector:

```bash
node --inspect script.js              # listen, keep running
node --inspect-brk script.js          # pause on first line
node --inspect=127.0.0.1:9230 script.js
```

List targets:

```bash
curl -s http://127.0.0.1:9229/json/list
```

**Security:** bind to `127.0.0.1` only. `--inspect=0.0.0.0` exposes remote code execution.

## Vitest / Jest under debugger

```bash
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism path/to/test.ts
# Jest: --runInBand
```

Attach with `node inspect -p <pid>`, set `sb(...)`, `cont`.

## Programmatic CDP (optional)

```bash
npm i chrome-remote-interface   # project-local or throwaway dir
node --inspect-brk=9229 target.js &
```

Driver sketch:

```javascript
const CDP = require('chrome-remote-interface');
(async () => {
  const client = await CDP({ port: 9229 });
  const { Debugger, Runtime } = client;
  Debugger.paused(async ({ callFrames, reason }) => {
    const top = callFrames[0];
    console.log(`PAUSED: ${reason} @ ${top.url}:${top.location.lineNumber + 1}`);
    await Debugger.resume();
  });
  await Runtime.enable();
  await Debugger.enable();
  await Debugger.setBreakpointByUrl({ urlRegex: '.*app\\.js$', lineNumber: 41 });
  await Runtime.runIfWaitingForDebugger();
})();
```

CPU profile / heap snapshot: enable `Profiler` / `HeapProfiler` on the same client; write `.cpuprofile` / `.heapsnapshot` for Chrome DevTools.

## Pitfalls

1. **TS line numbers** — `node inspect` hits emitted JS; use `dist/` breakpoints or `--enable-source-maps` with a CDP client that follows maps.  
2. **`--inspect` vs `--inspect-brk`** — without `-brk`, attach may miss early breakpoints.  
3. **Port collisions** — default 9229; use `--inspect=0` for a random port and read `/json/list`.  
4. **Children** — parent `--inspect` does not inspect children; use `NODE_OPTIONS='--inspect'` carefully (ports auto-increment).  
5. **Leaving target paused** — `cont` or `kill` before abandoning the session.

## Verification

- [ ] `/json/list` shows the intended target  
- [ ] First breakpoint hits  
- [ ] `list` / source at pause is the right file  
- [ ] `exec process.pid` in `repl` matches the expected PID  

## Completion criteria

1. Inspector session established and pause observed (or blocker stated).  
2. Stack/values reported with evidence.  
3. No lingering paused processes; inspect bound to localhost.  
4. Fix path continues via `debugging-assistant` / `test-first` when appropriate.
