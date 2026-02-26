"""CLI entrypoint for labo_frontier_algorithms."""

from __future__ import annotations

import argparse
from pathlib import Path

from .demo import run_ssl_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m labo_frontier_algorithms",
        description="Reproducible frontier audio algorithm baselines.",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_demo = subparsers.add_parser("run_ssl_demo", help="Run synthetic GCC-PHAT SSL demo")
    run_demo.add_argument("--outdir", type=Path, default=Path("out"), help="Output directory")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run_ssl_demo":
        output_path = run_ssl_demo(args.outdir)
        print(f"Saved demo figure to: {output_path}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
