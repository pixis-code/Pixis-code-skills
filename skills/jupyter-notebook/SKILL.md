---
name: jupyter-notebook
description: "Create or run Jupyter notebooks for data exploration and analysis. Use when the user asks for a .ipynb, sales/dataset analysis, pandas load/inspect, missing-value handling, exploratory data analysis (EDA), Matplotlib/Seaborn visualizations, Markdown sections plus code cells, or a live Jupyter kernel with persistent state. Prefer an existing project dataset; otherwise state the sample data you will use. Run cells when the environment supports it and report errors. Not for one-shot non-notebook scripts (run), unit-test TDD (test-first), pdb stepping (python-advanced-debugger), or explaining code without a notebook (code-explainer)."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Data Science
    tags: [jupyter, notebook, pandas, eda, matplotlib, visualization, repl, data-science]
    related_skills: [run, python-advanced-debugger, test-first, code-explainer]
---

# Jupyter notebook

Author and/or execute **Jupyter notebooks** (`.ipynb`) for dataset exploration and analysis — pandas, EDA, visualizations — and optionally drive a **live kernel** when the environment supports it.

Adapted from Hermes `jupyter-notebook` / hamelnb (MIT) for Pixis code beta. Prefer the project’s pinned Python (`.venv` / `uv` / `poetry`).

## When to use

- “Create a Jupyter Notebook to explore a dataset…” (sales analysis, EDA, etc.)
- Load/inspect with **pandas**, handle missing values, exploratory analysis
- Charts with **Matplotlib** (or Seaborn if already in the project)
- Organize clear **Markdown sections** + executable **code cells**
- Use an existing project dataset if available; otherwise explain sample data
- Run notebook cells and report errors
- Iterative REPL / live kernel with persistent state

## Do not use

| Request | Hand off to |
|---------|-------------|
| One-shot project command / build / lint (no notebook) | `run` |
| Failing unit test then fix | `test-first` |
| Step with pdb/debugpy breakpoints | `python-advanced-debugger` |
| Explain existing analysis code without creating/running a notebook | `code-explainer` |
| Pure app feature review vs requirements | `sdlc-review` |

## Steps

### A. Create / author a notebook (primary for analysis prompts)

1. Search the repo for an existing dataset (`.csv`, `.parquet`, `.xlsx`, `data/`, `datasets/`). If found, use it and cite the path. If not, state clearly what sample data you will create (columns, row count, how generated) before writing cells.
2. Create or update a `.ipynb` with a clear section structure, e.g.:
   - Title / goal (Markdown)
   - Setup & imports
   - Load data
   - Inspect (`shape`, `dtypes`, `head`, missingness)
   - Clean / handle missing values (justify choices)
   - EDA (groupbys, summaries, correlations as relevant)
   - Visualizations (Matplotlib)
   - Short conclusions
3. Keep Markdown explanatory and code cells focused and runnable top-to-bottom.
4. Install missing packages (**pandas**, **matplotlib**, jupyter as needed) into the **same** env you will execute with.
5. **Run cells** when possible (Jupyter / `jupyter nbconvert --execute` / papermill / live kernel). Report successes and any errors with the failing cell’s message — do not claim success without a run when the env supports execution.
6. If the environment cannot run notebooks, say so, leave the `.ipynb` ready to run, and note how the user can execute it.

### B. Live kernel (when iterating or verifying)

1. Prefer project env Jupyter; optional [hamelnb](https://github.com/hamelsmu/hamelnb) helper for structured execute/edit.
2. Start or attach a kernel; execute with persistent state; retry once on first-timeout after kernel start.
3. Use restart-run-all when the user wants clean top-to-bottom verification.
4. Prefer compact output; on flaky websocket replies retry with zmq transport if using hamelnb.

```bash
# optional hamelnb
git clone https://github.com/hamelsmu/hamelnb.git ~/.agent-skills/hamelnb
SCRIPT="$HOME/.agent-skills/hamelnb/skills/jupyter-live-kernel/scripts/jupyter_live_kernel.py"
```

## Completion criteria

Done when you can state:

1. Notebook path created or updated.
2. Dataset used (project path) or sample-data explanation.
3. Sections covered: load, inspect, missing values, EDA, visualizations.
4. Whether cells were executed, and any errors (with messages).
5. Packages installed into the execution environment when needed.
