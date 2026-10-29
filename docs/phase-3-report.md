# Phase 3 report — analysis

Run on 2026-10-29 with `chipledger analyze` on the dataset after the Gate 2 decisions (79 products, 66 primary
rows, Cloud AI 100 Ultra excluded as not per package). Every number below is in `results/numbers.json`; the
tables are in `results/tables/`. Changes to frozen rules and analysis details not fixed by the pre-registration
are logged in `DEVIATIONS.md` (rows 4–8). Nothing was published or sent to an external service.

## Hypotheses

| | rule (§5) | estimate | verdict |
|---|---|---|---|
| H1 | doubling of headline P ≤ 1.5 yr, 95 % CI upper bound < 2.0 yr | 0.83 yr [0.62, 1.13], 9 flagships | **supported** |
| H2 | (a) density doubling ≥ 2.5 yr; (b) density share of the NVIDIA chain < 1/3 | (a) 2.76 yr [2.20, 3.43]; (b) 0.327, K20X → H100 | **supported, (b) by a hair** |
| H3 | (a) chain: specialization + precision share > density share; (b) regression: their slopes minus the density slope > 0, CI excludes 0 | (a) 0.450 vs 0.327; (b) 0.090 doublings/yr [−0.103, 0.307] | **falsified** ((a) passes, (b) fails) |
| H4 | NVIDIA chain: mean Δlog2 of area and of TDP larger on steps ending after 2020 | area −0.02 vs 0.15; TDP 0.81 vs 0.19 (one late step, A100 → H100) | **not supported** (area fails) |
| H5 | slope of P minus slope of memory bandwidth > 0, CI excludes 0 | 0.709 doublings/yr [0.395, 1.072], 7 flagships | **supported** |
| H6 | MLPerf per-accelerator slope below headline slope on every qualifying benchmark | 4 of 4 benchmarks (NVIDIA): realized 0.45–0.83 vs headline 0.79–1.01 doublings/yr | **supported** (exploratory) |
| H7 | K20X → H100: growth of N·f ≥ 10× | 30.5× (N 11.3×, f 2.7×) | **supported** |

**H1.** Headline dense throughput of the nine flagships in the decomposition sample (K40, M40, P100, V100,
MI60, A100, GC200, WSE-2, H100; 2013–2022) doubles every 0.83 years. The result holds in every computable
sensitivity: the largest upper bound is 1.38 years (clock-free identity). On the wider throughput sample, which
needs no silicon fields, the doubling time is 1.23 years [1.08, 1.49] over 43 flagships (2013–2026) and 0.96
years [0.82, 1.05] on the frontier envelope. Moore's law in its two forms, on the flagships that publish the
fields: transistors per package double every 1.87 years [1.47, 2.26] (26 flagships), density every 3.06 years
[2.49, 3.80] (12 flagships).

**H2.** Part (a) passes on the point estimate as the rule requires, but the interval [2.20, 3.43] reaches below
2.5. Part (b) passes by 0.006: density carries 0.327 of the cumulative Δlog2 P against a threshold of 0.333.
Every chain variant keeps it below one third (0.283 to 0.327), but the margin is thin: the share depends only on
the two endpoints, and a 4 % change in K20X's or H100's die area or transistor count would reverse it.

**H3.** The chain accounting passes: specialization (0.339) and precision (0.111) together carry 0.450, density
0.327. The regression part fails: the specialization and precision slopes (0.332 and 0.121 doublings/yr)
exceed the density slope (0.363) by 0.090, and the bootstrap interval includes zero. Three of sixteen
sensitivities exclude zero (FP32 reference 0.211 [0.030, 0.516]; headline with sparsity 0.322 [0.015, 0.633];
vendor fixed effects 0.248 [0.103, 0.603]); the primary result decides. The precision term is the weak one:
its Theil–Sen slope is 0, because most flagships have a precision multiplier of 1 or 2.

**H4.** The five-term chain has one step ending after 2020 (A100 → H100). Its TDP rose (400 → 700 W, Δlog2
0.81 against a mean of 0.19 before), but its die area fell slightly (826 → 814 mm²). Over every NVIDIA chain
member with a TDP (to B300), the TDP part holds: 0.60 vs 0.19 (supplementary). Area after H100 cannot be
observed: NVIDIA publishes no die area for Blackwell.

