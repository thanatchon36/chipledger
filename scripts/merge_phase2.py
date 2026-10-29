"""Merge the Phase 2 collectors' files in work/phase2/ into data/.

Usage: uv run python scripts/merge_phase2.py [work/phase2]
- `*_accelerators.csv` + `*_sources.csv`: new products, appended; a product already present is an error.
- `*_patches.csv`: rows in the sources format that fill an EMPTY cell of an existing product; the value is
  written to data/accelerators.csv and the row appended to data/sources.csv. A patch for a filled cell is
  refused and listed, never applied.
- `nodes_rows.csv` + `nodes_sources.csv`: appended to data/nodes.csv and data/node_sources.csv.
Validation is left to `chipledger validate`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chipledger.schema import COLUMNS, SOURCE_COLUMNS  # noqa: E402


def read(p: Path) -> pd.DataFrame:
    return pd.read_csv(p, dtype=str, keep_default_na=False)


def main(work: Path) -> None:
    acc, src = read(Path("data/accelerators.csv")), read(Path("data/sources.csv"))
    n0, s0 = len(acc), len(src)
    new = [read(p) for p in sorted(work.glob("*_accelerators.csv"))]
    if new:
        add = pd.concat(new, ignore_index=True)
        unknown = [c for c in add.columns if c not in COLUMNS]
        if unknown:
            raise SystemExit(f"unknown columns: {unknown}")
        add = add.reindex(columns=COLUMNS, fill_value="")
        clash = sorted(set(add["product"]) & set(acc["product"]))
        dup = add["product"][add["product"].duplicated()].tolist()
        if clash or dup:
            raise SystemExit(f"products already present: {clash}; duplicated: {dup}")
        acc = pd.concat([acc, add], ignore_index=True)
    paths = [p for p in sorted(work.glob("*_sources.csv")) if p.name != "nodes_sources.csv"]
    srcs = [read(p).reindex(columns=SOURCE_COLUMNS, fill_value="") for p in paths]

    refused = []
    applied = 0
    for p in sorted(work.glob("*_patches.csv")):
        patch = read(p).reindex(columns=SOURCE_COLUMNS, fill_value="")
        keep = []
        for i, r in patch.iterrows():
            hit = acc.index[acc["product"] == r["product"]]
            if len(hit) != 1 or r["field"] not in COLUMNS:
                refused.append((p.name, r["product"], r["field"], "unknown product or field"))
                continue
            cur = acc.at[hit[0], r["field"]]
            if cur not in ("", r["value"]):
                refused.append(
                    (p.name, r["product"], r["field"], f"cell holds {cur}, patch says {r['value']}")
                )
                continue
            acc.at[hit[0], r["field"]] = r["value"]
            keep.append(i)
            applied += 1
        srcs.append(patch.loc[keep])
    if srcs:
        src = pd.concat([src, *srcs], ignore_index=True)

    acc.to_csv("data/accelerators.csv", index=False)
    src.to_csv("data/sources.csv", index=False)
    print(f"products {n0} -> {len(acc)}; source rows {s0} -> {len(src)}; patches applied {applied}")
    for r in refused:
        print("refused:", *r)

    if (work / "nodes_rows.csv").exists():
        nodes = pd.concat([read(Path("data/nodes.csv")), read(work / "nodes_rows.csv")], ignore_index=True)
        nodes.to_csv("data/nodes.csv", index=False)
        ns = work / "nodes_sources.csv"
        if ns.exists():
            out = Path("data/node_sources.csv")
            prev = [read(out)] if out.exists() else []
            pd.concat([*prev, read(ns)], ignore_index=True).to_csv(out, index=False)
        print(f"nodes: {len(nodes)} rows")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("work/phase2"))
