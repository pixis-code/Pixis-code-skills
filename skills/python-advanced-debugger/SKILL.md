---
name: python-advanced-debugger
description: "Advanced Python debugging with pdb, breakpoints, and debugpy/remote attach. Use when the user asks to step, set breakpoints, or attach a debugger. Not for general traceback fixes without a debugger (debugging-assistant) or Node.js (nodejs-advanced-debugger)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos]
metadata:
  pixis:
    category: Software Development
    tags: [debugging, python, pdb, debugpy, breakpoints, dap]
    related_skills: [debugging-assistant, test-first, nodejs-advanced-debugger]
---

# Python advanced debugger

Step through Python with **pdb**, `breakpoint()`, or **debugpy** / **remote-pdb** when print and long tracebacks are not enough. Prefer the cheapest tool that works.

Adapted from Hermes `python-debugpy` for Pixis (Hermes-process recipes removed; use project entrypoints instead).

## When to use

- Need to watch values mutate / step into a function
- Test fails but traceback does not show *why* a value is wrong
- Attach to a long-lived Python process that cannot easily restart
- Post-mortem inspection of locals at the crash frame

## Do not use

| Request | Hand off to |
|---------|-------------|
| General bug hunt without interactive debugger | `debugging-assistant` |
| Node.js / inspector debugging | `nodejs-advanced-debugger` |
| API HTTP layer isolation | `api-backend-troubleshooter` |
| Things `print` / `pytest --tb=long --showlocals` already answer | Skip this skill |

## Dependencies

| Kind | Dependency | Notes |
|------|------------|-------|
| **Required** | `python3` + stdlib `pdb` | Enough for most sessions |
| **Optional** | `debugpy` | DAP / IDE attach / `--pid` |
| **Optional** | `remote-pdb` | TCP pdb via `nc` |

**Production:** never inject debug packages into production runtimes. Use a project/dev venv.

```bash
bash scripts/ensure_deps.sh --check-only
bash scripts/ensure_deps.sh --yes --with-debugpy
bash scripts/ensure_deps.sh --yes --with-remote-pdb
# Prefer: .venv/bin/pip install debugpy
```

Hermes source had no `references/` — recipes live in this SKILL.md only.

## Tool pick

| Tool | When |
|------|------|
| `breakpoint()` + pdb | Local, interactive, simplest |
| `python -m pdb script.py` | No source edits; launch under pdb |
| `debugpy` | IDE attach / DAP / already-running process |
| `remote-pdb` + `nc` | Agent-friendly remote pdb over TCP |

**Start with `breakpoint()`.**

## pdb cheat sheet

| Cmd | Action |
|-----|--------|
| `n` / `s` / `r` / `c` | next / step in / return / continue |
| `l` / `ll` / `w` | list / full fn / where |
| `u` / `d` | up / down stack |
| `p` / `pp` / `a` | print / pretty / args |
| `b file:line` / `cl N` | break / clear |
| `!stmt` / `interact` | exec / full REPL in frame |
| `q` | quit |

## Recipes

### 1. Local breakpoint

```python
def compute(x, y):
    result = some_helper(x)
    breakpoint()
    return result + y
```

Remove before commit:

```bash
rg -n 'breakpoint\(\)|set_trace\(|debugpy\.listen' --type py
```

### 2. Launch under pdb (no edits)

```bash
python -m pdb path/to/script.py arg1
(Pdb) b path/to/script.py:42
(Pdb) c
```

### 3. Pytest interactive

Use the **project** interpreter (same discovery as `test-first`). Output-capturing / xdist runners hide the prompt — run a single file directly:

```bash
.venv/bin/python -m pytest tests/foo_test.py::test_bar --pdb
# or: pytest -vv --tb=long --showlocals   # non-interactive
```

### 4. Post-mortem

```bash
python -m pdb -c continue script.py
```

```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

### 5. debugpy (listen / wait / attach)

Install in a **dev** env only — do not inject into production:

```bash
pip install debugpy   # or project/dev dependency
python -c "import debugpy; print(debugpy.__version__)"
```

**A. Wait at launch (source edit):**

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
print("waiting for debugger on 5678...", flush=True)
debugpy.wait_for_client()
```

**B. No source edit:**

```bash
python -m debugpy --listen 127.0.0.1:5678 --wait-for-client your_script.py
```

**C. Attach to PID** (may need `ptrace_scope=0` on hardened Linux):

```bash
python -m debugpy --listen 127.0.0.1:5678 --pid <pid>
```

Attach from Cursor/VS Code (`request: attach`, port 5678) or use **remote-pdb** for a terminal agent:

```python
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)
```

```bash
nc 127.0.0.1 4444
```

Bind listeners to `127.0.0.1` only (remote inspect = arbitrary code execution).

## Pitfalls

1. Parallel/capturing test runners → hang with no prompt; run pytest directly on one file.
2. `PYTHONBREAKPOINT=0` disables `breakpoint()`.
3. `debugpy.listen` without `wait_for_client()` races past early breakpoints.
4. pdb is single-thread; use debugpy for multithreaded code.
5. asyncio `await` in pdb needs care on older Pythons — prefer `interact` or remote-pdb.
6. Multiprocessing: each child needs its own breakpoint.

## Verification

- [ ] First breakpoint hits (else check `PYTHONBREAKPOINT`, attach timing, runner)
- [ ] `w` shows expected stack
- [ ] Port listening if remote: `ss -tlnp | grep 5678` (or equivalent)
- [ ] No leftover `breakpoint()` / `set_trace()` / `debugpy.listen` in the commit

## Completion criteria

1. Debugger method chosen and session actually reached a pause (or blocker stated).
2. Observed values/stack reported with evidence.
3. Temporary breakpoints/debug hooks removed or flagged for the user.
4. Root-cause fix still follows `debugging-assistant` / `test-first` after inspection.
