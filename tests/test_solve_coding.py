import numpy as np
from arc_agi.solve_coding import _array_diff


def test_array_diff_matching():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 4]])
    expected = "1 2\n3 4"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_mismatch():
    arr1 = np.array([[1, 5], [3, 4]])
    arr2 = np.array([[1, 2], [3, 8]])
    expected = "1 5/2\n3 4/8"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_empty():
    arr1 = np.array([[]])
    arr2 = np.array([[]])
    assert _array_diff(arr1, arr2) == ""


def test_array_diff_1d_row_col():
    arr1 = np.array([[7]])
    arr2 = np.array([[9]])
    assert _array_diff(arr1, arr2) == "7/9"
