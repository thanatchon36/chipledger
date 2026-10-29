"""Merge the collectors' files in work/phase1/ into data/accelerators.csv and data/sources.csv.

Usage: uv run python scripts/merge_phase1.py [work/phase1]
The merge keeps the schema's column order, rejects unknown columns and duplicate products, and leaves the
validation to `chipledger validate`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chipledger.schema import COLUMNS, SOURCE_COLUMNS  # noqa: E402


def main(work: Path) -> None:
    acc = [pd.read_csv(p, dtype=str, keep_default_na=False) for p in sorted(work.glob("*_accelerators.csv"))]
    src = [pd.read_csv(p, dtype=str, keep_default_na=False) for p in sorted(work.glob("*_sources.csv"))]
    if not acc:
        raise SystemExit(f"no *_accelerators.csv in {work}")
    products = pd.concat(acc, ignore_index=True)
    unknown = [c for c in products.columns if c not in COLUMNS]
    if unknown:
        raise SystemExit(f"unknown columns: {unknown}")
    products = products.reindex(columns=COLUMNS, fill_value="")
    dup = products["product"][products["product"].duplicated()].tolist()
    if dup:
        raise SystemExit(f"duplicate products: {dup}")
    sources = pd.concat(src, ignore_index=True).reindex(columns=SOURCE_COLUMNS, fill_value="")
    products.to_csv("data/accelerators.csv", index=False)
    sources.to_csv("data/sources.csv", index=False)
    print(f"{len(products)} products, {len(sources)} source rows")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("work/phase1"))
