# Status

**Phase 2 — full dataset, done; waiting at Gate 2 (2026-10-29).** 79 products from 14 vendors, 1,150 source
rows; the five-term chain reaches K20X → H100, the A′ chain MI60 → MI355X. Report: `docs/phase-2-report.md`.

## Done

- Phase 0 — setup (2026-10-29): conventions read from the sibling repositories (`cpilens`, `sandbank`,
  `coauthored`); skeleton; dataset schema with validation rules; identity code with tests; seed list;
  pre-registration drafted, not frozen. Report: `docs/phase-0-report.md`. No data collected, no source fetched,
  no external service used.
- Phase 1 — feasibility (2026-10-29): 16 products (NVIDIA 8, AMD 4, Google 4), 288 source rows, all from vendor
  documents; chain and trend estimators with tests; rough F1 and F2. Report: `docs/phase-1-report.md`.
- Gate 1 (2026-10-29): dense from sparse where the vendor states the rule, Epoch AI as a medium-confidence
  fallback, identity A′ for products without die area (`DEVIATIONS.md` #1–3).
- Phase 2 — full dataset (2026-10-29): 79 products, 1,150 source rows, 56 conflicts, 22 process nodes; Epoch AI
  cross-check 138/158 within 2 %. Report: `docs/phase-2-report.md`.

## Next

- Gate 2: the author decides on the Kepler flagship and per-package accounting, the highest-TDP primary
  variant, a vector INT8 column, and the use of the node series (`docs/phase-2-report.md`, last section).
- Phase 3 — analysis. Phase 4 — paper and figures. Phase 5 — release
  packaging. Publishing steps are the author's.

## Open issues

- TechPowerUp returns HTTP 403 to every fetcher available here; WikiChip refuses connections.
- Die area is unpublished for Blackwell, Rubin, MI100 onward, every TPU after v3, and every AWS, Huawei and Meta
  part after MTIA v2.
