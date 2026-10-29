# Pre-registration — *Is Huang's Law Moore's Law? Decomposing a Decade of AI Accelerator Performance Growth, 2012–2026*

- **Author:** Thanatchon Chongmankhong (independent research; public data only; does not represent the views of
  any employer or institution)
- **Frozen at:** git tag `prereg-v1` (to be set when the author approves this file; until then it is a draft)
- **Status at freezing:** no specification has been entered into `data/accelerators.csv` and no source has been
  fetched. This is not a blind pre-registration: the headline figures of NVIDIA's flagship parts and the published
  trend estimates (Epoch AI's hardware trends; NVIDIA's own account of a thousand-fold gain in ten years) are widely
  known, and before drafting the thresholds the author worked the identity through from remembered figures for
  K20X → B200 and P100 → B200 to check that no decision rule is trivially met or trivially failed. Those figures
  are not in the dataset and will be replaced by sourced values. What this document freezes is the question, the
  identity, the sample rule, the reference-precision rule, the estimators and the decision thresholds, so that none
  of them can be chosen after seeing the decomposition.

Changes after freezing are logged in [`DEVIATIONS.md`](DEVIATIONS.md) with date, reason and effect.

## 1. Research questions

- **RQ1 (rate).** How fast has the peak per-chip throughput of data-centre AI accelerators grown between 2012 and
  2026, at a fixed reference precision and at the headline (lowest supported) precision, and how does each
  compare with the cadence of Moore's law in its two forms, transistors per package and transistor density?
- **RQ2 (decomposition).** What share of the growth in headline throughput is attributable to transistor
  density, to total die area (including multi-die packaging), to clock, to architectural specialization at fixed
  precision, and to precision reduction?
- **RQ3 (efficiency).** How fast have throughput per watt, per mm², per transistor and, where prices exist, per
  dollar grown?
- **RQ4 (memory wall).** How fast have memory bandwidth and capacity grown relative to throughput?
- **RQ5 (realized).** Does measured MLPerf throughput per accelerator track headline FLOPS?
- **RQ6 (reconciliation).** Does an independent accounting agree with NVIDIA's own decomposition of its
  2012–2022 gain, and if not, why?

**Relation to prior work.** Epoch AI has estimated doubling times of FLOP/s and FLOP/s per dollar for machine
learning hardware (Hobbhahn & Besiroglu 2022; *Trends in machine learning hardware*, 2023); NVIDIA has published a
vendor decomposition of its own ten-year gain (Dally, Hot Chips 2023; Dally, Keckler & Kirk 2021); Sun et al.
(2019) fitted product-data trends for CPUs and GPUs; Gholami et al. (2024) quantified the memory wall. This study
does not claim the trends as new. What it adds is an exact per-chip accounting identity that splits headline
throughput growth into a Moore's-law component and non-Moore's-law components across vendors, with a source for
every number and an uncertainty for every share, and a quantitative reconciliation with the vendor's account. The
literature review is written in Phase 4 (`docs/literature/`); every reference cited in the paper must have been
opened by the author.

## 2. Definitions

**Unit.** One accelerator *product*: a distinct silicon configuration sold or deployed as a data-centre machine
learning part (one row of `data/accelerators.csv`). Variants of the same silicon that differ only in memory,
power or form factor (A100 40 GB vs 80 GB; H100 SXM vs PCIe) are separate rows with `variant_of` naming the
primary variant; only primary variants enter the analyses. The primary variant is the highest-TDP module form
(SXM, OAM, mezzanine) of the product.

**Date.** Primary: the announce date, the first public disclosure of the product with specifications.
Sensitivity: the ship date (general availability). Year is decimal.

**Flagship.** Within each vendor and architecture generation, the primary-variant part with the highest headline
dense throughput among parts positioned for training. Inference-only parts (T4, L4, L40S, A30, Inferentia) are
not flagships.

