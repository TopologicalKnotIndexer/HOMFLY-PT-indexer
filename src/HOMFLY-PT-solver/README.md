# HOMFLY-PT-solver

Compute the mirror-image HOMFLY-PT polynomial of a knot represented by a
planar diagram (PD) code. Output follows the convention used by the
TopologicalKnotIndexer HOMFLY-PT polynomial catalog.

## Requirements

- Python 3.10 or newer
- SageMath with the `sage` command on `PATH`, or an explicit executable path

On Windows, an installed WSL Sage can be selected with a structured URI such
as `wsl://Ubuntu-26.04/home/user/miniforge3/envs/math_env/bin/sage`. The WSL
launcher uses direct execution rather than a shell command string.

No third-party package is required by the ordinary Python interpreter. This
repository is independently cloneable and contains regular tracked copies of
all organization-owned helper source; it does not require Git submodules.

## Command-line usage

Write one Python-literal PD code to standard input:

```bash
echo '[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]' | python src/main.py
```

Optional controls:

```bash
python src/main.py --sage /path/to/sage --timeout 120
```

Malformed input and SageMath failures produce a diagnostic and a nonzero exit
status.

## Python API

```python
from homflypt_solver import homflypt_solver

polynomial = homflypt_solver(pd_code, sage_path="sage", timeout=120)
```

## Algorithm and convention

The input is parsed with `ast.literal_eval`, structurally validated, and
simplified by removing Reidemeister-I and verified nugatory crossings. The
unknot is returned directly as `1`. Other diagrams are passed to SageMath's
`Knot.homfly_polynomial()`.

Sage releases have used a PD orientation convention opposite to the historical
catalog convention. Generated Sage code evaluates a fixed trefoil reference;
when that reference has the opposite-variable orientation, the input diagram
is mirrored before evaluation. This keeps the result compatible with the
catalog while avoiding a hard-coded assumption about the installed Sage
version.

The former helper directories below `src/` are ordinary source snapshots.
Runtime imports are static and do not alter `sys.path`. Their audited revisions
are listed in `VENDORED_DEPENDENCIES.md`.

## Development

The default suite uses a fake Sage backend for deterministic contract coverage.
Set `TKI_SAGE_EXECUTABLE` to include real SageMath calculations of the trefoil
and figure-eight catalog polynomials:

```bash
python -m unittest discover -s tests -v
```

Run each bundled dependency's tests from its own directory when refreshing a
snapshot. No PyPI publication is performed as part of repository maintenance.
