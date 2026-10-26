import asyncio
import os
from arc_agi.sandbox import run

def test_sandbox_run_success():
    code = """
import numpy as np

def transform(grid: np.ndarray) -> np.ndarray:
    return grid + 1
"""
    ok, res = asyncio.run(run(code, [[1, 2], [3, 4]]))
    assert ok is True
    assert res == "[[2, 3], [4, 5]]"

def test_sandbox_env_isolation():
    # Set a dummy secret environment variable in host process
    os.environ["SECRET_API_KEY"] = "super-secret-key"
    try:
        code = """
import os
import numpy as np

def transform(grid: np.ndarray) -> np.ndarray:
    secret = os.environ.get("SECRET_API_KEY", "")
    if secret:
        raise ValueError("Secret leaked!")
    return grid
"""
        ok, res = asyncio.run(run(code, [[1, 2], [3, 4]]))
        assert ok is True, f"Execution failed: {res}"
    finally:
        os.environ.pop("SECRET_API_KEY", None)
