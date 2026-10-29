# Status

**Phase 1 — feasibility, done; waiting at Gate 1 (2026-10-29).** 16 products collected with provenance; the
full decomposition reaches only K20X → A100. Report: `docs/phase-1-report.md`.

## Done

- Phase 0 — setup (2026-10-29): conventions read from the sibling repositories (`cpilens`, `sandbank`,
  `coauthored`); skeleton; dataset schema with validation rules; identity code with tests; seed list;
  pre-registration drafted, not frozen. Report: `docs/phase-0-report.md`. No data collected, no source fetched,
  no external service used.
- Phase 1 — feasibility (2026-10-29): 16 products (NVIDIA 8, AMD 4, Google 4), 288 source rows, all from vendor
  documents; chain and trend estimators with tests; rough F1 and F2. Report: `docs/phase-1-report.md`.

## Next

- Gate 1: the author decides on dense-from-sparse values, sources for clock and area beyond vendor documents,
  and products without a published die area (`docs/phase-1-report.md`, last section).
- Phase 2 — full dataset and coverage report. Phase 3 — analysis. Phase 4 — paper and figures. Phase 5 — release
  packaging. Publishing steps are the author's.

## Open issues

- TechPowerUp returns HTTP 403 to every fetcher available here; WikiChip refuses connections.
- Die area is unpublished for Blackwell, all four AMD parts and every TPU (v4 gives only "< 600 mm²").
- H100, B200, B300 lack dense tensor rates in the dataset, so their headline/reference fall back to FP32.
