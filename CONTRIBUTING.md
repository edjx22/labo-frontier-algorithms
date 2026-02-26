# Contributing

Thanks for contributing to `labo-frontier-algorithms`.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

## Workflow

1. Create a feature branch.
2. Implement changes with tests.
3. Run checks locally:

```bash
ruff check .
mypy labo_frontier_algorithms
pytest
```

4. Open a pull request with a clear summary and reproducibility notes.

## Coding guidelines

- Keep algorithms deterministic by default (fixed seeds where appropriate).
- Avoid external datasets in baseline demos unless explicitly documented.
- Add docstrings and type hints for all public functions.
