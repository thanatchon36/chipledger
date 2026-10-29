"""The paper builder (`chipledger.paper`): placeholders, the hand-typed-number check, cross-references."""

from pathlib import Path

import pytest

from chipledger.paper import _table, check, crossref, fill, fmt, lookup, number_captions, results

DATA = {
    "sensitivity": [
        {"label": "primary", "headline_doubling": 0.8276},
        {"label": "NVIDIA only", "headline_doubling": 0.85},
    ],
    "n": 1234567,
    "ci": [0.04, 0.15],
    "missing": None,
}


def test_lookup_with_selectors() -> None:
    assert lookup(DATA, "sensitivity[label=NVIDIA only].headline_doubling") == 0.85
    assert lookup(DATA, "ci[1]") == 0.15
    with pytest.raises(KeyError):
        lookup(DATA, "sensitivity[label=none].headline_doubling")


def test_fmt() -> None:
    assert fmt(0.08704, "pct1") == "8.7%"
    assert fmt(1234567, ",") == "1,234,567"
    assert fmt(30.4779, "x1") == "30.5×" and fmt(501.01, "x0") == "501×" and fmt(1.234, "x2") == "1.23×"
    assert fmt(None, ".2f") == "n/a"
    assert fmt(1.208, "inv") == "0.83"
    assert fmt(16.0, "lg") == "4.00"
    assert fmt(-0.103, ".3f") == "−0.103"


def test_fill_and_missing_key() -> None:
    assert fill("P doubles every {{sensitivity[label=primary].headline_doubling|.2f}} yr.", DATA) == (
        "P doubles every 0.83 yr."
    )
    with pytest.raises(SystemExit, match="nope"):
        fill("{{nope}}", DATA)


def test_check_flags_hand_typed_numbers_only() -> None:
    text = """---
title: x
fontsize: 10pt
---
From K20X to H100 and MI355X, WSE-2, GC200 and TPU v4 in 2012–2022 (§4.2) [@dally2023], see `--draws 2000`.
The gain was 501× in FP8 and INT4 terms; MLPerf v1.0 and log2 are fine.
Threshold of 1.5 years <!-- numbers-ok: pre-registered -->
![Caption with 12 products](results/figures/f1.svg){#fig:f1 width=100%}
1. A list item with a 95% CI, under CC BY 4.0, and 95% of something else.
"""
    assert check(text) == [(6, "501"), (8, "12"), (9, "95")]


def test_fill_accepts_escaped_pipe_in_tables() -> None:
    assert fill("| {{a.b\\|pct1}} |", {"a": {"b": 0.087}}) == "| 8.7% |"


def test_crossref_numbers_in_order_of_appearance() -> None:
    text = """# Intro
See Figure @fig:b, Table @tbl:t and Section @sec:m.
# Method {#sec:m}
## Detail {#sec:d}
![x](a.svg){#fig:a width=50%}
![y](b.svg){#fig:b}
: cap {#tbl:t}
# References {-}
"""
    out = crossref(text)
    assert "See Figure 2, Table 1 and Section 2." in out
    assert crossref("@sec:d\n" + text).startswith("2.1\n")
    with pytest.raises(SystemExit):
        crossref("@fig:missing")


def test_number_captions_matches_typst_order() -> None:
    body = "![A](a.svg){#fig:a}\n\n: Hyp {#tbl:h}\n\n![B\nwrapped](b.svg){#fig:b width=50%}\n"
    out = number_captions(body)
    assert "![Figure 1. A](a.svg)" in out and "![Figure 2. B\nwrapped]" in out
    assert "**Table 1.** Hyp" in out


def test_results_strip_kinds() -> None:
    data = {
        "hypotheses": {"H1": {"verdict": "supported"}, "H3": {"verdict": "falsified"}, "H6": {"verdict": "x"}}
    }
    rows = results(data)
    assert [r[1] for r in rows] == ["pos", "ref", "nf"]
    assert rows[1][3] == "falsified"


def test_included_tables_lose_their_titles(tmp_path: Path) -> None:
    p = tmp_path / "t.md"
    p.write_text("# Title\n\n| a |\n|---|\n| 1 |\n\n## Sub\n\n| b |\n|---|\n")
    assert _table(p) == "| a |\n|---|\n| 1 |\n\n\n| b |\n|---|"
