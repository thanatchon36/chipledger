# Status

**Phase 3 — analysis, done; waiting at Gate 3 (2026-10-29).** H1, H2, H5 and H7 supported, H3 falsified, H4
not supported, H6 (exploratory) supported. Report: `docs/phase-3-report.md`; numbers: `results/numbers.json`; tables:
`results/tables/`.

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
- Gate 2 (2026-10-29): per-package rows (K80, Wormhole n300), K40 as the Kepler flagship, MI325X as the primary
  of the MI300X silicon, a vector INT8 column, node series by year only (`DEVIATIONS.md` #4–8).
- Phase 3 — analysis (2026-10-29): `chipledger analyze` runs estimators (a)–(c), H1–H7, the §6 sensitivities
  and the §7 secondary analyses. Report: `docs/phase-3-report.md`.

## Next

- Gate 3: the author accepts the verdicts as reported and the Phase 4 scope (`docs/phase-3-report.md`, last
  section).
- Phase 4 — paper, figures F1–F7, literature review with every cited document opened. Phase 5 — release
  packaging. Publishing steps are the author's.

## Open issues

- TechPowerUp returns HTTP 403 to every fetcher available here; WikiChip refuses connections.
- Die area is unpublished for Blackwell, Rubin, MI100 onward, every TPU after v3, and every AWS, Huawei and Meta
  part after MTIA v2; boost clock is unpublished for Blackwell and Rubin, so every NVIDIA chain ends at H100.
- NVIDIA's four factors in estimator (c) are as written in the pre-registration; they are checked against
  Dally's Hot Chips 2023 talk in Phase 4.