**Peak throughput.** The vendor-published peak, dense (no structured sparsity), per package (per *accelerator
die* is also recorded for multi-die parts), in TFLOP/s for floating-point formats and TOPS for integer formats,
both counting two operations per multiply–accumulate. Vector (SIMT) rates and matrix-unit rates (tensor cores,
matrix cores, MXUs, systolic arrays) are separate columns.

**Headline dense throughput** `P`: the largest dense rate over every supported format and unit, INT8 and INT4
included. **Headline format:** the format at which `P` is reached.

**Reference throughput** `R`: the dense matrix-unit FP16 or BF16 rate, whichever is larger; if the product has no
matrix unit, the vector FP16/BF16 rate; if it supports no 16-bit format, the FP32 rate, with `ref_is_fp32` set.

**Precision multiplier** `P / R`: the gain from running arithmetic narrower than 16 bits.

**Specialization** `R / (N f)`: reference operations per transistor per clock cycle, where `N` is the transistor
count of the package and `f` the boost clock. It rises when more of the silicon does reference-precision
arithmetic per cycle (matrix units, wider SIMD, packed 16-bit math) and falls when transistors go to caches, I/O
or features that do not raise `R`. For products without a 16-bit format, the later introduction of packed FP16
math is counted here in the primary analysis and under the precision multiplier in the FP32-reference
sensitivity (§6).

**Area** `A`: the total silicon area of the package's compute dies (`die_area_compute_total_mm2`), primary;
total area including I/O dies as a sensitivity. **Density** `N / A`, in millions of transistors per mm².
**Transistors per package** `N`.

**Sparsity multiplier:** the vendor's structured-sparsity rate divided by the dense rate at the same format
(usually 2), reported on its own and never inside `P`.

**Power** `W`: the vendor's TDP or TBP of the primary variant.

**Moore's law** is tested in both of its usual forms: transistors per package (`N`, the 1965/1975 formulation)
and transistor density (`N / A`, the scaling formulation).

## 3. Sample

**Inclusion rule.** A product is in the sample if (i) it is a data-centre accelerator marketed by its vendor for
machine learning training and/or inference, (ii) it was announced between 2012-01-01 and 2026-10-31, and
(iii) the vendor or a vendor-authored paper has published at least one peak throughput figure for it. A product
enters the **decomposition sample** only if `N`, `A`, `f`, `W` and a reference rate are all published with a
source; otherwise it stays in the throughput-trend sample and is listed in `data/coverage.md` with the missing
fields.

**Exclusions.** Consumer and workstation GPUs; CPUs; FPGAs; mobile and edge NPUs; products whose only published
numbers come from leaks.

**Seed list.** `configs/seed.yaml`, frozen with this file, names the products the search starts from. Products
found during collection that meet the rule are added and logged in `DEVIATIONS.md`.

**Flags.** Wafer-scale parts (Cerebras) are included and flagged; every regression is reported with and without
them. Google TPUs rarely publish transistor count or die area; they enter the throughput-trend sample and the
efficiency analysis where TDP is published. A product whose boost clock is not published by the vendor takes the
TechPowerUp value at medium confidence; if no clock is published anywhere, the product leaves the decomposition
sample and the clock-free identity of §6 covers it.

**Sources**, in priority order: vendor datasheet, whitepaper or product page → vendor-authored conference paper
(ISSCC, Hot Chips, ISCA) → the TechPowerUp GPU database and WikiChip → Epoch AI's machine learning hardware
database (CC BY; used as a cross-check and cited) → press (prices only, low confidence). Every value carries a
URL, an access date and a confidence level in `data/sources.csv`; a value without a source fails
`chipledger validate`. When sources disagree, the vendor's primary document wins and the alternatives are listed
in `data/conflicts.md`.

## 4. Identities and estimators

**Identity A (silicon view).** For every product in the decomposition sample, by construction,

    log2 P = log2 (N / A) + log2 A + log2 f + log2 (R / (N f)) + log2 (P / R)
           = density      + area    + clock  + specialization   + precision multiplier

Sparsity is outside `P`. `chipledger derive` computes every term and fails if the identity does not hold to
10⁻⁹ for any complete row.

