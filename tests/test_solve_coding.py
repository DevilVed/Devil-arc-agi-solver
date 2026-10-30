import asyncio
import time
import pytest
from arc_agi.solve_coding import _eval_on_train_and_test

valid_code = """
def transform(grid):
    return grid * 2
"""

error_code = """
def transform(grid):
    raise ValueError("custom error")
"""

timeout_code = """
import time
def transform(grid):
    time.sleep(2)
    return grid
"""

bad_shape_code = """
def transform(grid):
    return grid[0:1, 0:1]
"""


@pytest.mark.asyncio
async def test_eval_on_train_and_test_success():
    train_in = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    train_out = [[[2, 4], [6, 8]], [[10, 12], [14, 16]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        valid_code, train_in, train_out, test_in, timeout_s=1.5
    )

    assert len(train_res) == 2
    assert all(r["success"] for r in train_res)
    assert all(r["soft_score"] == 1.0 for r in train_res)
    assert all(r["error"] is None for r in train_res)

    assert len(test_res) == 1
    assert not test_res[0]["success"]
    assert test_res[0]["error"] is None
    assert test_res[0]["output"] == "[[0, 2], [4, 6]]"


@pytest.mark.asyncio
async def test_eval_on_train_and_test_error_handling():
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[2, 4], [6, 8]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        error_code, train_in, train_out, test_in, timeout_s=1.5
    )

    assert len(train_res) == 1
    assert not train_res[0]["success"]
    assert train_res[0]["soft_score"] == 0.0
    assert "ValueError: custom error" in train_res[0]["error"]

    assert len(test_res) == 1
    assert not test_res[0]["success"]
    assert "ValueError: custom error" in test_res[0]["error"]


@pytest.mark.asyncio
async def test_eval_on_train_and_test_shape_mismatch():
    train_in = [[[1, 2], [3, 4]]]
    train_out = [[[2, 4], [6, 8]]]
    test_in = [[[0, 1], [2, 3]]]

    train_res, test_res = await _eval_on_train_and_test(
        bad_shape_code, train_in, train_out, test_in, timeout_s=1.5
    )

    assert len(train_res) == 1
    assert not train_res[0]["success"]
    assert train_res[0]["soft_score"] == 0.0
    assert train_res[0]["error"] is None


@pytest.mark.asyncio
async def test_eval_on_train_and_test_timeout():
    train_in = [[[1]]]
    train_out = [[[1]]]
    test_in = [[[1]]]

    train_res, test_res = await _eval_on_train_and_test(
        timeout_code, train_in, train_out, test_in, timeout_s=0.3
    )

    assert len(train_res) == 1
    assert not train_res[0]["success"]
    assert train_res[0]["error"] == "timeout"

    assert len(test_res) == 1
    assert not test_res[0]["success"]
    assert test_res[0]["error"] == "timeout"


@pytest.mark.asyncio
async def test_eval_concurrency_speedup():
    train_in = [[[1]], [[2]], [[3]], [[4]]]
    train_out = [[[2]], [[4]], [[6]], [[8]]]
    test_in = [[[5]], [[6]]]

    t0 = time.perf_counter()
    train_res, test_res = await _eval_on_train_and_test(
        valid_code, train_in, train_out, test_in, timeout_s=1.5
    )
    elapsed = time.perf_counter() - t0

    assert len(train_res) == 4
    assert len(test_res) == 2
    # 6 subprocess invocations sequentially take ~0.25-0.35s in this environment.
    # Concurrently it should easily take under 0.25s.
    assert elapsed < 1.0
