import asyncio
from arc_agi.sandbox import run

def test_sandbox_success_numpy_array():
    async def _test():
        code = """
import numpy as np
def transform(grid: np.ndarray) -> np.ndarray:
    return grid + 1
"""
        input_grid = [[1, 2], [3, 4]]
        ok, res = await run(code, input_grid)
        assert ok is True
        assert res == "[[2, 3], [4, 5]]"

    asyncio.run(_test())


def test_sandbox_success_python_list():
    async def _test():
        code = """
def transform(grid):
    return [[10, 20], [30, 40]]
"""
        input_grid = [[1, 2], [3, 4]]
        ok, res = await run(code, input_grid)
        assert ok is True
        assert res == "[[10, 20], [30, 40]]"

    asyncio.run(_test())


def test_sandbox_non_utf8_output():
    async def _test():
        code = """
import sys
def transform(grid):
    sys.stderr.buffer.write(b"\\xff\\xfe\\xfa Error occurred")
    sys.stderr.flush()
    raise ValueError("Failed")
"""
        input_grid = [[1]]
        ok, res = await run(code, input_grid)
        assert ok is False
        assert "Error occurred" in res or "Failed" in res

    asyncio.run(_test())


def test_sandbox_timeout_cleanup():
    async def _test():
        code = """
import time
def transform(grid):
    time.sleep(10)
    return grid
"""
        input_grid = [[1]]
        ok, res = await run(code, input_grid, timeout_s=0.2)
        assert ok is False
        assert res == "timeout"

    asyncio.run(_test())
