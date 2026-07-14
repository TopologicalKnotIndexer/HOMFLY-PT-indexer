"""Execute generated Python source with an installed SageMath command."""

from pathlib import Path
import os
import shutil
import subprocess


def _find_sage(explicit: str | os.PathLike[str] | None = None) -> str:
    candidate = os.fspath(explicit) if explicit is not None else "sage"
    resolved = shutil.which(candidate)
    if resolved:
        return resolved
    path = Path(candidate)
    if path.is_file():
        return str(path.resolve())
    raise FileNotFoundError(
        f"SageMath executable not found: {candidate}; install SageMath, put "
        "'sage' on PATH, or pass sage_path"
    )


def sage_run(
    sage_code: str,
    sage_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
) -> tuple[int, str, str]:
    """Run *sage_code* and return ``(exit_code, stdout, stderr)``."""

    if not isinstance(sage_code, str):
        raise TypeError("sage_code must be a string")
    completed = subprocess.run(
        [_find_sage(sage_path), "-c", sage_code],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr
