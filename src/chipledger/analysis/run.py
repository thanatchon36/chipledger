"""Phase 3: every pre-registered analysis of PREREGISTRATION.md §4–§7, as one dictionary of results.

``run`` takes the raw product and source tables and the seed list, and returns the content of
``results/numbers.json``; :mod:`chipledger.analysis.tables` turns it into Markdown tables. Nothing here reads
or writes files, so every number in the paper can be traced to one call.

Samples (§2–§3). Only primary variants enter, and products whose rates are not per package
(``NOT_PER_PACKAGE``, Gate 2) are left out of every analysis. The *flagship decomposition sample* is the
flagships with N, A, f, W and R (``sample_a``); it is the primary sample of estimator (b) and of H1, H2a, H3b
and H5. The NVIDIA chain of estimator (a) is the seed's chain resolved to primary rows, restricted to the
members in the identity's sample.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd

from chipledger import identity, schema
from chipledger.analysis import chain, trend
from chipledger.identity import TERMS, TERMS_CF, TERMS_N, Options

NOT_PER_PACKAGE = frozenset({"Cloud AI 100 Ultra"})  # Gate 2: a multi-SoC card with an unstated SoC count
H4_CUTOFF = 2021.0  # H4: steps whose later member was announced after 2020-12-31
IDENTITIES: dict[str, tuple[list[str], str]] = {
    "A": (TERMS, "sample_a"),
    "A_prime": (TERMS_N, "sample_an"),
    "clock_free": (TERMS_CF, "sample_cf"),
}
LOG_EXTRA = [  # series used by the secondary analyses and identities B and C
    "ref_tflops",
    "fp32",
    "transistors_b",
    "tdp_w",
    "tflops_per_w",
    "ref_tflops_per_w",
    "tflops_per_mm2",
    "tflops_per_btransistor",
    "mem_bandwidth_gbs",
    "mem_capacity_gb",
    "ops_per_byte",
]
# Dally, Hot Chips 2023, as frozen in PREREGISTRATION §4 (c): factors of single-chip inference K20X -> H100
NVIDIA_ACCOUNT = {
    "number_representation": 16.0,
    "complex_instructions": 12.5,
    "process": 2.5,
    "sparsity": 2.0,
}


# ---------------------------------------------------------------------------------------------- frames


def prepare(raw: pd.DataFrame, opts: Options = identity.PRIMARY) -> pd.DataFrame:
    """Derived table for every product (variants included), with the log2 columns the analyses use."""
    d = identity.derive(schema.typed(raw), opts)
    identity.check(d)
    for c in LOG_EXTRA:
        d[f"log2_{c}"] = np.log2(d[c])
    d["variant_of"] = d["variant_of"].fillna("")
    d["sample_w"] = d[["headline_tflops", "tdp_w"]].notna().all(axis=1)
    d["sample_wa"] = d[["headline_tflops", "tdp_w", "area_mm2"]].notna().all(axis=1)
    return d


def primaries(d: pd.DataFrame) -> pd.DataFrame:
    """Primary variants with per-package rates: the population of every analysis."""
    return d[d["variant_of"].eq("") & ~d["product"].isin(NOT_PER_PACKAGE)].copy()


def flagships(d: pd.DataFrame) -> pd.DataFrame:
    p = primaries(d)
    return p[p["is_flagship"].astype(bool)]


def frontier(frame: pd.DataFrame) -> pd.DataFrame:
    """Products that set a new maximum headline rate when announced (ties on a date both count)."""
    f = frame.dropna(subset=["year", "headline_tflops"]).sort_values(["year", "headline_tflops"])
    best, keep = -math.inf, []
    for i, r in f.iterrows():
        if r["headline_tflops"] > best:
            keep.append(i)
            best = r["headline_tflops"]
    return f.loc[keep]


def blank_low_confidence(raw: pd.DataFrame, sources: pd.DataFrame) -> pd.DataFrame:
    """The raw table without every value whose source is medium or low confidence (Gate 1 sensitivity)."""
    out = raw.copy()
    weak = sources[sources["confidence"] != "high"]
    for p, f in zip(weak["product"], weak["field"], strict=True):
        out.loc[out["product"] == p, f] = ""
    return out


def swap_primary(raw: pd.DataFrame, new: str) -> pd.DataFrame:
    """Make the variant ``new`` the primary of its silicon (ship-date / Gate 2 sensitivity)."""
    out = raw.copy()
    old = out.loc[out["product"] == new, "variant_of"].iloc[0]
    out.loc[out["variant_of"] == old, "variant_of"] = new
    out.loc[out["product"] == old, "variant_of"] = new
    out.loc[out["product"] == new, "variant_of"] = ""
    flag = out.loc[out["product"] == old, "is_flagship"].iloc[0]
    out.loc[out["product"] == old, "is_flagship"] = "false"
    out.loc[out["product"] == new, "is_flagship"] = flag
    return out


# -------------------------------------------------------------------------------------------- helpers


def _clean(x: Any) -> Any:
    """JSON-safe: inf and NaN become None, numpy scalars become Python numbers."""
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, list | tuple):
        return [_clean(v) for v in x]
    if isinstance(x, np.generic):
        x = x.item()
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def _series(terms: list[str]) -> list[str]:
    return ["log2_headline", *[f"log2_{t}" for t in terms]]


SAMPLE_FIELDS = [  # the paper's table of the decomposition sample: the five inputs and the derived terms
    "vendor",
    "product",
    "year",
    "process_node",
    "transistors_b",
    "area_mm2",
    "boost_clock_mhz",
    "tdp_w",
    "ref_tflops",
    "ref_format",
    "headline_tflops",
    "headline_format",
    "density_mtr_mm2",
    "spec_ops_per_transistor_cycle",
    "precision_multiplier",
    "mem_bandwidth_gbs",
    "wafer_scale",
]


def sample_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """The products of a decomposition sample, oldest first, with their inputs and terms."""
    rows = frame.sort_values("year")[SAMPLE_FIELDS].to_dict("records")
    out = [{str(k): (bool(v) if k == "wafer_scale" else v) for k, v in r.items()} for r in rows]
    for r in out:  # the paper's worked example quotes specialization per million transistors
        r["spec_ops_per_mtransistor_cycle"] = r["spec_ops_per_transistor_cycle"] * 1e6
    return out


def _products(frame: pd.DataFrame, cols: list[str]) -> list[str]:
    sub = frame.dropna(subset=["year", *cols])
    return [str(p) for p in sub.sort_values("year")["product"]]


def decomposition_trend(
    sample: pd.DataFrame, terms: list[str] = TERMS, groups: str | None = None
) -> dict[str, Any]:
    """Estimator (b) for one identity on one sample, with the H3b contrast."""
    series = _series(terms)
    fits, draws = trend.fit_all(sample, series, groups=groups)
    trend.check_additivity(fits, terms)
    spec, prec = f"log2_{terms[-2]}", f"log2_{terms[-1]}"
    physical = [f"log2_{t}" for t in terms[:-2]]
    out: dict[str, Any] = {
        "n": fits[0].n,
        "products": _products(sample, series),
        "fits": {f.series.removeprefix("log2_"): f.to_dict() for f in fits},
        "contrast_arch_minus_physical": trend.contrast(draws, [spec, prec], physical, fits),
    }
    if "density_mtr_mm2" in terms:
        out["contrast_arch_minus_density"] = trend.contrast(
            draws, [spec, prec], ["log2_density_mtr_mm2"], fits
        )
    ts = {f.series: f.theil_sen for f in fits}
    out["theil_sen_arch_minus_density"] = (
        ts[spec] + ts[prec] - ts["log2_density_mtr_mm2"] if "density_mtr_mm2" in terms else None
    )
    return out


def single_trends(frame: pd.DataFrame, series: list[str]) -> dict[str, Any]:
    """Each series fitted on its own sample (the flagships that publish it)."""
    out: dict[str, Any] = {}
    for s in series:
        sub = frame.dropna(subset=["year", s])
        if len(sub) < 3 or sub["year"].nunique() < 2:
            out[s.removeprefix("log2_")] = {"n": len(sub), "fit": None}
            continue
        fits, _ = trend.fit_all(sub, [s])
        out[s.removeprefix("log2_")] = {
            "n": fits[0].n,
            "fit": fits[0].to_dict(),
            "products": _products(sub, [s]),
        }
    return out


def chain_result(d: pd.DataFrame, names: list[str], terms: list[str], sample: str) -> dict[str, Any]:
    p = primaries(d)
    members = [m for m in chain.resolve(d, names) if m in set(p["product"])]
    st = chain.steps(p, members, terms, sample)
    return {
        "requested": names,
        "resolved": members,
        "in_sample": chain.cumulative(st)["members"],
        "steps": st.to_dict("records"),
        "step_shares": chain.shares(st).to_dict("records") if not st.empty else [],
        "cumulative": chain.cumulative(st),
    }


def _chain_names(seed: dict[str, Any], vendor: str) -> list[str]:
    v = seed["vendors"][vendor]
    return [*v["chain"], *v.get("chain_candidates", [])]


# ------------------------------------------------------------------------------------------ hypotheses


def h4(steps: list[dict[str, Any]], cols: tuple[str, ...] = ("area_mm2", "tdp_w")) -> dict[str, Any]:
    """Mean per-step Δlog2 of area and TDP, steps ending after 2020 vs earlier steps (descriptive)."""
    late = [s for s in steps if s["year_to"] >= H4_CUTOFF]
    early = [s for s in steps if s["year_to"] < H4_CUTOFF]
    out: dict[str, Any] = {"late_steps": [f"{s['from']} → {s['to']}" for s in late]}
    out["early_steps"] = [f"{s['from']} → {s['to']}" for s in early]
    if not late or not early:
        return {**out, "verdict": "not assessable"}
    for c in cols:
        out[f"mean_dlog2_{c}_late"] = float(np.mean([s[f"dlog2_{c}"] for s in late]))
        out[f"mean_dlog2_{c}_early"] = float(np.mean([s[f"dlog2_{c}"] for s in early]))
    both = all(out[f"mean_dlog2_{c}_late"] > out[f"mean_dlog2_{c}_early"] for c in cols)
    out["verdict"] = "supported" if both else "not supported"
    return out


def reconcile(d: pd.DataFrame, start: str, end: str) -> dict[str, Any]:
    """Estimator (c): identity A from ``start`` to ``end`` against NVIDIA's account (§4)."""
    p = primaries(d).set_index("product")
    rec = p.to_dict("index")
    a, b = rec[start], rec[end]

    def ratio(c: str) -> float:
        return float(b[c]) / float(a[c])

    factors = {t: ratio(t) for t in TERMS}
    nf = ratio("transistors_b") * ratio("boost_clock_mhz")
    arch = factors["spec_ops_per_transistor_cycle"] * factors["precision_multiplier"]
    nv = NVIDIA_ACCOUNT
    nv_dense = nv["number_representation"] * nv["complex_instructions"] * nv["process"]
    return {
        "start": start,
        "end": end,
        "start_rate": {"tflops": float(a["headline_tflops"]), "format": a["headline_format"]},
        "end_rate": {"tflops": float(b["headline_tflops"]), "format": b["headline_format"]},
        "headline_ratio": ratio("headline_tflops"),
        "factors": factors,
        "transistor_ratio": ratio("transistors_b"),
        "clock_ratio": ratio("boost_clock_mhz"),
        "physical_nf": nf,
        "architecture_spec_x_precision": arch,
        "nvidia": {
            **nv,
            "total": nv_dense * nv["sparsity"],
            "total_dense": nv_dense,
            "non_physical": nv["number_representation"] * nv["complex_instructions"],
        },
        "physical_over_nvidia_process": nf / nv["process"],
        "h7_verdict": "supported" if nf >= 10.0 else "falsified",
    }


