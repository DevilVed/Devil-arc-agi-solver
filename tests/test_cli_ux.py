import unittest
from arc_agi.utils import format_score, format_status_mark


class TestCLIUX(unittest.TestCase):
    def test_format_status_mark_no_color(self):
        self.assertEqual(format_status_mark(1.0, use_color=False), "✓")
        self.assertEqual(format_status_mark(0.5, use_color=False), "◐")
        self.assertEqual(format_status_mark(0.0, use_color=False), "✗")

    def test_format_status_mark_with_color(self):
        self.assertEqual(format_status_mark(1.0, use_color=True), "\033[92m✓\033[0m")
        self.assertEqual(format_status_mark(0.5, use_color=True), "\033[93m◐\033[0m")
        self.assertEqual(format_status_mark(0.0, use_color=True), "\033[91m✗\033[0m")

    def test_format_score(self):
        self.assertEqual(format_score(0), "0")
        self.assertEqual(format_score(0.0), "0")
        self.assertEqual(format_score(5.0), "5")
        self.assertEqual(format_score(2.5), "2.5")
        self.assertEqual(format_score(10), "10")


if __name__ == "__main__":
    unittest.main()
