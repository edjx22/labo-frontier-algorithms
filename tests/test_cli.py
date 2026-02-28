from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_module_help_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "labo_frontier_algorithms", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "run_ssl_demo" in result.stdout


def test_run_ssl_demo_command_creates_plot(tmp_path: Path) -> None:
    outdir = tmp_path / "out"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "labo_frontier_algorithms",
            "run_ssl_demo",
            "--outdir",
            str(outdir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (outdir / "waveforms.png").exists()
    assert (outdir / "xcorr.png").exists()
    assert (outdir / "result.json").exists()


def test_run_ssl_demo_command_writes_complete_result_json(tmp_path: Path) -> None:
    outdir = tmp_path / "out"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "labo_frontier_algorithms",
            "run_ssl_demo",
            "--outdir",
            str(outdir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads((outdir / "result.json").read_text(encoding="utf-8"))
    expected_keys = {
        "true_delay",
        "est_delay",
        "true_angle_deg",
        "est_angle_deg",
        "abs_error_deg",
    }
    assert set(payload) == expected_keys
    for key in expected_keys:
        assert isinstance(payload[key], float)
