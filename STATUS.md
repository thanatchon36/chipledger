# Status

**Phase 5 — release packaging, done locally (2026-10-29).** Ready to publish; the steps are the author's
(`docs/phase-5-report.md`, release checklist). Paper: `paper/chipledger.pdf`; dataset: `data/`; web paper:
`docs/site/paper/`.

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

- Gate 3 (2026-10-29): verdicts accepted as reported; Phase 4 scope as proposed.
- Phase 4 — paper, figures, literature (2026-10-29): figures F1–F7, the paper built with pandoc → Typst, 31
  sources opened and reviewed, Dally's four factors checked against the Hot Chips 2023 slides (they match).
  Report: `docs/phase-4-report.md`.

- Gate 4 (2026-10-29): the author asked for every recommendation to be carried out: the paper keeps 12 pages,
  Phase 5 proceeds.
- Phase 5 — release packaging (2026-10-29): README with results, Hugging Face card and build script, citation
  metadata at 0.1.0, byte-identical rebuild from a clean clone, history check. Report: `docs/phase-5-report.md`.
- Revision (2026-10-29, after release): at the author's request the seven figures were redrawn in the house
  style at text width and the paper was expanded from 12 to 18 pages (background on matrix instructions and
  number formats, a worked example of the identity, the hypotheses listed in the method, three more tables,
  a fuller discussion); figures and tables now float in the Typst template. No number changed.

## Next

- The author's publishing steps: GitHub repository, Zenodo release and DOI, Hugging Face dataset, Pages.

## Open issues

- TechPowerUp returns HTTP 403 to every fetcher available here; WikiChip refuses connections.
- Die area is unpublished for Blackwell, Rubin, MI100 onward, every TPU after v3, and every AWS, Huawei and Meta
  part after MTIA v2; boost clock is unpublished for Blackwell and Rubin, so every NVIDIA chain ends at H100.
- Three requested references could not be opened and are not cited (Hennessy & Patterson 2019, Thompson &
  Spanuth 2021, Wulf & McKee 1995); Thompson & Spanuth is open access and worth one more try after release.
