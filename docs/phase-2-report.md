# Phase 2 report — full dataset

Collected 2026-10-29 by six collectors working from one brief (vendor documents first, vendor-authored papers
second, Epoch AI at medium confidence only where nothing else exists, press only for on-the-record vendor
statements, leaks never), merged and validated here. Nothing was published or sent to an external service.

## The dataset

| | count |
|---|---|
| products (rows) | 79: 67 primary, 12 variants |
| vendors | 14 — NVIDIA 18, AMD 12, Google 11, Meta 6, AWS 5, Intel 4, Huawei 4, Tenstorrent 4, Cerebras 3, Graphcore 3, Microsoft 3, SambaNova 3, Qualcomm 2, Groq 1 |
| flagships | 45 (44 with a headline rate) |
| source rows | 1,150: high 1,121, medium 24 (18 from Epoch AI), low 5 |
| conflicts listed | 56 rows in `data/conflicts.md` |
| process nodes | 22 in `data/nodes.csv` |

`chipledger validate`: 0 errors, 36 warnings (flagships outside the decomposition sample). Every identity holds
to 3.6·10⁻¹⁵.

**Samples (primary variants).**

| sample | products | flagships | flagship members |
|---|---|---|---|
| throughput trend | 66 | 44 | — |
| identity A (N, A, f, W, R) | 11 | 9 | K20X, M40, P100, V100, A100, H100, MI60, WSE-2, GC200 |
| identity A′ (N, f, W, R) | 19 | 15 | the nine above + MI100, MI250X, MI300X, MI355X, TPU v2, TPU v3 |
| clock-free (N, A, W, R) | 13 | 11 | the nine above + MI25, Maia 100 |

What this buys: the five-term NVIDIA chain runs K20X → H100 (2012–2022); the AMD chain runs MI60 → MI355X under
A′ (2018–2025). Blackwell, Rubin, every TPU after v3 and every AWS, Huawei and Meta part stay in the throughput
and efficiency analyses only: their vendors publish neither die area nor clock.

**Not included** (fail inclusion rule (iii), no vendor-published peak rate): SambaNova SN10 (only "> 300 TFLOPs"),
Cerebras WSE-1, Huawei Ascend 910B (every figure is from analysts, resellers or leaks). Cerebras WSE-3 is in the
dataset but has only a sparse rate (unstructured sparsity, no vendor rule for dense), so it has no headline.

**Beyond the seed list** (added because they meet the inclusion rule; to be logged in `DEVIATIONS.md`): Rubin,
MI455X, TPU 8t, TPU 8i, WSE-3 Turbo, Ascend 950DT, Ascend 950PR, Maia 200, Maia 300, MTIA 300, 400, 450, 500,
SN30, SN50.

## Checks

1. **Spot-check against the documents.** Fourteen Phase 2 values were drawn at random (seed 20261029) from the
   fields that drive the identity and re-read from the cited source. Nine were found verbatim with the right
   context (A30 clock, WSE-3 transistors, TPU 8i FP4 rate, Wormhole n150 TDP, Ascend 910 compute-die area, MI210
   FP16 rate, MI350X vector FP16, MTIA v2 die area, Inferentia FP16 rate). Two (MTIA 500 FP8, MTIA 450 TDP) come
   from a table Meta published as an image; every ratio the blog states in text (FP8 ×5, MX4 +75 % and +43 %,
   bandwidth +51 %, ×2, +50 %, ×4.5 overall) matches the recorded rates and bandwidths exactly, but the TDPs have
   no textual cross-check. Three (MI250 transistors, GroqChip transistors, T4 INT8) could not be re-read
   automatically and were not re-verified.
2. **Epoch AI cross-check.** 47 products matched by name; 138 of 158 overlapping values (excluding values taken
   from Epoch AI) agree within 2 %. The 20 that differ are variant choices (Epoch AI's B200/B300 rows are the
   1,000/1,100 W HGX parts; MI250X and Maia 100 have two TDP figures), known source conflicts (Ascend 910/910C,
   Gaudi 2, TPU v2 bandwidth), a definitional difference (Epoch AI's MTIA v1/v2 bandwidth is on-chip SRAM; this
   dataset records DRAM), and K80, which is recorded as a two-GPU board (below). Details:
   `work/phase2/epoch_crosscheck.md` (not committed; reproducible from the snapshot).
3. **Patches** filled 19 empty cells of existing rows (H100 dense rates and clock from Epoch AI; B200 and B300
   dense rates from NVIDIA's stated sparse/dense rule; TPU v7 memory type; MI100 and MI250X L2). No filled cell
   was overwritten.

## Process nodes

All 22 nodes have a year of volume production from the foundry's own documents. Absolute logic density is
published only for Intel 14 nm (37.5 MTr/mm²) and Intel 10 nm (100.8 MTr/mm²); TSMC and Samsung publish relative
gains only ("N5 1.8× N7"), quoted in the notes, and Samsung's "area efficiency" is not a density. The series can
date when accelerators adopt a node relative to its volume production; it cannot give an absolute density
frontier without building a derived index.

## Decisions needed before Phase 3 (Gate 2)

1. **Kepler flagship.** K20X and K80 are both marked flagship. §2 counts throughput *per package*; K80 is a board
   with two GK210 packages, recorded as board totals. Per package, K80 (4.37 TFLOP/s FP32) is below K40 (5.04), so
   the literal rule makes **K40** the Kepler flagship. *Recommendation:* convert K80 to per-package values
   (÷ 2, DERIVED, NVIDIA states two GPUs), make K40 the Kepler flagship, keep K20X as the first member of the
   pre-registered chain (the chain is frozen by name, and H7 is K20X → H100). The same per-package rule applies
   to Wormhole n300 (two ASICs; n150 becomes the primary) and Cloud AI 100 Ultra (chip count not stated: keep
   as a card, flag it, and exclude it from per-package analyses).
2. **Highest-TDP primary variant.** §2 makes MI325X (1,000 W) the primary over MI300X (750 W): same silicon, more
   memory, announced later. *Recommendation:* apply the frozen rule as written; report MI300X in the
   ship-date/announce-date sensitivity. (H200 ties H100 at 700 W; H100 stays primary.)
3. **Vector INT8.** §2's headline counts every format and unit, but the schema has no vector INT8 column; this
   changes MI60's and MI50's headline (≈ 59 TOPS DP4A-style vs 29.5 FP16). *Recommendation:* add an `int8`
   column (a schema fix to match the frozen definition, not a deviation) and fill it where vendors publish it
   (V100, MI50, MI60).
4. **Node series.** *Recommendation:* use the year of volume production only (adoption lag), and quote the
   foundries' relative gains in the text; do not build a derived absolute-density index.
