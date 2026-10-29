---
license: cc-by-4.0
pretty_name: "chipledger: sourced specifications of data-centre AI accelerators, 2012–2026"
language:
  - en
size_categories:
  - n<1K
tags:
  - hardware
  - ai-accelerators
  - gpu
  - moores-law
  - technology-trends
  - provenance
configs:
  - config_name: accelerators
    data_files: data/accelerators.csv
    default: true
  - config_name: sources
    data_files: data/sources.csv
  - config_name: derived
    data_files: results/derived.csv
  - config_name: mlperf
    data_files: data/mlperf.csv
  - config_name: nodes
    data_files: data/nodes.csv
---

# chipledger: sourced specifications of data-centre AI accelerators, 2012–2026

{{PRODUCTS}} data-centre machine learning accelerators from {{VENDORS}} vendors, announced {{FIRST}} to {{LAST}}: process
node, transistor count, compute and total die area, boost clock, TDP, every published peak rate from FP64 vector
to FP4 matrix (dense and, where published, with structured sparsity), memory type, capacity and bandwidth. Every
value has a row in `sources.csv` with the URL it came from, the access date and a confidence level
({{SOURCES}} source rows: {{CONFIDENCE}}). Values that had to be computed (for example a dense rate as the
vendor-stated sparse rate ÷ 2, or a per-package value from a board total) are marked `DERIVED` in the source
note, with the arithmetic.

The dataset was built for the paper *Is Huang's Law Moore's Law? Decomposing a Decade of AI Accelerator
Performance Growth, 2012–2026* ([PDF](https://github.com/thanatchon36/chipledger/blob/main/paper/chipledger.pdf)),
which splits the growth of headline throughput into transistor density, die area, clock, operations per
transistor per cycle and the gain from narrower formats. Code: <https://github.com/thanatchon36/chipledger>;
archived on Zenodo: [10.5281/zenodo.23763729](https://doi.org/10.5281/zenodo.23763729).

*Independent personal research. Public data only. Does not represent the views of any employer or institution.*

## Files

| path | content |
|---|---|
| `data/accelerators.csv` | one row per product: a distinct silicon configuration; memory, power or form-factor variants are separate rows linked by `variant_of` to the primary (highest-TDP module) row |
| `data/sources.csv` | one row per sourced value: `product`, `field`, `value`, `url`, `access_date`, `confidence` (high, medium, low), `note` |
| `results/derived.csv` | the same products with derived columns (density, reference rate, specialization, precision multiplier, ratios) and the residuals of the three accounting identities (≤ 10⁻⁹) |
| `data/mlperf.csv` | per-accelerator MLPerf Training and Inference results used for the peak-against-measured comparison, with the result-repository URL and how each value was computed |
| `data/nodes.csv`, `data/node_sources.csv` | volume-production year of each process node, with sources |
| `data/conflicts.md` | values on which sources disagreed, the alternatives and the choice made |
| `data/coverage.md` | which products lack which fields of the decomposition |
| `configs/seed.yaml` | the frozen seed list the search started from |
| `SHA256SUMS` | checksums of every file above |

## Conventions

- **Rates** are vendor-published peak rates in TFLOP/s or TOPS, counting two operations per multiply–accumulate,
  per package. The headline rate used in the paper is the largest dense rate in any format; sparsity is kept in
  separate `_sparse` columns. These are datasheet peaks, not measured throughput.
- **Die area** is the sum over compute dies (`die_area_compute_total_mm2`) and over all dies including I/O dies
  (`die_area_total_mm2`). Wafer-scale parts are flagged (`wafer_scale`).
- **Confidence**: `high` is a vendor document or vendor-authored paper; `medium` is Epoch AI's hardware database,
  an archived copy of a vendor page, or a verbatim copy of a vendor press release whose original is gone, used
  where no live vendor document gives the value; `low` is press coverage of a vendor announcement (four announce
  dates and one transistor count).
- **Empty means unpublished.** Die area is not published for Blackwell, Rubin, AMD MI100 onward, any TPU after
  v3 and several other recent products, and boost clock not for Blackwell or Rubin; no value was imputed. No
  vendor states launch prices for these products, so the price columns are empty.

## Method and validation

Pre-registered (`PREREGISTRATION.md`, tag `prereg-v1`); deviations in `DEVIATIONS.md`. `chipledger validate`
checks types, dates, units and internal consistency, and that every value in `accelerators.csv` equals its row in
`sources.csv`. Values were cross-checked against Epoch AI's machine learning hardware database where both exist.

## Licence

CC BY 4.0. Specifications are facts transcribed from the cited public documents, which remain under their own
terms; the URLs are given for verification.
