import asyncio
import time
import pytest
from arc_agi.solve_coding import _eval_on_train_and_test

pytestmark = pytest.mark.asyncio

async def test_eval_on_train_and_test_correctness():
    code = """
import numpy as np
def transform(input_grid):
    return input_grid + 1
"""
    train_in = [[[1, 2], [3, 4]], [[0, 0], [1, 1]]]
    train_out = [[[2, 3], [4, 5]], [[1, 1], [2, 2]]]
    test_in = [[[5, 5], [5, 5]]]

    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )

    assert len(train_res) == 2
    assert len(test_res) == 1
    assert train_res[0]["success"] is True
    assert train_res[0]["soft_score"] == 1.0
    assert train_res[1]["success"] is True
    assert train_res[1]["soft_score"] == 1.0
    assert test_res[0]["output"] == "[[6, 6], [6, 6]]"


async def test_eval_on_train_and_test_concurrency():
    # Code that sleeps 0.2 sec per run
    code = """
import numpy as np
import time
def transform(input_grid):
    time.sleep(0.2)
    return input_grid
"""
    train_in = [[[1]], [[2]], [[3]]]
    train_out = [[[1]], [[2]], [[3]]]
    test_in = [[[4]], [[5]]]

    t0 = time.perf_counter()
    train_res, test_res = await _eval_on_train_and_test(
        code, train_in, train_out, test_in
    )
    t1 = time.perf_counter()

    assert len(train_res) == 3
    assert len(test_res) == 2
    # 5 runs * 0.2s sequentially would take >= 1.0s
    # Concurrently, total time should be substantially less than 0.8s
    total_time = t1 - t0
    assert total_time < 0.8, f"Expected concurrent execution < 0.8s (sequential would be ~1.0s+), got {total_time:.2f}s"
