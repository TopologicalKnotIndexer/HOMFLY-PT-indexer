import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from homflypt_solver import homflypt_solver  # noqa: E402


SAGE_EXECUTABLE = os.environ.get("TKI_SAGE_EXECUTABLE")
TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
FIGURE_EIGHT = [[4, 2, 5, 1], [8, 6, 1, 5], [6, 3, 7, 4], [2, 7, 3, 8]]


@unittest.skipUnless(SAGE_EXECUTABLE, "set TKI_SAGE_EXECUTABLE to run SageMath integration tests")
class HomflySageIntegrationTests(unittest.TestCase):
    def test_real_sage_matches_catalog_convention(self):
        cases = (
            (TREFOIL, "-L^4 + L^2*M^2 - 2*L^2"),
            (FIGURE_EIGHT, "-L^2 + M^2 - 1 - L^-2"),
        )
        for pd_code, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    homflypt_solver(
                        pd_code,
                        sage_path=SAGE_EXECUTABLE,
                        timeout=180,
                    ),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
