import asyncio
from arc_agi.sandbox import run, _build_script


def test_build_script_with_triple_quotes():
    code = '"""\nDocstring\n"""\nimport numpy as np\ndef transform(grid):\n    """Transform function"""\n    return grid'
    script = _build_script(code)
    assert '"""' in script
    assert "transform(np.array(data['input']))" in script


def test_sandbox_run_success():
    async def _test():
        code = "import numpy as np\ndef transform(grid):\n    return grid * 2"
        ok, res = await run(code, [[1, 2], [3, 4]])
        assert ok is True
        assert res == "[[2, 4], [6, 8]]"

    asyncio.run(_test())


def test_sandbox_run_list_return():
    async def _test():
        code = "def transform(grid):\n    return [[1, 1], [1, 1]]"
        ok, res = await run(code, [[0, 0], [0, 0]])
        assert ok is True
        assert res == "[[1, 1], [1, 1]]"

    asyncio.run(_test())


def test_sandbox_run_exception_does_not_leak_stacktrace():
    async def _test():
        code = "def transform(grid):\n    raise ValueError('Secret internal error')"
        ok, res = await run(code, [[1, 2]])
        assert ok is False
        assert res == "ValueError: Secret internal error"
        assert "Traceback" not in res
        assert ".py" not in res

    asyncio.run(_test())
