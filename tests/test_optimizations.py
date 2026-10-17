import numpy as np
import pytest

from arc_agi.io import _coerce_grid
from arc_agi.solve_coding import (
    _array_diff,
    _build_feedback,
    _example_to_diagram,
    _soft_score,
)
from arc_agi.solve_parallel_coding import _mean_soft
from arc_agi.types import ARCAGIResult, RunResult


def test_coerce_grid():
    # List case
    grid = [[1, 2], [3, 4]]
    assert _coerce_grid(grid) == [[1, 2], [3, 4]]

    # Numpy array case
    arr = np.array([[1, 2], [3, 4]])
    assert _coerce_grid(arr) == [[1, 2], [3, 4]]

    # String case
    s = "[[1, 2], [3, 4]]"
    assert _coerce_grid(s) == [[1, 2], [3, 4]]

    # Invalid cases
    assert _coerce_grid("not json") == []
    assert _coerce_grid(123) == []


def test_example_to_diagram():
    ex_list = [[1, 2], [3, 4]]
    expected = "1 2\n3 4"
    assert _example_to_diagram(ex_list) == expected

    ex_arr = np.array([[1, 2], [3, 4]])
    assert _example_to_diagram(ex_arr) == expected


def test_array_diff():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 5], [3, 4]])
    diff = _array_diff(arr1, arr2)
    assert diff == "1 2/5\n3 4"

    arr3 = np.array([[1, 2], [3, 4]])
    arr4 = np.array([[1, 2], [3, 4]])
    diff_same = _array_diff(arr3, arr4)
    assert diff_same == "1 2\n3 4"


def test_soft_score():
    pred = np.array([[1, 2], [3, 4]])
    truth = np.array([[1, 2], [3, 5]])
    score = _soft_score(pred, truth)
    assert score == 0.75

    # Shape mismatch
    pred_mismatch = np.array([[1, 2]])
    assert _soft_score(pred_mismatch, truth) == 0.0

    # Empty array
    empty = np.array([])
    assert _soft_score(empty, empty) == 1.0


def test_mean_soft():
    res1: ARCAGIResult = {
        "train_results": [
            RunResult(success=True, output="", soft_score=1.0, error=None, code=""),
            RunResult(success=False, output="", soft_score=0.5, error=None, code=""),
        ],
        "results": [],
        "iteration": 1,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    assert _mean_soft(res1) == 0.75

    res_empty: ARCAGIResult = {
        "train_results": [],
        "results": [],
        "iteration": 1,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    assert _mean_soft(res_empty) == 0.0


def test_build_feedback():
    train_results = [
        RunResult(success=True, output='[[1, 2]]', soft_score=1.0, error=None, code=''),
        RunResult(
            success=False,
            output='[[1, 3]]',
            soft_score=0.5,
            error='RuntimeError',
            code='',
        ),
    ]
    train_in = [[[1, 2]], [[1, 2]]]
    train_out = [[[1, 2]], [[1, 4]]]

    feedback, mean_score = _build_feedback(train_results, train_in, train_out)
    assert "Solves Example #1 correctly." in feedback
    assert "Solves Example #2 incorrectly." in feedback
    assert "1/3/4" in feedback or "1/3" in feedback or "3/4" in feedback
    assert "RuntimeError" in feedback
    assert mean_score == 0.75
