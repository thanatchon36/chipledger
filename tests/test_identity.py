import math

import pandas as pd
import pytest

from chipledger import identity
from chipledger.schema import COLUMNS, typed


def product(**values: object) -> dict[str, str]:
    row = dict.fromkeys(COLUMNS, "")
    row.update({k: str(v) for k, v in values.items()})
    return row


# synthetic rows in the shape of real products; the numbers are placeholders for the test, not data
V = product(
    vendor="x",
    product="v",
    announce_date="2017-05-10",
    transistors_b=21.1,
    die_area_compute_total_mm2=815,
    boost_clock_mhz=1530,
    tdp_w=300,
    fp32=15.7,
    fp16=31.4,
    fp16_tensor=125,
    mem_bandwidth_gbs=900,
)
A = product(
    vendor="x",
    product="a",
    announce_date="2020-05-14",
    transistors_b=54.2,
    die_area_compute_total_mm2=826,
    boost_clock_mhz=1410,
    tdp_w=400,
    fp32=19.5,
    fp16_tensor=312,
    bf16_tensor=312,
    int8_tensor=624,
    fp16_tensor_sparse=624,
    int8_tensor_sparse=1248,
    mem_bandwidth_gbs=1555,
)
K = product(
    vendor="x",
    product="k",
    announce_date="2012-11-12",
    transistors_b=7.1,
    die_area_compute_total_mm2=561,
    boost_clock_mhz=732,
    tdp_w=235,
    fp32=3.95,
    mem_bandwidth_gbs=250,
)
T = product(
    vendor="y", product="t", announce_date="2021-06-01", bf16_tensor=275, tdp_w=200
)  # no silicon data


def frame(*rows: dict[str, str]) -> pd.DataFrame:
    return typed(pd.DataFrame(list(rows), columns=COLUMNS))


def test_reference_and_headline_rules() -> None:
    d = identity.derive(frame(V, A, K)).set_index("product")
    assert d.loc["v", "ref_format"] == "fp16_tensor" and d.loc["v", "headline_format"] == "fp16_tensor"
    assert d.loc["v", "precision_multiplier"] == 1
    assert d.loc["a", "headline_format"] == "int8_tensor" and d.loc["a", "precision_multiplier"] == 2
    assert d.loc["k", "ref_format"] == "fp32" and bool(d.loc["k", "ref_is_fp32"])
    assert not bool(d.loc["v", "ref_is_fp32"])


def test_identities_hold_exactly() -> None:
    d = identity.derive(frame(V, A, K))
    assert identity.check(d) < identity.TOL
    for col in ("residual_a", "residual_b", "residual_c"):
        assert (d[col].abs() < identity.TOL).all()


def test_terms_multiply_back_to_headline() -> None:
    d = identity.derive(frame(A)).iloc[0]
    prod = 1.0
    for t in identity.TERMS:
        prod *= float(d[t])
    assert prod == pytest.approx(624.0)
    assert float(d["density_mtr_mm2"]) == pytest.approx(54.2e3 / 826)


def test_sparsity_and_ops_per_byte() -> None:
    d = identity.derive(frame(A, V)).set_index("product")
    assert d.loc["a", "sparsity_multiplier"] == 2
    assert math.isnan(float(d.loc["v", "sparsity_multiplier"]))
    assert float(d.loc["a", "ops_per_byte"]) == pytest.approx(624e3 / 1555)


def test_incomplete_rows_stay_out_of_the_identity() -> None:
    d = identity.derive(frame(T, V)).set_index("product")
    assert math.isnan(float(d.loc["t", "residual_a"]))
    assert float(d.loc["t", "headline_tflops"]) == 275
    assert float(d.loc["t", "tflops_per_w"]) == pytest.approx(275 / 200)
    assert identity.check(d) < identity.TOL  # NaN rows are skipped, not passed


def test_check_raises_on_a_broken_identity() -> None:
    d = identity.derive(frame(A))
    d.loc[0, "residual_a"] = 1e-6
    with pytest.raises(ValueError, match="residual"):
        identity.check(d)


def test_decimal_year() -> None:
    assert identity.decimal_year("2020-01-01") == 2020.0
    assert identity.decimal_year("2021-07-02") == pytest.approx(2021.5, abs=0.01)
