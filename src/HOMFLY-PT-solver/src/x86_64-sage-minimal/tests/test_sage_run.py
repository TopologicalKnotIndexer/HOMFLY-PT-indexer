import subprocess
import unittest
from unittest.mock import patch

from src.sage_run import _find_sage, sage_run


class SageRunTests(unittest.TestCase):
    def test_import_and_lookup_do_not_exit_when_sage_is_missing(self):
        with patch("src.sage_run.PORTABLE_SAGE") as portable, patch(
            "src.sage_run.shutil.which", return_value=None
        ):
            portable.is_file.return_value = False
            with self.assertRaises(FileNotFoundError):
                _find_sage()

    def test_captures_completed_process(self):
        completed = subprocess.CompletedProcess(
            ["sage", "-c", "print(2)"], 0, stdout="2\n", stderr=""
        )
        with patch("src.sage_run._find_sage", return_value="sage"), patch(
            "src.sage_run.subprocess.run", return_value=completed
        ) as run:
            self.assertEqual(sage_run("print(2)", timeout=5), (0, "2\n", ""))
            self.assertEqual(run.call_args.args[0], ["sage", "-c", "print(2)"])
            self.assertEqual(run.call_args.kwargs["timeout"], 5)

    def test_rejects_non_string_code(self):
        with self.assertRaises(TypeError):
            sage_run(42)


if __name__ == "__main__":
    unittest.main()
