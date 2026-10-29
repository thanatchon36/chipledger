"""Estimator (b): log-linear trends, log2 y = a + b · year, for every term and the headline rate
(PREREGISTRATION.md §4). One chip-level bootstrap serves every series, so differences between slopes
(H3b, H5) use the same resampled chips as the slopes themselves.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import theilslopes

from chipledger.identity import TERMS

DRAWS = 2000
SEED = 20261029
SERIES = ["log2_headline", *[f"log2_{t}" for t in TERMS]]


@dataclass
class Fit:
    series: str
    n: int
    slope: float  # doublings per year
    intercept: float
    doubling_years: float
    se_hc3: float
    slope_ci: tuple[float, float]  # bootstrap percentile 95%
    doubling_ci: tuple[float, float]  # from the slope interval; (hi, lo) of 1/slope, inf if a bound is ≤ 0
    theil_sen: float

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["slope_ci"] = list(self.slope_ci)
        d["doubling_ci"] = list(self.doubling_ci)
        return d


def _ols(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    xm, ym = x.mean(), y.mean()
    b = float(((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum())
    return b, float(ym - b * xm)


def _doubling(slope: float) -> float:
    return float("inf") if slope <= 0 else 1.0 / slope


def _demean(v: np.ndarray, groups: np.ndarray) -> np.ndarray:
    """v minus its group mean: OLS on demeaned data gives the fixed-effects (within) slope."""
    out = v.astype(float).copy()
    for g in np.unique(groups):
        m = groups == g
        out[m] -= out[m].mean()
    return out


def bootstrap(
    x: np.ndarray,
    ys: dict[str, np.ndarray],
    draws: int = DRAWS,
    seed: int = SEED,
    groups: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """Slope draws per series from the same resampled chips; within-group slopes if ``groups`` is given."""
    rng = np.random.default_rng(seed)
    n = len(x)
    out = {k: np.empty(draws) for k in ys}
    for i in range(draws):
        while True:
            idx = rng.integers(0, n, n)
            xi = x[idx] if groups is None else _demean(x[idx], groups[idx])
            if np.ptp(xi) > 0:  # a draw with no variation in year has no slope
                break
        for k, y in ys.items():
            yi = y[idx] if groups is None else _demean(y[idx], groups[idx])
            out[k][i] = _ols(xi, yi)[0]
    return out


def fit_all(
    frame: pd.DataFrame,
    series: list[str] = SERIES,
    draws: int = DRAWS,
    seed: int = SEED,
    groups: str | None = None,
) -> tuple[list[Fit], dict[str, np.ndarray]]:
    """Fits for every series on the rows where all of them are finite; returns the slope draws too.

    With ``groups`` (a column, e.g. vendor) the slope is the fixed-effects slope: OLS on data demeaned within
    each group, HC3 from OLS with group dummies, Theil–Sen on the demeaned data.
    """
    cols = ["year", *series]
    sub = frame[[*cols, groups] if groups else cols].dropna(subset=cols)
    if len(sub) < 3:
        raise ValueError(f"too few rows for a trend: {len(sub)}")
    x0 = sub["year"].to_numpy(dtype=float)
    g = sub[groups].astype(str).to_numpy() if groups else None
    ys0 = {s: sub[s].to_numpy(dtype=float) for s in series}
    draws_by = bootstrap(x0, ys0, draws, seed, g)
    x = x0 if g is None else _demean(x0, g)
    design = sm.add_constant(x0)
    if g is not None:
        dummies = pd.get_dummies(pd.Series(g), drop_first=True, dtype=float).to_numpy()
        design = np.column_stack([design, dummies])
    fits = []
    for s, y0 in ys0.items():
        y = y0 if g is None else _demean(y0, g)
        b, a = _ols(x, y)
        hc3 = sm.OLS(y0, design).fit(cov_type="HC3")
        lo, hi = (float(v) for v in np.percentile(draws_by[s], [2.5, 97.5]))
        fits.append(
            Fit(
                series=s,
                n=len(x),
                slope=b,
                intercept=a,
                doubling_years=_doubling(b),
                se_hc3=float(hc3.bse[1]),
                slope_ci=(lo, hi),
                doubling_ci=(_doubling(hi), _doubling(lo)),
                theil_sen=float(theilslopes(y, x)[0]),
            )
        )
    return fits, draws_by


def check_additivity(fits: list[Fit], terms: list[str] = TERMS) -> float:
    """The term slopes must sum to the headline slope on the same sample; returns the gap."""
    by = {f.series: f.slope for f in fits}
    gap = abs(sum(by[f"log2_{t}"] for t in terms) - by["log2_headline"])
    if gap > 1e-9:
        raise ValueError(f"term slopes do not add up to the headline slope: gap {gap:.3g}")
    return gap


def contrast(
    draws_by: dict[str, np.ndarray], plus: list[str], minus: list[str], fits: list[Fit]
) -> dict[str, Any]:
    """A linear combination of slopes with its bootstrap interval: sum(plus) − sum(minus)."""
    by = {f.series: f.slope for f in fits}
    point = sum(by[s] for s in plus) - sum(by[s] for s in minus)
    d = sum(draws_by[s] for s in plus) - sum(draws_by[s] for s in minus)
    lo, hi = (float(v) for v in np.percentile(d, [2.5, 97.5]))
    return {
        "plus": plus,
        "minus": minus,
        "estimate": float(point),
        "ci": [lo, hi],
        "excludes_zero": lo > 0 or hi < 0,
    }
