import asyncio
import os
import pytest
from arc_agi.sandbox import run

def test_sandbox_run_success():
    async def _test():
        code = """
def transform(grid):
    return grid + 1
"""
        input_grid = [[1, 2], [3, 4]]
        ok, result = await run(code, input_grid, timeout_s=2.0)
        assert ok is True
        assert result == "[[2, 3], [4, 5]]"

    asyncio.run(_test())

def test_sandbox_run_timeout_and_process_reap():
    async def _test():
        code = """
import time
def transform(grid):
    while True:
        time.sleep(0.1)
    return grid
"""
        input_grid = [[0]]
        ok, result = await run(code, input_grid, timeout_s=0.2)
        assert ok is False
        assert result == "timeout"

    asyncio.run(_test())

def test_sandbox_environment_isolation():
    async def _test():
        # Verify sensitive host env vars are not exposed in sandbox env
        os.environ["SECRET_TEST_KEY"] = "super_secret_value"
        code = """
import os
def transform(grid):
    val = os.environ.get("SECRET_TEST_KEY", "NOT_FOUND")
    if val == "super_secret_value":
        raise RuntimeError("Secret leaked!")
    return grid
"""
        input_grid = [[1]]
        ok, result = await run(code, input_grid, timeout_s=2.0)
        assert ok is True

    asyncio.run(_test())
