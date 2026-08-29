import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fgv_state.io import write_pair_if_changed


class StateIoTests(unittest.TestCase):
    def test_second_install_failure_rolls_back_the_first_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "catalog.jsonl"
            second = root / "dashboard.md"
            first.write_bytes(b"old catalog\n")
            second.write_bytes(b"old dashboard\n")
            import fgv_state.io as state_io
            real_replace = state_io.os.replace
            failed = False

            def fail_second_once(source, destination):
                nonlocal failed
                if Path(destination) == second and not failed:
                    failed = True
                    raise OSError("injected second install failure")
                return real_replace(source, destination)

            with patch("fgv_state.io.os.replace", side_effect=fail_second_once):
                with self.assertRaises(OSError):
                    write_pair_if_changed((first, b"new catalog\n"), (second, b"new dashboard\n"))
            self.assertEqual(first.read_bytes(), b"old catalog\n")
            self.assertEqual(second.read_bytes(), b"old dashboard\n")


if __name__ == "__main__":
    unittest.main()