**H5.** Over the seven flagships with a bandwidth in the decomposition sample (GC200 and WSE-2 have on-chip
memory only), headline P doubles every 0.88 years and memory bandwidth every 2.36. Over all 38 flagships with
both, the gap is 0.454 [0.349, 0.530] doublings per year (P 1.21 years, bandwidth 2.70 years).

**H6 (exploratory).** MLPerf results were collected from the MLCommons results repositories (`data/mlperf.csv`,
27 rows, each with the URL of the log it comes from; training values are the olympic mean of the run times,
DERIVED). Four benchmarks have three generations of one vendor's flagships, all NVIDIA; no other vendor has
three on one benchmark. Slopes of log2 per-accelerator throughput and of log2 headline P on announce year, same
products, each product's first round on the benchmark:

| benchmark | products | realized (doublings/yr) | headline (doublings/yr) |
|---|---|---|---|
| Training ResNet-50 | V100, A100, H100 | 0.450 | 0.846 |
| Training BERT (v1.0+ definition) | A100, H100, B200 | 0.651 | 0.786 |
| Training Llama 2 70B LoRA | H100, B200, B300 | 0.577 | 1.006 |
| Inference Llama 2 70B (99.9), Offline | H100, B200, B300 | 0.827 | 1.006 |

Realized throughput grows more slowly than the headline rate on all four, so H6 is supported; with each
product's best result over all rounds the realized slopes are 0.492, 0.556, 0.717 and 0.653, and the verdict is
the same. Caveats: three points per benchmark, so no interval; BERT v0.7 (V100's only BERT result, and A100's
first) stops at a lower target accuracy and is excluded, so A100's first BERT result is v1.0; several first
results are in the preview category (H100 ResNet and BERT, B200 BERT, LoRA and inference), and B200's first
inference result is a one-GPU system; the official reference-convergence-point scaling (up to about 3.5 %) is
not applied, equally to every row. Two values were re-read from the logs by hand (H100 and B300 Llama 2 70B
tokens per second) and two training values recomputed from the raw logs (B200 LoRA 12.7184 min, A100 BERT v1.0
21.6926 min); all four match.

**H7 and estimator (c).** From K20X (3.95 TFLOP/s FP32) to H100 SXM (1,979 TFLOP/s dense FP8) the headline
rate grows 501×; NVIDIA's account gives 1,000× including 2× sparsity, that is 500× dense. The two totals
agree. They divide it differently:

| factor | identity A | identity A, FP32 reference | NVIDIA (as frozen in §4) |
|---|---|---|---|
| physical: N·f (density 7.63 × area 1.48 × clock 2.70) | **30.5×** | 30.5× | process 2.5× |
| specialization R/(N f) | 8.22× | 0.56× | complex instructions 12.5× |
| precision multiplier P/R | 2.00× | 29.5× | number representation 16× |
| non-physical: spec × precision | **16.4×** | 16.4× | 200× |

The physical factor is 12.2 times NVIDIA's "process" term; 16.4 × 12.2 = 200, so the whole difference is the
transistors added by newer nodes and larger dies, which NVIDIA credits to architecture and identity A counts as
physical input. This is the interpretation pre-specified in §4. The NVIDIA factors are the ones written into the
pre-registration; they are checked against the talk itself in Phase 4.

## Estimator (a): chains

| chain | members in the sample | years | doublings of P | shares |
|---|---|---|---|---|
| NVIDIA, identity A | K20X → M40 → P100 → V100 → A100 → H100 | 9.4 | 8.97 (one per 1.04 yr) | density 0.327, area 0.063, clock 0.160, specialization 0.339, precision 0.111 |
| NVIDIA, identity A′ | the same six | 9.4 | 8.97 | transistors 0.390, clock 0.160, specialization 0.339, precision 0.111 |
| NVIDIA, clock-free | the same six | 9.4 | 8.97 | density 0.327, area 0.063, specialization (R/N) 0.499, precision 0.111 |
| AMD, identity A′ | MI60 → MI100 → MI250X → MI325X → MI355X | 6.6 | 7.42 (one per 0.89 yr) | transistors 0.513, clock 0.056, specialization 0.294, precision 0.137 |
| NVIDIA, identity B | K20X → … → H100 → B200 → B300 | 12.4 | 11.89 | P/W 0.783, power 0.217 |
| AMD, identity B | MI25 → MI60 → MI100 → MI250X → MI325X → MI355X | 8.0 | 8.68 | P/W 0.744, power 0.256 |

