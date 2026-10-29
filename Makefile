# chipledger pipeline. `make all` rebuilds everything from the committed dataset; stages not built yet say so.
.PHONY: all validate derive coverage analyze figures paper check lint test

all: validate derive coverage analyze figures paper check

# the hand-curated dataset: columns, types, dates, provenance, consistency
validate:
	uv run chipledger validate

# derived columns and the identity residuals -> results/derived.csv
derive:
	uv run chipledger derive

# which products lack which decomposition fields -> data/coverage.md
coverage:
	uv run chipledger coverage

analyze:
	uv run chipledger analyze

figures:
	uv run chipledger figures

# fill paper/paper.md from results/numbers.json, build the PDF and the web page (needs pandoc and typst)
paper:
	uv run chipledger paper

check: lint test

lint:
	uv run ruff check . && uv run ruff format --check . && uv run mypy

test:
	uv run pytest --cov=chipledger --cov-fail-under=80
