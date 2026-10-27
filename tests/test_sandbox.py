import asyncio
from arc_agi.sandbox import run


def test_run_success():
    ok, result = asyncio.run(run("def transform(x):\n    return x + 1", [[1, 2], [3, 4]]))
    assert ok is True
    assert result == "[[2, 3], [4, 5]]"


def test_run_with_stdout_prints():
    # User prints should redirect to stderr and not corrupt JSON IPC on stdout
    ok, result = asyncio.run(run("def transform(x):\n    print('DEBUG LOG MESSAGE')\n    return x", [[1, 2], [3, 4]]))
    assert ok is True
    assert result == "[[1, 2], [3, 4]]"


def test_run_timeout():
    ok, result = asyncio.run(run("def transform(x):\n    while True:\n        pass", [[1, 2]], timeout_s=0.5))
    assert ok is False
    assert result == "timeout"


def test_run_memory_limit():
    # Attempting massive memory allocation in sandbox script should raise MemoryError
    ok, result = asyncio.run(run("def transform(x):\n    a = [0] * (500 * 1024 * 1024)\n    return x", [[1, 2]]))
    assert ok is False
    assert "MemoryError" in result
