# x86_64-sage-minimal

Execute Python source with SageMath and capture the exit code, standard output,
and standard error without importing Sage into the caller's interpreter.

## Requirements

- Python 3.10 or newer.
- SageMath on `PATH` as `sage`, an executable passed with `sage_path`, or the
  optional `src/bin/portable_sage/sage.sh` layout.
- On Windows, SageMath installed in WSL can be selected without a shell wrapper
  by passing `wsl://DISTRIBUTION/absolute/path/to/sage`, for example
  `wsl://Ubuntu-26.04/home/user/miniforge3/envs/math_env/bin/sage`.

SageMath 10.3 or newer is recommended. See the
[SageMath repository](https://github.com/sagemath/sage).

## Python API

```python
from src.sage_run import sage_run

code, stdout, stderr = sage_run("print(factor(2024))", timeout=30)
```

The module is safe to import on a machine without Sage. A missing executable
raises `FileNotFoundError` only when `sage_run()` is called. A timeout is
reported through `subprocess.TimeoutExpired`.

## Command-line usage

```bash
echo "print(factor(2024))" | python src/main.py
```

The CLI prints the `(exit_code, stdout, stderr)` tuple.

## Security

This project intentionally executes the supplied source as Sage/Python code.
Run only trusted input and use the optional timeout when invoking it from a
service.

## Development

The wrapper itself uses only the Python standard library. Its subprocess
behavior is covered without requiring Sage:

```bash
python -m unittest discover -s tests -v
```

Set `TKI_SAGE_EXECUTABLE` to run the real SageMath integration test as part of
the same suite:

```powershell
$env:TKI_SAGE_EXECUTABLE = 'wsl://Ubuntu-26.04/home/user/miniforge3/envs/math_env/bin/sage'
python -m unittest discover -s tests -v
```

