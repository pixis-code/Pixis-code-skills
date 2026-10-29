#!/usr/bin/env python3
"""Generate common charts from CSV/TSV/JSON/Excel into an image file.

Stdlib + pandas + matplotlib (seaborn optional for heatmap). Does not modify
the source dataset file — reads only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _require_imports():
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
        except ImportError:
            raise SystemExit(
                json.dumps(
                    {
                        "ok": False,
                        "error": "openpyxl required for Excel input",
                        "hint": "python -m pip install openpyxl",
                    }
                )
            )
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    # fallback: try csv
    return pd.read_csv(path)


def _plot(df, args):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(args.width, args.height))
    kind = args.type

    if kind == "bar":
        if not args.x or not args.y:
            raise SystemExit("--x and --y required for bar")
        df.plot(kind="bar", x=args.x, y=args.y, ax=ax, legend=True)
    elif kind == "line":
        if not args.x or not args.y:
            raise SystemExit("--x and --y required for line")
        df.plot(kind="line", x=args.x, y=args.y, ax=ax, marker="o", legend=True)
    elif kind == "scatter":
        if not args.x or not args.y:
            raise SystemExit("--x and --y required for scatter")
        ax.scatter(df[args.x], df[args.y], alpha=0.7)
        ax.set_xlabel(args.x)
        ax.set_ylabel(args.y)
    elif kind == "hist":
        if not args.x:
            raise SystemExit("--x required for hist")
        ax.hist(df[args.x].dropna(), bins=args.bins, edgecolor="black", alpha=0.8)
        ax.set_xlabel(args.x)
        ax.set_ylabel("count")
    elif kind == "heatmap":
        numeric = df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise SystemExit("heatmap needs ≥2 numeric columns")
        corr = numeric.corr()
        try:
            import seaborn as sns

            sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", ax=ax)
        except ImportError:
            im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=45, ha="right")
            ax.set_yticklabels(corr.columns)
            fig.colorbar(im, ax=ax)
    else:
        raise SystemExit(f"unknown type: {kind}")

    title = args.title or f"{kind} chart"
    ax.set_title(title)
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=args.dpi, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot tabular data to an image")
    parser.add_argument("data", help="Path to CSV/TSV/JSON/Excel/Parquet")
    parser.add_argument(
        "--type",
        required=True,
        choices=["bar", "line", "scatter", "hist", "heatmap"],
    )
    parser.add_argument("--x", default=None)
    parser.add_argument("--y", default=None, help="Column name or comma-list for multi-series")
    parser.add_argument("-o", "--output", required=True, help="Output image path (.png/.svg)")
    parser.add_argument("--title", default=None)
    parser.add_argument("--bins", type=int, default=20)
    parser.add_argument("--width", type=float, default=8.0)
    parser.add_argument("--height", type=float, default=5.0)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()

    _require_imports()
    path = Path(args.data)
    if not path.exists():
        print(json.dumps({"ok": False, "error": f"file not found: {path}"}), file=sys.stderr)
        return 1

    df = _load(path)
    if args.y and "," in args.y:
        # multi y for bar/line via pandas
        ys = [c.strip() for c in args.y.split(",") if c.strip()]
        args.y = ys

    out = _plot(df, args)
    print(
        json.dumps(
            {
                "ok": True,
                "output": str(out.resolve()),
                "type": args.type,
                "rows": int(len(df)),
                "columns": list(map(str, df.columns)),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
