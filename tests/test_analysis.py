"""Chain and trend estimators on a synthetic ladder where every term grows at a known rate."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from chipledger.analysis import chain, trend
from chipledger.identity import TERMS, derive

RATES = {  # doublings per year, by construction
    "density_mtr_mm2": 0.4,
    "area_mm2": 0.1,
    "boost_clock_mhz": 0.05,
    "spec_ops_per_transistor_cycle": 0.25,
    "precision_multiplier": 0.2,
}


def ladder(n: int = 8, noise: float = 0.0, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        year = 2012 + 2 * i
        jitter = rng.normal(0, noise, len(RATES)) if noise else np.zeros(len(RATES))
        term = {t: 2 ** (RATES[t] * (year - 2012) + j) for t, j in zip(RATES, jitter, strict=True)}
        area = 100.0 * term["area_mm2"]
        density = 10.0 * term["density_mtr_mm2"]
        transistors_b = density * area / 1e3
        clock = 1000.0 * term["boost_clock_mhz"]
        spec = 1e-3 * term["spec_ops_per_transistor_cycle"]
        ref = spec * transistors_b * clock * 1e3  # TFLOP/s
        rows.append(
            {
                "product": f"chip{i}",
                "vendor": "X",
                "is_flagship": True,
                "announce_date": pd.Timestamp(f"{year}-01-01"),
                "transistors_b": transistors_b,
                "die_area_compute_total_mm2": area,
                "boost_clock_mhz": clock,
                "tdp_w": 100.0 + 50 * i,
                "fp16_tensor": ref,
                "int8_tensor": ref * term["precision_multiplier"],
                "mem_bandwidth_gbs": 100.0 * 2 ** (0.3 * (year - 2012)),
            }
        )
    df = pd.DataFrame(rows)
    for c in ["fp64", "fp32", "fp16", "bf16", "bf16_tensor", "fp8_tensor", "fp4_tensor", "fp6_tensor"]:
        df[c] = np.nan
    for c in ["fp64_tensor", "tf32_tensor", "int4_tensor"]:
        df[c] = np.nan
    for c in [
        f"{t}_sparse"
        for t in [
            "tf32_tensor",
            "fp16_tensor",
            "bf16_tensor",
            "fp8_tensor",
            "fp6_tensor",
            "fp4_tensor",
            "int8_tensor",
            "int4_tensor",
        ]
    ]:
        df[c] = np.nan
    return derive(df)


def test_chain_steps_add_up_and_recover_rates() -> None:
    d = ladder()
    st = chain.steps(d, [f"chip{i}" for i in range(8)])
    assert len(st) == 7
    for _, r in st.iterrows():
        assert abs(sum(r[f"dlog2_{t}"] for t in TERMS) - r["dlog2_headline"]) < 1e-9
    cum = chain.cumulative(st)
    assert cum["members"][0] == "chip0" and cum["members"][-1] == "chip7"
    assert cum["years"] == pytest.approx(14.0)
    assert cum["dlog2_headline"] == pytest.approx(14 * sum(RATES.values()))
    for t, rate in RATES.items():
        assert cum["shares"][t] == pytest.approx(rate / sum(RATES.values()))
    assert cum["dlog2"]["transistors_b"] == pytest.approx(14 * (RATES["density_mtr_mm2"] + RATES["area_mm2"]))
    sh = chain.shares(st)
    assert sh[list(TERMS)].sum(axis=1).round(9).eq(1).all()


def test_chain_skips_members_outside_the_decomposition_sample() -> None:
    d = ladder()
    d.loc[d["product"] == "chip3", "sample_a"] = False
    st = chain.steps(d, ["chip2", "chip3", "chip4", "ghost"])
    assert st[["from", "to"]].values.tolist() == [["chip2", "chip4"]]
    assert chain.cumulative(chain.steps(d, ["ghost"]))["members"] == []


def test_trend_slopes_add_up_and_recover_rates() -> None:
    d = ladder(noise=0.05)
    fits, draws = trend.fit_all(d, draws=200, seed=3)
    assert trend.check_additivity(fits) < 1e-9
    by = {f.series: f for f in fits}
    assert by["log2_headline"].slope == pytest.approx(sum(RATES.values()), abs=0.03)
    for t, rate in RATES.items():
        f = by[f"log2_{t}"]
        assert f.slope == pytest.approx(rate, abs=0.03)
        assert f.slope_ci[0] <= f.slope <= f.slope_ci[1]
        assert f.doubling_ci[0] <= f.doubling_years <= f.doubling_ci[1]
        assert f.se_hc3 > 0
    c = trend.contrast(
        draws,
        ["log2_spec_ops_per_transistor_cycle", "log2_precision_multiplier"],
        ["log2_density_mtr_mm2"],
        fits,
    )
    assert c["estimate"] == pytest.approx(0.25 + 0.2 - 0.4, abs=0.03)
    assert c["ci"][0] <= c["estimate"] <= c["ci"][1]
    assert isinstance(c["excludes_zero"], bool)
    assert by["log2_headline"].to_dict()["slope_ci"] == list(by["log2_headline"].slope_ci)


def test_trend_additivity_check_rejects_mismatch() -> None:
    fits, _ = trend.fit_all(ladder(), draws=50)
    fits[0].slope += 1
    with pytest.raises(ValueError, match="do not add up"):
        trend.check_additivity(fits)


def test_doubling_of_nonpositive_slope_is_infinite() -> None:
    assert trend._doubling(0.0) == float("inf")
    assert trend._doubling(-0.1) == float("inf")


def test_figures_render(tmp_path) -> None:  # type: ignore[no-untyped-def]
    from chipledger.analysis import figures

    d = ladder(noise=0.05)
    st = chain.steps(d, [f"chip{i}" for i in range(8)])
    fits, _ = trend.fit_all(d, draws=20)
    figures.f2_chain(st, tmp_path)
    figures.f1_ladder(d, fits, tmp_path)
    for name in ["f1_ladder", "f2_chain"]:
        assert (tmp_path / f"{name}.svg").stat().st_size > 1000
        assert (tmp_path / f"{name}.png").stat().st_size > 1000


def test_chain_on_identity_a_prime() -> None:
    from chipledger.identity import TERMS_N

    d = ladder()
    st = chain.steps(d, [f"chip{i}" for i in range(8)], TERMS_N, "sample_an")
    cum = chain.cumulative(st)
    assert set(cum["shares"]) == set(TERMS_N)
    assert cum["shares"]["transistors_mtr"] == pytest.approx(
        (RATES["density_mtr_mm2"] + RATES["area_mm2"]) / sum(RATES.values())
    )
    fits, _ = trend.fit_all(d, ["log2_headline", *[f"log2_{t}" for t in TERMS_N]], draws=20)
    assert trend.check_additivity(fits, TERMS_N) < 1e-9
