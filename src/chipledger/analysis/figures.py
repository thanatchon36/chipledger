"""Paper figures F1–F7, in the house style shared with the author's other papers.

Libertinus Serif (vendored in ``figures/fonts``); every figure is exactly the paper's text width, so 8 pt text
prints at 8 pt; panel letters "(a)", "(b)" and no in-figure titles; a hairline solid grid; recessive axes; one
fixed colour per identity term (Okabe–Ito) in every figure; white gaps between touching segments; legends
above or inside the axes plus a few direct labels. Every figure is written as SVG with text as paths (PDF
build) and as a 300-dpi PNG (web reader, README).

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
INK, MUTED, GRID, AXIS = "#1a1a1a", "#555555", "#e4e4e4", "#6b6b6b"
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
    "area_mm2": "#56B4E9",  # the same slot as the die-area term in the decomposition figures
    "mem_bandwidth_gbs": "#0072B2",
    "ops_per_byte": "#CC79A7",
}
PERIODS = [(2012, 2015), (2016, 2019), (2020, 2023), (2024, 2026)]
PERIOD_COLOUR = ["#9cc9e1", "#519ccc", "#1b69af", "#083573"]  # one hue, light to dark, for ordered periods
WIDTH = 16.6 / 2.54  # the paper's text block: A4 with 2.2 cm side margins
LINE = 1.0
DOT: dict[str, Any] = {"s": 14, "edgecolors": "white", "linewidths": 0.6, "zorder": 3}
HOLLOW: dict[str, Any] = {"s": 14, "facecolors": "white", "linewidths": 0.9, "zorder": 3}
GAP: dict[str, Any] = {"edgecolor": "white", "linewidth": 0.8}  # the surface gap between touching segments
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
            "font.size": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "legend.fontsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.5,
            "axes.edgecolor": AXIS,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": GRID,
            "grid.linewidth": 0.4,
            "grid.linestyle": "-",
            "axes.axisbelow": True,
            "xtick.major.size": 2,
            "ytick.major.size": 2,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.color": AXIS,
            "ytick.color": AXIS,
            "xtick.labelcolor": INK,
            "ytick.labelcolor": INK,
            "text.color": INK,
            "axes.labelcolor": INK,
            "legend.frameon": False,
            "legend.handlelength": 1.4,
            "legend.handletextpad": 0.5,
            "legend.columnspacing": 1.2,
            "legend.labelspacing": 0.35,
            "legend.borderaxespad": 0.0,
            "legend.borderpad": 0.2,
            "savefig.facecolor": "white",
        }
    )


def figure(height_cm: float, wspace: float = 0.06, hspace: float = 0.08) -> Figure:
    """A figure of the text width, laid out so that nothing outside the axes is clipped."""
    fig = plt.figure(figsize=(WIDTH, height_cm / 2.54), layout="constrained")
    engine = fig.get_layout_engine()
    assert engine is not None
    engine.set(w_pad=0.02, h_pad=0.02, wspace=wspace, hspace=hspace)  # type: ignore[call-arg]
    return fig


def save(fig: Figure, out: Path, name: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", metadata={"Date": None})
    fig.savefig(out / f"{name}.png", dpi=300)
    plt.close(fig)


def panel(ax: Axes, letter: str, text: str | None = None) -> None:
    """Bold panel letter above the top-left corner, with an optional plain descriptor after it."""
    ax.annotate(
        letter,
        (0, 1),
        xycoords="axes fraction",
        xytext=(0, 4),
        textcoords="offset points",
        ha="left",
        va="bottom",
        fontsize=9,
        weight="bold",
    )
    if text:
        ax.annotate(
            text,
            (0, 1),
            xycoords="axes fraction",
            xytext=(15, 4),
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=8,
        )


def short(product: str) -> str:
    return product.split()[0]


def _log_axis(ax: Axes, axis: str = "y") -> None:
    """Log-10 axis with plain-number tick labels (0.1, 1, 10, 1,000)."""
    (ax.set_yscale if axis == "y" else ax.set_xscale)("log")
    fmt = mpl.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def _doubling(fit: dict[str, Any]) -> str:
    lo, hi = fit["doubling_ci"]
    return f"{fit['doubling_years']:.2f} yr [{lo:.2f}, {hi:.2f}]"


def _line(ax: Axes, fit: dict[str, Any], years: pd.Series, colour: str, **kw: Any) -> None:
    """A fitted log2-linear trend drawn in value space over the years of its sample."""
    xs = np.linspace(float(years.min()), float(years.max()), 2)
    ax.plot(xs, 2 ** (fit["intercept"] + fit["slope"] * xs), color=colour, linewidth=LINE, zorder=2, **kw)


def _points(ax: Axes, sub: pd.DataFrame, col: str, colour: str) -> None:
    """Flagship values against year; wafer-scale parts hollow (they are in every fit)."""
    wafer = sub["wafer_scale"].astype(bool)
    ax.scatter(sub.loc[~wafer, "year"], sub.loc[~wafer, col], color=colour, **DOT)
    ax.scatter(sub.loc[wafer, "year"], sub.loc[wafer, col], edgecolors=colour, **HOLLOW)


def _trend(ax: Axes, flag: pd.DataFrame, col: str, colour: str, fit: dict[str, Any]) -> pd.DataFrame:
    sub = flag.dropna(subset=["year", col])
    _points(ax, sub, col, colour)
    _line(ax, fit["fit"], sub["year"], colour)
    return sub


def _stat(ax: Axes, fit: dict[str, Any], corner: str = "upper left") -> None:
    """n and the doubling time with its interval, in an empty corner of a rising trend."""
    text = f"n = {fit['n']}\ndoubling {_doubling(fit['fit'])}".replace(" yr [", " yr\n[")  # three short lines
    if corner == "upper left":
        ax.text(0.03, 0.96, text, transform=ax.transAxes, va="top", ha="left", fontsize=7, linespacing=1.3)
    else:
        ax.text(
            0.97, 0.04, text, transform=ax.transAxes, va="bottom", ha="right", fontsize=7, linespacing=1.3
        )


def _handle(colour: str, label: str, hollow: bool = False, line: bool = True) -> Any:
    return mpl.lines.Line2D(
        [],
        [],
        color=colour,
        marker="o",
        markersize=3.8,
        markerfacecolor="white" if hollow else colour,
        markeredgecolor=colour if hollow else "white",
        markeredgewidth=0.9 if hollow else 0.6,
        linewidth=LINE if line else 0,
        label=label,
    )


def _year_ticks(ax: Axes, lo: int, hi: int, step: int) -> None:
    ax.set_xlim(lo - 0.7, hi + 0.7)
    ax.set_xticks(range(lo, hi + 1, step))


def _dark(colour: str) -> bool:
    """Whether white text is the readable choice on a fill (relative luminance below 0.3)."""
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in mpl.colors.to_rgb(colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.3


# ------------------------------------------------------------------------------------------ F1 ladder


def f1_ladder(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """(a) Headline, reference and FP32 rates of the flagships; (b)–(d) transistors, density, die area."""
    setup()
    rq1 = numbers["rq1_throughput"]
    fits = {**rq1["flagships"], **rq1["flagships_density"], **rq1["flagships_ladder"]}
    flag = run.flagships(d)
    fig = figure(12.0, wspace=0.08, hspace=0.12)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.45, 1.0])

    a = fig.add_subplot(gs[0, :])
    handles = []
    for key, col, name in [
        ("headline", "headline_tflops", "headline dense rate"),
        ("ref_tflops", "ref_tflops", "16-bit reference rate"),
        ("fp32", "fp32", "vector FP32 rate"),
    ]:
        fit = fits[key]
        _trend(a, flag, col, SERIES_COLOUR[key], fit)
        handles.append(
            _handle(SERIES_COLOUR[key], f"{name}: n = {fit['n']}, doubling {_doubling(fit['fit'])}")
        )
    handles.append(_handle(MUTED, "wafer-scale part (hollow; in every fit)", hollow=True, line=False))
    _log_axis(a)
    _year_ticks(a, 2014, 2026, 2)
    a.set_ylabel("peak rate (TFLOP/s; TOPS for integer formats)")
    a.set_xlabel("announce year")
    a.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    panel(a, "(a)")

    silicon = [  # the stat block goes in whichever corner the wafer-scale outliers leave empty
        ("transistors_b", "transistors per package (10⁹)", "upper left"),
        ("density_mtr_mm2", "transistor density (10⁶ per mm²)", "lower right"),
        ("area_mm2", "compute die area (mm²)", "upper left"),
    ]
    for i, (letter, (key, name, corner)) in enumerate(zip("bcd", silicon, strict=True)):
        ax = fig.add_subplot(gs[1, i])
        _trend(ax, flag, key, SERIES_COLOUR[key], fits[key])
        _stat(ax, fits[key], corner=corner)
        _log_axis(ax)
        if key == "density_mtr_mm2":  # under one decade: name the ticks, no 6 × 10¹ labels
            ax.set_yticks([10, 20, 50, 100, 200])
            ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        _year_ticks(ax, 2014, 2026, 4)
        ax.set_ylabel(name)
        ax.set_xlabel("announce year")
        panel(ax, f"({letter})")
    save(fig, out, "f1_ladder")


# ------------------------------------------------------------------------------------------- F2 chain


def _stack(ax: Axes, x: float, parts: list[tuple[str, float]], width: float, horizontal: bool) -> float:
    """Stacked segments, positive ones upward from zero and negative ones downward; returns the top."""
    pos = neg = 0.0
    for term, v in parts:
        base = pos if v >= 0 else neg
        kw: dict[str, Any] = {"color": TERM_COLOUR[term], **GAP}
        if horizontal:
            ax.barh(x, v, width, left=base, **kw)
        else:
            ax.bar(x, v, width, bottom=base, **kw)
        if v >= 0:
            pos += v
        else:
            neg += v
    return pos


def f2_chain(numbers: dict[str, Any], out: Path) -> None:
    """(a) Δlog2 per term for each step of the NVIDIA chain; (b) cumulative shares, NVIDIA and AMD."""
    setup()
    nv = numbers["estimator_a"]["nvidia_a"]
    amd = numbers["estimator_a"]["amd_a_prime"]
    terms = [t for t in TERM_NAME if f"dlog2_{t}" in nv["steps"][0]]
    fig = figure(11.5, hspace=0.14)
    gs = fig.add_gridspec(2, 1, height_ratios=[2.1, 1.0])
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    for i, s in enumerate(nv["steps"]):
        _stack(a, i, [(t, s[f"dlog2_{t}"]) for t in terms], 0.6, horizontal=False)
        net = s["dlog2_headline"]
        a.scatter(i, net, s=20, color=INK, edgecolors="white", linewidths=0.6, zorder=4)
        a.text(i + 0.36, net, f"{net:.2f}", ha="left", va="center", fontsize=7.5)
    labels = [
        f"{short(s['from'])} → {short(s['to'])}\n{s['year_to'] - s['year_from']:.1f} yr" for s in nv["steps"]
    ]
    a.axhline(0, color=AXIS, linewidth=0.5, zorder=1)
    a.set_xticks(range(len(labels)), labels)
    a.set_xlim(-0.6, len(labels) - 0.2)
    a.set_ylabel("change per step (doublings, Δlog2)")
    handles: list[Any] = [mpl.patches.Patch(color=TERM_COLOUR[t], label=TERM_NAME[t]) for t in terms]
    handles.append(mpl.patches.Patch(color=TERM_COLOUR["transistors_mtr"], label="transistors (identity A′)"))
    handles.append(_handle(INK, "net change of the headline rate", line=False))
    fig.legend(handles=handles, loc="outside upper right", ncol=4)
    panel(a, "(a)")

    def span(c: dict[str, Any]) -> str:
        members = c["cumulative"]["members"]
        return f"{short(members[0])} → {short(members[-1])}"

    rows = [(nv, f"NVIDIA\n{span(nv)}\nidentity A"), (amd, f"AMD\n{span(amd)}\nidentity A′")]
    for i, (c, _) in enumerate(rows):
        sh = c["cumulative"]["shares"]
        order = [t for t in TERM_NAME if t in sh]
        _stack(b, i, [(t, sh[t]) for t in order], 0.62, horizontal=True)
        left = 0.0
        for t in order:
            if sh[t] >= 0.05:
                colour = "white" if _dark(TERM_COLOUR[t]) else INK
                b.text(
                    left + sh[t] / 2, i, f"{sh[t]:.0%}", ha="center", va="center", fontsize=7.5, color=colour
                )
            left += max(sh[t], 0)
    b.set_yticks(range(len(rows)), [r[1] for r in rows])
    b.set_ylim(len(rows) - 0.5, -0.5)
    b.set_xlim(0, 1)
    b.xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    b.grid(axis="x")
    b.grid(axis="y", visible=False)
    b.tick_params(axis="y", length=0)
    b.set_xlabel("share of the cumulative change in the headline rate")
    panel(b, "(b)")
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
    fig = figure(15.0, hspace=0.12)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.55])
    a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    handles = []
    for k, (key, name, colour) in enumerate(samples):
        fits = numbers[key]["fits"]
        for i, r in enumerate(rows):
            if r not in fits:
                continue
            f = fits[r]
            y = i + (k - 1) * 0.26
            a.plot(f["slope_ci"], [y, y], color=colour, linewidth=LINE, solid_capstyle="butt", zorder=2)
            a.scatter(f["slope"], y, s=16, color=colour, edgecolors="white", linewidths=0.6, zorder=3)
        handles.append(_handle(colour, f"{name}, n = {numbers[key]['n']}"))
    a.axvline(0, color=AXIS, linewidth=0.5, zorder=1)
    a.set_yticks(range(len(rows)), [row_name[r] for r in rows])
    a.set_ylim(len(rows) - 0.5, -0.6)
    a.grid(axis="y", visible=False)
    a.grid(axis="x")
    a.tick_params(axis="y", length=0)
    a.set_xlabel("trend (doublings per year) with its 95% bootstrap interval")
    a.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=3)
    panel(a, "(a)")

    sens = [r for r in numbers["sensitivity"] if r.get("h3b")]
    kinds = {"primary": "#0072B2", "excludes": "#D55E00", "other": "#8a8a8a"}
    for i, r in enumerate(sens):
        est, (lo, hi) = r["h3b"]["estimate"], r["h3b"]["ci"]
        kind = "primary" if r["label"] == "primary" else ("excludes" if lo > 0 else "other")
        b.plot([lo, hi], [i, i], color=kinds[kind], linewidth=LINE, solid_capstyle="butt", zorder=2)
        b.scatter(est, i, s=16, color=kinds[kind], edgecolors="white", linewidths=0.6, zorder=3)
    b.axvline(0, color=AXIS, linewidth=0.5, zorder=1)
    b.set_yticks(range(len(sens)), [f"{r['label']} (n = {r['n']})" for r in sens])
    b.set_ylim(len(sens) - 0.5, -0.6)
    b.grid(axis="y", visible=False)
    b.grid(axis="x")
    b.tick_params(axis="y", length=0)
    b.set_xlabel("specialization + precision − density (doublings per year) with its 95% bootstrap interval")
    b.legend(
        handles=[
            _handle(kinds["primary"], "primary analysis"),
            _handle(kinds["excludes"], "interval excludes zero"),
            _handle(kinds["other"], "other variants"),
        ],
        loc="lower right",
        bbox_to_anchor=(1.0, 1.0),
        ncol=3,
    )
    panel(b, "(b)")
    save(fig, out, "f3_regression")


# -------------------------------------------------------------------------------------- F4 efficiency


def f4_efficiency(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """Headline rate per watt, per mm² of compute die and per billion transistors, flagships."""
    setup()
    eff = numbers["rq3_efficiency"]
    spec = [
        ("tflops_per_w", "headline rate per watt of TDP (TFLOP/s per W)"),
        ("tflops_per_mm2", "headline rate per mm² of compute die"),
        ("tflops_per_btransistor", "headline rate per 10⁹ transistors"),
    ]
    flag = run.flagships(d)
    fig = figure(6.0, wspace=0.1)
    axes = fig.subplots(1, 3)
    for ax, letter, (col, name) in zip(axes, "abc", spec, strict=True):
        # one series per panel, so every panel takes the headline colour and the axis label names it
        _trend(ax, flag, col, SERIES_COLOUR["headline"], eff[col])
        _stat(ax, eff[col])
        _log_axis(ax)
        _year_ticks(ax, 2014, 2026, 4)
        ax.set_ylabel(name)
        ax.set_xlabel("announce year")
        panel(ax, f"({letter})")
    save(fig, out, "f4_efficiency")


# ------------------------------------------------------------------------------------------ F5 memory


def f5_memory(d: pd.DataFrame, numbers: dict[str, Any], out: Path) -> None:
    """(a) Headline rate against memory bandwidth, with lines of constant ops per byte; (b) ops/byte."""
    setup()
    mem = numbers["rq4_memory"]
    flag = run.flagships(d).dropna(subset=["year", "headline_tflops", "mem_bandwidth_gbs"])
    fig = figure(7.4, wspace=0.1)
    a, b = fig.subplots(1, 2, width_ratios=[1.15, 1.0])

    xs = np.array([0.1, 60.0])
    for opb in (10, 100, 1000):  # ops per byte = (TFLOP/s) / (TB/s)
        a.plot(xs, xs * opb, color="#cfcfcf", linewidth=0.5, zorder=1)
        x_end = min(45.0, 6e4 / opb)
        a.text(x_end, x_end * opb, f"{opb:,} ops/byte ", fontsize=6.5, color=MUTED, ha="right", va="bottom")
    handles = []
    for (lo, hi), colour in zip(PERIODS, PERIOD_COLOUR, strict=True):
        sub = flag[(flag["year"] >= lo) & (flag["year"] < hi + 1)]
        a.scatter(sub["mem_bandwidth_gbs"] / 1e3, sub["headline_tflops"], color=colour, **DOT)
        handles.append(_handle(colour, f"{lo}–{hi}", line=False))
    for idx in (flag["year"].idxmin(), flag["headline_tflops"].idxmax()):
        r = flag.loc[idx]  # type: ignore[call-overload]
        a.annotate(
            short(str(r["product"])),
            (r["mem_bandwidth_gbs"] / 1e3, r["headline_tflops"]),
            xytext=(5, -2),
            textcoords="offset points",
            fontsize=6.5,
            color=MUTED,
            ha="left",
            va="top",
        )
    _log_axis(a)
    _log_axis(a, "x")
    a.set_xlim(0.15, 45)
    a.set_ylim(1, 6e4)
    a.set_xlabel("memory bandwidth (TB/s)")
    a.set_ylabel("headline dense rate (TFLOP/s or TOPS)")
    a.grid(axis="x")
    a.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 0.0), ncol=1, title="announced")
    panel(a, "(a)")

    col = "ops_per_byte"
    sub = run.flagships(d).dropna(subset=["year", col])
    _points(b, sub, col, SERIES_COLOUR[col])
    fit = mem[col]
    _line(b, fit["fit"], sub["year"], SERIES_COLOUR[col])
    _log_axis(b)
    _year_ticks(b, 2014, 2026, 4)
    b.set_ylim(15, 4e4)
    b.set_xlabel("announce year")
    b.set_ylabel("headline operations per byte of bandwidth")
    lines = [
        f"n = {fit['n']}",
        f"ops/byte: doubling {_doubling(fit['fit'])}",
        f"headline: doubling {_doubling(mem['headline']['fit'])}",
        f"bandwidth: doubling {_doubling(mem['mem_bandwidth_gbs']['fit'])}",
    ]
    b.text(0.03, 0.96, "\n".join(lines), transform=b.transAxes, va="top", fontsize=7, linespacing=1.3)
    panel(b, "(b)")
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
    fig = figure(6.8, wspace=0.04)
    axes = np.atleast_1d(fig.subplots(1, len(benches), sharey=True))
    head_c, real_c = "#D55E00", "#0072B2"
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
        for y, colour in ((head - head[0], head_c), (real - real[0], real_c)):
            ax.plot(x, y, color=colour, linewidth=LINE, zorder=2)
            ax.scatter(x, y, color=colour, **DOT)
        ax.set_xlim(x.min() - 0.7, x.max() + 0.7)
        ax.set_ylim(-0.4, 5.0)
        ax.set_xticks(x, [f"{short(p)}\n{yr:.0f}" for p, yr in zip(g["product"], x, strict=True)])
        ax.text(
            0.04,
            0.96,
            f"slope, doublings/yr\nheadline {bm['slope_headline']:.2f} · MLPerf {bm['slope_realized']:.2f}",
            transform=ax.transAxes,
            va="top",
            fontsize=6.8,
            linespacing=1.3,
        )
        panel(ax, f"({letter})", BENCH_NAME.get((bm["benchmark"], bm["suite"]), bm["benchmark"]))
    axes[0].set_ylabel("doublings since the first product")
    fig.legend(
        handles=[_handle(head_c, "headline dense rate"), _handle(real_c, "MLPerf, per accelerator")],
        loc="outside upper right",
        ncol=2,
    )
    fig.supxlabel("product and announce year", fontsize=8)
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
    bars: list[tuple[str, list[tuple[str, float, str]]]] = [
        (
            "NVIDIA's account\n(Dally, Hot Chips 2023)",
            [(NVIDIA_NAME[k], nv[k], NVIDIA_COLOUR[k]) for k in NVIDIA_COLOUR],
        ),
        (
            "identity A,\n16-bit reference",
            [(TERM_NAME[t], v, TERM_COLOUR[t]) for t, v in c["factors"].items()],
        ),
        (
            "identity A,\nFP32 reference",
            [(TERM_NAME[t], v, TERM_COLOUR[t]) for t, v in c32["factors"].items()],
        ),
    ]
    fig = figure(6.6)
    ax = fig.subplots()
    half = 0.3
    for i, (_, parts) in enumerate(bars):
        pos = neg = 0.0
        for name, ratio, colour in parts:
            v = float(np.log2(ratio))
            left = pos if v >= 0 else neg + v
            hatch = "////" if name == "sparsity" else None
            ax.barh(i, abs(v), 2 * half, left=left, color=colour, hatch=hatch, **GAP)
            ink = "white" if _dark(colour) else INK
            label = f"{name}\n{ratio:.3g}×"
            if v < 0:  # a factor below one: labelled outside, left of the bar
                ax.text(left - 0.1, i, label, ha="right", va="center", fontsize=6.8, linespacing=1.2)
            elif v >= 0.8:
                ax.text(
                    left + v / 2, i, label, ha="center", va="center", fontsize=6.8, color=ink, linespacing=1.2
                )
            else:  # too thin for a label inside: just above the segment
                ax.text(
                    left + v / 2,
                    i - half - 0.04,
                    f"{name} {ratio:.3g}×",
                    ha="center",
                    va="bottom",
                    fontsize=6.5,
                )
            if v >= 0:
                pos += v
            else:
                neg += v
    ax.axvline(0, color=AXIS, linewidth=0.5, zorder=1)
    dense = float(np.log2(nv["total_dense"]))
    ax.axvline(dense, color=MUTED, linewidth=0.6, linestyle=DASH, zorder=1)
    ax.text(
        dense,
        -0.5 - half,
        f"{nv['total_dense']:.0f}× dense ",
        fontsize=7,
        color=MUTED,
        ha="right",
        va="bottom",
    )
    ax.set_yticks(range(len(bars)), [b[0] for b in bars])
    ax.set_ylim(len(bars) - 0.5, -0.5 - half - 0.25)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x")
    ax.tick_params(axis="y", length=0)
    top = int(np.ceil(np.log2(nv["total"])))
    ax.set_xlim(-3.0, top + 0.3)
    ax.set_xticks(range(-2, top + 1))
    ax.set_xlabel("log2 of the K20X → H100 gain (doublings); each segment is labelled with its factor")
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
