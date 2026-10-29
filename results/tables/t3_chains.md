# Estimator (a): chain-linked decomposition

## NVIDIA, identity A

| step | years | Δlog2 P | Δlog2 density N/A | Δlog2 area A | Δlog2 clock f | Δlog2 specialization R/(N f) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|---|
| K20X → M40 | 3.00 | 0.78 | 0.05 | 0.13 | 0.61 | 0.01 | 0.00 |
| M40 → P100 SXM2 | 0.40 | 1.64 | 0.91 | 0.02 | 0.41 | 0.30 | 0.00 |
| P100 SXM2 → V100 SXM2 16GB | 1.09 | 2.56 | 0.05 | 0.42 | 0.05 | 2.05 | 0.00 |
| V100 SXM2 16GB → A100 SXM4 40GB | 3.01 | 3.32 | 1.34 | 0.02 | -0.12 | 0.08 | 2.00 |
| A100 SXM4 40GB → H100 SXM5 80GB | 1.85 | 0.67 | 0.58 | -0.02 | 0.49 | 0.61 | -1.00 |
| **cumulative K20X → H100 SXM5 80GB** | 9.36 | 8.97 | 2.93 | 0.56 | 1.44 | 3.04 | 1.00 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.327 | 0.063 | 0.160 | 0.339 | 0.111 |

## NVIDIA, identity A′

| step | years | Δlog2 P | Δlog2 transistors N | Δlog2 clock f | Δlog2 specialization R/(N f) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|
| K20X → M40 | 3.00 | 0.78 | 0.17 | 0.61 | 0.01 | 0.00 |
| M40 → P100 SXM2 | 0.40 | 1.64 | 0.94 | 0.41 | 0.30 | 0.00 |
| P100 SXM2 → V100 SXM2 16GB | 1.09 | 2.56 | 0.46 | 0.05 | 2.05 | 0.00 |
| V100 SXM2 16GB → A100 SXM4 40GB | 3.01 | 3.32 | 1.36 | -0.12 | 0.08 | 2.00 |
| A100 SXM4 40GB → H100 SXM5 80GB | 1.85 | 0.67 | 0.56 | 0.49 | 0.61 | -1.00 |
| **cumulative K20X → H100 SXM5 80GB** | 9.36 | 8.97 | 3.49 | 1.44 | 3.04 | 1.00 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.390 | 0.160 | 0.339 | 0.111 |

## NVIDIA, clock-free identity

| step | years | Δlog2 P | Δlog2 density N/A | Δlog2 area A | Δlog2 specialization R/N (clock-free) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|
| K20X → M40 | 3.00 | 0.78 | 0.05 | 0.13 | 0.61 | 0.00 |
| M40 → P100 SXM2 | 0.40 | 1.64 | 0.91 | 0.02 | 0.70 | 0.00 |
| P100 SXM2 → V100 SXM2 16GB | 1.09 | 2.56 | 0.05 | 0.42 | 2.10 | 0.00 |
| V100 SXM2 16GB → A100 SXM4 40GB | 3.01 | 3.32 | 1.34 | 0.02 | -0.04 | 2.00 |
| A100 SXM4 40GB → H100 SXM5 80GB | 1.85 | 0.67 | 0.58 | -0.02 | 1.10 | -1.00 |
| **cumulative K20X → H100 SXM5 80GB** | 9.36 | 8.97 | 2.93 | 0.56 | 4.47 | 1.00 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.327 | 0.063 | 0.499 | 0.111 |

## AMD, identity A′

| step | years | Δlog2 P | Δlog2 transistors N | Δlog2 clock f | Δlog2 specialization R/(N f) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|
| MI60 → MI100 | 2.03 | 1.65 | 0.96 | -0.26 | 1.95 | -1.00 |
| MI100 → MI250X | 0.98 | 1.05 | 1.18 | 0.18 | -0.31 | 0.00 |
| MI250X → MI325X | 2.57 | 2.77 | 1.40 | 0.30 | 0.07 | 1.00 |
| MI325X → MI355X | 1.03 | 1.95 | 0.27 | 0.19 | 0.47 | 1.01 |
| **cumulative MI60 → MI355X** | 6.60 | 7.42 | 3.81 | 0.42 | 2.18 | 1.01 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.513 | 0.056 | 0.294 | 0.137 |

