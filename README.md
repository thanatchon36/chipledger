<p align="center"><img src="docs/assets/logo.svg" alt="chipledger logo" width="120"></p>

<h1 align="center">chipledger</h1>

[![CI](https://github.com/thanatchon36/chipledger/actions/workflows/ci.yml/badge.svg)](https://github.com/thanatchon36/chipledger/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Data](https://img.shields.io/badge/data-CC--BY--4.0-blue)](LICENSE-DATA)
[![Status](https://img.shields.io/badge/status-phase%200-lightgrey)](STATUS.md)
[![Pre-registered](https://img.shields.io/badge/pre--registered-prereg--v1-blue)](PREREGISTRATION.md)

🧾 **[Pre-registration](PREREGISTRATION.md)** · 🔀 **[Deviations](DEVIATIONS.md)** · 🔁 **[Reproduce](REPRODUCE.md)** ·
📋 **[Status](STATUS.md)** · 🗒️ **[Decisions](docs/decisions.md)**

**Is Huang's Law Moore's Law? Decomposing a Decade of AI Accelerator Performance Growth, 2012–2026.** The peak
throughput of data-centre AI accelerators has grown far faster than Moore's law. `chipledger` asks how much of
that growth is Moore's law at all. For every product with public silicon data it computes an exact accounting
identity,

    log2 P = log2 density + log2 area + log2 clock + log2 specialization + log2 precision multiplier,

which splits headline throughput `P` into transistor density (Moore's law proper), total die area including
multi-die packaging, clock, reference-precision operations per transistor per cycle (matrix units), and the gain
from arithmetic narrower than 16 bits. The dataset carries a source URL, an access date and a confidence level for
every value; the design is pre-registered.

> Independent personal research. Public data only. Does not represent the views of any employer or institution.

## Result

Not yet. Phase 0 built the schema, the validation rules and the identity code; the dataset is empty and the
pre-registration is a draft awaiting freeze. See [`STATUS.md`](STATUS.md).

## What is here

| Part | Where | What it does |
|---|---|---|
| Pre-registration | `PREREGISTRATION.md` | Questions, definitions, sample rule, identities, estimators, decision rules |
| Dataset | `data/accelerators.csv`, `data/sources.csv` | One row per product; one row per sourced value |
| Seed list | `configs/seed.yaml` | The products the search starts from, by vendor |
| Schema and validation | `src/chipledger/schema.py` | Columns, types, provenance and consistency rules |
| Identity | `src/chipledger/identity.py` | Derived columns and the three identity residuals |
| CLI | `src/chipledger/cli.py` | `validate`, `derive`, `coverage`; `analyze`, `figures`, `paper` from Phase 3 |
| Tests | `tests/` | Every validation rule; the identity holds to 10⁻⁹ |

## Reproduce

```bash
uv sync
make check              # ruff, mypy, pytest
make validate derive    # the dataset and results/derived.csv
```

See [`REPRODUCE.md`](REPRODUCE.md).

## Citation

See [`CITATION.cff`](CITATION.cff). The paper will be the preferred citation once it is released.

## License

Code: [MIT](LICENSE). Data: [CC BY 4.0](LICENSE-DATA). Vendored fonts (Libertinus) are under the SIL OFL and
the Typst templates under pandoc's BSD licence; see `paper/fonts/OFL.txt` and `paper/templates/`.
