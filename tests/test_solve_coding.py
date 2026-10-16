import asyncio
import numpy as np
import pytest

from arc_agi.solve_coding import _eval_on_train_and_test, _example_to_diagram


def test_example_to_diagram():
    example = [[1, 2], [3, 4]]
    expected = "1 2\n3 4"
    assert _example_to_diagram(example) == expected

    example_np = np.array([[0, 5], [9, 8]])
    expected_np = "0 5\n9 8"
    assert _example_to_diagram(example_np) == expected_np


@pytest.mark.asyncio
async def test_eval_on_train_and_test_success():
    code = """
def transform(input_grid):
    return input_grid + 1
"""
    train_in = [[[1, 2], [3, 4]], [[0, 0], [1, 1]]]
    train_out = [[[2, 3], [4, 5]], [[1, 1], [2, 2]]]
    test_in = [[[5, 6], [7, 8]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 2
    assert all(r["success"] for r in train_res)
    assert train_res[0]["soft_score"] == 1.0

    assert len(test_res) == 1
    assert not test_res[0]["success"]
    assert test_res[0]["output"] == "[[6, 7], [8, 9]]"


@pytest.mark.asyncio
async def test_eval_on_train_and_test_failure():
    code = """
def transform(input_grid):
    return input_grid * 0
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[2, 3], [4, 5]]]
    test_in = [[[5, 6], [7, 8]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 1
    assert not train_res[0]["success"]
    assert train_res[0]["soft_score"] == 0.0
