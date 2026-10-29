# ruff: noqa: E501  (one-off data patch; the strings quote vendor documents)
"""Apply the four Gate 2 decisions (approved by the author 2026-10-29) to data/.

Usage: uv run python scripts/apply_gate2.py   (run once; it refuses to run twice)
1. Per package: K80 converted from board totals to one GK210 package; K40 becomes the Kepler flagship;
   Wormhole n150 becomes the primary (n300 = two n150 ASICs on one board); Cloud AI 100 Ultra flagged.
2. Highest-TDP primary variant: MI325X primary, MI300X its variant.
3. Vector INT8 column (schema fix): MI60 and MI50 filled from AMD's support pages.
4. Node series: no data change (year of volume production only).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chipledger.schema import COLUMNS  # noqa: E402

DATE = "2026-10-29"
GATE = "Gate 2 (2026-10-29): "


def read(p: str) -> pd.DataFrame:
    return pd.read_csv(p, dtype=str, keep_default_na=False)


def main() -> None:
    acc, src = read("data/accelerators.csv"), read("data/sources.csv")
    if "int8" in acc.columns:
        raise SystemExit("Gate 2 already applied")
    acc = acc.reindex(columns=COLUMNS, fill_value="")
    row = {p: i for i, p in enumerate(acc["product"])}

    def setv(product: str, field: str, value: str) -> None:
        acc.at[row[product], field] = value

    def note(product: str, old: str | None, new: str) -> None:
        i = row[product]
        cur = acc.at[i, "notes"]
        if old is None:
            acc.at[i, "notes"] = f"{cur} {new}".strip()
        else:
            if old not in cur:
                raise SystemExit(f"{product}: note text not found: {old!r}")
            acc.at[i, "notes"] = cur.replace(old, new)

    def resource(product: str, field: str, value: str, note_text: str) -> None:
        hit = src.index[(src["product"] == product) & (src["field"] == field)]
        if len(hit) != 1:
            raise SystemExit(f"{product}/{field}: expected one source row, found {len(hit)}")
        src.at[hit[0], "value"] = value
        src.at[hit[0], "note"] = note_text

    # 1. K80 per package (two GK210 GPUs per board, stated by NVIDIA)
    k80 = {
        "fp32": (
            "4.37",
            "DERIVED per GPU package: board 'up to 8.74 teraflops single-precision' / 2 GK210 GPUs "
            "('The Tesla K80 Accelerator has two Tesla GK210 GPUs'); datasheet base-clock board total "
            "'5.6 Tflops'",
        ),
        "fp64": (
            "1.455",
            "DERIVED per GPU package: board 'up to 2.91 teraflops double-precision' / 2 GK210 GPUs; "
            "datasheet base-clock board total '1.87 Tflops'",
        ),
        "tdp_w": ("150", "Per GPU: 'Power cap level 150 W per GPU' (board power 300 W)"),
        "mem_capacity_gb": ("12", "Per GPU: '24GB of ultra-fast GDDR5 memory - 12GB of memory per GPU'"),
        "mem_bandwidth_gbs": (
            "240",
            "DERIVED per GPU package: board 'Memory bandwidth: 480 GB/sec (cumulative)' / 2 GK210 GPUs",
        ),
        "n_compute_dies": (
            "1",
            "Per GPU package: one GK210 ('The Tesla K80 Accelerator has two Tesla GK210 GPUs'; "
            "datasheet '2 x GK210')",
        ),
    }
    for f, (v, n) in k80.items():
        setv("K80", f, v)
        resource("K80", f, v, n)
    setv("K80", "is_flagship", "false")
    note(
        "K80",
        "Dual-GPU board (two GK210 GPUs); all figures are per board as sold.",
        "Dual-GPU board (two GK210 GPUs). Recorded per GPU package (PREREGISTRATION §2 counts per package; "
        "Gate 2, 2026-10-29): rates and bandwidth are the board totals / 2 (DERIVED), TDP and memory are "
        "NVIDIA's per-GPU figures.",
    )
    note(
        "K80",
        "is_flagship=true per PREREGISTRATION §2 (highest headline dense rate among Kepler training parts: "
        "8.74 vs K40 5.04 vs K20X 3.95) and the press release ('the new flagship offering of the Tesla "
        "Accelerated Computing Platform'); this conflicts with K20X is_flagship=true in data/accelerators.csv - "
        "see report.",
        "is_flagship=false: per package K80 (4.37 TFLOPS FP32) is below K40 (5.04), so K40 is the Kepler "
        "flagship under §2, although NVIDIA's press release calls K80 'the new flagship offering'.",
    )
    setv("K40", "is_flagship", "true")
    note(
        "K40",
        "is_flagship=false: the Kepler part with the highest headline dense rate is K80 (8.74 TFLOPS FP32).",
        "is_flagship=true: the Kepler training part with the highest per-package headline dense rate (K80 is "
        "4.37 per GK210 package; Gate 2, 2026-10-29).",
    )
    setv("K20X", "is_flagship", "false")
    note(
        "K20X",
        None,
        GATE + "is_flagship=false (K40 is the Kepler flagship under §2); K20X stays the first "
        "member of the pre-registered NVIDIA chain, which is frozen by name.",
    )

    # Wormhole: n300 is two n150-class ASICs on one board
    setv("Wormhole n150", "variant_of", "")
    setv("Wormhole n150", "is_flagship", "true")
    note(
        "Wormhole n150",
        None,
        GATE + "primary row and Wormhole flagship: one Wormhole ASIC per package (§2 counts "
        "per package); n300 carries two ASICs and is recorded as its variant.",
    )
    setv("Wormhole n300", "variant_of", "Wormhole n150")
    setv("Wormhole n300", "is_flagship", "false")
    note(
        "Wormhole n300",
        None,
        GATE + "two Wormhole ASICs per board, figures are board totals; recorded as a "
        "variant of the single-ASIC n150, which is the primary row.",
    )
    note(
        "Cloud AI 100 Ultra",
        None,
        GATE + "a multi-SoC card with an unstated SoC count, so its rates are not per "
        "package; excluded from every per-package analysis (trend, efficiency, memory wall).",
    )

    # 2. Highest-TDP primary variant: MI325X (1,000 W) over MI300X (750 W)
    setv("MI325X", "variant_of", "")
    setv("MI325X", "is_flagship", "true")
    note(
        "MI325X",
        None,
        GATE + "primary row and flagship under §2 (highest-TDP module form of the MI300X silicon, "
        "1,000 W vs 750 W); MI300X is its variant and is reported in a sensitivity.",
    )
    setv("MI300X", "variant_of", "MI325X")
    setv("MI300X", "is_flagship", "false")
    note(
        "MI300X",
        None,
        GATE + "variant of MI325X (same silicon, lower TDP); the pre-registered chain member "
        "'MI300X' resolves to the primary row, MI325X.",
    )

    # 3. Vector INT8 (AMD support pages list it next to FP16/FP32)
    amd = "https://www.amd.com/en/support/downloads/drivers.html/accelerators/instinct/instinct-mi-series/"
    new = [
        (
            "MI60",
            "int8",
            "59",
            amd + "instinct-mi60.html",
            "Support page: 'Peak INT8 Performance 59 TOPs' (vector dot-product rate; no matrix unit on Vega 20)",
        ),
        (
            "MI50",
            "int8",
            "53",
            amd + "instinct-mi50.html",
            "Support page: 'Peak INT8 Performance 53 TOPs' (vector dot-product rate; no matrix unit on Vega 20)",
        ),
    ]
    for p, f, v, *_ in new:
        setv(p, f, v)
    add = pd.DataFrame(
        [
            dict(product=p, field=f, value=v, url=u, access_date=DATE, confidence="high", note=n)
            for p, f, v, u, n in new
        ]
    )
    src = pd.concat([src, add], ignore_index=True)

    acc.to_csv("data/accelerators.csv", index=False)
    src.to_csv("data/sources.csv", index=False)
    print(f"applied; {len(acc)} products, {len(acc.columns)} columns, {len(src)} source rows")


if __name__ == "__main__":
    main()
