# Deviations from the pre-registration

`PREREGISTRATION.md` was frozen at tag `prereg-v1` on 2026-10-29. Every change or clarification to a frozen
rule, and every product added beyond the seed list, is logged here with date, what changed, why, and its effect
on results.

| # | Date | What | Why | Effect |
|---|---|---|---|---|
| 1 | 2026-10-29 | Dense rates may be taken as sparse ÷ 2 where a vendor document states that rule in writing (NVIDIA GB200/GB300 pages: "Dense is one-half sparse spec shown"); the sentence is quoted in the source note. | NVIDIA lists Hopper and Blackwell tensor rates with sparsity only; without this, H100, B200 and B300 fall back to FP32 as headline or reference (Phase 1 report). Approved by the author at Gate 1. | H100, B200, B300 enter the throughput and efficiency samples with dense tensor rates. No hypothesis changes. |
| 2 | 2026-10-29 | Epoch AI's machine learning hardware database (snapshot 2026-10-29) may supply a value at `medium` confidence when no vendor document or vendor-authored paper gives it; the note names the Epoch row and the source Epoch cites. §3 listed Epoch AI as a cross-check only. | TechPowerUp, the pre-registered fallback for clocks, returns HTTP 403 to every fetcher available; Epoch AI carries the TechPowerUp values. Approved by the author at Gate 1. | Adds values such as H100's boost clock (1,980 MHz). Every Epoch-sourced value is flagged `medium`; a sensitivity drops them. |
| 3 | 2026-10-29 | Identity A′, the transistor-count form `log2 P = log2 N + log2 f + log2 spec + log2 precision`, is computed for products with `N`, `f`, `W` and `R` but no die area; estimator (a) is run on it as an additional chain. Density and area shares (H2b) come from the five-term chain only. | Die area is unpublished for Blackwell, MI300-class and TPU parts (Phase 1 report). `N` is the pre-registered first form of Moore's law (§2), so A′ uses only defined quantities. Approved by the author at Gate 1. | The five-term NVIDIA chain is expected to end at H100 (2022); the A′ chain extends it to the latest product with `N` and `f`. |
