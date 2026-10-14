import pytest
from arc_agi.scoring import score_task, grids_equal
from arc_agi.io import build_kaggle_two_attempts, _coerce_grid


def test_grids_equal():
    grid_a = [[1, 2], [3, 4]]
    grid_b = [[1, 2], [3, 4]]
    grid_c = [[1, 2], [3, 5]]
    assert grids_equal(grid_a, grid_b) is True
    assert grids_equal(grid_a, grid_c) is False


def test_score_task():
    gt_outputs = [[[1, 0], [0, 1]]]

    # Matching attempt_1
    preds_match_1 = [{"attempt_1": [[1, 0], [0, 1]], "attempt_2": [[0, 0], [0, 0]]}]
    assert score_task(preds_match_1, gt_outputs) == 1.0

    # Matching attempt_2
    preds_match_2 = [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[1, 0], [0, 1]]}]
    assert score_task(preds_match_2, gt_outputs) == 1.0

    # No match
    preds_no_match = [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[1, 1], [1, 1]]}]
    assert score_task(preds_no_match, gt_outputs) == 0.0

    # Empty GT
    assert score_task(preds_match_1, []) == 0.0


def test_coerce_grid():
    assert _coerce_grid([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert _coerce_grid('[[1, 2], [3, 4]]') == [[1, 2], [3, 4]]
    assert _coerce_grid('invalid json') == []
    assert _coerce_grid(123) == []


def test_build_kaggle_two_attempts():
    results = [
        {
            "results": [
                {"output": [[1, 2], [3, 4]]}
            ]
        },
        {
            "results": [
                {"output": [[5, 6], [7, 8]]}
            ]
        }
    ]
    test_in = [[[]]]  # 1 test item

    kaggle_preds = build_kaggle_two_attempts(results, test_in)
    assert len(kaggle_preds) == 1
    assert kaggle_preds[0]["attempt_1"] == [[1, 2], [3, 4]]
    assert kaggle_preds[0]["attempt_2"] == [[5, 6], [7, 8]]
