import numpy as np
import pytest

from arc_agi.io import _coerce_grid
from arc_agi.scoring import grids_equal, score_task
from arc_agi.solve_coding import _array_diff, _build_feedback, _soft_score
from arc_agi.solve_parallel_coding import _mean_soft
from arc_agi.types import ARCAGIResult, RunResult


def test_array_diff_matching():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 4]])
    diff = _array_diff(arr1, arr2)
    assert diff == "1 2\n3 4"


def test_array_diff_mismatching():
    arr1 = np.array([[1, 5], [3, 4]])
    arr2 = np.array([[1, 2], [3, 9]])
    diff = _array_diff(arr1, arr2)
    assert diff == "1 5/2\n3 4/9"


def test_soft_score():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 9]])
    # 3 out of 4 match -> 0.75
    score = _soft_score(arr1, arr2)
    assert pytest.approx(score) == 0.75

    # Mismatched shape -> 0.0
    arr3 = np.array([[1, 2]])
    assert _soft_score(arr1, arr3) == 0.0

    # Empty array -> 1.0
    arr_empty = np.array([[]], dtype=int)
    assert _soft_score(arr_empty, arr_empty) == 1.0


def test_build_feedback():
    train_in = [[[1, 2]], [[3, 4]]]
    train_out = [[[1, 2]], [[3, 4]]]

    train_results: list[RunResult] = [
        RunResult(success=True, output="[[1, 2]]", soft_score=1.0, error=None, code=""),
        RunResult(success=False, output="[[3, 9]]", soft_score=0.5, error="Mismatch", code=""),
    ]

    feedback, mean_score = _build_feedback(train_results, train_in, train_out)
    assert "Solves Example #1 correctly." in feedback
    assert "Solves Example #2 incorrectly." in feedback
    assert pytest.approx(mean_score) == 0.75


def test_mean_soft():
    res: ARCAGIResult = {
        "train_results": [
            RunResult(success=True, output="", soft_score=1.0, error=None, code=""),
            RunResult(success=False, output="", soft_score=0.5, error=None, code=""),
        ],
        "results": [],
        "iteration": 1,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    assert pytest.approx(_mean_soft(res)) == 0.75

    empty_res: ARCAGIResult = {
        "train_results": [],
        "results": [],
        "iteration": 1,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    assert _mean_soft(empty_res) == 0.0


def test_coerce_grid():
    arr = np.array([[1, 2], [3, 4]])
    assert _coerce_grid(arr) == [[1, 2], [3, 4]]
    assert _coerce_grid("[[1, 2], [3, 4]]") == [[1, 2], [3, 4]]
    assert _coerce_grid([[1, 2]]) == [[1, 2]]
    assert _coerce_grid("invalid") == []
