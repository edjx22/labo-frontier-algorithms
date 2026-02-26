"""Signal generation utilities for SSL demos."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def fractional_delay(signal: FloatArray, delay_samples: float) -> FloatArray:
    """Apply a fractional sample delay using linear interpolation."""
    n = np.arange(signal.size)
    x = n - delay_samples
    delayed = np.interp(x, n, signal, left=0.0, right=0.0)
    return np.asarray(delayed, dtype=np.float64)


def generate_two_mic_sine(
    fs: int,
    duration_s: float,
    freq_hz: float,
    mic_distance_m: float,
    angle_deg: float,
    snr_db: float,
    c: float = 343.0,
    seed: int = 0,
) -> tuple[FloatArray, FloatArray, float]:
    """Generate a synthetic two-microphone signal pair and true TDOA.

    Returns (x1, x2, true_delay_seconds).
    """
    t = np.arange(int(fs * duration_s), dtype=np.float64) / fs
    rng = np.random.default_rng(seed)
    tone = np.sin(2 * np.pi * freq_hz * t)
    texture = rng.normal(0.0, 1.0, size=t.shape)
    mono = 0.8 * tone + 0.2 * texture

    theta = np.deg2rad(angle_deg)
    true_delay_s = (mic_distance_m * np.sin(theta)) / c
    delayed = fractional_delay(mono, true_delay_s * fs)

    signal_power = np.mean(mono**2)
    noise_power = signal_power / (10 ** (snr_db / 10))
    noise_std = float(np.sqrt(noise_power))

    x1 = mono + rng.normal(0.0, noise_std, size=mono.shape)
    x2 = delayed + rng.normal(0.0, noise_std, size=mono.shape)
    return x1.astype(np.float64), x2.astype(np.float64), true_delay_s
