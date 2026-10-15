import pytest
from arc_agi import sandbox

@pytest.mark.asyncio
async def test_sandbox_basic_execution():
    code = """
def transform(x):
    return x + 1
"""
    ok, res = await sandbox.run(code, [[1, 2], [3, 4]])
    assert ok is True
    assert res == "[[2, 3], [4, 5]]"

@pytest.mark.asyncio
async def test_sandbox_env_isolation(monkeypatch):
    monkeypatch.setenv("SECRET_API_KEY", "super_secret_value_123")
    code = """
def transform(x):
    import os
    secret = os.environ.get("SECRET_API_KEY", "")
    if secret:
        raise ValueError("Secret leaked: " + secret)
    return x
"""
    ok, res = await sandbox.run(code, [[1, 2], [3, 4]])
    assert ok is True, f"Expected sandbox execution to succeed without leaking env, got: {res}"
