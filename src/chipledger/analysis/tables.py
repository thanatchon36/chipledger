"""Markdown tables from results/numbers.json, as returned by :func:`chipledger.analysis.run.run`."""

from __future__ import annotations

from typing import Any

TERM_LABEL = {
    "headline": "headline P",
    "density_mtr_mm2": "density N/A",
    "area_mm2": "area A",
    "boost_clock_mhz": "clock f",
    "spec_ops_per_transistor_cycle": "specialization R/(N f)",
    "spec_ops_per_transistor_us": "specialization R/N (clock-free)",
    "precision_multiplier": "precision P/R",
    "transistors_mtr": "transistors N",
    "transistors_b": "transistors N",
    "ref_tflops": "reference R",
    "tflops_per_w": "P/W",
    "ref_tflops_per_w": "R/W",
    "tflops_per_mm2": "P/A",
    "tflops_per_btransistor": "P/N",
    "tdp_w": "power W",
    "mem_bandwidth_gbs": "memory bandwidth",
    "mem_capacity_gb": "memory capacity",
    "ops_per_byte": "operations per byte (P/bandwidth)",
}


def _f(x: Any, nd: int = 3) -> str:
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, int | float):
        return f"{x:.{nd}f}"
    return str(x)


def _ci(ci: list[Any] | None, nd: int = 3) -> str:
    if not ci:
        return "—"
    lo, hi = ci
    return f"[{_f(lo, nd) if lo is not None else '−∞'}, {_f(hi, nd) if hi is not None else '∞'}]"


