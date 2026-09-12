"""Run AlgoX verification locally without GitHub Actions.

Usage from repository root:
    python tools/local_verify.py
    python tools/local_verify.py --pytest

The default mode uses only the Python standard library plus the existing
benchmark entry point. The optional --pytest mode runs the full pytest suite
when pytest is installed locally.
"""

from __future__ import annotations

import argparse
import compileall
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> int:
    print("$", " ".join(command))
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pytest",
        action="store_true",
        help="run the full pytest suite after compilation and benchmark checks",
    )
    args = parser.parse_args()

    print("AlgoX local verification")

    if not compileall.compile_dir(str(ROOT / "algox"), quiet=1):
        print("FAIL: Python compilation")
        return 1
    print("PASS: Python compilation")

    if run([sys.executable, "experiments/memory_benchmark.py"]) != 0:
        print("FAIL: EXP-MEM-0001 benchmark")
        return 1
    print("PASS: EXP-MEM-0001 benchmark")

    if args.pytest:
        if run([sys.executable, "-m", "pytest", "-q"]) != 0:
            print("FAIL: pytest suite")
            return 1
        print("PASS: pytest suite")
    else:
        print("SKIP: pytest suite (use --pytest to run it locally)")

    print("LOCAL VERIFICATION COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
