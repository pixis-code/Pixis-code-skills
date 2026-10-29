---
name: data-visualization
description: "Explore data and generate charts (bar, line, scatter, hist, heatmap). Use when the user wants a chart, graph, plot, or visual analysis of CSV/Excel/JSON data as image files. Not for Jupyter notebooks (jupyter-notebook), Excel-embedded charts (xlsx), architecture diagrams (excalidraw), or model serving (model-deployment)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Data Science
    tags: [charts, graphs, matplotlib, pandas, visualization, data]
    related_skills: [jupyter-notebook, xlsx, powerpoint, pdf]
    attribution: New Pixis skill; chart practices informed by common data-viz conventions (no direct Hermes skill clone)
---

# Data visualization

Help explore, prepare, and visualize tabular data with clear charts (PNG/SVG)
and short interpretation of trends, comparisons, and outliers. Prefer saving
chart files over embedding only in notebooks unless the user asks for `.ipynb`.

**When to use:** bar/line/scatter/histogram/heatmap · “plot this CSV” · compare
series · distribution · correlation heatmap · save chart images.

**Do not use:** full EDA notebook workflow → `jupyter-notebook`; Excel workbook
charts → `xlsx`; architecture/flow diagrams → `excalidraw`; deploy ML models →
`model-deployment`.

## Dependencies

| Kind | Package | Notes |
|------|---------|-------|
| Required | `pandas`, `matplotlib` | Core load + plot |
| Optional | `seaborn` | nicer heatmaps/distributions |
| Optional | `openpyxl` | Excel `.xlsx` input |
| Optional | `pyarrow` | Parquet |

```bash
bash scripts/ensure_deps.sh --check-only
# install only when needed and approved:
bash scripts/ensure_deps.sh --yes
```

Helper CLI (optional shortcut):

```bash
python scripts/plot_data.py data.csv --type bar --x category --y value -o chart.png
python scripts/plot_data.py data.csv --type line --x date --y revenue -o trend.png
python scripts/plot_data.py data.csv --type scatter --x a --y b -o scatter.png
python scripts/plot_data.py data.csv --type hist --x age -o hist.png
python scripts/plot_data.py data.csv --type heatmap -o corr.png
```

## Procedure

### 1. Clarify objective and data

Identify the question (compare categories, trend over time, relationship,
distribution, correlation). Locate the dataset (CSV/TSV/JSON/Excel/Parquet) or
ask for a path. Prefer project data over inventing samples; if sampling, say so.

### 2. Inspect before plotting

Load with pandas. Report shape, dtypes, missingness, and a few example rows.
State if rows/columns are insufficient for the requested chart.

### 3. Prepare (copy, don’t mutate source)

Work on a **copy** in memory or a derived file. Clean only as needed for the
chart (parse dates, drop empty rows for plotted columns, coerce numerics).
**Do not overwrite the source dataset** unless the user explicitly asks.

### 4. Choose chart type

| Goal | Prefer |
|------|--------|
| Compare categories | bar |
| Trend over time/order | line |
| Relationship of two numerics | scatter |
| Distribution of one numeric | hist |
| Correlation matrix | heatmap |
| Part-to-whole (few categories) | bar (prefer) or pie sparingly |

Avoid dual axes and truncated baselines that exaggerate differences. Prefer
direct labels over cryptic legends when few series.

### 5. Render with best practices

Every chart needs: title, axis labels (with units when known), readable ticks,
legend when multi-series, non-deceptive scale. Save to a path the user can open
(e.g. `charts/…png`). Prefer PNG for sharing; SVG when the user wants crisp
vector output.

Use `scripts/plot_data.py` or a short project script. Prefer project-pinned
Python (`.venv` / `uv` / `poetry`) when present.

### 6. Interpret (when asked)

Summarize notable trends, comparisons, outliers, and data gaps. Do not invent
causation. Call out missing data or tiny sample sizes that weaken claims.

## Pitfalls

- Chart without inspecting missing values or wrong dtypes
- Overwriting source CSV/Excel
- Misleading truncated y-axis for bar comparisons
- Pie charts with many slices
- Claiming seaborn/openpyxl available without checking

## Completion criteria

- Dataset path (or stated sample) and chart objective clear
- Chart type justified; labels/title present
- Output file path reported and exists when save requested
- Source data unmodified unless user asked
- Interpretation grounded in the plotted data (or explicitly skipped)