## AMD, identity A′, MI300X as the primary variant

| step | years | Δlog2 P | Δlog2 transistors N | Δlog2 clock f | Δlog2 specialization R/(N f) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|
| MI60 → MI100 | 2.03 | 1.65 | 0.96 | -0.26 | 1.95 | -1.00 |
| MI100 → MI250X | 0.98 | 1.05 | 1.18 | 0.18 | -0.31 | 0.00 |
| MI250X → MI300X | 2.08 | 2.77 | 1.40 | 0.30 | 0.07 | 1.00 |
| MI300X → MI355X | 1.52 | 1.95 | 0.27 | 0.19 | 0.47 | 1.01 |
| **cumulative MI60 → MI355X** | 6.60 | 7.42 | 3.81 | 0.42 | 2.18 | 1.01 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.513 | 0.056 | 0.294 | 0.137 |

## AMD, clock-free identity

| step | years | Δlog2 P | Δlog2 density N/A | Δlog2 area A | Δlog2 specialization R/N (clock-free) | Δlog2 precision P/R |
|---|---|---|---|---|---|---|
| MI25 → MI60 | 1.38 | 1.26 | 0.66 | -0.58 | 0.18 | 1.00 |
| **cumulative MI25 → MI60** | 1.38 | 1.26 | 0.66 | -0.58 | 0.18 | 1.00 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.520 | -0.458 | 0.145 | 0.792 |

## NVIDIA, identity B (P = P/W · W)

| step | years | Δlog2 P | Δlog2 P/W | Δlog2 power W |
|---|---|---|---|---|
| K20X → M40 | 3.00 | 0.78 | 0.69 | 0.09 |
| M40 → P100 SXM2 | 0.40 | 1.64 | 1.38 | 0.26 |
| P100 SXM2 → V100 SXM2 16GB | 1.09 | 2.56 | 2.56 | 0.00 |
| V100 SXM2 16GB → A100 SXM4 40GB | 3.01 | 3.32 | 2.90 | 0.42 |
| A100 SXM4 40GB → H100 SXM5 80GB | 1.85 | 0.67 | -0.14 | 0.81 |
| H100 SXM5 80GB → B200 | 1.99 | 2.34 | 1.56 | 0.78 |
| B200 → B300 | 1.00 | 0.58 | 0.36 | 0.22 |
| **cumulative K20X → B300** | 12.35 | 11.89 | 9.32 | 2.57 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.783 | 0.217 |

## AMD, identity B

| step | years | Δlog2 P | Δlog2 P/W | Δlog2 power W |
|---|---|---|---|---|
| MI25 → MI60 | 1.38 | 1.26 | 1.26 | 0.00 |
| MI60 → MI100 | 2.03 | 1.65 | 1.65 | 0.00 |
| MI100 → MI250X | 0.98 | 1.05 | 0.15 | 0.90 |
| MI250X → MI325X | 2.57 | 2.77 | 1.93 | 0.84 |
| MI325X → MI355X | 1.03 | 1.95 | 1.46 | 0.49 |
| **cumulative MI25 → MI355X** | 7.98 | 8.68 | 6.46 | 2.22 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.744 | 0.256 |

## NVIDIA, identity C (P = P/A · A)

| step | years | Δlog2 P | Δlog2 P/A | Δlog2 area A |
|---|---|---|---|---|
| K20X → M40 | 3.00 | 0.78 | 0.66 | 0.13 |
| M40 → P100 SXM2 | 0.40 | 1.64 | 1.62 | 0.02 |
| P100 SXM2 → V100 SXM2 16GB | 1.09 | 2.56 | 2.14 | 0.42 |
| V100 SXM2 16GB → A100 SXM4 40GB | 3.01 | 3.32 | 3.30 | 0.02 |
| A100 SXM4 40GB → H100 SXM5 80GB | 1.85 | 0.67 | 0.69 | -0.02 |
| **cumulative K20X → H100 SXM5 80GB** | 9.36 | 8.97 | 8.41 | 0.56 |
| **share of cumulative Δlog2 P** |  | 1.000 | 0.937 | 0.063 |
