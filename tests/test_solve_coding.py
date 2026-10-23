import asyncio
import numpy as np
import pytest

from arc_agi.io import _coerce_grid
from arc_agi.solve_coding import _array_diff, _eval_on_train_and_test


@pytest.mark.asyncio
async def test_eval_on_train_and_test_success():
    code = """
import numpy as np
def transform(input_grid):
    return input_grid * 2
"""
    train_in = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    train_out = [[[2, 4], [6, 8]], [[10, 12], [14, 16]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 2
    assert len(test_res) == 1
    assert all(r["success"] for r in train_res)
    assert train_res[0]["soft_score"] == 1.0
    assert test_res[0]["output"] == "[[0, 2], [4, 6]]"


@pytest.mark.asyncio
async def test_eval_on_train_and_test_mismatch():
    code = """
import numpy as np
def transform(input_grid):
    return input_grid + 1
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[1, 2], [3, 4]]]
    test_in = [[[0, 0], [0, 0]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 1
    assert not train_res[0]["success"]
    assert train_res[0]["soft_score"] == 0.0


def test_array_diff():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 5], [3, 4]])
    diff = _array_diff(a, b)
    expected = "1 2/5\n3 4"
    assert diff == expected


def test_coerce_grid_numpy():
    arr = np.array([[1, 2], [3, 4]])
    coerced = _coerce_grid(arr)
    assert coerced == [[1, 2], [3, 4]]
