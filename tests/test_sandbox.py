import pytest
import asyncio
from arc_agi.sandbox import run


@pytest.mark.asyncio
async def test_sandbox_valid_code():
    code = """
def transform(grid):
    return grid * 2
"""
    ok, res = await run(code, [[1, 2], [3, 4]])
    assert ok is True
    assert res == "[[2, 4], [6, 8]]"


@pytest.mark.asyncio
async def test_sandbox_returns_list():
    code = """
def transform(grid):
    return [[1, 2], [3, 4]]
"""
    ok, res = await run(code, [[0]])
    assert ok is True
    assert res == "[[1, 2], [3, 4]]"


@pytest.mark.asyncio
async def test_sandbox_non_utf8_stderr():
    code = """
import sys
def transform(grid):
    sys.stderr.buffer.write(bytes([0x80, 0x81, 0xfe, 0xff]))
    sys.stderr.flush()
    raise ValueError("Error with invalid utf-8 stderr")
"""
    ok, res = await run(code, [[1]])
    assert ok is False
    assert "ValueError: Error with invalid utf-8 stderr" in res


@pytest.mark.asyncio
async def test_sandbox_timeout():
    code = """
import time
def transform(grid):
    time.sleep(10)
    return grid
"""
    ok, res = await run(code, [[1]], timeout_s=0.2)
    assert ok is False
    assert res == "timeout"
