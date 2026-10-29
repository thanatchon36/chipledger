"""Prepare the Hugging Face dataset in dist/hf/ (pushed by the author, not by this script).

Copies the dataset, the derived table, the MLPerf and node series and the frozen seed list, writes checksums
and fills the dataset card from the data. Nothing here contacts the network.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd

OUT = Path("dist/hf")
FILES = [
    Path("data/accelerators.csv"),
    Path("data/sources.csv"),
    Path("data/mlperf.csv"),
    Path("data/nodes.csv"),
    Path("data/node_sources.csv"),
    Path("data/conflicts.md"),
    Path("data/coverage.md"),
    Path("results/derived.csv"),
    Path("configs/seed.yaml"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for src in FILES:
        dest = OUT / src
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    shutil.copy2("LICENSE-DATA", OUT / "LICENSE")
    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    (OUT / "SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.relative_to(OUT)}\n" for p in files))

    acc, src = pd.read_csv("data/accelerators.csv"), pd.read_csv("data/sources.csv")
    conf = src["confidence"].value_counts()
    fill = {
        "PRODUCTS": f"{len(acc)}",
        "VENDORS": f"{acc['vendor'].nunique()}",
        "FIRST": acc["announce_date"].min()[:4],
        "LAST": acc["announce_date"].max()[:4],
        "SOURCES": f"{len(src):,}",
        "CONFIDENCE": ", ".join(f"{conf.get(k, 0):,} {k}" for k in ["high", "medium", "low"]),
    }
    card = Path("docs/dataset-card.md").read_text(encoding="utf-8")
    for key, value in fill.items():
        card = card.replace("{{" + key + "}}", value)
    (OUT / "README.md").write_text(card, encoding="utf-8")
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(json.dumps({**fill, "files": len(files) + 2, "bytes": size}))


if __name__ == "__main__":
    main()
