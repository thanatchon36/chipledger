"""Derived quantities and the accounting identities (PREREGISTRATION.md §2 and §4).

Identity A holds for every product by construction::

    log2 P = log2 density + log2 area + log2 clock + log2 spec + log2 precision_multiplier

P is the headline dense rate (TFLOP/s, or TOPS for integer formats); density = N / A in millions of
transistors per mm²; area = A, the package's compute-die area in mm²; clock = f in MHz; spec = R / (N f),
reference operations per transistor per cycle; precision_multiplier = P / R with R the reference rate.
Identity B splits P into P/W and W (TDP); identity C into P/A and A. Identity A′ (DEVIATIONS.md #3) merges
density and area into N, for products without a published die area; the clock-free identity (§6) folds the
clock into specialization, R / N. The residual of each identity is computed for every complete row and must be
zero to ``TOL``; rows with a missing term get NaN, not a pass.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

from chipledger.schema import DENSE, SPARSE, TENSOR

TOL = 1e-9
TERMS = [
    "density_mtr_mm2",
    "area_mm2",
    "boost_clock_mhz",
    "spec_ops_per_transistor_cycle",
    "precision_multiplier",
]
TERMS_N = ["transistors_mtr", "boost_clock_mhz", "spec_ops_per_transistor_cycle", "precision_multiplier"]
TERMS_CF = ["density_mtr_mm2", "area_mm2", "spec_ops_per_transistor_us", "precision_multiplier"]
# sample membership: the identity's terms plus W (§3)
SAMPLES = {
    "sample_a": ["transistors_b", "area_mm2", "boost_clock_mhz", "tdp_w", "ref_tflops"],
    "sample_an": ["transistors_b", "boost_clock_mhz", "tdp_w", "ref_tflops"],
    "sample_cf": ["transistors_b", "area_mm2", "tdp_w", "ref_tflops"],
}
# §2: the first group with a published value gives the reference rate; FP32 is flagged
REFERENCE_RULE = (("fp16_tensor", "bf16_tensor"), ("fp16", "bf16"), ("fp32",))
INTEGER = ["int8", "int8_tensor", "int4_tensor"]


@dataclass(frozen=True)
class Options:
    """The pre-registered sensitivities of §6 that change a definition. The defaults are the frozen rules."""

    date: Literal["announce", "ship"] = "announce"
    reference: Literal["primary", "fp32"] = "primary"  # fp32: FP32 is the reference rate for every product
    headline: Literal["all", "float", "sparse"] = "all"  # float: INT8/INT4 excluded; sparse: sparsity counted
    area: Literal["compute", "total"] = "compute"  # total: area including I/O dies


PRIMARY = Options()


def _present(row: pd.Series[Any], cols: tuple[str, ...] | list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for c in cols:
        v = row.get(c)
        if v is not None and not pd.isna(v):
            out[c] = float(v)
    return out


def reference(row: pd.Series[Any], opts: Options = PRIMARY) -> tuple[float, str, bool]:
    """(R, format, ref_is_fp32): matrix-unit FP16/BF16, else vector FP16/BF16, else FP32 and flagged."""
    rule = (("fp32",),) if opts.reference == "fp32" else REFERENCE_RULE
    for group in rule:
        vals = _present(row, group)
        if vals:
            fmt = max(vals, key=lambda c: vals[c])
            return vals[fmt], fmt, group == ("fp32",)
    return math.nan, "", False


def headline(row: pd.Series[Any], opts: Options = PRIMARY) -> tuple[float, str]:
    """(P, format): the largest dense rate over every format and unit, INT8/INT4 included."""
    cols = DENSE
    if opts.headline == "float":
        cols = [c for c in DENSE if c not in INTEGER]
    elif opts.headline == "sparse":
        cols = DENSE + SPARSE
    vals = _present(row, cols)
    if not vals:
        return math.nan, ""
    fmt = max(vals, key=lambda c: vals[c])
    return vals[fmt], fmt


def sparsity(row: pd.Series[Any]) -> float:
    """The largest sparse/dense ratio over formats where the vendor publishes both; NaN if none."""
    ratios = []
    for c in TENSOR:
        pair = _present(row, (c, f"{c}_sparse"))
        if len(pair) == 2:
            ratios.append(pair[f"{c}_sparse"] / pair[c])
    return max(ratios) if ratios else math.nan


def decimal_year(date: str | pd.Timestamp) -> float:
    d = pd.Timestamp(date)
    return d.year + (d.day_of_year - 1) / (366.0 if d.is_leap_year else 365.0)


def derive(df: pd.DataFrame, opts: Options = PRIMARY) -> pd.DataFrame:
    """Add every derived column of §2 and the identity residuals; ``opts`` selects a §6 sensitivity."""
    out = df.copy()
    dates = out["ship_date"] if opts.date == "ship" else out["announce_date"]
    out["year"] = [math.nan if pd.isna(d) or d == "" else decimal_year(d) for d in dates]
    refs = [reference(r, opts) for _, r in out.iterrows()]
    out["ref_tflops"] = [r[0] for r in refs]
    out["ref_format"] = [r[1] for r in refs]
    out["ref_is_fp32"] = [r[2] for r in refs]
    heads = [headline(r, opts) for _, r in out.iterrows()]
    out["headline_tflops"] = [h[0] for h in heads]
    out["headline_format"] = [h[1] for h in heads]
    out["sparsity_multiplier"] = [sparsity(r) for _, r in out.iterrows()]
    out["area_mm2"] = out["die_area_total_mm2" if opts.area == "total" else "die_area_compute_total_mm2"]
    out["density_mtr_mm2"] = out["transistors_b"] * 1e3 / out["area_mm2"]
    out["precision_multiplier"] = out["headline_tflops"] / out["ref_tflops"]
    # R·1e12 operations per second over N·1e9 transistors and f·1e6 cycles per second
    out["spec_ops_per_transistor_cycle"] = out["ref_tflops"] / (
        out["transistors_b"] * out["boost_clock_mhz"] * 1e3
    )
    # A′ and clock-free (§6) need N in millions to close: MTr · MHz · spec = R, MTr · (R / MTr) = R
    out["transistors_mtr"] = out["transistors_b"] * 1e3
    # R·1e12 operations per second over N·1e9 transistors, per µs: R / (N·1e3)
    out["spec_ops_per_transistor_us"] = out["ref_tflops"] / out["transistors_mtr"]
    out["tflops_per_w"] = out["headline_tflops"] / out["tdp_w"]
    out["ref_tflops_per_w"] = out["ref_tflops"] / out["tdp_w"]
    out["tflops_per_mm2"] = out["headline_tflops"] / out["area_mm2"]
    out["tflops_per_btransistor"] = out["headline_tflops"] / out["transistors_b"]
    out["ops_per_byte"] = out["headline_tflops"] * 1e3 / out["mem_bandwidth_gbs"]
    out["log2_headline"] = np.log2(out["headline_tflops"])
    residual = out["log2_headline"].copy()
    for t in TERMS:
        out[f"log2_{t}"] = np.log2(out[t])
        residual = residual - out[f"log2_{t}"]
    out["residual_a"] = residual
    for name, terms in (("residual_an", TERMS_N), ("residual_cf", TERMS_CF)):
        r = out["log2_headline"].copy()
        for t in terms:
            out[f"log2_{t}"] = np.log2(out[t])
            r = r - out[f"log2_{t}"]
        out[name] = r
    for flag, cols in SAMPLES.items():
        out[flag] = out[cols].notna().all(axis=1)
    out["residual_b"] = out["log2_headline"] - np.log2(out["tflops_per_w"]) - np.log2(out["tdp_w"])
    out["residual_c"] = out["log2_headline"] - np.log2(out["tflops_per_mm2"]) - np.log2(out["area_mm2"])
    return out


def check(derived: pd.DataFrame) -> float:
    """The largest |residual| over complete rows; raises if any identity fails."""
    worst = 0.0
    for col in ("residual_a", "residual_an", "residual_cf", "residual_b", "residual_c"):
        r = derived[col].dropna()
        if len(r):
            worst = max(worst, float(r.abs().max()))
    if worst > TOL:
        raise ValueError(f"identity residual {worst:.3g} exceeds {TOL}")
    return worst
