"""Run the bundled HOMFLY-PT solver as an isolated local program."""

from pathlib import Path
import os
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
SOLVER_MAIN = SOURCE_DIR / "HOMFLY-PT-solver" / "src" / "main.py"


def get_homflypt_by_pd_code(
    pd_code: list[list[int]],
    *,
    sage_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
) -> str:
    """Return the mirror-image HOMFLY-PT polynomial for *pd_code*."""

    if not isinstance(pd_code, list):
        raise TypeError("pd_code must be a list")
    if not SOLVER_MAIN.is_file():
        raise FileNotFoundError(SOLVER_MAIN)
    if timeout is not None and timeout <= 0:
        raise ValueError("timeout must be positive")
    command = [sys.executable, str(SOLVER_MAIN)]
    if sage_path is not None:
        command.extend(["--sage", os.fspath(sage_path)])
    if timeout is not None:
        command.extend(["--timeout", str(timeout)])
    completed = subprocess.run(
        command,
        input=repr(pd_code),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=None if timeout is None else timeout + 10,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"bundled HOMFLY-PT solver failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    polynomial = completed.stdout.strip()
    if not polynomial:
        raise RuntimeError("bundled HOMFLY-PT solver returned an empty polynomial")
    return polynomial


if __name__ == "__main__":
    print(
        get_homflypt_by_pd_code(
            [[2, 8, 3, 7], [4, 10, 5, 9], [6, 2, 7, 1], [8, 4, 9, 3], [10, 6, 1, 5]]
        )
    )
