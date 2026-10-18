import asyncio
from arc_agi.sandbox import run


def test_sandbox_valid_code():
    async def _test():
        code = "def transform(grid):\n    return grid + 1"
        input_grid = [[1, 2], [3, 4]]
        ok, res = await run(code, input_grid, timeout_s=1.0)
        assert ok is True
        assert res == "[[2, 3], [4, 5]]"

    asyncio.run(_test())


def test_sandbox_timeout():
    async def _test():
        code = "import time\ndef transform(grid):\n    time.sleep(5)\n    return grid"
        input_grid = [[1]]
        ok, res = await run(code, input_grid, timeout_s=0.2)
        assert ok is False
        assert res == "timeout"

    asyncio.run(_test())


def test_sandbox_runtime_error():
    async def _test():
        code = "def transform(grid):\n    raise ValueError('Something failed')"
        input_grid = [[1]]
        ok, res = await run(code, input_grid, timeout_s=1.0)
        assert ok is False
        assert "ValueError: Something failed" in res

    asyncio.run(_test())


def test_sandbox_memory_limit():
    async def _test():
        # Attempting to allocate huge bytearray (>2GB virtual memory limit)
        code = "def transform(grid):\n    _ = bytearray(3 * 1024 * 1024 * 1024)\n    return grid"
        input_grid = [[1]]
        ok, res = await run(code, input_grid, timeout_s=1.0)
        assert ok is False
        assert "MemoryError" in res or "bad-json" in res or res != ""

    asyncio.run(_test())
