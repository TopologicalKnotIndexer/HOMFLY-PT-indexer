import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sage_run import sage_run  # noqa: E402


SAGE_EXECUTABLE = os.environ.get("TKI_SAGE_EXECUTABLE")


@unittest.skipUnless(SAGE_EXECUTABLE, "set TKI_SAGE_EXECUTABLE to run SageMath integration tests")
class SageIntegrationTests(unittest.TestCase):
    def test_real_sage_arithmetic(self):
        exit_code, stdout, stderr = sage_run(
            "print(factor(2024))",
            sage_path=SAGE_EXECUTABLE,
            timeout=120,
        )
        self.assertEqual(exit_code, 0, stderr)
        self.assertEqual(stdout.strip(), "2^3 * 11 * 23")


if __name__ == "__main__":
    unittest.main()
