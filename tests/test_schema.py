from pathlib import Path

import pandas as pd

from chipledger import schema
from chipledger.schema import COLUMNS, SOURCE_COLUMNS


def product(**values: object) -> dict[str, str]:
    row = dict.fromkeys(COLUMNS, "")
    row.update({k: str(v) for k, v in values.items()})
    return row


def source(product: str, field: str, value: object, **over: str) -> dict[str, str]:
    row = {
        "product": product,
        "field": field,
        "value": str(value),
        "url": "https://example.org/spec",
        "access_date": "2026-10-29",
        "confidence": "high",
        "note": "",
    }
    row.update(over)
    return row


GOOD = product(
    vendor="x",
    product="p1",
    announce_date="2020-05-14",
    ship_date="2020-06-01",
    is_flagship="true",
    transistors_b=54.2,
    die_area_compute_total_mm2=826,
    boost_clock_mhz=1410,
    tdp_w=400,
    fp16_tensor=312,
)
FIELDS = (
    "announce_date",
    "ship_date",
    "transistors_b",
    "die_area_compute_total_mm2",
    "boost_clock_mhz",
    "tdp_w",
    "fp16_tensor",
)
GOOD_SOURCES = [source("p1", f, GOOD[f]) for f in FIELDS]


def report(rows: list[dict[str, str]], sources: list[dict[str, str]]) -> schema.Report:
    return schema.validate(
        pd.DataFrame(rows, columns=COLUMNS).astype(str),
        pd.DataFrame(sources, columns=SOURCE_COLUMNS).astype(str),
    )


def test_clean_dataset_passes() -> None:
    rep = report([GOOD], GOOD_SOURCES)
    assert rep.ok and rep.warnings == []


def test_every_value_needs_a_matching_source() -> None:
    rep = report([GOOD], GOOD_SOURCES[:-1])
    assert any("fp16_tensor" in e and "no row" in e for e in rep.errors)
    rep = report([GOOD], GOOD_SOURCES[:-1] + [source("p1", "fp16_tensor", 311)])
    assert any("sources.csv says 311" in e for e in rep.errors)


def test_row_rules() -> None:
    bad = dict(GOOD, announce_date="May 2020", ship_date="2019-01-01", transistors_b="many", tdp_w="-1")
    bad["is_flagship"] = "yes"
    msgs = "\n".join(report([bad], GOOD_SOURCES).errors)
    for needle in ("announce_date", "ship_date", "transistors_b", "tdp_w", "is_flagship"):
        assert needle in msgs


def test_variants_sparsity_and_prices() -> None:
    v = product(
        vendor="x",
        product="p2",
        announce_date="2020-05-14",
        variant_of="p1",
        is_flagship="true",
        fp16_tensor=300,
        fp16_tensor_sparse=200,
        launch_price_usd=10000,
    )
    srcs = GOOD_SOURCES + [
        source("p2", "announce_date", "2020-05-14"),
        source("p2", "fp16_tensor", 300),
        source("p2", "fp16_tensor_sparse", 200),
        source("p2", "launch_price_usd", 10000),
    ]
    msgs = "\n".join(report([GOOD, v], srcs).errors)
    assert "a variant cannot be the flagship" in msgs
    assert "smaller than the dense rate" in msgs
    assert "price_confidence" in msgs
    ghost = product(vendor="x", product="p3", announce_date="2020-05-14", variant_of="nope")
    rep = report([GOOD, ghost], GOOD_SOURCES + [source("p3", "announce_date", "2020-05-14")])
    assert any("variant_of" in e for e in rep.errors)


def test_source_rows_are_checked() -> None:
    srcs = GOOD_SOURCES + [
        source("p9", "tdp_w", 1, url="ftp://x", access_date="yesterday", confidence="sure")
    ]
    srcs.append(source("p1", "notes", "x"))
    msgs = "\n".join(report([GOOD], srcs).errors)
    for needle in (
        "unknown product",
        "url must be",
        "access_date",
        "confidence must be",
        "not a sourced field",
    ):
        assert needle in msgs


def test_flagship_coverage_warning_and_duplicates() -> None:
    thin = product(vendor="y", product="p1", announce_date="2021-01-01", is_flagship="true", bf16_tensor=275)
    rep = report([GOOD, thin], GOOD_SOURCES + [source("p1", "bf16_tensor", 275)])
    assert any("duplicate product" in e for e in rep.errors)
    thin["product"] = "t1"
    srcs = GOOD_SOURCES + [source("t1", "announce_date", "2021-01-01"), source("t1", "bf16_tensor", 275)]
    rep = report([GOOD, thin], srcs)
    assert rep.ok
    assert any("t1" in w and "outside the decomposition sample" in w for w in rep.warnings)


def test_column_set_is_checked() -> None:
    rep = schema.validate(pd.DataFrame({"product": ["x"]}), pd.DataFrame(columns=SOURCE_COLUMNS))
    assert any("missing columns" in e for e in rep.errors)


def test_load_types(tmp_path: Path) -> None:
    pd.DataFrame([GOOD], columns=COLUMNS).to_csv(tmp_path / "a.csv", index=False)
    df = schema.load(tmp_path / "a.csv")
    assert df.loc[0, "transistors_b"] == 54.2 and bool(df.loc[0, "is_flagship"])
    assert pd.isna(df.loc[0, "fp32"]) and not bool(df.loc[0, "wafer_scale"])
