import pytest
from arc_agi.sandbox import run

@pytest.mark.asyncio
async def test_sandbox_normal_execution():
    code = """
def transform(grid):
    return grid + 1
"""
    input_grid = [[1, 2], [3, 4]]
    ok, res = await run(code, input_grid)
    assert ok is True
    assert res == "[[2, 3], [4, 5]]"

@pytest.mark.asyncio
async def test_sandbox_path_isolation():
    code = """
import os
def transform(grid):
    # PATH should be empty
    path = os.environ.get("PATH", "")
    if path != "":
        raise ValueError(f"PATH is not empty: {path}")
    return grid
"""
    input_grid = [[0]]
    ok, res = await run(code, input_grid)
    assert ok is True

@pytest.mark.asyncio
async def test_sandbox_pythonpath_isolation():
    code = """
import os
def transform(grid):
    pythonpath = os.environ.get("PYTHONPATH", "")
    if pythonpath != "":
        raise ValueError(f"PYTHONPATH is not empty: {pythonpath}")
    return grid
"""
    input_grid = [[0]]
    ok, res = await run(code, input_grid)
    assert ok is True
