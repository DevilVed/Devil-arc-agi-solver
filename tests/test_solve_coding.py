import asyncio
import pytest
from arc_agi.solve_coding import _eval_on_train_and_test


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
        code, train_in, train_out, test_in, timeout_s=2.0
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
    assert test_res[0]["output"] == "[[0, 2], [4, 6]]"


@pytest.mark.asyncio
async def test_eval_on_train_and_test_mismatch():
    code = """
import numpy as np

def transform(input_grid):
    return input_grid + 1
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[2, 4], [6, 8]]]  # Expected *2, but code does +1 -> [[2, 3], [4, 5]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in, timeout_s=2.0
    )

    assert len(train_res) == 1
    assert train_res[0]["success"] is False
    assert train_res[0]["soft_score"] == 0.25  # 1 element matches (2) out of 4
    assert train_res[0]["error"] is None


@pytest.mark.asyncio
async def test_eval_on_train_and_test_runtime_error():
    code = """
def transform(input_grid):
    raise ValueError("Custom calculation error")
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[1, 2], [3, 4]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in, timeout_s=2.0
    )

    assert len(train_res) == 1
    assert train_res[0]["success"] is False
    assert "ValueError: Custom calculation error" in train_res[0]["error"]


@pytest.mark.asyncio
async def test_eval_on_train_and_test_timeout():
    code = """
import time

def transform(input_grid):
    time.sleep(10)
    return input_grid
"""
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[1, 2], [3, 4]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in, timeout_s=0.5
    )

    assert len(train_res) == 1
    assert train_res[0]["success"] is False
    assert train_res[0]["error"] == "timeout"
