# Hypotheses H1–H7

|  | rule (PREREGISTRATION §5) | estimate | verdict |
|---|----------------------------------------|----------------------------------------|---------------------------------|
| H1 | doubling of P ≤ 1.5 yr, CI upper bound < 2.0 yr | 0.83 yr, CI [0.62, 1.13], n = 9 | supported |
| H2 | (a) density doubling ≥ 2.5 yr; (b) density share of the NVIDIA chain < 1/3 | (a) 2.76 yr; (b) 0.327 | supported |
| H3 | (a) chain: spec + precision share > density share; (b) spec + precision − density slope > 0, CI excludes 0 | (a) 0.450 vs 0.327; (b) 0.090 doublings/yr, CI [−0.103, 0.307] | falsified ((a) passes, (b) fails) |
| H4 | NVIDIA chain: area and TDP grow more per step after 2020 | area −0.02 vs 0.15; TDP 0.81 vs 0.19 (1 late step) | not supported |
| H5 | slope of P − slope of bandwidth > 0, CI excludes 0 | 0.709 doublings/yr, CI [0.395, 1.072], n = 7 | supported |
| H6 | MLPerf slope < headline slope on every benchmark | BERT 0.65 vs 0.79; Llama 2 70B inference 0.83 vs 1.01; Llama 2 70B LoRA 0.58 vs 1.01; ResNet-50 0.45 vs 0.85 (NVIDIA, n = 3 each) | supported |
| H7 | K20X → H100: N·f grows ≥ 10× | 30.5× | supported |
