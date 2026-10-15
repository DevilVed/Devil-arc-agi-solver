import unittest
from main import _format_score, _get_task_mark


class TestCLIUX(unittest.TestCase):
    def test_get_task_mark_full_pass(self):
        self.assertEqual(_get_task_mark(1.0), "✓")

    def test_get_task_mark_partial_pass(self):
        self.assertEqual(_get_task_mark(0.5), "◐")
        self.assertEqual(_get_task_mark(0.25), "◐")

    def test_get_task_mark_failure(self):
        self.assertEqual(_get_task_mark(0.0), "✗")

    def test_format_score_integer(self):
        self.assertEqual(_format_score(1.0), "1")
        self.assertEqual(_format_score(0.0), "0")
        self.assertEqual(_format_score(10.0), "10")

    def test_format_score_float(self):
        self.assertEqual(_format_score(0.5), "0.5")
        self.assertEqual(_format_score(1.25), "1.25")


if __name__ == "__main__":
    unittest.main()
