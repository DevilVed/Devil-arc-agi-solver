import asyncio
import os
import pytest
from arc_agi.sandbox import run

def test_sandbox_env_isolation(monkeypatch):
    # Set sensitive environment variables in main process
    monkeypatch.setenv("OPENAI_API_KEY", "secret_key_12345")
    monkeypatch.setenv("CUSTOM_SECRET", "super_secret_value")

    # User code attempting to access process environment variables
    code = """
import os
def transform(grid):
    # Check if sensitive env vars are visible
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    custom_secret = os.environ.get("CUSTOM_SECRET", "")
    if openai_key or custom_secret:
        raise ValueError(f"Leaked env vars: OPENAI_API_KEY={openai_key}, CUSTOM_SECRET={custom_secret}")
    return grid
"""
    ok, res = asyncio.run(run(code, [[1, 2], [3, 4]]))
    assert ok is True, f"Execution failed: {res}"
