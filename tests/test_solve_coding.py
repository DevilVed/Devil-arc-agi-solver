import pytest
import numpy as np
from arc_agi.solve_coding import _eval_on_train_and_test, _example_to_diagram


def test_example_to_diagram():
    grid = [[1, 2, 3], [4, 5, 6]]
    expected = "1 2 3\n4 5 6"
    assert _example_to_diagram(grid) == expected

    np_grid = np.array([[1, 2], [3, 4]])
    assert _example_to_diagram(np_grid) == "1 2\n3 4"


@pytest.mark.asyncio
async def test_eval_on_train_and_test_success():
    code = """
def transform(input_grid):
    return input_grid + 1
"""
    train_in = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    train_out = [[[2, 3], [4, 5]], [[6, 7], [8, 9]]]
    test_in = [[[0, 0], [1, 1]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 2
    assert len(test_res) == 1

    assert train_res[0]["success"] is True
    assert train_res[0]["soft_score"] == 1.0
    assert train_res[1]["success"] is True
    assert train_res[1]["soft_score"] == 1.0

    assert test_res[0]["error"] is None


@pytest.mark.asyncio
async def test_eval_on_train_and_test_failure():
    code = """
def transform(input_grid):
    raise ValueError("Invalid operation")
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[2, 3], [4, 5]]]
    test_in = [[[0, 0], [1, 1]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 1
    assert len(test_res) == 1

    assert train_res[0]["success"] is False
    assert "ValueError: Invalid operation" in train_res[0]["error"]
