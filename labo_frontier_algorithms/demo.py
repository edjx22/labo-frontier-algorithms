"""Demo runner for SSL baseline."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from .signal import generate_two_mic_sine
from .ssl import estimate_angle_from_tdoa, gcc_phat

FloatArray = NDArray[np.float64]


def run_ssl_demo(outdir: str | Path = "out") -> Path:
    """Run synthetic GCC-PHAT demo and save output figure."""
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
    est_tdoa, cc = gcc_phat(x2, x1, fs=fs, max_tau=max_tau)
    est_angle_deg = estimate_angle_from_tdoa(est_tdoa, mic_distance_m)

    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    fig_path = outdir_path / "ssl_demo_gcc_phat.png"

    lag_idx: NDArray[np.int64] = np.arange(-len(cc) // 2 + 1, len(cc) // 2 + 1)
    lag_idx = lag_idx[: len(cc)]
    lags: FloatArray = lag_idx.astype(np.float64) / float(fs)

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=True)
    axes[0].plot(x1, label="mic1", linewidth=1.0)
    axes[0].plot(x2, label="mic2", linewidth=1.0, alpha=0.8)
    axes[0].set_title("Synthetic Two-Mic Signals")
    axes[0].set_xlabel("Sample")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend()

    axes[1].plot(lags * 1000.0, np.abs(cc), color="tab:orange")
    axes[1].axvline(est_tdoa * 1000.0, color="tab:red", linestyle="--", label="Estimated delay")
    axes[1].axvline(true_tdoa * 1000.0, color="tab:green", linestyle=":", label="True delay")
    axes[1].set_title(
        "GCC-PHAT | "
        f"true angle={true_angle_deg:.1f} deg, est angle={est_angle_deg:.1f} deg"
    )
    axes[1].set_xlabel("Lag (ms)")
    axes[1].set_ylabel("|CC|")
    axes[1].legend()

    fig.savefig(fig_path, dpi=140)
    plt.close(fig)
    return fig_path
