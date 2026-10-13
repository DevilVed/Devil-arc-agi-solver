import unittest
import numpy as np
from arc_agi.solve_parallel_coding import _mean_soft
from arc_agi.io import _coerce_grid
from arc_agi.types import ARCAGIResult, RunResult

class TestOptimizations(unittest.TestCase):
    def test_mean_soft(self):
        # Test empty
        self.assertEqual(_mean_soft(ARCAGIResult(train_results=[], results=[], iteration=1)), 0.0)

        # Test single item
        res1 = ARCAGIResult(
            train_results=[RunResult(success=True, output="", soft_score=0.75, error=None, code="")],
            results=[], iteration=1
        )
        self.assertAlmostEqual(_mean_soft(res1), 0.75)

        # Test multiple items
        res2 = ARCAGIResult(
            train_results=[
                RunResult(success=True, output="", soft_score=0.5, error=None, code=""),
                RunResult(success=True, output="", soft_score=1.0, error=None, code=""),
                RunResult(success=True, output="", soft_score=0.75, error=None, code=""),
            ],
            results=[], iteration=1
        )
        self.assertAlmostEqual(_mean_soft(res2), 0.75)

    def test_coerce_grid(self):
        # Test list input
        grid_list = [[1, 2], [3, 4]]
        self.assertEqual(_coerce_grid(grid_list), [[1, 2], [3, 4]])

        # Test string input
        grid_str = "[[1, 2], [3, 4]]"
        self.assertEqual(_coerce_grid(grid_str), [[1, 2], [3, 4]])

        # Test numpy array input
        arr = np.array([[1, 2], [3, 4]])
        self.assertEqual(_coerce_grid(arr), [[1, 2], [3, 4]])

        # Test non-grid types
        self.assertEqual(_coerce_grid(123), [])
        self.assertEqual(_coerce_grid("not a json"), [])
        self.assertEqual(_coerce_grid('{"key": "value"}'), [])

if __name__ == "__main__":
    unittest.main()
