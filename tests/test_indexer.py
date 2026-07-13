from pathlib import Path
from unittest.mock import patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from get_homflypt_by_pd_code import get_homflypt_by_pd_code  # noqa: E402
from get_knotname_by_homflypt import (  # noqa: E402
    get_knotname_by_homflypt,
    load_homflypt_index,
)
from homflypt_indexer import homflypt_indexer  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
TREFOIL_POLYNOMIAL = "-L^4 + L^2*M^2 - 2*L^2"


class HomflyIndexerTests(unittest.TestCase):
    def test_complete_catalog_load_and_known_lookups(self):
        index = load_homflypt_index()
        self.assertEqual(len(index), 1669)
        self.assertEqual(sum(map(len, index.values())), 1783)
        self.assertEqual(get_knotname_by_homflypt("1"), ["K0a1"])
        self.assertIn("K3a1", get_knotname_by_homflypt(TREFOIL_POLYNOMIAL))
        self.assertEqual(get_knotname_by_homflypt("not in catalog"), [])

    def test_local_solver_process_contract(self):
        completed = subprocess.CompletedProcess(
            args=["python"], returncode=0, stdout=" P(L,M)\n", stderr=""
        )
        with patch("get_homflypt_by_pd_code.subprocess.run", return_value=completed) as run:
            result = get_homflypt_by_pd_code(TREFOIL, sage_path="custom-sage", timeout=4)
        self.assertEqual(result, "P(L,M)")
        command = run.call_args.args[0]
        self.assertIn("--sage", command)
        self.assertIn("custom-sage", command)
        self.assertIn("--timeout", command)
        self.assertEqual(run.call_args.kwargs["input"], repr(TREFOIL))

    def test_local_solver_failure_is_not_silenced(self):
        completed = subprocess.CompletedProcess(
            args=["python"], returncode=2, stdout="", stderr="bad PD code"
        )
        with patch("get_homflypt_by_pd_code.subprocess.run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "bad PD code"):
                get_homflypt_by_pd_code(TREFOIL)

    def test_indexer_composes_solver_and_lookup(self):
        with (
            patch("homflypt_indexer.get_homflypt_by_pd_code", return_value=TREFOIL_POLYNOMIAL),
            patch("homflypt_indexer.get_knotname_by_homflypt", return_value=["K3a1"]) as lookup,
        ):
            self.assertEqual(homflypt_indexer(TREFOIL), ["K3a1"])
        lookup.assert_called_once_with(TREFOIL_POLYNOMIAL)

    def test_end_to_end_unknot_without_sage(self):
        self.assertEqual(homflypt_indexer([]), ["K0a1"])
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="[]",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "K0a1")

    def test_cli_does_not_execute_input(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="__import__('os').getcwd()",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("malformed node", completed.stderr)


if __name__ == "__main__":
    unittest.main()
