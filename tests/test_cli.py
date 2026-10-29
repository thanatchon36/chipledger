from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from chipledger import __version__
from chipledger.cli import app
from chipledger.schema import COLUMNS, SOURCE_COLUMNS

runner = CliRunner()


def product(**values: object) -> dict[str, str]:
    row = dict.fromkeys(COLUMNS, "")
    row.update({k: str(v) for k, v in values.items()})
    return row


def source(product: str, field: str, value: object) -> dict[str, str]:
    return {
        "product": product,
        "field": field,
        "value": str(value),
        "url": "https://example.org/spec",
        "access_date": "2026-10-29",
        "confidence": "high",
        "note": "",
    }


FULL = product(
    vendor="x",
    product="full",
    announce_date="2020-05-14",
    is_flagship="true",
    transistors_b=54.2,
    die_area_compute_total_mm2=826,
    boost_clock_mhz=1410,
    tdp_w=400,
    fp16_tensor=312,
)
THIN = product(
    vendor="y", product="thin", announce_date="2021-06-01", is_flagship="true", bf16_tensor=275, notes="n/a"
)


def write(tmp: Path, rows: list[dict[str, str]], sources: list[dict[str, str]]) -> tuple[Path, Path]:
    a, s = tmp / "accelerators.csv", tmp / "sources.csv"
    pd.DataFrame(rows, columns=COLUMNS).to_csv(a, index=False)
    pd.DataFrame(sources, columns=SOURCE_COLUMNS).to_csv(s, index=False)
    return a, s


def test_version() -> None:
    assert runner.invoke(app, ["version"]).output.strip() == __version__


def test_validate_passes_and_fails(tmp_path: Path) -> None:
    fields = (
        "announce_date",
        "transistors_b",
        "die_area_compute_total_mm2",
        "boost_clock_mhz",
        "tdp_w",
        "fp16_tensor",
    )
    srcs = [source("full", f, FULL[f]) for f in fields]
    a, s = write(tmp_path, [FULL, THIN], srcs + [source("thin", "announce_date", "2021-06-01")])
    r = runner.invoke(app, ["validate", "--products", str(a), "--sources", str(s)])
    assert r.exit_code == 1 and "bf16_tensor = 275 has no row" in r.output
    a, s = write(
        tmp_path, [FULL, THIN], srcs + [source("thin", f, THIN[f]) for f in ("announce_date", "bf16_tensor")]
    )
    r = runner.invoke(app, ["validate", "--products", str(a), "--sources", str(s)])
    assert r.exit_code == 0, r.output
    assert "2 products, 0 errors, 1 warnings" in r.output and "thin: flagship outside" in r.output


def test_derive_and_coverage(tmp_path: Path) -> None:
    a, _ = write(tmp_path, [FULL, THIN], [])
    out = tmp_path / "derived.csv"
    r = runner.invoke(app, ["derive", "--products", str(a), "--out", str(out)])
    assert r.exit_code == 0, r.output
    assert "2 products, 1 in the decomposition sample" in r.output
    d = pd.read_csv(out).set_index("product")
    assert abs(d.loc["full", "residual_a"]) < 1e-9 and pd.isna(d.loc["thin", "residual_a"])
    cov = tmp_path / "coverage.md"
    r = runner.invoke(app, ["coverage", "--products", str(a), "--out", str(cov)])
    assert r.exit_code == 0 and "1 of 2 products outside" in r.output
    text = cov.read_text()
    assert "| thin | transistors_b, die_area_compute_total_mm2, boost_clock_mhz, tdp_w | n/a |" in text
    a, _ = write(tmp_path, [FULL], [])
    r = runner.invoke(app, ["coverage", "--products", str(a), "--out", str(cov)])
    assert "(none)" in cov.read_text()


def test_empty_dataset_is_valid(tmp_path: Path) -> None:
    a, s = write(tmp_path, [], [])
    r = runner.invoke(app, ["validate", "--products", str(a), "--sources", str(s)])
    assert r.exit_code == 0 and "0 products, 0 errors" in r.output
    r = runner.invoke(app, ["derive", "--products", str(a), "--out", str(tmp_path / "d.csv")])
    assert r.exit_code == 0, r.output