Every NVIDIA chain ends at H100: B200, B300 and Rubin have no published boost clock, so the A′ chain does not
extend past H100 as DEVIATIONS #3 anticipated. The AMD five-term chain has one member (MI60) and is not
reported. With MI300X as the primary variant the AMD chain is unchanged except for the dates.

Per step, the drivers differ sharply (`results/tables/t3_chains.md`): K20X → M40 is clock (K20X runs at 732 MHz
with no boost); M40 → P100 is density (28 nm → 16 nm); P100 → V100 is specialization (tensor cores, 2.05 of
2.56 doublings); V100 → A100 is density plus precision (A100's INT4 rate); A100 → H100 is density, clock and
specialization, minus one doubling of precision (H100's headline is FP8, which has no INT4 above it).

## Sensitivities (§6)

`results/tables/t5_sensitivity.md` has every row. In short: H1 holds in every computable variant; density
doubles in 2.6–3.5 years in every variant with a density term except "without NVIDIA" (3.9, three products); the density share of the NVIDIA chain stays
between 0.283 and 0.327; the H3b contrast is positive in fifteen of sixteen variants but its interval excludes
zero in only three.

Two variants could not be computed as specified:

- **Ship date.** Only 2 of the 9 decomposition flagships have a vendor-stated ship date, so the trend cannot be
  fitted. In the throughput sample, 15 flagships have one: by ship date P doubles every 1.67 years, and by
  announce date the same 15 products give 1.70 years. The date convention barely matters; the difference from
  1.23 years is which products publish a ship date.
- **Area including I/O dies** gives the primary numbers exactly: all nine flagships in the sample are
  monolithic, so the two areas are equal.

"Without NVIDIA" leaves three products and is shown for completeness only. The high-confidence-only variant
(no Epoch AI or press values) drops H100's clock, so its chain ends at A100.

## Secondary analyses (§7)

| series (flagships) | n | doubling (yr) | 95 % CI |
|---|---|---|---|
| headline P | 43 | 1.23 | [1.08, 1.49] |
| reference R | 42 | 1.61 | [1.38, 2.10] |
| P / W | 29 | 1.63 | [1.38, 2.13] |
| R / W | 29 | 2.22 | [1.80, 3.32] |
| P / A | 12 | 1.27 | [0.88, 2.00] |
| P / N | 25 | 2.02 | [1.71, 2.75] |
| memory bandwidth | 38 | 2.70 | [2.24, 3.47] |
| memory capacity | 39 | 2.61 | [2.27, 3.12] |
| operations per byte | 38 | 2.20 | [1.89, 2.87] |

No vendor states a launch price for any product in the dataset, so P per dollar is not estimated.

**Node adoption lag.** For the 28 primary products whose foundry is published, the median time from a node's
volume production (mid-year) to the accelerator's announcement is 2.5 years; NVIDIA 1.2, AMD 1.9, Graphcore
2.7, Cerebras 3.2, Intel 3.8, SambaNova 4.2, Meta 4.3. The lag shows no clear trend (0.20 years per year,
[−0.01, 0.40]). NVIDIA publishes no foundry for K20X, K40 and M40, and Google, AWS and Huawei none for most
parts, so they are not in this series; NVIDIA's custom nodes (4N, 4NP, 12 nm FFN) are mapped to the nearest
foundry node.

## Surprises

1. The independent accounting reproduces NVIDIA's total almost exactly (501× vs 500× dense) and disagrees on
   the split by a factor of 12, all of it the transistor count.
2. The precision term is lumpy, not a trend: it jumps at A100 (INT4) and falls back at H100, and its
   regression slope is not distinguishable from zero. Specialization, not precision, carries the architectural
   share.
3. H2b passes by 0.006 of a share, the effect of a 4 % change in one endpoint's die area or transistor count.
4. Die area stopped being published in 2022, so the hypothesis about bigger silicon after 2020 (H4) is tested
   on one step.

## Decisions for Gate 3

1. **Report as is.** The verdicts follow the frozen rules; H3 is falsified and H4 not supported, and the paper
   reports them as such, with the sensitivities next to them.
2. **Phase 4 scope:** figures F1–F7, the paper (pandoc → Typst), and the literature review, in which every
   cited document is opened, including Dally's Hot Chips 2023 talk to check the four factors used in estimator
   (c).
