"""Write announce/poster.png: a 1200×1500 (4:5) LinkedIn poster of the headline result.

Every number is read from results/numbers.json; the chart is the paper's reconciliation (Figure 4) in the
figure house style (Libertinus Serif, Okabe–Ito term colours). Nothing here is typed by hand except the names
of things, the study window's last year and Moore's 1975 forecast.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch

from chipledger.analysis import figures as fig

W, H, DPI = 1200, 1500, 150  # pixels; LinkedIn shows 4:5 at full height in the feed
M = 72  # margin, px
R = W - M  # right edge of the text column
TILE = "#f1f2f4"
WINDOW_END = 2026  # the last announce year of the study window, as in the paper's title
LINKS = (
    "github.com/thanatchon36/chipledger   ·   thanatchon36.github.io/chipledger/paper   ·   "
    "doi.org/10.5281/zenodo.23763729"
)


def _canvas() -> tuple[Figure, Axes]:
    """A figure with one pixel-addressed overlay axes: x right, y down, 1 unit = 1 px."""
    f = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = f.add_axes((0, 0, 1, 1), facecolor="none")
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_axis_off()
    return f, ax


def _t(ax: Axes, x: float, y: float, s: str, size: float, **kw: Any) -> Any:
    kw = {"color": fig.INK, "ha": "left", "va": "top", **kw}
    return ax.text(x, y, s, fontsize=size, **kw)


def _fit(f: Figure, ax: Axes, x: float, y: float, s: str, size: float, width: float, **kw: Any) -> Any:
    """One line of text, shrunk in half-point steps until it fits in `width` pixels."""
    r = f.canvas.get_renderer()  # type: ignore[attr-defined]
    while True:
        t = _t(ax, x, y, s, size, **kw)
        if t.get_window_extent(r).width <= width or size <= 8:
            return t
        t.remove()
        size -= 0.5


def _chain(
    f: Figure, ax: Axes, x: float, y: float, parts: list[tuple[str, float, str]], gap: float = 7
) -> None:
    """Pieces of one line in different sizes and weights, laid left to right on a shared baseline."""
    r = f.canvas.get_renderer()  # type: ignore[attr-defined]
    for s, size, weight in parts:
        t = _t(ax, x, y, s, size, weight=weight, va="baseline")
        x = t.get_window_extent(r).x1 + gap


def _tile(ax: Axes, x: float, y: float, w: float, h: float, accent: str | None = None) -> None:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=14", fc=TILE, ec="none"))
    if accent:
        ax.add_patch(
            FancyBboxPatch(
                (x + 28, y + 26), 44, 6, boxstyle="round,pad=0,rounding_size=3", fc=accent, ec="none"
            )
        )


Segment = tuple[str, float, str, str | None]  # name, factor, colour, share label


def _chart(
    f: Figure, c: dict[str, Any], shares: dict[str, float], box: tuple[float, float, float, float]
) -> None:
    """The two accountings of the K20X → H100 gain as stacked segments of log2, labelled with factors."""
    x0, y0, x1, y1 = box
    ax = f.add_axes((x0 / W, 1 - y1 / H, (x1 - x0) / W, (y1 - y0) / H))
    nv = c["nvidia"]
    ours: list[Segment] = [
        (fig.TERM_NAME[t], v, fig.TERM_COLOUR[t], f"{100 * shares[t]:.0f}%") for t, v in c["factors"].items()
    ]
    theirs: list[Segment] = [
        (fig.NVIDIA_NAME[k], nv[k], fig.NVIDIA_COLOUR[k], None) for k in fig.NVIDIA_COLOUR
    ]
    rows = [("This paper\n(identity A)", ours), ("NVIDIA's account\n(Hot Chips 2023)", theirs)]
    half = 0.4
    for i, (_, parts) in enumerate(rows):
        left = 0.0
        for name, ratio, colour, share in parts:
            v = math.log2(ratio)
            hatch = "////" if name == "sparsity" else None
            ax.barh(i, v, 2 * half, left=left, color=colour, hatch=hatch, **fig.GAP)
            ink = "white" if fig._dark(colour) else fig.INK
            factor = f"{ratio:.3g}×" + (f" · {share}" if share else "")
            if v >= 0.95:
                ax.text(
                    left + v / 2, i, f"{name}\n{factor}", ha="center", va="center", fontsize=10, color=ink
                )
            else:  # too thin for a label inside: above the segment
                ax.text(
                    left + v / 2, i - half - 0.06, f"{name} {factor}", ha="center", va="bottom", fontsize=9.5
                )
            left += v
    ax.axvline(0, color=fig.AXIS, linewidth=0.6, zorder=1)
    dense = math.log2(nv["total_dense"])
    ax.axvline(dense, color=fig.MUTED, linewidth=0.8, linestyle=fig.DASH, zorder=1)
    label = f"{nv['total_dense']:.0f}× dense"
    ax.text(dense - 0.08, -0.5 - half, label, fontsize=9.5, color=fig.MUTED, ha="right", va="bottom")
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=11, linespacing=1.3)
    ax.set_ylim(len(rows) - 0.5, -0.5 - half - 0.3)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=fig.GRID, linewidth=0.6)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=10)
    top = int(math.ceil(math.log2(nv["total"])))
    ax.set_xlim(0, top + 0.1)
    ax.set_xticks(range(0, top + 1), [f"{2**k:,}×" for k in range(0, top + 1)])
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)


def main() -> None:
    fig.setup()
    n = json.loads(Path("results/numbers.json").read_text())
    pop, c = n["population"], n["estimator_c"]
    chain = n["estimator_a"]["nvidia_a"]["cumulative"]
    shares = chain["shares"]
    b = n["estimator_b"]["fits"]
    h1, ladder = n["hypotheses"]["H1"], n["rq1_throughput"]["flagships"]["headline"]["fit"]
    bw, opb = n["rq4_memory"]["mem_bandwidth_gbs"]["fit"], n["rq4_memory"]["ops_per_byte"]["fit"]
    bench = n["hypotheses"]["H6"]["benchmarks"]
    resnet = next(x for x in bench if x["benchmark"] == "resnet")
    below = sum(1 for x in bench if x["realized_below_headline"])
    h100 = next(r for r in n["sample"] if r["product"] == c["end"])
    y_end = math.floor(h100["year"])
    y_start = math.floor(h100["year"] - chain["years"])
    assert c["start"] == chain["members"][0] and c["end"] == chain["members"][-1]
    nvp = c["nvidia"]

    f, ax = _canvas()
    # header
    _t(
        ax,
        M,
        60,
        f"PRE-REGISTERED · {pop['products']} DATA-CENTRE AI ACCELERATORS · {pop['vendors']} VENDORS · "
        f"{pop['source_rows']:,} SOURCED VALUES · {y_start}–{WINDOW_END}",
        10,
        color=fig.MUTED,
    )
    title = "Is Huang's law Moore's law? Where a decade of AI-chip speed came from"
    _fit(f, ax, M, 90, title, 20, R - M, weight="semibold")
    # hero
    _t(ax, M - 4, 142, f"{c['headline_ratio']:.0f}×", 76, color=fig.SERIES_COLOUR["headline"], weight="bold")
    start_fmt, end_fmt = c["start_rate"]["format"].upper(), c["end_rate"]["format"].split("_")[0].upper()
    _t(
        ax,
        470,
        168,
        f"gain in NVIDIA's flagship headline peak throughput\nfrom {c['start']} ({y_start}) to H100 "
        f"({y_end}): {c['start_rate']['tflops']:.3g} TFLOP/s\n({start_fmt}) → "
        f"{c['end_rate']['tflops']:,.0f} TFLOP/s (dense {end_fmt}).",
        15.5,
        linespacing=1.3,
    )
    _fit(
        f,
        ax,
        470,
        308,
        f"Headline doubling time {h1['doubling']:.2f} yr on the {h1['n']} flagships that publish every field "
        f"(95% CI {h1['doubling_ci'][0]:.2f}–{h1['doubling_ci'][1]:.2f})",
        10,
        R - 470,
        color=fig.MUTED,
    )
    _chain(
        f,
        ax,
        M,
        378,
        [
            ("Transistors × clock:", 15, "normal"),
            (f"{c['physical_nf']:.1f}×", 22, "bold"),
            ("· Matrix units and narrower number formats:", 15, "normal"),
            (f"{c['architecture_spec_x_precision']:.1f}×", 22, "bold"),
        ],
    )
    # chart
    _t(
        ax,
        M,
        418,
        f"Where the {c['headline_ratio']:.0f}× came from: two accountings of the same gain",
        12.5,
        weight="semibold",
    )
    _chart(f, c, shares, (M + 170, 448, R, 735))
    _t(
        ax,
        M,
        786,
        f"Both accountings reach about {nvp['total_dense']:.0f}× dense. NVIDIA credits process with "
        f"{nvp['process']:.3g}×; the physical factors here (density × area × clock)\ngive "
        f"{c['physical_nf']:.1f}×, {c['physical_over_nvidia_process']:.1f}× more, because NVIDIA counts the "
        "extra transistors a new node gives as architecture.\n"
        "Sparsity (hatched) is outside the dense comparison.",
        9.5,
        color=fig.MUTED,
        linespacing=1.35,
    )
    # the three shares
    dens = b["density_mtr_mm2"]
    tiles = [
        (
            fig.TERM_COLOUR["density_mtr_mm2"],
            shares["density_mtr_mm2"],
            "Moore's law: transistor density",
            f"doubles every {dens['doubling_years']:.2f} yr "
            f"(CI {dens['doubling_ci'][0]:.2f}–{dens['doubling_ci'][1]:.2f})",
        ),
        (
            fig.TERM_COLOUR["spec_ops_per_transistor_cycle"],
            shares["spec_ops_per_transistor_cycle"] + shares["precision_multiplier"],
            "matrix units + narrower formats",
            f"specialization {100 * shares['spec_ops_per_transistor_cycle']:.0f}% + "
            f"precision {100 * shares['precision_multiplier']:.0f}%",
        ),
        (
            fig.TERM_COLOUR["boost_clock_mhz"],
            shares["boost_clock_mhz"] + shares["area_mm2"],
            "clock + die area",
            f"{100 * shares['boost_clock_mhz']:.0f}% + {100 * shares['area_mm2']:.0f}%; clock trend "
            f"{b['boost_clock_mhz']['slope']:.2f} doublings/yr",
        ),
    ]
    tw, th, gap = (R - M - 2 * 20) / 3, 150, 20
    for i, (accent, share, name, sub) in enumerate(tiles):
        x, y = M + i * (tw + gap), 866
        _tile(ax, x, y, tw, th, accent=accent)
        _t(ax, x + 28, y + 36, f"{100 * share:.0f}%", 32, weight="bold")
        _t(ax, x + 28, y + 102, name, 11)
        _fit(f, ax, x + 28, y + 126, sub, 9.5, tw - 40, color=fig.MUTED)
    _t(
        ax,
        M,
        1034,
        "Moore's law in the density sense is about a third of Huang's law. The rest is matrix units, "
        "narrower\nnumber formats, bigger dies and a faster clock, and the clock has nearly stopped rising.",
        13,
        style="italic",
        linespacing=1.3,
    )
    # four more facts, one row each
    facts = [
        (
            f"{ladder['doubling_years']:.2f} yr",
            f"doubling time of the flagship headline peak over all {ladder['n']} flagships to {WINDOW_END} "
            f"(95% CI {ladder['doubling_ci'][0]:.2f}–{ladder['doubling_ci'][1]:.2f});\n"
            "Moore's 1975 forecast for transistor counts was two years",
        ),
        (
            f"{bw['doubling_years']:.2f} yr",
            f"memory bandwidth doubling time on {bw['n']} flagships (95% CI {bw['doubling_ci'][0]:.2f}–"
            f"{bw['doubling_ci'][1]:.2f}) vs {ladder['doubling_years']:.2f} yr for compute:\n"
            f"operations per byte fetched double every {opb['doubling_years']:.2f} yr. "
            "The memory wall widens",
        ),
        (
            f"{below} of {len(bench)}",
            "MLPerf benchmarks on which measured per-accelerator throughput grew more slowly than the\n"
            f"headline (ResNet-50 training: {resnet['slope_realized']:.2f} vs {resnet['slope_headline']:.2f} "
            "doublings per yr). A peak is not delivered work",
        ),
        (
            f"{y_end}",
            "the last flagship with transistor count, die area and clock all published (H100). Since then\n"
            "no vendor in the sample publishes both die area and clock, so the full decomposition ends there",
        ),
    ]
    fh = 58
    for i, (num, text) in enumerate(facts):
        y = 1108 + i * (fh + 7)
        _tile(ax, M, y, R - M, fh)
        _t(ax, M + 24, y + 11, num, 21, weight="bold")
        _t(ax, M + 210, y + 8, text, 10, linespacing=1.35)
    # footer
    _fit(
        f,
        ax,
        M,
        1386,
        "Every rate is a vendor-published peak, not measured throughput. "
        "Every value carries a source URL, an access date and a confidence level.",
        11.5,
        R - M,
        weight="semibold",
    )
    _t(ax, M, 1414, LINKS, 10.5)
    _t(
        ax,
        M,
        1440,
        "Independent personal research. Public data only. "
        "Does not represent the views of any employer or institution.",
        9.5,
        color=fig.MUTED,
    )
    out = Path("announce/poster.png")
    out.parent.mkdir(exist_ok=True)
    f.savefig(out, dpi=DPI, facecolor="white", metadata={"Software": None})
    print(out)


if __name__ == "__main__":
    main()
