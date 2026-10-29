# Conflicts between sources

When two sources disagree about a value, the vendor's primary document wins (PREREGISTRATION.md §3) and the
alternatives are listed here with their URLs, so that a reader can judge the choice.

| product | field | value used (source) | alternative (source) | note |
|---|---|---|---|---|
| K20X | announce_date | 2012-11-11 ([source](https://nvidianews.nvidia.com/news/nvidia-unveils-world-s-fastest-most-efficient-accelerators-powers-world-s-no-1-supercomputer-6622729)) — NVIDIA press release, November 11, 2012 | 2012-11-12 (HPCwire coverage; Epoch AI) |  |
| M40 | fp32 | 6.8 ([source](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)) — Volta whitepaper table | 7 TFLOPS (M40 datasheet, rounded); 6844 GFLOPS (Inside Pascal blog); URL to be added in Phase 2 | same quantity, different rounding |
| P100 SXM2 | mem_bandwidth_gbs | 732 ([source](https://images.nvidia.com/content/tesla/pdf/nvidia-tesla-p100-datasheet.pdf)) — datasheet and Inside Pascal table | 720 GB/s (NVIDIA press release, April 2016); URL to be added in Phase 2 |  |
| V100 SXM2 16GB | transistors_b | 21.1 ([source](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)) — Volta whitepaper | 21 billion (NVIDIA press release); URL to be added in Phase 2 | rounding |
| H100 SXM5 80GB | mem_bandwidth_gbs | 3350 ([source](https://www.nvidia.com/en-us/data-center/h100/)) — nvidia.com product page | 3 TB/s (NVIDIA press release, March 2022, preliminary); URL to be added in Phase 2 |  |
| H100 SXM5 80GB | fp16_tensor | (empty: nvidia.com gives 1979 with sparsity only) | 1000 dense / 2000 sparse, preliminary ([Hopper in-depth blog](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/)); 989.5 dense (Epoch AI) | dense rate pending Gate 1 decision |
| H100 SXM5 80GB | boost_clock_mhz | (empty: NVIDIA says 'Not finalized') | 1980 MHz (Epoch AI, citing TechPowerUp, which returns HTTP 403 to every fetcher used) | pending Gate 1 decision |
| B200 | tdp_w | 1200 ([source](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/)) — Blackwell Ultra technical blog, 1200 W module | 1000 W (HGX B200 page; Epoch AI) | variant choice: highest-TDP module (§2) |
| B200 | mem_capacity_gb | 192 ([source](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/)) — Blackwell Ultra technical blog, 192 GB | 186 GB (GB200 superchip 372 GB / 2); 180 GB (HGX B200); URL to be added in Phase 2 |  |
| B200 | fp32 | 80 ([source](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)) — GB200 superchip column / 2 = 80 | 75 (HGX B200 600 / 8); 62.08 (Epoch AI) | derived per-GPU value |
| B300 | fp4_tensor | 15000 ([source](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/)) — Blackwell Ultra blog, 15 PF dense | 13.5 PF dense (HGX B300 108 / 8); URL to be added in Phase 2 | variant: 1400 W module vs HGX |
| B300 | fp32 | 83.3 ([source](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)) — GB300 NVL72 / 72 = 83.3 | 75 (HGX B300 600 / 8; Epoch AI) | derived per-GPU value |
| MI250X | tdp_w | 560 ([source](https://www.amd.com/en/products/accelerators/instinct/mi200/mi250x.html)) — AMD product page '500W | 560W Peak', 560 recorded | 500 W (same page; Epoch AI) | highest-TDP rule applied to a peak figure; revisit in Phase 2 |
| MI100 | int8_tensor | 184.6 ([source](https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/product-briefs/instinct-mi100-brochure.pdf)) — 184.6 (brochure and CDNA 2 whitepaper) | 92.3 TOPS ([product page](https://www.amd.com/en/products/accelerators/instinct/mi100.html)) | the page row looks copied from BF16 |
| MI355X | fp4_tensor | 10100 ([source](https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html)) — product page | 10 PF ([CDNA 4 whitepaper](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-4-architecture-whitepaper.pdf)) | rounding |
| MI300X | chip_to_chip_bandwidth_gbs | 896 ([source](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-3-white-paper.pdf)) — 896 GB/s Infinity Fabric P2P | 1024 GB/s total incl. PCIe host link (same page) | definition: peer-to-peer only |
| TPU v4 | die_area_compute_total_mm2 | (empty: paper gives '<600 mm2' only) | '< 400' ([Wikipedia](https://en.wikipedia.org/wiki/Tensor_Processing_Unit), citing the same paper) | bound, not a value |
| TPU v5p | chip_to_chip_bandwidth_gbs | 1200 ([source](https://docs.cloud.google.com/tpu/docs/v5p)) — docs, 1200 GBps bidirectional | 4,800 Gbps = 600 GB/s ([Dec 2023 blog](https://cloud.google.com/blog/products/ai-machine-learning/introducing-cloud-tpu-v5p-and-ai-hypercomputer)) | direction convention |
| TPU v5p | mem_capacity_gb | 96 ([source](https://docs.cloud.google.com/tpu/docs/v5p)) — docs text, 96 GiB physical | 95 GiB usable (docs table) |  |
| TPU v5p | fp8_tensor | 459 ([source](https://docs.cloud.google.com/tpu/docs/v5p)) — docs table, 459 | emulated per [Ironwood blog](https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/) | native vs emulated |
| TPU v6e | fp8_tensor | (empty: architecture page lists int8 for v6e) | 918 (TPU7x docs comparison table) |  |
| TPU v6e | ship_date | 2024-12-12 ([source](https://cloud.google.com/blog/products/compute/trillium-tpu-is-ga)) — blog, 2024-12-12 | 2024-12-16 (Cloud TPU release notes) |  |
| TPU v7 | mem_bandwidth_gbs | 7380 ([source](https://docs.cloud.google.com/tpu/docs/tpu7x)) — docs table, 7380 | 7.37 TB/s (April 2025 blog) | rounding |

Dates in Epoch AI's database are release dates; this dataset uses announce dates (§2), so date differences with
Epoch AI are not listed. Values marked “pending Gate 1 decision” are discussed in `docs/phase-1-report.md`.
