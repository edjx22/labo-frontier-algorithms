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

The demo writes:

- `out/waveforms.png`
- `out/xcorr.png`
- `out/result.json`

Example `result.json`:

```json
{
  "abs_error_deg": 0.0,
  "est_angle_deg": 30.0,
  "est_delay": 0.00011607142857142857,
  "true_angle_deg": 30.0,
  "true_delay": 0.00011661807580174927
}
```

## Reproducibility notes

- The SSL baseline uses synthetic 2-channel sinusoid mixtures with deterministic random seed.
- No external datasets or model downloads are required.
- Core algorithm is GCC-PHAT for TDOA estimation plus angle reconstruction.
- The demo parameters are fixed in code (`fs=16000`, `duration=0.1 s`, `freq=800 Hz`, `mic_distance=0.08 m`, `angle=30 deg`, `snr=20 dB`, `seed=42`) so repeated runs reproduce the same output structure and near-identical estimates.

## Reproduce the demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
python -m labo_frontier_algorithms run_ssl_demo --outdir out
python -m json.tool out/result.json
```

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

## Demo Output

Synthetic two-microphone example using GCC-PHAT.

### Waveforms
![Waveforms](docs/assets/waveforms.png)

### Cross-correlation
![GCC-PHAT](docs/assets/xcorr.png)

Example result:

```json
{
  "true_angle_deg": 30,
  "est_angle_deg": 31.28,
  "abs_error_deg": 1.28
}

## Roadmap

- Add broadband and chirp-based SSL synthetic benchmarks.
- Add ANC baseline (FxLMS) with deterministic synthetic acoustic paths.
- Add experiment tracking helpers (config snapshots + metric dumps).
- Add richer plots and tabular summaries for baseline comparisons.

## Citation

If this repository helps your work, please cite it using `CITATION.cff`.
