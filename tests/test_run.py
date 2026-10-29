"""Phase 3 analysis (`chipledger.analysis.run`) on a small synthetic dataset in the raw string format."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from typer.testing import CliRunner

from chipledger import identity, schema
from chipledger.analysis import chain, run, tables
from chipledger.cli import app
from chipledger.identity import Options

SEED = {
    "vendors": {
        "NVIDIA": {"chain": ["K20X", "M40", "P100", "V100", "A100", "H100", "B200"], "chain_candidates": []},
        "AMD": {"chain": ["MI60", "MI100", "MI300X"], "chain_candidates": ["MI400 series"]},
    }
}
LADDER = [  # product, vendor, year, flagship, variant_of, wafer_scale
    ("K20X", "NVIDIA", 2012, "false", "", "false"),
    ("K40", "NVIDIA", 2013, "true", "", "false"),
    ("M40", "NVIDIA", 2015, "true", "", "false"),
    ("P100 SXM2", "NVIDIA", 2016, "true", "", "false"),
    ("V100 SXM2", "NVIDIA", 2017, "true", "", "false"),
    ("A100 SXM4", "NVIDIA", 2020, "true", "", "false"),
    ("A100 PCIe", "NVIDIA", 2020, "false", "A100 SXM4", "false"),
    ("H100 SXM5", "NVIDIA", 2022, "true", "", "false"),
    ("MI60", "AMD", 2018, "true", "", "false"),
    ("MI100", "AMD", 2020, "true", "", "false"),
    ("MI325X", "AMD", 2024, "true", "", "false"),
    ("MI300X", "AMD", 2023, "false", "MI325X", "false"),
    ("WSE", "Cerebras", 2021, "true", "", "true"),
    ("Cloud AI 100 Ultra", "Qualcomm", 2023, "false", "", "false"),
]


def dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(7)
    rows, src = [], []
    for i, (p, v, y, flag, var, wafer) in enumerate(LADDER):
        g = y - 2012
        row = dict.fromkeys(schema.COLUMNS, "")
        vals = {
            "transistors_b": 7.0 * 2 ** (0.5 * g + rng.normal(0, 0.1)),
            "die_area_compute_total_mm2": 550 * 2 ** (0.05 * g + rng.normal(0, 0.05)),
            "boost_clock_mhz": 800 * 2 ** (0.07 * g + rng.normal(0, 0.05)),
            "tdp_w": 235 * 2 ** (0.15 * g + rng.normal(0, 0.05)),
            "fp32": 4.0 * 2 ** (0.4 * g + rng.normal(0, 0.1)),
            "fp16_tensor": 8.0 * 2 ** (0.8 * g + rng.normal(0, 0.1)),
            "int8_tensor": 16.0 * 2 ** (0.9 * g + rng.normal(0, 0.1)),
            "fp16_tensor_sparse": 16.0 * 2 ** (0.8 * g + rng.normal(0, 0.1)) * 2,
            "mem_bandwidth_gbs": 250 * 2 ** (0.35 * g + rng.normal(0, 0.05)),
            "mem_capacity_gb": 6 * 2 ** (0.4 * g),
        }
        if p in ("MI325X", "MI300X"):  # no die area: A′ only
            vals.pop("die_area_compute_total_mm2")
        if p == "MI325X":  # sparse must stay above dense
            vals["fp16_tensor_sparse"] = vals["fp16_tensor"] * 2
        vals["fp16_tensor_sparse"] = max(vals["fp16_tensor_sparse"], vals["fp16_tensor"])
        row.update(
            vendor=v,
            product=p,
            announce_date=f"{y}-0{1 + i % 9}-01",
            ship_date=f"{y}-1{i % 3}-01" if i % 2 else "",
            is_flagship=flag,
            variant_of=var,
            wafer_scale=wafer,
            process_node="TSMC 7nm" if y >= 2018 else "28 nm",
            foundry="TSMC",
            die_area_total_mm2="",
        )
        for c, x in vals.items():
            row[c] = f"{x:.6g}"
            src.append([p, c, f"{x:.6g}", "https://example.org", "2026-10-29", "high", ""])
        for c in schema.TEXT_SOURCED:
            if row[c]:
                src.append([p, c, row[c], "https://example.org", "2026-10-29", "high", ""])
        rows.append(row)
    src[0][5] = "medium"  # K20X transistors_b
    return pd.DataFrame(rows, columns=schema.COLUMNS), pd.DataFrame(src, columns=schema.SOURCE_COLUMNS)


NODES = pd.DataFrame({"node": ["TSMC 28nm", "TSMC N7"], "hvm_year": [2011, 2018]})
MLPERF = pd.DataFrame(
    {
        "product": ["P100 SXM2", "V100 SXM2", "A100 SXM4", "H100 SXM5"],
        "benchmark": ["bert"] * 4,
        "suite": ["training"] * 4,
        "scenario": ["closed"] * 4,
        "rule": ["first"] * 4,
        "per_accelerator": [1.0, 2.0, 4.0, 8.0],
    }
)


@pytest.fixture(scope="module")
def numbers() -> dict:
    raw, src = dataset()
    assert schema.validate(raw, src).ok, schema.validate(raw, src).errors
    return run.run(raw, src, NODES, SEED, MLPERF)


def test_population_excludes_variants_and_cards(numbers: dict) -> None:
    pop = numbers["population"]
    assert pop["products"] == len(LADDER)
    assert pop["primary"] == len(LADDER) - 3  # two variants and the multi-chip card
    assert numbers["population"]["excluded_not_per_package"] == ["Cloud AI 100 Ultra"]


def test_trend_terms_add_up(numbers: dict) -> None:
    fits = numbers["estimator_b"]["fits"]
    total = sum(f["slope"] for k, f in fits.items() if k != "headline")
    assert total == pytest.approx(fits["headline"]["slope"], abs=1e-9)


def test_hypotheses_have_verdicts(numbers: dict) -> None:
    allowed = {"supported", "falsified", "not supported", "partly supported", "not assessed"}
    allowed.add("not assessable")
    for k in ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]:
        assert numbers["hypotheses"][k]["verdict"] in allowed


def test_h6_on_a_doubling_benchmark(numbers: dict) -> None:
    h6 = numbers["hypotheses"]["H6"]
    assert h6["benchmarks"][0]["n"] == 4
    assert h6["benchmarks"][0]["slope_realized"] == pytest.approx(3 / (2022 - 2016), rel=0.2)
    assert numbers["hypotheses"]["H6"]["best_rule"]["verdict"] == "not assessed"


def test_reconciliation_multiplies_out(numbers: dict) -> None:
    c = numbers["estimator_c"]
    assert c["start"] == "K20X" and c["end"] == "H100 SXM5"
    assert c["physical_nf"] * c["architecture_spec_x_precision"] == pytest.approx(c["headline_ratio"])
    assert c["nvidia"]["total"] == pytest.approx(1000.0)


def test_chain_resolves_to_primaries(numbers: dict) -> None:
    a = numbers["estimator_a"]
    assert "MI325X" in a["amd_a_prime"]["resolved"] and "MI300X" not in a["amd_a_prime"]["resolved"]
    assert "MI300X" in a["amd_a_prime_mi300x"]["resolved"]
    assert a["nvidia_a"]["resolved"][:3] == ["K20X", "M40", "P100 SXM2"]


def test_resolve_rejects_ambiguity() -> None:
    d = pd.DataFrame({"product": ["A1 x", "A1 y"], "variant_of": ["", ""]})
    with pytest.raises(ValueError, match="ambiguous"):
        chain.resolve(d, ["A1"])
    assert chain.resolve(d, ["Z"]) == []


def test_sensitivities_cover_section_6(numbers: dict) -> None:
    labels = [r["label"] for r in numbers["sensitivity"]]
    for want in [
        "primary",
        "ship date",
        "FP32 reference",
        "floating-point headline",
        "headline with sparsity",
        "area including I/O dies",
        "clock-free identity",
        "all products in the sample",
        "all products, vendor fixed effects",
        "NVIDIA only",
        "without wafer-scale",
        "frontier envelope",
        "high-confidence values only",
    ]:
        assert want in labels
    assert any(lbl.startswith("without ") and lbl != "without wafer-scale" for lbl in labels)


def test_numbers_are_json_safe(numbers: dict) -> None:
    text = json.dumps(numbers, allow_nan=False)
    assert "Infinity" not in text


def test_tables_render(numbers: dict) -> None:
    t = tables.all_tables(numbers)
    assert len(t) == 9
    assert all(re.search(r"\|-{3,}\|", md) for md in t.values())
    assert "H7" in t["t1_hypotheses.md"]


def test_options_change_the_definitions() -> None:
    raw, _ = dataset()
    base = identity.derive(schema.typed(raw))
    fl = identity.derive(schema.typed(raw), Options(headline="float"))
    sp = identity.derive(schema.typed(raw), Options(headline="sparse"))
    f32 = identity.derive(schema.typed(raw), Options(reference="fp32"))
    ship = identity.derive(schema.typed(raw), Options(date="ship"))
    assert (base["headline_format"] == "int8_tensor").all()
    assert (fl["headline_format"] == "fp16_tensor").all()
    assert (sp["headline_tflops"] >= base["headline_tflops"]).all()
    assert f32["ref_is_fp32"].all() and (f32["ref_format"] == "fp32").all()
    assert ship["year"].isna().sum() == (raw["ship_date"] == "").sum()


def test_frontier_and_swap() -> None:
    f = pd.DataFrame({"product": list("abcd"), "year": [1.0, 2.0, 3.0, 4.0], "headline_tflops": [1, 3, 2, 5]})
    assert run.frontier(f)["product"].tolist() == ["a", "b", "d"]
    raw, _ = dataset()
    s = run.swap_primary(raw, "MI300X").set_index("product")
    assert s.loc["MI300X", "variant_of"] == "" and s.loc["MI325X", "variant_of"] == "MI300X"
    assert s.loc["MI300X", "is_flagship"] == "true"


def test_node_mapping() -> None:
    assert run.node_of("TSMC 4N", "TSMC") == "TSMC N4"
    assert run.node_of("TSMC 3nm | 6nm FinFET", "") == "TSMC N3"
    assert run.node_of("28 nm", "") == ""  # foundry not published: not mapped
    assert run.node_of("14nm", "Samsung") == "Samsung 14nm FinFET"
    assert run.node_of("16 nm FinFET", "TSMC") == "TSMC 16FF+"  # not N6
    assert run.node_of("TSMC 16nm", "") == "TSMC 16FF+"


def test_blank_low_confidence() -> None:
    raw, src = dataset()
    out = run.blank_low_confidence(raw, src)
    assert out.loc[out["product"] == "K20X", "transistors_b"].iloc[0] == ""


def test_cli_analyze(tmp_path: Path) -> None:
    raw, src = dataset()
    a, s, n, sd = tmp_path / "a.csv", tmp_path / "s.csv", tmp_path / "n.csv", tmp_path / "seed.yaml"
    raw.to_csv(a, index=False)
    src.to_csv(s, index=False)
    NODES.to_csv(n, index=False)
    sd.write_text(json.dumps(SEED))
    args = ["analyze", "--products", str(a), "--sources", str(s), "--nodes", str(n), "--seed", str(sd)]
    args += ["--mlperf", str(tmp_path / "none.csv"), "--out", str(tmp_path / "r")]
    res = CliRunner().invoke(app, args)
    assert res.exit_code == 0, res.output
    assert (tmp_path / "r" / "numbers.json").exists()
    assert (tmp_path / "r" / "tables" / "t5_sensitivity.md").exists()
    assert "H6: not assessed" in res.output


def test_h6_skips_excluded_rows() -> None:
    raw, _ = dataset()
    d = run.prepare(raw)
    ml = MLPERF.assign(excluded=["", "", "", "not comparable"], scenario=[None] * 4)
    out = run.h6(ml, d)
    assert out["verdict"] == "supported" and out["benchmarks"][0]["n"] == 3
    assert run.h6(None, d)["verdict"] == "not assessed"


def test_figures_draw(numbers: dict, tmp_path: Path) -> None:
    from chipledger.analysis import figures

    raw, _ = dataset()
    drawn = figures.draw_all(raw, numbers, MLPERF.assign(excluded="", rule="first"), tmp_path)
    assert drawn == figures.NAMES
    for name in drawn:
        assert (tmp_path / f"{name}.svg").stat().st_size > 1000 and (tmp_path / f"{name}.png").exists()
