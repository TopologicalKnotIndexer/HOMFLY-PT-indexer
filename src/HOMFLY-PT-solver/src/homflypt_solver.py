"""Compute the mirror-image HOMFLY-PT polynomial of a knot PD code."""

from os import PathLike

from de_r1_k8 import de_r1_k8
from input_sanity import input_sanity
from sage_run_interface import sage_run


_REFERENCE_POLYNOMIAL = "L^-2*M^2 - 2*L^-2 - L^-4"
_TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


def _build_sage_code(pd_code: list[list[int]]) -> str:
    """Build injection-safe Sage source from an already validated PD code."""

    return f"""from sage.all import Knot
diagram = Knot({pd_code!r})
reference = Knot({_TREFOIL!r})
if str(reference.homfly_polynomial()).strip() == {_REFERENCE_POLYNOMIAL!r}:
    diagram = diagram.mirror_image()
print(diagram.homfly_polynomial())
"""


def homflypt_solver(
    input_pdcode: str | list[list[int]],
    *,
    sage_path: str | PathLike[str] | None = None,
    timeout: float | None = None,
) -> str:
    """Return the catalog-compatible mirror-image HOMFLY-PT polynomial.

    The reference trefoil check compensates for Sage releases whose PD-code
    orientation convention is the mirror of the convention used by this
    organization's polynomial catalog.
    """

    pd_code = de_r1_k8(input_sanity(input_pdcode))
    if not pd_code:
        return "1"
    exit_code, stdout, stderr = sage_run(
        _build_sage_code(pd_code), sage_path=sage_path, timeout=timeout
    )
    if exit_code != 0:
        detail = stderr.strip() or "SageMath produced no diagnostic output"
        raise RuntimeError(f"SageMath failed with exit code {exit_code}: {detail}")
    result = stdout.strip()
    if not result:
        raise RuntimeError("SageMath returned an empty HOMFLY-PT polynomial")
    return result


if __name__ == "__main__":
    trefoil_sum = [
        [1, 5, 2, 4], [3, 7, 4, 6], [5, 3, 6, 2],
        [7, 10, 8, 11], [9, 12, 10, 1], [11, 8, 12, 9],
    ]
    print(homflypt_solver(trefoil_sum))
