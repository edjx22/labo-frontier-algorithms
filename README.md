# labo-frontier-algorithms

Reproducible baseline implementations for frontier audio algorithms (SSL, ANC) with experiments.

## Who is this for?

- Researchers
- Students
- Engineers

## Quickstart

```bash
git clone https://github.com/<your-org>/labo-frontier-algorithms.git
cd labo-frontier-algorithms
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

Run CLI help:

```bash
python -m labo_frontier_algorithms --help
```

Run SSL demo:

```bash
python -m labo_frontier_algorithms run_ssl_demo --outdir out
```

The demo writes `out/ssl_demo_gcc_phat.png`.

## Reproducibility notes

- The SSL baseline uses synthetic 2-channel sinusoid mixtures with deterministic random seed.
- No external datasets or model downloads are required.
- Core algorithm is GCC-PHAT for TDOA estimation plus angle reconstruction.

## Project layout

```text
labo_frontier_algorithms/
  signal.py      # synthetic signal generation
  ssl.py         # GCC-PHAT + angle estimate
  demo.py        # plotting and experiment runner
  __main__.py    # CLI entrypoint
experiments/
  run_ssl_demo.py
tests/
  test_ssl.py
  test_cli.py
```

## Development

```bash
ruff check .
mypy labo_frontier_algorithms
pytest
```

CI runs lint + type check + tests on Python 3.10/3.11/3.12.

## Roadmap

- Add broadband and chirp-based SSL synthetic benchmarks.
- Add ANC baseline (FxLMS) with deterministic synthetic acoustic paths.
- Add experiment tracking helpers (config snapshots + metric dumps).
- Add richer plots and tabular summaries for baseline comparisons.

## Citation

If this repository helps your work, please cite it using `CITATION.cff`.