# ------------------------------------------------------------------------------------------ sensitivity


def sensitivity_row(
    label: str,
    d: pd.DataFrame,
    seed: dict[str, Any],
    *,
    select: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    identity_name: str = "A",
    groups: str | None = None,
    with_chain: bool = True,
) -> dict[str, Any]:
    """Headline and density doubling times, the H3b contrast and the NVIDIA chain shares on one variant."""
    terms, sample = IDENTITIES[identity_name]
    base = primaries(d)
    pool = base[base[sample]]
    pool = select(pool) if select else pool[pool["is_flagship"].astype(bool)]
    row: dict[str, Any] = {"label": label, "identity": identity_name}
    try:
        res = decomposition_trend(pool, terms, groups)
    except ValueError as e:
        return {**row, "n": len(pool), "error": str(e)}
    fits = res["fits"]
    row.update(
        n=res["n"],
        products=res["products"],
        headline_doubling=fits["headline"]["doubling_years"],
        headline_doubling_ci=fits["headline"]["doubling_ci"],
        headline_slope=fits["headline"]["slope"],
        headline_theil_sen=fits["headline"]["theil_sen"],
    )
    if "density_mtr_mm2" in terms:
        row.update(
            density_doubling=fits["density_mtr_mm2"]["doubling_years"],
            density_theil_sen=fits["density_mtr_mm2"]["theil_sen"],
            h3b=res["contrast_arch_minus_density"],
            h3b_theil_sen=res["theil_sen_arch_minus_density"],
        )
    if with_chain:
        c = chain_result(d, _chain_names(seed, "NVIDIA"), terms, sample)["cumulative"]
        if c["members"]:
            sh = c["shares"]
            row.update(
                chain=f"{c['members'][0]} → {c['members'][-1]}",
                chain_density_share=sh.get("density_mtr_mm2"),
                chain_arch_share=sh[terms[-2]] + sh[terms[-1]],
                chain_spec_share=sh[terms[-2]],
                chain_precision_share=sh[terms[-1]],
            )
    return row


