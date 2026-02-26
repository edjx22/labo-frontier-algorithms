"""GCC-PHAT baseline implementation."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def gcc_phat(
    sig: FloatArray,
    refsig: FloatArray,
    fs: int,
    max_tau: float | None = None,
    interp: int = 16,
) -> tuple[float, FloatArray]:
    """Estimate TDOA using GCC-PHAT.

    Returns (tau_seconds, cross_correlation).
    """
    n = sig.shape[0] + refsig.shape[0]
    nfft = 1
    while nfft < n:
        nfft <<= 1

    sig_fft = np.fft.rfft(sig, n=nfft)
    ref_fft = np.fft.rfft(refsig, n=nfft)
    r = sig_fft * np.conj(ref_fft)
    denom = np.abs(r)
    r /= np.maximum(denom, 1e-12)

    cc = np.fft.irfft(r, n=interp * nfft)

    max_shift = int(interp * nfft / 2)
    if max_tau is not None:
        max_shift = min(int(interp * fs * max_tau), max_shift)

    cc_shifted = np.concatenate((cc[-max_shift:], cc[: max_shift + 1]))
    shift = int(np.argmax(np.abs(cc_shifted)) - max_shift)
    tau = shift / float(interp * fs)
    return tau, cc_shifted


def estimate_angle_from_tdoa(tdoa_s: float, mic_distance_m: float, c: float = 343.0) -> float:
    """Estimate azimuth angle in degrees from TDOA."""
    arg = np.clip((tdoa_s * c) / mic_distance_m, -1.0, 1.0)
    return float(np.rad2deg(np.arcsin(arg)))
