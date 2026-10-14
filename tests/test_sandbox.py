import json
import pytest
from arc_agi.sandbox import run

@pytest.mark.anyio
async def test_sandbox_run_numpy_array():
    code = """
import numpy as np

def transform(grid: np.ndarray) -> np.ndarray:
    return grid + 1
"""
    input_grid = [[1, 2], [3, 4]]
    ok, res_str = await run(code, input_grid)
    assert ok is True
    assert json.loads(res_str) == [[2, 3], [4, 5]]

@pytest.mark.anyio
async def test_sandbox_run_python_list():
    code = """
def transform(grid):
    return [[1, 0], [0, 1]]
"""
    input_grid = [[0, 0], [0, 0]]
    ok, res_str = await run(code, input_grid)
    assert ok is True
    assert json.loads(res_str) == [[1, 0], [0, 1]]

@pytest.mark.anyio
async def test_sandbox_run_exception():
    code = """
def transform(grid):
    raise ValueError("Test error")
"""
    input_grid = [[1, 2]]
    ok, err_str = await run(code, input_grid)
    assert ok is False
    assert "ValueError: Test error" in err_str

@pytest.mark.anyio
async def test_sandbox_run_timeout():
    code = """
import time
def transform(grid):
    time.sleep(10)
    return grid
"""
    input_grid = [[1]]
    ok, err_str = await run(code, input_grid, timeout_s=0.2)
    assert ok is False
    assert err_str == "timeout"