def sensitivities(raw: pd.DataFrame, sources: pd.DataFrame, seed: dict[str, Any]) -> list[dict[str, Any]]:
    """§6, in its order, plus the sensitivities promised at Gates 1 and 2."""
    d = prepare(raw)
    rows = [sensitivity_row("primary", d, seed)]
    for label, opts in [
        ("ship date", Options(date="ship")),
        ("FP32 reference", Options(reference="fp32")),
        ("floating-point headline", Options(headline="float")),
        ("headline with sparsity", Options(headline="sparse")),
        ("area including I/O dies", Options(area="total")),
    ]:
        rows.append(sensitivity_row(label, prepare(raw, opts), seed))
    rows.append(sensitivity_row("clock-free identity", d, seed, identity_name="clock_free"))
    rows.append(sensitivity_row("all products in the sample", d, seed, select=lambda f: f, with_chain=False))
    rows.append(
        sensitivity_row(
            "all products, vendor fixed effects",
            d,
            seed,
            select=lambda f: f,
            groups="vendor",
            with_chain=False,
        )
    )
    rows.append(
        sensitivity_row(
            "NVIDIA only",
            d,
            seed,
            select=lambda f: f[f["is_flagship"].astype(bool) & f["vendor"].eq("NVIDIA")],
            with_chain=False,
        )
    )
    rows.append(
        sensitivity_row(
            "without wafer-scale",
            d,
            seed,
            select=lambda f: f[f["is_flagship"].astype(bool) & ~f["wafer_scale"].astype(bool)],
            with_chain=False,
        )
    )
    rows.append(sensitivity_row("frontier envelope", d, seed, select=frontier, with_chain=False))
    flag = flagships(d)
    for v in sorted(flag.loc[flag["sample_a"], "vendor"].unique()):

        def drop(f: pd.DataFrame, v: str = str(v)) -> pd.DataFrame:
            return f[f["is_flagship"].astype(bool) & f["vendor"].ne(v)]

        rows.append(sensitivity_row(f"without {v}", d, seed, select=drop, with_chain=False))
    rows.append(
        sensitivity_row("high-confidence values only", prepare(blank_low_confidence(raw, sources)), seed)
    )
    rows.append(sensitivity_row("identity A′ (no area)", d, seed, identity_name="A_prime"))
    return rows