**Identity B (power view).** `log2 P = log2 (P / W) + log2 W`: throughput growth split into efficiency and a
larger power budget.

**Identity C (area view).** `log2 P = log2 (P / A) + log2 A`.

**Estimator (a), chain-linked decomposition.** The NVIDIA chain is the first flagship of each architecture:
K20X (Kepler), M40 (Maxwell), P100, V100, A100, H100 SXM, B200, and B300 and Rubin if their `N`, `A`, `f`, `W`
and `R` are public at collection. For each step and cumulatively from K20X, the change in each term of identity
A is reported as its Δlog2 and as a share of Δlog2 `P`. The AMD Instinct chain (MI25, MI60, MI100, MI250X,
MI300X, MI355X, MI400-series if public) is reported the same way as a secondary chain.

**Estimator (b), regression.** For each term `y` of identity A and for `P`, ordinary least squares of
`log2 y` on decimal announce year. The primary sample is the flagships in the decomposition sample, all
vendors. Because the identity is additive in logs, the slopes of the terms sum to the slope of `P` on the same
sample; `chipledger analyze` asserts this. Doubling time is `1 / slope`. Uncertainty: percentile intervals
from a chip-level bootstrap (2,000 draws, seed 20261029) and HC3 standard errors; the Theil–Sen slope as a
robustness estimator. Subsamples: NVIDIA only; all products in the decomposition sample with vendor fixed
effects; the frontier envelope (products that set a new maximum headline rate when announced); with and without
wafer-scale parts.

**Estimator (c), reconciliation with the vendor's account.** NVIDIA attributes its ~1000× single-chip
inference gain from K20X (2012) to H100 (2022) to number representation 16×, complex instructions 12.5×, process
2.5× and sparsity 2× (Dally, Hot Chips 2023). Identity A is computed for K20X → H100 SXM with the same endpoint
rate NVIDIA uses (dense FP8 for H100; the 2× sparsity is set aside). The physical factor, density × area × clock
= growth of `N f`, is compared with NVIDIA's "process" contribution, and the non-physical factor, specialization
× precision multiplier, with NVIDIA's "number representation × complex instructions". The pre-specified
interpretation: the two accountings put transistor count on different sides of the ledger; NVIDIA's "process"
is the per-transistor gain from a newer node, and the transistors added by the node and the larger die are
credited to architecture, whereas identity A counts every transistor as a physical input. The paper reports both
accountings and the mapping between them.

## 5. Hypotheses and decision rules

Each hypothesis is decided on its own pre-registered rule. The hypotheses are directional and few, and no
multiplicity correction is applied; every one is reported whatever its outcome.

- **H1 (rate).** In the flagship decomposition sample, the doubling time of headline dense throughput from
  estimator (b) is at most 1.5 years and its 95% bootstrap interval excludes 2.0 years (upper bound below 2.0).
  *Falsified* if the point estimate exceeds 1.5 years or the interval reaches 2.0.
