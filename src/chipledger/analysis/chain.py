"""Estimator (a): chain-linked decomposition along an ordered list of flagships (PREREGISTRATION.md §4).

For consecutive members of the chain that are both in the sample of an identity (A, A′ or clock-free; see
``chipledger.identity``), every term of that identity changes by Δlog2, and the Δlog2 of the terms sum to the
Δlog2 of the headline rate exactly. Shares are Δlog2(term) / Δlog2(P), per step and cumulatively
from the first member to the last.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from chipledger.identity import TERMS

EXTRA = ["tdp_w", "tflops_per_w", "mem_bandwidth_gbs", "transistors_b"]  # identity B and context, no shares
ALIASES = {"MI400 series": "MI455X"}  # seed names that are a family, mapped to the family's flagship row


def resolve(derived: pd.DataFrame, names: list[str]) -> list[str]:
    """Map the seed's chain names to primary rows (PREREGISTRATION §2: only primary variants enter).

    A name that is a product is replaced by its primary variant ("MI300X" -> "MI325X"); otherwise the unique
    primary row that starts with the name and a space ("P100" -> "P100 SXM2"). Names with no row are skipped.
    """
    variant_of = {
        str(p): (str(v) if isinstance(v, str) and v else str(p))
        for p, v in zip(derived["product"], derived["variant_of"], strict=True)
    }
    primaries = [p for p, v in variant_of.items() if p == v]
    out: list[str] = []
    for raw in names:
        n = ALIASES.get(raw, raw)
        if n in variant_of:
            hit = variant_of[n]
        else:
            hits = [p for p in primaries if p.startswith(n + " ")]
            if len(hits) > 1:
                raise ValueError(f"ambiguous chain member {n}: {hits}")
            if not hits:
                continue
            hit = hits[0]
        if hit not in out:
            out.append(hit)
    return out


def _values(
    derived: pd.DataFrame, members: list[str], terms: list[str], sample: str
) -> dict[str, dict[str, float]]:
    """Plain floats per product, for the members present in the sample, in chain order."""
    cols = ["year", "log2_headline", *[f"log2_{t}" for t in terms], *[c for c in EXTRA if c not in terms]]
    inside = set(derived.loc[derived[sample].astype(bool), "product"])
    out: dict[str, dict[str, float]] = {}
    for rec in derived[["product", *cols]].to_dict("records"):
        out[str(rec["product"])] = {c: float(rec[c]) for c in cols}
    return {m: out[m] for m in members if m in inside}


def steps(
    derived: pd.DataFrame, members: list[str], terms: list[str] = TERMS, sample: str = "sample_a"
) -> pd.DataFrame:
    """One row per consecutive pair of chain members present in the sample."""
    v = _values(derived, members, terms, sample)
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
        for t in terms:
            row[f"dlog2_{t}"] = v[b][f"log2_{t}"] - v[a][f"log2_{t}"]
        for c in EXTRA:
            if c not in terms:
                row[f"dlog2_{c}"] = float(np.log2(v[b][c] / v[a][c]))  # nan propagates
        rows.append(row)
    out = pd.DataFrame(rows)
    out.attrs["terms"] = list(terms)
    return out


def _terms(step_table: pd.DataFrame) -> list[str]:
    if "terms" in step_table.attrs:
        return list(step_table.attrs["terms"])
    return [
        c.removeprefix("dlog2_")
        for c in step_table.columns
        if c.startswith("dlog2_") and c != "dlog2_headline" and c.removeprefix("dlog2_") not in EXTRA
    ]


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
        "dlog2": {t: float(step_table[f"dlog2_{t}"].sum()) for t in _terms(step_table)},
        "shares": {t: float(step_table[f"dlog2_{t}"].sum()) / total for t in _terms(step_table)},
    }
    for c in EXTRA:
        if c in out["dlog2"] or f"dlog2_{c}" not in step_table:
            continue
        col = step_table[f"dlog2_{c}"]
        out["dlog2"][c] = None if col.isna().any() else float(col.sum())
    return out


def shares(step_table: pd.DataFrame) -> pd.DataFrame:
    """Per-step share of each term in that step's Δlog2 of the headline rate."""
    out = step_table[["from", "to"]].copy()
    for t in _terms(step_table):
        out[t] = step_table[f"dlog2_{t}"] / step_table["dlog2_headline"]
    return out
