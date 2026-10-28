import time
import numpy as np
from arc_agi.solve_parallel_coding import _mean_soft
from arc_agi.solve_coding import _array_diff
from arc_agi.types import RunResult


def test_mean_soft_correctness():
    # Test empty list
    res_empty = {"train_results": []}
    assert _mean_soft(res_empty) == 0.0

    # Test list of RunResults
    trs = [
        RunResult(success=False, output="", soft_score=0.8, error="", code=""),
        RunResult(success=False, output="", soft_score=0.2, error="", code=""),
        RunResult(success=True, output="", soft_score=1.0, error="", code=""),
    ]
    res = {"train_results": trs}
    expected = (0.8 + 0.2 + 1.0) / 3
    assert abs(_mean_soft(res) - expected) < 1e-9


def test_array_diff_correctness():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 5], [3, 4]])

    expected = "1 2/5\n3 4"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_performance():
    a1 = np.random.randint(0, 10, (30, 30))
    a2 = np.random.randint(0, 10, (30, 30))

    t0 = time.perf_counter()
    for _ in range(500):
        _array_diff(a1, a2)
    elapsed = time.perf_counter() - t0

    # Sanity check that 500 diffs on 30x30 grids execute in under 0.5s
    assert elapsed < 0.5