- **H2 (Moore's law proper is the minority).** Both: (a) the doubling time of transistor density in the same
  sample is at least 2.5 years (point estimate); (b) in the NVIDIA chain, density's share of the cumulative
  Δlog2 `P` from K20X to the last chain member is below one third. *Falsified* if either part fails.
- **H3 (architecture and arithmetic outweigh density).** Both: (a) in the NVIDIA chain, the cumulative shares of
  specialization and precision multiplier together exceed the share of density; (b) in the flagship regression,
  the sum of the specialization and precision slopes exceeds the density slope, with the 95% bootstrap interval
  of the difference excluding zero. *Falsified* if either part fails.
- **H4 (bigger silicon and more watts after 2020).** In the NVIDIA chain, the mean per-step Δlog2 of area and
  the mean per-step Δlog2 of TDP are both larger over steps whose later member was announced after 2020-12-31
  than over earlier steps. Descriptive: too few steps for an interval. *Supported* only if both are larger.
- **H5 (memory wall).** In the flagship regression, the slope of memory bandwidth is below the slope of
  headline throughput, with the 95% bootstrap interval of the difference excluding zero.
- **H6 (realized vs headline; exploratory, timeboxed to one session).** For each MLPerf benchmark with results for
  at least three generations of one vendor's flagships, the slope of log2 per-accelerator throughput on year is
  smaller than the slope of log2 headline dense throughput on the same products. *Supported* if this holds for
  every analysed benchmark, *partly supported* for a majority, *not supported* otherwise, *not assessed* if no
  benchmark qualifies within the timebox.
- **H7 (reconciliation).** For K20X → H100 SXM, the physical factor of estimator (c), the growth of `N f`, is at
  least 10×, that is, at least four times NVIDIA's stated 2.5× from process. *Falsified* if the growth of `N f`
  is below 10×.

## 6. Sensitivity analyses

Pre-specified and reported in one table next to the primary result: ship date instead of announce date; FP32 as
the reference rate for every product; headline restricted to floating-point formats (INT8/INT4 excluded);
headline taken with sparsity; area including I/O dies; the clock-free identity (specialization defined as
`R / N`, so the clock is absorbed into it; covers products without a published clock); all products in the
decomposition sample rather than flagships only; NVIDIA only; without wafer-scale parts; the frontier envelope;
the Theil–Sen slope; leave-one-vendor-out.

## 7. Secondary analyses

- **Efficiency (RQ3).** Doubling times of `P / W`, `R / W`, `P / A`, `P / N` and, where prices exist, `P` per
  dollar; the last compared with Epoch AI's estimate of about 2.5 years for FLOP/s per dollar and labelled low
  confidence.
- **Memory wall (RQ4).** Doubling times of memory bandwidth and capacity; the trajectory of operations per byte
  (`P` over bandwidth); comparison with Gholami et al. (2024).
- **Node reference series.** Logic-transistor density by process node and year of volume production
  (`data/nodes.csv`, sourced the same way), to show whether AI accelerators ride the node frontier or lag it.
- **Identity B and C shares**, per chain step and cumulatively.

## 8. Data rules and tests

The schema is `src/chipledger/schema.py`. `chipledger validate` fails on: a missing or unknown column; a
duplicate product; a malformed or inconsistent date; a non-positive or non-numeric value; a variant marked as
flagship or pointing to an unknown product; a sparse rate below its dense rate; total area below compute-die
area; a price without a confidence level; a value in a sourced field without a row in `data/sources.csv`, or
with a source row that states a different value; a source row with an unknown product, a non-web URL, a
malformed access date or an unknown confidence level. It warns for every flagship outside the decomposition
sample. `chipledger derive` fails if any identity residual exceeds 10⁻⁹. Every rule has a unit test.

## 9. What is frozen

This file; `configs/seed.yaml`; the column set, the reference rule, the headline rule and the identity terms in
`src/chipledger/schema.py` and `src/chipledger/identity.py`; the decision rules of §5; the sensitivity list of §6.
Code may change to fix defects or add analyses; any change to a frozen rule, and any product added beyond the
seed list, is logged in `DEVIATIONS.md`.

## 10. Limitations stated in advance

Peak rates are vendor marketing figures and overstate what software achieves; H6 measures the gap only where
MLPerf data allow. Transistor counts and die areas are vendor-reported and rounded. Google's TPUs and most
custom parts lack the silicon fields and fall out of the decomposition. Boost clocks are not always published
and are unstable across SKUs. The regressions have few points (roughly 15–25 flagships), so intervals will be
wide. The chain decomposition follows one vendor, and "announce" dates differ in meaning across vendors. Prices
are unreliable and used only in a labelled secondary analysis. The identity is an accounting, not a causal
model: it says how much of the growth each term carries, not what would have happened without it.

## 11. Release

Data CC BY 4.0 (`LICENSE-DATA`), code MIT (`LICENSE`). The dataset is released on Hugging Face with its provenance
table and this pre-registration; the repository is archived on Zenodo at release. No personal data are involved.
