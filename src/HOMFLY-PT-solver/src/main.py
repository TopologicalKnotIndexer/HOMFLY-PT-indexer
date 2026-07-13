"""Command-line interface for HOMFLY-PT-solver."""

import argparse
import sys

from homflypt_solver import homflypt_solver


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read a knot PD code from stdin and print its mirror HOMFLY-PT polynomial."
    )
    parser.add_argument("--sage", help="path or command name for SageMath")
    parser.add_argument("--timeout", type=float, help="maximum SageMath runtime in seconds")
    args = parser.parse_args(argv)
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        parser.exit(2, "error: expected a PD-code literal on standard input\n")
    try:
        print(homflypt_solver(raw, sage_path=args.sage, timeout=args.timeout))
    except (FileNotFoundError, TypeError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