# --------------------------------------------------------------------------------------------- nodes


NODE_MAP = [  # (process_node text, foundry text) pattern -> node row; first compute die named first
    (r"(?<!\d)2\s?nm|N2", "TSMC", "TSMC N2"),
    (r"N3P", "TSMC", "TSMC N3P"),
    (r"(?<!\d)3\s?nm|N3", "TSMC", "TSMC N3"),
    (r"4N|N4", "TSMC", "TSMC N4"),
    (r"(?<!\d)5\s?nm|N5", "TSMC", "TSMC N5"),
    (r"(?<!\d)6\s?nm|N6", "TSMC", "TSMC N6"),
    (r"(?<!\d)7\s?nm|N7", "TSMC", "TSMC N7"),
    (r"(?<!\d)12\s?nm", "TSMC", "TSMC 12FFC"),
    (r"(?<!\d)16\s?nm|N16", "TSMC", "TSMC 16FF+"),
    (r"(?<!\d)28\s?nm", "TSMC", "TSMC 28nm"),
    (r"(?<!\d)14\s?nm", "Samsung", "Samsung 14nm FinFET"),
    (r"(?<!\d)14\s?nm", "Intel", "Intel 14nm"),
    (r"(?<!\d)10\s?nm", "Intel", "Intel 10nm"),
    (r"(?<!\d)7\s?nm", "Samsung", "Samsung 7nm EUV (7LPP)"),
    (r"(?<!\d)5\s?nm", "Samsung", "Samsung 5nm EUV"),
]


