import asyncio
from arc_agi.solve_coding import _eval_on_train_and_test


def test_eval_on_train_and_test_success():
    code = """
def transform(grid):
    return grid
"""
    train_in = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    train_out = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    test_in = [[[9, 0], [1, 2]]]

    train_res, test_res = asyncio.run(
        _eval_on_train_and_test(code, train_in, train_out, test_in, timeout_s=2.0)
    )

    assert len(train_res) == 2
    assert len(test_res) == 1

    assert train_res[0]["success"] is True
    assert train_res[0]["soft_score"] == 1.0
    assert train_res[0]["error"] is None
    assert train_res[1]["success"] is True
    assert train_res[1]["soft_score"] == 1.0
    assert train_res[1]["error"] is None

    assert test_res[0]["success"] is False
    assert test_res[0]["error"] is None
    assert test_res[0]["output"] == "[[9, 0], [1, 2]]"


def test_eval_on_train_and_test_failure_and_error():
    code = """
def transform(grid):
    if grid[0][0] == 1:
        return grid
    raise ValueError("grid[0][0] not 1")
"""
    train_in = [[[1, 2], [3, 4]], [[0, 0], [0, 0]]]
    train_out = [[[1, 2], [3, 4]], [[1, 1], [1, 1]]]
    test_in = [[[2, 2], [2, 2]]]

    train_res, test_res = asyncio.run(
        _eval_on_train_and_test(code, train_in, train_out, test_in, timeout_s=2.0)
    )

    assert len(train_res) == 2
    assert len(test_res) == 1

    assert train_res[0]["success"] is True
    assert train_res[0]["soft_score"] == 1.0
    assert train_res[0]["error"] is None

    assert train_res[1]["success"] is False
    assert train_res[1]["error"] is not None
    assert "ValueError" in train_res[1]["error"]

    assert test_res[0]["success"] is False
    assert test_res[0]["error"] is not None
    assert "ValueError" in test_res[0]["error"]
