"""Look up knot names in the bundled HOMFLY-PT catalog."""

from functools import lru_cache
from pathlib import Path

from slow_dict_reader.src.slow_dict_reader import slow_dict_reader


SOURCE_DIR = Path(__file__).resolve().parent
HOMDMP = SOURCE_DIR / "HOMFLY-PT-polynomial-list" / "data" / "sorted_HOMFLY-PT.txt"


@lru_cache(maxsize=1)
def load_homflypt_index() -> dict[str, list[str]]:
    """Load and normalize the committed polynomial/name records once."""

    if not HOMDMP.is_file():
        raise FileNotFoundError(HOMDMP)
    return slow_dict_reader(str(HOMDMP))


def get_knotname_by_homflypt(homflypt: str) -> list[str]:
    """Return independent copies of all catalog names matching *homflypt*."""

    if not isinstance(homflypt, str):
        raise TypeError("homflypt must be a string")
    key = homflypt.strip()
    if not key:
        return []
    return list(load_homflypt_index().get(key, ()))


if __name__ == "__main__":
    print(get_knotname_by_homflypt("-L^4 + L^2*M^2 - 2*L^2"))
