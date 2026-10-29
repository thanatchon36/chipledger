# Hypotheses H1–H7

|  | rule (PREREGISTRATION §5) | estimate | verdict |
|---|---|---|---|
| H1 | doubling of P ≤ 1.5 yr and 95% CI upper bound < 2.0 yr | 0.83 yr, CI [0.62, 1.13], n = 9 | supported |
| H2 | (a) density doubling ≥ 2.5 yr; (b) density share of NVIDIA chain < 1/3 | (a) 2.76 yr; (b) 0.327 (K20X → H100 SXM5 80GB) | supported |
| H3 | (a) chain: spec + precision share > density share; (b) regression: spec + precision − density slope > 0, CI excludes 0 | (a) 0.450 vs 0.327; (b) 0.090 doublings/yr, CI [-0.103, 0.307] | falsified ((a) passes, (b) fails) |
| H4 | NVIDIA chain: mean Δlog2 area and TDP larger on steps ending after 2020 | area -0.02 vs 0.15; TDP 0.81 vs 0.19 (late steps: A100 SXM4 40GB → H100 SXM5 80GB) | not supported |
| H5 | slope of P − slope of bandwidth > 0, CI excludes 0 (flagship decomposition sample) | 0.709 doublings/yr, CI [0.395, 1.072], n = 7 | supported |
| H6 | MLPerf per-accelerator slope < headline slope on every benchmark | no MLPerf data collected | not assessed |
| H7 | K20X → H100: growth of N·f ≥ 10× | 30.5× | supported |
