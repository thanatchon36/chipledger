# Phase 5 report — release packaging

Done on 2026-10-29, locally. Nothing was pushed, uploaded or published.

## What was prepared

- **README** in the sibling header style (logo, badges, quick links, lead paragraph) with the result, the
  NVIDIA chain figure and the hypothesis table. The web-paper, PDF and dataset links point to the addresses the
  release will create; the DOI badge is added once Zenodo has minted it.
- **Hugging Face dataset**: `docs/dataset-card.md` and `scripts/build_hf_dataset.py` (`make hf`) write
  `dist/hf/` (git-ignored): the dataset, sources, derived table, MLPerf and node series, conflicts, coverage,
  seed list, licence, `SHA256SUMS` and the card with counts filled from the data (79 products, 14 vendors, 1,152
  source rows, about 0.6 MB).
- **Citation metadata**: `CITATION.cff` and `.zenodo.json` at version 0.1.0 (creator "Chongmankhong,
  Thanatchon", no affiliation, MIT).
- **Reproduction**: `make all` runs validate, derive, coverage, analyze, figures, paper, lint and tests in about
  35 seconds with no network. From a fresh clone at `058cbb1` it rebuilds every result, table, figure, the PDF
  and the web page byte for byte (`git status` empty afterwards). The PDF's embedded date now comes from the last
  commit of `paper/paper.md`, which removed the only difference.
- **Web**: `docs/site/index.html` redirects to the paper at `docs/site/paper/`.

## History check

Fourteen commits plus the `prereg-v1` tag, all authored and committed as
`thanatchon36 <10392423+thanatchon36@users.noreply.github.com>`. No planning file (`MISSION`, `PROGRESS`,
notes, working folders) was ever committed; `notes/` and `work/` are git-ignored. No personal e-mail, home-directory
path, key or token appears in any commit. Downloaded documents stay in git-ignored `data/raw/`; the largest
blob is the 0.46 MB PDF.

## Literature, last attempt

Thompson & Spanuth 2021 was tried again (MIT DSpace: HTTP 429; ACM's open-access PDF: 403) and stays uncited.

## Release checklist (the author's steps)

1. Create the public repository `thanatchon36/chipledger` and push `main` and the tag `prereg-v1`.
2. With Zenodo's GitHub integration on, publish the GitHub release `v0.1.0`; read the concept DOI and add it to
   the README badge, `CITATION.cff` (`doi:`) and the paper's availability section, then cut `v0.1.1` (as for
   `cpilens`).
3. `make hf`, then upload `dist/hf/` as the dataset `thanatchon36/chipledger`.
4. Publish `docs/site/` to GitHub Pages so that `https://thanatchon36.github.io/chipledger/paper/` resolves.
5. arXiv is the author's decision.
