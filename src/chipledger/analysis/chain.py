"""Estimator (a): chain-linked decomposition along an ordered list of flagships (PREREGISTRATION.md §4).

For consecutive members of the chain that are both in the decomposition sample, every term of identity A
changes by Δlog2, and the Δlog2 of the terms sum to the Δlog2 of the headline rate exactly. Shares are
Δlog2(term) / Δlog2(P), per step and cumulatively from the first member to the last.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from chipledger.identity import TERMS

EXTRA = ["tdp_w", "tflops_per_w", "mem_bandwidth_gbs", "transistors_b"]  # identity B and context, no shares


def _values(derived: pd.DataFrame, members: list[str]) -> dict[str, dict[str, float]]:
    """Plain floats per product, for the members present in the decomposition sample, in chain order."""
    cols = ["year", "log2_headline", *[f"log2_{t}" for t in TERMS], *EXTRA, "residual_a"]
    out: dict[str, dict[str, float]] = {}
    for rec in derived[["product", *cols]].to_dict("records"):
        out[str(rec["product"])] = {c: float(rec[c]) for c in cols}
    return {m: out[m] for m in members if m in out and not np.isnan(out[m]["residual_a"])}


def steps(derived: pd.DataFrame, members: list[str]) -> pd.DataFrame:
    """One row per consecutive pair of chain members present in the decomposition sample."""
    v = _values(derived, members)
    present = list(v)
    rows: list[dict[str, Any]] = []
    for a, b in zip(present, present[1:], strict=False):
        row: dict[str, Any] = {
            "from": a,
            "to": b,
            "year_from": v[a]["year"],
            "year_to": v[b]["year"],
            "dlog2_headline": v[b]["log2_headline"] - v[a]["log2_headline"],
        }
        for t in TERMS:
            row[f"dlog2_{t}"] = v[b][f"log2_{t}"] - v[a][f"log2_{t}"]
        for c in EXTRA:
            row[f"dlog2_{c}"] = float(np.log2(v[b][c] / v[a][c]))  # nan propagates
        rows.append(row)
    return pd.DataFrame(rows)


def cumulative(step_table: pd.DataFrame) -> dict[str, Any]:
    """Sum of the steps, with the share of each term in the cumulative Δlog2 of the headline rate."""
    if step_table.empty:
        return {"members": [], "dlog2_headline": None, "shares": {}}
    total = float(step_table["dlog2_headline"].sum())
    out: dict[str, Any] = {
        "members": [step_table["from"].iloc[0], *step_table["to"].tolist()],
        "years": float(step_table["year_to"].iloc[-1] - step_table["year_from"].iloc[0]),
        "dlog2_headline": total,
        "doubling_years": (step_table["year_to"].iloc[-1] - step_table["year_from"].iloc[0]) / total,
        "dlog2": {t: float(step_table[f"dlog2_{t}"].sum()) for t in TERMS},
        "shares": {t: float(step_table[f"dlog2_{t}"].sum()) / total for t in TERMS},
    }
    for c in EXTRA:
        col = step_table[f"dlog2_{c}"]
        out["dlog2"][c] = None if col.isna().any() else float(col.sum())
    return out


def shares(step_table: pd.DataFrame) -> pd.DataFrame:
    """Per-step share of each term in that step's Δlog2 of the headline rate."""
    out = step_table[["from", "to"]].copy()
    for t in TERMS:
        out[t] = step_table[f"dlog2_{t}"] / step_table["dlog2_headline"]
    return out
