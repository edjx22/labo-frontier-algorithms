# SSL Demo Guide (GCC-PHAT)

This guide explains what the SSL demo does and how to interpret the generated artifacts.

## What algorithm is used?

The demo uses **GCC-PHAT** (Generalized Cross-Correlation with Phase Transform) to estimate **time difference of arrival (TDOA)** between two microphones.

In simple terms:

1. Compute cross-correlation between the two microphone signals in the frequency domain.
2. Apply PHAT weighting so phase is emphasized and magnitude effects are reduced.
3. Find the lag (delay) where the weighted correlation peaks.
4. Convert delay to arrival angle using microphone spacing and speed of sound.

Why PHAT helps: it often improves robustness when signal amplitudes differ or reverberation/noise is present.

---

## Run the demo

```bash
python -m labo_frontier_algorithms run_ssl_demo --outdir out
```

Generated files:

- `out/waveforms.png`
- `out/xcorr.png`
- `out/result.json`

---

## How to read the plots

### 1) `waveforms.png`
- Shows the two simulated microphone signals.
- One channel is slightly time-shifted relative to the other.
- The visible shift corresponds to source direction in this synthetic setup.

### 2) `xcorr.png`
- Shows the GCC-PHAT correlation curve versus lag.
- The **highest peak** indicates the estimated inter-microphone delay.
- Peak sign indicates which channel leads/lags.

---

## Usage example (copy-paste)

```bash
python -m labo_frontier_algorithms run_ssl_demo --outdir out
python -m json.tool out/result.json
```

Example output:

```json
{
  "abs_error_deg": 0.0,
  "est_angle_deg": 30.0,
  "est_delay": 0.00011607142857142857,
  "true_angle_deg": 30.0,
  "true_delay": 0.00011661807580174927
}
```

Interpretation:
- `true_angle_deg`: ground-truth angle used to generate synthetic data.
- `est_angle_deg`: angle estimated from GCC-PHAT peak delay.
- `abs_error_deg`: absolute angular estimation error.

---

## Notes

- This demo is deterministic (fixed seed and synthetic signal generation).
- It is intended as a baseline for learning and reproducible experiments.
- For real-room recordings, multipath and noise can widen/shift peaks and increase error.