def node_of(process: str, foundry: str) -> str:
    """The node row for a product's leading compute node; '' when the foundry or node is not in the series."""
    first = process.split("|")[0].strip()
    fdry = foundry if foundry else ("TSMC" if first.upper().startswith("TSMC") else "")
    for pat, f, node in NODE_MAP:
        if fdry.startswith(f) and re.search(pat, first):
            return node
    return ""


def node_lag(d: pd.DataFrame, nodes: pd.DataFrame) -> dict[str, Any]:
    """Years from a node's volume production to the announcement of the accelerators built on it (§7)."""
    hvm = dict(zip(nodes["node"], nodes["hvm_year"].astype(float), strict=True))
    p = primaries(d)
    rows = []
    for _, r in p.iterrows():
        proc = r["process_node"] if isinstance(r["process_node"], str) else ""
        fdry = r["foundry"] if isinstance(r["foundry"], str) else ""
        node = node_of(proc, fdry)
        if node and node in hvm and not math.isnan(r["year"]):
            rows.append(
                {
                    "product": r["product"],
                    "vendor": r["vendor"],
                    "flagship": bool(r["is_flagship"]),
                    "process_node": proc,
                    "foundry": fdry,
                    "node": node,
                    "hvm_year": hvm[node],
                    "year": float(r["year"]),
                    "lag_years": float(r["year"]) - (hvm[node] + 0.5),  # mid-year of volume production
                }
            )
    t = pd.DataFrame(rows)
    out: dict[str, Any] = {"n": len(t), "products": rows}
    if t.empty:
        return out
    out["median_lag"] = float(t["lag_years"].median())
    out["median_lag_by_vendor"] = {
        str(k): float(v) for k, v in t.groupby("vendor")["lag_years"].median().items()
    }
    out["median_lag_flagships"] = float(t.loc[t["flagship"], "lag_years"].median())
    fits, _ = trend.fit_all(t, ["lag_years"])
    out["trend"] = {"slope_years_per_year": fits[0].slope, "ci": list(fits[0].slope_ci), "n": fits[0].n}
    unmapped = p[~p["product"].isin(t["product"])]
    out["unmapped"] = [
        f"{r['product']} ({r['process_node'] if isinstance(r['process_node'], str) else 'no node'})"
        for _, r in unmapped.iterrows()
    ]
    return out


