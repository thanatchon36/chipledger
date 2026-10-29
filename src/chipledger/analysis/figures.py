"""Figures in the house style shared with the author's other papers: Libertinus Serif (vendored in
``figures/fonts``), Okabe–Ito colours, no in-figure titles, light horizontal grid, SVG with text as paths
and 300-dpi PNG. Phase 1 draws the rough versions of F1 (ladder) and F2 (chain contributions).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from chipledger.analysis.trend import Fit
from chipledger.identity import TERMS

ROOT = Path(__file__).resolve().parents[3]
FONT_DIR = ROOT / "figures" / "fonts"
INK, MUTED, GRID = "#1a1a1a", "#5a5a5a", "#e3e3e3"
TERM_COLOUR = {
    "density_mtr_mm2": "#0072B2",
    "area_mm2": "#56B4E9",
    "boost_clock_mhz": "#999999",
    "spec_ops_per_transistor_cycle": "#009E73",
    "precision_multiplier": "#D55E00",
}
TERM_NAME = {
    "density_mtr_mm2": "transistor density (Moore's law proper)",
    "area_mm2": "die area, incl. multi-die",
    "boost_clock_mhz": "clock",
    "spec_ops_per_transistor_cycle": "specialization (ops per transistor-cycle at FP16)",
    "precision_multiplier": "precision (headline / FP16)",
}
WIDTH = {"full": 16.0 / 2.54, "column": 7.8 / 2.54}


def setup() -> None:
    for p in sorted(FONT_DIR.glob("LibertinusSerif-*.otf")):
        font_manager.fontManager.addfont(str(p))
    plt.rcParams.update(
        {
            "svg.hashsalt": "chipledger",
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
            xytext=(14, 12),
            textcoords="offset points",
            ha="left",
            va="top",
            fontsize=8,
        )


def f2_chain(step_table: pd.DataFrame, out: Path) -> None:
    """Stacked Δlog2 contributions per chain step, and the cumulative bar."""
    setup()
    labels = [f"{a}\n→ {b}" for a, b in zip(step_table["from"], step_table["to"], strict=True)] + [
        "cumulative"
    ]
    fig, ax = plt.subplots(figsize=(WIDTH["full"], 2.9))
    x = np.arange(len(labels))
    pos = np.zeros(len(labels))
    neg = np.zeros(len(labels))
    for t in TERMS:
        v = np.append(step_table[f"dlog2_{t}"].to_numpy(dtype=float), step_table[f"dlog2_{t}"].sum())
        base = np.where(v >= 0, pos, neg)
        ax.bar(x, v, 0.62, bottom=base, color=TERM_COLOUR[t], label=TERM_NAME[t], linewidth=0)
        pos = pos + np.where(v >= 0, v, 0)
        neg = neg + np.where(v < 0, v, 0)
    total = np.append(step_table["dlog2_headline"].to_numpy(dtype=float), step_table["dlog2_headline"].sum())
    ax.scatter(x, total, s=14, color=INK, zorder=3, label="headline Δlog2 (= sum)")
    ax.axhline(0, color="#3a3a3a", linewidth=0.6)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Δlog2 (doublings)")
    ax.legend(loc="upper left", ncol=2, bbox_to_anchor=(0, 1.3))
    save(fig, out, "f2_chain")


def f1_ladder(derived: pd.DataFrame, fits: list[Fit], out: Path) -> None:
    """log2 of the headline rate, the reference rate, transistors per package and density against year."""
    setup()
    series = [
        ("log2_headline", "headline dense rate (TFLOP/s or TOPS)", "#D55E00"),
        ("log2_ref", "reference rate, FP16/BF16 (TFLOP/s)", "#009E73"),
        ("log2_transistors", "transistors per package (billions)", "#56B4E9"),
        ("log2_density_mtr_mm2", "transistor density (MTr/mm²)", "#0072B2"),
    ]
    d = derived.copy()
    d["log2_ref"] = np.log2(d["ref_tflops"])
    d["log2_transistors"] = np.log2(d["transistors_b"])
    by = {f.series: f for f in fits}
    fig, ax = plt.subplots(figsize=(WIDTH["full"], 3.4))
    for col, name, colour in series:
        sub = d[["year", col, "product"]].dropna()
        ax.scatter(sub["year"], sub[col], s=16, color=colour, zorder=3)
        label = name
        if col in by:
            f = by[col]
            xs = np.linspace(sub["year"].min(), sub["year"].max(), 2)
            ax.plot(xs, f.intercept + f.slope * xs, color=colour, linewidth=1.1)
            label += f" — doubling {f.doubling_years:.1f} y"
        else:
            b, a = np.polyfit(sub["year"], sub[col], 1)
            xs = np.linspace(sub["year"].min(), sub["year"].max(), 2)
            ax.plot(xs, a + b * xs, color=colour, linewidth=1.1, linestyle=(0, (3, 2)))
            label += f" — doubling {1 / b:.1f} y"
        ax.plot([], [], color=colour, marker="o", markersize=4, linewidth=1.1, label=label)
    for _, r in d.dropna(subset=["log2_headline"]).iterrows():
        ax.annotate(
            str(r["product"]),
            (r["year"], r["log2_headline"]),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=6,
            color=MUTED,
        )
    ax.set_xlabel("announce year")
    ax.set_ylabel("log2")
    ax.legend(loc="upper left")
    save(fig, out, "f1_ladder")
