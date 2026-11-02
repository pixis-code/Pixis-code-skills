---
name: data-visualization
description: "Explore data and produce focused charts plus optional dashboards with quantified insights. Use when the user wants charts, graphs, plots, a visual dashboard, or visual analysis of CSV/Excel/JSON. Not for Jupyter notebooks (jupyter-notebook), Excel-embedded charts (xlsx), architecture diagrams (excalidraw), or model serving (model-deployment)."
version: 1.1.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Data Science
    tags: [charts, graphs, matplotlib, pandas, visualization, dashboard, insights, data]
    related_skills: [jupyter-notebook, xlsx, powerpoint, pdf]
    attribution: New Pixis skill; chart practices informed by common data-viz conventions (no direct Hermes skill clone)
---

# Data visualization

Produce **publication-ready chart images** and a **structured insight brief** from
tabular data. For broad analysis asks, deliver **both**:

1. **Focused charts** — one clear metric/question per file (easy to reuse/share)
2. **A multi-panel dashboard** — single overview image when the ask is exploratory
   (“analyze this”, “dashboard”, “what’s going on in this data”)

Prefer saving image files over notebooks unless the user asks for `.ipynb`.

**When to use:** bar/line/scatter/histogram/heatmap · plot a CSV · compare series ·
visual dashboard · trend / dip / ranking analysis with chart evidence.

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
bash scripts/ensure_deps.sh --yes   # only when needed and approved
```

Helpers:

```bash
# Single focused chart
python scripts/plot_data.py data.csv --type line --x month --y revenue -o charts/revenue.png \
  --title "Monthly revenue"

# Multi-panel dashboard (2–6 panels from a JSON layout)
python scripts/plot_data.py data.csv --dashboard layout.json -o charts/dashboard.png \
  --title "Business overview"
```

## Default deliverable (follow this)

Unless the user asks for **exactly one** chart:

| Output | Required? |
|--------|-----------|
| 3–6 **focused** chart PNGs (one metric each) | Yes for multi-metric asks |
| 1 **dashboard** PNG (subplots combining those views) | Yes for “analyze / overview / dashboard” asks; optional if user named one metric only |
| **Insight brief** with quantified findings | Always |
| Chart index (path → question answered) | Always |

Save under a clear folder (e.g. `charts/` or `data-viz-output/`). **Never overwrite
the source dataset** unless the user asks.

## Procedure

### 1. Clarify objective and profile the data

State the analysis goal. Load the file; report shape, dtypes, date range,
missingness, and key columns. Prefer project data; if sampling, say so.

Derive candidate metrics from columns (totals, rates, averages, rankings). Do
not invent columns that are not computable from the data.

### 2. Plan the visual story (before drawing)

Pick **3–6 questions** the charts will answer, e.g.:

- How does the primary KPI move over time?
- Where is the largest dip/spike, and by how much?
- How do categories rank on efficiency / volume / satisfaction?
- Are two metrics related (scatter) or unevenly distributed (hist)?

Map each question → one chart type + columns. Prefer:

| Goal | Chart |
|------|--------|
| Trend over time | line |
| Compare categories | bar |
| Relationship | scatter |
| Distribution | hist |
| Correlation matrix | heatmap |

Avoid dual axes and truncated bar baselines. Prefer few categories on pie; usually
use bar instead.

### 3. Prepare on a copy

Clean in memory (parse dates, coerce numerics, drop empty plot rows). Compute
derived fields (e.g. AOV = revenue/orders, efficiency = revenue/spend) only when
inputs exist. Keep formulas in the insight brief.

### 4. Render focused charts + dashboard

For each planned question, write one PNG with title, axis labels (units when
known), legend if needed, readable ticks.

Then, for overview asks, build a **dashboard** (2×2 or 2×3 subplot grid) that
reuses the same views so the user gets one shareable overview **and** separate
files for deep dives. Use `plot_data.py --dashboard` or a short matplotlib script.

### 5. Insight brief (mandatory quality bar)

After charts, write findings that a stakeholder can act on. Every major claim
must be **quantified** and tied to a chart:

- Magnitude: % change, absolute delta, rank, min/max period
- Anomalies: dips/spikes with the period name (e.g. “April dip”)
- Comparisons: best/worst category with the metric value
- Caveats: missing months, small N, definition of derived metrics

**Do not** stop at “revenue increased.” Prefer:
“Revenue grew **45.8%** from Jan→Jun; the only monthly decline was **April**
(see `charts/revenue_trend.png`).”

Structure the reply as:

1. **Chart index** — path + one-line purpose  
2. **Key findings** — 4–8 bullets with numbers  
3. **Per-chart notes** (optional, short) — what that panel shows  
4. **Limitations** — data gaps / what was not computed  

### 6. Verify before claiming success

Confirm each output path exists and is non-empty. Re-open or re-read image
metadata/size if needed. If a chart failed, say which panel and why — do not
claim a complete dashboard.

## Layout JSON (dashboard)

`layout.json` example for `--dashboard`:

```json
{
  "panels": [
    {"type": "line", "x": "month", "y": "revenue", "title": "Revenue trend"},
    {"type": "line", "x": "month", "y": "aov", "title": "Average order value"},
    {"type": "bar", "x": "category", "y": "efficiency", "title": "Marketing efficiency"},
    {"type": "bar", "x": "category", "y": "satisfaction", "title": "Customer satisfaction"}
  ]
}
```

Precompute derived columns into a working CSV if needed, then pass that path.

## Pitfalls

- Only separate charts **or** only a dashboard — for overview asks, ship **both**
- Insights without numbers or without linking to a chart file
- Overwriting source data
- Misleading scales; overcrowded pie charts
- Claiming seaborn/openpyxl without checking deps

## Completion criteria

- [ ] Data profiled (shape, key columns, gaps stated)
- [ ] Focused charts saved for each planned metric/question
- [ ] Dashboard saved when the ask was broad/overview (or user declined it)
- [ ] Insight brief includes quantified findings tied to chart paths
- [ ] Source dataset unmodified unless explicitly requested
- [ ] Output paths verified to exist