# ------------------------------------------------------------------------------------------------ H6


def h6(mlperf: pd.DataFrame | None, d: pd.DataFrame, rule: str = "first") -> dict[str, Any]:
    """Realized vs headline: per benchmark and vendor with ≥ 3 flagship generations, OLS slopes of log2
    per-accelerator MLPerf throughput and of log2 headline rate on announce year, same products (§5 H6)."""
    if mlperf is None or mlperf.empty:
        return {"verdict": "not assessed", "reason": "no MLPerf data collected", "benchmarks": []}
    flag = flagships(d).set_index("product")
    ml = (
        mlperf.fillna({"scenario": "", "excluded": ""})
        if "excluded" in mlperf
        else mlperf.fillna({"scenario": ""})
    )
    if "excluded" in ml:
        ml = ml[ml["excluded"].astype(str).eq("")]  # rows kept for the record, not comparable across rounds
    m = ml[(ml["rule"] == rule) & ml["product"].isin(flag.index)].copy()
    m["per_accelerator"] = m["per_accelerator"].astype(float)
    m["vendor"] = [flag.loc[p, "vendor"] for p in m["product"]]
    out: list[dict[str, Any]] = []
    for (bench, suite, scen, vendor), g in m.groupby(["benchmark", "suite", "scenario", "vendor"]):
        g = g.drop_duplicates("product")
        if g["product"].nunique() < 3:
            continue
        x = np.array([flag.loc[p, "year"] for p in g["product"]], dtype=float)
        yr = np.log2(g["per_accelerator"].to_numpy(dtype=float))
        yh = np.array([flag.loc[p, "log2_headline"] for p in g["product"]], dtype=float)
        sr, sh = trend._ols(x, yr)[0], trend._ols(x, yh)[0]
        out.append(
            {
                "benchmark": str(bench),
                "suite": str(suite),
                "scenario": str(scen),
                "vendor": str(vendor),
                "n": len(g),
                "products": [str(p) for p in g.sort_values("product")["product"]],
                "slope_realized": sr,
                "slope_headline": sh,
                "realized_below_headline": sr < sh,
            }
        )
    if not out:
        return {
            "verdict": "not assessed",
            "reason": "no benchmark has three flagship generations",
            "benchmarks": [],
        }
    k = sum(b["realized_below_headline"] for b in out)
    verdict = "supported" if k == len(out) else ("partly supported" if k > len(out) / 2 else "not supported")
    return {"verdict": verdict, "rule": rule, "benchmarks": out, "n_below": k}


# ----------------------------------------------------------------------------------------------- run


