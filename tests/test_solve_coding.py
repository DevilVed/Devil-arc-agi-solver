import numpy as np
from arc_agi.solve_coding import _array_diff


def test_array_diff_identical():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 4]])
    expected = "1 2\n3 4"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_with_differences():
    arr1 = np.array([[1, 5], [3, 4]])
    arr2 = np.array([[1, 2], [3, 9]])
    expected = "1 5/2\n3 4/9"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_single_element():
    arr1 = np.array([[7]])
    arr2 = np.array([[8]])
    assert _array_diff(arr1, arr2) == "7/8"
