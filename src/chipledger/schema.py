"""The hand-curated dataset: columns, loading and validation (PREREGISTRATION.md §2–§3, §8).

``data/accelerators.csv`` has one row per product and ``data/sources.csv`` one row per sourced value
(product, field, value, url, access date, confidence). Every hand-entered value in a sourced field needs a
source row whose value matches. Derived quantities are computed in :mod:`chipledger.identity` and never
typed in. ``data/nodes.csv`` is the reference series of logic-transistor density by process node (§7).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

DATA = Path("data")

IDENTITY = [
    "vendor",
    "product",
    "architecture",
    "announce_date",
    "ship_date",
    "form_factor",
    "is_flagship",
    "variant_of",
    "wafer_scale",
    "notes",
]
SILICON = [
    "process_node",
    "foundry",
    "transistors_b",
    "n_compute_dies",
    "n_io_dies",
    "die_area_compute_total_mm2",
    "die_area_total_mm2",
    "package_type",
    "reticle_limited",
]
CLOCK_POWER = ["boost_clock_mhz", "tdp_w", "flops_convention"]
VECTOR = ["fp64", "fp32", "fp16", "bf16", "int8"]  # SIMT / vector-unit dense rates (int8 in TOPS)
TENSOR = [  # matrix-unit dense rates: tensor cores, matrix cores, MXUs, systolic arrays
    "fp64_tensor",
    "tf32_tensor",
    "fp16_tensor",
    "bf16_tensor",
    "fp8_tensor",
    "fp6_tensor",
    "fp4_tensor",
    "int8_tensor",
    "int4_tensor",
]
SPARSE = [f"{c}_sparse" for c in TENSOR if c != "fp64_tensor"]  # vendor rates with structured sparsity
MEMORY = ["mem_type", "mem_capacity_gb", "mem_bandwidth_gbs", "on_chip_sram_mb"]
INTERCONNECT = ["chip_to_chip_bandwidth_gbs"]
PRICE = ["launch_price_usd", "price_confidence"]
COLUMNS = IDENTITY + SILICON + CLOCK_POWER + VECTOR + TENSOR + SPARSE + MEMORY + INTERCONNECT + PRICE

DENSE = VECTOR + TENSOR  # any of these may set the headline (§2)
NUMERIC = [
    "transistors_b",
    "n_compute_dies",
    "n_io_dies",
    "die_area_compute_total_mm2",
    "die_area_total_mm2",
    "boost_clock_mhz",
    "tdp_w",
    *DENSE,
    *SPARSE,
    "mem_capacity_gb",
    "mem_bandwidth_gbs",
    "on_chip_sram_mb",
    "chip_to_chip_bandwidth_gbs",
    "launch_price_usd",
]
BOOLEAN = ["is_flagship", "wafer_scale", "reticle_limited"]
TEXT_SOURCED = ["announce_date", "ship_date", "process_node", "foundry", "package_type", "mem_type"]
SOURCED = TEXT_SOURCED + NUMERIC  # a non-empty value here needs a row in sources.csv
DECOMPOSITION = [
    "transistors_b",
    "die_area_compute_total_mm2",
    "boost_clock_mhz",
    "tdp_w",
]  # plus a rate (§3)
SOURCE_COLUMNS = ["product", "field", "value", "url", "access_date", "confidence", "note"]
NODE_COLUMNS = [
    "node",
    "foundry",
    "hvm_year",
    "logic_density_mtr_mm2",
    "url",
    "access_date",
    "confidence",
    "note",
]
CONFIDENCE = ("high", "medium", "low")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_raw(path: Path) -> pd.DataFrame:
    """A CSV as strings, empty cells as ''."""
    return pd.read_csv(path, dtype=str, keep_default_na=False).fillna("")


def typed(raw: pd.DataFrame) -> pd.DataFrame:
    """The product table with numeric and boolean columns converted; empty cells become NaN / False."""
    df = raw.copy()
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c].where(df[c] != "", None), errors="coerce").astype(float)
    for c in BOOLEAN:
        df[c] = df[c].str.lower().eq("true")
    return df


def load(products: Path = DATA / "accelerators.csv") -> pd.DataFrame:
    return typed(read_raw(products))


def _num(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


def _same(a: str, b: str) -> bool:
    x, y = _num(a), _num(b)
    if x is None or y is None:
        return a == b
    return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))


def validate(raw: pd.DataFrame, sources: pd.DataFrame) -> Report:
    """Every rule the dataset must satisfy; errors fail `chipledger validate`, warnings are coverage notes."""
    rep = Report()
    missing = [c for c in COLUMNS if c not in raw.columns]
    unknown = [c for c in raw.columns if c not in COLUMNS]
    if missing:
        rep.errors.append(f"accelerators.csv: missing columns {missing}")
    if unknown:
        rep.errors.append(f"accelerators.csv: unknown columns {unknown}")
    if list(sources.columns) != SOURCE_COLUMNS:
        rep.errors.append(f"sources.csv: columns must be {SOURCE_COLUMNS}")
    if rep.errors:
        return rep
    products = set(raw["product"])
    for p in raw["product"][raw["product"].duplicated()]:
        rep.errors.append(f"{p}: duplicate product")
    for _, row in raw.iterrows():
        _check_row(row, products, rep)
    for _, s in sources.iterrows():
        _check_source(s, products, rep)
    have = {(p, f): v for p, f, v in zip(sources["product"], sources["field"], sources["value"], strict=True)}
    for _, row in raw.iterrows():
        p = row["product"]
        for c in SOURCED:
            if not row[c]:
                continue
            if (p, c) not in have:
                rep.errors.append(f"{p}: {c} = {row[c]} has no row in sources.csv")
            elif have[p, c] and not _same(have[p, c], row[c]):
                rep.errors.append(f"{p}: {c} = {row[c]} but sources.csv says {have[p, c]}")
        if row["is_flagship"].lower() == "true":
            gaps = [c for c in DECOMPOSITION if not row[c]]
            if not any(row[c] for c in DENSE):
                gaps.append("a dense rate")
            if gaps:
                rep.warnings.append(f"{p}: flagship outside the decomposition sample, missing {gaps}")
    return rep


def _check_row(row: pd.Series[str], products: set[str], rep: Report) -> None:
    p = row["product"] or "(unnamed)"
    if not row["product"] or not row["vendor"]:
        rep.errors.append(f"{p}: vendor and product are required")
    if not ISO_DATE.match(row["announce_date"]):
        rep.errors.append(f"{p}: announce_date must be YYYY-MM-DD")
    if row["ship_date"] and (not ISO_DATE.match(row["ship_date"]) or row["ship_date"] < row["announce_date"]):
        rep.errors.append(f"{p}: ship_date must be YYYY-MM-DD and not before announce_date")
    for c in BOOLEAN:
        if row[c].lower() not in ("true", "false", ""):
            rep.errors.append(f"{p}: {c} must be true or false")
    values: dict[str, float] = {}
    for c in NUMERIC:
        if row[c]:
            x = _num(row[c])
            if x is None or x <= 0:
                rep.errors.append(f"{p}: {c} must be a positive number, got {row[c]!r}")
            else:
                values[c] = x
    if row["variant_of"]:
        if row["variant_of"] not in products or row["variant_of"] == row["product"]:
            rep.errors.append(f"{p}: variant_of must name another product in the table")
        if row["is_flagship"].lower() == "true":
            rep.errors.append(f"{p}: a variant cannot be the flagship")
    a, b = values.get("die_area_compute_total_mm2"), values.get("die_area_total_mm2")
    if a is not None and b is not None and b < a:
        rep.errors.append(f"{p}: die_area_total_mm2 is smaller than die_area_compute_total_mm2")
    for c in TENSOR:
        s = f"{c}_sparse"
        if c in values and s in values and values[s] < values[c]:
            rep.errors.append(f"{p}: {s} is smaller than the dense rate")
    if row["price_confidence"] and row["price_confidence"] not in CONFIDENCE:
        rep.errors.append(f"{p}: price_confidence must be one of {CONFIDENCE}")
    if row["launch_price_usd"] and not row["price_confidence"]:
        rep.errors.append(f"{p}: a price needs price_confidence")


def _check_source(s: pd.Series[str], products: set[str], rep: Report) -> None:
    where = f"sources.csv {s['product']}/{s['field']}"
    if s["product"] not in products:
        rep.errors.append(f"{where}: unknown product")
    if s["field"] not in SOURCED:
        rep.errors.append(f"{where}: {s['field']} is not a sourced field")
    if not s["url"].startswith(("http://", "https://")):
        rep.errors.append(f"{where}: url must be a web address")
    if not ISO_DATE.match(s["access_date"]):
        rep.errors.append(f"{where}: access_date must be YYYY-MM-DD")
    if s["confidence"] not in CONFIDENCE:
        rep.errors.append(f"{where}: confidence must be one of {CONFIDENCE}")
