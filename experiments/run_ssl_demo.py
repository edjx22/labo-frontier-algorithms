"""One-click experiment runner for SSL baseline."""

from labo_frontier_algorithms.demo import run_ssl_demo

if __name__ == "__main__":
    output = run_ssl_demo("out")
    print(f"Generated: {output}")
