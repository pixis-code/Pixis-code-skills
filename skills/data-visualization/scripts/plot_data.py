#!/usr/bin/env python3
"""Generate focused charts or a multi-panel dashboard from tabular data.

Stdlib + pandas + matplotlib (seaborn optional for heatmap). Reads the source
file only — never modifies it.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def _require_imports() -> None:
    try:
        import pandas as pd  # noqa: F401
        import matplotlib  # noqa: F401

        matplotlib.use("Agg")
    except ImportError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"missing dependency: {exc}",
                    "hint": "bash scripts/ensure_deps.sh --yes",
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)


def _load(path: Path):
    import pandas as pd

    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv", ".txt"}:
        sep = "\t" if suffix == ".tsv" else ","
        return pd.read_csv(path, sep=sep)
    if suffix in {".xlsx", ".xls"}:
        try:
            return pd.read_excel(path)
        except ImportError as exc:
            raise SystemExit(
                json.dumps(
                    {
                        "ok": False,
                        "error": f"openpyxl required for Excel input: {exc}",
                        "hint": "python -m pip install openpyxl",
                    }
                )
            )
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _resolve_y(y: Any):
    if y is None:
        return None
    if isinstance(y, list):
        return y
    if isinstance(y, str) and "," in y:
        return [c.strip() for c in y.split(",") if c.strip()]
    return y


def _draw_on_ax(ax, df, panel: dict[str, Any]) -> None:
    kind = panel.get("type") or panel.get("kind")
    x = panel.get("x")
    y = _resolve_y(panel.get("y"))
    title = panel.get("title") or (f"{kind} chart" if kind else "chart")
    bins = int(panel.get("bins", 20))

    if kind == "bar":
        if not x or y is None:
            raise ValueError("bar panel needs x and y")
        df.plot(kind="bar", x=x, y=y, ax=ax, legend=True)
        ax.set_xlabel(str(x))
    elif kind == "line":
        if not x or y is None:
            raise ValueError("line panel needs x and y")
        df.plot(kind="line", x=x, y=y, ax=ax, marker="o", legend=True)
        ax.set_xlabel(str(x))
    elif kind == "scatter":
        if not x or not y or isinstance(y, list):
            raise ValueError("scatter panel needs single x and y")
        ax.scatter(df[x], df[y], alpha=0.7)
        ax.set_xlabel(str(x))
        ax.set_ylabel(str(y))
    elif kind == "hist":
        if not x:
            raise ValueError("hist panel needs x")
        ax.hist(df[x].dropna(), bins=bins, edgecolor="black", alpha=0.8)
        ax.set_xlabel(str(x))
        ax.set_ylabel("count")
    elif kind == "heatmap":
        numeric = df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise ValueError("heatmap needs ≥2 numeric columns")
        corr = numeric.corr()
        try:
            import seaborn as sns

            sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", ax=ax)
        except ImportError:
            im = ax.imshow(corr.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(list(corr.columns), rotation=45, ha="right")
            ax.set_yticklabels(list(corr.columns))
            ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    else:
        raise ValueError(f"unknown panel type: {kind}")

    ax.set_title(title)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")


def _plot_single(df, args) -> Path:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(args.width, args.height))
    panel = {
        "type": args.type,
        "x": args.x,
        "y": args.y,
        "title": args.title,
        "bins": args.bins,
    }
    _draw_on_ax(ax, df, panel)
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=args.dpi, bbox_inches="tight")
    plt.close(fig)
    return out


def _plot_dashboard(df, layout: dict[str, Any], args) -> Path:
    import matplotlib.pyplot as plt

    panels = layout.get("panels") or []
    if not panels:
        raise SystemExit(json.dumps({"ok": False, "error": "layout.panels is empty"}))
    if len(panels) > 6:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "error": "dashboard supports at most 6 panels; split into multiple dashboards",
                }
            )
        )

    n = len(panels)
    ncols = 2 if n > 1 else 1
    nrows = int(math.ceil(n / ncols))
    fig_w = args.width if args.width != 8.0 else max(10.0, 5.0 * ncols)
    fig_h = args.height if args.height != 5.0 else max(4.0, 3.8 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=(fig_w, fig_h), squeeze=False)
    flat = [axes[r][c] for r in range(nrows) for c in range(ncols)]

    for i, panel in enumerate(panels):
        _draw_on_ax(flat[i], df, panel)
    for j in range(n, len(flat)):
        flat[j].axis("off")

    if args.title:
        fig.suptitle(args.title, fontsize=14, y=1.02)
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=args.dpi, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plot tabular data to a focused chart or multi-panel dashboard"
    )
    parser.add_argument("data", help="Path to CSV/TSV/JSON/Excel/Parquet")
    parser.add_argument(
        "--type",
        choices=["bar", "line", "scatter", "hist", "heatmap"],
        help="Single-chart type (required unless --dashboard)",
    )
    parser.add_argument(
        "--dashboard",
        metavar="LAYOUT.json",
        help="Multi-panel dashboard layout JSON (see skill docs)",
    )
    parser.add_argument("--x", default=None)
    parser.add_argument("--y", default=None, help="Column or comma-list for multi-series")
    parser.add_argument("-o", "--output", required=True, help="Output image (.png/.svg)")
    parser.add_argument("--title", default=None)
    parser.add_argument("--bins", type=int, default=20)
    parser.add_argument("--width", type=float, default=8.0)
    parser.add_argument("--height", type=float, default=5.0)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()

    if not args.dashboard and not args.type:
        parser.error("provide --type for a single chart, or --dashboard LAYOUT.json")

    _require_imports()
    path = Path(args.data)
    if not path.exists():
        print(json.dumps({"ok": False, "error": f"file not found: {path}"}), file=sys.stderr)
        return 1

    df = _load(path)
    args.y = _resolve_y(args.y)

    try:
        if args.dashboard:
            layout_path = Path(args.dashboard)
            layout = json.loads(layout_path.read_text(encoding="utf-8"))
            out = _plot_dashboard(df, layout, args)
            mode = "dashboard"
            panel_count = len(layout.get("panels") or [])
        else:
            out = _plot_single(df, args)
            mode = "single"
            panel_count = 1
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "mode": mode,
                "output": str(out.resolve()),
                "type": args.type,
                "panels": panel_count,
                "rows": int(len(df)),
                "columns": list(map(str, df.columns)),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
