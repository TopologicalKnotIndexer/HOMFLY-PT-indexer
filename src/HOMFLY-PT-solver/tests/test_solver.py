from pathlib import Path
from unittest.mock import patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from de_r1_k8 import de_r1_k8  # noqa: E402
from homflypt_solver import _build_sage_code, homflypt_solver  # noqa: E402
from input_sanity import input_sanity  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


class HomflySolverTests(unittest.TestCase):
    def test_generated_code_is_valid_and_contains_convention_check(self):
        code = _build_sage_code(TREFOIL)
        compile(code, "<generated-sage>", "exec")
        self.assertIn("reference.homfly_polynomial", code)
        self.assertIn("diagram.mirror_image()", code)

    def test_backend_contract_and_keyword_forwarding(self):
        with patch("homflypt_solver.sage_run", return_value=(0, " P(L,M)\n", "")) as run:
            result = homflypt_solver(TREFOIL, sage_path="custom-sage", timeout=3.5)
        self.assertEqual(result, "P(L,M)")
        _, kwargs = run.call_args
        self.assertEqual(kwargs, {"sage_path": "custom-sage", "timeout": 3.5})

    def test_unknot_avoids_backend(self):
        with patch("homflypt_solver.sage_run") as run:
            self.assertEqual(homflypt_solver([]), "1")
            self.assertEqual(homflypt_solver([[1, 2, 2, 1]]), "1")
        run.assert_not_called()

    def test_backend_failure_is_not_silenced(self):
        with patch("homflypt_solver.sage_run", return_value=(7, "", "bad diagram")):
            with self.assertRaisesRegex(RuntimeError, "bad diagram"):
                homflypt_solver(TREFOIL)

    def test_safe_parser_and_simplifier_are_static_dependencies(self):
        self.assertEqual(input_sanity(str(TREFOIL)), TREFOIL)
        self.assertEqual(de_r1_k8([[1, 2, 2, 1]]), [])
        with self.assertRaises(ValueError):
            input_sanity("__import__('os').getcwd()")

    def test_cli_rejects_empty_stdin(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("expected a PD-code literal", completed.stderr)


if __name__ == "__main__":
    unittest.main()
