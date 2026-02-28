"""Demo runner for SSL baseline."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "labo_frontier_algorithms-mpl"),
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from .signal import generate_two_mic_sine
from .ssl import estimate_angle_from_tdoa, gcc_phat, gcc_phat_lags

FloatArray = NDArray[np.float64]
INTERP = 16


def _save_waveforms_plot(x1: FloatArray, x2: FloatArray, fs: int, fig_path: Path) -> None:
    time_ms = np.arange(x1.shape[0], dtype=np.float64) / float(fs) * 1000.0

    fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
    ax.plot(time_ms, x1, label="mic1", linewidth=1.0)
    ax.plot(time_ms, x2, label="mic2", linewidth=1.0, alpha=0.8)
    ax.set_title("Synthetic Two-Mic Waveforms")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    fig.savefig(fig_path, dpi=140)
    plt.close(fig)


def _save_xcorr_plot(
    cc: FloatArray,
    lags_s: FloatArray,
    est_tdoa: float,
    true_tdoa: float,
    fig_path: Path,
) -> None:
    peak_idx = int(np.argmax(np.abs(cc)))
    peak_lag_ms = float(lags_s[peak_idx] * 1000.0)
    peak_value = float(np.abs(cc[peak_idx]))

    fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
    ax.plot(lags_s * 1000.0, np.abs(cc), color="tab:orange", linewidth=1.2)
    ax.axvline(est_tdoa * 1000.0, color="tab:red", linestyle="--", label="Estimated delay")
    ax.axvline(true_tdoa * 1000.0, color="tab:green", linestyle=":", label="True delay")
    ax.scatter([peak_lag_ms], [peak_value], color="tab:red", s=36, zorder=3, label="Peak")
    ax.annotate(
        f"peak={peak_lag_ms:.3f} ms",
        xy=(peak_lag_ms, peak_value),
        xytext=(8, 8),
        textcoords="offset points",
    )
    ax.set_title("GCC-PHAT Cross-Correlation")
    ax.set_xlabel("Lag (ms)")
    ax.set_ylabel("|CC|")
    ax.legend()
    fig.savefig(fig_path, dpi=140)
    plt.close(fig)


def run_ssl_demo(outdir: str | Path = "out") -> Path:
    """Run a deterministic synthetic GCC-PHAT demo and save outputs."""
    fs = 16000
    duration_s = 0.1
    freq_hz = 800.0
    mic_distance_m = 0.08
    true_angle_deg = 30.0
    snr_db = 20.0

    x1, x2, true_tdoa = generate_two_mic_sine(
        fs=fs,
        duration_s=duration_s,
        freq_hz=freq_hz,
        mic_distance_m=mic_distance_m,
        angle_deg=true_angle_deg,
        snr_db=snr_db,
        seed=42,
    )

    max_tau = mic_distance_m / 343.0
    est_tdoa, cc = gcc_phat(x2, x1, fs=fs, max_tau=max_tau, interp=INTERP)
    est_angle_deg = estimate_angle_from_tdoa(est_tdoa, mic_distance_m)
    abs_error_deg = abs(est_angle_deg - true_angle_deg)
    lags_s = gcc_phat_lags(cc, fs=fs, interp=INTERP)

    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    waveforms_path = outdir_path / "waveforms.png"
    xcorr_path = outdir_path / "xcorr.png"
    result_path = outdir_path / "result.json"

    _save_waveforms_plot(x1, x2, fs=fs, fig_path=waveforms_path)
    _save_xcorr_plot(cc, lags_s, est_tdoa=est_tdoa, true_tdoa=true_tdoa, fig_path=xcorr_path)

    result = {
        "true_delay": float(true_tdoa),
        "est_delay": float(est_tdoa),
        "true_angle_deg": float(true_angle_deg),
        "est_angle_deg": float(est_angle_deg),
        "abs_error_deg": float(abs_error_deg),
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return outdir_path
