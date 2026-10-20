import asyncio
from arc_agi.sandbox import run

def test_sandbox_successful_execution():
    async def _test():
        code = "def transform(x):\n    return x + 1"
        input_grid = [[1, 2], [3, 4]]
        ok, result_str = await run(code, input_grid)
        assert ok is True
        assert result_str == "[[2, 3], [4, 5]]"
    asyncio.run(_test())

def test_sandbox_timeout_handling():
    async def _test():
        code = "import time\ndef transform(x):\n    time.sleep(10)\n    return x"
        input_grid = [[1, 2]]
        ok, result_str = await run(code, input_grid, timeout_s=0.2)
        assert ok is False
        assert result_str == "timeout"
    asyncio.run(_test())

def test_sandbox_error_execution():
    async def _test():
        code = "def transform(x):\n    raise ValueError('Custom error')"
        input_grid = [[1]]
        ok, result_str = await run(code, input_grid)
        assert ok is False
        assert "ValueError: Custom error" in result_str
    asyncio.run(_test())
