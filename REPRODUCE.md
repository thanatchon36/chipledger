# Reproducing the results

Needs Python ≥ 3.11 and [`uv`](https://docs.astral.sh/uv/). No API key, no paid service, no network beyond
installing packages.

```bash
git clone https://github.com/thanatchon36/chipledger && cd chipledger
uv sync
```

## 1. The dataset and the identity (seconds, no network)

```bash
uv run chipledger validate   # every value typed, dated, sourced and consistent, or the command fails
uv run chipledger derive     # results/derived.csv: every derived column and the identity residuals (≤ 1e-9)
uv run chipledger coverage   # data/coverage.md: products outside the decomposition sample and why
```

## 2. Every table, figure and number (Phase 3 onward)

```bash
uv run chipledger analyze    # results/numbers.json, results/tables/, bootstrap seed 20261029
uv run chipledger figures    # results/figures/*.svg and *.png
```

## 3. The paper (Phase 4 onward)

Needs pandoc ≥ 3.8 and Typst ≥ 0.13 on the `PATH`; fonts are vendored in `paper/fonts/`.

```bash
uv run chipledger paper      # paper/chipledger.pdf and docs/site/paper/index.html
```

Every number in the paper is filled from `results/numbers.json`; a number typed by hand fails the build.

## What is frozen

`PREREGISTRATION.md` and `configs/seed.yaml` are frozen at tag `prereg-v1` once the author approves them. Every
later change to a frozen rule is listed in `DEVIATIONS.md`.
