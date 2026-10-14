import pytest
from arc_agi.solve_coding import _eval_on_train_and_test

@pytest.mark.asyncio
async def test_eval_on_train_and_test_concurrent():
    code = """
import numpy as np
def transform(grid: np.ndarray) -> np.ndarray:
    return grid + 1
"""
    train_in = [[[1, 2], [3, 4]] for _ in range(4)]
    train_out = [[[2, 3], [4, 5]] for _ in range(4)]
    test_in = [[[1, 2], [3, 4]] for _ in range(2)]

    train_res, test_res = await _eval_on_train_and_test(code, train_in, train_out, test_in)

    assert len(train_res) == 4
    assert len(test_res) == 2
    assert all(r["success"] for r in train_res)
    assert all(r["output"] == "[[2, 3], [4, 5]]" for r in train_res)
