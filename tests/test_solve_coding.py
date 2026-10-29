import numpy as np
import pytest
from arc_agi.solve_coding import _array_diff, _example_to_diagram


def test_example_to_diagram_list():
    grid = [[1, 2], [3, 4]]
    expected = "1 2\n3 4"
    assert _example_to_diagram(grid) == expected


def test_example_to_diagram_ndarray():
    grid = np.array([[0, 9], [5, 8]])
    expected = "0 9\n5 8"
    assert _example_to_diagram(grid) == expected


def test_example_to_diagram_large_values():
    grid = [[10, 11], [0, 1]]
    expected = "10 11\n0 1"
    assert _example_to_diagram(grid) == expected


def test_array_diff_matching():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 4]])
    expected = "1 2\n3 4"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_mismatch():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 5], [3, 0]])
    expected = "1 2/5\n3 4/0"
    assert _array_diff(arr1, arr2) == expected