def _table(head: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def _label(k: str) -> str:
    return TERM_LABEL.get(k, k)


def trend_table(fits: dict[str, Any]) -> str:
    rows = []
    for k, f in fits.items():
        rows.append(
            [
                _label(k),
                str(f["n"]),
                _f(f["slope"]),
                _ci(f["slope_ci"]),
                _f(f["doubling_years"], 2),
                _ci(f["doubling_ci"], 2),
                _f(f["se_hc3"]),
                _f(f["theil_sen"]),
            ]
        )
    head = ["series", "n", "slope (doublings/yr)", "95% CI", "doubling (yr)", "95% CI", "HC3 se", "Theil–Sen"]
    return _table(head, rows)


def single_table(block: dict[str, Any]) -> str:
    rows = []
    for k, v in block.items():
        f = v.get("fit")
        if f is None:
            rows.append([_label(k), str(v["n"]), "—", "—", "—", "—"])
            continue
        rows.append(
            [
                _label(k),
                str(v["n"]),
                _f(f["slope"]),
                _ci(f["slope_ci"]),
                _f(f["doubling_years"], 2),
                _ci(f["doubling_ci"], 2),
            ]
        )
    return _table(["series", "n", "slope (doublings/yr)", "95% CI", "doubling (yr)", "95% CI"], rows)


def chain_table(c: dict[str, Any]) -> str:
    if not c["steps"]:
        return f"No two chain members in the sample (resolved: {', '.join(c['resolved'])}).\n"
    terms = list(c["cumulative"]["shares"])
    head = ["step", "years", "Δlog2 P", *[f"Δlog2 {_label(t)}" for t in terms]]
    rows = []
    for s in c["steps"]:
        rows.append(
            [
                f"{s['from']} → {s['to']}",
                _f(s["year_to"] - s["year_from"], 2),
                _f(s["dlog2_headline"], 2),
                *[_f(s[f"dlog2_{t}"], 2) for t in terms],
            ]
        )
    cu = c["cumulative"]
    rows.append(
        [
            f"**cumulative {cu['members'][0]} → {cu['members'][-1]}**",
            _f(cu["years"], 2),
            _f(cu["dlog2_headline"], 2),
            *[_f(cu["dlog2"][t], 2) for t in terms],
        ]
    )
    rows.append(["**share of cumulative Δlog2 P**", "", "1.000", *[_f(cu["shares"][t]) for t in terms]])
    return _table(head, rows)


def hypotheses_table(n: dict[str, Any]) -> str:
    h = n["hypotheses"]
    h1, h2, h3, h4, h5, h7 = h["H1"], h["H2"], h["H3"], h["H4"], h["H5"], h["H7"]
    c = h3["b_contrast"]
    rows = [
        [
            "H1",
            "doubling of P ≤ 1.5 yr and 95% CI upper bound < 2.0 yr",
            f"{_f(h1['doubling'], 2)} yr, CI {_ci(h1['doubling_ci'], 2)}, n = {h1['n']}",
            h1["verdict"],
        ],
        [
            "H2",
            "(a) density doubling ≥ 2.5 yr; (b) density share of NVIDIA chain < 1/3",
            f"(a) {_f(h2['a_density_doubling'], 2)} yr; (b) {_f(h2['b_density_share'])} ({h2['b_chain']})",
            h2["verdict"],
        ],
        [
            "H3",
            "(a) chain: spec + precision share > density share; (b) regression: spec + precision − density "
            "slope > 0, CI excludes 0",
            f"(a) {_f(h3['a_arch_share'])} vs {_f(h3['a_density_share'])}; "
            f"(b) {_f(c['estimate'])} doublings/yr, CI {_ci(c['ci'])}",
            h3["verdict"] + f" ((a) {'passes' if h3['a_pass'] else 'fails'}, (b) "
            f"{'passes' if h3['b_pass'] else 'fails'})",
        ],
        [
            "H4",
            "NVIDIA chain: mean Δlog2 area and TDP larger on steps ending after 2020",
            (
                f"area {_f(h4.get('mean_dlog2_area_mm2_late'), 2)} vs "
                f"{_f(h4.get('mean_dlog2_area_mm2_early'), 2)}; "
                f"TDP {_f(h4.get('mean_dlog2_tdp_w_late'), 2)} vs {_f(h4.get('mean_dlog2_tdp_w_early'), 2)} "
                f"(late steps: {', '.join(h4['late_steps'])})"
            ),
            h4["verdict"],
        ],
        [
            "H5",
            "slope of P − slope of bandwidth > 0, CI excludes 0 (flagship decomposition sample)",
            f"{_f(h5['contrast']['estimate'])} doublings/yr, CI {_ci(h5['contrast']['ci'])}, n = {h5['n']}",
            h5["verdict"],
        ],
        ["H6", "MLPerf per-accelerator slope < headline slope on every benchmark", *_h6(h)],
        [
            "H7",
            "K20X → H100: growth of N·f ≥ 10×",
            f"{_f(h7['nf_growth'], 1)}×",
            h7["verdict"],
        ],
    ]
    return _table(["", "rule (PREREGISTRATION §5)", "estimate", "verdict"], rows)


def _h6(h: dict[str, Any]) -> list[str]:
    h6 = h.get("H6")
    if not h6:
        return ["—", "not assessed"]
    parts = [
        f"{b['benchmark']} ({b['vendor']}, n = {b['n']}): "
        f"{_f(b['slope_realized'])} vs {_f(b['slope_headline'])}"
        for b in h6.get("benchmarks", [])
    ]
    return ["; ".join(parts) or h6.get("reason", "no benchmark qualifies"), h6["verdict"]]


def reconciliation_table(c: dict[str, Any], c32: dict[str, Any]) -> str:
    nv = c["nvidia"]
    fx, fx32 = c["factors"], c32["factors"]
    rows = [
        [
            "headline rate",
            f"{_f(c['start_rate']['tflops'], 2)} {c['start_rate']['format']} → "
            f"{_f(c['end_rate']['tflops'], 1)} {c['end_rate']['format']}",
            "",
            "",
        ],
        [
            "total (dense)",
            f"{_f(c['headline_ratio'], 1)}×",
            f"{_f(c32['headline_ratio'], 1)}×",
            f"{_f(nv['total_dense'], 0)}× (1000× with 2× sparsity)",
        ],
        ["density", f"{_f(fx['density_mtr_mm2'], 2)}×", f"{_f(fx32['density_mtr_mm2'], 2)}×", ""],
        ["area", f"{_f(fx['area_mm2'], 2)}×", f"{_f(fx32['area_mm2'], 2)}×", ""],
        ["clock", f"{_f(fx['boost_clock_mhz'], 2)}×", f"{_f(fx32['boost_clock_mhz'], 2)}×", ""],
        [
            "**physical: N·f**",
            f"**{_f(c['physical_nf'], 1)}×**",
            f"{_f(c32['physical_nf'], 1)}×",
            f"process {_f(nv['process'], 1)}×",
        ],
        [
            "specialization",
            f"{_f(fx['spec_ops_per_transistor_cycle'], 2)}×",
            f"{_f(fx32['spec_ops_per_transistor_cycle'], 2)}×",
            f"complex instructions {_f(nv['complex_instructions'], 1)}×",
        ],
        [
            "precision multiplier",
            f"{_f(fx['precision_multiplier'], 2)}×",
            f"{_f(fx32['precision_multiplier'], 2)}×",
            f"number representation {_f(nv['number_representation'], 1)}×",
        ],
        [
            "**non-physical: spec × precision**",
            f"**{_f(c['architecture_spec_x_precision'], 1)}×**",
            f"{_f(c32['architecture_spec_x_precision'], 1)}×",
            f"{_f(nv['non_physical'], 0)}×",
        ],
    ]
    return _table(
        ["factor", "identity A (primary reference)", "identity A (FP32 reference)", "NVIDIA (Dally 2023)"],
        rows,
    )


def sensitivity_table(rows_in: list[dict[str, Any]]) -> str:
    rows = []
    for r in rows_in:
        if "error" in r:
            rows.append([r["label"], str(r["n"]), f"not computable ({r['error']})", *["—"] * 6])
            continue
        h3 = r.get("h3b")
        rows.append(
            [
                r["label"],
                str(r["n"]),
                f"{_f(r['headline_doubling'], 2)} {_ci(r['headline_doubling_ci'], 2)}",
                _f(r.get("density_doubling"), 2),
                f"{_f(h3['estimate'])} {_ci(h3['ci'])}" if h3 else "—",
                _f(r.get("chain_density_share")) if "chain" in r else "same as primary",
                _f(r.get("chain_spec_share")) if "chain" in r else "",
                _f(r.get("chain_precision_share")) if "chain" in r else "",
                r.get("chain", ""),
            ]
        )
    head = [
        "variant",
        "n",
        "P doubling (yr) [95% CI]",
        "density doubling (yr)",
        "H3b: spec + prec − density (dbl/yr) [95% CI]",
        "chain: density share",
        "chain: spec share",
        "chain: precision share",
        "chain",
    ]
    return _table(head, rows)


def sensitivity_short(rows_in: list[dict[str, Any]]) -> str:
    """The paper's version of the §6 table: rates and the H3b contrast, typographic minus signs."""
    rows = []
    for r in rows_in:
        if "error" in r:
            rows.append([r["label"], str(r["n"]), "not computable", "—", "—"])
            continue
        h3 = r.get("h3b")
        rows.append(
            [
                r["label"],
                str(r["n"]),
                f"{_f(r['headline_doubling'], 2)} {_ci(r['headline_doubling_ci'], 2)}",
                _f(r.get("density_doubling"), 2),
                f"{_f(h3['estimate'])} {_ci(h3['ci'])}" if h3 else "—",
            ]
        )
    head = [
        "variant",
        "n",
        "P doubling, yr [95% CI]",
        "density doubling, yr",
        "H3b contrast, dbl/yr [95% CI]",
    ]
    return _table(head, [[*r[:2], *(c.replace("-", "−") for c in r[2:])] for r in rows])


def nodes_table(n: dict[str, Any]) -> str:
    rows = [
        [
            p["product"],
            p["process_node"].replace("|", "/"),
            p["node"],
            _f(p["hvm_year"], 0),
            _f(p["year"], 2),
            _f(p["lag_years"], 2),
        ]
        for p in sorted(n["products"], key=lambda p: p["year"])
    ]
    return _table(
        ["product", "process (as published)", "node row", "volume production", "announced", "lag (yr)"], rows
    )


def all_tables(n: dict[str, Any]) -> dict[str, str]:
    """File name -> Markdown."""
    a = n["estimator_a"]
    rq1 = n["rq1_throughput"]
    t: dict[str, str] = {}
    t["t1_hypotheses.md"] = "# Hypotheses H1–H7\n\n" + hypotheses_table(n)
    t["t2_trend.md"] = (
        "# Estimator (b): flagship decomposition sample, identity A\n\n"
        + f"Products: {', '.join(n['estimator_b']['products'])}.\n\n"
        + trend_table(n["estimator_b"]["fits"])
        + "\n## Identity A′ (no area), flagships\n\n"
        + f"Products: {', '.join(n['estimator_b_a_prime']['products'])}.\n\n"
        + trend_table(n["estimator_b_a_prime"]["fits"])
        + "\n## Clock-free identity, flagships\n\n"
        + f"Products: {', '.join(n['estimator_b_clock_free']['products'])}.\n\n"
        + trend_table(n["estimator_b_clock_free"]["fits"])
    )
    t["t3_chains.md"] = "# Estimator (a): chain-linked decomposition\n\n" + "\n".join(
        f"## {title}\n\n" + chain_table(a[key])
        for key, title in [
            ("nvidia_a", "NVIDIA, identity A"),
            ("nvidia_a_prime", "NVIDIA, identity A′"),
            ("nvidia_clock_free", "NVIDIA, clock-free identity"),
            ("amd_a_prime", "AMD, identity A′"),
            ("amd_a_prime_mi300x", "AMD, identity A′, MI300X as the primary variant"),
            ("amd_clock_free", "AMD, clock-free identity"),
            ("nvidia_b", "NVIDIA, identity B (P = P/W · W)"),
            ("amd_b", "AMD, identity B"),
            ("nvidia_c", "NVIDIA, identity C (P = P/A · A)"),
        ]
    )
    t["t4_reconciliation.md"] = (
        "# Estimator (c): K20X → H100 SXM against NVIDIA's account\n\n"
        + reconciliation_table(n["estimator_c"], n["estimator_c_fp32_reference"])
    )
    t["t5_sensitivity.md"] = "# Sensitivity analyses (PREREGISTRATION §6)\n\n" + sensitivity_table(
        n["sensitivity"]
    )
    t["t5_sensitivity_paper.md"] = "# Sensitivity analyses, short form\n\n" + sensitivity_short(
        n["sensitivity"]
    )
    t["t6_throughput.md"] = "# RQ1: throughput-trend sample and Moore's law\n\n" + "\n".join(
        f"## {title}\n\n" + single_table(rq1[key])
        for key, title in [
            ("flagships", "Flagships"),
            ("flagships_density", "Flagships with density"),
            ("all_primary", "All primary products"),
            ("frontier", "Frontier envelope"),
            ("flagships_no_wafer", "Flagships without wafer-scale"),
            ("flagships_mi300x_primary", "Flagships, MI300X as the primary variant"),
            ("flagships_ship_date", "Flagships with a ship date, by ship date"),
            ("flagships_ship_date_products_by_announce", "The same products, by announce date"),
        ]
    )
    t["t7_efficiency_memory.md"] = (
        "# RQ3 efficiency and RQ4 memory (flagships)\n\n"
        + single_table(n["rq3_efficiency"])
        + "\n"
        + single_table(n["rq4_memory"])
    )
    t["t8_nodes.md"] = "# Node adoption lag\n\n" + nodes_table(n["nodes"])
    return t
