"""Run Python source through a SageMath executable and capture its streams."""

from pathlib import Path
import os
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
PORTABLE_SAGE = HERE / "bin" / "portable_sage" / "sage.sh"


def _find_sage(explicit: str | os.PathLike[str] | None = None) -> str:
    if explicit is not None:
        candidate = os.fspath(explicit)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        path = Path(candidate)
        if path.is_file():
            return str(path.resolve())
        raise FileNotFoundError(f"SageMath executable not found: {candidate}")

    if PORTABLE_SAGE.is_file():
        return str(PORTABLE_SAGE)
    resolved = shutil.which("sage")
    if resolved:
        return resolved
    raise FileNotFoundError(
        "SageMath was not found; install it, put 'sage' on PATH, or pass sage_path"
    )


def sage_run(
    python_code: str,
    sage_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
) -> tuple[int, str, str]:
    """Execute *python_code* with Sage and return `(exit_code, stdout, stderr)`."""

    if not isinstance(python_code, str):
        raise TypeError("python_code must be a string")
    executable = _find_sage(sage_path)
    result = subprocess.run(
        [executable, "-c", python_code],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


SAMPLE_CODE = """
from sage.all import *
K = Knot([[2, 8, 3, 7], [4, 10, 5, 9], [6, 2, 7, 1], [8, 4, 9, 3], [10, 6, 1, 5]])
K3a1 = Knot([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]])
if str(K3a1.homfly_polynomial()).strip() == "L^-2*M^2 - 2*L^-2 - L^-4":
    K = K.mirror_image()
print(K.homfly_polynomial())
print(K.connected_sum(K).pd_code())
"""


if __name__ == "__main__":
    print(sage_run(SAMPLE_CODE))