def run(
    raw: pd.DataFrame,
    sources: pd.DataFrame,
    nodes: pd.DataFrame,
    seed: dict[str, Any],
    mlperf: pd.DataFrame | None = None,
) -> dict[str, Any]:
    d = prepare(raw)
    prim, flag = primaries(d), flagships(d)
    out: dict[str, Any] = {
        "population": {
            "products": len(d),
            "primary": len(prim),
            "excluded_not_per_package": sorted(NOT_PER_PACKAGE),
            "flagships": len(flag),
            "vendors": int(d["vendor"].nunique()),
            "source_rows": len(sources),
            "source_confidence": {str(k): int(v) for k, v in sources["confidence"].value_counts().items()},
            "flagships_with_headline": int(flag["headline_tflops"].notna().sum()),
            **{f"{k}_flagships": int(flag[v].sum()) for k, (_, v) in IDENTITIES.items()},
            **{f"{k}_primary": int(prim[v].sum()) for k, (_, v) in IDENTITIES.items()},
        }
    }

    # estimator (b), primary sample
    decomp = flag[flag["sample_a"]]
    out["sample"] = sample_rows(decomp)
    est_b = decomposition_trend(decomp, TERMS)
    out["estimator_b"] = est_b
    out["estimator_b_a_prime"] = decomposition_trend(flag[flag["sample_an"]], TERMS_N)
    out["estimator_b_clock_free"] = decomposition_trend(flag[flag["sample_cf"]], TERMS_CF)

    # estimator (a)
    chains = {
        "nvidia_a": chain_result(d, _chain_names(seed, "NVIDIA"), TERMS, "sample_a"),
        "nvidia_a_prime": chain_result(d, _chain_names(seed, "NVIDIA"), TERMS_N, "sample_an"),
        "nvidia_clock_free": chain_result(d, _chain_names(seed, "NVIDIA"), TERMS_CF, "sample_cf"),
        "amd_a": chain_result(d, _chain_names(seed, "AMD"), TERMS, "sample_a"),
        "amd_a_prime": chain_result(d, _chain_names(seed, "AMD"), TERMS_N, "sample_an"),
        "amd_clock_free": chain_result(d, _chain_names(seed, "AMD"), TERMS_CF, "sample_cf"),
        "nvidia_b": chain_result(d, _chain_names(seed, "NVIDIA"), ["tflops_per_w", "tdp_w"], "sample_w"),
        "nvidia_c": chain_result(
            d, _chain_names(seed, "NVIDIA"), ["tflops_per_mm2", "area_mm2"], "sample_wa"
        ),
        "amd_b": chain_result(d, _chain_names(seed, "AMD"), ["tflops_per_w", "tdp_w"], "sample_w"),
    }
    swapped = prepare(swap_primary(raw, "MI300X"))
    chains["amd_a_prime_mi300x"] = chain_result(swapped, _chain_names(seed, "AMD"), TERMS_N, "sample_an")
    out["estimator_a"] = chains

    # estimator (c)
    h100 = chain.resolve(d, ["H100"])[0]
    out["estimator_c"] = reconcile(d, "K20X", h100)
    # NVIDIA's "number representation" starts from FP32: the same accounting with FP32 as every reference
    out["estimator_c_fp32_reference"] = reconcile(prepare(raw, Options(reference="fp32")), "K20X", h100)

    # hypotheses
    fb = est_b["fits"]
    nv = chains["nvidia_a"]["cumulative"]
    head, dens = fb["headline"], fb["density_mtr_mm2"]
    h3b = est_b["contrast_arch_minus_density"]
    arch_share = nv["shares"]["spec_ops_per_transistor_cycle"] + nv["shares"]["precision_multiplier"]
    bw_sample = decomp.dropna(subset=["log2_mem_bandwidth_gbs"])
    bfits, bdraws = trend.fit_all(bw_sample, ["log2_headline", "log2_mem_bandwidth_gbs"])
    h5 = trend.contrast(bdraws, ["log2_headline"], ["log2_mem_bandwidth_gbs"], bfits)
    allbw = flag.dropna(subset=["log2_headline", "log2_mem_bandwidth_gbs"])
    afits, adraws = trend.fit_all(allbw, ["log2_headline", "log2_mem_bandwidth_gbs"])
    h4_res = h4(chains["nvidia_a"]["steps"])
    h4_full = h4(chains["nvidia_b"]["steps"], ("tdp_w",))  # TDP only, every chain member with a TDP
    out["hypotheses"] = {
        "H1": {
            "doubling": head["doubling_years"],
            "doubling_ci": head["doubling_ci"],
            "n": head["n"],
            "verdict": "supported"
            if head["doubling_years"] <= 1.5
            and head["doubling_ci"][1] is not None
            and head["doubling_ci"][1] < 2.0
            else "falsified",
        },
        "H2": {
            "a_density_doubling": dens["doubling_years"],
            "a_pass": dens["doubling_years"] >= 2.5,
            "b_chain": f"{nv['members'][0]} → {nv['members'][-1]}",
            "b_density_share": nv["shares"]["density_mtr_mm2"],
            "b_pass": nv["shares"]["density_mtr_mm2"] < 1 / 3,
            # the change in an endpoint's transistor count or die area that would move the share to 1/3
            # (P is unchanged: a different N moves density and specialization in opposite directions)
            "b_margin_endpoint_change": 2 ** (nv["dlog2_headline"] / 3 - nv["dlog2"]["density_mtr_mm2"]) - 1,
        },
        "H3": {
            "a_arch_share": arch_share,
            "a_density_share": nv["shares"]["density_mtr_mm2"],
            "a_pass": arch_share > nv["shares"]["density_mtr_mm2"],
            "b_contrast": h3b,
            "b_pass": h3b["estimate"] > 0 and h3b["ci"][0] > 0,
        },
        "H4": {**h4_res, "supplementary_tdp_full_chain": h4_full},
        "H5": {
            "n": bfits[0].n,
            "products": _products(bw_sample, ["log2_mem_bandwidth_gbs"]),
            "fits": {f.series.removeprefix("log2_"): f.to_dict() for f in bfits},
            "contrast": h5,
            "verdict": "supported" if h5["ci"][0] > 0 else "not supported",
            "all_flagships": {
                "n": afits[0].n,
                "fits": {f.series.removeprefix("log2_"): f.to_dict() for f in afits},
                "contrast": trend.contrast(adraws, ["log2_headline"], ["log2_mem_bandwidth_gbs"], afits),
            },
        },
        "H7": {
            "nf_growth": out["estimator_c"]["physical_nf"],
            "threshold": 10.0,
            "verdict": out["estimator_c"]["h7_verdict"],
        },
    }
    h = out["hypotheses"]
    h["H6"] = h6(mlperf, d, "first")
    h["H6"]["best_rule"] = h6(mlperf, d, "best")
    h["H2"]["verdict"] = "supported" if h["H2"]["a_pass"] and h["H2"]["b_pass"] else "falsified"
    h["H3"]["verdict"] = "supported" if h["H3"]["a_pass"] and h["H3"]["b_pass"] else "falsified"

    # RQ1: the throughput-trend sample and Moore's law in both forms
    ship_flag = flagships(prepare(raw, Options(date="ship")))
    rq1 = {
        "flagships": single_trends(flag, ["log2_headline", "log2_ref_tflops", "log2_transistors_b"]),
        "flagships_density": single_trends(flag, ["log2_density_mtr_mm2"]),
        # descriptive lines of the ladder figure (F1)
        "flagships_ladder": single_trends(flag, ["log2_fp32", "log2_area_mm2"]),
        "all_primary": single_trends(prim, ["log2_headline", "log2_ref_tflops", "log2_transistors_b"]),
        "frontier": single_trends(frontier(prim), ["log2_headline"]),
        "frontier_products": [str(p) for p in frontier(prim)["product"]],
        "flagships_no_wafer": single_trends(flag[~flag["wafer_scale"].astype(bool)], ["log2_headline"]),
        "flagships_mi300x_primary": single_trends(flagships(swapped), ["log2_headline"]),
        "flagships_ship_date": single_trends(ship_flag, ["log2_headline"]),
        # the same products by announce date: separates the date convention from the change of sample
        "flagships_ship_date_products_by_announce": single_trends(
            flag[flag["product"].isin(ship_flag.dropna(subset=["year"])["product"])], ["log2_headline"]
        ),
    }
    out["rq1_throughput"] = rq1

    # §7 secondary
    out["rq3_efficiency"] = single_trends(
        flag,
        ["log2_tflops_per_w", "log2_ref_tflops_per_w", "log2_tflops_per_mm2", "log2_tflops_per_btransistor"],
    )
    out["rq3_efficiency"]["price"] = {"n": int(prim["launch_price_usd"].notna().sum()), "fit": None}
    out["rq4_memory"] = single_trends(
        flag, ["log2_mem_bandwidth_gbs", "log2_mem_capacity_gb", "log2_ops_per_byte", "log2_headline"]
    )
    # the same trends as growth factors per two years, the unit Gholami et al. (2024) report in
    out["per_two_years"] = {
        k: 2 ** (2 * v["fit"]["slope"]) for k, v in out["rq4_memory"].items() if v.get("fit")
    }
    out["nodes"] = node_lag(d, nodes)
    out["sensitivity"] = sensitivities(raw, sources, seed)
    return _clean(out)  # type: ignore[no-any-return]
