# Phase 0 report — setup

Conventions read from `cpilens`, `sandbank` and `coauthored`; skeleton created; pre-registration drafted (not
frozen). No data collected, no source fetched, no external service used, nothing published.

- Repository: `~/github/chipledger`, local only; git author set to the GitHub noreply identity used by the
  sibling repositories; planning notes git-ignored from the first commit.
- Tooling: uv, Python 3.11/3.12, ruff, mypy (strict), pytest with coverage; pandoc 3.8.3 and Typst 0.15.1 on
  the machine for the paper (Phase 4). Fonts, CSL and Typst templates vendored from `coauthored`.
- Code: `chipledger validate` (columns, types, dates, provenance, consistency), `chipledger derive` (derived
  columns and identity residuals), `chipledger coverage` (products outside the decomposition sample);
  `analyze`, `figures` and `paper` are stubs until Phases 3–4.
- Tests: the identity holds to 10⁻⁹ on synthetic rows and fails loudly when broken; every validation rule;
  typed loading.
- Decisions D1–D9: `docs/decisions.md`.
- Gate 0: the author approves `PREREGISTRATION.md`, then it is tagged `prereg-v1`.
