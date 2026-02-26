from __future__ import annotations

import numpy as np

from labo_frontier_algorithms.signal import fractional_delay, generate_two_mic_sine
from labo_frontier_algorithms.ssl import estimate_angle_from_tdoa, gcc_phat


def test_fractional_delay_preserves_shape() -> None:
    x = np.linspace(0, 1, 200)
    y = fractional_delay(x, 2.75)
    assert y.shape == x.shape


def test_gcc_phat_estimates_tdoa_close_to_true() -> None:
    fs = 16000
    x1, x2, true_tdoa = generate_two_mic_sine(
        fs=fs,
        duration_s=0.15,
        freq_hz=700.0,
        mic_distance_m=0.08,
        angle_deg=20.0,
        snr_db=30.0,
        seed=7,
    )
    est_tdoa, _ = gcc_phat(x2, x1, fs=fs, max_tau=0.08 / 343.0)
    assert np.isclose(est_tdoa, true_tdoa, atol=2.5e-5)


def test_estimate_angle_from_tdoa_is_reasonable() -> None:
    angle = estimate_angle_from_tdoa(6.0e-5, mic_distance_m=0.08)
    assert 10.0 < angle < 20.0
