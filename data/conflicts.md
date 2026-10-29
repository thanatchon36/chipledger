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

| K40 | fp32 | 5.04 at boost clock (Pascal whitepaper K40 column) | 4.29 at base clock (NVIDIA press release) | clock convention |
| K80 | fp32 | 8.74 at boost (NVIDIA press release) | 5.6 at base clock (K80 datasheet) | board total for two GK210 GPUs |
| T4 | mem_bandwidth_gbs | 320 (Turing whitepaper) | 300 (T4 datasheet) |  |
| T4 | tdp_w | 70 (whitepaper, product page) | 75 (press release) |  |
| B100 | fp64 | HGX B100 April 2024 snapshot, 240 TF / 8 | March 2024 snapshot, 30 TF / 8 (web.archive.org copies of the HGX page) | NVIDIA revised the page |
| B200 | mem_capacity_gb | 192 (Blackwell Ultra blog) | 186 ([Blackwell datasheet](https://dam-cdn.nvd.orangelogic.com/AssetLink/y441155802qub41q118b2852i557jem5.pdf)); 180 (HGX B200) |  |
| B300 | fp32 | 83.3 (GB300 NVL72 / 72) | 80 ([Blackwell Ultra datasheet](https://dam-cdn.nvd.orangelogic.com/AssetLink/1k0p832eq8r5ca0u5383ie5o4tp3bst1.pdf)); 75 (HGX B300 / 8) | derived per-GPU values |
| B300 | mem_capacity_gb | 288 (Blackwell Ultra blog) | 279 (Blackwell Ultra datasheet) |  |
| B300 | int8_tensor_sparse | 333.3 (GB300 NVL72 / 72) | 330 (Blackwell Ultra datasheet); 375 (HGX B300 / 8) |  |
| Rubin | mem_bandwidth_gbs | 19200 (current product page and datasheet) | 22 TB/s ([January 2026 press release](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer)) | NVIDIA revised the figure |
| Rubin | chip_to_chip_bandwidth_gbs | 3000 (current product page) | 3.6 TB/s (January 2026 press release) |  |
| MI355X | fp16_tensor | 2500 (product page) | 2516.6 ([MI355X brochure](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/product-briefs/amd-instinct-mi355x-gpu-brochure.pdf)); MI350X row uses the brochure's precise values | rounding; MI355X and MI350X rows use different AMD documents |
| MI60 | fp32 | 14.7 (AMD support page) | 14.8 ([AMD press release, Nov 2018](https://ir.amd.com/news-events/press-releases/detail/859/amd-unveils-worlds-first-7nm-datacenter-gpus----powering-the-next-era-of-artificial-intelligence-cloud-computing-and-high-performance-computing-hpc)) |  |
| MI50 | fp16 | 26.5 at 1725 MHz (AMD support page) | 26.8 (same press release) |  |
| Gaudi | tdp_w | 300 ([Hot Chips 2019](https://old.hotchips.org/hc31/HC31_1.14_HabanaLabs.Eitan_Medina.v9.pdf)) | 400 ([Hot Chips 2024](https://hc2024.hotchips.org/assets/program/conference/day1/60_HC2024.Intel.RomanKaplan.Gaudi3-0826.pdf)) |  |
| Gaudi 2 | mem_bandwidth_gbs | 2460 (Gaudi 3 paper, Hot Chips 2024) | 2450 ([Gaudi 2 whitepaper](https://habana.ai/wp-content/uploads/pdf/2022/gaudi2-whitepaper.pdf)); 2400 (datasheet) |  |
| Gaudi 3 | bf16_tensor | 1678 ([Gaudi 3 paper, July 2025](https://cdrdv2.intel.com/v1/dl/getContent/817486?fileName=gaudi-3-ai-accelerator-white-paper.pdf)) | 1835 (Hot Chips 2024) | Intel revised the rate |
| Gaudi 3 | tdp_w | 900 (Gaudi 3 paper) | 900 air / 1200 liquid (Hot Chips 2024) | highest-TDP rule would give 1200; revisit |
| Trainium | bf16_tensor | 190 ([Trainium page](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium.html)) | 191 (Trainium2 page comparison table) | rounding |
| Trainium3 | mem_bandwidth_gbs | 4900 (Neuron docs) | 4.7 TB/s ([NKI guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html)) |  |
| Ascend 910 | tdp_w | 310 ([MindSpore news](https://www.mindspore.cn/news/en/172)) | 350 ([Hot Chips 2019 slide 33](https://old.hotchips.org/hc31/HC31_1.11_Huawei.Davinci.HengLiao_v4.0.pdf)) |  |
| Ascend 910C | fp16_tensor | 750 (Atlas 800T A3: 6.0 PF / 8) | 800 (Atlas 900 A3 SuperPoD 307.2 / 384); 781.25 (Huawei Connect 2025 keynote 300 PF / 384) | system figures divided by chip count |
| Ascend 950DT | fp8_tensor | 973 (Huawei 950 whitepaper, top bin, Cube) | 1 PFLOPS (keynote); 804 (Atlas 650E server, lowest bin) | speed bins |
| Maia 100 | tdp_w | 700 'Design to TDP' ([Hot Chips 2024](https://hc2024.hotchips.org/assets/program/conference/day2/81_HC2024.Microsoft.Xu.Ramakrishnan.final.v2.pdf)) | 500 'Provision TDP' (same slide; Epoch AI) | highest-TDP rule |
| MTIA v1 | mem_capacity_gb | 64 (2024 blog table) | 'can scale up to 128 GB' (2023 blog) |  |
| MTIA 400 | mem_bandwidth_gbs | 9200 (Meta blog table) | 9.4 TB/s (Epoch AI, citing Meta's Hot Chips 2026 talk; slides not accessible) |  |
| SN40L | bf16_tensor | 638 ([arXiv 2405.07518](https://arxiv.org/abs/2405.07518), Hot Chips 2024) | 640 (2026 product page) | rounding |
| Blackhole p150 | fp8_tensor | 774 (archived 2025 docs) | 664 BLOCKFP8 (current docs, 120 Tensix); 745 (Hot Chips 2024, chip level) | Tenstorrent revised the specification |
| TPU v3 | tdp_w | 450 ([ISCA 2021](https://www.cs.cmu.edu/~18742/papers/Jouppi2021.pdf)) | 'N.A.' ([ISCA 2023](https://arxiv.org/pdf/2304.01433v3)) |  |
| TPU v5e | mem_bandwidth_gbs | 819 GBps (Spanish docs) | 800 GiBps (English docs) | units |
| GroqChip 1 | int8_tensor | 750 at 900 MHz (GroqChip product brief v1.5) | 820 at 1 GHz ([ISCA 2020](https://groq.com/wp-content/uploads/2024/02/2020-Isca.pdf)); 1 POPS (2019 press release) | clock |
| GC200 | transistors_b | 59.4 (Graphcore blog) | 59,334,610,787 active ([Hot Chips 33](https://hc33.hotchips.org/assets/program/conference/day2/HC2021.Graphcore.SimonKnowles.v04.pdf)) | rounding |
| Cloud AI 100 | mem_bandwidth_gbs | 137 (product page) | 136 (Hot Chips 33) | rounding |

Dates in Epoch AI's database are release dates; this dataset uses announce dates (§2), so date differences with
Epoch AI are not listed. Values marked “pending Gate 1 decision” are discussed in `docs/phase-1-report.md`.
