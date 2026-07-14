"""Execute generated Python source with an installed SageMath command."""

from pathlib import Path
import os
import shutil
import subprocess
from urllib.parse import unquote, urlsplit


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


def _sage_command(
    explicit: str | os.PathLike[str] | None = None,
) -> list[str]:
    """Return a direct command prefix for local or WSL SageMath."""

    if explicit is None:
        return [_find_sage()]
    candidate = os.fspath(explicit)
    parsed = urlsplit(candidate)
    if parsed.scheme.lower() != "wsl":
        return [_find_sage(candidate)]
    if not parsed.netloc or not parsed.path.startswith("/"):
        raise ValueError("a WSL Sage URI must include a distribution and absolute path")
    if parsed.query or parsed.fragment or "\x00" in candidate:
        raise ValueError("invalid WSL Sage URI")
    launcher = shutil.which("wsl.exe") or shutil.which("wsl")
    if launcher is None:
        raise FileNotFoundError("WSL launcher was not found")
    return [launcher, "-d", parsed.netloc, "-e", unquote(parsed.path)]


def sage_run(
    sage_code: str,
    sage_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
) -> tuple[int, str, str]:
    """Run *sage_code* and return ``(exit_code, stdout, stderr)``."""

    if not isinstance(sage_code, str):
        raise TypeError("sage_code must be a string")
    completed = subprocess.run(
        [*_sage_command(sage_path), "-c", sage_code],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr
