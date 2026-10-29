# Phase 4 report — paper, figures, literature

Done on 2026-10-29. The draft is `paper/paper.md`, built with `chipledger paper` to `paper/chipledger.pdf` (12
pages, of which 1.5 are references) and to the web reader `docs/site/paper/index.html`. Every number in the
text is either filled from `results/numbers.json` by a `{{…}}` placeholder or marked as quoted from a cited
source; the build fails on any other hand-typed number. Nothing was published or sent to an external service.

## Figures

All seven are in `results/figures/` (SVG with text as paths, plus 300-dpi PNG), drawn by `chipledger figures`
from `data/` and `results/numbers.json`, in the house style shared with the sibling repositories.

| file | paper | content |
|---|---|---|
| `f1_ladder` | Figure 1 | (a) headline, 16-bit reference and FP32 rates of flagships by announce year; (b) transistors, density and die area, with fitted trends |
| `f2_chain` | Figure 2 | (a) NVIDIA chain, identity A, one bar per generation step; (b) cumulative shares, NVIDIA (A) and AMD (A′) |
| `f3_regression` | Figure 3 | (a) term slopes with 95 % intervals for identity A, A′ and clock-free; (b) H3b contrast under each sensitivity |
| `f7_dally` | Figure 4 | NVIDIA's four factors against identity A with the 16-bit and the FP32 reference |
| `f4_efficiency` | Figure 5 | headline rate per W, per mm² and per billion transistors |
| `f5_memory` | Figure 6 | memory wall: rate against bandwidth with iso-ops/byte lines; ops per byte over time |
| `f6_mlperf` | Figure 7 | headline against per-accelerator MLPerf throughput, four NVIDIA benchmarks |

No vendor publishes prices, so the brief's per-dollar panel of F4 is not drawn; the caption says so.

## Paper

Structure as in the brief: abstract, introduction, background, data, method, results (rate, decomposition,
reconciliation, efficiency and memory, MLPerf, hypotheses), robustness, discussion (precision floor, reticle and
power limits, forecasts, disclosure), limitations, conclusion, data availability. The brief asked for about 8
pages; the draft is 12 in the sibling template, against 15 for `coauthored` and 18 for `sandbank`. The cheapest
further cuts, if wanted: the identity-A trend table (Figure 3a shows the same slopes), and the background
paragraph on demand-side trend studies.

Changes to analysis output made for the paper (no change to estimates or verdicts):
- `numbers.json` gained population counts (vendors, source rows by confidence), the flagship FP32 and die-area
  trends shown in Figure 1, and the H2b margin: a 4.1 % change in one endpoint's transistor count or die area
  would move the density share to one third.
- Tables: the hypothesis and reconciliation tables use readable labels; a short sensitivity table exists but the
  paper refers to the full one in the repository (`docs/decisions.md` D10).

## Literature

`docs/literature/REVIEW.md`: 31 sources, every one opened on 2026-10-29, metadata checked against Crossref or
arXiv; 29 are cited in the paper. `paper/refs.bib` holds the same 31 entries.

Not cited because no copy could be read (D11): Hennessy & Patterson 2019, Thompson & Spanuth 2021, Wulf & McKee
1995. The paper no longer names the origin of "memory wall" and states the specialization argument from
Leiserson et al. 2020 instead.

Corrections the reading forced on the draft:
- Moore 1975 forecast the two-year cadence for the end of the decade, and already split chip growth into area,
  dimensions and "cleverness"; the paper now says so and calls it the first decomposition of this kind.
- Koomey: 1.57 years (1946–2009), not "about 1.6".
- Gholami et al.: interconnect bandwidth grows 1.4× per two years, DRAM 1.6×; both are now given.
- The WSJ article (Mims 2020) could be read only to its paywall; it is cited only for the headline.

Additions from the reading: Jouppi et al. 2017 (four of six TPU workloads memory-bound), 2021 (compiler-only
MLPerf gains) and 2023 (Google's own split of one TPU generation's peak gain); Mattson et al. 2020 (1.3× from
software on unchanged hardware between the first two MLPerf rounds); Chowdhery et al. 2023 (model FLOPs
utilization 21–46 %); Micikevicius et al. 2022 (FP8 formats).

## Check of Dally's four factors

The factors in estimator (c) match slide 11 of Dally's keynote "Hardware for Deep Learning" (Hot Chips 35,
2023-08-29, doi:10.1109/HCS59251.2023.10254716), read from the PDF: number representation ~16×, complex
instructions ~12.5×, process ~2.5×, sparsity ~2×, product 1000×. No deviation is needed. Clarifications now in
the paper:
1. The chart plots peak Int8-equivalent TOPS, K20X 3.94 → H100 4000; the endpoint includes sparsity (the A100
   point, 1248, is the sparse figure), so 500× is the right dense comparator for our 501×.
2. The slide prints no dates; 2012 and 2022 are read off the chart.
3. The same slide says "Model efficiency has also improved – overall gain > 1000x", which a chip's peak rate
   does not contain.
4. NVIDIA's blog post on the talk is dated 2023-09-29 (the brief had 08-29, the date of the talk).
Earlier versions (MLSys 2021 slides, IEEE Micro 2021) give 317× over 2012–2020 and no numeric split.

## Checks

`ruff`, `ruff format --check`, `mypy --strict` clean; `pytest` passes with 96 % coverage. The PDF was rendered
page by page and inspected; the reader page builds with MathML.

## Decisions for Gate 4

1. **Length.** Keep 12 pages, or cut toward the brief's 8 (the two cuts above give roughly one page).
2. **Phase 5** — release packaging (README, CITATION.cff, .zenodo.json, release notes, history check), local
   only. Repository creation, the Zenodo release, Hugging Face and Pages remain the author's steps.
