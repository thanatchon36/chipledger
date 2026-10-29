# Sensitivity analyses (PREREGISTRATION §6)

| variant | n | P doubling (yr) [95% CI] | density doubling (yr) | H3b: spec + prec − density (dbl/yr) [95% CI] | chain: density share | chain: spec share | chain: precision share | chain |
|---|---|---|---|---|---|---|---|---|
| primary | 9 | 0.83 [0.62, 1.13] | 2.76 | 0.090 [-0.103, 0.307] | 0.327 | 0.339 | 0.111 | K20X → H100 SXM5 80GB |
| ship date | 9 | not computable (too few rows for a trend: 2) | — | — | — | — | — | — |
| FP32 reference | 7 | 0.88 [0.67, 1.26] | 2.65 | 0.211 [0.030, 0.516] | 0.327 | -0.094 | 0.545 | K20X → H100 SXM5 80GB |
| floating-point headline | 9 | 0.87 [0.64, 1.27] | 2.76 | 0.027 [-0.158, 0.218] | 0.327 | 0.339 | 0.111 | K20X → H100 SXM5 80GB |
| headline with sparsity | 9 | 0.69 [0.47, 1.09] | 2.76 | 0.322 [0.015, 0.633] | 0.294 | 0.305 | 0.201 | K20X → H100 SXM5 80GB |
| area including I/O dies | 9 | 0.83 [0.62, 1.13] | 2.76 | 0.090 [-0.103, 0.307] | 0.327 | 0.339 | 0.111 | K20X → H100 SXM5 80GB |
| clock-free identity | 11 | 0.99 [0.67, 1.38] | 2.79 | 0.076 [-0.119, 0.313] | 0.327 | 0.499 | 0.111 | K20X → H100 SXM5 80GB |
| all products in the sample | 11 | 0.89 [0.68, 1.13] | 3.05 | 0.101 [-0.062, 0.314] | same as primary |  |  |  |
| all products, vendor fixed effects | 11 | 0.91 [0.70, 1.05] | 3.06 | 0.248 [0.103, 0.603] | same as primary |  |  |  |
| NVIDIA only | 6 | 0.85 [0.60, 1.18] | 2.65 | 0.229 [-0.046, 0.597] | same as primary |  |  |  |
| without wafer-scale | 8 | 0.93 [0.74, 1.24] | 2.60 | 0.144 [-0.073, 0.404] | same as primary |  |  |  |
| frontier envelope | 8 | 0.76 [0.58, 0.99] | 3.47 | 0.179 [-0.072, 0.643] | same as primary |  |  |  |
| without AMD | 8 | 0.82 [0.62, 1.09] | 2.76 | 0.092 [-0.135, 0.327] | same as primary |  |  |  |
| without Cerebras | 8 | 0.93 [0.74, 1.24] | 2.60 | 0.144 [-0.073, 0.404] | same as primary |  |  |  |
| without Graphcore | 8 | 0.79 [0.58, 1.02] | 2.83 | 0.127 [-0.077, 0.387] | same as primary |  |  |  |
| without NVIDIA | 3 | 0.39 [0.16, 0.81] | 3.94 | -0.192 [-0.298, 0.109] | same as primary |  |  |  |
| high-confidence values only | 8 | 0.79 [0.57, 1.23] | 2.81 | 0.055 [-0.228, 0.390] | 0.283 | 0.292 | 0.241 | K20X → A100 SXM4 40GB |
| identity A′ (no area) | 15 | 1.03 [0.84, 1.23] | — | — | — | 0.339 | 0.111 | K20X → H100 SXM5 80GB |
