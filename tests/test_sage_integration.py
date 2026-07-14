import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from homflypt_indexer import homflypt_indexer  # noqa: E402


SAGE_EXECUTABLE = os.environ.get("TKI_SAGE_EXECUTABLE")
TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
FIGURE_EIGHT = [[4, 2, 5, 1], [8, 6, 1, 5], [6, 3, 7, 4], [2, 7, 3, 8]]


@unittest.skipUnless(SAGE_EXECUTABLE, "set TKI_SAGE_EXECUTABLE to run SageMath integration tests")
class HomflyIndexerSageIntegrationTests(unittest.TestCase):
    def test_real_sage_resolves_known_knots_through_catalog(self):
        cases = ((TREFOIL, ["K3a1"]), (FIGURE_EIGHT, ["K4a1"]))
        for pd_code, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    homflypt_indexer(
                        pd_code,
                        sage_path=SAGE_EXECUTABLE,
                        timeout=180,
                    ),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
