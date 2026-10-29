"""Paper figures F1–F7, in the house style shared with the author's other papers.

Libertinus Serif (vendored in ``figures/fonts``), sized so 8 pt prints at 8 pt at a 16 cm text width; no
in-figure titles (panel labels only); light horizontal grid; one fixed colour per identity term (Okabe–Ito),
used in every figure. Every figure is written as SVG with text as paths (PDF build) and 300-dpi PNG.

Each figure draws from the product table (``run.prepare``) for the points and from ``results/numbers.json``
for every fitted line, interval and ratio, so the figures and the paper's text cannot disagree.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from chipledger.analysis import run

ROOT = Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "figures" / "fonts"
INK, MUTED, GRID = "#1a1a1a", "#5a5a5a", "#e3e3e3"
TERM_COLOUR = {
    "density_mtr_mm2": "#0072B2",
    "area_mm2": "#56B4E9",
    "transistors_mtr": "#2F5D8A",
    "boost_clock_mhz": "#999999",
    "spec_ops_per_transistor_cycle": "#009E73",
    "spec_ops_per_transistor_us": "#7FC4A8",
    "precision_multiplier": "#D55E00",
}
TERM_NAME = {
    "density_mtr_mm2": "transistor density",
    "area_mm2": "die area",
    "transistors_mtr": "transistors",
    "boost_clock_mhz": "clock",
    "spec_ops_per_transistor_cycle": "specialization",
    "spec_ops_per_transistor_us": "specialization incl. clock",
    "precision_multiplier": "precision",
}
SERIES_COLOUR = {
    "headline": "#D55E00",
    "ref_tflops": "#009E73",
    "fp32": "#E69F00",
    "transistors_b": "#2F5D8A",
    "density_mtr_mm2": "#0072B2",
    "area_mm2": "#CC79A7",
    "mem_bandwidth_gbs": "#0072B2",
}
WIDTH = 16.0 / 2.54
DOT: dict[str, Any] = {"s": 15, "edgecolors": "white", "linewidths": 0.5, "zorder": 3}
DASH = (0, (3, 2))
NAMES = ["f1_ladder", "f2_chain", "f3_regression", "f4_efficiency", "f5_memory", "f6_mlperf", "f7_dally"]


def setup() -> None:
    for p in sorted(FONT_DIR.glob("LibertinusSerif-*.otf")):
        font_manager.fontManager.addfont(str(p))
    plt.rcParams.update(
        {
            "svg.hashsalt": "chipledger",  # stable element ids: byte-identical SVGs across runs
            "svg.fonttype": "path",
            "font.family": "Libertinus Serif",
            "font.size": 8.5,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.6,
            "axes.edgecolor": "#3a3a3a",
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "axes.axisbelow": True,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "text.color": INK,
            "axes.labelcolor": INK,
            "legend.frameon": False,
            "legend.handlelength": 1.6,
            "savefig.facecolor": "white",
        }
    )


def save(fig: Figure, out: Path, name: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", bbox_inches="tight", pad_inches=0.02, metadata={"Date": None})
    fig.savefig(out / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def panel(ax: Axes, letter: str, text: str | None = None) -> None:
    ax.annotate(
        letter,
        (0, 1),
        xycoords="axes fraction",
        xytext=(0, 12),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=9,
        weight="bold",
    )
    if text:
        ax.annotate(
            text,
            (0, 1),
            xycoords="axes fraction",
            xytext=(12, 12),
            textcoords="offset points",
            ha="left",
            va="top",
            fontsize=8,
        )


def _log_axis(ax: Axes, axis: str = "y") -> None:
    """Log-10 axis with plain-number tick labels (0.1, 1, 10, 1,000)."""
    (ax.set_yscale if axis == "y" else ax.set_xscale)("log")
    fmt = mpl.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def _doubling(fit: dict[str, Any]) -> str:
    lo, hi = fit["doubling_ci"]
    return f"doubling {fit['doubling_years']:.2f} yr [{lo:.2f}, {hi:.2f}]"


def _line(ax: Axes, fit: dict[str, Any], years: pd.Series, colour: str, **kw: Any) -> None:
    """A fitted log2-linear trend drawn in value space over the years of its sample."""
    xs = np.linspace(float(years.min()), float(years.max()), 2)
    ax.plot(xs, 2 ** (fit["intercept"] + fit["slope"] * xs), color=colour, linewidth=1.1, **kw)


def _year_axis(ax: Axes, lo: int = 2012, hi: int = 2026) -> None:
    ax.set_xlim(lo - 0.5, hi + 0.5)
    ax.set_xticks(range(lo, hi + 1, 2))


# ------------------------------------------------------------------------------------------ F1 ladder


def f1_ladder(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """Flagships against year: (a) headline, reference and FP32 rates; (b) transistors, density, area.
    Wafer-scale parts are drawn hollow; they are in every fit."""
    setup()
    rq1 = numbers["rq1_throughput"]
    fits = {**rq1["flagships"], **rq1["flagships_density"], **rq1["flagships_ladder"]}
    panels = [
        [
            ("headline", "headline_tflops", "headline dense rate (TFLOP/s or TOPS)"),
            ("ref_tflops", "ref_tflops", "reference rate, FP16/BF16 (TFLOP/s)"),
            ("fp32", "fp32", "vector FP32 rate (TFLOP/s)"),
        ],
        [
            ("transistors_b", "transistors_b", "transistors per package (billions)"),
            ("density_mtr_mm2", "density_mtr_mm2", "transistor density (MTr/mm²)"),
            ("area_mm2", "area_mm2", "compute die area (mm²)"),
        ],
    ]
    flag = run.flagships(d)
    wafer = flag["wafer_scale"].astype(bool)
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2.9), gridspec_kw={"wspace": 0.22})
    for ax, letter, series in zip(axes, "ab", panels, strict=True):
        for key, col, name in series:
            sub = flag.dropna(subset=["year", col])
            colour = SERIES_COLOUR[key]
            solid, hollow = sub[~wafer.loc[sub.index]], sub[wafer.loc[sub.index]]
            ax.scatter(solid["year"], solid[col], color=colour, **DOT)
            ax.scatter(
                hollow["year"],
                hollow[col],
                s=15,
                facecolors="white",
                edgecolors=colour,
                linewidths=0.9,
                zorder=3,
            )
            fit = fits[key]
            _line(ax, fit["fit"], sub["year"], colour)
            lo, hi = fit["fit"]["doubling_ci"]
            label = (
                f"{name}\nn = {fit['n']}, doubling {fit['fit']['doubling_years']:.2f} yr [{lo:.2f}, {hi:.2f}]"
            )
            ax.plot([], [], color=colour, marker="o", markersize=4, linewidth=1.1, label=label)
        _log_axis(ax)
        ax.set_xlim(2013.3, 2027.0)
        ax.set_xticks([2014, 2016, 2018, 2020, 2022, 2024, 2026])
        ax.tick_params(axis="x", labelsize=7.5)
        ax.set_xlabel("announce year")
        ax.legend(
            loc="upper left", bbox_to_anchor=(-0.02, -0.17), fontsize=7.2, handlelength=1.6, labelspacing=0.5
        )
        panel(ax, letter)
    axes[0].set_ylabel("value (log scale; units in the legend)")
    axes[1].text(
        0.02, 0.98, "hollow: wafer-scale", transform=axes[1].transAxes, va="top", fontsize=7, color=MUTED
    )
    save(fig, out, "f1_ladder")


# ------------------------------------------------------------------------------------------- F2 chain


def _stack(ax: Axes, x: float, parts: list[tuple[str, float]], width: float, horizontal: bool) -> None:
    pos = neg = 0.0
    for term, v in parts:
        base = pos if v >= 0 else neg
        kw: dict[str, Any] = {"color": TERM_COLOUR[term], "linewidth": 0}
        if horizontal:
            ax.barh(x, v, width, left=base, **kw)
        else:
            ax.bar(x, v, width, bottom=base, **kw)
        if v >= 0:
            pos += v
        else:
            neg += v


def f2_chain(numbers: dict[str, Any], out: Path) -> None:
    """(a) Δlog2 per term for each step of the NVIDIA chain; (b) cumulative shares, NVIDIA and AMD."""
    setup()
    nv = numbers["estimator_a"]["nvidia_a"]
    amd = numbers["estimator_a"]["amd_a_prime"]
    terms = [t for t in TERM_NAME if f"dlog2_{t}" in nv["steps"][0]]
    fig, (a, b) = plt.subplots(
        2, 1, figsize=(WIDTH, 5.0), gridspec_kw={"height_ratios": [2.3, 1.0], "hspace": 1.05}
    )
    labels = [f"{s['from'].split()[0]}\n→ {s['to'].split()[0]}" for s in nv["steps"]]
    for i, s in enumerate(nv["steps"]):
        _stack(a, i, [(t, s[f"dlog2_{t}"]) for t in terms], 0.62, horizontal=False)
        a.scatter(i, s["dlog2_headline"], s=16, color=INK, zorder=4)
    a.axhline(0, color="#3a3a3a", linewidth=0.6)
    a.set_xticks(range(len(labels)), labels)
    a.set_ylabel("Δlog2 per step (doublings)")
    handles: list[Any] = [mpl.patches.Patch(color=TERM_COLOUR[t], label=TERM_NAME[t]) for t in terms]
    handles.append(
        mpl.lines.Line2D([], [], marker="o", color=INK, ls="none", ms=4, label="headline (sum of the terms)")
    )
    a.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.24))
    panel(a, "a", "NVIDIA chain, identity A, one bar per generation step")

    rows = [
        (amd, f"AMD {amd['cumulative']['members'][0]} → {amd['cumulative']['members'][-1]}\n(identity A′)"),
        (
            nv,
            f"NVIDIA {nv['cumulative']['members'][0]} → {nv['cumulative']['members'][-1].split()[0]}"
            "\n(identity A)",
        ),
    ]
    for i, (c, _) in enumerate(rows):
        sh = c["cumulative"]["shares"]
        order = [t for t in TERM_NAME if t in sh]
        _stack(b, i, [(t, sh[t]) for t in order], 0.6, horizontal=True)
        left = 0.0
        for t in order:
            if sh[t] >= 0.06:
                b.text(
                    left + sh[t] / 2, i, f"{sh[t]:.2f}", ha="center", va="center", fontsize=7, color="white"
                )
            left += max(sh[t], 0)
    b.set_yticks(range(len(rows)), [r[1] for r in rows])
    b.set_xlim(0, 1)
    b.xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    b.grid(axis="x", color=GRID, linewidth=0.6)
    b.grid(axis="y", visible=False)
    b.set_xlabel("share of the cumulative headline Δlog2")
    handles_b = [mpl.patches.Patch(color=TERM_COLOUR["transistors_mtr"], label="transistors (A′)")]
    b.legend(handles=handles_b, loc="lower right", bbox_to_anchor=(1, 1.0))
    panel(b, "b", "cumulative shares over the whole chain")
    save(fig, out, "f2_chain")


# -------------------------------------------------------------------------------------- F3 regression


def f3_regression(numbers: dict[str, Any], out: Path) -> None:
    """(a) Estimator (b): doublings per year per term, three identities; (b) the H3b contrast, §6 variants."""
    setup()
    samples = [
        ("estimator_b", "identity A", "#0072B2"),
        ("estimator_b_clock_free", "clock-free identity", "#009E73"),
        ("estimator_b_a_prime", "identity A′ (no area)", "#D55E00"),
    ]
    rows = ["headline", *TERM_NAME]
    row_name = {"headline": "headline rate", **TERM_NAME}
    fig, (a, b) = plt.subplots(
        2, 1, figsize=(WIDTH, 6.4), gridspec_kw={"height_ratios": [1.0, 1.45], "hspace": 0.32}
    )
    for k, (key, name, colour) in enumerate(samples):
        fits = numbers[key]["fits"]
        for i, r in enumerate(rows):
            if r not in fits:
                continue
            f = fits[r]
            y = i + (k - 1) * 0.24
            a.errorbar(
                f["slope"],
                y,
                xerr=[[f["slope"] - f["slope_ci"][0]], [f["slope_ci"][1] - f["slope"]]],
                fmt="o",
                ms=3.6,
                color=colour,
                ecolor=colour,
                elinewidth=0.9,
                capsize=0,
                mec="white",
                mew=0.5,
            )
        a.errorbar([], [], fmt="o", ms=3.6, color=colour, label=f"{name}, n = {numbers[key]['n']}")
    a.axvline(0, color="#3a3a3a", linewidth=0.6)
    a.set_yticks(range(len(rows)), [row_name[r] for r in rows])
    a.invert_yaxis()
    a.grid(axis="y", visible=False)
    a.grid(axis="x", color=GRID, linewidth=0.6)
    a.set_xlabel("trend (doublings per year), 95% bootstrap interval")
    a.legend(loc="lower right")
    panel(a, "a", "estimator (b), flagships")

    sens = [r for r in numbers["sensitivity"] if r.get("h3b")]
    for i, r in enumerate(sens):
        est, (lo, hi) = r["h3b"]["estimate"], r["h3b"]["ci"]
        colour = "#D55E00" if lo > 0 else ("#0072B2" if r["label"] == "primary" else MUTED)
        b.plot([lo, hi], [i, i], color=colour, linewidth=1.0)
        b.scatter(est, i, s=16, color=colour, edgecolors="white", linewidths=0.5, zorder=3)
    b.axvline(0, color="#3a3a3a", linewidth=0.6)
    b.set_yticks(range(len(sens)), [f"{r['label']} (n = {r['n']})" for r in sens])
    b.invert_yaxis()
    b.grid(axis="y", visible=False)
    b.grid(axis="x", color=GRID, linewidth=0.6)
    b.set_xlabel("specialization + precision − density (doublings per year), 95% bootstrap interval")
    panel(b, "b", "H3b contrast across the sensitivity analyses; orange: interval above zero")
    save(fig, out, "f3_regression")


# -------------------------------------------------------------------------------------- F4 efficiency


def f4_efficiency(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """Headline rate per watt, per mm² of compute die and per billion transistors, flagships."""
    setup()
    eff = numbers["rq3_efficiency"]
    spec = [
        ("tflops_per_w", "TFLOP/s per W (TDP)", "#D55E00"),
        ("tflops_per_mm2", "TFLOP/s per mm² of compute die", "#56B4E9"),
        ("tflops_per_btransistor", "TFLOP/s per billion transistors", "#009E73"),
    ]
    flag = run.flagships(d)
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH, 2.5), gridspec_kw={"wspace": 0.42})
    for ax, letter, (col, name, colour) in zip(axes, "abc", spec, strict=True):
        sub = flag.dropna(subset=["year", col])
        ax.scatter(sub["year"], sub[col], color=colour, **DOT)
        fit = eff[col]
        _line(ax, fit["fit"], sub["year"], colour)
        _log_axis(ax)
        _year_axis(ax, 2012, 2026)
        ax.set_xticks([2012, 2016, 2020, 2024])
        ax.set_ylabel(name)
        ax.set_xlabel("announce year")
        lo, hi = fit["fit"]["doubling_ci"]
        ax.text(
            0.03,
            0.97,
            f"n = {fit['n']}\ndoubling {fit['fit']['doubling_years']:.2f} yr\n[{lo:.2f}, {hi:.2f}]",
            transform=ax.transAxes,
            va="top",
            fontsize=7.5,
        )
        panel(ax, letter)
    save(fig, out, "f4_efficiency")


# ------------------------------------------------------------------------------------------ F5 memory


def f5_memory(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """(a) Headline rate against memory bandwidth, with lines of constant ops per byte; (b) ops/byte."""
    setup()
    mem = numbers["rq4_memory"]
    flag = run.flagships(d).dropna(subset=["year", "headline_tflops", "mem_bandwidth_gbs"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(WIDTH, 3.0), gridspec_kw={"wspace": 0.62})
    sc = a.scatter(
        flag["mem_bandwidth_gbs"] / 1e3,
        flag["headline_tflops"],
        c=flag["year"],
        cmap="cividis",
        s=16,
        edgecolors="white",
        linewidths=0.4,
        zorder=3,
    )
    xs = np.array([0.1, 50.0])
    for opb in (10, 100, 1000):  # ops per byte = (TFLOP/s) / (TB/s)
        a.plot(xs, xs * opb, color="#c8c8c8", linewidth=0.8, linestyle=DASH, zorder=1)
        x_end = min(40.0, 5e4 / opb)
        a.text(x_end, x_end * opb, f"{opb:,} ops/byte ", fontsize=6.5, color=MUTED, ha="right", va="bottom")
    _log_axis(a)
    _log_axis(a, "x")
    a.set_xlim(0.15, 40)
    a.set_ylim(1, 5e4)
    a.set_xlabel("memory bandwidth (TB/s)")
    a.set_ylabel("headline dense rate (TFLOP/s or TOPS)")
    a.grid(axis="x", color=GRID, linewidth=0.6)
    cb = fig.colorbar(sc, ax=a, fraction=0.05, pad=0.02)
    cb.set_ticks([2014, 2018, 2022, 2026])
    cb.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%d"))
    cb.set_label("announce year", fontsize=7.5)
    cb.ax.tick_params(labelsize=7)
    cb.outline.set_linewidth(0.4)
    panel(a, "a", f"flagships, n = {len(flag)}")

    col = "ops_per_byte"
    sub = run.flagships(d).dropna(subset=["year", col])
    b.scatter(sub["year"], sub[col], color="#CC79A7", **DOT)
    fit = mem[col]
    _line(b, fit["fit"], sub["year"], "#CC79A7")
    _log_axis(b)
    b.set_xlim(2013.3, 2027.0)
    b.set_xticks([2014, 2018, 2022, 2026])
    b.set_xlabel("announce year")
    b.set_ylabel("headline operations per byte of bandwidth")
    lines = [
        f"ops/byte: {_doubling(fit['fit'])}",
        f"headline: {_doubling(mem['headline']['fit'])}",
        f"bandwidth: {_doubling(mem['mem_bandwidth_gbs']['fit'])}",
    ]
    b.set_ylim(15, 3e4)
    b.text(0.03, 0.97, "\n".join(lines), transform=b.transAxes, va="top", fontsize=7)
    panel(b, "b", f"flagships, n = {fit['n']}")
    save(fig, out, "f5_memory")


# ------------------------------------------------------------------------------------------ F6 MLPerf


BENCH_NAME = {
    ("resnet", "training"): "ResNet-50 training",
    ("bert", "training"): "BERT training",
    ("llama2_70b_lora", "training"): "Llama 2 70B LoRA fine-tuning",
    ("llama2-70b-99.9", "inference"): "Llama 2 70B inference, offline",
}


def f6_mlperf(d: pd.DataFrame, numbers: dict[str, Any], mlperf: pd.DataFrame, out: Path) -> None:
    """Per-accelerator MLPerf throughput (first result per product) against the headline rate, both
    relative to the earliest product of each benchmark."""
    setup()
    h6 = numbers["hypotheses"]["H6"]
    flag = run.flagships(d).set_index("product")
    ml = mlperf.fillna({"scenario": "", "excluded": ""})
    ml = ml[ml["excluded"].astype(str).eq("") & ml["rule"].eq(h6["rule"])]
    benches = sorted(h6["benchmarks"], key=lambda b: (b["suite"] != "training", b["benchmark"]))
    fig, grid = plt.subplots(1, len(benches), figsize=(WIDTH, 2.6), sharey=True, gridspec_kw={"wspace": 0.12})
    axes = np.atleast_1d(grid)
    for ax, letter, bm in zip(axes, "abcd", benches, strict=False):
        g = ml[
            ml["benchmark"].eq(bm["benchmark"])
            & ml["suite"].eq(bm["suite"])
            & ml["scenario"].eq(bm["scenario"])
            & ml["product"].isin(bm["products"])
        ].drop_duplicates("product")
        g = g.assign(year=[flag.loc[p, "year"] for p in g["product"]]).sort_values("year")
        real = np.log2(g["per_accelerator"].astype(float).to_numpy())
        head = np.array([flag.loc[p, "log2_headline"] for p in g["product"]], dtype=float)
        x = g["year"].to_numpy(dtype=float)
        ax.plot(x, head - head[0], color="#D55E00", linewidth=1.1, marker="o", ms=3.6, mec="white", mew=0.5)
        ax.plot(x, real - real[0], color="#0072B2", linewidth=1.1, marker="o", ms=3.6, mec="white", mew=0.5)
        for xi, yi, p in zip(x, real - real[0], g["product"], strict=True):
            ax.annotate(
                p.split()[0],
                (xi, yi),
                xytext=(3, -9),
                textcoords="offset points",
                fontsize=6.5,
                ha="left",
                color=MUTED,
            )
        ax.set_xlim(x.min() - 0.6, x.max() + 0.6)
        ax.set_ylim(-0.6, 5.2)
        ax.set_xticks(sorted({round(v) for v in x}))
        ax.tick_params(axis="x", labelsize=7)
        name = BENCH_NAME.get((bm["benchmark"], bm["suite"]), bm["benchmark"])
        ax.text(
            0.03,
            0.97,
            f"{name}\nheadline {bm['slope_headline']:.2f}, MLPerf {bm['slope_realized']:.2f}\ndoublings/yr",
            transform=ax.transAxes,
            va="top",
            fontsize=6.5,
        )
        panel(ax, letter)
    axes[0].set_ylabel("doublings since the first product")
    axes[0].plot([], [], color="#D55E00", marker="o", ms=3.6, label="headline peak rate")
    axes[0].plot([], [], color="#0072B2", marker="o", ms=3.6, label="MLPerf per accelerator")
    fig.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.1))
    fig.supxlabel("announce year", fontsize=8.5, y=-0.04)
    save(fig, out, "f6_mlperf")


# ------------------------------------------------------------------------------------------- F7 Dally


NVIDIA_COLOUR = {
    "process": "#0072B2",
    "complex_instructions": "#009E73",
    "number_representation": "#D55E00",
    "sparsity": "#F3C3A1",
}
NVIDIA_NAME = {
    "process": "process",
    "complex_instructions": "complex instructions",
    "number_representation": "number representation",
    "sparsity": "sparsity",
}


def f7_dally(numbers: dict[str, Any], out: Path) -> None:
    """NVIDIA's factors for K20X → H100 against identity A's, as segments of log2 of the gain."""
    setup()
    c, c32 = numbers["estimator_c"], numbers["estimator_c_fp32_reference"]
    nv = c["nvidia"]
    bars: list[tuple[str, list[tuple[str, float, str, str]]]] = [
        (
            "NVIDIA's account\n(Dally, Hot Chips 2023)",
            [(NVIDIA_NAME[k], nv[k], NVIDIA_COLOUR[k], "") for k in NVIDIA_COLOUR],
        ),
        (
            "identity A,\nFP16/BF16 reference",
            [(TERM_NAME[t], v, TERM_COLOUR[t], "") for t, v in c["factors"].items()],
        ),
        (
            "identity A,\nFP32 reference",
            [(TERM_NAME[t], v, TERM_COLOUR[t], "") for t, v in c32["factors"].items()],
        ),
    ]
    fig, ax = plt.subplots(figsize=(WIDTH, 2.7))
    for i, (_, parts) in enumerate(bars):
        pos = neg = 0.0
        for name, ratio, colour, _ in parts:
            v = float(np.log2(ratio))
            left = pos if v >= 0 else neg + v
            hatch = "////" if name == "sparsity" else None
            ax.barh(i, abs(v), 0.58, left=left, color=colour, linewidth=0, hatch=hatch, edgecolor="white")
            ink = INK if name in ("sparsity", "die area") else "white"
            if v < 0:  # a factor below one: labelled outside, left of the bar
                ax.text(left - 0.08, i, f"{name}\n{ratio:.3g}×", ha="right", va="center", fontsize=6.5)
            elif v >= 0.7:
                ax.text(
                    left + v / 2,
                    i,
                    f"{name}\n{ratio:.3g}×",
                    ha="center",
                    va="center",
                    fontsize=6.5,
                    color=ink,
                )
            elif v >= 0.4:
                ax.text(left + v / 2, i, f"{ratio:.3g}×", ha="center", va="center", fontsize=6, color=ink)
            if v >= 0:
                pos += v
            else:
                neg += v
    ax.axvline(0, color="#3a3a3a", linewidth=0.6)
    dense = float(np.log2(nv["total_dense"]))
    ax.axvline(dense, color=MUTED, linewidth=0.7, linestyle=DASH)
    ax.text(
        dense, -0.42, f"{nv['total_dense']:.0f}× dense ", fontsize=7, color=MUTED, ha="right", va="center"
    )
    ax.set_yticks(range(len(bars)), [b[0] for b in bars])
    ax.set_ylim(2.45, -0.6)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    top = int(np.ceil(np.log2(nv["total"])))
    ax.set_xlim(-3.0, top + 0.3)
    ax.set_xticks(range(-2, top + 1))
    ax.set_xlabel("log2 of the K20X → H100 gain (doublings); labels give each factor as a ratio")
    handles = [mpl.patches.Patch(color=TERM_COLOUR["area_mm2"], label="die area")]
    ax.legend(handles=handles, loc="upper left", fontsize=7)
    save(fig, out, "f7_dally")


# ----------------------------------------------------------------------------------------------- all


def draw_all(raw: pd.DataFrame, numbers: dict[str, Any], mlperf: pd.DataFrame | None, out: Path) -> list[str]:
    d = run.prepare(raw)
    f1_ladder(d, numbers, out)
    f2_chain(numbers, out)
    f3_regression(numbers, out)
    f4_efficiency(d, numbers, out)
    f5_memory(d, numbers, out)
    drawn = NAMES[:5]
    if mlperf is not None and numbers["hypotheses"]["H6"]["benchmarks"]:
        f6_mlperf(d, numbers, mlperf, out)
        drawn.append("f6_mlperf")
    f7_dally(numbers, out)
    return [*drawn, "f7_dally"]
