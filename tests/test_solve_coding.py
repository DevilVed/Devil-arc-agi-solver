import numpy as np
from arc_agi.solve_coding import _array_diff


def test_array_diff_matching():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 2], [3, 4]])
    expected = "1 2\n3 4"
    assert _array_diff(a, b) == expected


def test_array_diff_mismatch():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 5], [3, 4]])
    expected = "1 2/5\n3 4"
    assert _array_diff(a, b) == expected


def test_array_diff_multiple_mismatches():
    a = np.array([[0, 1, 2], [3, 4, 5]])
    b = np.array([[0, 9, 2], [7, 4, 8]])
    expected = "0 1/9 2\n3/7 4 5/8"
    assert _array_diff(a, b) == expected
