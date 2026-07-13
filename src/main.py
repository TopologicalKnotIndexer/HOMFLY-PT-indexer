"""Command-line interface for HOMFLY-PT-indexer."""

from ast import literal_eval
import argparse
import subprocess
import sys

from homflypt_indexer import homflypt_indexer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Identify catalogued knots by mirror-image HOMFLY-PT polynomial."
    )
    parser.add_argument("--sage", help="path or command name for SageMath")
    parser.add_argument("--timeout", type=float, help="maximum SageMath runtime in seconds")
    args = parser.parse_args(argv)
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        parser.exit(2, "error: expected a PD-code literal on standard input\n")
    try:
        pd_code = literal_eval(raw)
        if not isinstance(pd_code, list):
            raise TypeError("a PD code must be a list")
        for name in homflypt_indexer(
            pd_code, sage_path=args.sage, timeout=args.timeout
        ):
            print(name)
    except (
        FileNotFoundError,
        KeyError,
        subprocess.TimeoutExpired,
        SyntaxError,
        TypeError,
        ValueError,
        RuntimeError,
    ) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
