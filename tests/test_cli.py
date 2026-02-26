from __future__ import annotations

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
    assert (outdir / "ssl_demo_gcc_phat.png").exists()
