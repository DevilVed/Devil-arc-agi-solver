import asyncio
import pytest
from arc_agi.sandbox import run

def test_sandbox_success():
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

def test_sandbox_timeout():
    async def _test():
        code = """
import time
def transform(grid):
    time.sleep(5)
    return grid
"""
        input_grid = [[1, 2], [3, 4]]
        ok, result = await run(code, input_grid, timeout_s=0.1)
        assert ok is False
        assert result == "timeout"

    asyncio.run(_test())

def test_sandbox_error_path_sanitization():
    async def _test():
        code = """
def transform(grid):
    raise ValueError("custom error message")
"""
        input_grid = [[1, 2], [3, 4]]
        ok, result = await run(code, input_grid, timeout_s=2.0)
        assert ok is False
        assert "ValueError: custom error message" in result
        # Check that temporary file paths (e.g., /tmp/tmp...) are sanitized
        assert "/tmp/" not in result
        assert "u.py" not in result or "solution.py" in result

    asyncio.run(_test())
