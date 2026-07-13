"""Identify catalogued knots by mirror-image HOMFLY-PT polynomial."""

from os import PathLike

from get_homflypt_by_pd_code import get_homflypt_by_pd_code
from get_knotname_by_homflypt import get_knotname_by_homflypt


def homflypt_indexer(
    pd_code: list[list[int]],
    *,
    sage_path: str | PathLike[str] | None = None,
    timeout: float | None = None,
) -> list[str]:
    """Return all catalog names sharing the input diagram's polynomial."""

    polynomial = get_homflypt_by_pd_code(
        pd_code, sage_path=sage_path, timeout=timeout
    )
    return get_knotname_by_homflypt(polynomial)


if __name__ == "__main__":
    print(
        homflypt_indexer(
            [[2, 8, 3, 7], [4, 10, 5, 9], [6, 2, 7, 1], [8, 4, 9, 3], [10, 6, 1, 5]]
        )
    )
