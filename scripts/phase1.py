"""Phase 1 feasibility run: chain decomposition, trend table and the two rough figures.

Usage: uv run python scripts/phase1.py
Reads results/derived.csv (from `chipledger derive`) and configs/seed.yaml; writes
work/phase1/phase1.json, work/phase1/*.md tables and figures/phase1/f{1,2}_*.{svg,png}.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chipledger.analysis import chain, figures, trend  # noqa: E402
from chipledger.identity import TERMS  # noqa: E402

OUT = Path("work/phase1")
FIG = Path("figures/phase1")


def md_table(df: pd.DataFrame, fmt: str = "{:.3f}") -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = [fmt.format(v) if isinstance(v, float) else str(v) for v in r]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    d = pd.read_csv("results/derived.csv")
    seed = yaml.safe_load(Path("configs/seed.yaml").read_text())
    out: dict = {"n_products": len(d), "n_decomposition": int(d["residual_a"].notna().sum())}

    # estimator (a) on the NVIDIA chain, AMD chain secondary
    for vendor in ["NVIDIA", "AMD"]:
        members = seed["vendors"][vendor]["chain"] + seed["vendors"][vendor].get("chain_candidates", [])
        st = chain.steps(d, chain.resolve(d.fillna({"variant_of": ""}), members))
        out[f"chain_{vendor}"] = {"steps": st.to_dict("records"), "cumulative": chain.cumulative(st)}
        if not st.empty:
            sh = chain.shares(st)
            (OUT / f"chain_{vendor}.md").write_text(
                "Δlog2 per step\n\n"
                + md_table(st[["from", "to", "dlog2_headline", *[f"dlog2_{t}" for t in TERMS]]])
                + "\n\nshare of the step's headline Δlog2\n\n"
                + md_table(sh)
                + "\n"
            )
            if vendor == "NVIDIA":
                figures.f2_chain(st, FIG)

    # estimator (b) on flagships in the decomposition sample
    flag = d[d["is_flagship"] & d["residual_a"].notna()]
    fits, draws = trend.fit_all(flag)
    trend.check_additivity(fits)
    rows = [
        {
            "series": f.series.removeprefix("log2_"),
            "n": f.n,
            "slope (dbl/yr)": f.slope,
            "95% CI": f"[{f.slope_ci[0]:.3f}, {f.slope_ci[1]:.3f}]",
            "doubling (yr)": f.doubling_years,
            "doubling CI": f"[{f.doubling_ci[0]:.2f}, {f.doubling_ci[1]:.2f}]",
            "HC3 se": f.se_hc3,
            "Theil–Sen": f.theil_sen,
        }
        for f in fits
    ]
    (OUT / "trend_flagships.md").write_text(md_table(pd.DataFrame(rows)) + "\n")
    out["trend_flagships"] = [f.to_dict() for f in fits]
    out["contrast_h3"] = trend.contrast(
        draws,
        ["log2_spec_ops_per_transistor_cycle", "log2_precision_multiplier"],
        ["log2_density_mtr_mm2"],
        fits,
    )
    figures.f1_ladder(d[d["is_flagship"]], [], FIG)  # per-series fits on every flagship with the value

    # H5: bandwidth vs headline on flagships with both
    bw = d[d["is_flagship"] & d["mem_bandwidth_gbs"].notna() & d["log2_headline"].notna()].copy()
    bw["log2_bw"] = np.log2(bw["mem_bandwidth_gbs"])
    bfits, bdraws = trend.fit_all(bw, ["log2_headline", "log2_bw"])
    out["h5"] = {
        "fits": [f.to_dict() for f in bfits],
        "contrast": trend.contrast(bdraws, ["log2_headline"], ["log2_bw"], bfits),
    }

    (OUT / "phase1.json").write_text(json.dumps(out, indent=2, default=float))
    print(json.dumps({k: v for k, v in out.items() if k.startswith("n_")}))
    print((OUT / "trend_flagships.md").read_text())
    for vendor in ["NVIDIA", "AMD"]:
        c = out[f"chain_{vendor}"]["cumulative"]
        if c["members"]:
            print(
                vendor,
                c["members"][0],
                "→",
                c["members"][-1],
                f"{c['years']:.1f} y,",
                f"{c['dlog2_headline']:.2f} doublings, doubling every {c['doubling_years']:.2f} y",
            )
            print("  shares:", {t: round(s, 3) for t, s in c["shares"].items()})
    print("H3 contrast:", out["contrast_h3"])
    print("H5 contrast:", out["h5"]["contrast"])


if __name__ == "__main__":
    main()
